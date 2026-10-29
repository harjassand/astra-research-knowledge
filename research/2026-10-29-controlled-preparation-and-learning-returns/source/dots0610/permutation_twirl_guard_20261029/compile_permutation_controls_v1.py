#!/usr/bin/env python3
"""Exact classical permutation sampling/route compilation; no hardware claims."""
import itertools,random,json,pathlib,math
R=pathlib.Path(__file__).resolve().parent
rng=random.Random(202610290424)
def sample(n,cap=24):
 a=list(range(n));bits=0;draws=0
 for k in range(n,1,-1):
  b=(k-1).bit_length()
  for attempt in range(cap):
   x=rng.getrandbits(b);bits+=b;draws+=1
   if x<k:break
  else:return None,bits,draws
  a[k-1],a[x]=a[x],a[k-1]
 return a,bits,draws

def route(target,line=False):
 a=list(range(len(target)));out=[]
 for i,want in enumerate(target):
  j=a.index(want)
  if line:
   while j>i:
    a[j-1],a[j]=a[j],a[j-1];out.append((j-1,j));j-=1
  elif i!=j:
   a[i],a[j]=a[j],a[i];out.append((i,j))
 assert a==list(target)
 return out

def execute(n,swaps):
 a=list(range(n))
 for i,j in swaps:a[i],a[j]=a[j],a[i]
 return a
rows=[];total=0
for n in range(2,9):
 maxdirect=maxline=0
 for p in itertools.permutations(range(n)):
  a=route(p);b=route(p,True)
  assert len(a)<=n-1 and len(b)<=n*(n-1)//2
  assert execute(n,a)==list(p) and execute(n,b)==list(p)
  assert execute(n,a+list(reversed(a)))==list(range(n))
  assert execute(n,b+list(reversed(b)))==list(range(n))
  maxdirect=max(maxdirect,len(a));maxline=max(maxline,len(b));total+=1
 rows.append({'n':n,'permutations_checked':math.factorial(n),'max_unrestricted_swaps':maxdirect,'max_line_swaps':maxline})
samples=[]
for n in (16,64,256,1024):
 bitcounts=[];ds=[];ls=[]
 for _ in range(100):
  p,bits,draws=sample(n);assert p is not None
  a=route(p);z=route(p,True)
  assert execute(n,a)==p and execute(n,z)==p
  assert len(a)<=n-1 and len(z)<=n*(n-1)//2
  bitcounts.append(bits);ds.append(len(a));ls.append(len(z))
 samples.append({'n':n,'runs':100,'mean_bits_observed':sum(bitcounts)/100,
 'max_bits_observed':max(bitcounts),'cap24_worst_bits':24*sum((k-1).bit_length() for k in range(2,n+1)),
 'cap24_failure_union_bound':(n-1)*2**-24,'mean_direct_swaps':sum(ds)/100,'mean_line_swaps':sum(ls)/100})
# A SWAP's three-CNOT implementation is exactly a bit permutation on each
# computational-basis input, hence equal as a quantum unitary, including phases.
for x in range(4):
 a=(x>>1)&1;b=x&1
 b^=a;a^=b;b^=a
 assert (a,b)==(x&1,(x>>1)&1)
out={'all_checks_passed':True,'exhaustive_route_count':total,'exhaustive':rows,'random_samples':samples,
 'scope':'Exact classical route identities; fair-bit sampling under Python PRNG is reproducibility only, not a source of certified private physical randomness.',
 'pre_post_cost':'Double each route count. A physical SWAP costs3CNOT if decomposed; existing encoder/decoder/frame controls are additional.'}
(R/'compile_permutation_controls_v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'exhaustive_route_count':total,'sampled_routes':400},indent=2))
