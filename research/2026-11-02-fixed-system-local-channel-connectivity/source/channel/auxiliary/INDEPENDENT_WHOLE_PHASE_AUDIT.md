# Independent whole phase/locality audit

2026-11-01. This is an independent whole-interface check of ROOT_PHASE_CONSTRUCTION.md, LOCAL_CHANNEL.md, LOCAL_CHANNEL_AUDIT.md and STABLE_CLUSTERING.md against the admitted actual-code encoder/Gram/gap inputs. Internal verdict labels were not used as evidence.

## Verdict and exact channel model

**The two-way specified-state construction survives in a product-work-register, arbitrary-local-block-channel model, subject to the explicit scope corrections below. No fatal mathematical locality or logical-sector obstruction was found. It does NOT currently establish a bounded-total-ancilla-density, bounded-work-dimension circuit on the unchanged physical lattice.**

The safe model is: physical memory and bath qubits have uniformly bounded density and dimension; each physical root additionally receives an input-independent local work register containing at most polylog(N/epsilon) classical bits (or a conservative fixed power thereof for buffers). Its local dimension may grow as exp(polylog(N/epsilon)). Work inputs are products across roots. Gates are arbitrary CPTP maps on geometrically bounded blocks of physical systems AND work registers, with messages and persistent records included in their deterministic causal cones. No shared nonlocal random seed, global success flag, or postselection is admitted. Registers may be discarded locally after use. Gate synthesis/runtime and work dimension are distinct resources from causal radius.

Under this model, and the inherited actual trace representation and geometric contraction premises, the construction provides channels in both directions between the normalized ground-code projector with a product bath reference and the actual weakly perturbed low-temperature Gibbs state. For every fixed inverse-power whole-state accuracy, the circuit has polylogarithmic physical causal radius and error O(epsilon+eta_n). Composition gives the same endpoint equivalence throughout a uniform strict parameter window. This is a genuine specified-state local-channel relation; it does not say the two channels invert one another on arbitrary inputs or that every gate is locally reversible.

## 1. The ancillary-resource issue is real, not a proof of impossibility

A capped root record contains a polylogarithmic number of event timestamps/marks, each with logarithmic or polylogarithmic bit length. Encoding it in ordinary qubits colocated at its root increases work-qubit density with N. Calling the register merely 'finite' does not make that density uniformly bounded. A bounded-density physical sample already containing Theta(N) occupied sites cannot in general host N polylog(N) extra persistent qubits in its unchanged volume at constant density.

Moving all registers into bounded-density cells by a size-dependent geometric dilation would change the microscopic metric/layout. It can be a useful separate implementation theorem, but is not a proof on the original unchanged lattice. Likewise a constant-memory local recomputation compiler might exist, but none is supplied. This audit does not infer a no-go from either omission.

The growing work dimension does not invalidate the claimed causal-radius or correlation proof in the stated augmented model. Independent local records cannot import remote correlations, and their spatial support is still local. The quantum spectral-flow step can discard the large classical simulation records beforehand, retaining only O(1) sign controls per actual physical check/site, so its Lieb–Robinson estimate need not acquire a growing ancillary-density factor.

## 2. Physical trace envelopes and actual local decoding

The trace diameter argument needs INDIVIDUALLY VALID isolated replay, not just an arbitrary sparse history. Given that admitted splitting premise, w<=m top inputs and alternating factor-two contraction force all active stages below O(log m). A connected trace with m objects then has at most m carrier steps, each of physical extent O(lambda^{O(log m)}). Downward correction reconstruction has the same bound by fixed branching and forward carrier displacement. This earns polynomial radius in m, including complete stencils, not merely polynomial correction cardinality. No inverse-Lipschitz embedding or physically free shortcut edge is used.

