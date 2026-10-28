# Charged acquisition, ordinary comparators and unresolved physical inputs

## What the supplied-model compiler actually consumes

The six-state rates, observation map and rate-response formula are explicit
rational mathematical inputs. They are constructed in this folder; no
model learning, physical rate calibration or experiment is counted as done.
The response-control interface is stated exactly in PROOF.md. The result
is an experiment-design separation and a certified predicted probability,
not an implemented instrument or a new stochastic-thermodynamics method.

Ordinary methods receive the same full model and every proposed protocol:

| Comparator/interface | Result at its actual scope |
|---|---|
| full passive baseline law of reversible six-state S | exactly matches all source words at arbitrary observation times |
| complete linear FDT/response spectroscopy | satisfies every accessible channel relation at every static field; baseline response curves match S |
| full static laws at all fields and any isolated constant-level pulse | exactly matched by the twelve-state parity comparator, with stated canonical preparation |
| ordinary Crooks work/path reciprocity on the two-pulse protocol | succeeds with the identical certificate; no algorithmic advantage over it |
| controlled-HMM/PSR model learning | established broader machinery; no unknown-model learner or its acquisition costs were implemented here |

The twelve-state comparator is reducible. Its half/half sector law is a
supplied canonical preparation, not something waiting can acquire. Its
alternative stationary + sector reproduces all source protocols exactly.
The positive-flip construction gives arbitrarily long finite shadows when
no hidden mixing contract is available. Thus visible stationarity alone
is insufficient to give the active receiver its physical interpretation.

## Finite preparation for the two explicit irreducible six-state models

For the strict instance, Q=S+K with K skew in the uniform inner product.
All nonzero symmetric graph edges have rate at least m=1/100; only the
marker-marker edge is absent. The missing squared difference is at most
twice a two-edge route, so the complete-graph sum of squared differences
is at most three times the existing-edge sum. For a mean-zero f,

    -<f,Sf>_pi >= 2m ||f||_pi^2 = (1/50)||f||_pi^2.

The skew part does not change the L2 derivative. For an arbitrary hidden
initial law, both Q and S therefore satisfy

    ||mu exp(TQ)-pi||_TV <= (sqrt(5)/2)exp(-T/50).

T=1250 gives a bound less than 3/(2*10^10). The exact partial sum of exp(5)
through degree 6 exceeds 100, so exp(25)>10^10; sqrt(5)/2<3/2 suffices.
This is less than delta/16 for delta=7/10^8, a certified signal floor.
Waiting this long replaces arbitrary hidden point preparation for these
supplied models. It does not acquire a device-independent mixing bound,
and does not prepare the reducible twelve-state comparator's sector law.

## A fully charged conservative statistical design

Conditional on a valid preparation-error bound epsilon<delta/16 for the
actual model and the equilibrium null, use each forward/reverse protocol
N times. Record the event indicator, including zero for every failed event.
The protocol lasts 3/2 model time units and reads six labels. No successful
event is treated as a free trial.

Take

    N=ceil(160/delta^2)=32653061224489796 cycles per arm.

Hoeffding with per-arm deviation delta/8 gives total failure probability
at most 4 exp(-N delta^2/32)<=4 exp(-5)<0.04. Preparation can shift each
mean by at most epsilon. Under the null the difference is then less than
3delta/8 in magnitude, while the target's negative difference exceeds
5delta/8 in magnitude. A threshold -delta/2 separates them. Independent
repetitions suffice; a uniform conditional preparation bound also permits
the same martingale-Hoeffding argument on sequential cycles.

For the two explicit irreducible models, burn-in 1250 before each cycle
costs at most N*(2503) approximately 8.17e19 model time units across both
arms, plus readout/control. The scale of a physical time unit is unacquired.
This is a very conservative **sufficient upper budget**, not a lower bound
or an optimized experiment. A different receiver, full-record likelihood,
better control design, or sharper preparation estimate might cost less;
no advantage for those unimplemented methods is inferred. The present
design does not establish practical measurement value.

The wider parity null has no supplied uniform mixing bound. Thus that
preparation qualification is a missing physical input, not silently
included in this numerical budget. The exact model comparison remains
valid independently of any experiment.

## Every exploratory and verification execution is charged

Python 3.12.14 on the available macOS arm64 host; only local CPU was used.
No paid compute, GPU, samples, detector, device, physical action or public
write was acquired. Timers below have their stated execution scope; source
reading, web retrieval, design, shell startup and report writing were not
metered and are not claimed free.

| Run | Retained output | measured seconds |
|---|---|---:|
| three static fields: pairs through lag 20, words through length 8; no reversal defect | EXPLORATION.json | 8.00245212 |
| 2907 one-pulse zero-work-word candidates; none separates | PROTOCOL_EXPLORATION.json | 2.31034533 |
| two-pulse search, six candidates across three fields | TWO_PULSE_EXPLORATION.json | 0.00246438 |
| first symbolic run; wrong guessed b^3*a coefficient assertion rejected | tool execution, exact returned expression -256*b^5*gamma*tau^6*(d-1)^3 | 1.49607417 wall |
| corrected universal symbolic identity and static metric | SYMBOLIC_FAMILY.json | 1.70748350 |
| four continuous-time floating proposals, all retained | CONTINUOUS_PROPOSAL.json | 0.11267783 |
| six exact degree-48 normalized-uniformization kernels and receiver | CONTINUOUS_CERTIFICATE.json | 0.11389125 |
| independent degree-80 signed-Taylor replay and parity comparator | INDEPENDENT_TAYLOR_REPLAY.json | 0.25477538 |
| exact four-state holding-time countercontrol | CALIBRATION_COUNTERCONTROL.json | 0.00012529 |

Module timings and one failed-run wall timing are not a homogeneous
hardware benchmark. No aggregate speedup is claimed. The first discarded
symbolic guess was corrected to the computed b^5 formula; its failure and
cost are retained. No numerical fit, local Hessian grid or Monte Carlo
result is a proof premise. Peak memory and whole-session CPU were not
measured.

## Completion boundary

ACQUIRED: continuous-family passive/static/one-pulse obstruction; exact
two-pulse polynomial signal; actual fixed-time CTMC interval; independent
same-worker arithmetic replay; waiting-time and unresolved-sector
countercontrols; an explicit full input/cost contract.

NOT_ACQUIRED: a new generic response theorem, novelty priority, unknown-
model identification, physical energetic/parity/preparation calibration,
experimental diagnosis, practical advantage, entropy-production rate,
or a high-impact new physical capability. The useful result is a sharp
measurement-interface distinction and the exact qualifications without
which the broader inference fails.
