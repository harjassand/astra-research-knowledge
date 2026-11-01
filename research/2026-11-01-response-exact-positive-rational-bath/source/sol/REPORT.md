# First-turn scientific return: response-exact positive rational bath hierarchy

I developed a concrete mathematical primitive for simulating a gapless quantum continuum with a finite valid quantum channel. The result is narrower than a revolutionary scientific foundation: **an explicit, unconditional construction for one zero-temperature Ohmic family, with exact free-bath dissipative response, monotone control of added noise, selected thermal zeros, a complete-channel error bound, and a paid oscillator cutoff**. Novelty and advantage over the strongest existing methods remain UNKNOWN. No second research worker was used, and this new proof has not received an independent review.

## Consequential objective and operation actually earned

The selected objective is reliable finite-memory simulation of quantum systems with genuinely long-lived continuum environmental correlations. Full success would support controlled quantum materials, chemistry and open-system computation in regimes where a Markov approximation, an assumed mixing gap or a bath fit with unphysical negative weights is inadequate. It would not solve arbitrary many-body Hamiltonian simulation or supply an experimentally unknown spectral density.

The hard operation was to acquire a physically valid compressed bath, rather than assume the very pseudomode decomposition being invented. I fixed the objective and attempted accumulated-influence compression before retrieving Astra or the literature; the original record is `ORIGINATION.md`.

The actual input family, in dimensionless units, is

    S_*(w)=alpha (|w|+w)/(1+w^2)^2, alpha>0.

The system has arbitrary finite-dimensional H_S(t), a bounded Hermitian coupling Q, a factorized Gaussian bath state and, optionally, system interventions at prescribed times. The complete reduced channel, including an arbitrary reference, is the output. No RWA, weak-coupling approximation or supplied spectral gap enters the channel-error theorem. The explicit analytic spectrum is an acquired finite-description input; measurement/model uncertainty is a separate unearned task.

## The central mechanism

For any positive nodes a_k, define P(x)=product(a_k+x) and

    r_n(x)=x [P(x)^2+P(-x)^2]/[P(x)^2-P(-x)^2],
    S_n(w)=alpha [r_n(w)+w]/(1+w^2)^2.

The value at0 is removable. An elementary product identity proves r_n(x)>=|x| for every real x. It follows that S_n is a globally nonnegative rational spectrum, with three simultaneous exact properties:

1. **Free-bath response is exact:** S_n(w)-S_n(-w)=S_*(w)-S_*(-w), hence Im C_n(t)=-(alpha/4)t exp(-t), exactly the target commutator.
2. **The entire error is classical:** S_n-S_* is even and nonnegative. It is precisely an independent stationary real Gaussian Hamiltonian noise, not a signed measure.
3. **Thermal nodes are exact and refinement is monotone:** S_n(-a_k)=0 and S_n(a_k)=S_*(a_k). Adding a positive node reduces the excess spectrum everywhere and inserts another cold zero without refitting. These are weak-coupling rate statements at the selected frequencies, not an exact finite-coupling thermal generator; coherent Lamb shifts and multi-quantum processes are not thereby fixed.

A stable spectral factor and its controllability Gramian construct a genuine coupled Lindblad realization with at most n+1 oscillator modes. No SDP-feasibility or fitted-mode oracle is an input. For an odd repeated reciprocal dyadic node grid, I also derived pole-separation and confluent-Cauchy Gramian bounds that give finite-bit synthesis with polynomial arithmetic and guard bits in the logarithmic range parameters. Whitening is a realization of a new canonical oscillator network, not an illegal nonunitary canonical change of existing physical oscillators.

The simplest exact realization has two modes:

    A=[[0,1],[-1,-2]], ell=(0,2)^T,
    c=sqrt[alpha/(2a)](-ia,1)/2,
    A+A^dagger=-ell ell^dagger,
    C_1(t)=alpha exp(-t)[1+a^2+(a^2-1-2ia)t]/(8a).

Its spectrum is alpha(w+a)^2/[2a(1+w^2)^2]. Use the jump ell^dagger b, number-preserving one-particle Hamiltonian H=(i/2)(A-A^dagger), and coupling Q(c b+b^dagger c^dagger). This is a valid CPTP simulator. H has positive and negative eigenvalues: it is a driven/synthetic representation, not a claim of an equilibrium positive-energy material reservoir. Finite qubit encoding and reset/control energy still have to be paid.

## Proof and executable discriminator

For endpoints delta=2^-L, Lambda=2^L, with at least m nodes within a factor two of every interior frequency, the added classical variance satisfies

    sigma_n^2 <= alpha/pi [2*4^-L + 3^-2m/(1-3^-2m)].

Coupling the target and approximate models through that actual extra Gaussian process and applying Duhamel gives, uniformly for t<=T,

    ||Phi_n(t)-Phi_*(t)||_diamond
       <=min(2, 2||Q||T sqrt(2/pi) sigma_n).

