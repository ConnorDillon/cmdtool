import argparse


class ToList(argparse.Action):
    def __call__(self, parser, args, value, option_string=None):
        values = getattr(args, self.dest)
        if values is None:
            values = []
        values.append(value)
        setattr(args, self.dest, values)