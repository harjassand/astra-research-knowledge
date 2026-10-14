import sympy as s,json
from pathlib import Path
a,b,c,d=s.symbols('a b c d');vs=(a,b,c,d);u=a*a+c*c;v=b*b+d*d;q=a*d-b*c
F=s.expand(3*(u+v-2*q)**2+s.Rational(35,24)*u*u+q*q-s.Rational(5,2)*q*u)
DF=s.Matrix([s.diff(F,z) for z in vs]);HF=s.hessian(F,vs);I=s.Matrix([1,0,0,1]);X=s.Matrix(vs)
x,y,r=s.symbols('x y r', positive=True);kk=y*(1-y);ff2=x*(1-x)
def integ(P):
 out=0
 for ff,lo,hi in [(2*x,0,s.Rational(1,3)),(1-x,s.Rational(1,3),1)]:
  pol=s.expand(P.subs({a:s.diff(ff,x)*kk,b:ff*s.diff(kk,y),c:s.diff(ff2,x)*kk,d:ff2*s.diff(kk,y)}))
  out+=s.integrate(s.integrate(pol,(x,lo,hi)),(y,0,1))
 return s.factor(out)
HP=s.Matrix(4,4,lambda i,j:integ(HF[i,j]));BP=s.Matrix([integ(e) for e in DF]);CP=integ(F);CC=s.Matrix(4,4,lambda i,j:integ(X[i]*X[j]));M4=integ((u+v)**2)
Hbase=HF.subs({a:0,b:1,c:0,d:0})/2;cbase=F.subs({a:0,b:1,c:0,d:0})/2
print('HP',HP,'BP',BP,'CP',CP,'cov',CC,'covrank',CC.rank(),'M4',M4,sep='\n',flush=True)
print('direction H', (I.T*HP*I)[0], 'direction b',BP.dot(I),flush=True)
Hr=Hbase+r*HP;br=s.sqrt(r)*BP
minors=[s.factor(Hr[:j,:j].det()) for j in range(1,5)]
print('minors',minors,flush=True)
loss=s.factor((br.T*Hr.inv()*br)[0]/2)
lim=s.factor(BP.dot(I)**2/(2*(I.T*HP*I)[0]));assert s.limit(loss,r,0)==lim
print('loss(r)',loss,'limit',lim,flush=True)
gap=s.factor(cbase+CP-loss);print('gap',gap,'limit',s.limit(gap,r,0),flush=True)
Path(__file__).with_name('fullrank_pulse.json').write_text(json.dumps({'spike_H':list(map(str,HP)),'spike_b':list(map(str,BP)),'spike_c':str(CP),'spike_C':list(map(str,CC)),'spike_M4':str(M4),'spike_covrank':CC.rank(),'H_positive_minors':list(map(str,minors)),'loss':str(loss),'limit':str(lim),'gap':str(gap)},indent=2))
