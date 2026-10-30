#!/usr/bin/env python3
import itertools,json
from pathlib import Path
import stress
out=[]
for L in (3,4):
 c=stress.make_code(L);sec=c['sectors'][0]
 for w in range(1,5):
  count=0;ex=None
  for qs in itertools.combinations(range(c['N']),w):
   e=sum(1<<q for q in qs);s=stress.syndrome(e,sec['checks'])
   if s and not any(stress.choose(s,fam) for fam in sec['families']):
    count+=1
    if ex is None:ex={'qubits':qs,'syndrome_mask':s,'minimum_syndrome_weight':sec['dist'][s]}
  out.append({'L':L,'weight':w,'nonzero_syndrome_local_minima':count,'example':ex})
  if count:break
Path(__file__).with_name('traps.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
