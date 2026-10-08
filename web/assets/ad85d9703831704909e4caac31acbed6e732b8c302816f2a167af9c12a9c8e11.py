"""Exact small-dimensional audit of a sufficient co-Choi tensor certificate."""
import sympy as s

def red2(c,t):
    d=2; out=s.zeros(4)
    # (D - t id) tensor (D - t id), standard trace convention.
    for i in range(2):
      for j in range(2):
       for k in range(2):
        for l in range(2):
         val=t*t*c[2*i+j,2*k+l]
         if i==k: val-=t*sum(c[2*a+j,2*a+l] for a in range(2))
         if j==l: val-=t*sum(c[2*i+a,2*k+a] for a in range(2))
         if i==k and j==l: val+=s.trace(c)
         out[2*i+j,2*k+l]=val
    return out

def build(t):
    u=s.Matrix([1,0,0,1]);ells=[]
    for a in range(4):
        e=s.eye(4)[:,a]
        ells.append(red2(e*u.T,t))
    A=red2(u*u.T,t);ai=A.inv()
    R=s.zeros(16);S=s.zeros(16)
    for a in range(4):
      for b in range(4):
        E=s.zeros(4);E[b,a]=1
        R[4*a:4*a+4,4*b:4*b+4]=red2(E,t)
        S[4*a:4*a+4,4*b:4*b+4]=ells[b]*ai*ells[a].T
    return R,S

if __name__=='__main__':
 R,S=build(s.Rational(1,2))
 v=(S+s.Rational(11,9)*R).nullspace()[0]
 den=s.ilcm(*[e.q for e in v]);v=v*den
 print('v=',list(v))
 print('Rv norm=',(v.T*R*v)[0], 'Sv=',(v.T*S*v)[0])
 assert S*v == -s.Rational(11,9)*R*v
 print('tensor-square value',(v.T*R*v)[0]**2-(v.T*S*v)[0]**2)
 t=s.symbols('t',real=True)
 Rt,St=build(t)
 print('general qR',s.factor((v.T*Rt*v)[0]))
 print('general qS',s.factor((v.T*St*v)[0]))
 print('RplusS',s.factor((v.T*(Rt+St)*v)[0]))
 print('RminusS',s.factor((v.T*(Rt-St)*v)[0]))
