"""Read-only packet replay; all potentially writing checks run in a temporary copy."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,time,platform
import numpy as np
import sympy
ROOT=Path(__file__).resolve().parent
manifest=ROOT/'SHA256SUMS.txt'
assert manifest.exists(), 'Missing SHA256SUMS.txt'
for line in manifest.read_text().splitlines():
    digest,name=line.split('  ',1)
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest, name
print('PASS: SHA-256 manifest',flush=True)
print('Python',platform.python_version(),'NumPy',np.__version__,'SymPy',sympy.__version__,flush=True)
with tempfile.TemporaryDirectory(prefix='measured_povm_replay_') as td:
    p=Path(td)/'packet';shutil.copytree(ROOT,p)
    def run(name):
        start=time.monotonic()
        result=subprocess.run([sys.executable,str(p/'checks'/name)],cwd=p,text=True,capture_output=True)
        if result.returncode:
            print(result.stdout);print(result.stderr);raise RuntimeError(name+' failed')
        print('PASS:',name,'(%0.2f s)'%(time.monotonic()-start),flush=True)
        print(result.stdout.strip(),flush=True)
    before={n:np.load(p/'data'/n) for n in ['huang_theta0_printed.npy','huang_theta_pi_over_4_printed.npy']}
    run('parse_huang.py')
    for n,arr in before.items():
        assert np.array_equal(arr,np.load(p/'data'/n)),n
        prefix=n.replace('_printed.npy','')
        for k in range(4):assert np.array_equal(arr[k],np.loadtxt(p/'data'/f'{prefix}_E{k+1}.csv',delimiter=',',dtype=complex))
    print('PASS: regenerated Huang transcription equals packaged arrays and CSVs',flush=True)
    reference=json.loads((p/'data/welte_risk_prediction.json').read_text())
    run('evaluate_welte.py')
    actual=json.loads((p/'data/welte_risk_prediction.json').read_text())
    for key in ['fixed_score_risk','source_ideal_risk','calibration_refit_risk']:
        assert abs(reference[key]-actual[key])<1e-12,key
    checks=json.loads((p/'data/welte_checksums.json').read_text())
    assert len(checks)==5 and all(x['matches_archive'] for x in checks.values())
    print('PASS: all five Welte files match original archive MD5 checksums',flush=True)
    exact_reference=json.loads((p/'certificates/tight_box_certificate.json').read_text())
    # Audit the archived witnesses before constructors may regenerate them.
    run('check_huang_frozen.py')
    run('check_huang_tight_box.py')
    run('certify.py')
    run('certify_half_box.py')
    run('tight_box_bound.py')
    generated=json.loads((p/'certificates/tight_box_certificate.json').read_text())
    for a,b in zip(exact_reference,generated):
        assert sympy.simplify(sympy.sympify(a['risk_upper_exact'])-sympy.sympify(b['risk_upper_exact']))==0
    run('check_huang_tight_box.py')
print('PASS: all archived certificates, regenerated certificates and independent checks',flush=True)
