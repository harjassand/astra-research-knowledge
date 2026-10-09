"""Exact rational construction. SymPy is used only to solve one finite linear system."""
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as sp

folder=Path(__file__).parent
seed=json.loads((folder/'frame_rational_seed_v3.json').read_text())
v=sp.Matrix([[sp.Rational(a) for a in row] for row in seed['points']])
B=sp.Matrix([[sp.Rational(a) for a in row] for row in seed['B']])
m=sp.Matrix([sum(v[:,k])/5 for k in range(2)])
u=v-sp.ones(5,1)*m.T
C=u.T*u/5
D0=B*C.inv()
edges=seed['directed_edges']
columns=[]
for i,j in edges:
    column=sp.zeros(15,1)
    column[2*i:2*i+2,0]=(v[i,:]-v[j,:]).T
    column[10+i]=1;column[10+j]=-1
    columns.append(column)
matrix=sp.Matrix.hstack(*columns)
rhs=sp.Matrix([(D0*u[i,:].T)[k]/5 for i in range(5) for k in range(2)]+[0]*5)
flow=matrix.inv()*rhs if matrix.rows==matrix.cols else sp.linsolve((matrix,rhs))
if isinstance(flow,set) or isinstance(flow,sp.FiniteSet):
    solution=list(flow)[0]
else: solution=list(flow)
assert not any(x.free_symbols for x in solution)
assert all(x>0 for x in solution)
assert matrix*sp.Matrix(solution)==rhs
reset=sp.Rational(seed['reset_rate'])
D=D0+reset*sp.eye(2)
Q=sp.zeros(10)
for (i,j),w in zip(edges,solution):Q[i,j]=5*w
for i in range(5):
    for j in range(5):
        if i!=j:Q[i,j]+=reset/5
order=[0,3,1,4,2]
eta=sp.Rational(1,10)
facets=[]
for k in range(5):
    i,j=order[k],order[(k+1)%5]
    edge=v[j,:]-v[i,:]
    # l(x,y)=constant+cx*x+cy*y, determinant(edge, point-v_i).
    coeff=[edge[1]*v[i,0]-edge[0]*v[i,1],-edge[1],edge[0]]
    facets.append(coeff)
    for h in range(5):
        rate=eta*(coeff[0]+coeff[1]*v[h,0]+coeff[2]*v[h,1])
        assert rate>=0
        Q[h,5+k]=Q[5+k,h]=rate
for i in range(10):Q[i,i]=-sum(Q[i,j] for j in range(10) if i!=j)
z=sp.Matrix([[sp.Rational(a) for a in row] for row in seed['farkas_z']])
mono=[((z[i,:]-z[j,:])*(v[i,:]-v[j,:]).T)[0] for i in range(5) for j in range(i+1,5)]
pair=sum((z[i,:]*D*u[i,:].T)[0]/5 for i in range(5))
assert min(mono)>0
assert pair<0
assert C*D.T==D*C
assert B.det()>0 and B[0,0]>0
assert sp.ones(1,10)*Q==sp.zeros(1,10)
assert Q*sp.ones(10,1)==sp.zeros(10,1)
hidden=sp.Matrix.hstack(sp.ones(5,1),v)
H=sp.zeros(10,8);H[:5,:3]=hidden
for k in range(5):H[5+k,3+k]=1
M=H.T*H/10
L=M.inv()*H.T*Q*H/10
assert Q*H==H*L
assert M*L==L.T*M
moment=sp.Matrix([[1,v[i,0],v[i,1],v[i,0]**2,v[i,0]*v[i,1]] for i in range(5)]).T
assert moment.det()!=0

def strings(matrix):return [[str(a) for a in row] for row in matrix.tolist()]
out=dict(points=strings(v),mean=[str(a) for a in m],covariance=strings(C),B=strings(B),internal_D=strings(D),reset_rate=str(reset),marker_eta=str(eta),ccw_order=order,facets=[[str(a) for a in row] for row in facets],base_directed_edges=edges,base_directed_flows=[str(a) for a in solution],farkas_z=strings(z),monotonicity_pairings=[str(a) for a in mono],farkas_drift_pairing=str(pair),Q=strings(Q),H=strings(H),M=strings(M),L=strings(L),five_point_moment_determinant=str(moment.det()),summary=dict(states=10,outputs=6,observable_rank=8,min_monotonicity=float(min(mono)),negative_pairing=float(pair),all_internal_offdiagonal_positive=True,stationary_uniform=True,restricted_generator_symmetric=True))
(folder/'exact_certificate_v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['summary'],indent=2))
