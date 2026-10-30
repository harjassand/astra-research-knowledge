"""Construct a universal amplitude gluing certificate by auxiliary wave rays.

One certificate must hold for every admissible cubic and ROC quadratic,
all three real wave amplitudes, all means and overall amplitudes.
"""
from pathlib import Path
import sys,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
sys.path.insert(0,str(Path(__file__).resolve().parent));import boundary_variation as b
start=time.perf_counter();rays=[np.array([1.,0,0,0]),np.array([0.,0,0,1]),np.ones(4)]+[np.array([1.,t,t,t*t]) for t in (-1,.5,2)]
HH=[b.Hvalue(r) for r in rays];GG=[b.derivatives(r,b.cpows)@b.N for r in rays]
_,target,_,_=b.field(np.array([[1.,0],[0,1.],[1.,1.]]));target*=3**1.5
Fmat=np.diag([3/8*b.Fvalue(r) for r in rays[:3]])
for i,j in ((0,1),(0,2),(1,2)):Fmat[i,j]=Fmat[j,i]=rays[j]@HH[i]@rays[j]/16
solutions=[]
for minimum in range(3):
    XX=cp.Variable((6,4));energy=cp.Variable(6,nonneg=True);P=cp.Variable((3,3),symmetric=True);N=cp.Variable((3,3),symmetric=True);gap=cp.Variable()
    constraints=[sum(g.T@XX[i] for i,g in enumerate(GG))==target,P>>0,N>=0]
    for i,H in enumerate(HH):
        vals,vecs=la.eigh(H);W=np.sqrt(np.maximum(vals,0))[:,None]*vecs.T
        constraints.append(cp.sum_squares(W@XX[i])<=energy[i])
    newenergy=9*energy[3]+9/16*energy[4]+9*energy[5]
    matrices=[]
    for i in range(3):
        M=np.ones((3,3));M[i,:]=0;M[:,i]=0;np.fill_diagonal(M,0);matrices.append(M)
    D=Fmat-sum(energy[i]*matrices[i] for i in range(3))-newenergy*matrices[minimum]
    chart=np.column_stack([np.eye(3)[:,i] for i in range(3) if i!=minimum]+[np.ones(3)])
    constraints.append(chart.T@D@chart-gap*np.eye(3)==P+N)
    prob=cp.Problem(cp.Maximize(gap),constraints)
    prob.solve(solver='CLARABEL',tol_feas=1e-10,tol_gap_abs=1e-10,tol_gap_rel=1e-10,max_iter=300)
    print('chart',minimum,prob.status,'gap',gap.value,flush=True)
    solutions.append({'minimum':minimum,'gap':None if gap.value is None else float(gap.value),'X':None if XX.value is None else XX.value.tolist(),
      'energy':None if energy.value is None else energy.value.tolist(),'P':None if P.value is None else P.value.tolist(),'N':None if N.value is None else N.value.tolist()})
out={'charts':solutions,'seconds':time.perf_counter()-start,'scope':'Numerical proposal; requires exact cubic matching, covariance identities and copositive remainder reconstruction.'}
(b.root/'work/triad_gluing_proposal.json').write_text(json.dumps(out,indent=2)+'\n')
