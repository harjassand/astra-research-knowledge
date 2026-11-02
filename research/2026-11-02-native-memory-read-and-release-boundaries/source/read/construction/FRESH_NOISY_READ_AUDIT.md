# Fresh independent audit of noisy terminal READ

2026-11-02. Audited `NOISY_TERMINAL_READ_THEOREM.md`, including its normalized Bell-channel appendix and destructive classical-read corollary. This review uses the already established actual native Gibbs ratio, actual-code witness enumeration and fixed-decoder stability premises. It does not infer a service-noise model from equilibrium storage.

## Verdict

**The partial-occupancy argument, support-wise operator-algebra threshold, normalized quantum extraction, and stored-state comparison survive independent audit.** The result is a conditional TERMINAL READ theorem, not a noisy WRITE theorem or a proof that the native hardware supplies the assumed access controls, reliable Bell resource and classical/output apparatus.

One resource-interface clarification is required for a fully reference-safe statement: epsilon_Bell must bound the released resource/induced channel jointly with the stored input and reference, or resource preparation must be independent of that state with the stipulated trace-distance error. Marginal resource fidelity alone is insufficient in the presence of uncontrolled correlations with the stored bath. This was reported promptly to the root. Merely requiring the fault SUPPORT sampler to be independent does not establish resource-state independence. The theorem's requirement that all error parameters be consistently converted to channel error is compatible with the necessary clarification.

## 1. Partial occupancy: valid surgery and exact cost

Let L=|tau| and let u be the number of initially missing defects in tau. Flipping the complete valid tau changes the leading check energy by 2J0(L-2u). The per-check remainder norm loses at most 2epsilon0 J0 L. If all missing defects lie in the fault-touching set, u<=m=|tau intersect N(F)|. Therefore

    F0(x)-F0(x+tau)>=2J0[(1-epsilon0)L-2m].

The actual positive Gibbs ratio loses another Lambda L+4r_n, giving

    mu(A_tau,F)<=exp[-B L+4beta J0 m+4r_n].

The map is a fixed syndrome translation and hence injective on the partial-occupancy event. It need not preserve that event or the selected decoder witness. The occupied subset of tau is never asserted valid; only the FULL original witness is translated. Conditioning on the other CSS syndrome is valid and does not assume statistical factorization.

If a Pauli on the fault support reaches an unstable syndrome, its occupied source witness has no missing checks outside N(F). Thus partial occupancy is a necessary event for every possible Pauli value and every prefix. The source's unchanged witness enumeration covers this union; no exponential Pauli-value union is needed.

## 2. Support averaging and threshold

Let c=exp(hb)-1>=0. Since m<=b sum_(ell in I_tau)1_(ell in F),

    E exp(hm)<=E product_(ell in I_tau)(1+c1_(ell in F))
                <=(1+cq)^|I_tau|<=(1+cq)^(aL).

The second inequality follows by expanding into subsets and applying the local-stochastic upper bound to each nonnegative term. Spatial independence of faults is not needed. Independence from the stored state IS needed when averaging its Gibbs event probability against this support law.

Hence the reduced tension B_q=B-a log(1+q[exp(hb)-1]) is correct. If B_crit is a sufficient fixed witness-counting threshold and B>B_crit, any positive q satisfying

    q < [exp((B-B_crit)/a)-1]/[exp(hb)-1]

(with the usual cap at one and strict slack) suffices. Poor constants do not make this threshold volume-dependent. The global exp(4r_n) factor is paid once in the union bound and changes a prefactor, not the witness tension or an additive error floor.

## 3. Entire-support correctness, not a Pauli mixture argument

By definition of G_F, every syndrome reachable using any Pauli on the effective support avoids the original bad set. Each prefix of a decomposition into elementary Paulis remains in this family. Applying the original elementary decoder-stability identity sequentially proves [Q_mu,P]G_F=0 for every support Pauli P. Linear expansion gives the same for every support operator, including arbitrary coefficients on clock/environment systems.

For Kraus operators E_a of a trace-preserving support channel,

    sum_a E_a^dagger Q_mu E_a G_F
       =sum_a E_a^dagger E_a Q_mu G_F=Q_mu G_F.

The difference between the adjoint logical observable and Q_mu is Hermitian, has norm at most two, and annihilates G_F on both sides. Its expectation with any bounded reference observable is therefore bounded by twice the bad-subspace probability. Good/bad coherences introduce no square root.

This argument does not require Clifford propagation through U, Pauli stochastic values, or a Pauli twirl. A fixed-depth local U and terminal circuit transport a fault into a bounded lightcone; arbitrary qudit fault operators can then be expanded in data Paulis with ancillary operator coefficients. All those supports must be included in the constants a,b and in G_F.

## 4. Bell normalization and the actual decoder frame

For real CSS encoding V, direct Bell contraction gives

    K_P=(2d)^(-1/2) W V^dagger P,   d=2^(n_data).

