import logging
import logging.handlers
import argparse
from .base_script import BaseScript


class Script(BaseScript):
    def __init__(self, name, description, *args, log_output='console',
                 log_level='info', log_format='%(message)s', **kwargs):
        if log_output == 'console':
            log_handler = logging.StreamHandler()
        elif log_output == 'syslog':
            log_handler = logging.handlers.SysLogHandler(address='/dev/log',
                                                         facility=logging.handlers.SysLogHandler.LOG_CRON)
        else:
            raise AssertionError

        if log_level == 'debug':
            real_log_level = logging.DEBUG
        elif log_level == 'info':
            real_log_level = logging.INFO
        elif log_level == 'warn':
            real_log_level = logging.WARN
        elif log_level == 'error':
            real_log_level = logging.ERROR
        else:
            raise AssertionError

        log_handler.setFormatter(logging.Formatter(log_format))
        log = logging.getLogger(__name__)
        log.setLevel(real_log_level)
        log.addHandler(log_handler)

        parser = argparse.ArgumentParser(description=description)

        super().__init__(name, description, log, parser, *args, **kwargs)

    def script(self):
        raise NotImplementedError

    def run(self):
        self.args = self.parser.parse_args()
        super().run()