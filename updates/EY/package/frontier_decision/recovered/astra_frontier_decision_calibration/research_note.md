# ASTRA FRONTIER — Decision-matched sensing without Hamiltonian identification

**Investigation date:** 13 October 2026.  
**Status:** Research derivations, fresh numerical construction, and exact rational post-construction verification. No independent mathematical review, formal verification, historical-priority clearance, laboratory experiment, or universal efficient many-body inversion theorem.

## 0. Result and evidence boundary

The new output is a **measurement-to-control rule**, not a more accurate absolute transport number. For the same interacting quantum chain as the preceding investigation, fix hopping `t=1`, allow unknown parameters

\[
U\in[3.9,4.1],\qquad d\in[1.9,2.1],
\]

and choose the actual next-neighbour interaction `V` in `[0,3]`. The rule uses one local interference-measurement setting, repeated on independently prepared specimens. It does not estimate `U` and `d` separately, fit their posterior, or simulate a new many-body model after seeing the observations.

Conditional on this parameter box, the specified physical structure and error budgets, the following uniform guarantees are derived and checked:

| Decision-assay shots | Absolute global regret, with probability greater than 99% | Native interrogation time |
|---:|---:|---:|
| 262,144 | less than 0.000087804 | 131,072 |
| 1,048,576 | less than 0.000043428 | 524,288 |

Regret means

\[
\max_{0\le V\le3}D(V;U,d)-D(V_{\rm chosen};U,d),
\]

for the **actual** unknown model, not a posterior-average or worst-value objective. Preparation, reset, switching, calibration and readout are additional physical costs. No such assay was run on a device. The samples executed here are labelled synthetic tests.

A strict interface separation is also certified. Two admissible models yield exactly the same probability law for this chosen contrast, at every number of repetitions, while their absolute `D` values at the nominal control differ by more than **0.0203442**. The near-optimal decision can therefore be obtained from an observation that cannot consistently identify those parameters or that absolute response. This is not a lower bound against other experiments: a second quadrature would convey additional information.

Every fixed control chosen without observations has worst-case regret at least **0.00012390875** over the supplied box. Both listed policies improve on that bound. This comparator supplies only the common parameter box; it does not have another experiment's raw data.

The recorded offline construction/checking stages total **252.14 seconds**, with peak **1,967,736 KiB** (about 1.88 GiB), one BLAS thread. The dictionary was freshly acquired from span-eight enumeration, using previously written code and predetermined enrichment settings; no previously solved response packet was input. Model-development work and exploratory choice of settings are excluded. The result is a successful, paid construction on a nonperturbative uncertainty family, not a uniform termination bound for arbitrary quantum models.

## 1. Exact physical task

Use lattice spacing and hbar equal to one. The Hamiltonian and original noise are

\[
H(U,V)=-\frac12\sum_i(X_iX_{i+1}+Y_iY_{i+1})
 +\frac U4\sum_i Z_iZ_{i+1}+\frac V4\sum_i Z_iZ_{i+2},
\]
\[
\mathcal L_{U,V,d}O=i[H(U,V),O]
 +\frac d4\sum_i(Z_iOZ_i-O).
\]

No interaction is dropped, expanded to first order in its strength, or replaced by an effective rate model. The physical dephasing can be uncertain but is not artificially increased. The defining state is the normalized infinite-temperature product trace, including every particle-number sector. Set

\[
n_i=(I-Z_i)/2,\quad j_i=\tfrac12(X_iY_{i+1}-Y_iX_{i+1}),\quad\chi=1/4.
\]

The macroscopic output is

\[
D(U,V,d)=\lim_{T\to\infty}\frac1{2T\chi}
 \sum_xx^2\langle e^{T\mathcal L}(n_x-1/2),n_0-1/2\rangle.
\]

This is a second-moment coefficient, not a Gaussian hydrodynamic theorem, finite-temperature conductivity, ground-state property, or closed-system limit. The claimed scalar is not a finite-ring proxy. The same bounds separately hold for each periodic finite-ring coefficient `D_n` with `n>=41`, by the finite-packet transfer below.

The following remain physical inputs: known hopping and its time unit; the stated local interaction/noise structure; a calibrated control that can set `V` while keeping `U,d` fixed to the specified tolerance; and the ability to freeze hopping in the calibration region without changing relevant diagonal energies or the dephasing beyond a charged bias. Arbitrary nonlocal terms, nonunital noise, memory, spatial defects and uncalibrated hopping are not covered.

## 2. Mathematical object: a decision on measurement fibres

For an experiment with model-dependent mean `m(eta)`, define the exact fibre

