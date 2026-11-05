# Independent audit of the completed preparation operation

Audited `operation_and_consequences.md` against the accepted predecessor `noisy_interface_work/operation_theorem.md`. This audit checks composition and scope; it does not reprove the accepted Bell/tree compiler or its calibration theorem.

## Outcome

The main all-temperature preparation composition is compatible with the accepted physical model. No additional ideal encoder, ideal raw port, equilibrium preparation, unknown-input promise, or bath reduction is inserted. The mathematical extension to arbitrary near-identity single-site CPTP maps is kept separate from the physically implemented independent-Pauli boundary.

## Checks that pass

1. **Positive input and approximation.** The finite sampler's block floor is eta/2. The stated delta_* bounds the block inverse correction by eta/2^(B+2), leaving at least eta/(4*2^|A|) in every inverse block. Thus finite matrix computation has a real positive reserve. The forward image of each actual sampled inverse block is its original sampled block. No claim of approximating the exact global inverse state is needed.

2. **Physical control interface.** The predecessor explicitly says its product-boundary statement applies to any protected quantum circuit. The new operation therefore may synthesize known bounded-block inverse states and use that boundary. Its fixed-error gates, preparations, resets, records, controller, links and endpoint timing remain paid. No new physical general-noise interface is inferred from the broader mathematical theorem.

3. **Acquisition error.** The acquired channels must be physical Pauli channels in the permitted radius. Comparing actual and acquired forward channels on the valid acquired-channel preimage gives half the sum of endpoint diamond mismatches. This is an ordinary CPTP telescoping bound and has no extensive inverse-condition-number multiplier. Channel-estimator projection to the physical permitted set is compatible with the stated procedure; approximation and confidence failure remain charged.

4. **Target description.** Differentiating normalized Gibbs states gives D(rho_beta(H),rho_beta(Hhat))<=beta||H-Hhat||<=beta N xi. With fixed local dimension and range this requires logarithmic coefficient precision in N/epsilon, when supplied or separately acquired. The interaction-strength bound must contain both the actual described Hamiltonian and its approximation, as the note states.

5. **Records.** Fresh ensemble labels are erased/discarded or their actual correlated extension is specified. They are not re-labelled as independent Gibbs samples. Retained calibration and pre-existing records are compatible with a uniform confidence-set error bound plus an explicit failure probability. This known-target operation does not claim transmission of an unknown reference-entangled input or a prescribed purification.

6. **Reuse and costs.** Fresh preparations compose through the uniform conditional guarantee with the stated hybrid sum. Reset, metrology, routing, occupied time, private randomness and record erasure are charged. Source sampling is retained as its actual published polynomial cost under the source numerical convention. No new bit-complexity theorem, useful sufficient threshold, energy advantage, or near-linear classical positive-mixture sampler is asserted. The newer ideal all-temperature near-linear Gibbs algorithm is a comparator and does not change this cost.

7. **Exact dimer optimum.** SU(2) twirling reduces the endpoint optimization to Werner inputs. Their reachable parameter is lambda^2 u, u in [-1/3,1], giving the exact error (3/4)(t-lambda^2)_+. The singlet or positive preimage attains it. This is a sharp channel-range statement, stronger than showing failure of one decomposition.

## Corrections applied directly to the operation note

- **Remote heralding:** the uniform spectral floor is stated for the exact Gibbs representation. For a physical output within epsilon, an outcome of target probability q>epsilon has conditional error at most 2epsilon/q. The note no longer suggests an outcome-uniform floor for arbitrarily rare events in the approximate implementation.
- **Thermodynamic limit:** fix one compatible infinite family of site channels and use its restrictions on all finite volumes. The fixed local channels then pass through a weak-star subsequential limit. Allowing unrelated finite-volume channels without specifying a limiting family would not justify the originally stated conclusion.

No further numerical testing was needed for these scope corrections. The separate finite verification suite tests the new algebra and examples only.
