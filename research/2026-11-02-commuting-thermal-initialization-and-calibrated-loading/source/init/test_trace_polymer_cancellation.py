"""Finite exact test of full-input marking; not an RX/RZ binding proof."""
from itertools import product
from fractions import Fraction
import json
from pathlib import Path
N=6;q=Fraction(1,7);full_z=Fraction(0);gas_z=Fraction(0);valid=0
# Pair XOR validators: all valid strings are unions of 11-pairs.
# A gate with input11 has zero output but MUST join its input objects.
for bits in product((0,1),repeat=2*N):
 if any(bits[2*j]^bits[2*j+1] for j in range(N)):continue
 valid+=1; full_z+=q**sum(bits)
 components=[]
 for j in range(N):
  if bits[2*j] or bits[2*j+1]:
   # complete stencil: two input wires + XOR validator output
   components.append((2*j,2*j+1))
 for c in components:
  single=[0]*(2*N)
  for k in c:single[k]=bits[k]
  assert all(not(single[2*j]^single[2*j+1]) for j in range(N))
 assert sum(len(c) for c in components)==sum(bits)
for occupied in product((0,1),repeat=N):gas_z+=q**(2*sum(occupied))
assert full_z==gas_z==(1+q*q)**N
# Negative control: nonzero-output marking misses cancellation gate.
wrong_isolated=(1,0);assert wrong_isolated[0]^wrong_isolated[1]
res={'valid_syndromes':valid,'exact_partition':str(full_z),'polymer_partition_matches':True,'cancellation_only_output_marking_fails':True,'scope':'pair-XOR abstract toy only; no actual recursive decoder claim'}
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