\[
\Theta_y=\{\eta:m(\eta)=y\}.
\]

The relevant question is not whether this fibre contains a unique model. It is whether a single decision has small loss throughout the fibre. With finite-sample error `h`, replace it by the thickened fibre `|m(eta)-y|<=h`.

Let `F(u,eta)` be a performance objective, with `u` a small-dimensional control. Suppose a global-exclusion certificate places every model's maximizer in a region in which

\[
-\nabla_u^2F\succeq\mu I.
\]

If a proposed policy `u(y)` and the maximizer share that region, and a computable bound proves

\[
\|\nabla_uF(u(y),\eta)\|\le G
\]

uniformly on the thickened fibre, then

\[
\boxed{\max_uF(u,\eta)-F(u(y),\eta)\le G^2/(2\mu).}\tag{1}
\]

Proof: strong concavity bounds the objective increase at displacement `h` by `g.h-mu||h||^2/2`; maximizing that quadratic proves (1). Region membership and global exclusion are essential hypotheses to check, not inferred from the gradient at one point.

### 2.1 Why few measured combinations can suffice

At a nominal parameter and control, write

\[
A=F_{uu},\qquad B=F_{u\eta}.
\]

The compensation matrix

\[
C=-A^{-1}B
\]

has at most `dim(u)` rows. For an approximate `C`, suppose the control gradient at the base point has norm at most `delta0`, `||AC+B||<=delta1`, and its second directional derivative along `(C eta,eta)` has norm at most `L||(C eta,eta)||^2`. Then, for `||eta||<=rho`,

\[
\|F_u(u_0+C\eta,\eta)\|
\le\delta_0+\delta_1\rho+\tfrac L2(1+\|C\|^2)\rho^2.\tag{2}
\]

This is Taylor's theorem applied to the **optimality condition**, not to an entire state. If the measured adjustment differs from `C eta` by at most `e`, a bound `||F_uu||<=M` adds `Me`. Equation (1) then squares this total. Exact first-order cancellation leads to fourth-order loss in unmeasured nuisance radius, until numerical, statistical or model-error floors dominate.

The low row rank alone is not an algorithm: `A,B`, their validity region, a realizable sensor for `C eta`, and all remainders must be acquired. In addition, a local stationary point says nothing about competing distant optima. Tan and Frazier [1] already obtain cross-Hessian decision-risk bounds with a fourth-order remainder in estimate-then-optimize. These general principles are credited. The work here constructs and checks them for a degenerate-dissipation, thermodynamic quantum response and implements the required observation without identifying the nuisance vector.

The executed policy uses the exact nonlinear sensor law, not just (2). Its derivative bounds are checked throughout the complete uncertainty box.

## 3. Mixed quantum error derivatives, including uncertain physical noise

### 3.1 Conservation and fixed-reference normalization

Write `B_theta=S(d)+A(U,V)`, where `A=-i[H,.]` is skew and `S` is the positive dissipator. Let `R` be +1 on conjugation-odd Hermitian operators and -1 on conjugation-even operators. Then `Rj=j`, `RS=SR`, `RA=-AR`, and `RB` is symmetric.

Use finite translation-polynomial trials `f(theta),g(theta)`, odd and even respectively, with

\[
PA_0 f_\alpha=0\tag{3}
\]

for every trial coefficient. Here `A_0` is the hopping commutator. All diagonal-control commutators have zero population output, so (3) preserves exact balance throughout `theta=(V,U,d)`.

For the proof on a finite ring, introduce only the scalar resolvent regularizer `lambda>0`. Set

\[
S_{\rm ref}=S(2)+\lambda I,\qquad
T_{\theta,\lambda}=S_{\rm ref}^{-1/2}(B_\theta+\lambda I)S_{\rm ref}^{-1/2}.
\]

The reference is kept fixed while the physical `d` varies. Its real part satisfies

\[
\Re T_{\theta,\lambda}\succeq\beta I,
\qquad\beta=\min(1,d/2)>0,
\qquad\|T^{-1}\|\le\beta^{-1}.\tag{4}
\]

Indeed, off-diagonal damping ratios are `(dq/2+lambda)/(q+lambda)`, and the diagonal ratio is one. This is a known dissipative norm after normalization, not a supplied many-body relaxation rate.

For the two diagonal interaction directions and the noise direction,

\[
\|K_V\|\le1,\quad\|K_U\|\le1,\quad\|K_d\|\le1/2,
\quad K_i=\partial_iT.\tag{5}
\]

