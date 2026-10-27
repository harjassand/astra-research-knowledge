"""Meaningful transport, count-only import, and rational replay checks."""
import hashlib,json,py_compile,subprocess,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
before=sha(ROOT/'rational_certificate.json')
scripts=['exact_certificate.py','residual_validation.py','compare_variants.py',
         'source_simplex_scan.py','overcomplete_fixture.py']
checks=[]
for script in scripts:
    child_code='''import builtins,runpy,sys
original=builtins.__import__
def checked(name,*args,**kwargs):
    if name.split('.')[0]=='plant':raise RuntimeError('FORBIDDEN_PRIVATE_PLANT_IMPORT')
    return original(name,*args,**kwargs)
builtins.__import__=checked
sys.path.insert(0,sys.argv[1])
runpy.run_path(sys.argv[2],run_name='__main__')
'''
    result=subprocess.run([sys.executable,'-c',child_code,str(ROOT),str(ROOT/script)],
        capture_output=True,text=True,timeout=60)
    assert result.returncode==0,(script,result.stdout,result.stderr)
    checks.append({'script':script,'replay':'PASS','private_plant_import_guard':'PASS'})
assert before==sha(ROOT/'rational_certificate.json')
for record in json.loads((ROOT/'ADDITIONAL_SOURCES.json').read_text()):
    assert sha(ROOT/'source_counts'/record['file'])==record['sha256']
for name in ['counts.json','residual_counts.json']:
    data=json.loads((ROOT/name).read_text())
    assert data['resets']==sum(t['shots'] for t in data['tables'])
    assert data['native_interventions']==sum(len(t['actions'])*t['shots'] for t in data['tables'])
    for table in data['tables']:assert sum(table['counts'].values())==table['shots']
for path in ROOT.glob('*.py'):py_compile.compile(str(path),doraise=True)
result={'scope':'Count-only import separation, exact replay, frozen-source hashes and integer cost accounting',
        'checks':checks,'primary_byte_identical':True,'frozen_copies_unchanged':True,
        'integer_count_costs':'PASS','owned_python_compile':'PASS',
        'mathematical_correctness_not_implied_by_hashes':True}
(ROOT/'REPLAY_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
