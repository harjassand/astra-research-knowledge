import itertools,json
# Exact binary syndrome test for a path CSS sector H (rank n-1), opposite stabilizers empty.
rows=[]
for n,T in [(4,1),(4,2),(4,3),(4,4),(4,5),(6,1),(6,2),(6,3),(6,4)]:
 m=n-1; Hcols=[sum(1<<c for c in range(m) if i in (c,c+1)) for i in range(n)]
 # d then m columns; check blocks indexed by time slice.
 cols=[Hcols[i]<<(j*m) for j in range(T+1) for i in range(n)]
 cols += [((1<<c)<<(j*m))^((1<<c)<<((j+1)*m)) for j in range(T) for c in range(m)]
 for j in range(T):
  for i in range(n):
   syn=cols[j*n+i]^cols[(j+1)*n+i]
   for c in range(m):
    if Hcols[i]>>c&1:syn^=cols[n*(T+1)+j*m+c]
   assert syn==0
 c=n//2-1;target=(1<<c)^((1<<c)<<(T*m));F=min(c+1,n-c-1)
 # Exhaust exact weight classes up to known representative bound.
 found=None
 for w in range(1,min(T,2*F)+1):
  for inds in itertools.combinations(range(len(cols)),w):
   syn=0
   for i in inds:syn^=cols[i]
   if syn==target:found=w;break
  if found is not None:break
 assert found is not None and found>=min(T,F)
 rows.append({'n':n,'temporal_edges':T,'singleton_filling':F,'vertical_local_check_energy':2,'exact_minimum_same_syndrome_weight':found,'proved_lower_bound':min(T,F)})
print(json.dumps({'sector':'H_X=path incidence, H_Z empty; exact binary diagnostic, not good-distance Tanner family','local_transport_syndromes':'all zero','cases':rows},indent=2))
