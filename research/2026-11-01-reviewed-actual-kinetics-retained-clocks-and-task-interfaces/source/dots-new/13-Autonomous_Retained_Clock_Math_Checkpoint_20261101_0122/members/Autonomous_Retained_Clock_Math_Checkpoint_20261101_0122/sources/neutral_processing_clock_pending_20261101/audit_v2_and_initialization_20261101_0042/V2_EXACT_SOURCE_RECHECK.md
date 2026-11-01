# V2 exact-source adversarial recheck

Date: 2026-11-01 UTC. Verdict: **PASS, conditional analytical theorem.**

Exact reviewed consolidated source:
`PASSIVE_PORT_CLOCK_ROOT_V2.md`, SHA-256
`7696ef6f47f8003749e0b0fbbfdf8c067d1834e398d011c75c8cc075853a5579`.

## Reviewer-role boundary

The V1 audit was independent review of the parent's root. This reviewer then
consolidated the accepted precision corrections into V2. The present receipt is
a fresh exact-source/adversarial recheck by that consolidator, NOT a newly
independent second reviewer of V2. The separate nonequilibrium-initialization
source was newly authored by the parent and independently reviewed here.

## Current proof, not a patch dependency

V2 contains the reference assumptions, energy-space Schur proof, finite-horizon
small-gain proof, certificate normalization, correctly ordered actual-propagator
survival transfer, rate-interval correction, concrete global-process receiving,
strict scope and provenance. Reading V1 plus a patch is not required.

The recheck confirms:

1. Inverse-form finiteness makes the H-orthogonality constraint continuous in
   the energy completion; its kernel is the energy closure of V intersect Q.
   Resolvent approximation proves sigma=a-1/q without Ae or A^-1e in H.
2. x in L2_loc(V), c absolutely continuous, valid terminal H representatives
   and integrated storage are expressly required. A formal skew operator is
   not treated as an existence/domain theorem.
3. The finite-horizon port bound is Y<=sigma C; convolution gains are 1/a in
   L2 and 1/sqrt(2a) pointwise. The final constant (aq-1)/2 is correct.
4. N need not equal M. Both aq-1<=epsilon and k0/a-1<=epsilon are justified.
   Euler's NUMBER is used, with exp(1)>8/3 proving the rational 7/8 bound.
5. u=P_{0,t}^*e, not the wrong-order nonautonomous observable evolution.
   Positivity and same-m contraction justify the initial-law identity; the
   absolute value of a difference of nonnegative terms is bounded by their
   maximum. The rho normalization term is retained for this base theorem.
6. The source-current split is separate: improved B_A is not silently reused
   as an improved B_S. Numerical acquisition is not supplied.
7. The concrete transverse drift is smooth and compactly supported. It has
   zero weighted divergence, preserves h, and is tangent to killing. The
   proper explicit Lyapunov bound earns global SDE nonexplosion. Its common
   form bound earns weak-domain compatibility. Full m preservation is justified
   through the actual common-form density evolution or conservative splitting,
   not finite Gibbs mass or a formal-skew label alone.
8. The example admits arbitrary locally bounded predetermined amplitudes
   without a common amplitude/bandwidth constant in the clock error. It does
   not assert that every unbounded or state-selected processing description
   has such a receiving.
9. Absolute CDF accuracy, exact base initialization and same-m contraction
   are explicit. No processed MFPT, physical preparation/control, arbitrary
   feedback, quantum-fault, iid-restart or executable claim is made. Ordinary
   Schur/passivity/control explanations retain full credit.

## Separately accepted initialization theorem

The unchanged source `NON_EQUILIBRIUM_INITIALIZATION_ROOT.md`, SHA-256
`2accda82d25a2a14f357f2cd8ef28eda0be91a9fb457f31cdb9115e90aa627ff`, separately
passes independent review in `INITIALIZATION_INDEPENDENT_ACCEPTANCE.md`. It
allows a density f in L2(m), supported in A_set, with acquired
D_init=M||f||^2, ONLY when the actual evolution earns the energy inequality for
that initial f. Its bound and TV warning are verified there. This is not a
physical method of acquiring or preparing f and does not establish restart or
mean-time claims.

## Reproducible checks and their limits

The accompanying stdlib-only `check_integrity_and_algebra.py` verifies every
source hash listed in PROVENANCE.json and passes **7,492 exact rational algebra
checks**: finite matrix Schur identities, the two general-initial-storage gain
coefficients, normalization inequalities, D_init identities, and rational
constant reductions. These are regression checks, NOT a finite test presented
as proof of the infinite-dimensional or actual-process theorem.

The original root remains SHA-256
`487a37d2d7d0c15ee756ccda3717bb47c5bd9aa4b1e0bec5ea7201c435950a6d`.
All old audit/background bytes included in the package are unchanged. A full
package SHA256SUMS and a separately generated ZIP/extraction receipt bind the
packaging. No upload is performed.
