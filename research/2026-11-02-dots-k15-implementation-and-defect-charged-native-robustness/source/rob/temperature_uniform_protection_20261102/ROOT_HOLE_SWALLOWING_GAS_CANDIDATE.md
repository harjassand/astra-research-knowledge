# Root construction: finite-capacity holes and decorated source polymers

2026-11-02. Construction candidate for a COMMUTING reference plus weak generic local perturbations at fixed positive temperature. Not a native-clock transfer or an admitted theorem until exact regrouping, local coefficient decomposition and all KP rows are checked.

## 1. Exact candidate starting interface

Use the new audited contact-completed canonical trace gas for the commuting syndrome law. A defect polymer gamma has valid top syndrome tau_gamma, mass M_gamma, activity exp(-B M_gamma), charged trace size <=C M_gamma. Here B=2 beta J (uniform reference for clarity). Different compatible polymers have disjoint occupied top bits.

Group used perturbation labels by overlap of actual physical supports OR affected-check sets. Distinct source components A then have disjoint affected-check sets C_A, and commute with one another's affected check Hamiltonians. Write H0=H_out+sum_A H_CA with H_CA=2J sum_{a in C_A} q_a >=0. The exact commuting-reference hole lemma gives a local operator replacement O_A, with every label used at least once, and

 ||O_A|| <= product_{lambda in A}(exp(beta ||V_lambda||)-1).

Source components affecting disjoint checks cannot cancel a nonzero net syndrome flip between them; stabilizer dephasing can therefore retain only the zero-net-flip part of each O_A before the trace. This dephasing is norm-contracting. Its physical support is contained in source supports plus supports of affected check generators, of size <=b'|A|. Expand it in a finite Pauli/bath operator dictionary on this region. The number of terms and coefficient l1 overhead are at most C_dict^|A|, with no exp(beta J). Terms below distance are stabilizer words B_A, so tracing the data gives the actual character chi_BA(sigma). Large/logical words remain exceptional and must be charged separately.

Under this interface the partition expansion is exactly a sum over compatible sources and reference defect polymers, with factors

  source coefficient times exp[B |sigma intersect C_A|] times chi_BA(sigma).

The factor exp(+B occupied holes) is NOT bounded separately by exp(B|C_A|).

## 2. Canonical swallowing

In a joint source/defect configuration, join a source A to every defect polymer whose TOP occupied support meets C_A. Merge sources sharing such a defect polymer. The connected components containing a source are decorated source polymers; defect polymers touching no hole remain ordinary defects.

This grouping is deterministic and reversible from its constituents. Every occupied bit in a group's hole belongs to a defect polymer swallowed by that group. Thus local source functions of the released check values have no dependence on leftover defects. Cross-character phases remain between groups, rather than being overcounted as positive weights.

If a decorated group contains m distinct source labels and swallowed defect mass M, at most b_c m occupied defect bits have lost their thermal energy. Therefore its absolute weight is bounded by

  (C_dict q)^m exp[-B max(0,M-b_c m)],

where q=max_lambda(exp(beta||V_lambda||)-1). Its connected mixed trace shape has size O(m+M): source labels are connected through their actual support/check ports, and each swallowed defect has its own charged trace. Rooted counting consequently costs at most A^(m+M), provided the local dictionary and graph degrees are explicitly charged.

Crucial finite-capacity estimate, for B>log A:

 sum_{M>=0} A^M exp[-B max(0,M-b_c m)] <= C(A,B,b_c)^m.

For M<=b_c m this is a finite geometric sum through b_c m. For M>b_c m the remaining tail has ratio A exp(-B)<1. No exp(B b_c m) appears after performing the split in this order. If A=1 the polynomial prefactor can be absorbed in a fixed exponential in m. This is the prospective removal of the exponential beta J source-admission penalty.

## 3. Exact interactions after grouping

Original source exclusions and original defect exclusions become pairwise hard cores between constituent groups. A source group and an external defect are incompatible if that defect hits a hole (otherwise it should have been swallowed). The remaining factors are actual characters, of modulus one:

 - a group's stabilizer word against the external defect syndrome;
 - between two groups, word_1 against swallowed_defects_2 and word_2 against swallowed_defects_1.

Internal phases are retained in group activities. Thus every cross factor is 0 or +/-1; do not introduce normalized character ratios that can exceed one. The no-source subgas is exactly the original reference defect gas. A convergent KP expansion of the full gas would therefore give connected normalization by subtracting the no-source logarithm.

## 4. KP strategy requiring explicit verification

Assign charge a_s m+a_d M to a decorated group. Absorb these factors into the constants in the finite-capacity sum. Hard-core rows are bounded by charged mixed trace size and rooted densities.

For phase rows use the SAME actual nontrivial character relation with TWO DIFFERENT certificates:

 (i) Word B of support O(m) versus defect tau: represent canonical correction D(tau)=sum_i J_(0:i)c_i. Its phase is sum_i of symplectic pairings between adjoint-propagated B and c_i. The source probe has <=C m K_adj^i sites, while a nonzero correction at level i forces top defect mass >=c2^i. Rooted defect density is therefore exponentially small in 2^i, and the source row is <=C m sum_i K_adj^i exp(-a2^i).

 (ii) Fix a defect of mass M. Nontrivial phase implies that an occupied top defect lies in an actual stabilizer filling of B. The existing polynomial-radius anchored filling theorem bounds possible connected source placements per defect by poly(m). Summing poly(m)(Cq)^m gives O(q)M. No exponential of the physical filling volume is needed.

For decorated groups, reaching a high level through a swallowed defect forces M>=c2^i. Either m>=c2^i/(2b_c), paying many source labels, or M-b_c m>=c2^i/2, paying thermal mass. Splitting a fraction of the source activity off first should retain an overall small-in-q factor and a high-level tail exp(-a'2^i). This extends the two certificates to group/group phases. It must be proved with the correct row (reverse-dependency) bound for adjoints, not merely a column norm for lifts.

## 5. Consequence if the complete construction passes

A finite-temperature generic perturbation window governed by beta v times fixed local/geometric constants, rather than exp(C beta J) beta v, for the actual commuting reference and its valid-defect decoder. A marked-witness version must still show hybrid suppression: large witness occupancy paid either by thermal defects outside source holes or by sufficiently many source labels. Exceptional logical components are controlled at fixed beta using distance, not claimed uniformly as beta tends to infinity.

This would be a substantive source-admission improvement, but it does not by itself supply native two-body clock preparation, a noisy WRITE operation, or a usable engineering regime. Generic clock/bath perturbations of the native model do not satisfy the commuting positive-hole identity automatically.
