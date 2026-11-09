# P1 complete Xi return

Source: https://chatgpt.com/c/6af1a606-c6c8-83ec-b948-b552107573bf
Actual scientific user turn: 7c93835f-c8ce-4c0e-9d4b-4ee17ee47cb2; subsequent actual user turns 1b8037d2-e649-45e8-a5ae-319c827cd4fe and 0f596841-9a13-4780-8a98-d67d82f90a4b were each "please continue." Response: 61457110-8611-40aa-bd35-0f1adc56abca.
Exact original prompt reference: P1_FULL_BATCH_MINIMAX_AFTER_7A07_XI_20261109.txt; SHA-256 da8bba4a8b29cd687f3ba41d8cf73d03aff6c2e07b102163ea9d37cf4d36dedd, terminal LF omitted in the posted body.
Model: GPT-6 standard, Extra High verified at post and recovery. No ZIP identified in the completed response.

## Available visible activity

Original turn: Assessed research plan, explored coupling costs, and refined model.
First continuation: Explored coupling strategies, exchangeability, finite extensions, and Poisson parallelism.
Latest continuation, Worked for 27m 30s: Developed coupling strategies while assessing exactness and retention constraints.

> The accepted exact-\(m\) threshold and the expected-stopping lower bound remain the baseline. I’m focusing on whether an exchangeable, adaptively sampled archive can share source information across rows without disturbing the exact \(Q^m\) law. That is the main obstruction between the existing upper and lower rates.

Refined coupling ideas; Searched 9 websites; Balanced exactness and reuse; Evaluated adaptive batch coupling efficiency; Developed and evaluated coupling strategies with structural bounds; Assessed coupling costs, complexity, batching, and structural limits; Developed structural bounds and analyzed batch couplings; Searched 19 websites; Assessed batch coupling limits and refined oracle lower bounds; Evaluated adaptive archive bias and computed stopping-rule cancellation bounds.

> A second restriction now follows from the same polynomial argument: even unlimited target sampling cannot compensate for a fixed cap on fresh \(P\)-calls below the empirical-estimation scale. This helps isolate why the one-row factory’s rare, long stopping paths matter. I’m checking whether it extends to an expected-query lower bound without accidentally imposing a cap.

Assessed batch coupling.

## Complete response (verbatim)

# Continuation: exact whole-batch reuse minimax

The accepted bounds and the exact minimum-cost threshold remain in force. I have obtained a further structural result: **additional target samples alone cannot improve the optimal retained fraction beyond the original \(m\)\-sample histogram construction.** This holds even with unlimited adaptive \(Q\)\-sampling and stopping.

## 1\. New theorem: the fresh-\(P\)\-free barrier

Define

\[
D_m(P,Q)=
\mathbb E\left[
\operatorname{TV}\left(
\widehat P_m,\widehat Q_m
\right)\right],
\]

where the empirical measures come from independent samples of size \(m\)\.

**Theorem.** Among all universally exact algorithms making zero fresh \(P\)\-oracle calls, while allowing arbitrarily many adaptive fresh \(Q\)\-calls,

\[
\boxed{
\inf_A\mathbb E\left[
\frac1m\sum_{j=1}^m\mathbf1\{Y_j\ne X_j\}
\right]=D_m(P,Q)
}
\tag{1}
\]

simultaneously for every \(P,Q\)\.

The accepted \(m\)\-sample histogram matcher attains equality using exactly \(m\) fresh \(Q\)\-calls. Thus extra \(Q\)\-calls cannot improve this trade-off in the absence of fresh \(P\)\-calls.

### Proof: polynomial identifiability forces conditional exactness

Let \(A=\operatorname{hist}(X)\)\. For each possible count vector \(a\), define

\[
K_a(y)=\Pr(Y=y\mid A=a).
\]

This conditional probability is independent of the unknown numerical values of \(P\), because the algorithm makes no fresh \(P\)\-calls and, conditional on \(A=a\), the ordering of \(X\) is uniformly distributed over its type class.

Universal exactness gives, for every \(P\),

\[
\sum_{\substack{a_1+\cdots+a_d=m\\a_i\ge0}}
\binom{m}{a_1,\ldots,a_d}
\prod_i p_i^{a_i}K_a(y)
=\prod_{j=1}^m q_{y_j}.
\tag{2}
\]

The multinomial Bernstein polynomials of total degree \(m\) are linearly independent on the probability simplex. The constant function on the right has Bernstein coefficients equal to that same constant.

Consequently,

\[
\boxed{
\mathcal L(Y\mid A=a)=Q^m
\quad\text{for every type }a.
}
\tag{3}
\]

This conclusion includes adaptive \(Q\)\-sampling: none of its choices can introduce dependence on \(P\) once the old type is fixed.

Now let \(B=\operatorname{hist}(Y)\)\. Equation (3) implies that \(B\sim\operatorname{Mult}(m,Q)\), independently of \(A\)\.

For every pair of ordered words \(x,y\), the number of differing positions is at least the histogram transport distance\:

