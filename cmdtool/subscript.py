from .end_script import EndScript


class Subscript(EndScript):
    def __init__(self, name, superscript):
        parser = superscript.subparsers.add_parser(name)
        super().__init__(superscript.name + '/' + name, superscript.description, parser,
                         superscript.log, superscript.log_fmt, superscript.log_datefmt)