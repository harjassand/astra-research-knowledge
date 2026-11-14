# Two-macroscopic-droplet entrance-current exclusion

Read THEOREM.md for the full statement, proof, precise source clock, and excluded families. Run `python certify.py` to reproduce exact rational scalar certificates.

This extension depends on the thermal-core capacity theorem in the previously prepared bulk-free capacity package. It is a current-coverage result, not physical growth or a full mean-transition predictor. Internally derived; independent verification remains necessary.

Checked governing source:
https://github.com/harjassand/astra-research-knowledge/blob/main/research/2026-11-04-ordered-ising-current-and-full-residence/source/P2_DIRECT_CURRENT_COMPLETE_RETURN.txt

Primary comparison:
https://arxiv.org/abs/1809.07044 (GMV, especially Lemma4.5).

The extension at the end of THEOREM.md covers pure disjoint mergers with largest precursor≤4R², by combining two explicit families. This is an area-based current exclusion, not a thermal-supercriticality or growth theorem. The script also retains an optional weaker collective witness calculation; the refined area-cut formula is the intended stronger merger conclusion.
