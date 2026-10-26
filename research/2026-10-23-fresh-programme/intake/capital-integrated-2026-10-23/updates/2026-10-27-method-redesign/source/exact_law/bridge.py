"""Checked sign proposals compiled into exact rational sparse output laws.

Scientific code for one bounded case study. Upstream source files are unchanged.
All numeric proposals are untrusted; exact checks determine admissibility.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import sys,json,time,math,hashlib,random,itertools,warnings,resource,traceback
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'vendor'))
import numpy as np
from scipy.optimize import linprog
import rounding_sparse_compiler as cube
import rounding_partition_compiler as part
from gsw_core.gsw import gram_schmidt_walk
from gsw_core.lpla import make_round
ORIGINAL_CUBE=cube.balanced_sign
ORIGINAL_PART=part.moment_sign

def cntr():return {'signing_calls':0,'max_signing_size':0,'compression_deletions':0,'max_precompression_support':0}
def seedfor(*vals):return int.from_bytes(hashlib.sha256(repr(vals).encode()).digest()[:4],'big')
def row_sums(D,eta):return [sum((v*s for v,s in zip(row,eta)),F(0))for row in D]
def score(D,eta):return max((abs(v)for v in row_sums(D,eta)),default=F(0))

def certify_sign(D,eta,s,factor):
 if len(eta)!=(len(D[0])if D else 0)or any(type(x)not in(int,np.int32,np.int64)or int(x)not in(-1,1)for x in eta):return False,'nonbinary_or_shape',None
 eta=[int(v)for v in eta];r=(2*len(D)-1).bit_length();vals=row_sums(D,eta)
 bound=factor*r*s
 if not all(x*x<bound for x in vals):return False,'exact_row_bound_rejected',max(map(abs,vals))
 return True,'exact_row_bound_passed',max(map(abs,vals),default=F(0))

class SignBridge:
 def __init__(self,method,case):self.method=method;self.case=case;self.events=[];self.cache={};self.proposals=0;self.failures=0;self.fallbacks=0;self.hits=0
 def choose(self,D,s,factor,fallback):
  key=(tuple(tuple(row)for row in D),s,factor);t=len(D[0]);call=len(self.events)
  event={'call':call,'active_size':s,'directions':t,'rows':len(D),'bound_factor':factor,'attempts':[]}
  if key in self.cache:
   eta=list(self.cache[key]);ok,why,val=certify_sign(D,eta,s,factor);assert ok
   self.hits+=1;event.update(cache_hit=True,chosen_score=str(val),fallback=False);self.events.append(event);return eta
  if self.method=='n24_exact':
   eta=fallback();ok,why,val=certify_sign(D,eta,s,factor);assert ok
   event.update(cache_hit=False,chosen_score=str(val),fallback=False,source='existing_N24_moment_signer')
  else:
   candidates=[]
   for attempt in range(8):
    rngseed=seedfor(self.case['seed'],call,attempt);rng=random.Random(rngseed)
    rec={'attempt':attempt,'seed':rngseed};eta=None
    try:
     if self.method.startswith('gsw'):
      # A common exact integer scale bounds every column norm by1.
      # GSW is only a proposal; no concentration or unbiasedness claim is used.
      scale=max(1,4*len(D));B=np.array([[float(v)/scale for v in row]for row in D],dtype=float)
      np.random.seed(rngseed)
      with warnings.catch_warnings(record=True)as ws:
       warnings.simplefilter('always')
       result=gram_schmidt_walk(B,chop=make_round(3)if self.method=='gsw3_checked'else None,max_steps=max(1,4*t))
      rec.update(upstream_failed=result.failed,steps=result.steps,warnings=[str(w.message)for w in ws],common_scale=scale)
      if result.failed is None:eta=[int(v)for v in result.assignment]
      else:rec['reason']='upstream_'+result.failed
     elif self.method=='random8_checked':eta=[rng.choice([-1,1])for _ in range(t)]
     elif self.method=='greedy8_checked':
      order=list(range(t))
      if attempt:rng.shuffle(order)
      vals=[F(0)]*len(D);eta=[0]*t
      for j in order:
       options=[]
       for sign in(-1,1):
        nxt=[v+sign*row[j]for v,row in zip(vals,D)]
        options.append(((max(map(abs,nxt),default=F(0)),sum(v*v for v in nxt),sign),sign,nxt))
       _,eta[j],vals=min(options,key=lambda x:x[0])
     else:raise ValueError(self.method)
     if eta is not None:
      ok,why,val=certify_sign(D,eta,s,factor);rec.update(accepted=ok,reason=why,score=str(val)if val is not None else None,signs=eta)
      if ok:candidates.append((val,tuple(eta),attempt))
     else:rec['accepted']=False
    except Exception as exc:rec.update(accepted=False,reason=type(exc).__name__,error=str(exc))
    self.proposals+=1
    if not rec['accepted']:self.failures+=1
    event['attempts'].append(rec)
   if candidates:
    val,eta,attempt=min(candidates);eta=list(eta);event.update(chosen_score=str(val),chosen_attempt=attempt,fallback=False)
   else:
    self.fallbacks+=1;eta=fallback();ok,why,val=certify_sign(D,eta,s,factor);assert ok
    event.update(chosen_score=str(val),fallback=True,fallback_source='existing_N24_moment_signer')
  self.cache[key]=tuple(eta);self.events.append(event);return eta
 def cube_sign(self,A,S,counter):
  padded=list(S)+([-1]if len(S)%2 else[]);pairs=list(zip(padded[::2],padded[1::2]))
  D=[[(row[i]if i>=0 else F(0))-(row[j]if j>=0 else F(0))for i,j in pairs]for row in A]
  def fallback():
   signs=ORIGINAL_CUBE(A,S,cntr());lookup=dict(zip(S,signs));return[lookup[i]for i,j in pairs]
  eta=self.choose(D,len(S),8,fallback);lookup={}
  for(i,j),v in zip(pairs,eta):
   if i>=0:lookup[i]=v
   if j>=0:lookup[j]=-v
  xi=[lookup[j]for j in S];assert abs(sum(xi))<=1
  counter['signing_calls']+=1;counter['max_signing_size']=max(counter['max_signing_size'],len(S));return xi
 def partition_sign(self,D,s,counter):
  eta=self.choose(D,s,16,lambda:ORIGINAL_PART(D,s,cntr()))
  counter['signing_calls']+=1;counter['max_signing_size']=max(counter['max_signing_size'],s);return eta

def exact_verify(case,law):
 A=[[F(v)for v in row]for row in case['A']];p=[F(v)for v in case['p']];n=len(p)
 assert law and len(law)<=n+1,'support'
 assert all(w>0 for a,w in law),'positive_weights'
 assert sum(w for a,w in law)==1,'normalization'
 assert all(len(a)==n and all(v in(0,1)for v in a)for a,w in law),'binary_shape'
 assert all(sum(w*a[j]for a,w in law)==p[j]for j in range(n)),'exact_means'
 assert all(a[j]==p[j]for a,w in law for j in range(n)if p[j]in(0,1)),'face'
 if case['blocks'] is not None:
  for block in case['blocks']:
   quota=sum(p[j]for j in block);assert quota.denominator==1,'input_quota'
   assert all(sum(a[j]for j in block)==quota for a,w in law),'quota'
 errors=[max(abs(sum(v*(z-q)for v,z,q in zip(row,a,p)))for row in A)for a,w in law]
 err=max(errors);mu=sum(min(v,1-v)for v in p);r=(2*len(A)-1).bit_length()
 if case['kind']=='cube':envelope=err<=1+mu if mu<=1 else max(F(0),err-1)**2<=144*r*mu
 else:envelope=err<=2+mu if mu<1 else max(F(0),err-1)**2<=400*r*mu
 return {'valid':True,'support':len(law),'discrepancy_exact':str(err),'discrepancy_float':float(err),'all_atom_errors':[str(x)for x in errors],'source_N24_envelope_passed':envelope,'largest_weight_denominator_bits':max(w.denominator.bit_length()for a,w in law)}

def systematic(case):
 p=[F(v)for v in case['p']];blocks=case['blocks'];intervals=[];cuts={F(0),F(1)}
 if blocks is None:
  cuts.update(p);cuts=sorted(cuts)
  return[(tuple(int((lo+hi)/2<q)for q in p),hi-lo)for lo,hi in zip(cuts,cuts[1:])],cntr(),{}
 intervals=[None]*len(p)
 for block in blocks:
  total=F(0)
  for j in block:
   intervals[j]=(total,total+p[j]);total+=p[j];cuts.add(total-math.floor(total))
 cuts=sorted(cuts);law=[]
 for lo,hi in zip(cuts,cuts[1:]):
  u=(lo+hi)/2;law.append((tuple(math.floor(b-u)-math.floor(a-u)for a,b in intervals),hi-lo))
 counter=cntr();law=cube.compress(law,counter);return law,counter,{}

def dependent(case):
 p=[F(v)for v in case['p']];A=[[F(v)for v in row]for row in case['A']];n=len(p)
 if case['blocks']is None:
  dummy=F(math.ceil(sum(p)))-sum(p);p=p+[dummy];A=[row+[F(0)]for row in A];blocks=[list(range(n+1))]
 else:blocks=case['blocks']
 law=[(tuple(p),F(1))];counter=cntr();rounds=0
 while any(any(v not in(0,1)for v in a)for a,w in law):
  rounds+=1;assert rounds<=len(p);branches=[]
  for atom,weight in law:
   options=[]
   for block in blocks:
    active=[j for j in block if 0<atom[j]<1]
    for i,j in itertools.combinations(active,2):options.append((max(abs(row[i]-row[j])for row in A),i,j))
   if not options:assert all(v in(0,1)for v in atom);branches.append((atom,weight));continue
   _,i,j=min(options);plus=min(1-atom[i],atom[j]);minus=min(atom[i],1-atom[j]);assert plus>0 and minus>0
   for delta,prob in[(plus,minus/(plus+minus)),(-minus,plus/(plus+minus))]:
    new=list(atom);new[i]+=delta;new[j]-=delta;branches.append((tuple(new),weight*prob))
  law=cube.compress(branches,counter)
 if case['blocks']is None:law=cube.compress([(a[:n],w)for a,w in law],counter)
 return law,counter,{'branching_rounds':rounds}

def exact_linear_solution(columns,rhs):
 if not columns:return None
 count=len(columns);M=[[F(columns[j][i])for j in range(count)]+[F(rhs[i])]for i in range(len(rhs))];row=0;piv=[]
 for col in range(count):
  at=next((i for i in range(row,len(M))if M[i][col]),None)
  if at is None:continue
  M[row],M[at]=M[at],M[row];v=M[row][col];M[row]=[x/v for x in M[row]]
  for i in range(len(M)):
   if i!=row and M[i][col]:v=M[i][col];M[i]=[x-v*y for x,y in zip(M[i],M[row])]
  piv.append(col);row+=1
  if row==len(M):break
 if any(not any(r[:-1])and r[-1]for r in M):return None
 x=[F(0)]*count
 for i,col in enumerate(piv):x[col]=M[i][-1]
 if any(v<0 for v in x):return None
 return x

def hull_certificate(vertices,p):
 n=len(p);k=len(vertices)
 if not k:return 'infeasible',{'empty_vertex_set':True}
 columns=[(1,)+tuple(v)for v in vertices];rhs=[F(1)]+p
 result=linprog(np.zeros(k),A_eq=np.array(columns,dtype=float).T,b_eq=np.array(rhs,dtype=float),bounds=(0,None),method='highs')
 if result.success:
  support=[j for j,v in enumerate(result.x)if v>1e-9];weights=exact_linear_solution([columns[j]for j in support],rhs)
  if weights is not None:
   law=[(tuple(vertices[j]),w)for j,w in zip(support,weights)if w]
   if all(sum(w*F(a[i])for a,w in law)==p[i]for i in range(n))and sum(w for a,w in law)==1:
    return 'feasible',{'law':law}
 # Independently propose a separating affine hyperplane and check it exactly.
 C=np.array([tuple(v)+(1,)for v in vertices],dtype=float)
 sep=linprog(np.array(p+[F(1)],dtype=float),A_ub=-C,b_ub=np.zeros(k),bounds=[(-1,1)]*(n+1),method='highs')
 if sep.success:
  q=[F(float(v)).limit_denominator(10**8)for v in sep.x]
  margins=[sum(v*x for v,x in zip(q[:-1],a))+q[-1]for a in vertices];target=sum(v*x for v,x in zip(q[:-1],p))+q[-1]
  if min(margins)>=0 and target<0:return 'infeasible',{'affine_separator':[str(v)for v in q],'minimum_vertex_margin':str(min(margins)),'target_margin':str(target)}
 return 'unknown',{'primal_status':result.message,'separator_status':sep.message}

def global_exact(case):
 if case['n']>8:return None,None,{'status':'not_applicable_predeclared_n_gt_8'}
 p=[F(v)for v in case['p']];A=[[F(v)for v in row]for row in case['A']];records=[]
 for atom in itertools.product((0,1),repeat=len(p)):
  if any(atom[j]!=p[j]for j in range(len(p))if p[j]in(0,1)):continue
  if case['blocks']is not None and any(sum(atom[j]for j in b)!=sum(p[j]for j in b)for b in case['blocks']):continue
  err=max(abs(sum(v*(z-q)for v,z,q in zip(row,atom,p)))for row in A);records.append((err,atom))
 thresholds=sorted({r[0]for r in records});lo=-1;hi=len(thresholds)-1;trace=[];certs={}
 def check(index):
  if index in certs:return certs[index]
  vv=[a for e,a in records if e<=thresholds[index]];state,cert=hull_certificate(vv,p);trace.append({'threshold':str(thresholds[index]),'state':state,'vertices':len(vv)});certs[index]=(state,cert);return state,cert
 state,cert=check(hi);assert state=='feasible',('whole_polytope_not_verified',state)
 while hi-lo>1:
  mid=(lo+hi)//2;state,cert=check(mid)
  if state=='feasible':hi=mid
  elif state=='infeasible':lo=mid
  else:raise RuntimeError('exact_global_status_unknown:'+str(trace))
 state,primal=check(hi);assert state=='feasible'
 predecessor={'nonnegative_norm_lower_bound':True}
 if hi>0:
  state,predecessor=check(hi-1);assert state=='infeasible'
 counter=cntr();law=cube.compress(primal['law'],counter)
 return law,counter,{'status':'exact_global_optimum_certified','optimum':str(thresholds[hi]),'eligible_vertices_total':len(records),'thresholds':len(thresholds),'trace':trace,'predecessor_threshold':str(thresholds[hi-1])if hi else None,'predecessor_certificate':predecessor}

def run(case,method):
 start=time.perf_counter();cpu=time.process_time();solver_start=time.perf_counter();bridge=None
 if method=='systematic':law,counter,meta=systematic(case)
 elif method=='dependent_greedy':law,counter,meta=dependent(case)
 elif method=='global_exact_small':law,counter,meta=global_exact(case)
 else:
  bridge=SignBridge(method,case);cube.balanced_sign=bridge.cube_sign;part.moment_sign=bridge.partition_sign
  A=[[F(v)for v in row]for row in case['A']];p=[F(v)for v in case['p']]
  if case['kind']=='cube':law,counter=cube.round_law(A,p)
  else:law,counter,_=part.partition_law(A,p,case['blocks'])
  meta={'proposals':bridge.proposals,'proposal_failures':bridge.failures,'fallback_calls':bridge.fallbacks,'cache_hits':bridge.hits,'signing_events':bridge.events}
 solve=time.perf_counter()-solver_start
 if law is None:return {'case_id':case['id'],'method':method,'status':'not_applicable','metadata':meta}
 verify_start=time.perf_counter();validation=exact_verify(case,law);verify=time.perf_counter()-verify_start
 return {'case_id':case['id'],'split':case['split'],'method':method,'status':'complete','validation':validation,'counter':counter,'solve_seconds':solve,'independent_validation_seconds':verify,'internal_total_seconds':time.perf_counter()-start,'cpu_seconds':time.process_time()-cpu,'peak_rss_raw':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'peak_rss_unit':'bytes_on_macOS','metadata':meta,'law':[{'atom':list(map(int,a)),'weight':str(w)}for a,w in law]}

if __name__=='__main__':
 cases=json.loads((ROOT/'INPUTS.json').read_text())['cases'];case=next(c for c in cases if c['id']==sys.argv[1]);method=sys.argv[2]
 out=ROOT/'runs'/__import__('os').environ.get('RUN_GENERATION','manual')/case['split']/(case['id']+'__'+method+'.json');out.parent.mkdir(parents=True,exist_ok=True)
 try:result=run(case,method)
 except BaseException as exc:result={'case_id':case['id'],'split':case['split'],'method':method,'status':'failed','error':repr(exc),'traceback':traceback.format_exc()}
 out.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in('case_id','method','status','validation','solve_seconds','error')if k in result}))
