# Independent Pauli-triple scalar-noise improvement

Status: internally derived on 2026-10-15; not externally verified, not a priority claim. This file freezes the construction before comparison with other new workers. Input `sources/regularization_pasted.txt` was treated as data. No other new-worker report was read before this freeze.

## Contract and general radial constraints

Use the Fourier convention `hat μ(t)=∫exp(i t·x) μ(dx)`. The target is a positive normalized qubit POVM on R^3 with

`hat M(t)=φ(|t|) exp(i t·σ)`,

where φ is the characteristic function of a **positive scalar radial probability law** on R^3. Let the scalar one-coordinate density be h(x), even. If the noise radius has an absolutely continuous law, write

`h(x)=∫[|x|,∞) g(s) ds`, `g(s)≥0`, `2∫s g(s) ds=1`.

Its radius density is `2s g(s)` and its spatial density is `g(|z|)/(2π|z|)`. In particular positivity of the scalar noise is explicit, not inferred from positivity of M.

Write a rotationally covariant POVM as

`M(dr,dn)=q(r)dr [I+a(r)n·σ] dΩ(n)/(4π)`, `q≥0`, `|a|≤1`.

Let `c(x)=[h(x−1)+h(x+1)]/2` and `b(x)=[h(x−1)−h(x+1)]/2`. The projection of M onto a fixed axis has density `c(x)I+b(x)σ_axis`. Inverting the radial projection gives, for r>0,

`q(r)=−2r c'(r)` and `a(r)q(r)=−2r² (b(r)/r)'`.

Consequently the necessary and sufficient positivity inequalities, in this density class, are

* for `0<r<1`: `2r g(1−r) ≤ ∫[1−r,1+r]g(s)ds ≤ 2r g(1+r)`;
* for `r≥1`: `∫[r−1,r+1]g(s)ds ≤ 2r g(r+1)`.

For r≥1 the other eigenvalue inequality is automatic. These formulas are obtained from both eigenvalues `q±aq`, and are sufficient because the inverse projection is explicitly a positive POVM.

## A positive law strictly better than variance 23/9

Define the unnormalized profile G by

`G(s)=1` for `0≤s≤2`,

and, successively on the intervals of length 2, solve

`2(s−1)G'(s)=−G(s)−G(s−2)` for `s>2`.

The method of steps gives a unique continuous solution, C^1 for s>2. Its integral identity is

`2(s−1)G(s)=∫[s−2,s]G(u)du` for `s≥2`.

Indeed the derivative of the difference of the two sides is zero, and both agree at s=2. A first zero cannot occur: the integral at the first zero would be strictly positive. Thus G>0. The differential equation then gives G'<0 for s>2. Furthermore

`G(s)≤G(s−2)/(s−1)` for s≥2.

Iterating yields factorial decay on intervals of length 2, so `∫exp(b s)s^kG(s)ds<∞` for every finite b and nonnegative integer k. The positive tail continues to every finite s, so the law is unbounded.

Let `Jk=∫[0,∞)s^kG(s)ds` and `C=1/(2J1)`. Set the normalized scalar profile `g=C G`. The scalar noise radius density is

`η(s)=2C sG(s)`, `s≥0`.

It is a positive probability law with all exponential moments. Set

`q(r)=C r[G(r−1)+G(r+1)] 1_{r≥1}`, `a(r)=1`.

For 0<r<1 both radial POVM coefficients vanish because G is constant on [0,2]. For r≥1 the integral identity saturates the upper positivity inequality; hence q=aq≥0. Direct integration gives `∫q=2C J1=1`. The projected densities are exactly `[h(x−1)+h(x+1)]/2` and `[h(x−1)−h(x+1)]/2`, so uniqueness of the Fourier transform proves the full target identity at **every** t, with φ explicitly the scalar radial characteristic function `∫η(s)sinc(|t|s)ds`.

No positive-Fourier-only shortcut is used.

## Exact moments and strict improvement

For s∈[2,4], `G(s)=2/sqrt(s−1)−1`.

In distributional form on the nonnegative half-line,

`2(s−1)G'(s)+G(s)+G(s−2)=1_[0,2](s)`,

with the G(s−2) term zero for s<2; integration by parts includes the boundary contribution at zero. Multiplying by s^n and integrating gives

`J1=2J0−1`, `J2=5J0−8/3`, `J3=(46/3)J0−8`.

Therefore

