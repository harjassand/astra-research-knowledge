# Clean-island service and the remaining asynchronous gate

2 November 2026. Primary: [Cook–Gács–Winfree draft](https://www.cs.bu.edu/faculty/gacs/papers/3Dasync.pdf). Local copies: `3Dasync.pdf`, `3Dasync.txt` (layout extraction). This note deliberately separates a conservative, clean-evolution consequence from a continuing-fault threshold.

## Source coordinates / mathematical interface

- Definitions 2.12–2.13, Proposition 2.7: PDF pp. 10–11.
- Clock lift: equation (3.2), PDF p. 15.
- Slack and repair theorem: PDF pp. 19–20.
- Repair rules: PDF pp. 27, 29–30.
- Milestone explanation paths: PDF pp. 32–34.
- Deadline probabilities: PDF pp. 34–35.

For independent unit-rate Poisson updates, at fixed `(x,t)`:

    P[exists blame path: length <= n, span >= gamma*n] < exp(-delta*n).

The path's spatial vertices are neighbors. For its decreasing times `t_i`, forward means `t_i = next update of u_i after t_(i+1)`; backward means `t_(i+1) = previous update of u_(i+1) before t_i`.

Let `Lambda = v0+[0,L]^3`, `Gamma = v0+B_1(G+6L)`, `G>L`.

    Slack: defects inside Lambda; outside lift s with
    Delta(x,y)=s(y)-s(x), kappa=s mod 3;
    |u-v|_1 <= G+3L  =>  |s(u)-s(v)| <= G.

Source deadline: `t_done-T0 = (27*gamma+1)*L + gamma*G`.

## Independent consequences and limits

### 1. What the Poisson estimate is uniform over

The path event is a property of the update-point processes, not of clock values or quantum data. Consequently its probability does not depend on any deterministic initial configuration. No clock lift and no fault-free tube are needed to *define or bound that event*. The state-dependent argument is a separate implication:

    delayed intended service => existence of a short, long-duration blame path.

That implication requires correct local rules along the explanation and a bound on causal path length. It is exactly what an arbitrary corrupted clock field need not supply.

Uniformity over deterministic initialization does not mean that the same numerical estimate survives conditioning on an arbitrarily selected endpoint state. Such a state may encode the rare past clock history being bounded. For a random start time, use the strong Markov property when it is a stopping time and analyze future clocks, or use an explicit deterministic-deadline union bound. Do not condition backward Poisson paths on a favorable or unfavorable future event without proof.

The source's localized-trajectory language is not a complete boundary-noise interface. A safe application below assumes globally correct updates after the initial island. It therefore avoids inferring an uncontrolled-boundary theorem from the draft.

### 2. Genuine finite-island corollary, not a threshold counterexample

Suppose all clock damage is initially supported in a finite cube, and the exterior clock field is constant. Include one lattice collar so every affected plaquette is inside `Lambda`. Choose `G=2L`. The exterior lift is constant, so Slack holds automatically. Under subsequent globally fault-free intended updates, the source proof gives a clock-repair duration linear in `L`, except with probability exponentially small in `L`.

The star-marked repair region does not expand beyond the initial bounding box. This does **not** say classical data or quantum errors have such a deterministic support bound: data propagation is a separate dynamical question. On a torus the island must fit in an unwrapped region, and the exterior must have zero holonomy; otherwise the simply-connected exterior argument does not apply.

This is a useful eroder component. It is not a perpetual-noise result. In particular, demanding an entirely fault-free repair cylinder of radius `O(L)` and duration `O(L)` costs a probability of order `exp[-Theta(nu*L^4)]` under independent faults of fixed intensity `nu` in three dimensions. Large-island correction under continuing faults needs a sparse-fault/multiscale argument, not repetition of this clean-cylinder condition.

### 3. Stronger clean-evolution tail by rescaling all deadlines

This is our own consequence of the proof's explanation-path bounds, not a claimed theorem statement of the source. Retain the globally fault-free evolution assumption and fixed initial Slack(L,G).

The four post-formation path-length bounds are:

    3L, G+3L, 18L, 3L.

The candidate starting-site bounds used by that proof are respectively:

    2L^3, 400L^2, 2L^3, 2L^3.

Set `M=max(18L,G+3L)` and choose `h` with `floor(h/gamma)>=M`. Put five deterministic deadlines at `T0+j*h`, `j=1,...,5`. If a milestone misses its deadline but its predecessor met the preceding deadline, its explanation has span at least `h` and length at most `M`. Apply the schedule estimate with `n=floor(h/gamma)` and union-bound possible starting sites. The initial formation stage instead has an elementary no-update probability `exp(-h)`. Thus

    P[T_done-T0 > 5h]
      <= 2L^3*exp(-h)
         + (6L^3+400L^2)*exp[-delta*floor(h/gamma)].

Equivalently, for `t >= C(L+G)`,

    P[T_done-T0 > t] <= C'*(L+1)^3*exp(-c*t).

For `G=Theta(L)`, integration yields expected repair duration `O(L)`. Constants depend only on the fixed neighborhood/rates. This does not survive insertion of arbitrary faults into the explanation path. Nor should it be extrapolated to a fixed bounded tube with arbitrary hostile boundary evolution for indefinitely long times.

### 4. Why zero winding still does not imply service

Consider the infinite lattice, with clock field `kappa(x,y,z)=x mod 3`, integer lift `s(x,y,z)=x`, and no stars. Every elementary plaquette has zero circulation; a global lift exists. Nonetheless each site sees its negative-x neighbor one step behind, so the Wait rule disables every site. No defect/star repair rule activates. This is an absorbing computation stall even though Poisson update attempts continue.

This is **not** a finite-fault-start threshold counterexample: it is an inadmissible infinite initial slope outside the flat-exterior basin. Its role is narrower and decisive: a theorem uniform over all lifted clock fields is impossible for this rule. A service proof needs a reachable-state/damage-conditioned slope bound, or a separate memory mechanism that makes outer waiting harmless.

### 5. Physical locality of the rule

The base clock comparisons use the six axis neighbors. The complete repair rule also inspects plaquettes and corner squares. It is therefore not an on-site-plus-six-site contact rule literally. A fixed Moore-radius-one neighborhood suffices for these tests (including surface adjacency), so the interaction range remains constant. Compiling the tests into smaller-arity noisy contacts requires its own finite local controller and fault propagation audit.

For direct transcription rather than a paraphrase, use the source coordinates above: Wait/Emulate on pp. 13–14; Form/Swell on p. 27; Shrivel on p. 29; Synchronize on p. 30. In particular, Emulate permits nonnegative clock difference, not strictly positive difference; the browser's PDF text extraction misrenders the inequality. The actual PDF/layout extraction has the correct symbol.

## Consequence for protected waiting

Protecting data independently of outer transaction progress changes the contract productively: an outer delayed attempt need not count as an accumulating quantum error. It still requires (i) a demonstrably live independent correction service, (ii) bounded-support failure/abort, and (iii) durable ownership/commit information across any destructive teleportation step. A timeout cannot restore an already measured unknown input. Ambiguous commit must become a bounded flagged faulty gadget, not repeated consumption or uncontrolled fanout. The classical eroder above may repair redundant control records, but the quantum causal argument is separate.

## Wang access update

A further ordinary public search found only bibliography/abstract copies, not a new open primary full text. No challenged IEEE/DBLP endpoint was retried, and no ProQuest access barrier was bypassed. Exact Wang timing, fault, and service hypotheses remain unverified.
