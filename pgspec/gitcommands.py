import re
import subprocess
from subprocess import Popen, PIPE

import osprocessor

class GitCommands:
    def __init__(self, os_processor):
        self.os_processor = os_processor

    def status_branch(self):
        self.os_processor.change_to_root()

        specs = []
        p = Popen(['git', '-c', 'color.status=false', 'diff', '--name-status', 'origin/master'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()

        regex = re.compile('\s*[AM]+\s*(spec|app)(.*)', re.IGNORECASE)
        return regex.findall(output)

    def status_add_modified(self, directory):
        self.os_processor.change_dir(directory)

        specs = []
        p = Popen(['git', '-c', 'color.status=false', 'status', '-s', '.'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()

        regex = re.compile('\s*[AM]+\s*(.*)', re.IGNORECASE)
        return regex.findall(output)

    def diff_changes(self, files):
        spec_diff = {}

        for file in files:
            p = Popen(['git', '-c', 'color.status=false', 'diff', '-U100', file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            diff, err = p.communicate()
            regex = re.compile('\s*def\s*([\w_\?\!]+)', re.IGNORECASE)
            definition = regex.findall(diff)
            spec_diff[file] = definition

        return spec_diff
