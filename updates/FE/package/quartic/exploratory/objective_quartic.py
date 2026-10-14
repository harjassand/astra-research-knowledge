import sympy as S
x=S.symbols('a b c d'); a,b,c,d=x
s,t=S.symbols('s t')
pars=S.symbols('A B C E G H L M N'); AA,BB,CC,EE,GG,HH,LL,MM,NN=pars
u=a*a+c*c;v=b*b+d*d;w=a*b+c*d;q=a*d-b*c
basis=[u*u,v*v,u*v,w*w,u*w,v*w,q*u,q*v,q*w]
F=sum(p*f for p,f in zip(pars,basis))
ac=S.expand(s*s*S.diff(F,a,a)+2*s*t*S.diff(F,a,b)+t*t*S.diff(F,b,b))
M11=S.hessian(ac.coeff(s,2).coeff(t,0),x)/2
M12=S.hessian(ac.coeff(s,1).coeff(t,1),x)/4
M22=S.hessian(ac.coeff(s,0).coeff(t,2),x)/2
if __name__=='__main__':
 for name,m in [('M11',M11),('M12',M12),('M22',M22)]:print(name);print(m)
