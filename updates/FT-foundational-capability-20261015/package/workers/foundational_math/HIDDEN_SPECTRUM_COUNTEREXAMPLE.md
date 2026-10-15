# A precise hidden-mode counterexample to full collision-spectrum invariance

15 October 2026. Standard observable-realization issue, independently checked.
This is a correction to the stated scope of one displayed claim, not a review
of the entire source paper or a claim that observable spectral methods fail.

## Exact source and hypothesis check

Source: Zonnios, Boyd and Binder, *Quantum generation of stochastic processes:
spectral invariants and memory bounds*, arXiv:2412.12812v2, dated 29 September
2026. Primary full text inspected live:
https://arxiv.org/html/2412.12812v2

The relevant prose after Theorem 1 states:

> the distinct, non-zero spectrum is an invariant of the process

Theorem 1 asserts equality of the full sets `Lambda_R` and `Lambda_Q` when
two QHMMs generate the same process. The model definition permits arbitrary
instruments and initial density operators. Equivalence means equality of every
word probability at every length. The spectral definition takes all distinct
nonzero transfer eigenvalues, rather than only those with nonzero scalar
observation coefficients. The displayed theorem does not impose minimality,
reachability or observability; minimal generating models enter the later
memory-bound argument. Its diagonalizability premise is satisfied below.

## Two equivalent classical models

Model A has one state and symbol matrices `T_0=T_1=[1/2]`. It emits a fair iid
coin. Its collision transfer is the scalar `E_A=1/2`, whose nonzero spectrum
is `{1/2}`.

Model B has two hidden states, stationary initial row vector `pi=(1/2,1/2)`,
and

`P = [[3/4,1/4],[1/4,3/4]],  T_0=T_1=P/2`.

For every word `w` of length `L`,

`pi T_w 1 = 2^(-L) pi P^L 1 = 2^(-L)`.

Thus the complete output law equals Model A's fair iid law for all lengths,
not merely a finite collection of tests.

The collision transfer of Model B is

`E_B = sum_(x=0,1) T_x tensor T_x = (P tensor P)/2`.

Let `v_+=(1,1)^T` and `v_-=(1,-1)^T`. Since
`P v_+=v_+` and `P v_-=v_-/2`, the four tensor eigenvectors give

`spec(E_B) = {1/2,1/4,1/4,1/8}`,

so its distinct nonzero spectrum is `{1/2,1/4,1/8}`. Both transfers are
diagonalizable. The initial vector `pi tensor pi` and trace functional see
only the `v_+ tensor v_+` mode. The additional eigenvalues have zero
observation coefficients.

These classical models are legitimate QHMMs: for each outcome `x` and hidden
coordinates `a,b`, use the matrix-unit Kraus operators
`sqrt(P_(ab)/2) |b><a|` for Model B (with the corresponding row/column
convention). They erase input coherences. The full quantum collision transfer
therefore has the same nonzero spectrum as the displayed four-dimensional
diagonal block, with additional zero modes. `P` is symmetric, so using the
transpose in the source transfer convention does not change this example.

## The exact failed inference and surviving invariant

Equality of scalar sequences implies that the coefficient of every frequency
in their difference is zero. It does not imply that an unobserved frequency
cannot occur in either full internal spectrum. Here the scalar collision
sequence is `2^(-L)` in both models; its only observable nonzero pole is
`1/2`. The displayed extra modes are invisible to that scalar sequence.

The surviving invariant is the minimal scalar recurrence (including visible
Jordan orders), or equivalently the poles after cancellations in the scalar
generating function. Minimal reachable-observable realization and Hankel
rank are established tools. This note does not supply a general new
QHMM-minimization theorem, nor establish that every later claim in the source
depends on the exact false scope in the same way.

`verify_hidden_spectrum.py` uses exact rational arithmetic to verify the
four eigenvector equations and every binary word through length ten. The
all-length equality follows from the written formula above, not those finite
checks. No message was sent to the authors or any external party.
