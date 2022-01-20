"""Initialize the Python logging system"""
import logging


class LoggerConfig():
    """
    Useful log message formats:
    LOGGING_FORMAT = '%(asctime)-15s: [%(name)s] %(message)s'
    LOGGING_FORMAT = '[%(name)s] %(message)s'
    LOGGING_FORMAT = '%(message)s'
    """

    def __init__(self):
        """Initialize log config with default level info and a short log
        message (contains just the message and not meta information)
        """
        # Default log level: info
        # logging.basicConfig(level=logging.INFO,
        #                     format='%(message)s')
        self.__format_plain = '%(message)s'
        self.__format_debug = '%(asctime)-15s: [%(name)s] %(message)s'
        self.__handler = logging.StreamHandler()
        logging.getLogger().addHandler(self.__handler)
        self.info()

    def debug(self):
        """Switch to debug log level. Change level-of-detail for log message.
        (add meta information)
        """
        logging.getLogger().setLevel(logging.DEBUG)
        self.__handler.setFormatter(logging.Formatter(self.__format_debug))

    def info(self):
        """Switch to info log level. Change level-of-detail for log message.
        (just the log message)
        """
        logging.getLogger().setLevel(logging.INFO)
        self.__handler.setFormatter(logging.Formatter(self.__format_plain))

    def warning(self):
        """Switch to info log level. Change level-of-detail for log message.
        (just the log message)
        """
        logging.getLogger().setLevel(logging.WARNING)
        self.__handler.setFormatter(logging.Formatter(self.__format_plain))