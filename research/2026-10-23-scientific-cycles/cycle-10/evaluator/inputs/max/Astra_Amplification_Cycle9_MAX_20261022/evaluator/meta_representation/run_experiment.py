"""One fresh sequential process for each prespecified arm; bounded resources."""
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    frozen = json.loads((root/'FROZEN_INPUTS.json').read_text())
    for item in frozen['files']:
        assert sha(root/item['path']) == item['sha256'], item['path']
    directory = root/'results'
    directory.mkdir(exist_ok=True)
    assert not (directory/'WHOLE_PROCESS_RECEIPTS.json').exists(), 'Do not overwrite a run.'
    receipts = []
    for arm in ('A_counts_flags', 'B_occupancy_flags', 'C_occupancy_support_flags'):
        output = directory/(arm+'.json')
        assert not output.exists(), 'One execution per arm.'
        env = os.environ.copy()
        env['PYTHONHASHSEED'] = '0'
        start = time.perf_counter()
        with (directory/(arm+'.stdout.txt')).open('w') as stdout, \
             (directory/(arm+'.stderr.txt')).open('w') as stderr:
            proc = subprocess.Popen([sys.executable, str(root/'common_search.py'),
                                     '--arm', arm, '--output', str(output)],
                                    cwd=root, env=env, stdout=stdout, stderr=stderr,
                                    start_new_session=True)
            wall_kill = False
            while True:
                pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
                if pid:
                    break
                if time.perf_counter()-start > 300:
                    os.killpg(proc.pid, signal.SIGKILL)
                    wall_kill = True
                    pid, status, usage = os.wait4(proc.pid, 0)
                    break
                time.sleep(0.1)
            proc.returncode = os.waitstatus_to_exitcode(status)
        receipt = {
            'arm': arm, 'returncode': proc.returncode, 'wall_kill': wall_kill,
            'whole_process_wall_seconds': time.perf_counter()-start,
            'whole_process_cpu_seconds': usage.ru_utime + usage.ru_stime,
            'whole_process_user_seconds': usage.ru_utime,
            'whole_process_system_seconds': usage.ru_stime,
            'whole_process_peak_rss_bytes': usage.ru_maxrss*1024,
            'measurement': 'Linux wait4 rusage, includes interpreter/import/setup/'
                           'search/serialization and process exit; one sample',
            'output_exists': output.exists(), 'output_sha256': sha(output) if output.exists() else None,
        }
        if output.exists():
            data = json.loads(output.read_text())
            receipt.update({key: data[key] for key in ('reason', 'active_families',
                           'discovered_families', 'checked_transitions')})
        receipts.append(receipt)
        record = {'protocol_sha256': sha(root/'PROTOCOL.txt'),
                  'frozen_inputs_sha256': sha(root/'FROZEN_INPUTS.json'),
                  'python': sys.version, 'platform': platform.platform(),
                  'receipts': receipts,
                  'scope': 'One measured execution each; total development, proof, '
                           'inference and integration cost unknown.'}
        (directory/'WHOLE_PROCESS_RECEIPTS.json').write_text(json.dumps(record, indent=2)+'\n')
        print(json.dumps(receipt, indent=2), flush=True)


if __name__ == '__main__':
    main()
