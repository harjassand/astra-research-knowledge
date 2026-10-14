import sympy as s,numpy as np,pickle,os,itertools
BASE=os.path.dirname(__file__)
with open(BASE+'/c4_heat_symbolic.pkl','rb') as f:z=pickle.load(f)
a=s.symbols('a b c d',real=True);h=s.symbols('h0:6',real=True);x=a[0]+s.I*a[2];y=a[1]+s.I*a[3];X=h[0]+s.I*h[3];Y=h[1]+s.I*h[4];Z=h[2]+s.I*h[5]
bplus=[x*X+s.I*y*Z,x*Z+s.I*y*X,y*Y+s.I*x*Y]
bminus=[x*X-s.I*y*Z,x*Z-s.I*y*X,y*Y-s.I*x*Y]
pa=list(itertools.combinations_with_replacement(range(4),2));ph=list(itertools.combinations_with_replacement(range(6),2))
def ex(p,n):
 e=[0]*n
 for j in p:e[j]+=1
 return tuple(e)
idx={ex(p,4)+ex(q,6):i for i,(p,q) in enumerate(itertools.product(pa,ph))}
def vec(poly):
 v=s.zeros(210,1)
 for exp,c in s.Poly(s.expand(poly),*(a+h)).terms():
  if c:v[idx[exp]]=c
 return v
ij3=list(itertools.combinations_with_replacement(range(3),2));Tspin=[]
for b in [bplus,bminus]:
 Tspin.append(s.Matrix.hstack(*[vec(s.re(s.expand(b[i]*s.conjugate(b[j])))*(1 if i==j else 2)) for i,j in ij3]))
T=z['T'].row_join(Tspin[0]).row_join(Tspin[1]);C=z['P']*T
print('rank',C.rank(), 'shape',C.shape,flush=True)
z.update(T=T,C=C,spin_basis=[bplus,bminus])
with open(BASE+'/c4_spin2.pkl','wb') as f:pickle.dump(z,f)
