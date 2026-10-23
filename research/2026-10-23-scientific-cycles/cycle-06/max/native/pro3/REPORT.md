# Critical sampling robustness closed in the interior regime

Astra PRO3, 22 October 2026 Australia/Brisbane.

## Decision

Accept the full critical-window theorem for the exact native finite family
when alpha exp(-K)<1-alpha. The previous amplitude lower is sharp:

    eta_n log n = loglog n/c_* + s + o(1)
    => (log n) R_eta_n(n) -> max(K,(1-exp(-K))*exp(-c_*s)),
    F(c_*)=alpha exp(-K)/(1-alpha),
    F(c)=c(1-c)^((1-c)/c).

This proves existence and identifies the class supremum; it is not a fit to
finite matrices. The theorem rules out a heterogeneous native transport
geometry with a larger critical amplitude in this regime. It preserves all
accepted first-order and fixed-screen results.

## What changed scientifically

The old strict-c certificate controlled the sum of separate first-hit Lp
norms. That sum lost its bound at the endpoint. The new argument absorbs all
bad first hits into one boundary vector, keeps the actual killed global mass
and local rejection diagonal, and allows its energy to grow slightly for only
O(loglog n) steps. The total growth is 1+o(1). A single union of bounded-test
bad sets covers every relevant first-hit time; afterwards the actual original
kernel propagates every hit, retaining all return paths.

The information allocation matters as much as transport. For b=q(W<h),
k=-log(1-b), and a=pi(W>R), the new finite joint inequality bounds
k+a log R by K plus an explicit vanishing remainder. If k has a fixed gap
below K, global escape is stronger and critical transport disappears. If k
tends to K, the ordinary high-weight tail has no leading entropy budget left.
This yields a maximum rather than an unjustified sum of two full-budget
obstructions. It is a reusable information/transport principle in this class.

## Concrete comparison

At K=1,alpha=1/2, c_*=0.64841952744070018... . The critical crossover is
s=log(1-exp(-1))/c_*=-0.7073740471658282... . At offsets s=-2,-1,0,1, the
hybrid's limiting amplitudes are approximately 2.31211781948,
1.20894053126,1,1. Ordinary pure IMH has amplitude one throughout. The new
result is useful robustness/complexity theory and supplies no practical
sampler advantage. COMPARATOR.md gives the matched ordinary proof and cost
boundary; EXPERIMENT_CONTRACT.md keeps native queries, caches and precision
distinct from verifier inputs.

## Evidence and limits

The complete principal proof is CRITICAL_ENDPOINT_THEOREM.md. It received
two distinct source-bound challenges without repair: the absorbed energy
inequality and the first-hit/full-return/uniform-supremum interface. The
principal separately accepted the independent joint-budget contribution.
A complementary scoped potential theorem excludes loop/retry improvements
in the old one-core family; the principal upper then covers the full class.

The frozen six-state Fraction diagnostic checked 16 exact positive-definiteness
energy certificates, 64 absorption identities and two full-return decompositions.
It passed on its first execution in about 0.128 seconds of measured body wall
time, with peak RSS 11,776 KiB. These are exact finite algebra checks, not proof
of the asymptotic law, a graph simulation or a discovery-cost measure. Complete
inputs, outputs, code and resource receipts are included. Total active inference,
tokens, money and historical research costs remain unknown.

Hypotheses remain finite positive pi,q, one certified population forward-KL
budget, proposal initialization, fixed symmetric target-independent Q, fixed
alpha and eta within each trajectory, and the lazy random mixture with its
actual diagonal. The theorem does not cover adaptive or nonreversible kernels,
deterministic schedules, empirical KL certification or numerical implementation
error. Historical novelty, formal verification and external acceptance remain
unestablished. Primary literature and the precise nearest comparison are in
SOURCES.md; no general technique-superiority claim follows.

## Continuation

The next selected question is the critical amplitude at the global-dominant
boundary r0>=1, where the many-level optimal transport geometry degenerates.
The continuation seed records an unproved one-crossing candidate and the exact
weighted-absorption and single-budget obligations needed to test it. The interior
critical problem is closed; no old search, new empirical campaign or hypothetical
application has been substituted for this result.

The original Cycle4 ZIP is unchanged and complete. Protected programmes and
retired scientific operations remain with their owners or closed as recorded.
Max owns integration. Private delivery is a separate recorded event, not an
assertion of reading, scientific acceptance by Max, or repository integration.
