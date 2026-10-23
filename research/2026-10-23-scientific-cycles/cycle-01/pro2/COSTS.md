# Observed costs and error accounting

This record distinguishes construction, unsuccessful attempts, verification,
prior work, and delivery. All original receipts are retained. No isolated
proposal timing is presented as an accepted calculation. Timers below refer
to their stated scope; they are not a monetary, energy, or end-to-end research
cost estimate. Computational paths are relative to `research/` in the archive.

## 1. Main new actual-input calculation

Python3.12.14, NumPy2.3.5, SciPy1.17.0, OpenBLAS0.3.30 on the available
CPU runtime. Both BLAS libraries used one thread for the main calculation.
No GPU, purchased compute, new data collection, new probes or added Krylov
steps were used. Integer products use explicit overflow guards and multi-limb
accumulation into Python integers; complete-basis residual acceptance is exact
up to outward rational square-root bounds.

| Activity | Wall seconds | CPU seconds | Peak RSS bytes |
|---|---:|---:|---:|
| Initial failed scout invocation | 0.608256022 | Not retained | Not retained |
| Successful scout and frozen preconditioner, body | 0.563941192 | 0.562245922 | 96,215,040 |
| Joint certificate producer, body | 39.019276241 | 39.016117860 | 238,608,384 |
| Independent replay, body | 39.306566515 | 39.506364305 | 239,243,264 |
| Independent replay, enclosing process | 39.758677765 | Includes preceding CPU scope | Same process |

The body and enclosing replay timers overlap and must **not** be added.
The failed scout expected three loader outputs instead of two; the one-line
unpacking correction changed no input or theorem. The successful scout was
run once. Its SVD0.125259032s is contained in its body timer, not an extra cost.
The main producer and independent replay were each run once.

### Producer breakdown, already included in39.019276241 seconds

| Stage | Wall seconds |
|---|---:|
| Original exact-decimal input reconstruction | 0.257013492 |
| Strict support proof by component row sums | 0.005503710 |
| Exact change of512-column coordinates | 6.716619543 |
| Exact coordinate Gram | 8.127264555 |
| Exact sparse action on512 rounded-coordinate columns | 0.120919997 |
| Exact cross-action product | 10.573486481 |
| Exact action Gram | 11.412717401 |
| Lower pencil construction | 0.195767048 |
| Lower floating eigenproposal | 0.036987954 |
| Lower complete certificate verification | 0.319738859 |
| Upper pencil construction | 0.212193575 |
| Upper floating eigenproposal | 0.035321672 |
| Upper complete certificate verification | 0.307311409 |

The difference between the stage sum and the body total includes source
hashes, rounding/norm scalar operations, certificate assembly and other
untimed body work. The512 actions are charged even though the spanning
vectors were previously saved. They cannot be inferred free of cost from
the scalar Jacobi matrices. No omitted-complement basis was enumerated.

## 2. Sparse identification attempts and actual conditioning witness

| Activity | Wall seconds | Timer scope |
|---|---:|---|
| Initial339-column local-rank construction | 0.873786552 | Including Python imports |
| Initial selected-minor replay | 0.639225728 | Including imports |
| Original degeneracy order construction | 0.030234011 | Body |
| Nine-column symmetric construction and clique attempt | 0.566901561 | Including imports |
| Nine-column selected-minor replay | 0.541821593 | Including imports |
| Independent degeneracy and no9-clique verification | 0.511630065 | Including imports |
| Root84-vertex core construction | 0.043208654 | Body |
| Independent core and dimension-obstruction challenge | 0.048456051 | Including imports |
| Actual dyadic sensitivity witness producer | 0.209474910 | Body; includes0.148673457s SVD proposal |
| Actual sensitivity witness replay | 0.070603267 | Body |
| Independent Fraction/support/noise-witness checker | 0.154445284 | Body |

The339-column construction is valid but superseded; its cost remains.
The9-clique argument failed; its complete search/check is within the
indicated symmetric and degeneracy runs. The84-vertex core argument proved
the sharp eight-versus-nine identification threshold instead. Neither
identification checker computes matrix actions, reconstructs coefficients,
or produces a spectrum, so these small timings are not accepted spectral
calculation timings. The nine-column loader materializes the earlier339
column prefix before slicing nine; that implementation cost is included.

The noise witness is proposed once on the657-coefficient core map and
rounded to denominator2^40. Its exact acceptance uses no floating SVD.
Independent verification checks every original nonzero support location
and exact action entry. The producer's peak RSS was86,822,912 bytes; the
independent Fraction check's peak RSS was34,578,432 bytes.

## 3. Structural proof checks

| Check | Wall seconds | CPU seconds | Scope |
|---|---:|---:|---|
| Completion theorem fixtures | 0.034004261 | 0.033990393 | Four exact rational cases, including support-boundary failure |
| Integer product kernel | 0.063060163 | 0.063062265 | 29 fixtures,10 invalid-input rejections; small scale test included |
| Path flow and isometry | 0.029332419 | 0.029304189 | 12 exact rational fixtures and2 dependent-row null cases |
| Row-cap counterexample | 0.015776333 | 0.015750594 | Exact quadratic-field Gram/eigenvector proof for n4 |
| Forest operation | 0.018744901 | 0.018732572 | Eight exact recovery/noise fixtures and5 invalid forests |

