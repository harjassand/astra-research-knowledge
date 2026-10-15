# Positive frozen-direction ground states and attained weak phase duals

Research date: 15 October 2026. Status: internally reconstructed, unreviewed externally. Historical novelty: UNKNOWN.

## Result and exact remaining barrier

The supplied phase-density work leaves positivity of attained amplitude minimizers and attainment of a scalar dual open. Both can be closed under its explicit coercive hypothesis `mu_F>0` in the planar setting.

For a prescribed smooth direction field, every nonnegative, nonzero fixed-mass amplitude minimizer is strictly positive in the interior. On a torus it is bounded away from zero. The same global lower bound holds on a bounded Lipschitz domain if its continuous boundary amplitude is strictly positive. This includes the target-translated affine boundary data used in the supplied reduction.

For a planar left-SO(2)-invariant quartic, the positive ground state produces an **attained weak flux dual**, with flux in `L^(4/3)` and divergence in `L^1`. No `C^2` ground-state regularity is assumed. The torus formula is

    lambda(theta)
      = max_j ess inf [-div j/4 - f_grad(theta)^*(j)].       (0.1)

For positive fixed boundary amplitude `g`, the fixed-mass value `I_g(M)` is convex and `C^1` on `M>0`. At the optimum, `lambda=I_g'(M)`, and the dual includes the exact weak boundary flux term:

    I_g(M)=lambda M + beta_j(g^4)/4.                       (0.2)

These statements remove a real **frozen-direction** premise. They do not supply the sign needed uniformly over directions or compute the ground state. A decisive limitation is proved below: the unrestricted torus phase infimum at zero affine background equals `0` when periodic Jensen holds and equals `-infinity` if it fails, even when directions are confined to one open half-plane. Asking that this global ground-state problem be bounded below is therefore equivalent to the zero-background Jensen gate, not a weaker sufficient theorem.

The positivity proof uses an actual primary Harnack theorem of **E. DiBenedetto and N. S. Trudinger (1984)** for scalar variational minima. The exact scalar reduction, growth hypotheses, signed-minimum argument, boundary trace, and weak-dual class are supplied here. No claimed complete planar Morrey proof is used. In particular, the automatic `mu_F>0` classification comment in the incoming packet is not a premise; `mu_F>0` remains an explicit input.

## 1. Inputs, pins and scope

Canonical Astra checkout:

    /Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-phase-closure-20261015
    846f185763ed3a27310fad4ce9471ba324d1e5f4

`AGENTS.md` and `00_START_HERE.txt` were read. The supplied `PHASE_DENSITY_COMPATIBILITY.md` and `CHECKPOINT.md` were read in full. This report uses their fixed-direction perspective/Picone identities, reconstructing the decisive steps below. Their numerical searches and interval certificate are not premises here.

OpenAI Math main was refreshed and remains

    1581d4cbdd69a0faf34b2089614fe2a814316a6a.

Its current preprints tree hash is `df0564b2deaab87e07854b6344d8c2f037682e77`, exactly the earlier acquired tree. The unchanged tree was used for selective navigation. New actual proof reading concerns its one-dimensional matrix Lieb-Thirring manuscript, recorded separately. No theorem from that manuscript is imported as a quartic-gradient result.

Throughout, `Omega` is a bounded connected Lipschitz domain in `R^2`, or a connected flat two-torus. The direction `n` is `C^1` on the closure, takes values in `S^(m-1)`, and has bounded derivative. Let

    F:R^(m x 2)->R

be a real homogeneous quartic polynomial, rank-one convex, with

    mu=min{F(R):rank R=1, |R|=1}>0.                       (1.1)

There is no quasiconvexity assumption. The positivity theorem permits any target dimension `m`; the flux formulation later assumes `m=2` and left-SO(2) invariance. The spatial dimension stays two, so `W^(1,4)` embeds in continuous functions on the closure and in `L^infinity`.

Define

    E_n(r)=integral_Omega F(n tensor grad r + r Dn),
    L_n(x,s,z)=F(n(x) tensor z+s Dn(x)).                  (1.2)

For boundary problems take a nonnegative admissible amplitude trace `g`, with a nonnegative `W^(1,4)` extension. For the global boundary dual require additionally `g` continuous and bounded below by a positive constant. The affine case has `g=|Bx+c|>0` after a sufficiently large target translation.

