import sympy as s,numpy as np,json
from pathlib import Path
from scipy.optimize import differential_evolution
out=Path(__file__).parent
x=s.Matrix(s.symbols('a b c d'));a,b,c,d=x;u=a*a+c*c;v=b*b+d*d;q=a*d-b*c;w=a*b+c*d;r=u-v
F=s.expand(u*u+v*v+s.Rational(166,3)*u*v-s.Rational(460,9)*w*w-s.Rational(52,9)*q*r);grad=s.Matrix([s.diff(F,t) for t in x]);Hess=s.hessian(F,x)
ff=s.lambdify([x],F,'numpy');df=s.lambdify([x],grad,'numpy');hf=s.lambdify([x],Hess,'numpy');qf=s.lambdify([x],q,'numpy');J=np.array(s.hessian(q,x),float);R=np.array(s.hessian(r,x),float)
def toh(z):th,ph=z;return np.array([np.cos(th/2),np.sin(th/2)*np.cos(ph),0,np.sin(th/2)*np.sin(ph)])
def test(z,be,ret=False):
 h=toh(z);g=np.array(df(h),float).ravel();al=3968/39-6*be/13;T=.5*np.array(hf(h),float)-qf(h)*.5*(al*J+be*R)-np.outer(g,g)/(4*ff(h));e,V=np.linalg.eigh(T);return (e[0],V[:,0]) if ret else e[0]
lo=-100.;hi=100.;cuts=[]
for i in range(20):
 be=(lo+hi)/2
 sol=differential_evolution(lambda z:test(z,be),[(0,np.pi),(0,2*np.pi)],tol=1e-10,popsize=20,maxiter=200,seed=101+i,polish=True);ev,A=test(sol.x,be,True);H=toh(sol.x)
 # rational rounding of both vectors, independent of any numerical eigenvalue claim
 AA=s.Matrix([s.Rational(float(t)).limit_denominator(100) for t in A]);HH=s.Matrix([s.Rational(float(t)).limit_denominator(100) for t in H]);sx=dict(zip(x,AA));sh=dict(zip(x,HH));FA=F.subs(sx);FH=F.subs(sh);GA=grad.subs(sh).dot(AA);HH2=HH.dot(Hess.subs(sx)*HH);qA=q.subs(sx);rA=r.subs(sx);qH=q.subs(sh)
 c0=s.factor(2*FH*HH2-GA**2-4*s.Rational(3968,39)*qA*FH*qH);cb=s.factor(4*(rA-s.Rational(6,13)*qA)*FH*qH);bound=c0/cb
 rec={'A':[str(t) for t in AA],'H':[str(t) for t in HH],'C0':str(c0),'Cb':str(cb),'bound':str(bound),'direction':'upper' if cb>0 else 'lower','beta_probe':be,'numeric_min':ev}
 cuts.append(rec)
 if cb>0:hi=min(hi,float(bound))
 else:lo=max(lo,float(bound))
 print(i,be,ev,rec['direction'],float(bound),'range',lo,hi,flush=True)
 if lo>hi:break
(out/'QUADRATIC_PC_CUTS.json').write_text(json.dumps({'cuts':cuts,'lo':lo,'hi':hi},indent=2)+'\n')
