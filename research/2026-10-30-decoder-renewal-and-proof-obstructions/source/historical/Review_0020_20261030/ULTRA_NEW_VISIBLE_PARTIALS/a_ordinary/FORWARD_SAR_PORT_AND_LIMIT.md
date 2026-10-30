# What forward-isometry storage does, and does not, supply to mixed recovery

30 October 2026. A mathematical composition and a sharp interface obstruction.
No source, quantum circuit or numerical optimizer is executed here. The input
is the exact flat channel of `FLAT_RDS_RECOVERY.md`; all original calls below
are ordinary forward physical calls. This file does not claim a linear-r
mixed-channel recovery, or a quadratic physical-query lower bound.

## 1. The actual ordinary predecessor

Yoshida--Miyazaki--Murao, 2507.10784v4, Corollary 2 and its PBT construction,
stores an unknown isometry F:C^2 -> C^d using n parallel FORWARD F calls.
For a later qubit input, the retrieval channel is F composed with an ordinary
qubit teleportation channel. It does not apply F^*, F^T, a controlled F, or a
reflection about ran(F). Its output includes the full d-dimensional isometry
output, not a retroactively supplied purification of an earlier output.

For the optimized qubit resource the teleportation entanglement fidelity is

    f_n = cos^2(pi/(n+2)).                                      (1)

This explicit formula and the resource coefficients are from Ishizaka--
Hiroshima 0901.2975, Section IV.2, equations (35),(40),(41). Covariance makes
the teleportation channel depolarizing, so its HALF diamond distance from the
identity is exactly 1-f_n. Isometric composition preserves diamond norm:

    (1/2)||Retr_F - Ad_F||_diamond
       = sin^2(pi/(n+2)) <= pi^2/(n+2)^2.                       (2)

This is a forward service on arbitrary references. A fidelity-only or an
average-input substitute is not being used. All failed PBT outcomes are
included; this is a deterministic complete channel, not heralded retention.

## 2. A paid common-frame adaptive FORWARD service from the original channel

Theorem 3 of Yoshida--Niwa--Utsumi--Takagi--Murao 2512.21260v2 supplies the
parallel superchannel identity

    Xi(N^tensor Q) = E_V [Ad_V^tensor Q],                       (3)

with ONE random Stinespring frame V:C^2 -> C^r tensor C^D. The equality is
of channels on arbitrary joint inputs, not an identity only on maximally
mixed inputs or Choi states. Its Lemma 6 optionally replaces V by the random
conditional isometry

    F_theta = (e^(i theta)|0>V0 + |1>V)/sqrt2,                  (4)

where V0 is public and theta is ONE common phase. Both (3) and (4) have
parallel original-channel slots. They do not directly offer adaptive slots.

Here is a legitimate conversion. Suppose a known future circuit requires m
adaptive FORWARD uses of one common V (or F_theta), with arbitrary memory.
Prepare m independent optimized PBT input resources, each with n Bob qubits.
Feed all Q=mn Bob inputs through (3), and (4) if desired, in one offline batch.
Conditional on the one latent isometry F, the resulting state is

    tensor_(j=1)^m (id tensor Ad_F^tensor n)(Psi_n).            (5)

This conditional tensor product is essential. Averaging each output block
independently would give a different resource and generally lose coherence
between later calls. The frame need never be revealed. The RDS factory may
depend on Q; only this one declared finite batch is needed.

Reserve one block for each future slot. At that slot perform the known PBT
measurement on its small Alice systems and the adaptive logical input, select
the indicated full output port, and discard its other ports. Conditional on F
each slot obeys (2), even with all unused programme blocks and arbitrary
reference retained. The channel/comb hybrid inequality therefore gives

    (1/2)||actual m-slot consumer - ideal common-F consumer||
       <= m*pi^2/(n+2)^2,                                    (6)

before finite gate/factory errors. The norm here is the distinguishability
of any fixed known adaptive consumer, or equivalently the ordinary comb norm
for the declared order. The same bound survives averaging over common F.

A literal safe schedule is n=ceil(sqrt(64m/epsilon)). Since pi^2<16, the ideal
PBT contribution is at most epsilon/4. Give epsilon/4 to the complete factory,
epsilon/4 to all resource/controller gates, and keep epsilon/4 as spare. Then

    original forward calls Q=mn=O(m^(3/2)/sqrt(epsilon))        (7)

produce this finite adaptive FORWARD service. There are no original N queries
after the payload arrives. The programme is consumed, not catalytic. The
bare stored port registers alone cost O(Q(log(rD)+1)) qubits; factory workspace
and small-port registers are additional. PBT measurements act on n+1 small
qubits; selecting one full port also costs known routing of O(n log(rD)) bits
or gates in a direct implementation. Online latency and coherence are paid.

