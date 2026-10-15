#!/usr/bin/env python3
"""Independent implementation regressions after the decimal-input finding.

All writes stay in this audit directory. This deliberately does not call
the construction compiler's self-check, which writes to its own directory.
"""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

import sympy as sp


OUT=Path(__file__).resolve().parent
CONSTRUCTION=OUT.parent/'full_invariant_genesis'/'flat_completion_compiler.py'
INITIAL=OUT/'PRE_CORRECTION_INPUT_FINDING.json'
CHECKS=[]
source=CONSTRUCTION.read_bytes()
namespace={'__name__':'independently_audited_compiler','__file__':str(CONSTRUCTION)}
exec(compile(source,str(CONSTRUCTION),'exec'),namespace)
analyse=namespace['analyse']


def check(name,condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append({'name':name,'status':'PASS'})


def data(coeffs,lam='0',reserve='0'):
    return {'coefficients':[str(q) for q in coeffs],'lambda':str(lam),'reserve':str(reserve)}


# Load an independent exact checker without executing its output-writing tail.
math_source=(OUT/'verify.py').read_text()
math_prefix=math_source[:math_source.index('\nfixtures=[')]
independent={'__name__':'independent_certificate_checker','__file__':str(OUT/'verify.py')}
exec(compile(math_prefix,str(OUT/'verify.py'),'exec'),independent)
own_certificate=independent['certificate']
V=independent['V']
u,v,w,j,H=(independent[q] for q in ('u','v','w','j','H'))
hvec=[1,1,6,-4,0,0,-4,-4,0]
fixtures=[
    ('rank4 radial',[1,1,2,0,0,0,0,0,0],(u+v)**2,sp.Integer(0)),
    ('rank4 nonzero lambda',[1,1,2,0,0,0,0,0,0],(u+v)**2,sp.Integer(1)),
    ('rank3 contact',[0,1,0,1,0,0,0,0,0],w*w+v*v,sp.Integer(0)),
    ('rank3 contact negative lambda',[0,sp.Rational(3,4),0,1,0,0,0,-1,0],
     w*w-v*j+sp.Rational(3,4)*v*v,sp.Integer(-3)),
    ('rank2 column',[0,1,0,0,0,0,0,0,0],v*v,sp.Integer(0)),
    ('rank2 nonstandard kernel',[1,16,8,16,8,32,0,0,0],(u+4*v+4*w)**2,sp.Integer(0)),
    ('rank1 extra flatness fails',[0,0,1,-1,0,0,0,0,0],j*j,sp.Integer(2)),
    ('rank0 negative H',[-3*q for q in hvec],-3*H,sp.Integer(0)),
    ('rank0 zero',[0]*9,sp.Integer(0),sp.Integer(0)),
    ('non-PSD supplied lambda',[0,1,0,0,0,0,0,0,0],v*v,sp.Integer(1)),
]
comparisons=[]
for name,coeffs,polynomial,lam in fixtures:
    own=own_certificate(name,polynomial,lam)
    actual=analyse(data(coeffs,lam,reserve='2/3'))
    admitted=own['admission']=='PASS'
    check(name+' admission agrees', (actual['status']=='ADMITTED')==admitted)
    if admitted:
        check(name+' rank agrees',actual['rank']==own['rank'])
        check(name+' threshold agrees',sp.Rational(actual['sufficient_alpha'])==sp.Rational(own['alpha_star']))
        check(name+' reserve agrees',sp.Rational(actual['output_alpha'])==sp.Rational(own['alpha_star'])+sp.Rational(2,3))
        check(name+' margin agrees',sp.Rational(actual['gradient_L4_margin'])==sp.Rational(8,5625))
        if own['rank']:
            check(name+' kappa agrees',sp.Rational(actual['kappa'])==sp.Rational(own['kappa']))
            check(name+' expanded coefficient norm agrees',sp.Rational(actual['tensor_bound_M'])==sp.Rational(own['M']))
            check(name+' matrix basis agrees',actual['Q']==own['matrix'])
    comparisons.append({'name':name,'independent':own,'construction_status':actual['status']})


CLI=OUT/'corrected_cli_cases'
CLI.mkdir(exist_ok=True)


def run_cli(name,raw):
    inp=CLI/(name+'.input.json')
    out=CLI/(name+'.output.json')
    inp.write_text(raw+'\n')
    proc=subprocess.run([sys.executable,str(CONSTRUCTION),'--input',str(inp),'--output',str(out)],
                        capture_output=True,text=True)
    record={'name':name,'exit_code':proc.returncode,'stderr':proc.stderr}
    if proc.returncode==0:
        record['result']=json.loads(out.read_text())
    (CLI/(name+'.execution.json')).write_text(json.dumps(record,indent=2)+'\n')
    return record


# Exact replay of the originally failing literal.
exact_decimal=run_cli('long_decimal',
    '{"coefficients":[0,1.00000000000000000001,0,0,0,0,0,0,0],"lambda":0,"reserve":0}')
expected=sp.Rational('1.00000000000000000001')
check('long decimal CLI preserves original exact value',exact_decimal['exit_code']==0 and
      sp.Rational(exact_decimal['result']['coefficients'][1])==expected)

scientific=run_cli('long_scientific',
    '{"coefficients":[0,1.00000000000000000001e-7,0,0,0,0,0,0,0],"lambda":0,"reserve":0}')
check('scientific decimal CLI preserves original exact value',scientific['exit_code']==0 and
      sp.Rational(scientific['result']['coefficients'][1])==sp.Rational('1.00000000000000000001e-7'))

lambda_and_reserve=run_cli('lambda_and_reserve',
    '{"coefficients":[1,1,2,0,0,0,0,0,0],"lambda":1.00000000000000000001e-20,"reserve":0.123456789012345678901}')
check('supplied lambda decimal preserved',lambda_and_reserve['exit_code']==0 and
      sp.Rational(lambda_and_reserve['result']['lambda'])==sp.Rational('1.00000000000000000001e-20'))
check('reserve decimal preserved',lambda_and_reserve['exit_code']==0 and
      sp.Rational(lambda_and_reserve['result']['reserve'])==sp.Rational('0.123456789012345678901'))
check('exact rational reserve margin preserved',sp.Rational(lambda_and_reserve['result']['gradient_L4_margin'])==
      sp.Rational(4,1875)*sp.Rational('0.123456789012345678901'))

for token in ('NaN','Infinity','-Infinity'):
    rr=run_cli('reject_'+token.replace('-','negative_'),
        '{"coefficients":[0,'+token+',0,0,0,0,0,0,0],"lambda":0,"reserve":0}')
    check('nonfinite CLI token rejected: '+token,rr['exit_code']!=0)

negative=run_cli('negative_reserve',
    '{"coefficients":[0,1,0,0,0,0,0,0,0],"lambda":0,"reserve":-0.00000000000000000000000000001}')
check('negative rational reserve rejected',negative['exit_code']!=0)

# A caller that already rounded a scalar to float cannot recover the input.
# The exact interface must reject such direct Python and SymPy float inputs.
for name,edit in (
    ('Python float coefficient',lambda q:q['coefficients'].__setitem__(1,1.0)),
    ('SymPy float coefficient',lambda q:q['coefficients'].__setitem__(1,sp.Float('1.00000000000000000001'))),
    ('Python float lambda',lambda q:q.__setitem__('lambda',0.0)),
    ('Python float reserve',lambda q:q.__setitem__('reserve',0.5)),
):
    inp=data([0,1,0,0,0,0,0,0,0])
    edit(inp)
    rejected=False
    try:
        analyse(inp)
    except (TypeError,ValueError):
        rejected=True
    check(name+' rejected at scalar boundary',rejected)

check('construction source stable during independent audit',CONSTRUCTION.read_bytes()==source)
initial=json.loads(INITIAL.read_text())
check('initial bug finding remains retained',initial['input_preserved_exactly'] is False)
check('corrected compiler differs from preserved initial compiler',sha256(source).hexdigest()!=initial['compiler_sha256'])

result={'status':'IMPLEMENTATION_AND_INPUT_BOUNDARY_PASS','checks':CHECKS,
        'exact_check_count':len(CHECKS),'independent_fixtures':comparisons,
        'corrected_compiler_sha256':sha256(source).hexdigest(),
        'pre_correction_compiler_sha256':initial['compiler_sha256'],
        'scope':'Exact certificate implementation and input preservation; no external mathematical review or formal verification.',
        'lambda_contract':'Rational lambda is supplied as part of the certificate; finding feasible lambda is not free.'}
(OUT/'implementation_verification.json').write_text(json.dumps(result,indent=2)+'\n')
files=['verify.py','verification.json','receipt.json','REPORT.md','verify_implementation.py',
       'implementation_verification.json','PRE_CORRECTION_INPUT_FINDING.json',
       'pre_correction_decimal_input.json','pre_correction_decimal_output.json','ADDENDUM_IMPLEMENTATION.md']
receipt={'recorded_utc':datetime.now(timezone.utc).isoformat(),'status':result['status'],
         'file_sha256':{name:sha256((OUT/name).read_bytes()).hexdigest() for name in files if (OUT/name).exists()},
         'corrected_compiler_sha256':result['corrected_compiler_sha256'],
         'pre_correction_compiler_sha256':result['pre_correction_compiler_sha256'],
         'prior_nonshear_audit_modified':False,'construction_sources_modified_by_auditor':False,
         'external_review':'NOT_PERFORMED','formal_verification':'NOT_PERFORMED'}
(OUT/'implementation_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':result['status'],'exact_checks':len(CHECKS),'fixtures':len(fixtures),
                  'corrected_compiler_sha256':result['corrected_compiler_sha256']},indent=2))
