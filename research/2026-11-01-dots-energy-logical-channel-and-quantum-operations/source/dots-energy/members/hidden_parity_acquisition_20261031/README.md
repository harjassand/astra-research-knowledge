# Retained parity-family acquisition: valid extension, failed new advantage

## Finding

A single generic planar trivalent tensor network determines its compatible
parity-axis lines. Retaining those lines gives an exact, locally checkable
family of later inputs, **including singular local tensors**. The implementation
acquires the chart from raw coefficients; it never receives the generator's
hidden gauges. A standard matchgate/Pfaffian bridge then evaluates all admitted
weights, zeros and cancellations included.

This is a **source-derived reuse extension of existing Astra N1077**, not a new
tractability class. The attempted four-task subspace-learning advantage failed:
the stronger one-instance method gets the same family faster. The tested
Pfaffian execution also loses badly to retained ordinary elimination.

## Ordinary proof and execution

* `PROOF.md`: linear-preserver acquisition theorem; generic single-member
  rigidity; all-weights gadget/sign construction; exact costs and limitations.
* `acquire.py`: learns local parity spaces from four independent observations.
* `strong_retained_comparison.py`: the stronger one-instance, retained-chart
  adapter derived from N1077's CP/quadratic equations.
* `all_weights_pfaffian.py`: exact rational execution, including singular queries.
* `retained_elimination.py`: equally informed ordinary retained-plan comparator.
* `test_construction.py`: exact adversarial and structural tests.
* `retained_single_instance_chart.json`: an actually persisted chart. Loading
  rechecks the graph, invertibility and every edge-duality identity; each new
  query still undergoes the full parity-membership check.
* `*_results.json`: first-run measured records; no benchmark result is hidden.

Run from this directory (Python 3 and the existing SymPy installation):

```
python -m unittest -v test_construction
python acquire.py
python strong_retained_comparison.py
python all_weights_pfaffian.py
python retained_elimination.py
```

Re-running the four executable reports replaces their timing JSON files.

## What the stronger comparisons established

Five separate generated hidden-gauge fixtures gave **identical accepted
four-dimensional local subspaces** for the two acquisition routes:

* Four-task linear-preserver method: approximately 0.200--0.244 s.
* One-generic-member retained adapter: approximately 0.047--0.051 s, including
  one rejected generic trial in one fixture.
* Exact retained query membership: approximately 0.8--0.9 ms on eight vertices.

The all-weights executor matched 12 original-edge exhaustive partition sums,
including zero hyperdeterminants, pivot flips and zero results. The further
unit tests cover signed values, all city signatures in 27 coefficient settings,
parallel edges, disconnected graphs, insufficient rank and rejected off-family
queries. These are implementation checks, not historical novelty evidence.

On eight new original-input cube queries, retained ordinary elimination took
0.72--1.02 ms, while chart verification plus the dense rational Pfaffian took
24.8--29.3 ms. Its plan setup cost was about 0.000293 s, versus approximately
0.0841 s for chart acquisition in that independent comparison run. The plan
retains 622 projection indices and has maximum bag size six.

The cube is a low-width, generated fixture. It is not a convincing large-width
application. On growing-width planar graphs the familiar Pfaffian-versus-generic
elimination asymptotics may matter, but an equally informed retained holographic
method already has that advantage. No useful nongenerated workload, new strong-
baseline speedup, all-in payback, or civilisation-level consequence is claimed.

## Scope that genuinely changed

N1077's fresh generic-input frontend requires nonzero hyperdeterminants and
nonzero CP pairings. The retained rational-chart adapter can accept later
arbitrary members of the acquired parity spaces even when those conditions
fail. Every later membership check and every final exact computation is paid.
The implementation does not claim normalized marginals or uniform sampling.

Obtaining four independent observations is not free or universally fast. It
can stall indefinitely. The one-instance route requires a suitable generic
member and rationally split axes; failed attempts are counted. The broader
N1077 quadratic-field pipeline handles cases this rational adapter rejects.

## Actual source intake and attribution

The source was read from `harjassand/astra-research-knowledge` at commit
`cb87e72296824ae2a677ccd337025d02d20cbb0a`, beginning with its current entry and
task-first browse, then packet N1077, its **complete governing proof and review**,
and relevant exact source files. This was read-only; no branch was contacted.

[Pinned N1077 packet](https://github.com/harjassand/astra-research-knowledge/blob/cb87e72296824ae2a677ccd337025d02d20cbb0a/knowledge/current/packets/N1077.json)
contains the exact governing source paths and version-bound review scope.
`prior_n1077/` holds byte-preserving copies of five inspected Python sources;
`SOURCE_MANIFEST.json` records their SHA-256 hashes and URLs. They are credited
prior implementation, not newly authored algorithms. `compiler.py` retains its
published hash `91a5daeae2b48321e0c868466b3b2fe46fd47a97165a541042356b25e8c5927f`.

Existing primary ancestry is material, not decorative:

* [Cai--Lu, Holographic algorithms: From art to science](https://doi.org/10.1016/j.jcss.2010.06.005):
  basis acquisition is already an algorithmic operation.
* [Morton, Pfaffian Circuits](https://arxiv.org/abs/1101.0129):
  nonsymmetric and odd signatures, heterogeneous basis changes and Pfaffian execution.
* [Margulies--Morton, Algebraic models and Pfaffian circuits](https://arxiv.org/abs/1311.4066):
  linked polynomial systems are an existing heterogeneous-gauge recognition route.
* [Chernyak--Chertkov, Planar Graphical Models Which Are Easy](https://arxiv.org/abs/0902.0320):
  the gauge-transformed planar free-fermion family is established.

The primary sources and N1077 are strong comparators. This package does not
rename them as a new general learning theory. It retains a precise all-weight
reuse bridge and the failed leverage result for future work.
