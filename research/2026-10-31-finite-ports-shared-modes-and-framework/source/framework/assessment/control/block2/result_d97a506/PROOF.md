# Gain compensation under only first local motion: scoped barriers

All trace and diamond norms are unhalved. Nothing in this note is a full
impossibility theorem for the question in `CONTROL_NEXT_SCOPE.md`. It proves
three precise restrictions, gives an explicit moving-bath counterexample to
a natural polynomial route, and leaves the unrestricted existence question
open. The native operations, unknown static gains, arbitrary initial
correlations, and private-coin noise game are retained.

Write `F=Z1 X2`, `q=g_A g_B g_C`. No memory initialization, measurement,
logical pulse, bath inverse, or additional Hamiltonian is used.

## 1. A fixed accuracy floor for clean cubic-macro compilation

Consider programs assembled only from clean effective calls

`exp(-i q theta F) tensor V`,

where each real coefficient `theta` is classically specified and independent
of the gains. Bath-only factors may depend on the gains, the fixed bath,
and all private coins. Calls may have either orientation and arbitrary
random coefficients; no moment or bounded-support assumption on those
coefficients is required. This is the comparison class obtained by refining
the checkpoint's cubic cycles, then composing only their clean logical
limits. Errors in implementing the calls are charged separately.

For each private record, composition and discarding memory give
`Ad_exp(-i q Theta F)` for some real random `Theta`. This holds even on
correlated data-memory-reference inputs. Put

`z=exp(-2i Theta)`, `m=E z`, `n=E z^2`, `t=-i`.

The two gain triples `(1,1,1)` and `(2,1,1)` are admitted. A superposition
between one `F=+1` and one `F=-1` data eigenvector witnesses error at least
`|m-t|` and `|n-t|`, respectively. If both are at most `e`, the unit-circle
moment identity gives

`|n-m^2| = |E (z-m)^2| <= E |z-m|^2 = 1-|m|^2`.

Let `r=|m|`, so `1-e <= r <= 1` for `e<1`. Then

`|t^2-t| = sqrt(2) <= e(1+r) + 1-r^2 + e`.

For `e<2/3` the last expression decreases with `r` on `[1-e,1]`, and is
at most `5e-2e^2`. For `e>=2/3` the following lower bound already holds.
Consequently every such randomized compiler has worst-box error at least

`e_0 = (5-sqrt(25-8sqrt(2)))/4 = 0.3251252956...`.

If an actual compiled program is within diamond error `eta`, uniformly in
q, of this clean-macro class, its target error is at least `e_0-eta`.
This is an obstruction to gain flattening by commuting cubic macros. It is
not an obstruction to programs that interleave physical native handles or
produce other gain functions.

## 2. A moving-bath obstruction to refining any fixed higher-order word

### 2.1 The restricted program class

Fix a finite chronological native profile on normalized time `[0,l]`:

`f_j(t) in [-1,1]`, with at most one nonzero profile at a time.

Piecewise constant profiles suffice. Each handle has zero area. Suppose the
zero-bath unitary has no first or second Taylor coefficient when this word
is scaled to physical time `d[0,l]`. In particular, this holds for a pure
commutator word with first nonidentity term of degree `k>=3`.

Each physical cycle multiplies the entire profile by a fresh independent
pair of fair signs `s_A,s_B`, with `s_C=s_A s_B`. The same fixed profile is
repeated `N` times at scale `d`. This is deliberately a restricted class:
word shape does not grow with `1/d`, and there are no privately selected
word shapes or private random translations/dilations beyond these signs.

Assume `f_A` is not identically zero. Define

`P_A(t)=integral_0^t f_A(u)du`,
`h(t)=sign(P_A(t))`, with `sign(0)=0`,
`H(t)=integral_0^t h(u)du`,
`mu_j=integral_0^l f_j(t) H(t)dt`.

Integration by parts and zero area give