## 2. Scalar growth and mass-value convexity

Changing `z` changes the matrix argument in (1.2) by a rank-one matrix. Thus `L_n(x,s,.)` is convex for every `x,s`. Polynomial growth, (1.1), and Young's inequality give constants `a>0`, `A,b<infinity`, depending on `F,mu,||Dn||_infinity`, such that

    a|z|^4-b|s|^4 <= L_n(x,s,z)
                          <= A|z|^4+b|s|^4.              (2.1)

For completeness, expand the quartic around `n tensor z`. Its leading term is at least `mu |z|^4`. Every remaining monomial is bounded by a constant times `|z|^(4-j)|s Dn|^j`, `1<=j<=4`. Apply Young separately with a total leading loss at most `mu/2`; this gives `a=mu/2` after enlarging `b`. Absolute upper growth follows in the same way. Negative full-rank values of `F` do not invalidate (2.1).

For `M>0` define

    I_g(M)=min {E_n(r): r>=0, trace r=g, integral r^4=M}.   (2.2)

Use the corresponding periodic class on a torus. The minimum exists by the supplied scalar direct-method argument: (2.1) bounds gradients at fixed mass; compact `W^(1,4)->L^4`, scalar convexity in the gradient, and the growth bound preserve the trace/mass and give lower semicontinuity. This does not rely on vectorial quasiconvexity.

The mass domain is all `(0,infinity)` for an admissible nonnegative boundary trace. To obtain arbitrarily small masses, cut off a nonnegative boundary extension in a layer whose width tends to zero. Each such extension is in `W^(1,4)` with the exact trace; its gradient cost may diverge, which is harmless for finite feasibility. Add a nonnegative smooth interior bump with a scalar coefficient to realize every larger mass by continuity. On the torus, constants give every positive mass directly.

The hidden-convex interpolation

    r_t=[(1-t)r_0^4+t r_1^4]^(1/4)

has the same boundary trace and mass `(1-t)M_0+tM_1`. Pointwise rank-one convexity in the normalized gradient, equivalently the perspective in `rho=r^4`, gives

    E_n(r_t)<=(1-t)E_n(r_0)+tE_n(r_1).                   (2.3)

Consequently `I_g` is finite and convex on `(0,infinity)`. The lower bound `I_g(M)>=-bM` follows from (2.1); fixed feasible amplitudes give finite upper values.

Fix a minimizer `r` at mass `M` and select a finite supporting slope

    lambda in partial I_g(M).

For any nonnegative competitor `v` with the same trace,

    E_n(v)-lambda integral v^4
       >= I_g(M)-lambda M.                               (2.4)

Thus `r` is a global unconstrained minimizer of the shifted scalar functional, with the original boundary trace. This is stronger than merely writing a formal Lagrange multiplier equation.

If `g` is identically zero, the zero competitor has mass zero. Scaling preserves the zero trace, so `I_0(M)=M I_0(1)` and (2.4) extends to that competitor as well. For nonzero boundary trace, every competitor has positive mass.

On a torus, homogeneity gives `I(M)=M lambda_n`, where

    lambda_n=min_(integral r^4=1) E_n(r).                 (2.5)

There the same argument is immediate from the Rayleigh quotient, whether `lambda_n` is positive, zero or negative.

## 3. Signed minimum and the primary Harnack theorem

The obstacle `r>=0` does not block signed scalar variations. A real homogeneous quartic is even under total matrix negation. The Sobolev chain rule gives

    D(|v|n)=sign(v)D(vn) almost everywhere on {v!=0},

and the gradients vanish in the needed scalar sense on `{v=0}`. Hence

    E_n(|v|)=E_n(v),      integral |v|^4=integral v^4.     (3.1)

If `trace v=g>=0`, then `trace |v|=g`. Applying (2.4) to `|v|` proves that the nonnegative minimizer is an actual minimum among all real scalar competitors with that trace. It is therefore a local `Q=1` minimum under compactly supported variations of

    J_lambda(v)=integral [L_n(x,v,grad v)-lambda |v|^4].   (3.2)

