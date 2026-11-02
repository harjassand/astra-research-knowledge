import json, math
from pathlib import Path
q=8; L=16
h=[[x%q for y in range(L)] for x in range(L)]
def dist(a,b):
    d=(a-b)%q
    return min(d,q-d)
def okay(a):
    return all(dist(a[x][y],a[(x+1)%L][y])<=1 and dist(a[x][y],a[x][(y+1)%L])<=1 for x in range(L) for y in range(L))
assert okay(h)
accepted=0
for w in [1,2,3]:
 for z in [1,2,3]:
  for x0 in range(L):
   for y0 in range(L):
    a=[r[:] for r in h]
    for dx in range(w):
     for dy in range(z):a[(x0+dx)%L][(y0+dy)%L]=(a[(x0+dx)%L][(y0+dy)%L]+1)%q
    accepted+=okay(a)
assert accepted==0
# The literal repair predicates are inactive in this valid winding field.
invalid_nec=0; active_inflation=0
for x in range(L):
 for y in range(L):
  v=[h[x][y],h[(x+1)%L][y],h[x][(y+1)%L]]
  invalid_nec+=any(dist(a,b)>1 for a in v for b in v)
  mx=max(h[x][y],h[(x-1)%L][y],h[x][(y-1)%L])
  active_inflation+=dist(h[x][y],mx)>1
assert invalid_nec==active_inflation==0
p=.001
stall=[]
for k in [1,2,4,16,64,512,4096]:
    log_prob=math.lgamma(k+1)+math.lgamma(1+1/p)-math.lgamma(k+1+1/p)
    stall.append({'k':k,'log_all_fault_probability':log_prob,'per_site_root_probability':math.exp(log_prob/k),'root_over_p':math.exp(log_prob/k)/p})
res={'clock_modulus':q,'torus_side':L,'nearest_neighbor_clock_valid':True,'accepted_rectangular_increments_up_to_3_by_3':accepted,'invalid_NEC_predicates':invalid_nec,'active_SW_inflation_predicates':active_inflation,'scope':'Global winding obstruction only, not a finite-island threshold counterexample. Updates tested increment each whole rectangle atomically.','shared_stall':{'noise_rate':p,'service':'one shared Exp(1) delay','exact_formula':'Gamma(k+1) Gamma(1+1/p) / Gamma(k+1+1/p)','values':stall}}
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
