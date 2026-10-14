import sympy as S
f,a,L=S.symbols('f a L', real=True)
p=12*f-L;r=4*f-L
beta=(9*a*a/p+a*a/r-2*L)/4
delta=(9*a*a/p-a*a/r)/4
k,l,i,j,g,h=S.symbols('k l i j g h',real=True)
z2=i*i+j*j; w2=k*k+l*l; rr=i*k+j*l; ss=j*k-i*l
F=f*z2**2+beta*z2*w2+g*w2**2+delta*(rr**2-ss**2)+a*z2*rr+h*w2*rr
C=S.diff(F,i).subs({i:-3*a*k/p,j:-a*l/r})
cs=[S.factor(S.expand(C).coeff(k,3)),S.factor(S.expand(C).coeff(k,1).coeff(l,2))]
print('cubic coeffs',cs)
print('difference',S.factor(cs[0]-cs[1]))