Divide its integrand by `a` from (2.1). The resulting Caratheodory integrand satisfies exactly the primary theorem's structure

    |z|^4-b_lambda |s|^4
       <= f(x,s,z) <= C |z|^4+b_lambda |s|^4,            (3.3)

where `b_lambda` is bounded and the additive forcing term is **zero**. The coefficient condition of the primary theorem is satisfied: for `p=4` greater than the spatial dimension two, its bounded lower-order coefficient is admissible.

DiBenedetto-Trudinger, *Harnack inequalities for quasi-minima of variational integrals*, Ann. IHP Anal. Non Lineaire 1(4) (1984), 295-308, Section 4, structure (4.2), Lemma 4.1 and Corollary 3, now applies. Its proof passes variational minima into a De Giorgi class by truncation, then uses the Harnack estimates. When the additive forcing is zero, Corollary 3 gives the homogeneous estimate

    sup_(B_sigma R) r <= C inf_(B_sigma R) r.              (3.4)

The scanned hypotheses, treatment of exponent at least the dimension, and homogeneous conclusion were visually inspected on printed pages 305-307. The source authors are DiBenedetto and Trudinger; Giaquinta-Giusti are cited predecessors, not the authors of this Harnack theorem.

Since the mass is positive, `r` is not identically zero. Harnack and connectedness imply

    r>0 everywhere in the interior,
    inf_K r>0 for every compact K inside Omega.            (3.5)

Here one may use the continuous representative supplied by planar `W^(1,4)`. On a torus, compactness upgrades (3.5) to `min r>0`. If `g>=g0>0` on the boundary, continuity on the compact closure gives `min_closure r>0` as well: otherwise a minimum zero would occur either in the interior, contradicting (3.5), or on the positive boundary.

This does not claim `r` is smooth, nor a uniform lower bound independent of the direction. Harnack constants depend on the coefficient bounds, including `||Dn||` and `lambda`.

### The positive rank-one bound is necessary to this theorem

One cannot drop (1.1). Let `F(A)=|A e_1|^4`, which is convex, and fix `n=e_1` on a two-torus. Every normalized nonnegative amplitude `r(y)` has energy zero, including smooth amplitudes vanishing on an open band. They are minimizers but are not strictly positive and are not unique. This integrand has `mu=0`. Thus any extension of positivity across degenerate rank-one faces needs a separate argument.

## 4. The mass value is C1 and positive amplitude minimizers are unique

Because `r` minimizes the differentiable polynomial functional (3.2) among all real scalar variations, it satisfies the weak Euler equation

    integral [partial_z L_n(x,r,grad r).grad psi
                   +partial_s L_n(x,r,grad r) psi]
       =4lambda integral r^3 psi                          (4.1)

for every admissible zero-boundary or periodic `W^(1,4)` test.

If two different supporting slopes `lambda_1,lambda_2` existed for the same mass value, the same minimizer would satisfy (4.1) for both. Subtraction gives

    (lambda_1-lambda_2) integral r^3 psi=0

for all compactly supported smooth `psi`. Since `r` is nonzero in the interior, some such integral is nonzero. Hence the supporting slope is unique. A finite convex function on an open interval with a unique supporting slope everywhere is differentiable; its derivative is continuous. Therefore

    I_g in C^1((0,infinity)),      lambda=I_g'(M).          (4.2)

There is also uniqueness of the nonnegative mass minimizer. On the torus, or when the reference is bounded below up to the boundary, the supplied Picone identity extends to the positive `W^(1,4)` reference by the Sobolev chain rule. For any other real amplitude `s` of the same mass and boundary trace,

    E_n(s)-E_n(r)
      >= (mu/3) integral r^4 |grad(s/r)|^4.               (4.3)

For the boundary case, the correct zero-trace test in (4.1) is `s^4/r^3-r`; its boundary value is zero because both amplitudes equal `g`. For the torus it is periodic. The mass terms cancel. All products are legal: `r,s` are bounded, `r` has a positive lower bound, and `DF(D(rn))` belongs to `L^(4/3)`.

If both amplitudes minimize, (4.3) forces `s/r` constant. Connectedness and nonnegativity, followed by mass normalization, give `s=r`. This proof claims uniqueness in the nonnegative amplitude class; the signed periodic problem also admits the total sign reversal.

