from pathlib import Path
import sys,random,json,itertools
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'gaussian_transfer'))
from large_herald_arb import LargeHeraldGaussian,AggregateMatching,CappedTickets,TicketBudgetExceeded
class Preset:
 def __init__(self,x):self.x=iter(x)
 def getrandbits(self,k):assert k==2;return next(self.x)
counts=[0,0,0,0]
for v in itertools.product(range(4),repeat=2):
 t=CappedTickets(Preset(v),1,F(1,2));assert t.attempt_cap==2
 try:counts[t.randrange(3)]+=1
 except TicketBudgetExceeded:counts[3]+=1
assert counts==[5,5,5,1]
class Ones:
 def getrandbits(self,k):return (1<<k)-1
B=[[F(1,5),F(1,7),F(1,11)],[F(1,7),F(1,4),F(1,13)],[F(1,11),F(1,13),F(1,6)]]
m=LargeHeraldGaussian.from_pure(B,0,100)
v=m.sample(Ones(),F(1,100))
assert v==[0,0] and m.last_ticket_fallback
adversarial={'value':v,'bits':m.last_random_bits,'tickets':m.last_ticket_count,'attempt_cap':m.last_ticket_attempt_cap,'ticket_bound':m.last_ticket_bound}
invalid=0
for x in [True,False,1.0,1.5,F(1),F(3,2),'1',None]:
 for f in [lambda x: LargeHeraldGaussian.from_pure(B,0,x),lambda x:LargeHeraldGaussian.from_pure(B,x,1),lambda x:AggregateMatching(F(1),F(1),x)]:
  try:f(x);raise AssertionError(('invalid accepted',x))
  except TypeError:invalid+=1
stats=[]
for h in [0,1,10**6,10**20,10**100]:
 model=LargeHeraldGaussian.from_pure(B,0,h)
 for seed in range(5):
  v=model.sample(random.Random(seed),F(1,10**8));assert (sum(v)+h)%2==0
  assert model.last_ticket_count<=model.last_ticket_bound
 stats.append({'h_bits':h.bit_length(),'output_bits':list(map(int.bit_length,v)),'bits':model.last_random_bits,'tickets':model.last_ticket_count,'cap':model.last_ticket_attempt_cap,'ticket_bound':model.last_ticket_bound,'fallback':model.last_ticket_fallback})
out={'exhaustive_width3_cap2_outcomes':counts,'forced_fallback':adversarial,'invalid_inputs_rejected':invalid,'large_herald_regression':stats}
(Path(__file__).resolve().parent/'cap_results_v2.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
