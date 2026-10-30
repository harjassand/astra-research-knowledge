"""Exact graph check; no eigenvalues or recurrence assumption."""
import json
from tree_residual_matrix import HEIGHTS
from joint_matrix import fall

def endpoint_signature(R,K,cut):
 h=HEIGHTS[K]; states={(c,b) for b in range(K+1) for c in range(cut+1,R+h[b]+1)}
 adj={s:set() for s in states}
 for c,b in states:
  a=R+h[b]-c
  edges=[(c,b+1,1,1),(c,b+3,2,a*b),(c,b-4,-3,fall(a,3)*fall(b,4)),
   (c-1,b,0,(6*fall(c,3)+a*fall(c,2)+7*fall(a,2)*c)*fall(b,4)),
   (c+1,b,0,(12*a*fall(c,2)+fall(a,2)*c+fall(a,3))*fall(b,4))]
  for cc,bb,dn,rate in edges:
   if not rate: continue
   if not 0<=bb<=K or dn-h[bb]+h[b]!=0:
    adj[c,b].add('kill')
   elif cc==cut: adj[c,b].add(('core',bb))
   else:
    assert (cc,bb) in states
    adj[c,b].add((cc,bb))
 def destinations(start):
  todo=[start];seen=set();out=set()
  while todo:
   u=todo.pop()
   if u in seen:continue
   seen.add(u)
   for v in adj[u]:
    if v=='kill' or v[0]=='core':out.add(str(v))
    else:todo.append(v)
  return sorted(out)
 sig={str(b):destinations((cut+1,b)) for b in range(4,K+1)}
 trapped=[str(s) for s in states if not destinations(s)]
 return {'signature':sig,'trapped':trapped,'vertices':len(states)}

out=[]
for K in [4,8,12]:
 for L in [3,4,5,8,12]:
  R=100;cut=R-L
  a=endpoint_signature(R,K,cut);b=endpoint_signature(R+1,K,cut)
  out.append({'K':K,'L':L,'equal':a['signature']==b['signature'],'old':a,'new':b})
print(json.dumps(out,indent=2))