For boundary traces vanishing somewhere, interior positivity remains proved, and a localized/regularized Picone argument may yield further uniqueness. The global lower-bound and dual statements below deliberately use the torus or strictly positive boundary data, where no singular division near the boundary occurs.

## 5. Attained torus flux dual with a nonsmooth positive ground state

Now take `m=2` and left-SO(2)-invariant `F`. Write locally

    n=(cos theta,sin theta),  k_i=(Jn).partial_i n.

The globally defined vector field `k` is continuous and closed in distributions, with possible winding periods; it is smooth when `n` is smooth. No global periodic real lift of `theta` is required. Set

    f_k(a)=F([[a_1,a_2],[k_1,k_2]]).

At fixed `k`, this is a convex quartic function of `a`, since its row differences are rank one. The ground state representation is

    E_n(r)=integral r^4 f_k(grad r/r).                    (5.1)

Let `r` be the positive normalized torus minimizer. Define

    a=grad r/r,       j=partial_a f_k(a).                 (5.2)

Since `r` is bounded above and below, `a in L^4`, and quartic polynomial growth gives `j in L^(4/3)`. Put `f_k^*(j)=sup_a(j.a-f_k(a))`. Convexity and differentiability give the pointwise Fenchel equality

    f_k^*(j)=a.j-f_k(a) in L^1.                           (5.3)

The radial scalar Euler equation (4.1) becomes

    -div(r^3 j)+r^3(4f_k(a)-a.j)=4lambda_n r^3.          (5.4)

To divide safely in the weak equation, use `psi=eta/r^3` for smooth periodic `eta`. This is a legal `W^(1,4)` test because `r>=c>0`. Product differentiation gives

    div j=4[f_k(a)-a.j-lambda_n] in L^1,
    -div j/4-f_k^*(j)=lambda_n almost everywhere.         (5.5)

This is a nonlinear logarithmic-gradient, or Riccati-type, ground-state identity. It is proved in distributions and then identified with an `L^1` function; no classical second derivative of `r` has been asserted.

Define the weak dual class

    D={j in L^(4/3)(T^2;R^2): div j in L^1(T^2)}.         (5.6)

Polynomial coercivity of `f_k` gives `f_k^*(j) in L^1` for every `j in D`. For any such flux, Fenchel's inequality and integration by parts yield, for every normalized real `s in W^(1,4)`,

    E_n(s)>=integral [-div j/4-f_k^*(j)]s^4
             >=ess inf[-div j/4-f_k^*(j)].                (5.7)

The weak integration by parts is justified by smooth approximation of `s^4` in `W^(1,4)` **and uniformly**. Planar Morrey embedding supplies uniform convergence, so the `L^1` divergence can be paired with these approximants. It would be insufficient to assume merely weak convergence of a density.

Taking the primal infimum in (5.7) proves weak duality. The flux in (5.2) has constant residual by (5.5), so it attains equality:

    lambda_n=max_(j in D) ess inf[-div j/4-f_k^*(j)].       (5.8)

Thus frozen-phase duality and weak dual attainment are proved. Smooth-flux attainment is not claimed. Mollification generally gives only `L^1` residual control, which does not control the essential infimum against arbitrary concentrating amplitudes.

## 6. Exact boundary dual and weak normal trace

Let `Omega` be bounded connected Lipschitz, let `g>=g0>0`, and retain a fixed prescribed smooth direction. Let `r` be its mass-`M` minimizer and `lambda=I_g'(M)`. The same construction gives a global flux

    j in L^(4/3)(Omega;R^2),      div j in L^1(Omega),
    R_j:=-div j/4-f_k^*(j)=lambda almost everywhere.       (6.1)

The boundary contribution must not be discarded or replaced by a classical pointwise normal derivative. For a density trace `h`, define its weak normal trace pairing by

    beta_j(h)=integral_Omega [j.grad H+(div j)H],          (6.2)

where `H in W^(1,4)(Omega)` is any bounded extension of `h`. For the application `h=g^4`, such an extension exists. The quantity is independent of the extension: the difference has zero trace, can be approximated by compactly supported smooth functions in `W^(1,4)` and uniformly, and the defining distributional divergence identity applies. A fixed bounded trace extension and Morrey embedding bound this pairing continuously in the relevant trace norm. When `j` is smooth, (6.2) is exactly `integral_boundary h j.nu`.

