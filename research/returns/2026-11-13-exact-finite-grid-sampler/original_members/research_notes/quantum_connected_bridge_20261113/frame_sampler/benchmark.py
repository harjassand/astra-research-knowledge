import numpy as np,json,time,resource,tracemalloc
from pathlib import Path
from sampler import sample,exact_density
rng=np.random.default_rng(20261113);start=time.perf_counter();out={'implementation':'floating numpy; no large-system speed claim','trajectory_checks':[],'distribution_checks':[]}
for n,layers,r,e,N in [(4,[[(0,1),(2,3)],[(0,2),(1,3)]]*50,.03,.05,150),(4,[[(0,1),(2,3)],[(0,2),(1,3)]]*20,.5,.2,150),(3,[[(0,1)],[(1,2)]]*15,.2,.3,100)]:
 rows=[]
 for i in range(N):p,s=sample(n,layers,r,e,rng,validate=True,distribution=True);rows.append(s)
 out['trajectory_checks'].append({'n':n,'layers':len(layers),'r':r,'epsilon':e,'trajectories':N,'maximum_conditional_probability_error':max(x['conditional_output_max_error'] for x in rows),'maximum_measurement_probability_error':max(x['measurement_probability_error'] for x in rows),'maximum_infidelity':max(x['trajectory_infidelity'] for x in rows),'maximum_component_sites':max(x['max_component_physical_sites'] for x in rows),'maximum_amplitude_storage_bytes':max(x['amplitude_storage_bytes'] for x in rows),'resets_actually_sampled':sum(x['actual_resets'] for x in rows)})
for depth,N in [(12,10000),(100,3000)]:
 layers=[[(0,1),(2,3)],[(0,2),(1,3)]]*(depth//2);ref=exact_density(4,layers,.03,.05);sums=np.zeros(16);sq=np.zeros(16);t0=time.perf_counter();maxmem=0
 for i in range(N):
  p,s=sample(4,layers,.03,.05,rng,distribution=True);sums+=p;sq+=p*p;maxmem=max(maxmem,s['amplitude_storage_bytes'])
 mean=sums/N;var=np.maximum(0,(sq-N*mean*mean)/(N-1));se=np.sqrt(var/N);err=abs(mean-ref)
 out['distribution_checks'].append({'n':4,'layers':depth,'r':.03,'epsilon':.05,'trajectories':N,'seconds':time.perf_counter()-t0,'TV_estimate_vs_exact_density':float(sum(err)/2),'max_coordinate_error':float(max(err)),'max_coordinate_error_in_empirical_standard_errors_diagnostic':float(max(err/np.maximum(se,1e-15))),'simultaneous_99_percent_Hoeffding_coordinate_radius':float(np.sqrt(np.log(2*16/.01)/(2*N))),'mean_normalization':float(sum(mean)),'exact_distribution':ref.tolist(),'trajectory_average_distribution':mean.tolist(),'maximum_amplitude_storage_bytes':maxmem})
# Every candidate star on a2x2 square contains all4 sites; cap2 fails iff any candidate appears.
layers=[[(0,1),(2,3)],[(0,2),(1,3)]]*6;N=2000;fail=0
for i in range(N):x,s=sample(4,layers,.03,.05,rng,cap=2);fail+=s['aborted'];assert not s['aborted'] or x==0
out['cap_test']={'physical_site_cap':2,'trials':N,'observed_abort_rate':fail/N,'exact_abort_probability':1-(1-.05/.97)**24,'failure_output':'all zero bits','claim':'This cap is deliberately unusable here; no small TV guarantee asserted.'}
invalid=[]
for args in [(2,[[(0,1)]],.03,1.),(3,[[(0,1),(1,2)]],.03,.02)]:
 try:sample(*args,rng)
 except ValueError as e:invalid.append(str(e))
out['invalid_inputs_rejected']=invalid
tracemalloc.start();sample(4,[[(0,1),(2,3)],[(0,2),(1,3)]]*50,.03,.05,rng,validate=True,distribution=True);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
out['one_validation_trajectory_tracemalloc_peak_bytes']=peak;out['process_peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;out['total_seconds']=time.perf_counter()-start
Path(__file__).with_name('benchmark_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
