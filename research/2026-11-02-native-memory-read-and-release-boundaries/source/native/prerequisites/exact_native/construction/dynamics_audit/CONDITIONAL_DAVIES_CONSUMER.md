# Conditional dynamical consumer for the exact clock-dressed native model

2026-11-01. **PASS-CONDITIONAL: the stipulated rare crossing-witness Gibbs estimate gives a stretched-exponential thermal-encoding memory bound for bounded-rate local-contact Davies dynamics. There is no additional global secular obstruction in this EXACT syndrome-only Hamiltonian.** This does not prove the ancillary Gibbs estimate, exact microscopic bath dynamics, or generic perturbation robustness.

Bindings:
- `independent_constructor.md`: SHA256 `5c8200818c8cc3c1612fc0628c8181ad6ce99a0450af17e961f27008b01f4be1`.
- `ROOT_EXCURSION_PROOF_TARGET.md`: SHA256 `b97a54e94ad715c0927252a6af10570f67c449ded3b7de9ad3793a6d327604c4`.

## Established criterion and originality boundary

This consumer belongs to the established Chesi–Loss–Bravyi–Terhal thermal criterion, not a new memory principle. Their arXiv:0907.2807v2, Sections 6–7, treats corrected logical observables, Gibbs thermal encoding, and bad-syndrome probabilities for stabilizer/subsystem memories. The discussion before Proposition 1 explains why energy Fourier projection preserves protection; Proposition 1 controls generator strength without counting Bohr frequencies; Eq. (39) gives the corresponding lifetime scale. Primary source inspected: https://arxiv.org/pdf/0907.2807 . The proof below independently binds that mechanism to the clock construction's exact ancilla algebra and gives a reference-safe channel estimate. No claim is made that the cited work proves the missing clock free-energy/witness premise.

## 1. Precise assumptions and decoder frame

Work first in finite volume and apply the exact finite-depth dressing U. The native Hamiltonian becomes

    H = sum_s P_s tensor H_a(s),

where s ranges over allowed COMPLETE data syndromes, and H_a(s) is arbitrary on all ancillary clocks. Each data sector carries one logical qubit. Fix the original syndrome decoder isomorphism D on data, with exact corrected logical Pauli algebra Q_X,Q_Y,Q_Z. These are syndrome-dependent operators, NOT just the bare logical Pauli strings. Since H has no logical dependence inside any sector,

    [H,Q_mu]=0,
    [H,P_good]=0,
    [Q_mu,P_good]=0.

Take P_good=sum_{s good}P_s tensor I_a. Its complement must be the original decoder bad set enlarged sufficiently to protect the entire data operator algebra on every dressed contact footprint X. Thus for all data Paulis P supported in X,

    [Q_mu,P] P_good=0.

This is a code/witness-correctability premise. For bounded footprint size it can be obtained by the previously used Pauli-prefix enlargement, IF the hypothesized Gibbs witness estimate includes that enlargement. Mere locality or bare logical symmetry is not a substitute.

The present audit assumes the actual traced Gibbs law supplies

    p_n = Tr(P_bad rho_beta) <= poly(n) exp(-c n^eta),
    rho_beta=exp(-beta H)/Z.

This p_n includes ALL ancilla levels and their true conditional Gibbs weights. It does not require a vacuum ancilla approximation or an ancilla gap/mixing assumption.

Native physical contacts B_nu of bounded support become A_nu=U†B_nu U with a fixed enlarged data footprint X_nu and bounded ancilla support. Their norm is unchanged. Assume independent bath channels with nonnegative Davies rates 0<=g_nu(omega)<=g_nu,max and total charged strength

    Gamma = sum_nu g_nu,max ||A_nu||^2 = O(n).

Bounded-size local correlation blocks of bath contacts can be included by enlarging the footprint and charging the rate-matrix norm. An arbitrary dense collective bath rate matrix is NOT implied by this hypothesis.

## 2. Fourier components can be globally supported, but retain a protected algebra

Because H is syndrome-only, every exact energy spectral projector has the form

    Pi_E = sum_s P_s tensor pi_E(s),

where pi_E(s) is the full eigenspace projector of H_a(s) at energy E, possibly zero. Degeneracy, delocalized ancilla eigenvectors, overlapping ancillary spectra and tiny level spacings cause no problem. Pi_E is identity on the logical qubit within each sector.

For a fixed data footprint X define the finite-volume algebra

    A_X = span { P_X P_s tensor B : P_X a Pauli on X,
                                    s allowed,
                                    B any operator on all ancillas }.

This is a *-algebra: a data Pauli translates the syndrome projector, products of two X-supported Paulis remain X-supported, and ancillary coefficients can be multiplied in their actual order. This algebra is not spatially local on the ancillas; that is intentional.

