# Independent focused review of the OA029 retuning

Review status: **the zero-detector, disk reciprocal, and contour-height interfaces pass this focused attack conditional on the printed source identities. The proposed zero-free theorem and arbitrary-field extension are not cleared.** No concrete new fatal defect was found in the reviewed dependency. The outstanding gate is the exact normalized theta/Whittaker/reflection architecture, including its applicability outside the declared cyclotomic scope. This verdict is separate from both the arithmetic schedule certificate and external theorem validation.

Inputs were `number_theory_algorithms/RETUNING_PROOF.md`, its `schedule_certificate.json`, and the exact copied family-029 TeX at OpenAI commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. File hashes and sizes are frozen in `retuning_review_inputs.json`. Independent exact arithmetic for the focused margins and open boxes is in `retuning_independent_arithmetic.json`. Neither artifact validates an analytic identity. I did not modify sibling files, run their certificate writer, or re-derive the full theta algebra.

## The dependency attacked

The consequential new contour is `Re xi = .919`, far left of the source's `.998`. Its legal use requires a reciprocal bound uniformly over each nonexceptional row and every height on the shifted finite contour. A detector exponent alone would not establish that. The chain that must survive is:

1. detect every nonprincipal denominator zero with real part at least `.917` and height at most `4 U^rho`;
2. leave at most `O(U^.61)` exceptional rows;
3. obtain `1/L = O_epsilon(U^epsilon)` at all points with `Re xi >= .919` and `|Im xi| <= 2 U^rho`;
4. shift the central contour and its horizontal edges inside that rectangle;
5. bound the discarded original tails using the original right line, without asserting the reciprocal estimate outside its rectangle.

The source supplies each component as a proof rather than a black-box zero-free theorem. The relevant printed interfaces are `029_06-zero-free.tex:13–30` (distinct primitive row characters and conductor count), `37–136` (conductor sieve), `139–163` (conservative convexity and omitted factors), `187–333` (detector), `335–366` (disk argument), and `389–411,562–601` (height decay and legal truncated contour shift).

## Detector and family uniformity

Keep the inverse polynomial truncated at norm `U^2`. Its product coefficients satisfy `alpha_U(1)=1`, vanish for `1 < Norm n <= U^2`, are independent of the row character, and satisfy the fixed-field divisor bound. This independence matters: the common coefficient mass can be put into the conductor sieve. These facts are printed at `029_06-zero-free.tex:192–214` and do not depend on the smoothing exponent.

With smoothing length `U^(181/50)` and a zero `beta+i gamma`, move the smoothing Mellin line to `Re v = 1/2-beta`. For `.917 <= beta <= 1`, this line is in `[-.5,-.417]`; exactly one gamma pole is crossed, at zero, and its residue is zero because it includes `L(beta+i gamma)`. The denominator character is nonprincipal, so its L-function introduces no pole. The inverse polynomial costs `O_F(U)` and the source conservative convexity costs `U^(1/2+epsilon)(2+|gamma|)^A_F`. Therefore the shifted integral is

\[
O\bigl(U^{-477/50000+A_F\rho+\epsilon}\bigr).
\]

The source bound is valid on fixed strips including `Re L = 1/2`, with `A_F` depending only on the fixed field; it is not obtained from any unproved zero-free input. Choose once for fixed `F,S,eta`

\[
0<\rho<\min\{.001,.002/(A_F+1)\}.
\]

Then `A_F rho < .002`. Choosing the detector loss below `.001` leaves a negative exponent below `-.00654`. Gamma decay also controls the horizontal limits uniformly in `beta` on this compact interval. The tail past `U^3.63` is bounded by a fixed power times `exp(-c U^.01)`. This proves the required cancellation of the unit coefficient uniformly throughout the zero rectangle for sufficiently large `U` depending on the fixed data.

The retained weight `t^(.917-beta) exp(-t/U^3.62)` is decreasing and at most one, so a dyadic prefix must have modulus at least a constant times `1/log U`. The binary-prefix estimate costs logarithms; the height Sobolev bound costs `U^rho` and logarithms. The squared coefficient mass and conductor sieve then cost

\[
(N+U^2)N^{1-2(.917)+\epsilon}
\ll U^{3.63(2-2(.917))+O(\epsilon)}
=U^{.60258+O(\epsilon)}.
\]

The density margin is `.61-.60258=.00742`. With `rho<.001`, the remaining sieve/divisor/logarithmic losses can be chosen below `.00642`. Distinct primitive characters convert this character count to a row count; the at most one principal denominator row is included separately. There is no additional power depending on field degree: ideal counts, divisor bounds, and the finite S-component partition contribute fixed-field constants or arbitrary small powers. This is fixed-field uniformity over the family; it is **not** uniform constants over all fields.

## Reciprocal bound and legal truncation

Use the four proposed disk radii centered at `2+i t`: outer radius `1.0825`, Borel–Carathéodory radius `1.082`, three-circles target radius `1.081`, and Euler radius `.999`. The outer left edge is `.9175`, strictly inside the detected zero-free rectangle. For `|t|<=2T`, `T=U^rho`, its height lies below `4T` once `U` exceeds a fixed threshold. The logarithm branch is fixed by the Euler value at the center. Conservative convexity gives a real-part upper bound `C_F log U` on the outer disk, and the center value is bounded independently of the character and height.

Borel–Carathéodory bounds `log L` by `O_F(log U)` on radius `1.082`. On radius `.999`, the entire disk lies in `Re s>=1.001`; the Euler logarithm is bounded uniformly. Three circles gives

