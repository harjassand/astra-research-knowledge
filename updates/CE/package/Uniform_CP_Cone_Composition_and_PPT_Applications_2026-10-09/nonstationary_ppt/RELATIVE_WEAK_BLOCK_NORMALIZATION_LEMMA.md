# A factor-sensitive output-normalization lemma for weak PPT words

9 October 2026. New conditional derivation. This note assumes the exact arbitrary-word EB bound in dimension d−1 and proves the proposed multi-block limit lemma. It does not establish the unrestricted dimension-d exact theorem. No priority claim is made.

## Result at the tagged gate

Assume every product of R arbitrary PPT CP maps on M_(d−1) is entanglement breaking (EB). As usual, padding transfers this premise to chains whose intermediate and endpoint dimensions are at most d−1.

Set

    B = 2R+1,       Q = (R+1)B.

Use exactly the max-over-B-subwords tag f_tag on actual Q-tuples from EXACT_UNRESTRICTED_GATE_REDUCTIONS.md. For two Q-tuples of PPT CPTP maps, let E(t) be the product of the first tuple and V(t) the product of the second tuple. If the first tuple's tag tends to zero, then every limit of

    Ad_[(V(t)E(t)(I))^(dagger/2)] V(t)E(t)

is EB. Here X^(dagger/2) is the inverse square root on supp X, extended by zero on ker X. The output is regarded as a map on its actual support, or equivalently as a CP map into M_d with zero outside that support.

Consequently the requested number of tagged blocks may be taken to be

    m = 2.

Only the first block needs to have tag tending to zero. The conclusion is uniform when the whole word is preceded by Ad_[H(t)^(1/2)], for arbitrary H(t)>=0 of trace d, and the resulting output is normalized. In fact only R+1 constituent PPT CPTP factors of the second block are needed. The remaining factors are harmless, provided they are included in the intermediate normalization argument below. More generally, the proof applies directly to any tail of length at least R+1.

The statement does not treat a Q-factor tagged block as an arbitrary near-EB PPT map without justification. The actual first Q-tuple is retained and its compact boundary theorem is applied. Nor does this note claim a tagged one-block counterexample: filtering a single strict PPT seed toward a replacer need not furnish a Q-factor tuple with all tagged B-subwords weak.

## 1. Stronger general theorem

Let E_n be CPTP maps on M_d, and let

    Phi_(1,n), ..., Phi_(L,n)

be PPT CPTP maps on M_d, where L >= R+1. E_n itself need not be PPT. Suppose E_n converges to an EB map E. Let H_n be any positive semidefinite matrices of trace d; no uniform positive lower eigenvalue bound and no invertibility are assumed.

Define

    U_(0,n) = E_n Ad_[H_n^(1/2)],
    U_(i,n) = Phi_(i,n) ... Phi_(1,n) E_n Ad_[H_n^(1/2)],
    S_(i,n) = U_(i,n)(I),
    N_n = Ad_[S_(L,n)^(dagger/2)] U_(L,n).

Then every accumulation point of N_n is EB.

Equivalently, a near-EB initial channel followed by R+1 actual PPT trace-preserving factors has an output-normalized limit in the EB cone, even when its unnormalized output concentrates onto a proper subspace and even when that subspace moves with n.

The trace-preserving hypothesis on the tail is essential to the proof: it supplies the positive-state transport identities used below. Arbitrary intervening filters are not silently allowed here.

## 2. Exact unital completion at finite n

This step handles singular finite-parameter outputs, rather than assuming invertibility and then appealing informally to regularization.

Suppress n temporarily. Put S_(-1)=H_n, Phi_0=E_n, and let P_i=supp S_i and Q_i=I−P_i. Define

    A_i = Ad_[S_i^(dagger/2)] Phi_i Ad_[S_(i−1)^(1/2)],
    D_i(X) = tr(X) Q_i/d,
    B_i = A_i + D_i,

for i=0,...,L. At i=0 the right input filter is Ad_[H_n^(1/2)].

These maps have the following exact properties.

### 2.1 Unitality and boundedness

Since Phi_i(S_(i−1))=S_i,

    A_i(I)=P_i,     D_i(I)=Q_i,     B_i(I)=I.

Thus B_i is CP and unital. For i>=1 it is also PPT: CP input/output filters preserve PPT, and D_i is EB. The set of unital CP maps on fixed M_d is compact, so all B_i are uniformly bounded even when S_i has arbitrarily small nonzero eigenvalues.