\[
\sum_j\mathbf1\{x_j\ne y_j\}
\ge\frac12\sum_i|a_i-b_i|.
\]

Taking expectations yields

\[
\mathbb E[\text{changed fraction}]
\ge D_m(P,Q).
\tag{4}
\]

The accepted permutation-equivariant histogram matcher attains equality, proving the theorem.

### Consequence

At \(P=Q=\operatorname{Unif}[d]\), the theorem yields exactly

\[
D_m(P,P)=\delta_{d,m}.
\]

Therefore, whenever

\[
\boxed{\eta<\delta_{d,m},}
\]

every admissible algorithm must have a positive probability of making at least one fresh \(P\)\-call under some law pair.

This is stronger than observing that the particular \(m\)\-sample archive matcher fails: **no amount of additional target-only sampling can fix the deficiency while preserving exact \(Q^m\)\.**

## 2\. Stronger deterministic-cap obstruction: only the \(P\)\-calls need be capped

The preceding argument extends to a result that distinguishes adaptive expected-query algorithms from bounded-sampling schemes.

**Theorem.** Suppose a universally exact algorithm makes at most \(k\) fresh \(P\)\-calls on every execution, with no restriction on the number of \(Q\)\-calls. Put \(n=m+k\)\. Then, for every \(P,Q\),

\[
\boxed{
\mathbb E[\text{changed fraction}]
\ge
\mathbb E_{A\sim\operatorname{Mult}(n,P)}
\operatorname{TV}\left(\frac An,Q\right).
}
\tag{5}
\]

### Proof

After the algorithm terminates, pad its unused \(P\)\-call positions with independent fresh \(P\)\-draws. These draws are analytical padding for the proof; they are not being declared free algorithmic resources.

The resulting length-\(n\) \(P\)\-word consists of the actual \(m\) original observations and \(k\) additional iid observations.

Condition on its histogram \(A=a\)\. Its complete ordering is uniform over its type class, independently of the numerical values of \(P\)\.

Applying the same multinomial Bernstein identity gives

\[
\mathcal L(Y\mid A=a)=Q^m.
\tag{6}
\]

For every original index \(j\),

\[
\mathcal L(X_j\mid A=a)=a/n,
\qquad
\mathcal L(Y_j\mid A=a)=Q.
\]

The elementary coupling inequality therefore yields

\[
\Pr(X_j\ne Y_j\mid A=a)
\ge\operatorname{TV}(a/n,Q).
\]

Average over \(j\) and \(A\) to obtain (5).

### Uniform-law consequence

Choose \(P=Q=\operatorname{Unif}[d]\)\. Equation (5) becomes the exact computable obstruction

\[
\boxed{
\eta\ge
\phi_{d,n}:=
\frac{d}{2n}
\mathbb E\left|
\operatorname{Bin}(n,1/d)-\frac nd
\right|.
}
\tag{7}
\]

Standard binomial absolute-deviation bounds give

\[
\phi_{d,n}\asymp
\min\left\{1,\sqrt{\frac dn}\right\}.
\]

Thus a deterministic \(P\)\-query cap compatible with the accuracy requirement must satisfy

\[
\boxed{
m+k=\Omega(d/\eta^2).
}
\tag{8}
\]

There is no restriction on target-query stopping or computation in this statement.

It does **not** imply \(\mathbb E N_P=\Omega(d/\eta^2-m)\)\. The accepted one-row factory already shows why such an inference would be false: rare, expensive executions can permit much smaller expectations.

The new distinction is that the bounded-query obstruction can be imposed on **fresh \(P\)\-calls alone**, while allowing unrestricted adaptive \(Q\)\-sampling.

## 3\. Reduction of the candidate optimal rate to one critical batch size

There is also a precise reduction of the outstanding constructive question.

Define

\[
M(d,\eta)=\left\lceil\frac d\eta\right\rceil.
\]

**Critical-batch reduction.** Suppose one constructs a uniformly exact, permutation-equivariant \(M\)\-row coupler with

\[
\sup_{P,Q}\mathbb E[N_P+N_Q]\le K M
\]

for a universal constant \(K\), while satisfying the original TV-plus-\(\eta\) retention guarantee.

Then a computably uniform algorithm achieves, for every \(m\),

\[
\boxed{
C^*(d,m,\eta)=\Theta\left(m+\frac d\eta\right).
}
\tag{9}
\]

To prove sufficiency, for \(m<M\), acquire \(M-m\) fresh \(P\)\-samples, append them to the actual old rows, run the \(M\)\-coupler and project back onto the designated original indices. Uniform random permutation and inverse permutation ensure that each original position receives the mean retention guarantee and that the projected output has exact law \(Q^m\)\.

For \(m>M\), partition the old rows into blocks of size \(M\), with one possibly shorter final block. Run independent copies of the construction, padding only that final block. The outputs of the blocks are independent, so concatenation has exact law \(Q^m\)\.

