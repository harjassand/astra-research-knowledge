# Exact reductions and a local-robustness barrier for unrestricted PPT words

9 October 2026. These are rigorous reductions, not a completion of the unrestricted theorem. They complement the proved-candidate bistochastic theorem and the strictly-positive filtered-word theorem. No priority claim is made.

## 1. Strict-positive versus low-Schmidt-number dichotomy

Every PPT CP map Phi:M_d -> M_d satisfies at least one of:

- Phi is strictly output-positive;
- Phi is (d-1)-superpositive: it admits a Kraus decomposition of matrices of rank at most d-1.

To prove this, if strict positivity fails, choose a rank-one projection P with Phi(P) singular. Choose a proper nonzero output projection P' containing its support; if Phi(P)=0, any proper nonzero P' works. The rectangular PPT split in MOVING_SUPPORT_AND_NORMALIZATION.md gives Phi=F+G, where F is output-supported on P' and G is input-supported on Q=I-P. Every Kraus matrix in F has rank at most rank P'<=d-1, and every Kraus matrix in G has rank at most rank Q=d-1.

The assertion for d=1 is trivial because every map is EB; the displayed split is used for d>=2.

This dichotomy does not assert PPT_d subset SP_(d-1): strictly positive PPT maps are not assigned a Schmidt-number bound here.

## 2. Compact tagged boundary, conditional on lower dimensions

Assume the unrestricted arbitrary-word EB bound R=N(d-1) is valid. By fixed-dimension padding it also applies to rectangular PPT chains whose intermediate and endpoint dimensions are at most d-1.

Put

 B=2R+1,          Q=(R+1)B.

Consider any word of Q PPT CPTP maps on M_d.

First, R+1 factors having singular GLOBAL output support force the whole word to be EB. List their positions j_1<...<j_(R+1), and choose isometries V_l onto supp Phi_(j_l)(I). Compress each intervening segment as

 Theta_l=Ad_(V_(l+1)*) Phi_(j_(l+1)) ... Phi_(j_l+1) Ad_(V_l).

Every Theta_l is a rectangular PPT map between dimensions at most d-1. There are R such transitions. Their product is EB by the hypothesis and factors through the original word with CP endpoints. Adjacent singular factors cause no problem: the segment still contains the next PPT factor.

Otherwise there are at most R singular-global-output factors. If all consecutive runs of full-output factors had length at most B-1, the total word length would be at most

 R+(R+1)(B-1)=Q-1.

Hence there is a B-long run in which every factor Phi_i(I)>0. If the entire word is nonEB, this subword is nonEB. Section 3 of MOVING_SUPPORT_AND_NORMALIZATION.md then makes this subword strictly output-positive.

For the Q-tuple define

 f_tag=max { f(Phi_(j+B-1)...Phi_j) : 1<=j<=Q-B+1 },
 f(T)=min_{rho>=0,tr rho=1} lambda_min T(rho).

We have proved

 f_tag=0  ==>  the Q-word is EB.                         (1)

The tuple space is the full compact PPT CPTP slice raised to the Qth Cartesian power; no faithfulness restriction is imposed on its factors. The tag is continuous and semialgebraic. Lojasiewicz plus the Kraus lift therefore gives a Kraus family for the whole Q-word satisfying

 sum_a ||wedge^2 K_a|| <= A f_tag^alpha                  (2)

for constants A,alpha>0 depending only on d and the lower-dimensional bound.

## 3. Strong tagged blocks are now handled without unitality

A tagged Q-block with f_tag>=epsilon contains a contiguous strictly-positive CPTP subword with margin at least epsilon. Distinct Q-blocks have disjoint such anchors. The strongly-positive filtered theorem applies to these anchors, allowing all maps between them to be arbitrary CP.

Thus a sufficiently large number H(d,epsilon) of strong tagged blocks forces EB. This statement no longer needs the intervening maps to be bistochastic.

The only branch not closed by (1)–(2) and the strong-anchor theorem is a long run of blocks with arbitrarily small tags. A maximal tag may sit near the beginning of the evolution, and ordinary rank-one truncation of the long later tail need not be small relative to its possibly singular output state.

## 4. Local filtered robustness near a pure replacer is equivalent to the whole problem

Fix a unit vector a and the EB CPTP pure-replacer map

 R_a(X)=tr(X)|a><a|.

Let U be any relative neighborhood of R_a in the PPT CPTP slice. Fix a positive integer N. The following statements are equivalent:

(A) Every product of N arbitrary PPT CP maps on M_d is EB.
(B) Every word of N factors from U, with arbitrary CP maps inserted between them, is EB.

The forward implication absorbs each intervening CP map into a neighboring PPT factor.

For the converse first take arbitrary strictly output-positive PPT CPTP maps Phi_i. For one such map Phi, set P=|a><a|, A_t=P+t(I-P), t>0, and

 Y_t=Phi*(A_t^2),
 Theta_t=Ad_(A_t) Phi Ad_(Y_t^(-1/2)).

Strict output positivity of Phi implies Phi*(P)>0: for every nonzero x,

 <x,Phi*(P)x>=<a,Phi(|x><x|)a>>0.

Hence Y_t is invertible even at the t=0 limit. Each Theta_t is CPTP and PPT, and

 Theta_t -> R_a                 as t decreases to zero.             (3)

Indeed the limit sends X to P times tr[Phi*(P) Y_0^(-1/2) X Y_0^(-1/2)]=tr(X)P.

For each Phi_i choose t_i so that Theta_i lies in U. The identity

 Phi_i=Ad_(A_(t_i)^(-1)) Theta_i Ad_(Y_(t_i)^(1/2))

rewrites the original word as a word of the Theta_i with invertible single-Kraus CP maps between them and at its two endpoints. Under (B), the middle word is EB, hence the original word is EB.

For arbitrary PPT CPTP factors, regularize each as (1-delta)Phi_i+delta D/d. These are strictly output-positive. Apply the proved conclusion and let delta tend to zero. Finally use the exact same-dimension CP-to-CPTP word normalization in MOVING_SUPPORT_AND_NORMALIZATION.md to obtain (A).

Consequences:

- A single pure replacer has filtered EB index one, but its pointwise property cannot be promoted to a uniform filtered index on a neighborhood by an automatic compactness argument.
- Any proposed such neighborhood theorem, even around this simplest singular EB map, already contains the full unrestricted PPT-word problem.
- This is an exact equivalence, not a counterexample to (A) or (B).
- The fixed strictly-positive seed theorem remains compatible: its compact family stays away from this singular limit, and its constants are allowed to depend on that family.
