"""Finite signed-gas identity check; no substitute for continuum KP proof."""
import math,json,itertools
u=[.1,.08];h=-1.;z=[.02,.03];pins=[[-1.,1.],[1.,-1.]]
def Z(k):return 1+u[0]*k[0]+u[1]*k[1]+h*u[0]*u[1]*k[0]*k[1]
def logseries(k,N):
 # log(1+a*x+b*x*x), coefficient recurrence from derivative.
 a=u[0]*k[0]+u[1]*k[1];b=h*u[0]*u[1]*k[0]*k[1]
 c=[0.]*(N+1)
 for n in range(1,N+1):
  rhs=a if n==1 else (2*b if n==2 else 0.)
  if n>=2:rhs-=a*(n-1)*c[n-1]
  if n>=3:rhs-=b*(n-2)*c[n-2]
  c[n]=rhs/n
 return c
N=20;k0=[1.,1.];base=Z(k0);direct=0;regroup=0
c0=logseries(k0,N);R0=sum(c0[2:])
for mask in range(4):
 k=[1.,1.];w=1.;single=0.
 for i in range(2):
  if mask>>i&1:
   w*=z[i];single+=sum(u[j]*(pins[i][j]-1) for j in range(2));k=[k[j]*pins[i][j] for j in range(2)]
 direct+=w*Z(k)/base
 c=logseries(k,N);regroup+=w*math.exp(single+sum(c[2:])-R0)
assert abs(direct-regroup)<1e-13
lam=10.;naive_single=math.exp(-2*lam);pair_response=1.
result=dict(scope='Two disjoint source-contact sets; signed background pair h=-1. Connected-event log series truncated at20.',direct_normalized_partition=direct,regrouped_two_species_partition=regroup,absolute_error=abs(direct-regroup),same_contact_poisson_warning=dict(single_response=naive_single,pair_response=pair_response,pair_over_single_product=math.exp(4*lam),required_action='Merge both used labels into one contact component; do not normalize by actual singleton source weights.'))
print(json.dumps(result,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(result,indent=2)+'\n')
