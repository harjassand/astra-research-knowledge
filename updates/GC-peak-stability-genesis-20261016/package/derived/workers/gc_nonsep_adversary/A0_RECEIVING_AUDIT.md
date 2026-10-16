# Independent receiving audit of the homogeneous separated tube

Internal receiving audit, 2026-10-16. This is analytic review and exact finite verification, not external validation or historical clearance.

**Finding:** no decisive flaw found. The candidate proves a homogeneous nonseparated tube around every nonconstant separated first potential, including the acoustic boundary `||F'||2=0`. It is stronger than the incoming positive-fraction comparison theorem in scope, but it uses a corrected second potential and does not assert that comparison at `A=0`.

The explicitly authorized receiving input is `workers/gc_nonsep_genesis/PROOF.md`, SHA256 `c564e52914d70ba14000e1abadb17ac7432b04d19fd62cb0bfb159b6c8713b36`. Sections 4–7 carry the new argument. I read this candidate only after the parent specifically requested a receiving audit; earlier independent results are in `PROOFS.md`. The exact source Gram data and incoming proof hashes are in `VERIFICATION_RECEIPT.json`.

## 1. Restated claim and limits

Fix `r>0`. Let `f0=Pi f=F(x)+H(y)` be the coordinate-average projection and `eta=f-f0`; both coordinate averages of `eta` vanish. Put `R=||Df0||4>0`, `epsilon=||Deta||4`, and keep the original quartic integrand `J_r`. The candidate supplies a positive constant `delta_r` depending only on `r`, such that `epsilon<=delta_r R` implies, for every real scalar conformal background `sI` and every periodic `g in W^{1,4}`,

```
E_r(f,g,s)>=alpha/2 (R⁴+||Dg0||4⁴)+mu/2 s² B(f,g)>0.
```

Here `g0=g+p(eta)` is a compatible scalar Fourier correction; `B` is the exact integrated acoustic energy. This statement includes arbitrarily concentrated separated profiles, all admitted fine scales, and arbitrarily large `g,s`. The proof gives no general affine-background theorem and no unrestricted mixed-source theorem. Since all gradient norms and energies scale homogeneously, the ratio condition is invariant under simultaneous amplitude scaling.

A radius around a constant first potential would be a qualitatively different result: by scaling, any positive gradient-ball radius at that center, valid for every `g,s`, would imply the unrestricted scalar-conformal Jensen theorem. No such radius is claimed.

## 2. Independent projection reconstruction

Use `sigma=r+1`, `kappa=r(r+2)/3`, `A=eta_x`, and a Fourier frequency `(m,n)`. Let

```
p_hat=sigma*m*n/(n²+kappa*m²)*eta_hat,
k=p_x, e=sigma*A-p_y.
```

The corresponding real derivative multipliers are, up to the common factor `i`,

```
e_hat=i sigma kappa m³/(n²+kappa m²)*eta_hat,
k_hat=i sigma m²n/(n²+kappa m²)*eta_hat.
```

They obey `e_y-kappa k_x=0` distributionally. Writing `g0=g+p`, the actual acoustic variables are `U=U0+e` and `c=c0-k`. Integration against `Dg0` therefore cancels the cross pairing `<d0 e-kappa c0 k>`. Moreover `<F'(x)e>=0` because the mixed perturbation has no horizontal Fourier modes. Consequently

```
B(f,g)=B(f0,g0)+Br(eta),
Br=sigma² sum[kappa m⁴/(n²+kappa m²)] |eta_hat|²>=0.
```

The coefficient signs and the correction direction are correct. This is the orthogonal acoustic projection, not an estimate that discards a negative cross term. Since

```
Br>=sigma² min(1,kappa)||R_x eta_x||2²,
```

the candidate's `Ca=max(1,kappa^-1/2)/sigma` is valid.

I verified the exact Fourier identities independently in `verify.py`. At `A=0`, the new corrected `g0` differs from the old comparison's `g`; that is precisely why the positive-fraction countermodel in `PROOFS.md` does not refute this projection route.

## 3. Primary analytic input checked at its precise scope

