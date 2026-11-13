from sampler import *
from pathlib import Path
import json,time
rng=np.random.default_rng(20261114);layers=[[(0,1),(2,3)],[(0,2),(1,3)]]*50;N=30000;ref=exact_density(4,layers,.03,.05);sums=np.zeros(16);sq=np.zeros(16);start=time.perf_counter()
for i in range(N):
 p,s=sample(4,layers,.03,.05,rng,distribution=True);sums+=p;sq+=p*p
mean=sums/N;var=np.maximum(0,(sq-N*mean*mean)/(N-1));se=np.sqrt(var/N);err=abs(mean-ref)
out={'purpose':'Fixed larger independent replication to reduce depth100 Monte Carlo uncertainty; initial3000-run result retained separately','n':4,'layers':100,'r':.03,'epsilon':.05,'trajectories':N,'seed':20261114,'seconds':time.perf_counter()-start,'TV_estimate_vs_exact_density':float(sum(err)/2),'max_coordinate_error':float(max(err)),'max_coordinate_error_in_empirical_standard_errors_diagnostic':float(max(err/np.maximum(se,1e-15))),'simultaneous_99_percent_Hoeffding_coordinate_radius':float(np.sqrt(np.log(2*16/.01)/(2*N))),'exact_distribution':ref.tolist(),'trajectory_average_distribution':mean.tolist(),'coordinate_standard_errors':se.tolist()}
Path(__file__).with_name('extended_benchmark_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
