from pathlib import Path
from fractions import Fraction as F
from itertools import product
from copy import deepcopy
import sys,json,random,hashlib,time
A=Path(__file__).resolve().parent;version=sys.argv[1]if len(sys.argv)>1 else 'v1';sys.path.insert(0,str(A/('replay_'+version)));import common_box as C
start=time.perf_counter();checks=0;refusals=[];cats={};rng=random.Random(11010325)
def ok(z,k):
 global checks
 assert z,k
 checks+=1;cats[k]=cats.get(k,0)+1

def no(fn,k,allowed=(C.Unsupported,C.BudgetRefusal,ValueError,TypeError)):
 try:fn()
 except allowed as e:refusals.append({'test':k,'class':type(e).__name__,'reason':str(e)});ok(True,k)
 else:raise AssertionError('false admission '+k)
raw=C.fixture();p=C.construct(raw)
# Exact default public raw receiver and byte receiving.
ok(C.receive(raw,p)['box_sha256']==p['raw']['canonical_box_sha256'],'actual full canonical certificate receiving')
pay=C.canonical_bytes(p);ok(C.receive_wire(raw,pay,max_bytes=len(pay))['certificate_sha256']==C.digest(p),'wire exact byte budget admits')
no(lambda:C.receive_wire(raw,pay,max_bytes=len(pay)-1),'wire byte budget refuses one below')
for budget in [True,False,1.0,F(1),-1,'100']:
 no(lambda budget=budget:C.receive_wire(raw,pay,max_bytes=budget),'strict byte-budget type')
for val in [pay.decode(),bytearray(pay),memoryview(pay),None,True]:no(lambda val=val:C.receive_wire(raw,val),'strict wire payload bytes type')
# Every leaf of actual acquired certificate, including source support and box bounds.
def leaves(o,path=()):
 if type(o)is dict:
  for k,v in o.items():yield from leaves(v,path+(k,))
 elif type(o)in(tuple,list):
  for k,v in enumerate(o):yield from leaves(v,path+(k,))
 else:yield path,o
# Convert containers to mutable lists without changing canonical mathematical bytes.
def mutable(o):
 if type(o)is dict:return {k:mutable(v)for k,v in o.items()}
 if type(o)in(tuple,list):return [mutable(v)for v in o]
 return o
base=mutable(p)
for path,v in leaves(base):
 q=deepcopy(base);d=q
 for k in path[:-1]:d=d[k]
 d[path[-1]]=v+1 if type(v)in(int,F)else v+'__altered'if type(v)is str else None
 no(lambda q=q:C.receive(raw,q),'every full certificate proof leaf rejects mutation',(C.Unsupported,))
# Nested mutable input support cannot alias the acquired channels/rate guard.
r=mutable(raw);g=C.RateGuard(r);oldraw=deepcopy(r);oldactive=g.active;oldhash=g.box_sha256;r[0][0][0]=999;r[1][2]=F(999);r.append(r[-1])
ok(g.active==oldactive and g.box_sha256==oldhash,'rate guard detaches raw input containers')
for j in range(120):
 req=[l+(h-l)*F(rng.randrange(101),100)for u,v,l,h in p['raw']['channels']];before=tuple(req);ans=g.select(req);ok(ans['status']=='ADMIT_MODEL_RATES'and g.active==before,'actual convex box action admission');req[0]=-1;ok(g.active==before,'rate action copy detaches mutable request')
 x=tuple(rng.randrange(20)for _ in range(p['raw']['m']));intens=g.intensities(x)
 for got,(u,v,l,h),k in zip(intens,p['raw']['channels'],before):
  a=1
  for s,n in zip(u,x):
   for i in range(s):a*=max(n-i,0)
  ok(got==k*a and l*a<=got<=h*a,'actual rate-to-intensity falling factorial and box enclosure')
prev=g.active
bad=[[0]*len(prev),[True]*len(prev),[1.0]*len(prev),[F(-1)]*len(prev),[],list(prev[:-1]),list(prev)+[F(1)],None,{},'rates']
for req in bad:
 ans=g.select(req);ok(ans['status']=='REJECT_KEEP_PREVIOUS' and g.active==prev,'invalid command retains entire prior positive choice')
for x in [[0]*(p['raw']['m']-1),[0]*(p['raw']['m']+1),[False]*p['raw']['m'],[-1]*p['raw']['m'],[F(0)]*p['raw']['m'],None]:no(lambda x=x:g.intensities(x),'invalid model state strictly rejected')
# Parse adversaries: exact schema, positive lower bounds, no alternate dynamics.
for val in [None,{},[],[1],[[]],[((),(),1,2)],[((),(),1,2,3)],True,'raw']:
 no(lambda val=val:C.construct(val),'malformed raw architecture',(C.Unsupported,))
