# Output-sensitive residual filters: degree and precision cannot both be discarded

27 October 2026. These are restrictions on proposed repairs of the supplied
replacement-form algorithm, not lower bounds for all circuit algorithms.

## Setting

For an acyclic Boolean program with input x and stored states y_1,...,y_s,
write e_j=y_j+f_j(x,y_1,...,y_(j-1)) over F_2. At each fixed x, the residual
map y -> e is a bijection. The intended trace is e=0. The observation here
concerns a selected output; it does not require preserving all internal
observables. Protected final evaluation means the output is evaluated exactly
after the noisy states have been supplied. This is a legitimate subproblem
of causal-kernel proposals, not an assumption that all raw circuits have this
form.

## 1. One selected parity output forces high rational selector degree

Let chi(e)=(-1)^(e_1+...+e_s). Suppose a rational polynomial w(e) is used as a
normalized residual weight and must preserve the parity output at the correct
trace:

    sum_e w(e) = 1,
    sum_e w(e) (1+chi(e))/2 = 1.

Then deg w >= s.

Proof. The equations imply sum_e w(e)chi(e)=1. If deg w<s, every monomial in
w omits at least one variable e_j, even after Boolean multilinear reduction.
The two terms obtained by summing e_j=0,1 cancel because chi changes sign.
Consequently sum_e w(e)chi(e)=0, a contradiction. This is exact over any
characteristic-zero field. It applies even when w depends on the original
input x, by fixing x. Rational coefficients and negative weights do not help.

The example is realizable with s constant-zero stored states followed by a
protected XOR of all those states. It is intentionally not a hard circuit:
constant propagation solves its original semantics immediately. Its purpose
is to show that a generic low-degree residual reweighting rule cannot derive
its degree bound solely from original input count or output count.

The bound is attained by w(e)=2^(-s)(1+chi(e)), which is degree s and has
mass one. It is uniform on the even-parity residuals and zero elsewhere.
This already shows a crucial distinction: rational polynomial degree s does
not imply large Fourier support. The displayed weight has two Fourier terms.

## 2. A one-row parity filter incurs a large exact normalization

The same example has a perfect rank-one F_2 residual filter:

    e_1+...+e_s=0.

All its 2^(s-1) residuals preserve the selected parity output. More generally,
suppose a rank-r residual filter A e=0 preserves the requested output at each
input. Then summing all accepted traces under that filter gives

    Z_filtered = 2^(s-r) Z_original.

Proof. At every input the residual bijection gives exactly 2^(s-r) admitted
traces, and output invariance makes all of them contribute the same indicator.

Therefore exact recovery from a residue modulo 2^P requires, in general,

    P >= (s-r)+(n+1)

when the original count may be any integer in [0,2^n]. This is the uniform
sufficient precision; necessity in the worst case follows because residues
modulo 2^P determine the quotient only modulo 2^(P-(s-r)) when P>=s-r,
and are all zero when P<=s-r. At P=(s-r)+n, counts 0 and 2^n coincide.

This is not an assertion that every output-invariant filter needs high rank.
The example shows the opposite. The obstruction is that dividing out an even
multiplicity consumes 2-adic precision. One cannot retain only n+1 output
bits before that division. A specialized algorithm that never materializes
the multiplicity might evade this restriction and would require an additional
construction.

## 3. Odd-modulus parity lifts pay another cost

One possible repair is to count modulo an odd prime p, where 2^(s-r) is
invertible. This avoids the normalization loss, but does not preserve the
source's low-degree polynomial parity lift.

Let a(Y) be a polynomial over F_p, p odd, that equals the parity indicator
1 when Y is even and 0 when Y is odd for every integer Y in [0,m].

* If m>=p, no such polynomial exists: 0 and p are the same field point but
  have different target values.
* If m<p, every such polynomial has degree at least m, unless m=0.

For the second claim, its m-th forward difference at zero is

    Delta^m a(0) = (-2)^m/2             (m>=1),

up to the harmless convention for choosing the even/odd indicator. It is
nonzero modulo p. Every polynomial of degree below m has zero m-th forward
difference, so degree at least m is necessary. The same obstruction applies
to coefficients with denominators invertible modulo p, by reduction.

Over the integers or rationals, the same difference argument shows degree at
least m for exact agreement on 0,...,m. The source's short parity polynomial
works modulo powers of two because the high finite differences acquire powers
of two. It does not transfer to an odd-modulus setting while keeping this
degree advantage.

This statement concerns polynomial functions of the integer Hamming weight.
It does not exclude Fourier characters, extension-field tensors, or an entirely
different odd-prime contraction algorithm. Those alternatives must pay for
their entries and their own reconstruction rather than citing the source's
2-adic parity-lift lemma unchanged.

## 4. Remaining viable attack

Output-specific Fourier sparsity survives the rational-degree barrier: the
parity example has only two Fourier terms. For a general quadratic Boolean
circuit, expanding consistency constraints in Fourier characters converts a
fixed dual character into a quadratic exponential sum, which is computable
by Gaussian elimination. But the dual sum has one bit per nonlinear state.
No bound reducing that sum to original input count has been obtained here.

A useful next target is a raw circuit class for which the *observable Fourier
family* can be constructed and summed efficiently, with all inherited affine
states eliminated. This is a specific remaining construction problem, not a
claimed representation theorem. Standard affine and Clifford-type simplifica-
tions must be separated from a new algorithm if this avenue is pursued.

## Executed checks

`output_filter_checks.py` verifies the selector degree by exact rational sums,
the rank-one multiplicity, the normalization collision, and the finite-
difference odd-modulus obstruction. Its results are written to
`output_filter_results.json`. These checks are algebraic identity tests, not
performance comparisons or implementations of the asymptotic source counter.

## Governing source

OpenAI, *The Exponential Time Hypothesis is False*, 25 October 2026, pinned
commit 7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a, Sections 5.1--5.2 for the
2-adic parity lift and Appendix D.4.4 for precision-sensitive reconstruction.
The parity and finite-difference arguments above are elementary, and no
historical novelty is claimed for them.
