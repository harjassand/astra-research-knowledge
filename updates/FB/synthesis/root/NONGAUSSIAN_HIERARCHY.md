# Finite-order vacuum spectroscopy does not certify an interacting environment

13 October 2026. Capital baseline4025c5252f1ca992d3eae6ed422d6338ebe6c5a4.
This is an integration-derived exact obstruction, with same-team criticism and
finite diagnostics. Historical originality, external correctness and material
relevance remain UNKNOWN. It extends the submitted two-bath one-particle witness;
it is not a new claim that generic correlation hierarchies close at finite order.

## 1. Exact information and energy task

Fix an integer k>=1 and put r=k+1. There are r labelled environmental fermion
modes c1,...,cr and ONE impurity mode d. Let n_i=c_i^dagger c_i and n_d=d^dagger d.
The available bath information may include every zero-temperature vacuum
multi-time expectation of a word containing at most k elementary creation
operators and at most k elementary annihilation operators, at arbitrary times,
with arbitrary labelled modes or their linear combinations. The energies and
matrix elements of the bath Hamiltonian in every sector N_B<=k may even be
supplied. This is stronger than one-particle spectroscopy and any finite list of
its frequency moments.

This access does NOT include preparing a bath with r particles, strong pumping
that populates that sector, finite-temperature correlators, the coupled-system
ground state or its charge, arbitrary products of occupation projectors, or
unbounded-order responses. Those would be different information contracts.

Both candidate designs have the same bath and the same quadratic coupling

    H_c=(1/2)(d^dagger c1+c1^dagger d).

Only the known impurity Hamiltonian differs. The target is the zero-temperature
grand-canonical ground-energy ordering at chemical potential zero. The common
uncoupled bath ground energy is zero, so its subtraction changes no comparison.
This is the output regime of the new moment-environment submission, not an
isolated molecule's preselected electron-number sector.

## 2. Two indistinguishable environments

Put

    delta=1/(8r),   P_full=product_(i=1)^r n_i,
    H_B,quad=sum_i n_i,
    H_B,hid=sum_i n_i+(-r+delta)P_full.

The two baths are number conserving. Both have a unique vacuum ground state
at energy zero. In the quadratic bath a q-particle state has energy q. In the
hidden-interaction bath it has the same energy for q<r, and the fully occupied
state instead has energy delta>0. Thus they agree as operators on N_B<=k.

**Lemma.** Every available vacuum multi-time correlator is identical in these
two environments.

Proof. Express each elementary Heisenberg operator as exp(iH_B t)c_i exp(-iH_B t)
or its adjoint and evaluate a word from right to left on the vacuum. Propagators
preserve particle number. At any intermediate stage its number cannot exceed
the total number of creation operators in the word, at most k. A negative
occupation attempt annihilates the vector in both models. All remaining
intermediate vectors and propagations therefore lie in sectors where the two
Hamiltonians coincide. The resulting vacuum expectation is equal. Linearity
covers arbitrary linear mode combinations. No time ordering, approximate
resolution or finite frequency cutoff is needed. QED.

The order-r addition/removal experiment can distinguish the baths: the fully
occupied state accumulates phase exp(-irt) in one and exp(-i delta t) in the
other. The theorem concerns a finite bound on accessible probe order, not an
impossibility of acquiring any environmental information.

## 3. Exact same-coupling design reversal

Define the positive rational number

    a=r/[2(4r^2+1)],

and the two supplied local designs

    H_A,1=n_d,
    H_A,0=(2r+1)n_d-(a/2)I.

Both use the same H_c above. Let E_j(B) be the minimum of
H_A,j+H_B+H_c on the full Fock space and Delta(B)=E_1(B)-E_0(B).
Then

    Delta(quad)=+a/2,
    Delta(hid)<=-a/2.

Thus the design preference reverses, with a two-sided margin at least
`r/[4(4r^2+1)]`, despite complete agreement of the entire supplied information.

Proof for the quadratic bath. Ignoring design0's scalar, the coupled d,c1
one-particle matrix is [[M,1/2],[1/2,1]], where M=1 or2r+1. It is positive
definite for either choice; all remaining modes have energy1. Its fermionic
second quantization is positive, with vacuum minimum zero. Consequently
E_1(quad)=0 and E_0(quad)=-a/2.

Proof for the hidden bath. Occupations of spectator modes c2,...,cr commute
with the complete Hamiltonian. Fix their total q. If q<r-1, the interaction
vanishes and the d,c1 Hamiltonian, without the design scalar, is

    q I + M n_d+n_1+(1/2)(d^dagger c1+c1^dagger d),

