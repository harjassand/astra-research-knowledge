# Separate independent review: W1,4 fixed-direction extension

15 October 2026. This is an append-only extension to the frozen adversarial review. The previous proof files and manifest remain unchanged. Internal analytic reconstruction only; external correctness and historical originality are UNKNOWN.

Actual source reviewed in full: `workers/external_duality/ROUGH_DIRECTION_EXTENSION.md`. Its smooth-direction core remains a separate source. Repository pin: `846f185763ed3a27310fad4ce9471ba324d1e5f4`.

## 1. Disposition and exact scope

The rough-direction extension survives independent reconstruction. Let Omega be a bounded connected Lipschitz planar domain, or a connected flat two-torus. Let F be a real homogeneous quartic polynomial, rank-one convex, with strictly positive minimum mu on unit rank-one matrices. Fix `n in W1,4(Omega;S^(m-1))`, with the periodic counterpart. No essential bound on Dn is required.

At fixed positive fourth mass and admissible nonnegative amplitude trace, the minimum is attained and its nonnegative minimizer is strictly positive in the interior. The minimizer is unique even when the boundary amplitude can vanish; Section 7 below gives this slight strengthening of the producer's conservative uniqueness statement. On the torus, or with a continuous strictly positive boundary amplitude, its global positive lower bound permits exact weak-flux dual attainment. There is no smooth optimal-flux or computational acquisition conclusion.

The quantitative `K^8+K^4` coercivity bound below is planar. The analytic positivity/attainment proof also extends to spatial dimension d<4 with the corresponding Sobolev constants and changed GN powers; no critical-dimensional statement is inferred.

## 2. Product and density domains are legal

In dimension below four, Sobolev extension and Morrey give `W1,4 -> L-infinity`, and compact embedding into continuous functions. Thus `u=rn` is an actual Sobolev map and

    Du=n tensor grad r+r Dn in L4.

The unit constraint makes `|n|=1` everywhere for the continuous representative, not merely almost everywhere. The amplitude-to-gradient map is bounded linear from W1,4 to L4, with operator norm depending on the fixed direction's L4 derivative norm. A quartic polynomial energy is therefore Frechet differentiable on the amplitude space.

For nonnegative amplitudes, the fourth-root interpolation is a Lipschitz composition of the two amplitudes. It preserves the Sobolev class, the fixed density trace and the affine fourth-mass constraint. All perspective inequalities hold pointwise almost everywhere at weak differentiability points; Dn being merely measurable L4 does not affect rank-one convexity of the scalar gradient slice. At common zeros the Sobolev gradients vanish almost everywhere. No false unqualified Sobolev space for the density is needed; in this subcritical dimension each amplitude's fourth power itself is W1,4 because the amplitude is bounded.

## 3. Critical-weight coercivity, including nonzero boundary data

Pointwise quartic expansion about `n tensor z`, its positive rank-one value and Young's inequality give constants determined by F and mu such that

    L(x,r,z)=F(n tensor z+rDn)
      >=(mu/2)|z|^4-C|Dn|^4 r^4.                         (1)

The potentially negative coefficient `|Dn|^4` is only L1. Treating it as a bounded potential would be invalid. It is instead controlled by the planar GN estimate

    ||r||_infinity^4<=C_Omega(X^2 M^(1/2)+M),
    X=||grad r||_4, M=||r||_4^4.

The additional M term is essential on a torus and for unrestricted nonzero boundary values. A zero-boundary Poincare estimate cannot be substituted here.

One direct derivation uses whole-plane local averages and Morrey:

    |v(x)|<=C(R^(-1/2)||v||_4+R^(1/2)||grad v||_4).

Optimizing R gives the product estimate. A Lipschitz-domain extension bounded in L4 and with derivative norm controlled by `||grad r||_4+||r||_4` adds the lower-order M term. A cutoff of a finite periodic extension gives the torus version. Thus the constants depend on the fixed domain; positive boundary data introduce no invalid step.

Set `B=||Dn||_4^4=K^4`. Integrating (1) gives

    E(r)>=(mu/2)X^4-CB(X^2 M^(1/2)+M).

