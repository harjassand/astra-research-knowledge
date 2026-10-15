# Independent quantum-trajectory and fixed-decoder audit

Date: 16 October 2026. Investigator: trajectory worker, initial Sol 1.

## Verdict and precise scope

**The exact Lindblad-to-joint-Pauli-trajectory reduction is valid.** Below is
an independent proof for arbitrary encoded density operators, including
arbitrary reference entanglement. It includes the no-jump terms, simultaneous
two-face conditional corrections, X/Z interleaving and constant-rate Y faults.
The fixed syndrome recovery can be defined as a CPTP map on the entire physical
Hilbert space. Its effective channel is a six-qubit Pauli channel, and its
unhalved diamond distance from identity is exactly twice the probability of a
nonidentity final logical Pauli. A bound on the probability of any earlier
decoded-homology change is a sufficient upper bound for that probability.

I found no invalid implication in that quantum reduction under its stated
hypotheses. **This report does not independently prove the probabilistic
continual-noise tail in canonical proof sections 1–4.** The exponential bound
in (T) depends on those sections. No worker agreement, numerical experiment,
or finite incidence check is used as a substitute for them.

The exact checks accompanying this report are finite corroboration. The proof
below, rather than those checks, establishes the algebraic lemma. The six
countermodels below falsify proposed enlargements of the hypotheses; none is
a counterexample to the exact model.

## Audited inputs and source locations

Paths below are relative to `/Users/harjas/Documents/ChatGPT/ultra`.

* **C:** `research/2026-10-15-autonomous-frontier-v2/THEOREM_AND_PROOF.md`.
  Read in full. Model and rates: lines 11–38; channel claim: 40–53;
  deterministic homology argument: 164–178; quantum transfer: 180–187;
  resources and implementation boundary: 189–210.
* **G:** `research/2026-10-15-autonomous-frontier-v2/sweep/GENERATOR_AND_PAULI_TRAJECTORIES.md`.
  Code and jumps: lines 7–32; trajectory argument: 38–56; scope: 58–64.
* **R:** `research/2026-10-15-autonomous-frontier-v2/lead/READOUT_CONSTRUCTION.md`.
  Cubical prism contraction: lines 7–25; complexity and fallback: 27–44.
* **H:** `research/2026-10-15-autonomous-frontier-v2/lead/LOCAL_DECODER_HAZARD.md`.
  Fixed filling and local stability: lines 14–47; hazard formulation: 51–72.
* **S:** `research/2026-10-15-new-foundational-power/s5/MECHANISM_AND_PROOF.md`.
  Earlier exact model: lines 95–118. Earlier continual-noise obligations:
  lines 140–148. It is not used to infer the newer lifetime theorem.
* **V:** `research/2026-10-15-new-foundational-power/l4/REVIEW.md`.
  Read as requested, including lines 49–79. Its conclusions are not premises
  of this reconstruction.

SHA-256 pins of these exact files are in `EXACT_CHECKS.json`. The independent
derivation uses the displayed generator, stabilizer algebra, finite-dimensional
ODE uniqueness, cubical chain contraction, and the triangle inequality for
channels. It does not import a single-qubit-only quantum reduction theorem.

