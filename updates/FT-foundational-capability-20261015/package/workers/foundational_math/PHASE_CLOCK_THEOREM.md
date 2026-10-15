# Finite-horizon state complexity of a fixed irrational phase

15 October 2026. Independently derived candidate theorem, written proof below.
External review and historical novelty are unresolved. This is a theorem about a
specified finite-state model, not a physical quantum advantage or a general
classical-computation lower bound.

## Contract

Fix an irrational number `alpha` in `(0,1)` and put
`z = exp(2 pi i alpha)` and `p_k = (1 + Re(z^k))/2`.
A classical model with `n` states is a triple `(mu,P,f)`, where `mu` is a
probability row vector, `P` is an `n by n` row-stochastic matrix and
`f in [0,1]^n`. Its output probability after `k` identical wait operations is
`g_k = mu P^k f`. The initial distribution, transition probabilities and
readout may depend on the requested finite horizon `T` and error `epsilon`.
There is no restriction to reversible, diagonalizable, stationary, ergodic,
deterministic or rational models.

The model receives identical wait operations and a terminal read command. It
does not receive the elapsed integer `k` as an additional readout input, an
external table indexed by `k`, or a continuous phase register. Those operations
would change the comparator. Both models receive the phase specification.

Let `N_alpha(T,epsilon)` be the least `n` for which
`|g_k-p_k| <= epsilon` for every integer `0 <= k <= T`.

## Theorem

Suppose there is a constant `kappa>0` such that
`||q alpha||_(R/Z) >= kappa/q` for every integer `q>=1`.
For every fixed `0<epsilon<1/4`,

`N_alpha(T,epsilon) = Theta_(alpha,epsilon)((T+1)^(1/3))` as `T -> infinity`.

More precisely, with `C_alpha = 1/|1-z^2|`, every classical model satisfies

`n^3 >= kappa^2 [(T+1)(1/2-2 epsilon)-C_alpha]`.

A negative right hand side gives no nontrivial lower bound. Conversely,
choosing a continued-fraction denominator `N` with

`N >= L := max{3, (2 pi^2 T/epsilon)^(1/3)}`

gives a model with `N` states and error at most `epsilon`; the first such
denominator obeys `N < L/kappa` (apart from harmless initial denominators).

A two-dimensional ideal quantum model gives `p_k` exactly: prepare `|0>`,
apply the real rotation by `pi alpha` once per wait, and measure `|0><0|` at
readout. This uses a supplied exact gate in the ideal model. A finite-precision
implementation must acquire and maintain phase accuracy of order
`epsilon/(T+1)`; its input and calibration costs are not one qubit.

The condition `epsilon>0` matters. At zero error the state complexity is
between `T` and `T+1` for `T>=1`, hence has linear order. A proof is given
below; the cube-root theorem does not include zero error.

## Lemma 1: a conditioning-free stochastic resolvent bound

For a row-stochastic `n by n` matrix `P`, a complex `z` with `|z|=1`, and

`delta_n(z) := min_(1<=q<=n) |1-z^q| > 0`,

the inverse exists and

`||(z I-P)^(-1)||_(infinity -> infinity) <= 8 n/delta_n(z)^2`.

Proof. Take a nonzero vector `v` and normalize `||v||_infinity=1`. Put
`eta=||(z I-P)v||_infinity`, and choose `i` with `|v_i|=1`.
Because `P` is an infinity-norm contraction, telescoping gives

`||P^t v-z^t v||_infinity <= t eta` for all `t>=0`.

Let `X_t` be the Markov chain started at `i`. For `a_t=z^t v_i`, which has
unit modulus,

`E |v_(X_t)-a_t|^2`
`= E |v_(X_t)|^2 + 1 - 2 Re(conj(a_t) E v_(X_t))`
`<= 2 t eta`.

Consequently, for each `t=0,...,n`, some state `j_t` in the support of `X_t`
satisfies `|v_(j_t)-a_t| <= sqrt(2 t eta)`. At `t=0` take `j_0=i`.
There are `n+1` chosen states and only `n` possible values, so `j_s=j_t` for
some `0<=s<t<=n`. Thus

`delta_n(z) <= |z^(t-s)-1| = |a_t-a_s|`
`<= sqrt(2s eta)+sqrt(2t eta) <= sqrt(8 n eta)`.

