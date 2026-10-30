#!/usr/bin/env python3
import itertools,json
from pathlib import Path
import stress
root=Path(__file__).parent
out={'burst_tests':[],'silent_failures':[],'paired_final':[]}
for L in (3,4):
 c=stress.make_code(L);checks=0;witnesses=[]
 for sector,sec in enumerate(c['sectors']):
  for q in range(c['N']):
   e=1<<q;s=stress.syndrome(e,sec['checks'])
   while True:
    moves=0
    for family in sec['families']:
     move=stress.choose(s,family)
     if move:e^=move[0];s^=move[1];moves+=1
    if not moves:break
   assert s==0 and stress.reduce(e,sec['basis'])==0;checks+=1
  for qs in itertools.combinations(range(c['N']),L):
   e=sum(1<<q for q in qs)
   if not stress.syndrome(e,sec['checks']) and stress.reduce(e,sec['basis']):
    errors=[0,0];errors[sector]=e
    assert stress.decoded_failure(errors,[0,0],c)
    witnesses.append({'sector':sector,'qubits':qs,'syndrome':0,'logical_failure':True});break
 out['burst_tests'].append({'N':c['N'],'single_pauli_sector_errors_recovered':checks,'logical_witnesses':witnesses})
x=json.loads((root/'results.json').read_text())
for L in (3,4):
 for eps in x['rates']:
  rs=[r for r in x['raw'] if r['L']==L and r['epsilon']==eps]
  for mode in ('async','round_robin'):
   rows=[r['records'][mode][-1] for r in rs]
   out['silent_failures'].append({'N':2*L*L,'epsilon':eps,'mode':mode,'t':100,'count':sum(r['failure'] and r['syndrome_weight']==0 for r in rows),'n':len(rows)})
  out['paired_final'].append({'N':2*L*L,'epsilon':eps,'async_only_failure':sum(r['records']['async'][-1]['failure'] and not r['records']['round_robin'][-1]['failure'] for r in rs),'RR_only_failure':sum(r['records']['round_robin'][-1]['failure'] and not r['records']['async'][-1]['failure'] for r in rs)})
(root/'diagnostics.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
