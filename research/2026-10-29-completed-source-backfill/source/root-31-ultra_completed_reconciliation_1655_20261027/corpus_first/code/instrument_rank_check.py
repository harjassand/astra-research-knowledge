"""Exact full reachable/observable rank and nontrivial output memory."""
import sys
sys.dont_write_bytecode=True
import json,time
from pathlib import Path
import numpy as np
from scipy.linalg import qr
from exact_instrument import *
from compile_classical import coordinates
BASE=Path(__file__).resolve().parents[1]

def heisenberg(A,X):return clean(A.H*phi(X)*A)
def generate(maps,initial,act):
 states=[initial];layer=[initial]
 for length in range(2):
  layer=[act(m['A'],v) for v in layer for m in maps];states+=layer
 return states

def exact_minor(mats):
 C=S.Matrix.hstack(*[S.Matrix(coordinates(M)) for M in mats])
 num=np.array(C,dtype=float);_,_,perm=qr(num,pivoting=True,mode='economic')
 selected=list(map(int,perm[:D*D]));det=C[:,selected].det(method='domain-ge')
 assert det!=0
 return dict(columns=selected,exact_minor=str(det),rank=D*D)

def run():
 t=time.monotonic();maps=model();rho=S.eye(D)/D
 reach=exact_minor(generate(maps,rho,branch));obs=exact_minor(generate(maps,S.eye(D),heisenberg))
 p=S.trace(branch(maps[0]['A'],rho));p00=S.trace(branch(maps[0]['A'],branch(maps[0]['A'],rho)))
 assert p00-p*p!=0
 ex=json.loads((BASE/'results'/'EXACT_PRODUCT_COUNTEREXAMPLE.json').read_text())
 v=S.Matrix([S.sympify(x) for x in ex['state']]);rank=v.reshape(D,D).rank();assert rank>1
 result=dict(hankel_rank=D*D,classical_state_lower_bound=D*D,classical_state_upper_bound=15,
  reachable=reach,observable=obs,p0=str(p),p00=str(p00),p00_minus_p0_squared=str(S.factor(p00-p*p)),
  gate_output_schmidt_rank=rank,
  non_EB_branches='Each invertible prefilter preserves the negative inertia of the partially transposed Werner Choi matrix.',
  elapsed_seconds=time.monotonic()-t)
 (BASE/'results'/'INSTRUMENT_RANK.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ('reachable','observable')},indent=2))

if __name__=='__main__':run()
