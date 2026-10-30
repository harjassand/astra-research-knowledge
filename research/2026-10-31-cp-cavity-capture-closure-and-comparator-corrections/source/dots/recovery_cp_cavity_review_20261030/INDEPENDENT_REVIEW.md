# Independent review: CP-cavity local-fault bridge and disjoint-gadget receiving
30 October 2026. The frozen sources and their exact hashes are in sources/ and SOURCE_SHA256.txt. This review was performed separately from the construction. It does not assess historical novelty.

## Verdict

**PASS for the stated finite, bounded, fixed-schedule, joint-CP-divisible circuit noise-interface theorem, and for the exact disjoint-gadget sieve under its separately supplied correctness premise.** No load-bearing counterexample was found. The inclusive signed fault bound is

 ||sum_(F contains S0) E_F||_diamond <= [2*3^(q-1)*g*eta*tau]^(|S0|/q),

when the bracket is at most one. There is no device-volume or total-runtime exponential in this bound. The complete generator must generate CPTP propagators on EVERY interval; a merely CPTP final channel or a non-CP-divisible reduced generator is insufficient. The finite-dimensional bounded assumptions are substantive.

This is not a complete new fault-tolerance threshold theorem. Actual good-gadget correctness, overlapping extended-rectangle bookkeeping where used, input preparation, physical gates, detectors, and decoder/encoding resources remain separate. Nor is this a native autonomous controller construction. The primary Hamiltonian common-bath threshold results cited by the author remain established prior machinery.

## 1. The cavity really is a legitimate generator

For an active selected block R, let E_R insert its normalized maximally mixed state and let R_R denote partial trace. Both maps are CPTP. Therefore A->R_R A E_R is contractive in complete trace norm. Tensoring the identity on the selected block preserves the diamond norm, so the generator projection P_R has norm at most one. On disjoint active blocks, normalized embeddings and partial traces commute; consequently the P_j commute and P_R=product P_j. Idempotence follows directly.

If L is the actual joint generator, the reduced map R_R exp(hL) E_R is CPTP, is the identity at h=0, and has derivative R_R L E_R. In finite dimensions, the product limit of these short-step maps proves that this derivative is a CPTP generator. This does not require a subsystem of the original noise decomposition to generate a positive evolution.

The key identity is

 L^R=P_R L+sum_(j in R)L_id,j.

Trace preservation makes P_R L_id,j=0 for each selected j, including NONUNITAL intended generators. Intended generators on the complement are unchanged. The first term in this identity is the identity on the selected systems tensored with a legitimate complementary generator. Adding their independent intended generators is therefore legitimate. The author does not delete an arbitrary non-CP perturbation and assert that the remainder stays CP.

Piecewise-continuous time dependence and changes of the active partition are handled by chronological product limits. A selected location variable is active only on that location's interval. Repeated use of a qubit at a later location does not require projections at different times to commute; only the simultaneous disjoint-block projections are multiplied.

## 2. Exact Möbius identities and the supported fault class

The Möbius definition gives sum_F E_F=T^empty. For a fixed S0, summing over F containing S0 cancels every cavity vertex except those R subset S0, with the stated alternating sign. This identity is independent of positivity of E_F.

On a fixed layer, selected ideal blocks are isolated from all complementary system/bath disturbance. Their intended evolution factors from the arbitrary complementary evolution. A finite system operator expansion of the latter expresses it as a linear combination of maps on the allowed faulty blocks, with arbitrary bath-map coefficients. The bath coefficients may be attached to one of the allowed faulty locations; if there is none, they remain bath-only evolution. No norm bound is taken after this expansion, so no bath dimension factor enters the inclusive estimate.

This proves linear-span fault support, not a positive trajectory interpretation. It also explains why a cavity-dependent bath channel is harmless: bath-only histories are unrestricted in the shared-bath fault class. In particular E_empty is the ideal SYSTEM circuit tensored with some bath channel; it need not have the bath channel of a chosen noiseless physical reference. The desired system/reference action is preserved even on initially correlated inputs.

For asynchronous but fixed schedules, refine the description into intervals with a fixed partition. Arbitrary fault interactions within a declared faulty gate duration remain allowed. A theorem requiring strictly layered boxes must count any needed refinement overhead; the source explicitly preserves that caveat. Arbitrary overlapping autonomous interactions are not covered.

## 3. CP interpolation removes the global Dyson norm cost

At every time, the multilinear generator interpolation is a convex combination of the legitimate cavity generators. Thus all propagators between derivative insertions have diamond norm one. This is the step which removes the global exp(total noise norm times runtime) penalty.

