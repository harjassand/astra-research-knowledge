# A uniform exact EB length for arbitrary PPT words

9 October 2026. New complete proof candidate. This closes the previously isolated normalized weak-tail mechanism by retaining the constituent factors and a dual state path. It was developed after the preserved focused reviews and is not covered by those reports. No external certification, priority claim, explicit practical exponent, or PPT-square bound is asserted.

## Theorem

For every d>=1 there is a finite integer N(d) such that every serial product of N(d) arbitrary PPT completely positive maps on M_d is entanglement breaking.

The factors may vary arbitrarily. Trace preservation, unitality, a common state, stationarity, commutativity and a finite alphabet are not required. The theorem concerns serial composition, not tensor powers.

The proof is by dimension induction. Its essential new step is Section 4: a first block tending to EB remains EB in every output-normalized limit after sufficiently many further PPT factors, either through a faithful limiting state or through a moving chain of kernels. This supplies a semialgebraic estimate uniform over the initial state. Normalized weak-block estimates can then be multiplied along the actual state trajectory.

## 1. Three positive-composition tools

### 1.1 Moving proper supports

Suppose PPT CP maps Phi_i on M_d transport proper nonzero projections P_(i-1) to P_i, meaning supp Phi_i(P_(i-1))<=P_i. Put Q_i=I-P_i. The rectangular PPT split gives

 Phi_i=F_i+G_i,

with F_i CP and output-supported on P_i, and G_i CP and input-supported on Q_(i-1). The two diagonal corner maps are PPT. Neither entire summand is asserted to be PPT.

The proof is recorded in MOVING_SUPPORT_AND_NORMALIZATION.md, Sections 1–2: triangular Kraus matrices [[A,B],[0,C]] and the zero block of the positive partial-transposed Choi matrix force sum A X C*=0; a unitary change of Kraus coordinates separates the A and C coefficient spaces. Then G_(i+1)F_i=0. The full word is a sum of positive one-switch terms

 sum_(j=0)^n F_n ... F_(j+1) G_j ... G_1.

A run of k F factors contains k−1 PPT P-corner maps, and a run of k G factors contains k−1 PPT Q-corner maps, with CP endpoints.

Assume every word of R arbitrary PPT CP maps on M_(d−1) is EB. Rectangular maps on dimensions at most d−1 are padded with zeros and embedded by isometries into M_(d−1), so the same R applies to their chains. Every moving-proper-support word of length

 B=2R+1                                                   (1)

is therefore EB. No rank monotonicity is used.

### 1.2 Compact strict-positive anchors, with arbitrary CP gaps

For each epsilon>0, there is a finite H(d,epsilon) such that H disjoint CPTP subwords, each strictly output-positive with margin at least epsilon, force the containing word to be EB, even with arbitrary CP maps between those subwords.

The complete proof is STRICTLY_POSITIVE_FILTERED_WORD_THEOREM.md. Its published input is Davidson–Marcoux–Radjavi, arXiv:0706.2449v1, Theorem 4.9, https://arxiv.org/html/0706.2449 . Product spans of rectangular transitive matrix spaces increase their transitivity degree; d strictly output-positive CP factors separated by nonzero CP filters consequently have full Choi rank. Normalize each intervening filter by its Choi trace. Compactness then gives a common positive Choi lower margin for each d-anchor chunk. A positive expansion into a depolarizing component plus a shrinking CP remainder, together with an elementary separable ball, makes sufficiently many chunks EB. A zero filter already makes the word zero.

This input does not assume PPT or an invariant state. Its constants depend on the compact strict-positive family.

### 1.3 Kraus defect, multiplication and rank-one truncation

For a chosen Kraus family K define

 b(K)=sum_a ||wedge^2 K_a||_op.

For compositions, product Kraus families satisfy b(KL)<=b(K)b(L). Replacing each Kraus matrix by its leading rank-one singular term gives an EB map E with

 ||J(T−E)||_F<=kappa_d b(K),   kappa_d=sqrt(d^2−1).       (2)

These bounds are explicitly proved in filter_closed_uniformity/FULL_SEMIALGEBRAIC_MAPPING_CONE_UNIFORMIZATION.md, Sections 1–2. For a CP unital map, every Kraus family also has b(K)<=d/2, since each top singular-value product is at most half the squared Frobenius norm and sum ||K_a||_F^2=tr T(I)=d.

