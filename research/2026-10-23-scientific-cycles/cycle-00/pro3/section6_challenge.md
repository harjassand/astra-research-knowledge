# Independent challenge of Section 6 only

Reviewed source snapshot: `PROOF.md`, 17,426 bytes, SHA256 `610ab32e442ac06f301063f0b578fc8e973576ca08288186986269e773c89bf9`, read on 21 October 2026 at 11:41 UTC. Later source edits require checking whether this review's Section 6 assumptions or formulas changed.

## Verdict

The new Section 6 warm-start inequality and its explicit finite budget are correct under the stated hypotheses. I found no missing factor of two, reversed inequality, density-normalization error, spectral defect, or finite-state restriction. This review checks the principal investigator's new derivation; it does not establish historical novelty, an application speedup, or the independently separate claims in Sections 2--4.

The assumptions needed are: equivalent probability measures pi and q with a positive finite measurable likelihood ratio; the independence-MH kernel G; a fixed pi-reversible Markov kernel L; fixed `0<alpha<1`; the lazy kernel `C=(I+alpha G+(1-alpha)L)/2`; and a probability initializer nu whose density satisfies `0<=dnu/dpi<=B<infinity`. Functions in the Dirichlet argument are real-valued and essentially bounded. The finite-budget substitution also assumes the stated population bound `D(pi||q)<=K`, with K>0.

## 1. Independence-MH Dirichlet form

For the accepted part of G, detailed balance gives conductance

`pi(dx) q(dy) min(1,W(y)/W(x)) = pi(dx) pi(dy)/max(W(x),W(y))`.

The rejection diagonal contributes zero to the Dirichlet form. This remains true on spaces with atoms. Therefore

`E_G(g,g) = (1/2) integral pi(dx)pi(dy) (g(x)-g(y))^2/max(W(x),W(y)`.

Let `A_R={W<=R}` and `h=pi(A_R^c)`. On `A_R x A_R`, the reciprocal maximum is at least 1/R. The mass of the complement under `pi tensor pi` is `2h-h^2`. Since the variance has the same pair-integral representation without the reciprocal factor,

`Var_pi(g) <= R E_G(g,g) +(h-h^2/2) Osc(g)^2 <= R E_G(g,g)+h Osc(g)^2`.

The off-core term and all factors of two in the root's weak inequality are therefore valid.

Linearity of the Dirichlet form gives

`E_C=(alpha/2)E_G+((1-alpha)/2)E_L >= (alpha/2)E_G`.

Consequently

`Var_pi(g) <= (2R/alpha) E_C(g,g)+h Osc(g)^2`.

No finite spectral gap is used or required.

## 2. Spectrum, laziness, and variance recursion

Both G and L are self-adjoint contractions on `L2(pi)` because they are reversible Markov kernels. Their convex mixture H is likewise self-adjoint with spectrum in `[-1,1]`. Thus `C=(I+H)/2` is self-adjoint with spectrum in `[0,1]`.

In the quadratic-form sense,

`I-C^2 >= I-C`,

because `1-lambda^2 >= 1-lambda` for `lambda in [0,1]`. This is exactly where positivity/laziness is used. Invariance or reversibility alone would not justify that step for a kernel with negative eigenvalues.

For `u=C^j g-pi(g)` and `v_j=||u||_2^2`,

`v_j-v_(j+1)=<u,(I-C^2)u> >= E_C(C^j g,C^j g)`.

A Markov kernel contracts essential oscillation, and pi-invariance ensures the L-infinity equivalence-class operation is well-defined. The weak inequality then yields

`v_(j+1) <= (1-kappa)v_j+kappa h Osc(g)^2`, with `kappa=alpha/(2R)`.

Here `0<kappa<1`. Iteration gives the slightly stronger form

`v_n <= (1-kappa)^n Var_pi(g)+[1-(1-kappa)^n] h Osc(g)^2`,

which implies the root's displayed bound

