"""Adaptive lifted heat-Gram proposal; all actual gradients are the target.

Uses the acquired positive seven-dimensional leading lift, exact
annihilation constraints and a free null-lift completion at each point.
Numerical proposals do not establish QC or a QC obstruction.
"""
from pathlib import Path
from fractions import Fraction as R
from itertools import combinations,product
from functools import lru_cache
import sys,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
sys.path.insert(0,str(Path(__file__).resolve().parent));import heat_model as h
root=h.root;b=h.b;r=h.r;ca=h.ca
start=time.perf_counter();av=list(map(R,h.base['ray']['A0']));aa,bb,cc,dd=av;av2=[-bb,aa,dd,-cc]
# E*z=RHS*C is the exact global root-row annihilation condition.
E=[];RHS=[];powers=json.loads((root/'outputs/graded_stabilization/certificate.json').read_text())['cubic_powers']
for av0,hi in ((av,0),(av2,2)):
 for ux,uy in ((R(1),R(0)),(R(0),R(1)),(R(1),R(1))):
  A=[ux*av0[0]-uy*av0[2],ux*av0[1]-uy*av0[3],uy*av0[0]+ux*av0[2],uy*av0[1]+ux*av0[3]];kh=[R(0)]*6;kh[hi]=ux;kh[hi+3]=uy
  for j in range(6):
   E.append([sum(kh[i]*A[a]*R(float(h.XB[a,i,j,l])) for a in range(4) for i in range(6)) for l in range(80)])
   row=[]
   for pw in powers:
    P={tuple(pw):R(1)};HC=[[b.evaluate(b.diff(b.diff(P,i),k),A) for k in range(4)] for i in range(4)];B=np.zeros((6,6),dtype=object)
    for inds in ((0,1,3,4),(1,2,4,5)):
     for i in range(4):
      for k in range(4):B[inds[i],inds[k]]+=HC[i][k]
    row.append(-sum(kh[i]*B[i,j] for i in range(6))/2)
   RHS.append(row)
rankE=b.rank(E);rankAug=b.rank([e+f for e,f in zip(E,RHS)]);qc=json.loads((root/'outputs/quadratic_boundary/certificate.json').read_text());CB=[list(map(R,v)) for v in qc['normal_form_basis']]
sol,rr=ca.solve_range(E,[[sum(row[k]*v[k] for k in range(20)) for v in CB] for row in RHS]);assert rr==rankE and rankAug-rankE==8
print('exact root-row rank',rankE,'augmentation',rankAug,'admitted cubic dimension',12,flush=True)
c0=[R(q) for q in qc['example_cubic_coefficients']];rhs=[sum(a*c for a,c in zip(row,c0)) for row in RHS];EN=np.array(E,float);rhsN=np.array(rhs,float);sc=la.norm(EN,axis=1);mask=sc>1e-14;assert np.max(abs(rhsN[~mask]),initial=0)<1e-12;EN=EN[mask]/sc[mask,None];rhsN=rhsN[mask]/sc[mask]
N=la.null_space(EN);z0=la.lstsq(EN,rhsN)[0];assert N.shape==(80,80-rankE)
np.testing.assert_allclose(EN@z0,rhsN,atol=1e-11)
# Canonical heat lift L^T T^2 S_F L = D^T M D.
eta0,zeta0=map(R,h.base['ray']['canonical_zero']);perm=h.base['permutation'];Q=np.eye(6);Q[3,0]=float(bb);L=np.eye(6)[:,perm]@Q
Mpoly=[[b.literal(p,2) for p in row] for row in h.base['M']]
@lru_cache(maxsize=None)
def M_exact(eta,zeta):return [[b.evaluate(p,[eta,zeta]) for p in row] for row in Mpoly]
def whiten_exact(A):
 n=len(A);LL=[[R(int(i==j)) for j in range(n)] for i in range(n)];DD=[]
 for j in range(n):
  pp=A[j][j]-sum(LL[j][k]**2*DD[k] for k in range(j))
  if pp<=0:return None
  DD.append(pp)
  for i in range(j+1,n):LL[i][j]=(A[i][j]-sum(LL[i][k]*LL[j][k]*DD[k] for k in range(j)))/pp
 return np.diag(1/np.sqrt(np.array(DD,float)))@la.solve_triangular(np.array(LL,float),np.eye(n),lower=True)
