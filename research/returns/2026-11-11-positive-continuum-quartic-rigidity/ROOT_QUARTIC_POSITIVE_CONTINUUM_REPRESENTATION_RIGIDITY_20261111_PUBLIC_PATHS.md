Positive continuum representations of the original quartic family
11 November 2026 Brisbane

1. Question and inherited geometry.

For k>1/3 let ell=3k-1,n=k+1 and
 J_k(F)=ell(ku-v+2j)^2/(8n)+ell uv/4+j^2,
 u=|F_col1|^2,v=|F_col2|^2,j=det F.
The accepted family is nonnegative and rank-one convex. The original full quasiconvexity question remains open outside its proved large-parameter tail. This note does not prove quasiconvexity or construct a negative compatible gradient.

The unchanged original family_geometry.txt gives the complete nonzero Legendre--Hadamard zero pairs, with B_k=[[0,k],[1,0]]:
 (F,H)=(t Q,a Qe1 tensor e2),
 (F,H)=(t Q B_k,a Qe1 tensor e1),
 Q in SO(2), t and a nonzero.
Its geometric rigidity argument also establishes the following useful form: if h>1/3 and invertible L,R satisfy
 D^2[J_h(L dot R)](F)[H,H]=0
on BOTH full zero orbits above, then h=k. The proof first forces R to be monomial; orthogonality through every Q then forces L to be conformal, and the remaining column-length ratios force h=k. This is the already established zero-orbit argument, not a new proof of rank-one convexity or of that finite rigidity theorem.

Finite positive transformed-family propagation is already excluded by that result. The operation addressed here is a positive CONTINUUM integral, where individual parameter points may have measure zero and cannot be subtracted as positive atoms. Its differentiation and common almost-everywhere zero set must be justified rather than assumed.

2. Precise continuum theorem.

Let (Omega,mu) be any positive sigma-finite measure space. Let h:Omega->(1/3,infinity), c:Omega->[0,infinity), and L,R:Omega->R^(2x2) be measurable finite-valued functions. Matrices L,R may be singular. Put
 p_omega(F)=c(omega)J_(h(omega))(L(omega)F R(omega)).
Suppose the positive integral is finite at every point of the FIXED grid
 Xi={0,1,2,3,4}^4,
where F is identified with its four real entries. Suppose for a finite C^2 rank-one-convex function H on R^(2x2) that
 J_k(F)=H(F)+integral_Omega p_omega(F)dmu(omega)          (1)
for every F. Pointwise finiteness of an originally proposed representation already implies the grid condition; it is not an additional uniform-integrability assumption on the parameters.

Then for mu-almost EVERY omega with c(omega)>0 and BOTH L(omega),R(omega) invertible,
 h(omega)=k.                                          (2)

Every summand whose L or R is singular is an ordinary convex function of F. In particular if h(omega) is restricted to a set excluding k, every nonzero integral contribution must be singular and convex almost everywhere. A positive continuum of genuinely invertible changes of OTHER family parameters cannot provide (1).

3. Automatic coefficient integrability and differentiation.

Each p_omega is a nonnegative homogeneous quartic polynomial in four variables, with total degree4 and degree at most4 in each variable. Tensor Lagrange interpolation on Xi writes every coefficient a_alpha(omega) as a FIXED finite rational linear combination
 a_alpha(omega)=sum_(xi in Xi)w_(alpha,xi)p_omega(xi).
There are only35 total-degree-four coefficients; using the625-point tensor grid is a convenient fixed overdescription. Thus
 integral |a_alpha|dmu
 <=sum_xi |w_(alpha,xi)| integral p_omega(xi)dmu<infinity. (3)
Nonnegativity is essential to this bound. No cancellation of divergent positive integrals is permitted.

It follows that the integral in(1) is itself a homogeneous quartic polynomial P, and derivatives through order4 commute with the integral. On every bounded set of F, the derivative integrands are dominated by a fixed finite multiple of sum_xi p_omega(xi). In particular
 D^2 P(F)[U,U]=integral D^2p_omega(F)[U,U]dmu.           (4)
