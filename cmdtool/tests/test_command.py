import unittest
from .test_log import TestLog
from cmdtool import Command


class SomeCommand(Command):
    def __init__(self):
        super().__init__('test', 'a test script', log_fmt='%(levelname)s: %(message)s')
        self.add_arg('derp')

    def script(self):
        shell_output = self.sh('echo {derp}')
        self.info(shell_output)
        self.warning(shell_output)
        self.error(shell_output)


class TestCommand(unittest.TestCase):
    def setUp(self):
        self.command = SomeCommand()

    def test_script(self):
        with TestLog() as log:
            self.command.parse_args('herpdaderpa --console')
            self.command()
            expected = ['INFO: herpdaderpa\n', '\n', 'WARNING: herpdaderpa\n', '\n', 'ERROR: herpdaderpa\n', '\n']
            self.assertEqual(log, expected)