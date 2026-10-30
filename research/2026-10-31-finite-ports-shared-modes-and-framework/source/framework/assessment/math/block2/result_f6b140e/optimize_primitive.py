"""Residual-circle reduction of every possible polynomial leading heat primitive."""
from leading_rigidity import *
x1,x2,y1,y2,P1,P2,Q1,Q2,R1,R2=s.symbols('x1 x2 y1 y2 P1 P2 Q1 Q2 R1 R2',real=True)
vars=[x1,x2,y1,y2,P1,P2,Q1,Q2,R1,R2]
sub={a:(x1+y1)/2,b:(y2-x2)/2,c:(x2+y2)/2,d:(x1-y1)/2,h[0]:P1+2*Q1+R1,h[1]:-P2+R2,h[2]:-P1+2*Q1-R1,h[3]:P2+2*Q2+R2,h[4]:P1-R1,h[5]:-P2+2*Q2-R2}
LF=s.expand(L.subs(dict(zip(coef,sol))).subs(sub,simultaneous=True)/16)
rot=sum(w*(-vars[i+1]*s.diff(LF,vars[i])+vars[i]*s.diff(LF,vars[i+1])) for i,w in zip(range(0,10,2),[-4,-2,-5,-3,-1]))
reflection=LF.subs({x2:-x2,y2:-y2,P2:-P2,Q2:-Q2,R2:-R2},simultaneous=True)-LF
free=sorted(set().union(*(e.free_symbols for e in sol)) & set(coef),key=str)
ss=list(s.linsolve(s.Poly(rot,*vars).coeffs()+s.Poly(reflection,*vars).coeffs(),free))[0]
Lsym=s.expand(LF.subs(dict(zip(free,ss))))
print('symmetric leading parameters',ss,flush=True)
open(__file__.replace('.py','_density.txt'),'w').write(str(Lsym)+'\n')
print('remaining free',sorted(Lsym.free_symbols & set(coef),key=str),flush=True)
r,t,z=s.symbols('r t z',real=True)
Lrt=s.expand(Lsym.subs({coef[55]:24*(1+r),coef[59]:36*(1+t)}))
real_block=(s.hessian(Lrt,[P1,Q1,R1])/2).subs({x1:z,x2:0,y1:1,y2:0})
imag_block=(s.hessian(Lrt,[P2,Q2,R2])/2).subs({x1:z,x2:0,y1:1,y2:0})
print('real block',real_block.applyfunc(s.factor),flush=True)
print('imag block',imag_block.applyfunc(s.factor),flush=True)
for name,mat in [('real',real_block),('imag',imag_block)]:
    print(name,'det',s.factor(mat.det()),flush=True)
    print(name,'2minors',[s.factor(mat.extract(ids,ids).det()) for ids in combinations(range(3),2)],flush=True)