`v_n <= r_n Var_pi(g)+h Osc(g)^2`, `r_n=exp(-alpha n/(2R))`.

## 3. Density and indicator estimates

If `f=dnu/dpi` is a probability density bounded by B, then

`Var_pi(f)=E_pi f^2-1 <= B E_pi f-1=B-1`, and `Osc(f)<=B`.

For any measurable A, `Var_pi(1_A)<=1/4` and `Osc(1_A)<=1`. Centering either function does not change variance or oscillation.

Reversibility gives the required split:

`nu C^(2n)(A)-pi(A) = <C^n(f-1), C^n(1_A-pi(A))>`.

Cauchy--Schwarz and the two variance estimates give

`|nu C^(2n)(A)-pi(A)| <= sqrt([r_n(B-1)+hB^2][r_n/4+h])`.

Taking the supremum over measurable A proves the claimed TV convention without an additional factor of 1/2. A finite state space, an eigendecomposition, a compact operator, and a discrete spectrum are unnecessary: the bounded self-adjoint spectral calculus on `L2(pi)` suffices.

## 4. Explicit epsilon budget

Take an integer N at least `16 exp(2K+1) log(3/epsilon)` for `0<epsilon<=1/2`. The already-reviewed initialization lemma gives `beta<=epsilon/3`. Its normalized good density satisfies

`4/(1-beta) <= 4/(1-epsilon/3) <= 4.8 < 6`.

It is therefore valid to apply Section 6 with the uniform constant B=6, independent of the unknown actual bad mass.

For `h_0=epsilon/18` and `R=exp(1+18K/epsilon)`, K>0 ensures R>e and the entropy tail bound yields `h<=h_0`. Choose an integer n at least `(2R/alpha) log(18/epsilon)`. Then `r_n<=h_0`.

The root's square-root bound is at most

`h_0 sqrt((B-1+B^2)(1/4+1))`.

At B=6 this is `h_0 sqrt(41*1.25)`, approximately `7.159 h_0`. In particular it is below the stated conservative bound `2B h_0=2epsilon/3`. The mixture estimate is

`TV(mu_N C^(2n),pi) <= beta +(1-beta)TV(nu C^(2n),pi)`

and is therefore at most epsilon under the proposed choices. Replacing the factor `(1-beta)` by 1 only weakens the bound and is harmless.

Integer ceilings for N and n should be understood in any executable budget; no change to the theorem constants is needed.

## 5. Access, cost, and scope

The canonical implementation of each C application performs no underlying update with probability 1/2, a global update with probability alpha/2, and a local update with probability `(1-alpha)/2`. Over 2n applications the expected global and local update counts are respectively `alpha n` and `(1-alpha)n`, exactly as stated. Initialization uses N proposal candidates; if implemented as pure IMH, those are one initial candidate and N-1 updates. Local update costs remain additional and depend on L.

The direct SIR initialization proof and Section 6 both hold on general measurable spaces. The published finite-space IMH-versus-SIR theorem must retain its stated scope unless its extension is supplied; the separate `warmstart_challenge.md` gives an approximation argument for the needed hockey-stick comparison. There is no need to import that extension for the general-space direct-SIR version of Section 6.

This is an ideal exact-kernel guarantee. Approximate density evaluations, finite-precision acceptance decisions, learned state-dependent mixture probabilities, or adaptation of L are not automatically covered. The root's stated fixed reversible-kernel scope is sufficient. A bound on population KL remains an input assumption.

The constants are deliberately poor: the final R grows as `exp(1+18K/epsilon)`. The result repairs the failure of a uniform cold-start guarantee by paying an explicit safe-initialization cost. It establishes no rate improvement over pure independence MH, and the proof correctly says so.

## Disposition

Accept Section 6 as an internally checked mathematical result under its explicit hypotheses. No mathematical correction is required. Preserve laziness, reversibility, fixed mixture weights, the bounded good density, and the population-KL qualification in any continuation or condensed handoff.
