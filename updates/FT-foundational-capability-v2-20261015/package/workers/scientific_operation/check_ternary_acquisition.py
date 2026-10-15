#!/usr/bin/env python3
"""Verify the same theorem on three physical actuator levels {0,1,2}."""
import json
from pathlib import Path
import numpy as np
from check_scalar_acquisition import ScalarOracle, acquire, dissipative_plant, response

root=Path(__file__).parent
rows=[]
for noise in (0.,1e-8,1e-6,1e-4):
    errors=[]; relative=[]; nonreal=[]; minimum=[]
    for seed in range(8):
        f0,a,H,physical=dissipative_plant(32,seed)
        oracle=ScalarOracle(f0,a,H,noise,1000+seed)
        fh,ah,Hh,info=acquire(32,oracle,t1=1.,t2=2.,t3=1.)
        rng=np.random.default_rng(10000+seed)
        us=rng.uniform(0,2,(100,32))
        truth=np.array([response(f0,a,H,u) for u in us])
        pred=np.array([response(fh,ah,Hh,u) for u in us])
        errors.append(float(np.sqrt(np.mean(abs(pred-truth)**2))))
        relative.append(float(np.linalg.norm(pred-truth)/np.linalg.norm(truth-f0)))
        nonreal.append(info["nonreal_pairs"])
        minimum.append(info["minimum_triangle_candidate_separation"])
    rows.append({"m":32,"actuator_levels":[0,1,2],"queries_per_run":info["queries"],
                 "runs":8,"absolute_response_noise_sd":noise,
                 "median_heldout_rms_absolute_error":float(np.median(errors)),
                 "maximum_heldout_rms_absolute_error":float(np.max(errors)),
                 "median_error_relative_to_control_induced_response":float(np.median(relative)),
                 "total_nonreal_pair_estimates":sum(nonreal),
                 "median_minimum_triangle_candidate_separation":float(np.median(minimum))})

f0,a,H,physical=dissipative_plant(8,43)
oracle=ScalarOracle(f0,a,H)
fh,ah,Hh,info=acquire(8,oracle,t1=1.,t2=2.,t3=1.)
receipt={"kind":"synthetic_scalar_measurement_receipt_not_laboratory_data",
         "m":8,"actuator_levels":[0,1,2],"seed":43,"physical_metadata":physical,
         "measurements":[{"u":u.tolist(),"response":y} for u,y in oracle.records],
         "ground_truth_normalized_model":{"f0":f0,"a":a.tolist(),"H":H.tolist()},
         "acquired_normalized_model":{"f0":fh,"a_real":ah.real.tolist(),"a_imag":ah.imag.tolist(),
                                      "H_real":Hh.real.tolist(),"H_imag":Hh.imag.tolist()},
         "acquisition_info":info}
(root/'ternary_example_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
output={"status":"synthetic_check_only","trials":rows}
(root/'ternary_acquisition_results.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
