# An actual four-value scalar Stein correction with a quartic full-law example

27 October 2026. Derived from frozen S3/S4 and the joint-divergence construction in this chat. The Gaussian-mean target in CASE remains open. This note supplies a finite positive correction when its coefficient S is explicitly evaluable; acquisition of a useful S for a general unknown source is a separate, charged obligation.

## 1. The legal operation

Let h:R->R be globally ell-Lipschitz. Draw independent standard Gaussians G,Z and put `X=h(G)+Z`. For analysis only, write `mu=E h(G)` and let K be the canonical Stein kernel, with `delta_G K=h-mu`, `|K|<=ell`.

Supply a smooth explicitly evaluable coefficient `S(G,Z)` and its derivatives `S_G,S_Z`. These are derivatives of the supplied coefficient, not derivatives of h. Assume the displayed divergences and second moments exist. An independently fitted coefficient is allowed by conditioning on its fitting transcript; every fitting query and arithmetic operation is additional.

Draw fresh independent Gprime,W and the Gaussian seeds for the R22 secant. Query h(G) and h(Gprime). Independently draw U uniform on [0,1] and C~chi_3; set `r=sqrt(1-U^2) C`, query `h(UG+r),h(UG-r)`, and return

`Jhat=[h(UG+r)-h(UG-r)]/(2r)`.

R22 gives exactly `E[Jhat|G]=K(G)` and `|Jhat|<=ell`. The uniform U itself uses only three standard Gaussians: `U=(1+A1/sqrt(A1^2+A2^2+A3^2))/2`. The null denominator events receive a fixed bounded value.

For a paid Gaussian reserve a>0, output

`Y=h(G)+Z+Uhat+aW`,

`Uhat=S(G,Z)[h(G)-h(Gprime)+Z]-S_G(G,Z)Jhat-S_Z(G,Z)`. (1)

This uses exactly FOUR original h-value queries on every execution, plus the separately charged acquisition/evaluation of S. It uses no potential, derivative of h, mean, or conditional-mean oracle. Apart from coefficient work, arithmetic and storage are constant in this scalar problem. Exact Gaussian seeds and real arithmetic specify the theorem; a floating program is only a numerical implementation check unless a commonly rounded target and primitive-error budget are supplied.

The source offset cancels algebraically in both differences in (1).

## 2. Exact mean and the variance price of acquisition

The ideal, unacquired correction is

`u=delta_(G,Z)(S[K,1])=S[X-mu]-K S_G-S_Z`.

Condition on Q=(G,Z) and any independent coefficient-fitting transcript. Then `E[Uhat|Q]=u`. Therefore

`E Y=mu` exactly.                                    (2)

Indeed `E u=0` by Gaussian divergence. The error `D=Uhat-u` is

`D=-S[h(Gprime)-mu]-S_G[Jhat-K(G)]`.

Its two terms are conditionally independent and centered. Gaussian Poincare and the bounded secant give

`E[D^2|Q] =S^2 Var(h(Gprime))+S_G^2 Var(Jhat|G)`

`          <=ell^2(S^2+S_G^2)`.                       (3)

No conditional covariance contribution is discarded.

## 3. Full-law replacement bounds

Let `Yideal=X+u+aW`. Then

`TV(Law(Y),Law(Yideal))`

` <=phi(1) E D^2/a^2`

` <=phi(1)ell^2 E(S^2+S_G^2)/a^2`,                   (4)

where `phi(1)=exp(-1/2)/sqrt(2pi)`.

To prove this, Taylor-expand the Gaussian density `p_a(y-D)` around D=0. Conditional centering cancels the linear term; the L1 remainder is at most `E[D^2|Q] ||p_a''||_1/2`. Total variation adds a factor 1/2, while `||p_a''||_1=4phi(1)/a^2`. Integrate over Q. Translation by the dependent ideal center does not change the bound. This proves a full-law result, not moment matching. Scaling S by t makes this replacement error O(t^2).

There is also a conditional chi-square bound. The error D has conditional subgaussian proxy `v(Q)=ell^2(S^2+S_G^2)`: scalar Gaussian concentration handles h(Gprime), and the secant's interval of length 2ell gives the other proxy. If v(Q)<a^2,

