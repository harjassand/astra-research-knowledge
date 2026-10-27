"""Exact evaluation of the accepted N1038 upper criterion on the new example.
No numerical SDP, float eigenvalue or transferred instance answer is used.
"""
import json
from pathlib import Path
import sympy as s
root=Path(__file__).resolve().parent
raw=json.loads((root/'NONDEGRADED_INPUT.json').read_text());K=s.Matrix(raw['K']);L=s.Matrix(raw['L'])
P=s.Matrix([[1,0,0],[0,1,0]]);B=s.Matrix([[1,0],[0,1],[-1,-1]])
R=P*L.inv();D=P*K*B;c=s.Rational(3,4);z=s.Matrix([s.Rational(1,3),s.Rational(1,3)])
blocks=[]
for i in range(3):
    x=P*K[:,i];e=s.Matrix([int(i==0),int(i==1)])
    M=sum((L[y,i]*R[:,y]*R[:,y].T for y in range(3)),s.zeros(2))
    H=M-e*e.T;T=s.diag(*list(x))-x*x.T;S=D*H*D.T
    C=c*T-S-(1-c)*(z-x)*(z-x).T
    assert C==C.T and C[0,0]>0 and C[1,1]>0 and C.det()>0
    blocks.append({'input':i,'matrix':[[str(v) for v in C.row(j)] for j in range(2)],
                   'diagonal':[str(C[0,0]),str(C[1,1])],'determinant':str(C.det())})
Rfull=K*L.inv();assert Rfull[0,0]==-s.Rational(1,20)
assert all(v>0 for v in K) and all(v>0 for v in L)
ans={'conditional_Umegaki_upper':'3/4','center':['1/3','1/3'],'blocks':blocks,
     'unique_signed_postprocessor':[[str(v) for v in Rfull.row(j)] for j in range(3)],
     'L_determinant':str(L.det()),
     'scope':'Accepted N1038 3-LMI criterion reused at its classical-input/all-finite-quantum-reference scope. This new example has not inherited source-instance audit acceptance.'}
(root/'ENTROPY_SEPARATION_CERTIFICATE.json').write_text(json.dumps(ans,indent=2)+'\n')
print(json.dumps(ans,indent=2))
