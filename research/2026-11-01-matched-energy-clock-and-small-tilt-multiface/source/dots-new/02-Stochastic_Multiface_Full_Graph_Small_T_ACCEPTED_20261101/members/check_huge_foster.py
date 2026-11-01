from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,time
import independent_receiver as I
HERE=Path(__file__).resolve().parent

def signed_hash(x):
 return hashlib.sha256((I.rational_text(x)).encode()).hexdigest()
def run():
 started=time.monotonic();out=[]
 fixtures=[('triangle_plus_edge',I.fixture()),('P4_plus_isolate_sparse',I.fixture(5,((0,1),(1,2),(2,3)),sparse=True)),('two_triangles',I.fixture(6,((0,1),(0,2),(1,2),(3,4),(3,5),(4,5)),sparse=True))]
 for name,raw in fixtures:
  p=I.construct(raw);r=p['raw'];f=I.IntervalFoster(p,precision=8192,exact_power_bits=20000);N=p['Nstar'];T=p['T'];n=r['n'];states=[]
  def state(A,**kw):
   x=[0]*(n+1);x[0]=A
   for i,v in kw.items():x[int(i)]=v
   return tuple(x)
  for offset in [0,1,17]:
   K=N+offset
   states += [state(0,**{'1':K}),state(1,**{'1':K}),state(2,**{'1':K}),state(K,**{'1':K}),state(0,**{'1':K,'2':K}),state(0,**{'1':K,'4':K//(10*T)}),state(1,**{'1':K,'4':K//(10*T)}),state(0,**{'1':K,'4':K//(10*T),'5':1}),state(0,**{'1':K,'4':T+1,'5':T+1}),state(1,**{'1':K,'4':1,'5':1}),state(0,**{'1':K,'2':1,'4':T+1,'5':1})]
  # Exact N=Nstar controls, plus highly separated inactive/active reservoirs.
  states += [state(1,**{'1':N-1}),state(2,**{'1':N-2}),state(N),state(0,**{'1':N*N,'4':N}),state(1,**{'1':N*N,'4':N}),state(0,**{'1':N*N,'4':N,'5':1})]
  states=list(dict.fromkeys(states));records=[];branches={'empty_large':0,'nonempty_large':0,'strict_subset':0,'last_death':0,'inactive':0}
  for index,x in enumerate(states):
   assert sum(x)>=N
   lo,hi=f.generator(x,f.h);assert hi<=-p['nu'],(name,index,'Foster failure')
   pl,ph=f.generator(x,f.psi);rhs=f.global_rhs_lower(x);assert ph<=rhs,(name,index,'global sum failure')
   A=x[r['A']];Qhub=sum(x[a]*x[b]for a,b in r['edges'])
   if A==0 and Qhub==0:branches['inactive']+=1
   if A==1 and Qhub==0:branches['last_death']+=1
   for face in p['faces']:
    U=sum(x)-sum(x[i]for i in face['I']);large=frozenset(i for i in face['I']if x[i]>=T*(U+1))
    if not large:branches['empty_large']+=1
    else:
     branches['nonempty_large']+=1
     if large!=face['I']:branches['strict_subset']+=1
   assert lo<=hi
   records.append({'state':[I.decimal(v)for v in x],'total_count_bits':sum(x).bit_length(),'generator_upper_sha256':signed_hash(hi),'generator_lower_sha256':signed_hash(lo),'certified_integer_multiple_of_nu':(-hi/p['nu']).numerator//(-hi/p['nu']).denominator,'global_inequality_slack_nonnegative':rhs-ph>=0})
  out.append({'fixture':name,'Nstar_bits':N.bit_length(),'Nstar_decimal':I.decimal(N),'faces':len(p['faces']),'states':records,'branches':branches,'precision_bits':f.precision,'exact_power_bit_budget':f.exact_power_bits,'max_expanded_power_bit_bound':f.max_expanded_power_bits,'max_profile_resource_bits':f.max_resource_bits,'exact_profile_values':f.exact,'enclosed_profile_values':f.enclosed,'giant_head_power_expanded':False})
 result={'status':'PASS_INDEPENDENT_ACTUAL_POINTWISE_FOSTER_AND_GLOBAL_SUM_INTERVALS','theorem_sha256':'dc96226443a99ee0a8541f03cce5af28ff735a95c6855053d223cf87d5001327','candidate_code_imported':False,'fixtures':out}
 (HERE/'HUGE_FOSTER_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'actual_states':sum(len(f['states'])for f in out),'fixture_Nstar_bits':[f['Nstar_bits']for f in out],'elapsed_seconds':time.monotonic()-started},sort_keys=True))
if __name__=='__main__':run()
