"""Independent Fraction-only check of each recorded online oracle output."""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,math,time
root=Path(__file__).parent;data=json.load(open(root/'online_ftpl_result.json'));pairs=list(itertools.combinations_with_replacement(range(4),2))
def exp(pair):
 e=[0]*4
 for i in pair:e[i]+=1
 return tuple(e)
z=[exp(pair) for pair in pairs];groups={}
for i in range(10):
 for j in range(i,10):groups.setdefault(tuple(a+b for a,b in zip(z[i],z[j])),[]).append((i,j,1 if i==j else 2))
exps=sorted(groups);q2square={tuple(2*(int(k==i)+int(k==j)) for k in range(4)):1 if i==j else 2 for i in range(4) for j in range(i,4)}
count=0;max_gap=F(0);st=time.time()
for records in data['oracle_calls']:
 for record in records:
  c=record['certificate'];assert c['status']=='certified' and c['method']=='rational_SOS';scale=c['gram_scale'];co={e:F(v)/scale for e,v in zip(exps,record['query'])};lo=F(c['normalized_lower']);qr=[F(v) for v in c['quaternion']];G=[[F(v) for v in row] for row in c['gram']]
  assert sum(v*v for v in qr)==1
  assert all(G[i][j]==G[j][i] for i in range(10) for j in range(10))
  for e,terms in groups.items():assert sum(a*G[i][j] for i,j,a in terms)==co[e]-lo*q2square.get(e,0)
  # Independent Schur elimination of exact positive pivots.
  A=[row[:] for row in G]
  for i in range(10):
   assert A[i][i]>0
   for j in range(i+1,10):
    for k in range(j,10):A[j][k]-=A[j][i]*A[i][k]/A[i][i];A[k][j]=A[j][k]
  upper=sum(a*math.prod(qr[i]**e[i] for i in range(4)) for e,a in co.items())*scale
  assert upper==F(c['upper']) and lo*scale==F(c['lower'])
  gap=upper-lo*scale;assert 0<=gap<=F(data['requested_gap']);max_gap=max(max_gap,gap);count+=1
out=dict(exact_online_certificates=count,max_absolute_gap=float(max_gap),requested_gap=data['requested_gap'],seconds=time.time()-st,scope='Verifies all returned rotations/global objective gaps; does not independently replay quantum trajectory or certify experimental performance.')
(root/'independent_online_certificate_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
