import itertools,json
from pathlib import Path
count=0
for d in range(2,10):
 for k in range(0,6):
  def comps(n,m):
   if m==1:yield(n,);return
   for a in range(n+1):
    for b in comps(n-a,m-1):yield(a,)+b
  for a in comps(k,d):
   ts=[k];total=0
   for x in a:total+=x;ts.append(k-total)
   assert ts[0]==k and ts[-1]==0 and all(ts[j]>=ts[j+1] for j in range(d))
   rows=[([k]*(j-1)+[ts[j]]) for j in range(1,d)]+[[k]*(d-1)+[0]]
   weights=[sum(rows[j])-sum(rows[j-1]) if j else sum(rows[j]) for j in range(d)]
   assert weights==[k-x for x in a]
   for j in range(d-1):
    if not a[j]:continue
    b=list(a);b[j]-=1;b[j+1]+=1
    phasea=(-1)**sum((i+1)*x for i,x in enumerate(a));phaseb=(-1)**sum((i+1)*x for i,x in enumerate(b));assert phasea*phaseb==-1
    # Squared simple-root strength is a_j*(a_(j+1)+1), a nonnegative integer.
    assert a[j]*(a[j+1]+1)>0
   count+=1
Path(__file__).with_suffix('.json').write_text(json.dumps(dict(exact_patterns=count,d_range=[2,9],k_range=[0,5],weight_and_parity_checks=True,scope='Exact combinatorial check of explicit rectangle basis relabeling, not a complete physical CG circuit'),indent=2)+'\n');print(count)