Writing `q=CB`, the relevant exact square completion is

    (mu/2)X^4-q X^2 sqrt(M)
      =(mu/4)X^4+(mu/4)(X^2-2q sqrt(M)/mu)^2-q^2 M/mu.

Consequently

    E(r)>=(mu/4)X^4-C'(B^2+B)M
         =(mu/4)X^4-C'(K^8+K^4)M.                       (2)

This proves fixed-mass coercivity without a hidden Dn-infinity norm. A fixed-direction L1-tail split also proves a nonuniform form bound, but the GN argument explicitly retains a norm-budget bound. In dimension d<4 the analogous exponent on B is `4/(4-d)`; the displayed eighth-power K dependence is specific to d=2.

## 4. Attainment and mass multipliers

Coercivity (2) bounds a minimizing sequence in W1,4. A subsequence converges weakly there and uniformly in amplitude. Hence `(r_j-r)Dn ->0` strongly in L4. The quartic difference estimate permits replacing the lower field `r_j Dn` by `r Dn` in the energies with an error tending to zero.

With that lower field fixed, the energy is a finite continuous convex functional of the scalar gradient in L4: its matrix increments are rank one. Such a functional is weakly lower semicontinuous. This is a valid scalar convexity argument; weak continuity of a general vectorial quartic is not being assumed. Nonnegativity, trace and mass pass to the limit.

Evenness still removes the amplitude obstacle: `E(|v|)=E(v)` by the Sobolev chain rule and total-gradient sign symmetry. The mass derivative is nonzero on the zero-trace variation space for a nontrivial amplitude, so the signed constrained Euler equation has a finite multiplier.

The producer's additional C1 mass-value assertion also checks. Every positive mass is feasible: retain an admissible nonnegative boundary lift only in a sufficiently thin boundary layer to make its mass arbitrarily small, then add a nonnegative compact interior bump to attain the desired mass continuously. Every finite layer has finite Sobolev energy; no uniform energy bound while shrinking the layer is claimed. Constants cover all torus masses.

The resulting finite mass value is convex on `(0,infinity)` by density interpolation, so a supporting slope exists. It makes the constrained minimizer a global signed minimum of energy minus that slope times fourth mass. If two supporting slopes existed, their Euler equations at the same nonzero minimizer would imply their difference times `r^3` vanishes as a distribution, forcing equal slopes. Thus the finite convex mass value is differentiable everywhere, and its monotone derivative is continuous. The zero-mass competitor in the zero-boundary case is consistent with this argument by quartic scaling.

For nonzero boundary, none of this permits `lambda=E/M`; the boundary contribution remains present.

## 5. The logarithmic estimate retains all rough lower terms

Put `z=grad r`, `A=L_z` and `C=L_r`. Convexity and quartic growth give

    A.z>=c|z|^4-C0 r^4|Dn|^4,
    |A|<=C0(|z|^3+r^3|Dn|^3),
    |C|<=C0|Dn|(|z|^3+r^3|Dn|^3).

Here C is in L1, which suffices because Sobolev tests are bounded. It need not lie in L^(4/3). The derivative is nevertheless continuous as a functional on W1,4, by the bounded product map from Section 2.

For each epsilon>0, the compactly supported test `eta^4/(r+epsilon)^3` is legal in the weak Euler equation. Every term is finite for that fixed epsilon. Put `G=|grad r|/(r+epsilon)`. The two lower-order terms that would be lost by pretending Dn bounded are

    eta^3 |grad eta| |Dn|^3,
    eta^4 |Dn| G^3.

Young's inequality controls them by `C(|grad eta|^4+eta^4|Dn|^4)` plus an absorbable fraction of `eta^4G^4`. The remaining cutoff, potential and multiplier terms are controlled in the same way. Thus

    integral eta^4 |grad log(r+epsilon)|^4
       <=C integral (|grad eta|^4+eta^4|Dn|^4
                                          +|lambda|eta^4). (3)

The right side is finite and independent of epsilon. No derivative of Dn occurs.

