"""Paid synthetic acquisition; only this file imports the plant."""
import json
import argparse
import math
from pathlib import Path
import numpy as np
from plant import word_table

ROOT = Path(__file__).resolve().parent
SETTINGS = [(0,), (1,), (0,0), (0,1), (1,1), (0,0,1), (0,1,1)]
parser=argparse.ArgumentParser()
parser.add_argument('--shots',type=int,default=1_000_000)
parser.add_argument('--seed',type=int,default=327687952)
parser.add_argument('--output',default='counts.json')
args=parser.parse_args()
N = args.shots
rng = np.random.default_rng(args.seed)
tables = []
for actions in SETTINGS:
    words, probabilities = word_table(actions)
    counts = rng.multinomial(N, probabilities)
    tables.append({"actions": list(actions), "shots": N,
                   "counts": {''.join(map(str,w)): int(c) for w,c in zip(words,counts)}})
width_denominator=1000000
width_target=(441*width_denominator**2+100*N-1)//(100*N)
width_numerator=math.isqrt(width_target)
if width_numerator**2<width_target:width_numerator+=1
data = {"provenance": "Synthetic multinomial batches of legal full-process reset episodes",
        "rank_upper_bound": 2, "preparations": [[],[0]],
        "tests": [[], [[1,1]]], "actions": [0,1], "outcomes": [0,1],
        "confidence_pool_K": 18, "hoeffding_width_rational": [width_numerator,width_denominator],
        "resets": N*len(SETTINGS),
        "native_interventions": N*sum(map(len,SETTINGS)), "tables": tables}
(ROOT/args.output).write_text(json.dumps(data, indent=2)+'\n')
print(json.dumps({k:data[k] for k in ['resets','native_interventions','rank_upper_bound']}, indent=2))