It follows that `||(z I-P)v||_infinity >= delta_n(z)^2/(8n)` for every
unit vector. The matrix therefore has trivial kernel and is invertible, and
the displayed inverse bound follows. No eigenbasis, mixing time, positive
stationary distribution or minimum transition probability was used. QED.

## Lemma 2: a finite-horizon Fourier witness

For every classical model above,

`|sum_(k=0)^T z^(-k) (2g_k-1)| <= 16n/delta_n(z)^2`.

Proof. Set `a=2f-1`, so `||a||_infinity<=1` and
`2g_k-1=mu P^k a`. The geometric identity gives

`sum_(k=0)^T z^(-k) P^k`
`= (I-z^(-1)P)^(-1) [I-z^(-(T+1)) P^(T+1)]`.

The bracket has operator infinity norm at most two, `||mu||_1=1`, and
`||(I-z^(-1)P)^(-1)||_infinity=||(zI-P)^(-1)||_infinity`.
Apply Lemma 1. QED.

For the target cosine,

`sum_(k=0)^T z^(-k) Re(z^k)`
`= (T+1)/2 + (1/2) sum_(k=0)^T z^(-2k)`.

The second term has modulus at most `C_alpha`, since `z^2 != 1`. Uniform
probability error `epsilon` changes the Fourier sum by at most
`2 epsilon (T+1)`. Therefore its modulus is at least
`(T+1)(1/2-2epsilon)-C_alpha`.

For `d=||q alpha||_(R/Z) in [0,1/2]`,
`|1-z^q|=2 sin(pi d)>=4d`. The Diophantine premise implies
`delta_n(z)>=4 kappa/n`. Lemma 2 is consequently at most `n^3/kappa^2`.
Combining the upper and lower bounds proves the theorem's lower bound.

## Lemma 3: matching stochastic construction

Let `p/N` be a continued-fraction convergent of `alpha` with `N>=3`.
Write `h=2pi/N`, `d=2pi |alpha-p/N|`, and
`s=sign(alpha-p/N)`. Irrationality gives `s in {-1,1}` and
`0<d<h/N<h`. The two unit complex numbers

`u=exp(2pi i p/N)` and `v=exp(2pi i(p+s)/N)`

lie on either side of the ray through `z`. There is a unique `t in (0,1)`
such that `(1-t)u+t v=r z`, explicitly

`t = sin(d)/[sin(d)+sin(h-d)]`.

Chord geometry gives

`r = cos(h/2)/cos(d-h/2)`.

In particular `0<r<1`, and

`1-r = 2 sin(d/2) sin((h-d)/2)/cos(d-h/2)`
`<= d(h-d)/(2 cos(h/2)) <= d h <= 4pi^2/N^3`,

using `cos(h/2)>=1/2` for `N>=3` and
`|alpha-p/N|<1/N^2` for convergents.

On states `j mod N`, let `P` jump by `p` with probability `1-t` and by
`p+s` with probability `t`. Start at state zero and use
`f(j)=(1+cos(2pi j/N))/2`. Each increment multiplies the first Fourier
character by `r z`, so

`g_k=(1+r^k cos(2pi alpha k))/2`.

Hence, for every `0<=k<=T`,

`|g_k-p_k| <= (1-r^k)/2 <= k(1-r)/2 <= 2pi^2 T/N^3`.

This proves the asserted error bound. If `q_j,q_(j+1)` are consecutive
continued-fraction denominators, then

`kappa/q_j <= |q_j alpha-p_j| < 1/q_(j+1)`,

so `q_(j+1)<q_j/kappa`. The first denominator at least `L` is therefore
less than `L/kappa`, once the usual initial denominators are passed. QED.

## An entirely specified phase

Take `alpha=(sqrt(5)-1)/2`. One may use `kappa=1/3` uniformly. Indeed, for
a nearest integer `p` to `q alpha`, `p/q in [0,1]`. The conjugate root is
`beta=-(sqrt(5)+1)/2`, and the nonzero integer
`p^2+pq-q^2` has absolute value at least one. Thus

`|alpha-p/q| = |p^2+pq-q^2|/[q^2 |p/q-beta|] > 1/(3q^2)`.

Its continued-fraction denominators are Fibonacci numbers, with successive
ratios at most two. This makes the construction algorithmic from a fixed
computable constant rather than an oracle for an unspecified real phase.