`mu_A = -integral_0^l |P_A(t)|dt != 0`.

The adversary chooses the following qubit bath, repeated on every physical
cycle:

`H_M(ndl+dt) = h(t) Z_M/2`, `0<=t<l`.

This waveform depends on the public fixed profile and scale but not on any
realized private sign or input. It is piecewise continuous and satisfies
`||[H_M,sigma_x]||, ||[H_M,sigma_y]|| <= 1`, and
`[H_M,sigma_z]=0`. Its norm is at most `1/2`. Thus the obstruction already
uses a bounded, two-dimensional bath. Its switching bandwidth grows as the
word is refined, which the task permits.

### 2.2 The order-two private fluctuation

Use the bath interaction frame separately at the start of each cycle.
At normalized time t,

`S_x(dt)=cos(dH(t)) S_x(0)-sin(dH(t)) S_y(0)`,
`S_y(dt)=sin(dH(t)) S_x(0)+cos(dH(t)) S_y(0)`,
`S_z(dt)=S_z(0)`.

Here the axes at the start of the cycle may have rotated from earlier
cycles; this does not change the following norm or Pauli-square identities.
The signs of the linear terms follow from
`exp(i theta Z/2) X exp(-i theta Z/2)=X cos(theta)-Y sin(theta)`.

Zero areas, and the vanishing frozen second Dyson term, give

`U_s(d)=I+d^2(s_A L_A+s_B L_B)+R_s(d)`,

where

`L_A=i g_A mu_A X1 tensor S_y(0)`,
`L_B=-i g_B mu_B X2 tensor S_x(0)`,

and, uniformly over `g_j in [1,2]`,

`||R_s(d)|| <= K d^3`, `K=6l^3`, when `dl<=1/2`.

An explicit bound: the first-Dyson-term quadratic-axis Taylor remainder is
at most `l^3 d^3/3`; the difference of the moving and frozen second Dyson
terms is at most `2l^3 d^3`; and all Dyson terms of degree at least three
are bounded by `(4/3)e l^3 d^3`. Their sum is less than `6l^3 d^3`.
These estimates use only `|h|<=1`, gains at most two, and the norm-one
Pauli axes. They import no bath derivative assumption.

### 2.3 Exact sign-Fourier structure isolates data flips

For `r=0,A,B,C`, define the four Fourier coefficients

`U_0=E_s U_s`, `U_j=E_s s_j U_s`.

The even-sign characters are orthogonal, so `E U_s^dag O U_s` equals
`sum_r U_r^dag O U_r`. Every native Dyson monomial has one of these four
characters. Its data factor commutes with `Z1` in characters 0 and B and
anticommutes in characters A and C. To verify this, the data sign under
conjugation by Z1 is `(-1)^(n_A+n_C)`; equal even-sign characters differ
by parity 111, which leaves that exponent unchanged. This is an exact
statement about the entire convergent Dyson series, not a truncation.

Unitarity also gives `sum_r U_r^dag U_r=I`. Therefore the averaged cycle
satisfies the exact Heisenberg identity

`Phi^*(Z1) = Z1 [I-2(U_A^dag U_A+U_C^dag U_C)]`.

The previous expansion implies

`U_A=d^2 L_A+O_K(d^3)`, `U_C=O_K(d^3)`.

Since `L_A^dag L_A=g_A^2 mu_A^2 I`, this yields

`Phi^*(Z1)=(1-2c d^4) Z1+R_Z`,
`c=g_A^2 mu_A^2 > 0`,
`||R_Z|| <= R d^5`, `R=96l^5`, for `dl<=1/2`.

For the stated constant: `||L_A||<=l^2`,
`||U_A^dag U_A-d^4 L_A^dag L_A|| <= 2l^2 K d^5+K^2d^6`, and
`||U_C^dag U_C||<=K^2d^6`. Multiply the sum by two and use `dl<=1/2`.
Bath-only restoration of the laboratory frame commutes with Z1 and leaves
this formula unchanged.

