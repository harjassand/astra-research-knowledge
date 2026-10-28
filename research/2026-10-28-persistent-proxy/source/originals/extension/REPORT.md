# Exact proxy acquisition: executable extension and its drift boundary

Mission: **NOT_ACHIEVED**. This branch delivers an exact operation and a sharp
operational boundary from N1073. The constructions use established block-channel,
coupling and Bernoulli-factory methods; historical novelty and practical advantage
remain UNKNOWN. New general derivations await a substantive independent audit.
N1073's existing completed version-matched audit remains sufficient at its scope.

The pinned archive advanced to `e1e2272165c8548326c31bb11817c28f871d21e9` with
1762 records. The complete governing proof and completed review were read and
retained with hashes; see `SOURCE_MANIFEST.json`. Only selected navigation and
sources were fetched. No shared checkout, archive record or public state was edited.

| Contract | Cheap calls | Raw disclosure probability |
|---|---:|---:|
| Accepted source pair, one exact known-channel record | 1 | 3/40 optimal |
| Persistent X, two known-channel records | 2 | 0; ordinary classifier/garbling matches |
| Open stationary uncertainty, any fixed finite cheap budget | 0 suffices | 11/40 optimal |
| Stationary uncertainty, TV radius 1/600, unbounded sampling | 44351/32 expected | 0; explicit lazy exact factory |
| Exact robustness to every tiny finite-prefix nonstationarity | 0 suffices | 11/40 optimal, even with unbounded stopping |
| Ordinary approximate comparator, TV tolerance 1e-6 | 102 fixed | 0, also tolerates predictable drift |

These rows have different correctness/source contracts. The proofs state the
quantifiers, and every ordinary comparator gets the identical observations,
calibration information, persistence promise and raw-access cost.

The nominal two-record construction outputs zero with probabilities
13/25,17/100,0 according to whether 0,1,2 records equal zero. Its exact matrix
identity holds at every input. An ordinary nearest-column classifier with an
exact stochastic garbling also uses two records, so this is no special
algorithmic advantage. A general classifier/inversion construction is proved
for all strictly positive finite K and distinct known L columns, with explicit
separation, type-enumeration and bit-cost limitations.

The robust factory works at an unknown fixed channel point, using a persistent
stationary iid cheap stream. It starts at degree1024, initially continues with
probability3861/65536, then with probability1/8. Expected cheap count is exactly
44351/32, about1386. A lazy uniform comparison evaluates the large exact
hypergeometric sum only on exponentially rare events at positive plateau
margin. This repairs the naive factory's infinite expected bit work and gives
finite expected internal bit work for the stated TV-radius1/600 promise.
Worst-case runtime remains unbounded. This is an ordinary specialization of
[Nacu–Peres](https://arxiv.org/pdf/math/0309222) and
[Holtz–Nazarov–Peres](https://arxiv.org/pdf/0808.1936).

The strongest obstruction is nonstationarity: if exactness must survive any
independent open perturbation of any finite prefix, followed by nominal iid
tail, multi-affine polynomial uniqueness forces the conditional final output
law at every prefix to equal K. A no-raw finite prefix can carry only the
common target subdistribution. Monotone convergence then forces raw probability
at least11/40, even under the nominal stream and even if stopping is unbounded.
Every positive total TV-perturbation budget contains the needed finite open
boxes. Ordinary common-part splitting attains11/40. This does not contradict
stationary-unknown-point factory success.

An equally informed approximate method is much cheaper: threshold102 cheap
zero-indicators at5/12, then sample the corresponding known K column. Its
Hoeffding TV bound is9.455010408690606e-7, certified with exact rational Taylor
bounds. It also works under predictable within-interval drift. Exactness must
have application value before the more expensive exact factory offers value.

Run `python3 verify.py`, `python3 verify_factory.py`, and `python3 verify_lazy.py`.
They check source hashes and primal/dual certificates; all-input two-record
identities; exact drift failures; interpolation ranks; all1025 initial factory
coefficients; selected exact elevation/interval identities; exhaustive uniform-
prefix cases; a forced rare exact fallback; and the approximate bound. Finite
seeded PRNG diagnostics produced96 outputs, including a65536-call terminal
degree resolved lazily, using about0.04seconds for the callback runs. They are
implementation diagnostics, not ideal-law, physical, throughput or expectation
proofs. Analytic proofs carry the general claims and require audit.

Only Y leaves the module. Proxy records, read flags, terminal degree/count,
raw values and memory remain private/discarded. A count independent of X can
still alter the joint experiment when disclosed with Y. The avoided operation
is disclosure of an already-classical X, not a newly avoided damaging physical
measurement. Persistent iid proxy service and calibration remain supplied.

There is no measured complete-resource advantage. The robust factory's
service-only crossover against common-part splitting is roughly5040 cheap
calls per raw disclosure, before other costs. A known persistent input also
allows ordinary one-read caching across many requested outputs. Physical
source acquisition, source stability, application benefit and historical
priority remain unresolved; no civilisation-level discovery is promoted.
