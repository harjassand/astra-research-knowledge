# Conserved sectors, invariant-law control, and precision at coexistence

29 October 2026. Complementary necessity and counterexamples. These results
support the scope of the root's bounded excursion compiler; they do not
supply convergence, a physical hold, or a new equilibrium reservoir.

## 1. Structural condition when hidden memory never mixes

Let H be a conserved hidden variable and K_h the visible endpoint kernel
conditional on H=h. A fixed visible law pi is preserved jointly with every
hidden distribution, in the product form lambda(dh)pi(dy), if and only if
pi K_h=pi for every allowed h, or almost everywhere under the allowed priors.
Sufficiency follows by integration. Necessity follows by concentrating the
prior in a sector; for a fixed prior, requiring the joint identity on every
measurable hidden event gives the same almost-everywhere conclusion.

This is invariance, not convergence. If every sector converges to pi,
arbitrary sector weights become harmless for the visible limiting law.
Uniform finite-time preparation from retained old information still requires
a uniform conditional convergence bound. Different sector targets remain
physically relevant forever. A correct aggregate equilibrium at one prior
cannot replace this condition.

Common detailed balance is sufficient but not necessary for invariance:
a nonreversible circulation can preserve pi. Detailed balance becomes
necessary if pi must survive arbitrary independent isolation of each
undirected edge, because each isolated two-state flux must balance.

## 2. A global invariant tilt need not be preparable

Disintegrate a warranted baseline measure as

    mu(dh,dy)=lambda(dh)mu_h(dy).

For a positive visible weight W, write Z_h=mu_h(W), Z=mu(W). The global
weighted measure is

    nu(dh,dy)=[Z_h/Z]lambda(dh)[W(y)mu_h(dy)/Z_h].             (1)

A correct excursion compiler preserves (1). A conserved H prevents it from
creating the new hidden weights Z_h lambda/Z from arbitrary old weights.
If its sector dynamics converges, a run with hidden prior lambda_0 instead
approaches

    lambda_0(dh)[W(y)mu_h(dy)/Z_h].                          (2)

For (2) to have one visible target for every lambda_0, the normalized sector
tilts must coincide. Because W is positive, this is equivalent to the
baseline sector visible laws mu_h themselves coinciding. This is a sharp
factorization criterion for one common visible weight transform. Use
conserved communicating components in place of H for a microscopic chain.
Already warranted target component weights provide another legitimate route.

### Exact two-sector obstruction

Take two frozen sectors, each initially of probability1/2, with conditional
baseline probabilities Pr(Y=1|H)=1/4 and3/4. Their aggregate visible baseline
is uniform. Each sector may be an ordinary irreducible reversible binary
chain. Put W(0)=1 and W(1)=3.

The global tilt has visible probability3/4. Its sector normalization factors
are3/2 and5/2, so its hidden weights are3/8 and5/8. Its visible conditionals
within sectors are1/2 and9/10. Preserving the original hidden weights gives
the limiting visible probability

    (1/2)(1/2)+(1/2)(9/10)=7/10.                            (3)

The discrepancy1/20 persists after arbitrarily many macro updates. The
global tilted law remains correctly invariant; the preparation inference
fails. The executable verifies every value in (3) with exact fractions.

## 3. Finite calibration can select kinetics within an exact structural class

Suppose every available local operation has a warranted common invariance
and isolation contract. A calibration record D may select and freeze one
operation per local context, with the same choice used in both orientations
of each edge. The root's stationary-kernel algebra then preserves its target
for every D and every relevant sector. No pre-calibration unconditional
density ceiling is being applied after data selection. The target ratio
is imposed structurally; the data selects kinetics within that class.

Calibration changes the conditional initial state. Invariance of every
frozen K_D does not say the post-calibration state is already pi given D,
or independent of old records. Preparation needs conditional convergence.
Arbitrary online adaptation also does not follow from invariance of each
available kernel: selection correlated with the current state can destroy
invariance. Fixed scans and independent scans avoid this inference.
State-dependent edge mobilities are legitimate only when the resulting
combined kernel satisfies the required balance or stationarity identity.

Finite observations cannot certify an exact stationary or detailed-balance
identity against every nearby alternative without a structural promise.
For positive finite-state kernels, every finite path event with positive
probability under one kernel also has positive probability under nearby
perturbations of the same support. A finite acceptance event therefore
cannot be an error-free exact-identity test. Confidence bounds on measured
defects are legitimate and different statements.

## 4. Vanishing row errors can change a phase by order one

Use the conventional Curie-Weiss family on n spins sigma_i in{-1,+1},
M_n=n^{-1}sum_i sigma_i:

    pi_{n,h}(sigma) proportional to
      exp[(beta/(2n))(sum_i sigma_i)^2+h sum_i sigma_i],
    beta>1.                                                (4)

