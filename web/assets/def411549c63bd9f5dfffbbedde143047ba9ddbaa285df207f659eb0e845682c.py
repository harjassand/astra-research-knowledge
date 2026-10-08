#!/usr/bin/env python3
"""Exact enumeration of the two-type zero-map detyping counterexample.

Uses the intended symmetric block parsing of arXiv:2510.07162v1 Def. 5.8.
No floating-point computation or optimization is needed.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent
SOURCES = HERE / 'sources'
SOURCES.mkdir(exist_ok=True)
source_dir = HERE.parent / 'repetition_application' / 'sources'
for filename in ('lin-source-CondLineardist.tex', 'lin-source-Preliminary.tex'):
    if not (SOURCES / filename).exists():
        shutil.copyfile(source_dir / filename, SOURCES / filename)

# Two-bit mask positions are ordered by types (0, 1).
def at(mask, v):
    return (mask >> (1-v)) & 1

def restrict(mask, v):
    return at(mask, v) << (1-v)

def sample(control):
    s0, s1, s2, s3, s4, s5 = control
    if s1 == 3:
        x = (s0, s1, 0, 0, s4, restrict(s5, s0), 0)
    else:
        x = (s0, s1, 0, 0, 0, 0, 0)
    if s3 == 3:
        y = (s2, s3, 0, 0, s5, restrict(s4, s2), 0)
    else:
        y = (s2, s3, 0, 0, 0, 0, 0)
    nontrivial = s1 == s3 == s4 == s5 == 3
    parity = (s0 ^ s2) if nontrivial else 0
    return x, y, nontrivial, parity

def bits(q):
    widths = (1,2,1,2,2,2,1)
    return ''.join(format(v, f'0{width}b') for v,width in zip(q,widths))

q0 = (0,3,0,0,3,2,0)
q1 = (1,3,0,0,3,1,0)
z = (0,0,0,0,0,0,0)
expected = [
    ((0,3,1,3,3,3), q0, q1, True, 1),
    ((0,3,0,0,3,2), q0, z, False, 0),
    ((1,3,0,0,3,1), q1, z, False, 0),
    ((0,0,1,3,1,3), z, q1, False, 0),
    ((0,0,0,0,0,0), z, z, False, 0),
]
for c,x,y,n,p in expected:
    assert sample(c) == (x,y,n,p), (c, sample(c))

counts = Counter()
flags = defaultdict(set)
questions = set()
nontrivial_count = 0
for c in product(range(2),range(4),range(2),range(4),range(4),range(4)):
    x,y,n,p = sample(c)
    counts[x,y,p] += 1
    flags[x,y].add((n,p))
    questions.update((x,y))
    nontrivial_count += n
    # Both endpoints canonical iff the shared seed is nontrivial.
    assert ((x in (q0,q1)) and (y in (q0,q1))) == n

# Def. 5.10 is a genuine output-dependent decider on this fixture.
assert all(len(f) == 1 for f in flags.values())
assert sum(counts.values()) == 1024
assert nontrivial_count == 4
assert all(counts[x,y,p] == counts[y,x,p] for x,y,p in counts)

def extended_answer(q, assignment):
    if q == q0:
        return assignment[0]
    if q == q1:
        return assignment[1]
    return 0

source_extension_loss = sum(
    mass for (x,y,p),mass in counts.items()
    if extended_answer(x,(0,1)) ^ extended_answer(y,(0,1)) != p
)
assert Fraction(source_extension_loss,1024) == Fraction(7,256)

# Verify the exact affine extension identity for all 16 deterministic strategies,
# including suboptimal and nonsynchronous ones. This is a finite consistency
# check of the abstract proof, not a proof against arbitrary quantum strategies.
affine_extensions_checked = 0
for a0,a1,b0,b1 in product(range(2), repeat=4):
    alice, bob = (a0,a1), (b0,b1)
    original_wins = sum((alice[v] ^ bob[w]) == (v ^ w)
                        for v,w in product(range(2), repeat=2))
    repaired_wins = 0
    for (x,y,p),mass in counts.items():
        a,b = extended_answer(x,alice), extended_answer(y,bob)
        canonical = x in (q0,q1) and y in (q0,q1)
        accept = ((a == b) if x == y else ((a ^ b) == p if canonical else True))
        repaired_wins += mass * accept
    rho = Fraction(nontrivial_count,1024)
    assert Fraction(repaired_wins,1024) == 1-rho+rho*Fraction(original_wins,4)
    affine_extensions_checked += 1
certificate = [
    {'x':bits(x),'y':bits(y),'required_xor':p,'mass_numerator':counts[x,y,p],
     'mass_denominator':1024}
    for x,y,p in sorted(counts)
]
summary = {
    'status':'exact-finite-enumeration-passed',
    'source_version':'arXiv:2510.07162v1',
    'interpretation':'intended symmetric block parsing in Definition 5.8',
    'parameters':{'p':1,'m':1,'k':1,'types':[0,1],'neighbors':{'0':'11','1':'11'}},
    'control_seeds':1024,'full_seeds':2048,'data_seed_is_irrelevant':True,
    'nontrivial_control_seeds':nontrivial_count,
    'source_proposed_extension_loss':str(Fraction(source_extension_loss,1024)),
    'repaired_perfect_extension_loss':'0',
    'affine_suboptimal_extensions_checked':affine_extensions_checked,
    'question_count':len(questions),'supported_ordered_pairs':len(counts),
    'q0':bits(q0),'q1':bits(q1),'z':bits(z),
    'witness_pairs':[
        {'x':bits(x),'y':bits(y),'required_xor':p,'mass_numerator':counts[x,y,p],
         'mass_denominator':1024}
        for x,y,p in ((q0,q1,1),(q0,z,0),(q1,z,0),(z,q1,0),(z,z,0))
    ],
    'synchronous_loss_lower_bound':'1/3072',
    'general_commuting_loss_lower_bound':'1/4096',
    'primary_source_sha256':{
        f.name: hashlib.sha256(f.read_bytes()).hexdigest()
        for f in sorted(SOURCES.glob('*.tex'))
    },
}
(HERE / 'FULL_FINITE_GAME.json').write_text(json.dumps(certificate,indent=2)+'\n')
(HERE / 'ENUMERATION_RESULT.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
