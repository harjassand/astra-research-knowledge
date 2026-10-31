#!/usr/bin/env python3
"""Independent exact task/certificate and saved modular-witness checks."""
import json,itertools,inspect,copy
from pathlib import Path
import sympy as sp
from learn import acquire,encode,evaluate,exact,fixture,metric
from verify import verify

def checked(A,b,c,r):
 if 'expected_length' in inspect.signature(verify).parameters:
  return verify(A,b,c,r,expected_length=r['length'],expected_tolerance=sp.Rational(r['tolerance']))
 return verify(A,b,c,r)

def run():
 checks=0
 pi=sp.Matrix([sp.Rational(4,10),sp.Rational(3,10),sp.Rational(2,10),sp.Rational(1,10)])
 mats=[]
 for cycle in [[0,1,2,3],[0,2,1,3]]:
  A=sp.eye(4)
  for i,j in zip(cycle,cycle[1:]+cycle[:1]):
   rate=sp.Rational(1,30)/pi[i];A[i,i]-=rate;A[i,j]+=rate
  mats.append(A)
 assert metric(mats)[0]==pi;checks+=1
 assert mats[0]!=sp.diag(*pi).inv()*mats[0].T*sp.diag(*pi);checks+=1
 b=sp.Matrix([1,0,-1,0]);c=sp.Matrix([0,1,0,-1])
 for kernels in [mats,[(1-sp.Rational(1,5))*A+sp.Rational(1,5)*sp.ones(4,1)*pi.T for A in mats]]:
  model=acquire(kernels,b,c,5,sp.Rational(1,100));r=encode(model)
  assert checked(kernels,b,c,r);checks+=1
  for l in range(6):
   for w in itertools.product(range(2),repeat=l):
    assert (exact(kernels,b,c,pi,w)-evaluate(model,w))**2<=model['quadratic_error_bound_squared'];checks+=1
 # Adversarial requested-task binding and strict certificate parsing.
 fixed_length=5;fixed_tol=sp.Rational(1,100)
 def vrec(rec,**kw):
  return verify(kernels,b,c,rec,expected_length=kw.get('length',fixed_length),expected_tolerance=kw.get('tol',fixed_tol))
 for key,value in [('length',0),('tolerance','1'),('length',True),('alpha','0')]:
  bad=copy.deepcopy(r);bad[key]=value;assert not vrec(bad);checks+=1
 for value in [None,[],True,'record']:
  assert not vrec(value);checks+=1
 for value in [True,1.0,'1']:
  bad=copy.deepcopy(r);bad['basis'][0][0][0]=value;assert not vrec(bad);checks+=1
 assert not vrec(r,length=True);checks+=1
 assert not vrec(r,tol=0.01);checks+=1
 for zero_b,zero_c in [(True,False),(False,True),(True,True)]:
  bb=sp.zeros(4,1) if zero_b else b;cc=sp.zeros(4,1) if zero_c else c
  zz=acquire(kernels,bb,cc,5,fixed_tol)
  assert verify(kernels,bb,cc,encode(zz),expected_length=5,expected_tolerance=fixed_tol)
  assert evaluate(zz,[0,1,0])==0;checks+=1
 from algebra_witness import witness
 for badprime in [True,1000000,1000000000039]:
  try:witness(kernels,badprime)
  except ValueError:checks+=1
  else:raise AssertionError('invalid/unsafe modular interface admitted')
 # Saved full-algebra witness, replayed using unbounded Python integer arithmetic.
 saved=json.loads(Path(__file__).with_name('algebra_witness.json').read_text())['perturbed']
 p=saved['prime'];assert sp.isprime(p);A,_,_=fixture();d=A[0].rows-1
 T=sp.Matrix.vstack(sp.eye(d),-sp.ones(1,d))
 R=[]
 for M in A:
  B=(M*T)[:d,:];assert M*T==T*B
  R.append([[int(x.p)%p*pow(int(x.q)%p,-1,p)%p for x in B.row(i)] for i in range(d)])
 def mul(X,Y):return [[sum(X[i][k]*Y[k][j] for k in range(d))%p for j in range(d)] for i in range(d)]
 pivots={}
 for word in saved['word_witnesses']:
  M=[[int(i==j) for j in range(d)] for i in range(d)]
  for a in word:M=mul(M,R[a])
  v=sum(M,[])
  for k,u in sorted(pivots.items()):
   z=v[k]
   if z:v=[(x-z*y)%p for x,y in zip(v,u)]
  nz=next((i for i,x in enumerate(v) if x),None)
  assert nz is not None
  z=pow(v[nz],-1,p);pivots[nz]=[(x*z)%p for x in v]
 assert len(pivots)==d*d==121;checks+=1
 return {'scope':'Independent exact nonreversible/metric/gap tests and Python-integer replay of saved full modular algebra witness; not a strong-baseline performance comparison.', 'checks':checks,'saved_modular_rank':len(pivots),'nonreversible_exhaustive_words':126}
if __name__=='__main__':
 out=run();Path(__file__).with_name('independent_reuse_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
