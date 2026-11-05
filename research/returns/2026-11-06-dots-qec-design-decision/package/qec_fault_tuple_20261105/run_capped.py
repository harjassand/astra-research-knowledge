"""External fixed-run launcher. Does not change the frozen sampler.

Checks the launch manifest, caps wall time at 1200 s, and checks resident memory
against 2 GiB every 25 ms. Linux wait4 supplies whole-child CPU time and peak RSS.
The RSS monitor is sampled, not a kernel hard memory cgroup. No interval is
created by this launcher for a killed/partial run.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / 'qec_fault_tuple_20261105'
PYTHON = BASE / 'matched_decoder_runtime_recovery_20261018/venv/bin/python'

p = argparse.ArgumentParser()
p.add_argument('--distance', type=int, choices=[13,21], required=True)
a = p.parse_args()
shots, seed = {13:(20000,202611051913),21:(10000,202611052921)}[a.distance]
prefix = OUT / f'production_d{a.distance}_{shots}'
manifest_log = prefix.with_name(prefix.name + '_launch_hashcheck.log')
with manifest_log.open('w') as f:
    subprocess.run(['sha256sum','-c',str(OUT/'PRECOMMIT_SHA256SUMS')],cwd=BASE,stdout=f,stderr=subprocess.STDOUT,check=True)
cmd = [str(PYTHON),str(OUT/'exact_sampler.py'),'--directory',str(OUT/f'd{a.distance}'),
       '--shots',str(shots),'--seed',str(seed),'--output',str(prefix.with_suffix('.json'))]
env = dict(os.environ, MPLCONFIGDIR='/tmp/mpl_qec_audit')
start = time.perf_counter()
start_utc = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
monitored_peak = 0
kill_reason = None
with prefix.with_suffix('.log').open('w') as log:
    proc = subprocess.Popen(cmd,cwd=BASE,stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
    while True:
        pid, status, usage = os.wait4(proc.pid,os.WNOHANG)
        if pid:
            proc.returncode = os.waitstatus_to_exitcode(status)
            break
        rss = 0
        try:
            for line in Path(f'/proc/{proc.pid}/status').read_text().splitlines():
                if line.startswith('VmRSS:'):
                    rss = int(line.split()[1])*1024
                    break
        except FileNotFoundError:
            pass
        monitored_peak = max(monitored_peak,rss)
        if kill_reason is None:
            if rss > 2*1024**3:
                kill_reason = 'resident memory exceeded 2 GiB'
            elif time.perf_counter()-start > 1200:
                kill_reason = 'wall time exceeded 1200 seconds'
            if kill_reason:
                os.killpg(proc.pid,signal.SIGKILL)
        time.sleep(.025)
record = {
    'command':cmd,'start_utc_system_clock':start_utc,'shots':shots,'seed':seed,
    'exit_code':proc.returncode,'kill_reason':kill_reason,
    'full_subprocess_wall_seconds':time.perf_counter()-start,
    'full_subprocess_user_seconds':usage.ru_utime,
    'full_subprocess_system_seconds':usage.ru_stime,
    'full_subprocess_peak_rss_kib':usage.ru_maxrss,
    'monitored_peak_rss_bytes':monitored_peak,
    'max_wall_seconds':1200,'max_resident_bytes':2*1024**3,
    'resident_monitor_interval_seconds':.025,
    'resident_cap_caveat':'Sampled RSS monitor, not a kernel memory cgroup. wait4 reports whole-process peak RSS.',
    'precommit_manifest_sha256':hashlib.sha256((OUT/'PRECOMMIT_SHA256SUMS').read_bytes()).hexdigest(),
    'launch_hashcheck_log':manifest_log.name,
}
prefix.with_name(prefix.name+'_process_resources.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2),flush=True)
raise SystemExit(proc.returncode or (1 if kill_reason else 0))
