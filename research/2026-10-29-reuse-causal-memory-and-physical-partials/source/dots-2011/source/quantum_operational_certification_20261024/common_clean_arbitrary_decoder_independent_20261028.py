#!/usr/bin/env python3
"""Known CPTP decoder with a genuinely non-Pauli bad decoded branch."""
import itertools,json
from pathlib import Path
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Z=s.diag(1,-1)
k=s.kronecker_product
R=(3*I-4*s.I*Z)/5
CN=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
Enc=s.zeros(4,2);Enc[0,0]=1;Enc[3,1]=1
C=k(I,s.diag(1,0))+k(R,s.diag(0,1))
def clean(A):return A.applyfunc(s.expand)
def decode(A):
    B=C*CN*A*CN.H*C.H
    return clean(s.Matrix(2,2,lambda i,j:sum(B[2*i+a,2*j+a] for a in range(2))))
entries=0
for i,j in itertools.product(range(2),repeat=2):
    E=s.zeros(2);E[i,j]=1
    assert decode(Enc*E*Enc.H)==E
    assert decode(k(I,X)*Enc*E*Enc.H*k(I,X))==clean(R*E*R.H)
    entries+=8
phi=s.Matrix([[1,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,1]])/2
phiR=clean(k(I,R)*phi*k(I,R.H))
# A Pauli mixture has no off-diagonal Bell-basis matrix element. This one does.
phiI_vec=s.Matrix([1,0,0,1]);phiZ_vec=s.Matrix([1,0,0,-1])
off=s.expand((phiI_vec.H*phiR*phiZ_vec)[0]/2)
assert off==12*s.I/25
p=s.Rational(1,4);b=s.Rational(1,5)
real=(1-p)*k(phi,s.diag(1,0))+p*k(phiR,s.diag(0,1))
ideal=k(phi,s.diag(1-p,p));common=(1-b)*(1-p)*k(phi,s.diag(1,0))
# Explicit positive residuals, no logical Pauli representation of R required.
assert clean(real-common)==clean(b*(1-p)*k(phi,s.diag(1,0))+p*k(phiR,s.diag(0,1)))
assert clean(ideal-common)==clean(b*(1-p)*k(phi,s.diag(1,0))+p*k(phi,s.diag(0,1)))
lam=s.symbols('lam')
assert s.expand((p*(phiR-phi)).charpoly(lam).as_expr()-lam**2*(lam-s.Rational(1,5))*(lam+s.Rational(1,5)))==0
out={'status':'PASS_KNOWN_CODE_COMMON_SUBCHANNEL_WITH_NON_PAULI_BAD_DECODER',
     'source_calls':0,'random_draws':0,'exact_decoded_matrix_entries':entries,
     'good_physical_patterns':['II'],'bad_physical_pattern':'IX',
     'bad_logical_channel':'Ad_((3I-4iZ)/5), not a Pauli mixture',
     'off_diagonal_Bell_matrix_element':str(off),
     'exact_tagged_Bell_half_distance':'1/5','native_bad_effect':'1/4',
     'positive_common_subchannel_residuals':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