The initial B_0 is only required to be CP and unital.

### 2.2 Positive-state transport

Every S_i has trace d because tr H_n=d and all original channel factors are TP. Moreover

    B_i^*(S_i) = S_(i−1).                              (1)

For a direct verification, S_i supports the output of Phi_i on the support of S_(i−1). Indeed, writing Phi_i with Kraus matrices K_a,

    Q_i Phi_i(S_(i−1)) Q_i = 0

implies Q_i K_a P_(i−1)=0 for every a. Consequently

    P_(i−1) Phi_i^*(P_i) P_(i−1) = P_(i−1),

using Phi_i^*(I)=I. Therefore

    A_i^*(S_i)
      = S_(i−1)^(1/2) Phi_i^*(P_i) S_(i−1)^(1/2)
      = S_(i−1).

Also D_i^*(S_i)=0. This proves (1), including singular S_i and i=0.

### 2.3 Exact prefix reconstruction and support compression

Let

    C_i = B_i ... B_0.

Then

    U_i = Ad_[S_i^(1/2)] C_i,                           (2)
    Ad_[P_i] C_i = Ad_[S_i^(dagger/2)] U_i.              (3)

One way to verify both identities is to expand the B_i=A_i+D_i. Each A_i kills inputs supported on Q_(i−1), because of its input filter. Each D_i outputs in Q_i. Therefore, once a term uses D_k, every subsequent nonzero factor must be D_(k+1), D_(k+2), and so on. Every such term ends in Q_i and vanishes under either Ad_[P_i] or Ad_[S_i^(1/2)]. The all-A term telescopes, because every U_(i−1) already has output support in P_(i−1).

In particular (3) is an actual positive compression, not an inference by subtracting an EB remainder.

## 3. Take bounded limits

Starting with any subsequence along which N_n converges, take a further subsequence such that, simultaneously,

    H_n -> h,
    Phi_(i,n) -> Phi_i,
    S_(i,n) -> s_i,
    B_(i,n) -> B_i,
    P_(L,n) -> p_actual.

The channels and unital maps range over compact sets; the last support projections also have a convergent subsequence. Each s_i is positive with trace d, so its support is nonzero. Put

    p_i = supp s_i,       q_i = I−p_i,
    C_i = B_i ... B_0.

The symbol p_actual is intentionally distinct from p_L: eigenvalues can tend to zero without vanishing at any finite n, so the limiting actual support projection need not equal supp s_L.

Passing to limits in (1) and (2) gives

    B_i^*(s_i)=s_(i−1),                                (4)
    Phi_i ... Phi_1 E Ad_[h^(1/2)]
       = Ad_[s_i^(1/2)] C_i.                           (5)

The left side of (5) is EB, since E is EB, the input filter is CP, and every following map is CP. This is why an arbitrary initial H_n causes no additional difficulty. Applying the CP inverse filter on supp s_i therefore shows

    Ad_[p_i] C_i is EB,       for every i=0,...,L.      (6)

If any s_i is faithful, (6) already makes C_i EB, and all later C_j are EB. Hence assume from now on that all s_0,...,s_L are singular. Then all q_i are nonzero proper projections.

## 4. The surviving rare sector is a proper moving-support chain

Equation (4) gives

    tr[s_i B_i(q_(i−1))]
       = tr[s_(i−1) q_(i−1)] = 0.

Both operators in the trace are positive. Thus

    supp B_i(q_(i−1)) <= q_i.                          (7)

Apply the established rectangular PPT moving-support split to B_i, with moving input projection q_(i−1) and output projection q_i. For i=1,...,L, write

    B_i = F_i + G_i,

where F_i is CP and output-supported in q_i, while G_i is CP and input-supported in p_(i−1). Neither summand is claimed to be PPT.

Equation (6) makes every term

    G_i C_(i−1) = G_i Ad_[p_(i−1)] C_(i−1)

EB. Iterating C_i=F_i C_(i−1)+G_i C_(i−1) therefore yields a positive decomposition

    C_L = F_L ... F_1 B_0
          + sum_(j=1)^L F_L ... F_(j+1) G_j C_(j−1),  (8)

whose summands in the displayed sum are all EB.

