import sys
import threading
import time

import serial

serial_lock = threading.Lock()
port_lock = threading.Lock()
serial_content = ""


class SerialConnector(threading.Thread):
    def __init__(self, port):
        super(SerialConnector, self).__init__()
        self.port_num = port
        self.output_to = None
        self.__maxsize = 1024 * 10
        self.__serial_log = ""
        self.serial_log_path = None
        self.serial_fp = None
        self.__port = None
        self.open()

    def log_fp(self):
        fp = open(self.serial_log_path, "w")
        return fp

    def __log_close(self):
        self.serial_fp.close()

    def open(self):
        global serial_content
        try:
            if self.__port:
                self.__close()
            self.__port = serial.Serial(self.port_num, 115200, timeout=5)
            serial_content += "\nOpen connect {} port successful".format(self.port_num)
            return True
        except Exception as ex:
            serial_content += "\n" + str(ex)
            self.__port = None
            return False

    def __close(self):
        if self.__port:
            self.__port.close()

    def run(self):
        global serial_lock
        global serial_content
        show_serial_error = True
        self.__is_stop = False
        while not self.__is_stop:
            try:
                if serial_lock:
                    serial_lock.acquire()
                if self.__port:
                    date_length = self.__port.in_waiting
                    if date_length > 0:
                        serial_info = self.__port.read(date_length).decode()
                        serial_content += serial_info
                        if self.serial_fp:
                            self.serial_fp.write(serial_info)
                else:
                    time.sleep(5)
                    if not self.open():
                        self.__is_stop = True
            except Exception as ex:
                if show_serial_error:
                    serial_content += "\n" + str(ex)
            finally:
                if serial_lock:
                    serial_lock.release()
        if self.__port:
            self.__close()
        if self.serial_fp:
            self.serial_fp.flush()
            self.__log_close()

    def stop(self):
        if not self.__is_stop:
            global serial_content
            serial_content += "\nClose connect {} port".format(self.port_num)
            self.__is_stop = True
            self.join(1)
            if self.is_alive():
                self.stop()


if __name__ == '__main__':
    s = serial.Serial("COM11", 115200, timeout=5)
    while True:
        print(s.read(1024).decode())
        time.sleep(2)