"""Exact bounded checks of the fixed pure-input witness; not a universal proof."""
from pathlib import Path
import json
import sympy as s

eps=s.Rational(1,8); r=s.Rational(1,2)
D=3

def phi(A,t):
    C=s.Matrix([[t,1],[0,t]])
    R=r*s.eye(2)-eps*C.T*C
    X=A[1:3,1:3]
    B=s.zeros(D)
    B[0,0]=A[0,0]+(1-r)*s.trace(X)
    B[0:1,1:3]=eps*A[0:1,1:3]*C.T
    B[1:3,0:1]=eps*C*A[1:3,0:1]
    B[1:3,1:3]=eps*C*X*C.T+s.trace(R*X)*s.eye(2)/2
    return B

psi=s.zeros(6,1);psi[0]=1;psi[4]=1
rho=psi*psi.T/2
assert rho.rank()==1 and s.trace(rho)==1
rows=[]
for t in [s.Rational(1,16),s.Rational(-1,16),s.Rational(1,4),s.Rational(-1,4)]:
    output=rho
    for n in range(1,13):
        output=s.BlockMatrix([[phi(output[a*3:(a+1)*3,b*3:(b+1)*3],t)
                               for b in range(2)] for a in range(2)]).as_explicit()
        assert s.trace(output)==1
        pt=s.Matrix(6,6,lambda i,j:output[(j//3)*3+i%3,(i//3)*3+j%3])
        minor=pt.extract([1,3],[1,3])
        expected=s.Matrix([[0,(eps*t)**n/2],[(eps*t)**n/2,(1-r**n)/2]])
        assert minor==expected
        assert minor.det()==-(eps*t)**(2*n)/4<0
    rows.append({'t':str(t),'iterations_checked':12,'all_negative_principal_minors':True})
result={'status':'PASS','arithmetic':'exact SymPy rational matrices',
        'input':'(|0,0>+|1,1>)/sqrt(2)', 'cases':rows,
        'scope':'Checks a single fixed pure qubit-qutrit input in the explicit nonfaithful family. Universal survival uses the written invariant-corner proof.'}
Path(__file__).with_name('fixed_pure_witness_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