The reverse recognizer's unchanged original-syndrome copy, full backward cones, M+1 exploration cap, complete adjacent active-incidence checks, and zero outgoing frontier are essential. Omitting inactive inputs could miscompute a gate; accepting a visible fragment could misdecode a large component. With those conditions, any undiscovered higher active object would require an active path through the tested frontier. True small components terminate by isolated replay and pass. Bounded branching over O(log M) levels costs polynomial(M) support, hence physical polylog radius at M=O(log(N/epsilon)). This is not a global decoder oracle.

The all-small-component event is a probability statement only for the admitted target law. The channel must still be CPTP on every input; fixed local fallback provides this without communicating a global failure bit. Correction factors can be combined as local Pauli bits with a fixed CSS order; irrelevant Pauli phases do not alter conjugation.

## 3. Graphical sampling: the locality proof is not mixing alone

At a physical root, the connected-trace count and low activity give bounded total dominating proposal intensity. At most one compatible occupied polymer has that root. Unit rooted-death clocks therefore implement the desired death rates. Every acceptance decision reads only a polynomial-cutoff envelope, including quantum-potential dependence and compatibility stencils. Bath heat baths add bounded-rate onsite proposals.

For radius-r_u records, bounded physical density gives O(r_u^3) next-root choices. Poisson factorial moments for ordered event times supply T^k/k!, including repeated visits to the same root. Thus the quoted union bound and k_*=C[r_u^3 T+log(N/epsilon)] cap are sufficient. Fixed coloring should separate neighborhoods whose supports overlap; replacing r_u by 2r_u or another fixed multiple leaves all exponents unchanged.

Ready-event rounds with ordered same-root records and fixed neighborhood colors process the chronological dependency DAG within the height budget. Conservative coloring overhead gives the stated O(r_u^7 log(N/epsilon)) radius. Timestamps need enough precision to charge ties globally, not an epsilon-scale number of execution rounds. Capped fallback makes the radius deterministic on bad records as well. The construction therefore supplies an actual finite block circuit, not only a stochastic-process mixing estimate.

## 4. Controlled quantum spectral flow and invalid labels

The full controlled parent is a local operator built from mismatch projectors, not a sum of separately norm-bounded exponentially many sector operators. Its root-connected expansion and derivative inherit the physical interaction bound uniformly in all sign strings, valid or invalid. The control bits commute with parent, derivative, and every filtered evolution.

Define one quasiadiabatic filter whose Fourier transform has the required inverse-frequency value outside the VALID-sector gap. Its integral defines a Hermitian generator on the full finite Hilbert space regardless of invalid-block gaps. Physical LR estimates for that integral use interaction strength and filter decay, not a spectral gap of the complete controlled operator. In each invariant valid block, the same integral is exactly the gapped spectral-flow generator. Therefore it transports the rank-two kernel there. This is a valid extension of the controlled-flow argument, not an illicit use of a global gap theorem.

For exponentially physical-local parents, a conservative stretched-exponential generator tail permits logarithmic-squared range truncation. Coarse blocks have strength O(r^3); O(r^3) path-time slices plus logarithmic overlap yield the cited log^9 causal-radius upper bound. Arbitrary block gates are essential to this statement. Their dimensions or elementary implementations may be exp(polylog), so no native polylog-time or simultaneous polynomial-gate theorem follows.

The maximally mixed logical sector removes holonomy from this specified-state task: any unitary transport of the same rank-two subspace maps its normalized projector identically. Near-scalar Gram, with weights Tr G_a/Z, then compares the weighted filtered projectors with the actual Gibbs state at O(eta_n). Reverse measurement gives actual Gibbs blocks B_a G_a B_a dagger/Z, so it does not attempt to infer a hidden label of a nonorthogonal ensemble.

## 5. Correlation consequence: valid, dimension-free, and restricted

For source regions X,Y with no common touching check and |X|<d, a stabilizer supported on X union Y splits into two centralizers. Distance makes the X factor a stabilizer, hence the Y factor also one. The converse is immediate. Pauli coefficients therefore prove exact reduced-state factorization of P_0/2 on X:Y. This is an equality of density operators, not an expansion of an arbitrary exterior operator with an exponentially bad norm loss.