This proof holds for noncommuting system dynamics, references and prescribed-time instruments. It does not rely on a favorable dephasing fixture. Thus O(log^2[1+||Q||T sqrt(alpha)/epsilon]) modes suffice for this family.

I then derived factorial occupation bounds for the actual driven quantum process, including arbitrary number-preserving auxiliary couplings and passive linear damping:

    E[(N)_k] <= (||Q|| ||c|| t)^(2k).

For lambda=(||Q|| ||c||T)^2, cutting total Fock occupation at K incurs at most

    2||Q|| ||c||T sqrt(K+1) sqrt(lambda^K/K!)

in complete-channel error. A finite-cutoff Cauchy argument defines the canonical infinite-Fock vacuum process without assuming uniqueness of every formal unbounded GKSL extension. Binary encoding costs O(n log(K+1)) bath-register qubits. Finite-bit coefficient synthesis, oscillator boundary tests, H_S/control implementation and digital Lindblad evolution are additional costs.

The tests actually executed are in `results/`:

- Three exact symbolic two-mode identities; eight positive rational approximations with the proved variance inequality, exact response and exact thermal-node tests.
- Four explicit 2-,4-,6-,8-mode passive Lindblad realizations checked at 65 decimal digits. The largest reported physical-realizability residual was about 4.9e-61. Two additional 10- and16-mode repeated reciprocal-grid realizations passed at 100 decimal digits, including the explicit pole-separation inequalities; their Gramian condition numbers were about 6.1e10 and 2.2e15. This is a finite arithmetic check, not an independent mathematical audit.
- A noncommuting qubit test H_S=.7 sigma_z+.31 sigma_y, Q=sigma_x, alpha=.2, T=2. The finite channel difference upper bound from K=5 to a refined K=6 reference was 8.85e-10; step refinement changed the normalized-Choi-based channel upper bound by 4.64e-12. These test the two-mode generator and cutoff, not universal continuum accuracy or practical advantage.
- An exact positive two-quantum scattering integral, described next.

## Failures that fix the claim boundary

The initial mechanism used independent positive damped modes. Their spectrum is a positive sum of Lorentzians and has strictly positive zero-frequency noise. In dephasing, their eventual integrated influence is linear rather than the target logarithm. They cannot cancel that contribution. This killed the uniform accumulated-influence idea, while leaving horizon-dependent fitting possible. Interference between coupled modes was a materially different positive mechanism.

Exact thermal zeros also fail to make an all-order cold reservoir. With nodes {1,2}, an anharmonic qutrit with energies {0,1,3} has both adjacent one-quantum upward rates exactly zero, yet a positive two-quantum on-shell upward channel survives. The explicitly simplified spectral weight integrates to

    3.3036379974411842e-5  (alpha=1; fixed positive rate prefactor omitted).

Even its restricted nonresonant window [1/4,3/4] contributes 6.0351283047297066e-6. This is an allowed outgoing-channel discriminator, not a nonperturbative lifetime. An initially tried equal-spaced qutrit cancelled the two denominators and was rejected; the successful example's anharmonicity is load-bearing. See `TWO_QUANTUM_OBSTRUCTION.md` and `two_quantum_check.py`.

There is also a decisive analytic boundary: a nonzero finite rational spectrum cannot satisfy exact global finite-beta KMS, nor vanish on the entire negative half-line at zero temperature. The approximation must retain a finite horizon/accuracy contract.

## Strongest comparators and what is different

