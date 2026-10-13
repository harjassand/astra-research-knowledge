# ASTRA continuation checkpoint — 13 October 2026

## Changed target and actual result

Pivoted from increasingly elaborate infinite-chain residual derivatives to a fair-access physical decision test. The new output is stationary throughput J of a finite four-site driven hard-core diamond, NOT the previous macroscopic D. Four interaction coefficients lie within .04 of (4,3,1,2). Pump=.4, physical dephasing=.01. A fresh persistent phase fault is one of {0,2pi/3,4pi/3}. Nine nominal actions combine three phase commands with drain rates{2,4,8}.

One unknown-link exposure of pi/4 followed by a constructed 3-outcome POVM selects an ideal-menu-optimal action with probability>0.99819460749. With phase/drain setting errors<=1/4096 each, good-event regret<3.085217e-6 and worst expected regret<9.418554e-5. Every blind randomized action has worst expected regret>=.016009727377.

Every phase IDENTIFIER using total unknown-link exposure<=pi/4 and link magnitude<=1 has worst failure>=.011031161767, even with arbitrary preparation, ancillas, known controls, feedback, resets and readout. This is not a chosen-contrast lower bound. It is a hard summed exposure cap, not a parallel wall-time or expected-time claim. Common characterization and known computation can be supplied free to the lower-bound competitor. Additional phase-sensitive probes, stronger unknown drive or more exposure void the claim.

## New representation of the decision

Good action sets can overlap without defining model-equivalence classes. A minimal incompatible family of q good sets reduces exactly, in both directions and with the same worst failure, to quantum state exclusion. State exclusion and its SDP are PRIOR ART, not invented here. The concrete loss-to-probe-to-action construction is a new research candidate, without priority clearance.

The physical payoff certificates prove two nonmatching phase commands at drain4 are uniformly optimal. A compiler enumerates four link-connected occupation pairs and finds the only nuisance-null pair|0100>,|0001>. Unknown density interactions vanish on this probe but remain fully present in the stationary output. The physical Lindblad solution gives three rotated qubit states. Loss minimization yields the anti-trine E_a=(I-n_a.sigma)/3. A dual matrix proves optimum among ALL POVMs on this prepared probe. Verified payoff-operator dominance eliminates drain2/8 without presupposing drain4. No generic optimal preparation/experiment search is claimed.

## Mathematics/evidence

Six 70-dimensional all-charge neutral steady-state systems; total-degree6 polynomials in four interaction deviations plus phase/drain actuation;924 polynomial coefficients each. Proposed floating inverses and trials rounded to dyadics. Exact integer/Fraction checking establishes a uniform left-inverse Neumann bound q<1, ALL residual coefficients, phase/root remainders, and shared payoff ordering. No supplied gap or fitted-output error.

462 full16-state Kronecker steady-state tests, six independent generator comparisons,30 reflection checks,36 physical probe checks,120 random POVM checks, exact common-exposure constants and rejected corrupted inverse. Nominal occupation probability above one is~.294; interactions change full throughput materially. These are diagnostics, not laboratory evidence or independent proof review.

Fresh benchmark6.2948s including imports,135588KiB peak memory; exact rebuild/independent checks12.2117s. This is a small finite-state computation, NOT a many-body speedup. Initial model/action/probe-family selection and code development excluded. No prior response coefficients used.

## Physical costs

Known phase-independent readout is not free: one sufficient 4-channel implementation requires known hopping/control scale Gamma4096 and time<=20pi/Gamma; physical readout dephasing then costs<=.000154 TV. Timing rounded down and jitter guarded so actual unknown exposure<=pi/4. Aggregate preparation/freeze/readout/timing law error must be<=.0005. Actual pulses/readout were NOT built.

Optional four-interaction characterization starts with [0,8] priors and uses2621440 quadrature shots,1310720 native time units, mean-bias bound1e-4. It may reject. Accepted-false-box failure<6.498e-5; joint accepting and bad decision probability<.001871. These observations have no phase-sensitive hopping and cannot reveal the fresh fault. No calibration shots were executed; synthetic input tests only. Reference rate/structure validation and device settling time remain outside the result.

## Limits and next target

Strict fixed-budget decision-vs-identification separation, not an asymptotic/exponential sensing advantage. Decision-aware active learners can match it. Exact three-phase promise, finite nine-action menu and rapid calibrated readout are restrictive. Do not assert continuous-flux global optimality, low-rank inversion, infinite transport improvement, low temperature, or civilisation-level consequence.

Next substantive theorem: construct certified good-action/conflict sets and realizable nuisance-null/exclusion experiments for extended interacting devices with continuous uncertainty, without full Hilbert-space enumeration or supplied response representations. The mathematical obstacle is acquiring the loss and experimental structure cheaply; naming a decision class or writing an SDP does not solve it.

## Sources/provenance

Previous complete decision-calibration note read. Astra pinned4ae225b0bf2a07e1ced2952a3e1399d4b45e039c. Targeted openai/math search returned no applicable result. No external proof imported as validated; no repository writes or formal verification. Prior state exclusion2013/2014, Hamiltonian distinguishability2001/2002, decision-specific experimental design, semiparametric estimation and certified steady states are explicitly credited in research_note.md.
