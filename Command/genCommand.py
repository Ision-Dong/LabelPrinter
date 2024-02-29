import logging
import threading
import time

from config.commands import *
from connect.SerialPort import SerialPort
from utils.log import output
from utils.utils import convert_to_hex, encode_to_gbk


class GreatThanMaxValueError(Exception):
    pass


class Command:

    """
    定义label打印机的各个功能接口，
        # testPage  打印测试页
        # reset    重置打印机
        # paper_in  打印机进纸
        # gen_text_command 生成文本行打印机指令
        # set_qr_location 设置二维码的大小和位置
        # gen_QR_command 生成二维码打印指令
        # gen_command 生成完整的打印指令
        # ...

    详细信息可以参考: doc/developerDOC.pdf， 打印机使用文档
    打印指令定义在: config/commands.py中
    打印指令的生成以行为单位， 调用gen_text_command/gen_QR_command一次，生成一行对应的打印指令
    所有指令生成完后在发送前必须转换成16进制，才能发送给串口。
    代码样例在main 中，可以参考
    """

    const = "18 00 00 00 " # 打印指令前缀

    def __init__(self, **kwargs):
        self.connect = SerialPort(portName=kwargs.get("com_port", None))
        self.order = ""
        self.x_lenght = 384 # 384 这个参数是从打印机使用文档中预估出来的
        self.y_lenght = 320  # 320 这个参数是从打印机使用文档中预估出来的
        self.args = kwargs
        self.text_postfix = " 00"  # 预示打印指令结束
        self.enter = "\n"
        # by default: x is 20, y is 55.
        self.text_x = self.convert_to_hex(kwargs.get("text_x", 20))
        self.text_y = self.convert_to_hex(kwargs.get("text_y", 55))
        self.next_line = self.convert_to_hex(30)
        self.call_text = 0
        # by default: x is 190, y is 150.
        if self.args.get("qr_x", 0) > 325 or self.args.get("qr_y", 0) > 390:  # 325 390 这两个参数是从打印机使用文档中推理出来的
            raise GreatThanMaxValueError("QR x or QR y are great than the max value set.")
        self.qr_x = None
        self.qr_y = None

    def testPage(self):
        """
        Print the test page.
        :return:
        """
        command = convert_to_hex(test_page)
        self.send(command)

    def reset(self):
        command = convert_to_hex(reset_device)
        self.send(command)

    def paper_in(self):
        command = convert_to_hex(paper_in)
        self.send(command)

    def gen_text_command(self, content):
        """
        ex:
            1A 54 00 00 00 88 00 C0 E0 B1 F0 A3 BA 00
        :param content: content printed.
        :return: return text command.
        """
        if self.call_text >= 1:
            self.text_y = self.convert_to_hex(self.convert_to_dec(self.text_y) + self.convert_to_dec(self.next_line))

        if type(content) == str:
            content = encode_to_gbk(content)
            text_add_x = text + str(self.text_x) + " 00 "
            text_add_y = text_add_x + str(self.text_y) + " 00 "
            text_command = text_add_y + self.const + content[0] + self.text_postfix
            self.call_text += 1
            return text_command
        elif type(content) == list:
            pass

    def set_qr_location(self):
        self.qr_x = self.convert_to_hex(self.args.get("qr_x", 190))
        self.qr_y = self.convert_to_hex(self.args.get("qr_y", 150))
        if len(self.qr_x) > 2:
            command = print_qr.format(self.qr_x[::-1][:2][::-1] + " 0" + self.qr_x[::-1][2:], self.qr_y)
            return command
        else:
            command = print_qr.format(self.qr_x.upper() + " 00", self.qr_y, self.args.get("qr_size", "04"))
            return command

    def gen_QR_command(self, content):
        """
        1A 31 00 03 03 D8 00 38 00 03 00 D0 ED B2 FD CA D0 D6 D0 D0 C4 D2 BD D4 BA 0D 0A BF C6 CA D2 A3 BA BF BA    \
        B4 E5 C9 A8 C2 EB 0D 0A C0 E0 B1 F0 A3 BA C6 E4 CB FB 0D 0A D6 D8 C1 BF A3 BA 31 33 2E 39 6B 67 0D 0A CA B1 BC \
        E4 A3 BA 32 30 32 31 2D 31 30 2D 31 35 20 20 20 20 30 36 3A 30 33 3A 30 31 00
        用set_qr_location 和 gen_QR_command 拼接出如上的指令行
        :param content: 扫描二维码后显示的内容
        :return:
        """
        command = self.set_qr_location()
        content = encode_to_gbk(content)[0]
        command += content + self.text_postfix
        return command

    @staticmethod
    def convert_to_hex(position):
        """
        For handling the position to convert to hex.
        :param position:
        :return:
        """
        position = str(hex(position)).replace("0x", "")
        return position

    @staticmethod
    def convert_to_dec(position):
        position = int("0x" + str(position), 16)
        return position

    @staticmethod
    def __start_page():
        return start_page

    @staticmethod
    def __end_page():
        return end_page

    @staticmethod
    def __start_print():
        return printer

    @staticmethod
    def __cut_paper():
        return cut_paper

    @staticmethod
    def __init_command():
        return init_command

    def __str__(self):
        return border

    def gen_command(self, *args):
        """
        以如下的方式传递需要的内容并生成打印指令
        command = c.gen_command(
            (c.gen_text_command, content), # 生成文本打印指令
            (c.gen_text_command, content), # 生成文本打印指令
            (c.gen_text_command, content), # 生成文本打印指令
            (c.gen_text_command, content), # 生成文本打印指令
            (c.gen_text_command, content), # 生成文本打印指令
            (c.gen_QR_command, content), # 生成二维码打印指令
        )

        # 打印指令样式请参考: template/temp.py
        # 最终生成的指令将是这个样子的
        :param args: all operations
        :return: the text command
        """
        whole_command = ""
        whole_command += self.__init_command() + self.enter
        whole_command += self.__start_page() + self.enter
        for f, arg in args:
            whole_command += f(arg) + self.enter

        whole_command += self.__end_page() + self.enter
        whole_command += self.__start_print() + self.enter
        whole_command += self.__cut_paper() + self.enter

        return whole_command

    def send(self, c):
        self.connect.send(c)

    def close(self):
        self.connect.close()
        del self

    def get_print_status(self):
        """
        times: 循环10次去获取串口数据， 10次没拿到打印机状态返回false。
        :return:
        """
        times = 10
        while times:
            status = self.connect.receive(1024)
            if times == 0:
                status = "fc6e6f"
            if status == "fc4f4b":  # fc4f4b   Print successful
                output(message="Print successful.", level=logging.INFO)
                return True
            elif status == "fc6e6f": # fc6e6f   Print failure.
                output(message="Print failure.", level=logging.ERROR)
                return False
            time.sleep(0.5)
            times -= 1


if __name__ == '__main__':
    c = Command(com_port="COM11")

    t = threading.Thread(target=c.get_print_status)
    t.setDaemon(True)
    t.start()

    s1 = "S/N: 1234567890abcd1234567890"
    s2 = "M/N: 1234567890abcd1234567890"
    model = "MODEL: DDDDDDDD"
    input = "INPUT: DC5V/1A"
    html = "URL: WWW.MOCOCHI.COM"
    date = "DATE: 2023/06/23"
    command = c.gen_command(
        (c.gen_text_command, s1),
        (c.gen_text_command, s2),
        (c.gen_text_command, html),
        (c.gen_text_command, model),
        (c.gen_text_command, input),
        (c.gen_QR_command, s1),
    )
    # 生成的指令需要转换成16进制后，才能发送给对应的串口， 所以必须调用convert_to_hex来做转换
    # 该方法未作错误处理，确保传入的数据是在16进制的范围内
    command = convert_to_hex(command)
    c.send(command)
    c.close()
    t.join()
