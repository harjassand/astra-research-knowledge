# Profile circulation: proof and scope audit

The incoming proof supports two conditional positivity mechanisms for compatible two-column gradients: exact cancellation of a polynomial profile circulation, and an exact calibration on one finite profile graph. The main identity and quartic lower bound survive the zero, sign, and large-background checks below. The result does not establish quasiconvexity for arbitrary planar gradients, and the finite-difference operation does not preserve an input field's energy.

The source package is work/FO-circulation-audit/source-copy/PROFILE_CIRCULATION.md (SHA256 881b80eac0bcfd04113dcba7226b9faee324dda66d44ffee5ae3ea097b072622). It is dated 14 October 2026 and labels its claims unreviewed. I found no algebraic contradiction in the stated hypotheses or checked examples. This is an internal proof audit and exact replay, not external mathematical or priority validation.

## Reconstructed circulation theorem

Let $F:\mathbb R^{m\times2}\to\mathbb R$ be $C^1$ and rank-one convex, let $\phi$ be smooth and periodic on a rectangle of $x$-period $L$, and fix a constant matrix $B$. Set $P=(\phi_x\mid0)$ and $Q=(0\mid\phi_y)$. Both increments have rank at most one. With

$$
R_F(C,Z)=F(C+Z)-F(C)-DF(C)[Z],
$$

one has pointwise

$$
F(B+P+Q)-F(B)
=R_F(B+Q,P)+R_F(B,Q)+DF(B+Q)[P]+DF(B)[Q].
$$

Convexity along the two rank-one lines makes both remainders nonnegative. The $y$-average of $DF(B)[Q]$ is zero. If $u(x)=\phi(x,\cdot)$ is viewed as a closed curve of periodic profiles, the remaining linear term is the circulation of

$$
\alpha_{F,B}(u)[v]=\mathbb E_y DF(B+(0\mid u_y))[(v\mid0)].
$$

Thus the exact identity is

$$
LJ_F(B,D\phi)=\int_0^L\mathbb E_y[R_F(B+Q,P)+R_F(B,Q)]\,dx+\oint_u\alpha_{F,B}.
$$

No phase coordinate, polar representation, or nonvanishing condition is used. This reconstructs source lines 27–56.

For a finite profile expansion $\phi(x,y)=\sum_{j=1}^d a_j(x)\psi_j(y)$, the one-form is $\sum_j\alpha_j(a)\,da_j$. If $F$ is polynomial of degree at most four, each $\alpha_j$ is a polynomial of degree at most three in $a$. Therefore the conditions

$$
\oint_a a^\beta\,da_j=0\qquad(|\beta|\le3,\ j=1,\ldots,d)
$$

cancel the circulation for every $B$, every choice of profiles, and every such $F$. The cancellation is independent of the coefficients of $F$. The resulting Jensen inequality applies to this compatible-gradient class; finite Fourier and polygonal approximation of arbitrary fields does not preserve these moment conditions (source lines 58–74, 76–101, 333–339).

For the quantitative bound, restrict $F$ to any rank-one line and write

$$
f(t)=At^4+Lt^3+C_2t^2+Dt+E,\qquad A=F_4(R)\ge0.
$$

Global convexity of $f$ gives $C_2\ge3L^2/(8A)$ when $A>0$, and the exact square identity

$$
f(1)-f(0)-f'(0)-A/3
=\frac{3(L+4A/3)^2}{8A}+C_2-\frac{3L^2}{8A}\ge0.
$$

If $A=0$, nonnegativity of $f''(t)=6Lt+2C_2$ for all real $t$ forces $L=0$ and $C_2\ge0$, so the same lower bound holds. With

$$
\mu_F=\min_{|R|=1,\ \operatorname{rank}R=1}F_4(R),
$$

each remainder is at least $\mu_F$ times the fourth power of its increment's norm divided by three. Since $|D\phi|^4\le2(|\phi_x|^4+|\phi_y|^4)$ pointwise, the source obtains, uniformly for every $B$,

$$
J_F(B,D\phi)\ge\frac{\mu_F}{6}\mathbb E|D\phi|^4.
$$

