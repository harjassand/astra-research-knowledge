# Thermal transition observations: a bounded response certificate and its paid interface

Status: internally derived analytic result; not formally verified, not a novelty or efficiency claim. The finite-dimensional construction has close precedents in quantum dynamic-structure-factor and phase-estimation algorithms. This note answers an interface question exposed by the incoming thermal-anchor failure: can the desired response be measured as one scalar without reconstructing a spectrum? Yes, conditionally on Gibbs preparation, an observable filter, and calibrated energy readout. Those are additional operations, not consequences of the anchored stochastic model.

## 1. Target and assumptions

Let H be a finite-dimensional Hermitian Hamiltonian, rho=exp(-beta H)/Z with beta>0, A=A*, and a>=||A||>0 known. Let eta>0. The target is the regular dissipative response

    chi_A(i eta) = sum_(E_m>E_n) 2 d (p_n-p_m) |A_nm|^2/(d^2+eta^2), d=E_m-E_n.

It excludes the diagonal/conserved isothermal term, diamagnetism, and claims about exchanging eta->0 with thermodynamic limits. A Gibbs state, rather than only a temperature label or pairwise balance on some accessible transitions, is part of the input contract. Cost is measured per raw trial; failed filters and zero-gap outcomes count.

## 2. A completely positive transition observation

Prepare rho, make a nondemolition measurement of H, apply the instrument

    K_success=A/a,    K_failure=(I-A^2/a^2)^(1/2),

and on success measure H again. The success joint probability is

    q(n,m) = p_n |A_nm|^2/a^2.

