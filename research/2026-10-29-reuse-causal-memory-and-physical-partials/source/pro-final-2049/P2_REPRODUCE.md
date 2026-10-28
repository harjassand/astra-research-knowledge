# Reproducing the saved constructions

The mathematical claims, actual reviews and scope are indexed in `README.md`. These commands reproduce executable evidence; they do not acquire physical controls or certify a device. Python 3.12 was used. Exact scalar and pulse certificates use the standard library; the general passive compiler also uses NumPy and SciPy. The direct-record script has an optional SciPy integral, labelled as a floating diagnostic.

Several programs write results beside their source. Preserve the reviewed originals by making a temporary working copy first:

```python
from pathlib import Path
import shutil
import tempfile

source = Path('producer-workspace/p2_mediator')
copy = Path(tempfile.mkdtemp(prefix='p2_mediator_replay_')) / 'p2_mediator'
shutil.copytree(source, copy, ignore=shutil.ignore_patterns('__pycache__'))
print(copy)
```

From the printed copy directory, run the particular check required:

```bash
python causal/passive_streaming.py
python reviews/causal_review/exact_pair_audit.py
python schur/certify_angular_cell.py
python reviews/pulse_review/independent_audit.py
python eraser/two_bin_checks.py
python reviews/erasure_challenge/no_memory_checks.py
python star/star_checks.py
python reviews/erasure_challenge/star_loss_gram_checks.py
```

These checks were already executed for the saved tranche, with actual independent replays recorded in the reviews. Optional repetition is not additional scientific validation. Compare certificate fields rather than elapsed time, Python-version strings or machine-specific paths. The compiler's numerical residuals are diagnostics; its exact rational feature algebra and analytic proof supply separate evidence. Its floating rank tolerance is not a physical calibration certificate.

The energy-restricted corollary and adaptive necessity are analytic results with separately saved independent reviews. They do not depend on a missing numerical run. The unrounded star arithmetic attempt is a preserved failed representation and should not be used in place of `star/star_checks.py`. The larger analytic pulse compiler has a different, narrower review status; see the result map before using it.

`MANIFEST.json` binds the retained proof, code, data, source acquisitions and review files by SHA-256. It excludes itself and generated Python bytecode. It is an integrity inventory, not a scientific review or a claim that every saved exploration is correct.
