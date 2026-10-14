#!/usr/bin/env python3
"""Independent exact mixed local/mean gate checks; no source code imported."""
from pathlib import Path
import argparse,json,platform,time
import sympy as s

def main(out):
 start=time.monotonic();q,v,b,c,theta=s.symbols('q v b c theta',positive=True);beta=b*(1-theta);a=3*b*b/(16*c)
 f=lambda z:a*z*z/2-b*z**4/4+c*z**6/6
 h=a*v+c*v**5
 D=f(q)-f(v)+theta*b*(q**4-v**4)/4+beta*v*v*(q*q-v*v)/2-h*(q-v)
 P4=q**4+2*q**3*v+3*q*q*v*v+4*q*v**3+5*v**4
 K=a/2-beta*(q+v)**2/4+c*P4/6
 assert s.expand(D-(q-v)**2*K)==0
 t=s.symbols('t',nonnegative=True);P=t**4+2*t**3+3*t*t+4*t+5;ratio=P/(t+1)**4
 assert s.simplify(s.diff(ratio,t)-2*(t**3-3*t-8)/(t+1)**5)==0
 roots=s.polys.polytools.intervals(t**3-3*t-8,eps=s.Rational(1,10**12))
 assert len(roots)==1 and roots[0][0][0]>2 and roots[0][0][1]<3
 alpha=s.RootOf(t**3-3*t-8,0);rmin=ratio.subs(t,alpha);theta_path=1-s.sqrt(rmin)
 lin=1-s.sqrt(15)/4;conv=1-s.sqrt(15)/6
 assert 0<float(lin)<float(theta_path)<float(conv)<1
 # An exact finite-amplitude counterexample with all homogeneous Hessians positive.
 N=32;th=s.Rational(1,10);vv=s.Rational(1,4);w=s.Rational(5,8);bb=cc=1;aa=s.Rational(3,16);hh=aa*vv+vv**5
 bare=lambda z:aa*z*z/2-z**4/4+z**6/6
 E=lambda zs:sum(bare(z)-hh*z+th*z**4/4 for z in zs)+(1-th)*sum(z*z for z in zs)**2/(4*len(zs))
 diff=s.factor(E([w]+[vv]*(N-1))-E([vv]*N));assert diff<0
 chem=s.factor(D.subs({q:w,v:vv,b:bb,c:cc,theta:th}));assert chem<0
 assert s.simplify(diff-chem-(1-th)*(w*w-vv*vv)**2/(4*N))==0
 linear_margin=aa-(1-th)**2/5;assert linear_margin==s.Rational(51,2000)>0
 # Direct vector differentiation, including the global removal identity.
 qs=s.symbols('x0:4',real=True);U,B=s.symbols('U B',positive=True);nn=len(qs);S2=sum(z*z for z in qs)
 gate=theta*U*sum(z**4 for z in qs)/4+(1-theta)*U*S2*S2/(4*nn)
 remove=gate-U*nn*B**4/4-U*B**3*sum(z-B for z in qs)
 exact=theta*U*sum((z-B)**2*(z*z+2*B*z+3*B*B) for z in qs)/4+(1-theta)*U*(S2-nn*B*B)**2/(4*nn)+(1-theta)*U*B*B*sum((z-B)**2 for z in qs)/2
 assert s.expand(remove-exact)==0
 energy=sum(f(z) for z in qs)+gate.subs(U,b)
 Hess=s.hessian(energy,qs);M2=S2/nn
 expected=s.diag(*[a-3*beta*z*z+5*c*z**4+beta*M2 for z in qs])+2*beta*s.Matrix(qs)*s.Matrix(qs).T/nn
 assert s.simplify(Hess-expected)==s.zeros(nn)
 Hhom=Hess.subs({z:v for z in qs});one=s.ones(nn,1)
 assert s.simplify(Hhom*one-(a+5*c*v**4)*one)==s.zeros(nn,1)
 zvec=s.Matrix([1,-1,0,0]);assert s.simplify(Hhom*zvec-(a-2*beta*v*v+5*c*v**4)*zvec)==s.zeros(nn,1)
 # A positive semidefinite nonlocal gate need not be convex in q.
 J=s.Matrix([[1,-1],[-1,1]]);xx,yy=s.symbols('xx yy',real=True);r=s.Matrix([xx*xx,yy*yy]);g=(r.T*J*r)[0]/4
 assert s.hessian(g,(xx,yy)).subs({xx:1,yy:0})==s.diag(3,-1)
 result=dict(status='PASS',python=platform.python_version(),sympy=s.__version__,seconds=time.monotonic()-start,groups=8,
 sharp_global_path_threshold=dict(alpha_definition='unique positive root of t^3-3t-8=0',alpha=str(s.N(alpha,18)),formula='1-sqrt((alpha^4+2alpha^3+3alpha^2+4alpha+5)/(alpha+1)^4)',theta=str(s.N(theta_path,18))),
 homogeneous_linear_threshold=str(s.N(lin,18)),all_N_global_convexity_threshold=str(s.N(conv,18)),
 finite_amplitude_counterexample=dict(N=N,theta=str(th),selected_q=str(vv),alternative_q=str(w),uniform_bias=str(hh),chemical_tangent_gap=str(chem),total_energy_difference=str(diff),homogeneous_Hessian_margin=str(linear_margin)),
 removal_identity='Exact nonnegative local Bregman plus mean-square and endpoint-distance terms.',
 full_spatial_Hessian=str(expected),kernel_countermodel=dict(J=[[1,-1],[-1,1]],H_at_1_0=[[3,0],[0,-1]]),
 scope='Exact conditional control theorem and finite-cell countermodel. Ideal gate available only as mathematical ansatz;no material implementation,finite-temperature success,work-recovery efficiency,novelty or device performance established.')
 out.mkdir(parents=True,exist_ok=True);(out/'MIXED_GATE_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',required=True,type=Path);main(ap.parse_args().output_dir)