The new query bound is \(O(m+M)\)\. The accepted lower bound is already \(\Omega(m+M)\), proving (9).

Conversely, if (9) holds with a computably uniform attaining algorithm, that algorithm at \(m=M\) necessarily has \(O(M)\) expected cost.

Hence **achieving the candidate rate \(\Theta(m+d/\eta)\) in all regimes is equivalent, up to universal constants and the computational uniformity requirement, to obtaining \(O(d/\eta)\) cost at the single critical batch size \(m=\lceil d/\eta\rceil\)\.**

This is a reduction, not a claim that the required critical-batch coupler exists.

## 4\. Two exact-product obstructions to apparent shortcuts

### Shared empirical estimates do not preserve independence

Suppose an algorithm first constructs a shared random object \(H\) using auxiliary oracle samples, independently of the actual old rows.

It then applies the same estimated transition kernel to every old row, with independent randomness conditional on \(H\)\.

Write \(R_H\) for the resulting one-row output distribution. Conditional on \(H\), the outputs are iid \(R_H\)\.

If the unconditional batch law is exactly \(Q^m\) for \(m\ge2\), then for every label \(i\),

\[
\mathbb E[R_H(i)]=q_i,
\qquad
\mathbb E[R_H(i)^2]=q_i^2.
\]

Therefore

\[
\boxed{\operatorname{Var}(R_H(i))=0,}
\]

and hence

\[
\boxed{R_H=Q\quad\text{almost surely}.}
\tag{10}
\]

This proves that a random learned transition kernel cannot be merely unbiased on average. Under conditional iid application, it must already be exactly calibrated almost surely.

The theorem does not exclude shared learning followed by jointly dependent output generation. Rather, it shows why that joint correction is mathematically necessary.

### Adaptive histogram stopping can destroy exactness

Consider the binary case \(d=2,m=1\), with \(P(1)=p,Q(1)=q\)\.

Use this natural-looking adaptive archive construction\:

1. Draw one fresh \(Q\)\-label \(Z_1\)\. If \(Z_1=X_1\), return \(X_1\)\.
2. Otherwise draw one extra \(P\)\-label and one extra \(Q\)\-label, optimally histogram-match both two-element archives, and return the output corresponding to the actual \(X_1\)\.

For either fixed archive length, the relevant matcher is exact. But direct enumeration of the adaptive procedure gives

\[
\boxed{
\Pr(Y_1=1)
=q+\frac12q(1-q)(2p-1).
}
\tag{11}
\]

For example, at \(p=0.7,q=0.3\),

\[
\Pr(Y_1=1)=0.342\ne0.3.
\]

The adaptive procedure is therefore invalid.

Its failure is not a lack of sufficient samples. The stopping rule conditions on early matching success, breaking the exchangeability argument that establishes exactness for fixed-length archives.

This eliminates a straightforward attempted improvement: keep extending the balanced archive only until the observed mismatch is sufficiently small. A different exactness mechanism would be required.

## 5\. Updated result ledger

| Result | Status |
|--------|--------|
| \(C^*(d,1,\eta)=\Theta(d/\eta)\) | Accepted, complete |
| Exact \(m\)\-query floor iff \(\eta\ge\delta_{d,m}\) | Accepted, complete |
| Expected-stopping lower \(\Omega(m+d/\eta)\) | Accepted, complete |
| Unlimited \(Q\)\-sampling cannot improve the optimum without fresh \(P\)\-calls | New theorem |
| Fixed cap on fresh \(P\)\-calls alone requires \(m+k=\Omega(d/\eta^2)\) | New strengthened cap result |
| Critical-batch reduction at \(m=\lceil d/\eta\rceil\) | New reduction |
| All-regimes matching minimax upper and lower | **Open** |

The quantitative all-regimes bounds remain

\[
\boxed{
c\left(m+\frac d\eta\right)
\le C^*(d,m,\eta)
\le C\min\left\{
\frac{md}{\eta},\
m+\frac d{\eta^2}
\right\}.
}
\]

The exact-\(m\) regime and bounded-\(m\) regime remain closed at their accepted scopes.

The main outstanding issue has been narrowed constructively: can one produce \(M=\lceil d/\eta\rceil\) exact iid target outputs from \(M\) actual old rows with only \(O(M)\) expected fresh calls and mean disagreement at most \(\operatorname{TV}(P,Q)+\eta\)?

A positive solution would prove the full candidate rate \(\Theta(m+d/\eta)\)\. A negative solution would require a stronger expected-query lower bound at that critical scale. Neither has been established in this continuation.

The related literature on multiple-output Bernoulli factories confirms that sharing factory input across exact independent outputs is a substantive issue, but it does not supply the missing batch coupling theorem. citeturn313038search5

**Conclusion\:** This continuation establishes a sharp \(P\)\-free impossibility theorem, a strengthened bounded-\(P\)\-sampling obstruction, and a reduction to one critical batch scale. It does not yet establish the requested universal minimax equivalence or a new all-regimes attaining algorithm.