For each outcome P, exactly one valid syndrome s has a nonzero block V^dagger P V_s. Its block is the logical Pauli L_P up to phase. Applying the inverse of THIS observed-outcome frame gives

    Ktilde_P=(2d)^(-1/2) W V_s^dagger.

There are four logical classes times d/2 stabilizers, hence exactly 2d outcomes for each syndrome. Summing the corrected Kraus channel therefore gives exactly

    sum_s W V_s^dagger sigma V_s W^dagger
      =W Tr_G(D sigma D^dagger) W^dagger.

The normalization and completeness are correct. Syndrome coherences are removed exactly as in the intended gauge partial trace, while logical/reference coherence is retained. Redundant stabilizer labels do not multiply the number of independent sectors.

For source and resource Paulis E,F, the physical Bell identity yields F^T P E=P E_P with E_P=P^dagger F^T P E. Conjugation by the product Pauli P changes only phases, not support. Thus the observed-P correction produces Ktilde_P E_P, not a correction using an unavailable shifted outcome. Joint coherent S–A Kraus operators produce sums Ktilde_P M_(P,a) in the SAME support algebra. Those outcome-dependent M operators need not define separate trace-preserving channels; the full instrument does.

The global ideal intertwining Ktilde_P Q_mu=sigma_mu^out Ktilde_P combines with [M,Q_mu]G_F=0 to give the noisy intertwining on G_F. Summing the physical Kraus completeness relation then proves two-sided bad support for READ_F^dagger(sigma_mu^out)-Q_mu. This is the needed coherent-fault argument; a statement only about Pauli probabilities would not suffice.

Faults directly acting on the active B block, or logical resource errors not representable by the admitted A-side support channel, must remain in the separately charged output/resource error terms.

## 5. Stored states, all-effect domination, and reference norm

The inherited storage consumer supplies a bound for EVERY effect, not only its original bad projector. In particular, from encoded-state domination by 2rho_bar, stationarity of the SAME-H Gibbs state rho, and the equal-trace effect inequality, one gets

    Tr(A Gamma(t))<=2Tr(A rho)+||rho_bar-rho||_1

for all 0<=A<=I. Thus K=2 and the stated twirl discrepancy can be used for arbitrary new read bad projectors. This remains true with generic syndrome coherences.

With an independent support sampler, the averaged bad projector is one effect. Applying domination once gives K p_read+delta_st. Paying delta_st per witness or per location would be incorrect; the theorem avoids that mistake.

For each of three output logical Paulis, the adjoint difference is bad-supported with norm at most two. Reference trace-norm duality and the qubit Pauli expansion therefore give the conservative factor six multiplying the averaged bad weight. Completeness removes the identity coefficient. The resulting bound is valid for entangled logical inputs, not only single-system expectation values.

Additional service failures must be stated in compatible reference-safe norms. An input-uniform failure-probability bound epsilon contributes at most 2epsilon to trace-norm channel error. A merely average failure probability or bare resource fidelity does not automatically qualify.

## 6. Resource, access, and classical-read boundaries

The theorem explicitly charges a separately prepared encoded A half, actively protected B output, constant-factor spatial placement/routing, reliable classical decoder/frame computation, and maintenance of B during potentially long classical latency. The mathematical existence of these operations is not a construction of their noisy compiler or an efficiency bound. The active-memory comparator must receive the same controls and resources.

Faults in destructive outcomes can be represented by premeasurement flips for this measurement instrument, provided remaining classical processing errors are charged separately. Arbitrary correlated or state-dependent classical failures are not justified by an unqualified scalar failure rate.

Always-on native or environment Hamiltonian action during access is not automatically a local-stochastic sampled fault. It must be compensated, included exactly in the ideal access circuit, or independently admitted by the stated service model. A fixed-strength global Duhamel error of order n v tau_access would not close this gate. The explicit exclusion in the theorem is essential.

For the separate-sector CSS decoder, destructive Z-basis data readout computes the appropriate check syndrome, raw logical Z and correction sign, implementing the full-space Q_Z observable; X is analogous. The support-wise proof applies to this cheaper classical-read channel. It neither simultaneously reads incompatible observables nor extracts an unknown quantum state.

## Final scope

This is terminal extraction from a state already satisfying the storage all-effect domination premise. The output is either the specified active quantum block or a chosen classical logical measurement. No claim follows for noisy WRITE followed by long passive holding: correcting the immediate logical action does not restore the necessary stationary joint gauge/clock/environment preparation. That distinction is mathematically necessary, not a terminology choice.

## Additional output-metric clarification

