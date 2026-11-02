import mpmath as m
m.mp.dps=60
L=m.sqrt(m.pi);H=L/2
v=1/m.e+m.mpf('.00001')
def ent(v):
 def integrand(s):
  a=[m.exp(-(s+j*L)**2/(2*v))/m.sqrt(2*m.pi*v) for j in range(-15,16)]
  g=sum(a);p=sum(y for j,y in zip(range(-15,16),a) if j%2)/g
  return -2*g*(p*m.log(p,2)+(1-p)*m.log(1-p,2))
 return m.quad(integrand,[0,H/4,H/2,3*H/4,H])
for r in [m.mpf(1),m.mpf(2),m.mpf(3),m.mpf(4)]:
 a=ent(v/r);b=ent(v*r)
 print('v',m.nstr(v,50),'r',r,'Hsmall',m.nstr(a,50),'Hlarge',m.nstr(b,50),'Ic',m.nstr(1-a-b,50),flush=True)
