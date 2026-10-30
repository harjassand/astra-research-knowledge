# Independent hostile audit: weighted SSF connected-animal progress
2026-10-29. No publication; no global/noise threshold is claimed by this review.

Reviewed candidate:
`producer-workspace/WEIGHTED_PROGRESS.md`
SHA256: 6b4dcbfa813840e09f6ef6d24623dcebe5ee1737059bddc5aadaedd2b0cd69eb.

## Verdict
**The weighted-drift algebra is valid, and its container interface can be constructed from the actual FGL SSF code geometry.** The explicit construction below replaces the candidate's informal fixed-radius explanation and verifies disjointness, connectivity, true global activity, assignment and counting constants. I found no counterexample to the per-move charging, rich/poor decomposition, or the claimed drift on the stipulated small-reduced-component basin.

This establishes a clean ideal-atomic SSF drift lemma, not a continuous-coherent-noise memory theorem. A logical/exit barrier, a valid quantum stopping/escape argument, and any transfer to finite-duration controllers remain separate obligations. In particular the syndrome potential cannot distinguish a logical Pauli from the vacuum by itself.

## 1. Explicit noncircular FGL container construction
Work in one CSS sector. Let Q be its check set, V its DATA sites, and h its SSF hubs. Use the actual finite candidate family of FGL (or a superset). Define:

- A_h: the generator support on which hub h may flip subsets.
- B_h: every check whose value can be changed by any allowed subset at h; using all checks incident to A_h is a safe fixed choice.
- R_h=A_h union union_{q in B_h} supp(q): the COMPLETE syndrome read footprint.
- Gamma(v): checks incident to DATA site v.
- J_v=Gamma(v) union union_{h:v in R_h} B_h.

All these sets and incidences are bounded for a fixed-degree expander-code family. In particular D0=max_v |J_v| is independent of N.

Construct a fixed DATA graph H containing an edge u--v whenever J_u intersects J_v, and also all desired original read-footprint/local-support edges. Explicitly including every R_h as a clique is harmless and removes any convention about empty candidate/check sets. This is a bounded-degree graph: each J_v has bounded size, each check belongs to only boundedly many J_u, and added footprint families have bounded incidence.

Construct a fixed CHECK graph G_Q containing each J_v as a clique and, for every H edge u--v, the entire J_u union J_v as a clique. Again the degree is bounded independently of N. These constructions are performed once from the code/hub footprints; J_v is NOT recursively redefined using the new graph.

For an error representative E, let C be the connected components of H[E], and put

  J_C=union_{v in C} J_v,     S_C=sigma(E intersect C).

Then:

**Disjointness.** If J_C and J_C' overlap, there are u in C and v in C' with J_u intersect J_v nonempty. H then contains u--v, forcing C=C'.

**Connectivity.** Each J_v is a clique; along every path in C, successive J_u union J_v are cliques in G_Q. Thus J_C is connected. This remains valid if H contains extra fixed bounded-degree edges beyond the intersection graph.

**Exact occupied content.** Suppose an occupied check q lies in J_C. Some actual error site u incident to q has q in Gamma(u), hence in J_u. Since q also belongs to some J_v with v in C, u is in C. The same argument applies to every error site incident to q, so there is no cancellation between components. Conversely sigma(E intersect C) lies in J_C. Therefore J_C contains exactly S_C among globally occupied checks, and the S_C partition sigma(E).

**Size.** |J_C|<=D0 |C|. If E is stabilizer-reduced, every subset E intersect C is reduced by FGL Lemma 17. If each |C| is below the FGL cutoff, Lemma 15 gives |S_C|>=h|C|. Thus |J_C|<=b0 |S_C| with b0=D0/h. A nonempty C cannot have S_C empty under these hypotheses.

Only the relevant components need be small. The total weight of E may be extensive. A fixed sectorwise minimum-syndrome representative is sufficient to supply stabilizer-reducedness; minimum full-Pauli support is not a substitute for sectorwise reducedness.