For a generator derivative indexed by A, all locations in A must be simultaneously active. Each differentiated factor P_j-I kills every bath-only or system term not touching j. At most q simultaneously disjoint locations can be touched by a q-system-site term. The remaining interpolation factors are contractions. Thus the displayed derivative bound 2^|A| sum_(e touches every A)eta_e is valid and zero for |A|>q.

Repeated differentiation of the propagator uses ordered SET PARTITIONS: each derivative label occurs exactly once, either sharing a generator insertion with other labels or at a separate insertion. For one unordered partition, summing the chronological orders partitions the cube of independent insertion times. Applying the triangle inequality and integrating the scalar norm bounds gives the product of the w_A. There is no additional factorial. Coincident times have measure zero for the stipulated bounded coefficients. Parameter-independent instantaneous CPTP boundary maps are contractions and do not change this derivative argument; they are declared ideal resources, not qualified noisy detectors.

## 4. The rooted recursion gives the stated exponent and constant

Fix a location j. A noise term active in its interval can meet at most q selected locations. Summing all derivative blocks containing j gives

 sum_(A contains j) w_A x^(-|A|)
 <= integral_(j active)sum_(e touches j)eta_e * (2/x)(1+2/x)^(q-1).

The per-site incident bound and at most g sites in the location give an integral at most g eta tau. For 0<x<=1, 1+2/x<=3/x, so the sum is at most 2*3^(q-1)g eta tau x^(-q). Choosing the claimed x makes it at most one. Induction in the exact rooted set-partition recursion then gives Z(S0)<=x^|S0| for every finite set S0. Unequal intervals can use their actual integrated incidences. Zero noise is obtained by the continuous limit, without dividing by zero in the induction.

The root-power loss for q-body terms is genuine in this bound and is not advertised as an independent-fault rate. Shared bath dimension, the number of unselected locations, and the full circuit duration do not enter the local constant.

## 5. The gadget sieve is exact but its physical premise is not supplied

The integer identity for 1_(k>=t) is correct. The coefficient comparison is exact:

 binom(L,s)binom(s-1,t-1)=(t/s)binom(L,t)binom(L-t,s-t).

It yields the claimed bound binom(L,t)x^t(1+x)^(L-t) on the actual signed bad-gadget SUM, not a sum of exact-path norms. For disjoint gadgets, multiplying the identities produces disjoint inclusive sets, so the norm sum factorizes into the same bound per selected gadget.

This is a valid receiving rule conditional on actual good-fault-class correctness and incoming/outgoing correctable-module semantics. It does not prove that an arbitrary circuit gadget corrects t-1 faults. Overlapping extended rectangles cannot be treated as disjoint here. A separate established construction or proof must handle that overlap and the exact superoperator norm convention before claiming universal fault tolerance.

## 6. Independent executable checks

The original four-location/two-time regression was rerun from frozen sources. It checks inclusive Möbius identities and repeated uses of physical qubits, with non-GKSL individual summands and CPTP cavities. Its unnormalized Choi nuclear norm is a dimension-conservative upper bound on the diamond norm; no equality with the diamond norm is claimed.

New check_nonunital_cavities.py tests NONUNITAL intended amplitude-damping generators with a TOTAL perturbation -mu D_lowering+mu D_XX that is itself non-GKSL. The full intended-plus-perturbation generator remains valid. Across three rates, the perturbation-only channel has a strictly negative Choi eigenvalue, while all cavities and sampled convex interpolants are CPTP within numerical tolerance. The exact cavity identity has residual below1.2e-16 and projection idempotence residual zero. This tests a stronger positivity seam than merely splitting a valid noise generator into non-CP summands.

New check_partition_and_sieve.py checks 100 random q=3 layered incidence instances, all511 nonempty subsets of nine locations per instance: 51,100 partition bounds, maximum observed ratio0.18012. It also checks3,080 exact integer sieve identities and the coefficient identity through L=20. These finite checks corroborate the algebra; the all-size proof is the argument above.

## Scope retained

Accepted: a constructive exact signed fault expansion, ordinary fault-location linear-span support, and a volume-free inclusive complete-superoperator noise bound under the declared schedule and generator assumptions; plus its elementary disjoint-gadget combinatorics.

Not accepted by this receipt: infinite/unbounded bath extensions, merely final-time CP dynamics, adaptive schedules, an actual fault-tolerant gadget family or complete threshold theorem, raw-input acquisition, idealized external classical resources, autonomous operation, practical advantage, or historical novelty. No external state was changed.
