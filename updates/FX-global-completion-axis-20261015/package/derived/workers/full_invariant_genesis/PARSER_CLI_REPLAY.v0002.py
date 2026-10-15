"""End-to-end exact-input regression, independent of compiler imports."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
FIXTURES=HERE/'parser_regressions_v0002'
FIXTURES.mkdir(exist_ok=True)
COMPILER=HERE/'flat_completion_compiler.py'
checks=[]
runs=[]


def run_case(name,payload,valid=True):
    source=FIXTURES/(name+'.json')
    output=FIXTURES/(name+'.result.json')
    source.write_text(payload+'\n')
    # Outputs are this replay's own generated files; a rejected input must
    # not leave a previous successful output looking current.
    if output.exists():
        output.unlink()
    proc=subprocess.run([sys.executable,str(COMPILER),'--input',str(source),
                         '--output',str(output)],capture_output=True,text=True)
    if valid:
        assert proc.returncode==0,(name,proc.stderr)
        assert output.is_file(),name
        result=json.loads(output.read_text())
    else:
        assert proc.returncode==2,(name,proc.returncode,proc.stderr)
        assert not output.exists(),name
        assert 'error:' in proc.stderr,name
        result=None
    runs.append({'name':name,'returncode':proc.returncode,
                 'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                 'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest() if output.exists() else None,
                 'stderr':proc.stderr if not valid else ''})
    return result


decimal=run_case('decimal_literal','{"coefficients":[0,0.75,0,1.00000000000000000001,0,0,0,-1,0],"lambda":-3,"reserve":0}')
rational=run_case('decimal_rational_equivalent',json.dumps({
    'coefficients':['0','3/4','0','100000000000000000001/100000000000000000000','0','0','0','-1','0'],
    'lambda':'-3','reserve':'0'}))
assert decimal==rational
assert decimal['coefficients'][3]=='100000000000000000001/100000000000000000000'
checks.append('long JSON decimal gives the identical complete certificate as its exact rational string')

scientific=run_case('scientific_literal','{"coefficients":[-7e0,-7e0,-4.2e1,2.8e1,0,0,2.8e1,2.8e1,0],"lambda":0e0,"reserve":1.234567890123456789e-23}')
scientific_rational=run_case('scientific_rational_equivalent',json.dumps({
    'coefficients':['-7','-7','-42','28','0','0','28','28','0'],
    'lambda':'0','reserve':str(1234567890123456789)+'/'+str(10**41)}))
assert scientific==scientific_rational
assert scientific['output_alpha']=='700000000000000000000001234567890123456789/100000000000000000000000000000000000000000'
checks.append('signed scientific JSON notation gives the identical complete certificate as exact rational strings')

example=run_case('original_rational_example',(HERE/'EXAMPLE_INPUT.json').read_text().strip())
assert example==json.loads((HERE/'EXAMPLE_COMPILED.json').read_text())
checks.append('the original exact rational example output is unchanged')

invalid=[
    ('negative_reserve','{"coefficients":[0,0.75,0,1,0,0,0,-1,0],"lambda":-3,"reserve":-1}'),
    ('nonfinite_scalar','{"coefficients":[0,0.75,0,1,0,0,0,-1,0],"lambda":NaN}'),
    ('binary_boolean_scalar','{"coefficients":[0,0.75,0,true,0,0,0,-1,0],"lambda":-3}'),
]
for name,payload in invalid:
    run_case(name,payload,valid=False)
    checks.append(name+' is rejected by the CLI with exit code 2 and no result file')

baseline=json.loads((HERE/'PARSER_CORRECTION_BASELINE.v0001.json').read_text())
unchanged={}
for name,rec in baseline['files'].items():
    if 'unchanged_sha256' in rec:
        digest=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
        assert digest==rec['unchanged_sha256'],name
        unchanged[name]=digest

receipt={
    'status':'PASS',
    'version':2,
    'scope':'Exact CLI input parsing, unchanged rational outputs, and invalid-input guards only; no theorem changes.',
    'check_count':len(checks),
    'checks':checks,
    'runs':runs,
    'protected_artifacts_unchanged':unchanged,
    'compiler_sha256':hashlib.sha256(COMPILER.read_bytes()).hexdigest(),
    'replay_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
output=HERE/'PARSER_CLI_RECEIPT.v0002.json'
output.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':'PASS','check_count':len(checks),'receipt':str(output)},indent=2))
