import logging
import serial.tools.list_ports as com
from utils import log


def get_comports():
    """
    Detect the com port from current system. Please make sure your device has connected your system.
    :return:
    """
    ports = com.comports()
    for port in ports:
        if "USB Serial Port" in port.description:
            log.output("Got %s port from current system." % port.name, level=logging.DEBUG)
            return port.name

def get_all_comports():
    """
    Detect the com port from current system. Please make sure your device has connected your system.
    :return:
    """
    com_ports = []
    ports = com.comports()
    for port in ports:
        if "USB Serial Port" in port.description:
            log.output("Got %s port from current system." % port.name, level=logging.DEBUG)
            com_ports.append(port.name)
    return com_ports


if __name__ == '__main__':
    print(get_all_comports())