# Focused source-bound review: critical-window amplitude lower

Reviewer: `/root/reachable_obstruction_challenge`.
Scientific date: 22 October 2026 Australia/Brisbane.

**Accepted within the stated native finite-positive class, with r_0<1.**
I read the complete separate `CRITICAL_WINDOW_LOWER.md` source and checked
its dependence on the unchanged main theorem's algebraic finite event bound.
The source matches the mathematical refinement previously challenged; no
additional correction or broader audit was required.

## Exact source and scope

Reviewed source: `CRITICAL_WINDOW_LOWER.md`.
Bytes: 6991.
SHA256: `1f0e0a6da68b6447455c870d49e6d544a75d30cc6a1ee1dba8e6c4746c55d7f0`.
Review completed: 2026-10-21T20:29:28.276169+00:00.

This verdict accepts the lower bound

    liminf (log n) R_eta_n(n) >= max(K, (1-exp(-K))*exp(-c_* s))

for eta_n log n=(loglog n)/c_*+s+o(1), fixed real s, and
r_0=alpha exp(-K)/(1-alpha)<1. It does not identify the exact critical
prefactor, establish its limit, or extend this refinement to r_0>=1.
The two lower families justify a maximum, with no addition of their KL budgets.

## Load-bearing checks

The varying degree is controlled rather than substituted into a fixed-degree
asymptotic. Here u is of order log L, m is of order u, D is of order u²,
and the nonroot proposal mass is O(exp(-a L/u)), hence o(u^-r) for every
fixed r. Thus q_star=exp(-K)+u^-2-o(u^-2). Its logarithmic slack is
exp(K)u^-2+o(u^-2), which dominates the positive leaf KL term O(L^-3).
All probabilities are positive and the admitted KL budget is strict eventually.
The forward and reverse local branches remain correct because D/n² tends to
zero; the reverse acceptance retains the necessary factor D.

The accumulation of the screening error is
O(u log L/L+u² log u/L)=o(1), not merely an uncontrolled per-edge o(1).
The competition parameter differs from r_0 by O(u^-2), and multiplication
by m=O(u) gives O(u^-1). The local forward mass tends to a positive constant;
the additional competing-exit probabilities are uniformly O(n^-2), so their
accumulated logarithmic contribution also tends to zero. All this permits
reuse of the exact finite marked-event inequality from the unchanged main
source, without claiming a uniform fixed-degree asymptotic theorem.

At the finite optimum v_*, H_u(x)=x log(1+r_0 exp(u/x)) has derivative zero
at x=u/v_* and second derivative O(1/u) within bounded distance of that
point. Nearest-integer rounding therefore costs O(1/u), proving that the
logarithmic capture error tends to zero rather than leaving an unspecified
constant amplitude. This step requires r_0<1, exactly as the source states.

The actual global escape lower stays bounded away from zero, so the
waiting correction is relative 1+o(1). Leaf-union escape still has
n e_m=O(L^-2+n^-1), giving the same relative retention. The target leaf
mass p=L^-4 is negligible compared with L^-1. The resulting marked mass
is b_K exp(-c_*u)(1+o(1)), which proves the new amplitude lower after
multiplication by L. The ordinary independent Q=I family supplies K.

## Status and costs

This was a bounded analytic review of the three unresolved interfaces:
growing-degree admission, accumulated errors, and optimal rounding. I read
the full separate source to bind the verdict. There was no additional
scientific code, numerical calculation, matrix replay or search. Metadata
hashing and writing this receipt are source handling, not scientific tests.
Model inference time, tokens, monetary cost and complete discovery cost are
unknown. The earlier tree review and its receipts remain unchanged.

No formal-proof-assistant, historical-originality, external-acceptance or
practical-sampling-speed claim is supplied. The critical prefactor remains
a live question; this lower is substantive progress within it.
