"""Exact finite set causal-cone/packing test for the actual macro schedule."""
import json
from pathlib import Path
W=4;L=(2*W-1)**2;m=3*L;n=5*m
# True V is block-local on neighboringpairs; both input algebras occupy thatpair.
S=[];J=[]
for i in range(n):
 lo=(i//2)*2;hi=min(n-1,lo+1);S.append(set(range(lo,hi+1)));J.append(set(range(max(0,lo-1),min(n-1,hi+1)+1)))
# Greedy coloring of intervals, with exact disjointness in each color.
order=sorted(range(n),key=lambda i:(min(J[i]),max(J[i]),i));colors=[];assignment={}
for i in order:
 for c,owners in enumerate(colors):
  if all(not(J[i]&J[j]) for j in owners):owners.append(i);assignment[i]=c;break
 else:assignment[i]=len(colors);colors.append([i])
assert len(colors)<=2*W-1
rank={i:k for k,i in enumerate(order)}
# Label modes: physical0..n-1, receivern+i. Eachmacro actsJ_i plusreceiveri.
support=[set(J[i])|{n+i} for i in range(n)]
max_count=0;max_span=0
for fault in range(n):
 cone=set(support[fault])
 for layer in colors[assignment[fault]+1:]:
  touches=[i for i in layer if support[i]&cone]
  for i in touches:cone|=support[i]
 rec=sorted(rank[x-n] for x in cone if x>=n)
 max_count=max(max_count,len(rec));max_span=max(max_span,rec[-1]-rec[0]+1)
 assert rec[-1]-rec[0]+1<=L
 codes=[(x//(5*L))*L+(x%(5*L))%L for x in rec];assert len(codes)==len(set(codes))
maxmacro=0;maxnative=0
for b in range(m):
 tile=b//L;local=b%L
 target={n+order[tile*5*L+local+k*L] for k in range(5)};cone=set(target);owners=set()
 for layer in reversed(colors):
  touches=[i for i in layer if support[i]&cone]
  owners.update(touches)
  for i in touches:cone|=support[i]
 phys={x for x in cone if x<n};native={i for i in range(n) if S[i]&phys}
 assert len(owners)<=5*L and len(native)<=5*L
 maxmacro=max(maxmacro,len(owners));maxnative=max(maxnative,len(native))
r={'status':'PASS_EXACT_ACTUAL_MACRO_CAUSAL_CONES','physical_inputs':n,'logical_codes':m,'output_tiles':3,'W':W,'universal_L':L,'actual_macro_layers':len(colors),'bound_macro_layers':2*W-1,'fault_locations_checked':n,'max_final_receiver_count':max_count,'max_final_sorted_receiver_span':max_span,'max_perlogical_relevant_macros':maxmacro,'max_perlogical_relevant_native_sites':maxnative,'bound_each_perlogical':5*L,'source_draws':0,'scope':'Exact finite support/schedule construction only. Does not simulate a noisy735qubitstate or prove hardware/encoder fault tolerance.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