On any compact bounded-Choi-trace family of CP maps, distance g of the Choi matrix from the separable cone controls the existence of a Kraus family with b(K)<=C sqrt(g). To recall the interface, choose a closest bounded separable matrix J_0, a finite rank-one Kraus factor W_0=sqrt(J_0)U with U a coisometry, and lift it to W=sqrt(J)U. The square-root estimate ||sqrt(J)−sqrt(J_0)||_F^2<=||J−J_0||_1 and exterior-square perturbation then give the bound. Padding the finite separable decomposition is harmless. This does not require TP or a global continuous Kraus choice.

## 2. A compact tagged boundary for CPTP words

Assume the lower-dimensional R in Section 1. Put

 B=2R+1,             Q=(R+1)B.                          (3)

For a Q-tuple of PPT CPTP factors define

 f_tag=max_(1<=j<=Q−B+1) f(Phi_(j+B−1)...Phi_j),
 f(S)=min_(rho>=0,tr rho=1) lambda_min S(rho).

The tag belongs to the tuple, not just to its product. It is continuous and semialgebraic on the compact tuple space, and

 f_tag=0 ==> the Q-word is EB.                           (4)

Here is the full counting reason. If R+1 factors have singular global output Phi_i(I), compress between their proper output supports. There are R intervening rectangular PPT transitions, so the word is EB by the lower-dimensional hypothesis. Otherwise at most R factors have singular global output. A Q-word then contains a B-long run in which every factor has full global output. If this run is not strictly output-positive, follow a pure input with singular final output. TP keeps each support nonzero, and full-global-output factors cannot map a full-support state to a singular state. Thus all supports along this run are proper. Section 1.1 makes the run EB. This proves (4).

The proof does not assume an all-PPT rank-(d−1) Kraus decomposition.

## 3. Unital normalization along a forward state trajectory

For the moment take CPTP maps U_1,...,U_k and an initial S_0>0 with tr S_0=d, such that every

 S_i=U_i(S_(i−1))

is positive definite. Define

 B_i=Ad_(S_i^(-1/2)) U_i Ad_(S_(i−1)^(1/2)).             (5)

Then B_i is CP and unital, and PPT if U_i is PPT. Trace preservation gives the exact dual relation

 B_i*(S_i)=S_(i−1).                                     (6)

The factors telescope:

 B_i...B_1=Ad_(S_i^(-1/2)) U_i...U_1 Ad_(S_0^(1/2)).     (7)

All S_i lie in the compact trace-d state slice, and all B_i lie in the compact unital CP slice. Thus both have convergent subsequences when the original data degenerate. The limiting B_i remain PPT.

## 4. The normalized boundary lemma

Consider a sequence of such trajectories in which U_1 tends to an EB CP map, followed by at least B=2R+1 further PPT CPTP factors U_2,...,U_(B+1). The initial S_0 may vary and may have a singular limit. Every limit of the normalized product B_(B+1)...B_1 is EB.

Pass to a subsequence where all maps and states converge, writing lower-case s_i for the state limits. Every s_i has trace d.

If some s_i with i>=1 is positive definite, take the limit of (7) for that prefix. Its middle product begins with the limiting EB U_1, and its endpoint filters have finite limits because s_i is faithful and sqrt(S_0) is continuous even at a singular limit. Thus the normalized prefix is EB. The remaining limiting B factors are CP, so the full product is EB.

Otherwise every s_i, i>=1, is singular. Let P_i be the projection onto ker s_i. Since tr s_i=d, each P_i is proper and nonzero. For i>=2, relation (6) and positivity give

 tr[s_i B_i(P_(i−1))]=tr[s_(i−1)P_(i−1)]=0.

Hence supp B_i(P_(i−1))<=P_i. The normalized tail B_(B+1)...B_2 has B factors transporting proper nonzero supports. Section 1.1 makes that tail EB. Composing it with B_1 again proves the full product EB.

This proves the lemma with arbitrary varying initial trace-d states. It uses the factors and their dual state path; an output-only approximation or local filtering argument would not supply it.

## 5. A uniform normalized Kraus estimate for pairs of tagged blocks

Take two consecutive tagged Q-blocks, an arbitrary S_0>0 of trace d, and assume the forward states remain positive definite. Treat the first whole Q-product as U_1 and the Q constituent factors of the second block as the later U_i. Normalize as in Section 3. Let Z be the normalized product over both blocks, and let s be the first block's tag.