The proof covers degree-at-most-four rank-one-convex polynomials, any target dimension $m$, and two input columns. In particular, it covers the full 35-dimensional homogeneous quartic coefficient space on $2\times2$ matrices, conditional on exact circulation cancellation. It does not bound a general field merely because some profile moments are small (source lines 78–117).

## Regularity, density, and concentration

The theorem allows a closed coefficient path in $W^{1,4}([0,L];\mathbb R^d)$. Such a one-dimensional Sobolev path is continuous and bounded. With fixed smooth profiles, its compatible gradient lies in $L^4$, and the polynomial energy integrals vary continuously under strong $W^{1,4}$ approximation. Polygonal paths therefore give continuous potentials with piecewise smooth gradients; the derivative may jump at an interface, but the potential itself does not (source lines 119–123).

Every smooth periodic potential can be approximated in $W^{1,4}$ by truncating its Fourier series in $y$ and then approximating its coefficient curves in $x$ by polygonal curves. This is a density statement about representation only. It does not preserve exact circulation cancellation, so it cannot promote the theorem to all periodic gradients.

For zero-boundary rectangular examples, the source requires each profile to vanish at the $y$-endpoints and the amplitude path to start and finish at zero. Under the critical two-dimensional scaling $\phi_\rho(x)=\rho^{1/2}\phi(x/\rho)$, the unnormalized integral of $|D\phi_\rho|^4$ is unchanged. For a homogeneous quartic, the fully optimized unnormalized affine gap is unchanged as well: change variables $x=\rho z$ and rescale the optimizing background by $\rho^{-1/2}$. This covers concentrations of examples already in the construction; it does not represent arbitrary concentrated gradients in the cancelled-profile class.

## Two amplitudes and the finite-difference operation

For $d=2$, Green's theorem writes a polynomial one-form circulation as the integral of its curl against the signed winding function $w_a(r,s)$. The curl has degree at most two, so the six signed area moments

$$
M_{00},M_{10},M_{01},M_{20},M_{11},M_{02},\qquad
M_{ij}=\int w_a(r,s)r^is^j\,dr\,ds,
$$

are exactly the moments needed to cancel every polynomial one-form of degree at most three. They are signed moments, not moments of a positive probability law. For homogeneous quartics, they respectively remove the quadratic-, linear-, and constant-in-$B$ parts of the profile curvature (source lines 125–163).

The construction takes a closed loop $\Gamma$ and vector $v$, then forms the oriented current

$$
\Gamma-3T_v\Gamma+3T_{2v}\Gamma-T_{3v}\Gamma.
$$

For a degree-three polynomial one-form, the integral over $T_{tv}\Gamma$ is at most quadratic in $t$: the possible cubic term is a constant one-form, whose integral around $\Gamma$ is zero. The third finite difference therefore cancels it. Realizing the signed coefficients means one forward traversal, three reversals, three forward traversals, and one reversal, joined to a base point by exactly retraced connectors. This produces a new closed compatible profile path. It does not transform the original field while preserving its energy (source lines 165–187).

The explicit translated-square example has 46 segments. Its six area moments vanish, but $\int\!\!\int w r^3\,dr\,ds=-48$ and $\oint r^4\,ds=-192$, so it is not a retracing identity. Direct independent line integration also verifies all 20 moments $\oint r^is^j\,dr$ and $\oint r^is^j\,ds$ for $i+j\le3$, not just the six Green moments. Reversing the translation direction moves the path through negative $r$ and flips the higher current to $+192$, while all 20 cancelled moments remain zero. Both paths include the zero profile.

An exact energy check confirms the warning about preservation. On the same $x$-period 46, use scalar profiles $\psi_1=\cos y$, $\psi_2=\sin y$, the convex quartic $F(A)=A_{11}^4$, and the unit-square loop with four widths $23/2$. Its optimized normalized Jensen gap is $6/23^4$. Applying the displayed finite difference with step $(2,0)$, using unit widths for its 46 segments, gives $798/23$. For either field the affine gap is $\mathbb E(\phi_x^4)+6B_{11}^2\mathbb E(\phi_x^2)$, since the $y$-averages of $\phi_x$ and $\phi_x^3$ vanish. Thus these are exact fully optimized values, not merely different parameterizations of a fixed energy. Special loops or degenerate energies can still coincide; the counterexample is to universal energy preservation.

