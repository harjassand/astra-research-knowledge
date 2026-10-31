"""Reproduce the separate fitted-mixture sampling check after phase_experiment.py."""
import json
import math
from pathlib import Path

import numpy as np

import phase_experiment as p

directory = Path(__file__).resolve().parent
path = directory / "phase_results.json"
result = json.loads(path.read_text())
adjacency = p.complete_graph(result["n"])
field = result["fit"]["estimate"]
rng = np.random.default_rng(923011)
samplers = {
    sign: p.PolymerSampler(
        p.make_polymers(adjacency, result["beta"], field, sign, result["cutoff"]),
        result["n"], result["certificate"]["theta"], 1e-6, rng
    ) for sign in [1, -1]
}
values, signs = [], []
rejected = 0
for _ in range(5000):
    sign = 1 if rng.random() < result["estimated_plus_phase_weight"] else -1
    threshold = result["n"]//2 if sign == 1 else (result["n"]+1)//2-1
    while True:
        mask = samplers[sign].sample()
        if mask.bit_count() <= threshold:
            break
        rejected += 1
    signs.append(sign)
    fraction = (result["n"]-mask.bit_count())/result["n"] if sign == 1 else mask.bit_count()/result["n"]
    values.append(fraction)
result.update(
    digital_mixture_sample_count=len(values),
    digital_minus_phase_samples=signs.count(-1),
    digital_mean_activation=float(np.mean(values)),
    digital_mean_hoeffding_radius_95=math.sqrt(math.log(40)/(2*len(values))),
    digital_phase_volume_rejections=rejected,
    digital_sample_update_attempts=sum(s.attempts for s in samplers.values()),
)
path.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({key:result[key] for key in [
    "digital_mixture_sample_count", "digital_minus_phase_samples", "digital_mean_activation",
    "digital_mean_hoeffding_radius_95", "digital_sample_update_attempts"
]}, indent=2))