The only constants in this integrability step are fixed rational interpolation weights and elementary polynomial norm bounds; no integral-evaluation oracle is assumed. Since J_k-P is a polynomial, H in(1) is also a homogeneous quartic; no unobserved singular remainder is hidden in(1).

4. A common full-measure zero set.

For rank-one U, each integrand in(4) is nonnegative: composition by L,R sends a rank-one increment to rank at most one. The same Hessian of H is nonnegative by its C^2 rank-one convexity.

Fix one LH-zero pair (F,U) of J_k. Differentiating(1) gives
 0=D^2H(F)[U,U]+integral D^2p_omega(F)[U,U]dmu.
Hence D^2p_omega(F)[U,U]=0 almost everywhere for this pair. To avoid incorrectly intersecting uncountably many full-measure sets, first take t=a=1 and a COUNTABLE dense collection of rotations Q on each of the two zero orbits. Intersect those countably many full-measure sets. At every omega in the intersection, continuity of the polynomial Hessian in Q gives zero for ALL Q. Homogeneity then restores arbitrary nonzero t,a.

For c>0 and invertible L,R, the inherited zero-orbit rigidity argument now applies and proves(2). This uses its actual geometric hypothesis. It does NOT assert that J_k-p_omega is rank-one convex for a zero-measure parameter point, an inference that would be unjustified for a nonatomic integral.

5. Singular transformations are convex contributions.

If either L or R has rank at most one, then L(F1-F0)R has rank at most one for EVERY F0,F1. Rank-one convexity of J_h on this image therefore gives ordinary convexity of F->J_h(LFR) along every matrix segment. Multiplication by c>=0 preserves convexity. Their integrable positive sum is convex, with the smoothness supplied by(3).

Consequently, even allowing singular matrices INSIDE the integral does not restore an invertible positive propagation route from a proved parameter tail to a different k. If the remainder H is to be quasiconvex, constructing that remainder is still an actual operation; (1) cannot supply it merely by positive averaging of other parameter values. A zero integral and H=J_k are of course permitted and prove nothing new about J_k.

6. Exact scope and what remains open.

The theorem covers finite sums, countable positive series and positive nonatomic integrals with finite pointwise energy. No uniform bound on h, L, R or c was imposed. Ordinary positive-integral proposals therefore cannot bypass the earlier finite rigidity by switching to a continuum and citing lack of domination; the finite-dimensional polynomial structure supplies the required domination itself.

This does NOT exclude every coefficientwise limit of positive decompositions. A sequence may escape to parameters at infinity or degenerate transformations with compensating unbounded weights, so that its limiting representation has no ordinary measure on the finite parameter space used here. Such compactified or singular limiting constructions require an additional theorem. Nonlinear transformations, nonlocal operations, translated functions, signed cancellations and the separate two-row projection construction also remain outside this statement. The missing touching representation for J_k is not supplied. No full original positive or negative follows.

7. Governing source binding.

The current full question is P1_FULL_ORIGINAL_QUARTIC_AFTER_GLOBAL_TAIL_PRO_20261111.txt7150ASCII/SHA1361685f04ee421c5035987a76fa3b5b1c59bf0eb2fe72ca3f617cb467024e27. The inherited zero classification/finite rigidity is in the unchanged P1_PRO_BCE9EB_ORIGINAL_20261111.zip1315850/SHA48575ad94d9ebfc7c999285f9d5a5ee412a98e758e916e933c72f485d831eea8, member quartic_research_packet/family_geometry.txt4470UTF8/SHAec43b4a60031bacbe3ae4d9dc382e0654e753998b9463f22673d049d41576dd9. The original member was read at its governing proof, without executing its lh.py code. Its zero-orbit machinery is credited once. The additional operation here is the automatic coefficient-integrability argument, the common almost-everywhere zero set for an arbitrary positive continuum, and the explicit distinction from singular limits outside that representation.
