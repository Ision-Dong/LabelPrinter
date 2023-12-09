import binascii
import time

from pyqt5_plugins.examplebutton import QtWidgets
from serial import Serial

from connect.SerialPort import SerialPort
from utils.log import output


def sender(data, com=None, baud=None) -> int:
    config = {
        'port': com,
        'baudrate': baud,
        'bytesize': 8,
        'timeout': 10,
        'write_timeout': 20,
    }
    serial = Serial(**config)
    num = serial.write(bytes(data.encode()))
    serial.close()
    return num

def reader(com=None, baud=None, output_to: QtWidgets.QRadioButton=None) -> None:
    try:
        serial = SerialPort(portName=com, baudrate=baud)
    except Exception as ex:
        output(message="Run into Error: {}".format(ex))
        return

    while True:
        s = serial.receive(1024)
        if s != "":
            rec = binascii.unhexlify(s).decode()
            if output_to is not None:
                output_to.setText(rec)
            return
        time.sleep(1)


if __name__ == '__main__':
    reader(com="COM13", baud=115200)