Product work environments preserve this factorization. If deterministic backward cones are disjoint, their pulled-back operators act on independent source factors and independent environments, giving zero output covariance. Trace-norm continuity costs at most three times whole-state error. The argument is unaffected by growing LOCAL register dimension. It would fail with an uncharged globally shared random seed.

Consequently, for each fixed k and suitable small inner region A, separation C_k log^q N and |A_R|<d gives covariance at most N^{-k}+O(eta_n), uniformly over arbitrary norm-one exterior operators. The advertised distance-dependent stretched-exponential form additionally requires using the construction at epsilon=N exp[-cR^{1/q}] and checking M<Cd. The component estimates support this extended cutoff regime; an inverse-polynomial-only theorem statement by itself would not justify extrapolation. Where epsilon>=1, simply use the trivial covariance bound.

The inner-region radius must remain small enough that |A_R|<d; fixed/polylog-radius A satisfies this asymptotically. This is neither the all-annulus nor the exponential-distance stable-clustering definition of MKS. Parameter-uniform constants give stability under a strict local perturbation neighborhood, but do not remove these geometric/exponent qualifications. Product-phase separation and gate-by-gate local reversibility remain unproved and correctly unclaimed.

## 6. Primary-source comparison

[Xun–Cao–Watanabe, 2610.27939v1](https://arxiv.org/html/2610.27939v1), Section II.4 and supplementary S44, explicitly use product local work records and arbitrary geometric block maps, count messages toward radius, and derive the ordered-event path cap. Its controlled spectral-flow section supplies the block-slicing precedent. It does not furnish the present quantum-code gap or a bounded-density compiler for persistent polylog-bit work registers. The present result should be labeled in that same work-register model, not automatically a stronger hardware model.

[Ma–Khemani–Sang, 2509.15204v3](https://arxiv.org/html/2509.15204v3), Definitions 1–3, require exponential annulus covariance for their stated stable-clustering premise and distinguish gate-by-gate local reversibility. Endpoint two-way connectivity and restricted stretched correlations do not by themselves establish those stronger properties. The direct channel construction bypasses, rather than verifies, their full hypothesis.

## 7. Scope corrections and decision boundary

1. Explicitly distinguish bounded physical-system density/dimension from growing work-register dimension/density. Name the product-work-register block-channel model in the main theorem.
2. The inherited gap completion was explicitly for bath QUBITS. The new phrase 'all onsite Hilbert dimensions bounded' needs a constant-size qubit embedding/unused-level-invariance extension, or the theorem should simply retain bath qubits. This is a fixable scope issue, not an identified physical obstruction.
3. Keep cutoff M<Cd, whole-state intrinsic remainder, known couplings and all bath access, and the absence of efficient block synthesis.
4. Keep restricted stretched covariance distinct from MKS full stable clustering, endpoint equivalence distinct from local reversibility, and connectivity distinct from nontrivial phase separation.

With these qualifications, no new fatal mathematical join was found. This audit accepts the specified inherited actual trace/code/Gram/gap inputs rather than re-proving every source construction. It independently checks their physical-locality/channel/observable composition. No external contact/publication or stopped-source retrieval occurred.

## Reviewed snapshot hashes

- `ROOT_PHASE_CONSTRUCTION.md`: `48a63027ac3d9b5ae5ec3f4c7e82de323c9059aad120f4133fcf4a44569f4dca`.

- `LOCAL_CHANNEL.md`: `d6f8c9f180b2f43a292ee5b8ac33cef666a2ec61ea1ddffac8934c8f67c0cfff`.

- `LOCAL_CHANNEL_AUDIT.md`: `6859ddacdb13d62bd39d7b94a6292c4a6f5c3df1e0b62eb99e4189604006eb0a`.

- `STABLE_CLUSTERING.md`: `f6bcf0b1b02b18b1eadcd59b0dc6b9c50053ccb75c68246a88d91f9ee7965f39`.
