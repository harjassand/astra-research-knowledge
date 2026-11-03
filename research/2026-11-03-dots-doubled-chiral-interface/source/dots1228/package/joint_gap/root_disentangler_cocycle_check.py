from fractions import Fraction as F
import itertools,random,json
random.seed(12)
tets=[(tuple(j for j in range(5) if j!=i),(-1)**i)for i in range(5)]
edges=list(itertools.combinations(range(5),2));faces=list(itertools.combinations(range(5),3))
def rnd(x):
 y=x+F(1,2);return y.numerator//y.denominator

def sf(u):
 m={(a,b):rnd(u[b]-u[a])for a,b in edges}
 n={(a,b,c):m[b,c]-m[a,c]+m[a,b]for a,b,c in faces}
 return sum(s*m[a,b]*n[b,c,d]for (a,b,c,d),s in tets)
def omega(u,th,A,V):
 dt={(a,b):th[b]-th[a]for a,b in edges};du={(a,b):u[b]-u[a]for a,b in edges}
 m={e:rnd(du[e]+V*dt[e])for e in edges}
 n={(a,b,c):m[b,c]-m[a,c]+m[a,b]for a,b,c in faces}
 C={(a,b):A*m[a,b]-(rnd(A*u[b])-rnd(A*u[a]))-A*V*(rnd(th[b])-rnd(th[a]))for a,b in edges}
 return sum(s*(th[a]*C[a,b]*n[b,c,d]+A*V*dt[a,b]*(rnd(th[c])-rnd(th[b])-rnd(dt[b,c]))*(m[c,d]-rnd(u[d])+rnd(u[c])))for (a,b,c,d),s in tets)
pars=[(2,2),(-8,1)];errors={'cocycle':0,'input_periodicity':0,'ancilla_periodicity':0};examples=[]
for trial in range(100):
 us=[[F(random.randrange(-20,21),19)for _ in range(5)]for _ in pars];th=[F(random.randrange(-20,21),19)for _ in range(5)];beta=F(random.randrange(-20,21),19)
 w=sum(omega(u,th,A,V)for u,(A,V)in zip(us,pars))
 wp=sum(omega(u,[x+beta for x in th],A,V)for u,(A,V)in zip(us,pars))
 goal=beta*sum(A*sf([u[j]+V*th[j]for j in range(5)])for u,(A,V)in zip(us,pars))
 if wp-w!=goal:errors['cocycle']+=1;examples.append(str(wp-w-goal))
 ui=[u[:] for u in us];ui[0][trial%5]+=1
 diff=sum(omega(u,th,A,V)for u,(A,V)in zip(ui,pars))-w
 if diff.denominator!=1:errors['input_periodicity']+=1
 tt=th[:];tt[trial%5]+=1
 diff=sum(omega(u,tt,A,V)for u,(A,V)in zip(us,pars))-w
 if diff.denominator!=1:errors['ancilla_periodicity']+=1
print(errors,examples[:3]);json.dump({'trials':100,'exact_rational_errors':errors,'first_cocycle_residuals':examples[:3]},open('producer-workspace/root_disentangler_cocycle_check.json','w'),indent=2)
