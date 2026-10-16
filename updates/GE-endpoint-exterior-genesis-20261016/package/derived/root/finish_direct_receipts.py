"""Combine exact averaging and the unchanged source finite-fair-bit sampler bound.
No finite boost or mixing tail is added. This reads source code only after static
inspection; its table construction is rational and has no I/O on import.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util,json,hashlib
R=Path(__file__).resolve().parents[1]
p=next(x for base in [R,R.parent] for x in [base/'originals/pair/fair_bit_sampler.py',base/'originals/expanded/pair/fair_bit_sampler.py'] if x.exists())
s=importlib.util.spec_from_file_location('source_sampler',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
out=[]
for name in ['DIRECT_PATH6.json','DIRECT_BRANCH6.json','DIRECT_PATH20.json']:
 f=Path(__file__).parent/name;v=json.loads(f.read_text());n=v['n'];blocks=v['actual_fast_components']
 assert blocks==[[0],[1],list(range(2,n))]
 assert v['original_rates'][:2]==[1,10]
 assert all(x==0 for x in v['fast_design_rates'][:2])
 bound=F(v['direct_average_TV_upper_exact']);err=m.sampler_error(n);total=bound+err
 out.append({'input':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'n':n,'direct_average_TV_upper_exact':str(bound),'source_fair_bit_sampler_error_exact':str(err),'full_sampler_TV_upper_exact':str(total),'full_sampler_TV_upper_display':float(total),'certified_at_005':total<=F(1,20),'artificial_boost':None,'mixing_tail':None})
r={'schema':'astra.ge-direct-full-sampler.v1','source_sampler_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'assumptions':'independent fair bits; horizon 1, boundary rates 1 and 10, actual suffix component; original source sampler used unchanged','results':out,'scope':'Internal exact rational certificate composition. No external validation, historical priority, physical rates or incumbent speed advantage.'}
(Path(__file__).parent/'DIRECT_FULL_SAMPLER_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps([{k:x[k] for k in ['input','full_sampler_TV_upper_display','certified_at_005']} for x in out]))
