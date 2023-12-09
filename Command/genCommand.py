import logging
import sys
import threading
import time

import serial

from config.commands import *
from connect.SerialPort import SerialPort
from connect.connector import SerialConnector
from utils.log import output
from utils.utils import convert_to_hex, encode_to_gbk

class GreatThanMaxValueError(Exception):
    pass

class Command:

    const = "18 00 00 00 "

    def __init__(self, **kwargs):
        self.connect = SerialPort(portName=kwargs.get("com_port", None))
        self.order = ""
        self.x_lenght = 384
        self.y_lenght = 320
        self.args = kwargs
        self.text_postfix = " 00"
        self.enter = "\n"
        # by default: x is 20, y is 55.
        self.text_x = self.convert_to_hex(kwargs.get("text_x", 20))
        self.text_y = self.convert_to_hex(kwargs.get("text_y", 55))
        self.next_line = self.convert_to_hex(30)
        self.call_text = 0
        # by default: x is 190, y is 150.
        if self.args.get("qr_x", 0) > 325 or self.args.get("qr_y", 0) > 390:
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
        while True:
            status = self.connect.receive(1024)
            if status == "fc4f4b":  # fc4f4b   Print successful
                output(message="Print successful.", level=logging.INFO)
                return True
            elif status == "fc6e6f": # fc6e6f   Print failure.
                output(message="Print failure.", level=logging.ERROR)
                return False
            time.sleep(0.5)


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

    command = convert_to_hex(command)
    c.send(command)
    c.close()
    t.join()
