#!/usr/bin/env python3
import ast,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
import independent_variance as iv
ROOT=Path(__file__).resolve().parent
INPUTS=ROOT/'frozen_inputs'
VAR=INPUTS/'inverse_clock_variance_20261101'
SCALAR=INPUTS/'inverse_clearance_clock_20261101'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    binding=json.loads((ROOT/'RECEIPT_BINDINGS.json').read_text())
    for row in binding['files']:assert sha(ROOT/row['path'])==row['sha256'],row['path']
    for folder,name in [(VAR,'VARIANCE_FREEZE.json'),(SCALAR,'SCALAR_FREEZE.json')]:
        for row in json.loads((folder/name).read_text())['files']:
            assert sha(folder/row['path'])==row['sha256'],row['path']
    for row in json.loads((VAR/'SOURCE_BINDINGS.json').read_text())['sources']:
        assert sha(INPUTS/row['path'])==row['sha256'],row['path']
    for source in (VAR/'validated_variance.py',SCALAR/'validated_clock.py',ROOT/'independent_variance.py',ROOT/'independent_scalar.py'):
        tree=ast.parse(source.read_text())
        assert not any(isinstance(n,ast.Constant) and isinstance(n.value,float) for n in ast.walk(tree)),str(source)
    saved=json.loads((VAR/'VARIANCE_CERTIFICATE.json').read_text())
    assert saved['code_sha256']==sha(VAR/'validated_variance.py')
    assert saved['scalar_code_sha256']==sha(SCALAR/'validated_clock.py')
    result,expected=iv.check(VAR/'VARIANCE_CERTIFICATE.json')
    tests=subprocess.run([sys.executable,str(ROOT/'independent_tests.py')],check=True,capture_output=True,text=True)
    test_result=json.loads(tests.stdout)
    with tempfile.TemporaryDirectory(prefix='inverse_variance_author_replay_') as temp:
        output=Path(temp)/'replay.json'
        subprocess.run([sys.executable,str(VAR/'validated_variance.py'),'--output',str(output)],check=True,capture_output=True,text=True)
        replay=json.loads(output.read_text());iv.no_floats(replay)
        for key,value in saved.items():
            if key!='wall_nanoseconds_nonproof':assert replay[key]==value,key
    out={'status':'PASS_INDEPENDENT_DETERMINISTIC_CANDIDATE_VARIANCE_REVIEW',
      'receipt_bindings_sha256':sha(ROOT/'RECEIPT_BINDINGS.json'),'bound_files_verified':len(binding['files']),
      'variance_freeze_sha256':sha(VAR/'VARIANCE_FREEZE.json'),'scalar_freeze_sha256':sha(SCALAR/'SCALAR_FREEZE.json'),
      'all_source_bindings_verified':True,'source_float_literals_found':False,
      'independent_replay':result,'independent_tests':test_result,'fresh_author_replay_passed':True,
      'fresh_author_replay_nanoseconds_nonproof':replay['wall_nanoseconds_nonproof'],
      'actual_chain_CLT_accepted':False,'measured_SSA_variance_accepted':False,'finite_noise_variance_accepted':False}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
