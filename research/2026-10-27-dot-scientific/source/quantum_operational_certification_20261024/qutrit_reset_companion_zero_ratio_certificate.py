import sympy as S
u,v,w,z=S.symbols('u v w z');a=w/(1+v);b=u/(1+v);s=z/(1+v);th=1/(1+v)
x=1/(a+s);y=1/(b+s);h=1/s
g=S.factor(-3/(3+x)-1/(1+x+y+h)+2/(2+x+y)+2/(2+x+h));q=S.factor(s*g/(a+s)**2);base=4*(z-1)/((z+1)*(z+3)*(3*z+1))/th
r=S.factor(q/base);rn,rd=S.fraction(r)
num=S.expand(S.diff(rn,z)*rd-rn*S.diff(rd,z))
f=u**2*v**2*w+2*u**2*v**2-6*u**2*w**2-17*u**2*w-12*u**2+3*u*v**2*w**2+14*u*v**2*w+14*u*v**2+12*u*v*w**2+34*u*v*w+24*u*v-9*u*w**2-24*u*w-16*u+6*v**2*w**2+20*v**2*w+16*v**2+18*v*w**2+48*v*w+32*v
# All subsequent computations are exact; no cached polynomial is trusted.
grootnum,grootden=S.fraction(S.factor(g.subs(z,1)))
assert S.expand(grootnum+(v+1)*(w+1)**2*f)==0
q0=4*(z-1)/((z+1)*(z+3)*(3*z+1))
assert S.integrate(q0,(z,0,S.oo))==0
print('PASS: source crossing identity and baseline integral zero',flush=True)
A=S.Poly(f,v).nth(2);B=S.Poly(f,v).nth(1);C=-S.Poly(f,v).nth(0)/u
assert S.expand(B-2*C)==0
assert all(c>0 for c in S.Poly(A,u,w).coeffs())
assert all(c>0 for c in S.Poly(C,u,w).coeffs())
upper=S.factor(f.subs(v,u/2))
assert S.expand(upper-u**2*A/4)==0
lower=S.factor(f.subs(v,2*u/(u+4))*(u+4)**2)
expected=-u**2*(6*u**2*w**2+13*u**2*w+4*u**2+21*u*w**2+36*u*w+8*u+12*w**2+16*w)
assert S.expand(lower-expected)==0
print('PASS: quadratic root bounds 2u/(u+4)<=v<=u/2',flush=True)
# F is strictly increasing on v>=0 and F(0)=-uC.
assert S.degree(num,v)==7
rem=S.prem(num,f,v)
R,rr=S.div(rem,(z-1)**2,z)
assert rr==0 and S.degree(R,v)==1
P=S.Poly(R,u,v,w,z)
assert len(P.terms())==7607
assert sum(1 for c in P.coeffs() if c<0)==301
print('PASS: exact pseudo-remainder=(z-1)^2 R, R linear in v',flush=True)
# R=R0+v(Rplus-Rminus), with coefficientwise Rplus,Rminus>=0.
# Then (u+4)R >= L=(u+4)R0+2u Rplus-u(u+4)Rminus/2.
from collections import defaultdict
d=defaultdict(lambda:S.Integer(0))
for (i,j,k,l),c in P.terms():
    if j==0:
        d[i+1,k,l]+=c;d[i,k,l]+=4*c
    elif c<0:
        d[i+2,k,l]+=c/2;d[i+1,k,l]+=2*c
    else:
        d[i+1,k,l]+=2*c
L=S.Poly.from_dict(dict(d),(u,w,z))
assert len(L.terms())==4066
assert all(c>0 for c in L.coeffs())
print('PASS:4066 strictly positive lower-bound coefficients',flush=True)
print('L minimum coefficient:',min(L.coeffs()),'maximum:',max(L.coeffs()),flush=True)
# Strictness for u>0,z>0 including w=0: a surviving monomial suffices.
survivors=[(m,c) for m,c in L.terms() if m[1]==0 and m[0]>0]
assert survivors
print('Strictness monomial:',survivors[-1],flush=True)