For a diagonal interaction, two configurations differing at `q` sites have energy difference at most `2 J_* q`, whereas their reference damping is `2q/2=q`; here `J_*=1/2`. The noise derivative is `S(2)/2` and gives the third bound. These operators annihilate diagonal inputs and do not create populations.

### 3.2 Exact corrected-output identity

Let `y=f+g` and define

\[
\mathcal F_\lambda=2\langle j,f\rangle
-\langle f,(S(d)+\lambda)f\rangle
+\langle g,(S(d)+\lambda)g\rangle
+2\langle Af,g\rangle.
\]

With normalized complete residual

\[
r_\lambda=S_{\rm ref}^{-1/2}[(B_\theta+\lambda)y-j],
\]

square completion using `(RB)^*=RB` yields

\[
\boxed{\kappa_{n,\lambda}-\mathcal F_\lambda
=\langle r_\lambda,R T^{-1}_{\theta,\lambda}r_\lambda\rangle.}\tag{6}
\]

The residual's population part is `lambda Pg`; its normalized norm tends to zero. This is exactly why (3) cannot be replaced by a small but nonzero population residual.

### 3.3 Multivariate derivative certificate

Let `alpha` be a multi-index in the axes `[V,U,d]`, and write `q_alpha=||partial^alpha r||` in the limiting reference `S(2)^+` norm. The trial has total polynomial order three; the complete residual has order four and all 35 residual coefficients are retained.

For affine `T`, the inverse derivative is a sum of `|c|!` ordered products. Equations (4)-(5) imply

\[
\|\partial^cT^{-1}\|
\le |c|!\,\beta^{-|c|-1}\prod_iw_i^{c_i},
\quad(w_V,w_U,w_d)=(1,1,1/2).
\]

Leibniz differentiation of (6) proves

\[
\boxed{
|\partial^\alpha(D-\widehat D)|\le
4\sum_{a+b+c=\alpha}
\frac{\alpha!\,|c|!}{a!b!c!}
\beta^{-|c|-1}w^c q_aq_b,
\qquad\widehat D=4\mathcal F.
}\tag{7}
\]

For the deployed control derivative, this specializes to

\[
E_1=4(2q_0q_V/\beta+q_0^2/\beta^2),\tag{8}
\]
\[
E_2=4(2q_0q_{VV}/\beta+2q_V^2/\beta
+4q_0q_V/\beta^2+2q_0^2/\beta^3).\tag{9}
\]

No Galerkin orthogonality or optimally solved trial is required. Exact rational residual Gram matrices provide polynomial squared norms, including their cross terms. Centered-box coefficient bounds, sometimes applied to a finite partition, enclose these polynomials. Rational upward square roots give the `q` bounds.

A nonlinear proposed policy can be substituted into these finite polynomials. This retains correlation between controls and uncertainty; independent value intervals are not subtracted.

### 3.4 Infinite-system validity

All trial and full commutator words have footprint at most twenty. Their translation-covariance inner products equal their per-site ring inner products exactly for `n>40`: the long empty complementary arc makes distinct finite translation words distinguishable without wraparound. Thus all finite residual identities stabilize on every `n>=41`.

At fixed `lambda>0`, finite-time locality [6] and contractivity give the thermodynamic limit of the Laplace-transformed current correlation. For real parameters in the uncertainty box, (4)-(5) also give a uniform complex neighbourhood `sum_i w_i |s_i|<beta` on which the normalized inverse is bounded. The normalized current has squared norm at most `1/4`. Normal-family uniqueness therefore passes each parameter derivative through the fixed-lambda size limit, then the `lambda` limit. The finite population residual vanishes as above.

For clarity, the last scalar is the physical second-moment coefficient, not an abstract inverse. The parity Schur operator at positive lambda is

\[
S_o+\lambda+C_{eo}^*(S_e+\lambda)^{-1}C_{eo}.
\]

Subtracting `lambda I` makes this monotone as lambda decreases, while its lower bound `dI` controls the difference of the two inverses by `lambda a/d^2`, where `a=1/2`. This gives the finite zero-Laplace limit in infinite volume. The evenly extended stationary current correlation has a positive even spectral measure `nu`. For `nu_s(E)=nu(sE)/s`, the Poisson transforms converge to that limit and

\[
\int_{|y|>R}y^{-2}\,d\nu_s(y)\le2a/(Rd).
\]

Uniqueness of the even Stieltjes transform and this tail bound permit integration against `2(1-cos y)/y^2`. The continuity equation gives the second derivative of the density second moment as twice the current correlation, proving `D=4 kappa_0`. This is the inherited thermodynamic argument with its original scope; the uncertain-noise derivative extension is justified by the uniform neighbourhood above. No unregularized size/time limits are exchanged, and no Gaussian-profile conclusion is asserted.

