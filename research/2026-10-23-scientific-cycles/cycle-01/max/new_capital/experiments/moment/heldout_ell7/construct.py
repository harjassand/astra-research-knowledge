from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import sys,json,time,hashlib
START=time.perf_counter(); CPU=time.process_time()
ROOT=Path('/workspace/scratch/f2e6b9408a0a/work/amplification_cycle_20261021/owners/pro2/Astra_Restore_PRO2_20261021')
sys.path.insert(0,str(ROOT/'src'))
from certified_jacobi import _IntervalArithmetic
D=2**32
jall=json.loads((ROOT/'results/krylov_certificates.json').read_text()); c=jall['64'][7]
inp=json.loads((ROOT/'results/input_construction.json').read_text());j=c['jacobi']
f=lambda z:F(int(z['numerator']),int(z['denominator']))
fj=lambda z:{'numerator':str(z.numerator),'denominator':str(z.denominator)}
aI=[int(z) for z in j['diagonal_int']]; bI=[int(z) for z in j['offdiagonal_int']]
a=[F(z,D) for z in aI]; b=[F(z,D) for z in bI]; bs=[z*z for z in b]
S=f(inp['M'])+f(inp['tau'])+f(c['residual']['operator_error']);x=F(12983,536870912)
source={'jacobi':{'diagonal_int':j['diagonal_int'],'offdiagonal_int':j['offdiagonal_int'],'denominator':str(D)},'M':inp['M'],'tau':inp['tau'],'operator_error':c['residual']['operator_error'],'x':fj(x),'S':fj(S),'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'results/krylov_certificates.json',ROOT/'results/input_construction.json']}}
Path('input.json').write_text(json.dumps(source,indent=2))
def R(t):
 r=1/(t-a[0])
 for ai,di in zip(a[1:],bs):r=1/(t-ai-di*r)
 return r
# Exact leading-minor positivity at +/-S, before any extension.
for sign in [1,-1]:
 pivot=S+sign*a[0]; assert pivot>0
 for ai,bi in zip(a[1:],bs):
  pivot=S+sign*ai-bi/pivot; assert pivot>0
AR=_IntervalArithmetic(180)
one=AR.integer(1);zero=AR.integer(0)
def weight(lo,hi,v):
 t=AR.enclosure(lo,hi);prev=one;curr=AR.mul(AR.sub(t,AR.rational(a[0])),AR.rational(1/b[0]));total=AR.add(one,AR.square(curr))
 for k in range(1,63):
  nxt=AR.mul(AR.sub(AR.mul(AR.sub(t,AR.rational(a[k])),curr),AR.mul(AR.rational(b[k-1]),prev)),AR.rational(1/b[k]))
  prev,curr=curr,nxt;total=AR.add(total,AR.square(curr))
 # Last normalized polynomial squared without approximating sqrt(v).
 num=AR.sub(AR.mul(AR.sub(t,AR.rational(a[63])),curr),AR.mul(AR.rational(b[62]),prev))
 total=AR.add(total,AR.mul(AR.square(num),AR.rational(1/v)))
 w=AR.reciprocal_positive(total)
 return w

def make(y,label):
 start=time.perf_counter();rx=R(y);v=(S-y)/(R(S)-rx);d=y-v*rx
 assert v>0
 assert S-d-v*R(S)==0
 left=d+S+v*R(-S);assert left>0
 # Zero-preserving integer Sturm recurrence on the original leading64 block,
 # with only the final step using the rational extension parameters.
 calls=0
 def count(t):
  nonlocal calls
  calls+=1
  u=t*D;m,q=u.numerator,u.denominator;q2=q*q
  prev=1;curr=aI[0]*q-m;last=1;n=0
  if curr:
   s=1 if curr>0 else -1;n+=s!=last;last=s
  for k in range(1,64):
   nxt=(aI[k]*q-m)*curr-bI[k-1]**2*q2*prev;prev,curr=curr,nxt
   if curr:
    s=1 if curr>0 else -1;n+=s!=last;last=s
  # Multiply through positive denominators rather than building a Fraction.
  dt=d-t
  final=dt.numerator*curr*v.denominator-dt.denominator*v.numerator*D*q*prev
  if final:
   s=1 if final>0 else -1;n+=s!=last
  return n,final==0
 assert count(-S)==(0,False);assert count(S)==(64,True)
 assert count(y)==(1,True)
 # All exact atoms are roots of this real irreducible65 Jacobi matrix.
 # Isolate every atom; first one is refined for a useful CDF enclosure.
 nodes=[]
 for idx in range(65):
  if idx==1:lo=hi=y
  elif idx==64:lo=hi=S
  else:
   lo,hi=-S,S
   bits=270 if idx==0 else 80
   while hi-lo>F(1,2**bits):
    mid=(lo+hi)/2;n,eq=count(mid)
    if eq and n==idx:lo=hi=mid;break
    if n<=idx:lo=mid
    else:hi=mid
   assert count(lo)[0]==idx and count(hi)[0]==idx+1
  wi=weight(lo,hi,v)
  nodes.append({'index':idx+1,'lower':fj(lo),'upper':fj(hi),'weight_lower':str(wi.lo),'weight_upper':str(wi.hi),'exact_node':lo==hi})
 # Certified first atom remains below the ORIGINAL threshold.
 assert f(nodes[0]['upper'])<x
 assert f(nodes[2]['lower'])>y
 assert all(f(nodes[k]['upper'])<f(nodes[k+1]['lower']) for k in range(64))
 cdf=AR.enclosure(F(nodes[0]['weight_lower']),F(nodes[0]['weight_upper']))
 if y==x:cdf=AR.add(cdf,AR.enclosure(F(nodes[1]['weight_lower']),F(nodes[1]['weight_upper'])))
 out={'prescribed_node':fj(y),'last_diagonal':fj(d),'last_offdiagonal_squared':fj(v),'support_left_schur':fj(left),'right_schur_exact_zero':True,'nodes':nodes,'cdf_at_x':{'lower':str(cdf.lo),'upper':str(cdf.hi)},'sturm_calls':calls,'wall_seconds':time.perf_counter()-start}
 Path(label+'.json').write_text(json.dumps(out,indent=2));print(label,'first_weight',nodes[0]['weight_lower'],nodes[0]['weight_upper']);print(label,'at_prescribed',nodes[1]['weight_lower'],nodes[1]['weight_upper']);print(label,'CDF',out['cdf_at_x'],'secs',out['wall_seconds'],flush=True)
 return out
up=make(x,'maximum_witness');near=make(x+F(1,2**60),'near_infimum_witness')
loW=F(up['nodes'][0]['weight_lower']);hiW=F(up['nodes'][0]['weight_upper']);wxl=F(up['nodes'][1]['weight_lower']);wxh=F(up['nodes'][1]['weight_upper'])
width=AR.enclosure(wxl,wxh)
gap=AR.sub(AR.enclosure(F(up['cdf_at_x']['lower']),F(up['cdf_at_x']['upper'])),AR.enclosure(F(near['cdf_at_x']['lower']),F(near['cdf_at_x']['upper'])))
summary={'infimum_inclusive':{'lower':str(AR.rational(loW).lo),'upper':str(AR.rational(hiW).hi),'attained':False},'maximum_inclusive':up['cdf_at_x'],'extremal_width':{'lower':str(width.lo),'upper':str(width.hi)},'concrete_witness_gap':{'lower':str(gap.lo),'upper':str(gap.hi)},'wall_seconds':time.perf_counter()-START,'cpu_seconds':time.process_time()-CPU,'precision':180,'notes':'Nonfirst nonprescribed atom weight intervals may be wide; exact weights are defined by the recurrence and atomic measure.'}
Path('summary.json').write_text(json.dumps(summary,indent=2));print('SUMMARY',json.dumps(summary,indent=2))
