# Binary isotope controls already identify simple ancestry in the ideal limit

Status: conditional information theorem and explicit readout construction. This is an application of established random-set avoidance theory, not a new probability theorem, experimentally validated tomography, or novelty claim. It refines the worker's correct multiplicity counterexample; it does not invalidate it.

## The representation that changes the interface requirement

The unrestricted ancestry object is an unordered multiset of n atom-entry ages. The isolated information worker proved ideal identification using arbitrary interval-valued isotope probabilities and gave two distinct six-atom laws invisible to every binary waveform. Its counterexample has coincident entry ages: its occupancy vectors are even versus odd permutations of (0,1,5) on three time nodes. That assumption matters.

Suppose instead the n ages are almost surely pairwise distinct. Then the multiset is a simple finite random set. Its law is determined by avoidance probabilities

    v(B)=P(no entry age belongs to B)

for all Borel age sets B. Thus binary isotope controls and whole-product counts already suffice in the same ideal infinite-control/prehistory limit. No additional isotope-composition level is required for identifiability under this extra simplicity premise. It remains unestablished whether the relevant physical entry convention and time resolution satisfy this premise.

## Direct avoidance projection with imperfect purity

Use actual calibrated isotope probability p_H on B and p_L off B, where 0<=p_L<p_H<=1 and a=p_H-p_L. Let J be the number of ancestral entries in B and K the detected whole-product heavy-isotope count. Conditional independent labels give

    E[t^K | J] = (1-p_H+p_H t)^J (1-p_L+p_L t)^(n-J).

Evaluate at t=-(1-p_H)/p_H. The high-level factor is zero and the low-level factor is a/p_H. Therefore the finite count statistic

    V_B(K)=p_H^(n-K) [-(1-p_H)]^K / a^n

satisfies E V_B(K)=P(J=0)=v(B). This identity holds with repeated ages too; only the subsequent interpretation of the entire multiset requires simplicity. The high/low waveform, synchronized product time, relevant prehistory, count calibration, conditional label independence and isotope-neutral ancestry are real acquired interface assumptions. The waveform can contain multiple intervals; a single rectangular pulse is insufficient to supply arbitrary B.

The decoder uses n+1 count bins. A range bound is

    |V_B| <= R = [max(p_H,1-p_H)/a]^n.

At p_H=0.99,p_L=0.01,n=4, R=(99/98)^4, about 1.04145. For N iid conditional products a conservative Hoeffding bound is

    P(|v_hat-v|>epsilon) <= 2 exp[-N epsilon^2/(2R^2)].

This is only a product-sampling bound conditional on a deterministic calibrated waveform and a fixed stationary ancestry law. It does not bound chemistry correlation, drift, shared preparation, detector inversion or unknown prehistory. Small purity contrast can make R very large.

## Elementary proof of the simple-law conclusion

Partition a bounded age interval into half-open cells I_1,...,I_q. For the random set of occupied cells O, the probability of O=S is obtained exactly by inclusion-exclusion:

    P(O=S) = sum_(T subset S) (-1)^|T| v(union_(j in S^c union T) I_j).

All terms on the right are acquired by binary masks and the avoidance projection. Hence the occupied-cell set law is identified at every partition resolution. Use nested partitions with mesh tending to zero, then let the bounded interval increase to the whole nonnegative age axis. On each realization with finitely many distinct finite ages, sufficiently fine cells separate all ages; the occupied cells locate each age with error at most the mesh. The resulting simple point measure converges realization by realization to the true unordered measure. Thus equality of every avoidance probability implies equality of the simple unordered law. This is a determination theorem, not a stable finite-data inversion.

This is established random-set mathematics. Root independently derived the finite partition argument before checking Ilya Molchanov's *Lectures on random sets and their applications in economics and finance* (18 June 2012), Section 1.3 and Example 1.26, which explicitly state the simple-point-process avoidance characterization. Root read the relevant PDF text at pages 5-8 and the opening definitions; no claim to have read all 32 pages. [Primary author lecture notes](https://www.cemmap.ac.uk/wp-content/legacy/resources/molchanov_mc/lectures_sets.pdf). The decoder above is a direct binomial generating-function evaluation. Its historical application to isotope-ancestry tomography has not been cleared.

## Finite-bin operation and a sharp boundary

If ages occupy q known bins with at most one entry per bin and exactly n entries, the possible histories are the M=choose(q,n) occupied subsets. For a candidate S of size n, program B=S^c. Then

    v(S^c)=P(O subset S)=P(O=S).

M such binary masks therefore directly obtain the entire finite-bin law using this one projection per histogram. No hidden reaction network is reconstructed. A generic dimension count with complete n+1-bin histograms gives the necessary lower bound J n>=M-1, so the explicit M-setting scheme is not claimed optimal. Union-bounding the preceding sufficient concentration inequality costs at most

    N >= 2R^2 epsilon^-2 log(2M/delta)

independent products per setting for simultaneous entrywise error epsilon. Full-distribution accuracy additionally pays for dimension; estimating one decision functional need not do so. The number of settings, isotope dose, wash-in between distinct programs, time alignment, finite slew and effective independent product rate all remain charged.

If a declared binning has collision probability at most eta, a size-n candidate's containment probability can receive up to eta from histories with collisions. Thus the simple-model coordinate estimate has an extra absolute bias at most eta. Without an acquired separation or collision bound, arbitrarily close distinct entries can be indistinguishable under finite bandwidth even though the ideal law is simple. Arbitrarily old inventory similarly blocks finite preparation. Exact mathematical simplicity is not a free experimental resolution assumption.

The six-atom even/odd occupancy counterexample remains an exact failure for general multisets under all binary waveforms. Avoidance identifies the underlying support set and loses multiplicity; its two support-set laws agree. Interval-valued controls/polarization still supply a general multiset-identification interface in the ideal limit. Neither argument grants low-cost practical reconstruction.

## Consequence for the joint Markov operation

The root three-level Markov code has an explicit history-shift-invariant kernel for the joint adjacent-pair length and middle gap. Its observable is useful without reconstructing a network or full age law, and all old telegraph rates fail on a provided exact witness. It is not a fundamentally more informative interface than every binary program on simple histories, nor is a third level generically necessary. Any claimed efficiency must beat optimized binary multipulse/frequency-response controls at the same information, prehistory, slew, dose, calibration and confidence. The finite tuned competitor already wins on the synthetic witness. The open physical question is a chemistry-backed decision for which a selected stationary kernel has lower total cost or greater robustness than those strongest controls.
