"""
Custom logging utilities for enhanced log messages.

This module provides:
- A custom log formatter (`ClassNameFormatter`) that injects the caller's class
    name into log records.
- A file-based log handler (`Log`) that writes formatted log messages to a file,
    with options to include process ID and clear previous logs.
- A helper function (`setup_custom_logger`) to easily configure a logger with
    these custom features.

Usage:
    logger = setup_custom_logger("log_my_module")
    logger.info("This is a log message.")

The log output includes timestamps, logger name, log level, module, line number,
class name, function name, and the message.
"""

import inspect
import logging
import os


class ClassNameFormatter(logging.Formatter):
    """
    Custom formatter that adds the class name to the log message.
    """

    def format(self, record: logging.LogRecord):
        stack = inspect.stack()
        caller_frame = stack[8]
        scope = caller_frame[0]

        class_name = ""

        if "self" in caller_frame[0].f_locals.keys():
            class_name: str = scope.f_locals["self"].__class__.__name__
            class_name.strip().strip('"')
            class_name = f"{class_name}."

        record.class_name = class_name

        return super().format(record)


class Log(logging.Handler):
    """
    Custom logger that writes to a file.
    """

    def __init__(
        self,
        log_file: str = "log.log",
        pid: bool = False,
        clear: bool = True,
        level: int = logging.DEBUG,
    ):
        super().__init__(level)
        format_str = (
            "%(asctime)s %(name)s %(levelname)-8s "
            "%(module)s[%(lineno)d] >> %(class_name)s%(funcName)s(): "
            "%(message)s"
        )

        if pid:
            format_str = (
                "%(asctime)s %(name)s P%(process)-7d %(levelname)-8s "
                "%(module)s[%(lineno)d] >> %(class_name)s%(funcName)s(): "
                "%(message)s"
            )

        self.log_file = log_file
        self.setFormatter(ClassNameFormatter(format_str))

        if os.path.exists(self.log_file) and clear:
            os.remove(self.log_file)

    def emit(self, record):
        try:
            msg = self.format(record)

            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{msg}\n")

        except SyntaxError:
            self.handleError(record)
        except KeyError:
            self.handleError(record)


def setup_custom_logger(name, pid=False, clear=True):
    """
    Setup the logger for the given name.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    custom_handler = Log(name + ".log", pid, clear)
    logger.addHandler(custom_handler)

    return logger
