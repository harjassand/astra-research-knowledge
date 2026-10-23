"""Exact finite illustration of the adjacent identification proof.

Not a chemistry simulation, scientific performance test, or owner replay.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import resource
import time

start_wall=time.perf_counter()
start_cpu=time.process_time()

rows=[]
for s in [F(1,4),F(3,4)]:
    x={t:F(1,2**t) for t in [0,1,2,3]}
    y={t:s*(1-x[t]) for t in x}
    u={t:(1-s)*(1-x[t]) for t in x}
    assert all(x[t]+y[t]+u[t]==1 for t in x)
    assert all(min(x[t],y[t],u[t])>=0 for t in x)
    z={t:y[t]/y[2] for t in x}
    rows.append({'s':str(s),'nitrite':{str(t):str(v) for t,v in x.items()},
                 'retained_nitrate':{str(t):str(v) for t,v in y.items()},
                 'other_original_N':{str(t):str(v) for t,v in u.items()},
                 'normalized_nitrate_at_t2':{str(t):str(v) for t,v in z.items()}})
assert rows[0]['nitrite']==rows[1]['nitrite']
assert rows[0]['normalized_nitrate_at_t2']==rows[1]['normalized_nitrate_at_t2']
ratio=F(rows[1]['retained_nitrate']['2'])/F(rows[0]['retained_nitrate']['2'])
assert ratio==3
amplitude=F(rows[0]['retained_nitrate']['2'])
loss=1-F(rows[0]['nitrite']['2'])
identified_s=amplitude/loss
assert identified_s==F(1,4)
photon_dose=F(24)
identified_yield=amplitude/photon_dose
assert identified_yield==F(1,128)
# The product query is fixed while independently unobserved gas partition varies.
other=F(rows[0]['other_original_N']['2'])
gas_partitions=[{'gas_original_N':str(h*other),
                 'other_retained_original_N':str((1-h)*other)} for h in [F(0),F(1)]]
assert gas_partitions[0]!=gas_partitions[1]
# Optional measured-interval example; these are artificial exact values, not chemistry data.
qlo,qhi=F(23),F(25)
a=(F(11,64)/qhi,F(13,64)/qlo)
b=(F(35,64)/qhi,F(37,64)/qlo)
assert a[1]<b[0]
out={'scope':'Exact finite descriptive illustration; continuum algebra in adjacent proof is authoritative.',
     'rows':rows,'identical_observed_channels':True,'retained_product_ratio_at_same_dose':str(ratio),
     'one_original_N_amplitude_identifies':{'amplitude_t2':str(amplitude),'s':str(identified_s),
                                          'delivered_photon_dose':str(photon_dose),
                                          'product_per_photon':str(identified_yield)},
     'gas_partition_still_unidentified':gas_partitions,
     'artificial_measured_interval_illustration':{'A':list(map(str,a)),'B':list(map(str,b)),
                                                  'B_strictly_exceeds_A':True},
     'costs':{'body_wall_seconds':time.perf_counter()-start_wall,
              'body_process_CPU_seconds':time.process_time()-start_cpu,
              'process_high_water_RSS_KiB_Linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'scope':'Body and process memory only, excluding authoring, source review and initial unmetered illustrative run.',
              'discovery_cost':'unknown'},
     'physical_model_admission':False,'owner_science_replayed':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