@lru_cache(maxsize=None)
def M_whitener(eta,zeta):
 M=M_exact(eta,zeta);w,g=eta-eta0,zeta-zeta0;nn=[g,-w,R(0),R(0),R(0),R(0),R(0)]
 for pp in [R(0)]+[R(2)**k for k in range(0,161,4)]:
  pad=[[M[i][j]+pp*nn[i]*nn[j] for j in range(7)] for i in range(7)];W=whiten_exact(pad)
  if W is not None:return W
 raise AssertionError('No positive null padding found; no positivity inference is made.')
GA=np.array([[0,0,0,1],[0,0,-1,0],[0,1,0,0],[-1,0,0,0]],float);GH=np.zeros((6,6))
for i,(j,s) in enumerate(zip((5,4,3,2,1,0),(1,-1,1,1,-1,1))):GH[i,j]=s
for eta,zeta in ((R(0),R(0)),(R(-1,2),R(3,4))):
 A=np.array([1.,float(eta),0.,float(zeta)]);w=float(eta-eta0);g=float(zeta-zeta0);DM=np.zeros((7,6));DM[0,0]=w;DM[1,0]=g
 for j in range(1,6):DM[j+1,j]=1
 assert la.norm(L.T@h.SF(A)@L-DM.T@np.array(M_exact(eta,zeta),float)@DM/(A@A)**2)<1e-7
 assert la.norm(GH.T@h.SF(GA@A)@GH-h.SF(A))<1e-7

import heat_leading_family as lf
margin=cp.Variable();lead=cp.Variable(15);leadscale=cp.Parameter(15,nonneg=True);leadreal=cp.multiply(leadscale,lead);leadmax=np.ones(15)
free=cp.Variable(N.shape[1]);oq=cp.Variable(6);nu=cp.Variable(nonneg=True);z=z0+N@free
DQ=2*nu*np.diag([1,2,1,1,2,1])+sum(oq[p]*h.Wedges[p] for p in range(6))
def X(v):
 v=np.array(v,float);const=np.einsum('a,aij->ij',v,h.X0);co=np.einsum('a,aijl->ijl',v,h.XB).reshape(36,80);return const+cp.reshape(co@z,(6,6),order='C')
def transforms(u,gamma):
 x,y=map(float,u);UA=np.array([[x,0,-y,0],[0,x,0,-y],[y,0,x,0],[0,y,0,x]]);UH=np.kron(np.array([[x,-y],[y,x]]),np.eye(3))
 if gamma:UA=UA@GA;UH=UH@GH
 return UA,UH
