import datetime
import logging
import os
import logging as logger
import logging.config as log

from PyQt5.QtWidgets import QApplication

CURRENT_PATH = os.getcwd()

log.fileConfig("{}\\config\\logging.conf".format(CURRENT_PATH))
log = logger.getLogger(name=os.path.split(__file__)[1])


def output(message=None, level: logging=logging.INFO, output_to=None):

    format = str(datetime.datetime.now()) + " - " + __file__.split("\\")[-1] + " - {} - ".format("INFO") + message

    if output_to is not None:
        QApplication.processEvents()
        output_to.append(format)
        return

    if level is None:
        log.error(message)
    elif level == logging.DEBUG:
        log.debug(message)
    elif level == logging.INFO:
        log.info(message)
    elif level == logging.ERROR:
        log.error(message)
    elif level == logging.WARNING:
        log.warning(message)
    elif level == logging.FATAL or level == logging.CRITICAL:
        log.critical(message)

