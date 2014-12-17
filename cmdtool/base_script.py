import subprocess
import traceback
import logging


class BaseScript:
    def __init__(self, name, description, log, parser, testmode=False):
        self.name = name
        self.description = description
        self.log = log
        self.parser = parser
        self.args = None
        self.params = {}
        self.testmode = testmode

    def fmt_exception(self, exception):
        if isinstance(exception, subprocess.CalledProcessError):
            error = exception.output.decode()
        else:
            error = str(exception)
        if self.log.level == logging.DEBUG:
            return error + '  TRACEBACK:\n' + ''.join(traceback.format_tb(exception.__traceback__))
        return error

    def add_arg(self, *args, **kwargs):
        return self.parser.add_argument(*args, **kwargs)

    def add_parser(self, **kwargs):
        return self.parser.add_subparsers(**kwargs)

    def debug(self, msg):
        self.log.debug(msg)

    def info(self, msg):
        self.log.info(msg)

    def warn(self, msg):
        self.log.warn(msg)

    def error(self, msg):
        self.log.error(msg)

    def script(self):
        raise NotImplementedError

    def run(self):
        self.params.update(self.args.__dict__)
        self.debug('starting script: ' + self.name)
        try:
            self.script()
        except Exception as e:
            self.error(self.fmt_exception(e))
        finally:
            self.debug('stopping script: ' + self.name)

    def format(self, string):
        return string.format(**self.params)

    def sh(self, command):
        if self.testmode:
            print(self.format(command))
        else:
            return subprocess.check_output(self.format(command),
                                           stderr=subprocess.STDOUT, shell=True).decode()

    def __call__(self):
        self.run()
