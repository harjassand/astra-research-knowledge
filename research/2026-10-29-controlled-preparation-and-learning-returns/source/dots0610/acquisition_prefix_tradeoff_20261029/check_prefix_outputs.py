import numpy as np,json
from pathlib import Path
h=Path(__file__).parent;a=np.load(h/'prefix_bank.npz');b=np.load('producer-workspace/actual_bank_counters.npz');maps=np.load(h/'prefix_maps.npz');old=np.load('producer-workspace/reviewed_fixture_arrays.npz');matching=np.load('producer-workspace/matching_memory_maps.npz')
out={'counter_replay_residual':float(np.linalg.norm(a['sums_1000000']-b['sums'])),'bath_replay_residual':float(np.linalg.norm(a['bath_1000000']-b['bath'])),'previous_1m_map_residuals':{},'CP_checks':[]}
for k,oldk in [('good','good'),('bad','bad'),('six_pass','two_pass'),('six_fail','two_fail'),('sigma','sigma')]:out['previous_1m_map_residuals'][k]=float(np.linalg.norm(maps[k+'_1000000']-old[oldk]))
for k,oldk in [('matching_pass','pass_map'),('matching_fail','fail_map')]:out['previous_1m_map_residuals'][k]=float(np.linalg.norm(maps[k+'_1000000']-matching[oldk]))
for m in [100,1000,10000,100000,1000000]:
 for k in ['good','bad','six_pass','six_fail','matching_pass','matching_fail']:
  T=maps[f'{k}_{m}'];C=T.reshape(2,2,2,2).transpose(0,2,1,3).reshape(4,4);v=float(np.linalg.eigvalsh(C).min());assert v>-1e-12
  out['CP_checks'].append({'prefix':m,'map':k,'min_Choi_eigenvalue':v})
assert max(out['previous_1m_map_residuals'].values())<1e-11
# Cross-over under exactly the same two fixed policies, continued retained bath.
t=np.load(h/'terminal_memory_maps.npz');tr=np.array([1,0,0,1]);acc={100000:0.,1000000:0.};calls={100000:0.,1000000:0.};states={m:maps[f'sigma_{m}'].reshape(-1) for m in acc};cross=None
for A in range(1,10001):
 rates={}
 for m in acc:
  q=states[m];acc[m]+=float((tr@t[f'six_acc_{m}']@q).real);calls[m]+=float((t[f'six_cost_{m}']@q).real);states[m]=t[f'six_end_{m}']@q;rates[m]=35*acc[m]/(m+calls[m])
 if rates[1000000]>=rates[100000] and cross is None:cross={'attempt_count':A,'rates':rates.copy()}
out['sixstate_1m_overtakes_100k_after_attempts']=cross
out['ten_thousand_attempts_rates']=rates
print(json.dumps(out,indent=2))
