from .base_script import BaseScript


class Subscript(BaseScript):
    def __init__(self, name, superscript, parent_parsers=None):
        if parent_parsers is None:
            parent_parsers = []
        parser = superscript.subparsers.add_parser(name, parents=parent_parsers)
        super().__init__(superscript.name + '/' + name, superscript.description,
                         superscript.log, parser)