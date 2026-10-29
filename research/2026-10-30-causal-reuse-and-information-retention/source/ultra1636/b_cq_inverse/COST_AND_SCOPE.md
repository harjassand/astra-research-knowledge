# Decision and full cost boundary

The assigned equal-reference question is answered positively by a general
theorem: for any two linearly independent pure preparations with overlap
`s`, the minimum retained Umegaki fraction, after any finite quantum
reference, is exactly `1-s^2`. For the fixed `|0>,|+>` channel the reverse
coefficient is exactly2. The actual proof is analytical, applies to all
reference dimensions, and does not supply a finite dimension cutoff.

The ordinary unambiguous-discrimination comparator pays an explicit
heralded inverse with success `1-s`, yielding reverse bound
`1/(1-s)`. The improved information comparison does not implement a
better heralded inverse. BKM integration and inverse congruence are
ordinary tools. Historical priority of the resulting exact minimum
retention formula is UNKNOWN; narrow primary retrieval did not settle
that question, and no absence argument is made.

The unequal-reference, subtracted conditional comparison is NOT solved
by this theorem. It remains bounded between2 and `2+sqrt(2)` for the
fixed pair using the inherited filter. Parent independently owns the
attempt to strengthen the BKM slack by the reference term. This scope
distinction is load-bearing, not a numerical precision qualification.

## Work actually executed

1. No channel/source acquisition, quantum state simulation, SDP, global
   optimization, or reference-dimension search was performed.
2. `derive_resolvent.py` checks the complex Hermitian two-index trace
   identity, its nonnegative scalar coefficient identity, and the Gram
   inverse/change of variable symbolically. The analytical proof sums
   the same per-index relation at arbitrary finite size. Its first
   receipt is `EXACT_RESULT.json`; 0.126825s after imports, about0.715s
   process wall time. The consumer was executed once. Its proof metadata
   binds the pre-amendment proof; `EXECUTION_BINDING.json` records the
   later explanatory regularization change. The consumer's mathematical
   computation does not depend on the proof text.
3. `conditional_probe.py` computes the true input/output/reference BKM
   quadratic forms on a complete seven-real-dimensional trace-zero
   tangent space for a two-dimensional reference. It evaluates three
   points on the SINGLE fixed-angle continuation
   `A=diag(1,e),B=R(pi/4)A R*`. A second command reuses those functions on
   the coalescing-angle continuation `tan(theta)=sqrt(e)`. Six proposal
   points total, always the SAME prescribed `0,+` channel. Arithmetic
   costs after imports were0.010874s and0.013899s; process wall times
   were about0.317s and0.348s. These failed
   to produce a conditional reverse ratio above2. Neither result proves
   a conditional bound. All arithmetic is untrusted binary64 and no
   exact finite-state witness was claimed.

Primary read-only research was used for ordinary reverse-DPI/BKM and
unambiguous-discrimination comparators. Several narrow web searches
were unproductive; their cost and lack of a priority conclusion are
retained. An initial overlarge retrieval output was truncated and was
not treated as source knowledge. C's full AIRR v3 investigation is
separate; this packet does not claim to have duplicated it.

All premises here are mathematical states/channels supplied in the
question. Physical preparation, noise calibration, advantage over an
actual experimental inference protocol, and novelty clearance are
NOT_ACQUIRED. No physical/external action occurred.
