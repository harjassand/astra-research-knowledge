import itertools, math, json
import numpy as np
# Exact signed threshold sieve; no probability assumption.
cases=0
for M in range(1,11):
 for K in range(1,M+1):
  for a in range(M+1):
   got=sum((-1)**(j-K)*math.comb(j-1,K-1)*math.comb(a,j) for j in range(K,a+1))
   assert got==int(a>=K); cases+=1
  for j in range(K,M+1):
   assert math.comb(M,j)*math.comb(j-1,K-1)<=math.comb(M,K)*math.comb(M-K,j-K)
# Resource region merges two disjoint predicates by OR, not max.
for d,a in itertools.product([0,1],repeat=2): assert d+a-d*a==int(d or a)
xstar=.01; x0=.00001; B=100; r=x0/xstar
xs=[xstar*r**(2**j) for j in range(8)]
p=math.expm1(B*sum(math.log1p(x) for x in xs))
upper=math.expm1(B*x0/(1-r)); assert p<=upper
# A noncommuting compression fixture: P below an E spectral cut suffices.
E=np.diag([0.,.4,2.]); V=np.diag(np.exp(np.diag(E)))
G=np.array([[.45,.1,.08],[.1,.5,.1],[.08,.1,.4]])
assert np.linalg.eigvalsh(G).min()>0 and np.linalg.eigvalsh(G).max()<1
F=np.diag(np.exp(np.diag(E)/2))@G@np.diag(np.exp(np.diag(E)/2))
v=np.array([1.,1.,0.])/math.sqrt(2); P=np.outer(v,v)
res=np.linalg.eigvalsh(math.exp(.4)*P-P@F@P).min()
assert res>-1e-12 and np.linalg.norm(P@F-F@P)>1e-3
# Large-support exponent can be made negative for fixed delta,c0.
c0=3.; delta=.001; noise=1e-10
rate=delta*math.log(math.e*c0*noise/delta)+c0*math.log1p(noise)
assert rate<0
print(json.dumps({'result':'PASS','signed_sieve_integer_cases':cases,'decoder_floor':p,'uniform_upper':upper,'noncommuting_compression_min_eigenvalue':float(res),'nonzero_P_F_commutator':float(np.linalg.norm(P@F-F@P)),'illustrative_tail_log_bound_per_N':rate,'scope':'finite algebra and bound checks only; no hardware or threshold simulation'},indent=2))
