# Independent finite-width, error and cost transfer audit

28 October 2026. Auditor: `producer-workspace/audit_algebra_extraction`.

This independent derivation connects an explicitly received unitary locality import to the immutable approximate-locality recovery theorem. It does not derive a new Lieb–Robinson theorem, simulate an unknown Hamiltonian, or sample a source. The primary import is received through `nearest_neighbor_hamiltonian_locality_import_controls_audit_20261028.md` and its receipt; all four manifest bindings were checked. The approximate theorem is `ordinary_approximately_local_joint_recovery_20261028.md`, SHA `1ae8d8f836d366268a4c8f182b9c8b679ba77aea9fde5ebe669e5e576ad74c4d`; all13 bindings in its independent receipt were checked.

## 1. Structural import and hidden placement

The imported local-unitary result supplies local Hermitian reflection proxies on width

    w=min(n,2D+1),  tau_D=4D exp(6eJT−D),  integer D>=4.

Its scope is the stated grouped-edge nearest-neighbor Hamiltonian model on a known open line, not generic local dissipation. The received primary review pays the extended truncation region, positive shell exponent, reversed NEGATIVE Hamiltonian for time-dependent conjugation orientation, isolated/full-chain/zero-generator cases and the unknown nature of the witnesses. The proxy is obtained from a truncated UNITARY, so it really is a reflection without a new sign-rounding assumption.

Each original logical factor must occupy one unknown DISTINCT initial physical site, with the remaining factors gauge, before that local evolution. Arbitrary unknown global encoding before the evolution would not satisfy this implication. The assignment can remain hidden: ordinary coarse localization uses the input logical labels to acquire physical envelopes. No unknown Hamiltonian term, inverse, gauge basis or cross-frame alignment is delivered to the learner. Pauli/gauge structure, aggregate margin, global identity dominance and independent reset calls remain separate assumptions.

If the chosen supplied width is n, the exact global true generators are valid full-register proxies with tau=0. This is a separate proof choice, not a claim that a radius-D ball around an unknown endpoint covers every site. Its full4^n cost remains charged.

## 2. Width and error arithmetic

For the approximate theorem define W=min(n,3w−2), C=min(q,4W−2), S=W+2(C−1)(W−1), K=min(q,2S), A=min(q,K^2). Since W>=1,

    S<=W+2(4W−3)(W−1)=8W^2−13W+6<=8W^2,
    K<=16W^2,
    A<=256W^4<=20736w^4.

For D>=4, w<=2D+1<=(9/4)D and20736(9/4)^4=3^12. Thus A<=3^12 D^4. Consequently the decoder-regret floor obeys

    Delta=7920qA tau_D^2/kappa
         <=126720*3^12*(q/kappa)D^6 exp(12eJT−2D).       (A)

No factor from the final encoder comparison has yet been discarded: the final approximate theorem multiplies Delta by1+gamma.

The logarithm inequalities are elementary. The exponential series gives e>8/3 and(8/3)^3>18, so ln18<3. For D>=18, D−6lnD is positive at18 and increasing thereafter. Therefore6lnD<D. Also D−lnD>=D/2 for D>=18. The previously proposed real-valued sufficient cap

    ceil max{18,12eJT+2ln(32/kappa),
                  12eJT+ln[506880*3^12 q/(kappa epsilon)]}

is mathematically valid. Implementing its exact transcendental comparisons is unnecessary, because the following stronger rational cap removes them altogether.

## 3. A fixed exact-rational cap

Let B be the supplied nonnegative rational upper bound on JT, with0<kappa,epsilon<=1 rational (or conservative rational replacements). Put

    C0=506880*3^12=269376814080,
    L1=ceil log2(32/kappa),
    L2=ceil log2[C0 q/(kappa epsilon)],
    D=ceil(36B)+max{18,2L1,L2}.

All quantities are finite integers/rationals. The ceil-log2 values can be obtained exactly by comparing the integer numerator with the denominator times powers of two. No unknown-source information or transcendental equality oracle is involved. The width and all acquisition horizons are fixed before any source outcomes.

Because e<3 and ln z<=log2 z for z>=1,

    D>=18,
    D>=12eJT+2ln(32/kappa),
    D>=12eJT+ln[C0 q/(kappa epsilon)].

The visibility bound follows from

    tau_D=4 exp(6eJT−[D−lnD])
          <=4 exp(6eJT−D/2)<=kappa/8.

Using6lnD<=D in(A) gives

    Delta<=126720*3^12*(q/kappa) exp(12eJT−D)<=epsilon/4.

A purely rational certificate after the analytic reductions is even simpler:

    tau_D<=4*2^(−L1)<=kappa/8,
    Delta<=126720*3^12*(q/kappa)*2^(−L2)<=epsilon/4.