constraints=[DQ>>0,nu==2048,cp.norm(leadreal,'inf')<=10];points=[];pointset=set()
def addpoint(eta,zeta,u,gamma):
 eta,zeta=R(eta),R(zeta);u=tuple(map(R,u));key=(eta,zeta,*u,gamma)
 if key in pointset:return
 pointset.add(key);points.append(key);UA,UH=transforms(u,gamma);A=np.array([1.,float(eta),0.,float(zeta)]);tt=1+float(eta*eta+zeta*zeta);w,g=float(eta-eta0),float(zeta-zeta0)
 Xhat=L.T@UH.T@X(UA@A)@UH;Xeta=L.T@UH.T@X(UA[:,1])@UH;Xzeta=L.T@UH.T@X(UA[:,3])@UH
 if w or g:
  DD=[[R(0)]*6 for _ in range(7)];DD[0][0]=eta-eta0;DD[1][0]=zeta-zeta0
  for j in range(1,6):DD[j+1][j]=R(1)
  DT=ca.transpose(DD);G0=ca.mm(DT,ca.mm(M_exact(eta,zeta),DD));WB=whiten_exact(G0);Z=tt*Xhat;dim=6
 else:
  DD=[[R(int(i==j)) for j in range(7)] for i in range(7)];DT=DD;G0=M_exact(eta,zeta);WB=whiten_exact(G0);dim=7
  Z=cp.vstack([cp.reshape(tt*Xeta[0],(1,6),order='C'),cp.reshape(tt*Xzeta[0],(1,6),order='C'),tt*Xhat[1:]])
 assert WB is not None
 WM=WB/float(u[0]*u[0]+u[1]*u[1]);WZ=WM@Z
 top=cp.Constant(WB@np.array(G0,float)@WB.T)
 for ell,MM in enumerate(lf.Ms):
  value=ca.mm(DT,ca.mm([[b.evaluate(p,[eta,zeta]) for p in row] for row in MM],DD));VV=WB@np.array(value,float)@WB.T;leadmax[ell]=max(leadmax[ell],float(la.norm(VV)));top=top+leadreal[ell]*VV
 constraints.append(cp.bmat([[top,WZ/64],[(WZ/64).T,(UH.T@DQ@UH)/4096]])-margin*np.eye(dim+6)>>0)
angles=[(R(1),R(0)),(R(1),R(1)),(R(0),R(1)),(R(1),R(-1))]
for gamma in (0,1):
 for eta,zeta in product((R(-1),R(-1,2),R(0),R(1,2),R(1)),repeat=2):
  for u in angles:addpoint(eta,zeta,u,gamma)
 for u in angles:addpoint(eta0,zeta0,u,gamma)
# Critical background, in a rational canonical chart.
uu=list(map(R,qc['lower_rank_one_output']));nn=list(map(R,qc['lower_rank_one_spatial']));ray=[uu[i]*nn[j] for i in range(2) for j in range(2)];H=[[b.evaluate(p,ray) for p in row] for row in h.HF];gg=[b.evaluate(b.diff(h.C,i),ray) for i in range(4)];ac=[-v for v in r.m.linear_solve(H,gg)]
if ac[0]**2+ac[2]**2>=ac[1]**2+ac[3]**2:
 gamma=0;u=(ac[0],ac[2]);eta=(ac[0]*ac[1]+ac[2]*ac[3])/(u[0]**2+u[1]**2);zeta=(ac[0]*ac[3]-ac[1]*ac[2])/(u[0]**2+u[1]**2)
else:
 gamma=1;u=(-ac[3],ac[1]);eta=-(ac[0]*ac[1]+ac[2]*ac[3])/(u[0]**2+u[1]**2);zeta=-(ac[0]*ac[3]-ac[1]*ac[2])/(u[0]**2+u[1]**2)
scale=max(u,key=abs);u=tuple(v/scale for v in u);addpoint(eta,zeta,u,gamma)
for u0 in angles:addpoint(eta,zeta,u0,gamma)
# Retain the narrow non-wave valleys discovered by the fixed-primitive
# attempt as actual point constraints, before trusting a new fit.
previous=json.loads((root/'work/graded_heat_adaptive_proposal.json').read_text())
for hist in previous.get('adaptive_history',[]):
 ee,ff,tt=hist['worst_coordinates'];oc=hist['output_chart'];ga=hist['Gamma_chart'];eu=R(round(ee*10**10),10**10);fv=R(round(ff*10**10),10**10);tv=R(round(tt*10**10),10**10);us=(R(1),tv) if oc==0 else (tv,R(1))
 addpoint(eu,fv,us,ga)
 for us0 in angles:addpoint(eu,fv,us0,ga)
# The continuum Bernstein attempt found this exact negative Schur value.
# It rejects the old correction, never the QC polynomial itself.
failure=json.loads((root/'work/heat_candidate_failure.json').read_text());fe,ff,ft=map(R,failure['coordinates']);foc=failure['output_chart'];fga=failure['Gamma_chart'];addpoint(fe,ff,(R(1),ft) if foc==0 else (ft,R(1)),fga)
for ee,zz in product((fe,-fe),(ff,-ff)):
 for ga in (0,1):
  for us0 in angles:addpoint(ee,zz,us0,ga)
