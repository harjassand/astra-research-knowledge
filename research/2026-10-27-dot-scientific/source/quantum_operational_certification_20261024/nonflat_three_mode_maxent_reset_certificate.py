"""Exact receiving only: no numerical optimization, no inherited PASS."""
import sympy as S
from math import comb
from pathlib import Path
import json,itertools,hashlib
s,b,c,d=S.symbols('s b c d');C=[S.Integer(1),c,d];pol=lambda v:S.Poly(v,s,b,c,d)
O=[6*(s+b)*(s+C[i])*(s+C[j])-b*(C[i]*(s+C[j])+C[j]*(s+C[i])) for i in range(3) for j in range(i)]
J=S.cancel((3*(s+b)*S.prod(3*s+x for x in C)-b*sum(C[i]*S.prod(3*s+C[j] for j in range(3) if j!=i) for i in range(3)))/s)
R=[3*(s+b)*(s+3*x)-b*x for x in C]
num=pol(3**27*s**9);den=pol(64)
for x in C:num*=pol((s+x)**2);den*=pol((3*s+x)**6)
for o in O:num*=pol(o)**2
den*=pol(J)**3
for rr in R:den*=pol(rr)
N=num-den;assert N.degree(s)==31
ends={j:sum(v*b**bb*c**cc*d**dd for (jj,bb,cc,dd),v in N.terms() if jj==j) for j in (0,31)}
assert S.expand(ends[31]-711559752519106944*(1+c*c+d*d))==0
assert S.expand(ends[0]+884736*b**3*c**7*d**7*(b*c*d+b*c+b*d+c*d)**3)==0
co={j:{} for j in range(32)}
# c=z/(1+z),d=w/(1+w), multiply all coefficients by(1+z)^10(1+w)^10.
for (j,bb,cc,dd),val in N.terms():
 assert cc<=10 and dd<=10
 for z in range(cc,11):
  for w in range(dd,11):
   key=(bb,z,w);co[j][key]=co[j].get(key,0)+int(val)*comb(10-cc,z-cc)*comb(10-dd,w-dd)
co={j:{k:v for k,v in row.items() if v} for j,row in co.items()}
for j in range(13):assert all(v<0 for v in co[j].values())
for j in range(28,32):assert all(v>0 for v in co[j].values())
path=Path(__file__).with_name('nonflat_three_mode_maxent_reset_chain_weights.json');ww=json.loads(path.read_text())['weights'];mons=list(itertools.product(range(2),repeat=3));report=[]
for j in range(13,27):
 weights=ww[str(j)];assert len(weights)==16 and all(v>=0 for v in weights) and sum(weights[:8])>0 and sum(weights[8:])>0
 out={}
 for row,sg,part in [(co[j],-1,weights[:8]),(co[j+1],1,weights[8:])]:
  for mult,m in zip(part,mons):
   for key,v in row.items():
    target=tuple(x+y for x,y in zip(key,m));out[target]=out.get(target,0)+sg*mult*v
 assert all(v>=0 for v in out.values()),j
 positive={k:v for k,v in out.items() if v};assert positive
 canonical='\n'.join(str(k)+':'+str(v) for k,v in sorted(positive.items()))
 report.append({'chain':j,'positive_coefficients':len(positive),'zero_coefficients':len(out)-len(positive),'sha256':hashlib.sha256(canonical.encode()).hexdigest()})
 print(j,'PASS',len(positive),'positive coefficients,',len(out)-len(positive),'zero coefficients',flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'degree':31,'domain':'b>0,0<c,d<1','coefficient_transform':'(1+z)^10(1+w)^10; c=z/(1+z),d=w/(1+w)','chains':report,'weight_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))
print('PASS all14 exact chains. Coefficients0..12 negative,28..31 positive.')
