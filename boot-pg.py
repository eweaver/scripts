#!/usr/bin/python

# Pathgather API & Frontend Bootstrap
#
# Starts Postgres & Redis Server for the API
# Starts grunt server and runs rackup for the Frontend
# Runs Foreman for the API
#
# TODO: Add --frontend & --backend options to selectively start

import argparse
import os
import subprocess

#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')

#api_path = os.environ['PG_API_PATH'] || 1

os.chdir("/Users/eweaver/Development/pathgather/pathgather/")
#os.chdir(os.environ['PG_API_PATH'])

# POSTGRES
subprocess.call(["pg_ctl", "stop", "-m", "fast", "-D", "/Users/eweaver/Library/Application Support/Postgres/var-9.4"])
subprocess.call(["pg_ctl", "start", "-D", "/Users/eweaver/Library/Application Support/Postgres/var-9.4"])

# REDIS
subprocess.Popen(["redis-server"])

# FRONTEND
os.chdir("/Users/eweaver/Development/pathgather/frontend/")
#os.chdir(os.environ['PG_FRONTEND_PATH'])

subprocess.Popen(["grunt", "server"])
subprocess.Popen(["rackup"])

# WEBSERVER
os.chdir("/Users/eweaver/Development/pathgather/pathgather/")
#os.chdir(os.environ['PG_API_PATH'])
subprocess.call(["foreman", "start", "-f", "Procfile.local"])


