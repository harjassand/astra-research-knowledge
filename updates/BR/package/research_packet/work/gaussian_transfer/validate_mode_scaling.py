from fractions import Fraction as F
from pathlib import Path
import random,time,json,statistics,resource
from large_herald_arb import LargeHeraldGaussian,AggregateMatching
from rational_gaussian_arb import RationalGaussian
from flint import __version__ as flint_version
out={'flint_version':flint_version,'tolerance':'1e-10','rows':[],'matched_DP':[],'negative_input_tests':[]}
for m in [3,5,8]:
 B=[[F(1,5) if i==j else F(1,10*m) for j in range(m)] for i in range(m)]
 h=10**20
 start=time.perf_counter();g=LargeHeraldGaussian.from_pure(B,0,h);setup=time.perf_counter()-start
 timings=[];outputs=[];random_bits=[]
 for seed in [777,778,779]:
  start=time.perf_counter();outputs.append(g.sample(random.Random(seed),F(1,10**10)));timings.append(time.perf_counter()-start);random_bits.append(g.last_random_bits)
 out['rows'].append({'modes':m,'herald':str(h),'output_dimension':len(outputs[0]),'setup_s':setup,'sample_seconds':timings,'median_s':statistics.median(timings),'max_scalar_calls':g.base.engine.max_scalar_calls,'routing_entries':sum(len(r.through)**2 for r in g.base.engine.records),'output_max_bits':max(x.bit_length() for y in outputs for x in y),'random_bits':random_bits,'last_ticket_bound':g.last_ticket_bound,'last_ticket_attempt_cap':g.last_ticket_attempt_cap,'first_output':list(map(str,outputs[0]))})
 for hsmall in [20,80]:
  start=time.perf_counter();old=RationalGaussian.from_pure(B,herald_modes=[0],herald_counts=[hsmall]);old_setup=time.perf_counter()-start
  start=time.perf_counter();new=LargeHeraldGaussian.from_pure(B,0,hsmall);new_setup=time.perf_counter()-start
  ot=[];nt=[]
  for seed in [777,778,779]:
   start=time.perf_counter();old.sample(random.Random(seed),F(1,10**10));ot.append(time.perf_counter()-start)
   start=time.perf_counter();new.sample(random.Random(seed),F(1,10**10));nt.append(time.perf_counter()-start)
  out['matched_DP'].append({'modes':m,'herald':hsmall,'old_DP_states':old.matching.Z.cache_info().currsize,'old_setup_s':old_setup,'new_setup_s':new_setup,'old_draw_median_s':statistics.median(ot),'new_draw_median_s':statistics.median(nt)})
 print('done',m,flush=True)
for name,call in [
 ('fractional_herald',lambda:AggregateMatching(1,1,F(-1,2))),
 ('float_herald',lambda:AggregateMatching(1,1,1.5)),
 ('bool_herald',lambda:AggregateMatching(1,1,True)),
 ('fractional_mode',lambda:LargeHeraldGaussian.from_pure([[F(1,4),F(1,4)],[F(1,4),F(1,4)]],F(1,2),4)),
 ('zero_event',lambda:AggregateMatching(1,0,3)),
 ('negative_herald',lambda:AggregateMatching(1,1,-1)),
 ('float_kernel',lambda:LargeHeraldGaussian.from_pure([[0.25,0],[0,0.25]],0,4))]:
 try:call()
 except (TypeError,ValueError) as err:out['negative_input_tests'].append({'name':name,'error':str(err)})
 else:raise AssertionError(name)
class AllOnes:
 def getrandbits(self,k):return (1<<k)-1
x=LargeHeraldGaussian.from_pure([[F(1,4),F(1,2)],[F(1,2),0]],0,10**20)
y=x.sample(AllOnes(),F(1,10**10))
assert y==[0] and x.last_ticket_fallback
out['injected_ticket_exhaustion']={'output':y,'flag':x.last_ticket_fallback,'bits':x.last_random_bits,'attempt_cap':x.last_ticket_attempt_cap}
out['whole_process_peak_rss_platform_units']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
Path(__file__).with_name('mode_scaling_results.json').write_text(json.dumps(out,indent=2))
