# Unknown gains with only first local motion: two channel-level barriers

The full unknown-gain question remains **OPEN** in this continuation. All error norms below use the task's convention without a factor of one half. This work proves a resource-independent obstruction for protocols built only from the checkpoint's clean cubic rotations, and a separate first-motion obstruction for fixed-shape higher-order words. A concrete palindromic degree-five family is shown to lose essentially all distinguishability of a pair of data states before its useful angle accumulates. These are scoped obstructions, not an all-policy impossibility theorem.

The scientific target is still one gain-independent implementation of `E=exp(-i pi Z1 X2/4)`, uniformly over static gains in `[1,2]^3`, all admitted coin-independent moving baths, and all correlated inputs. No calibration, preparation, measurement, bath reversal, extra control or temporal regularity has been added. Sources read were the frozen control task, named checkpoint, context procedure, and the supplied predecessor supplement. This is one constructor's derivation with exact algebra and finite numerical checks; no independent review or hardware claim is made.

## 1. What the checkpoint retains, and what it leaves unresolved

Write `F=Z1 X2` and `c=g_A g_B g_C in [1,8]`. The checkpoint's private-sign word retains an instantaneous cubic invariant and controls its **averaged channel**, including fourth-order fluctuation. Its logical angle becomes proportional to `c` when the gains are unknown. Removing the bath does not remove that unknown scalar.

The predecessor's higher odd-power construction can compensate a positive coarse chirality interval under its stronger local regularity hypotheses. Its explicit warning about taking commutators between completed logical macros and bare native handles remains applicable: the accompanying memory unitary cannot be dropped inside such a commutator. Its high-order physical extraction does not have a uniform first-motion remainder merely because its frozen Lie polynomial is correct.

The representation used here has two parts. Positive-definite gain-transfer kernels retain the positivity constraints of randomized commuting logical rotations. Choi covariance retains the fluctuation erased by an averaged-unitary or formal-log calculation. Each leads to an obstruction that survives unlimited repetition or a final bath discard at the stated scope.

## 2. A resource-independent error floor for the clean-cubic library

Consider the enlarged ideal interface that supplies perfect operations

`exp(-i alpha c F) tensor V`

for any classically specified real `alpha`, at no cost. `V` can be any bath unitary and can depend on the gains, program and private coins. Permit arbitrary compositions, correlated classical random choices, signed angles, arbitrary finite duration and even any probability distribution of total angles. No gain evaluation is supplied. This interface includes all protocols that compose fully qualified clean cubic macros as complete operations.

For each realized classical program all logical generators commute. Let `T` be its total signed coefficient. Bath factors disappear after the final partial trace even for initial data-memory-reference correlations. The data channel multiplies the `F=+1` to `F=-1` coherence by

`phi(c) = E exp(-2 i c T)`.

The target multiplier is `-i`. The diamond distance from the target is exactly

`|phi(c)+i|`.                                                    (1)

For the upper bound in (1), the off-diagonal-block map is `(Id-Ad_F)/2`, of diamond norm one, followed by a diagonal unitary phase. A superposition of one vector from each eigenspace attains the bound. This also proves the lower bound with no reference or bath assumptions.

**Theorem 1.** Every protocol in this enlarged ideal interface has worst-gain diamond error at least

`B = [cot(pi/18)-1]/8 = 0.583910227452...`.                       (2)

This holds for arbitrary probability laws of `T`, not just a finite coin space or bounded control action.

**Proof.** For each integer `k=1,...,8`, the gain box contains a triple with product `k`, for example `(k^(1/3),k^(1/3),k^(1/3))`. Put `Z=exp(-2iT)`, so `phi(k)=E Z^k`. The Toeplitz moment matrix

`M_jk = E Z^(j-k)`, `0 <= j,k <= 8`,

is positive semidefinite, since it is a Gram matrix. If every tested gain has error at most `eta`, each of its positive moments differs from `-i` by at most `eta`.

Let `M0` have diagonal 1, lower entries `-i` and upper entries `+i`. For general size `n`, the unit vector

`v_j = exp(i pi j/n)/sqrt(n)`

is an eigenvector of `M0` with eigenvalue `1-cot(pi/(2n))`. This follows by summing the two finite geometric series in each row. Grouping the moment errors by displacement gives

`|v^*(M-M0)v| <= (2 eta/n) sum_{k=1}^{n-1}(n-k) = (n-1) eta`.

Positive semidefiniteness therefore requires

`eta >= [cot(pi/(2n))-1]/(n-1)`.

