Nucleation_Block_Transport_20261107

The full two-dimensional all-minus-to-nonnegative-magnetization predictor is
UNRESOLVED and remains the governing endpoint.

Read RESEARCH_REPORT.txt for the complete construction, proofs, costs and
limitations. The positive operation is an exact conditional law on a supplied
ordered region; the exterior is frozen and not acquired. The global comparison
and direct-simulation obstruction retain the actual physical target and clocks.

Files
  RESEARCH_REPORT.txt       Scientific report and proofs
  block_transport.py       Exact integer conditional law and sampling operations
  validate_transport.py    Bounded, reproducible finite checks
  VALIDATION.json          Exact check records and observed timings
  ENDPOINT.json            Full retained endpoint and missing central operation
  FAILURE_OBJECTS.json     Scoped microscopic failure family
  SOURCE_SCOPE.json        Primary credits and governing source pin
  PREDECESSORS.json        Ten earlier archives, preserved byte-for-byte
  SHA256_MANIFEST.json     Hashes of the other files in this archive

The code uses only the Python standard library. To reproduce the finite checks,
run this command from the extracted directory:

  python3 validate_transport.py

This rewrites VALIDATION.json with the new observed timings. It does not contact
the network or run a physical experiment. No additional environment is needed.
The seeded PRNG is for reproducibility only; the sampling theorem explicitly
assumes independent fair input bits. The exact sampler has polynomial expected
work; the fixed-bit sampler has a stated total-variation error and fixed budget.

Example of the conditional operation:

  from fractions import Fraction
  from random import Random
  from block_transport import periodic_strip, FrontierLaw, precision_for_tv

  region = periodic_strip(16, 3, [0]*16, [1]*16,
                          Fraction(1,4096), Fraction(255,256))
  law = FrontierLaw(region, magnetization=True)
  normalizer = law.normalizer
  slice_probability = law.count_probability([24])
  bits = precision_for_tv(region.m, Fraction(1,10**8))
  sample = law.sample(Random(1722).getrandbits, bits, plus_count=24)

This example conditions on exactly 24 plus spins in a 48-site frozen-exterior
strip. It is not a critical-droplet acquisition or a nucleation trajectory.
In particular, a large number of configurations represented by the recurrence
does not establish a larger physical prediction capability.

All predecessor scopes and source/resource holds are retained. No new role,
worker, descendant, infrastructure, hardware, spending, outreach or physical
experiment was used; no peer branch was contacted.
