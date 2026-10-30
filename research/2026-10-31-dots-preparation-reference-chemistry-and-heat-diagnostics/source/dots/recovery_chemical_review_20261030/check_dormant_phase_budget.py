from collections import deque
import json

def H(b,m,q):
 if b==0:return 0
 j,v=divmod(b-1,q-1)
 return j*(m-1)+v+1
rows=[]
for m,q in [(4,5),(4,8),(6,7),(6,9)]:
 for b in range(q,200):
  assert -m+H(b,m,q)-H(b-q,m,q)<=0
 for b in range(1,200):
  assert (m-1)-H(b+q-1,m,q)+H(b,m,q)==0
 for initial in [m,2*m,5*m]:
  # Explore complement of the proposed rare-event union: I=0; H<=1;
  # H=1 requires L=0, H=0 requires L<=q-2.
  start=(initial,q,False,0,0)
  seen={start};todo=deque([start]); terminals=0;maximum=-1e99
  r0=initial-H(q,m,q)
  def admit(a,b,left,l,h):return h<=1 and ((h==1 and l==0) or (h==0 and l<=q-2))
  while todo:
   a,b,left,l,h=todo.popleft()
   if a>=m and b>=q:
    # Actual seed preserves N and B, so r equals pre-seed r.
    dr=a-H(b,m,q)-r0;maximum=max(maximum,dr);terminals+=1;assert dr<=0
   succ=[]
   # Immigration at high B is outside complement, never include it.
   if b<q:succ.append((a+1,b+1,left,l+(b>0),h))
   if a*b>0:succ.append((a+m-1,b+q-1,left,l,h+(b>=q)))
   if a>=m and b>=q:succ.append((a-m,b-q,left,l,h))
   for aa,bb,wasleft,ll,hh in succ:
    nowleft=wasleft or bb<q
    if not admit(aa,bb,nowleft,ll,hh):continue
    if wasleft and bb==q:
     dr=aa-H(bb,m,q)-r0;maximum=max(maximum,dr);terminals+=1;assert dr<=0
     continue
    y=(aa,bb,nowleft,ll,hh)
    if y not in seen:seen.add(y);todo.append(y)
  rows.append(dict(m=m,q=q,initial_A=initial,states=len(seen),terminal_checks=terminals,max_terminal_residual_increase=maximum))
json.dump(rows,open('recovery_chemical_review_20261030/check_dormant_phase_budget.json','w'),indent=2)
print(json.dumps(rows,indent=2))
