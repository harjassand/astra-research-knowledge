"""Strengthen the counterexample: currents are rows of a passive connected graph.

Original real voltage coordinates are (x,y,w,t)=(x,y,x-u,y-v).
The graph is x -- w -- t -- y with unit real branch admittances.
At the two fixed-injection buses, J_x=x-w=u and J_y=y-t=v.
"""
from pathlib import Path
from fractions import Fraction as F
import json
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'EXACT_COUNTEREXAMPLE.json').read_text())
m={(r['k'],r['l']):F(r['value']) for r in d['moments']}
def L(k,l):return m[tuple(sorted((k,l)))]
lin=[(0,0),(1,0),(0,1),(-1,0),(0,-1)]
def matrix(terms):
 return [[sum(c*L(a[0]+b[0]+t[0],a[1]+b[1]+t[1]) for t,c in terms.items()) for b in lin] for a in lin]
def pivots(A):
 n=len(A);D=[];T=[[F(0)]*n for _ in range(n)]
 for i in range(n):
  T[i][i]=F(1);D.append(A[i][i]-sum(T[i][k]**2*D[k] for k in range(i)))
  assert D[-1]>0,(i,str(D[-1]))
  for j in range(i+1,n):T[j][i]=(A[j][i]-sum(T[j][k]*T[i][k]*D[k] for k in range(i)))/D[i]
 assert all(A[i][j]==sum(T[i][k]*D[k]*T[j][k] for k in range(n)) for i in range(n) for j in range(n))
 return D
lo,hi=F(1,10000),F(100)
tests={}
for label,axis in [('w',0),('t',1)]:
 pos=(2,0) if axis==0 else (0,2)
 neg=(-2,0) if axis==0 else (0,-2)
 tests[label+'_lower']=pivots(matrix({pos:F(1),neg:F(1),(0,0):-2-lo}))
 tests[label+'_upper']=pivots(matrix({pos:F(-1),neg:F(-1),(0,0):hi+2}))
result={'status':'EXACT_PASSIVE_EMBEDDING_VERIFIED','voltage_vector':['x','y','w=x-u','t=y-v'],'squared_voltage_bounds':{'x':[1,4],'y':[1,4],'w':[str(lo),str(hi)],'t':[str(lo),str(hi)]},'Y':[[1,0,-1,0],[0,1,0,-1],[-1,0,2,-1],[0,-1,-1,2]],'fixed_injection_buses':[0,1],'fixed_power_at_both':1,'B_i':[1,0,-1,0],'B_j':[0,1,0,-1],'graph':'x--w--t--y, each edge unit positive real admittance','equality_ideal':['x*(x-w)-1','y*(y-t)-1'],'exact_ldlt_pivots':{k:list(map(str,v)) for k,v in tests.items()},'lower_cut_value':d['lower_cut_value'],'proof':'An invertible linear pullback preserves moment positivity, degree, and equality localizers. The w/t voltage localizers are checked in the invertibly equivalent basis (1,x,y,u,v).','limitations':'No claim for standard narrow voltage boxes, branch-angle restrictions, generator/thermal limits, or the pinned PGLib instance.'}
(ROOT/'PASSIVE_EMBEDDING.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='exact_ldlt_pivots'},indent=2))
