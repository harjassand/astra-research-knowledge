# Independent audit: exact physical-time consumer in the robust native join

2026-11-02. **PASS of the exact dynamical/initialization/native-coordinate join, CONDITIONAL on the separately audited actual joint-Gibbs bad-syndrome bound and local-protection input.** This receipt does not certify the mixed source/rod static proof.

Audited root: `ROOT_ROBUST_NATIVE_MEMORY_JOIN.md`, SHA256 `d833625e8a392a291071499b3d32d8f52161aeb12754a430ad9f5429f79eda8c`.

## 1. The thermal twirl does not require a commuting reference Hamiltonian

The only Hamiltonian-symmetry premise needed here is [H_ref,Q_mu]=0 for the full-space fixed decoder Pauli algebra. H_ref may be noncommuting within the gauge/ancillary factor. The native construction's exact syndrome-only form H_anc(S)+H_B0 satisfies this premise, including all internal-clock excitations.

Let P_bad commute with every Q_mu, and suppose each actual Hermitian memory-touching perturbation term satisfies [Q_mu,V_j]P_good=0. Hermiticity makes the commutator vanish on the good sector on both sides. Thus

    Delta_mu=Q_mu H_tot Q_mu-H_tot
            =P_bad Delta_mu P_bad,
    ||Delta_mu||<=2 sum_(memory-touching j)||V_j||<=2vn.

For the actual finite-volume Gibbs state rho,

    D(Q_mu rho Q_mu || rho)=beta Tr(rho Delta_mu)
                          <=2 beta vn p,
    p=Tr(P_bad rho).

Pinsker and the exact logical Pauli twirl give

    ||rho_bar-rho||_1<=2sqrt(beta vn p),
    rho_bar=I_L/2 tensor tau_GB.

No use of commuting Gibbs factors, exponential operator monotonicity, a Davies generator or a spectral gap occurs. The substantial static input remains the probability p for the ACTUAL perturbed joint Gibbs state, not the reference Gibbs state.

## 2. Native back-transform and norm budget

U is the fixed finite-depth bounded-range data/internal-clock dressing. A native local perturbation becomes U†V_jU on an enlarged but fixed footprint, with EXACTLY the same operator norm. Its expansion into data Paulis and ancillary matrix units can cost a fixed coefficient factor for the static proof, but that expansion need not be charged again in the dynamical norm budget: group each original Hermitian term before bounding its commutator.

Pure external-bath terms are unchanged by U and commute with all logical operators. They contribute zero to Delta_mu and i[H_tot,Q_mu], even if their total norm or number grows with bath volume. The sum of terms that can affect the native memory/clock region is O(vn) under the fixed range, bounded-density and incidence hypotheses. Here n correctly includes the K=7 clocks and remains within a fixed factor of data size.

Conjugating Q_mu and P_bad back by U preserves their Pauli algebra, projector relations and every norm/probability inequality. The native reference H_nat can have substantial fixed noncommuting two-body terms; they commute exactly with the native dressed logical algebra and therefore do not contribute to the dynamical coefficient. The coefficient is not ||H_nat|| or the total bath Hamiltonian norm.

## 3. Actual-equilibrium initialization and clock access

The incoming xi_LR should be explicitly assumed initially independent of the supplied equilibrium native-memory/external-bath system. This is the ordinary channel-input convention but worth stating.

An ideal physical overwrite can be implemented by applying U† on data and internal clocks, applying the fixed data decoder tensor-factor unitary, replacing/swapping the logical qubit with the incoming input, discarding the old logical factor, and undoing those unitaries. It acts only on native data and internal clocks. It never requires direct access to the external bath.

Applied to the ACTUAL interacting Gibbs state, it retains exactly tau_GB=Tr_L rho, including gauge–clock–bath correlations. The input may be entangled with R; after overwrite the state is xi_LR tensor tau_GB in the decoder frame. No factorized-bath ansatz or knowledge of the unknown perturbation is needed. U and the decoder are fixed by the nominal construction; the supplied actual equilibrium state automatically provides its actual marginal.