The factory's large-r uniform Schur/Haar implementation must use the already
qualified small-Schur/highest-weight port, not fixed-r n^r GT enumeration.
All fixed-batch approximation errors are allocated before its execution.
This is polynomial in Q,r,log D and inverse error under the same known-control
model as the baseline; it is not an iid-Choi-copy construction.

## 3. The optimized qubit PBT resource is acquired, not an oracle

Grinko--Burchardt--Ozols 2312.03188v2 Theorem 1 gives polynomial-size PBT
MEASUREMENTS, including optimized deterministic PBT. The paper explicitly
leaves GENERAL optimized deterministic resource preparation open. It cannot
silently be cited as supplying that missing resource. The qubit closed form
does supply it as follows.

Write n qubits in the known Schur basis with spin j, irrep dimension 2j+1,
and multiplicity g_n(j). The resource is the normalized vector corresponding
to sqrt(X) applied to n known singlets, with X from primary equation (35).
Its squared sector weights are exactly

    w_j = 4/(n+2) sin^2(pi(2j+1)/(n+2)),
    j=j_min,j_min+1,...,n/2,  sum_j w_j=1.                     (8)

Thus, up to the PUBLIC spin-singlet/conjugate-basis convention, it has form

    sum_j sqrt(w_j) |j,j> tensor Phi_(2j+1) tensor Phi_gn(j).   (9)

The convention is fixed by the known qubit Schur transform and its known
complex-conjugate circuit. No conjugation of an unknown isometry is needed.

There is a direct polynomial preparation of (9). Prepare the O(n) known
spin weights. Conditional on j, prepare the irrep Bell pair of dimension
2j+1. For the multiplicity Bell pair, count ballot paths. Let M(l,s) count
length-l paths from 0 to s with steps +/-1 staying nonnegative. Then

    M(0,0)=1; M(l,s)=M(l-1,s-1)+M(l-1,s+1),                 (10)

