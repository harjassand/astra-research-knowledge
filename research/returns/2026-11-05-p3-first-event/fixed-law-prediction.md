# Exact prediction constrained by one fixed Lipschitz law

The independent [complete proof](package/next4_theory/FIXED_LAW_CERTIFICATION.md) constructs finite-data prediction and safety certificates for a deterministic, fully observed, time-homogeneous Euclidean law with a **trusted global Lipschitz bound**. It retains every pairwise consistency condition across observations and future steps. A sequence of separately permitted future transitions need not arise from one fixed law.

Finite Lipschitz interpolation gives a Gram SDP description. The relaxation always upper-bounds the target and is exact when its optimizing Gram matrix embeds in the **physical dimension**; a sufficient automatic condition is dimension at least known-vector span rank plus the number of unknown vector values. Otherwise the rank constraint is substantive and may leave a nonconvex problem. A rank-valid primal witness realizes an actual compatible law/trajectory; a checked dual supplies an upper certificate.

## A sharp envelope and dimension separation

From the sole observation `f(0)=-e`, `||e||=1`, the exact maximum of `<e,f(f(-e))>` in dimension at least two is

```text
-1+L(1+L)/(1+2L),  0<=L<=1/2;
L^2-7/8,           L>=1/2.
```

Exact upper identities and attaining maps are supplied. At L=1 this value is **1/8**, while the scalar fixed-law value is **-1/3** and the specified stepwise outer relaxation permits **1**. Low-dimensional rank is therefore a real physical distinction, not a removable numerical preference. The scalar transition point and complete dimension diagram are in the proof.

For exact data and `L<1`, possible equilibria are exactly an intersection of explicit observation-derived balls. A geometric contraction tail converts finite-horizon analysis into all-time certificates for safety questions with a positive margin. Equality thresholds and degenerate conic cases need separate care; dual infima need not be attained even when primal optima exist. No unqualified finite-time decision claim is made at a zero margin.

## Acquisition and computation are paid

The model excludes hidden state, stochastic innovations, time-varying law and an unproved global regularity prior. Metric/physical units are part of the Lipschitz assumption. A finite observed trajectory does not establish that prior or model completeness. SDP dimension and pairwise inequalities grow with horizon/records; low-rank feasibility, arithmetic precision, conditioning, degeneracy and the desired certification margin remain costs. Quantifier elimination is a computability statement, not practical polynomial runtime.

[Numerical verification](package/next4_theory/verification_results.json) and [candidate solver code](package/next4_theory/certify_fixed_law.py) are retained. A floating objective/status/residual is not a proof-level dual or PSD certificate. The explicit sharp identities avoid that issue for the displayed example. Established Kirszbraun interpolation and semidefinite performance-estimation machinery are credited rather than renamed a new optimization principle. Particular historical novelty and practical benchmark superiority are unestablished.

This is an independent conditional mathematical construction, not an empirical new dynamical law or an uncertainty extension of the first-event theorem. No code or solver was run by Capital. [Original package and provenance](SOURCES.json).
