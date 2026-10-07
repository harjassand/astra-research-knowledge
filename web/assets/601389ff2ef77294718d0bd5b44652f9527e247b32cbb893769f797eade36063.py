import json
import math
from pathlib import Path


root = Path(__file__).resolve().parent
codec = json.loads((root / "revisions" / "R2_codec_bound.json").read_text())
K = 1000
epsilon = 1 / 1000
h2 = -epsilon * math.log2(epsilon) - (1 - epsilon) * math.log2(1 - epsilon)
penalty = epsilon * math.log2(K) + 2 * h2
label_bits = math.log2(codec["total_labels_D"])
assert penalty < 0.1

print(json.dumps({
    "status": "PASS_FINITE_ALPHABET_CONTINUITY_DIAGNOSTIC",
    "K": K,
    "epsilon": epsilon,
    "continuity_penalty_bits": penalty,
    "R2_label_count_D": codec["total_labels_D"],
    "worst_case_label_bits": label_bits,
    "assertion": "epsilon*log2(K)+2*h2(epsilon)<0.1",
    "scope": "Numerical continuity-bound and label-bit check only; proofs are in R3.txt."
}, indent=2))
