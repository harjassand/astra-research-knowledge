"""IID Schur shape sampling through the RSK word correspondence, not a source-memory simulation."""
import random,bisect,json,math
from pathlib import Path
rng=random.Random(202610291047);sizes=[8,16,32,64,128,256,512];trials=10000;out=[]
for name,weights in [('uniform_rank8',[1]*8),('two_axis_gram',[1,1,1,2,2,3,3,3])]:
 cumulative=[];a=0
 for w in weights:a+=w;cumulative.append(a)
 stats={N:[] for N in sizes}
 for _ in range(trials):
  rows=[]
  for t in range(1,max(sizes)+1):
   x=bisect.bisect_right(cumulative,rng.randrange(a));r=0
   while True:
    if r==len(rows):rows.append([x]);break
    j=bisect.bisect_right(rows[r],x)
    if j==len(rows[r]):rows[r].append(x);break
    rows[r][j],x=x,rows[r][j];r+=1
   assert len(rows)<=8
   if t in stats:stats[t].append(len(rows[7]) if len(rows)==8 else 0)
 for N,vals in stats.items():
  count=sum(k>0 for k in vals);mean=sum(vals)/trials;p=count/trials;out.append(dict(model=name,N_minus_records=N,trials=trials,success_count=count,success_frequency=p,binomial_standard_error=math.sqrt(p*(1-p)/trials),mean_kernel_programs=mean,min_programs=min(vals),max_programs=max(vals)))
root=Path(__file__).parent;root.joinpath('iid_schur_counts.json').write_text(json.dumps(dict(scope='Seeded classical Monte Carlo of exact IID Schur distribution via RSK; not correlated-source guarantee, physical Schur circuit run, or hardware observation',rows=out),indent=2)+'\n')
for x in out:print(x['model'],x['N_minus_records'],x['success_frequency'],x['mean_kernel_programs'])
