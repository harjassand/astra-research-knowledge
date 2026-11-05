"""Verify the frozen manifest and optionally rerun checks in a temporary copy."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, time

ROOT=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run-tests',action='store_true');args=ap.parse_args()
    expected={}
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert name not in expected and not Path(name).is_absolute() and '..' not in Path(name).parts
        expected[name]=digest
    found={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS'}
    assert found==set(expected),(found-set(expected),set(expected)-found)
    for name,digest in expected.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    report={'manifested_files':len(expected),'all_hashes_and_coverage_passed':True,'checks':[]}
    if args.run_tests:
        with tempfile.TemporaryDirectory(prefix='weak_parent_replay_') as tmp:
            copy=Path(tmp)/'packet';shutil.copytree(ROOT,copy)
            for name in ['check_pvbs_repair.py','check_coboundary_reset.py',
                         'check_boundary_gap_counterexample.py','check_native_pvbs_coboundary.py',
                         'check_block_representative.py']:
                start=time.perf_counter()
                p=subprocess.run([sys.executable,str(copy/name)],cwd=tmp,
                                 env={**os.environ,'OPENBLAS_NUM_THREADS':'1'},
                                 capture_output=True,text=True)
                if p.returncode:raise RuntimeError(name+'\n'+p.stdout+'\n'+p.stderr)
                report['checks'].append({'script':name,'exit_code':p.returncode,
                                         'complete_subprocess_wall_seconds':time.perf_counter()-start})
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
