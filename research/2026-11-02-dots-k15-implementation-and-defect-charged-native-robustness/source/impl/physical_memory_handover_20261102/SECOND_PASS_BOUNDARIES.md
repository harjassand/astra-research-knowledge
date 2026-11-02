# Second constructor pass: three sharp boundaries

2 November 2026. These are boundary results, not a completed generic noisy loader.

## A. Exact dressed-bath basin: positive but rejected as the target solution

Let the native memory H0 have bounded-local commuting syndrome projectors Q_a and decoded logical algebra L, with [H0,Q_a]=[H0,L]=0. Here these are the prefix-dressed checks/logical operators, not bare checks. Add one finite-dimensional bath cell at each native site and a bath-only Hamiltonian and dissipator, at arbitrary fixed positive rates. The bath initial state need not be pure or thermal.

Choose W=product_i W_i, with each W_i onsite on the native carrier plus its bath cell and ||W_i-I||<=theta. Set the ACTUAL generator to

  L_actual = Ad_W o L_0 o Ad_(W†),

where L_0 consists of H0 plus the bath-only dynamics. Thus all actual jump operators are W_i(I tensor l_i)W_i†. They are genuine fixed-rate local noise contacts and may disturb physical data observables. The actual Hamiltonian is W(H0+H_B)W†. It remains two-site on constant-dimensional composite sites; its difference from H0+H_B has local norm O(theta) times the fixed local energy budget. This is a restricted isospectral perturbation family, NOT an arbitrary small V.

A direct sparse-syndrome lemma: suppose rho obeys Tr[rho product_(a in T) Q_a]<=q^|T|. If each check touches at most k composite sites and the check-support overlap graph has degree at most kappa-1, every T contains R of size >=|T|/kappa with disjoint check supports. For each selected a,

  W† Q_a W <= 2 Q_a + 2 k^2 theta^2 I.

This is (A+B)†(A+B)<=2A†A+2B†B applied to Q_a W_local. The selected inequalities have disjoint support and can be multiplied. Therefore every full or partial onsite product W obeys the syndrome-inclusion bound

  q -> f(q) = [2(q+k^2 theta^2)]^(1/kappa).

This holds for arbitrary bath correlations and quantum syndrome coherences. It has no system-size factor. Choose fixed q and theta small enough that f(f(q)) is within the banked decoder threshold.

The conjugated evolution is W exp(t L_0) W†. L_0 preserves every syndrome probability and every decoded logical observable. Telescope W and W† into O(n) local factors. A local factor commutes with the logical algebra on the enlarged good-syndrome projector; its contribution to a logical expectation is at most twice the square root of its bad-projector probability. The component decoder theorem and the preceding inclusion bound therefore give a reference-safe, uniform-in-time logical error bounded by initial write error plus poly(n) exp(-c n^eta).

Thus extensive locally sparse startup errors and arbitrary clock gauge are admitted without Gibbs preparation, under this specifically engineered reservoir. Finite-temperature imperfect bath resets and arbitrary bath-only coherent dynamics are harmless within the declared algebra. Generic independent faults breaking that algebra are NOT admitted. Finite-depth stochastic service/switching faults can be included in the initial sparse class; a noisy native switch must remain within this algebra or be charged as such a finite startup fault channel.

**Why this is not the desired advance:** the reservoir has an exact dressed noiseless subsystem. The same-resource active comparator inherits it and can dispense with most of the native thermal-memory mechanism. This is a useful positive boundary, not an open operating region for generic contact imperfections. The governing mechanism is established noiseless-subsystem theory: Knill–Laflamme–Viola, https://arxiv.org/abs/quant-ph/9908066 .

## B. Domination calibration obstruction on the actual commuting code, not only a toy product model

The root's averaged-output condition W(I/2)<=kappa rho_actual is an operationally sufficient criterion. The following limits the inference from local-stochastic terminal noise to that criterion; it is NOT a memory no-go.

