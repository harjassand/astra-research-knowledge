from pathlib import Path
import sys,random,json,math,hashlib,time
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'gaussian_transfer'))
from large_herald_arb import LargeHeraldGaussian,AggregateMatching
from rational_gaussian_arb import pure_kernel,RationalGaussian,RationalElimination
from bigint_sampler_arb import DyadicUnimodal,binomial
from flint import arb
R=Path(__file__).resolve().parent
names=['bigint_sampler_arb.py','rational_gaussian_arb.py','large_herald_arb.py','validate_extension.py']
root=R.parent/'gaussian_transfer'
out={'sha256':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}}

class RejectFirstBits(random.Random):
 def __init__(self,n):super().__init__(1);self.remaining=n;self.calls=0
 def getrandbits(self,k):
  self.calls+=1
  if self.remaining:self.remaining-=1;return (1<<k)-1
  return 0
law=DyadicUnimodal(1,0,lambda k,m:arb(0),F(1,100),10)
r=RejectFirstBits(10000);v=law.draw(r)
out['uncapped_random_integer']={'outer_cap':law.max_attempts,'outer_attempts':law.last_attempts,'getrandbits_calls':r.calls,'output':v}

K,_=pure_kernel([[F(1,4),F(1,2)],[F(1,2),F(0)]])
invalid=[]
for h in [F(-1,2),F(3,2),1.5,-.5]:
 try:
  model=LargeHeraldGaussian(K,0,h)
  invalid.append({'input':str(h),'accepted_h':model.h,'output':model.sample(random.Random(2))})
 except Exception as e:invalid.append({'input':str(h),'rejected':str(e)})
for hmode in [F(-1,2),F(1,2),-.5,.5]:
 try:
  model=LargeHeraldGaussian(K,hmode,2)
  invalid.append({'mode_input':str(hmode),'accepted_mode':model.base.H})
 except Exception as e:invalid.append({'mode_input':str(hmode),'rejected':str(e)})
out['invalid_inputs']=invalid

# Exact degeneracy, pure-state parity, and trace-convergence edge checks.
edge=[]
for a,b,h,expected in [(0,0,0,0),(0,F(1,3),10,10),(F(1,4),0,12,0),(F(1,4),F(1,5),1,1)]:
 k=AggregateMatching(a,b,h).draw_k(random.Random(1),F(1,10**8));assert k==expected
 edge.append([str(a),str(b),h,k])
for a,b,h in [(0,0,1),(F(1,4),0,1)]:
 try:AggregateMatching(a,b,h);raise AssertionError('invalid zero event accepted')
 except ValueError:pass
for h in [0,1,2,3,10,10**100]:
 model=LargeHeraldGaussian.from_pure([[0,F(1,2)],[F(1,2),0]],0,h)
 assert model.sample(random.Random(1))==[h]
B=[[F(1,10),F(1,9),F(1,8)],[F(1,9),F(1,7),F(1,11)],[F(1,8),F(1,11),F(1,12)]]
r=random.Random(9536)
parity_count=0
for h in [0,1,2,3,10,31,10**20]:
 model=LargeHeraldGaussian.from_pure(B,0,h)
 for _ in range(60):
  sample=model.sample(r);assert (sum(sample)+h)%2==0;parity_count+=1
for Bbad in [[[F(1)]],[[0,F(1)],[F(1),0]],[[F(11,10),0],[0,F(1,2)]]]:
 try:LargeHeraldGaussian.from_pure(Bbad,0,0);raise AssertionError('divergent B accepted')
 except ValueError:pass
out['edge_cases']={'degenerate_matching':edge,'pure_parity_count':parity_count,'tmsv_deterministic_cases':6,'noncontractive_rejected':3}

# Mixed physical rank-one thermal kernels give an independent known NB output.
# K=[[0,C],[C,0]], C=t u u^T PSD, rho(C)<1. At herald h,
# P(n|h) = choose(n+h,n) (1-C22)^(h+1) C22^n.
emp=[]
r=random.Random(871635)
for h in [0,1,4,12]:
 C=[[F(1,5),F(1,5)],[F(1,5),F(1,5)]]
 Kmixed=[[F(0) for j in range(4)] for i in range(4)]
 for i in range(2):
  for j in range(2):Kmixed[i][j+2]=Kmixed[i+2][j]=C[i][j]
 model=LargeHeraldGaussian(Kmixed,0,h)
 n=4000;vals=[];start=time.perf_counter()
 for _ in range(n):vals.append(model.sample(r,F(1,10**10))[0])
 pgfs=[]
 for z in [F(1,2),F(3,4)]:
  target=float((F(4,5)/(1-F(1,5)*z))**(h+1))
  samples=[float(z**x) for x in vals];mean=sum(samples)/n
  se=math.sqrt(sum((x-mean)**2 for x in samples)/(n*(n-1)))
  score=(mean-target)/se
  assert abs(score)<5,(h,z,score)
  pgfs.append({'z':str(z),'target':target,'empirical':mean,'se':se,'z_score':score})
 emp.append({'h':h,'draws':n,'pgfs':pgfs,'seconds':time.perf_counter()-start})
out['independent_mixed_rank1_thermal_NB_comparator']=emp
assert out['sha256']=={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names},'targets changed during audit'
(R/'audit_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
