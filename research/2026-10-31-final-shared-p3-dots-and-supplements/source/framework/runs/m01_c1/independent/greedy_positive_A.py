import sys,json,itertools,random,math
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
here=Path(__file__).parent
raw=json.loads((here/'two_free.json').read_text());pol={tuple(m):F(c) for m,c in raw if m[0]>0}
base={m:c for m,c in pol.items() if all(e%2==0 for e in m)}
odd=[(m,c) for m,c in pol.items() if any(e%2 for e in m)]
def pairs(m):
 ids=[i for i,e in enumerate(m) if e%2]
 ans=[]
 for signs in itertools.product([-1,1],repeat=len(ids)):
  if signs[0]<0:continue
  v=[0]*len(m)
  for i,s in zip(ids,signs):v[i]=s
  # retain multidegrees of the individual output vectors
  if v[1]+v[2] or v[3]+v[4]:continue
  a=tuple(e+w for e,w in zip(m,v));b=tuple(e-w for e,w in zip(m,v))
  if min(a+b)>=0:ans.append((a,b))
 return ans
options={m:pairs(m) for m,c in odd}
rng=random.Random(7);found=False
for trial in range(50):
 rem=base.copy();todo=odd.copy();rng.shuffle(todo)
 # rank by the amount of diagonal product available relative to the cross coefficient.
 todo.sort(key=lambda mc:max([float(base.get(a,0)*base.get(b,0)/(mc[1]*mc[1])) for a,b in options[mc[0]]]+[0]))
 cert=[];failed=None
 for m,c in todo:
  cand=[]
  for a,b in options[m]:
   d1=rem.get(a,0);d2=rem.get(b,0)
   if d1<=0 or d2<=0:continue
   score=float(d1*d2/(c*c));cand.append((score,a,b))
  if not cand:failed=m;break
  cand.sort(reverse=True);_,a,b=cand[0];d1=rem[a];d2=rem[b]
  if d1*d2<c*c/4:failed=m;break
  # rational weight near the balanced relative consumption
  ratio=math.sqrt(float(d1/d2));rat=F(ratio).limit_denominator(1000)
  w1=abs(c)*rat/2;w2=c*c/(4*w1)
  if w1>d1 or w2>d2:
   low=c*c/(4*d2);high=d1;w1=(low+high)/2;w2=c*c/(4*w1)
  rem[a]-=w1;rem[b]-=w2;cert.append((m,c,a,b,w1,w2))
 if failed is None:
  found=True;print('FOUND',trial,'squares',len(cert),'residue',sum(c!=0 for c in rem.values()),flush=True)
  out={'pairs':[[list(m),str(c),list(a),list(b),str(w1),str(w2)] for m,c,a,b,w1,w2 in cert],'residue':[[list(m),str(c)] for m,c in rem.items() if c]}
  (here/'two_free_positive_A_sos.json').write_text(json.dumps(out));break
 if trial==0:print('first fail',failed,'processed',len(cert),'of',len(todo),flush=True)
print('found',found)
