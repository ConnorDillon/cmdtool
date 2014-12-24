import logging
import argparse
from .end_command import EndCommand


class Command(EndCommand):
    def __init__(self, name, description, *args, **kwargs):
        log = logging.getLogger(__name__)
        parser = argparse.ArgumentParser(description=description)
        super().__init__(name, description, parser, log, *args, **kwargs)