The failure branch is assigned zero. Energy degeneracy causes no problem: for spectral projections P_E, the joint mass is exp(-beta E) Tr(P_E A P_E' A)/(Z a^2). Summing the two ordered events at a nonzero magnitude d gives

    q(-d) = exp(-beta d) q(+d).

Neither an ordinary projective measurement of A nor a free draw from the normalized f-sum spectral measure is the specified instrument. For unitary Hermitian A (a Pauli observable), the filter is deterministic, but Gibbs preparation and global energy readout remain paid operations.

## 3. Bounded folding theorem

For a raw success outcome let d=|E_m-E_n|. Output

    Y = 2 a^2 d tanh(beta d/2)/(d^2+eta^2).

Set Y=0 on filter failure or d=0. Then

    E Y = chi_A(i eta),
    0 <= Y <= B := a^2 min(beta,1/eta).

Proof. The total mass of the two signs is q(+d)(1+exp(-beta d)); multiplying by the displayed weight cancels this sum to 2 a^2 d q(+d)(1-exp(-beta d))/(d^2+eta^2), the Lehmann contribution. The range follows from tanh x<=x and 2d/(d^2+eta^2)<=1/eta. No division by a possibly small f-sum is used.

For comparison, the signed unbiased output is S=2a^2(E_m-E_n)/((E_m-E_n)^2+eta^2), with |S|<=a^2/eta. Conditioning S on success and the magnitude d gives exactly Y. Therefore Var(Y)<=Var(S), by conditional variance. The upward-only output 2a^2 d(1-exp(-beta d))/(d^2+eta^2) on positive gaps is also unbiased but has the weaker bound a^2 min(2beta,1/eta).

For n independent complete trials, Hoeffding gives

    P(|mean(Y)-chi|>epsilon) <= 2 exp(-2 n epsilon^2/B^2).

At fixed beta the sufficient number of trials for absolute accuracy has no eta^-4 divergence. This is an upper bound on statistical trials at this interface, not a bound on Gibbs preparation, time evolution, bit complexity, energy resolution, or an optimal quantum algorithm. A relative-error claim still depends on chi, which can vanish.

### Rejected exponential reweighting

The all-sided output a^2 d_signed(1-exp(-beta d_signed))/(d_signed^2+eta^2) is unbiased and nonnegative, but is not uniformly bounded by a temperature-independent resolvent range. Rare downward gaps carry exponential weights. With a=beta=eta=1 and d_signed=-10 the weight exceeds 2180. A worker's proposed range-halving argument for that output was rejected before integration. The positive fold uses detailed balance to average signs, not exponential reweighting of an individual backward event.

## 4. Finite-resolution and preparation certificate

Define k(d)=2d tanh(beta d/2)/(d^2+eta^2) for d>=0. Direct differentiation gives the global Lipschitz bound

    Lip(k) <= L := min(beta/eta, 3/eta^2).

For the first bound, each of the two derivative terms is at most beta/(2eta): use tanh(beta d/2)<=beta d/2, |eta^2-d^2|<=eta^2+d^2 and d/(d^2+eta^2)<=1/(2eta). For the second, the rational derivative term is at most 2/eta^2, while x sech^2(x)<=1/2 bounds the other by 1/eta^2. The latter inequality follows from cosh^2 x>=1+x^2>=2x for x>=0.

If each recorded energy differs from its latent energy by at most zeta, the magnitude gap differs by at most 2zeta, so the mean-output bias is at most 2a^2 L zeta. Clipping the computed output into [0,B] preserves that bound.

An implementable noisy readout contract need not resolve individual eigenvalues. Suppose the measurement Kraus operators are functions of H, and for each latent E the readout is within zeta with failure probability at most kappa. Since the initial Gibbs state is diagonal in H, the joint readout distribution is the ideal transition law convolved with per-energy classical kernels. This remains true for energy degeneracies and arbitrarily close levels. The first readout preserves each latent energy; final readout probabilities depend only on the final spectral populations. A coupling has probability at most 2kappa of a bad label pair. Arbitrary disruptive noisy measurements do not satisfy this contract.

If the prepared state has trace distance at most delta from rho and the entire implemented transition instrument differs from its ideal outcome channel by total variation at most gamma (uniformly for allowed inputs), data processing and the bounded output give the conditional certificate

    |mean(Y_implemented)-chi| <= epsilon_stat
        + B(delta+gamma+2kappa) + 2a^2 L zeta

with the Hoeffding confidence for independent implemented trials. This certifies the canonical target under these error contracts. It does not claim the physical response of an arbitrary non-Gibbs prepared state equals that target.

The resolution requirement is substantive. For H0=0 and H1=(eta/2) sigma_z, A=sigma_x, the regular responses are 0 and tanh(beta eta/2)/eta. The latter tends to beta/2 as eta->0. A gap readout that rounds both gaps to zero loses an order-one contribution. This is an indistinguishability example for that readout, not a lower bound against algorithms supplied with explicit H matrices or other measurements. The finite-eta regular response is not uniformly continuous at a collapsing gap as eta simultaneously tends to zero.

## 5. Unbounded observables require a separate tail gate

The source oscillator uses A=q, which is unbounded; a finite operator norm must not be silently assigned to it. Suppose a Gibbs state has M2=Tr(rho A^2)<infinity and M4=Tr(rho A^4)<infinity, and define spectral clipping A_L=clip(A,[-L,L]). The positive Lehmann quadratic form obeys

    chi_B(i eta) <= beta Tr(rho B^2)

for Hermitian B. Indeed (p_n-p_m)/(E_m-E_n)<=beta(p_n+p_m)/2, and summing the unordered pairs proves the inequality. Cauchy-Schwarz in this positive quadratic form, ||A_L||_(rho,2)<=sqrt(M2), and ||A-A_L||_(rho,2)<=sqrt(M4)/L give

    |chi_A(i eta)-chi_A_L(i eta)| <= 2 beta sqrt(M2 M4)/L.

Thus a bounded-filter certificate extends conditionally using acquired moment bounds and a physically implementable clipped filter. The sufficient statistical cost can be very poor as L grows. No unbounded-observable efficiency or physical implementation follows from this truncation lemma.

## 6. Correct local balance does not acquire missing equilibrium weights

Take two disjoint two-level blocks with energies (0,1) and (D,D+1), and A=diag(sigma_x,c sigma_x), 0<=c<=1. Any mixture with mass w in the first block and conditional Gibbs ratios in each block has q(-1)/q(+1)=exp(-beta). Nevertheless

    chi_w(i eta) = [2 tanh(beta/2)/(1+eta^2)] [w+(1-w)c^2].

The canonical weight is w*=1/(1+exp(-beta D)). Transition balance alone does not determine w*. If c differs from one, the response varies with this unacquired component mass. Filter frequencies may supply additional information, but a balance test alone does not. The missing normalization/sector preparation is a real scientific input; it cannot be repaired by declaring a local source to be thermal. This is the specific interface connection to Astra's source-normalization and Gibbs-acquisition capital.

## 7. Why a positive Euclidean averaging kernel does not supply this operation

For a two-level regular transition, the Euclidean kernel on 0<=tau<=beta is

    [exp(-tau d)+exp(-(beta-tau)d)]/[1-exp(-beta d)].

For any nonzero positive finite averaging measure its small-d integral diverges as a positive constant/d, whereas the target kernel 2d/(d^2+eta^2) tends to zero at fixed eta>0. Positive averaging cannot give a universal off-axis response functional.

More strongly, if a finite signed measure on the compact interval represented this target for every d>0, multiplying by 1-exp(-beta d) would equate an entire Laplace transform to

    (1-exp(-beta d)) 2d/(d^2+eta^2).

The right-hand side has nonremovable poles at +/- i eta unless beta eta is an integer multiple of 2pi. Analytic continuation of the identity yields a contradiction. At Matsubara eta=2pi k/beta the usual signed Fourier functional exists. This rules out exact universal bounded linear averaging of the compact Euclidean correlator at a non-Matsubara eta. It does not rule out approximate finite-error certificates, nonlinear inference, extra spectral information, or data-dependent estimators; those include the primary Mutzel-Tilloy comparator. Diagonal/conserved contributions must be treated separately.

## 8. Synthesis, comparator and remaining operation

The incoming anchor theorem rules out one specified finite local drift interface as a general temperature repair. The construction here changes the interface to equilibrium energy transitions and estimates only the desired functional. It avoids reconstruction of all hidden states or a full spectral density. It does not remove thermal preparation, observable implementation, or coherent spectral-resolution costs. Exact diagonalization is a truth fixture in the accompanying script, not a freely supplied operation in the proposed experiment.

Closest technical comparators include Sun et al., PRX Quantum 2, 010317 (2021), arXiv:2009.03542 (dynamic structure factors using phase estimation); Sakuma et al., arXiv:2404.19554 (2024); quantum work-distribution linear response (Guarnieri, Eisert and Miller, arXiv:2307.01885v2); and the scalar Euclidean-functional certificate of Mutzel and Tilloy, arXiv:2606.09791 (2026). The filter and balance/Rao-Blackwell ingredients are established ideas. No historical priority, total-cost advantage, laboratory verification, or civilization-enabling result is established here.

The highest-value acquisition question is an experimentally realizable bounded A with cheap Gibbs preparation and nondemolition coarse energy measurements whose required zeta is affordable, compared on the same target, error, preparation and runtime with real-time correlations, compact-Euclidean functional bounds and existing phase-estimation methods. A strong theorem on total cost or a measured operation is still missing.

Attribution: worker fk_transition_acquisition independently proposed the CP-filter transition interface and its signed estimator; root derived and checked the bounded-fold, robustness, clipping, component-weight and compact-kernel statements above. The worker had also derived folded spectral acceptance before receiving root's fold. Root shared the formula after the independent interface finding; the subsequent comparison is collaboration, not cold replication. External ingredients are credited above; originality is UNKNOWN.