## 4. Constructing the finite response family

The previously written translation-orbit compiler was reused, but the reported run starts from enumeration of all permitted reflection-paired words through footprint eight. Ten full-residual-driven enrichment steps acquire the final dictionaries, capped at footprint eighteen. This is a heuristic discovery rule, not an assumed compact solution or uniform convergence theorem.

For each multivariate derivative alpha, the right-hand side contains the known sum

\[
-\sum_i\alpha_i B_i y_{\alpha-e_i}.
\]

The same two reference least-squares matrices, separated by parity and exact balance, are reused. Twenty derivative vectors through total order three are solved. At the proof stage every residual coefficient through order four is regenerated, whether or not its word occurs in the discovery dictionary.

Final basis sizes are 53,088 and 53,024. The six interaction/derivative commutator matrices contain 3,540,695 nonzeros. The saved exact packet contains 1,056,586 nonzero lower-field derivative coefficients and 1,060,478 upper-field coefficients, each in a reflection-paired translation basis. This is about 7.50 MB compressed.

Only free lower-field coordinates are dyadically rounded; dependent coordinates are reconstructed through the exact rational nullspace. This preserves (3). The verifier checks every population row, exact polynomial values and complete residual Gram matrices. Integer products use a checked 14-bit limb scheme: each binary64 limb product and every absolute partial sum are below `2^52`, so the product is exact; the final limb combination uses arbitrary-precision integers. Independent Python-integer tests verify that implementation. Overflow and footprint guards reject unsupported inputs.

No full state, many-body eigenbasis, tensor-rank promise or sampled equilibrium ensemble is supplied to this computation.

## 5. Compile a sensor for the decision direction

Let

\[
V_0=1109/512.
\]

The corrected Hessian proposes an optimum-compensation direction near

\[
(\partial_UV_*,\partial_dV_*)\approx(0.60955,-0.07682).
\]

That numerical derivative is used only to select a candidate. The final policy is checked over the full uncertainty box; it does not rely on that numerical approximation being exact.

The compiler rounds and searches finite Pythagorean readout directions, selecting

\[
c_U=39/64,\qquad c_d=-13/170,
\qquad c=3341/5440,
\quad c^2=c_U^2+c_d^2.\tag{10}
\]

The first-order control is `V0+c_U(U-4)+c_d(d-2)`. This low-dimensional object is not a full model reconstruction.

### 5.1 Physically specified contrast

Freeze hopping incident on six consecutive spins while preserving diagonal interactions and original dephasing to the stated expectation-bias allowance. Prepare the middle pair in

\[
(|10\rangle+|01\rangle)/\sqrt2,
\]

and the four neighbours with

\[
n_{-2}=n_{-1}=1,\qquad n_2=n_3=0.
\]

The diagonal energy difference for the two central configurations is exactly

\[
(U-V)(n_{-1}-n_2)+V(n_{-2}-n_3)=U.
\]

Thus the probe phase is independent of the control `V`. The coherence differs on two sites and decays at exactly the physical rate `d`.

Set interrogation time `tau=1/2` and choose the logical readout quadrature with

\[
\cos\psi=32/257,\qquad\sin\psi=-255/257,
\]

relative to the known nominal phase `U0 tau=2`. Each ideal outcome `X` is +1 or -1 with

\[
\boxed{\mu(U,d)=\mathbb E X=e^{-d/2}\cos((U-4)/2+\psi).}\tag{11}
\]

Prepare independently for each shot. These are local coherent preparations and measurements, not passive occurrences in an equilibrium distribution. Their work, timing, reset and switching costs are real resources.

Define

\[
S=2ec=3341e/2720,\qquad S\mu(4,2)=13/85.
\]

The program stores the rational approximation

\[
\widehat S=14340421443/4294967296,
\]

with rigorously bounded error below `2^-32`. Given the empirical mean `Xbar`, compute

\[
\boxed{
V_{\rm cmd}=\operatorname{clip}_{[0,3]}
\operatorname{round}_{1/2048}
\left(V_0+\widehat S\,\bar X-13/85\right).
}\tag{12}
\]

The actuator is allowed an additional error at most `1/4096` around that command. Rounding plus actuator error is therefore at most `1/2048`. No nuisance estimate or online many-body solve is used.

### 5.2 Matched one-copy measurement comparison

At the nominal point, rotate the known phase away. The logical qubit has Bloch vector `(r,0,0)`, `r=e^-1`. Its derivatives are `partial_U rho=r tau Y/2` and `partial_d rho=-r tau X/2`.

