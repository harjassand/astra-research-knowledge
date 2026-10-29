#!/usr/bin/env python3
"""Exact controls for root's directed phase realization. No samples or RNG.

Construct full positive CTMCs, eliminate them independently, and compare
their full killed means. Fractions only; all rates, masses and moments exact.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import hashlib,json,time

ROOT=Path(__file__).resolve().parent

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F())
def solve(a,b):
 n=len(b)
 if not n:return []
 u=[list(a[i])+[b[i]] for i in range(n)]
 for j in range(n):
  r=next(i for i in range(j,n) if u[i][j])
  u[j],u[r]=u[r],u[j];pivot=u[j][j];u[j]=[v/pivot for v in u[j]]
  for i in range(n):
   if i!=j:
    z=u[i][j];u[i]=[x-z*y for x,y in zip(u[i],u[j])]
 x=[u[i][-1] for i in range(n)]
 assert all(dot(a[i],x)==b[i] for i in range(n))
 return x

def sub(a,ii,jj=None):
 if jj is None:jj=ii
 return [[a[i][j] for j in jj] for i in ii]

def build(wb,channels):
 """Each channel: (i,j,flow,[(mixture probability,[phase means]),...]).
 Empty branch means an actual direct edge; diagonal direct edges prohibited.
 """
 w=list(wb);edges=[];groups=[]
 for i,j,flow,branches in channels:
  assert flow>0 and sum(p for p,_ in branches)==1
  for p,means in branches:
   if not p:continue
   assert p>0
   f=flow*p;previous=i
   for mu in means:
    assert mu>0
    new=len(w);w.append(f*mu);edges.append((previous,new,f));previous=new
    groups.append((new,i,j))
   assert previous!=j,'zero-duration self jump is not a CTMC jump'
   edges.append((previous,j,f))
 n=len(w);lap=[[F()]*n for _ in range(n)]
 for i,j,f in edges:lap[i][i]+=f;lap[i][j]-=f
 assert all(sum(row)==0 for row in lap)
 assert all(sum(lap[i][j] for i in range(n))==0 for j in range(n))
 assert all(wi>0 for wi in w)
 # Every constructed channel is reachable from its source port; port
 # strong connectivity is checked on the full directed positive graph.
 for start in range(n):
  seen={start};todo=[start]
  while todo:
   i=todo.pop()
   for j in range(n):
    if i!=j and lap[i][j]<0 and j not in seen:seen.add(j);todo.append(j)
  assert len(seen)==n
 return {'w':w,'L':lap,'ports':len(wb),'hidden_channels':groups}

def extract(model):
 w=model['w'];lap=model['L'];m=model['ports'];hidden=list(range(m,len(w)))
 g=sub(lap,hidden);wi=[w[i] for i in hidden]
 t=solve(g,wi);s=[lap[i][i] for i in range(m)]
 harmonic=[solve(g,[-lap[i][j] for i in hidden]) for j in range(m)]
 timed=[solve(g,[wi[k]*harmonic[j][k] for k in range(len(hidden))]) for j in range(m)]
 f=[[F()]*m for _ in range(m)];mom=[[F()]*m for _ in range(m)]
 for i in range(m):
  inflow=[-lap[i][k] for k in hidden]
  for j in range(m):
   f[i][j]=(-lap[i][j] if i!=j else F())+dot(inflow,harmonic[j])
   mom[i][j]=dot(inflow,timed[j])
 assert all(sum(f[i])==s[i] for i in range(m))
 assert all(sum(f[i][j] for i in range(m))==s[j] for j in range(m))
 sr=[[F(i==j)*s[i]-f[i][j] for j in range(m)] for i in range(m)]
 br=[w[i]+sum(mom[i]) for i in range(m)]
 bl=[w[j]+sum(mom[i][j] for i in range(m)) for j in range(m)]
 assert sum(br)==sum(bl)==sum(w)
 direct_br=[w[i]+dot([-lap[i][k] for k in hidden],t) for i in range(m)]
 assert direct_br==br
 left=solve([list(row) for row in zip(*g)],wi)
 direct_bl=[w[j]+dot(left,[-lap[k][j] for k in hidden]) for j in range(m)]
 assert direct_bl==bl
 c=dot(wi,t)
 second=solve(g,[2*wi[k]*t[k] for k in range(len(hidden))])
 assert sum((dot([-lap[i][k] for k in hidden],second) for i in range(m)),F())/2==c
 return {'F':f,'M':mom,'wB':w[:m],'s':s,'S':sr,'bR':br,'bL':bl,'c':c,'mass':sum(w)}

def phases(mu,q,k):
 q0=mu*mu*(1+F(1,k));assert q>=q0
 if q==q0:return [(F(1),[mu/k]*k)],'erlang'
 if q<2*mu*mu:
  assert k>1
  alpha=(q-q0)/(2*mu*mu-q0)
  assert 0<alpha<1
  return [(1-alpha,[mu/k]*k),(alpha,[mu])],'erlang_exponential_mix'
 if q==2*mu*mu:return [(F(1),[mu])],'exponential'
 slow=q/mu-mu;p=mu*mu/(2*q-3*mu*mu)
 assert slow>mu and 0<p<1
 assert (1-p)*mu/2+p*slow==mu
 assert 2*((1-p)*(mu/2)**2+p*slow**2)==q
 return [(1-p,[mu/2]),(p,[slow])],'hyperexponential'

def realize(record,eps,region_of=None,region_c=None):
 assert eps>0
 k=(F(1)/eps).__ceil__();m=len(record['wB']);f=record['F'];mom=record['M']
 keys=[(i,j) for i in range(m) for j in range(m) if f[i][j]>0 and mom[i][j]>0]
 q={key:(mom[key[0]][key[1]]/f[key[0]][key[1]])**2*(1+F(1,k)) for key in keys}
 if region_of is None:
  region_of=[0]*m;region_c={0:record['c']}
 else:
  assert all(region_of[i]==region_of[j] for i,j in keys)
 regions=sorted(set(region_of));target_c={};baseline={}
 for r in regions:
  kk=[key for key in keys if region_of[key[0]]==r]
  baseline[r]=sum((f[i][j]*q[i,j] for i,j in kk),F())/2
  c=region_c[r]
  if baseline[r]<c:
   assert kk
   i,j=kk[0];q[i,j]+=2*(c-baseline[r])/f[i][j]
  target_c[r]=max(c,baseline[r]);assert c<=target_c[r]<=(1+eps)*c
 branches_used=[];channels=[]
 for i in range(m):
  for j in range(m):
   if not f[i][j]:assert mom[i][j]==0;continue
   if not mom[i][j]:
    assert i!=j
    channels.append((i,j,f[i][j],[(F(1),[])]));continue
   mu=mom[i][j]/f[i][j];branch,kind=phases(mu,q[i,j],k)
   # Independently verify mixture first and second moments.
   got_mu=sum(p*sum(means) for p,means in branch)
   got_q=sum(p*(sum(means)**2+sum(x*x for x in means)) for p,means in branch)
   assert got_mu==mu and got_q==q[i,j]
   channels.append((i,j,f[i][j],branch));branches_used.append(kind)
 fitted=build(record['wB'],channels)
 assert len(fitted['w'])<=m+k*len(keys)+sum(region_c[r]>0 for r in regions)
 actual=extract(fitted)
 for key in ['F','M','wB','s','S','bR','bL','mass']:assert actual[key]==record[key],key
 assert actual['c']==sum(target_c.values())
 return fitted,{'k':k,'positive_duration_channels':len(keys),'baseline_c':baseline,
  'target_c':target_c,'branches':branches_used,'state_bound':m+k*len(keys)+sum(region_c[r]>0 for r in regions)}

def mean(model,target):
 keep=[i for i in range(len(model['w'])) if i not in target]
 if not keep:return None,[]
 w=[model['w'][i] for i in keep];h=solve(sub(model['L'],keep),w)
 return dot(w,h)/sum(w),list(zip(keep,h))

def attach(model,load,ground,pendant_mass,pendant_flow):
 w=list(model['w']);m=model['ports'];lap=[row[:] for row in model['L']]
 for i in range(m):w[i]+=load[i]
 old=len(w);w.extend([pendant_mass,F(1)])
 for row in lap:row.extend([F(),F()])
 lap.extend([[F()]*(old+2) for _ in range(2)])
 def edge(i,j,f):
  lap[i][i]+=f;lap[j][j]+=f;lap[i][j]-=f;lap[j][i]-=f
 edge(0,old,pendant_flow)
 for i in range(m):edge(i,old+1,ground[i])
 return {'w':w,'L':lap,'ports':m},old+1

def source_cases():
 cases=[]
 for phases_n in [1,2,7]:
  channels=[(0,1,F(1),[(F(1),[F(1,phases_n)]*phases_n)]),(1,0,F(1),[(F(1),[])])]
  cases.append((f'two_port_erlang_{phases_n}',build([F(1),F(1)],channels)))
 cases.append(('two_port_hyper',build([F(3,2),F(2)],[(0,1,F(1),[(F(6,7),[F(1,2)]),(F(1,7),[F(4)])]),(1,0,F(1),[(F(1),[])])])))
 cases.append(('one_port_self_return',build([F(1,2)],[(0,0,F(1),[(F(1),[F(1,7)]*7)])])))
 f=[[F(1),F(2),F(1)],[F(),F(1,2),F(2)],[F(3),F(),F()]]
 mus={(0,0):F(1,2),(0,1):F(1),(1,1):F(2),(1,2):F(3,2),(2,0):F(1,3)}
 ch=[]
 for i in range(3):
  for j in range(3):
   if f[i][j]:ch.append((i,j,f[i][j],[(F(1),[mus[i,j]/5]*5 if (i,j) in mus else [])]))
 cases.append(('three_port_directed_with_self_returns',build([F(2),F(3,2),F(1)],ch)))
 # No hidden duration: c=0 adjustment must be skipped.
 cases.append(('direct_two_port',build([F(1),F(2)],[(0,1,F(3),[(F(1),[])]),(1,0,F(3),[(F(1),[])])])))
 return cases

def serialize(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,list):return [serialize(v) for v in x]
 if isinstance(x,dict):return {str(k):serialize(v) for k,v in x.items()}
 return x

def main():
 begin=time.perf_counter();results=[];port_checks=0;external_checks=0;branch_set=set();exact_corollary=[]
 for name,source in source_cases():
  record=extract(source);m=source['ports']
  a=sum((record['M'][i][j]**2/record['F'][i][j] for i in range(m) for j in range(m) if record['M'][i][j]>0),F())/2
  if record['c']:
   assert a<record['c']
   k_exact=max(1,(a/(record['c']-a)).__ceil__())
   fitted_exact,exact_info=realize(record,F(1,k_exact))
   assert extract(fitted_exact)['c']==record['c']
   exact_corollary.append({'case':name,'a':a,'c':record['c'],'k_exact':k_exact,
                           'fitted_states':len(fitted_exact['w']),'state_bound':exact_info['state_bound']})
  for eps in [F(1,3),F(1,2),F(1),F(2)]:
   fitted,info=realize(record,eps);actual=extract(fitted);branch_set.update(info['branches'])
   mean_ratios=[]
   for mask in range(1,1<<m):
    target=[i for i in range(m) if mask>>i&1]
    original,hs=mean(source,target);approx,hf=mean(fitted,target)
    if original is None:assert approx is None;continue
    assert original<=approx<=(1+eps)*original
    rs=dict(hs);rf=dict(hf)
    assert all(rs[i]==rf[i] for i in range(m) if i not in target)
    mean_ratios.append(approx/original);port_checks+=1
   for trial in range(3):
    load=[F((trial+i)%3,3) for i in range(m)]
    ground=[F(trial+i+1,2) for i in range(m)]
    ex0,target0=attach(source,load,ground,F(trial+1,2),F(2,3))
    ex1,target1=attach(fitted,load,ground,F(trial+1,2),F(2,3))
    original,hs=mean(ex0,[target0]);approx,hf=mean(ex1,[target1])
    assert original<=approx<=(1+eps)*original
    assert all(dict(hs)[i]==dict(hf)[i] for i in range(m))
    assert (approx-original)*(sum(ex0['w'])-ex0['w'][target0])==actual['c']-record['c']
    external_checks+=1
   results.append({'case':name,'epsilon':eps,'source_states':len(source['w']),'fitted_states':len(fitted['w']),
    'source_c':record['c'],'fitted_c':actual['c'],'max_port_mean_factor':max(mean_ratios,default=F(1)),'construction':info})

 # Separator-aware modules; global-c matching alone is an explicit negative.
 z=F(10**6);wb=[F(1,10**6)]*4
 channels=[(0,1,F(1),[(F(1),[F(1,5)]*5)]),(1,0,F(1),[(F(1),[])]),
           (2,3,F(1),[(F(1),[F(1)]*2)]),(3,2,F(1),[(F(1),[])])]
 channels.extend((i,j,z,[(F(1),[])]) for i in [0,1] for j in [2,3])
 channels.extend((j,i,z,[(F(1),[])]) for i in [0,1] for j in [2,3])
 source=build(wb,channels);record=extract(source);eps=F(1,3)
 region_c={0:F(3,5),1:F(3)};region_of=[0,0,1,1]
 good,info=realize(record,eps,region_of,region_c)
 bad,badinfo=realize(record,eps)
 macro=[]
 for killed in [0,1]:
  def killed_set(model):
   ports=[i for i in range(4) if i//2==killed]
   hidden=[idx for idx,i,j in model['hidden_channels'] if i//2==killed]
   return ports+hidden
  original,hs=mean(source,killed_set(source));approx,hg=mean(good,killed_set(good))
  uncontrolled,hb=mean(bad,killed_set(bad))
  assert original<=approx<=(1+eps)*original
  if killed==1:assert uncontrolled>(1+eps)*original
  macro.append({'absorbed_module':killed,'true_mean':original,'modulewise_mean':approx,
                'global_c_only_mean':uncontrolled,'global_c_only_factor':uncontrolled/original})
 assert extract(bad)['c']==record['c']
 # State lower-bound algebra with exact fixed F,M,wB.
 lower_controls=[]
 for n in [1,2,7,64,1024]:
  for eps in [F(1,2),F(1,8),F(1,32)]:
   required=1/(eps+(1+eps)/n)
   lower_controls.append({'erlang_source_phases':n,'epsilon':eps,'necessary_hidden_states_at_least':required})
 assert branch_set=={'erlang','exponential','erlang_exponential_mix','hyperexponential'}
 out={'status':'PASS','source_calls':0,'RNG_calls':0,'numeric_arithmetic':'exact rational only',
  'constructed_cases':results,'port_target_mean_checks':port_checks,'passive_external_mean_checks':external_checks,
  'separator_module_checks':macro,'modulewise_construction':info,'global_c_only_construction':badinfo,
  'all_four_phase_branches_checked':sorted(branch_set),'state_lower_bound_algebra':lower_controls,
  'instance_dependent_exact_corollary_checks':exact_corollary,
  'scope':'Exact supplied records and mathematical positive CTMC realizations; no statistical acquisition, physical compilation, all-path-law guarantee, or historical novelty claim.',
  'wall_seconds':time.perf_counter()-begin}
 (ROOT/'NONREVERSIBLE_APPROXIMATE_REALIZATION_CHECKS.json').write_text(json.dumps(serialize(out),indent=2)+'\n')
 print(json.dumps({'status':'PASS','cases':len(results),'port_mean_checks':port_checks,'external_mean_checks':external_checks,
  'macro_factors':[{k:float(v) for k,v in r.items() if isinstance(v,F)} for r in macro],
  'wall_seconds':out['wall_seconds']},indent=2))

if __name__=='__main__':main()
