#!/usr/bin/python

# Check files for changes and run the appropriate spec files

import argparse
import os
import re
import subprocess
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description='Run specs for files that have changed.')
parser.add_argument("-p", "--path", dest="path")
parser.add_argument("-s", "--seed", dest="seed")
args = parser.parse_args()

origin = os.getcwd()
specs = []

print "Changes to commit\n"

### SPECS ###
os.chdir(args.path + "/spec")

subprocess.call(['git', 'status', '-s', '.'])
p = Popen(['git', 'status', '-s', '.'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()

regex = re.compile('([\w]+)\s+(.*)', re.IGNORECASE)
changes = regex.findall(output)

for a in changes:
  specs.append("spec/" + a[1])

### APP FILES ###
os.chdir(args.path + "/app")

subprocess.call(['git', 'status', '-s', '.'])
p = Popen(['git', 'status', '-s', '.'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()

regex = re.compile('([\w]+)\s+(.*)', re.IGNORECASE)
changes = regex.findall(output) 

for a in changes:
  specs.append("spec/" + a[1].replace('.rb', '_spec.rb'))

if len(specs) == 0:
  print "Nothing to run\n"
else:
	### RUN SPECS ###
	os.chdir(args.path)

	rspec = ["rspec", "-c", "-f", "d"]
	if args.seed:
  	  rspec.extend(["--seed", args.seed])

	rspec.extend(list(set(specs)))
	subprocess.call(rspec)

# end, return to home
os.chdir(origin)
