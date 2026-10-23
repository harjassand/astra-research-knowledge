# Cycle8 PRO3 scientific checkpoint

## Decision and strongest result

The public-asymmetry convergence question is closed internally by a sharp
necessary-and-sufficient criterion. Preserve the accepted Cycle7 reciprocal
critical laws and the unrestricted mismatch obstruction. The new result
explains exactly when a genuine public proposal bound removes that
obstruction.

For fixed K>0, 0<alpha<1 and beta=1-alpha, let the run at horizon n use
0<eta_n<1, finite kappa_n>=0, and a fixed target-independent reciprocal
row-stochastic Q satisfying

\[
 \max_{x\ne y:Q_{xy}>0}|\log(Q_{yx}/Q_{xy})|\le A_n<\infty.
\]

Keep positive pi,q, the one population D(pi||q)<=K budget, q initialization,
the actual two-stage reciprocal Hastings acceptance, rejection diagonals,
and C=(I+alpha G+beta L)/2. Define R_n as the supremum of actual full-chain
TV at time n over this class. Then

\[
 \boxed{
 R_n\to0\quad\Longleftrightarrow\quad
 \frac{\eta_n\log n}{1+|\kappa_n-\eta_n|A_n}\to\infty.}
\]

All parameters stay fixed within each run; supports can grow across the
supremum. Kappa and A may grow without a uniform bound, eta may vanish,
and the mismatch sign may alternate. The criterion covers A_n tending
to zero with an arbitrarily large positive exponent mismatch. It does
not impose a hidden minimum atom, support cap, target table, normalizer,
or empirical population-KL estimate.

For fixed mismatched powers, the exact condition is A_n=o(log n).
Thus a fixed finite public asymmetry bound makes any fixed mismatch
harmless for uniform convergence, although unrestricted reciprocal
proposals can still produce the preserved positive floor.

## A finite upper and the ordinary-optimal regime

Put D_n=|kappa_n-eta_n|A_n, v_n=eta_n log n/(1+D_n),
r_0=alpha exp(-K)/beta and c_0=min(1/4,r_0/8)/4.
The proof gives constants C,n_0 depending only on K,alpha such that

\[
 R_n\le
 \frac K{\log n-4\log\log n-1}
 +\frac C{(\log n)^2}+2e^{-c_0v_n}
 \qquad(n\ge n_0).
\]

If v_n/loglog n tends to infinity, then

\[
 (\log n)R_n\longrightarrow K.
\]

This stronger condition is sufficient for amplitude K, not claimed
necessary. The exponential constant in the displayed upper is deliberately
nonsharp. No exact rate or critical amplitude for general public
asymmetry policies follows from it.

## Why the upper works

Cycle7's reverse-proposal Jensen argument is retained. The actual screen is
r_q^eta exp(xi), with |xi|<=D. The changed finite scalar envelope is

\[
 H_w(D)=\sup_{0<z\le1}
       \left\{w e^{D\theta p/\eta}z^{p(1-\theta/\eta)}-z\right\},
 \qquad p=(1-\theta)^{-1}.
\]

The negative term comes from actual accepted outflow in the rejection
diagonal. Off-diagonal distortion alone would not give this energy bound.
Reverse-Q Jensen coefficients use the outgoing Q row at each destination,
so arbitrary counting-column sums and growing support are allowed.

Taking theta proportional to eta/(1+D) gives a uniform local energy
margin paid by the actual global killing probability. The absorbed
first-hit counter accumulates every hit time. The full-chain decomposition
then follows each hit by the original C, including all later exits and
returns.

The accumulated multiplier is retained: for fixed eta and bounded D it
need not approach one. Its logarithm is O(theta loglog n), while the
first-hit term supplies -theta log n. Their combined exponent gives the
uniform upper even when theta is arbitrarily small.

## Why the condition is necessary

If eta_n log n stays bounded on a subsequence, the accepted symmetric
three-state mechanism already supplies a positive retained error. The
new obligation is the case where mismatch grows on the screen's scale.

Suppose D_n/(eta_n log n)>=a>0 on a subsequence. Choose one fixed depth
J with Ja>1. Set M=ceil(exp A_n) and use a genuine labelled M-ary tree
plus a core. Positive mismatch expands from root to leaves; negative
mismatch coalesces from the leaf union to the root. On every edge the
native reverse-proposal ratio is exactly exp(A_n) or exp(-A_n), and
both native outgoing row budgets are satisfied.

