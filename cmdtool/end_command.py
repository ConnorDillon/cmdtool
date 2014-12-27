import logging
import logging.handlers
import subprocess
import traceback
import threading
from .base_command import BaseCommand


class EndCommand(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threads = []
        self.params = {}
        self.testmode = False
        self.add_arg('--loglevel', choices=['debug', 'info', 'warning', 'error'], default='info')
        self.add_arg('--testmode', action='store_true')
        self.add_arg('--console', action='store_true')

    def set_loglevel(self):
        if self.args.loglevel == 'debug':
            self.log.setLevel(logging.DEBUG)
        elif self.args.loglevel == 'info':
            self.log.setLevel(logging.INFO)
        elif self.args.loglevel == 'warning':
            self.log.setLevel(logging.WARNING)
        else:
            assert self.args.loglevel == 'error'
            self.log.setLevel(logging.ERROR)

    def add_arg(self, *args, **kwargs):
        return self.parser.add_argument(*args, **kwargs)

    def fmt_exception(self, exception):
        if isinstance(exception, subprocess.CalledProcessError):
            error = 'cmd: ({0}) msg: {1}'.format(exception.cmd, exception.output.decode())
        else:
            error = str(exception)
        if self.log.level == logging.DEBUG:
            return error + '  TRACEBACK:\n' + ''.join(traceback.format_tb(exception.__traceback__))
        return error

    def set_testmode(self):
        if self.args.testmode:
            self.testmode = True
            self.log.setLevel(logging.DEBUG)

    def set_loghandler(self):
        if self.args.console:
            handler = logging.StreamHandler()
        else:
            handler = logging.handlers.SysLogHandler(address='/dev/log',
                                                     facility=logging.handlers.SysLogHandler.LOG_USER)

        handler.setFormatter(logging.Formatter(fmt=self.log_fmt, datefmt=self.log_datefmt))

        if not self.log.handlers:
            self.log.addHandler(handler)
        else:
            assert len(self.log.handlers) == 1
            self.log.handlers[0] = handler

    def debug(self, msg):
        self.log.debug(self.format(msg))

    def info(self, msg):
        self.log.info(self.format(msg))

    def warning(self, msg):
        self.log.warning(self.format(msg))

    def error(self, msg):
        self.log.error(self.format(msg))

    def format(self, string):
        return string.format(**self.params)

    def sh(self, command):
        cmd = self.format(command)
        if self.testmode:
            print(cmd)
        else:
            self.debug('executing command: ' + cmd)
            return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()

    def run(self, args=None):
        super().run(args)
        self.set_loghandler()
        self.set_loglevel()
        self.set_testmode()
        self.params.update(vars(self.args))
        self.debug('starting script: ' + self.name)

        try:
            self.script()
        except Exception as e:
            self.error(self.fmt_exception(e))
        finally:
            if self.threads:
                self.debug('waiting for completion of threads of: ' + self.name)
                for t in self.threads:
                    t.join()
            self.debug('stopping script: ' + self.name)

    def run_thread(self, fn, *args, **kwargs):
        def try_fn():
            try:
                fn(*args, **kwargs)
            except Exception as e:
                self.error(self.fmt_exception(e))
        t = threading.Thread(target=try_fn)
        t.start()
        self.threads.append(t)

    def script(self):
        raise NotImplementedError