Use the following explicit compact semialgebraic relation, which contains the full-rank normalization graph and its closure. Its coordinates are the 2Q original PPT CPTP factors; U_1, their first Q-product; U_2,...,U_(Q+1), their remaining constituent factors; positive matrices X_0,...,X_(Q+1) with tr(X_i^2)=d; PPT unital CP maps B_1,...,B_(Q+1); the first block's tag s; and Z=B_(Q+1)...B_1. Put S_i=X_i^2 and impose

 S_i=U_i(S_(i−1)),
 Ad_(X_i) B_i=U_i Ad_(X_(i−1)),
 B_i*(S_i)=S_(i−1),           B_i(I)=I.                 (7a)

Every coordinate lies in a fixed compact set: raw factors are CPTP, B_i are unital CP, and ||X_i||_F=sqrt(d). Positivity/PPT and the displayed relations are closed finite real-algebraic conditions; the tag is continuous semialgebraic. Thus the relation is compact semialgebraic. No inverse occurs in its boundary definition. One could restrict to the closure of the genuine full-rank graph, but the larger relation is sufficient because the following argument applies at every one of its points.

At a point with s=0, the first Q-product U_1 is EB by Section 2. If some S_i, i>=1, is faithful, telescoping the inverse-free intertwining equations (7a) gives

 B_i...B_1=Ad_(X_i^(-1)) U_i...U_1 Ad_(X_0),            (7b)

an EB prefix with bounded filters at that point. If all these S_i are singular, the dual equations in (7a) give the proper kernel chain for B_2,...,B_(Q+1). There are Q>=2R+1 such factors, so Section 1.1 makes this tail EB. Hence Z is EB in either case. Let

 g=dist_F(J(Z),Sep).

Both s and g are continuous semialgebraic functions on this compact relation, and {s=0} is contained in {g=0}. The compact semialgebraic Lojasiewicz inequality gives g<=A_0 s^beta for some A_0,beta>0. Applying the bounded-trace Kraus lift in Section 1.3 yields constants A,alpha>0 such that Z has a Kraus family with

 b(Z)<=A s^alpha.                                      (8)

The bound is UNIFORM over the initial S_0, including arbitrarily ill-conditioned initial states through the compact relation. It is not obtained by bounding an inverse output eigenvalue. This is the missing relative estimate.

The semialgebraic inequality used here is the continuous compact version already specified in filter_closed_uniformity/SOURCE_DEPENDENCY_LOCATIONS.md. The theorem makes no claim of a practical numerical value of alpha.

## 6. Multiplying weak normalized groups

Consider 2m consecutive Q-blocks, each with tag at most s. Divide them into m consecutive pairs. Start from any S_0>0 with trace d, follow the actual forward states, and normalize each pair at its input and output states. Equation (8) supplies a Kraus family for each normalized pair with defect at most A s^alpha. Multiplication gives the normalized total product a Kraus family with

 b<= (A s^alpha)^m.                                    (9)

Two versions of (9) will be used.

### Forward version

Let U be the original 2m-block CPTP product and choose S_0=I. Write S_out=U(I). Then

 U=Ad_(sqrt(S_out)) Z,

where Z is the normalized product. Since tr S_out=d, ||S_out||_op<=d and ||wedge^2 sqrt(S_out)||<=d. Therefore U has a Kraus family with

 b(U)<=d(A s^alpha)^m.                                 (10)

### Reverse version, including an interior suffix

Let R_0 be any CPTP suffix between a selected anchor and the 2m-block product U, with S_0=R_0(I)>0. Define R'=Ad_(S_0^(-1/2))R_0, which is CP unital. Set S_out=U R_0(I). Then

 V=Ad_(S_out^(-1/2)) U R_0=Z R'