Taking `n=9` proves (2). All these constraints concern actual data-channel coherences, rather than a particular microscopic product gauge. QED.

The two-gain version, using only `c=1,2`, has the **sharp** error floor `(sqrt(3)-1)/2 = 0.3660254...`. Sharpness follows by taking `Z=-1` with probability `(3-sqrt(3))/6` and `Z=exp(-i pi/3)` otherwise: both moment errors attain that value. Sharpness of the stronger eight-moment bound (2) is not claimed.

If a physical protocol is within diamond error `xi` of some ideal-library protocol uniformly in the gains, its worst-gain error is at least `B-xi`. Thus making the known-gain primitive more accurate, using random gate counts, or choosing an elaborate classical distribution of clean cubic angles cannot solve the next scope. This is an obstruction for a stronger idealized library, so timing precision and extra duration cannot remove it. It does not cover protocols that use additional noncommuting native excursions between these completed operations.

## 3. Why a fixed high-order word lacks a first-motion remainder

Here is a local obstruction encompassing more than one selected pulse list. Let `w` be a fixed finite signed/amplitude native profile on dimensionless interval `[0,S]`, with each handle's area zero. Suppose its frozen zero-drift propagator is `I+O(d^5)` for every even-sign choice `s_A,s_B,s_C=s_A s_B`. Execute its scaled profile in time `Sd` with those fresh private signs.

Let `f_A` be its nonzero A profile and `F_A(s)=integral_0^s f_A`. Define

`h(s) = [F_A(s)-mean(F_A)] / ||F_A-mean(F_A)||_infinity`,

and use the deterministic qubit bath

`H_M(t) = h(t/d) Z_M/2`, `0 <= t <= Sd`.                         (3)

This is piecewise continuous, obeys all three local commutator bounds, is independent of the private signs, and has zero net bath angle. Write `q(s)=integral_0^s h`. In its interaction frame,

`S_x(ds)=X-d q(s)Y+O(d^2)`,
`S_y(ds)=Y+d q(s)X+O(d^2)`.

Consequently the leading controlled residual is

`U_s = I + i d^2 [s_A a X1 Y_M - s_B b X2 X_M] + O(d^3)`,       (4)

where `a=integral f_A q` and `b=integral f_B q`. Integration by parts gives

`a = - integral (F_A-mean(F_A))^2 / ||F_A-mean(F_A)||_infinity < 0`.

The first-motion promise therefore cannot make (4) smaller than order `d^2` uniformly for a fixed nontrivial profile. The bath (3) is allowed to change its shape when a different program or scale is tested; that is exactly what a uniform bath guarantee requires covering.

After averaging signs and starting the bath maximally mixed, the order-`d^4` data-channel covariance contains

`a^2(Ad_X1-Id) + b^2(Ad_X2-Id)`.                                (5)

The averaged order-three term is bath only: even-sign projection keeps either all-even control counts or all-odd counts; the only degree-three all-odd contribution is the frozen cubic term, which vanishes by hypothesis. Remaining fourth-order terms can add a Hamiltonian commutator, but cannot cancel the positive covariance (5). Equivalently, the normalized data Choi matrix has nonprincipal eigenvalue mass

`(a^2+b^2)d^4 + o(d^4)`.

Its trace-norm distance from every pure Choi state, hence from every data unitary channel, is at least

`2(a^2+b^2)d^4 + o(d^4)`.                                      (6)

This follows from the largest-eigenvalue bound `||J-|u><u|||_1 >= 2(1-lambda_max(J))`; a fourth-order Hamiltonian only rotates the leading pure vector. Thus a **fixed flat word plus global even-sign averaging** that extracts degree five or higher cannot have a uniform `o(d^4)` channel remainder under first local motion. The construction works with a qubit bath and unit gains, both admitted instances.

This local statement alone cannot be summed into an accumulated-error lower bound: a retained memory could return information later. For the specific fresh-cycle class considered here, however, a joint-channel comparison proves a stronger consequence.

**Theorem 2 (fixed-word repeated-cycle barrier).** Fix a finite word as above, repeat it with fresh independent global even-sign choices, and suppose its desired frozen logical term has degree `k>=5`. For any repetition family with `N d^k` tending to a nonzero constant, there is an admitted periodic qubit bath, independent of the signs, for which the worst output error has limit inferior at least **one**.

**Proof.** Repeat (3) every word period; its net bath angle is zero. The joint cycle is stationary after averaging. By the same coefficient argument,

`Phi_d = Id+d^3[G3,.]+d^4([G4,.]+D0)+O(d^5)`,