## 2. Genuine global activity and unique hub assignment
An accepted correction has positive syndrome decrease and therefore its syndrome support contains an occupied check q. Some erroneous site v incident to q lies in R_h. All erroneous sites in R_h lie in the same C because R_h is an H clique. Assign that active hub uniquely to C.

Every chosen syndrome-flip support D_h is contained in B_h, which is contained in J_v and hence J_C. It is a clique in G_Q. An active hub cannot be assigned to two components.

Conversely apply FGL Proposition 14 with D=0 to the restricted error E intersect C. A locally accepted candidate has a check q in its syndrome support intersecting S_C, so its hub's read footprint meets C. Every global error within that complete footprint belongs to C. Thus the syndrome on ALL checks used by the candidate agrees with the restricted syndrome. It is genuinely accepted for the global configuration, not a counterfactual restricted move. This is exactly where full read footprints are needed.

Let B=max_F |sigma(F)| and let M bound the number of candidate identities belonging to one hub. FGL's mass inequality implies at least c1 |S_C|/B valid candidate identities, hence at least

  g_C >= kappa |S_C|,     kappa=c1/(B M)

active hubs assigned to C. If a candidate can be represented at several hubs, select one fixed admissible hub for counting; bounded multiplicity still gives this conservative lower bound. Each active hub may actually choose ANY accepted subset: the chosen support remains in the same J_C. No assumption that it chooses the particular FGL witness candidate is needed.

Take k=max_h |B_h| as a safe move-size bound, and

  nu=max_q #{h:q in B_h}.

With one chosen move per active hub, each occupied check belongs to at most nu active supports. Counting all possible candidate identities instead only enlarges this fixed constant. These constants verify every abstract input in Section A.

Primary source checked directly earlier in this audit sequence: Fawzi–Grospellier–Leverrier, arXiv:1808.03821, Proposition 14 and Lemmas 15/17, https://arxiv.org/html/1808.03821 . Their hypotheses include the stated expander parameters and beta range; an arbitrary small finite HGP fixture is not covered merely by having bounded degree.

## 3. Per-move charging is correct
For a positive-increment animal A, let r,t count removed/added flip sites in A. Then t>r and B=A union D is connected. Direct substitution gives

  f_B(pre)/f_A(post)
  =exp[a(k_D-r-t)] theta^(m_+-r).

With L=log(1/theta), its log divided by L is

  c k_D-m_+ +(1-c)r-c t.

It is minimized at r=0,t=m_+, giving c m_--m_+. The proposed R_D is therefore a valid lower bound. At most 2^k_D animals A map to a fixed B, since A and B agree outside D. Every target B contains all flip sites and has exact loss (1-theta^d) f_B(pre); targets cannot themselves be increasing animals.

The displayed R_D condition pays at most half each target loss. The remaining half is available for EVERY connected B containing D, including those receiving no charge. Other losses may be discarded. This proves the stated strict per-move inequality. The integer d>=1 justifies replacing 1-theta^d by 1-theta.

Since m_--m_+>=beta k_D and m_-+m_+=k_D,

  c m_--m_+ >= k_D[c(1+beta)-(1-beta)]/2.

Choosing c>(1-beta)/(1+beta) and then sufficiently small theta supplies a uniform condition for all bounded move sizes. There is no volume dependence.

## 4. Sparse/rich/poor coverage audit
**Sparse animals.** f_A=theta^[(1-c)|A|-|S intersect A|], so sparsity gives the stated theta^[(1-c-eta)|A|] bound. Rooted-animal counting over all sizes gives a finite O(N_chk) bound on their weighted sum when A0 theta^(1-c-eta)<1. The extra factor m in C0 is conservative.

**Rich animals.** The incidence lower bound converts |A|f_A into 4/(kappa eta) copies of f_A assigned to intersecting hubs. Completing by D_h costs at most theta^[-(1-c)k] and has at most 2^k preimages for a fixed hub/B pair. The displayed C_rich follows, with active hub identities retained in Dsum.

