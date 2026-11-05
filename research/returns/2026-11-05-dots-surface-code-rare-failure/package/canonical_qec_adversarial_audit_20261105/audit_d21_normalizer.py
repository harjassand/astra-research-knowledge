"""Independent forward-walk DP, reverse integer confidence CDF, frozen replay."""
import sys,time,json,hashlib,random
from pathlib import Path
from fractions import Fraction as F
from math import comb,isqrt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'canonical_qec_witness_20261105'))
from phenomenological import RepeatedModel
from sampler import Proposal
start=time.perf_counter();root=Path(__file__).resolve().parents[1];r=json.loads((root/'canonical_qec_witness_20261105/phenomenological_d21_result.json').read_text());d,T,Lmax=r['distance'],r['rounds'],r['Lmax'];m=RepeatedModel(d,T)
p=F(r['p']);a,b=p.numerator,p.denominator;E=len(m.edges)
# Forward nonbacktracking walks, O(E) storage. Update through node incoming
# totals minus the reverse directed-edge count, absorbing all boundary arrivals.
u=[];v=[]
for x,y in m.edges:u.extend([x,y]);v.extend([y,x])
internal=[z in m.checkid for z in u];right=[z in m.right for z in v]
c=[0]*(2*E)
for rootnode in m.left:
 neighbor,e=m.adj[rootnode][0];c[2*e+int(m.edges[e][0]!=rootnode)]=1
counts=[0];z=F(0)
for L in range(1,Lmax+1):
 cnt=sum(cc for cc,isright in zip(c,right) if isright);counts.append(cnt)
 B=F(sum(comb(L,k)*a**k*(b-a)**(L-k) for k in range((L+1)//2,L+1)),b**L)
 z+=cnt*B
 if L<Lmax:
  totals=[0]*len(m.coords)
  for dst,cc in zip(v,c):totals[dst]+=cc
  c=[totals[src]-c[k^1] if inside else 0 for k,(src,inside) in enumerate(zip(u,internal))]
assert z==F(r['Z_exact'])
# Tail derived from graph incidence, distinct from the implementation's storage.
maxdegree=max(sum(1 for _ in m.adj[x]) for x in m.checks);branch=maxdegree-1
D=10**12;s=isqrt((4*a*(b-a)*D*D)//(b*b))
while s*s*b*b<4*a*(b-a)*D*D:s+=1
rho=F(s,D);assert branch*rho<1
bound=F(len(m.left),branch)*(branch*rho)**(Lmax+1)/(1-branch*rho)
assert bound==F(r['tail_exact'])
normalizer_sec=time.perf_counter()-start
# Reverse direction exact sum, starting at k instead of the k=0 term used by
# the production recurrence. Check root inequalities and one-grid sharpness.
n=r['shots'];x=r['counts']['accepted'];cl,cu=map(F,r['interval_exact']);lo=cl/z;hi=(cu-bound)/z;DD=1<<20;denom=DD**n
assert (lo*DD).denominator==(hi*DD).denominator==1
jlo=int(lo*DD);jhi=int(hi*DD)
def reverse_cdf(k,j):
 term=comb(n,k)*j**k*(DD-j)**(n-k);total=term
 for ell in range(k,0,-1):
  num=term*ell*(DD-j);div=(n-ell+1)*j
  term,rem=divmod(num,div);assert rem==0;total+=term
 return total
assert (denom-reverse_cdf(x-1,jlo))*2000<=denom
assert (denom-reverse_cdf(x-1,jlo+1))*2000>denom
assert reverse_cdf(x,jhi)*2000<=denom
assert reverse_cdf(x,jhi-1)*2000>=denom
confidence_sec=time.perf_counter()-start-normalizer_sec
# Reproduce the fixed 10k-trial execution. This is not an additional statistical
# experiment; it checks source / seed / output reproducibility.
q=Proposal(m,p,Lmax);assert q.counts==counts
rng=random.Random(r['seed']);replay={k:0 for k in ['accepted','nonsimple','not_failure','other_witness']}
for i in range(n):val,why=q.trial(rng);replay[why]+=1
assert replay==r['counts']
out={'status':'PASS: independent d21 forward normalization, tail, reverse integer CP and exact fixed-seed replay','distance':d,'rounds':T,'fault_edges':E,'detectors':len(m.checks),'maximum_internal_degree':maxdegree,'left_boundary_vertices':len(m.left),'walk_counts_sha256':hashlib.sha256(json.dumps(counts).encode()).hexdigest(),'Z_exact_match':True,'tail_exact_match':True,'CP_dyadic_numerators':[jlo,jhi],'CP_dyadic_denominator':DD,'counts_reproduced':replay,'timing_seconds':{'independent_normalizer_tail':normalizer_sec,'independent_reverse_CDF':confidence_sec,'total':time.perf_counter()-start},'source_sha256':{name:hashlib.sha256((root/'canonical_qec_witness_20261105'/name).read_bytes()).hexdigest() for name in ['sampler.py','phenomenological.py']}}
Path(__file__).with_name('d21_independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
