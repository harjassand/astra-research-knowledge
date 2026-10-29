from pathlib import Path
import json,time
import clocked_channel_v1 as m
HERE=Path(__file__).parent
cases=[('rate_'+str(k),.001,k,{'one':1.,'two':2.,'prep':2.,'measure':4.,'feedback':1.}) for k in [.001,.003,.01,.03,.1,.3,1.]]
# At common rate0.0001/reference-unit, vary measurement duration ratio.
for dm in [1.,16.]:
 clock={'one':1.,'two':2.,'prep':2.,'measure':dm,'feedback':1.}
 tf=sum(m.duration(k,clock) for k,qs in m.fc.circuit(0,True));tu=sum(m.duration(k,clock) for k,qs in m.fc.circuit(0,False));tau=4*tf+4*tu+5
 cases.append(('measure_'+str(dm),.001,.0001*tau,clock))
for name,eta,strength,clock in cases:
 p=HERE/(name+'_v1.json')
 if p.exists():continue
 r=m.run_one(eta,strength,clock);p.write_text(json.dumps(r,indent=2)+'\n')
 print(name,'T32',r['encoded'][-1]['entanglement_infidelity'],'secs',r['timing']['construction_seconds'],flush=True)
