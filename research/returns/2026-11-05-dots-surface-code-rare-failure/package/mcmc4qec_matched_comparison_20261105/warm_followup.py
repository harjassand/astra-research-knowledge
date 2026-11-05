from independent_mcmc import *
start=time.perf_counter();m=Model(13);n=len(m.edges);ps=ladder(n,m.d)
chains=16;steps=8000;burn=1000
traces=np.empty((len(ps),chains,steps),np.uint16);current=[None]*chains;records=[]
a=json.loads((ROOT/'anchor.json').read_text())
for j,p in enumerate(ps):
 m._cache={};m._decode_calls=0;stats=[];init_trials=0
 for k in range(chains):
  if j==0:
   rng=np.random.default_rng(202611057000+k)
   while True:
    init_trials+=1;e=(rng.random(n)<p).astype(np.uint8)
    if State(m,e).isfailure():current[k]=e;break
  terminal=[]
  traces[j,k],st=simulate(m,p,'zanella',steps,burn,k,202611059000+100*j+k,initial=current[k],terminal=terminal)
  current[k]=terminal[0];stats.append(st)
 row=dict(rung=j,p=p,mean_weight=float(traces[j].mean()),chain_means=traces[j].mean(1).tolist(),
  actual_decoder_calls_including_initialization=m._decode_calls,cache_entries=len(m._cache),stats=stats,initialization_trials=init_trials)
 records.append(row);print(json.dumps({k:row[k] for k in ['rung','p','mean_weight','actual_decoder_calls_including_initialization']}),flush=True)
sample=time.perf_counter()-start
np.savez_compressed(ROOT/'zanella_warm_traces.npz',traces=traces,ladder=np.array(ps))
t=time.perf_counter();h=np.array([[np.bincount(x,minlength=n+1) for x in rung] for rung in traces])
rs=[bar(h[j].sum(0),h[j+1].sum(0),ps[j],ps[j+1],n) for j in range(len(ps)-1)]
rc=np.array([[bar(h[j,k],h[j+1,k],ps[j],ps[j+1],n) for j in range(len(ps)-1)] for k in range(chains)])
tot=rc.sum(1);point=math.exp(math.log(a['estimate'])+sum(rs));sechain=float(tot.std(ddof=1)/math.sqrt(chains))
seanchor=math.sqrt((1-a['estimate'])/(a['trials']*a['estimate']));se=math.hypot(sechain,seanchor)
crit=float(student_t.ppf(.9995,chains-1));err=crit*se
for j,row in enumerate(records):row['weight_iat_diagnostics']=[iat(x) for x in traces[j]]
r=dict(implementation='Independent published-kernel implementation with established warm-start splitting; not upstream software execution',kernel='zanella_warm',
 n=n,p=.001,chains=chains,steps=steps,burn_in=burn,ladder=ps,anchor=a,point_estimate=point,
 nominal_999_student_interval=[point*math.exp(-err),point*math.exp(err)],
 interval_status='Diagnostic asymptotic interval, not a finite-time coverage guarantee. Unverified mixing/systematic bias excluded.',
 log_standard_error=se,chain_log_standard_error=sechain,anchor_log_standard_error=seanchor,
 per_chain_log_ratio_sum=tot.tolist(),pooled_log_ratios=rs,rungs=records,
 total_proposals=sum(z['proposals'] for r in records for z in r['stats']),
 total_decoder_calls=sum(row['actual_decoder_calls_including_initialization'] for row in records),
 timing_seconds=dict(sampling_and_initialization=sample,analysis=time.perf_counter()-t,total_excluding_anchor=time.perf_counter()-start,total_including_anchor=time.perf_counter()-start+a['seconds']))
(ROOT/'zanella_warm_result.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:r[k] for k in ['point_estimate','nominal_999_student_interval','timing_seconds']}),flush=True)
