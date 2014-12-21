import logging
import logging.handlers
import argparse
from .base_script import BaseScript


class Script(BaseScript):
    def __init__(self, name, description, log_output='console',
                 log_format='%(message)s', log_dateformat='%b %d %H:%M:%S'):
        if log_output == 'console':
            log_handler = logging.StreamHandler()
        elif log_output == 'syslog':
            log_handler = logging.handlers.SysLogHandler(address='/dev/log',
                                                         facility=logging.handlers.SysLogHandler.LOG_USER)
        else:
            raise AssertionError

        log_handler.setFormatter(logging.Formatter(log_format, datefmt=log_dateformat))
        log = logging.getLogger(__name__)
        log.addHandler(log_handler)

        parser = argparse.ArgumentParser(description=description)

        super().__init__(name, description, log, parser)

    def run(self):
        self.args = self.parser.parse_args()
        super().run()