# Local unit-rate rules can hide long transients and hard prediction

This independent [complete companion note](package/companions/local_rules_prediction_obstacle.txt) constructs an elementary spectral obstruction and a scoped complexity reduction. It was retained as a design constraint, rather than selected as the main [quantum acquisition result](README.md). Strong prior results exist; no new foundational theorem, unconditional runtime lower bound or fault-tolerant physical capability is claimed.

## Exact stochastic path and local compiler

Take distinct deterministic computation configurations `c_0,...,c_L`, with a halting final configuration, and put independent rate-one exponential holding times on successive steps. On this reachable component, `Q(j,j+1)=1`, `Q(j,j)=-1` for `j<L`, with absorbing `Q(L,L)=0`. Its characteristic polynomial is `z(z+1)^L`: every nonzero eigenvalue is `-1`, yet mean absorption time is `L` and variance is `L`.

At time `t`, the state is `c_min(N_t,L)` for `N_t` Poisson with mean `t`; its distance from the stationary point mass is `Pr(N_t<L)`. At `t=L/2`, that distance is at least `1-exp[-(log(2)-1/2)L]`. The killed generator's large Jordan block produces a long transient despite the unit real-part eigenvalue gap. Eigenvalue lists alone therefore do not control this nonreversible relaxation.

A fixed deterministic one-tape machine uses a finite alphabet, one head-state symbol and end markers on `O(s)` cells. Each transition is a one- or nearest-neighbour two-cell rewrite with rate one. Exactly one rewrite is enabled on each valid nonhalting configuration. A polynomial-space decider cannot repeat a configuration on its halting run; its prepared reachable component is exactly the path above, potentially of exponential length. No assertion is made about invalid strings or unique stationarity over every representable configuration.

## Scoped prediction hardness

Compile a fixed polynomial-space TQBF decider and final output-write routine. A configuration-count bound `U` has polynomially many bits. At binary-encoded time `t=8U`, accepting inputs have output-one probability above `0.95`, while rejecting inputs have probability zero. An additive-`1/4` polynomial-time predictor for this promised class would decide TQBF: a deterministic predictor implies `P=PSPACE`, and a randomized bounded-error predictor implies `BPP=PSPACE`.

The restricted accept/reject promise is itself in PSPACE by following the deterministic polynomial-space decider to halt. Its stated PSPACE-completeness does not assert PSPACE membership for all arbitrary stochastic local generators. Hardness is conditional in the usual complexity sense, not an unconditional superpolynomial prediction-time theorem. The observation time and ordinary physical execution remain exponential in the input size.

## Costs and error boundary

The local transition table is exactly supplied, not inferred. Ideal calibrated rate-one clocks with a constant positive lower bound preserve a robust late-time accept/reject gap; per-rule rate calibration needs the stated prepared contexts and completed jumps. It does not certify absent rules. Wrong-symbol transitions of total per-step hazard `delta` can accumulate error of order `L delta`; a finite local calibration cannot establish exact zero, and no fault-tolerant compiler is supplied. An irreversible driven implementation also pays fuel/reset per update. A bounded-energy thermal-equilibrium realization was not established.

Ordinary execution costs `Theta(L)` mean serial clock time and local updates. An irreducible reversible chain with known full-support stationary law instead has `TV(P_t(x,.),pi)<=0.5 pi(x)^(-1/2)exp(-gamma t)`. Polynomial inverse gap and polynomial log inverse starting mass then bound relaxation; the absorbing nonnormal path lacks those premises. A biased reversible path can hide the long time in an exponentially unlikely initial state, whose energy/mass cost cannot be granted free.

Succinct-chain convergence hardness, nonreversible singular-value/contraction analysis and reliable computation under persistent noise have strong established machinery, cited in the [full note](package/companions/local_rules_prediction_obstacle.txt). The [selection record](package/SELECTION_RECORD.txt) preserves why this idealized obstruction was not promoted to a new physical advantage. No source program, proof-assistant check, fault-tolerance experiment or new Capital audit was run. [Original package and provenance](SOURCES.json).