For a locally unbiased estimator of `c_U deltaU+c_d deltad`, any first-moment observable `L=l0 I+lx X+ly Y+lz Z` must satisfy

\[
l_x=-c_d/(r\tau),\quad l_y=c_U/(r\tau),\quad l_0=c_d/\tau.
\]

Its variance is minimized at `lz=0`, giving

\[
\boxed{\operatorname{Var}_{\rm min}
=\tau^{-2}\left((c_U^2+c_d^2)/r^2-c_d^2\right)
\approx11.12479246.}\tag{13}
\]

For a general POVM and its estimator, the second-moment operator is at least the square of its first-moment operator, by the operator Schwarz inequality. Consequently the same lower bound applies to every one-copy POVM that is locally unbiased for this scalar. Spectral measurement of `L`, exactly (11)-(12) before sample averaging and rounding, attains it.

This is an elementary instance of established quantum nuisance-parameter/semiparametric estimation [4], not a new quantum metrological bound. It is only local, at the nominal point and fixed preparation/time. No global finite-sample or collective-measurement optimality is claimed.

## 6. Finite-box, finite-shot proof

Put `a=U-4`, `b=d-2`, so `|a|,|b|<=1/10`. The ideal mean-to-control shift is

\[
s(a,b)=2c\left[e^{-b/2}
\left(\frac{32}{257}\cos(a/2)+\frac{255}{257}\sin(a/2)\right)
-\frac{32}{257}\right].\tag{14}
\]

The exact cubic polynomial used in the certificate is

\[
\begin{aligned}
s_3(a,b)={}&\frac{39}{64}a-\frac{13}{170}b
-\frac{39}{128}ab-\frac{13}{680}a^2+\frac{13}{680}b^2\\
&+\frac{39}{512}ab^2+\frac{13}{1360}a^2b
-\frac{13}{512}a^3-\frac{13}{4080}b^3.
\end{aligned}\tag{15}
\]

This is a Taylor approximation of the **known local measurement law**, not of the unknown many-body response. With `z=(-b+ia)/2`, `|z|<=1/10`; the exponential remainder gives

\[
|s-s_3|\le\frac{2c(10/9)(1/10)^4}{24}.\tag{16}
\]

The use of `exp(1/10)<=10/9` is an elementary geometric-series bound.

Suppose the mean of actual outcomes differs from (11) by at most `10^-4`, incorporating calibrated preparation, switching, axis, timing and readout effects. For `N` independent bounded outcomes,

\[
\Pr(|\bar X-\mathbb E X|>h)\le2e^{-Nh^2/2}.
\]

Use `(N,h)=(2^18,13/2000)` or `(2^20,13/4000)`. Both have `Nh^2/2=5.537792`. Exact positive Taylor sums show its exponential exceeds 250; the failure probability is actually below 0.008, and the reported bound conservatively states greater than 99% coverage.

On that event, the actual control differs from `V0+s3(a,b)` by at most

\[
S_U(h+10^{-4})+\frac1{2048}+2^{-32}
+\frac{2c(10/9)(1/10)^4}{24},\tag{17}
\]

where `S_U` is an explicit rational upper enclosure of `S`. The two totals are below `0.023` and `0.012`, respectively. Clipping does not activate on the good event, since the complete certified control tube lies inside `(2,2.5)`.

Substitute `V=V0+s3(a,b)+e` into all corrected-gradient and residual polynomials. Exact rational box bounds on `|a|,|b|<=.1` and `|e|<=.023` or `.012`, together with (8)-(9), give:

| Tube | Bound on absolute true control gradient | Curvature bound used for regret |
|---:|---:|---:|
| 0.023 | 0.003651315584 | `D_VV <= -0.07592003516` |
| 0.012 | 0.002567883056 | same root-containing 0.023 tube |

At the centre of each such tube the absolute gradient is below the curvature times `0.023`, so the unique root belongs to the larger tube. Both the actual root and either deployed control share the region to which (1) applies. Squaring the exact gradient bounds proves the policy table in Section 0.

### 6.1 Globality and uniqueness over every unknown model

The result does not assume the objective is globally concave. Four newly constructed small anchor families give a positive `D_V` on `[0,1.75]` for every `U,d` in the box. The central family gives a positive derivative on `[1.75,2]`, a negative derivative on `[2.5,3]`, and

\[
-0.108942 <D_{VV}<-0.0628181
\quad(2\le V\le2.5)
\]

uniformly on the box. Therefore each true model has exactly one global maximizer on `[0,3]`, inside `(2,2.5)`. The tighter tube curvature then supplies the stated regret. Two additional attempted small anchors were not sharp enough; their computation is charged, but they are not used in the proof.

