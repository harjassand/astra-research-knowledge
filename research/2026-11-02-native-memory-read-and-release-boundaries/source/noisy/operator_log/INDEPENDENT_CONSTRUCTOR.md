# Independent constructor: quantum inverse-noise release
1 November 2026. Initial target-only construction reported to root before receiving its method. Status: an exact local-flow equation and a precise remaining analytic lemma, NOT an earned polynomial preparer.

## Initial independent mechanism
Set sigma=C^{-1}(rho_H). Positivity is given. Attempt to construct its effective Hamiltonian K=-log sigma by connected-cluster cardinality expansion around the preparable commuting reference, then use the admitted ideal weak-perturbation thermal encoder. A scalar partition-function expansion is insufficient: an operator logarithm is required. This was reported independently at 22:02 UTC before root supplied its preferred approach.

## Stronger exact mechanism: inverse-noise modular flow
For a Pauli conjugation A_i=Ad(P_i), define t_i=-log(1-2q_i)/2. Since A_i^2=id,
 C_i=exp[t_i(A_i-id)], C_i^{-1}=exp[t_i(id-A_i)].
Use sigma(u)=exp[u sum_i t_i(id-A_i)]rho_H, 0<=u<=1. Positivity at intermediate u follows from the stated uniform small-noise theorem, since its effective noise rates are (1-exp(-2ut_i))/2<=q_i. Let K(u)=-log sigma(u); scalar normalization terms may be ignored in Hamiltonian interactions.

Define T_i(K)=exp(K/2)P_i exp(-K/2), and B_i(K)=I-T_i(K)T_i(K)^dagger. Then
 sigma^{-1/2} sigma'(u) sigma^{-1/2}=sum_i t_i B_i(K),
 K'(u)=-sum_i t_i f(ad_K)[B_i(K)],
 f(w)=w/(2sinh(w/2)), f(0)=1.
This is exact, obtained entrywise in the eigenbasis of K using the Frechet derivative of log. Moreover
 f(ad_K)[B]=integral_R (pi/2) sech^2(pi s) exp(isK)B exp(-isK) ds.
The kernel integrates to one and decays as exp(-2pi|s|). There is no target-marginal oracle in these identities and no invocation of a CP inverse map.

At K=beta Href (commuting Pauli stabilizers and compatible onsite bath), P_i K P_i commutes with K, so B_i=I-exp(K-P_i K P_i), supported on a bounded reference star. The RHS is therefore local and O(max t_i) in local strength despite extensive total norm. For K=beta Href+W, weak W, imaginary-time dressing of P_i is governed by the same commuting-reference connected expansions as the admitted filtered-parent construction. Real-time evolution in the reference interaction picture has time-dependent weak terms exp(is beta Href)W_X exp(-is beta Href): support expands by a bounded reference star and the norm is unchanged. This suggests propagation in connected weak-label cardinality at rate O(||W||), rather than at the strong reference interaction scale. The exponentially decaying modular kernel can dominate that growth at sufficiently small W.

### Decisive missing lemma (do not silently assert)
Prove the RHS defines a locally Lipschitz vector field in a suitable scale of exponentially cardinality-weighted interaction norms, uniformly in volume, and keeps ||W(u)||_a <= C(beta,J)(||beta V||_a+max t_i) on [0,1]. A fixed-norm proof must account for support-size factors and any loss of locality weight; bare LR spatial bounds do NOT suffice. Strong commuting reference stars enlarge support by O(cluster cardinality), not a logarithmic-radius ball.
Also prove computable connected coefficient/remainder bounds, e.g. sum_{X containing x, |labels(X)|>L} ||W_X|| <= C lambda^L with lambda<1, plus derivative bounds for the preparation path. This is the concrete new theorem needed. Positivity alone and the exact differential equation alone do not prove it.

### If that lemma is earned: genuinely polynomial compilation
Truncate connected label sets at L=O(log(N/epsilon)); each support contains O(L) physical spins, not O(L^d). Bounded-degree connected-set enumeration is N exp(O(L)). Compute finite-cluster exponentials, the finite inverse-noise map, and matrix logarithms on O(L) spins, then connected inclusion-exclusion. Each costs exp(O(L)) times polynomial precision, hence polynomial overall; summing repeated histories by finite-cluster evaluation avoids factorial enumeration. Ensure the coefficient definition includes appropriate reference boundary stars and prove inclusion-exclusion reproduces the chosen interaction potential.
Feed the resulting K into the already earned ideal Gibbs encoder only after extending its bounds to this cardinality-quasilocal interaction class. Alternatively its filtered-parent proof can be rerun with these connected coefficients. Final release error adds computational preparation error and calibrated channel mismatch. Unknown logical input requires the separate overwrite/prefix argument supplied by root, not CP of C^{-1} composed with the ideal encoder.

