#!/usr/bin/env python3
from script import Script


class BackupSh(Script):
    def __init__(self):
        super().__init__(name='backupsh',
                         description='Use rsync to backup a directory. '
                                     'Source and destination can be specified by unix path '
                                     'or user@host:dir, the latter requires SSH keys. '
                                     'Results will be logged to syslog.',
                         log_output='syslog')
        self.add_arg('source')
        self.add_arg('dest')
        self.add_arg('-f', '--flags', default='aAXv')

    def script(self):
        self.info(self.format('transferring data from {source} to {dest}'))
        self.sh('rsync -{flags} {source} {dest}')


if __name__ == '__main__':
    BackupSh()()