is CP unital. Since b(R')<=d/2, it has a Kraus family with

 b(V)<=(d/2)(A s^alpha)^m.                              (11)

The anchor Psi has not been input-normalized here: the exact identity is

 V Psi=Ad_(S_out^(-1/2))(U R_0 Psi).

Thus its original margin s is retained in the reverse anchor below. If one instead folds an output normalization into an anchor chi=Ad_(S_0^(-1/2))Psi with tr S_0=d, its output margin is at least s/||S_0||_op>=s/d; that alternative only changes a dimension constant. The chosen factorization avoids even that loss.

All inverse filters in this argument are finite at the current positive-definite data. Their possible degenerations have already been controlled by the inverse-free compact relation in Section 5.

## 7. A maximal weak tag gives an exact separable margin

For a CP map X, write D(X)=tr(X)I_d. The elementary separable ball around I_d tensor I_d has Frobenius radius 1/d^2; its proof is in Appendix A of the preserved uniform-power theorem.

Let Psi be CPTP with f(Psi)=s>0. The following two anchors are used.

### Forward anchor

If U is CPTP and E is an EB approximation with delta=||J(U−E)||_F, then delta<=1/(2sqrt(d)) gives E*(I)>=I/2. For any intervening CPTP prefix L_0,

 Psi L_0 E >=_EB (s/2)D.

This is positive measure-and-prepare order: Psi sends every density output of L_0 E to an operator at least sI, and the total input effect is E*(I).

Left composition by a CPTP map has Hilbert–Schmidt operator norm at most sqrt(d), so

 ||J(Psi L_0 U−Psi L_0 E)||_F<=sqrt(d)delta.

The separable ball proves Psi L_0 U is EB whenever

 delta<=s/(2d^2 sqrt(d)).                              (12)

This condition also implies the preceding effect lower bound because s<=1/d.

### Reverse anchor

If V is unital and E is EB with delta=||J(V−E)||_F, then delta<=1/(2sqrt(d)) gives E(I)>=I/2. The strict-output bound for Psi is equivalent to Psi*(F)>=s tr(F)I for every F>=0. In a Holevo representation of E this implies

 E Psi >=_EB [X -> s tr(X) E(I)] >=_EB (s/2)D.

Right composition by the CPTP map Psi also changes the Frobenius Choi norm by at most sqrt(d). Thus (12) makes V Psi EB. Undoing an output filter preserves EB, so the reverse version V in (11) gives EB of U R_0 Psi.

Choose m so that alpha m>1 and put C=kappa_d d. Choose epsilon>0, with epsilon<=1/d, small enough that

 C A^m epsilon^(alpha m−1)<=1/(2d^2 sqrt(d)).            (13)

Let W=4m+1. In any run of W tagged Q-blocks all having tag at most epsilon, select a block with maximal tag s. If s=0, that block is EB by Section 2. Otherwise one side contains at least 2m consecutive whole Q-blocks.

The selected tag is attained by a B-factor subword Psi inside its block. The remaining part of the selected block between Psi and the chosen side is a CPTP L_0 or R_0. Equations (2), (10) or (11) give an EB approximation with

 delta<=C(A s^alpha)^m<=s/(2d^2 sqrt(d)).

Use the corresponding anchor. The surrounding factors are CP, so the entire W-block run is EB.

## 8. Strong tags, counting and dimension induction

A strong Q-block has tag at least epsilon and therefore contains a strict-positive CPTP anchor of margin at least epsilon. H=H(d,epsilon) strong blocks force EB by Section 1.2.

If a word has fewer than H strong blocks and has no W-consecutive weak run, it has at most

 (H−1)+H(W−1)=HW−1

tagged blocks. Thus every word of HW tagged blocks is EB. One may take

 N(d)=Q H W.                                           (14)

At this stage the argument has been applied to strictly output-positive PPT CPTP constituent factors, so every forward state needed for normalization is positive definite. This class is dense in all PPT CPTP maps: replace each factor Phi by (1−t)Phi+tD_d, where D_d(X)=tr(X)I/d. The constants in (8), (13) and (14) were taken from the compact graph of the entire dimension-d class and the fixed lower-dimensional R, not from t. Hence the same N(d) works for all regularized words. Let t decrease to zero; closedness of EB proves the result for all PPT CPTP words.

Finally, the exact backwards-effect normalization in POSTSELECTION_ROBUST_EB_APPROXIMATION.md, Section 2, factors any arbitrary PPT CP word into a same-length PPT CPTP word after one CP input filter. Applying the CPTP result and undoing the input filter gives the result for arbitrary CP factors.

The induction starts at d=1, where every CP map is EB and N(1)=1. At dimension d use R=N(d−1). All corner invocations concern unrestricted CP words in a strictly smaller dimension. This completes the proof candidate.

## Scope, compatibility and preservation

- The uniform length may be very large. This proof does not give N(d)=2 or any practical explicit exact exponent.
- The explicit O(d^2 log(d/eta)) approximation and positive-noise repair remain useful quantitative results; this exact proof instead uses a non-numerical semialgebraic exponent and dimension induction.
- The known output-only counterexamples remain valid. Section 4 uses the actual factors, intermediate states and their dual identities, so no small-distance-to-exactness inference is being made.
- Neither the general PPT Schmidt-number conjecture nor an abstract compact nil-semigroup implication is used.
- The earlier reviewed cores, reports and delivered bistochastic theorem are unchanged. This later proof is an internally derived candidate, with no extra broad review roster or external certification.
