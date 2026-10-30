import itertools,json
r=4
# Target0 has self-weight1, external weight4; ties occur and retain target.
weights=[1,2,1,1];d=sum(weights)
def majority(y):
    opposite=sum(weights[j]*(y[j]!=y[0]) for j in range(1,r))
    return y[0]^int(2*opposite>sum(weights[1:]))
def gates(y,w):
    y=list(y);w=list(w)
    states=[(y[:],w[:])]
    for x in range(r):
        w[x]^=y[x];states.append((y[:],w[:]))
    w[r]^=w[0]^majority(w[:r]);states.append((y[:],w[:]))
    y[0]^=w[r];states.append((y[:],w[:]))
    return states
checks=0
for y in itertools.product([0,1],repeat=r):
    out=gates(y,[0]*(r+1))[-1][0]
    assert out[0]==majority(y)
    fullmajority=int(sum(a*b for a,b in zip(weights,y))>d/2)
    if y[0]==1 and fullmajority==0: assert out[0]==0
    assert gates(out,[0]*(r+1))[-1][0]==out
    before=sum(weights[j]*(y[0]!=y[j]) for j in range(1,r))
    after=sum(weights[j]*(out[0]!=out[j]) for j in range(1,r))
    assert after<=before
    if out!=list(y):assert after<before
    for b in [0,1]:
        for z,w in gates(y,[0]*(r+1)):
            assert (z[0]!=b)<=sum(a!=b for a in y)
            checks+=1
# Test each mask component's actual permutation and full-Hilbert dirty bound.
targets=list(range(r))+[0,0]
def apply(t,y,w):
    y=list(y);w=list(w)
    if t<r:w[t]^=y[t]
    elif t==r:w[r]^=w[0]^majority(w[:r])
    else:y[0]^=w[r]
    return y,w
fullchecks=0
for mask in itertools.product([0,1],repeat=r):
 for prefix in range(r+3):
  start=0
  for edge in range(prefix):
   if not mask[targets[edge]]:start=edge+1
  images=set()
  for y in itertools.product([0,1],repeat=r):
   for w in itertools.product([0,1],repeat=r+1):
    z,s=list(y),list(w)
    for edge in range(start,prefix):
     assert mask[targets[edge]]
     z,s=apply(edge,z,s)
    image=tuple(z+s);assert image not in images;images.add(image)
    bad=not(all(mask) and not any(w))
    for b in [0,1]:
     assert (z[0]!=b)<=sum(a!=b for a in y)+bad
     fullchecks+=1
print(json.dumps({'clean_prefix_checks':checks,'full_mask_prefix_workspace_checks':fullchecks,'all_pass':True},indent=2))
