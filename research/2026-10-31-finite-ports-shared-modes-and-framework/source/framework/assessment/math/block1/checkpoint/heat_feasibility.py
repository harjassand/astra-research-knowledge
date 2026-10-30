exec(open(__file__.replace('heat_feasibility.py','heat_attack.py')).read().split('f,g,j,k=')[0])
q0,q1,q2,q3,q4=S.symbols('q0:5',real=True)
az=S.Matrix([-y,x,0,0]);aw=S.Matrix([0,0,-v,u]);rw=S.Matrix([0,0,u,v]);PP=q0*r*az+q1*t*az+q2*r*aw+q3*t*aw+q4*r*rw
BFgen=heat(F)+correction(PP);eq=[]
for ox,oy in [(1,0),(0,1),(1,1),(1,-1)]:
 for nx,ny in [(1,0),(0,1),(1,1),(1,-1)]:
  U=S.Matrix([[ox,-oy],[oy,ox]]);V=S.Matrix([[nx,-ny],[ny,nx]]);K=U*S.diag(S.Rational(1,3),1)*V.T
  ac={x:K[0,0]+K[1,1],y:K[1,0]-K[0,1],u:K[0,0]-K[1,1],v:K[1,0]+K[0,1]}
  hh=S.Matrix([ox*nx*nx,ox*nx*ny,ox*ny*ny,oy*nx*nx,oy*nx*ny,oy*ny*ny]);eq.extend(BFgen.subs(ac)*hh)
print('fullleading constraints',S.solve(eq,[q0,q1,q2,q3,q4],dict=True))
leadsol=S.solve(eq,[q0,q1,q2,q3,q4],dict=True)[0];BFgen=BFgen.subs(leadsol)
f,g,j,k=S.symbols('f g j k',real=True);PC=S.Matrix([0,0,x*u+y*v,y*u-x*v]);PCi=S.Matrix([0,0,x*v-y*u,x*u+y*v]);PQ=S.Matrix([-j*y/2,j*x/2,-k*v/2,k*u/2]);B=BFgen+heat(C)+f*correction(PC)+g*correction(PCi)+heat(Q)+correction(PQ)
hh=S.Matrix([1,-1,1,1,-1,1]);tau=S.symbols('tau',real=True);Ac={x:-S.Rational(1,4),y:tau,u:-tau/2,v:-S.Rational(1,4)}
eq=[]
for e in B.subs(Ac)*hh:eq.extend(S.Poly(S.expand(e),tau).all_coeffs())
sol=S.solve(eq,[q1,q3,f,g,j,k],dict=True);print('fullboundary sol',sol)
for ss in sol:
 B0=S.simplify(B.subs(ss).subs({x:0,y:0,u:0,v:0}));print('B0',B0)
 print('B0 base subspaces',[(S.factor((hh0.T*B0*hh0)[0])) for hh0 in [S.Matrix([1,0,0,0,1,0]),S.Matrix([0,0,1,1,0,0]),S.Matrix([1,0,-1,0,0,0])]])
# numerical cutting-plane feasibility in the two remaining constants
import numpy as np
BB=S.simplify(B.subs(sol[0]));Bbase=BB.subs({j:0,k:0});Bj=S.diff(BB,j);Bk=S.diff(BB,k)
funcs=[S.lambdify((x,y,u,v),mat,'numpy') for mat in (Bbase,Bj,Bk)]
# w can be made real by the exact residual rotational symmetry
points=[(a,b,c,0) for a in [-4,-2,-1,-.5,-.25,0,.25,.5,1,2,4] for b in [0,.25,.5,1,2] for c in [0,.125,.25,.5,1,2,4]]
matrices=[tuple(np.array(ff(*pt),float) for ff in funcs) for pt in points]
poly=[(-10.,-10.),(10.,-10.),(10.,10.),(-10.,10.)]
def cut(poly,aa,bb,cc):
 out=[]
 for P,Q in zip(poly,poly[1:]+poly[:1]):
  fp=aa*P[0]+bb*P[1]+cc;fq=aa*Q[0]+bb*Q[1]+cc
  if fp>=-1e-12:out.append(P)
  if (fp>0 and fq<0) or (fp<0 and fq>0):
   z=fp/(fp-fq);out.append((P[0]+z*(Q[0]-P[0]),P[1]+z*(Q[1]-P[1])))
 return out
cuts=[]
for it in range(150):
 if not poly:break
 jj,kk=np.mean(poly,axis=0);worst=(0,None,None)
 for pt,mats in zip(points,matrices):
  mat=mats[0]+jj*mats[1]+kk*mats[2];ev,U=np.linalg.eigh(mat)
  if ev[0]<worst[0]:worst=(ev[0],pt,U[:,0])
 print('iter',it,'params',jj,kk,'eig',worst[0],'polyvertices',len(poly),flush=True)
 if worst[0]>-1e-9:break
 _,pt,hh=worst;hh=np.round(hh*100)/100;idx=points.index(pt);mm=matrices[idx]
 aa,bb,cc=[float(hh@mm[ii]@hh) for ii in [1,2,0]];cuts.append((pt,hh.tolist(),aa,bb,cc));poly=cut(poly,aa,bb,cc)
print('polygon',poly)
print('cuts',cuts)