`chi2(Law(Y|Q)||Law(Yideal|Q))`

` <=[1-v(Q)^2/a^4]^(-1/2)-1`.                        (5)

This follows from the exact Gaussian-mixture identity `1+chi2=E exp(DD'/a^2)` and the two proxy bounds. The expectation of the right side bounds the augmented joint chi-square, hence also the output chi-square after forgetting Q. Equation (5) is useful for bounded coefficients; it is not necessarily a better TV constant than (4).

## 4. Combining actual queries with a full equation-residual bound

Use the weak smoothed-law theorem independently proved in `../coercive_audit/SMOOTHED_LAW_NEWTON_THEOREM.md`, sections 3–4A. Set

`R=K h'`, `r0=||R||_2`, `B=[K,1]`, `tau=1+R`,

and let `E=R+L(u,SB)` be the FULL linearized equation residual, where

`L(u,SB)=B dot grad(u)+S tau`.

No derivative of h or K in this paragraph is a runtime query. Let `e=||E||_2`, `U2=||u||_2^2`, and `V2=ell^2 E(S^2+S_G^2)`. The actual four-value law satisfies

`TV(Law(Y),N(mu,1+a^2))`

` <= C2(a)e+C3(a) r0 sqrt(U2)+phi(1)(U2+V2)/a^2`,     (6)

with scalar constants

`C2(a)=phi(1) log(1+a^(-2))`,

`C3(a)=[phi(0)+4phi(sqrt(3))][1/a-arctan(1/a)]`.

The scalar refinements follow from the zero integrals of the second and third Gaussian density derivatives: for a smoothed event indicator, the derivative supremum is at most half the derivative's L1 norm. The identities are `||phi''||_1=4phi(1)` and `||phi'''||_1=2phi(0)+8phi(sqrt(3))`. OU integration then gives C2 and C3. The final Taylor remainder uses `E Uhat^2=U2+E D^2`.

The theorem uses the full equation residual, not residuals merely tested against a finite fitting basis. It requires no L-infinity bound on S, no pointwise positivity of the corrected Stein coefficient, and no asserted Gaussian law for the random correction.

## 5. An elementary nonconstant coefficient with quartic law error

Put

`k(x)=x/(1+x^2)`, `f(x)=1-2/(1+x^2)^2`.

Then `delta_gamma k=f`, so `E f(G)=0`; moreover

`f'(x)=8x/(1+x^2)^3`, `Lip(f)=L0=125/(27sqrt(5))`.

Take the nonaffine globally Lipschitz source `h(x)=c+lambda f(x)`. Thus `mu=c`, `ell=lambda L0`, and its canonical kernel is `K=lambda k`. The offset c is not supplied to the sampler.

Define explicit rational functions

`s(x)=-k(x)f'(x)/2=-4x^2/(1+x^2)^4`,

`t(x)=-k(x)s'(x)/3=(8/3)x^2(1-3x^2)/(1+x^2)^6`,

and supply the coefficient

`S(G,Z)=lambda^2 s(G)+lambda^3 t(G)Z`.                (7)

Its required derivatives are

`s'(x)=-8x(1-3x^2)/(1+x^2)^5`,

`t'(x)=(16/3)x(1-11x^2+12x^4)/(1+x^2)^7`,

`S_G=lambda^2 s'+lambda^3 t' Z`, `S_Z=lambda^3 t`.

They are explicit coefficient arithmetic, not derivative queries to h. The coefficient is unbounded linearly in Z, which is permitted by (6).

The ideal correction is exactly

`u=lambda^2 s Z+lambda^3[s f+t(Z^2+2)]`

`  +lambda^4(t f-k t')Z`.                            (8)

Write `r=k f'`. Direct differentiation gives the FULL equation residual

`E=lambda^4 A(G,Z)+lambda^5 B0(G)Z`,                 (9)

where

`A=-4s^2+k t'(Z^2+1)-2t f`,

`B0=2t r+k f t'-k k't'-k^2 t''`.

Both the quadratic and cubic powers vanish pointwise: `r+2s=0` and `k s'+3t=0`. Thus (9) is an exact finite identity beyond formal cubic cancellation. The source-value randomization adds order lambda^6 through (3), and the full smoothed-law estimate (6) is order lambda^4.

