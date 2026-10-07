import sys, json, random, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bandwidth_parity import *
from low_rank_parity import sample_uv, dense_offdiagonal_rank_one, determinant
start = time.perf_counter(); rng = random.Random(8701)
F = [[G(int(i != j)) for j in range(4)] for i in range(4)]
UV = dense_offdiagonal_rank_one(F)
boundaries = {}
for name, call in [
    ('simple_sampler_negative_k', lambda: sample_uv(*UV, -1)),
    ('simple_sampler_empty_invalid_table', lambda: sample_uv(*UV, allowed=[]))
]:
    try:
        call(); raise AssertionError(name)
    except ValueError:
        boundaries[name] = 'REJECTED'
delta = Q(1, 2**24); F[0][1] += G(delta)
coeff, meta = count_band(F); assert coeff[2] == 2*delta*delta
word = sample_band(F, 2, randbits=rng.getrandbits)
I = [i for i, t in enumerate(word) if t == 'R']; J = [i for i, t in enumerate(word) if t == 'C']
assert len(I) == len(J) == 2 and determinant([[F[i][j] for j in J] for i in I]).norm() > 0
res = {'status': 'PASS', 'boundaries': boundaries,
       'tiny_band_sector': {'delta': str(delta), 'c2': str(coeff[2]), 'word': word, 'meta': meta},
       'scope': 'API audit after fixing invalid input handling; exact rare-sector finite bandwidth execution',
       'elapsed_seconds': time.perf_counter()-start}
Path('work/cycle6/c02_s01/revisions/SELF_AUDIT_CHECKS.json').write_text(json.dumps(res, indent=2)+'\n')
print(json.dumps(res, indent=2))
