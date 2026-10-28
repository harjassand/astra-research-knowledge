# Primary quaternion fitting import for the on site statistics review

28 October 2026. Reviewer `producer-workspace/audit_count_pilot_fresh`.

I independently read the author-hosted primary paper by Berthold K. P. Horn, *Closed-form solution of absolute orientation using unit quaternions*, JOSA A **4** (1987), 629–642, particularly §1D and the quaternion/rotation and eigenproblem discussion in §§3–4. The scanned reprint identifies volume 4, April 1987, starting page 629. [Primary paper](https://people.csail.mit.edu/bkph/papers/Absolute_Orientation_Scanned.pdf).

The relevant established fact is that proper-rotation fitting can be represented by a unit quaternion and a real symmetric four-by-four maximum-Rayleigh-quotient problem. This review does not attribute a new statistical or quantum-recovery theorem to Horn. I independently expanded the manuscript's chosen SU(2) convention to verify every sign in its K(M), rather than assuming a matching matrix/coordinate convention from the paper.

The gap-free finite rational Jacobi construction and exact-unitary implementation are imported separately from the received known-matrix rounding note, not from an assertion that an exact irrational eigenvector is free. No visual page inspection or PDF byte-hash verification is claimed; the primary read used parsed PDF text. No source calls or random samples occurred.
