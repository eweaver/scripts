#!/usr/bin/python

# Run RSpec files for changes made to a feature branch
#
# author    Eric Weaver <eweaver@pathgather.com>
# since     2015-10-16
# version   1.0
#
# Built on top of git and rpsec to provide a few different methods
# running specific rspec tests based on changes.  At the moment, most
# methods rely on simple git commands and file matching to run.  It
# will not cascade down to models/helpers that could be affected by
# a top-level change.
#
#
#   Methods:
#       - Run specs for all files that have changed between a feature branch
#         and given remote master.  This will run specs for upstream changes
#         not yet in your feature branch as well (for now).
#       - Run specs for locally staged changes
#
#   TODOs:
#       - Separate specs based on changes made in feature branch vs. changes
#         made in remote master.  Allow a single set to be run, if desired.
#       - Run individual tests in a spec file if individual tests can be determined.
#       - Show missing specs
#       - Add extended mode to pull in all models associated with a controller/model
#         that has changed.
#


import argparse
import os
import re
import subprocess
from subprocess import Popen, PIPE

from gitcommands import GitCommands
from specparser import SpecParser
from osprocessor import OsProcessor

__CONFIG_FILE_PATH__ = "PGSPEC_DIRECTORY"
__CONFIG_ITEM_PATH__ = "PATHGATHER_DIRECTORY"
__CONFIG_FILE__ = "/pgspec.conf"

parser = argparse.ArgumentParser(description='Run specs for files that have changed.')
parser.add_argument("-p", "--path", dest="path")
parser.add_argument("-s", "--seed", dest="seed")
parser.add_argument("-b", "--branch", dest="branch")
parser.add_argument("-a", "--all", dest="allchanges", action="store_true")
parser.add_argument("-f", "--force", dest="cleanup", action="store_true")
args = parser.parse_args()
root_path = None

# Try to set root path from config first
fo = open(os.path.dirname(os.path.realpath(__file__)) + __CONFIG_FILE__, "r")
for line in fo:
    config_name, config_value = line.split("=", 1)
    if config_name.strip() == __CONFIG_ITEM_PATH__:
        root_path = config_value.strip()
    elif config_name.strip() == __CONFIG_FILE_PATH__:
        __CONFIG_FILE__ = config_value.strip() + __CONFIG_FILE__
        break

# Fall back to using passed in values
if root_path == None and args.path != None:
    root_path = args.path

if root_path == None:
    print "No valid root project path set!"
    exit(0)

### GET READY! ####
os_processor = OsProcessor(root_path)

### Some cleanup, perhaps? ###
if args.cleanup == True:
    print "Forcing run, cleaning up previous run..."
    os_processor.end_pid()

### SETUP ###
specs = []
if os_processor.start_pid() == False:
    print "Process already running"
    exit(0)


git = GitCommands(os_processor, args.branch)
parser = SpecParser()

print "Checking for specs to run..."

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
missing_specs = []

for idx, spec in enumerate(unique_specs):
    if os_processor.file_exists(spec) == True:
        valid_specs.append(spec)
    else:
        missing_specs.append(spec)

if len(valid_specs) == 0:
    print "Nothing to run"
    os_processor.end_pid()
    exit(0)
else:
    print "Found " + str(len(valid_specs)) + " specs to run"
    for s in valid_specs:
        print " > " + '\033[92m' + s + '\033[0m'

### RUN SPECS ###
rspec = ["rspec", "-c", "-f", "d"]
if args.seed:
    rspec.extend(["--seed", args.seed])

rspec.extend(valid_specs)
subprocess.call(rspec)

os_processor.end_pid()
os_processor.return_to_origin()
