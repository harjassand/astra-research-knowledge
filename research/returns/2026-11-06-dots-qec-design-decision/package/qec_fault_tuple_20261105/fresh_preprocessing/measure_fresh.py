"""Fresh, isolated preprocessing only. No statistical sampling.

Source copies are byte-identical and retain their original relative directory
structure. Each distance has a 1200-second joint screen+producer budget and a
2-GiB sampled process-group RSS cap. wait4 reports exact kernel largest-process
peak RSS over waited descendants; aggregate group RSS is sampled every 25 ms.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import time

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parent
BASE = FROZEN.parent
PYTHON = BASE / 'matched_decoder_runtime_recovery_20261018/venv/bin/python'
ENV = dict(os.environ, MPLCONFIGDIR='/tmp/mpl_qec_audit')


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for part in iter(lambda: f.read(1 << 20), b''):
            h.update(part)
    return h.hexdigest()


def group_rss_kib(group):
    total = 0
    for path in Path('/proc').iterdir():
        if not path.name.isdigit():
            continue
        try:
            stat = (path/'stat').read_text()
            rest = stat[stat.rfind(')')+2:].split()
            if int(rest[2]) != group:
                continue
            for line in (path/'status').read_text().splitlines():
                if line.startswith('VmRSS:'):
                    total += int(line.split()[1])
                    break
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            pass
    return total


def measure(name, command, deadline):
    start = time.perf_counter()
    peak = 0
    reason = None
    with (HERE/f'{name}.log').open('w') as log:
        proc = subprocess.Popen(command,cwd=HERE,env=ENV,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
        while True:
            pid,status,usage = os.wait4(proc.pid,os.WNOHANG)
            if pid:
                proc.returncode = os.waitstatus_to_exitcode(status)
                break
            rss = group_rss_kib(proc.pid)
            peak = max(peak,rss)
            if reason is None:
                if rss > 2*1024**2:
                    reason = 'aggregate resident memory exceeded 2 GiB'
                elif time.perf_counter() > deadline:
                    reason = 'joint preprocessing wall budget exceeded 1200 seconds'
                if reason:
                    os.killpg(proc.pid,signal.SIGKILL)
            time.sleep(.025)
    result = {'stage':name,'command':list(map(str,command)),
              'full_subprocess_wall_seconds':time.perf_counter()-start,
              'full_subprocess_user_seconds':usage.ru_utime,
              'full_subprocess_system_seconds':usage.ru_stime,
              'wait4_largest_process_peak_rss_kib':usage.ru_maxrss,
              'observed_peak_process_group_rss_kib':peak,
              'exit_code':proc.returncode,'budget_failure':reason,
              'rss_monitor_interval_seconds':.025}
    (HERE/f'{name}_resource.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    if proc.returncode or reason:
        raise RuntimeError(f'{name} failed: {result}')
    return result


def verify_copies():
    items = [
        ('qec_overlap_gate_20261105/fault_tuple_screen.py',BASE/'qec_overlap_gate_20261105/fault_tuple_screen.py'),
        ('qec_fault_tuple_20261105/build.py',FROZEN/'build.py'),
        ('qec_fault_tuple_20261105/certify_tuple.cpp',FROZEN/'certify_tuple.cpp'),
    ]
    for d in (13,21):
        name=f'canonical_qec_circuit_gate_20261105/d{d}_r{d}_p1_1000_graph.json'
        items.append((name,BASE/name))
    out=[]
    for relative,original in items:
        copy=HERE/relative
        h=digest(original)
        assert digest(copy)==h,(copy,original)
        out.append({'copy':relative,'original':str(original),'sha256':h,'byte_identical':True,'path_changes':'None; original relative layout preserved.'})
    record={'copied_sources':out,'measurement_script_sha256':digest(__file__)}
    (HERE/'SOURCE_COPY_MANIFEST.json').write_text(json.dumps(record,indent=2)+'\n')
    return record


def compare(d):
    import numpy as np
    original=FROZEN/f'd{d}'
    fresh=HERE/'qec_fault_tuple_20261105'/f'd{d}'
    comparisons={}
    for name in ['U.npy','J_lo.npy','J_hi.npy','distance.npy','W.npy','starts.npy']:
        a,b=np.load(original/name,mmap_mode='r'),np.load(fresh/name,mmap_mode='r')
        comparisons[name]={'shape_equal':a.shape==b.shape,'dtype_equal':a.dtype==b.dtype,
                           'array_equal':bool(np.array_equal(a,b)),
                           'byte_hash_equal':digest(original/name)==digest(fresh/name),
                           'original_sha256':digest(original/name),'fresh_sha256':digest(fresh/name)}
        assert all(comparisons[name][key] for key in ['shape_equal','dtype_equal','array_equal','byte_hash_equal']),name
    a=json.loads((original/'parameters.json').read_text())
    b=json.loads((fresh/'parameters.json').read_text())
    fields=['Z_exact','conversion_TV_upper_exact','N','D','Q','qden','q_numerators','dl','dr','dlmax','certificate']
    fields_equal={key:a[key]==b[key] for key in fields}
    assert all(fields_equal.values()),fields_equal
    record={'distance':d,'arrays':comparisons,'parameter_fields_equal':fields_equal,
            'Z_exact':b['Z_exact'],'conversion_TV_upper_exact':b['conversion_TV_upper_exact'],
            'all_equivalent':True}
    (HERE/f'd{d}_equivalence.json').write_text(json.dumps(record,indent=2)+'\n')
    return record


def run(d):
    verify_copies()
    with (HERE/f'd{d}_frozen_launch_hashcheck.log').open('w') as f:
        subprocess.run(['sha256sum','-c',str(FROZEN/'PRECOMMIT_SHA256SUMS')],cwd=BASE,stdout=f,stderr=subprocess.STDOUT,check=True)
    start=time.perf_counter()
    deadline=start+1200
    screen=measure(f'd{d}_floating_screen',[str(PYTHON),str(HERE/'qec_overlap_gate_20261105/fault_tuple_screen.py'),
                   '--distance',str(d),'--cut-distance','64','--modulus','64'],deadline)
    producer=measure(f'd{d}_exact_producer',[str(PYTHON),str(HERE/'qec_fault_tuple_20261105/build.py'),
                     '--distance',str(d)],deadline)
    pipeline=time.perf_counter()-start
    equivalence=compare(d)
    result={'distance':d,'scope':'Genuinely fresh isolated floating table plus exact producer, including each Python import, compiler invocation, and output. No statistical sampling.',
            'stages':[screen,producer],
            'fresh_preprocessing_joint_wall_seconds':pipeline,
            'sum_complete_stage_wall_seconds':sum(x['full_subprocess_wall_seconds'] for x in [screen,producer]),
            'largest_wait4_process_peak_rss_kib':max(x['wait4_largest_process_peak_rss_kib'] for x in [screen,producer]),
            'largest_observed_process_group_rss_kib':max(x['observed_peak_process_group_rss_kib'] for x in [screen,producer]),
            'exact_equivalence':equivalence['all_equivalent'],
            'resource_scope':'Each stage measured as a complete subprocess. Joint wall includes sequential launch/record overhead but excludes setup copying, pre-run hashcheck, and post-run equivalence comparisons. Group RSS sampled every25ms, not a kernel hard memory cgroup.',
            'max_joint_preprocessing_seconds':1200,'max_resident_bytes':2*1024**3}
    (HERE/f'd{d}_preprocessing_summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--distance',type=int,choices=[13,21],required=True)
    run(p.parse_args().distance)
