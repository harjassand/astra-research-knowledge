"""Fig.29/30 sub-T stars: inherited boundary codes retained, no three-arm assumption."""
import json
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
 from t_star_joint_certificate import linbasis, solve
R=[]
for n,name,F in [(1,'blue-boundary',[0,1]),(1,'red-boundary',[0]),(2,'degree-two',[0,3])]:
 def rep(x):return min((x^f for f in F),key=lambda y:(y.bit_count(),y))
 g=[]
 for l in range(2):
  for j in range(n):g.append((1<<(2*n*l+j))|(1<<(2*n*l+n+j))|(1<<(4*n+j)))
 for block in range(5):
  for f in F[1:]:g.append(f<<(n*block))
 basis=linbasis(g);count=0
 for x in range(1<<(5*n)):
  a,p,b,q,c=[(x>>(n*j))&((1<<n)-1) for j in range(5)]
  U,V,W=rep(a^p),rep(b^q),rep(p^q^c)
  if U!=V or W:continue
  count+=1;target=U|(U<<(2*n));sol=solve(basis,x^target)
  assert sol is not None
  assert 2*U.bit_count()<=x.bit_count()
 R.append(dict(arms=n,color=name,tested=1<<(5*n),matching=count,passed=True))
print(json.dumps(R,indent=2))
