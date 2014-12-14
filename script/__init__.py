import subprocess


__all__ = ['Script', 'Subscript', 'Superscript', 'sh']


from .script import Script
from .subscript import Subscript
from .superscript import Superscript


def sh(command):
    return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).decode()
