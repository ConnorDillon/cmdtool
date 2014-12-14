import subprocess
import traceback


class BaseScript:
    def __init__(self, name, description, log, parser):
        self.name = name
        self.description = description
        self.log = log
        self.parser = parser
        self.args = None

    @staticmethod
    def fmt_exception(exception):
        if isinstance(exception, subprocess.CalledProcessError):
            error = exception.output.decode()
        else:
            error = str(exception)
        return error + '  TRACEBACK:\n' + ''.join(traceback.format_tb(exception.__traceback__))

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
        self.args = self.parser.parse_args()
        self.debug('starting script: ' + self.name)
        try:
            self.script()
        except Exception as e:
            self.error(self.fmt_exception(e))
        finally:
            self.debug('stopping script: ' + self.name)

    def __call__(self):
        self.run()
