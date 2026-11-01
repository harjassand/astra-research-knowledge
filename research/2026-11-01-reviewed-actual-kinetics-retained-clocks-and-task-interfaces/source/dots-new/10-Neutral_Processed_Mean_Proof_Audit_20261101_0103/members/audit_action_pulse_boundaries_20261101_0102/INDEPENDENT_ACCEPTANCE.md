# Optional boundary audit: path-law action and a strict mean-increase pulse

Date: 2026-11-01 UTC. These are separate boundary receipts. They do not change
the independently accepted common-form/sharp-mean receipt or either prior ZIP.

## 1. Girsanov action note — PASS with a precise KL reading

Frozen source `neutral_processing_clock_pending_20261101/PROCESSING_ACTION_COST_ROOT.md`,
SHA-256 `d81b0f3f869d3652407455a7374373d89c82687442cab8953542ad37e4f691ea`.

For the actually received nonexplosive diffusion with constant noise covariance
2 beta^-1 D, D SPD, let Sigma Sigma^T=2 beta^-1 D. The added drift is
s(t)c(x), with c smooth compactly supported and bounded and s predetermined and
locally essentially bounded. The Brownian change-of-drift vector is

  theta=Sigma^-1 s(t)c(X_t),
  ||theta||^2=(beta/2)s(t)^2 c(X_t)^T D^-1 c(X_t).

On every finite horizon its integrated square is bounded by a deterministic
finite constant. Thus Novikov holds under either process and the stochastic
integrals needed to take the controlled expectation have mean zero. With the
SAME initial law, the path-law relative entropy is exactly

  KL(P_controlled[0,T] || P_reference[0,T])
    =(1/2)E_controlled int_0^T ||theta||^2dt
    =(beta/4)E_controlled int_0^T s(t)^2 c^T D^-1 c(X_t)dt.

This statement uses actual nonexplosion, uniqueness/identification of the drift-
changed SDE, constant nondegenerate diffusion and the finite-horizon Novikov
bound; it is not inferred just from a formal generator.

If the common invariant probability pi is the actual initial law, then every
controlled-time marginal is pi. Tonelli yields precisely the factorization
in the source. For a nonzero field in L2(pi), scaling a fixed nonzero schedule
by amplitude A makes this path-law KL grow as A^2. For a conditional-basin
start, the stated spatial-supremum upper bound remains valid, but the stationary
factorization need not hold.

**Controlling interpretation:** “increasingly distinguishable” is supported here
as growth of this path-law RELATIVE ENTROPY. Large KL alone does not establish
TV tending to one or vanishing optimal testing error. In fact a compact-field
example may retain a positive-probability set of finite-horizon trajectories
that never visit its support and are unaffected by amplitude. No stronger TV
limit is needed for the note's intended no-free-control point.

A killed/stopped/censored record is a common measurable map of the full path,
so data processing gives a KL upper bound. Equality for an arbitrary discarded
record does not follow. The source correctly avoids claiming it.

This is mathematical path action, not a measured work or heat in joules,
physical entropy-production receipt, apparatus power certificate, bandwidth
limit or controller implementation. The source's distinction is essential and
correct. It is entirely compatible with an amplitude-independent clock error.

## 2. Fixed-amplitude predetermined pulse — PASS for the core boundary

Frozen sources:

- `test_processed_clock_lifetime_20261101_0043/TIME_DEPENDENT_MIXING_CAN_STRICTLY_INCREASE_MEAN.md`,
  SHA-256 `c6d797b8a9a8d6ac9ca9ed4bff8afa52a9d0f4120cb291bcca8bd71874361484`.
- `test_processed_clock_lifetime_20261101_0043/PULSE_FIRST_VARIATION_ADDENDUM.md`,
  SHA-256 `e78fa0dd3e902410619abd1e1d812c592865498117467ff77459fac744517289`.

The displayed symmetric positive killed generator has row killing rates
(1,0,100), valid nonnegative live transition rates, and uniform probability
m on three states. Direct multiplication verifies

  v=A^-1 1=(1,13/25,1/50),
  Q=<1,v>_m=77/150.

For u(t)=exp(-tA)1, u'(0)=-(1,0,100), so
u_1(t)-u_0(t)>0 for every sufficiently small positive t. The additional
symmetric conservative C mixes states 0 and 1, is positive semidefinite and
annihilates h=1 on both sides. It preserves the same m.

The intervention calculation is exact: exp(-bC) exchanges the two coordinates
with fraction alpha=(1-exp(-2b))/2. The change in future mean is
alpha(v0-v1)(u1-u0)/3>0. Its finite-rate approximation is valid in finite
dimension; all rates are finite in every member.

More decisively, the addendum avoids any large-rate limit. For fixed R>0 and
a pulse A+RC of duration epsilon at the predetermined time t,

  J(epsilon)=int_0^t <1,u(s)>ds
    +int_0^epsilon <1,exp[-s(A+RC)]u(t)>ds
    +<v,exp[-epsilon(A+RC)]u(t)>.

Differentiating at zero is legitimate in finite dimension. Since Av=1 and A
is self-adjoint,

  J'(0)=<1,u(t)>-<v,(A+RC)u(t)>
        =-R<v,Cu(t)>
        =R(v0-v1)(u1-u0)/3>0.

Also J(0)=Q by splitting the reference occupation integral. Thus sufficiently
short FIXED finite-amplitude pulses strictly increase actual mean above Q.
The full reference A and Q are fixed, the added form is dissipative, and the
schedule is predetermined. There is no density injection, state feedback,
instantaneous intervention requirement or infinite-rate premise.

This disproves a blanket nonautonomous constant-one comparison; it does NOT
contradict the new constant-four principle or normalized near-clock limit.
The “rare-gadget near-clock embedding” mentioned in the addendum refers to a
separate README construction and is NOT independently accepted by this receipt;
the direct three-state strict-increase boundary is sufficient here.

## 3. Evidence and exclusions

Sources were read and left unchanged. The finite-state calculations above are
exact; no simulation is substituted for proof. No extra helper, upload,
external contact, denied read or permission escalation was used. This optional
receipt is separate from the main mean audit and prior proof archives.
