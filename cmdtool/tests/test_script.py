import unittest
from .test_log import TestLog
from cmdtool import Script


class SomeScript(Script):
    def __init__(self):
        super().__init__('test', 'a test script', log_fmt='%(levelname)s: %(message)s')
        self.add_arg('derp')

    def script(self):
        shell_output = self.sh('echo {derp}')
        self.info(shell_output)
        self.warning(shell_output)
        self.error(shell_output)


class TestScript(unittest.TestCase):
    def setUp(self):
        self.script = SomeScript()

    def test_script(self):
        with TestLog() as log:
            self.script.parse_args('herpdaderpa --console'.split())
            self.script()
            expected = ['INFO: herpdaderpa\n', '\n', 'WARNING: herpdaderpa\n', '\n', 'ERROR: herpdaderpa\n', '\n']
            self.assertEqual(log, expected)