which is positive by the preceding one-particle calculation. If q=r-1, split
by the number in the d,c1 pair. Its zero-particle energy is r-1, its
two-particle energy is M+delta, and its one-particle block, in the order
|d occupied,c1 empty>, |d empty,c1 occupied>, is

    [[r-1+M,1/2],[1/2,delta]].

A fermionic basis phase can make the off-diagonal entries positive; it does
not change energies or the trial argument.

For design0, M=2r+1 gives the block [[3r,1/2],[1/2,1/(8r)]]. Its determinant
is1/8 and both diagonal entries are positive. Every sector is therefore
nonnegative before adding the scalar, and vacuum remains a zero-energy state.
Hence E_0(hid)=-a/2 exactly.

For design1, M=1 gives [[r,1/2],[1/2,1/(8r)]], whose determinant is-1/8.
The rational trial vector(-1/(2r),1) has Rayleigh quotient

    [-1/(8r)]/[1+1/(4r^2)]=-r/[2(4r^2+1)]=-a.

All other sectors are nonnegative; this block has one negative eigenvalue.
Thus E_1(hid)<=-a and Delta(hid)<=-a/2. The bound follows from exact rational
arithmetic, not numerical eigenvalue agreement. The precise ground energy is
the lower eigenvalue of the displayed2-by-2 block. QED.

## 4. What information this rules out

Any deterministic inference procedure using only the stipulated bath data sees
the same transcript for both environments. It cannot certify the correct sign
for both. A randomized binary design choice has worst-case wrong-choice
probability at least1/2. Its worst-case expected energy regret is at least a/4:
choosing design1 in the quadratic bath costs a/2, choosing design0 in the hidden
bath costs at least a/2, and the same output distribution is used in both.
The exact minimax regret for unequal true margins may be larger; no equality
claim is needed here. An algorithm may return UNKNOWN honestly.

This is an indistinguishability theorem for the acquired information interface,
not a query-complexity lower bound when higher-order probes are allowed. It
applies even if all allowed low-order observations are exact and free. More
precise one-particle moments or a better quadratic bath fit cannot repair the
missing model qualification.

The active dimension and hybridization rank remain constant: one impurity
fermion and one coupled bath mode, with coupling norm1/2. The r-body environment
interaction has norm r-delta; the known design0 local level is2r+1. Bath mode
count, interaction order and these energy scales grow linearly with k. The
certified sign margin is of order1/k, not a constant as k grows. The hidden
bath's vacuum gap is delta=1/(8r); no size-independent bath gap is asserted.
No spatial locality, two-body-only bath class or physical implementation of
the r-body interaction is supplied. Such additional promises could exclude
this family and need their own proofs/information costs.

Finite temperature can populate the hidden sector and alter low-order data.
No finite-temperature indistinguishability follows from this vacuum proof.
Likewise a repeated control/probe sequence whose total particle additions exceed
k is outside the information contract even if each pulse is individually linear.

## 5. A sector certificate can remove this obstruction

For this same pair, if the requested energy is restricted to a known total
charge Q<=k, then N_B<=Q<=k everywhere in that sector. P_full vanishes exactly.
The two total Hamiltonians therefore agree on the full target sector for each
design, so the hidden interaction cannot change that fixed-sector decision.

More generally, an acquired operator agreement on all bath charges<=Q plus
number-conserving coupling and nonnegative active charges supplies the same
restricted equality. This is an exact compatible interface with the
charge-aware discipline of N778, not an implication that ordinary covariance
selects the right sector or that low-order spectra automatically certify Q.
The hidden coupled ground state above has total charge r, whereas the quadratic
coupled ground state is vacuum. A separately measured/supplied charge restriction
changes the energy task and removes those alternatives; it is not available
from the original low-order data for free.

Macroscopic material electron number is generally not a small excitation count.
Obtaining an appropriate particle/hole encoding, selected sector, environment
interaction restriction or quantitative non-Gaussian error remains the decisive
physical/mathematical gate. Full k-particle operator acquisition itself has
dimension sum_(j<=k) binom(r,j); no cheap general spectroscopy compiler is
established here.

## 6. Provenance and tests

The source moment-environment note§11 supplies a two-mode one-particle
counterexample with two impurity modes and different coupled/reference controls.
Root extended the information hierarchy; the independent critic supplied the
same-coupling design0 refinement above. Both are separately attributed internal
deductions. The new positive quadratic moment theorems remain intact: H_B,hid
is outside their genuinely quadratic model class.

`hierarchy_checks.py` independently builds fermionic operators, checks exact
rational2-by-2 pivots/Rayleigh signs and selected full-Fock/charge matrices, and
evaluates finite vacuum correlator diagnostics. Tests support the implementation;
the universal all-k statement is proved above. No primary literature priority
clearance, external theorem validation, physical observation or chemical-design
advantage is inferred from this counterexample.
