"""Exact isometry/parameter checks; floating log/exponential diagnostics labelled."""
import sympy as S
from fractions import Fraction as F
from math import comb, log, exp, ceil, sqrt
import json
from pathlib import Path
I=S.eye(2); X=S.Matrix([[0,1],[1,0]]); Y=S.Matrix([[0,-S.I],[S.I,0]]); Z=S.diag(1,-1)
def tensor(a):
 out=a[0]
 for b in a[1:]: out=S.kronecker_product(out,b)
 return out
E=S.zeros(16,2)
for x,a in [(5,1),(6,-1),(9,-1),(10,1)]: E[x,0]=S.Rational(a,2)
for x,a in [(3,2),(12,2),(5,-1),(6,-1),(9,-1),(10,-1)]: E[x,1]=a/(2*S.sqrt(3))
assert S.simplify(E.T*E)==S.eye(2)
for pauli in (X,Y,Z):
 J=S.zeros(16)
 for i in range(4): J+=tensor([pauli if k==i else I for k in range(4)])/2
 assert S.simplify(J*E)==S.zeros(16,2)
# Standard finite completion: exact Gram-Schmidt on E columns then basis vectors.
cols=[E[:,0],E[:,1]]
for j in range(16):
 v=S.eye(16)[:,j]
 for c in cols: v=S.simplify(v-c*(c.T*v)[0])
 norm=S.simplify((v.T*v)[0])
 if norm: cols.append(S.simplify(v/S.sqrt(norm)))
 if len(cols)==16: break
U=S.Matrix.hstack(*cols)
assert S.simplify(U.T*U)==S.eye(16)
assert U[:,:2]==E
# Encoder input ordering is |000>_ancilla tensor |logical>; inverse U is decoder
# then measure ancillas and RESET logical on any nonzero syndrome.
# Canonical reset Kraus operators, checked exactly for trace preservation.
ks=[E.T]
for syndrome in range(1,8):
 for logical in range(2):
  k=S.zeros(2,16); k[0,:]=U.T[2*syndrome+logical,:]; ks.append(k)
assert sum((k.T*k for k in ks),S.zeros(16))==S.eye(16)
# A finite two-level Givens decomposition
# exists in dimension16; this script does NOT claim an elementary-gate netlist.
assert F(48*10,250000)<F(1,512)
rows=[]
for h in range(5,13):
 B=2**h;n=4*h;t=B//8;b=B//32;N=t+b+1
 assert t-b+1>=F(3*B,32) and N<=F(3*B,16)
 C=F(n+2,n-1);s=1/(1+C)
 assert s>=F(1,3) and 1-s<=F(2,3)
 tail=F(sum(comb(N,k) for k in range(b+1)),2**N)
 eps=exp(-3*B/128)
 assert float(tail)<=eps
 g=.35;delta=.05;ell=log(25*(n-1)/delta)
 m=ceil(450500000*n*ell/g**2)
 e=(31*ell+sqrt((31*ell)**2+1800*m*ell))/m
 assert e<=g/(500*sqrt(n))
 rows.append(dict(h=h,B=B,n=n,t=t,b=b,matching_cost=str(C),service_probability=str(s),
 soundness_exact_fraction=str(tail),soundness_float=float(tail),soundness_bound_float=eps,
 acceptance_lower_float=1-delta-exp(-B/4)-exp(-(4*log(4)-3)*B/128),
 g0=g,delta=delta,training_cap=m,matrix_radius_float=e,
 payload_qubits=h*(B-4*t),exposure_ratio_float=h*(B-4*t)/(n*(m+6*B))))
out=dict(scope='Exact four-spin isometry and finite completion, rational guard parameters/tails; logarithmic sample and exponential bounds evaluated floating for diagnostics.',isometry_exact=True,three_collective_generators_annihilate_exact=True,completion_16x16_exact=True,canonical_reset_trace_preserving_exact=True,praw_constant_comparison_exact=True,rows=rows)
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n')
Path(__file__).with_name('four_spin_unitary_exact.txt').write_text(str(U)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
print(json.dumps(rows[6],indent=2))