Morrey-Poincare on a compact interior ball bounds the oscillation of `log(r+epsilon)` uniformly. A zero and a positive value on one ball would contradict that bound as epsilon tends to zero. Connectedness and positive mass therefore exclude every interior zero. This supplies local Harnack control with constants depending on local L4 direction-gradient information and the multiplier, not a uniform direction-independent positive minimum.

## 6. Rough unit-direction representation and weak boundary dual

For `m=2`, continuity of the S1-valued direction supplies local real phase lifts on small neighborhoods. The globally defined one-form

    k_i=(Jn).partial_i n in L4

equals the local phase gradient. It need not be the gradient of one globally periodic real phase: winding is allowed. The product formula and pointwise output rotation require no global phase choice.

More generally use `f_x(a)=F(Dn+n tensor a)` directly. Its conjugate obeys

    |f_x^*(j)|<=C(|j|^(4/3)+|Dn|^4),

up to harmless fixed constants, so it is integrable for any `j in L^(4/3)`. When the minimizer is globally bounded below, `a=grad log r in L4` and `j*=partial_a f_x(a) in L^(4/3)`. Dividing a compact density variation by `4r^3` is a legal Sobolev test and gives

    f_x(a)-a.j*-(1/4)div j*=lambda

in distributions. All other terms are L1, hence `div j* in L1`. Pointwise Fenchel equality gives the exact weak optimal residual. The same calculation in left-invariant phase coordinates gives the producer's formula.

For positive boundary trace, define `B_g(j)=1/4 integral(j.grad H+H div j)` with any W1,4 lift H of `g^4`. Differences of lifts are zero-trace and have compact smooth approximations converging both in W1,4 and uniformly. Thus the pairing is extension independent even with only L1 divergence. The same weak dual objective as before, `lambda M+B_g(j)`, is attained at j*. No classical normal trace, derivative bound on n, or smooth flux is needed.

Boundary zeros still obstruct a globally integrable unweighted logarithmic flux; the earlier exact `r=x` counterexample remains valid even for a constant direction. The rough extension does not remove that distinction.

## 7. Slight strengthening: uniqueness for all admissible nonnegative traces

The producer states uniqueness conservatively for the torus and positive-boundary cases, where a global Picone quotient test is convenient. Interior positivity plus strict density interpolation prove it for every admissible nonnegative trace, including those that vanish.

For two minimizers, the fourth-root interpolation is feasible. Its energy must equal the common minimum. At almost every interior point the amplitudes are positive, and the strict rank-one quartic remainder forces their logarithmic gradients to coincide. On each compact subset the quotient is a Sobolev function with zero gradient; connectedness and equal mass make it identically one. The argument is pointwise in the measurable rough coefficients and uses no division at a boundary zero. Thus Dn-infinity regularity is unnecessary for this stronger uniqueness statement as well.

## 8. Direct affine-boundary applicability and the remaining sign

An actual planar W1,4 vector map is bounded and continuous up to the Lipschitz boundary. A sufficiently large constant target translation makes it uniformly nonzero. Its direction `(u+c)/|u+c|` is W1,4 by smooth composition on that nonzero range, with a positive boundary amplitude. The rough theorem therefore applies directly to every such compatible test, without requiring a smooth direction approximation first.

The amplitude minimum is still only a fixed-direction object. Its norm-budget lower bound may be negative. A large translation does not make that lower bound prove Jensen: it typically makes `K=O(1/|c|)` while its fourth mass is `M=O(|c|^4)`, so the `K^4 M` term need not go to zero. No all-phase sign or full quasiconvexity theorem follows.

## 9. Final review state

No decisive analytic gap was identified in the stated rough-direction extension or its C1 mass-value assertion. The positive/unique amplitude and weak attained-dual conclusions survive under the explicit hypotheses. The review adds the zero-boundary uniqueness refinement above. It does not certify the cited historical Harnack theorem, require that literature as a premise, or claim an experiment, smooth certificate acquisition, efficient optimizer, full-direction sign or novelty. A separate receipt pins source bytes and confirms the prior frozen review was not edited.
