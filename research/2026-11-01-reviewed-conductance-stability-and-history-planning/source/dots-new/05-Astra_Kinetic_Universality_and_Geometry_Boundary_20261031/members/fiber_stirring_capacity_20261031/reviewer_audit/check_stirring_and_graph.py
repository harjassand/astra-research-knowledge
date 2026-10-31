from fractions import Fraction as F
import itertools,json,random
import sympy as s
rng=random.Random(431);checks=0;graphs=0
for m in range(2,6):
 edges=list(itertools.combinations(range(m),2))
 for mask in range(1<<len(edges)):
  E=[e for j,e in enumerate(edges) if mask>>j&1];graphs+=1
  independent=[S for k in range(1,m+1) for S in itertools.combinations(range(m),k) if not any(i in S and j in S for i,j in E)]
  S=max(independent,key=len);alpha=len(S)
  def q(w):return sum(x*x for x in w)+2*sum(w[i]*w[j] for i,j in E)
  w=[F(int(i in S),alpha) for i in range(m)]
  assert q(w)==F(1,alpha);checks+=1
  raw=[rng.randrange(1,7) for i in range(m)];w=[F(x,sum(raw)) for x in raw];original=q(w)
  while True:
   pair=next(((i,j) for i,j in E if w[i] and w[j]),None)
   if pair is None:break
   i,j=pair;u=w.copy();v=w.copy();u[i]+=u[j];u[j]=0;v[j]+=v[i];v[i]=0
   new=min([u,v],key=q);assert q(new)<=q(w);checks+=1;w=new
  assert q(w)>=F(1,alpha) and original>=q(w);checks+=1
# Algebra of a genuinely nonradial homogeneous constructor, without cutoff approximation.
y,x,z,b,k,beta=s.symbols('y x z b k beta',positive=True)
U=x**4+z**4+3*x*x*z*z;v=1+k*(1-y*y)**2;T=b*b-y*y
assert s.expand((-s.diff(T,y)*s.diff(v*U,y)+s.diff(T,y,2)/beta)-(-2/beta+2*y*s.diff(v*U,y)))==0;checks+=1
chi=s.Function('chi');psi=s.Function('psi');c=s.Matrix([-s.diff(U,z),s.diff(U,x)])*chi(U)*psi(y)
assert s.simplify(c.dot(s.Matrix([s.diff(v*U,x),s.diff(v*U,z)])))==0;checks+=1
assert s.simplify(s.diff(c[0],x)+s.diff(c[1],z))==0;checks+=1
print(json.dumps({'status':'PASS_EXACT_ALGEBRA','graphs':graphs,'checks':checks,'scope':'Exact finite graph support compression and explicit constructor/exit-generator algebra only; not a numerical PDE/capacity solver or proof of global receiving.'},indent=2))
