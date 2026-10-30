"""Independent exact-formula diagnostic, not a uniform tail proof."""
import mpmath as m, json
m.mp.dps=160
ys=[(0,72),(3,60),(5,36),(6,0)];ks=[2,1,1,1]
def F(a,b):
 r=m.log(m.mpf(a)+2)/m.log(m.mpf(b)+2);g0=m.log(2)/14
 if r<=20:g=g0
 elif r>=30:g=0
 else:
  t=(r-20)/10;g=g0*(1-3*t*t+2*t*t*t)
 return b*g

def falling(n,k):
 if n<k:return m.mpf(0)
 return m.fprod(n-j for j in range(k))
def defect(a,b):
 terms=[];out=[]
 for i,(u,v) in enumerate(ys):
  mon=falling(a,u)*falling(b,v);out.append(ks[i]*mon)
  if not mon:terms.append(m.mpf(0));continue
  h=(i-1)%4;du=ys[h][0]-u;dv=ys[h][1]-v
  coef=ks[h]*m.power(2,du)*m.exp(F(a+du,b+dv)-F(a,b))-ks[i]
  terms.append(coef*mon)
 return m.nstr(sum(terms)/max(out+[m.mpf(1)]),24)
rows=[]
for a,b in [(100**25,100),(1000**25,1000),(10**6,0),(10**6,1),(10**6,2),(10**60,0),(10**60,1),(10**60,2)]:
 rows.append({'A':str(a),'B':b,'normalized_defect':defect(a,b)})
print(json.dumps({'precision_digits':m.mp.dps,'scope':'Direct exact adjoint formula finite diagnostic only; no eventual threshold inferred.','rows':rows},indent=2))
