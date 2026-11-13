from fractions import Fraction as F
from pathlib import Path
import json,statistics
from exact_component_sampler import sample,grid_layers
rows=[]
for width in [16,32]:
 for eps in [F(1,50),F(1,20)]:
  vals=[]
  for j in range(20):
   output,s=sample(width*width,grid_layers(width,width,100),eps=eps,seed=60500+j,cap=4096,bitcap=20000);s['seed']=60500+j;s['output']=str(output);vals.append(s)
  summary=dict(n=width*width,T=100,epsilon=str(eps),trials=len(vals),aborts=sum(x['aborted'] for x in vals),mean_seconds=statistics.mean(x['seconds'] for x in vals),max_component_entries=max(x['max_component_entries'] for x in vals),max_live_entries=max(x['max_live_entries'] for x in vals),max_amplitude_integer_bits=max(x['max_amplitude_integer_bits'] for x in vals),max_live_payload_bits=max(x['max_live_payload_bits'] for x in vals),cap=4096,integer_bitcap=20000)
  rows.append(dict(summary=summary,raw=vals));print(summary,flush=True)
  Path(__file__).with_suffix('.json').write_text(json.dumps({'rows':rows,'scope':'Actual exactGaussianinteger output samples, ideal rational Born/category draws. Abortfallback bias remains; empiricalabort rates are not certifiedtails. Payloadbitmetric excludesPythonobjectoverhead and temporaryarrays.'},indent=2))
