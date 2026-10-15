import sys,json,itertools
sys.path.insert(0,'/workspace/shared/practical_binary_schedule')
from rank_probe import P,solve,rank
import random
rng=random.Random(105);m=5
a=[rng.randrange(1,P) for _ in range(m)]; B=[[0 if i==j else rng.randrange(P) for j in range(m)] for i in range(m)]
edges=[(i,j) for i in range(m) for j in range(m) if i!=j]; rows=[];sets=[]; pivots=[]
for mask in range(1<<m):
 S=[i for i in range(m) if mask>>i&1]
 if len(S)<2 or sum(i>=2 for i in S)>2:continue
 C=[[int(i==j)+B[i][j] for j in S] for i in S];v=solve(C,[1]*len(S));u=solve(list(map(list,zip(*C))),[a[i] for i in S]);ui=dict(zip(S,u));vi=dict(zip(S,v)); row=[-ui.get(i,0)*vi.get(j,0)%P for i,j in edges]
 if rank(rows+[row])>len(rows):rows.append(row);sets.append(S)
assert len(rows)==20
A=[r[:] for r in rows];det=1
for k in range(20):
 q=next(i for i in range(k,20) if A[i][k]);
 if q!=k:A[k],A[q]=A[q],A[k];det=-det
 det=det*A[k][k]%P;t=pow(A[k][k],-1,P)
 for i in range(k+1,20):
  v=A[i][k]*t%P;A[i]=[(x-v*y)%P for x,y in zip(A[i],A[k])]
assert det
receipt={'prime':P,'a':a,'B':B,'row_subsets_zero_indexed':sets,'minor_determinant_mod_prime':det,'column_order':edges}
open('/workspace/shared/practical_binary_schedule/rank_witness.json','w').write(json.dumps(receipt,indent=2));print(receipt)
# Conditional exact pair recovery from empty context and either of two known anchors.
import sympy as s
B=s.Matrix([[0,s.Rational(1,5),s.Rational(1,7),s.Rational(2,9)],[s.Rational(2,7),0,s.Rational(1,9),s.Rational(1,8)],[s.Rational(1,6),s.Rational(1,8),0,s.Rational(1,10)],[s.Rational(1,11),s.Rational(1,12),s.Rational(1,13),0]])
a=s.Matrix([1,2,3,4]);i,j=2,3

def g(T):
 return (a.extract(T,[0]).T*(s.eye(len(T))+B.extract(T,T)).inv()*s.ones(len(T),1))[0] if T else s.Integer(0)
rows=[];rhs=[]
for T in [[],[0],[1]]:
 inv=(s.eye(len(T))+B.extract(T,T)).inv(); bi=B.extract([i],T);bj=B.extract([j],T);ti=B.extract(T,[i]);tj=B.extract(T,[j]);ones=s.ones(len(T),1);at=a.extract(T,[0]).T
 scalar=lambda z:z[0]
 alpha=1-scalar(bi*inv*ti);delta=1-scalar(bj*inv*tj);r=scalar(bi*inv*tj);ss=scalar(bj*inv*ti)
 p=1-scalar(bi*inv*ones);q=1-scalar(bj*inv*ones);d=a[i]-scalar(at*inv*ti);e=a[j]-scalar(at*inv*tj);h=g(T+[i,j])-g(T)
 rows.append([h*ss+d*q,h*r+e*p,-h]);rhs.append(d*delta*p+e*alpha*q+d*r*q+e*ss*p-h*(alpha*delta-r*ss))
L=s.Matrix(rows);sol=L.inv()*s.Matrix(rhs)
assert sol==s.Matrix([B[i,j],B[j,i],B[i,j]*B[j,i]])
receipt={'determinant':str(L.det()),'solution_x_y_xy':[str(v) for v in sol]}
open('/workspace/shared/practical_binary_schedule/pair_witness.json','w').write(json.dumps(receipt,indent=2));print(receipt)
