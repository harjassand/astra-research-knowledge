"""Full-output truncation budget for a precomputed, outcome-independent gate list.
W[u,v] is the exact number of actual two-site calls after basis pruning.
"""
def svd_count_from_weights(W,order,backend='swap'):
 n=len(order)
 if sorted(order)!=list(range(n)):raise ValueError('Ordering is not a permutation')
 pos={v:i for i,v in enumerate(order)};count=0
 for u in range(n):
  for v in range(u+1,n):
   weight=float(W[u,v])
   if weight<0 or not weight.is_integer():raise ValueError('Gate counts must be nonnegative integers')
   d=abs(pos[u]-pos[v]);cost=(2*d-1 if backend=='swap' else d if backend=='mpo' else None)
   if cost is None:raise ValueError('Unknown backend; prove its SVD count separately')
   count+=int(weight)*cost
 return count

def local_allowance(delta,svds):
 if delta<0 or svds<0:raise ValueError('Invalid budget')
 return delta/svds if svds else 0.0

def combined_svd_count(n,records,neigh,order,physical=False):
 """Exact count for combined product-MPO implementation WITHOUT early measurement.
 Assumes known-basis pruning enabled and exactly one SVD per covered MPO bond.
 """
 pos={v:i for i,v in enumerate(order)};known=[True]*n
 counts={tuple(sorted((u,v))):0 for u in range(n) for v in neigh[u] if u<v};J=0
 for events,_,_,_ in records:
  for (u,v),reset,rare,candidate in events:
   counts[tuple(sorted((u,v)))]+=1
   if physical and not reset and not rare and not known[u] and not known[v]:J+=abs(pos[u]-pos[v])
  for (u,v),reset,rare,candidate in events:
   if not rare:continue
   if physical:J+=abs(pos[u]-pos[v])
   else:
    support={u,v}
    for w in (neigh[u]|neigh[v])-{u,v}:
     if not known[w] and (counts.get(tuple(sorted((u,w))),0) or counts.get(tuple(sorted((v,w))),0)):support.add(w)
    coordinates=[pos[w] for w in support];J+=max(coordinates)-min(coordinates)
   known[u]=known[v]=False
  for (u,v),reset,rare,candidate in events:
   if reset:known[u]=known[v]=True
 return J
