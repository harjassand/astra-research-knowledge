# Separate audit: bounded-rate local syndrome-conditioned Pauli faults

Date: 16 October 2026. This is the additional corollary requested after the
original audit. It does not replace or enlarge the verdict in `REPORT.md`.

## Verdict

**Yes, the proposed structured-noise extension follows from the same base
classical guard/cluster/torus argument, with fixed enlarged constants.** The
additional quantum algebra, Poisson coupling, envelope domination and decoder
geometry are proved below. No further obstruction was found under the precise
conditions stated here.

There is one tempting invalid intermediate claim: the actual two CSS sector
marginals need not remain autonomous Markov processes when a fault rate
depends on both syndromes. That claim is unnecessary. Independent proposal
streams, with every proposal treated as an envelope birth regardless of its
acceptance, restore an appropriate *dominating* primitive process. This is
the essential distinction from reusing the old marginal-identification proof.

This is a conditional corollary of the original classical argument. It is
not an independent certification of the named cluster theorem, its LSS
application, or the stopped finite-torus replay. Their audit status remains
exactly as recorded in `REPORT.md`.

## 1. Precise extension hypotheses

Retain the exact ideal primal and dual sweep correction terms, at rate
`kappa`. Add distinct Lindblad dissipators

    L_fault = sum_a D[J_a],        J_a=Q_a f_a(S_local).                    (E1)

Assume:

* `Q_a` is a fixed physical Pauli string, not a coherent sum of strings.
* `f_a(S_local)` is a scalar function of commuting toric-code stabilizers
  in a fixed neighborhood. It is scalar on each entire joint syndrome
  eigenspace. An arbitrary operator commuting with the stabilizers would
  be insufficient: it could act on the logical degeneracy.
* Each term has a deterministic owner fine cell `x(a)`. The Pauli support
  and the conditioning support have a common range bound independent of
  `L`. In each sector, the vertex support of the syndrome boundary of
  `Q_a` lies in an infinity ball `B_ell(x(a))`, after absorbing the fixed
  primal/dual coordinate offset into the integer `ell`.
* Write `M_a=||f_a||_infinity^2`. For every owner cell,

      sum_(a:x(a)=x) M_a <= nu.                                         (E2)

  The finite set of term types and their range are fixed independently of
  system size. Rates and functions are constant in time for a time-independent
  memory theorem.
* Initialization and readout remain exactly those of the original theorem.
  Leakage, coherent Hamiltonian faults outside the stabilizer algebra,
  noncommuting conditioning operators and noisy readout are not included.

The norm in (E2) is the full operator/spectral norm, so it is a valid bound
on every allowed syndrome's rate. If the original independent Pauli faults
are also retained, their rates consume the same budget. A conservative
per-cell total is

    nu_total = nu_added + 6(lambda_X+lambda_Y+lambda_Z).                   (E3)

The smallness condition below applies to the *combined* total. One cannot
add a new budget while silently keeping an old noise bound already at its
entire allowed threshold.

## 2. Exact joint trajectory and uniformization

The general proof in `REPORT.md`, equations (1)–(7), already covers (E1).
On a Pauli trajectory with joint syndrome `s`, a jump of type `a` occurs at
rate

    r_a(s)=|f_a(s)|^2 <= M_a,                                          (E4)

and multiplies by `Q_a`; its scalar complex amplitude affects only a global
branch phase. No-jump factors remain scalar on the complete logical/reference
state. Thus all proposal and acceptance probabilities can be chosen without
knowing the encoded input.

Take independent rate-`M_a` Poisson proposal streams, independent of the
ideal sweep clocks, and give every proposal an independent uniform mark
`U` in `[0,1]`. Accept type `a` exactly when

    U <= r_a(s_pre)/M_a,                                               (E5)

omitting zero-rate terms. Standard infinitesimal conditioning, or the finite
generator calculation `M_a*(r_a/M_a)=r_a`, shows that the accepted process
has exactly the required joint CTMC generator. Acceptance is allowed to
depend on both current CSS syndromes. Accepted proposals need not form
independent or state-independent Poisson processes; that is never used.

An equivalent, stronger domination is particularly convenient. At each fine
cell use one independent rate-`nu` Poisson stream. At a mark choose type `a`
with probability `M_a/nu` and a null type with the remaining probability,
then apply (E5). Poisson splitting recovers all the independent proposal
streams and a padding stream. On **every** cell mark, regardless of type or
acceptance, birth the entire ball `B_ell(x)` in both sector envelopes.

This padded-ball envelope has identical primitive rate and birth shape at
every fine cell, even if the actual fault rates or types are spatially
inhomogeneous. It avoids any additional homogeneity issue in the infinite
comparison. The physical storage model acquires no actual proposal register
or measurement; this is an analysis coupling.

## 3. Pathwise domination survives arbitrary local Pauli bursts

