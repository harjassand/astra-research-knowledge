# Family 197: an infinite, non-finite-type Wold tail for the one-sided inverse

Date: 2026-10-08, Brisbane.
Status: NEW TO THIS REPOSITORY (independently reconstructed here, conditional on the source's algebraic witness). This is NOT a resolution of the supremal Rokhlin-entropy question, NOT a theorem of Bernoulli measurable conjugacy, and NOT a claim of literature priority or specialist/formal verification.

## Evidence and pinning

* Astra repository base commit: b5824d0fcbfe0688980788da2722270a2f068fb0; initial route 00_START_HERE.txt, prior notes state/2026-10-08-bowen-bernoulli-direct-finiteness/RESEARCH.md and ADDITIONAL_AUDITS.md; state/2026-10-08-formanek-frontier/RESEARCH_STATE.md.
* Source repo openai/math at fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb; source preprint (October 4, 2026), build/sections/introduction.tex, algebra.tex and assembly.tex, in preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026. Its Proposition "Parity criterion" gives the specific finite sums a=sum_x g_x, b=sum_x g_x^{-1}, c=sum_y h_y^{-1}, with ab=1, ac=0, c nonzero, hence ba != 1. Its Main Theorem reports a finitely presented torsion-free group with finite 2-dimensional K(G,1). This source proof has not been independently certified in this run. Our conditional theorem requires only finite generation and ab=1 != ba.
* Seward, Krieger's finite generator theorem for actions of countable groups II (2019), Theorems 1.10, 1.12; https://mathweb.ucsd.edu/~bseward/Files/krieger2.pdf ; earlier Astra notes already audit their conditional use.
* Ceccherini-Silberstein, Coornaert, Phung, "On linear shifts of finite type and their endomorphisms", J. Pure Appl. Algebra 226 (2022), 106962; https://arxiv.org/abs/2011.14191 ; proves general limit-set / nilpotency and finite-dimensionality results. Infinite limit set for a non-nilpotent endomorphism of a finitely generated-group full shift is already covered by this prior art. We did not compare every proof/statement in the full paper. Novelty/priority of our *specific* left-module decomposition and non-SFT application is UNKNOWN, not certified.
* Tim Austin, ICM 2026 structural ergodic theory survey, Question 3.1 (whether a group can have Rokhlin entropy identically zero), https://epubs.siam.org/doi/10.1137/25M1805564 .

## Exact theorem (independent of the entropy supremum)

Let G be a **finitely generated infinite** group, k a finite field, R=k[G], and a,b in R satisfy ab=1 and ba != 1. Use X=k^G with the left G-shift (g.x)(h)=x(g^{-1}h) and Haar product measure. For v=sum_s v_s s in R put (T_v x)(h)=sum_s v_s x(hs), so T_v T_w=T_{vw}. Set

    A=T_a, B=T_b, r=1-ba, C=T_r=1-BA,
    K=ker A=im C,
    Y_n=B^nX  (n>=0),
    Z(x)=(C A^j x)_{j>=0}.

The following hold:

1. For every n>=1, the map x -> (C x, C A x, ..., C A^{n-1}x, A^n x) is an equivariant continuous compact-group isomorphism X ≅ K^n × X, inverse (z_0,...,z_{n-1},y) -> sum_{j<n} B^j z_j+B^n y. Haar pushes forward to Haar(K)^n × Haar(X). Consequently Z is an equivariant continuous surjection X -> K^N with Haar image equal to the infinite Haar product (iid K innovations).
2. ker Z = T = intersection_{n>=0} Y_n. The inclusions Y_n ⊋ Y_{n+1} are all strict. The left G-action preserves T; moreover A and B restrict to mutually inverse topological automorphisms of T.
3. The tail T is **not a subshift of finite type**, and hence cannot be equivariantly topologically conjugate to any nontrivial finite-alphabet full shift. This holds even without finite generation of G.
4. T is **infinite**, provided G is finitely generated. Its Haar measure is nonatomic. Thus the conditional Haar measure on every fiber of Z is a translate of Haar(T); in particular an iid innovation sequence never determines x, even modulo finitely many choices.
5. More precisely, identify the Pontryagin dual of X with the additive group of R using the finite-field trace pairing. The G-action makes it a left R-module. Let N=T^perp. Then, as *left R-modules*,

    N = union_{n>=1} ker( right multiplication by b^n )
      = direct_sum_{j>=0} (R r) a^j.

   Each summand is a nonzero left R-submodule, isomorphic to Rr. Hence N is an **infinitely generated left ideal** of R. The canonical cyclic left module R/N (dual to T) is not finitely presented.

The theorem is about the original G; NO product with another group is used.

## Proof, including all algebraic orientations

**Step 1: algebraic decomposition.** Since ab=1, AB=1. Also r^2=r, a r=0 and r b=0. Therefore C^2=C, A C=0 and C B=0, and B A+C=1. The one-step map x -> (Cx,Ax) has inverse (z,y) -> z+B y on K×X. Iteration gives assertion 1 and its inverse. These are compact-group isomorphisms, so Haar becomes product Haar, not merely an informal assertion about marginal distributions. Every finite prefix of Z is onto K^n. Hence Z(X), a closed subset of K^N, meets every finite cylinder; compactness implies Z(X)=K^N. Haar is therefore the Haar product.

**Step 2: residual kernel and strictness.** The identity Cx=0 iff x∈BX follows from C=1-BA and CB=0. More generally C A^j x=0 for all 0<=j<n iff x=B^n A^n x∈B^n X (inductively peel off the first n innovations). This gives ker Z=∩_n Y_n. Because B injective, non-surjectivity of B is equivalent to ba!=1 (as AB=1); if Y_n=Y_{n+1}, applying A^n would give X=BX, contradiction. The equality B(T)=T uses B injective and compactness to commute B with decreasing intersections. A B=1 and BA|_T=1 (because T⊆BX), proving A|_T=B|_T^{-1}.

**Step 3: non-SFT by compactness (proof independent of module Step 4).** Suppose T is SFT with a finite memory F⊆G and a finite set P⊆k^F of allowed patterns, i.e. x∈T iff (g^{-1}.x)|_F ∈P for all g. Replace P by the exact set π_F(T): because π_F(T)⊆P and T already equals the P-defined shift, the resulting shift is still T. The finite pattern sets π_F(Y_n) form a descending chain and satisfy

    intersection_n π_F(Y_n) = π_F(intersection_n Y_n) = π_F(T).

The second equality is compactness: preimages of a fixed finite pattern are clopen and the Y_n are nested compact. Since k^F is finite, for some n0 the sets π_F(Y_n) equal π_F(T) for all n>=n0. Hence every configuration y∈Y_{n0} has all shifted F-patterns in π_F(T), so y∈T. Thus Y_{n0}=T, contrary to the strict descent of Y_n. Hence T is not SFT. Since finite-range equivariant conjugacies and their inverses preserve SFT, T is not topologically conjugate to a finite-alphabet full shift.

**Step 4: Pontryagin dual and direct-sum calculation (independent adversarial check).** Under the right-convolution convention, for v∈R and x∈X,

    <v,T_b x> = <v b,x>,

where the pairing is coordinatewise with an additive character of k (using the field trace for extension fields). Thus (im B^n)^perp=ker(v -> v b^n), and T^perp is their increasing union. Note it is a LEFT R-ideal, because left multiplication commutes with right multiplication by b.

For v with vb^n=0, recursively apply v=vr+(vb)a to obtain the exact telescoping formula

    v = sum_{j=0}^{n-1} (v b^j) r a^j.

Conversely every w r a^j with j<n satisfies (w r a^j) b^n= w r b^{n-j}=0. The sum for a fixed n is direct: if sum_{j=0}^{n-1} w_j r a^j =0, multiply on the right by b^{n-1}. All terms j<n-1 vanish as r b=0 and the last becomes w_{n-1}r because a^{n-1}b^{n-1}=1; so w_{n-1}r=0. Descend inductively. The map Rr -> (Rr)a^j is injective, as (w r a^j)b^j=w r. Hence every summand is a nonzero left R-module isomorphic to Rr. This proves the asserted direct sum, and N is not finitely generated as a left ideal (a finite set of elements occupies only finitely many summands and left R-action preserves the summand index).

**Step 5: T is infinite.** Suppose the compact profinite k-vector group T were finite. Its Pontryagin dual R/N would be finite-dimensional over k. For a finitely generated G, *any finite-codimension left ideal J of k[G] is finitely generated*. Here is a direct proof of this lemma. Select elements t_1=1,t_2,...,t_d∈G whose images form a k-basis of R/J. Let S be a finite symmetric generating set of G. For each s∈S and i≤d, write s t_i ≡ sum_j c_{sij} t_j (mod J), and let J_0 be the left ideal generated by the finitely many elements s t_i−sum_j c_{sij}t_j. Then J_0⊆J. Induction on group-word length, repeatedly reducing left multiplication by s, shows R/J_0 is spanned by the d cosets of t_i; their images are linearly independent because J_0⊆J and they form a basis modulo J. Thus dim_k R/J_0=d=dim_k R/J, so J_0=J. Applying this to J=N contradicts the infinite direct-sum decomposition. Therefore R/N, and hence T, is infinite. Infinite compact groups have atomless Haar measure. By compact-group disintegration, every Z-fiber is a coset of T with conditional Haar measure; there cannot be a finite-to-one inverse even almost surely.

**Supplement:** ε(a)ε(b)=1 under augmentation ε:R→k, so ε(r)=0. Thus N⊆ker ε, and T contains all constant configurations. The proof above is much stronger: the tail has infinite dimension, not just q constant points. For the original F2 source, ε(a)=ε(b)=1, and a and b are formally inverse coefficient supports, but neither property is needed in the theorem.

## Scope and limitations for Rokhlin entropy and Bowen

In the existing Astra research, with m=|supp(1-ba)|, Seward's finite-window upper bound and finite Bernoulli minimum theorem gave the conditional inequality

    0 <= s=h_sup^Rok(G_197) <= (1-1/m) log 2 < log 2.

**Nothing here strengthens this inequality.** The tail theorem eliminates one tempting *method* for showing that all innovations exhaust X, but non-SFT is a topological invariant, not a measurable entropy lower bound. A measurable equivariant isomorphism between the tails and other actions is not excluded by the theorem; no nonlinear coding with small Shannon cost has been produced.

If s>0, Seward's minimum formula yields uncountably many pairwise nonisomorphic Bernoulli shifts with distinct base entropies below s, refuting Bowen's complete collapse for this G. If s=0, only finite-Shannon Bernoulli Rokhlin entropies collapse; infinite-base shifts still require ruling out *every* positive-Rokhlin-entropy free ergodic action, including infinite-entropy actions, and even that would not prove measurable conjugacy. This is inherited from the existing Astra notes and Seward, not a new theorem.

## Routes tested and exact failures

A. Zero-entropy direction: Try infinite iteration of the canonical Haar splitting and a nonlinear completion from the iid K-innovations. The exact factor Z is onto K^N with independent Haar coordinates, but the residual compact group T is *infinite*, not finite or trivial, and is non-SFT. Any generating partition measurable with respect to σ(Z) alone cannot generate X since its fibers are nonatomic. This is a decisive obstruction to innovation-only coding; it does not obstruct nonlinear coding that also encodes the tail.

B. Positive-entropy direction: Positive first L2-Betti numbers, cost inequalities and algebraic-action sofic-entropy techniques were investigated as candidate lower bounds. They do not yield a verified positive Rokhlin entropy action for the **nonsofic** family-197 G: relevant published results concern sofic entropy / require a sofic approximation, and neither a strictly positive L2-Betti invariant nor an entropy-preserving transfer theorem has been calculated for G. In particular a large Euler characteristic of a 2D aspherical presentation (if computable) does **not** imply beta_1^(2)>0 or a positive Rokhlin lower bound. This route did not produce a theorem.

C. Bernoulli isomorphism: Factor equivalence and equivariant topological Haar splitting do not give a measurable inverse or Bernoulli classification. No isomorphism between unequal-base Bernoulli shifts has been obtained.

D. Literature-priority correction: General infinitude of a limit set of a nonnilpotent cellular automaton on a mixing linear shift over finitely generated G is in Ceccherini-Silberstein–Coornaert–Phung (2022), so claiming novelty for infinitude alone would be wrong. The elementary compactness proof of non-SFT and the explicit decomposition of the dual annihilator are recorded as source-independent deductions, without a claim that their statements are unpublished.

## Remaining exact obstruction

To establish s=0, for every ε>0 one must construct a **G-generating measurable partition** of the free ergodic uniform 2-shift (or, by Seward's minimum theorem and the known strict bound, show its Rokhlin entropy 0) with Shannon entropy <ε. The innovation factor leaves an infinite nonatomic tail, so an innovation-based construction must additionally encode that tail equivariantly at vanishing *total* Shannon cost. No such theorem follows from the algebraic splitting.

To establish s>0, exhibit a free ergodic action with finite positive Rokhlin entropy (e.g. prove a uniform Shannon lower bound for all generating partitions of X), or prove an independent general lower-bound theorem applicable to this particular nonsofic group. No such bound is established.

To settle Bowen's measurable Bernoulli isomorphism question beyond an entropy obstruction, give a genuine measurable conjugacy or a distinct isomorphism invariant, while treating infinite-base shifts separately.

No independent subagents, formal proof assistant, specialist reviewers or priority certification were used; two distinct proof routes (symbolic compactness and explicit group-algebra module duality) were checked within a single agent. This is a conditional, rigorous intermediate theorem and handoff, not a resolution of the stated entropy dichotomy.


## Additional corollary: the whole finite-quotient subsystem survives every iterate

Let H_fin be the intersection of all finite-index normal subgroups of G (the finite residual). Then

    X^{H_fin} = closure{ configurations having finite G-orbit }  ⊆ T.

To verify the inclusion, for each normal finite-index subgroup L, the invariant space X^L is finite-dimensional and B acts injectively on it (AB=1). Therefore B is a bijection on X^L, so X^L=B^n(X^L)⊆B^nX for every n. Hence each finite-orbit configuration lies in T. The equality of the closure with X^{H_fin} follows because G/H_fin is residually finite: any finite prescribed pattern on distinct cosets of H_fin can be realized by a configuration factoring through some finite quotient, using a product of finite quotients to separate all finitely many required cosets.

Thus the non-SFT tail contains the entire full shift inflated from the maximal residually finite quotient. This sharpens the prior Astra finite-quotient observation (each B^n image contains all periodic points); it does not prove T is exhausted by periodic configurations, nor does it yield a free G-action or any positive Rokhlin-entropy lower bound, since H_fin acts trivially on X^{H_fin}. In particular this does **not** turn a sofic-entropy calculation for G/H_fin into one for G.


## Finite-stage contrast (explicit local models)

Every Y_n is itself a *linear subshift of finite type*: since A^nB^n=1, the operator B^nA^n is an idempotent cellular automaton with image Y_n and

    Y_n = ker( I - B^n A^n ) = {x in X : T_{1-b^n a^n}(x)=0}.

The last equation is a finite-radius, equivariant system of local linear constraints. Moreover B^n:X→Y_n is an equivariant topological group conjugacy, with inverse A^n restricted to Y_n. Therefore the system exhibits a **strictly descending tower of finite-type subshifts, each topologically conjugate to the full Bernoulli shift, whose intersection is not of finite type**. This clarifies why no finite stage, no finite-quotient test, and no fixed coding window recovers the tail. It remains a statement about topological symbolic structure, not measurable Rokhlin entropy.
