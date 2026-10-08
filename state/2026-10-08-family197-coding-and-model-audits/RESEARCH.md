# Family-197 Rokhlin-entropy investigation: nonlinear coding and finite-model obstructions

**Date:** 2026-10-08 (Brisbane); **status:** conditional mathematical deductions and failed routes, NOT a solution of the entropy question, NOT externally peer-reviewed, global novelty NOT established.

**Repository baseline:** harjassand/astra-research-knowledge at commit b5824d0fcbfe0688980788da2722270a2f068fb0. Initial routing: 00_START_HERE.txt, state/2026-10-08-bowen-bernoulli-direct-finiteness/{RESEARCH.md,ADDITIONAL_AUDITS.md}, frontier/review_cards/{N47-hyperbolic-group-ring,N129-hyperbolic-direct-finiteness}.txt, agent/RESEARCH_WORKFLOW.txt. Original OpenAI mathematical construction read at openai/math revision fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb, in build/sections/{introduction,algebra}.tex. External proofs checked: Seward, Krieger II, theorem 1.10 and remark 1.4 (https://mathweb.ucsd.edu/~bseward/Files/krieger2.pdf), and Weak containment and Rokhlin entropy, theorem 1.5 (https://mathweb.ucsd.edu/~bseward/Files/weakcontainrokentropy.pdf). The original OpenAI existence proof is an imported, unformalized premise, not independently replayed.

**Question frozen:** For the ORIGINAL group G from family 197, decide whether h_sup^Rok(G)=0 or >0, and investigate Bowen measurable Bernoulli-isomorphism question. Do not replace G with a product or an enlarged group.

**Prior state explicitly inherited, not newly derived:** For R=F_2[G] with ab=1, ac=0, c!=0, putting r=1-ba and X=F_2^G gives a splitting X = X x K (equivariant Haar group isomorphism), K=ker T_a=im T_r, and a strict upper bound h_sup^Rok(G) <= (1-1/|supp(r)|) log 2 < log 2. Finite-quotient periodic configurations are in im T_b, while K has no nonzero finite-orbit configurations. The group construction reports G torsion-free, finitely presented, finite-dimensional BG; source correctness not checked in this run. A later Formanek-based contradiction withdraws the separate proposed torsion-free hyperbolic upgrade, and does NOT invalidate the original (non-hyperbolic) hypothesis.

## Result 1: the defect kernel is free and strongly mixing, with dense homoclinic group

**Theorem 1 (direct conditional deduction; novelty beyond this repository not established).** Let G be any countably infinite torsion-free group, let F_q be any finite field, and suppose a,b in F_q[G] satisfy ab=1 but ba !=1. Put r=1-ba, let X=F_q^G with left shift and uniform product measure, and K=im T_r=ker T_a with Haar measure m_K. Then:

(a) K is nontrivial and its Haar action is a finite-radius linear factor of iid, hence finitely dependent (coordinates at finite sets whose r-memory patches are disjoint are independent). It is mixing of all finite orders.

(b) The subgroup K_fin=K intersect F_q^(G) of finitely supported configurations is nonzero and dense in K. In particular the homoclinic group is dense (homoclinic configurations in finite-alphabet full shifts are exactly finitely supported ones).

(c) The G-action on (K,m_K) is essentially free and ergodic.

(d) K has no nonzero periodic points: this last assertion was ALREADY established in ADDITIONAL_AUDITS.md and is repeated here only to contrast with (b).

**Proof.** The finite-radius map T_r:X -> X is a continuous equivariant group homomorphism with image K and T_r^2=T_r. Its pushforward of iid Haar is Haar on K. If S=supp(r), each z(g)=(T_r x)(g) depends only on x|_{gS}; output sets whose memory translates are disjoint are independent, establishing finite dependence. Since factors of an iid process are mixing of all finite orders, so is this action. More directly, cylinder events in K lift to cylinder events in X under the finite-radius map, so distant translates become literally independent. Haar ergodicity follows.

Since r !=0, T_r(delta_e) is a nonzero finitely supported configuration (the underlying formula is a translate/inversion of r). Therefore K_fin !=0. The finitely supported configurations are dense in X in the product topology. By continuity and surjectivity of T_r onto K, T_r(F_q^(G)) is dense in K; all its elements are finitely supported, proving (b).

For any g !=e, torsion-freeness gives infinitely many distinct powers g^n. Select n_1,n_2,... so that g^(n_j) S are pairwise disjoint. Because the coefficient vector r on S is nonzero, the random variables z(g^(n_j)) are independent and uniform on F_q. If z is fixed by g, all these variables must be equal. The probability that the first N independent uniform variables are equal is q^(1-N), tending to zero. Thus m_K(Fix(g))=0. A countable union over nonidentity elements proves essential freeness.

For (d), take a finite-index normal N and regard N-fixed configurations as F_q^(G/N), a finite-dimensional vector space. T_a T_b=I there, so T_b T_a=I there. Thus T_r=0 on that space. If a configuration has finite G-orbit, its stabilizer contains a finite-index normal subgroup (the core), so its membership in K forces it to be zero. QED.

**Impact/limit:** This supplies a concrete free, ergodic, mixing-of-all-orders, finitely-dependent algebraic action with dense homoclinic group and no nonzero periodic points. It is NOT a proof of positive Rokhlin entropy: nontrivial finite dependence, freely acting, or being a factor of iid is not a lower bound for Rokhlin entropy of nonsofic groups. Nor does a dense homoclinic group imply K is measurably Bernoulli. Prior art may already contain these general factor-of-iid consequences.

## Result 2: a precise nonlinear low-entropy coding failure

**Theorem 2 (first-order sensitivity obstruction).** Let G be any infinite group and choose nonzero elements u_1,...,u_k of F_2[G] (k>=2) with pairwise disjoint finite supports. For x in F_2^G set L_i(x)(g)=(T_{u_i}x)(g). Let phi:F_2^k -> {0,1} be a Boolean function satisfying

    phi(0,...,0)=phi(e_i) for every i=1,...,k,

where e_i are standard basis vectors. Define the equivariant finite-block code

    F_phi(x)(g)=phi(L_1(x)(g),...,L_k(x)(g)).

Then F_phi is NOT essentially injective for uniform Bernoulli measure. In fact there is a positive-measure cylinder on which flipping a single fixed input bit leaves the entire output configuration unchanged.

**Proof.** Fix h in G and let delta_h be the configuration supported at h. At a given g, L_i(delta_h)(g) is nonzero exactly when g^(-1)h lies in supp(u_i). Because those supports are pairwise disjoint, the vector of k outputs for delta_h at g is either zero or one of the e_i. The condition on phi therefore gives F_phi(delta_h)=F_phi(0), as configurations.

The set of output coordinates which can be affected by flipping x(h) is finite: it is the union of h supp(u_i)^(-1). Take the finite union D of all input sites used by the local rules centered at these potentially affected output coordinates, together with h. On the cylinder {x|_D=0}, the two configurations x and x+delta_h have the same output on every potentially affected coordinate by the computation at zero; they agree elsewhere because the local rules do not depend on x(h). This cylinder has strictly positive iid Haar measure 2^(-|D|). The flip x -> x+delta_h preserves Haar measure. If there were a full-measure subset on which F_phi were one-to-one, its intersection with its flip and this cylinder would have positive measure, a contradiction. QED.

**Concrete consequence.** Take phi(v)=v_1 v_2 ... v_k (Boolean AND). The L_i(x)(e) are independent fair bits because their support windows are disjoint and each u_i !=0; hence F_phi(x)(e) is Bernoulli(2^(-k)) and its one-site Shannon entropy H_b(2^(-k)) tends to zero. Nevertheless this observable is not generating even modulo null sets, regardless of the pathological family-197 relation. Similarly, any Boolean rule whose value is unchanged by all single-coordinate flips at zero is excluded. This defeats a natural but invalid attempt to make a rare generator by conjunction of many independent linear defect/kernel coordinates. It does NOT exclude nonlinear maps with nonzero first-order sensitivity, overlapping memory windows, nonlocal coding, or random marker constructions.

**Novelty qualification:** This is a self-contained failure theorem for one explicitly defined coding class, not a global no-go for nonlinear measurable coding. It must not be advertised as a solution, and its elementary mechanism may be known.

## Result 3: explicit uniform finite-permutation-model gap

**Theorem 3 (conditional quantitative microstate obstruction; standard rank-argument ancestry).** Let a,b,c be finite sums over F_2[G] with ab=1, ac=0 and c!=0. Let k=|supp(a)|, ell=|supp(b)|, m=|supp(c)|, so k,ell,m>=1. Let sigma map the finite set of group elements needed below to permutations of a nonempty n-point set. Assume

(i) d_H(sigma(st),sigma(s)sigma(t))<=delta for each s in supp(a), t in supp(b) union supp(c);

(ii) d_H(sigma(e),id)<=delta;

(iii) for one chosen u_0 in supp(c), d_H(sigma(u_0),sigma(v))>=1-delta for each other v in supp(c).

Then necessarily

    delta >= 1 / [ m*(k*(ell+m)+1) + (m-1) ].

For the OpenAI parity witness, b=a^*, so ell=k. This is a fully explicit positive forbidden-accuracy gap in finite permutation microstates, once the concrete support sizes are acquired. It does NOT depend on n.

**Proof.** Over F_2 let A,B,C be the n-by-n sums of the permutation matrices of sigma(s), with s ranging respectively over the supports of a,b,c. If two permutations disagree on at most delta*n inputs, the difference of their permutation matrices has rank at most delta*n: restrict to the columns indexed by those inputs (choose a consistent matrix convention). By rank subadditivity and (i,ii),

    rank(AB-I) <= (k*ell+1)*delta*n,
    rank(AC)   <= k*m*delta*n.

Indeed, after replacing each matrix product P_sigma(s)P_sigma(t) by P_sigma(st), its F_2 sum is P_sigma(e) or 0 by ab=1 or ac=0 respectively, with cancellation of repeated group terms. Thus nullity(A) <= (k*ell+1)*delta*n and

    rank(C) <= rank(AC)+nullity(A)
            <= (k*ell+k*m+1)*delta*n.                    (UPPER)

For all but at most (m-1)*delta*n row indices i, the position (i,sigma(u_0)(i)) receives a single 1 from u_0 and none of the other m-1 permutation matrices. Consequently C has at least [1-(m-1)*delta]*n distinct nonzero columns, provided the bracket is positive. Every row of C has at most m nonzeros. Choose rank(C) independent rows spanning its row space. Every nonzero column of C must be nonzero in at least one of these basis rows; therefore the number of nonzero columns is at most m*rank(C). It follows that

    rank(C) >= [1-(m-1)*delta]*n/m.                       (LOWER)

If the bracket is nonpositive, the claimed bound on delta is already automatic. Otherwise combine UPPER and LOWER and rearrange to obtain the asserted inequality. QED.

**Meaning and limits:** This is a quantitative obstruction to the usual finite permutation / sofic microstate route, different from an entropy upper bound. It is a standard-looking refinement of the established Elek-Szabo proof that sofic group algebras are stably finite, and **no publication-level novelty is claimed**. It does not imply that positive Rokhlin entropy actions cannot exist: neither positive Rokhlin entropy nor a free ergodic action automatically supplies finite permutation microstates of G. The source graph a,b,c are not instantiated here, so no numerical delta is asserted.

## Adversarial route audit

* POSITIVE-entropy route: Construct K as a genuinely free and finitely-dependent system (Theorem 1). **Fail:** No known universally applicable positive lower bound for h_G^Rok(K) derives from mixing, dense homoclinic points, finite dependence, freeness, or factor-of-iid status. The general nonamenable theorem that zero-Rokhlin-entropy actions can factor onto every Bernoulli shift (Bowen, Zero Entropy Is Generic, 2016) specifically blocks naive factor-monotonicity inference. No action with certified h_G^Rok>0 was produced. Crucially even K positive would suffice to establish POS(G), but not automatically s(G)>0, since the action's entropy might be +infinity; here K has an explicit finite-entropy coordinate generator, so a proof h_G^Rok(K)>0 would indeed imply s(G)>0.
* ZERO-entropy route: Use many kernel coordinates to make output the rare conjunction of k independent bits, with entropy H_b(2^(-k))->0. **Fail proved:** the corresponding finite-block observable is not generating (Theorem 2). This excludes precisely this sparse polynomial/threshold family, not all nonlinear measurable or nonlocal marker codings.
* FINITE-MODEL lower bound route: Construct positive entropy from finite permutation models / a sofic entropy invariant. **Fail quantitatively:** no approximations below the explicit tolerance in Theorem 3 can respect the witness. This is not a proof that all entropy-lower-bound mechanisms fail, and is not new evidence that positive entropy is impossible.
* AMENABLE-SUBGROUP route: The original group's torsion-freeness supplies infinite cyclic subgroups (and earlier Formanek-based work suggests BS(1,2^k)). Positive entropy on a subgroup cannot simply be promoted through infinite-index restriction or coinduction without a theorem applicable to this nonsofic G. A Bernoulli G-shift restricted to an infinite-index cyclic subgroup has infinitely many independent tracks, not a finite Rokhlin lower bound for G.
* HAAR-SPLITTING route: X is measurably conjugate to X x K and hence to X x K^n for every finite n. This does not permit subtracting Rokhlin entropies, establishing tensor-product superadditivity, or deducing h(K)=0. Those missing properties are not available for arbitrary nonsofic groups.
* ISOMORPHISM route: No conjugacy between Bernoulli bases of unequal Shannon entropies was constructed. Equality of Rokhlin entropies, zero-entropy extensions, mutual factor maps, and topological algebraic splitting remain strictly weaker.

## Exact main obstruction and status

The quantity s=h_sup^Rok(G_197) remains UNDETERMINED between zero and strictly positive. Seward's theorem 1.10 converts a finite positive s into a spectrum of nonisomorphic Bernoulli shifts, but no positive lower bound for G_197 was established. The original family's claimed failure of direct finiteness does not by itself imply that all Bernoulli shifts are measurably isomorphic. Likewise, proving s=0 would not establish total Bernoulli-isomorphism collapse, and would not alone exclude positive infinite-Rokhlin-entropy free ergodic actions (the POS vs INF distinction in Seward).

**Precise next mathematical gates:** (1) Produce an actual generating low-entropy Borel observable on the Haar binary Bernoulli G-space, with a measurable inverse to the full orbit-name map, beyond the finite-block first-order-insensitive class; OR (2) certify h_Rok(K)>0 for the explicit finitely-dependent free factor K, via a group-specific positive lower-bound mechanism not dependent on sofic microstates; OR (3) prove a different group-specific positive action and entropy lower bound. A proof of (2) would resolve s>0 because K has the finite-entropy one-coordinate generator, and thereby refute Bowen's complete collapse for this G. Current study supplies none of these gates.

**Verification scope and priority:** The three displayed theorems above were checked algebraically within one reasoning process; no independent subagents or specialist referee were available; no exact finite group presentation or numerical group197 a,b,c support was acquired; no programmatic group197 entropy computation was performed. Original lemma-level global novelty remains UNKNOWN. This is a preserved failed-route and structural-deduction note, NOT a claimed field-breaking breakthrough.

## Source links

* OpenAI math, preprint 2026-10-04: https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026
* Seward, Krieger II (Theorems 1.10/1.12, POS/INF), https://mathweb.ucsd.edu/~bseward/Files/krieger2.pdf
* Seward, Weak Containment and Rokhlin Entropy (Theorem 1.5), https://mathweb.ucsd.edu/~bseward/Files/weakcontainrokentropy.pdf
* Bowen, Zero Entropy Is Generic, https://www.mdpi.com/1099-4300/18/6/220
* Austin, ICM 2026 ergodic theory survey, Question 3.1, https://epubs.siam.org/doi/10.1137/25M1805564
* Elek and Szabo, Sofic groups and direct finiteness, J. Algebra 280 (2004), DOI 10.1016/j.jalgebra.2004.06.023.
