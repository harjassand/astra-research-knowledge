from fractions import Fraction as Q
from itertools import combinations,permutations,product
import json,time,pathlib,datetime
start=time.perf_counter()
def det(A):
    n=len(A)
    s=Q(0)
    for p in permutations(range(n)):
        v=Q((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n)))
        for i in range(n):v*=A[i][p[i]]
        s+=v
    return s

def z(F,R):
    if len(R)%2:return Q(0)
    ans=Q(0)
    for I in combinations(R,len(R)//2):
        J=[i for i in R if i not in I]
        a=det([[F[i][j] for j in J] for i in I])
        ans+=a*a
    return ans

def matrix(d):
    F=[[Q(i!=j) for j in range(4)] for i in range(4)]
    F[0][1]+=d
    return F
fixtures=[]
for d in [Q(0),Q(1,4),Q(1,16),Q(1,2**20)]:
    F=matrix(d)
    coeff={','.join(map(str,R)):str(z(F,R)) for m in range(5) for R in combinations(range(4),m)}
    assert z(F,range(4))==2*d*d
    for a,b in combinations(range(4),2):
        assert z(F,[a,b])==2+(2*d+d*d if (a,b)==(0,1) else 0)
    # sqrt(4+4d+2d^2) <= 2+2d for d>=0.
    assert 4+4*d+2*d*d <= (2+2*d)**2
    if d<=Q(1,4):
        assert (2-2*d)**2 > 2*d*d
    fixtures.append({'delta':str(d),'full':str(z(F,range(4))),'coefficients':coeff,'proved_lower_bound_on_det_hermitian':str((2-2*d)**2)})
pf_values=[]
for signs in product([-1,1],repeat=6):
    a,b,c,d,e,f=signs
    pf=2*(a*f-b*e+c*d)
    assert pf*pf in [4,36]
    pf_values.append(pf*pf)
# Q0 Rayleigh difference at coordinates a=0,b=1, remaining u=x2,v=x3:
# Delta=2*u^2*v^2+4*u^2+4*u*v+4*v^2 (constant term zero).
# This unused Rayleigh comment is background only; the obstruction proof uses
# principal-minor gauge normalization, not a software factorization claim.
result={'status':'PASS','scope':'exact finite coefficient identities and 64 real-skew sign choices; general Schur/gauge proof is written separately','fixtures':fixtures,'real_skew_sign_count':len(pf_values),'possible_four_by_four_det':sorted(set(pf_values)),'elapsed_seconds':time.perf_counter()-start,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
pathlib.Path('work/cycle6/c02_s01/determinant_obstruction_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},indent=2))