It remains to treat the all-F term. For every i>=2, G_i vanishes on inputs supported in q_(i−1), so on that corner F_i equals B_i. The rectangular corner map

    Theta_i = Ad_[q_i] B_i Ad_[q_(i−1)]

is PPT between spaces of dimensions at most d−1. Since F_1 B_0 already outputs in q_1,

    F_L ... F_1 B_0 = Theta_L ... Theta_2 F_1 B_0.     (9)

There are L−1 >= R PPT corner factors in (9). The assumed lower-dimensional arbitrary-word bound makes their product EB, with any extra factors harmless. Composition with the CP endpoint F_1 B_0 remains EB. Equations (8)–(9) prove C_L EB.

Finally, (3) at i=L gives for the original normalized limit

    lim N_n = Ad_[p_actual] C_L,

which is EB by CP compression. This completes the proof, including moving and singular finite-parameter supports.

## 5. A simpler conservative proof, useful for checking the mechanism

If one only wants L>=2R+1, Section 4 can be shortened. If every s_i is singular, (7) is a whole chain of proper nonzero moving supports for B_1,...,B_L. The existing one-switch lemma directly makes their product EB when L>=2R+1. If any s_i is faithful, use (6) instead. This gives an independent short route to the two-Q-block conclusion because Q>=2R+1.

The sharper L>=R+1 argument uses the additional fact that every support-side prefix in (6) is already EB. That fact eliminates all G branches immediately, leaving only one lower-dimensional all-F branch.

## 6. Apply the actual tagged hypothesis

Take a sequence of actual first Q-tuples whose tags tend to zero. Extract a convergent tuple subsequence. Continuity of the max-over-B-subwords tag gives tag zero for the limit tuple. The proved tagged boundary statement then makes the limiting first Q-word E EB.

Keep all constituent factors of the second Q-word as the Phi_i in the general theorem, and allow an arbitrary H_n>=0 of trace d before the first word. Since Q>=R+1, every accumulation point of the output-normalized two-block product is EB.

For m>2, keep every remaining constituent factor in the tail as well; the same theorem applies with L=(m−1)Q. There is no potentially unbounded final output filter applied after an already-completed approximation argument: every factor is included in the single unital normalization and limit calculation.

This proves exactly the proposed candidate with m=2, and with the strictly weaker hypothesis that only the first tagged block has tag tending to zero.

## 7. Uniform and semialgebraic consequences

The sequential theorem implies a uniform modulus. Fix d and L>=R+1. As the initial CPTP map approaches the EB CPTP set, the distance of the final output-normalized map to the EB cone tends to zero uniformly over every choice of the L PPT CPTP tail factors and every initial H>=0 of trace d. Otherwise a sequence violating uniformity, followed by the compactness extraction in Section 3, would contradict the theorem.

For the tagged first Q-tuple one can obtain a Hölder form. Work in any fixed Euclidean norm on Choi matrices. Let the variables include that tuple, the L tail factors, H in the compact positive semidefinite trace-d slice, and the normalized final map. Take the closure of the graph of output normalization on this compact parameter space. The normalized maps are uniformly bounded because N(I) is a projection. The graph and its closure are semialgebraic: support, principal square root, and Moore–Penrose inverse on positive matrices have semialgebraic graphs. The EB cone is semialgebraic by a finite Caratheodory product-vector representation.

On this compact semialgebraic closure, define the continuous semialgebraic functions

    g = f_tag(first tuple),
    h = dist(J(N), Choi(EB)).

The theorem proves {g=0} is contained in {h=0}, including every boundary fiber created by singular normalization. The compact semialgebraic Lojasiewicz inequality therefore gives constants C>0 and beta>0, depending on the fixed dimensions and lengths, such that

    dist(J(N), Choi(EB)) <= C f_tag^beta.              (10)

The same Kraus-lift argument already used in the tagged boundary record converts (10) into a vanishing rank-one Kraus defect for the output-normalized product, with possibly changed constants and exponent.

No exponent is computed here. No positive threshold for the distance or defect is claimed to force EB for an individual finite-parameter word.

## 8. What is and is not closed

This proves the requested factor-sensitive weak-word normalization lemma, including its singular-support formulation, without assuming PPT_d is contained in SP_(d−1).

Its proof uses the actual serial factor structure: the trace-preserving transport identity makes the normalized rare kernels a positive moving-support chain, and the lower-dimensional exact premise kills that chain. It does not infer exactness from a final output certificate alone.

