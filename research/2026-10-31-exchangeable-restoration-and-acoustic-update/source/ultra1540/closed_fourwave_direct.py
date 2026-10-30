"""Can acoustic completion glue both triads on the ORIGINAL four rays?

No covariance exchange or amplitude order chart is used in this proposal.
"""
from pathlib import Path
from fractions import Fraction as R
import sys,json,time
import numpy as np,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/acoustic_capacity'))
from kernel import data,capacity_kernel,acoustic_side
from receive import r,b,ca,dot,quadratic
D=data();cert=json.loads((root/'outputs/acoustic_capacity/certificate.json').read_text());sd=r.setup();original=sd['original'];Ms=[];Js=[]
for ray in original:
    side=acoustic_side(ray)
    if side is None:
        M=[[b.evaluate(p,ray) for p in row] for row in D['HF']];J=[[b.evaluate(b.diff(P,j),ray) for P in D['polys']] for j in range(4)]
    else:
        u=[ray[0],ray[2]] if side==0 else [ray[1],ray[3]];x,y=u;K=D['nulls'][side]
        def rot(v):return [x*v[0]-y*v[2],x*v[1]-y*v[3],y*v[0]+x*v[2],y*v[1]+x*v[3]]
        null=rot(K);perp=[rot([R(int(i==j)) for i in range(4)]) for j in range(3)];deriv=[0,x,0,y] if side==0 else [x,0,y,0]
        J=[];gamma=[]
        for P in D['polys']:
            HC=[[b.evaluate(b.diff(b.diff(P,i),j),ray) for j in range(4)] for i in range(4)];gamma.append(quadratic(HC,null,deriv))
        J=[gamma]+[[sum(p[i]*b.evaluate(b.diff(P,i),ray) for i in range(4)) for P in D['polys']] for p in perp]
        M=[[R(z)*(x*x+y*y)**2 for z in row] for row in cert['acoustic_charts'][side]['deflated_Hessian_at_zero']]
    Yi,_=ca.solve_range(M,J);assert ca.mm(ca.transpose(J),Yi)==capacity_kernel(ray,'closed');Ms.append(M);Js.append(J)
targets=[[dot(v,[row[e] for row in sd['targets']]) for e in range(2)] for v in D['basis']];profiles=[]
for e,ids in enumerate(((0,1,2),(0,2,3))):
    L=[[Js[i][j][k] for i in ids for j in range(4)] for k in range(12)];sol,rank=ca.solve_range(L,[[row[e]] for row in targets]);xx=[[R(0)]*4 for _ in range(4)]
    for k,i in enumerate(ids):xx[i]=[sol[4*k+j][0] for j in range(4)]
    print('triad',e,'rank',rank,'energies',[float(quadratic(M,x)) for M,x in zip(Ms,xx)],flush=True);profiles.append(xx)
FM=np.array(sd['FM'],float)
for e,ids in enumerate(((0,1,2),(0,2,3))):
    for i in ids:
        pair=[j for j in ids if j!=i];en=float(quadratic(Ms[i],profiles[e][i]));FM[pair[0],pair[1]]-=en/2;FM[pair[1],pair[0]]-=en/2
cross=[quadratic(Ms[i],profiles[0][i],profiles[1][i]) for i in (0,2)];u,v=sd['u'],sd['v'];phase_bound=[max(abs(u-2*cross[1]),abs(u)),max(abs(v-2*cross[0]),abs(v))]
P=cp.Variable((4,4),symmetric=True);N=cp.Variable((4,4),symmetric=True);gamma=cp.Variable();constraints=[P>>0,N>=0];Z=cp.Constant(FM);young=[]
for i,co in zip((0,2),phase_bound):
    lam=cp.Variable(nonneg=True);beta=cp.Variable(nonneg=True);young.append((lam,beta));constraints+=[cp.bmat([[lam,1.],[1.,beta]])>>0]
    for j,vv in ((1,lam),(3,beta)):
        MM=np.zeros((4,4));MM[i,j]=MM[j,i]=1;Z=Z-float(co)*vv*MM/4
constraints +=[Z-gamma*np.array(sd['TU'],float)==P+N];problem=cp.Problem(cp.Maximize(gamma),constraints);problem.solve(solver='CLARABEL',tol_feas=1e-10,tol_gap_abs=1e-10,tol_gap_rel=1e-10,max_iter=300)
print(problem.status,'global phase/amplitude gap proposal',problem.value,flush=True)
out={'status':problem.status,'gap':None if problem.value is None else float(problem.value),'profiles':[[list(map(str,row)) for row in X] for X in profiles],'cross_costs':list(map(str,cross)),'quartet_phase_bounds':list(map(str,phase_bound)),'young':[[float(a.value),float(c.value)] for a,c in young],'scope':'A proposal on four completed original rays; a positive optimum needs exact remainder reconstruction.'}
(root/'work/closed_fourwave_direct.json').write_text(json.dumps(out,indent=2)+'\n')
