# Completed restricted operation; native quantum gate still open

The construction gives a retained CLASSICAL bit and an always-running
buffered copy into an arbitrary noisy destination. Both use one noisy bit
per site and fixed local Poisson channels, with no persistent clock or
history tape. The proof controls failure at ANY time in the interval and
admits future-dependent supported fault labels. It does not replace the
desired quantum syndrome decoder by an ideal classical register.

The load-bearing step is monotonicity: for each retained value, setting
every fault-touched bit to the WRONG value is a single pathwise worst
trajectory. That trajectory is Markov, so the subsequent drift/exponential
proof has a legitimate filtration. A direct Markov argument for the
original future-dependent fault labels would be invalid.

For n bits on the admitted graph and q-bit fault supports, the sufficient
conditions are initial errors<=n/256, per-bit Poisson fault incidence
lambda<=1/[1024(2^q-1)], and clock rates in[15/16,17/16]. The all-time
register failure upper is

    2^q n(1+lambda) T exp(-n/256).

The copy has an explicit initialization-forgetting term and exponential
excursion term in PROOF(8). A read-q bound supplies simultaneous all-time
failure bounds for many separate register/copy pairs, including fault
streams shared by up to q pairs. Arbitrary inter-pair feedback is excluded.

## Actually constructed

The exact n=65536, q=1 output uses the standard explicit eight-incidence
Margulis graph, three length16 walks per attempt, 144 fair bits and at most
four accessed data bits per update. Restoring/copy graph ranges are16/17.
The full524288-incidence graph catalogue (2097152bytes) was emitted and
checked. Its eight directional permutations and every inverse identity
passed. The named all-moduli spectral theorem is an ordinary imported
premise, not a numerically fitted eigenvalue.

At lambda=1/1024, with up to256 source errors, T=2^128 and copy latency256,
REGISTER_CONTRACT.json gives a total buffered-copy failure upper

    3.855621470697103e-34   (decimal diagnostic of an EXACT rational bound).

This is a compiled theorem receiver, not an executed long-time memory
experiment. No trajectory or new quantum-code fixture was generated.
The final graph/contract compilation took0.242976s and28.74MB peak RSS;
the earlier exact-rate-only compilation took0.232868s. Both runs are
charged, and the first receipt is retained. An independent finite scalar
and transport consumer passed in0.003117s without importing producer code.
Those execution times do not price the scientific derivation, literature
review, physical acquisition, or the exponentially long storage operation.

The storage WORK is not constant: the source/copy attempt rate is at most
139264 and the expected attempt count over the stated horizon is at most
47389083546877574175763401329377768200208384. Its nominal random-bit
budget is also explicitly returned. No negligible physical power claim
is attached to an ideal CPTP channel specification.

## Decision and next actual gate

Cruise--Ganesh already supplies Poisson three-poll majority and explicitly
discusses expander random-walk sampling. Majority-based noisy consensus,
expander mixing and branching-process exit bounds are ordinary. This is
therefore a paid strong-quantifier instantiation, not a new generic
classical-computation architecture or demonstrated advantage.

Its graph access is also a real change: it is not the programme's
bounded-density three-dimensional geometry. The proved Omega(L^2) mixing
cost for a reversible bounded-range grid walk prevents hiding that
communication inside a rate-one atomic update. The terminal global
mathematical majority, sparse initial source qualification, nominal finite
coin source and atomic graph-range read are stated inputs, not acquired
noisy hardware operations.

The survival question is consequently sharper. A geometrically local
controller must supply a pathwise restoring rule for CHANGING quantum
syndrome streams, together with its own noisy state and real correction
latencies. It cannot borrow this static register guarantee or a
synchronous/causal-only theorem without paying that composition. The
central autonomous charged-error quantum-memory threshold remains
NOT_ACQUIRED. Historical priority of the exact restricted bound is
UNKNOWN; no absence-based novelty claim is made.

Governing proof: PROOF.md. Literal channel: controller.py. Acquisition:
compile_contract.py, REGISTER_CONTRACT.json, GRAPH_CATALOGUE.u32le.
Independent finite receiver: replay_contract.py, REPLAY.json. Source
scope and strongest conventional alternatives: PRIOR_AND_GATE.md.
