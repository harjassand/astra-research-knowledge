#!/usr/bin/env python3
"""Run one baseline in an isolated process group, capturing its exact output.

Each invocation starts only one subprocess; getrusage(RUSAGE_CHILDREN) reports
that process (and waited descendants). No timings for download/build are mixed
into per-instance export+preprocess+count. Preprocessing inside d4 is included.
"""
import argparse
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("--timeout", type=float, default=120)
parser.add_argument("--memory-gib", type=int, default=8)
parser.add_argument("--result", required=True)
parser.add_argument("--log", required=True)
parser.add_argument("command", nargs=argparse.REMAINDER)
args = parser.parse_args()
command = args.command
if command and command[0] == "--":
    command = command[1:]
if not command:
    parser.error("missing command")

def constrain():
    resource.setrlimit(resource.RLIMIT_AS, (args.memory_gib*2**30, args.memory_gib*2**30))

start = time.perf_counter()
with Path(args.log).open("wb") as log:
    process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                               start_new_session=True, preexec_fn=constrain)
    timeout = False
    try:
        process.wait(timeout=args.timeout)
    except subprocess.TimeoutExpired:
        timeout = True
        os.killpg(process.pid, signal.SIGKILL)
        process.wait()
elapsed = time.perf_counter()-start
usage = resource.getrusage(resource.RUSAGE_CHILDREN)
result = {"command": command, "elapsed_seconds": elapsed, "timeout_seconds": args.timeout,
          "timed_out": timeout, "exit_code": process.returncode,
          "user_cpu_seconds": usage.ru_utime, "system_cpu_seconds": usage.ru_stime,
          "peak_rss_kib": usage.ru_maxrss, "address_space_limit_gib": args.memory_gib,
          "log": str(Path(args.log).resolve()),
          "measurement_note": "Single child per runner invocation; includes solver parsing and preprocessing; Linux ru_maxrss."}
Path(args.result).write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
