# Independent factory comparison: accepted model operation, no established separation

The finite scalar shift compiler is correct for the supplied optical model at
the reviewed scope. An independently implemented ordinary absorbing chain
reproduces every exact four-source probability and joint source/time first
moment at lambda=999/1000, 99999/100000 and 1. It also matches a finite PGF query.
The finite closure follows independently from the pure-death spectrum, and an
explicit ordinary phase-type tensor block reproduces the spectral contraction.

This resolves the bounded challenge positively as a target-specific validated
adaptation. It establishes no acquisition advantage over an equally informed
structured phase-type/transform solver, which can perform the identical
reduction. It establishes no useful distilled quantum resource or physical
capability.

## Actual exact comparison

The model is raw p=(99/500,4/5,1/500), common-mode photons, D=19/20, one clock
per raw or fusion action, sequential child preparation, independent pure-death
storage, and whole-current-node restart on click. These are supplied inputs.
The ordinary chain applies loss on the inputs before the beamsplitter and
counts every primitive in every failed attempt. No time or retry cutoff is used.

| Nominal sources n | Per-clock survival | Transient states | E[N] | E[source uses] | E[fusions] | E[clocks] | Cov(N,T) |
|---|---|---:|---:|---:|---:|---:|---:|
| 2 | 999/1000 | 13 | 1.51743111129833 | 3.78760628253744 | 1.89380314126872 | 5.68140942380616 | exactly 0 |
| 4 | 999/1000 | 103 | 2.91581780939493 | 19.3356956644045 | 12.2203432900262 | 31.5560389544306 | -0.0270528205724631 |
| 4 | 99999/100000 | 103 | 2.93671878708167 | 19.3843774520032 | 12.2498006715033 | 31.6341781235064 | -0.000274339358849398 |
| 4 | 1 | 103 | 2.93693068383301 | 19.3848695629794 | 12.2500984483352 | 31.6349680113145 | exactly 0 |

Displayed numbers are rounded from retained exact rational results. In every
case E[clocks]=E[source uses]+E[fusions] holds exactly. At each n4 fixture the
comparison comprises all nine output probabilities, nine joint source first
moments, nine joint time first moments and nine PGF components at z=lambda^2.
At lambda=1 that last query coincides with z=1. The n2 case has five components
of each type. Source cost is per eventual successful output, not per accepted
fusion attempt or nominal leaf.

The nonzero n4 covariance is a discriminating positive result: replacing the
state/time law by independent marginals would lose information actually used
by this factory. It is not legitimate to compute waiting loss from E[T] alone.

## Independent structural and enclosure checks

* Exact fusion check: 225 input-side-loss versus collapsed-kernel components
  at each of the three survivals, covering every input count 0,...,4.
* Exact memory-spectrum check: 81 falling-factorial identities on support
  0,...,8 at each survival.
* Explicit 65-state ordinary phase-type waiting block: 125 joint child-output
  and retained-count components at each of z=1 and z=lambda^2 agree exactly
  with the spectral contraction. No producer imports occur in that test.
* Directed dyadic n4 check at 256 bits: all 36 components enclose the independent
  exact-chain results. Maximum output-probability width is 2.102e-74. This
  reviews the small arithmetic interface, not the larger n16/n32 receipts.

The general proof shows the cumulative shift e<=2n-2 for a root query z=1.
An external root exponent e0 changes that to e<=e0+2n-2. The proof has no
hidden completion-time or photon-age truncation.

## Ordinary comparator and claim boundary

The literal chain is already an exact ordinary solution. Its size satisfies
M_n=(n+2)M_(n/2)+(n+1)^2, giving M32=690847. A factored solver diagonalizes the
pure-death block in falling factorials and obtains the very same arguments
H_m(j,z lambda^s). Thus comparison against the unreduced chain alone does not
establish a separation. Details and prior-source distinctions are in
[COMPARATOR_AND_COSTS.md](COMPARATOR_AND_COSTS.md).

Exact joint state/time transforms, memory-generator shifts and failure
resummation are established in
[Kuzmin and Vasilyev, Sec. III.2](https://arxiv.org/html/2009.10415v1).
Their particular linear-size higher-level implementation replaces exact
incoming completion laws by Poisson processes. This factory retains the exact
nested laws. That is a distinction between the stated implementations, not
a limitation of the prior transform method or a proof of historical priority.

Accepted: the supplied-model closure derivation, exact bounded output/cost
comparison, local kernel checks, phase-type equivalence and bounded directed
enclosure. Not reviewed here: producer n8 exact acquisition or larger dyadic
runs. Not established: a computational advantage over tailored structured
comparators, device inputs, optimal scheduling, robustness to general
multimode/coherent/non-Markov sources, or a useful quantum computing resource.

## Artifacts

* [PROOF.md](PROOF.md): independent Markov/phase-type derivation and closure.
* [code/](code/): independent model, rational solver and bounded controls;
  comparison/enclosure adapters are explicitly separate.
* [results/](results/): exact chain matrices, output/cost fractions, logs,
  componentwise comparisons and interval endpoints.
* [REPLAY.md](REPLAY.md): commands and provenance.
* [MANIFEST.json](MANIFEST.json): file hashes and exact reviewed producer versions.