## 7. An exact separation between model prediction and a good decision

For `a=+1/100` or `-1/100`, define

\[
U_a=4+a,\qquad
 d_a=2+2\log\left[\cos(a/2)+\frac{255}{32}\sin(a/2)\right].\tag{18}
\]

Both lie inside the uncertainty box. Substitution into (11) gives exactly

\[
\mu(U_a,d_a)=e^{-1}\,32/257.
\]

The entire Bernoulli observation law is identical for the two models, and so are all finite products of that law.

Rational sine/cosine Taylor enclosures and an atanh-series logarithm enclosure place the parameters and macroscopic values in:

| U | Rigorous d enclosure | Rigorous D(V0) enclosure, decimals outward |
|---:|---:|---:|
| 3.99 | [1.918655813574, 1.918655813575] | [0.6134535792, 0.6137844323] |
| 4.01 | [2.078116561482, 2.078116561483] | [0.5928974757, 0.5931093049] |

The exact value intervals differ by more than **0.0203442744**. These values are obtained from the physical response certificates, not from the two-level calibration model.

Any estimator based only on repeated observations of this contrast has the same distribution in both cases. If its required absolute-response tolerance is less than half that separation, the two success intervals are disjoint; their success probabilities sum to at most one. In particular, no such estimator can uniformly achieve 99% success. The certified decision policy, in contrast, succeeds with its stated regret for both models and every other model in the box.

This is not an assertion that these Hamiltonians are indistinguishable by all experiments. The optional coarse calibration below and a second fine quadrature use a different information interface. The separation concerns the **new decision assay once the common parameter box is supplied**, not an arbitrarily rich combined laboratory record.

## 8. A no-observation comparison with a proved lower bound

For `(U,d)=(3.9,2.1)`, the true derivative at `V=2.104` is negative. For `(4.1,1.9)`, the derivative at `V=2.223` is positive. Exact certificates also give

\[
D_{VV}<-0.07\quad\text{on }[2.1,2.24]
\]

for every model in the box.

Let `m=(2.104+2.223)/2`. For any fixed action `V<=m`, the second model has its optimizer to the right of `2.223`. Integrating the gradient lower bound between `m` and `2.223` gives loss at least `0.07(2.223-m)^2/2`; taking `V` still further left cannot improve it by the already certified global monotonicity. For `V>=m`, apply the symmetric argument to the first model.

Hence every deterministic action selected from only the common box obeys

\[
\boxed{\sup_{U,d}\operatorname{regret}(V;U,d)
\ge\frac{(7/100)(119/1000)^2}{8}
=0.00012390875.}\tag{19}
\]

This lower bound is smaller than a naive independent-value uncertainty yet larger than both sensor-policy upper bounds. It is a matched information comparison against fixed controls, not against all active sensing strategies or an optimal two-quadrature estimator.

## 9. Acquiring the coarse box rather than declaring it free

The main guarantee is conditional on a valid uncertainty box. An optional explicitly budgeted coarse procedure is supplied to establish that box, with a possible **inconclusive** result.

Start only from the broader structural bounds `U in [0,8]`, `d in [1,4]`. The same pair preparation has two orthogonal Ramsey means at `tau_c=1/8`:

\[
x=e^{-d/8}\cos(U/8),\qquad y=e^{-d/8}\sin(U/8).
\]

There is no phase wrapping over the supplied U range. Use `2^20` independent shots per axis and statistical radius `1/250`; allow a known mean bias of `1/10000` per axis. Exact exponential bounds give joint statistical failure below `1/1000`.

The Euclidean error of the measured contrast vector is at most `5799/10^6`, whereas its true radius is greater than `3/5`. Elementary angular and logarithmic bounds therefore give parameter error at most

\[
\frac{8(5799/10^6)}{3/5-5799/10^6}<0.079.
\]

Interval square roots, a half-angle arctangent series and an atanh logarithm series construct a rigorous outward box around the two estimates. Accept only when that entire box is contained in `[3.9,4.1] x [1.9,2.1]`. Otherwise return inconclusive; do not silently use the narrow certificate. The code supplies this test and labelled synthetic counts demonstrating one accepted run.

This optional stage uses **2,097,152 shots**, **262,144 native time units**, plus all preparations/switches/readouts. Combining its failure bound with the decision assay's sharper `<0.008` bound gives

\[
\Pr(\text{accept coarse calibration and return a bad decision})<0.009.
\]

That is an unconditional soundness-of-acceptance guarantee. It is **not** a bound on failure conditional on a rare acceptance event, and no acceptance probability for every broad-prior model is claimed. Structural model validity, hopping calibration and valid bias budgets remain separate.