The fourth-order term is positive channel variance. Its contribution to
this observable cannot be canceled by a coherent mean Hamiltonian, including
any data-only polynomial in F.

### 2.4 Uniform accumulation and a recipient-visible lower bound

For `2c d^4<=1`, let `z_n` be the Z1 expectation after n cycles, averaged
over all previous private signs. Fresh signs and a coin-independent bath
make each next averaged map apply to the full retained data-memory state.
There is no memory reset or Markov assumption. The Heisenberg estimate,
uniform in that state, gives

`|z_(n+1)-(1-2c d^4) z_n| <= R d^5`.

For an input supported on `Z1=+1`, iterate this scalar inequality:

`|z_N| <= exp(-2c N d^4) + (R/(2c)) d`.

The desired `E=exp(-i pi F/4)` commutes with Z1, so its output has
expectation exactly one. Measuring Z1 on the returned data alone gives the
trace-norm and hence diamond-norm lower bound

`error >= 1-exp(-2c N d^4)-(R/(2c))d`.                         (B)

The right side may be negative for a coarse scale; its useful content is
asymptotic. For every fixed word with clean first useful term of degree
`k>4`, a fixed nonzero logical angle requires `N d^k -> theta>0`.
Then `N d^4 -> infinity`, and (B) tends to one. Thus refining and repeating
that word does not converge uniformly under the first-motion bath promise.
The counterexample bath is allowed to vary with d in a uniform guarantee.
For the known cubic construction, `N d^3=O(1)` instead gives `N d^4=O(d)`;
there is no contradiction.

### 2.5 An explicit fifth-order word with zero first moments

Let `inv(w)` reverse a chronological word and flip its control signs, and
let

`comm(u,v)=inv(v),inv(u),v,u`.

This is only a definition of native profiles; no physical inverse of the
bath is used. Start with `v_2=comm(B,C)`, and set successively
`v_(j+1)=comm(A,v_j)` for j=2,3,4. The resulting raw fifth-order word has
46 segments. Flip C, then append the reversed chronological list without
sign changes. The resulting palindrome W has 92 unit-duration segments.
Its zero-bath expansion is

`W_s(d)=I-32i g_A^3 g_B g_C d^5 F+O(d^6)`

for each of the four even-sign records. Each handle's area AND first
moment is zero. Hence a static Z bath does not supply the leading
second-order fluctuation used above. The nonconstant h is essential here.

The exact generated profile and adversarial h are in `CHECKS.json`.
Gaussian-integer exponential-derivative arithmetic proves through degree
five, for unit gains:

- all frozen coefficients of degrees 1 through 4 vanish;
- the frozen degree-five coefficient is `-32i F` for all four records;
- `mu_A=-130`, `mu_B=-28`, and total bath angle is zero;
- `Phi^*(Z1)=Z1-33800d^4 Z1+O(d^6)`; its degree-five coefficient is exactly
  zero in this example.

The generated `mu_C=28` is just a profile integral; C commutes with the Z
bath, so it contributes no first-order moving-axis fluctuation. The bath
returns exactly to its initial frame at the end of each cycle, but memory
state resetting is never used. Integer gain-corner checks also confirm the
`g_A^3 g_B g_C` fifth-order coefficient.

The analytic theorem above uses the weaker O(d^5) remainder and therefore
covers more words than this symmetric example. There is also a finite
rational certificate. Exact expansion through degree nine gives

`Phi^*(Z1)=[1-33800d^4+(16701716/3)d^6-(1425644383/6)d^8] Z1+R_10`,
`||R_10|| <= (276d)^10/10!`.

The remainder follows directly by truncating the Heisenberg channel Dyson
series. Each actual Hamiltonian has norm at most 3/2 and normalized total
duration 92, so its commutator generator has integrated norm at most 276.
There is no exponential factor in this unitary-channel integral remainder.
Let

