import sympy as s,pickle
from pathlib import Path
P=Path(__file__).parent
A,L,E,Z,S,N,c=s.symbols('A L E Z S N c')
C=L-A+Z/2;D=L-A-Z/2;B=S-2*L+A-E
names=['0->A','A->0','2A->AC','AC->2A','2A->AD','AD->2A','2A->AE','AE->2A','AE->CD','CD->AE','CD->AB','AB->CD']
jumps=[(1,1,0,0,1),(-1,-1,0,0,-1),(-1,-s.Rational(1,2),0,1,0),(1,s.Rational(1,2),0,-1,0),(-1,-s.Rational(1,2),0,-1,0),(1,s.Rational(1,2),0,1,0),(-1,-1,1,0,0),(1,1,-1,0,0),(-1,0,-1,0,0),(1,0,1,0,0),(1,0,0,0,0),(-1,0,0,0,0)]
rates=[1,A,A*(A-1),A*C,A*(A-1),A*D,A*(A-1),A*E,A*E,2*C*D,C*D,A*B]
vars=[A,L,E,Z,S]
def move(f,j):return f.subs({v:v+x for v,x in zip(vars,j)},simultaneous=True)
def G(f):return s.factor(sum(rate*(move(f,j)-f) for rate,j in zip(rates,jumps)))
F=L-s.Rational(3,4)*E**2/N+A*E/N
V=E**2/(N*L)-c*A*E/(N*L)
R=E**2/(N*L)
F1=R-A*E*R/(N*L)
GF=s.factor(G(F));GV=G(V);GF1=G(F1)
r,u,t,a,z,delta=s.symbols('r u t a z delta')
sub={N:r/(u*u*t),E:r/(u*t),L:1/t,A:a/t,Z:z/t,S:(1+delta)*r/(u*u*t)}
# normalize physical drift by EL/N=u/t
nv=s.factor(GV.subs(sub)/(u/t));nf1=s.factor(GF1.subs(sub)/(u/t))
print('GF',GF)
for name,f in [('V',nv),('F1',nf1)]:
 print(name,'a degree',s.degree(s.fraction(f)[0],a))
 for i in range(4):
  cc=s.factor(s.Poly(f,a).coeff_monomial(a**i));print('a^',i,':',cc)
with (P/'practical_algebra.pkl').open('wb') as fp:pickle.dump(dict(A=A,L=L,E=E,Z=Z,S=S,N=N,c=c,r=r,u=u,t=t,a=a,z=z,delta=delta,names=names,jumps=jumps,rates=rates,GF=GF,GV=GV,GF1=GF1,nv=nv,nf1=nf1),fp)
(P/'exact_practical_formulas.txt').write_text('GF = '+str(GF)+'\nGV = '+str(GV)+'\nnormalized V = '+str(nv)+'\nnormalized F1 = '+str(nf1)+'\n')