## Large backgrounds, zeros, and negative coefficients

The source construction has no division by $r$, $s$, or $|\phi|$. The zero profile and negative profile coordinates therefore cause no singularity. The direct positive- and negative-translation checks establish exact degree-three moment cancellation even when the path meets zero or crosses to $r<0$.

The large-background warning is sharp. For $F(A)=|A|^4/4$ on $1\times2$ matrices and profiles $\psi_1=\cos y$, $\psi_2=\sin y$, direct integration gives

$$
\alpha=B_1B_2(s\,dr-r\,ds).
$$

On a counterclockwise square of side $1/100$, $M_{00}=1/10000$, yet $B_1=B_2=10^6$ gives circulation $-200{,}000{,}000$. Hence small nonzero moments alone cannot yield a background-uniform estimate. This is not a negative Jensen gap: $F$ is convex, and the nonnegative Bregman terms offset the signed circulation. On the cancelled 46-segment paths, every relevant moment is exactly zero, so this circulation vanishes identically even for arbitrarily large $B$.

For a $2\times2$ matrix, write $u=|A e_1|^2$, $v=|A e_2|^2$, $w=(A e_1)\cdot(A e_2)$, and $q=\det A$. The exact test integrand $G$ itself contains the negative invariant coefficient $-\tfrac52qu$:

$$
G=3(u+v-2q)^2+\frac{35}{24}u^2+q^2-\frac52qu.
$$

Its rank-one restriction is $3(u+v)^2+\tfrac{35}{24}u^2$, so $\mu_G=3$. The copied verifier reconstructs a positive semidefinite acoustic Gram: its positive $6\times6$ block has leading minors $107/2,642,1605/8,8445/16,2815/8,26865/4$, and the remaining Schur complement is zero. This is a global rank-one-convexity certificate, not angular sampling. Separately, the determinant-balanced law on $\pm36I$ and $\pm\operatorname{diag}(1,-1)$, with total masses $1/1297$ and $1296/1297$, has mean matrix and mean determinant zero but mean $G=-1350/1297$. It certifies non-polyconvexity only; it is not a compatible-gradient counterexample.

The degenerate case $\mu=0$ is not covered by a strict coercivity claim. For example $F(A)=(\det A)^2=uv-w^2$ has a negative invariant coefficient, is rank-one convex because the determinant is affine along rank-one lines, and has $F_4(R)=0$ on every rank-one $R$. The theorem then asserts Jensen positivity for its cancellation class with a zero lower-bound constant, as written.

## Exact graph result and examples

The second positivity mechanism concerns $G$ and profiles $U_{r,s}(y)=re^{iy}+se^{-iy}$, represented as real two-component fields. The vertices are $(i/4,j/4)$, $i,j=0,\ldots,8$, and the five allowed widths are $1/8,1/4,1/2,1,2$. For every directed strip, the source forms

$$
w_e=\int G(D\phi_e)-\frac14\int|D\phi_e|^4.
$$

Its rational vertex potential, with common denominator 245760, satisfies $w_e\ge P(\mathrm{end})-P(\mathrm{start})$ for all $81^2\cdot5=32{,}805$ directed edge/width choices. Telescoping proves the $1/4$ coercive bound for every finite closed walk in this graph at zero background. The source proof then uses $D\phi(x,y+\pi)=-D\phi(x,y)$ to eliminate odd powers of $B$, and Parseval plus rank-one convexity to show the quadratic background term is nonnegative. This yields its all-background claim for this graph class only.

The source replay reports 104 raw negative strip-energy edges, 2,046 negative adjusted edges, 93 tight inequalities, and no negative adjusted cycle; the most negative raw edge is $(5/4,2)\to(2,5/4)$, width $1/2$, with energy $-1431/1280$. An independent exact calculation used the $u_0+u_1\cos(2y)$, $v_0+v_1\cos(2y)$, $q_0+q_1\cos(2y)$ formulas and rational segment integration, rather than the supplied Laurent-polynomial helpers. It rechecked every inequality and recovered all counts and the same minimum edge.

