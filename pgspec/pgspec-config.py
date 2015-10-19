#!/usr/bin/python

# Set up environment configuration that pgspec will use.  Run this if you
# don't want to set those pesky variables every time!
#
# author    Eric Weaver <eweaver@pathgather.com>
# since     2015-10-16
# version   1.0
#

__CONFIG_FILE__ = "pgspec.conf"

str = raw_input("Pathgather repository location: ");
fo = open(__CONFIG_FILE__, "w")
fo.write("PATHGATHER_DIRECTORY=" + str)
fo.close()