`Var(Zj)=J3/(3J1)=23/9−1/(9J1)=23/9−2C/9 < 23/9`.

The POVM radius obeys `ER=3`, `ER²=3(1+Var(Zj))`. Numerical exploration suggests variance approximately 2.53376, but the exact formula and strict inequality do not depend on numerical solving.

A coarse explicit analytic bound is available. On [0,4], `∫sG=8sqrt(3)−28/3`. Let `d=G(4)=2/sqrt(3)−1`. On `[4+2j,6+2j]`, `G≤d/5^j`. Thus

`J1 ≤ 8sqrt(3)−28/3 + d Σ[j≥0](10+4j)/5^j`

`=8sqrt(3)−28/3+(55/4)(2/sqrt(3)−1)<7`.

It follows rigorously that `Var(Zj)<23/9−1/63=160/63≈2.539683`, already strictly below 23/9.

## A universal strict improvement on the elementary lower bound 2

This argument applies to all rotationally covariant exact-contract POVMs of finite variance, including singular radial laws. Let R have the scalar radial POVM law q. First and second moments give `E[a(R)R]=3`, `ER²=3(v+1)`, where v is the scalar coordinate variance. Hence `ER≥3`, `v≥2`.

At `k=π/2`, scalar-part Fourier equality gives `E f(R)=0` for `f(r)=sinc(πr/2)`. The cosine zero is essential. The integral representation `f(r)=∫[0,1]cos(π r u/2)du` gives the global upper second derivative bound `f''≤π²/12`. Therefore, for all r≥0,

`f(r)≤f(3)+f'(3)(r−3)+(π²/24)(r−3)²`.

Here `f(3)=−2/(3π)` and `f'(3)=2/(9π)`. Put d=ER−3≥0 and use `E(R−3)²=3(v−2)−6d`. Taking expectations yields

`0≤−2/(3π)+(π²/8)(v−2)+(2/(9π)−π²/4)d`

`≤−2/(3π)+(π²/8)(v−2)`.

Thus every feasible radial scalar noise satisfies

`v≥2+16/(3π³)≈2.172008`.

This is not sharp. It is a rigorous lower bound above 2 that uses the exact scalar-factor constraint rather than coordinate moment positivity alone.

## Compact scalar noise is impossible

The general radial inequalities already give an elementary density-class obstruction: if G had finite right endpoint B, the inequality at any x>B with x−2<B would demand a positive integral to be at most zero.

For arbitrary compactly supported scalar noise, including nonradial and singular laws, use the supplied Pauli-pair tilted moment inequality. The scalar cumulant satisfies `κ22(s,0)≥[sinh(2s)−2s]/(2s²)`. A bounded second coordinate has uniformly bounded tilted variance under every first-coordinate exponential tilt. The right side diverges; contradiction. Compact support is therefore impossible even before imposing radial symmetry.

## Information and implementation comparison

The POVM is implemented in the ideal model by the ordinary covariant spin measurement `N(dn)=[I+n·σ]dΩ/(4π)`, followed by an independent radius R∼q and report X=Rn. Since R≥1, n=X/|X| is exactly recoverable. The two statistical experiments are equivalent by state-independent Markov kernels. The improved scalar convolution variance is an improvement within the restrictive reporting contract, and adds no quantum information beyond N.

The usual report 3n has directional second moment 3. The new exact-convolution report has second moment v+1, strictly larger than 3; its ratio is `(v+1)/3`, approximately 1.17792. The radius optimization does not improve the ordinary Bloch-vector mean decoder.

Continuous random axes, one projective qubit measurement, classical radius sampling, arithmetic, and output precision are separate costs. The profile is defined by a delay equation, so exact finite-bit sampling has not been compiled here. Factorial envelopes give controlled truncation and a possible rejection sampler with a density-evaluation oracle. They do not by themselves certify arithmetic or device error. Common rounding must be applied when comparing a finite-bit implementation with the continuous target in total variation.

## Open gates at the independent freeze

* The construction is rigorously better than the supplied Dickman law; global optimality is unproved.
* The grid LP suggests the flat central profile may be optimal, but discretization and a finite tail cutoff do not certify this.
* The all-linear Wigner distribution and covariant spin measurement are prior mathematics. The transformed delay equation is a generalized Dickman equation in its tail. Exact historical priority of this scalar-noise variance construction is not cleared.
* This proof is an internal analytic derivation, not formal verification or external mathematical review.
