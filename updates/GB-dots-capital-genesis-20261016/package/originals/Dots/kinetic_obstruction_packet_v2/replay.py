"""Portable verifier. No network; no execution of acquired Julia sources."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time,platform
p=argparse.ArgumentParser();p.add_argument('--numerical',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args()
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
for item in manifest['files']:
    raw=(root/item['path']).read_bytes()
    assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'], item['path']
# Verify the preserved upstream Git blobs, independently of the payload SHA256 list.
up=json.loads((root/'tensor_baseline/MANIFEST.json').read_text())
for item in up['files']:
    raw=(root/'tensor_baseline/upstream'/item['path']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==item['sha'], item['path']
checks=['certificate/overwritten/check_common_factor.py','certificate/overwritten/check.py','certificate/check.py','context/product/check.py','context/product/check_exponential.py','context/product/check_prefactor.py','context/coupled/check.py','tensor_baseline/check_absorbing_diffusion.py']
if a.numerical: checks+=['tensor_baseline/verify_killed_operator.py','tensor_baseline/diffusion_gate_probe.py']
records=[]
for path in checks:
    start=time.perf_counter();r=subprocess.run([sys.executable,str(root/path)],capture_output=True,text=True,cwd=root)
    assert r.returncode==0, f'{path} failed: {r.stderr} {r.stdout}'
    result=json.loads(r.stdout)
    if path=='tensor_baseline/check_absorbing_diffusion.py':
        assert result['upstream_executed'] is False
        assert all(abs(x['rate']-v)<1e-10 for x,v in zip(result['checks'],[131.5312,131.5312,0.0,123.3105]))
    records.append({'check':path,'passed':True,'seconds_descriptive':time.perf_counter()-start,'result':result})
result={'status':'PASS','python':platform.python_version(),'manifest_files_verified':len(manifest['files']),'upstream_git_blobs_verified':len(up['files']),'numerical_smoke_tests_included':a.numerical,'checks':records,'qualification':'Exact checks use Fraction arithmetic; floating numerical smoke tests are not interval certificates.'}
text=json.dumps(result,indent=2)
if a.output:a.output.write_text(text+'\n')
print(text)
