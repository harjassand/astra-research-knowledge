from fractions import Fraction as F
from math import comb,ceil
from pathlib import Path
import json
rows=[]
# Independent direct binomial sums, including false acceptance at the boundary.
for eps in [F(1,2),F(2,3),F(3,5)]:
 for delta in [F(1,3),F(1,8)]:
  for j in [0,1]:
   L=(j+1)**2;dj=delta/F(2**(j+1)*L);b=0
   while F(1,2**b)>dj:b+=1
   m=ceil(32*b/eps);cut=int(3*eps*m/4)
   false=sum(F(comb(m,x))*eps**x*(1-eps)**(m-x) for x in range(cut+1))
   good=eps/4;rej=sum(F(comb(m,x))*good**x*(1-good)**(m-x) for x in range(cut+1,m+1))
   assert false<=dj and rej<=dj**8
   assert (F(1,4)+F(3,4)*rej)**L<=F(1,2**L)
   rows.append(dict(epsilon=str(eps),delta=str(delta),j=j,m=m,false_accept=float(false),good_reject=float(rej)))
# Exact stage-tail domination and allocation identities.
for js in range(8):
 for ss in range(1,40):
  expo=sum((i+1)**2 for i in range(js,js+ss));assert expo>=ss*(ss+1)//2
alloc=sum(F(1,2**(j+1)) for j in range(20));assert alloc==1-F(1,2**20)
res=dict(cases=rows,tail_inequality_cases=8*39,scope='Exact probability/schedule arithmetic; no random encoder or quantum learner executed')
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print('PASS',len(rows))
