from .script import Script


class Superscript(Script):
    def __init__(self, subscripts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.subscripts = {}
        for scriptclass in subscripts:
            subscript = scriptclass(self)
            self.subscripts[subscript.name] = subscript

    def script(self):
        subscript = self.subscripts[self.name + '/' + self.args.command]
        subscript.args = self.args
        subscript()