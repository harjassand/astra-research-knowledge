#!/usr/bin/env python3
"""Fresh-process exact-domain/serialization controls; no Foster-power expansion."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util,json,subprocess,sys
import independent_receiver as I
HERE=Path(__file__).resolve().parent
MAIN=HERE.parent if (HERE.parent/'compound_seed.py').exists() else HERE.parent/'stochastic_compound_seed_pending_20261031'
def load():
    sp=importlib.util.spec_from_file_location('candidate',MAIN/'compound_seed.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m

def main():
    C=load();raw=C.fixture();cases=[]
    for name,lam,mu in [('small_birth_fast_death',F(1,10**6),F(10**6)),('slow_death',F(1),F(1,10**5000))]:
        rr=[]
        for u,v,k in raw:
            if sum(u)==0:k=lam
            elif sum(v)==0:k=mu
            rr.append((u,v,k))
        c=C.numerical(rr,F(2),100000);assert I.receive_numerical(rr,F(2),c,100000)
        assert c['qualitative']['status']=='CERTIFIED_QUALITATIVE'
        row={'name':name,'status':c['status']}
        if c['status']=='CERTIFIED_NUMERICAL':
            r=I.parse(rr);N=c['constants']['Nstar']
            for x in [(0,N,0,0),(1,N,0,0),(2,N,0,0),(0,N,1,1),(3,N,2,2)]:I.verify_master(r,c,x)
            row['Nstar']=N
        else:assert c['work']=={'profile_recurrence_steps':0,'finite_head_checks':0}
        cases.append(row)
    aa=(2,0,0,0);hub=(0,0,1,1)
    noamp=[r for r in raw if (r[0],r[1]) not in [(aa,hub),(hub,aa)]]
    cert=C.qualitative(noamp);assert cert['reason']=='every hub needs 2A amplification pair'
    assert I.receive_qualitative(noamp,cert)
    # Fresh interpreter: candidate must itself remove the default wire guard before receiving imports.
    child=r'''
from pathlib import Path
from fractions import Fraction as F
import sys,json,importlib.util,hashlib
root=Path(sys.argv[1]); main=root.parent if (root.parent/'compound_seed.py').exists() else root.parent/'stochastic_compound_seed_pending_20261031'
before=sys.get_int_max_str_digits() if hasattr(sys,'get_int_max_str_digits') else None
sp=importlib.util.spec_from_file_location('candidate',main/'compound_seed.py');C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
after=sys.get_int_max_str_digits() if hasattr(sys,'get_int_max_str_digits') else None
assert after in (0,None)
raw=C.fixture();huge=10**5000
raw=[(u,v, F(huge) if u==(0,0,1,1) and v==(1,0,1,0) else k) for u,v,k in raw]
c=C.numerical(raw,F(2));assert c['status']=='CERTIFIED_NUMERICAL'
wire=C.canonical(c);decoded=json.loads(wire);assert C.receive_numerical(raw,F(2),decoded)
sys.path.insert(0,str(root));import independent_receiver as I
assert I.receive_numerical(raw,F(2),decoded)
r=I.parse(raw);N=c['constants']['Nstar']
for x in [(0,N,1,1),(1,N,0,0),(2,N,0,0)]:I.verify_master(r,c,x)
print(json.dumps({'before_import_decimal_limit':before,'after_candidate_import_decimal_limit':after,
 'wire_bytes':len(wire.encode()),'wire_sha256':hashlib.sha256(wire.encode()).hexdigest(),
 'retained_scalar_bits':c['work']['retained_scalar_bits'],'roundtrip':'candidate and independent accepted',
 'Foster_power_expanded':False},sort_keys=True))
'''
    childrun=subprocess.run([sys.executable,'-c',child,str(HERE)],check=True,text=True,capture_output=True)
    fresh=json.loads(childrun.stdout)
    assert fresh['wire_bytes']>4300 and fresh['retained_scalar_bits']>14000
    return {'status':'all extreme and fresh-process controls passed','rate_cases':cases,
      'missing_amplification_pair':'UNKNOWN verified independently','fresh_process':fresh}
if __name__=='__main__':print(json.dumps(I.wire(main()),sort_keys=True,indent=2))
