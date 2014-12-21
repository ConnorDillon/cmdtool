import subprocess
import threading
import traceback
import logging


class BaseScript:
    def __init__(self, name, description, log, parser):
        self.name = name
        self.description = description
        self.log = log
        self.parser = parser
        self.args = None
        self.params = {}
        self.testmode = False
        self.threads = []

        self.add_arg('--loglevel', choices=['debug', 'info', 'warning', 'error'], default='info')
        self.add_arg('--testmode', action='store_true')

    def set_testmode(self):
        self.testmode = True
        self.set_loglevel('debug')

    def set_loglevel(self, level):
        if level == 'debug':
            self.log.setLevel(logging.DEBUG)
        elif level == 'info':
            self.log.setLevel(logging.INFO)
        elif level == 'warning':
            self.log.setLevel(logging.WARNING)
        elif level == 'error':
            self.log.setLevel(logging.ERROR)
        else:
            raise AssertionError

    def fmt_exception(self, exception):
        if isinstance(exception, subprocess.CalledProcessError):
            error = 'cmd: ({0}) msg: {1}'.format(exception.cmd, exception.output.decode())
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
        if self.args.loglevel:
            self.set_loglevel(self.args.loglevel)
        if self.args.testmode:
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

    def format(self, string):
        return string.format(**self.params)

    def sh(self, command):
        if self.testmode:
            print(self.format(command))
        else:
            if self.log.level == logging.DEBUG:
                self.debug('executing command: ' + command)
            return subprocess.check_output(self.format(command),
                                           stderr=subprocess.STDOUT, shell=True).decode()

    def __call__(self):
        self.run()