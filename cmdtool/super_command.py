import logging
import argparse
from .base_command import BaseCommand


class SuperCommand(BaseCommand):
    def __init__(self, name, description, subscripts, *args, **kwargs):
        log = logging.getLogger(__name__)
        parser = argparse.ArgumentParser(description=description)
        super().__init__(name, description, parser, log, *args, **kwargs)
        self.subparsers = self.parser.add_subparsers(dest="command")
        self.subscripts = {}
        for scriptclass in subscripts:
            subscript = scriptclass(self)
            self.subscripts[subscript.name] = subscript

    def run(self, args=None):
        super().run(args)
        subscript = self.subscripts[self.name + '/' + self.args.command]
        subscript(self.args)