[Bañuelos and Baudoin, *Martingale transforms and their projection operators on manifolds*, Theorem 4.1(i), Section 4.2](https://arxiv.org/pdf/1109.5751) bounds constant-matrix second Riesz transforms on Lie groups of compact type by `(p*-1)||M||`. An abelian torus with any positive constant metric meets its hypotheses. With `p=4`, this gives factor `3`; a symmetric matrix with off-diagonal entries `1/2` has operator norm `1/2` and gives factor `3/2`. The diagonal choice has norm one. The anisotropic vector fields used by the candidate are orthonormal for such a flat metric. Normalizing the constant volume density changes no operator norm.

Thus the source supports both the projection's `L4` bounds and the cubic lemma's bounds uniformly over its positive anisotropy parameter. No Euclidean-to-torus transference assumption is missing. The convention for the sign of the second Riesz transform does not affect these norm bounds.

In particular,

```
||p_y||4<=3 sigma epsilon,
||p_x||4<=3 sigma epsilon/(2 sqrt(kappa)),
||Dp||4<=L epsilon, L=3 sigma(1+1/(2 sqrt(kappa))).
```

The candidate uses larger component constants `Lc=L` and `Le=sigma+L`, which are conservative.

## 4. Explicit absolute cubic lemma checked analytically

The proposed statement is stronger than a signed cubic estimate:

```
<|eta_x|³><=11 ||R_x eta_x||2 ||Deta||4².
```

Put `A=eta_x`, `B=eta_y`, `q*=||R_x A||2` and

```
A_tau_hat=tau² n²/(m²+tau² n²)*A_hat, 0<tau<=1.
```

Gradient compatibility gives `A_tau=tau T_tau B`, where the cross second Riesz multiplier of `T_tau` has norm at most `K=3/2` on `L4`. Therefore `||A_tau||4<=K tau epsilon`. This holds on the axes too: `n=0` gives `A_tau=0`, and `m=0` gives `A=0`.

Plancherel gives `||A-A_1||2<=q*`. The difference at dyadic scales has multiplier ratio to the absolute `R_x` symbol

```
3v sqrt(1+tau²v²)/[tau(v²+1)(4v²+1)]
 <=3v/[tau sqrt(v²+1)(4v²+1)]<=3/(4tau),
v=|m|/(tau|n|).
```

The first inequality uses `tau<=1`; the second uses `4v/(4v²+1)<=1`. The formula for the difference itself is `3v²/[(v²+1)(4v²+1)]`; both powers of `tau` are correct. Hence `||A_tau-A_{tau/2}||2<=3q*/(4tau)`.

For the first telescoping step, Holder and the elementary cubic difference inequality give coefficient `1+K+K²`. At scale `tau`, the three products of `L4` norms sum to `(7/4)K²tau²epsilon²`; multiplying the preceding `L2` bound gives `(21/16)K²tau q*epsilon²`. Summing the dyadic series gives

```
1+K+K²+21K²/8=341/32<11.
```

The terminal contribution tends to zero in `L3` because `||A_tau||4<=K tau epsilon`. Thus the telescoping is a valid infinite analytic argument, with every frequency included; there is no finite-cutoff premise. The same inequalities hold for `W^{1,4}` gradients by the bounded multipliers and strong approximation. This independently validates the explicit constant 11.

The qualitative mechanism is prior capital: the original conformal packet's mixed-derivative interpolation/Hodge argument already yields finite cubic control of this type. The explicit receiving argument and its use in a tube theorem should not be represented as discovery of generic cubic compensation.

## 5. Cubic difference: all six rows rederived

Use the exact identity

```
P=2aU²-(r+2)a²U+r c²U-2bcU-kappa a³-kappa ac².
```

Let `q=sqrt(B(f,g))` and `t=||Dg0||4`. Orthogonal projection gives `||U||2,||U0||2<=q`, `||c||2,||c0||2<=q/sqrt(kappa)`, and `||a0||2<=q/sigma`. The last fact follows from `<a0 d0>=0`; it does not require a positive lower bound on `||a0||2`.

I obtained the following decompositions independently:

```
aU²-a0U0² = A U²+a0 e(U+U0),
a²U-a0²U0 = A(a+a0)U+a0²e,
c²U-c0²U0 = -k(c+c0)U+c0²e,
bcU-b0c0U0 = B cU-b0 kU+b0c0e,
ac²-a0c0² = A c²-a0 k(c+c0).
```

Here the capital `B` in this display is `eta_y`, not the acoustic energy. Pairing one acoustic factor in `L2` and the other two factors in `L4` reproduces each of the candidate's table coefficients, including the factors of two and `sqrt(kappa)`.

The two exceptional slice cancellations are exact in the rough class:

```
<a0² e>=0, <a0² A>=0,
```

because `a0` depends only on `x` and `e,A` have zero `y` average. Fubini and Holder suffice; no derivative of `a0²` is taken. Thus

```
|<a³-a0³>|<=3||a0||2||A||4²+<|A|³>
           <=(3/sigma+11Ca)q epsilon².
```

This yields `|P-P0|<=CP epsilon q(R+t+epsilon)` with precisely the candidate's `CP`. The stress-conservation hypothesis of the incoming proof is not used for `eta`.

## 6. Quartic continuity and absorption independently checked

Direct differentiation of the original integrand gives

```
|DJ_r(V)|<=LJ |V|³,
LJ=6r/(r+2)+(2/3)r(r+1)+1+2r.
```

The four summands correspond to the squared conformal quantity, `u²`, `j²`, and `uj`. The inequalities `|j|<=|V|²/2`, `|Dj|=|V|`, `|Du|<=2|V|`, and `|D(|V|²-2j)|<=4|V|` justify every coefficient. This uses `|r-1|<=r+1`; no coefficient is assumed positive when it is not.

Since `||V-V0||4<=D epsilon`, `D=1+L`, the quartic difference is at most `LJ D epsilon(R+t+D epsilon)³`. Under `epsilon<=delta R`, `delta<=1/D`, this is at most `64 LJ D delta(R⁴+t⁴)`.

The separated reserve applies to `(f0,g0)` with its unrestricted `g0`. Set `Z=R⁴+t⁴`, `K0=max(2sigma²,kappa)`, and `mu=beta/K0<1`. It gives `E0>=alpha Z+mu s²B0`. Adding the nonnegative projection residual and bounding the cubic error yields

```
E>=alpha Z+mu s²q²
    -2CP epsilon |s|q(R+t)-64 LJ D delta Z.
```

Young's inequality costs at most `(mu/2)s²q²+(16CP²/mu)delta²Z`. Therefore

```
E>=[alpha-64LJD delta-(16CP²/mu)delta²]Z+(mu/2)s²q².
```

The two stated conditions `delta<=alpha/(256LJD)` and `delta<=sqrt(alpha mu)/(8CP)` make the two losses at most `alpha/4` each. This is uniform over arbitrary `s` and arbitrary `g`; neither is bounded during the argument. The acoustic coefficient is never replaced by a tiny uniform Gram floor.

At `r=1`, independent exact reconstruction gives

```
mu=1/12288, L=9, D=10, CP=140, LJ=19/3.
```

`delta=1/40000000` passes both absorption conditions as exact rational inequalities. The actual-ball factor `delta/5` is also correct: coordinate projection costs at most two, the mixed complement at most three, and `delta<=1` supplies the remaining slack.

The discriminant inequality follows by subtracting the proved lower bound and minimizing the remaining quadratic in `s`. The separate zero-acoustic case is treated without division, so no missing nullspace case remains.

## 7. Rough functions and finite evidence boundaries

All nonlinear expressions are integrable: gradients are in `L4`, cubics in `L^{4/3}`, and quartic energies in `L1`. Coordinate averaging preserves `W^{1,4}`. The correction is a bounded linear map on gradients, and real Fourier symmetry is preserved. Distributional projection orthogonality extends by smooth approximation. Slice cancellations use Fubini on integrable products. The estimates can be proved directly in this class or obtained by taking limits in the estimates before imposing the final radius condition; no claim that a boundary-radius ratio is preserved by each individual convolution is needed.

`verify.py` passed 62 exact/rational assertions, including the original Gram identity and positive pivots, full conformal expansion, rank-one convexity algebra, projection symbols, the dyadic constant, all `r=1` absorption conditions, and the exact positive domination counterfamily. Forty-eight anisotropic trigonometric diagnostics on a `256²` grid gave largest absolute-cubic ratio `0.8729434296468346` and relative projection discrepancy below `9e-17`. These finite observations are diagnostics only; they neither prove the analytic lemma nor certify the theorem externally.

**Frozen receiving conclusion:** the candidate's analytic theorem at the audited hash passes this independent receiving review. The older source theorem and the new projection theorem remain internally reviewed mathematical results. External review, historical originality, unrestricted scalar-conformal quasiconvexity, general affine-background quasiconvexity, and practical capability are unresolved.
