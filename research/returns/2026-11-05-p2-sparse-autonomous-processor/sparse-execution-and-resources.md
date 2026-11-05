# Sparse execution, initialization and complete resource accounting

[Return guide](README.md) · [Full proof report](package/report.txt) · [Accepted predecessor](package/accepted_reusable_report.tex)

The liveness lemma counts every register from preparation/input through its last syntactic read, retaining all controlled operands independently of the controller's value. Serial routing increases distance and duration without requiring every padding site to hold a live token. A finite gadget library therefore has a maximum live child-block count `Q_*` independent of padding `B`, giving `Q_m<=Q_* Q_(m-1)`.

The compiler retains only live source-register occurrences `(x,phi)` over a period. It installs two mutable registers at each retained occurrence, with fixed local layers of on-site swaps, continuation swaps, actual source resets and equal-phase gates. Persistent values form cycles; scratch forms paths. Discarded states travel backward and re-enter a useful track only through reset. Both tracks count toward hardware and updates.

Each cohort executes the intended source circuit by a tensor-factor channel identity. This is not an independence assumption about arbitrary junk or environments. The inherited annular embedding and selected radial tube retain the actual Poisson-source geometry and strong normalization contracts. Deleted padding is not treated as free physical storage or a fresh independent effective-noise law.

## Costs and fixed physical intensity

With `H=B^m`, `A=CB`, `kappa=log_B A`, `zeta=log_B Q_*`, logical width `w` and kernel factor `bar_b=b+w+1`, the report gives

```
P = O(bar_b H^kappa)
N = O(w bar_b H^(kappa+zeta))
L = O(bar_b H^kappa)
U_all = O(N K P).
```

The source error budget retains initial/final apparatus error, once-paid raw interface error, known-word preparation error, all protected bulk locations and whole-computation synthesis error. Memory uses logarithmic logical width/depth and chooses `H` to pay both the requested horizon and rounded extra period. Every installed register is charged on every tick, including waiting and backward tracks.

The threshold cannot silently shrink as padding grows. The supplied construction first fixes baseline code/alphabet/intensity, uses a finite baseline boost into each upper family's threshold, and then a computable slow horizon diagonal. Family constants, baseline overhead and selection work enter the `T^o(1)` terms. The resulting asymptotic exponents hold at one fixed positive intensity; constants can be enormous and no useful numerical threshold or practical hardware estimate follows.

Layout enumeration costs `O(N polylog N)` description work without scanning the deleted dense rectangle. Components and wire segments cost `O(N)`. Known controller initialization uses charged noisy local writes, bounded depth under declared distributed access, and a spatial span that can grow with `H`. Fabrication and access are declared resources rather than autonomously produced capabilities. Register time is not energy.

## Matching lower bound and its domain

For a static bounded-range device, a fixed Poisson substream covers the input-reachable component at rate at least `c lambda N^-r`. An allowed mark resets that whole component and discards its information. With an independent Bell input, no-signalling makes the reference inaccessible after the reset, even if apparatus components were entangled before admission. Thus

```
delta >= (3/4)(1-exp(-c lambda T N^-r)).
```

For `delta<=1/4` this forces the register exponent; bounding radius and all-register time give the remaining exponents. All input-bearing wires, buffers, accessible persistent environments and readout storage count. Moving carriers, changing layouts, external cached outputs and uncounted long-range carriers change this lower-bound model. It is not a universal energy theorem.

The original [adapter](package/sparse_adapter.py), [transaction harness](package/framed_transfer.py) and recorded [adapter checks](package/finite_checks.json)/[framed checks](package/framed_checks.json) are preserved as supplied. Their finite count/identity examples are not physical thresholds or full concatenated-code simulations. No script, numerical array, solver, PDF build or corpus build ran during this intake.