and g_n(j)=M(n,2j). Starting from s=2j, coherently select each predecessor
with probability M(l-1,s')/M(l,s), recording the reversed path in two matched
registers. All full paths then have amplitude 1/sqrt(M(n,2j)). This is exactly
the multiplicity Bell pair, with no enumeration of its exponentially many
paths. Zero-count predecessors are omitted rather than divided by zero.

The table has O(n^2) integer entries, each at most 2^n. Elementary arithmetic
therefore costs polynomial bit operations; O(n) finite-controlled rotations
per path branch and polynomial table lookups suffice. Compute square roots,
sine weights and all known rotations to a shared b-bit accuracy, with b
polynomial in log(1/error) and log n; polynomially many gates then have a
charged total error. Standard polynomial qubit inverse Schur circuits on both
sides finish the physical resource. Formula (9), including multiplicity
preparation, is consequently a paid qubit port, not the open general-d
resource task and not an assumed exponentially large-state compiler.

## 4. Why the four-query isometry inverse does not yet solve mixed recovery

2401.10137v3 Section 3.3/Corollary 6 gives deterministic exact qubit-isometry
inversion with four adaptive forward V calls, for every output dimension.
Its contract is a CPTP decoder D_V satisfying D_V Ad_V=id. It does NOT expose
a coherent V^* block, its success projector/workspace, or controlled V^*.
Reversing its circuit would reverse its unknown V calls, which are not given.

Equation (7) may supply those four future FORWARD V calls, with error, from
offline native N calls. But an earlier native payload is only N(rho) on B.
It is not V rho V^* on E tensor B. Attaching an independent I_E/r gives

    Tr[VV^*(I_E/r tensor N(rho))] = 1/r^2.                  (11)

This is a code-weight identity, not an upper bound on the actual four-query
decoder's performance outside its promised isometry range. The distinction
is decisive. Two mathematical CPTP completions correct on that range are

    D_bad(X)=V^*XV + Tr[(I-VV^*)X] I_2/2;
    D_good(X)=R_B(Tr_E X),                                 (12)

where R_B is the true mathematical flat inverse on B. The first yields

    D_bad(I_E/r tensor N(rho))
      =rho/r^2+(1-1/r^2) I_2/2,                            (13)

whereas D_good recovers rho exactly. Equation (12) is NOT an acquisition of
R_B; it proves only that the isometry-inversion code contract leaves the
native mixed-payload action undetermined. A constructive analysis of the
particular circuit outside ran(V), or a different active operation, is needed.
No rejection of all adaptive isometry circuits follows from (11).

## 5. A sharp source-query obstruction to the reflection-supplier shortcut

The forward-isometry storage rate in (7) cannot simply be relabelled as the
same rate for the reflections used in `FLAT_RDS_RECOVERY.md`. This already
fails in a native subclass with r=1 that is itself trivially recoverable:

    N_psi(rho)=rho tensor |psi><psi|,                       (14)

where psi is an arbitrary unknown d-dimensional pure state. Any adaptive,
entangled algorithm with n forward N_psi calls can be simulated EXACTLY from
n copies of psi and known operations: each source call just appends the next
copy. This reduction is not restricted to iid Choi-only algorithms.

Choose a public unit vector a. The conditional-isometry projector has the
form I_2 tensor |chi_theta><chi_theta|, where

    chi_theta=(e^(i theta)|0>a+|1>psi)/sqrt2.

Let A_theta=I_2 tensor(2|chi_theta><chi_theta|-I). Input a fixed logical qubit
and the state |1>x. After A_theta, measure the PUBLIC event flag=0 and junk=a.
Its probability is exactly |<psi|x>|^2, for EVERY theta. Thus a one-reflection
service whose averaged common-phase channel has half-diamond error at most
e would implement the unknown rank-one membership measurement with both
type errors at most e. An unobserved theta causes no loophole.

The exact n-copy lower bound for this comparison is elementary. Under equal
priors, compare test x=psi with x uniform in psi-perp, averaging psi Haar.
For d>=2 put d_l=binomial(d+l-1,l). The two joint density operators are

    Omega0=Pi_sym^(n+1)/d_(n+1),
    Omega1=((Pi_sym^n/d_n) tensor I - Omega0)/(d-1).          (15)

On Sym^(n+1), Omega1=Omega0/(n+1); off that space Omega0=0 and Omega1>=0.
It follows exactly that

    (1/2)||Omega0-Omega1||_1=n/(n+1),
    minimum equal-prior classification error=1/[2(n+1)].    (16)

Consequently any such uniformly valid reflection service requires

    n >= 1/(2e)-1.                                        (17)

This lower bound applies to arbitrary adaptive original-source queries in
(14), not only a particular DME collision implementation. In particular,
the square-root precision rate for FORWARD storage cannot be automatically
transferred to this reflection supplier, even at fixed logical dimension.
The comparison mechanism is ordinary programmable-state measurement:
2401.10137v3 Section 3.4, equations (112)--(114), explicitly credits Chabaud
et al., PRA98,062318(2018), for the one-sided symmetric-projector bound
1/(n+1). Equations (15)--(17) are the elementary two-sided testing reduction
needed for this native reflection interface, not a generic novelty claim.

This does NOT prove an r^2 recovery barrier. The channel in (14) has a known
perfect decoder: discard the last register. Nor does (17) rule out collective
or adaptive algorithms which bypass reflections or exploit the whole target
task. It isolates the precise supplier that the SAR headline does not improve.

## 6. Pure-query control for the new adaptive-comb investigation

Quintino--Ebler 2109.08202v3 Section 5.2/Theorem 5 and equation (56) give the
optimal PARALLEL qubit inversion fidelity with Q queries,

    F_parallel(Q)=cos^2(pi/(Q+3)).                           (18)

The proof relates parallel inversion to unitary estimation; for qubits the
known conjugation by sigma_Y also relates inversion and transposition. The
paper's Section 6/Figure 8 reports the two-query sequential value .7500 with
computer-assisted primal/dual bounds to four decimal places. The later
isometry paper 2401.10137v3 Corollaries 6 and 11 and Table 2 transfer and
identify these values for every qubit output dimension. Its table gives
Q=1: .5000; Q=2: parallel .6545, sequential .7500; Q=3: parallel .7500,
sequential .9330; and Q=4 sequential 1. These numerical table statements are
not promoted here into an exact analytic 3/4 or .9330 formula.

In particular F_parallel(2)=(3+sqrt5)/8. The new comb's r=1 Q2 discovery
values match the established ordinary pure endpoint. Mixed-r adaptive gaps
and asymptotic r cost require their own construction and proof. Equation
(18) is not asserted for those mixed encodings.

## 7. Outcome and honest costs

The ordinary storage predecessor genuinely supplies a useful offline-to-
adaptive FORWARD dilation service, with the explicit qubit resource and all
common-frame requirements paid. It does not by itself supply the reflection
or the correct input for a pure-isometry decoder. The native comparison (14)
proves a sharp precision obstruction to that particular relabelling while
granting the trivial ordinary decoder of the source itself.

These are all-n/all-r algebraic constructions or obstructions; no source
queries, quantum runs, simulated trajectories or optimizer calls were made.
Stored exact public resource coefficients are computable in polynomial bit
cost, but the quantum circuits have not been implemented. Practical advantage
and historical priority of this particular composition are UNKNOWN. The
closest ordinary pieces (RDS, PBT, isometry inversion, programmable comparison
and amplitude amplification) are explicitly credited rather than renamed.