**Poor components.** Non-poor components account for at most 2 n_intersect(A)/kappa occupied sites of A. For a non-rich dense animal this is less than eta|A|/2, leaving the asserted poor mass. A poor component has at least kappa|S_C|/2 chosen active supports disjoint from A. Each contains an occupied site outside A; at most nu supports can use one such site. Hence

  |S_C minus A| >= kappa |S_C|/(2nu) >= alpha |J_C|.

Complete one such component only. Added total size is at most j=|J_C| and added occupied size is at least alpha j, giving f_B/f_A>=theta^[-xi j]. For fixed C,B, at most 2^j preimages remain. The source charge |S_C intersect A| is at most |S_C|, so 2 theta^xi<=1 bounds their total by |S_C|f_B. Finally |S_C|<=g_C/kappa, and the g_C hubs for different components are distinct and all contained in B. This pays the sum over components through Dsum, not through an uncontrolled component count. The stated C_poor follows.

Combining these disjoint cases establishes W<=C1 Dsum+C0 N_chk. Sparse animals have not been omitted; they are the additive extensive term.

## 5. Untruncated sum and generator drift
The sum is over all connected nonempty animals of a FINITE graph. Thus V and W are finite for each finite N even on dense configurations. Infinite geometric sums are used only as upper bounds for the vacuum/sparse sectors.

Truncating at the error cutoff would indeed invalidate the charging map A->A union D and the one-component completion. The full sum is load-bearing.

Every individual accepted move has nonpositive V increment. Therefore lower-bounding its attempt rate by lambda is legitimate in the negative drift sum. Idle hubs contribute zero. Summing gives exactly

  L_SSF V <=-lambda(1-theta)Dsum/2
           <=-kappa_V W+b_V N_chk.

The simultaneous choices c>max{(1-beta)/(1+beta),1-alpha}, eta=(1-c)/2, and sufficiently small theta are compatible. Alpha>0 is independent of volume; moreover the incidence and container inequalities imply a harmless finite alpha<=1. No supplied weighted-expansion theorem is being assumed.

## 6. Scope and next obligations
The conclusion holds for syndromes admitting the specified sectorwise reduced representative with every H-error component below the FGL cutoff. Enlarging H must be done before defining this basin. It is not a global statement on all syndromes, arbitrary trap states, or all code families.

The clean ideal syndrome instrument acts classically on diagonal syndrome observables, so the pointwise drift has the corresponding syndrome-diagonal operator interpretation on that basin. This alone supplies neither a physically implemented basin projection nor a valid coherent exit estimate.

In particular:
- Logical Paulis have zero syndrome and vacuum V. A separate path/barrier theorem must show that an erroneous logical transition or relevant basin exit encounters large V under the actual allowed local dynamics.
- A quantum killed-basin or stopping construction must handle off-diagonal noise effects without assuming classical trajectories or uncharged projections.
- Continuous Hamiltonian/Lindblad orbit estimates must be checked with the SAME enlarged check graph and potential parameters.
- Finite-rate transactional controllers require an additional service/hypocoercivity transfer; the active ideal-SSF rate lower bound does not automatically hold for actual completions.

Thus the weighted clean-drift construction is accepted; the suggested continuous-coherent-noise memory consequence is not yet established by this review.

## Revised explicit-interface receipt
Re-read the added explicit J_v/J_C construction in the candidate. The revised source SHA256 is

eb73f1a44736fd20cad9039ea711fbc549cd4ae53e90c769c619da02eb882702.

It implements the noncircular fixed DATA/check graph construction, exact occupied-container property, unique hub assignment and kappa=c1/(BM) counting reviewed above. The remaining algebra is unchanged. The clean weighted-drift verdict applies to this revised source. B_h and R_h must retain their declared complete consulted/changed-check and complete read-support meanings.
