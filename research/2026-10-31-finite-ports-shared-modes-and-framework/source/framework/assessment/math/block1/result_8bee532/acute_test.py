import json,math,time
from fractions import Fraction
from collections import defaultdict
from pathlib import Path
start=time.time(); base=Path(__file__).parent
data=json.loads((base/'shift_1.json').read_text())
min_e=min(k[0] for k,v in data['terms']);print('min_e',min_e,flush=True)
pol=defaultdict(Fraction)
for (ee,pp,a,b,c),co in data['terms']:
 assert ee%2==0
 n=(ee-min_e)//2;co=Fraction(co)
 for i in range(n+1):
  for j in range(n-i+1):
   power=pp+2*j
   pol[(i,power,a,b,c)]+=co*math.comb(n,i)*math.comb(n-i,j)*(-1)**j
pol={k:v for k,v in pol.items() if v}
print('substituted terms',len(pol),'elapsed',time.time()-start,flush=True)
groups=defaultdict(dict)
for (ss,p,a,b,c),co in pol.items():groups[(ss,a,b,c)][p]=co*Fraction(-1,2)**p
neg=[];total=0;degree=0; bernstein=[]
for g,coeff in groups.items():
 d=max(coeff);degree=max(degree,d)
 for k in range(d+1):
  val=sum((v*Fraction(math.comb(k,j),math.comb(d,j)) for j,v in coeff.items() if j<=k),Fraction(0))
  total+=1
  bernstein.append((g,d,k,str(val)))
  if val<0:neg.append((g,k,str(val)))
print('Bernstein coefficients',total,'negative',len(neg),'max degree',degree,'elapsed',time.time()-start,flush=True)
(base/'acute_test.json').write_text(json.dumps({'min_e':min_e,'groups':len(groups),'total':total,'negative':neg,'max_degree':degree,'elapsed':time.time()-start,'bernstein_coefficients':bernstein},indent=2)+'\n')

assert not neg
