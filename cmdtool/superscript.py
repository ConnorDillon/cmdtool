from .script import Script


class Superscript(Script):
    def __init__(self, name, description, subscripts, log_output='console', log_level='info', log_format='%(message)s'):
        super().__init__(name, description, log_output, log_level, log_format)
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.subscripts = {}
        for scriptclass in subscripts:
            subscript = scriptclass(self)
            self.subscripts[subscript.name] = subscript

    def script(self):
        subscript = self.subscripts[self.name + '/' + self.args.command]
        subscript.args = self.args
        subscript()