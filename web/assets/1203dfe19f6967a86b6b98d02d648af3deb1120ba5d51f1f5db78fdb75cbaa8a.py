"""Runnable exact-admission example, not a state sampler.

For a four-site pair matrix supported across A={0,1}, B={2,3}, consider
canonical pair number k=2 and squared onsite filters t=(4,1,4,1).
The two t=4 sites exceed the uniform sufficient threshold 2, but compensation
within each color makes both complementary source polynomials admissible.
This does not require supplying F to test the filter class itself.
"""
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'work' / 'cycle3'))
from filter_rank_recognizer import recognize_complementary

result = {
    'scope': 'Exact coefficient admission only; counting/preparation not executed',
    'squared_filter_weights': [4, 1, 4, 1],
    'pair_number': 2,
    'color_A': recognize_complementary([[1, 1, 4], [1, 1, 1]], 2),
    'color_B': recognize_complementary([[4, 1, 1], [1, 1, 1]], 2),
}
print(json.dumps(result, indent=2))