lastfit=json.loads((root/'work/graded_heat_joint_second_proposal.json').read_text())
for hist in lastfit.get('adaptive_history',[]):
 ee,ff,tt=hist['worst_coordinates'];oc=hist['output_chart'];ga=hist['Gamma_chart'];eu=R(round(ee*10**10),10**10);fv=R(round(ff*10**10),10**10);tv=R(round(tt*10**10),10**10);addpoint(eu,fv,(R(1),tv) if oc==0 else (tv,R(1)),ga)
leadscale.value=1/np.sqrt(leadmax)
problem=cp.Problem(cp.Maximize(margin-1e-14*(cp.sum_squares(z)+cp.sum_squares(oq)+cp.sum_squares(lead))),constraints);problem.solve(solver='CLARABEL',tol_feas=1e-9,tol_gap_abs=1e-9,tol_gap_rel=1e-9,max_iter=400)
print('joint margin fit',problem.status,'nu',nu.value,'margin',margin.value,flush=True)
from scipy.optimize import minimize
allpowers=sorted(set(e for MM in [Mpoly]+lf.Ms for row in MM for p in row for e in p));PP=np.array(allpowers,int);MC0=np.array([[float(p.get(e,0)) for e in allpowers] for row in Mpoly for p in row]);MCD=np.array([[[float(p.get(e,0)) for e in allpowers] for row in MM for p in row] for MM in lf.Ms]);Dinvroot=np.diag(1/np.sqrt([1,2,1,1,2,1]));history=[]
critical_point=(float(eta),float(zeta),float(u[1] if u[0]==1 else u[0]),0 if u[0]==1 else 1,gamma)
for iteration in range(12):
 if z.value is None:break
 MC=MC0+np.einsum('l,lij->ij',np.array(leadreal.value),MCD)
 zz=np.array(z.value);zz+=la.lstsq(EN,rhsN-EN@zz)[0];XX=h.X0+np.einsum('aijl,l->aij',h.XB,zz);OO=sum(float(oq.value[p])*h.Wedges[p] for p in range(6))
 def xn(v):return np.einsum('a,aij->ij',v,XX)
 def score(x,outputchart,gamma):
  ee,ff,tt=map(float,x);u=(1.,tt) if outputchart==0 else (tt,1.);UA,UH=transforms(u,gamma);rho2=u[0]*u[0]+u[1]*u[1];A=np.array([1.,ee,0.,ff]);rad=1+ee*ee+ff*ff;w,g=ee-float(eta0),ff-float(zeta0);rr2=w*w+g*g
  MM=(MC@np.prod(np.array([ee,ff])[None,:]**PP,axis=1)).reshape(7,7)
  Xhat=L.T@UH.T@xn(UA@A)@UH;Xeta=L.T@UH.T@xn(UA[:,1])@UH;Xzeta=L.T@UH.T@xn(UA[:,3])@UH
  if rr2<1e-22:
   YY=rad*np.vstack([Xeta[0],Xzeta[0],Xhat[1:]]);GG=MM
  else:
   wn,gn=w/np.sqrt(rr2),g/np.sqrt(rr2);DT=np.zeros((7,6));DT[0,0]=wn;DT[1,0]=gn
   for j in range(1,6):DT[j+1,j]=1
   GG=DT.T@MM@DT;YY=rad*np.vstack([wn*Xeta[0]+gn*Xzeta[0],Xhat[1:]])
  try:cc=la.cho_factor((GG+GG.T)/2,lower=True);cost=YY.T@la.cho_solve(cc,YY)/rho2**2
  except la.LinAlgError:return 1e10*(1+max(0.,-float(la.eigvalsh((GG+GG.T)/2)[0])))
  RR=Dinvroot@(cost-UH.T@OO@UH)@Dinvroot/rho2
  return float(la.eigvalsh((RR+RR.T)/2)[-1]/2)
 scored=[]
 for oc,ga in product((0,1),repeat=2):
  grid=list(product(np.linspace(-1,1,5),np.linspace(-1,1,5),np.linspace(-1,1,5)))
  grid += [(float(eta0),float(zeta0),tt) for tt in np.linspace(-1,1,17)]
  grid += [critical_point[:3]]
  grid += [(float(fe),float(ff),float(ft)),(float(fe),float(ff),-float(ft))]
  for rr0 in (1e-3,.01,.05):
   grid += [(float(eta0)+rr0*np.cos(th),float(zeta0)+rr0*np.sin(th),tt) for th in np.linspace(0,2*np.pi,8,endpoint=False) for tt in (-.75,0,.75)]
  vals=sorted(((score(x,oc,ga),x) for x in grid if all(-1<=q<=1 for q in x)),reverse=True)
  candidates=vals[:12]
  for _,x in candidates:
   opt=minimize(lambda x:-score(x,oc,ga),np.array(x),method='L-BFGS-B',bounds=[(-1,1)]*3,options={'maxiter':100,'ftol':1e-12,'gtol':1e-5,'maxls':30})
   val=score(opt.x,oc,ga);scored.append((val,tuple(map(float,opt.x)),oc,ga))
  # At the acoustic zero optimize the one-dimensional output orbit directly.
  for t0 in np.linspace(-1,1,9):
   opt=minimize(lambda q:-score((float(eta0),float(zeta0),q[0]),oc,ga),[t0],method='L-BFGS-B',bounds=[(-1,1)],options={'maxiter':80,'ftol':1e-12});scored.append((score((float(eta0),float(zeta0),opt.x[0]),oc,ga),(float(eta0),float(zeta0),float(opt.x[0])),oc,ga))
 scored.sort(reverse=True);worst=scored[0];hist={'iteration':iteration,'nu':float(nu.value),'largest_numerical_required_nu':worst[0],'worst_coordinates':list(worst[1]),'output_chart':worst[2],'Gamma_chart':worst[3],'points':len(points),'finite_fit_margin':float(margin.value)};history.append(hist);print(json.dumps(hist),flush=True)
 out={'nu':float(nu.value),'leading_primitive_variation':leadreal.value.tolist(),'finite_fit_margin':float(margin.value),'all_cross_coefficients':zz.tolist(),'quadratic_two_form':oq.value.tolist(),'adaptive_history':history,'seconds':time.perf_counter()-start,'scope':'Adaptive continuous NUMERICAL proposal; no universal heat positivity or QC claim. Finite maximum searches cannot certify the continuum.'};(root/'work/graded_heat_joint_adaptive_proposal.json').write_text(json.dumps(out,indent=2)+'\n')
 if worst[0]<=float(nu.value)-.1 and float(margin.value)>0:break
 added=0
 for val,loc,oc,ga in scored:
  if val<=float(nu.value)+.01:continue
  e0,f0,t0=loc;eu=R(round(e0*10**10),10**10);fv=R(round(f0*10**10),10**10);tv=R(round(t0*10**10),10**10)
  if abs(e0-float(eta0))+abs(f0-float(zeta0))<1e-12:eu,fv=eta0,zeta0
  us=(R(1),tv) if oc==0 else (tv,R(1));oldn=len(points);addpoint(eu,fv,us,ga)
  if len(points)>oldn:added+=1
  if added>=6:break
 if not added:break
 leadscale.value=1/np.sqrt(leadmax)
 problem=cp.Problem(cp.Maximize(margin-1e-14*(cp.sum_squares(z)+cp.sum_squares(oq)+cp.sum_squares(lead))),constraints);problem.solve(solver='CLARABEL',tol_feas=1e-9,tol_gap_abs=1e-9,tol_gap_rel=1e-9,max_iter=400)
 if nu.value is None:print('adaptive solve',problem.status,flush=True);break