`D0=a^2(Ad_P-Id)+b^2(Ad_Q-Id)`,
`P=X1Y_M`, `Q=X2X_M`.

Here `G3` is bath only. `G4` is anti-Hermitian and its data factors belong to `span{I,F}`. To see the latter assertion, global even-sign projection keeps exactly the control parities `000` and `111`; their data factors are I and F. Unitarity gives the fourth-order symmetric part `-(a^2+b^2)I/2`, leaving `G4` as the anti-Hermitian part. These statements need no bath derivative.

Use the comparison channel

`Psi_d = exp(d^3[G3,.]+d^4[G4,.]+d^4 D0)`.

It is CPTP: its generator is a Hamiltonian commutator plus two positive Pauli dissipators. A fixed-profile bounded Dyson expansion gives `||Phi_d-Psi_d||_diamond <= C d^5` for all sufficiently small d, with a finite word-dependent C. Both Hamiltonian parts commute with `F tensor I_M`, while `D0(F tensor I_M)=-2a^2 F tensor I_M`. Consequently, for the pair of states used in Section 4, the comparison channel shrinks their joint difference by exactly `exp(-2a^2 m d^4)` after m cycles.

Choose `m=ceil(log(1/d)/(2a^2 d^4))`. Telescoping costs at most `C m d^5=O(d log(1/d))`, and the remaining actual cycles contract trace distance. Since `k>=5`, eventually `N>=m`. The two actual data outputs therefore become indistinguishable, while the target E preserves their trace-norm distance two. The triangle inequality gives a worst-state error at least `1-o(1)`. QED.

This theorem permits arbitrary fixed internal sign and amplitude profiles, including very long flat extraction words. It does not cover words or nested scales that change with accuracy, sign correlations across cycles, deterministic coherent repetition without the stated private-sign average, or all allowed native policies. The next section gives an explicit word, exact coefficients, actual counts and a finite rigorous error bound for this mechanism.

## 4. A palindromic degree-five family fails before its angle accumulates

Use chronological words and define `inv(w)` to reverse a list and flip its control signs. Define

`comm(u,v) = inv(v), inv(u), v, u`.

Starting from the one-pulse words A, B, C, set

`w3=comm(A,comm(B,C))`,
`w5=comm(A,comm(A,w3))`,
`p5=w5,reverse(w5)`.

`w5` has 46 unit-duration signed segments; `p5` has 92. In a frozen zero bath,

`log p5(d)=32 i g_A^3 g_B g_C d^5 F+O(d^7)`.                 (7)

 The leading coefficient is the double A-adjoint of the checkpoint cubic term. The palindrome removes the next even logarithmic degree. Flipping C changes the useful sign. These are the sort of extra gain monomials needed by polynomial compensation.

For each cycle choose independent fair `s_A,s_B`, with `s_C=s_A s_B`. Now use the coin-independent periodic bath

`H_M(t)=+Z_M/2` in the first 46 segments of every cycle,
`H_M(t)=-Z_M/2` in the final 46 segments of every cycle.          (8)

All segments have duration `d`. The local motion bound is saturated, not exceeded. The bath angle returns to zero after each cycle. Its switching rate grows as `d` shrinks; no bath bandwidth bound was granted.

For the 46-segment first half the signed first time moments are exactly

`(M_A,M_B,M_C)=(65,16,16)`.

The triangular bath angle doubles the relevant moments of the palindrome. Exact Taylor expansion at unit gains gives

`U_s = I + i d^2(130 s_A X1Y_M - 32 s_B X2X_M) + O(d^3)`,
`E U_1=E U_2=E U_3=0`,
`E U_4=-8962 I`,

where `U_j` in the last two lines denotes the coefficient of `d^j`. Therefore the averaged **joint** channel is

`Phi_d = Id+d^4 D+O(d^5)`,
`D=16900(Ad_P-Id)+1024(Ad_Q-Id)`,
`P=X1Y_M`, `Q=X2X_M`.                                         (9)

The fifth-order averaged unitary coefficient in this bath is `-4896 i F`, compared with the frozen `+32 i F`. This is additional coherent contamination, but the lower bound below needs only the irreversible fourth-order term. The whole-word signs and the entire bath period are specified without reference to one another's realized private values.

`exact_degree5.py` reproduces the pulse list and these coefficients using Gaussian-integer exponential derivatives. It writes `degree5_certificate.json`. No floating-point tolerance is used for its assertions. The fourth-order channel coefficient follows from the displayed unitary coefficients, including the indispensable `E U_2 (.) U_2^dagger` term.