This is nonetheless a strong ideal endpoint resource. It does not prove efficient acquisition of joint equilibrium, fault-tolerant encoding, a local-depth-efficient decoder, or preparation without clock access. The root explicitly retains those limitations.

## 4. Physical-time admission and reference-safe constant

Every encoded SYSTEM marginal satisfies E(xi_L)<=2rho_bar. Exact unitary evolution Phi_t under the SAME H_tot is positive and preserves rho. The equal-trace effect bound yields, for every physical time,

    Tr(P_bad Phi_t E(xi_L))
      <=2p+||rho_bar-rho||_1.

This is uniform in time and bath volume; it is not a perturbative comparison of two Hamiltonian evolutions over time T.

A_mu=i[H_tot,Q_mu] is Hermitian, bad-supported on both sides and obeys ||A_mu||<=2vn. For an arbitrary joint reference state, trace-norm duality gives

    ||Tr_native,bath[(A_mu tensor I_R) Omega(t)]||_1
        <=2vn Tr(P_bad Omega_native,bath(t)).

Expanding the decoded L-R state in the three nonidentity logical Paulis gives

    ||d Omega_LR(t)/dt||_1<=6vn p_bad(t).

Integration and the twirl bound therefore give exactly the root estimate

    error(T)<=min{2,6vnT[2p+2sqrt(beta vn p)]}.

No reference-dimension factor is hidden. If p<=poly(n)exp(-c n^eta), then any fixed exponent coefficient c'<c/2, with adequate slack for polynomial factors, gives vanishing error for T<=exp(c' n^eta). This is ordinary Hamiltonian time at fixed microscopic interactions, not Davies-rescaled time or a weak-coupling limit. There is no per-time approximation error from the native gadget: its reference dressing is exact on the full spectrum.

## 5. Finite-bath uniformity and interpretation

All global density operators and traces used above are finite-volume objects. Uniformity follows from the assumed volume-uniform static p estimate plus the O(vn) memory-touching norm budget. Arbitrary ancilla/bath eigenstructure, bath equilibration rates, recurrences and absence of Markovianity do not enter this consumer.

If an infinite-bath statement is later desired, use consistent finite-range interactions, a subsequential local equilibrium limit and local Hamiltonian dynamics at each fixed finite n and time. Do not write an infinite Gibbs density matrix or global infinite-volume trace distance. The present root only needs its stated uniform finite-bath family.

The bath-only interactions in V remain within the small local-strength class required by the STATIC theorem. Their cancellation from logical commutators does not independently authorize an arbitrary strongly interacting bath reference.

## 6. Generic V versus native two-body hardware

The root correctly distinguishes two statements:

- H_nat is a native onsite/two-body model on data qubits and fixed seven-level spins, allowing the specified general Hermitian qubit–qudit couplings.
- The mathematical robustness proof permits any sufficiently weak bounded-body finite-range V in a fixed local-norm/decomposition class.

To retain strictly two-body physical Hamiltonians, restrict V to its generic native two-body subclass; that is already covered. Allowing higher-body perturbations does not magically implement those terms with two-body hardware. “Open region” should mean an open neighborhood within the stated fixed range/body/dimension/local-norm parameter class, not robustness to unbounded support or arbitrary external noise.

Generic symmetry-breaking V is permitted by the consumer because only its local action on the good sector is used. Exact [H_tot,Q]=0 is NOT required. Exact calibration of V is unnecessary for the stipulated overwrite/decoder, while sufficient smallness and the actual-Gibbs static bound remain essential. Neither conclusion covers generic noisy loading or adversarial time-dependent controls.

## 7. Decision boundary

No resource or consequence overstatement was found in the physical-time consumer once the above explicit input-independence and parameter-class conventions are retained. The root's ideal actual-Gibbs initialization, clock access, restricted bounded-spin bath, fixed finite-temperature window and nonpractical constants are real limitations, not cosmetic caveats.

The accepted result of THIS audit is only: the stated static/protection premises imply the displayed exact physical-time native memory channel bound. No judgment about the correctness of Sections 2–3's mixed-source construction is made here; that is the separate static auditor's task. No external sources or actions were used for this algebraic audit.
