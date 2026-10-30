exec(open(__file__.replace('heat_family.py','heat_attack.py')).read().split('f,g,j,k=')[0])
q0,q1,q2,q3,q4=S.symbols('q0:5',real=True)
az=S.Matrix([-y,x,0,0]);aw=S.Matrix([0,0,-v,u]);rw=S.Matrix([0,0,u,v]);PP=q0*r*az+q1*t*az+q2*r*aw+q3*t*aw+q4*r*rw
BFgen=heat(F)+correction(PP);eq=[]
for ox,oy in [(1,0),(0,1),(1,1),(1,-1)]:
 for nx,ny in [(1,0),(0,1),(1,1),(1,-1)]:
  U=S.Matrix([[ox,-oy],[oy,ox]]);V=S.Matrix([[nx,-ny],[ny,nx]]);K=U*S.diag(S.Rational(1,3),1)*V.T
  ac={x:K[0,0]+K[1,1],y:K[1,0]-K[0,1],u:K[0,0]-K[1,1],v:K[1,0]+K[0,1]}
  hh=S.Matrix([ox*nx*nx,ox*nx*ny,ox*ny*ny,oy*nx*nx,oy*nx*ny,oy*ny*ny]);eq.extend(BFgen.subs(ac)*hh)
print('fullleading constraints',S.solve(eq,[q0,q1,q2,q3,q4],dict=True))
leadsol=S.solve(eq,[q0,q1,q2,q3,q4],dict=True)[0];BFgen=BFgen.subs(leadsol)
f,g,j,k=S.symbols('f g j k',real=True);PC=S.Matrix([0,0,x*u+y*v,y*u-x*v]);PCi=S.Matrix([0,0,x*v-y*u,x*u+y*v]);PQ=S.Matrix([-j*y/2,j*x/2,-k*v/2,k*u/2]);B=BFgen+heat(C)+f*correction(PC)+g*correction(PCi)+heat(Q)+correction(PQ)
hh=S.Matrix([1,-1,1,1,-1,1]);tau=S.symbols('tau',real=True);Ac={x:-S.Rational(1,4),y:tau,u:-tau/2,v:-S.Rational(1,4)}
eq=[]
for e in B.subs(Ac)*hh:eq.extend(S.Poly(S.expand(e),tau).all_coeffs())
sol=S.solve(eq,[q1,q3,f,g,j,k],dict=True);print('fullboundary sol',sol)
for ss in sol:
 B0=S.simplify(B.subs(ss).subs({x:0,y:0,u:0,v:0}));print('B0',B0)
 print('B0 base subspaces',[(S.factor((hh0.T*B0*hh0)[0])) for hh0 in [S.Matrix([1,0,0,0,1,0]),S.Matrix([0,0,1,1,0,0]),S.Matrix([1,0,-1,0,0,0])]])
BFdiag=S.simplify(BFgen.subs({y:0,v:0,u:1}));print('BF diag blocks')
for ids in [[0,2,4],[1,3,5]]:
 Dg=BFdiag.extract(ids,ids);print(Dg);print('det',S.factor(Dg.det()));print('minors',[S.factor(Dg[:n,:n].det()) for n in (1,2)])
