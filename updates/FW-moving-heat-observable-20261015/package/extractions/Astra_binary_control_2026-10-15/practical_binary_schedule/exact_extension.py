import sympy as s,itertools,time,json
k=3; a=s.Matrix([2,3,5]);astar=7
B=s.Matrix([[0,s.Rational(1,5),s.Rational(1,7)],[s.Rational(2,7),0,s.Rational(1,9)],[s.Rational(1,6),s.Rational(1,8),0]])
truthu=s.Matrix([[s.Rational(1,10),s.Rational(1,11),s.Rational(1,12)]]);truthv=s.Matrix([s.Rational(1,13),s.Rational(1,14),s.Rational(1,15)])
x=s.symbols('x0:3');h={};contexts={}
for mask in range(1,8):
 T=[i for i in range(3) if mask>>i&1];inv=(s.eye(len(T))+B.extract(T,T)).inv();p=inv*s.ones(len(T),1);q=a.extract(T,[0]).T*inv;u=truthu.extract([0],T);v=truthv.extract(T,[0]);h[mask]=s.factor((astar-(q*v)[0])*(1-(u*p)[0])/(1-(u*inv*v)[0]));contexts[mask]=(T,inv,p,q)
y=[(h[1<<i]-astar+astar*x[i])/((h[1<<i]+a[i])*x[i]-a[i]) for i in range(3)]
polys=[]
for mask in [3,5,6,7]:
 T,inv,p,q=contexts[mask];u=s.Matrix([[x[i] for i in T]]);v=s.Matrix([y[i] for i in T]);expr=h[mask]*(1-(u*inv*v)[0])-(astar-(q*v)[0])*(1-(u*p)[0]);polys.append(s.Poly(s.cancel(expr).as_numer_denom()[0],*x).monic().as_expr())
print('degrees',[s.Poly(f,*x).total_degree() for f in polys],flush=True)
t=time.time();gb=s.groebner(polys,*x,order='grevlex');print('time',time.time()-t,'basis',list(gb),flush=True)
open('/workspace/shared/practical_binary_schedule/exact_extension_receipt.json','w').write(json.dumps({'polynomial_degrees':[s.Poly(f,*x).total_degree() for f in polys],'groebner_basis':[str(p) for p in gb],'seconds':time.time()-t},indent=2))
solutions=s.solve(list(gb),x,dict=True)
for sol in solutions:
 vals=[s.factor(yy.subs(sol)) for yy in y];print('solution',sol,'v',vals,'singleton denominators',[s.factor(((h[1<<i]+a[i])*x[i]-a[i]).subs(sol)) for i in range(3)],flush=True)
valid=[];excluded=[]
for sol in solutions:
 den=[s.factor(((h[1<<i]+a[i])*x[i]-a[i]).subs(sol)) for i in range(3)]
 num=[s.factor((h[1<<i]-astar+astar*x[i]).subs(sol)) for i in range(3)]
 if any(d==0 for d in den):
  assert any(d==0 and nn!=0 for d,nn in zip(den,num));excluded.append({'u':[str(sol[xx]) for xx in x],'denominators':[str(d) for d in den],'numerators':[str(nn) for nn in num]});continue
 vv=s.Matrix([s.factor(yy.subs(sol)) for yy in y]);uu=s.Matrix([[sol[xx] for xx in x]])
 for mask,(T,inv,p,q) in contexts.items():
  ut=uu.extract([0],T);vt=vv.extract(T,[0]);dd=s.factor(1-(ut*inv*vt)[0]);assert dd!=0
  assert s.factor((astar-(q*vt)[0])*(1-(ut*p)[0])/dd-h[mask])==0
 valid.append({'u':[str(z) for z in uu],'v':[str(z) for z in vv]})
# If singleton elimination coefficient vanishes, its numerator is never zero for this receipt.
exceptional=[]
for i in range(3):
 xx=a[i]/(h[1<<i]+a[i]);nn=s.factor(h[1<<i]-astar+astar*xx);assert nn!=0;exceptional.append(str(nn))
assert len(valid)==1
open('/workspace/shared/practical_binary_schedule/exact_extension_receipt.json','w').write(json.dumps({'anchor_B':[[str(B[i,j]) for j in range(3)] for i in range(3)],'anchor_a':[str(z) for z in a],'new_a':astar,'marginal_readings':{str(mask):str(v) for mask,v in h.items()},'polynomial_degrees':[s.Poly(f,*x).total_degree() for f in polys],'groebner_basis':[str(p) for p in gb],'valid_extensions':valid,'excluded_poles':excluded,'nonzero_exceptional_singleton_numerators':exceptional},indent=2))
