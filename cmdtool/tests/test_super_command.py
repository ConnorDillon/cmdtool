from unittest import TestCase
from .test_log import TestLog
from cmdtool import SuperCommand, SubCommand


class SomeSuperCommand(SuperCommand):
    def __init__(self):
        super().__init__('test', 'test lalalal', subscripts=[SomeSubCommand])


class SomeSubCommand(SubCommand):
    def __init__(self, superscript):
        super().__init__('subtest', superscript)
        self.add_arg('bla')

    def script(self):
        self.info('{bla}')


class TestSuperCommand(TestCase):
    def setUp(self):
        self.command = SomeSuperCommand()

    def test_script(self):
        with TestLog() as log:
            self.command('subtest lalala --console')
            self.assertEqual(log, ['lalala', '\n'])
