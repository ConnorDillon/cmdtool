from unittest import TestCase
from .test_log import TestLog
from cmdtool import Superscript, Subscript


class SomeSuperscript(Superscript):
    def __init__(self):
        super().__init__('test', 'test lalalal', subscripts=[SomeSubscript])


class SomeSubscript(Subscript):
    def __init__(self, superscript):
        super().__init__('subtest', superscript)
        self.add_arg('bla')

    def script(self):
        self.info('{bla}')


class TestSuperscript(TestCase):
    def setUp(self):
        self.script = SomeSuperscript()

    def test_script(self):
        with TestLog() as log:
            self.script.parse_args('subtest lalala --console'.split())
            self.script()
            self.assertEqual(log, ['lalala', '\n'])
