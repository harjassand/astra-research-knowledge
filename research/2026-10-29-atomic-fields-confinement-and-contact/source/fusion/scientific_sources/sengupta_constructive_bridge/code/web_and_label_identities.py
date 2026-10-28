"""Exact algebra used by the global tube and source-Hessian proofs."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parents[2]/'capability_backward_bridge/code/vendor'))
import sympy as s
p,q,t=s.symbols('p q t',positive=True,real=True);a=(p+q)/2;b=(q-p)/2;z=t+s.pi/4
x=a*s.cos(z)-b*s.sin(z);y=a*s.sin(z)-b*s.cos(z);zz=a*b+s.sin(2*z)/2
assert s.trigsimp((x+y)/s.sqrt(2)-p*s.cos(t))==0
assert s.trigsimp((x-y)/s.sqrt(2)+q*s.sin(t))==0
assert s.trigsimp(zz-((q*q-p*p)/4+s.Rational(1,2)-s.sin(t)**2))==0
w,Xp,Xm=s.symbols('w Xp Xm',real=True)
F=Xm**2/(4*w)-Xp**2/(4*(1-w))+s.Rational(1,2)-w
dF=s.factor(s.diff(F,w))
assert s.simplify(dF+Xm**2/(4*w*w)+Xp**2/(4*(1-w)**2)+1)==0
U,V,k,T=s.symbols('U V k T',positive=True,real=True);m=k*k
D1=1-T+m*U*U*T;D2=1-T+m*V*V*T
logu=1/(U-V)-m*U*T/D1;logv=-1/(U-V)-m*V*T/D2
assert s.factor(logv-(1-T+m*U*V*T)/((V-U)*D2))==0
pa=1/k-1;df2=1-(1-k*k)*T;Q=1-(1-k)*T
assert s.factor(pa*logu.subs({U:1,V:1/k})+Q/df2)==0
assert s.factor(pa*logv.subs({U:1,V:1/k})-Q)==0
# Full tangency identity, using real Jacobi addition formulas.
# b=Uu*s*c/(kappa*D1), e=Vv*s*c/(kappa*D2),
# A=d*(U/D1+V/D2), Uu²/kappa²=(1-U²)(1-mU²),
# Vv²/kappa²=(V²-1)(mV²-1). The metric cross terms cancel.
assert s.factor(logu/D2+logv/D1)==0
quadU=(1-U*U)*(1-m*U*U);quadV=(V*V-1)*(m*V*V-1)
clock=(U/D1+V/D2)*(-(1-m)+df2*(1-m*U*U)/D1+df2*(1-m*V*V)/D2)
assert s.factor(logu*quadU/D1+logv*quadV/D2+clock)==0
out=dict(status='PASS',inverse_derivative=str(dF),positive_psi_V_log_form=str((1-T+m*U*V*T)/((V-U)*D2)),Hessian_identity='psi_U(axis)=-Q/df²,psi_V(axis)=Q; U_uu=-kappa²(1-m),V_vv=kappa²(1-m)/k',full_field_label_tangency='PASS via quartic/Jacobi identities',scope='Exact algebra, with domains and zero-component inverse limits stated in MATHEMATICS.md.')
Path('results/web_and_label_identities.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
