from sos_family import *
Cm=x*(u*u-v*v)-2*y*u*v
pm=S.Matrix([0,0,x*u-y*v,-x*v-y*u]);pmi=S.Matrix([0,0,x*v+y*u,x*u-y*v])
LCm=S.simplify(K.T*(heat(Cm)+correction(f*pm+g*pmi))*K)
r1,r2=S.symbols('r1 r2',real=True)
cross=2*S.re(r1*S1*cc+r2*S2*bb)
eq=S.Poly(S.expand(cross-(hh.T*LCm.subs(f,0)*hh)[0]),*A,*hh).coeffs();solm=S.solve(eq,[r1,r2,g],dict=True)
print('minus cubic cross solution',solm)
