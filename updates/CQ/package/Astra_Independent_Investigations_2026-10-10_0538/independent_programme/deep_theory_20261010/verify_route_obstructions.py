"""Exact, deterministic checks for the early discarded CH proof mechanisms.
Run from repository/workspace root. Uses Python stdlib and sympy only.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as sp
BASE=Path(__file__).resolve().parent

def strongly_connected(A):
 n=len(A)
 def reach(transpose=False):
  seen={0};todo=[0]
  while todo:
   v=todo.pop()
   for w in range(n):
    if (A[w][v] if transpose else A[v][w]) and w not in seen:
     seen.add(w);todo.append(w)
  return len(seen)==n
 return reach() and reach(True)

def combinatorial_checks(A):
 n=len(A)
 d=[sum(row) for row in A]
 din=[sum(A[i][j] for i in range(n)) for j in range(n)]
 assert all(not A[i][i] for i in range(n))
 assert all(not(A[i][j] and A[j][i]) for i in range(n) for j in range(n))
 assert not any(A[i][j] and A[j][k] and A[k][i] for i in range(n) for j in range(n) for k in range(n))
 sec=[sum(j!=i and not A[i][j] and any(A[i][k] and A[k][j] for k in range(n)) for j in range(n)) for i in range(n)]
 return d,din,sec

def weighted_energy_obstruction(m=12):
 n=4*m;D=11*m-1
 P=[[F(0) for _ in range(n)] for _ in range(n)]
 for b in range(4):
  for i in range(m):
   for j in range(m):
    if i<j:P[b*m+i][b*m+j]=F(6,D)
    P[b*m+i][((b+1)%4)*m+j]=F(8*m+2+6*(i-j),m*D)
 assert all(sum(row)==1 for row in P)
 assert all(sum(P[i][j] for i in range(n))==1 for j in range(n))
 A=[[int(x>0) for x in row] for row in P]
 combinatorial_checks(A);assert strongly_connected(A)
 energy=sum(x*x for row in P for x in row)
 assert energy==F(32*m+8,11*m-1)<3
 return {'n':n,'m':m,'row_and_column_sums':'exactly 1','energy':str(energy),'energy_below_3':str(F(3)-energy),'pi':'uniform','oriented':True,'triangle_free':True,'strongly_connected':True,'formula':'within forward: 6/(11m-1); next block (i,j): (8m+2+6(i-j))/(m(11m-1))'}

def maximum_pi_obstruction():
 raw=json.loads((BASE/'stationary_probe.json').read_text())['failures'][0]
 A=raw['A'];n=len(A);r=raw['r'];d,din,sec=combinatorial_checks(A)
 assert d==[r]*n and strongly_connected(A)
 P=sp.Matrix(A)/r;M=P.T-sp.eye(n);M[n-1,:]=sp.ones(1,n)
 b=sp.zeros(n,1);b[n-1]=1;pi=M.inv()*b
 assert all(x>0 for x in pi) and sum(pi)==1 and pi.T*P==pi.T
 top=max(range(n),key=lambda i:pi[i]);assert all(pi[top]>pi[j] for j in range(n) if j!=top)
 assert sec[top]<r
 out={'n':n,'r':r,'A':A,'pi':[str(x) for x in pi],'unique_maximum_pi_vertex':top,'second_count_at_maximum':sec[top],'indegree_at_maximum':din[top],'all_second_counts':sec,'all_indegrees':din,'stationary_second_mean':str(sum(pi[i]*sec[i] for i in range(n))),'verified_oriented_triangle_free_strongly_connected':True}
 (BASE/'exact_maximum_pi_counterexample.json').write_text(json.dumps(out,indent=2)+'\n')
 return {k:v for k,v in out.items() if k not in ('A','pi','all_second_counts','all_indegrees')}

if __name__=='__main__':
 out={'weighted_energy':weighted_energy_obstruction(),'maximum_pi':maximum_pi_obstruction()}
 (BASE/'route_obstructions_verified.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