The local contact A_nu lies in A_Xnu. Multiplication by any Pi_E on either side preserves A_Xnu. Consequently every Davies Fourier component

    A_nu,omega = sum_{E'-E=omega} Pi_E A_nu Pi_E'

belongs to A_Xnu, as do its adjoint and A_nu,omega† A_nu,omega. In particular it may change syndrome, but only via X_nu-supported Pauli shifts. It does not acquire a new logical action merely because its ancillary coefficient becomes nonlocal.

The diagonal-syndrome ancillary coefficients commute with Q_mu and P_good. The original full-footprint Pauli protection therefore extends to EVERY T in A_Xnu:

    [Q_mu,T]P_good=0.

This explicitly keeps the changed output syndrome and the fixed input decoder frame consistent. Protection is evaluated at the input syndrome; the Pauli's output frame is accounted for by the original decoder identity, not by pretending the syndrome is unchanged.

This argument also handles the full dissipator product requirement. With J=A_nu,omega,

    [Q,J]P_good=0,    [Q,J†J]P_good=0,

and [Q,P_good]=0 imply

    D_J^*(Q) P_good=0.

Since D_J^*(Q) is Hermitian, it vanishes on the other side too. Thus D_J^*(Q)=P_bad D_J^*(Q)P_bad. No unsupported inference from the jump commutator alone is used.

## 3. Frequency sums have no exponential counting factor

Use the genuine Bohr-frequency components, with the entire exactly degenerate block retained. Orthogonality of energy projectors gives

    sum_omega A_omega† A_omega
       =sum_E Pi_E A†A Pi_E <= ||A||^2 I.

This is exact regardless of the number of frequencies or their degeneracies. Hence

    0 <= sum_omega g(omega) A_omega†A_omega
       <= g_max ||A||^2 I.

The completely positive map Q -> sum_omega g(omega) A_omega†Q A_omega has operator norm at most g_max||A||^2 on ||Q||<=1. Its anticommutator contribution has the same bound. Summing contacts yields

    ||L^*(Q_mu)|| <= 2 Gamma,
    L^*(Q_mu)=P_bad L^*(Q_mu)P_bad,

for the dissipative part. The H commutator vanishes identically.

A Davies Lamb shift can also be included IF its coefficients satisfy a separately charged bound |h_nu(omega)|<=h_nu,max with sum_nu h_nu,max||A_nu||^2=O(n). Its terms sum h_nu(omega)A_nu,omega†A_nu,omega lie in the same protected algebra, commute with H, and add at most twice that strength to the logical derivative norm. Bounded dissipative rates alone do not automatically prove a bounded Lamb-shift Hilbert transform. Either omit the Lamb shift by the stated model convention or bound it explicitly.

It is incorrect to replace the coherent sum within one degenerate frequency by arbitrary independent rank-one eigenvector jumps that resolve the logical degeneracy. That would be a different bath model, potentially measuring the logical qubit. Correct Davies secularization does not perform that extra measurement.

## 4. Exact thermal encoding and reference-safe lifetime

In the fixed decoder tensor decomposition,

    H=I_L tensor H_Ga,
    rho_beta=I_L/2 tensor tau_Ga.

The gauge factor includes syndrome and all clocks and need not be a product or classical ancilla state. Define the ideal thermal encoding

    E(xi_LR)=xi_LR tensor tau_Ga

and decode by the same fixed logical factor. In native coordinates conjugate the encoding by U and undo U before terminal data decoding. Clock access at these ideal endpoints is part of the interface; no cheap or noisy preparation theorem follows. This is an exact Gibbs overwrite, with no approximate twirl step.

Assume the Davies generator is genuinely Gibbs-stationary at the same beta (the standard KMS-compatible rates ensure this). Every encoded SYSTEM marginal satisfies E(xi_L)<=2rho_beta. Positivity of the semigroup and stationarity imply uniformly for all t,

    Tr(P_bad omega(t))<=2p_n.

For arbitrary reference entanglement, let B_mu(t) be the partial trace against L^*(Q_mu). Reference trace-norm duality and two-sided bad support give

    ||B_mu(t)||_1<=2Gamma Tr(P_bad omega(t)).

The logical Pauli expansion, with its identity coefficient constant, then gives

    ||d xi_LR(t)/dt||_1<=6Gamma Tr(P_bad omega(t)),
    ||(Dec o exp(TL) o E tensor id_R)(xi_LR)-xi_LR||_1
        <=12 Gamma T p_n.

If a Lamb shift is charged, replace Gamma by the sum of dissipative and Lamb-shift strength budgets. Bounds may be clipped at two. With Gamma=O(n) and the assumed p_n, times exp(c' n^eta) with sufficiently reduced c'>0 have vanishing error, including entangled inputs.

The argument requires no spectral gap or rapid mixing of the Davies generator and no rapid preparation of rho_beta. It is a lower bound on retention from the stipulated thermal encoding, not an equilibration theorem.

## 5. Why the earlier generic secular warning does not apply here

The decisive property is EXACT full-spectrum independence from the decoded logical qubit, together with exact conservation of every syndrome projector. Arbitrary ancillary eigenstructure can only create syndrome-controlled bath coefficients in the Fourier jumps. Logical dependence cannot be generated by energy resolution, and the operator-algebra closure handles the anticommutator products.

A generic noncommuting perturbation that destroys this exact structure is a different problem: its energy projectors can resolve or rotate logical information, and this proof does not survive by continuity without additional control. Approximate low-energy gadget simulation would also be insufficient for the full-spectrum argument.

The bound is for the specified Davies semigroup, with its chosen rate/time normalization. It does not establish a uniform finite-coupling microscopic derivation of Davies dynamics over exponential memory times. It is not the earlier exact autonomous spin-bath theorem, and cannot be advertised as arbitrary physical-noise robustness.

## 6. Remaining bottleneck and decision

Assuming the exact dressing identity and the actual-code enlarged crossing-witness probability, the dynamical consumer is closed under the precise bounded-rate local-bath hypotheses above. There is no extra ancilla-eigenstructure or frequency-counting obstruction. The genuinely missing construction gate remains the FULL-temperature, volume-uniform ancillary free-energy/witness estimate identified by the root. This receipt does not prove the proposed temporal excursion expansion or certify its low-temperature convergence.

The only external source inspected for this audit was the successfully retrieved primary CLBT paper named above; no inaccessible source workaround or external action was used.