A standard actively protected output guarantees small error AFTER its specified recovery/decoding map. It does not generally guarantee small physical trace distance from the ideal code-space state W xi W^dagger: an entirely correctable physical Pauli error can make those states orthogonal. Therefore epsilon_out in the final comparison must be defined in a reference-safe decoded-logical channel norm, with the same output decoder applied to both compared states. That decoder may be a mathematical verification map; this does not require physically releasing a noisily decoded bare qubit. Alternatively one must explicitly assume the much stronger physical-channel error guarantee. Inserting a conventional logical FT failure rate into a physical trace-distance bound is invalid. This clarification was reported to root and constructor before freezing.

## Independent audit of the split-tail refinement

The root proposed a sharper replacement for the exponential-moment estimate. It is valid and can materially improve the dependence of the service threshold on temperature. Write m=|tau|, h=4beta J0 and let N=|I_tau|<=c m. For any fixed 0<theta, split the averaged partial-occupancy probability into coverage <=theta m and coverage >theta m.

On the first part the Gibbs comparison gives exp[-(B-h theta)m+4r_n]. On the second part discard the thermal event entirely. Since each fault location covers at most b checks, the number of sampled locations in I_tau must be greater than theta m/b. Put k=ceil(theta m/b). This is a conservative necessary lower bound even when theta m/b is an integer. If k>N the event is empty; otherwise the subset union bound gives

    Pr(coverage>theta m)
      <=binom(N,k)q^k
      <=(ecbq/theta)^k
      <=(ecbq/theta)^(theta m/b),

provided ecbq/theta<1. Consequently

    E_F mu(A_tau,F)
      <=exp(4r_n)exp[-(B-h theta)m]
        +exp[-T_q m],
    T_q=(theta/b)log[theta/(ecbq)].

Suppose the earned witness count is bounded by a polynomial prefactor times mu_ent^m in this SAME top-witness weight m. The two sufficient strict inequalities are

    B-h theta>log(mu_ent),
    T_q>log(mu_ent).

In particular theta<B/h by itself is NOT enough: the first exponent must still beat witness entropy. Taking theta below (B-log(mu_ent))/h with fixed slack and

    q < theta/(ecb) * mu_ent^(-b/theta)

with fixed strict slack suffices. At every temperature regime where (B-log(mu_ent))/h has a fixed positive lower bound, theta and this q can be chosen temperature-independent. This is a real improvement over the moment method's exp(hb) sufficient precision penalty; it is not a proof that noise tolerance is uniform over arbitrary parameter scalings without that relative margin.

The witness entropy must be converted to m=|tau| explicitly if the existing theorem counts graph or marked mass instead. The previously earned trace bound mass<=A_trace|tau| and exponential mass enumeration can provide such a conversion, with a larger fixed mu_ent and polynomial prefactor. One cannot silently identify those different size variables.

## Frozen revision review and final verdict

I re-read the revised theorem and verified SHA256 `9258892544090c560792b8aea3f19c8cd7963e6df814e1690c612fb5fd8487ba`.

Both interface issues identified above are resolved in this revision:

1. Bell preparation is explicitly independent of the stored input/reference/environment, and epsilon_Bell is a full-joint, reference-safe discrepancy at the physical-A/logical-B port, with retained fault labels included. Correlations or disturbances from any resource preparation that touches the storage bath must be charged. Marginal fidelity is explicitly not substituted.
2. Equation (5) is explicitly AFTER the stipulated mathematical recovery/decoder D_B; the output remains physically FT encoded. The resource and maintenance interfaces must compose reference-safely, or a single combined interface supplies their sum error. Correctable output faults are no longer implicitly required to have small physical codeword distance.

The revised split-tail proof is also correct. Its exact integer choice k=floor(theta m/b)+1 is stronger than the conservative ceiling version derived above. It applies the already-earned witness entropy sum separately at B_thermal and B_fault, avoiding any unsupported conversion to a simple top-weight exponential count. Requiring BOTH tensions to exceed a fixed B_req is sufficient. The conditional temperature-uniform interpretation retains the actual native perturbation theorem's admitted temperature domain and does not claim a zero-temperature-uniform robustness threshold.

**FINAL VERDICT: PASS for the conditional terminal quantum READ theorem and its destructive classical-read corollary, under the explicit inherited witness, support-noise, resource, output-decoder and all-effect storage assumptions. No unresolved gap was found in the audited mathematical interfaces.** This audit does not close noisy WRITE, admit arbitrary coherent always-on Hamiltonian action during access, supply the Bell-resource compiler, or establish efficient/noisy thermal preparation.

Minor editorial normalization: Section 7 still calls the classical failure probability epsilon_class, whereas Equation (5) and the final interface correctly use p_class and charge 2p_class (epsilon_class=2p_class if used as a trace-norm error). The explicit equation/final conventions govern. Replacing that residual sentence by 'failure probability p_class' is a permitted notation-only correction and changes no audited mathematics.

This verdict binds the frozen theorem hash above. A status-only change, that classical-probability notation correction, or a summary pointing to the sharper split-tail bound is permitted without changing the certified assumptions or result. Stronger access-noise, physical-output, resource-independence or WRITE claims are not covered.
