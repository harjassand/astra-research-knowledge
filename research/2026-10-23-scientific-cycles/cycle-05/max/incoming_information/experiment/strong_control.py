"""Post-primary optimized ordinary moment control; no treatment retuning."""
from pathlib import Path
import itertools,ast,json,time,resource
D=Path(__file__).resolve().parent
# Load ONLY definitions/setup before the primary training loop. The original
# primary source/results stay unchanged; all setup and solver checks are reused.
src=(D/'run_information_test.py').read_text();prefix=src.split('\ntrain=[]\n')[0]
scope={'__file__':str(D/'run_information_test.py'),'__name__':'control_definitions'}
exec(compile(prefix,str(D/'run_information_test.py'),'exec'),scope)
np=scope['np'];diameter=scope['diameter'];response=scope['response'];e=scope['e']
begin=time.monotonic();cpu=time.process_time()
train=[]
for T in [1700,2300,2700]:
 for name,k in response(T,'corrected_index').items():train.append((T,name,k,diameter(k,[],0)['diameter']))
trials=[]
for degrees in itertools.combinations(range(2,13),3):
 B=np.array([e**d for d in degrees])
 vals=[diameter(k,B,1e-6)['diameter']/base for T,name,k,base in train]
 trials.append({'degrees':list(degrees),'worst':max(vals),'values':vals})
winner=min(trials,key=lambda r:(r['worst'],r['degrees']))
design_cost={'wall_s':time.monotonic()-begin,'cpu_s':time.process_time()-cpu,'lp_count':scope['COUNTS']['lp']}
(D/'STRONG_CONTROL_DESIGN_LOCK.json').write_text(json.dumps({'winner':winner,'trials':trials,'cost':design_cost},indent=2)+'\n')
B=np.array([e**d for d in winner['degrees']]);rows=[]
for T in [1500,1900,2100,2500,3000]:
 for variant in ['literal','corrected_index']:
  for output,k in response(T,variant).items():
   base=diameter(k,[],0)['diameter']
   for eps in [0.,1e-8,1e-6,1e-4]:
    r=diameter(k,B,eps,True)
    r.update(T_K=T,variant=variant,output=output,epsilon=eps,design='optimized_power_moments',degrees=winner['degrees'],normalized_diameter=r['diameter']/base,baseline_diameter=base)
    rows.append(r)
summary=[]
for eps in [0.,1e-8,1e-6,1e-4]:
 rr=[r for r in rows if r['epsilon']==eps]
 summary.append({'epsilon':eps,'max_normalized_diameter':max(r['normalized_diameter'] for r in rr),'median_normalized_diameter':float(np.median([r['normalized_diameter'] for r in rr])),'R_worst':max(r['normalized_diameter'] for r in rr if r['output']=='R'),'M_worst':max(r['normalized_diameter'] for r in rr if r['output']=='M')})
out={'scope':__doc__,'winner':winner,'design_cost':design_cost,'resources':{'wall_s':time.monotonic()-begin,'cpu_s':time.process_time()-cpu,'max_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'setup_not_in_control_timer':True},'counts':scope['COUNTS'],'max_checks':scope['MAX_CHECKS'],'summary':summary,'rows':rows}
(D/'STRONG_CONTROL_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['winner','resources','counts','max_checks','summary']},indent=2))