For one sector let a Pauli fault contribute the fixed local 2-chain `F_a`,
and let `W_a` be the vertex support of `partial F_a`. If the current syndrome
is `s`, then

    supp_vertices(s+partial F_a)
        subset supp_vertices(s) union W_a.                              (E6)

This set inclusion is deterministic, independent of acceptance, rate,
number of written faces, disconnected local pieces, or the other CSS
syndrome. Therefore an envelope which sets all of `W_a` occupied on every
proposal dominates both the accepted and rejected possibilities. The padded
ball construction is an even larger birth map.

Between proposals, the ideal sweep clocks use the same old-state AND/OR
envelope map as before. Its pathwise correction argument depends only on
cycle parity and the sweep update, not on how the current cycle was created.
Every Pauli fault boundary is still a cycle by `partial^2=0`. The original
induction therefore gives domination of each actual sector trajectory by
its ball-birth envelope at all times.

The two actual sectors may be correlated and non-Markov when viewed
separately. The two dominating envelopes may also share all ball births.
Neither fact obstructs an individual envelope tail or a union bound.

The conditioning support cannot create a new causal propagation mechanism
for this envelope. The envelope ignores the acceptance decision completely.
Each proposed birth has a predetermined bounded output region, even if
the actual acceptance reads distant values inside the allowed local
conditioning neighborhood. It is erroneous to put accepted-jump events
instead of proposal events into fresh primitive bad flags.

## 4. Changes to the literal block flags

For the exact original definitions see
`research/2026-10-15-autonomous-frontier-v2/sweep/MONOTONE_ENVELOPE.md`,
lines 81–114; the canonical summary is C, lines 92–115.

Keep the forcing map `phi`, its radius `R`, the slab duration
`Delta=C b/kappa`, the slow-clock certificates and the fast-clock flag.
Let `G_z` be the old radius-`R+2` coarse primitive guard, whose fine side
length is `(2R+5)b`.

Replace the physical-single-face birth flag by:

    at least one cell proposal during the slab whose B_ell(x)
    meets G_z.                                                         (E7)

Its owner cell lies in the enlarged fine guard. A conservative count is

    N_guard <= [ (2R+5)b + 2ell + 2 ]^4,
    P(E7) <= nu Delta N_guard.                                         (E8)

The term `+2` only absorbs integer coordinate and primal/dual conventions.
The exact numerical padding is unimportant; the expression is uniform in
`L` and is finite for the fixed chosen `b,ell`.

The slow certificate is unchanged because the good event excludes births
in its required guard. The fast causal flag is also unchanged: the
old-state envelope clock map still has at most 35 predecessor choices per
step and displacement at most two fine units. A ball birth inside the
guard is excluded by (E7); any exterior-born occupied source must enter
through the same ordered clock dependency chain. The ball's possible
overlap with the guard is already accounted for by enlarging the owner
guard in (E8).

The resulting flags depend only on fresh ideal clock increments and fresh
cell-proposal increments in a fixed enlarged guard. They do not depend on
the actual state, acceptance marks, encoded input, or earlier slab history.
Their fields remain independent across time slabs and finite-range dependent
within a slab. With the padded-ball construction their law is also
translation invariant in infinite volume.

Their marginal obeys the direct replacement of canonical (B):

    delta <= 2b^4 exp(((s+4)log(8)-C/2)b)
             + b^4 (35 kappa Delta)^m/m!
             + nu Delta [ (2R+5)b+2ell+2 ]^4,
    m=floor(Rb/2).                                                     (E9)

This is the required quantitative alteration. There is no multiplicative
factor for the number of jump types once their norm-squared maxima have
already been summed in (E2).

### Noncircular parameter choice

Fix the physical range `ell`. Choose `s,C,R` as in the base argument. Demand
`b>=max(4,ell+1)` and reserve a conservative coarse primitive radius
`D=R+5`; this bounds all enlarged owner guards for every such `b`.

Choose the iid-death target and the LSS primitive threshold `delta_*` using
this fixed dependence range and the unchanged attractive eroder `phi`.
Then choose a fixed sufficiently large `b` to make each clock term in (E9)
at most `delta_*/3`, and finally choose

    nu <= kappa delta_*
          / [3 C b ((2R+5)b+2ell+2)^4].                                (E10)

The birth term is then at most `delta_*/3`. This is a strictly positive
threshold depending on the fixed range and base comparison parameters,
independent of `L`, `T`, and the logical/reference state. Fixing `D` before
choosing `b` prevents a hidden dependence-range/threshold circularity.

No usable numerical threshold follows without quantitative constants from
the imported classical results. As in the base proof, the resulting
constants can be extremely poor.

## 5. Whole-slab cover, stopped torus replay, and decoder geometry

The whole-slab cover uses only the same no-birth/no-fast-chain good event,
so its proof remains valid. A transient infected target has either a local
initial infected ancestor or a bad flag in that slab. Accepted state-dependent
faults introduce no additional envelope dependency because all their
proposals were already replaced by state-independent births.