**Coupled Lindblad physicality is established prior machinery.** [Huang-Park-Chan-Lin, arXiv:2506.10308v2](https://arxiv.org/html/2506.10308v2), equations 2-8 and Theorem 1, gives the relevant CP coupled-mode framework, a conditional feasibility theorem and robust SDP/frequency-domain construction. It already provides theoretical evidence and numerical examples of polylogarithmic mode counts. I do not count CP coupled modes, passive realization or the broad polylogarithmic ambition as new. The candidate distinction is the explicit unconditional exact-response/positive-excess/thermal-interpolation conjunction for this family. Their algorithm can reuse this primitive as a guaranteed feasible input; that reuse would not erase the construction's credit, but historical priority still requires checking.

**Unconstrained exponential compression has stronger general results than the initial framing assumed.** [Huang et al., arXiv:2603.25708v1](https://arxiv.org/html/2603.25708v1), Assumption 1, Theorem 1 and Corollary 2, establishes rigorous L1-correlation complexity across spectral singularities. Its conclusion explicitly leaves analogous physical coupled-Lindblad constraints as a further question. A fixed kernel-error tolerance is not a fixed complete-channel error at arbitrarily long T. The present family is a partial constructive answer with an explicit different norm conversion; it is not the general spectral-singularity theorem.

**Global positive low rank is another competing physical mechanism.** [Chen-Cai, arXiv:2610.29372v1](https://arxiv.org/html/2610.29372v1), sections 3-5, constructs finite-rank Gaussian baths, pays occupation cutoff/dilution and gives polynomial circuits under stated access/regularity assumptions. That prevents promoting the initially considered whole-kernel low-rank route as an invention. The present hierarchy preserves stationarity through coupled damping and exact response rather than a whole-window eigenbasis.

**Thermal consistency is a separate operation.** [Kessing et al., arXiv:2608.02517v1](https://arxiv.org/html/2608.02517v1), sections 1.3, 2 and 4, analyzes frequency-dependent effective temperature and limited-frequency detailed balance. Its distinctions reinforce the finite-horizon/weak-rate boundary; the new two-quantum calculation makes that boundary explicit for the actual constructed bath.

The product approximation motif is classical [Newman (1964)](https://people.math.ethz.ch/~hiptmair/Seminars/RAP_22/NEW64.pdf), and passive linear quantum realization is established [Gough-Zhang, arXiv:1311.1375v2](https://arxiv.org/html/1311.1375v2), section 3.1. No novelty is assigned to those ingredients.

## Complete costs: what the mode count does and does not buy

These are conservative **proved budget choices**, with alpha=.2, ||Q||=1. One third of requested error is reserved for the kernel approximation, one third for the Fock cutoff, and one third remains for coefficient/digital implementation. Bath qubits exclude the system, workspace and implementation ancillas. These are not optimized engineering estimates.

| T | Total requested error | Modes | Total Fock cutoff K | Bath register qubits | Kernel + cutoff bound |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.1 | 34 | 2 | 68 | 0.03727 |
| 10 | 0.1 | 86 | 17 | 430 | 0.04284 |
| 100 | 0.1 | 176 | 882 | 1760 | 0.0493 |
| 100 | 0.01 | 280 | 887 | 2800 | 0.004724 |
| 1000 | 0.001 | 676 | 86559 | 11492 | 0.0003537 |


All frequency nodes and mode parameters are computed from explicit finite inputs. The resulting one-particle H and damping norms are bounded polynomially in T/epsilon, while the coupling variance remains bounded. Ordinary finite sparse Lindblad simulation therefore supplies a polynomial-cost completion when the actual system operators are implementable. **There is no demonstrated full-cycle speedup:** a generic implementation can pay a large polynomial penalty for the fastest auxiliary rates and the Fock cutoff. Observable estimation adds its own repetitions. The numerical fitting baseline may also need far fewer modes than this conservative proof choice.

At matched input/output scope, the strongest ordinary pipeline is the coupled-Lindblad model acquisition of Huang-Park-Chan-Lin followed by the same finite Lindblad channel simulator, the same oscillator cutoff and the same observable-readout budget. Its numerical realization can be much smaller than this conservative construction. Once either pipeline has acquired the same final H,ell,c, their downstream simulation costs are identical. The prospective new primitive is acquiring a guaranteed response-exact feasible model from the analytic input, not replacing an ordinary consumer that can reuse it. No source or kernel is granted to one side for free.

Astra search identified a useful receiving gap. **N1510 has an actual completed internal mathematical review and remains accepted at that scope:** its final receiver is SHA 494742b2..., with the repaired Dyson phase. It compiles independent positively damped modes with diagonal number frequencies, supplied system encodings and private retained memory. The new interference bath instead has off-diagonal H and rank-one loss. Nonunitary drift diagonalization is not a canonical bosonic coordinate change. Consequently I have not silently received its logarithmic microscopic-rate cost for this different interface. N675 correctness was not reopened.

The relevant scoped Astra notch failure N1128 was read with its actual review and restrictions. It supplied a useful warning, not a theorem automatically applicable to the new qutrit. N710's elementary Duhamel noise comparison was independently reconstructed; its larger finite-seed compiler remains source-derived/unreviewed. Exact pinned source routes, all hashes, current notices and review boundaries are preserved in `SOURCES.md` and `source_receipts.json`.

## Best second-turn continuation

The evidence supports continuing one hard operation: **a rate-robust retained-memory compiler for the actual coupled Gaussian bath**, using its exactly computable free Gaussian channel while preserving the noncommuting simultaneous interaction and lost-field coherences. The free channel itself can be dilated using exp(At), its singular values and fresh vacuum modes; this is an earned established subroutine, not the full simulator. Naive splitting still pays the fast generator, and a nonpositive inverse dissipative interaction picture is not available. A Dyson/LCU expression without efficient complete-isometry normalization would simply move the hard operation into an assumed source.

A narrow priority check should run alongside that work: whether response-preserving rational upper envelopes with freely insertable exact thermal nodes and this full-channel certificate already appear in passive-network/quantum-Brownian-bath literature. If they do, credit the existing primitive and assess the compiler opening directly. If they do not, the explicit construction is still a mathematical primitive before any practical advantage. The general finite-temperature, non-Gaussian and measured-bath problems are not solved here.
