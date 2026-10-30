from complex_heat import *
I=S.I
zz=x+I*y;ww=u+I*v;aa=a+I*b;bb=c+I*d;cc=e+I*ff
S1=zz*bb+2*ww*aa;S2=zz*cc+2*ww*bb;S3=2*S.conjugate(ww)*aa+zz*S.conjugate(cc)
Ts=[S.conjugate(zz)*aa+2*S.conjugate(ww)*bb,zz*S.conjugate(bb)+2*ww*S.conjugate(cc),2*S.conjugate(ww)*bb+zz*S.conjugate(bb)]
c1,c2,c3=S.symbols('c1 c2 c3',real=True);GG=S.symbols('g11 g12 g13 g22 g23 g33',real=True)
G=S.Matrix([[GG[0],GG[1],GG[2]],[GG[1],GG[3],GG[4]],[GG[2],GG[4],GG[5]]])
expr=c1*S1*S.conjugate(S1)+c2*S2*S.conjugate(S2)+c3*S3*S.conjugate(S3)
expr+=sum(G[ii,jj]*S.conjugate(Ts[ii])*Ts[jj] for ii in range(3) for jj in range(3))
eq=S.Poly(S.expand(expr-(hh.T*LF*hh)[0]),*A,*hh).coeffs();sol=S.solve(eq,[c1,c2,c3,*GG,q1,q3],dict=True)[0]
print('leading solutions',sol)
d2,d3,d0,d1,d4=S.symbols('d2 d3 d0 d1 d4',real=True); ds=S.Matrix([d0,d1,d4])
cross=2*S.re(d2*S2*S.conjugate(aa)+d3*S3*S.conjugate(bb)+sum(ds[ii]*Ts[ii]*S.conjugate(cc) for ii in range(3)))
eq=S.Poly(S.expand(cross-(hh.T*LC.subs(f,0)*hh)[0]),*A,*hh).coeffs();solc=S.solve(eq,[d2,d3,d0,d1,d4,g],dict=True)[0]
print('cubic solutions',solc)
print('G after',G.subs(sol));print('c after',[cc0.subs(sol) for cc0 in [c1,c2,c3]])
