# Current owned question after the universal capacity floor

## Objective and what changed

At one fixed `0 < beta=sin(s) <= 1/512`, with the same actual fixed normal bath throughout each capacity sequence, prove a reliable rate above 3/2 or a converse excluding such a gain on a nonzero interval. Fixed nonzero feedback equality also remains open.

The new theorem proves `Q(V_s,tau)>=3/2` for every fixed s in the entire interval `[0,pi/2]`. One code sequence for each s works for every fixed normal tau. The prior upper bound remains `Q_backward_classical <= B(.01)=1.58164276090312...` in the small-angle interval. A decrease is no longer possible. This is an internally proved source-complete checkpoint, not external certification or a complete capacity solution.

The scientific mission remains live. The former balanced-only method is closed as a route to a gain, because its entire input dimension exponent is at most 3/2. No automatic return to reserve and no new management or publication assignment follows.

## Fixed physical contract

The same qutrit port and countable tree bath, exact root labels, U edge reversal, V_s=alpha U+i beta I, faithful reference eta and tau_pi. All forward calls, outcomes and retained registers counted. Arbitrary reference preservation. No reset, replenishment, bath access, preshared entanglement, backward quantum wire or free forward timing. Terminal return is not required by the perturbed-capacity contract. Normal instruments and measurable controls remain mandatory when feedback is used.

For the next operation fix **beta=1/512**, alpha=sqrt(1-beta^2), and the actual initializer **tau_pi**. Do not choose s with n or silently substitute a more convenient initializer.

## Exact current representation

Delete the exceptional root-port-0 edge. Then E=C^2_seed tensor binary Fock space. S_a creates a color, R swaps the two vacua, P0=R^2, and

`U = [[R,S1,S2],[S1*,0,0],[S2*,0,0]]`.

`tau_pi=(I2/2) tensor ((2/3) sum_w 6^(-|w|)|w><w|)`.

The code in `representation/` computes finite word amplitudes and their exact stationary final-bath overlaps in the F_uv,K_uv normal-form algebra. It never introduces a reflecting artificial boundary.

## Chosen next scientific operation

Test whether a coherent, high-entropy port input can prevent extensive bath information growth under the actual infinite reduced channel

`Phi_(s,rho)(tau)=Tr_port[V_s(rho tensor tau)V_s*]`.

Use the concrete starting family

`rho_(q,g)=[[q,ig,0],[-ig,(1-q)/2,0],[0,0,(1-q)/2]]`,

initially at `q=1/2-3 beta^2/32`, `g=beta/8`. These are exactly rational matrix entries at the fixed beta. Its entropy is certified to be

`1.50000011920888232206098894420954476211716...` bits.

That is a finite algebraic feasibility check, not the bottleneck. The load-bearing question is whether the iterates from tau_pi have a normal tight limiting state or a sufficiently controlled information/overflow bound to support a rate above 3/2. A stationary state of a finite reflecting cutoff says nothing by itself about this infinite-bath question.

The exact drift identity is

`d_s(rho,tau)=alpha^2(1-2q+q p0)+2 alpha beta Im sum_a rho_a0 Tr(tau S_a)`.

For this seed, positive real Tr(tau S1) supplies a negative coherent cross term. The drift is a bounded-increment expectation, also for infinite-mean normal states. One-step cancellation does not prove stationarity, tightness or low information leakage.

First derive the exact reduced-channel equations or a normal positive-state/Lyapunov construction on the Fock algebra, retaining the vacuum and both seeds. Determine whether coherence survives the noise strongly enough to keep the relevant bath information subextensive. If a candidate normal invariant state uses a different initializer, prove reachability from tau_pi with all preparation calls counted and sublinear overhead before claiming communication consequences.

If a controlled environment estimate is obtained, the next obligation is a high-entropy input typical-space or one-shot decoupling argument with arbitrary-reference error, not an IID coding theorem applied to a freshly reset bath. The present compression lemma provides a reusable sufficient interface when its hypotheses can be verified, but its particular r*sqrt(delta) bound is not a necessary condition for capacity.

## Closed methods and preserved failures

- Entire balanced/Dyck or critical-type input families have dimension exponent <=3/2. Searching for a gain only within them cannot succeed.
- The balanced coherent filter is exactly bath-returning and has norm alpha^2 at every length. The known protected subspace has dimension m+1. Its top singular multiplicity is not known in general, and finite counts are not an all-length theorem.
- Diagonal input q<1/2 has positive depth drift mu=alpha^2(1-2q). Every o(n)-depth coordinate projection has exponentially vanishing average mass. Simply biasing the critical compression proof is invalid.
- Exact PRODUCT stationarity with any normal bath and alpha!=0 forces q>1/2 and input entropy <3/2. The proposed next mechanism must use a weaker reduced-bath condition and retain correlations.
- At two calls and alpha beta!=0, no nontrivial exact subspace code exists for a faithful diagonal bath. The three-call probes were inconclusive. This is not an asymptotic obstruction.
- Operator Schmidt rank differs between U and V_s, excluding only one-use local gauge equivalence. Do not turn it into a capacity theorem.
- A one-initializer marginal channel and stationary bath return cannot justify memoryless reuse. The exact two-call erasure interface works because it holds on all joint inputs.

Stop a candidate when its normal tightness or cost premise is falsified. Preserve the obstruction and revise the construction within the capacity question. Do not reopen R1, its additive constant or noisy-output work, old feedback/stopping audits, generic novelty searches, or other owners' programmes.

## Source and receiving use

`COHERENT_CAPACITY_FLOOR.tex` plus `SUPPLEMENTARY_RESULTS.tex` is the complete proof. The two load-bearing reviews are `DEPTH_LAW_REVIEW.md` and `UNIVERSAL_COMPRESSION_REVIEW.md`. `COHERENT_DRIFT_CHECK.md` checks the exact next-operation identities. The unchanged prior archive preserves all old proof obligations and provenance.

Run `python verify_package.py` for integrity. `python replay_critical.py` checks the finite density/entropy identities, and `python representation/exact_representation.py --output replay/representation_reproduced.json` checks the normal forms. Do not mistake replay cost for discovery cost or finite checks for the universal proofs. `VERIFY.md` describes the deliberate limits.

Max owns integration. The evaluator receives the same private source. Upload, receipt verification, recipient reading, scientific acceptance and integration are distinct statuses.
