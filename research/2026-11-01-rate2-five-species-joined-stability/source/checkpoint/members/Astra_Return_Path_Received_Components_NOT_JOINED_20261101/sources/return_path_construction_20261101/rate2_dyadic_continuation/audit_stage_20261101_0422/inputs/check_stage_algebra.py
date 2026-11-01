"""Exact algebra, source-jump and declared constant checks, not independent review."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
z=lambda *ii:tuple(ii.count(i) for i in range(5))
A,B,C,D,E=range(5);zero=z();one=z(A);two=z(A,A)
pairs=[(zero,one,1,1),(two,z(A,C),1,1),(two,z(A,D),1,1),(two,z(A,E),1,1),(z(A,E),z(C,D),1,2),(z(C,D),z(A,B),1,1)]
raw=[r for u,v,k,l in pairs for r in [(u,v,k),(v,u,l)]]
def rate(u,x):
 p=1
 for n,j in zip(x,u):
  for k in range(j):p*=max(0,n-k)
 return p
def jump(x,u,v):return tuple(a+b-c for a,c,b in zip(x,u,v))
def gen(x,fn):
 fx=fn(x);return sum(k*rate(u,x)*(fn(jump(x,u,v))-fx) for u,v,k in raw if rate(u,x))
def ff(x,N):a,b,c,d,e=x;return F(2*a+c+d,2)-F(3*e*e,4*N)+F(a*e,N)
def ff_drift_formula(x,N):
 a,b,c,d,e=x;L=F(2*a+c+d,2)
 return 1+a+a*L-3*a*a+F(e,N)+F(c*d,2*N)+F(2*a*c*d,N)+F(a*(a-1)**2,N)-F(3*a*(a-1),4*N)+a*e*(1+F(c+d+2+3*e-b,N)-F(13*a,2*N))
# Formula-by-channel table exactly matches the theorem.
table={
 (z(A,B),z(C,D)):lambda a,b,c,d,e,N:-F(e,N),
 (z(C,D),z(A,B)):lambda a,b,c,d,e,N:F(e,N),
 (z(C,D),z(A,E)):lambda a,b,c,d,e,N:F(4*a-2*e+1,4*N),
 (z(A,E),z(C,D)):lambda a,b,c,d,e,N:F(2*e-4*a+1,4*N),
 (z(A,E),two):lambda a,b,c,d,e,N:1+F(10*e-4*a-7,4*N),
 (two,z(A,E)):lambda a,b,c,d,e,N:-1+F(4*a-10*e-7,4*N),
 (z(A,C),two):lambda a,b,c,d,e,N:F(1,2)+F(e,N),
 (z(A,D),two):lambda a,b,c,d,e,N:F(1,2)+F(e,N),
 (two,z(A,C)):lambda a,b,c,d,e,N:-F(1,2)-F(e,N),
 (two,z(A,D)):lambda a,b,c,d,e,N:-F(1,2)-F(e,N),
 (zero,one):lambda a,b,c,d,e,N:1+F(e,N),
 (one,zero):lambda a,b,c,d,e,N:-1-F(e,N)}
identities=jumps=0
for x in product(range(4),repeat=5):
 a,b,c,d,e=x;N=137
 assert gen(x,lambda y:y[A]*y[E])==e+3*e*c*d+2*a*c*d+a*(a-1)**2+2*c*d-a*e*(b-c-d-2+5*a)
 assert gen(x,lambda y:ff(y,N))==ff_drift_formula(x,N)
 assert gen(x,lambda y:y[C]-y[D])==-a*(c-d)
 for u,v,k in raw:
  if rate(u,x):assert ff(jump(x,u,v),N)-ff(x,N)==table[(u,v)](*x,N);jumps+=1
 identities+=1
# Large, literal integer tube grid: all quantities are exactly representable.
N=10**250;m=10**100;e=10**175;delta=F(1,10**100);K=10**40
assert e*e==N*m and m**5>=K**5*N and m<=delta*N
stage=F(16*e,m*m);H=F(10**4*e,N);J=F(10**7*m*e,N)
tube=0
for L,a,zz,ee in product([m//2,m,2*m],[0,m//64,m//16],[-m//16,0,m//16],[e//2,e,2*e]):
 c=L-a+zz//2;d=L-a-zz//2;b=N-a-c-d-ee;x=(a,b,c,d,ee)
 assert all(v>=0 for v in x) and sum(x)==N
 la=gen(x,lambda y:y[A]);la2=gen(x,lambda y:y[A]**2)
 assert la<=13*m*m-F(N*a,4)
 assert la2<=-F(N*a*a,2)+(3*N+24*m*m)*a+13*m*m
 qa=sum(k*rate(u,x) for u,v,k in raw if u[A]!=v[A]);assert qa<=13*m*m+5*N*a
 for u,v,k in raw:
  if rate(u,x):assert abs(ff(jump(x,u,v),N)-ff(x,N))<=2
 tube+=1
# Literal cumulative bracket allocations in the proof.
qa=13*m*m*stage+5*N*H;assert qa<=10**5*e
fast=(2*N*H+12*m*m*stage+2*e*H)*F(4*e*e,N*N)
slow=4*(2*e*H)+4*m*H+12*J+4*(stage+H)
assert fast+slow<=2*10**8*m
qe=J+4*e*H+8*m*m*stage;assert qe<=5*10**4*e
qz=2*J+4*m*H;assert qz<=3*10**7*F(m*e,N)
# Absolute drift allocation from each displayed term of the exact F identity.
r=F(1,10**50)
drift=stage+H+2*m*H+3*J+F(2*e,N)*stage+F(2*m*m,N)*stage+F(8*m*m,N)*H+F(m,16*N)*J+H/N+F(3,4*N)*J+32*r*(2*e*H)
assert drift<=10**9*r*m+4*stage<F(m,64)
# Freedman exponent comparisons are exact rational inequalities.
bern=lambda x,v,b:x*x/(2*(v+b*x/3))
assert bern(F(e),F(10**5*e),F(1))>=F(e,200002)
assert bern(F(m*e),F(10**5*m*m*e),F(m))>=F(e,200002)
assert bern(F(m,64),F(2*10**8*m),F(2))>=F(m,3*10**12)
assert bern(F(e,100),F(5*10**4*e),F(1))>=F(e,2*10**9)
assert bern(F(m,128),F(3*10**7*m),F(1))>=F(m,2*10**12)
result={'status':'PASS_SAME_AUTHOR_EXACT_STAGE_COMPONENT_CHECKS_NOT_INDEPENDENT_THEOREM_REVIEW','small_state_identity_cases':identities,'enabled_source_jump_checks':jumps,'literal_huge_tube_cases':tube,'full_channels_retained':len(raw),'reference_N_decimal_digits':len(str(N)),'stage_m_decimal_digits':len(str(m)),'proof_sha256':hashlib.sha256((root/'EXACT_CORRECTOR_AND_STAGE_LEMMA.md').read_bytes()).hexdigest()}
(root/'stage_check_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
