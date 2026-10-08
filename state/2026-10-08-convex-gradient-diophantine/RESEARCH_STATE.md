# Diophantine clock arrest in strongly convex polynomial gradient flows

**Date:** 2026-10-08 (Australia/Brisbane). **Research state:** exact self-contained reductions, not externally peer-reviewed; historical priority not established. **Base repository revision:** `b5824d0fcbfe0688980788da2722270a2f068fb0`. **No subagents.** This is NOT a new resolution of Hilbert's tenth problem, not a field-breaking theorem, and not a mass-action chemical reaction network realization.

## Motivation and discovery boundary

The earlier Astra reversible-explosion construction [draft PR #3] quantifies finite-window observational indistinguishability but does not carry a known deep open-problem resolution. A different cross-domain opening uses the Diophantine integer unsolvability theorem (Davis-Putnam-Robinson-Matiyasevich) and, *conditionally*, the September/October 2026 OpenAI preprint claiming undecidability of rational solvability. The correct separation is between **dynamical stability / real equilibrium existence** and **arithmetic exactness of an equilibrium**.

Primary inputs:
- Classical DPRM / H10(Z): see B. Poonen, *Undecidability in number theory*, Notices AMS, https://math.berkeley.edu/~poonen/papers/h10_notices.pdf.
- Claimed H10(Q) negative answer (NOT independently validated here): OpenAI, *Hilbert's tenth problem over the rational numbers*, Sept. 24 2026, https://github.com/openai/math/tree/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026.
- Classical Skolem degree reduction through arithmetic gates and sums of squares is PRIOR ART, not a new mathematical technique. The exact special dynamical restriction below is a constructed corollary; no historical novelty claim.

## Theorem I (unconditional, integer equilibrium)

There is an effective transformation sending each integer polynomial `p(t_1,...,t_n)` to a polynomial vector field on `R_{>0}^D`, `D` finite and computed from an arithmetic circuit for `p`, of the form

    xdot = -M(x) grad V(x),

such that:

1. `V` is an explicitly given rational-coefficient polynomial of total degree **3**, and its Hessian is >= identity on the entire positive orthant. In particular V is uniformly strongly convex, coercive on the positive orthant, and has an explicitly known unique positive global minimizer `r` with one irrational coordinate.
2. `M` is an explicitly given integer-coefficient sum-of-squares polynomial of total degree **at most 4**, and `M>=0` for all real x. Thus the vector field has total degree **at most 6**.
3. Every positive solution exists for every forward time, has every coordinate monotone, remains in a compact rectangular subset of the positive orthant depending only on its initial point, and converges to an equilibrium. In particular there are no nonconstant periodic orbits.
4. The vector field has a strictly positive **integer-coordinate** equilibrium if and only if `p` has an integer zero.

Consequently, by DPRM, there is no algorithm to decide whether an input vector field promised to arise from this explicitly specified class has a strictly positive integer equilibrium.

### Proof of Theorem I

Compute a finite straight-line arithmetic circuit for p with constant, input, addition and multiplication gates. For every gate g introduce **positive real variables** `a_g,b_g`, representing the signed gate value `q_g=a_g-b_g`. For input gates impose no residual. For constant gates impose `R_g=(a_g-b_g)-c_g`. For an addition gate `g=i+j`, impose `R_g=(a_g-b_g)-(a_i-b_i)-(a_j-b_j)`. For a multiplication gate `g=i*j`, impose `R_g=(a_g-b_g)-(a_i-b_i)(a_j-b_j)`. Also impose `R_{out}=a_{output}-b_{output}`. Every residual has degree <=2. Define

    M(a,b)=sum_g R_g(a,b)^2 + R_out(a,b)^2.

Then deg M<=4. Over integer-coordinate points, M=0 iff the original arithmetic circuit computes zero on integer inputs. Every signed integer q has a representation q=a-b with a,b positive integers; this construction extends to all intermediate gates. Hence p has an integer zero iff M has a positive-integer zero.

Add one new coordinate `z>0`, and put

    V(z,a,b) = z^3/3 + z^2/2 - z + (1/2) sum_g [(a_g-1)^2 + (b_g-1)^2].

Its gradient is `(z^2+z-1, a_g-1, b_g-1)`; its Hessian is diagonal with entries `1+2z` and `1`. The unique positive minimizer is

    r=(z_*,1,...,1),   z_*=(sqrt(5)-1)/2,

which does not have integer (or rational) coordinates. Let `xdot=-M grad V`. A stationary point satisfies `M=0` or `grad V=0`. At a positive-integer point the latter is impossible because `z_*` is irrational. This establishes equivalence and undecidability.

Each a and b coordinate obeys `dot y=M(1-y)`; z obeys `dot z=M(1-z-z^2)`. As M>=0, each coordinate is monotone toward the fixed target 1 or z_* and never crosses it. Its trajectory stays between its initial coordinate and its target, proving positivity, boundedness, global existence, and coordinatewise convergence. By continuity and autonomy, a convergent orbit's limit has zero vector field (otherwise some coordinate derivative would stay bounded away from zero), hence is an equilibrium. Finally `dot V=-M||grad V||^2 <=0`. QED.

## Theorem II (conditional on undecidability of H10(Q), rational equilibrium)

If there is no algorithm deciding whether an arbitrary integer-coefficient polynomial in an arbitrary number of variables has a zero over Q, then even the following *promised* decision problem is undecidable:

> Given a rational-coefficient polynomial vector field on an open unit cube `(0,1)^D` of the form `xdot=-M grad V`, with `V` uniformly strongly convex of degree <=3, and `M` a nonnegative sum of squares of degree <=6, determine whether it possesses a **strictly interior rational-coordinate equilibrium**.

The vector field has degree <=8. Every interior trajectory remains in a compact subcube, has monotone coordinates and converges to an equilibrium. Every instance has the **known explicitly given real equilibrium** `r=((sqrt(5)-1)/2,1/2,...,1/2)` even if it has no rational equilibrium.

### Proof of Theorem II

For each arithmetic circuit gate g replace the signed value `q_g` by **three** coordinates `(u_g,v_g,w_g)` in (0,1), interpreted as

    q_g = (u_g-v_g)/w_g.

Any q in Q can be represented this way with rational coordinates strictly in (0,1): take a small positive rational w with |q|w<1, then u=(1+qw)/2, v=(1-qw)/2. For input gates impose no residual. For each constant gate g=c impose `R_g=(u_g-v_g)-c w_g` (degree 1). For an addition gate g=i+j impose

    R_g=(u_g-v_g) w_i w_j
        -w_g [(u_i-v_i) w_j+(u_j-v_j) w_i]     (degree <=3).

For a multiplication gate g=i*j impose

    R_g=(u_g-v_g) w_i w_j - w_g (u_i-v_i)(u_j-v_j)   (degree <=3).

Impose `R_out=u_output-v_output`. Let `M=sum_g R_g^2+R_out^2`, degree <=6, nonnegative on all real inputs. All w are strictly positive inside the promised cube, so `M=0` at a rational cube point iff all rational gate equations hold and p has a rational zero.

Add z in (0,1) and define

    V(z,u,v,w)= z^3/3+z^2/2-z
                 +sum_g[(u_g-1/2)^2+(v_g-1/2)^2+(w_g-1/2)^2].

The Hessian is diagonal, with z-entry `1+2z>=1` and all other entries 2; its minimizer r has irrational z. The same stationary-point equivalence and monotonicity proof as in Theorem I applies, with all other coordinates moving toward 1/2. Degree of the vector field is <=8. This completes the Turing reduction **conditional on H10(Q)**. The external H10(Q) premise is not verified by this document.

## Exact dynamical interpretation (both theorems)

Set the nonnegative scalar clock `A(t)=integral_0^t M(x(s)) ds`. The solution follows the **one fixed strictly convex gradient trajectory** of `dx/dA=-grad V(x)`; M changes only how fast this trajectory is traversed. For y-coordinates, the clock trajectories are explicit:

- Theorem I: `y(A)=1+(y(0)-1)e^{-A}`.
- Theorem II: `y(A)=1/2+(y(0)-1/2)e^{-2A}`.

The z-clock trajectory solves the scalar Riccati equation `dz/dA=1-z-z^2` and is monotone toward `z_*`. If A(infinity)<infinity, continuity forces M to vanish at the limiting state. If A(infinity)=infinity, the orbit converges to the unique irrational minimizer r. Thus every orbit either asymptotically arrests at a zero-mobility state or reaches the same convex-potential minimizer. There is no chaotic, oscillatory or recurrent computational simulation hidden in the flow: all undecidability concerns exact arithmetic membership of stationary configurations.

## Independent counterexample / attempted falsification

One MUST NOT infer a weakly reversible or mass-action CRN from the SOS mobility. Nonnegative values of M do not ensure the monomial sign restrictions of kinetic polynomials. For example, `dot C=(X-Y)^2(1-C)` has nonnegative production at `C=0`, but its expansion contains the negative source coefficient `-2XY` in the C-equation with **zero C in the reactant monomial**. Any ordinary mass-action reaction decreasing C must consume at least one C, so this vector field is not an ordinary mass-action kinetic realization without additional variables/changes. The earlier tentative reversible-CRN/H10 composition **is not proved**. More strongly, guaranteed real equilibria and common permanence do not imply rational-point preservation under auxiliary-species embeddings.

Regularity boundary: replacing `M` by `M+epsilon` with any epsilon>0 removes *all* extraneous stationary points and leaves only the unique convex minimum r. The arithmetic hardness is concentrated in the **degenerate zero-mobility set**, not in the convex energy landscape. Robust-tolerance, physical-rate and integer-output questions are separate.

## Verification and literature status

Sympy exact polynomial expansion independently confirms a representative integer arithmetic-product gate has M degree 4 and vector-field degree 6; a rational addition/multiplication gate has residual degree 3, M degree 6, vector field degree 8. An exact Fraction(2/3), Fraction(-5/7) addition gate replay gives output -1/21 and precisely zero residual. The attached standard-library verifier further checks randomized exact circuits, sample witnesses, and coordinatewise monotonicity.

- Historically settled: H10(Z)/DPRM and Skolem's arithmetic-gate reduction.
- Conditional and source-dependent: H10(Q) is stated as resolved by OpenAI Sept 2026. No independent expert correctness/priority certification here.
- Newly assembled in this investigation: explicit **uniformly strongly convex SOS-clock dynamical normal form**, fixed degree bounds, bounded monotone convergence theorem, rational cube encoding and the kinetic-realizability warning. Historical novelty not established; the reduction may be viewed as a standard corollary.
- This is not comparable in verified significance to a major new open-problem resolution and does not imply an executable universal physical computer or an undecidable finite-precision experiment.

## Continuation / highest-value open gates

1. Seek a genuine **reversible mass-action** arithmetic-preserving encoding. This requires a constructive, rational-point-preserving realization theorem; the existing Boros-Craciun-Yu (2020) reversible positive-equilibrium continuum example does not automatically supply one: https://arxiv.org/abs/1912.10302.
2. Seek a structurally restricted perturbation-robust variant; adding any strictly positive mobility floor collapses the extra-equilibria mechanism, so the present proof cannot prove robustness.
3. Audit prior work in computable dynamics / SOS stationary point decision problems before any originality claim. Source-check the H10(Q) premise independently; do not silently promote a GitHub preprint into independently verified mathematics.
4. Test whether a *fixed observable or fixed rational initial condition* encodes unsolvability; the current result is an existential equilibrium decision problem with dimension growing with the input, NOT a trajectory-observation undecidability theorem.

**Do not merge or publish as a field-breaking result absent substantive new mathematics, specialist review and a priority clearance.**
