"""Prepare nearby rational circle points and rational selfadjoint drift."""
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog

rng=np.random.default_rng(801)
raw=rng.normal(size=(5,2));raw/=np.linalg.norm(raw,axis=1)[:,None]
points=[]
for t in [F(-7,2),F(2,9),F(7,2),F(-1,10),F(17,16)]:
    points.append([(1-t*t)/(1+t*t),2*t/(1+t*t)])
v=np.array([[float(a) for a in x] for x in points]);m=v.mean(axis=0);u=v-m
C=u.T@u/5
eig,rot=np.linalg.eigh(C);Csqrt=rot@np.diag(np.sqrt(eig))@rot.T
A=np.array([[.9837187265353232,.11858686203984926],[.11858686203984926,.1362565170981037]])
Bfloat=Csqrt@A@Csqrt
B=[[F(16,25),F(13,200)],[F(13,200),F(27,640)]]
B[1][0]=B[0][1]
D=np.array([[float(x) for x in row] for row in B])@np.linalg.inv(C)
rhs=(u@D.T/5).ravel()
edges=[(i,j) for i in range(5) for j in range(i+1,5)]
cols=[]
for i,j in edges:
    col=np.zeros((5,2));col[i]=v[i]-v[j];col[j]=v[j]-v[i];cols.append(col.ravel())
matrix=np.array(cols).T
dual=linprog(rhs,A_ub=-matrix.T,b_ub=np.zeros(len(edges)),bounds=[(-1,1)]*10,method='highs')
z=np.array(dual.x).reshape(5,2)
zrat=[[F(float(a)).limit_denominator(1000) for a in row] for row in z]
epsilon=F(1,1000)
zrat=[[zrat[i][k]+epsilon*points[i][k] for k in range(2)] for i in range(5)]
directed=[(i,j) for i in range(5) for j in range(5) if i!=j]
dcols=[]
for i,j in directed:
    col=np.zeros(15);col[2*i:2*i+2]=v[i]-v[j];col[10+i]=1;col[10+j]=-1;dcols.append(col)
direct=linprog(np.ones(20),A_eq=np.array(dcols).T,b_eq=np.r_[rhs,np.zeros(5)],bounds=(0,None),method='highs')
out=dict(points=[[str(a) for a in row] for row in points],B=[[str(a) for a in row] for row in B],farkas_z=[[str(a) for a in row] for row in zrat],directed_edges=[list(edge) for edge,flow in zip(directed,direct.x) if flow>1e-9],numeric_directed_flows=[float(flow) for flow in direct.x if flow>1e-9],numeric_pairing=float(dual.fun),selfadjoint_D=D.tolist(),reset_rate='1/1000')
print(json.dumps(out,indent=2))