`d=1/1000`, `N=ceil(pi/(128d^5))=24,543,692,606,171`,
`alpha=33800d^4-(16701716/3)d^6+(1425644383/6)d^8`.

The same expectation recursion, now with residual `(276d)^10/10!`, gives

`error >= 1-1/(1+N alpha)-[(276d)^10/10!]/alpha`
`       > 0.9999778781`.

The step `exp(-x)<=1/(1+x)` makes the displayed certificate wholly rational.
Machin-formula rational brackets for pi certify the integer N.

For comparison, the SAME finite program with zero bath has diamond error
less than `0.00001466109` from the target, for every private sign record.
This second certificate uses exact frozen unitary coefficients through
degree 12, subtracts `I-32id^5 F-512d^10 I`, bounds the discrepancy by the
Pauli coefficient l1 sum, and adds the two unitary integral remainders
`(92d)^13/13!` and `(32d^5)^3/6`. Multiplying that one-cycle operator
bound by `2N`, and charging less than `64d^5` for the target-angle rounding,
gives the stated diamond bound. All four records are related by data-Pauli
conjugations preserving F, so their coefficient norm bounds coincide.
These Pauli conjugations are a proof identity, not physical pulses.

The literal program has 2,258,019,719,767,732 native segments and duration
2,258,019,719,767.732 in the strength-one units. It uses 2N fresh fair bits.
Its common duration is exactly rational and every event time is on the
1/1000 grid; the event numerator needs at most 52 bits. This is a finite
counterexample comparison, not a positive resource claim for unknown-gain
control. No clock-jitter robustness is needed for this counterexample to
the ideal specified word.

Finite floating-point checks are diagnostics of the coefficients and
long-cycle behavior. They also report accumulated trace drift, which reaches
0.0021 in the longest diagnostic power. None of those floating-point powers
is used in either rational certificate.

### 2.6 Fixed finite gain-polynomial compositions

The same obstruction extends to a predetermined finite concatenation of
weak-word macros. Suppose each macro is either a convergent clean cubic
macro or a fixed word of the above type with first clean useful degree
`k>4`, with fresh global even signs per cycle. Suppose every higher-order
macro is refined with its nonzero intended angle held fixed. Its orientation
may be reversed to implement a negative polynomial coefficient.

Choose the adversarial h profile separately on each publicly prescribed
higher-order macro, and choose zero bath Hamiltonian during the cubic
macros. This is one concatenated, coin-independent, piecewise-continuous
bath. A higher-order macro sends the absolute Z1 expectation to o(1),
uniformly in the state it receives, by the scalar recurrence. Further such
macros have the same property; a clean cubic macro commutes with Z1 and
changes its expectation only by its vanishing implementation error.
Therefore, if at least one higher-order macro has nonzero angle, the entire
fixed finite polynomial compilation has output Z1 expectation o(1) from a
Z1=+1 input, hence target trace-norm error at least 1-o(1).

Reversing a logical coefficient does not reverse the positive variance
`g_A^2 mu_A^2`. This corollary invalidates the straightforward prescription
"choose a gain polynomial, then refine each fixed homogeneous native word"
under only the first-motion promise. It still does not cover word shapes,
private word choices, or nonperturbative constructions changing with epsilon.

## 3. A duration bound valid for every randomized native program

This section concerns the full unknown-gain model, with no restriction to
sign-projected words. It proves a finite-action accuracy lower bound, not
an epsilon-independent error floor.

Fix the admitted bath `H_M=0` and restrict the gain box to its common-scale
line `g_A=g_B=g_C=x in [1,2]`. Let omega be any private program record and
let its native action be

`A_omega=integral |u_omega(t)| dt`.

The duration is at least this action. Each record may have its own finite
word, stopping time, switching pattern, and amplitudes, all independent of
the unknown x. The proof allows unbounded support of the private action
and continuously distributed private choices. It assumes A is finite almost
surely; the expectation may be infinite.

