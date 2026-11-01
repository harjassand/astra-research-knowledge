# Retained-state alternating clocks: author candidate

The new result concerns the **same continuing original reversible diffusion**,
started once from its exact full Gibbs|A law. It does not reset hidden angular
state. It earns a whole finite sampled record and a separately scoped
continuous hysteretic time-jitter coupling, then a uniform finite-horizon
renewal limit. Independent review of this new construction remains pending.

Read in order:

1. `GLOBAL_ODD_MODE_AND_RENEWAL_CANDIDATE.md`: global inverse current, vector
   mode, history conditioning, stationary count identity and renewal join.
2. `FINITE_RATE_AND_SHARP_VECTOR_COROLLARY.md`: accepted sharper baseline
   vector plus exact rational reference-rate receiving.
3. `NO_GLOBAL_GAP_NOTE.md`: the original global spectral gap really is zero.
4. `CONCRETE_COMMITTOR_DOMAIN_JOIN.md`: the concrete equilibrium-potential,
   local boundary finite variation and actual stationary augmentation join.
5. `COSTS_PRIORS_AND_BOUNDARIES.md`: actual costs, ordinary priors, finite
   limitations, physical/nonautonomous exclusions and honest refusals.

The initial author suite passed 2,503 checks. From this directory,
`python receive_clock.py` regenerates the two actual
513D production records; `python check.py` checks the full author suite and
recomputes both records, including the saved stronger-target refusals. Python
stdlib suffices for receiving; only author symbolic tests additionally use
SymPy. Source-relative dependencies in `DEPENDENCIES.json` must remain present
at their declared hashes. Existing accepted proofs are not modified.

For a small extracted receiving replay:

```python
import json
import receive_clock as c
raw=json.load(open('small_raw_fixture.json'))
cert=json.load(open('small_certificate.json'))
print(c.verify(raw,cert,**c.external_from_record(cert)))
```

The producer/receiver takes explicit exact task fractions, strict integer
budgets, and the complete raw model. It returns UNKNOWN on a failed conjunction
or exhausted budget, not a smaller claimed error. Time-jitter coupling is not
continuous timestamp total variation. The finite 513D record bound is about
14%, and the one-horizon continuous coupling failure bound about 41%; the
structural asymptotic theorem is stronger than those modest finite numbers.
