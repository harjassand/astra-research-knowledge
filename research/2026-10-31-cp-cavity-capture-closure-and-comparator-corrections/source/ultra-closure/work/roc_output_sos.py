"""Lossless fixed-spatial-angle ROC representation by a 14 by 14 Gram.

Matrix Fejer--Riesz on a binary quartic gives necessity, including
singular matrices; the polynomial kernel reduces 18 features to 14.
The remaining spatial angle is NOT removed by finitely many samples.
"""
from pathlib import Path
from fractions import Fraction as R
import sys,json,time
import numpy as np,scipy.linalg as la,cvxpy as cp
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import roc_inner_model as m
b,ca=m.b,m.ca

def at(side,t):
 TOP,CC,QQ=m.charts[2*side];M=[[sum(v*t**ee[1] for ee,v in P.items() if ee[0]==0) for P in row] for row in TOP];G=np.zeros((4,4,12));Q=np.zeros((3,9))
 for j,col in enumerate(CC):
  for i,P in enumerate(col):
   for (s,k),v in P.items():G[s,i,j]+=float(v*t**k)
 for j,P in enumerate(QQ):
  P=m.divide_norm(P)
  for (s,k),v in P.items():Q[s,j]+=float(v*t**k)
 return M,G,Q

def skew(v):
 pairs=list(__import__('itertools').combinations(range(4),2));return sum(v[k]*(np.eye(4)[i,:,None]@np.eye(4)[j,None,:]-np.eye(4)[j,:,None]@np.eye(4)[i,None,:]) for k,(i,j) in enumerate(pairs))

def gram(M,G,Q,c,q,margin=0):
 L=la.cholesky(np.array(M,float),lower=True);W=la.solve_triangular(L,np.eye(4),lower=True);gg=[W@G[k]@c/64 for k in range(4)];qq=Q@q/4096;S0=cp.Variable(6);S1=cp.Variable(6);P=cp.Variable((4,4));v=cp.Variable(4);w=cp.Variable(4);s0,s1=skew(S0),skew(S1);top=cp.bmat([[np.eye(4),s0,P],[s0.T,2*np.eye(4)-P-P.T,s1],[P.T,s1.T,np.eye(4)]]);cross=cp.vstack([cp.hstack([cp.reshape(gg[0],(4,1),order='C'),cp.reshape(v,(4,1),order='C')]),cp.hstack([cp.reshape(gg[1]-v,(4,1),order='C'),cp.reshape(gg[2]-w,(4,1),order='C')]),cp.hstack([cp.reshape(w,(4,1),order='C'),cp.reshape(gg[3],(4,1),order='C')])]);bottom=cp.bmat([[cp.reshape(qq[0],(1,1),order='C'),cp.reshape(qq[1]/2,(1,1),order='C')],[cp.reshape(qq[1]/2,(1,1),order='C'),cp.reshape(qq[2],(1,1),order='C')]]);Z=cp.bmat([[top,cross],[cross.T,bottom]]);return Z-margin*np.eye(14)>>0,{'Gram':Z,'L':L,'P':P,'S0':S0,'S1':S1,'v':v,'w':w}

def c0_coordinates():
 from fractions import Fraction
 cv=list(map(Fraction,m.qc['example_cubic_coefficients']));op=list(map(lambda row:list(map(Fraction,row)),m.qc['normal_form_operator']));return np.array([float(sum(a*v for a,v in zip(row,cv))/s) for row,s in zip(op,m.scales)])

if __name__=='__main__':
 start=time.perf_counter();c0=c0_coordinates();nu=cp.Variable(nonneg=True);qT=np.array([float(sum(x*x for x in pw)==4) for pw in m.qpowers]);t=R(-385371,1000000);M,G,Q=at(0,t);con,state=gram(M,G,Q,c0,nu*qT);p=cp.Problem(cp.Minimize(nu),[con]);p.solve(solver='CLARABEL',tol_gap_abs=1e-7,tol_gap_rel=1e-10,tol_feas=1e-10,max_iter=300);print('lossless output-angle test',p.status,'least nu',nu.value,flush=True)
 # Compare the exact-one-angle Gram optimum to a direct continuous search.
 from scipy.optimize import minimize_scalar
 MI=la.inv(np.array(M,float));GC=np.einsum('kij,j->ki',G,c0)
 def cost(angle):
  x,y=np.cos(angle),np.sin(angle);v=np.array([x**3,x*x*y,x*y*y,y**3])@GC;return float(v@MI@v/(2*(1+float(t*t))))
 aa=np.linspace(0,np.pi,2049);k=int(np.argmax([cost(a) for a in aa]));opt=minimize_scalar(lambda th:-cost(th),bounds=(aa[k]-.003,aa[k]+.003),method='bounded',options={'xatol':1e-14});out={'spatial_side':0,'spatial_t':str(t),'Gram_size':14,'least_nu_Gram_numerical':float(nu.value),'largest_nu_direct_numerical':cost(opt.x),'status':p.status,'scope':'Numerical validation of the lossless fixed-spatial-angle algebra. No removal of the remaining spatial quantifier and no new QC or ROC separation.','seconds':time.perf_counter()-start};(root/'work/roc_output_sos_test.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