Choose the native q ratios so that the first screen is exactly one.
Correct per-vertex target Hastings ratios give aggregate forward local
probability f_n and reverse probability f_n/n^2. Level multiplicities
are included; a level-total ratio is never substituted into an individual
acceptance formula.

Let z be the level q ratio, V=-log z, q_i=bz^i and

\[
 p_n=\frac1{(\log n)^2(1+V)},\qquad
 \pi_i=p_n n^{-2(J-i)},\qquad 0<b<1-e^{-K}.
\]

The 1/(1+V) factor is essential when moving exponents make V enormous.
It keeps the entire noncore entropy contribution O(J/(log n)^2).
The full instance has KL tending to -log(1-b)<K. Meanwhile the
terminal importance weight satisfies W_J/n->infinity, so terminal
escape during n steps tends to zero.

A conservative path event marks every global attempt as failure before
capture and counts actual local forward/backward moves and holds.
Deterministic waiting windows prove

\[
 \liminf R_n\ge
 b\left(\frac{1-\alpha}{2\alpha+1-\alpha}\right)^J>0
\]

on the adverse subsequence. This is a positive lower bound, not the exact
floor. Multiple crossings are crucial: one crossing would miss small
positive ratios a below one. These two necessity branches exhaust
every policy for which v_n fails to diverge.

## Ordinary comparison and significance

Pure proposal-start IMH remains the strong comparator. On exactly the
new native lower inputs, its full-return bound is

\[
 \|qG^j-\pi\|_{\rm TV}
 \le \frac{p_n}{1-n^{-2}}
       +\frac{bz}{(1-b)(1-z)}+b^{j+1}\longrightarrow0
\]

for every j->infinity, including any deterministic j/n->t>0.
The hybrid instead retains positive error on the selected subsequence.
For fully known analytic targets, direct sampling and feasible enumeration
also remain allowed.

The result is a robustness theorem with an adverse computational comparison.
It is not a practical sampler speedup. Native indices, proposal/target
evaluations, reverse-Q probabilities, caching and precision remain charged.
The exact-real lower may require enormous supports and tiny masses; no
floating-point instability or finite-word theorem is claimed.

Closest inspected primary context: Sherlock and Lee's delayed-acceptance
variance-bounding results, including bounded-discrepancy inheritance and
examples of deterioration; and Andrieu, Lee, Power and Wang's ordinary
IMH Dirichlet and weight-tail weak-Poincare results. Their precise
relationship is recorded in COMPARATOR.md and SOURCES.md. Historical
originality and external acceptance remain unknown.

## Acceptance and executed evidence

The principal integrated and accepted the two distinct contributor
arguments and the complete necessity split. A fresh source-bound
challenge read the exact principal proof and both contributions and
found no unresolved load-bearing defect or required repair. Its verdict
binds to principal SHA256

eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1.

The principal personally implemented and ran frozen exact-rational
checks: 128 local and 128 mixed all-vector energy certificates,
384 first-hit identities, 16 original-return identities, and eight
fourteen-state native tree configurations with 24 full-law/lumping,
capture/retention and ordinary comparison checks. All assertions
passed on the first run.

The finite fixtures are algebra checks, not evidence for a limiting
rate. Their 24 conservative TV lower bounds are negative at the fixed
small inputs; that numerical limitation is preserved without retuning.
The asymptotic positive lower is proved analytically.

The diagnostic body used about 0.797 wall seconds and 0.795 CPU seconds,
with 14,080 KiB peak RSS. These are replayable computation costs, not
discovery costs. Inference, token, monetary and total research costs
are unavailable. Detailed measured receipts distinguish source,
contributor, review, execution and delivery stages.

## Continuation decision

Close the exact convergence criterion at this scope. The next selected
question is the sharp reachable-transport rate in the convergent region,
especially v_n of order loglog n. Determine whether v_n alone governs
the rate or whether the separate public asymmetry and native multiplicity
budgets produce different rates at the same v_n.

A useful advance must combine a support-uniform upper with an admitted
geometry and one KL allocation. Optimizing the scalar envelope alone,
fitting finite curves, or tuning a favorable application would not answer
it. The mission remains active; no numerical jobs are left running.

## Delivery status convention

The unchanged Cycle7 ZIP and its nested accepted source chain are included.
The common Cycle8 source was read from its supplied attachment and verified
against the exact frozen bytes. No other owner's work or retired campaign
was resumed. Final archive identity and private roundtrip/handoff receipts
are external to this frozen scientific source. Delivery is not evidence
of Max's or the evaluator's reading, scientific acceptance, or integration.