The other exact examples also reproduce:

- For the 46-strip, two-carrier field using $\psi_1=(\cos y,\sin y)$, $\psi_2=(\cos2y,\sin2y)$, $G$ has $b=(-3076/23,0,0,3064/23)\ne0$, $\mathbb E|D\phi|^4=191204/345$, $B_{\mathrm{opt}}=(-19549/92447,0,0,-96763/184894)$, and optimized gap $73027952684/31894215\ge\tfrac12\mathbb E|D\phi|^4$.
- Reversing the unit square in $[1,2]^2$ for carriers $1,3$ preserves $C$, $H$, $b=0$, and the fourth-gradient moment $25861/30$, but changes the exact optimized gaps from $119299/40$ to $106339/40$, a difference of $324$. This is a signed fourth-order interaction, not a negative gap.

These checks support the stated finite scope. The graph is not a calibration for arbitrary real profile values, widths, carrier families, or integrands; finite graph coverage does not pass to all profiles.

## What is new relative to N794 and N812

The source itself credits the component tools as established and disclaims historical priority. Internally, the new mathematical content is a distinct compatibility interface and restricted certificate, not the repetition of the previous modulation verifier.

| Earlier result | Already established there | Increment in this source | Still open |
|---|---|---|---|
| N794 | Exact eight-by-eight acoustic criterion for all nine left-SO(2) quartic coefficients; an equivalent nine-moment PSD-completion problem; the particular $F_\star$ now has a closed heat proof of quasiconvexity. | A field-level sufficient condition: vanishing profile-loop moments imply all-affine Jensen positivity for any rank-one-convex quartic, without rotational invariance; plus an exact finite-graph certificate for a different integrand $G$. | No general gradient-to-PSD-completion theorem, no arbitrary-gradient inclusion, and no consequence for the $F_\star$ heat-certificate class. Here $G\ne F_\star$. |
| N812 | A global Bregman/flux identity for one affine-phase convex-loop carrier with arbitrary real spatial amplitude; $\mu/12$ coercivity for invariant quartic modulations; a one-coordinate envelope class; exact resonance-separated packet assembly and its obstructions. | The profile-space identity applies to arbitrary closed two-column profile paths. Exact polynomial circulation cancellation gives a quartic class and $\mu/6$ bound; the finite-difference construction creates nontrivial cancelled loops; a new exact potential covers all finite walks in a specified 81-profile graph. | Moment cancellation is a condition on the test field and is not inherited from arbitrary-gradient approximation. The graph is finite in vertices and widths. The universal profile-space domination and full nine-moment completion remain unavailable. |

The $\mu/6$ and $\mu/12$ constants attach to different admissible families, so this audit does not treat the former as a strict refinement of the latter. N794's integrand $F_\star$ and the graph integrand $G$ are distinct. The internal novelty of the incoming source is the exact profile-circulation cancellation theorem and the finite graph calibration; whether either is historically novel remains UNKNOWN.

## Status, costs, and next gate

The central identities and exact finite checks are internally supported. The supplied verifier passed all nine groups and the standalone example generator completed; all three regenerated JSON results agree with the preserved source outputs after ignoring runtime-only elapsed_seconds fields. The independent checker passed 40 path-moment checks, the large-background and non-preservation examples, and all 32,805 graph inequalities. No formal proof assistant or external referee was used. The source's citations to prior mathematics were not independently re-audited in this investigation; historical novelty therefore remains UNKNOWN.

This is a mathematical proof/search result, with no physical acquisition or material-capability claim. The local environment was Python 3.14.3 and SymPy 1.14.0. Measured wall times were 3.72 s for verify_circulation.py, 1.16 s for check_loop_examples.py, and 15.37 s for independent_checks.py. CPU-energy cost, inference-token cost, and financial cost are unmeasured (null).

The decisive next mathematical gate is either a profile-space potential $P_B$ dominating every compatible strip action for all profiles and velocities, or an exact negative compatible closed walk for a globally rank-one-convex integrand outside the certified classes. Independent analytic and historical review is also still required. Neither the source nor this audit resolves the full planar Morrey problem or establishes priority.
