import copy,json,sys
from fractions import Fraction as F
from pathlib import Path
import acquire_local_admission as m
import test_acquire_local_admission as t
checks=0
names=t.main();assert len(names)==93
s=t.fixture();r=m.acquire(s)
assert m.verify_admitted(s,r);checks+=1
# All integer leaves in the external model reject bool and float aliases.
def leaves(o,path=()):
 if type(o) is dict:
  for k,v in o.items():yield from leaves(v,path+(k,))
 elif type(o) is list:
  for k,v in enumerate(o):yield from leaves(v,path+(k,))
 elif type(o) is int:yield path
for path in leaves(s):
 for val in [True,1.0]:
  bad=copy.deepcopy(s);at=bad
  for x in path[:-1]:at=at[x]
  at[path[-1]]=val
  try:m.acquire(bad)
  except m.InputError:pass
  else:raise AssertionError(('alias admitted',path,val))
  assert not m.verify_certificate(bad,r);checks+=1
# Whole external-spec binding versus valid altered certificates.
for path in [('task','id'),('locations',0,'id')]:
 changed=copy.deepcopy(s);at=changed
 for x in path[:-1]:at=at[x]
 at[path[-1]]+='-changed'
 new=m.acquire(changed);assert m.verify_admitted(changed,new)
 assert not m.verify_certificate(s,new);checks+=1
for n in range(1,9):
 z=t.million();z['source_model']['n']=n;z['couplings'][0]['source']=0
 program=m.acquire(z)
 explicit=copy.deepcopy(z);q=z['source_model']
 explicit['source_model']={'mode':'explicit','sources':[{'loss_lower':q['loss_lower'],'injection_upper':q['injection_upper']} for _ in range(n)],'hopping':[{'i':i,'j':i+1,'real':q['hopping_real'],'imag':q['hopping_imag']} for i in range(n-1)]}
 table=m.acquire(explicit)
 assert program['parameters']==table['parameters'] and program['certificate']==table['certificate'];checks+=1
# Asynchronous partitions cannot hide an always-on two-qubit term.
z=t.fixture();z['couplings']=[dict(t.term(0,0),pauli=[[0,'X'],[1,'Z']])]
z['locations']=[t.loc(0,0),t.loc(1,1)]
try:m.acquire(z)
except m.InputError:checks+=1
else:raise AssertionError('straddling term')
# Zero coupling decouples even a supercritical source, with genuine control error.
z=t.fixture();z['couplings']=[];z['source_model']['hopping'][0]['real']=[10**12,1]
z['locations'][0]['control_error']['integrated_hamiltonian_bound']=[1,100000]
r=m.acquire(z);assert r['status']=='PASS' and r['parameters']['gamma_lower'][0]<0 and r['certificate']['eta_upper']==[1,100000];checks+=1
for stem in ['explicit_fixture','million_source_fixture']:
 spec=m.load(Path(__file__).parent/(stem+'_input.json'));cert=m.load(Path(__file__).parent/(stem+'_certificate.json'))
 assert m.verify_admitted(spec,cert);checks+=1
print(json.dumps({'author_checks':len(names),'additional_checks':checks,'scope':'Exact known-model acquisition and binding checks only; no physical evidence or threshold validation.'},indent=2))