## Precision, cost and comparison boundaries

The construction has two nonzero transitions per state and one readout number
per state. The ideal real parameters are computable. Approximating `t` by a
rational changes each step's transition kernel by at most `|Delta t|` in
total variation, so it changes every terminal probability by at most
`T |Delta t|`. Approximating each readout probability to `eta` adds at most
`eta`. Thus a slightly stricter ideal error budget and
`|Delta t|=O(epsilon/(T+1))`, `eta=O(epsilon)` give rational finite input
parameters with `O(log((T+1)/epsilon))` precision bits. The quantum gate also
needs `O(log((T+1)/epsilon))` phase precision bits under a direct telescoping
error bound. This is a supplied-model description result, not a statement
that one can learn the required model or calibrate the gate at no cost.

The lower bound counts stochastic states. In ordinary binary memory this is
only `Omega(log T)` bits (with constant factor `1/3`), and a conventional
computer storing `k` and evaluating a cosine also uses `O(log T)` bits. An
analog phase register is outside the finite-state comparator. No speed,
energy, experiment, fabrication, learning, or acquisition advantage follows.

## Prior-art boundary (live sources checked 15 October 2026)

Classical stochastic peripheral spectra and Karpelevich eigenvalue regions,
positive realization, unary quantum automata and low-dimensional probability
clocks are established subjects. The new work claimed here is only the
independent derivation of the displayed finite-horizon proof and matching
construction. A bounded search did not settle whether the precise cubic
state-complexity formulation or the elementary resolvent lemma already
appears in this literature. Historical novelty remains **UNKNOWN**.

Relevant primary sources:

- Dmitriev and Dynkin, On characteristic roots of stochastic matrices (1946):
  https://www.mathnet.ru/php/archive.phtml?jrnid=im&option_lang=eng&paperid=3595&wshow=paper
- O. Szehr, Eigenvalue estimates for the resolvent of a non-normal matrix:
  https://arxiv.org/abs/1305.7208 (spectral resolvent estimates; this proof
  instead uses a direct stochastic phase argument).
- A. Gainutdinova and A. Yakaryilmaz, Unary Probabilistic and Quantum Automata
  on Promise Problems: https://arxiv.org/abs/1502.01462 (qualitative irrational
  rotation separation; exact finite-horizon rate still under comparison).
- M. Fanizza, J. Lumbreras and A. Winter, Quantum Theory in Finite Dimension
  Cannot Explain Every General Process with Finite Memory:
  https://doi.org/10.1007/s00220-023-04913-4 (finite-dimensional realization
  boundaries; a different, uncontrolled output-process contract).

No claim of exceptional significance or mission completion is made.

## Zero-error boundary

Suppose `g_k=p_k` for `0<=k<=T` and `n<=T-1`. Write
`q(x)=det(xI-P)`. Cayley-Hamilton gives
`sum_(j=0)^n q_j g_(j+s)=0` for `s=0,1`, and `q(1)=0` because `P` is
stochastic. Substitution of the target gives

`Re(q(z))=0` and `Re(z q(z))=0`.

Since `z` is nonreal, these force `q(z)=0`. The standard peripheral-spectrum
theorem for finite stochastic matrices then says `z` is a root of unity with
order at most `n`, contradicting irrationality. Equivalently, Lemma 1 alone
rules out this eigenvalue, without importing the peripheral-spectrum theorem.
Thus `n>=T`.
A deterministic chain of `T+1` states, with state `k` assigned readout
probability `p_k`, reproduces the entire prefix exactly. This is an ideal
real-parameter result, with the same finite-precision qualifications as above.
The present notes do not determine whether the exact minimum is `T` or
`T+1` for each horizon.

## Independent audit credit

The targeted helper `phase_clock_audit`, model `gpt-6.1-sol`, reasoning `max`,
independently checked the supplied proof, its transient/nonnormal scope,
constants, shift orientation, and continued-fraction denominator ratios.
The helper identified and proved the separate zero-error boundary and found
the closest qualitative positive-realization and quantum-automaton sources.
Its full report is `audit/AUDIT.md`. The campaign coordinator separately
reconstructed the positive-error proof and zero-error argument. These are
internal audits, not formal verification or external mathematical review.
