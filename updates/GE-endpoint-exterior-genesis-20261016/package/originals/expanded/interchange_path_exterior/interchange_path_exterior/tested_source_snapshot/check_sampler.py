import sys,secrets,time,json,resource
from pathlib import Path
sys.path.insert(0,'/workspace/shared/interchange_local_saturation')
from fair_bit_sampler import sample_one,sampler_error
n=20;num=1000;bits_total=0;calls=0
def bits(k):
 global bits_total,calls
 bits_total+=k;calls+=1;return secrets.randbits(k)
t=time.perf_counter();count=0
for _ in range(num):
 x,k=sample_one(tuple(range(n)),bits);assert sorted(x)==list(range(n));count+=k
r=dict(n=n,samples=num,labels_conserved=True,seconds=time.perf_counter()-t,total_random_bits=bits_total,random_calls=calls,mean_attempts_diagnostic=count/num,sampler_error_exact=str(sampler_error(n)),sampler_error_float=float(sampler_error(n)),randomness='theorem assumes independent fair bits; execution used system secrets.randbits')
Path(__file__).with_name('sampler_receipt.json').write_text(json.dumps(r,indent=2));print(r)
