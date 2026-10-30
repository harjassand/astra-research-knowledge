# Continuous-noise memory without a fixed noise-interaction graph
2026-10-30. Root extension candidate for independent review. Applies to the accepted continuous weighted-barrier theorem, not automatically to the stochastic spacetime witness theorem.

## Consequence sought
The existing continuous theorem declares bounded local support/incidence and enlarges its DATA graph by noise-support cliques. The latter enlargement appears unnecessary. If removed correctly, the same finite-rate simple-compiler memory can tolerate arbitrary time-varying bounded-body system/bath couplings with a uniform per-site strength budget, even when the UNION of their system supports has unbounded degree. Neither the noise coupling graph nor the environment must be reconstructed.

Nominal code/controller interactions and proof circuits retain their fixed bounded-degree geometry. The noise strength remains a genuinely bounded joint operator/generator norm, not only a mean power or a reduced-state fit. Unbounded-strength bath couplings are not covered.

## 1. Fixed graph needed only for code and nominal operations
Construct the DATA component graph G from check overlap, full nominal read/correction supports and the finite nominal gauge/credit footprints. In particular every stabilizer check's DATA support is a clique, and the accepted J_x container geometry remains available. DO NOT add a clique for a potentially distant noise support Z.

Let E be a sectorwise minimum representative with all G-components smaller than ell. Let P be ANY DATA Pauli supported on at most s sites, possibly in many distant G-components. Let F be a minimum representative of the new syndrome. Form connected components K of the induced G-subgraph on

    supp(E) union supp(P) union supp(F).

Because a check touching two such components would connect them by a check-overlap edge, the identity sigma(E)+sigma(P)+sigma(F)=0 holds separately on every K. Therefore replacing F on K by (E+P) on K preserves syndrome. Minimum weight gives

    |F intersect K|<=|(E+P) intersect K|,
    |K|<=2(|E intersect K|+|P intersect K|)
         <=2(|E intersect K|+s).                      (1)

No step requires the entire support of P to lie in one K or form a clique. Each original E-component meeting K is wholly inside K. Its confinement gives actual source occupied mass at least h|E intersect K|. The same connected container J(K) has size <=D0|K|. Thus any K of size >=ell implies exactly the original exponentially high source potential barrier, with s unchanged.

If every K is below the code distance, E P F restricted to each K is a stabilizer up to phase; their product has identity logical action. This proves the canonical local-edge lemma for bounded-cardinality disconnected supports. A shared bath coefficient in the Pauli expansion does not change that algebra.

## 2. Pointwise noise drift needs strength incidence, not graph degree
Let the perturbation at time t be a sum of HP identity-annihilating local generator terms N_Z,t*, where each Z contains at most q physical system sites (and an arbitrary shared bath). Assume

    sup_(i,t) sum_(Z containing i) ||N_Z,t*||_cb <=eta.

The set of supports may vary with time and its union may be dense. Fixed finite site dimensions and the nominal geometry imply that a q-site term can change at most kq commuting syndrome/flag factors of an animal f_A. All factors outside this affected set commute through it. The same relative-orbit estimate gives

    +/-N_Z,t*(f_A)<=C_q ||N_Z,t*||_cb f_A

when Z touches the physical support of f_A, and zero otherwise. That support has at most b|A| sites, so summing the actual norms gives

    N_t*V <=C_q b eta W.

This estimate counts strength, not the number of possible partners of a site. It is uniform over support patterns and time. It therefore also covers a dense family of weak terms whose summed incident norm is bounded.

For a physical Hamiltonian/Lindblad noise model use the usual cb norm bounds for each term and require the FULL joint time-local dynamics to have CPTP propagators on every time interval (with a well-defined CP trace-nonincreasing killed compression). Hamiltonian/GKLS joint dynamics is sufficient under the usual existence/domain conditions. Mere endpoint existence or an arbitrary signed HP perturbation does not supply this physicality premise. For time-dependent coefficients the inequality is applied pointwise; no stationarity or temporal independence enters.

## 3. Nominal dressing does not restore a hidden topology restriction
The forest/guard frame and every accepted CP credit have fixed depth and bounded nominal support. A perturbation on q distant sites expands only to the union of q bounded causal cones, of size at most q'=Cq. For any site j in an expanded support, the original support met one of only O(1) sites in its backwards cone. Therefore the expanded per-site norm incidence is at most C eta. The conjugated term may remain disconnected; Section 1 already permits that.

For the positive CP noise-transfer argument, use the local Stinespring dilation of the fixed nominal circuit. Conjugation preserves the joint cb norm and the same bounded-cone counting applies. Activity congruence is not needed for this extension of the already accepted simple compiler; a later native construction would require its actual analogous bound.

## 4. Killed basin and total error budget
Keep the original raw-potential/component basin based on the NOMINAL graph G. The edge proof in Section 1 prevents logical/component escape from low-potential source states for every noise Pauli term. A bounded q-site operator changes only O(q) label factors, so any cutoff-exit source still has V>=cM. The union of all such sources is bounded by this SAME high-potential projector, even if possible noise partners form a dense graph.

The total perturbation norm budget is at most N_phys eta, since summing per-site strengths overcounts every nonempty support at least once. Nominal total norm is O(N). Thus the existing Duhamel comparison retains O(N t sqrt(N/M)), with no extra factor counting possible noise hyperedges. Bath-only dynamics commutes with the barrier and is handled separately.

Subject to independent confirmation, the accepted Tanner simple-compiler conclusion therefore remains

    ||Dec_frame E_t Enc-id||_diamond <=C N^(3/2)t exp(-cN)

for this stronger bounded-body, bounded-incident-strength, time-varying noise class. All controller sites may be perturbed. Initial bath independence, fixed nominal hardware, encoded input/ideal framed output and impractically small possible thresholds remain explicit.

## 5. Scope separation
This is NOT a claim that fixed conflict-coloring assumptions can be removed from the separate Poisson physical-cell/ancestor-witness proof. That proof uses actual noisy support overlap and has its own counterexamples to cardinality-only coloring. The present route uses an instantaneous operator drift and a disconnected-support canonical edge argument instead.

Nor does a bounded average bath energy imply the required joint-norm bound. Arbitrary global high-amplitude bursts, unbounded system-bath operators and support size growing with N are outside this statement. The proposed gain is freedom from a fixed known noise topology, not removal of every physical noise assumption.