for mode in range(17):
 b=mutable(raw)
 if mode<8:b[0][2]=[True,1.0,'1',F(0),F(-1),None,float('nan'),float('inf')][mode]
 elif mode==8:b[0][3]=b[0][2]-1
 elif mode==9:b[0][0][0]=True
 elif mode==10:b[0][0][0]=F(0)
 elif mode==11:b[0][0][0]=-1
 elif mode==12:b[0][0].append(0)
 elif mode==13:b[0][1]=list(b[0][0])
 elif mode==14:b.pop(0)
 elif mode==15:b.pop(2)
 else:
  z=[0]*6;w=z.copy();w[1]=1;b.extend([(z,w,F(1),F(2)),(w,z,F(1),F(2))])
 no(lambda b=b:C.construct(b),'unsupported malformed rate or raw channel',(C.Unsupported,))
# Budget views have precise limited scope, not a total arithmetic meter.
n=p['raw']['n'];fs=C.faces(p,max_masks=2**n);ok(len(fs)==11,'all actual faces at exact enumeration mask cap')
no(lambda:C.faces(p,max_masks=2**n-1),'mask cap one below conservative enumerated limit',(C.BudgetRefusal,))
q=F(7,3);k=11;bits=k*(q.numerator.bit_length()+q.denominator.bit_length());ok(C.power(q,-k,max_exponent=k,max_bits=bits)==q**(-k),'exact exponent and rational-power precheck admission')
no(lambda:C.power(q,-k,max_exponent=k-1,max_bits=bits),'exponent cap one below',(C.BudgetRefusal,));no(lambda:C.power(q,-k,max_exponent=k,max_bits=bits-1),'power bit precheck one below',(C.BudgetRefusal,))
for val in [True,False,F(1),1.0,-1,None,'1']:
 no(lambda val=val:C.faces(p,max_masks=val),'strict mask budget')
 no(lambda val=val:C.power(q,1,max_exponent=val),'strict exponent budget')
 no(lambda val=val:C.power(q,1,max_bits=val),'strict power bit budget')
for bad in [True,False,F(1),1.0,-1,None,'1']:
 no(lambda bad=bad:C.resource_budget(p,bad,F(1),F(1,10)),'strict actual upper-total integer')
for field in ['time','risk']:
 for bad in [True,False,1.0,None,'1',F(-1)]:
  args=[p,10,F(1),F(1,10)];args[2 if field=='time'else 3]=bad;no(lambda args=args:C.resource_budget(*args),'strict exact resource '+field)
for bad in [F(0),F(1),F(2)]:no(lambda bad=bad:C.resource_budget(p,10,F(1),bad),'failure strictly between zero and one')
# Path-dependent ledger branches: history controls remaining-risk fractions.
for history in product([0,1],repeat=8):
 L=C.RiskLedger(F(1,10));spent=F(0);alloc=[]
 for bit in history:
  a=(F(1,10)-spent)/(2+bit);z=L.reserve(a);spent+=a;alloc.append(a)
  ok(z['status']=='ADMIT_EPISODE_RISK'and L.spent==spent and tuple(L.allocations)==tuple(alloc)and spent<=L.total,'continuing predictable ledger prefix invariant')
  before=(L.spent,tuple(L.allocations));no_alloc=L.reserve(L.total);ok(no_alloc['status']=='REJECT_NO_ALLOCATION'and before==(L.spent,tuple(L.allocations)),'overspend rejects without resetting history')
 for bad in [0,-1,True,0.01,'1/100',None]:
  before=(L.spent,tuple(L.allocations));ok(L.reserve(bad)['status']=='REJECT_NO_ALLOCATION'and before==(L.spent,tuple(L.allocations)),'invalid risk reservation unchanged')
report={'status':'PASS_VALID_CORE_CONTROLS_ONLY_REPAIR_FINDINGS_SEPARATE','version':version,'checks':checks,'expected_refusals':len(refusals),'categories':cats,'refusals':refusals,'seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(C.__file__).read_bytes()).hexdigest(),'scope':'actual raw/scalar receiver, all leaves, rate/input aliases, strict resource budget types, continuing-history ledger; separate v1 wire/alias/public-state failures not erased'}
(A/('controls_'+version+'_results.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='refusals'},indent=2))
