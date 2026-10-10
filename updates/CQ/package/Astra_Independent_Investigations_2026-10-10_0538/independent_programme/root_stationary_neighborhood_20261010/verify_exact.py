from fractions import Fraction as F
A=[[0]*8 for _ in range(8)]
for i in range(4):
 A[2*i][2*i+1]=1
 for u in (2*i,2*i+1):
  for v in (2*((i+1)%4),2*((i+1)%4)+1):A[u][v]=1
pi=[F(3 if i%2==0 else 4,28) for i in range(8)]
d=[sum(r) for r in A]
s=[sum(j!=i and not A[i][j] and any(A[i][k] and A[k][j] for k in range(8)) for j in range(8)) for i in range(8)]
assert all(sum(pi[i]*F(A[i][j],d[i]) for i in range(8))==pi[j] for j in range(8))
assert all(not(A[i][j] and A[j][k] and A[k][i]) for i in range(8) for j in range(8) for k in range(8))
assert s==[2]*8
assert sum(pi[i]*d[i] for i in range(8))==F(17,7)
print('Exact triangle-free construction verified; second=2, weighted outdegree=17/7')
