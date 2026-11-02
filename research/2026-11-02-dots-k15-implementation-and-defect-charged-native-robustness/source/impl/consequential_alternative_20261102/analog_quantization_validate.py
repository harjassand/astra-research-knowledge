import json,sys
import mpmath as mp
mp.mp.dps=50
L=mp.sqrt(mp.pi);H=L/2
F=lambda z:(1+mp.erf(z/mp.sqrt(2)))/2
entropy=lambda p:-(p*mp.log(p,2)+(1-p)*mp.log(1-p,2))
records=json.load(open('producer-workspace/analog_quantization_results.json'))
out=[]
for record in records['results']:
 v=1/mp.e if record['v']<.369 else mp.mpf('.37');s=mp.sqrt(v)
 def densities(x):
  values=[mp.exp(-(x+m*L)**2/(2*v))/mp.sqrt(2*mp.pi*v) for m in range(-8,9)]
  return sum(values),sum(value for m,value in zip(range(-8,9),values) if m%2)
 def fun(x):
  g,a=densities(x)
  return 2*g*entropy(a/g)
 hc=mp.quad(fun,[0,H/4,H/2,3*H/4,H])
 obj={'v':str(v),'continuous_Ic':str(1-2*hc),'binned':[]}
 for r in record['records']:
  edges=[mp.mpf(0)]+[mp.mpf(str(x)) for x in r['thresholds']]+[H]
  hb=mp.mpf(0)
  for a,b in zip(edges[:-1],edges[1:]):
   values=[2*(F((b+m*L)/s)-F((a+m*L)/s)) for m in range(-8,9)]
   w=sum(values);e=sum(value for m,value in zip(range(-8,9),values) if m%2)
   hb+=w*entropy(e/w)
  obj['binned'].append({'B':r['B'],'Ic':str(1-2*hb),'binning_loss':str(2*(hb-hc))})
 out.append(obj)
print(json.dumps(out,indent=2))
