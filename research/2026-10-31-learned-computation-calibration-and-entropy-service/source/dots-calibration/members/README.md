# Robust calibration checkpoint
31 October 2026

The main result is a finite-rate complete classical-quantum perturbation bound: for two source laws sharing the same stationary distribution and exactly centered coupling, controlled output error can be bounded independently of microscopic switching rate. It covers retained source labels and prescribed CQ instruments, not arbitrary source quantum coherences. A mean-changing bias counterexample shows why the restrictions matter.

Read source_model_robustness_20261031/COMMON_STATIONARY_CQ_ROBUSTNESS.md first, then BOUNDED_INNOVATION_CALIBRATION_RECEIVER.md. The latter earns a statistical model-error certificate for a known invertible affine mechanism with unknown iid bounded-width innovations. It does not infer the mechanism or validate iid assumptions from data. Its exact-rational calibrator is executable; the downstream quantum simulator is not implemented here.

The mathematical result, statistical receiver, executable calibrator and one-bit refinement have separate internal review receipts. Both supplied and independent code tests passed. Small dense CQ diagnostics are checks, not complete-norm proofs or performance comparisons. Code uses Python standard library; dense diagnostics use NumPy/SciPy.

False PASS is bounded jointly over training, not a posterior guarantee for each accepted transcript. Every observed clock event including selfloops must be supplied; fixed sample size is a caller commitment. Output dictionaries are recomputable results, not tamper-proof certificates. Model error and execution error accumulate over future experiments even though the same statistical confidence event can be reused.

Calibration costs can be large. The one-bit comparison reduces one sufficient sample bound from 489,982,526 to 80,613 using specialized constants; neither is a lower bound. The general executable calibrator retains the general constants. No practical advantage or historical novelty is established. ORDINARY_AFFINE_INNOVATION_COMPARATOR.md documents strong dense and multiscale alternatives, including inexpensive approximate Fourier calculations; an exponential exact closure is not an approximation lower bound.

The earlier affine realization and pure-return compiler remain prerequisites in previously delivered archives, notably Astra_Learned_Source_Acquisition_and_Reuse_20261031.zip and Astra_Pure_Return_Program_Compiler_20261031.zip. Relative links to those earlier source files describe dependencies, not additional files in this ZIP.

All source bytes are unchanged. MANIFEST.json records hashes; ZIP CRC and every included file hash were checked. Further lift/coalescence investigations are not included.
