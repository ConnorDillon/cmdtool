class BaseCommand:
    def __init__(self, name, description, parser, log, log_fmt=None, log_datefmt=None):
        self.name = name
        self.description = description
        self.parser = parser
        self.log = log
        self.log_fmt = log_fmt
        self.log_datefmt = log_datefmt
        self.args = None

    def run(self, args=None):
        if isinstance(args, str):
            self.args = self.parser.parse_args(args.split())
        elif args:
            self.args = args
        else:
            self.args = self.parser.parse_args()

    def __call__(self, args=None):
        self.run(args)