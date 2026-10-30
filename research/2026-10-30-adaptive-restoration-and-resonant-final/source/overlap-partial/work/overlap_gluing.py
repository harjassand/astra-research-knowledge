"""First overlapping resonance network: simultaneous cubic/quartic gluing."""
from pathlib import Path
from fractions import Fraction as R
import sys,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'outputs/quadratic_boundary'));import check_shape as m
sys.path.insert(0,str(root/'work'));import boundary_variation as b
start=time.perf_counter();F,_,T=m.acquired();powers=b.gd['cubic_powers']
freq=[(1,0),(0,1),(1,1),(2,1)];phase=[(0,0),(0,0),(-1,0),(-1,-1)]
original=[[R(1),R(0),R(0),R(0)],[R(0),R(0),R(0),R(1)],[R(1)]*4,[R(1),R(1,2),R(1,2),R(1,4)]]
images=[{} for _ in range(4)]
for k,ph,r in zip(freq,phase,original):
    for i in range(4):
        for sign in (-1,1):images[i]=m.add(images[i],{(sign*k[0],sign*k[1],sign*ph[0],sign*ph[1]):r[i]/2})
def compose(p):
    ans={}
    for pw,co in p.items():
        term={(0,0,0,0):co}
        for image,e in zip(images,pw):
            for _ in range(e):term=m.mul(term,image)
        ans=m.add(ans,term)
    return {e[2:]:co for e,co in ans.items() if e[:2]==(0,0)}
Fm=compose(F);assert set(Fm)<={(0,0),(1,1),(-1,-1),(1,-1),(-1,1)}
f0=Fm.get((0,0),R(0));fplus=2*Fm.get((1,1),R(0));fminus=2*Fm.get((1,-1),R(0));fcos=fplus+fminus;fsin=fminus-fplus
targets=[]
for pw in powers:
    mom=compose({tuple(pw):R(1)});assert set(mom)<={(1,0),(-1,0),(0,1),(0,-1)}
    targets.append([2*mom.get((1,0),R(0)),2*mom.get((0,1),R(0))])
e1=R(1,8);e2=R(1,128);eta=[R(1,9),R(16,9),R(1,9)]
aux1=[[R(1),t,t,t*t] for t in (R(-1),R(1,2),R(2))]
aux2=[[(1+t)**2,t*(1+t),t*(1+t),t*t] for t in (R(-1),R(1,2),R(2))]
rays=original+aux1+aux2;weights=[R(1,2)-e1-e2,R(1,2)-e1,R(1,2)-e1-e2,R(1,2)-16*e2]+[e1*q for q in eta]+[e2*q for q in eta]
assert all(w>0 for w in weights)
assert [[sum(w*r[i]*r[j] for w,r in zip(weights,rays)) for j in range(4)] for i in range(4)]==[[sum(r[i]*r[j]/2 for r in original) for j in range(4)] for i in range(4)]
HH=[b.Hvalue(np.array(r,float)) for r in rays];GG=[b.derivatives(np.array(r,float),b.cpows)@b.N for r in rays]
target=b.N.T@np.array(targets,float)
XX=cp.Variable((10,4));YY=cp.Variable((10,4));t1=cp.Variable();t2=cp.Variable();constraints=[]
constraints+=[sum(float(w)*g.T@XX[i] for i,(w,g) in enumerate(zip(weights,GG)))==target[:,0],sum(float(w)*g.T@YY[i] for i,(w,g) in enumerate(zip(weights,GG)))==target[:,1]]
blocks=[]
for i,(H,w) in enumerate(zip(HH,weights)):
    vals,vecs=la.eigh(H);W=np.sqrt(np.maximum(vals,0)*float(w)/2)[:,None]*vecs.T;blocks.append(W@cp.vstack([XX[i],YY[i]]).T)
L=cp.vstack(blocks);Acos=cp.bmat([[t1,float(fcos)/2],[float(fcos)/2,t2]]);Asin=cp.bmat([[t1,float(fsin)/2],[float(fsin)/2,t2]])
constraints+=[cp.bmat([[Acos,L.T],[L,np.eye(40)]])>>0,Asin>>0]
problem=cp.Problem(cp.Maximize(float(f0)-t1-t2),constraints);problem.solve(solver='CLARABEL',tol_feas=1e-10,tol_gap_abs=1e-10,tol_gap_rel=1e-10,max_iter=250)
result={'status':problem.status,'gap':None if problem.value is None else float(problem.value),
  'rays':[[str(v) for v in r] for r in rays],'weights':list(map(str,weights)),
  'cubic_target_vectors':[[str(v) for v in row] for row in targets],
  'quartic_phase_coefficients':list(map(str,[f0,fcos,fsin])),'radial_phase_moments':[[*e,co.numerator,co.denominator] for e,co in compose(m.core.mul(T,T)).items()],
  'X':None if XX.value is None else XX.value.tolist(),'Y':None if YY.value is None else YY.value.tolist(),
  't1':None if t1.value is None else float(t1.value),'t2':None if t2.value is None else float(t2.value),
  'seconds':time.perf_counter()-start,'scope':'Numerical proposal for all phases of an overlapping four-wave network; no positivity claim until exact reconstruction.'}
(root/'work/overlap_gluing_proposal.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','gap','quartic_phase_coefficients','seconds')},indent=2))