## 6. Explicit constants and a nonvacuous regime

Elementary rational bounds, proved or checked algebraically in the companion script, are

`|f|<=1`, `|k|<=1/2`, `|k'|<=1`, `|r|<=27/32`,

`|s|<=s0=27/64`, `|s'|<=2`, `|s''|<=8`,

`|t|<=1/3`, `|t'|<=2`, `|t''|<=104/3`.

For example `s''=-8(1-18q+21q^2)/(1+q)^6` and `t''=(16/3)(1-46q+181q^2-108q^3)/(1+q)^8`, q=x^2. Positive-coefficient polynomial dominations give the asserted bounds.

Let

`D0=7307/3072`, `A2=3+2D0+D0^2`, `Bmax=539/48`.

Since A is even in Z, the cross term in (9) vanishes. Hence

`r0 <=(27/32)lambda^2`,

`e <=lambda^4 sqrt(A2+lambda^2 Bmax^2)`,              (10)

`U2 <=(lambda^2 s0+(4/3)lambda^4)^2`

`      +lambda^6(s0+sqrt(11)/3)^2`,                  (11)

`V2 <= L0^2[lambda^6(s0^2+4)+lambda^8(1/9+4)]`.      (12)

Insert (10)–(12) into (6). This is a completely explicit full-law upper bound for the actual four-query program. It remains nonvacuous without a mean or derivative runtime oracle.

The script reports the certified upper bounds at specified lambda and a, executes the legal four-value program with a counting oracle, and checks the polynomial residual identities exactly. Its floating simulations are implementation checks; they are not used to establish TV.

## 7. Conventional alternatives and the exact remaining gap

At fixed k, independent averaging of h values plus the same final Gaussian noise has error of order lambda^2 on this example, while (6)–(12) give order lambda^4 AFTER coefficient S is supplied. A characteristic-function lower bound proves the former order: at frequency `1/sqrt(1+a^2)`, use `1-cos(v)>=(1-cos(1))v^2` for |v|<=1 and `Var(k^-1 sum f)=Var(f)/k`.

Explicitly, define `I_n=E(1+G^2)^(-n)`. Gaussian integration by parts gives `I_2=1/2`, `I_3=(I_1+1)/4`, and `I_4=(I_1+3/2)/6`. Hence `E f^2=2 I_1/3>=1/3`, the last step by Jensen. For `lambda<=sqrt(1+a^2)`, the fixed-k raw-average lower bound is therefore

`TV >= exp(-1/2)(1-cos(1))lambda^2/[6(1+a^2)k]`.

For a=1/2 and k=4, the analytic certificates are:

| lambda | Actual four-query TV upper bound | Four raw values averaged: TV lower bound |
|---:|---:|---:|
| 0.05 | 1.196e-5 | 2.323e-5 |
| 0.02 | 2.961e-7 | 3.717e-6 |
| 0.01 | 1.842e-8 | 9.294e-7 |

The upper bounds are rounded upward and the lower bounds downward. The source model and constants, rather than observed sample moments, establish this comparison.

This is only an order diagnostic. If the exact displayed source family is supplied to an ordinary competitor, the known zero-mean reference lambda f can be subtracted: one value query recovers c, giving an exact target sampler. That is the strongest conventional alternative for this explicitly known family. No speedup over it is claimed. For a general unknown h, acquisition of a useful S is still the real missing work; the packet's fixed-exponent compiler, bounded-input FORS under its actual assumptions, Gaussian-cloud correction, and conventional control variates retain their own stronger or different acquired contracts.

The theorem closes a specified scalar divergence-correction replacement by actual values. It does not close general coefficient fitting, high-dimensional joint correction, polylogarithmic query complexity, historical novelty, or practical advantage. Every fit query, residual certification cost, arithmetic/storage cost, and joint adaptive-reuse error must still be charged.

If an independently fitted S is reused, each output still costs four new values. Conditional on the fit, fresh executions are independent. A conditional per-output TV bound epsilon gives at most M epsilon for M joint outputs, plus any probability that the fitting certificate fails. Unconditional independence must not be inferred from conditional independence under a common random fit.
