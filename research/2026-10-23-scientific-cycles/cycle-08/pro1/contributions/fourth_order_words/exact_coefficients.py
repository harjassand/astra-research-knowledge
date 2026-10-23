#!/usr/bin/env python3
"""Exact new fourth-order diagnostics, k=2..5, from physical move/stay histories.

The all-k deletion/charge-selection proof is in FOURTH_ORDER_WORDS.md. This
bounded replay establishes the stated finite counterexamples and checks the
coefficient interface; it does not infer an asymptotic law from finite sizes.
The inherited physical path routine is copied unchanged in this directory.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import sys,time,json,resource,hashlib,platform,argparse
from inherited_representation import history,charge

def run(k):
 assert 2<=k<=5, "This bounded diagnostic is intentionally restricted to k=2..5"
 t=time.perf_counter(); words=list(product((0,1,2),repeat=k)); baths=list(product((1,2),repeat=k))
 groups=defaultdict(list)
 for i,x in enumerate(words):
  for u,w in enumerate(baths):
   for mask in range(1<<k):
    if mask.bit_count()>4:continue
    y,seed,v,r=history(x,0,w,mask)
    groups[(charge(x),y,seed,v)].append((i,u,r,mask))
 g1=defaultdict(int);g2=defaultdict(int)
 for (q,y,seed,w),paths in groups.items():
  delta=len(w)-k
  if not delta:continue
  for i,u,r,mask in paths:
   for j,v,s,mask2 in paths:
    if i==j:continue
    total=r+s
    if total not in (2,4):continue
    sign=1 if (s-r)%4==0 else -1
    key=i,u,j,v
    if total==2:
     g1[key]+=delta*sign
     g2[key]-=(k-1)*delta*sign
    else:g2[key]+=delta*sign
 g1={x:v for x,v in g1.items() if v};g2={x:v for x,v in g2.items() if v}
 weights=[sum(c==1 for c in w) for w in baths]
 tau={(u,v):F(1,(k+1)*comb(k,weights[u])) for u in range(2**k) for v in range(2**k) if weights[u]==weights[v]}
 h=defaultdict(F)
 for (i,u,j,v),c in g1.items():h[i,j]+=c*tau.get((v,u),0)
 h={ij:c for ij,c in h.items() if c}
 sigma=[F(1,2**(k+charge(w))) for w in words]
 var=sum(sigma[i]*c*c for (i,j),c in h.items())
 A=defaultdict(F)
 for (i,u,j,v),c in g2.items():A[u,v]+=sigma[j]*h.get((j,i),0)*c
 A={uv:c for uv,c in A.items() if c}
 deletion=defaultdict(F)
 for (q,y,seed,w),paths in groups.items():
  delta=len(w)-k
  if not delta:continue
  for i,u,r,mask in paths:
   for j,v,s,mask2 in paths:
    if r+s!=4 or not h.get((j,i),0):continue
    common=mask&mask2
    assert common.bit_count()==1 and (mask^mask2).bit_count()==2
    skipped=common.bit_length()-1
    sign=1 if (s-r)%4==0 else -1
    deletion[skipped,u,v]+=delta*sign*sigma[j]*h[j,i]
 deletion={key:c for key,c in deletion.items() if c}
 assert all(sum(deletion.get((r,u,v),0) for r in range(k))-(k-1)*(var if u==v else 0)==A.get((u,v),0) for u in range(2**k) for v in range(2**k))
 distance4=next(((i,u,j,v,c) for (i,u,j,v),c in g2.items() if sum((a!=0)!=(b!=0) for a,b in zip(words[i],words[j]))==4),None)
 witness=None if distance4 is None else {'input_bra':words[distance4[0]],'prefix_bra':baths[distance4[1]],'input_ket':words[distance4[2]],'prefix_ket':baths[distance4[3]],'G2_value':distance4[4]}
 if k in (2,3):
  scalar=-F(1,8) if k==2 else -F(23,32)
  assert all(A.get((u,v),0)==(scalar if u==v else 0) for u in range(2**k) for v in range(2**k))
 if k==3:
  for r,scalar in enumerate((F(1,8),F(1,32),F(1,8))):
   assert all(deletion.get((r,u,v),0)==(scalar if u==v else 0) for u in range(2**k) for v in range(2**k))
 if k==4:
  for u in range(2**k):
   perm=baths[u][1::-1]+baths[u][2:]
   v=baths.index(perm)
   for w in range(2**k):
    assert A.get((u,w),0)==(-F(113,64) if u==w else 0)+(-F(3,64) if v==w else 0)
 vals=set(A.get((u,u),0) for u in range(2**k)); off=[(u,v,c) for (u,v),c in A.items() if u!=v]
 out={'k':k,'G1_entries':len(g1),'G2_entries':len(g2),'v':str(var),'diagonal_values':sorted(map(str,vals)),'offdiagonal_entries':len(off),'first_offdiagonal':[(u,v,str(c)) for u,v,c in off[:10]],'distance4_witness':witness,'deletion_contractions':[[r,u,v,str(c)] for (r,u,v),c in sorted(deletion.items())],'T2':[[u,v,str(c)] for (u,v),c in sorted(A.items())],'wall_seconds':time.perf_counter()-t,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 return out
def distance_four_certificate():
 x=(0,1,0,1);y=(1,0,1,0);w=(1,2,1,1);rows=[];total=0
 for m in range(16):
  o,s,v,r=history(x,0,w,m);m2=m^15
  oo,ss,vv,t=history(y,0,w,m2)
  if (o,s,v)!=(oo,ss,vv):continue
  assert r+t==4
  delta=len(v)-4;phase=1 if (t-r)%4==0 else -1
  total+=delta*phase
  if delta:rows.append({'stay_bra_mask':m,'stay_ket_mask':m2,'output':o,'final_bath':v,'delta':delta,'phase':phase,'contribution':delta*phase})
 assert total==1
 return {'input_bra':x,'input_ket':y,'both_prefixes':w,'mask_bit_convention':'Bit j=1 means physical call j stays; indices start at0',
         'nonzero_terms':rows,'total_signed_displacement':total,'exact_bulk_polynomial':'b^2(1-b)^2',
         'scope':'Charge-distance-four coherence has no pair-sector leading coefficient; all prefixes/tails handled by actual path equality'}

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'));args=ap.parse_args()
 start=time.perf_counter();runs=[run(k) for k in range(2,6)]
 result={'scope':'New bounded fourth-order interface/counterexample checks, not an all-k theorem by enumeration',
         'runs':runs,'distance_four_certificate':distance_four_certificate(),
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'inherited_representation_sha256':hashlib.sha256(Path(__file__).with_name('inherited_representation.py').read_bytes()).hexdigest(),
         'wall_seconds':time.perf_counter()-start,'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'python':platform.python_version(),'inference_discovery_review_cost':'unknown'}
 args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({**{k:v for k,v in result.items() if k!='runs'},'runs':[{k:v for k,v in r.items() if k not in ('T2','deletion_contractions')} for r in runs]},indent=2))
