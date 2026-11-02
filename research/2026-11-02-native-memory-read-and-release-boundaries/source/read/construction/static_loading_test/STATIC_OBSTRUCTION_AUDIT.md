# Static loading test: precise missing construction, not a no-go

2 November 2026. Independent audit of the actual-Gibbs/native-two-body question.

## Result

I do not have a valid autonomous counterexample in the specified native model. The driven preparation-energy attack does **not** establish one. Nor does the stationary proof automatically establish protection after fixed-rate local preparation noise. These are distinct unresolved statements. In particular, failure of a Gibbs-domination sufficient criterion is not evidence that the physical memory fails.

The strongest concrete negative result obtained here is a barrier to a standard direct Feynman-clock Hamiltonianization of the driven attack, proved below. It rules out that proposed compiler/initialization accounting, not autonomous thermal machines in general.

## Four joins that a genuine counterexample must supply

1. **Actual initial state.** The state before preparation noise must be exp(-beta H_tot)/Z for the very same static H_tot used during storage. Replacing it by exp(-beta K)/Z with later-enabled interactions is a quench, not the premise. Small local interaction strength does not make the two global states uniformly trace-close over a polynomial-volume bank. Static clock/program/fuel correlations must be handled in the actual Gibbs measure.
2. **An autonomous controller with thermal initialization.** The old clean branch constrains O(log n) workspace spins. It does not constrain a polynomial-length clean clock tape. Scheduling, fresh-bank routing, and not revisiting records were supplied externally. All three now require Hamiltonian mechanisms and an explicitly priced thermal initialization event.
3. **The actual native contact.** The old energy-resolved Pauli-star transition is bounded-body but generally not two-body. It resolves a commuting stabilizer reference K, not the full-spectrum seven-level-clock H_nat plus generic V. An ordinary low-energy perturbative gadget does not establish an accurate thermal full-spectrum or polynomial-time simulator with fixed gaps and fixed strengths. A valid compiler must control simulation errors at the required physical times, uniformly in n, without freezing its mediator spins by assumption.
4. **Channel-level logical effect.** Obtaining directed motion, a charged battery, or a hot local spot does not prove logical dephasing in this hierarchical code. One must implement the code Pauli path or otherwise prove a final decoder-independent entanglement loss. Recurrent finite unitary dynamics also removes the old automatic isolation of spent records. A lower bound at a specified polynomial readout time is sufficient; irreversible dynamics forever is not required.

## A proved obstruction for the simple mobile-cursor compiler

Consider L zero/one cursor sites with onsite energy E>0 per cursor and a number-conserving nearest-neighbor hopping Hamiltonian W of strength at most g. Let N be cursor number. Suppose, as in the elementary hopping compiler, the restriction satisfies ||W|_{N=k}|| <= a g k, with fixed a. Including an internal d-state cursor only worsens the clean-sector counting; take d=1 for simplicity. First take this clock independently thermalized, without conditional pure initialization; an actual interacting-Gibbs extension is given below.

For H_clock=E N+W, the dimension of the k-sector is binomial(L,k), hence

 Z >= sum_k binomial(L,k) exp[-beta(E+a g)k]
   = (1+exp[-beta(E+a g)])^L.

The Gibbs probability of the entire one-cursor sector obeys

 Pr(N=1) <= L exp[-beta(E-a g)] /
                 (1+exp[-beta(E+a g)])^L
           = poly(L) exp[-c L],

with fixed c=log(1+exp[-beta(E+a g)])>0. Demanding the cursor also start at a specified input position can only decrease this probability. The vacuum-plus-one-cursor sector obeys the same exponential form. Every gap/coupling is fixed in n. A very large fixed E changes c but not the asymptotic conclusion.

Thus a polynomial-length single-head clock whose successful operation requires no other thermal heads has exponentially small initialization probability, unlike the old inverse-polynomial clean-workspace branch. Polynomial repetition does not repair it. Replacing hopping with a classical local unary-clock penalty has the analogous finite-temperature defect-density problem: bounded local penalties give a nonzero probability of a local clock defect at each of a positive-density set of separated positions. This latter observation needs its own commuting/classical conditional-probability proof if used quantitatively; it is not an operator inequality for arbitrary quantum clock Hamiltonians.

