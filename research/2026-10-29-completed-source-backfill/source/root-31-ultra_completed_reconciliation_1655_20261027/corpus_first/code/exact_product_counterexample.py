"""Rational gate, rational separating witness, and exact225 inequalities."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json
import numpy as np
import sympy as S
from exact_instrument import projector,clean,R,D
from direct_polytope import library
from product_witness_search import unhc
BASE=Path(__file__).resolve().parents[1]

def rational_unit(v,den=1024):
 v=np.asarray(v,complex);pivot=int(np.argmax(abs(v)))
 v=v*np.exp(-1j*np.angle(v[pivot]));other=[j for j in range(len(v)) if j!=pivot]
 ts=[(R(round(float(v[j].real/(1+v[pivot].real))*den),den),R(round(float(v[j].imag/(1+v[pivot].real))*den),den)) for j in other]
 total=sum((a*a+b*b for a,b in ts),R(0));out=S.zeros(len(v),1)
 out[pivot]=(1-total)/(1+total)
 for j,(a,b) in zip(other,ts):out[j]=2*(a+S.I*b)/(1+total)
 assert S.expand((out.H*out)[0])==1
 return clean(out)

def phi2(rho,c=R(9,5)):
 ra=S.Matrix(D,D,lambda i,k:sum(rho[D*i+j,D*k+j] for j in range(D)))
 rb=S.Matrix(D,D,lambda j,l:sum(rho[D*i+j,D*i+l] for i in range(D)))
 return clean((c*c*S.trace(rho)*S.eye(D*D)-c*S.kronecker_product(ra.T,S.eye(D))-c*S.kronecker_product(S.eye(D),rb.T)+rho.T)/(c*D-1)**2)

def replay():
 raw=json.loads((BASE/'results'/'PRODUCT_THRESHOLD_FAILURE.json').read_text())
 Wf=unhc(np.array(raw['witness']))
 W=S.Matrix(D*D,D*D,lambda i,j:R(float(Wf[i,j].real)).limit_denominator(10000)+S.I*R(float(Wf[i,j].imag)).limit_denominator(10000))
 assert W==W.H and S.trace(W)==1
 vals=[S.expand(S.trace(W*S.kronecker_product(a,b))) for a in library()[0] for b in library()[0]]
 assert all(v>=0 for v in vals)
 v=rational_unit(np.array(raw['state_real'])+1j*np.array(raw['state_imag']))
 # Rational complex Householder from the chosen computational basis input.
 pivot=int(np.argmax(abs(np.array(raw['state_real'])+1j*np.array(raw['state_imag']))))
 assert S.im(v[pivot])==0
 e=S.eye(D*D)[:,pivot];u=e-v
 U=clean(S.eye(D*D)-projector(u)/(1-v[pivot]))
 assert clean(U.H*U)==S.eye(D*D) and clean(U*e)==v
 out=phi2(projector(v));value=S.expand(S.trace(W*out))
 assert value<0
 artifact=dict(input_basis_index=pivot,c='9/5',W=[[str(x) for x in row] for row in W.tolist()],
  gate=[[str(x) for x in row] for row in U.tolist()],state=[str(x) for x in v],
  exact_witness_value=str(value),witness_float=float(value),
  product_inequalities=len(vals),minimum_product_value=str(min(vals)),
  zero_product_inequalities=sum(x==0 for x in vals),
  conclusion='Single-frame closure does not imply closure of its tensor product; no classical-simulation or separability no-go.')
 (BASE/'results'/'EXACT_PRODUCT_COUNTEREXAMPLE.json').write_text(json.dumps(artifact,indent=2)+'\n')
 print(json.dumps({k:v for k,v in artifact.items() if k not in ('W','gate','state')},indent=2))
 return U,W,v

if __name__=='__main__':replay()
