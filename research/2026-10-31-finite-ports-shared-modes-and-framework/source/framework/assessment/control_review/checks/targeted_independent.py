"""Small independent matrix check of the claimed moving-bath mechanism.

These finite floating-point checks support only their displayed scales.
They do not establish the continuum or adversarial-bath theorems.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import importlib.util
import numpy as np
from fractions import Fraction as Q
from itertools import product
import json
from math import factorial

ROOT = Path('producer-workspace/control')
OUT = Path(__file__).resolve().parent

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec); sys.modules[name]=m
    spec.loader.exec_module(m); return m

# Replay the exact second checkpoint without importing any original run.
load('exact_word_check',ROOT/'block2/checkpoint/exact_word_check.py').main()
load('checkpoint2_moving',ROOT/'block2/checkpoint/exact_moving_expansion.py').main()
load('checkpoint2_constants',ROOT/'block2/checkpoint/proof_constants.py').main()

# Reconstruct the word, waveform and matrix propagator independently of all
# continuation helper modules, using explicit 8x8 Hermitian exponentials.
def inv(w): return [(a,-s) for a,s in w[::-1]]
def comm(u,v): return inv(v)+inv(u)+v+u
w=comm([('B',1)],[('C',1)])
for _ in range(3): w=comm([('A',1)],w)
assert len(w)==46
w=[(j,-s if j=='C' else s) for j,s in w]
w=w+w[::-1]

primitive=Q(0); angle=Q(0); hs=[]; mu={j:Q(0) for j in 'ABC'}
for j,s in w:
    end=primitive+(s if j=='A' else 0)
    midpoint=(primitive+end)/2
    h=int(midpoint>0)-int(midpoint<0)
    hs.append(h)
    mu[j]+=s*(angle+Q(h,2)); angle+=h; primitive=end
assert mu=={'A':Q(-130),'B':Q(-28),'C':Q(28)}
assert angle==primitive==0

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)
def kron(a,b,c): return np.kron(np.kron(a,b),c)
J={'A':kron(X,I,X),'B':kron(I,X,Y),'C':kron(Y,I,Z)}
z1=kron(Z,I,I); zmem=kron(I,I,Z)
rows=[]
for d in (.01,.005,.0025):
    heis=np.zeros((8,8),complex)
    for a,b in product((-1,1),repeat=2):
        signs={'A':a,'B':b,'C':a*b}; u=np.eye(8,dtype=complex)
        for (j,s),h in zip(w,hs):
            H=signs[j]*s*J[j]+h*zmem/2
            eigenvalues,eigenvectors=np.linalg.eigh(H)
            u=((eigenvectors*np.exp(-1j*d*eigenvalues))@eigenvectors.conj().T)@u
        heis+=u.conj().T@z1@u/4
    lam=1-33800*d**4+float(Q(16701716,3))*d**6-float(Q(1425644383,6))*d**8
    residual=float(np.linalg.norm(heis-lam*z1,2))
    coeff=float(np.trace(z1@heis).real/8)
    remainder_bound=(276*d)**10/factorial(10)
    assert residual<remainder_bound+2e-12
    rows.append({'d':d,'coefficient_of_Z1':coeff,'residual_from_degree8_formula':residual,
                 'degree10_unitary_integral_remainder_bound':remainder_bound})

# Verify the rational exponential-law endpoint constants directly.
def squared_error(x): return (x*x-2*x+2)/(1+x*x)
mean=Q(11,30)
ends=[squared_error(2*mean*h) for h in (1,8)]
assert max(ends)==Q(5554,7969)
result={'independent_matrix_checks':rows,
        'rational_exponential_law_endpoint_squared_errors':list(map(str,ends)),
        'note':'Finite matrix checks only; no continuum claim inferred.'}
(OUT/'targeted_independent.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
