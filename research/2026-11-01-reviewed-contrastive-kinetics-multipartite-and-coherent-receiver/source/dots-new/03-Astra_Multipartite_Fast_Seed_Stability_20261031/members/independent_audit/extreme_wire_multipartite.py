#!/usr/bin/env python3
"""Fresh-process exact wire/rate-size stress; no power or count-head expansion."""
from pathlib import Path
import json,subprocess,sys
HERE=Path(__file__).resolve().parent

def main():
    child=r'''
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,importlib.util
here=Path(sys.argv[1]);base=here.parent if (here.parent/'multipartite_seed.py').exists() else here.parent/'stochastic_multipartite_seed_pending_20261031'
before=sys.get_int_max_str_digits() if hasattr(sys,'get_int_max_str_digits') else None
sp=importlib.util.spec_from_file_location('candidate',base/'multipartite_seed.py');C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)
after=sys.get_int_max_str_digits() if hasattr(sys,'get_int_max_str_digits') else None
assert after in (0,None)
sys.path.insert(0,str(here));import independent_multipartite_receiver as I
cases=[]
for name in ['slow_death','large_reverse']:
 raw=C.fixture()
 if name=='slow_death':raw=[(u,v,F(1,10**5000) if sum(v)==0 else k) for u,v,k in raw]
 else:raw=[(u,v,F(10**1500) if u==(0,1,1,0) and v==(1,1,0,0) else k) for u,v,k in raw]
 cert=C.numerical(raw,F(2));assert cert['status']=='CERTIFIED_NUMERICAL'
 wire=C.canonical(cert);parsed=json.loads(wire)
 assert C.receive_numerical(raw,F(2),parsed) and I.receive_numerical(raw,F(2),parsed)
 r=I.parse(raw);N=cert['constants']['Nstar']
 for x in [(0,N,0,0),(1,N,0,0),(0,N,1,0),(0,N,N,N)]:I.verify_master(r,cert,x)
 assert cert['work']['rate_dependent_iterations']==0 and cert['work']['expanded_Foster_powers']==0
 cases.append({'case':name,'Nstar_decimal_digits':len(str(N)),'Nstar_bits':N.bit_length(),
  'wire_bytes':len(wire.encode()),'wire_sha256':hashlib.sha256(wire.encode()).hexdigest(),
  'retained_scalar_bits':cert['work']['retained_scalar_bits'],'exact_target_states':4})
print(json.dumps({'before_import_decimal_limit':before,'after_candidate_import_decimal_limit':after,'cases':cases,
 'rate_dependent_iterations':0,'expanded_Foster_powers':0,'head_states_enumerated':0},sort_keys=True))
'''
    ran=subprocess.run([sys.executable,'-c',child,str(HERE)],check=True,capture_output=True,text=True)
    result=json.loads(ran.stdout)
    assert all(c['wire_bytes']>4300 for c in result['cases'])
    result['status']='fresh-process candidate and independent roundtrips passed'
    result['scope']='Polynomial-bit proof is algebraic; these finite rate-size tests are corroboration only, not a resource guarantee.'
    return result
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
