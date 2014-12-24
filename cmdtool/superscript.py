import logging
import argparse
from .base_script import BaseScript


class Superscript(BaseScript):
    def __init__(self, name, description, subscripts, *args, **kwargs):
        log = logging.getLogger(__name__)
        parser = argparse.ArgumentParser(description=description)
        super().__init__(name, description, parser, log, *args, **kwargs)
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.subscripts = {}
        for scriptclass in subscripts:
            subscript = scriptclass(self)
            self.subscripts[subscript.name] = subscript

    def run(self):
        super().run()
        subscript = self.subscripts[self.name + '/' + self.args.command]
        subscript.args = self.args
        subscript()