This is a counterexample to a gap-independent precision inference, not a
new solution of the model. Primary Curie-Weiss precedents are recorded in
`PRIMARY_COMPARISON.md`; the limit used here is proved below.

The random-scan heat-bath probability for setting site i to+1 is

    q_i^h(sigma_-i)=[1+tanh(beta sum_{j!=i}sigma_j/n+h)]/2.

Its derivative in h is at most1/2. Hence the h and0 update rows have TV
distance at most|h|/2, uniformly in the configuration and n. The same bound
holds for the complete random-scan kernel. Both chains are reversible for
their respective Gibbs laws.

Spin-flip symmetry gives E_{pi_{n,0}}M_n=0 for every finite n. Let m_beta>0
solve m=tanh(beta m). For any fixed t>0, set h=t/n. Then

    E_{pi_{n,t/n}}M_n -> m_beta tanh(t m_beta)>0,              (5)

although the row error is at most t/(2n), tending to zero.

Proof. At h=0, the weight of M_n=m is proportional to
binomial(n,n(1+m)/2)exp[n beta m^2/2]. Stirling bounds give concentration
at the maximizers of

    F_beta(m)=beta m^2/2
       -[(1+m)/2]log[(1+m)/2]-[(1-m)/2]log[(1-m)/2].

The derivative is beta m-artanh(m). Since artanh(m)/m increases strictly
from1 to infinity on(0,1), its only critical points are0 and±m_beta.
The nonzero points are the two equal global maxima. Outside any fixed
neighbourhoods of them the exponent has a strict gap, which dominates
polynomial prefactors. Symmetry gives M_n converging in law to
(delta_{m_beta}+delta_{-m_beta})/2. The field h=t/n tilts this bounded
variable by exp(t M_n). Weak convergence applied to the bounded continuous
numerator M_n exp(t M_n) and denominator exp(t M_n) proves (5). QED.

Thus no system-size-independent function g(delta)->0 bounds all stationary
magnetization errors from local row-TV error delta alone. This already
fails for a coherent conservative field error: nonreversibility or nonzero
cycle affinity is unnecessary. Finite calibration bounds that permit a
common signed error must allow this possibility unless extra structure
excludes it.

Taking h_n=n^{-1/2} selects the positive phase completely, with mean tending
to m_beta. The same exponent gap restricts mass to the two phases; positive
and negative magnetizations m,-m have weight ratio exp(2n h_n m), diverging
near m_beta. Yet h_n and the row-error bound both tend to zero.

For beta=2, m_beta is approximately0.9575040. The t=1 limit in (5) is
approximately0.7115801. At n=2000 and h=1/2000, the saved floating population
calculation gives row error at most0.00025 and perturbed mean0.7114955,
against target mean0. This illustrates the analytic theorem; it is not
acquired data, a confidence certificate, or a hardware experiment.

## 5. Free-energy density is a different objective

For (4),

    |log Z_{n,h}-log Z_{n,0}|/n <= |h|.

Symmetry and Jensen give log(Z_{n,h}/Z_{n,0})>=0. For h>=0,

    D_KL(pi_{n,h}||pi_{n,0})/n
      =h E_h M_n-log(Z_{n,h}/Z_{n,0})/n <= h.                (6)

Both errors vanish with h. They can coexist with the order-one change in
(5): pressure and relative-entropy densities do not determine the weights
of coexisting phases. To protect these weights against a common field bias,
the scale is n h. For example, Pinsker and (6) give TV<=sqrt(n h/2), a
sufficient small-error guarantee when n h is small.

For a coherent dimensionless energy perturbation |U_tilde-U|<=n e, pressure
changes by at most e and symmetrized relative entropy is at most2ne.
These bounded-tilt statements do not assert mixing. Arbitrary transition
errors need not correspond to a coherent energy at all.

This explains the usefulness of exact common edge ratios beyond contractive
models. Unknown kinetic mobility does not perturb the Gibbs weight, while
a small systematic ratio error can. Exact ratios do not remove metastable
barriers or certify the symmetry of an apparatus from finite samples.

## 6. Completion indices and physical time

For one native P executed back-to-back, stopping changes which actual
endpoints are marked as macro completions; the concatenated native path
still has kernel P. The root's exact occupation identity shows that its
stationary pre-call measure is proportional to the original mu, cancelling
the endpoint tilt. State-dependent completion times cannot be treated as
equal physical-time intervals.

The actual terminal state exists at its completion event and can be used
by a subsequent operation. This is a stopped-state preparation interface.
It does not mean the state remains there until a common deadline, the full
endpoint-clock record is autonomous, or a new physical Hamiltonian has been
realized. Local networks change the actuation schedule and require their
own physical-time analysis. All phase/equilibrium comparisons here concern
the completion-index target law unless a separate clock supplier is stated.