For a current primary-source boundary check, I opened
[Drechsler–Oreg–Aharonov v1](https://arxiv.org/html/2610.05589v1): its Definition
2.22, equation (31), has jumps `P_i f`, with a one-site Pauli; Definition 2.29
uses single-bit induced transitions. Its Section 4.6 derives logical Pauli
structure in its stated setting. The elementary proof here directly permits
Pauli strings and treats all six toric logical qubits jointly. These are
different proof scopes. The sweep predecessor was checked at its
[primary arXiv page](https://arxiv.org/abs/1809.10145). No originality claim is
made here.

## 1. General invariant-family lemma, reconstructed

Let `S` be an abelian Pauli stabilizer group on `n` qubits, excluding `-I`.
Let `P_0` be its code projector and `V` a fixed isometry from the full `k`-qubit
logical space to that code space. Index the nonzero joint syndrome projectors
by `P_s`. Their eigenspaces include the entire logical degeneracy.

For a physical Pauli label `e` modulo scalar phase, choose a representative
`E_e`. If the encoded/reference input is `rho_LR`, define

    rho_e = (E_e V tensor I_R) rho_LR (V^dagger E_e^dagger tensor I_R).       (1)

The syndrome `s(e)` depends only on commutation of `E_e` with stabilizers, so

    (P_s tensor I_R) rho_e = rho_e (P_s tensor I_R)
                           = 1_{s=s(e)} rho_e.                            (2)

This holds for every logical operator `rho_LR`, including off-diagonal logical
matrix elements and reference entanglement. It does not require a computational
basis codeword or a maximally mixed logical input.

Consider the slightly more general exact generator

    L(rho) = -i[H(S),rho] + sum_alpha D[Q_alpha f_alpha(S)](rho),            (3)

where each `Q_alpha` is a fixed Pauli string, `f_alpha(S)` is a function of
the commuting stabilizers, and `H(S)` is a Hermitian function of them. Thus
`f_alpha(S) P_s = f_alpha(s) P_s`; the value is a scalar on the *whole*
syndrome space. Write `q_alpha` for the Pauli label of `Q_alpha` and
`r_alpha(s)=|f_alpha(s)|^2`.

With the identity on `R` suppressed, direct multiplication gives

    J_alpha rho_e J_alpha^dagger
        = r_alpha(s(e)) Q_alpha rho_e Q_alpha^dagger,
    J_alpha^dagger J_alpha rho_e
        = rho_e J_alpha^dagger J_alpha = r_alpha(s(e)) rho_e,
    D[J_alpha](rho_e)
        = r_alpha(s(e)) [rho_(e+q_alpha) - rho_e],
    [H(S),rho_e] = 0.                                                     (4)

The first two equalities do not assume `Q_alpha` commutes with its conditioning
projector. For the specified projector jump,
`J=sqrt(gamma) Q Pi`, one has `J^dagger J=gamma Pi`, not a post-jump
projector. Therefore no-jump terms use precisely the pre-jump syndrome rate.

Let `p_t(e)` be the finite continuous-time Markov chain starting at `e=0`,
with transitions `e -> e+q_alpha` at rate `r_alpha(s(e))`. Its backward
generator is

    (G h)(e) = sum_alpha r_alpha(s(e)) [h(e+q_alpha)-h(e)].                 (5)

Substituting its forward equation into `sum_e p_t(e) rho_e` and using (4)
proves that this sum solves the quantum master equation with the correct
initial state. Finite-dimensional linear-ODE uniqueness then gives

    (exp(t L) Enc tensor id_R)(rho_LR) = sum_e p_t(e) rho_e                 (6)

for every `t>=0`. The same single distribution `p_t` works for every input
and reference. Linear dependence of orbit density operators is harmless:
the construction produces a solution; it does not infer a unique classical
decomposition from the quantum state.

The actual model has `H=0`, `f=sqrt(kappa) Pi` for corrections, and
`f=sqrt(lambda_P) I` for physical faults. It is exactly within (3).

### No-jump evolution explicitly

The rate operator is `R_op=sum_alpha J_alpha^dagger J_alpha`, with eigenvalue
`r(s)=sum_alpha r_alpha(s)` on `P_s`. The effective no-jump propagator is

    K_0(t)=exp[-it H(S)-t R_op/2].
    K_0(t) E_e V = exp[-it H(s(e))-t r(s(e))/2] E_e V.                     (7)

Thus the normalized no-jump state is unchanged, and its probability weight is
`exp[-t r(s(e))]`, independent of logical input. A subsequent jump multiplies
the state by a Pauli and a syndrome-dependent scalar. There is no hidden
continuous logical filtering from the anticommutator.

For the exact finite torus,

    r(s)=kappa [N_active,primal(s)+N_active,dual(s)]
         +6 L^4 (lambda_X+lambda_Y+lambda_Z).                              (8)

Both active counts are at most `L^4`. The total accepted-jump intensity is
bounded by `2 kappa L^4+6 L^4 sum_P lambda_P`. A coefficient `lambda D[P]`
corresponds to a rate-`lambda` Poisson Pauli flip; there is no additional
factor of two in the event rate.

### Simultaneous faces and X/Z ordering

Equation (4) only needs `Q` to be a unitary Pauli string. A two-face `Z_f Z_g`
correction is a *single* transition adding both faces at once. Replacing it
by two independent single-face corrections would change the process and is
unnecessary.

Any finite interleaving of X, Z and Y strings multiplies to the Pauli with
the binary-summed label, up to a scalar phase in `{1,-1,i,-i}`. That phase
cancels in (1). Independent finite-rate proposal clocks almost surely have
no simultaneous distinct marks, so there is no unresolved ordering ambiguity.
Logical/reference superpositions remain intact along each trajectory except
for the eventual logical Pauli action.

## 2. Exact rates, support and encoded resources

For sufficiently large `L` (in particular `L>=3` avoids small periodic-cell
identifications), there are `L^4` vertices and `binom(4,2)L^4=6L^4`
positively based faces. Six qubits per positive-base cell give dimension
`2^6=64`. Both primal and dual vertex sets have `L^4` elements.

The eight edge checks incident to a primal vertex are weight six. Their union
contains exactly the faces incident to that vertex: for each orientation
`{i,j}`, the four possible positive bases are

    v, v-e_i, v-e_j, v-e_i-e_j.

There are `6*4=24` distinct physical faces. The one or two positively based
correction faces are already in that union. The dual union is the set of 24
two-faces of a primal four-cube. Consequently each correction jump is supported
on at most 24 qubits. In either case the supporting positive-base cells have
coordinate diameter one in the periodic infinity metric. This is range one
in the cell convention of G; it is a 4D mathematical locality statement.

There are `binom(4,2)+binom(4,4)=7` nonempty even outgoing patterns. At a
vertex the pattern projectors are orthogonal. Each pattern is nonzero: the
boundary of its one/two selected positive faces realizes that local outgoing
pattern and has no incoming edges there. Therefore

    ||J_(v,O)|| = sqrt(kappa),
    sum_O J_(v,O)^dagger J_(v,O) = kappa sum_O Pi_(v,O) <= kappa I.          (9)

There are `14L^4` correction jump terms, each writing at most two qubits.
The noise specification adds `18L^4` listed Pauli jump terms, counting any
zero-rate ones. A rate-`kappa` clock per vertex and sector chooses the unique
active pattern, or does nothing. This is an exact *restricted classical
representation* on the invariant family; it is not an equality between
arbitrary full-Hilbert-space measurement superoperators.

For the cubical four-torus, `b_1=4`, `b_2=6`, and `rank(partial_1)=L^4-1`.
Thus

    rank(partial_2)=4L^4-(L^4-1)-4=3L^4-3,
    rank(partial_3)=6L^4-rank(partial_2)-6=3L^4-3,
    k=6L^4-rank(partial_2)-rank(partial_3)=6.                              (10)

The two ranks are the X- and Z-stabilizer ranks. A nonzero 2-homology class
has odd intersection with a complementary dual coordinate 2-torus. Its `L^2`
disjoint translates are homologous tests, so the chain meets every one and
contains at least `L^2` faces. A coordinate 2-torus attains that weight. The
self-dual argument gives the same X distance: the parameters are
`[[6L^4,6,L^2]]`.

These are storage resources. Exact initialization, ideal syndrome extraction,
and final processing are separate assumptions. The proof's error labels,
envelopes, slabs and independent null proposals are not physical registers.

## 3. Y correlations and precisely why the actual sector marginals close

Write a physical Pauli label as `(a,b)` for `X^a Z^b`; a Y event toggles both
bits on its face. Its scalar rate `lambda_Y` produces the correct correlation
in the joint process (5).

For a test function of `b` alone, X corrections and X noise leave it unchanged;
Z corrections depend only on the X-check syndrome `partial b`; and Z or Y
physical noise toggles a single `b_f` with total rate `lambda_Z+lambda_Y`.
Therefore the projected `b` process is exactly the stated primal sweep
process with independent Poisson face births at that rate. Similarly, the
dual `a` process has rate `lambda_X+lambda_Y` and its own sweep corrections.
For each marginal, the face-birth Poisson streams are independent across
faces and independent of correction attempts. The two marginals need not
be independent of one another.

If `Bad_Z` and `Bad_X` bound sector failures, then

    P(Bad_Z union Bad_X) <= P(Bad_Z)+P(Bad_X).                             (11)

This applies to simultaneous control of all six logical qubits. It does not
require a separate quantum channel factorization into independent sectors.

The stronger joint lemma (6) allows rates depending on both syndromes.
Separate marginal Markov closure then requires a lumpability check: all
rates leading to a specified projected transition must sum to a value
independent of the forgotten sector. A countermodel is given below.

## 4. The fixed decoder is a full CPTP map

Every allowed joint syndrome `s` admits a Pauli recovery `R_s` with

    R_s P_s R_s^dagger = P_0.                                            (12)

In the toric CSS model the measured sector syndromes lie in the images of
their boundary maps. Stabilizer constraints include the global relations;
one must not treat every locally closed non-boundary loop pattern as an
allowed physical eigenvalue pattern. Equivalently, the Pauli syndrome map
onto characters of the independent stabilizer generators is surjective.
The deterministic boundary solver in R provides the required fillings.

Define logical-output Kraus operators

    K_s = V^dagger R_s P_s,
    Dec(rho) = sum_s K_s rho K_s^dagger.                                  (13)

Since `V V^dagger=P_0`, equation (12) gives

    K_s^dagger K_s=P_s,
    sum_s K_s^dagger K_s=I.                                              (14)

This proves complete positivity and trace preservation on the *entire*
physical qubit Hilbert space. A bare compression `V^dagger rho V` is not
trace preserving on arbitrary states; in (13) it follows syndrome recovery
which maps each measured eigenspace into the code. Zero projectors for
inconsistent redundant-check patterns contribute nothing.

The map is fixed before storage and depends only on the final measured
syndrome. It does not use a trajectory label or a history-dependent choice.

### Constructing the fillings and preserving local stability

A vertex-connected component of a boundary 1-cycle is itself a cycle:
all incident edges at a vertex belong to the same component, so parity
holds componentwise. A sufficiently small component has a consistent
bounded lift to a coordinate box; the lift is unique up to a whole-period
translation. That translation has no effect after projection to the torus.

Inside its coordinate hull, project one coordinate at a time to the lower
face. The elementary prism identity is

    partial P_i + P_i partial = id+pi_i.                                 (15)

For `c_i=pi_i c_(i-1)`, each `c_i` is a cycle and the fourth projection
annihilates every edge. Hence

    D(c)=sum_(i=1)^4 P_i c_(i-1),
    partial D(c)=sum_i(c_(i-1)+c_i)=c.                                   (16)

This reconstructs R's filling. All written faces stay inside the hull.
The procedure uses at most `sum_i(b_i-a_i)*|c|` binary face toggles, so
the component regime costs `O(L^5)` toggles and an `O(L^4)`-bit dense face
bitset. For arbitrary large-component boundary syndromes a fixed binary
Gaussian solver supplies a filling. Its crude dense preprocessing costs
`O(L^12)` operations and `O(L^8)` bits. Neither estimate is a noisy or
fault-tolerant readout implementation.

For completeness I reconstructed the deterministic event argument used in C.
Take `r=L/32`, `rho=L/8`, and suppose all pre-event syndrome components have
ambient torus infinity-diameter `<r`. A fault face or one/two-face sweep event
has its vertex support in a unit coordinate box based at an anchor. Every
changed old component meets a vertex of `partial F` and fits within distance
`r` of that unit box. Every changed new component is made from those components
and `partial F`. Their union fits in one lifted box of side at most `2r+1`.
For sufficiently large `L`, this is `<rho` and the box is embedded.

Identical unaffected components receive identical fillings and cancel. All
remaining old and new fillings stay inside that common box, by their hull
construction. Thus

    F+D(s)+D(s+partial F)                                                 (17)

is a closed 2-chain supported in a contractible box. It has zero 2-homology,
so it is a stabilizer boundary. If `partial F=0`, the same conclusion follows
from the local support of `F`. This proves local invariance of the decoded
class `[E+D(partial E)]` at such an event, for the entire accumulated `E`.

Small current syndrome alone would not prove a trivial accumulated class:
a full logical membrane has zero syndrome. Starting at `E=0`, the eventwise
invariance above is what excludes such a membrane before a large-component
event. This distinction is essential. The separate probability estimate
must cover pre-event states at *all* event times; an instantaneous sampled
tail alone is not enough without the hazard or whole-slab transfer.

## 5. Decoded channel and the unhalved diamond bound

At error label `e`, only syndrome `s(e)` occurs in (13). The corrected Pauli
`R_(s(e)) E_e` normalizes the stabilizer group and induces a Pauli `L_e` on
all `k=6` logical qubits. Equations (6) and (13) give the channel identity

    Lambda_t = Dec exp(t L) Enc = sum_e p_t(e) Ad_(L_e).                  (18)

If both corrected CSS chains have zero 2-homology, each is a boundary of
3-cells on its respective lattice. The physical residual is a product of
X and Z stabilizers up to scalar phase, so `Ad_(L_e)=id` on *every* logical
and reference state.

Group the weights by logical Pauli. Let `p_nonI(t)` be the total weight of
nonidentity logical labels. Then

    ||Lambda_t-id||_diamond <= 2 p_nonI(t).                               (19)

To prove this, write `Lambda_t=(1-p_nonI)id+p_nonI B`, with `B` CPTP when
the weight is nonzero, and use `||B-id||_diamond<=2`.

In fact equality holds for this Pauli channel. Feed one half of the normalized
maximally entangled state of dimension `d=2^6` into the channel. Distinct
logical Paulis produce orthonormal Bell states. The output difference has
one eigenvalue `-p_nonI` and the nonidentity Pauli weights as its remaining
nonzero eigenvalues. Its trace norm is `2p_nonI`, matching (19):

    ||Lambda_t-id||_diamond = 2 p_nonI(t).                                (20)

No dimension-dependent factor or restriction to unentangled inputs is needed.
An event `Bad_[0,t]` outside which the decoded class remains zero gives
`p_nonI(t)<=P(Bad_[0,t])`. Consequently C's quantum conclusion follows if its
independent classical work proves

    P(Bad_[0,T]) <= C L^4(1+kappa T) exp(-cL).                            (21)

Combining (19) with the universal bound 2 and absorbing constants gives
exactly the form of C's (T). The logical identity weight also gives
entanglement infidelity at most `P(Bad_[0,T])` for every encoded input.

The final identity weight can exceed the probability of no earlier logical
change, because a trajectory may change class and later return. The stated
first-change bound is stronger than necessary for final recovery, and is
consistent with (18)–(21).

## 6. Measurement, leakage and generalization boundaries

The syndrome projectors can disclose syndrome information to a reservoir,
but their outcome probabilities are constant over the logical degeneracy
on each trajectory. They disclose no logical/reference information in this
exact model. Adding dephasing terms `D[g(S)]` or a syndrome-algebra Hamiltonian
does not change the orbit density operators: these terms vanish in (4).
This observation does not acquire a noisy measurement interface.

The following explicit countermodels isolate the assumptions. Each is
verified by integer arithmetic in `check_trajectory_exact.py`.

1. **Arbitrary physical input with coherent superpositions of syndromes.**
   One qubit with stabilizer `Z` and jump `J=X(I-Z)/2=|0><1|` obeys amplitude
   damping. For input `|+><+|`, at rate one,

       d rho/dt at 0 = [[1/2,-1/4],[-1/4,-1/2]],
       d <Z>/dt at 0 = 1.

   Every Pauli conjugate of `|+><+|` has `<Z>=0`. No convex mixture of those
   conjugates can reproduce this evolution at positive small time. This is
   a one-qubit exact countermodel to removing definite-syndrome initialization,
   not to arbitrary *logical* superpositions inside the code.

2. **Coherent Hamiltonian faults.** One qubit initialized in `|0>` and
   `H=X` develops off-diagonal entries with derivative `rho_01'=i`,
   `rho_10'=-i`. Its Pauli images remain diagonal. Thus arbitrary coherent
   generator errors do not admit (6). This refutes the exact reduction,
   and does not alone prove instability of the 4D memory under a specified
   small coherent perturbation.

3. **A coherent sum of Pauli jump amplitudes.** With
   `J=(X+Z)/sqrt(2)` and input `|0><0|`, the derivative is
   `[[-1/2,1/2],[1/2,1/2]]`. It also leaves the convex hull of the Pauli orbit.
   `D[J]` cannot be replaced by the sum of separate Pauli dissipators;
   cross terms matter. Implementing the specified conditional operator
   only approximately is a different model.

4. **Other-sector-dependent Y rates.** On two qubits with commuting
   stabilizers `XX,ZZ`, take `J=Y_1(I-ZZ)/2`. The error labels `II` and `XI`
   have the same Z-error vector but rates 0 and 1 for its next Y-induced
   flip. The Z-error marginal fails the Markov lumpability condition.
   The *joint* trajectory proof (6) still holds. Constant-rate Y faults in
   the stated model do not have this obstruction.

5. **A rate projector which can distinguish logical states.** The code
   stabilized by `ZI` has logical states `|00>` and `|01>`. A jump
   `J=XI(I+ZI)(I+IZ)/4` has rates 1 and 0 on those two code states.
   Input-independent weights and scalar logical no-jump evolution fail.
   Conditioning must be scalar on the full syndrome eigenspace, rather
   than merely commuting with all stabilizers. A logical operator also
   commutes with them, but is not a function of their eigenvalues.

6. **Leakage outside the qubit Hilbert space.** On a qutrit, with computational
   subspace `span{|0>,|1>}`, the jump `|2><1|` transfers initial `|1>`
   population outside that subspace at instantaneous rate one. Qubit Pauli
   trajectories cannot represent the output. The theorem excludes leakage;
   it does not give a leakage threshold or a recovery operation for leaked
   systems.

Classical syndrome mistakes which merely select different Pauli jumps can
remain inside the algebraic lemma if their rates are functions of stabilizer
syndrome. They nevertheless alter the classical process, so the sweep
probability tail needs another proof. A noisy final decoder also requires
its own quantitative guarantee: if its diamond distance from (13) is at
most `delta_read`, the end-to-end bound becomes at most
`2P(Bad_[0,T])+delta_read`.

A generic generator perturbation `Delta` has only the immediate continuity
estimate

    ||exp[T(L+Delta)]-exp(TL)||_diamond <= T ||Delta||_diamond,             (22)

when both semigroups are CPTP. This follows from Duhamel's formula and
channel contraction. For a sum of local perturbations with per-cell size
`delta`, the crude global bound is `O(T L^4 delta)`. It gives no exponentially
long storage guarantee at a fixed arbitrary perturbation strength.

## 7. Exact finite checks and remaining dependencies

Run:

    python3 research/2026-10-16-adversarial-quantum-memory/trajectory/check_trajectory_exact.py

The saved receipt reports:

* 64 Pauli labels for a three-data-qubit CSS code, with an arbitrary logical
  qubit tested maximally entangled with a reference qubit;
* 1,472 exact, denominator-cleared matrix equalities for conditional multi-qubit
  jumps, joint-syndrome conditions, X/Z/Y noise, and no-jump rate operators;
* complete Kraus normalization of a full toy decoder and recovery of all 64
  reference-entangled Pauli orbits;
* exact side-3 4D cubical incidence checks: 486 data qubits, weight-six checks,
  two stabilizer ranks 240, six logical qubits, 24-qubit primal/dual stars,
  567 active primal patterns and 81 simultaneous two-face patterns;
* the six scope countermodels above.

All arithmetic is arbitrary-precision integer arithmetic on Gaussian-integer
matrices, with denominators cleared. These checks verify the implemented
finite instances and examples. They do not establish the general lemma,
which is proved in sections 1–5, or any asymptotic classical stability claim.

The remaining dependencies for C's full lifetime theorem are explicit:

1. the monotone support coupling, block forcing and genuinely local fresh
   primitive flags claimed in C, lines 57–115;
2. valid application of the named infinite-volume domination and spacetime
   cluster theorem, C, lines 119–132;
3. the stopped finite-torus witness transfer and the whole-slab pre-event
   component control, C, lines 136–162;
4. their quantitative bound (21) for the actual two sector trajectories,
   with a union over sectors.

The deterministic decoder and quantum conversion from those premises are
proved here. The classical items above remain outside this report's
independent certificate. Exact jump engineering, physical 3D embedding,
preparation, reservoir/reset/energy/calibration costs, imperfect corrections,
and noisy readout also remain unacquired. Historical originality and external
formal certification are not established.
