#!/usr/bin/python

# Check files for changes and run the appropriate spec files

import argparse
import os
import re
import subprocess
from subprocess import Popen, PIPE

from gitcommands import GitCommands
from specparser import SpecParser
from osprocessor import OsProcessor

parser = argparse.ArgumentParser(description='Run specs for files that have changed.')
parser.add_argument("-p", "--path", dest="path")
parser.add_argument("-s", "--seed", dest="seed")
parser.add_argument("-a", "--all", dest="allchanges")
args = parser.parse_args()

### SETUP ###
specs = []
os_processor = OsProcessor(args.path)
git = GitCommands(os_processor)
parser = SpecParser()

print "Changes to commit\n"

if args.allchanges:
    files_changed = git.status_branch()
    specs.extend(parser.specs_from_changes(files_changed, False))
else:
    ### SPECS ###
    files_changed = git.status_add_modified(SpecParser.SPEC_DIRECTORY)
    specs.extend(parser.specs_from_changes(files_changed, SpecParser.SPEC_DIRECTORY))

    ### APP FILES ###
    files_changed = git.status_add_modified(SpecParser.APP_DIRECTORY)
    specs.extend(parser.specs_from_changes(files_changed, SpecParser.APP_DIRECTORY))

### CLEANUP; get ready to run specs ###
os_processor.change_to_root()
unique_specs = list(set(specs))
valid_specs = []

for idx, spec in enumerate(unique_specs):
    if os_processor.file_exists(spec) == True:
        print spec
        valid_specs.append(spec)

if len(valid_specs) == 0:
    print "Nothing to run\n"
    exit(0)

### RUN SPECS ###
rspec = ["rspec", "-c", "-f", "d"]
if args.seed:
    rspec.extend(["--seed", args.seed])

rspec.extend(valid_specs)
subprocess.call(rspec)

os_processor.return_to_origin()
