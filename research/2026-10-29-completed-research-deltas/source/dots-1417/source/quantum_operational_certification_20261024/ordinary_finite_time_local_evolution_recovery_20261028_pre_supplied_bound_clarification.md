# Ordinary joint recovery after an unknown finite-time local encoding evolution

28 October 2026. **New physical-family corollary candidate; independent review in progress.** No source calls or hardware data. This uses the received approximate-local theorem without modifying it. It supplies a physical reason for small logical-generator tails, then pays for the width required by GLOBAL reliability. It is not a result for arbitrary local noise or non-reset dynamics.

## 1. Physical source family and information actually supplied

Retain the source, ordinary controls, common Pauli/gauge structure, four-real-coordinate encoder family, aggregate contrast kappa and separate global identity-dominance promise from `ordinary_approximately_local_joint_recovery_20261028.md`, received SHA `1ae8d8f836d366268a4c8f182b9c8b679ba77aea9fde5ebe669e5e576ad74c4d`. The n physical qubits occupy a known line. An UNKNOWN injective assignment places the q input logical factors at distinct physical sites; the remaining factors are gauge. Let Pi denote that unknown identification. The common physical encoding unitary is now promised to have the form

    U_total=U_H(T) Pi,
    U_H(T)=time-ordered exp[−i integral_0^T H(t)dt],
    H(t)=sum_(a=1)^(n−1) h_(a,a+1)(t), ||h_(a,a+1)(t)||<=J. (1)

Terms may be unknown, complex, noncommuting and time dependent. Assume finite bounded piecewise-continuous dynamics; hbar=1 fixes units. The learner is supplied a rational upper bound B>=JT, not the Hamiltonian terms, their propagator, the site assignment, local generators or a source inverse. Single-site terms can be included only after an explicit decomposition into edge-supported terms with a valid adjusted J; they are not silently added to(1). For n=1 use the full-register case below.

The unknown Pauli/gauge operation acts BEFORE this common unitary as in the governing model. The coherent local evolution is NOT itself a claim that a general dissipative local process has positive Pauli contrasts or global identity dominance. Each source call resets; time dependence WITHIN a duration-T encoding call does not supply a non-reset/memory theorem.

For a nonvacuous instance, keep the literal four-dimensional selector family in `joint_local_logical_swap_physical_family_20261028.md`: the selector is measured in an unknown real basis, branch identity probabilities are(1,4/5,3/4,7/10), arbitrary correlated nonidentity Pauli probabilities fill the rest, and branch gauge states may be noncommuting, globally entangled or arbitrarily ill-conditioned. Replace its unknown shallow circuit by(1). Then kappa=2/5 and G_I>=G_alpha still hold, with an unknown perfect encoder. No Pauli table is supplied or reconstructed. That literal realization consumes TWO selector qubits per call in addition to the q logical inputs; its known selector preparation/control is paid separately. The four-dimensional encoder restriction remains substantive.

## 2. Exact primary locality import, restricted to unitary dynamics

