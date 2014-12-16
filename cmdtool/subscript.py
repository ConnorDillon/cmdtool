from .base_script import BaseScript


class Subscript(BaseScript):
    def __init__(self, name, superscript, *args, **kwargs):
        parser = superscript.subparsers.add_parser(name)
        super().__init__(superscript.name + '/' + name, superscript.description,
                         superscript.log, parser, *args, **kwargs)

    def script(self):
        raise NotImplementedError