Prepare maximally entangled data/reference and a maximally mixed qubit
memory as a witness input, purely for the lower-bound argument. Let
`P_E` be the target pure data/reference Choi-state projection. Define the
branch infidelity

`h_omega(x)=1-Tr[(P_E tensor I_M) U_(omega,x) rho U_(omega,x)^dag]`.

For real x this is nonnegative. At x=0 no native interaction acts, so

`h_omega(0)=1-|Tr(E)/4|^2=1/2`.

Duhamel differentiation and Leibniz give

`||partial_x^n U_(omega,x)|| <= A_omega^n`,
`|h_omega^(n)(x)| <= (2 A_omega)^n`.

These bounds hold also between x=0 and x=2. If the averaged channel error
is at most epsilon uniformly on `[1,2]`, a target-state projection gives
`E_omega h_omega(x)<=epsilon/2` at each x. Nonnegativity permits Tonelli
integration without exchanging derivatives with the private expectation.

Here is an explicit integral lower bound for each finite-action branch.
Put

`rho=3+2sqrt(2)`, `C_0=8e log(rho)`, `c_0=1/(4rho^2)`.

Choose `N=ceil(8e A)+2`, `n=N-1`, and interpolate h on the n+1
Chebyshev extrema of `[1,2]`. The absolute sum of exterior interpolation
weights at x=0 is at most `rho^n`. The real interpolation remainder is
bounded by `(4A)^N/N! <= (4eA/N)^N <= 2^(-N) <= 1/4`.
It follows from h(0)=1/2 that

`max_[1,2] h >= (1/4)rho^(-n) >= c_0 exp(-C_0 A) =: m(A)`.

The derivative bound `|h'|<=2A` shows that h is at least m/2 on a
one-sided interval of length at least `min(1,m/(4A))`, with A=0 handled
by continuity. Therefore

`integral_1^2 h(x) dx >= m(A)^2/[8(A+1)]`
`                         >= [1/(128rho^4)] exp[-C_* A]`,

where `C_*=16e log(rho)+1` and `1/(1+A)>=exp(-A)` was used.
Averaging and comparing with epsilon/2 proves

`epsilon >= [1/(64rho^4)] E_omega exp(-C_* A_omega)`.          (C)

Consequences include:

1. If `E A` is finite,
   `epsilon >= [1/(64rho^4)] exp(-C_* E A)` by Jensen. Hence expected
   action, and expected duration, must grow at least logarithmically in
   `1/epsilon`, up to the displayed conservative constants.
2. More generally, for every a>=0,
   `Pr(A<=a) <= 64rho^4 epsilon exp(C_*a)`.
3. Exactly zero error uniformly across the gain interval is impossible for
   any randomized policy with almost-surely finite action, even if its
   expected action is infinite: the expectation of the strictly positive
   variable in (C) is strictly positive.

This is a randomized, action-tail version of the supplied predecessor's
analytic uniform-gain lower-bound argument. It does not claim a new general
invention of analytic gain obstructions. The full approximation question
remains consistent with (C), since finite programs may have action growing
without bound as epsilon decreases.

## 4. What is established and what remains open

The supplied checkpoint already proves known-gain cubic reachability. Its
sign projection and the predecessor's higher-order gain polynomials remain
valid at their earned scopes. The new restriction here is operational:
commuting clean cubic calls have a gain-box accuracy floor, while the
straightforward fixed-word high-order refinement is vulnerable to an
admitted bath with first motion bounded by one and no higher regularity.
The explicit fifth-order example defeats static-moment cancellation as a
substitute for a uniform first-motion analysis.

Neither result covers every native randomized program. Word shapes or
randomization policies that change with epsilon, multiscale schedules,
nonperturbative controls, or a different construction might evade them.
The action lower bound covers all such programs but does not rule out
approximation with growing finite resources. Therefore the requested full
unknown-static-gain first-motion entangler is NOT RESOLVED here.