**Actual interacting-Gibbs extension for unitary-labelled hopping.** The same bound holds for H=I_clock tensor H_work + E N + W whenever [W,N]=0 and ||W restricted to N=k|| <= a g k, even if W acts on the work/memory spins and does not commute with H_work. In the k-sector, the reference partition function is binomial(L,k) exp(-beta E k) Z_work. The operator bounds H_ref,k - a g k I <= H_k <= H_ref,k + a g k I imply the corresponding trace-exponential bounds by eigenvalue monotonicity (not false operator monotonicity of exp). Z_work cancels from the probability ratio. Ordinary cursor hops labelled by bounded-norm work gates meet this norm condition on a bounded-degree track. This genuinely includes the actual Gibbs state of that static simulator, not a switched-on product-state approximation.

The lemma is still restricted: arbitrary cursor-dependent reference work Hamiltonians, non-number-conserving controllers, or thermal-fault-tolerant many-head algorithms need new analysis. It directly prices a clean-clock branch when preparation noise leaves the clock alone or preserves its relevant number distribution; it is not a no-go against a preparation channel specifically designed to initialize a different controller. A supposed small-rate channel that cleans an extensive tape also needs its own stochastic-support accounting.

An exponentially large bath does not simply supply exponentially many usable attempts in polynomial time in bounded-density 3D geometry: only polynomially many sites lie within a polynomial-time finite-velocity light cone of the memory. A quantitative application needs a Lieb–Robinson tail estimate, but the resource-accounting point is already clear.

## Routes not excluded

* A thermal-fault-tolerant autonomous controller that tolerates a finite density of unwanted heads/defects, powered by preparation-created athermality.
* An autonomous logarithmic-space clock with its program hardwired into local geometry and a rigorous dirty-carrier routing scheme. A logarithmic number of clean bits would retain polynomial Gibbs weight. Merely invoking a binary clock does not supply bounded-range, bounded-degree two-body transitions or gate selection.
* A direct autonomous instability tied to this code that avoids a circuit compiler altogether.

None of these is supplied by the driven construction. None is ruled out by the cursor lemma. A valid positive engine at fixed q can have enormous q-dependent constants, but may not hide n-dependent gaps, onsite dimensions, interaction strengths, or uncharged pure tapes.

## Why small thermodynamic disturbance does not close the positive proof either

For any fixed static H and its Gibbs rho, relative entropy is invariant under the H evolution: D(rho_t||rho)=D(rho_0||rho). Data processing through {P_bad,I-P_bad} therefore gives, writing b_t=Tr(P_bad rho_t), p=Tr(P_bad rho),

 b_t log(1/p) <= D(rho_0||rho)+log 2.

This is a valid uniform-in-time estimate, but with log(1/p)=Omega(n^eta) it requires a sub-barrier **total** relative-entropy budget even to force b_t small, and does not supply exponentially small b_t from an O(1) budget. Fixed-rate noise on a large bank need not obey that budget. For independent random local unitaries, convexity and the Gibbs identity give D(N(rho)||rho) <= beta times average energy injection = O(q N_total) under bounded local incidence. The bound is an upper estimate, not a lower bound or a failure proof.

The already identified stationary warm-start domination condition is stronger and sufficient. Arbitrary small local stochastic noise does not automatically imply it with a sub-barrier exponent. Conversely, a benign thermal/quotient loader can satisfy it without having to defeat every conceivable autonomous controller.

## Verdict

The exact-H theorem's existing stationarity proof does not automatically extend to generic preparation noise. The stronger assertion that a static native counterexample exists remains unproved by the supplied evidence and this pass. The direct mobile-cursor compiler has a concrete extensive thermal-initialization obstacle; native two-body/full-spectrum code contacts and actual-Gibbs accounting are separate outstanding joins. Claiming that all warm starts fail, or importing the driven entanglement-breaking amplification as a static result, would be incorrect.
