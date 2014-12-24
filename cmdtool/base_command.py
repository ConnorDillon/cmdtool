class BaseCommand:
    def __init__(self, name, description, parser, log, log_fmt=None, log_datefmt=None):
        self.name = name
        self.description = description
        self.parser = parser
        self.log = log
        self.log_fmt = log_fmt
        self.log_datefmt = log_datefmt
        self.args = None

    def parse_args(self, args=None):
        if args:
            self.args = self.parser.parse_args(args)
        else:
            self.args = self.parser.parse_args()

    def run(self):
        if not self.args:
            self.parse_args()

    def __call__(self):
        self.run()