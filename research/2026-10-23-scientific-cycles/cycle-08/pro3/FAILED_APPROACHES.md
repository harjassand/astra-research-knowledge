# Attempts and limitations that changed the Cycle8 decision

## 1. A one-crossing threshold is insufficient

An initial single-crossing picture would require a discrepancy of roughly
eta log n on that edge to cancel the proposal-mass drop of a retained trap.
It would miss every fixed positive ratio D/(eta log n) below one.

Decision: retire that proposed necessity threshold. A native depth J with
J a>1 accumulates proposal-mass loss across finitely many accepted crossings
when D/(eta log n)>=a. Each crossing has a fixed chance of beating the next
global attempt, so fixed J preserves a positive amount of captured mass.
The native row budgets and per-vertex ratios are proved explicitly.

This was a mathematical insufficiency identified during construction, not
a failed numerical experiment.

## 2. A target mass chosen only as a power of log n is not uniform

If moving kappa or A makes V=-log z arbitrarily large, a fixed choice such
as p=(log n)^-4 need not satisfy p J V=o(1). The single KL budget could fail.

Decision: use p=1/[(log n)^2(1+V)]. The exact entropy sum is then
O(J/(log n)^2), while terminal retention still follows from monotonicity
of (1+V)exp(-JV). This removes an unnecessary upper bound on mismatch
size and extends the criterion to every finite moving public policy.

## 3. Transient importance ratios need not be below the core

At enormous V, intermediate W_i can exceed W_star and even diverge.
A capture calculation that treated every global proposal to the core as
an accepted killing event would therefore lack its premise.

Decision: define a conservative lower event that marks every global
attempt as failure, including actual rejections. This has probability
alpha/2 per step independently of those target comparisons. The real
chain remains unchanged. Actual local backward events and holds give
the deterministic-window calculation. It sacrifices a constant but
closes the uniform necessity obligation.

## 4. Gamma tending to one is neither needed nor generally true after accumulation

In the upper proof theta is eta epsilon_0/[2(1+D)]. For fixed eta and
bounded D, N theta grows like loglog n. Consequently the accumulated
Gamma^(N/p) need not tend to one.

Decision: retain log Gamma throughout. Its growth is O(N theta), while
the first-hit factor contributes -theta log n. Their ratio tends to zero
uniformly, even for very small theta. The proof uses the combined
exponent, never a false Gamma^N=1+o(1) claim.

## 5. Scalar distortion or Dirichlet comparison alone does not settle this law

The elementary bound |log(S/S_matched)|<=D does not account for actual
rejection outflow, cold proposal initialization, growing support, or
retained first-hit mass. A scalar envelope is also not an attainable
native transport geometry. A generic n-times-one-step-TV bound was not
pursued as a completion method: it would require a much smaller
perturbation than the logarithmic asymmetry criterion proved here.

Decision: reuse reverse-proposal Jensen WITH the original diagonal and
accepted outflow, then the absorbed/full-return interface. Use a separate
native construction for necessity. No finite-time TV ordering is inferred
from off-diagonal acceptance or Dirichlet ordering.

## 6. Frozen finite fixtures do not numerically show the asymptotic floor

All required exact finite assertions passed on their first execution.
At the chosen small rational p and b, all 24 conservative TV lower
numbers are nonpositive. They are therefore numerically vacuous as
positive TV-floor certificates. The marked capture probabilities are
positive, and their event/retention inequalities and the native matrices
are checked exactly. The asymptotic positive floor follows from the
proved p_n->0, fixed-depth capture, and n d_T->0 calculation.

Decision: preserve the frozen fixtures and this limitation. Do not tune
p, b, depth or horizon after seeing the answers to manufacture a favorable
plot. Finite law comparisons vary with orientation and parameters and
do not establish a general sampler ordering.

## 7. Exact convergence is not an exact general risk function

The coarse upper has exp(-c_0 v_n) with a deliberately nonsharp constant.
The depth-J lower proves a positive error subsequence when v_n fails to
diverge. It does not give the exact positive floor or a matching rate
throughout the convergent region.

Decision: close only the convergence criterion. Select the sharp
transport rate, especially v_n of order loglog n, as the next scientific
question. Whether v_n alone suffices for a sharp rate is itself unresolved;
native multiplicity and the separate asymmetry scale may matter.

## Preserved earlier closures

The symmetric and reciprocal critical laws, global-boundary equality,
first-order laws, fixed-screen/prefix/optional-prefix results, and
strict one-step searches remain closed at their accepted scopes.
The B3 pISO mass correction, failed full halo inference and frozen
criterion, closed metadata case, and R3/anMC rejection are preserved.
No retired empirical campaign or other owner's programme was reopened.