Here D>=36B+2L1 and D>=36B+L2, with e>=2, justify these looser bounds. Neither tau_D nor e need actually be evaluated by the learner.

Run the approximate theorem at epsilon_stat=epsilon/2. For0<gamma<=1,

    epsilon_stat+(1+gamma)Delta<=epsilon/2+2(epsilon/4)=epsilon.

The global oracle comparison is therefore preserved with the claimed total tolerance. The full-n exact choice only improves this floor.

## 4. Explicit local-dimension and finite-control cost

Write z1=32/kappa and z2=C0 q/(kappa epsilon). Since2^ceil(log2 z)<=2z,

    4^w<=4*16^D
       <=64 exp(36B ln16)
          max{16^18,(64/kappa)^8,[2C0 q/(kappa epsilon)]^4}.  (B)

The manuscript's big-O bound with2^(144B),2^72,z1^8,z2^4 differs only by an absolute prefactor. Thus it is valid. All other received width factors are polynomial in B and logarithms of q,1/kappa,1/epsilon. The source cost still has an OUTER q and the stated dimension/width/confidence factors. This is not a linear-q acquisition corollary.

The correct fixed-parameter statement fixes the SUPPLIED upper bound B, not merely the unknown actual product JT: an arbitrarily loose B can make the chosen width large even for small actual JT. For fixed bounded B, all local Hilbert-space dimensions and their fixed powers are polynomial in q,1/epsilon,1/kappa. The inherited encoder acquisition adds1/gamma dependence. Physical register routing, memory and input/output traffic add polynomial n dependence. The source is still charged for q logical inputs and n output exposures per call; the literal four-dimensional selector source adds two prepared selector qubits per call.

Local selected-reflection synthesis has the inherited polynomial(w)4^w cost before precision. Spectrum comparisons can act on a union of up to2w qubits and hence pay a16^w dense synthesis factor; this too is polynomial after(B), but must not be confused with4^w or claimed to have the same polynomial degree. Collective Bures circuits, their full copy banks and routing, known-coefficient SDP optimization/repair, global Clifford control and all finite random-bit caps remain the received paid primitives.

Let G be a predetermined worst-case cap on these known operations, including bad histories and the payload. Allocating whole-process discrepancy nu=O(epsilon_stat) over this cap requires per-operation error O(nu/G), so gate-approximation bit accuracy scales with log(G/nu), with the inherited known-matrix conditioning factors. The regularized Choi optimization and finite backward spectral controls have explicit polynomial-bit margins in d and inverse target tolerance; no source spectral gap or gauge eigenvalue enters. The Hamiltonian can be unknown and is never numerically simulated by this learner. This is an inherited native finite-gate model statement, not a hardware fault-tolerance or constant-memory claim.

## 5. Nonvacuous family and strongest comparator

The manuscript's literal family with branch pI=(1,4/5,3/4,7/10), an unknown real orthonormal selector basis and arbitrary branch gauge densities satisfies every Pauli aggregate contrast H_P>=(2/5)G and G_I>=G_alpha termwise for all x. The nonidentity probabilities may be globally correlated. The unknown first selector direction is perfectly correctable. Every other branch has pI<1, so the unrestricted decoder's identity-dominance optimum is smaller; no gauge floor is needed. Replacing its shallow circuit by the local-Hamiltonian promise preserves these facts while changing locality from exact to quantitative.

The independent prescribed-matrix check uses a different concrete family, pI=(1,9/10,17/20,4/5), with four noncommuting gauge states, one rank deficient and one having eigenvalue1/1000. It verifies a3/5 margin and the unknown unique perfect selector direction through an exact4x4 quadratic matrix. This is family consistency evidence, not acquisition data. Arbitrarily small positive gauge weights can replace1/1000 without changing the argument. Local Hamiltonians with noncommuting adjacent terms and an unknown injection of the logical sites provide genuine hidden controls; the learner is not supplied their coefficients.

An equally informed conventional learner can run this same procedure. A baseline given the actual Hamiltonian inverse AND initial assignment is strictly more informed and may undo the coherent encoding directly, paying its implementation cost. No advantage over either baseline is claimed. The encoder optimum is only over the supplied four-real-coordinate family.

## 6. Deterministic checks and review boundary

`local_hamiltonian_transfer_cost_independent_check_20261028.py` checks432 exact rational parameter cases:250 use the full-support exact fallback and182 retain a proper local width. It verifies every finite cap, safe visibility/floor certificate, width inequality and explicit dimension bound; maximum checked D is435. It also verifies the prescribed noncommuting-gauge selector fixture and exact base constants. The script was rerun with byte-identical JSON output.

Zero source calls, RNG draws, Hamiltonian simulations or acquisition experiments were performed. Finite cases supplement, not replace, the analytic inequalities. This audit receives the imported propagation theorem from the separately bound primary-controls review rather than claiming an independent literature verification. All earlier received sources remain immutable.
