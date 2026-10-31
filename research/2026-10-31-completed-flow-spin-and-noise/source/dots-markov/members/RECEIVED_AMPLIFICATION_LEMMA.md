# Complete-isometry amplification: self-contained algebraic restatement

This restates the algebra used in the reviewed receiving ledger. It is not a new result or a reconstruction of an earlier archive. Known-success-amplitude amplification is ordinary machinery; the formulas below make its normalization and perturbation interface explicit.

Let a constructed unitary have a good rectangular block B=V/A, where V is an isometry on the unknown input and A is a known integer power of two. Input and output success reflections concern only designated source/work registers, not a projection onto the unknown system or retained reservoir state. Output Kraus-record registers are retained.

Set theta=pi/(4A+2) and c_A=A sin(theta)<1. One known flag rotation attenuates the entire good block to C=c_A B. Its ideal singular values are all sin(theta). Exactly A ordinary oblivious Grover iterations give unit success amplitude, since (2A+1)theta=pi/2. The output is the full isometry V, up to a known fixed phase. Applying this argument to a lone contraction K with unequal input-dependent singular values would be invalid.

Here is a dimension-independent operator perturbation bound. For any rectangular contraction C, form the selfadjoint contraction H_C=[[0,C],[C^dagger,0]]. The amplified good block is, up to a fixed sign, the off-diagonal block of the odd Chebyshev polynomial T_d(H_C), d=2A+1. For selfadjoint contractions X,Y and Delta=X-Y, the recurrence gives

T_d(X)-T_d(Y)=U_(d-1)(X)Delta
 +2 sum_(k=1)^(d-1) U_(d-1-k)(X)Delta T_k(Y).

Using ||T_k(Y)||<=1 and ||U_j(X)||<=j+1, the operator norm is at most d^2||Delta||. This telescopes actual operator products; it is not merely a scalar singular-value derivative assertion.

Thus a base-block error beta gives amplified good-block error O(d^2 beta). The entire implemented circuit is unitary before its output flags are discarded, so its failure norm is at most O(d sqrt(beta)). The total Stinespring error and hence unconditional output trace-norm error are bounded accordingly. All reference systems are included because the estimate is an operator-norm bound.

The final ledger chooses beta conservatively as a small fixed power of its per-call error divided by a polynomial in d. It charges the O(A) base calls, reflections, attenuation rotation and ordinary gate synthesis. A grows with the explicitly priced source normalization; it is not treated as an absolute constant when source conditioning varies. Finite phase/rotation accuracy is allocated over those calls. There is no normalized rare postselection.

The matrix H_C is an analysis device, not a new oracle that the implementation must acquire. The required circuit consists of the already constructed source unitary and its inverse, its two known workspace reflections, and the known attenuation flag.
