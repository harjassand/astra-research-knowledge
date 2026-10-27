import mpmath as m
m.mp.dps=60
p=m.mpf(1)/4;q=1-p;a=p/3
w=[m.mpf(1)/2,m.mpf(1)/4,m.mpf(1)/4];b=[q*x/3 for x in w]
r=[m.mpf(3)/4,m.mpf(99)/100,m.mpf(3)/40]
def P(x,s):return x/(x+s)
def integr(s):
 z=P(a,s);z3=P(3*a,s);v=[P(x,s) for x in b]
 return z3*v[2]/(3*(1-z3*sum(r[i]*v[i] for i in range(3))/3))+z*P(3*b[2],s)/(1-r[2]*z*P(3*b[2],s))-sum(z*v[2]/(1-z*(r[i]*v[i]+r[2]*v[2])/2) for i in [0,1])
d=m.quad(integr,[0,m.mpf('.001'),m.mpf('.01'),m.mpf('.1'),1,10,m.inf])
print('exact-source overlap derivative',m.nstr(d,50));assert d< -m.mpf('.0023')
def value(t):
 rr=[r[0],r[1],t]
 def fun(s):
  z=P(a,s);z3=P(3*a,s);v=[P(x,s) for x in b]
  return -m.log(1-z3*sum(rr[i]*v[i] for i in range(3))/3)-sum(m.log(1-rr[i]*z*P(3*b[i],s)) for i in range(3))+2*sum(m.log(1-z*(rr[i]*v[i]+rr[j]*v[j])/2) for i in range(3) for j in range(i+1,3))
 return m.quad(fun,[0,m.mpf('.001'),m.mpf('.01'),m.mpf('.1'),1,10,100]) + m.quad(fun,[100,m.mpf('1e5')])
# Finite high tail truncation avoids loss of precision in a balanced log formula.
# Its O(s^-2) tail after 1e5 is negligible for the strict .0001 comparisons.
vals=[value(t) for t in [m.mpf(0),m.mpf('.5'),m.mpf(1)]]
for t,v in zip([0,.5,1],vals):print('overlap',t,'truncated value',m.nstr(v,40))
assert vals[1] < min(vals[0],vals[2])-m.mpf('.0001')
def tf(G):return sum(x*m.log(x) for x in m.eigsy(G,eigvals_only=True) if x>m.mpf('1e-55'))
def scalarf(x):return x*m.log(x) if x else m.mpf(0)
def LM(x,ys,cs):
 G=m.zeros(len(ys)+1);G[0,0]=x
 for i,(y,c) in enumerate(zip(ys,cs),1):G[i,i]=y;G[0,i]=G[i,0]=m.sqrt(c*x*y)
 return tf(G)-scalarf(x)-sum(map(scalarf,ys))
def eigvalue(t):
 rr=[r[0],r[1],t]
 return LM(3*a,b,[x/3 for x in rr])+sum(LM(a,[3*b[i]],[rr[i]]) for i in range(3))-2*sum(LM(a,[b[i],b[j]],[rr[i]/2,rr[j]/2]) for i in range(3) for j in range(i+1,3))
for t in [0,m.mpf('.5'),1]:print('exact Gram value',t,m.nstr(eigvalue(t),50))
r[2]=m.mpf(0)
d0=m.quad(integr,[0,m.mpf('.001'),m.mpf('.01'),m.mpf('.1'),1,10,m.inf])
print('affine coherent c3 curvature at0',m.nstr(128*d0,50));assert 128*d0< -m.mpf('.33')