The extra coarse observations would convey information not present in the one-contrast nonidentifiability example. The fine decision rule only needs the certified box from this stage; claiming the entire two-stage raw record is identical between (18)'s models would be false.

## 10. Resource accounting and verification

Recorded construction/checking stages:

| Stage | Seconds |
|---|---:|
| Fresh span-eight dictionary acquisition and nominal response construction | 179.8333 |
| Twenty mixed V,U,d derivative solves | 46.4836 |
| Exact multivariate packet construction | 13.0620 |
| Six fresh anchor families, including two unused attempts | 9.0969 |
| Whole-domain policy, confidence and comparison certificate | 3.6676 |
| Sum | 252.1435 |

Peak memory is about 1.88 GiB. The stages were recorded separately, not by one stopwatch including intervening research. A standalone reconstruction of all seven exact multivariate packets without optimisation took 16.9518 seconds. Compiler caches, software versions and precise metadata are recorded in `results/resource_ledger.json`. Fixed centres and enrichment choices were selected during development, which is excluded from the timings.

At deployment the command requires only an integer count, rational arithmetic and one quantized control setting. There is no new quantum-response solve per observed model. No virtual experiment supplies actual laboratory data for free: all actual shots and calibrations remain to be performed.

The exact arithmetic work is polynomial in the explicit dictionary, derivative count, commutator nonzeros and rational bit lengths. At total derivative order M in q parameters, the number of trial derivatives is `binomial(q+M,M)`, and fixed dictionaries reuse the same two matrices. This is not a bound on the cost of finding adequate dictionaries as q or accuracy grows. The finite polynomial box checks are also explicitly charged; generic high-dimensional global optimization has not become easy.

### Executed checks

- Every exact multivariate packet was rebuilt from saved rational coefficients without invoking the optimizer. All full Grams, polynomial values, balance conditions and metadata matched.
- Twenty checked integer-limb products were compared with independent arbitrary-precision matrix products, including 60-bit signed inputs. Nine physical corrected-output/residual polynomial evaluations were independently contracted from the actual quantum trial fields at noncentral parameters; an injected population defect was rejected.
- A separate exact four-dimensional degenerate-dissipation model verified the residual identity with uncertain physical damping; 240 mixed derivative checks passed on its parameter family.
- Nine exact six-site diagonal-energy calculations verified cancellation of V from the calibration phase. Forty direct two-level Lindbladian calculations verified the Ramsey law.
- Two hundred sensor-series checks and two hundred rational polynomial-envelope checks passed.
- Ten synthetic policy trials, covering five nuisance settings and both shot budgets, were run as binomial simulations. Their physical regret upper bounds were recomputed from the quantum certificates. No true optimizer was assumed in these checks.
- One optional coarse-calibration run was generated from synthetic quadrature counts and accepted by the interval code.

An early exact-compiler implementation had a NumPy-integer denominator overflow; it was repaired by promotion to Python arbitrary-precision integers before producing the accepted packets. Zero-order handling in a symbolic test and formatting of very long coarse-calibration rationals were corrected before the final tests passed. These failures are implementation details, not discarded physical counterexamples.

## 11. Matched prior-art assessment

**Estimate-then-optimize:** Tan and Frazier [1], Theorem 3.4, already bound regret through a squared cross-Hessian parameter error and a fourth-order remainder. Their experimental-design objective accounts for decision-relevant directions. Thus the rank of `F_ueta`, nuisance cancellation and quartic local loss are not claimed as new general mathematical facts. Here no consistent estimate of the nuisance vector is required by deployment; a concrete local observation law and finite model-wise regret are certified using full thermodynamic quantum residuals.

**Goal-driven Bayesian experiment design:** Go, Qian and Yoon [2] combine an amortized variational posterior with a convex decision layer and study task-irrelevant parameter directions. Their theory assumes the relevant subspace structure and their applications have different physical interfaces. This run constructs a particular sensor direction and checks its nonlinear fibres, without a posterior surrogate or assumed global convexity. It does not claim to supersede their more general Bayesian framework.

**Goal-oriented reduced models and adjoints:** Janon, Nodet and Prieur [3] explicitly discuss corrected outputs, primal/dual residuals and online/offline computation. The corrected-output strategy is established. The new derivation's scope is a degenerate quantum dissipator, varying noise, exact population cancellation and infinite-system sensitivity; no external coercivity oracle or full-system snapshot is supplied.