### A finite rigorous accumulated bound

Every laboratory Hamiltonian in this example has norm at most `3/2`. The channel generator has diamond norm at most 3, over 92 segments. The integral Dyson remainder with a full unitary channel left in the fifth-order integral gives

`||Phi_d-(Id+d^4 D)||_diamond <= (276 d)^5/120`.

The channel `Psi_d=exp(d^4 D)` is CPTP, and `||D||_diamond <= 35848`. Hence

`||Phi_d-Psi_d||_diamond <= R(d)`,
`R(d) = (66732004224/5)d^5 + (35848^2/2)d^8`.                 (10)

Consider the admitted product inputs

`rho_+/- = [(I_D +/- F)/4] tensor (I_M/2)`.

Their difference has trace norm two, and `D(F tensor I_M)=-33800 F tensor I_M`. For any integers `N>=m`, fresh signs and the reset bath frame make the averaged joint channel exactly `Phi_d^N`. CPTP telescoping, followed by trace-norm contraction through all remaining cycles, gives

`||Phi_d^N(rho_+-rho_-)||_1`
`   <= 2 exp(-33800 m d^4)+2m R(d)`.                           (11)

The target gate preserves the distinguishability of these inputs because it commutes with F. Discarding memory cannot increase the actual distinguishability. The worst error on the two data outputs is consequently at least

`1-exp(-33800 m d^4)-m R(d)`.                                 (12)

Take `N=ceil(pi/(128 d^5))`, with C flipped for the target sign. This has the nominal degree-five angle `pi/4`, duration `92Nd`, 92N native segments and 2N private bits. For `m=ceil(log(1/d)/(33800d^4))`, eventually `N>=m`, and (12) tends to **one** as `d` tends to zero. Thus the increasingly weak family fails even at the admitted gain triple `(1,1,1)`.

There is also a finite analytic example. At the rational duration `d=10^-9`, take `m=1/(4000d^4)`. Then `exp(-33800md^4)=exp(-8.45)<1/4000`, `mR(d)<0.003337`, and `N>m`. Equation (12) is therefore **greater than 0.9964**. The clock times are rational multiples of `d`; the ideal negative example does not require an infinite schedule or irrational timing. `finite_certificate.py` verifies the rational inequalities and proves the exponential comparison using a finite positive Taylor sum. These extreme counts are only a finite mathematical witness.

### Finite numerical cross-checks

`channel_checks.py` uses analytic native matrix exponentials and powers the 64-dimensional joint superoperator only to an intermediate `m`, before using the contraction logic. It does not initialize or replace memory between cycles. The displayed errors below are numerical diagnostics, not interval certificates:

| d | intermediate cycles m | joint distance between the two inputs after m cycles | consequent numerical worst-error floor |
|---:|---:|---:|---:|
| .02 | 724 | .0538763 | .973062 |
| .01 | 13,625 | .0219331 | .989033 |
| .005 | 250,808 | .0102722 | .994864 |
| .0025 | 4,537,914 | .00503821 | .997481 |

Single-cycle unitary defects are below `6e-15` in these computations. The exact coefficients, bounds (10)-(12), and finite analytic witness supply the proof; floating-point powers supply an additional check only.

## 5. Consequence for the shared next scope

There are two separate earned facts:

* Even perfect clean cubic rotations, with arbitrary classical randomized angle programming and unlimited resources, have a worst-gain error floor of at least 0.58391 on this gain box.
* A fixed high-order flat word with fresh global private-sign choices cannot inherit a higher-order uniform channel remainder from its frozen Lie polynomial under first local motion. Theorem 2 gives a periodic admissible bath for which its nominal completed operation has error tending to at least one; the degree-five palindrome supplies explicit coefficients and a finite bound.

These facts rule out two direct continuations of the known-gain proof. They retain the full bath class and no-calibration information contract. A successful construction must preserve nonlinear gain information through an operation outside the commuting cubic library while controlling the associated channel covariance with only the first-motion promise. An all-policy quantitative lower bound, or such a positive compiler with actual duration/switching/precision resources, has not been established here.

Reproduce the checks from this directory with:

```
PYTHONDONTWRITEBYTECODE=1 python3 exact_degree5.py
PYTHONDONTWRITEBYTECODE=1 python3 finite_certificate.py
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 channel_checks.py
```

The exact algebra check needs only the Python standard library. The finite matrix cross-check uses the locally available NumPy. No installation or network access is needed.