\[
|\log L|\ll_F(\log U)^\theta,\qquad
\theta=\frac{\log(1.081/.999)}{\log(1.082/.999)}
\approx .9884147062<1.
\]

The target disk reaches `.919` at height `t`, and rightward Euler convergence covers the remaining real parts. Consequently `exp(C_F(log U)^theta) = O_{F,epsilon}(U^epsilon)` uniformly on the required contour rectangle. Omitting factors at conductor primes costs only another arbitrary small power because the real part is bounded away from zero. The small gap `1-theta` can make the threshold enormous; it does not invalidate the asymptotic exponent statement.

For the central shift, truncate at `|Im xi|=U^rho`; all horizontal edges remain inside the rectangle where the reciprocal bound holds. The discarded original tails stay on `Re xi>1`, where absolute Euler convergence bounds the reciprocal. The source's decay

\[
e^{-(\Im\xi+\Im z)^2}(1+|\Im z|)^{-A}(1+|\Im w|)^{-A}
\]

is not Gaussian decay in `xi` alone. Its convolution in `z,w` supplies arbitrary polynomial decay in the remaining `xi` height after choosing `A`. This yields a factor `U^(-rho A1)`. Since the candidate applies this only for `U>Z^.13`, choosing `A1>1/rho` after `rho` is fixed supplies more than `.13` extra saving in the Z exponent. The constants depend on those choices, but not on `Z,U` or the row. This checks the relevant uniformity and avoids moving an infinite contour through unprotected heights.

## Euler region corroboration

The printed good-prime closed factor at `029_05-poisson.tex:645–699` gives the five correction terms used by the candidate. The bad-prime estimates at `701–740` give the additional two restrictions. I independently decreased each endpoint of all three proposed boxes by `10^-5`; every required margin still exceeds `1/4000`. The smallest is

\[
(.919-10^{-5})+(.082-10^{-5})-1=.00098.
\]

Thus there is a real open neighborhood on which the product converges normally, uniformly in height. Positivity of all real parameters also keeps `1-V`, `1-W`, `1-D1`, and `1-E1` away from zero after a fixed prime cutoff. The principal row has no bad primes; a fixed enlargement of S makes all its good factors nonzero, yielding the required nonvanishing `H_eta(s)` down to `.98`. The cutoff must be chosen before reconstructing the arithmetic/coefficient family, as explicitly permitted at `029_02-arithmetic.tex:17–35`. Its existence here follows from the absolute local bounds, not from a cutoff that varies with summation variables.

This corroborates the proposed new local region. It does not independently derive the good-prime formula from the theta coefficients; that remains part of the unresolved source gate.

## General-field scope and verdict boundary

The published source explicitly declares F cyclotomic at `029_02-arithmetic.tex:8` and again in `029_03-theta.tex:15`. The stronger general-field conclusion is an extension proposed by the agent, not a theorem supplied by the release.

In the inspected arithmetic interface, no new cyclotomic obstruction appeared. For any F containing `mu12`, all archimedean places are complex, exterior residue fields contain `mu12`, S-principalization is available, and the norm to `Q(omega)` exists. In particular the Gauss correction at `029_02-arithmetic.tex:491–521` uses `Lambda=Lambda_Q(omega) o Norm_F/Q(omega)` and a residue-degree Davenport–Hasse lifting calculation. That calculation does not require F to be Galois or abelian over `Q(omega)`. Its infinity types are angular exponents `+1` or `-1`, so it does not introduce a degree-dependent radial power. The fixed-field norm-sheet bounds at `029_03-theta.tex:503–548` likewise preserve the power exponents while allowing field-dependent constants. In exact Gaussian smoothing, the reciprocal gamma product is raised to the finite number r of complex places (`680–735`); the Gaussian still dominates its height growth for each fixed r.

The actual field-extension gate is stronger: the exact theta proposition `029_03-theta.tex:47–174` must hold with the printed scalar quotient, inducing datum, cocycle orientation, normalized local values, global Whittaker factorization, complex Bessel normalization, and Weyl action for every F containing `mu12`. In particular, the prime cube-step factor `q_p^-1`, the `e=3k+1` Gauss phase, and the unit exponent must be the same identities used in the reflected coefficient. Ordinary existence of an exceptional representation is insufficient. The appendix at `029_10-whittaker-calculation.tex:72–171` cites Kazhdan–Patterson and addresses a global erratum, but I have not independently replayed those primary-source identifications or the reflected expansion. This review therefore **does not clear arbitrary-field applicability**.

Conditionally, if that exact architecture is valid for every F containing `mu12`, the final passage to an arbitrary K is sound: `F=K(mu12)` is abelian over K of degree at most four, and the finite-order norm-pullback L-function factors as the product of `L_K(s,chi psi)` over the extension characters. Away from s=1 the Hecke factors have no poles, so a target zero cannot cancel. The ordinary s=1 nonvanishing statement handles that point. This formal transfer adds no new zero-free hypothesis, but it cannot supply the missing architecture.

The certificate's rational inequalities are internally feasible; the decisive detector/reciprocal/truncation dependency survives this focused reconstruction. The admissible conclusion remains: **a conditional `.98` strip deduction from exact source identities, with a conditional arbitrary-field extension.** Neither the fixed `.98` boundary nor its downstream complexity consequences should be represented as independently validated mathematics yet. Extremely large contour, smoothing, and subpower constants also remain unquantified; this review supplies no practical onset or local resource bound.

A minor notation repair is advisable: the candidate's `eta=10^-7` initial-line displacement collides with its target Hecke character eta. Rename the displacement `delta_init`. This does not affect the mathematics.
