import sympy as S
x,y,u,v=S.symbols('x y u v',real=True); A=S.Matrix([x,y,u,v]);r=x*x+y*y;t=u*u+v*v
F=t*t+2*r*t;C=x*(u*u-v*v)+2*y*u*v
h=S.Matrix(S.symbols('h0:6',real=True))
X=S.Matrix([h[0]+h[4],h[3]-h[1],h[0]-h[4],h[3]+h[1]]);Y=S.Matrix([h[1]+h[5],h[4]-h[2],h[1]-h[5],h[4]+h[2]])
Jx=X.jacobian(h);Jy=Y.jacobian(h)
def correction(P):
 W=P.jacobian(A).T-P.jacobian(A);temp=Jx.T*W*Jy
 return S.expand((temp+temp.T)/2)
def heat(f):
 H=S.hessian(f,A);return S.expand(Jx.T*H*Jx+Jy.T*H*Jy)
q1,q3,f,g,j,k,lam=S.symbols('q1 q3 f g j k lam',real=True)
az=S.Matrix([-y,x,0,0]);aw=S.Matrix([0,0,-v,u]);rw=S.Matrix([0,0,u,v])
PF=(q1/8+S.Rational(3,2))*r*az+q1*t*az+(6-q3)*r*aw+q3*t*aw
PC=f*S.Matrix([0,0,x*u+y*v,y*u-x*v])+g*S.Matrix([0,0,x*v-y*u,x*u+y*v]);PQ=j*az/2+k*aw/2
BF=heat(F)+correction(PF);BC=heat(C)+correction(PC);BQ=heat(lam*(r+t))+correction(PQ)
B=BF+BC+BQ
if __name__=='__main__':
 print('BF blocks at y=v=0')
 for ids in [[0,2,4],[1,3,5]]:
  blk=S.simplify(BF.subs({y:0,v:0}).extract(ids,ids)); print(blk); print('det',S.factor(blk.det())); print('2minors',[S.factor(blk.extract(ii,ii).det()) for ii in [(0,1),(0,2),(1,2)]])
 print('BC full',BC); print('BQ',BQ)