For any admissible nonnegative density `rho=s^4` with trace `g^4` and mass `M`, Fenchel and (6.2) give

    E_n(s)>=integral R_j rho+beta_j(g^4)/4.               (6.3)

In particular, for any `j in D` and real `ell` with `R_j>=ell` almost everywhere,

    I_g(M)>=ell M+beta_j(g^4)/4.                          (6.4)

At the ground-state flux, pointwise Fenchel equality and (6.1) give exact equality. Therefore

    I_g(M)=max_(j,ell: R_j>=ell)
                      [ell M+beta_j(g^4)/4],              (6.5)
    I_g(M)-M I_g'(M)=beta_j(g^4)/4.                        (6.6)

All fluxes in (6.5) belong to `L^(4/3)` with `L^1` divergence; the admissible class and boundary pairing are explicit. The attained flux is acquired from a ground state, not from a solved algorithm. The sign of (6.5) relative to `|Omega|F(B)` is still unknown for arbitrary directions with affine boundary data.

### Why zero boundary cannot be silently included in the global flux class

A positive interior ground state can tend to zero at the boundary. Its logarithmic gradient may then behave like the reciprocal distance, and its cubic flux need not lie globally in `L^(4/3)`. Interior positivity is enough for local weak ground-state identities, but not for the unweighted global class (5.6)/(6.5). A weighted or singular-flux formulation would be an additional theorem. The target-translated affine application avoids this issue because its boundary amplitude is strictly positive.

## 7. A decisive global phase barrier

Use normalized torus integration, and define

    Lambda(F)=inf_(smooth n:T^2->S^(m-1))
                     min_(r>=0, integral r^4=1) E_n(r).   (7.1)

It is enough to restrict `n` to a fixed open hemisphere. In the planar case this means phases with a global real lift and no winding. Constants show `Lambda(F)<=0`.

There is an exact dichotomy:

    Lambda(F)=0          if integral F(Du)>=0 for every periodic u,
    Lambda(F)=-infinity  if some periodic u has negative energy. (7.2)

Proof. If periodic Jensen at zero holds, each map `rn` is an actual periodic Sobolev map. Smooth density and quartic growth extend the inequality to it, so every scalar amplitude value is nonnegative. Constant directions and amplitudes attain zero.

Conversely let a smooth periodic `u` have negative energy. Translate its target by a sufficiently large constant `c` so `u+c` stays in the fixed open half-space and never vanishes. This changes no gradient. Let

    v_N(x)=u(Nx)+c,
    r_N=|v_N|,   n_N=v_N/|v_N|,
    M=integral |u+c|^4.

For each integer `N`, normalized torus averaging gives the same mass `M`, while homogeneous quartic scaling gives

    integral F(Dv_N)=N^4 integral F(Du).

The normalized amplitude `M^(-1/4)r_N` is an admissible competitor for the smooth hemispherical direction `n_N`; hence

    lambda(n_N)<=N^4 integral F(Du)/M -> -infinity.

Every nonsmooth strict negative Sobolev test can first be smoothed, so no negative test is lost by the smooth formulation. This proves (7.2).

The dichotomy concerns zero-background periodic Jensen. No equivalence with the full all-background quasiconvexity problem is asserted. It already shows why a finite global phase ground-state existence theorem is not an independent shortcut: it would discharge that remaining sign theorem itself. Fixed-direction Harnack and weak dual attainment do not supply the needed uniform sign.

An explicit derivative/regularity budget for directions changes the optimization class and can restore coercive lower bounds. Such a supplied budget would be a restricted theorem, and is not available uniformly for all compatible tests. In the counterfactual negative construction above, `||Dn_N||` grows with `N`.

## 8. Exact finite checks and a simple dual sanity test

For the source energy

    G(A)=3(u+v-2q)^2+(35/24)u^2+q^2-(5/2)qu,

take the constant phase gradient `k=(0,1)`. At `a=0`, direct differentiation gives

    f_k(0)=3,       partial_a f_k(0)=(-12,0).