In the stopped torus replay, enlarge the fixed anchor patch by the new
primitive radius `D`. Copy the cell proposal streams and ideal correction
clocks in that fixed injective patch and extend them independently outside.
The copied proposal streams have their usual iid rate-`nu` law. The
zero-witness parent rule of the coarse `phi` is unchanged. Thus any valid
base replay/infinite-cluster transfer continues to apply with these enlarged
fixed constants. One still does not assert product domination directly
on an arbitrary finite torus.

For a proposed/accepted fault, let `d` bound the coordinate side length of
the local 2-chain's entire vertex support, in both sectors. With pre-event
component diameter `<r=L/32`, every changed old or new component and its
decoder filling is contained in the common `r`-neighborhood of that event
box, of side at most

    2r+d.                                                              (E11)

For fixed `d` and sufficiently large `L`, this is `<rho=L/8`. The residual
`F+D(s)+D(s+partial F)` is therefore a closed 2-chain in a contractible
box and is a stabilizer boundary. This is the original deterministic local
homology argument with `1` replaced by `d`. A fixed-range fault with zero
syndrome is also a boundary inside its local box; it cannot silently enact
a toric logical membrane for large `L`.

Thus the same fixed ideal decoder continues to work before a macroscopic
syndrome escape. It still covers all six logical qubits. Correlated
multi-face/Y events are not split into artificial independent faults.

## 6. Conditional mathematical consequence and actual limitations

Assuming the base local block forcing, infinite iid cluster tail and stopped
finite-torus transfer are correct with fixed enlarged guards, (E9)–(E11)
give constants `b,epsilon,A,c>0`, depending on the fixed fault range but
independent of `L=bM,T`, such that for `nu_total<=epsilon kappa`,

    ||Dec_L exp(T(L_sweep+L_fault)) Enc_L-id||_diamond
       <= min(2, A L^4(1+kappa T) exp(-cL)).                             (E12)

The identity-component and diamond argument is the one independently proved
in `REPORT.md`. Exact independent single-face Pauli noise is a special case
of this budgeted fault class. Local spatially correlated fault bursts and
arbitrary syndrome-conditioned acceptance are included; arbitrary temporal
noise correlations and arbitrary coherent perturbations are not.

Important boundaries:

* The actual marginal sector chain need not close. The envelope comparison,
  rather than the old exact marginal-identification assertion, carries the
  proof. A two-qubit countermodel to marginal closure is in `REPORT.md`.
* The range bound must be uniform in `L`. A jump supported on a whole logical
  membrane would violate the decoder box argument even at tiny rate.
* The operator functions must be scalar functions of stabilizers; conditioning
  on logical operators or general operators in the commutant can measure
  the stored information. The logical-sensitive countermodel in `REPORT.md`
  explains this distinction.
* Distinct dissipators may be summed incoherently as in (E1). A coherent sum
  of different Pauli amplitudes within one jump is not covered.
* The budget is the sum of maxima `sum ||f_a||^2`, not the maximum of an
  accepted rate averaged over a presumed state. Otherwise fresh uniform
  proposal domination is not established.
* A time-independent generator and independent primitive proposals are
  sufficient. More general external/adversarial time correlations would
  require a fresh block-dependence argument.
* The storage register remains `6L^4` qubits. The added terms use a fixed
  number and fixed support per cell under the hypotheses; their physical
  fabrication, conditioning, calibration, reservoir/reset and energy
  interfaces remain unacquired. This extension is not a robustness theorem
  for arbitrary implementation errors.

I found no obstruction beyond these explicit structured-model conditions,
the fixed enlarged guard/rate constants, event diameter, and the unchanged
base classical proof dependencies.

## 7. Exact corroboration

`check_extension_exact.py` verifies a genuinely non-projector complex
stabilizer function

    f(sx,sz)=(1+sx+2sz+i(1+sz))/4

for a conditional multi-qubit `Y_1 Y_3` jump on a reference-entangled CSS
code. Its squared rates are `5/4,0,1/2,1/4`; one rate-`5/4` proposal stream
has exact acceptance probabilities `1,0,2/5,1/5`. It checks 192
denominator-cleared matrix identities over 64 Pauli labels, including
the no-jump rate operator and the exact dissipator.

The script also checks all 8,192 accepted/rejected combinations formed from
64 initial local 2-chains and 64 correlated local fault chains on the six
positive plaquette orientations at a 4D vertex. Proposal boundary births
dominate both possibilities exactly. The general inclusion (E6) is the
proof; enumeration is finite corroboration only.

Run:

    python3 research/2026-10-16-adversarial-quantum-memory/trajectory/check_extension_exact.py

`EXTENSION_CHECKS.json` records the results and SHA-256 pins of the canonical
proof and two base construction companions. These checks establish no
asymptotic cluster tail or physical noise threshold.
