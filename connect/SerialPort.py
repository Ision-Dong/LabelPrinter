import binascii
import logging as logger
from serial import SerialException, SerialTimeoutException
from serial import Serial


class SerialPort:
    def __init__(self, portName=None, baudrate=115200, timeout=0, writeTimeout=0):
        self.portName = portName
        self.__serialConfig = {'port': portName,
                               'baudrate': baudrate,
                               'bytesize': 8,
                               'timeout': timeout,
                               'write_timeout': writeTimeout,
                               }
        self._serial = None
        self.open()

    def is_opened(self):
        return self._serial.is_open

    def open(self):
        '''
        create serial port object and open the it.
        :exception: DeviceError: WindowsError Access is denied or couldn't device.
        '''
        try:
            self._serial = Serial(**self.__serialConfig)
        except SerialException as ex:
            logger.error(ex)
            logger.warning('try to open again')
            self._serial = Serial(**self.__serialConfig)

    def __write(self, data):
        self._serial.reset_output_buffer()
        self._serial.reset_input_buffer()
        # length = self._serial.write(binascii.a2b_hex(data))
        length = self._serial.write(bytes(data))
        return length

    def send(self, data):
        length = 0
        if self._serial is None:
            self.open()

        try:
            logger.debug('serial write:{}'.format(data))
            length = self.__write(data)
            logger.debug('write done:{}'.format(length))
        except SerialTimeoutException as ex:
            logger.error(ex)
            self.close()
            logger.warning('re-open')
            self.open()
            logger.warning('re-send {0}'.format(data))
            try:
                length = self.__write(data)
                logger.debug('re-write done:{}'.format(length))
            except SerialTimeoutException as ex:
                logger.error(ex)
                return False

        return True if length == len(data) / 2 else False

    def receive(self, size=None):
        if self._serial is None:
            self.open()

        try:
            logger.debug('serial try receive:{}'.format(size))
            if size is None:
                data = binascii.b2a_hex(self._serial.read())
            else:
                data = binascii.b2a_hex(self._serial.read(int(size)))

            import six
            if six.PY2:
                data = data
            else:
                data = data.decode()

            logger.debug('receive done:{}'.format(data))
            return data
        except SerialException as ex:
            logger.error(ex)
            self.close()
            logger.warning('re-open')
            self.open()
            return ''

    def close(self):
        '''
        close serial port
        '''
        if self._serial:
            self._serial.close()
            self._serial = None