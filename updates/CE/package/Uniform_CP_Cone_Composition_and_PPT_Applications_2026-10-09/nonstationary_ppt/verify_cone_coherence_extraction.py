"""Exact finite checks of the triangular coherence witness in the cone proof.
These identities illustrate the universal algebraic argument, not cone membership
or the general uniform-composition theorem.
"""
from pathlib import Path
import json
import sympy as s
r=s.Rational
L=[s.Matrix([[r(1,2),r(1,3)],[0,r(1,4)]]),s.Matrix([[r(1,5),s.I/7],[0,s.I/6]])]
def apply(ks,X):return sum((K*X*K.adjoint() for K in ks),s.zeros(ks[0].rows)).applyfunc(s.expand)
def unit(d,a,b):
 M=s.zeros(d);M[a,b]=1;return M
lam=sum(K[0,0]*s.conjugate(K[1,1]) for K in L)
alpha=sum(abs(K[0,0])**2 for K in L)
assert lam!=0
E00,E01=unit(2,0,0),unit(2,0,1)
A,B=E00,E01
for n in range(1,13):
 A=apply(L,A);B=apply(L,B)
 assert s.simplify(A-alpha**n*E00)==s.zeros(2)
 assert s.simplify(B[0,1]-lam**n)==0
 assert B[1,0]==B[1,1]==0
 # The partially transposed normalized Bell output has this principal minor.
 assert s.simplify(-B[0,1]*s.conjugate(B[0,1])/4+abs(lam)**(2*n)/4)==0
rank_cases=[]
for p,q in [(1,2),(2,1),(1,3),(3,1),(2,3),(3,2)]:
 d=4;P=s.diag(*([1]*p+[0]*(d-p)));Pout=s.diag(*([1]*q+[0]*(d-q)))
 input_filter=s.zeros(d);input_filter[0,0]=1;input_filter[p,1]=1
 output_filter=s.zeros(d);output_filter[0,0]=1;output_filter[1,q]=1
 ks=[]
 for K in L:
  V=s.zeros(d);V[0,0]=K[0,0];V[0,p]=K[0,1];V[q,p]=K[1,1];ks.append(V)
 assert (s.eye(d)-Pout)*apply(ks,P)*(s.eye(d)-Pout)==s.zeros(d)
 extracted=[output_filter*K*input_filter for K in ks]
 for a,K in enumerate(extracted):
  expected=s.zeros(d);expected[:2,:2]=L[a];assert K==expected
 rank_cases.append([p,q])
result={'status':'PASS','arithmetic':'Exact SymPy rational complex','triangular_power_cases':12,'nonzero_cross_coefficient':str(lam),'negative_principal_minor':'-|lambda|^(2n)/4 for every n>=1','unequal_input_output_rank_cases':rank_cases,'scope':'Finite identity checks for the extracted persistent qubit witness; the universal conclusion is proved symbolically in the cone theorem.'}
Path(__file__).with_name('cone_coherence_extraction_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
