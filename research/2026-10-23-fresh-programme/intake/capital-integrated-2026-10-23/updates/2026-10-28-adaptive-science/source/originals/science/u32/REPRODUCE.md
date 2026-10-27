# Reproduction

All paths below are inside the owned u32 directory. Frozen Astra sources
were read at commit 2cba6a60646bb52982233c40d7ae941b266f0d5c; no active
checkout was edited or built. Extra scientific source copies and their
hashes are in ADDITIONAL_SOURCES.json and source_counts/.

The environment used /opt/homebrew/bin/python3 with NumPy. No dependency
installation, purchases, apparatus, or remote experiment was performed.
No memory, chats, other trajectories, dispatchers or admissions were
consulted. The sole helper was fresh GPT-6.1 Sol/Max, with no descendants.

From this directory:

```sh
python3 exact_certificate.py
python3 residual_validation.py
python3 compare_variants.py
python3 source_simplex_scan.py
python3 overcomplete_fixture.py
python3 coherent_diagnostic.py
python3 score_pattern.py
python3 verify_replay.py
```

The first three learners read integer counts only. The original frozen
qubit learner is run only from its owned copied source. The last two
diagnostics concern mathematical representation and private post-acquisition
evaluation, not confidence certification. score.py additionally evaluates
finite full transcript trees and may take tens of seconds; it never feeds
its plant evaluation back to a learner.

To reconstruct the stored synthetic batches exactly, rather than obtain
new independent observations:

```sh
python3 generate_counts.py
python3 generate_counts.py --shots 500000 --seed 327687953 --output residual_counts.json
```

The first dataset has 7M resets/14M native interventions; the second has
3.5M/7M. Their default seeds are recorded in the script. Replaying the same
seed is a deterministic transport check. Calling it another independent
experiment would be incorrect. Private plant matrices enter generation and
post-acquisition scorers only. Learners must never import plant.py; the
replay verifier enforces that import boundary dynamically.

The rational primary certificate proves inequalities conditional on its
stated count event. It is internally audited in helper/AUDIT.md, with a
separate exact implementation under helper/replay/. The overcomplete
fixture verifies exact intertwining, normalization and the three-state
trace obstruction; it does not acquire those instruments from observations.
The coherent finite diagnostic is illustrative; its all-horizon statement
is proved in COHERENT_OBSTRUCTION.md rather than inferred from a finite run.

External primary-source checks used the papers linked in
COHERENT_OBSTRUCTION.md. Firecrawl returned exhausted credits once, so no
retry was made; direct primary web reads supplied the literature check.
The invariant-polyhedral/CP realization framework and quantum/classical
separation are established prior machinery. No priority claim follows from
the present source check.

The manifest is a transport record, not evidence of mathematical correctness,
external validation, novelty, or physical performance. No formal goal,
automation, sidebar chat, purchase, or shared scientific edit was created.