These checks complement full universal proofs; theorems are not inferred
from fixture counts. The forest operation's computational model is three
action calls plus O(n) design/recovery, with explicit absolute noise and
per-row energy constraints. No new NIST actions were taken for that theorem.
Downstream spectral inference would require its own costed computation.

`results/cost_ledger.json`, generated by `src/build_cost_ledger.py`, lists
each distinct metered activity and a subtotal using the enclosing independent
replay timer. Stage timers and duplicate receipt files are excluded from
that subtotal. Some timers include imports and some measure bodies, so the
subtotal is only the sum of observed scopes. It is not total elapsed time
when agents run concurrently and is not full research cost.

## 4. Error budget and accepted boundaries

Original matrix conversion gives
`tau=11685898332914907/604462909807314587353088`, about1.93327e-8.
The joint support is S=M+tau, with M=2340600979/4294967296. Strictness is
proved by exact component row sums, not assumed from a floating eigenvalue.

| Joint pencil error source | Lower operator | Upper operator |
|---|---:|---:|
| Exact compressed quantization allowance | 3.4386142606288455e-8 | 3.43807595857027e-8 |
| Original exact-input allowance | 3.160646864233561e-8 | 3.160740367932518e-8 |
| Coordinate rounding allowance | 2.3118179763036223e-10 | 2.3118179763036223e-10 |
| Total before complete eigenverification | 6.622379304625443e-8 | 6.621934506265824e-8 |
| Final sorted eigenvalue radius | 8.177798345891796e-8 | 7.239547521508489e-8 |
| Certified sign margin | 2.4395208701284564e-7 | 2.6544178872667994e-7 |

Displayed decimals are explanatory; exact outward rationals in the receipt
govern acceptance. No sign remains unresolved. Integer arithmetic guards,
source hashes, coordinate rank, and allowance composition are independently
challenged. A changed source, nonzero threshold interval, failed rank bound,
or overflow guard stops the checker; it does not silently retune precision.

The sparse sensitivity witness has its separate absolute error model:
`||DX9||F` versus `||D||2`. It is not converted into a CDF guarantee, a
relative error model, or a global inverse upper bound. Likewise the path
minimax theorem assumes unit rows, while the capped-row theorem has weaker
constants. The failed stronger extension is preserved as an exact counterexample.

## 5. Prior work and incumbent, not new costs silently reset to zero

The original owned checkpoint contains its full construction and unsuccessful
attempts. Its whole fixed experiment took59.441511705s; its original replay
took33.143811565s. The verified dense proposal plus verification took
1.675848413s before shared input conversion, with maximum width9/1074.
The old tested certificate's maximum width was0.6288212904932393. All stand.

The incoming ell0 and heldoutell7 canonical-quadrature bodies took about
7.54s and7.15s for construction and checking, excluding research/authoring/
integration. They are accepted with their supplied provenance and checks;
they were not rerun merely to produce another audit. Their single-probe
widths are not compared as a matched performance gain against aggregate
envelopes or the common unweighted class.

The new common-action producer is already substantially more expensive
than the old dense proposal and verification, even before independent
verification and research. Its output is also a different information-class
result, not a tighter practical CDF enclosure. No new dense speedup is claimed.

## 6. Research, delivery and unknown totals

Scoped primary-literature work is recorded in four contributor notes:
completion theory (about18.5s source-call latency), sparse recovery (19.0s),
path conditioning (16.5s), and the treewidth comparator (5.2s). Several
arXiv/publisher routes failed and one Cornell request returned429; these
attempts are recorded. Root also read the primary papers and source packet.
These are access latencies, not complete research time or prices.

Proof development, mathematical challenges, code authoring, model inference,
tool/service latency, network, integration, money and energy were not all
metered. They are **unknown additional costs**, not zero or included in a
small checker timer. No price or physical energy advantage is asserted.

Package construction and the isolated portability check are separately
recorded in `delivery_receipts/`. The portability check replays only the
small new checks; it does not redo the already independently accepted
39-second joint computation or the resolved moment trial. Its purpose is
to test relocatable paths and the complete receiving source, not to generate
a new scientific result. Private attachment/chunk upload and readback costs
are recorded in a sidecar transport receipt after the final immutable ZIP
is created, so the ZIP's own digest cannot depend circularly on its uploads.

The completed relocated quick check passed all11 programs. Its wrapper body
took2.792118512s, with2.831873324s enclosing process time and2.831246s
subprocess-tree CPU. Maximum individual child-process peak RSS was59,650,048
bytes. These timers overlap and are one delivery check. An initial process
creation failed at the execution service after about22s, before a process
or output directory existed; an observed-state check preceded the one retry.
That infrastructure latency is separate from numerical status and is charged
in the portability receipt. The initial package copy and first manifest
took0.066197039s. Final manifest/ZIP/CRC construction has its own sidecar.

The final archive size and SHA-256 are transport identities, not measures
of scientific productivity. A successful upload/readback does not establish
Max's independent reconstruction or scientific acceptance.
