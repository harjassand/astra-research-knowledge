# Independent audit and closure of the temporal rod-gas lemma

2026-11-01. **The finite-temperature ancillary free-energy lemma closes under the explicit sufficient inequalities below.** This is a mathematical statement for the exact controlled-Pauli clock Hamiltonian. It is not a noisy-hardware, bath-dynamics, or practical-parameter theorem. It does not replace the separate decoder-witness transfer.

Reviewed `ROOT_EXCURSION_PROOF_TARGET.md` and `independent_constructor.md`, and independently reran `root_seed_clock.py` without rewriting its results. The exact seed gauge residual is zero on all 324 oriented edges. Cross coefficients agree with the saved values. Those finite checks are corroboration only.

## 1. Exact pair-factor algebra

Assume common K≥3; within each check the K factors are commuting single-site Hermitian Paulis/identities whose product is S_g. Let F_g(q) be its prefix and U(q)=F_1(q_1)...F_M(q_M), in the fixed bounded-color order. For a hop at g labelled P, let c=1 precisely for the closing edge, in either orientation. Its dressed label is

    S_g^c × product_{h<g} chi(P,F_h(q_h))
            × product_{h>g} chi(S_g^c,F_h(q_h)),

where chi is the ±1 Pauli commutation sign. This follows by moving P through the earlier prefixes, using F_g(q'_g)^† P F_g(q_g)=S_g^c, and conjugating the latter through the later prefixes. No three-clock factor is introduced. Reverse hops have the same sign at the unchanged other-clock coordinates.

Thus every closed worldline weight is a product of its individual closing-edge flux signs and pairwise clock-history signs. The latter depend on full hop times and internal states, not just lengths. A pair sign can differ from one only when the two clocks are neighbors in the check-overlap graph and their nonzero intervals overlap: F_h(0)=I. Once split into excursions, each sign contribution is assigned to the unique pair of rods present at that hop. Multiplying both directional contributions defines a symmetric pair factor. Same-clock overlap has factor zero. All other pair factors are ±1, hence h_ij∈{0,±1}, |h_ij|≤1, and f_ij=h_ij−1 has |f_ij|≤2.

## 2. Exact measure on the time circle

Use the continuous-time Duhamel trace with a fixed labelled time origin and circle circumference beta. For each clock there are precisely two possibilities, up to zero-measure coincident jumps:

1. It visits zero. Its maximal open intervals at nonzero clock position are ordinary rods. Each rod has its unique exit-from-zero hop as start u∈[0,beta), duration 0<l<beta, its entry and exit neighbors in {1,K−1}, and its ordered internal hops on the path {1,...,K−1}. Its measure is du dl times ordered internal-hop Lebesgue measure, t^(number of hops) exp(−Delta l), and its single-clock flux sign. An interval crossing the fixed time origin is represented by its start and positive circular length, with no additional marker.
2. It never visits zero. There is exactly one wrap rod on that clock. Its label is the initial nonzero position and the ordered internal hops in [0,beta), with equal initial/final position. Its measure is t^(number of hops) exp(−beta Delta) times ordered-hop measure. It occupies the full circle and conflicts with every rod on that same clock. Stationary paths with zero hops are included.

Sorting and gluing compatible rods recovers exactly one original clock history, including its state at the time origin. Conversely, splitting a history recovers those rods. The gas sum uses 1/k! for unordered rods. A rod with ordinary duration l has start measure beta, NOT beta−l. There is no division by the number of zero crossings, and no multiple choice of zero marking. Wrap paths have fixed-origin trace parametrization, not an extra integral over starts. These conventions remove both potential overcounts.

At finite volume all these measures are finite. Summing absolute internal paths gives, with T the adjacency matrix of the (K−1)-vertex path,

    A(l) = t² v^T exp(t l T)v exp(−Delta l)
         ≤ 2t² exp[−(Delta−2t)l],  v=e_1+e_(K−1),
    W0 = exp(−beta Delta) Tr exp(beta t T)
       ≤ (K−1) exp[−beta(Delta−2t)].

This includes ALL real ancillary excitations, not a vacuum-projected trace. A never-zero wrap cannot cross the closing edge and has no individual flux. Its pair signs with other rods are nevertheless retained.

## 3. Soft-sign cluster theorem and explicit KP inequalities

Primary checked source: Daniel Ueltschi, *Cluster Expansions & Correlation Functions*, https://arxiv.org/pdf/math-ph/0304003v3, Theorem 1. Its complex-measure continuum theorem allows general pair factors with modulus at most one; it is not restricted to hard-core interactions. Its integral criterion gives an absolutely convergent logarithm and a rooted connected-cluster bound by exp(a(root)). Thus it applies to these signed factors. Equivalently, the connected-graph induction uses |product_j(1+f_j)−1|≤sum_j|f_j|, valid here; negative pair signs cause no missing stability factor.

Let D≥1 count a clock and all its interacting neighbors. Fix a spatial diameter weight mu≥0, and set

    r=t/Delta, Dbar=D exp(mu),
    a0=64 Dbar r², b=32 Dbar t²/Delta,
    d=Delta−2t−b.

Sufficient assumptions are

    a0≤log 2,
    2r+32 Dbar r²≤1/2,
    (K−1) exp[−beta(Delta−2t−b)+a0]≤r².             (H)

Give ordinary rods charge a0+b l and wrap rods charge a0+b beta. Inflate the absolute measure of each nonroot rod by exp(mu), to pay spatial support weight. A fixed ordinary rod of length l has overlapping start measure at most l+l' for a neighboring ordinary rod, even on a circle. Consequently its KP integral is bounded by

    4 Dbar exp(a0)t² [l/d+1/d²]
       +2 Dbar exp(a0+b beta)W0.

Under (H), d≥Delta/2 and exp(a0)≤2, so this is at most

    16 Dbar(t²/Delta)l + 34 Dbar r²
    ≤ b l+a0.

For a wrap root, the overlapping ordinary start measure is exactly beta, and the same bound with l=beta is conservative. Neighboring wrap activities obey the same endpoint budget. Thus KP holds for every trajectory label, not only for a time-integrated average. The strict spare constants may be used for limiting/discretization arguments.

The thermal inequality in (H) is essential. At fixed beta Delta one cannot simply send r→0 while insisting that wrap fugacity fits an O(r²) endpoint charge. For any sufficiently small fixed r it is satisfied by sufficiently large beta Delta. It is consistent with beta J0 being large, where J0=2 Delta r^K. These are fixed-parameter, volume-independent conditions.

## 4. Winding support and the leading coefficient

A first-return path from zero that avoids zero internally has winding 0,+1, or −1. It winds iff its entry and exit nonzero endpoints differ. Because the interior graph is a path, it cannot accumulate multiple full windings. Its parity of closing-edge crossings is therefore exactly the single flux exponent. Wrap rods have exponent zero. Pair factors are flux-independent. Hence every flux-dependent cluster contains at least one winding ordinary rod, and any Fourier monomial containing g has a winding rod on g.

The exact absolute winding density is

    A_w(l)=2t² exp(−Delta l)[exp(t l T)]_(1,K−1).

The minimal paths contribute

    A_min(l)=2t^K exp(−Delta l) l^(K−2)/(K−2)!.

Their single-rod contribution to free energy is

    −J0 [1−Q_(K−1)(B)] sum_g s_g,
    J0=2t^K/Delta^(K−1), B=beta Delta,
    Q_(K−1)(B)=exp(−B) sum_{j=0}^{K−2} B^j/j!.

This is the RAW one-rod coefficient. It is not the exact isolated-clock Taylor coefficient: normalization by 1+(K−1)exp(−B) and spectator wrap effects come from additional clusters. They are included in the remainder below, not omitted or silently absorbed into J0.

## 5. Explicit marked-winding bound and local Fourier potential

The absolute cluster theorem gives, after removing the single-root term, a rooted ≥2-rod bound exp(a(root))−1. If a cluster has k rods, its spatial clock graph is connected and the diameter of its nonempty flux support is at most k−1. Inflating the other k−1 measures by exp(mu) therefore pays exp(mu diam(A)). Mark one winding rod on a selected g. This can overcount a cluster but never undercounts one whose flux monomial contains g. Integration over its start contributes beta and cancels the free-energy factor 1/beta.

We obtain the concrete bound

    sup_g sum_{A contains g} exp(mu diam(A)) |r_A|
      ≤ J0 Q_(K−1)(B)
        + integral_0^beta [A_w(l)−A_min(l)] dl
        + integral_0^beta A_w(l)[exp(a0+b l)−1] dl.        (*)

Here F_beta(s)=c_beta−J0 sum_g s_g+sum_nonempty_A r_A product_{g in A}s_g. Absolutely convergent grouping gives this actual scalar Fourier potential on the full formal flux cube, then restricts to physically allowed syndromes. It is a local interaction bound, not an extensive partition-function error.

For completeness, (*) implies an entirely explicit relative estimate. A walk from 1 to K−1 has length K−2+2j. Its count is at most 2^(K−2+2j), and the j=0 path is unique. Integrating the ordered-time simplex gives

    integral_0^beta (A_w−A_min) ≤ J0 [2^K r²/(1−4r²)].

Also the number of walks of length L+2j with net displacement L=K−2 is at most binomial(L+2j,j). Therefore

    A_w(l)≤2t^K exp[−(Delta−2t)l] l^(K−2)/(K−2)!.

Using exp(a0+b l)−1≤exp(a0+b l)(a0+b l), d≥Delta/2 and exp(a0)≤2 yields

    integral_0^beta A_w(l)[exp(a0+b l)−1] dl
       ≤ J0 [64 K 2^K Dbar r²].

Thus the sufficient final estimate is

    sup_g sum_{A contains g} exp(mu diam(A)) |r_A| / J0
      ≤ Q_(K−1)(B)
         + 2^K r²/(1−4r²)
         + 64 K 2^K Dbar r².                            (R)

Constants are intentionally conservative. At fixed K,D,mu, choose r small enough and then B large enough to make (R) any desired positive margin. All wrap clusters are included through KP; no global probability of all clocks being in zero is assumed. The surviving extensive density of real excitations is compatible with this local free-energy result.

## 6. Remaining scope and independent cross-checks

The proof above establishes the targeted scalar ancillary free-energy premise for the EXACT specified clock Hamiltonian. It is not an application to arbitrary perturbations of clock interactions or an unknown bath. The fixed K padding, exact onsite penalty, single-site Pauli/identity factors, exact ordered-prefix dressing, bounded overlap degree, and parameter inequalities are material assumptions.

The root's separate trace-component deletion comparison can now use (R) once its syndrome-flip count and decoder support are checked. A Davies or exact physical-environment lifetime theorem still needs its own dynamical hypotheses and logical initialization/readout admission. No claim of practical constants, hardware realization of arbitrary qudit couplings, or historical novelty follows.

Coordinated with the other independent auditor: their Cauchy/slab route and exact isolated coefficient are separate checks, not assumptions in (*). The marked-winding proof deliberately avoids needing uniform high-order coefficient estimates in beta t and avoids substituting the raw one-rod coefficient for the normalized isolated coefficient.