It provides uniform and semialgebraic control after normalization for a fixed number of genuinely PPT factors. To complete a dimension-d finite exact word theorem, one must still show how the resulting relative error and exponent interact with a genuine separable interior anchor or another exact mechanism. Approximate EB, even after all output normalization, is not itself exact EB at nonzero tag. The examples in FILTER_UNIFORM_APPROXIMATION_EXACTNESS_BARRIER.md remain consistent with this result because they do not supply the required long PPT factorization with an initial channel tending to EB.

## Appendix A. Direct semialgebraic Kraus-defect version

The Hölder conclusion can be stated directly in the multiplicative Kraus defect, without relying on a distance-to-separability exponent followed by a separate lifting estimate.

Let K=d^4 and, for a CP map T with tr T(I)<=d, define

    b(T) = min sum_(a=1)^K ||wedge^2 K_a||_op,

where the minimum is over K-term Kraus representations of T, padded by zero operators if necessary. In Choi coordinates, write V for the d^2-by-K matrix with columns vec K_a. Its constraint is VV*=J(T), and its squared Frobenius norm is tr J(T)<=d. Thus the feasible set is nonempty and compact.

The function b is semialgebraic, by its finite-dimensional minimum formulation and the semialgebraicity of the operator norm. Also b(T)=0 exactly when T is EB. The reverse implication uses the conical Caratheodory theorem in the real d^4-dimensional space of Hermitian d^2-by-d^2 matrices: an EB Choi matrix has a sum of at most d^4 positive product rank-one terms.

For completeness b is continuous, including at singular Choi matrices. Lower semicontinuity follows by extracting convergent minimizing Kraus arrays. For the upper bound, fix an optimal array V for J. There is a d^2-by-K coisometry W with

    V = sqrt(J) W,       WW*=I_(d^2).

Indeed the partial isometry in the polar factorization of V can be extended to such a coisometry because K>=d^2. If J_n->J, use V_n=sqrt(J_n)W; then V_n V_n*=J_n and V_n->V. Continuity of the objective gives limsup b(T_n)<=b(T).

Now apply the compact semialgebraic Lojasiewicz inequality directly with

    g=f_tag(first actual Q-tuple),      h=b(N)

on the closed normalization graph described in Section 7. The proved boundary lemma shows {g=0} subset {h=0}. Consequently

    b(N) <= A f_tag^alpha                               (11)

for fixed A,alpha>0, uniformly over every initial H>=0 of trace d and the fixed number L>=R+1 of PPT CPTP tail factors.

Although b was defined using K=d^4 slots for compactness, every representation used to estimate it can be taken with finitely many slots, and bounds can be propagated using the explicit represented Kraus families. In particular, if T_1,...,T_m each have families with defects at most b_1,...,b_m, their product has the composed family satisfying

    sum ||wedge^2(K_(m,a_m)...K_(1,a_1))||_op
      <= product_(j=1)^m b_j,                           (12)

by exterior-power multiplicativity and the operator-norm inequality. No assertion that the number of composed Kraus operators remains d^4 is needed in (12).

## Appendix B. Linear rank-one truncation estimate

For any Kraus matrix K, let L be its top singular-value term, let R=K−L, and write its largest two singular values as s_1>=s_2. The Hilbert–Schmidt vectors vec L and vec R are orthogonal. Thus

    || |K><K| − |L><L| ||_F^2
      = 2 s_1^2 ||R||_F^2 + ||R||_F^4
      <= (d^2−1) s_1^2 s_2^2.

Here ||R||_F^2<=(d−1)s_2^2 and s_2<=s_1. Since ||wedge^2 K||_op=s_1 s_2, termwise truncation of a Kraus family with defect at most b produces an EB map F such that

    ||J(T)−J(F)||_F <= sqrt(d^2−1) b.                  (13)

The estimate is linear in the defect, so no square-root loss in the exponent is necessary when (11) is multiplied across normalized groups.

Finally any CP map with tr T(I)=d has a Kraus family obeying

    sum ||wedge^2 K_a||_op
      <= (1/2) sum ||K_a||_F^2 = d/2,                 (14)

because s_1 s_2<=(s_1^2+s_2^2)/2. This applies both to CPTP maps and to unital CP maps, and controls fixed unnormalized gaps or the initial normalized prefix in a concatenation.