## Exact encoded inverse obstruction (scope-limited)
For every physical carrier noisy in a nontrivial single Pauli basis, C_i=(1-2q_i)id+2q_i D_{P_i}, where D_{P_i}=(id+AdP_i)/2. Consequently C contains complete joint-basis dephasing with weight r=product_i 2q_i. This component is entanglement breaking if it acts on ALL released quantum carriers, with no noiseless quantum side register carrying the logical input. For every preencoder F and decoder R, the decoded logical entanglement fidelity for input dimension d is at most 1-r(1-1/d): the entanglement-breaking component has overlap at most 1/d with a maximally entangled state. Therefore exact reversible logical target channels cannot equal C F. An equivalent Knill-Laflamme argument uses rank-one projectors in the span of all Pauli-error patterns. This exponentially small lower bound does NOT defeat the intended approximate logical theorem. It only forbids promoting scalar inverse positivity into an exact CP inverse encoder.

## False shortcuts
* Vectorizing sigma by applying inverse noise as a local imaginary-time filter on a doubled space produces |sigma>>, whose physical reduction is sigma^2/Tr(sigma^2), NOT sigma. Preparing |sqrt(sigma)>> remains necessary.
* Product inverse-noise quasiprobability norm is (1-2q)^{-N}; signed sampling is not a physical preparation and generally costs exponentially.
* Knowing sigma>0 gives no efficient square root, diagonalization, or Gibbs sampler.
* Scalar log Z and determinant zero-freeness do not establish operator-log locality. Even zero-free analytic matrix families require care with branches and noncommutativity.
* A block on radius log(N) in d>1 has polylog-volume and dense compilation is superpolynomial; connected CARDINALITY log(N) is the required cutoff.

## Resource ledger
Known q_i, local Hamiltonian coefficients, bath dimensions, and inverse polynomial numerical accuracy are classical inputs. Calibration mismatch of actual versus planned product release channels is at most 2 sum_i |q_i-q_i^planned| in diamond norm (by telescoping); precision O(epsilon/N) per rate suffices once a normalized preimage for planned noise is prepared. If learned by independent Bernoulli experiments, a direct Hoeffding estimate costs O(N^3 epsilon^{-2} log(N/delta)) total trials, before exploiting any shared calibration; this is polynomial but explicitly charged. Pure ancillas, reset, ideal/fault-tolerant gates, encoded logical input, and finite accessible bath are charged as in the admitted ideal encoder. No claim of unknown-noise tolerance, autonomous release, or full noisy physical encoder.

## Primary-source checks
* Chen/Kastoryano/Gilyén, https://arxiv.org/abs/2311.09207 : efficiently implementable exact noncommutative Gibbs generator, with complexity dependent on mixing time. Does not supply rapid mixing for this low-temperature code preimage merely from positivity.
* Rouzé/França/Alhambra, https://arxiv.org/abs/2403.12691 : high-temperature efficient thermalization/purification. Small noncommuting V around a strong code reference is not the theorem's high-temperature hypothesis.
* Bluhm/Capel/Pérez-Hernández, https://arxiv.org/abs/2401.10147 and published https://link.springer.com/content/pdf/10.1007/s10955-025-03512-y.pdf : explicitly records a gap in the earlier Kuwahara-et-al operator effective-Hamiltonian locality proof; cannot cite that step as established here.
* Arad/Firanko/Gurevich, https://arxiv.org/abs/2408.08672 : local-channel steady-state Gibbs-Hamiltonian perturbation theory; different direction and hypotheses from inverse-image preparation. Formal connected locality is not our needed uniform constructive norm bound.
* Eassa et al., https://www.nature.com/articles/s41534-024-00887-w : cluster quasidistribution method estimates observables using signed local states; does not instantiate this physical preimage preparer.

Conclusion: no unconditional polynomial quantum preimage preparer has been derived. The modular-flow equation supplies a particularly concrete positive construction target and isolates a potentially provable weighted-interaction ODE closure, rather than reusing the disproven implication positivity=>preparability.

## Follow-on correction, 22:42 UTC
The root correctly identified that small real-time velocity does not establish the proposed cardinality-weighted ODE closure: LR balls in 3D have volume O(t^3), while the modular kernel only decays exponentially in t. No closure proof has been obtained. See `EXACT_COMPLEX_POLE_BARRIER.md` for an exact bounded-degree 3-local inverse-Pauli/Gibbs family whose zero-noise operator-log derivative has complex poles at O(1/n). This rules out a volume-uniform jointly analytic Taylor/Cauchy approach even for the special inverse-Pauli structure. It does not rule out a nonanalytic real-axis representation or an efficient direct preparer.

The modular-time truncation itself has an exact norm ledger: with k(s)=(pi/2)sech^2(pi s), integral_{|s|>T} k(s) ds = 1-tanh(pi T) <= 2exp(-2pi T). Hence replacing each f(ad_K)B_i by its |s|<=T integral costs at most 2 sum_i t_i ||B_i|| exp(-2pi T) in global operator norm. If ||B_i||<=B is uniform, T=O(log(N/epsilon)) suffices for that one derivative evaluation. This is implementable using efficient real-time Hamiltonian simulation IF K is already supplied in an efficient representation; it is not a preparer, because obtaining/simulating the evolving K is precisely the unresolved recursive oracle. A fixed T=O(1/v) short-time-commutator argument leaves a volume-charged bound O(N q B exp(-c/v)), not all inverse-polynomial accuracies at fixed v.