For independent syndrome bits with target Bernoulli(q), a fixed output bias q+delta gives exactly

  kappa_min = [max{(q+delta)/q,(1-q-delta)/(1-q)}]^M.

Thus log kappa=Theta(M|delta|) at fixed nondegenerate q for small delta. Both distributions can be below the decoder threshold. Preparing a pure syndrome code state is even colder but still has kappa_min=(1-q)^(-M), exponentially large at every fixed positive temperature.

The extensive mismatch also occurs in a bounded-degree stabilizer Gibbs law without assuming independent checks. Choose M=Omega(n) physical Pauli errors P_i with nonempty, pairwise disjoint check-syndrome supports. Such a packing is available when bounded-degree local error/check incidence covers a positive density of carriers. Their syndromes are linearly independent because the supports are disjoint. Partition the valid syndrome space into orbits under their translations.

Within the orbit containing zero, write x_i for whether P_i is applied. Its CONDITIONAL Gibbs law factorizes, because its check supports are disjoint:

  pi(x | orbit0) = product_i q_i^(x_i)(1-q_i)^(1-x_i),
  q_i=1/(1+exp(beta Delta_i)),

where Delta_i is the positive bounded energy of that local syndrome. The orbit itself may have exponentially small Gibbs mass; that does not affect an exact pointwise domination test.

Now apply independently each P_i with a fixed small probability p. The noise preserves every orbit and its total probability. Within orbit0 it sends

  q_i -> q_i'=q_i+p(1-2q_i).

At the all-one point, the ratio of the noisy Gibbs weight to its original Gibbs weight is

  product_i [q_i'/q_i]
    = product_i [1+p(1-2q_i)/q_i] >= exp(c p n),

for uniform fixed low-temperature bounds on Delta_i. Consequently the noisy, logically reliable terminal ensemble can require log kappa=Omega(p n). No appeal to an unphysical independent-check Hamiltonian is needed. This is an exact commuting-reference calculation; it is not silently transferred to the native noncommuting Gibbs state.

For a stretched-exponential bad weight exp(-c n^eta), eta<1, a fixed per-site mismatch therefore need not fit the root's sub-barrier domination budget. Exact Gibbs-preserving contacts, size-dependent calibration, a suitable approximate/smoothed condition, or a genuinely local nonstationary theorem is necessary for this proof route. A bound on the encoded logical input's entropy alone does not price the extensive entropy removed by full-syndrome correction/reset.

## C. Current strongest autonomous comparator: primary v3 gate

Primary text: Dunneweber–Styliaris–Trivedi, arXiv:2601.20818v3, 25 September 2026, https://arxiv.org/html/2601.20818v3 . Relevant locations: II.2 (noise), VI (initialization), VII.2 (continuous time), Discussion (scope).

Verified scope, in brief: the rigorous result is synchronous local-channel fault tolerance, with noisy quantum and classical controls and a fault-set diamond-norm condition. The continuous-time construction is an outline; it admits added local unitary jumps but explicitly does not cover faulty engineered correction/reset channels. Autonomous hierarchy preparation remains open. The discrete-time architecture uses fixed local dimension and nearest-neighbor plaquette geometry, with ongoing reset service.

**Own consequence for this task:** adopt the proven controller organization rather than rebuilding a weaker ideal controller. Do not claim a completed continuous-time finite-temperature thermostat from it. Replacing a reset by a finite-purity reset is an admissible discrete-time local fault if its norm is below threshold; establishing a noisy continuous-time implementation still needs the asynchronous event/fault-set proof. Entropy removal, cooling, local update rates, and initial hierarchy preparation are physical resources, not free consequences of a mathematical RESET symbol. The active comparator must receive those same services.

This also identifies the immediate obstruction to the engineered-reference-thermostat candidate: a classical trace-polymer sampler can supply a useful target process, but its multi-site updates must be implemented by noisy finite-range local contacts while preserving the required quantum channel. Polynomial classical mixing and bounded classical description size do not establish that physical generator or its basin.
