from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,math

def add(A,B):return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def mm(A,B):return [[sum(x*y for x,y in zip(a,b)) for b in zip(*B)] for a in A]
def tr(A):return sum(A[i][i] for i in range(len(A)))
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def term(edge,erased):
 n=3;M=[[F(0) for _ in range(8)] for _ in range(8)];u=F(1,4);v=F(3,4);i,j=edge
 for x in range(8):
  b=[(x>>k)&1 for k in range(n)]
  def index(c):return sum(z<<k for k,z in enumerate(c))
  if (b[i]==b[j]) if erased else (b[i]!=b[j]):
   for q in [0,1]:
    c=b.copy();c[i]=q;c[j]=q if erased else 1-q
    M[index(c)][x]+=u
  c=b.copy();c[i]=b[j] if erased else 1-b[j];c[j]=b[i] if erased else 1-b[i]
  M[index(c)][x]+=v
 return M
A=[[F(0) for _ in range(8)] for _ in range(8)];A0=A
for edge in [(0,1),(0,2),(1,2)]:
 A=add(A,term(edge,False));A0=add(A0,term(edge,True))
P=eye(8);P0=eye(8);moments=[]
for k in range(7):
 moments.append({'k':k,'trace_Ak':str(tr(P)),'trace_A0k':str(tr(P0)),'difference':str(tr(P0)-tr(P))})
 P=mm(P,A);P0=mm(P0,A0)
rt=math.sqrt(13)
Z=4*math.exp(7/4)+2*math.exp(5/4+rt/2)+2*math.exp(5/4-rt/2)
Z0=4*math.exp(1/4)+2*math.exp(9/4)+2*math.exp(13/4)
# Check characteristic polynomial identity with rational matrix multiplications.
# Spin-1/2 eigenvalue 7/4, and 3/2-sector factor (x-5/4)^2-13/4.
Q=add(A,[[F(-7,4)*v for v in row] for row in eye(8)])
B=add(mm(A,A),[[F(-5,2)*v for v in row] for row in A]);B=add(B,[[F(-27,16)*v for v in row] for row in eye(8)])
assert all(z==0 for row in mm(Q,B) for z in row)
C0=eye(8)
for lam in [F(1,4),F(9,4),F(13,4)]:
 D0=add(A0,[[(-lam)*v for v in row] for row in eye(8)])
 C0=mm(C0,D0)
assert all(z==0 for row in C0 for z in row)
# Trace and second moment plus multiplicities pin eigenspectrum for real symmetric A.
res={'A':[[str(z) for z in row] for row in A],'A_erased':[[str(z) for z in row] for row in A0],'moments':moments,'true_spectrum':'7/4 (multiplicity 4), 5/4+sqrt(13)/2 (multiplicity 2), 5/4-sqrt(13)/2 (multiplicity 2)','erased_spectrum':'1/4 (multiplicity 4), 9/4 (multiplicity 2), 13/4 (multiplicity 2)','true_partition_beta1_float':Z,'erased_partition_beta1_float':Z0,'acceptance_beta1_float':Z/Z0,'acceptance_100_triangles_float':(Z/Z0)**100,'exact_A_minimal_polynomial_verified':True}
Path('work/agents/epr_parity/results/continuous_projection.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k not in ['A','A_erased']},indent=2))