We use [Barthel and Kliesch, arXiv:1111.4210v2](https://arxiv.org/pdf/1111.4210), Theorem2/Eq(14), with definitions(2)–(7). Their observable evolution is approximated by the propagator truncated to the EXTENDED region bar(V), not merely V. For interaction range a, term norm b, overlap degree Z, shell growth M r^s and D=ceil[distance(Y,Lambda\V)/a]>2s+1, the operator error is at most(2M/Z)||O_Y||D^s exp(eZbT−D). This is an imported established Lieb–Robinson/quasi-locality theorem; no new propagation bound is claimed here.

For(1), use a=1, b<=2J,1<=Z<=3,M=2 and s=1. The choice s=1 conservatively respects the theorem's positive shell exponent, even though the line's shell count is constant. If the commutator generator is identically zero (including scalar Hamiltonian/global phases), treat the evolution as exactly identity instead of using an undefined Z denominator.

There is an important orientation issue. The primary observable propagator acts as U_H^dagger O U_H, whereas our true logical generators are U_H O U_H^dagger. Apply the theorem to the reversed NEGATIVE Hamiltonian

    H_tilde(t)=−H(T−t).

Its Schrödinger propagator is U_H(T)^dagger, so its primary Heisenberg propagator is the required conjugation. Negating H(t) without reversing its order would generally be wrong for time-dependent noncommuting terms. The local norm/range bounds are unchanged.

## 3. Unknown exact local reflection proxies, no microscopic inverse

For a logical site y and integer D>=4, let V={z:|z−y|<D}. If V is proper, the distance parameter in the theorem is exactly D. The extended bar(V) adds at most one site per side. To include isolated sites possibly omitted by the interaction-defined extension, place the proxy in

    I_D(y)=[y−D,y+D] intersect Lambda,

which contains {y} union bar(V) and has at most min(n,2D+1) qubits. Apply the truncated UNITARY evolution to the initial on-site X or Z. It gives a Hermitian reflection supported in I_D(y), with

    ||B_ji−V_ji||<=tau_D:=4D exp(6eJT−D).               (2)

If V=Lambda, the full and truncated dynamics agree exactly; do not substitute an infinite complement distance into the primary formula. The bound is valid for each axis and every logical site. Since Tr rho=1, it implies Tr rho(B_ji−V_ji)^2<=tau_D^2 for ANY occupied gauge state. Thus no gauge spectral floor or state preparation estimate enters the tail import.

The truncated propagator and its reflections are proof-only witnesses. The learner does not know, simulate or invert them. It learns local CPTP pullbacks and physical controlled reflections from ordinary source records by the received protocol. There is no need to sign-round a truncated contraction in this unitary specialization: conjugation by the truncated unitary preserves reflections exactly. All unknown site assignments are handled by the acquired coarse locator. This is not free cross-frame alignment.

## 4. A finite, pre-outcome width giving global reliability

Fix target0<epsilon,gamma<=1 and0<kappa<=1. The approximate theorem's decoder-regret floor is Delta=7920qA tau^2/kappa, with its final encoder comparison multiplying Delta by1+gamma. Run that theorem with statistical tolerance epsilon_stat=epsilon/2 and choose width so that tau<=kappa/8 and Delta<=epsilon/4. Then its final expected one-payload loss is

    E ell <=(1+gamma)ell_star+epsilon_stat+(1+gamma)Delta
          <=(1+gamma)ell_star+epsilon.                  (3)

Here ell_star is the original unrestricted global CPTP optimum jointly optimized over the SUPPLIED four-coordinate encoder family; it is not an unrestricted encoder optimum.

The following conservative exact-arithmetic choice suffices. Let

    C0=506880*3^12,
    L1=ceil log2(32/kappa),
    L2=ceil log2[C0*q/(kappa epsilon)],
    D_cap=ceil(36B)+max{18,2L1,L2},
    w=min(n,2D_cap+1).                                  (4)

Ceil logarithms of positive rational inputs are computed by integer/power-of-two comparisons; no transcendental source oracle is required. B,kappa,epsilon are supplied rational bounds/tolerances (or conservative rational replacements), and this width is fixed BEFORE any observations. If w=n, choose full-register exact proxies B_ji and tau=0. This is a separate legitimate support choice, not an assertion that an unknown endpoint's radius-D ball necessarily covers the entire chain.

Otherwise D=D_cap and w=2D+1. To verify the floor, use the approximate theorem's

    W=min(n,3w−2), C=min(q,4W−2),
    S=W+2(C−1)(W−1), K=min(q,2S), A=min(q,K^2).

For D>=4,

    S<=8W^2, A<=256W^4<=20736w^4<=3^12 D^4.

Consequently

    Delta<=126720*3^12*(q/kappa) D^6 exp(12eJT−2D).       (5)

For D>=18,6 ln D<=D. Also D−ln D>=D/2. Since e<3, ln z<=log2 z for z>=1 and B>=JT, definition(4) ensures

    D>=12eJT+2ln(32/kappa),
    D>=12eJT+ln[C0*q/(kappa epsilon)].

The first inequality gives tau_D<=kappa/8; the second with(5) gives Delta<=epsilon/4. These estimates are deliberately conservative. They provide a deterministic finite width without fitting a tail parameter, estimating unknown Hamiltonian coefficients, or searching for an accidentally favorable source history.

## 5. Paid resources and the loss of fixed-width linear-q scaling

Substitute(4) into every dimension/width term of the received approximate theorem. In particular eta=epsilon/(32768qA), the four fine state tolerances are m=kappa^2 eta/512, and confidence/whole-process compilation budgets use epsilon_stat=epsilon/2. The complete source cap remains its displayed

    2q cN0+4C c1 N_B+C(R_max−1)N_pair+N_count+1,

with all parameters evaluated at this w and epsilon_stat. The final+1 is the payload. Zero comparison calls when R_max=1; all coarse failures, safe fallbacks, fixed source caps, collective-bank memory and finite control budgets remain. The global encoder test still uses ordinary known q-qubit Clifford/stabilizer inputs and global inverse-Clifford readout, not product marginal tests or a protected source reference.

At fixed w the prior source count was linear in q up to logarithms. That statement CANNOT be carried unchanged into this corollary: w grows to suppress the full qA tail floor. A transparent conservative bound from(4) is

    4^w <= O(2^(144B) * max{2^72,(32/kappa)^8,
                                      [C0*q/(kappa epsilon)]^4}). (6)

Rounding changes only the absolute prefactor. Width polynomial factors C,c1,A,R_max add polynomial factors in B and logarithms of q,1/epsilon,1/kappa. Thus for fixed bounded JT the construction has a finite source/control cap polynomial in q,1/epsilon,1/kappa,1/gamma and n, rather than exponential in n; the1/gamma dependence includes the inherited encoder stage. This is not a linear-q acquisition theorem. Dependence on encoding time/strength remains exponential in this conservative locality-to-dense-tomography construction. If w reaches n, the full-register cost4^n is still charged and bounded by the same4^(2D_cap+1) envelope; it has not become a free global decoder.

Every call consumes q logical input-qubit uses and n physical output exposures, plus the explicit selector preparation/interface (two additional source-input qubits in the literal family above). The q-output learned receiver has local controlled-reflection synthesis, mixed ancillas and restored routing, not Hamiltonian-inverse access. Its3q controls,4q Hadamards and bank-estimator workspace are evaluated at the chosen w. Known n-qubit coordinates and trusted control/storage remain assumptions. All strong equally informed conventional subsystem learners can use this same construction.

A known-Hamiltonian baseline is strictly more informed: when a certified physical implementation of U_H^dagger and the initial assignment is supplied, it can undo that coherent encoding directly, paying its real Hamiltonian simulation/routing cost. No advantage over that baseline is claimed. Conversely this corollary does not require identifying the microscopic H before recovering its logical algebra. Availability under arbitrary noise, generic local Lindbladian recovery, model-membership certification, larger nonconvex encoder families and long-time/non-reset prediction remain open rather than being absorbed into the propagation theorem.
