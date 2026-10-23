# Failures and corrections that affect continuation

These are scoped failures of arguments or shortcuts. They do not close the
communication programme or turn a lower bound into a capacity converse.

## Scalar first response does not persist

The Cycle7 certificate is \(T_k(\sigma H)=v_kI\). An initially plausible
simplification was that its contracted higher coefficients might also be
scalar. Exact coefficient enumeration defeats that at four calls:
\[
 \operatorname{Tr}_A[(\sigma H\otimes I)G_2]
 =-\frac{113}{64}I-\frac3{64}\mathrm{SWAP}_{1,2}.
\]
The two eigenvalues are \(-29/16\) and \(-55/32\). The actual all-order
argument therefore keeps a full coherent-prefix operator remainder.
No extrapolation from the scalar two- or three-call cases is used.

Source: `contributions/fourth_order_words/FOURTH_ORDER_WORDS.md`,
`exact_coefficients.py` and its exact rational JSON.

## Deletion of spectator interactions does not change the input operator

The all-order response has coefficients obtained by analytically deleting
common spectator stays. Those coefficients contract against the original
full-\(k\) input \(H_{ij}\), not a shorter-block optimizer.

At \(k=3\), the contractions for deleting positions \(0,1,2\) are respectively
\(I/8,I/32,I/8\). Their sum is \(9I/32\). Replacing each by the two-call
susceptibility would give \(3I/8\), which is false. These deletions are an
algebraic representation; they do not remove charged physical calls.

## Charge preservation alone is insufficient for the reusable pair interface

An exact bulk matrix element is
\[
 \langle0101,1211|G(b)|1010,1211\rangle=b^2(1-b)^2.
\]
There is no first-order term. Thus a charge-preserving input connecting four
endpoint positions has a genuine fourth-order response outside the pair
decomposition. For
\(J=|0101\rangle\langle1010|+\mathrm{h.c.}\), its contracted diagonal bath
element equals \(b^2(1-b)^2/32\). A sufficiently small perturbation of the
strictly positive \(\sigma\) by \(\sigma J\) is a valid input density.

The independent reviewer verified this with a separate raw prepend/pop
implementation and sixteen complementary mask pairs. It imports no
inherited representation code. This is an explicit counterexample to dropping
pair support, not merely an absent proof.

Consequently a Gibbs or exponential positive parametrization of the present
input is a distinct operation. Its powers introduce higher charge coherences;
the current response lemma cannot be applied without a new bound.

## The bulk formula cannot be extended through the physical root

Take one input port \(0\) and a \(+1\) vacuum eigenvector of \(R\). The device
keeps the bath at depth zero for every beta; the actual depth displacement is
zero. The falsely global diagonal bulk formula would give \(-(1-b)\).
The proof retains the finite root remainder and uses the inherited operator
Lyapunov/coding interface. No root approximation or reflecting cutoff is used.

## A generic uncontracted remainder pays the wrong quantity

Bounding the full \(G(b)-G_0-bG_1\) and then multiplying by a generic norm of
the input perturbation is valid but retains the old restrictive temporal
window. The exact all-order response resolves this obstruction by contracting
against the actual pair-supported \(H\) first. The reference drift
\(D_b(\sigma)=0\) is exact at every beta and is never charged as an error.
The diagonal correction \(Y\) also has an exact response, so no generic
nonlinear remainder is needed for it.

This failure concerns a sufficient estimate; it was not evidence of a
capacity plateau or an impossibility of longer blocks.

## Precision repair

The comparator uses the natural-log function
\[
 f(t)=\big((1+t)\ln(1+t)+(1-t)\ln(1-t)\big)/2.
\]
Its second derivative is \(1/(1-t^2)\), while
\(1-h_2((1+t)/2)=f(t)/\ln2\). The initial wording was clarified to make this
logarithm convention explicit. The inequality, constants and conclusions
did not change. The independent reviewer accepted the corrected source.

An assembly `apply_patch` context mismatch was corrected before the final
source was reviewed. It was not a scientific counterexample or a missing
piece of proof.

## Earlier closures and present limitation

The exact susceptibility problem is solved and is not reopened. Closed iid,
balanced-only, diagonal, product-stationary, reflecting-cutoff and fixed-four-
call improved-power searches remain closed at their proved scope.

The present proof uses \(bk^2\le1/16\). It does not show that positivity
requires this scale, and it does not establish a stronger exponent beyond
\(\beta^3\). The next spectral question is chosen because the new response
bound has removed the former nonlinear bottleneck, not because a finite-size
trend suggests a conjectured improvement.
