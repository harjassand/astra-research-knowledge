# PRO3 continuation after Cycle10

23 October 2026 Australia/Brisbane. Scientific ownership remains with PRO3.

Read CRITICAL_TRANSPORT_THEOREM.md first, REPORT.md, contributors/ENDPOINT_UPPER.md,
contributors/CRITICAL_NATIVE_LOWER.md, the source-bound review in reviews/,
INFORMATION_AND_COST_CONTRACT.md, FAILED_APPROACHES.md and COMPARATOR.md.
The exact Cycle9 predecessor ZIP is unchanged in sources/. Newer verified local
science takes precedence over this seed.

## Preserved exact native class

Finite labelled positive pi,q, D(pi||q)<=K>0, fixed alpha in (0,1), beta=1-alpha;
q initialization. Public A_n finite, 0<eta_n<1, kappa_n>=0. Q is fixed,
target-independent, row-stochastic, reciprocal, with actual max absolute log
reverse/forward ratio <=A_n. Off diagonal
L_xy=Q_xy min(1,S_xy)min(1,t_xy/S_xy),
S_xy=(q_y/q_x)^eta(Q_yx/Q_xy)^kappa,
t_xy=pi_y Q_yx/(pi_x Q_xy).
Keep the actual diagonal and C=(I+alpha G+beta L)/2. Every parameter stays fixed
within a run. Support may grow. TV is half l1; logs natural. No normalizer/table,
population-KL inference, free precision/index/reverse-Q or absorbed sampler.

## Closed new results

Fix d=|kappa_n-eta_n|A_n>0 exactly. Put ell=log n, L=log ell, u=eta_n ell,
r=alpha exp(-K)/beta, b0=1-exp(-K), h(a)=log(1+r exp(a)), gamma=h(0),
t=h'(0)=r/(1+r), d_star=gamma/t and c(d)=inf_a h(a)/(d+a).
Assume c(d)u=L+s+o(1).

1. If r>=exp(d), including equality, then
   ell R_n -> max(K,b0 exp(d-s)/r).
   Actual one-crossing lower; new weighted upper w=max(1,r_b exp(-d)).
2. If r<exp(d), d<=d_star, including equality, then
   ell R_n -> max(K,b0 exp(-s)).
   Interior attenuation pays integer rounding; d=d_star requires floor depth.
3. If d>d_star, the unrestricted limsup is exactly max(K,b0 exp(-s)).
   The unrestricted liminf is at least
   max(K,b0 exp[-s-gamma(1-d_star/d)]).
   If b0 exp(-s)<=K, the full limit is K in this regime as well.

An actual two-sign native family has
ell TV=b0 exp[-s-Psi({u/d})]+o(1),
Psi(x)=min((dt-gamma)x,gamma(1-x)). Its own amplitude oscillates; the
unrestricted class supremum is NOT proved to oscillate. Every phase is
approached along integer horizons under the allowed o(1) policy perturbation.

## New operations and exact proof obligations

The accepted finite weighted energy and all-return interface now operates at
the endpoint, with N log Gamma=o(1), not merely Gamma->1. The three-cell
information inequality k+ell a<=K+o(1) couples low-W mass and high-W tail.
At k<K a fixed larger c suppresses transport; at k=K the high-W leading
budget disappears. In the clipped branch a convex single-budget allocation
with the weighted boundary yields the reciprocal exp(d)/r coefficient.

The native family uses b_n=b0-L^-2, p_T=ell^-4, chi~(L+1)^4,
Q_parent,child=1/(M+exp A), Q_child,parent=exp A/(M+exp A), real diagonals.
Expansion M=ceil(exp A (L+1)^4); coalescence M=ceil(exp A/(L+1)^4).
Negative mismatch implies A>=d/eta, paying coalescence rounding.
For integer depth J, T=ell+6L+log b_n,
a=[eta T/J+eta log chi-d]_+, V=(d+a)/eta-log chi, z=exp(-V),
q_i=b_n z^i, pi_i=ell^-4 n^-2(J-i), with actual per-vertex division.
Actual local forward/reverse aggregate probabilities are f exp(-a) and
f exp(-a)/n², f=chi/(1+chi). KL slack L^-2 dominates positive terminal
entropy O(ell^-3). W_terminal>=n ell²; full terminal escape over n steps is o(1).

Uniform core hazard bounds pre-hit time even when forward acceptance is rare.
Exceptional reverse/global off-level moves before core or terminal cost
O(z+n^-2). Full-law contraction after core and actual retention after terminal
give TV=b_n exp[-J h(a)](1+o(1)). Complete levels are strongly lumpable;
arbitrary within-level query events are not covered by that partition.

## Exact restricted obstruction and LIVE frontier

The killed forward-control model permits progress x>0 with attenuation
(x-d)_+, competing fixed killing ratio r, paid holds and all history-dependent
mixtures. Its exact value is exp[-min_J J h((U/J-d)_+)]. A bounded
super-solution excludes improvement from changing actions after holds.
For d>d_star only floor/ceiling depth minimizes, leaving the phase Psi.

The missing universal step is a valid reduction of arbitrary native reciprocal
geometry to this control, preserving the q-weighted source measure, native row
budgets, returns, actual global killing and one entropy budget. No such reduction
has been established. Heterogeneous native geometry could fill the troughs.

NEXT SCIENTIFIC DECISION: seek either that support-uniform native transport
principle or a concrete admitted heterogeneous counterconstruction exceeding
the phase profile at a nonzero phase. Do not run more depth optimization within
the already solved control class. Do not infer the universal answer from
one-step norms, convex optimization without transport premises, or finite
matrix powers. This is a method boundary, not termination of the mission.

## Ordinary controls and implementation boundary

Ordinary IMH minimax amplitude K remains stronger. On the SAME native critical
families, G at j/n->t0>0 has error O(ell^-4), versus hybrid order ell^-1.
Direct sampling is allowed for analytic disclosed targets. No useful sampler,
target-call or wall-time gain is claimed. Native support is 1+sum M^i; no large
graph is materialized and no fixed-word precision guarantee follows.

The bounded precision note is separate: reciprocal-consistent first-screen
error preserves pi if the second target correction is exact; coherent log
target error of oscillation B changes the target with sharp bias tanh(B/4).
The latter changed-oracle null has an exact two-state law. Do not turn it into
a new numerical campaign without an actual arithmetic algorithm/cost model.

## Preserve evidence and ownership

expansion_native32 is admitted at frozen K=1. coalescence_native5462 fails K=1
and remains algebraic only. Neither is retuned or rerun. The changed-query
evaluator experiment is outside the new source's complete-level query scope.
The B3 pISO correction, failed full halo inference, R3/anMC closure, and
protected/retired programmes retain their statuses. Nothing is reassigned.

The accepted prior operations were genuinely used to establish this checkpoint,
but no causal claim about prompting tactics, agent counts or amplification is
made. Internal correctness, formal verification, historical novelty, external
acceptance and practical usefulness remain separate. Exact delivery identities
and status are in the external receipt. Delivery is not reading or integration.
No numerical jobs remain active; inference/design/discovery totals are unknown.
