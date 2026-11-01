# Author failure history

The first copied wrapper suite stopped at its expected-refusal mutation named `task`. The newly relaxed small test task uses KS tolerance 1/2, while the inherited corruption also wrote 1/2. Thus the purported mutation changed no bytes, and the verifier correctly accepted the unchanged proof/task. The exact initial test source is preserved in `check_before_task_mutation_fix.py`; the corruption was changed to 1/3. No producer, proof, numerical output or admitted endpoint was changed. The failed assertion was `unexpected admission: strict all-time model/task/proof receiving: task`. No permission denial or uncertain operation occurred.

The first final-freeze consistency command stopped before creating a manifest
because it compared a two-field calculated hash/size dictionary against an old
manifest entry containing an additional `role` field. Actual proof/code hashes
were unchanged. The check was corrected to compare the explicit bytes and
SHA256 fields, retaining the old metadata rather than treating extra metadata
as a source mismatch. No test, source or numerical certificate changed.
