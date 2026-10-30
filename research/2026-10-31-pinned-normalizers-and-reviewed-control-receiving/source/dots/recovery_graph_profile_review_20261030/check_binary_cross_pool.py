from itertools import combinations_with_replacement
from pathlib import Path
import json
n=5;A=0;D=1
names=['a','D','C','E','X']
def parts(xs):
 if not xs:yield [];return
 x,*tail=xs
 for pp in parts(tail):
  yield [(x,)]+pp
  for j in range(len(pp)):yield pp[:j]+[(x,)+pp[j]]+pp[j+1:]
def vec(pair):return tuple(pair.count(i) for i in range(n))
products=[vec(p) for p in combinations_with_replacement(range(n),2)]
counts={'partitions':0,'unit_channels':0,'cross_pool_channels':0,'active_true_face_survivors':0}
for pp0 in parts(list(range(1,n))):
 pp=[(A,)]+pp0;loc={i:j for j,b in enumerate(pp) for i in b};counts['partitions']+=1
 for h in range(n):
  src=vec((D,h))
  for dst in products:
   delta=[sum(dst[k]-src[k] for k in b) for b in pp]
   neg=[i for i,x in enumerate(delta) if x==-1];pos=[i for i,x in enumerate(delta) if x==1]
   if len(neg)!=1 or len(pos)!=1 or sum(abs(x) for x in delta)!=2:continue
   counts['unit_channels']+=1;i,j=neg[0],pos[0]
   # 2D has divided rate k(D-1), already supported on protected source coordinates.
   if h==D or h in pp[i]:continue
   counts['cross_pool_channels']+=1
   assert i==loc[D]
   state=list(src);assert state[D]==1 and sum(state[k] for k in pp[i])==1
   output=[state[k]+dst[k]-src[k] for k in range(n)]
   assert output[D]==0 and sum(output[k] for k in pp[i])==0
   if output[A]>=2:
    counts['active_true_face_survivors']+=1
    assert h==A and j==loc[A] and dst[A]==2 and sum(dst)==2
Path(__file__).with_suffix('.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
