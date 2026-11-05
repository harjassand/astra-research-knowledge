"""Verify the exact physical-check Lawrence contraction on dependent checks.
No CMR dependency."""
from bdl_matrices import *
from two_square_minor import seed
T=rx(seed());U=rx(T);A=T.columns('Z');B=U.columns('Z')
contract=[];points={};bridge={}
for i,l in enumerate(U.zlabels):
 if l[0]=='x' or (l[0]=='q' and l[2][0]=='layer'):contract.append(i)
 elif l[0]=='z':points[l[1],l[2]]=i
 elif l[0]=='q':bridge.setdefault(l[1],i)
retained=[points[z,0] for z in range(T.nz)]+[points[z,1] for z in range(T.nz)]+[bridge[q] for q in range(T.nq)]
piv={}
for i in contract:
 v=B[i]
 while v:
  k=v.bit_length()-1
  if k in piv:v^=piv[k]
  else:piv[k]=v;break
reduced=[]
for i in retained:
 v=B[i]
 for k in sorted(piv,reverse=True):
  if v>>k&1:v^=piv[k]
 reduced.append(v)
L=A+[v<<T.nq for v in A]+[(1<<q)|(1<<(q+T.nq)) for q in range(T.nq)]
ids,coords=basis_reduce(L,list(range(len(L))))
assert rank(reduced)==len(ids)
for i,c in enumerate(coords):
 v=reduced[i]
 for j in bits(c):v^=reduced[ids[j]]
 assert v==0
print('Verified physical RX check-coordinate contraction to exact Lawrence matroid.')
print('Old checks/rank =',T.nz,rank(A),'old qubits =',T.nq)
print('Contracted physical check count/rank =',len(contract),len(piv))
print('Retained physical check count/rank =',len(retained),len(ids))