**Quantum semiparametric estimation:** Tsang, Albarelli and Datta [4] study selected functionals with nuisance dimensions and asymptotic attainability. The one-copy bound (13) is a basic specialization reconstructed directly, not a new universal quantum bound. The finite uncertainty box and physical control-regret certificate are additional operational requirements.

**Hamiltonian learning:** Huang, Tong, Fang and Su [5] give efficient, actively controlled Hamiltonian learning with Heisenberg-limited scaling under their interface. It would be false to assert that full learning always needs tomography or exponential resources. Two quadratures can identify the two parameters in this local probe model. No sample-complexity superiority over the strongest allowed two-quadrature or coherent-learning protocol is established. The rigorous separation is for the particular one-contrast data law.

**Specialised transport algorithms:** Backflow and tensor-network approaches [7] remain strong numerical baselines. No independently optimized implementation was timed head-to-head. The comparisons actually proved are the no-observation lower bound and exact nonidentifiability of the chosen experiment for absolute D, at matched information access.

Historical priority of the combined quantum certificate-to-sensor-to-policy operation is unknown. No source is used as an unreviewed premise for the specific new finite-dimensional identities.

## 12. Research-capital provenance and remaining theorem

The complete attached response-error note and checkpoint were read. The nominal one-parameter design proof is retained as research capital, not treated as external validation. Its compiler modules are copied with explicit provenance; fresh coefficients, mixed derivative matrices and the policy were computed in this run.

Astra main was fetched at `74c2843bd224c2975c6e46735b30ae7c927f948b`. That record still treats compressed conservation and the inverse-rank gate as unreviewed/open. A targeted `openai/math` search for decision/regret/sensitivity returned no matching files; that is not an exhaustive literature search or a novelty certificate. No theorem from that repository was imported, no Lean build was run, and neither repository was modified.

The result is a restricted but concrete new output-specific capability: a uniform, acquisition-accounted control decision over a two-parameter family of strongly interacting models, even though its chosen assay cannot identify the model or its absolute transport response.

What remains open is a general **constructive decision complexity theorem**: from a specified broader physical model and accessible experiment set, construct sufficiently accurate conservation-safe decision residuals and a realizable low-dimensional measurement map at bounded total cost. A low-rank decision Jacobian alone does not guarantee a useful global policy, cheap calibration, or small trial dictionary. Competing optima, large nuisance ranges, phase ambiguity and unobserved physical effects can destroy the reduction.

No civilisation-scale capability, arbitrary high-dimensional materials design, finite-temperature result, generic many-body inverse compression, laboratory validation or universal resource superiority is established.

## Primary sources consulted

[1] Samuel Tan and Peter I. Frazier, *Regret Bounds and Experimental Design for Estimate-then-Optimize*, arXiv:2210.15576v1 (2022). Full HTML, including Theorem 3.4 and experimental-design section, inspected. https://arxiv.org/html/2210.15576v1

[2] Jinwoo Go, Xiaoning Qian and Byung-Jun Yoon, *Goal-driven Bayesian Optimal Experimental Design for Robust Decision-Making Under Model Uncertainty*, arXiv:2605.26093v1 (25 May 2026). Full HTML, formulation and stated subspace scope inspected. https://arxiv.org/html/2605.26093v1

[3] Alexandre Janon, Maelle Nodet and Clementine Prieur, *Goal-oriented error estimation for the reduced basis method, with application to sensitivity analysis*, arXiv:1303.6618v2 (2014). Full HTML, Sections 1.1-1.4 inspected. https://arxiv.org/html/1303.6618v2

[4] Mankei Tsang, Francesco Albarelli and Animesh Datta, *Quantum Semiparametric Estimation*, Physical Review X 10, 031023 (2020); arXiv:1906.09871v7, including later post-publication notes. Primary HTML inspected. https://arxiv.org/html/1906.09871v7

[5] Hsin-Yuan Huang, Yu Tong, Di Fang and Yuan Su, *Learning many-body Hamiltonians with Heisenberg-limited scaling*, arXiv:2210.03030 (2022), PRL 130, 200403 (2023). Primary abstract inspected; its theorem is not imported. https://arxiv.org/abs/2210.03030

[6] Thomas Barthel and Martin Kliesch, *Quasi-locality and efficient simulation of Markovian quantum dynamics*, PRL 108, 230504 (2012), arXiv:1111.4210. Finite-time locality only, not a supplied mixing theorem. https://arxiv.org/abs/1111.4210

[7] C. W. von Keyserlingk, Frank Pollmann and Tibor Rakovszky, *Operator backflow and the classical simulation of quantum transport*, PRB 105, 245101 (2022), arXiv:2111.09904. https://arxiv.org/abs/2111.09904