The constant flux `j=(-12,0)` is an exact supporting slope, so `f_k^*(j)=-3`, and its dual residual is `3`. The constant amplitude attains energy `3`; hence the frozen-direction value is exactly `3`. This is a small exact test of the factors and sign in the new dual formula, not a new general phase theorem. The source's coupled phase has a distinct certified bracket and is not substituted for this test.

`verify_external_duality.py` checks all 35 degree-four monomials for the scalar Euler/flux algebra, the weak residual factor, the exact constant-phase example, the terminal-weight toy and the global scaling exponents. It also pins the current checkout and records primary-source hashes. These are finite identities; Harnack, compactness, trace pairing and strong duality are analytic proofs supplied above, not formalized by the script.

## 9. Precise Pedregal proof obligation

The actual arXiv:1905.06571v4 Proposition 6.1 proof, including Step 2, was read. Its positivity-feasible set is shown to contain a neighborhood; the text then infers that full linear span makes that set the entire gradient space. No subspace property of the positivity-feasible set is established by that inference. This report identifies a missing lemma in the displayed argument. It does not give a counterexample to the proposition or claim the full theorem is false.

A sharper model of the exact obstruction than a bounded interval is the following. Let a prescribed interface have black point `m=0` and endpoint displacements `alpha=s`, `beta=t`, linear in two parameters. A nonnegative convex decomposition exists exactly when

    s t<=0.

This feasible set contains a neighborhood of `(1,-1)`, spans `R^2`, and is invariant under every real scalar dilation. Nevertheless `(1,1)` is infeasible. Thus even homogeneity and a full-rank linear construction do not repair the implication.

For each actual interface in the source's construction one must show that its two terminal endpoints straddle its intermediate point. Once collinearity is known, this is the condition

    alpha_e(S) beta_e(S)<=0,                              (9.1)

with the displacements determined by the actual compatible parameterization. If its claimed reduction is a linear isomorphism onto all target gradients, (9.1) must hold on that entire parameter space, not only near the original supplied function. If there is a kernel or an affine restriction, the corresponding quantified feasibility problem must instead be retained explicitly.

There is a useful exact characterization in the homogeneous linear case. For linear functionals `alpha,beta` on a real vector space,

    alpha(S) beta(S)<=0 for every S

holds if and only if one is identically zero or `beta=-c alpha` with `c>=0`. To prove necessity, if neither is zero, any vector in `ker alpha` must lie in `ker beta`; otherwise adding a large multiple of it to a vector with `alpha!=0` makes the product positive. Therefore the two functionals are proportional, and the sign forces a nonpositive multiplier. Sufficiency is immediate.

Equivalently, the symmetric rank-at-most-two quadratic matrix `(a b^T+b a^T)/2` must be negative semidefinite on the compatible parameter subspace. This gives a concrete finite algebraic obligation for the claimed global straddling step. It is not checked here for an unsupplied full source parameter matrix, and it would still not by itself verify the later global weight/marginal requirements. The complete Morrey claim is consequently not imported.

## 10. Actual external machinery and historical scope

The strongest applicable primary theorem was the scalar variational Harnack result, whose exact growth hypotheses were discharged rather than borrowed by terminology. Brasco-Franzina's established hidden-convexity/Picone treatment explains the eigenfunction uniqueness mechanism, but its stated nonnegative convex scalar gradient integrand is not directly the signed vectorial energy here; the rank-one frozen-direction reduction supplies that interface.

OpenAI Math's inspected matrix Lieb-Thirring source contains an actual positive scalar logarithmic derivative and factorization in its sharpness proof, as well as a matrix-field primitive constructed by trace differentiation and a quantitative tail estimate. These are concrete comparators for ground-state factorization and global exactness. Their one-dimensional quadratic spectral assumptions do not supply an all-direction planar quartic sign. No full Lieb-Thirring theorem or matrix trace estimate is used as a premise here.

The result is an internal closure of frozen-phase positivity and weak dual attainment, with a sharply retained global sign gate. It uses the established ground-state and Picone principles described above; historical priority of this exact vectorial application is UNKNOWN. No physical capability, numerical complexity bound, full nine-coefficient theorem, or external mathematical review is established.
