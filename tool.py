import logging
import sys
import time
import serial

from utils.log import output

#   Exit code:
#       10: com port not ready
#       00: exit normally


class NonContentError(Exception):...


class SerialServer:

    CMD_1 = "F2"
    CMD_2 = "F0"
    CMD_3 = "31"
    CMD_4 = "00"
    CMD_5 = "05"
    CMD_6 = "00"
    CMD_7 = "00"
    CMD_8 = "00"
    CMD_9 = "00"

    AUTH = "F0 F2 A5 01"
    UNLOCK_ALL = "F2 F0 31 00 05 00 01"
    SHUTDOWN = "F2 F0 31 00 05 00 03"
    READ_SIM_ID = "F0 F2 A1 01 00 A2"
    BINDING = "F0 F2 A0 01 00 A1"
    BINDING_COMPLETE = "F0 F2 D7 01 00 D8"
    MOTOR_DRIVE_BACK = "F2 F0 31 00 05 00 04"
    OPEN_UNLOCK = "F0 F2 A6 01 07 A7"
    LOCK_NUMBER = "F0 F2 A8 01 00 A7"
    QUERY_S1_STATUS = "F0 F2 B1 01 00 B2"
    UPDATE_S1_S2_STATUS = "F0 F2 B3 01 00 B4"
    QUERY_S2_STATUS = "F0 F2 B2 01 00 B3"
    MOTOR_FORWARD = "F0 F2 D4 01 00 D4"
    MOTOR_BACK = "F0 F2 D6 01 00 D6"
    MOTOR_STOP = "F0 F2 D2 01 00 D2"

    def __init__(self, **kwargs):
        """
        com: serial com port.
        baud: serial baud, default is 115200
        """
        self.com = kwargs.get("com", "COM6")
        self.baud = kwargs.get("baud", 115200)
        self.output_to = kwargs.get("output_to", None)
        self.serial = serial.Serial(self.com, self.baud, timeout=0.5)
        self.cmd_base = [self.CMD_1, self.CMD_2, self.CMD_3, self.CMD_4, self.CMD_5, self.CMD_6, self.CMD_7] if not kwargs.get("auto", False) else []

    def is_open(self):
        return self.serial.is_open

    def checksum(self, data, from_=2):
        """
        从cmd_base的from_位置开始计算checksum
        :param data: 计算的数据，该参数为list type。
        :param from_: 从第几个开始计算
        :return:
        """
        sum = 0
        for d in data[:]:
            data_ = int(d, base=16)
            sum += data_

        last_bit = hex(sum)[2:] if len(hex(sum)) <= 4 else hex(sum)[-2:]   # 取最后一个bit位
        output("Ready to compute: {}, The result is : {}".format(data[from_:], last_bit), level=logging.INFO, output_to=self.output_to)

        return last_bit

    def convert(self, data: str, add_=True):
        """
        Convert data to hex.
        :param data:
        :param add_: 该参数控制是否将转换完毕的结果自动增加到cmd_base里面
        :return:
        """
        list_data = list(data)
        start_ = 2
        while True:
            if start_ > len(list_data):
                break
            elif start_ == len(list_data):
                break
            else:
                list_data.insert(start_, " ")
                start_ = start_ + 2 + 1

        if not add_:
            output("Convert {} to {}".format(data, "".join(list_data).split(" ")), level=logging.INFO, output_to=self.output_to)
            return "".join(list_data).split(" ")
        else:
            self.cmd_base += "".join(list_data).split(" ")

    def recv(self, loop=10):
        while True:
            data = self.serial.read(1024).hex()
            output("Receive: {}".format(self.convert(data, add_=False)), level=logging.INFO, output_to=self.output_to)
            if data == '':
                if not loop:
                    raise NonContentError("Did not get content from the current com port!")
                loop -= 1   # when circulate <loop> times, It still do not get content. exit.
                continue
            else:
                break
        return " ".join(self.convert(data.upper(), add_=False)) # 转换成标准格式： F2 F0 31 00 00 00 00 49 9D 17

    def send(self, timeout=0):
        send_data = bytearray(int(i, 16) for i in self.cmd_base) # convert string to hex
        output(send_data.hex(), level=logging.INFO, output_to=self.output_to)
        if (self.serial.isOpen()):
            output("Send: {}".format(send_data.hex()), level=logging.INFO, output_to=self.output_to)
            self.serial.write(send_data)
        time.sleep(timeout)

    def Do(self, command, return_=False):
        self.cmd_base = command.split(" ")
        self.send()
        if return_:
            return self.recv().split(" ")

    def close(self):
        self.serial.close()
        output("Close com port success!", level=logging.INFO, output_to=self.output_to)


if __name__ == '__main__':
    s = SerialServer(com=None)    #   只需要传递com参数， baud 默认是115200
    # s.convert("499d", add_=True)    #    SN 转换格式
    # s.cmd_base.append(s.checksum(s.cmd_base))  #   把计算的checksum 加到 cmdbase
    # s.send()
    # content = s.recv()
    # output(content, level=logging.INFO)
    # s.close()
    # s.AUTH = (s.AUTH + " 00").split(" ")[2:]
    # print(s.checksum(s.AUTH))
    lock_number = "5"
    lock_number = str(hex(int(lock_number)))[2:].rjust(2, '0').upper()
    s.AUTH = s.AUTH + f" {lock_number}"
    s.AUTH = s.AUTH + " {}".format(s.checksum(s.AUTH.split(" ")[2:]).upper())
    print(s.AUTH)