# Seed extent, terminal readout, tail acquisition and execution costs

The [main report](package/report_text.txt), [final status](package/STATUS.txt), and [uniform-horizon refinement](package/independent/fault_tolerance/uniform_horizon_refinement.md) govern the selected [burst-recoverability opening](README.md). The earlier [readout/scope audit](package/independent/fault_tolerance/readout_and_scope_audit.md) preserves useful corrections and alternative targets; it is not permission to change the final fixed-seed quantifier silently.

## Necessary seed extent and finite-device endurance

For Pareto radii with alpha>d+1, let beta=alpha-d-1 and `C=Gamma(d+1)Gamma(alpha-d)/Gamma(alpha)`. At scales r0>=1, the complete-cone hazard tends to `lambda 2^d C r0^-beta/(v beta)`. Uniform total error<=delta<1/2 necessarily requires

```text
r0 >= [lambda 2^d C/(v beta[-log(1-2delta)])]^(1/beta).
```

This is a necessary spatial-extent charge, not an achieved initialization or automatic hardware-volume lower bound. Sparse records may be far apart and must pay their communication/readout costs separately.

For a closed device whose whole accessible state remains inside half-side L, full-cover resets occur at rate `h_L=lambda 2^d C L^(d-alpha)` for L>=1. The recoverability horizon obeys

```text
T_delta<=-log(1-2delta)/h_L.
```

Thus fixed positive heavy-tail noise bounds endurance polynomially in spatial extent regardless of repair quality. The conversion to hardware volume needs a shape/density convention. This ceiling does not construct a memory attaining it.

## Readout is part of the physical task

Evaluate the causal bound at actual delivery time, including a readout duration after storage. The reader, its mutable state, diagnostic transcripts and earlier usable outputs belong to the complete information support. An ideal global decoder strengthens a lower bound; it does not implement a positive local query operation.

For a fixed terminal observation cube of halfwidth r_out, the last h units of operation alone give output-error floor

```text
P_error,out>=(1-exp[-Lambda_out(h)])/2,
Lambda_out(h)=lambda 2^d integral_0^h E(R-r_out-vu)_+^d du.
```

Increasing internal memory size cannot remove a reset of the final backward observation cone. Unflagged corruption may overwrite both an answer and its success flag, so heralding is not automatically a remedy.

The minimal useful target is a declared finite terminal instrument with fixed error floor, initialized independently and connected only for the query, plus paid commissioning/storage/transfer error. Its total bound must include all terms, for example `epsilon_init+delta_store_transfer+epsilon_terminal`, and remain below a fixed nontrivial target such as 1/4. A fixed bare input likewise has an early-loss floor before replication.

Arbitrary total accuracy instead needs an earned scalable observation/protected-receiver contract, with extent, processing time, hardware and energy allowed to grow appropriately. Renaming a fixed noisy cell a decoder does not create it. The target does not promise infinitely many readouts jointly correct.

## Why the earlier critical-tail example is not a contradiction

For a tail proportional to `1/[r^(d+1)log r]`, E R^d is finite but E R^(d+1) is infinite. The fixed-seed obstruction still forces eventual forgetting. Yet the full-reset ceiling for a device whose initial input-dependent extent grows with L is order L log L, larger than its order-L propagation scale.

This leaves room for a weaker, separately commissioned device family with seed extent growing with mission length; it does not prove recovery even there. The final selected target keeps r0 independent of horizon, while permitting charged input-independent layout/schedule dependence on horizon. The [final refinement](package/independent/fault_tolerance/uniform_horizon_refinement.md) explicitly retains the lower theorem uniformly over that family. General tail behavior cannot be reduced to a Pareto label alone.

## Tail class and physical access must be earned

Finite unrestricted radius samples cannot uniformly certify the infinite-moment class. A bounded law F0 and `(1-epsilon)F0+epsilon G`, where G has finite d-th but infinite (d+1)-st moment, produce n-sample laws within n epsilon in TV while having different moment classifications. Completion needs a justified tail envelope, a restricted estimable family, or a finite-horizon guarantee retaining residual uncertainty. This is not a distribution-free inference of the physical noise law from a short trace.

Commissioning must implement finite encoding with a paid writer, timing, energy and error budget, then disconnect all external copies. Bounded reliable immutable local gate laws and an input-independent schedule are declared mathematical premises; a platform must realize them. All mutable controller/decoding memory is corruptible. Density, local state, update rate, replacement materials, latency, metrology, power and every horizon-specific installation remain charged.

For a filled region growing like r0+vt at constant power density p, cumulative energy scales, up to geometry, as `p[(r0+vT)^(d+1)-r0^(d+1)]/[v(d+1)]`. This is an explicit design cost, not an optimal thermodynamic bound. Infinite-duration service has unbounded total resources even at bounded local density and power. No bridge from the prior Gibbs, skip-free, finite-source repair or loaded-LTI classes is assumed.

## Supplied checks and preservation

The [root check receipt](package/results/opening_checks.json), [independent finite checks](package/independent/fault_tolerance/check_results.json), [first-principles checks](package/independent/first_principles/check_results.json), and [final scoped audit receipt](package/results/final_audit_receipt.json) record producer-side verification of closed-form identities and finite Toom examples. They do not prove the proposed multiscale recurrence, positive sufficiency or a physical implementation. The [figure](package/figures/cone_erasure_bound.png) plots unavoidable-error lower bounds, not recovery measurements.

The [complete preceding productive-control ZIP](package/preserved/Astra_Productive_Control_Research_Package.zip) is preserved unchanged, including its nested prevention and first-event packages. Inherited P2 source receipts retain their pinned provenance inside that predecessor; they do not imply a new standalone P2 source copy or cross-class reduction in this root.

The assembly script retains its original workspace expectations and is provenance rather than a portable extracted-package verifier. The supplied release manifest records delivered file identities. Capital published the original bytes, proofs, checks and independent rejection reasons without executing source programs, rendering/building the report, loading scientific arrays or reopening earlier scientific audits. The recovery converse, historical priority and civilisation-changing capability remain unestablished.
