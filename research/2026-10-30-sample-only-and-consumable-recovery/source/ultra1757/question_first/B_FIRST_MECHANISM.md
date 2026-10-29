# Question first: can finite useful distinctions be compiled into one decoder?

Initial mechanism formed before importing an Astra operation; not a final
priority or capability claim. B/C pair,30October2026.

The broad bottleneck is that a universal entropy inverse can disappear
under arbitrarily small full-rank noise while a finite prediction task
remains easy. Replacing exact supports by an arbitrary likelihood cutoff
does not solve this: two input priors may give one label probabilities
e and2e while keeping their likelihood ratio bounded. A faithful output
then has divergence O(e^2), whereas the input divergence is O(e).

The concrete question is instead whether individually testable finite
distinctions can be compiled into ONE decoder that works for every label
and every adjoining reference, at paid implementation cost. This asks for
a decision/simulation operation, not another entropy coefficient.

## First mechanism

For supplied normalized states tau_i, let S=sum_i tau_i on its support and
consider the ordinary square-root/pretty-good measurement

`M_i=S^-1/2 tau_i S^-1/2`.

For ANY individually chosen effect0<=E_i<=I, put

`a_i=Tr tau_i E_i`, `b_i=Tr(S-tau_i)E_i`.

Then its per-label success obeys

`Tr tau_i M_i >= a_i^2/(a_i+b_i)`.                    (1)

Proof: HS Cauchy on `B=S^1/4 E_i S^1/4` and
`C=S^-1/4 tau_i S^-1/4` gives
`a_i^2<=(Tr B^2)(Tr C^2)`. Since0<=E_i<=I,
`Tr B^2=Tr E_i S^1/2 E_i S^1/2<=Tr S E_i=a_i+b_i`.
Finally `Tr C^2=Tr tau_i M_i`.

Exact private-support tests recover success_i>=r_i. More usefully, (1)
still works for approximate/private tests and full-rank noise; it never
asks whether a numerically tiny eigenvalue is exactly zero. A uniform
success1-delta for this classical-label decoder gives trace-distance
simulation error at most2delta on every cq input and every quantum
reference. Adaptive composition would then use the usual hybrid bound,
not an entropy-to-channel-simulation assertion.

For example, on a d=n independent pure family, the original rank-one
private projectors under uniform depolarization of size eta have
`a_i=(1-eta)r_i+eta/n`, `b_i=(n-1)eta/n`.
Their entropy inverse may become infinite, while (1) still gives a finite
state-independent approximate decoder error. This is an analytic family
calculation, not a new numerical source or physical experiment.

## The first serious obstacle and the strongest ordinary competitor

This argument alone is not a new operation: the decoder is PGM/Petz,
standard quantum union bounds provide sequential test alternatives, and
ordinary statistical-experiment deficiency already formalizes additive
risk/simulation. Full state matrices or a block-encoding of S cannot be
supplied free for a many-body scientific system. A test-only implementation
or a paid acquisition that avoids an exponentially ill-conditioned
inverse would be the actual missing operation.

The initial primary screen found Montanaro's2019 *Pretty simple bounds on
quantum state discrimination* (arXiv:1908.08312), Gilyen et al.'s2022
*Quantum Algorithm for Petz Recovery Channels and Pretty Good Measurements*
(arXiv:2006.16924), and Wilde's2013 sequential-decoding construction
(arXiv:1303.0808). These are strong prospective incumbents, currently
being read. No novelty, advantage or paid test-only compiler is claimed.
If they already supply the entire mechanism with the same input contract,
this branch should be retired rather than dressed up as a new principle.
