# Direct decisions about long-run compliance

**Status.** A completed independent construction and selection boundary. It is a useful companion, not a claim that ordinary experimental design has been superseded. The central exact result is a Blackwell comparison of entire causal experiments. Its material example has a matching finite protocol and a separate operation that removes an arbitrary, bounded-energy initial state without waiting for equilibration.

The question is deliberately different from predicting a force response or preparing an unknown bath: can a local experiment decide whether an internal elastic strain is frozen forever or relaxes at a specified very small rate? The two answers give a constant difference in long-run compliance. The experiment can decide before the slow strain relaxes, but cannot do so at a rate-independent deadline, even if the initial state is perfectly known.

The exact statements and proofs are in [theorem.md](theorem.md). The executable calculation is [execute.py](execute.py); it writes `execution.json`. All quantities are dimensionless after normalizing the local drag to one.

The independent assessment of the selected thermal programme is in [thermal_endpoint_challenge.md](thermal_endpoint_challenge.md). Its constructive [weighted_score_corollary.md](weighted_score_corollary.md) supplies a finite private weight cache, an explicit error bound, and a next-round entropy ledger that counts the actual retained output after cache reset or isolation. It does not promote a new meter record to an independent old reference.

## Completed endpoints

1. For two known zero-state linear time-invariant plants whose difference impulse response is nonnegative, a maximal nonnegative input envelope Blackwell-dominates every causal adaptive or randomized input satisfying that pointwise envelope. Under Gaussian white position readout, the entire optimal decision problem reduces exactly to a scalar Gaussian experiment. This includes all bounded stopping rules before a declared deadline.
2. A frozen-versus-Maxwell strain pair has DC compliances `1/(mu+B)` and `1/mu`, but its optimal decision information has three regimes: proportional to `lambda^2 H^7`, then `lambda^2 H^3`, then `H`, with the dimensional constants given in the theorem. At fixed force, readout noise and confidence, its optimal small-rate decision time scales as `lambda^(-2/3)` while its slow relaxation time scales as `lambda^(-1)`.
3. Smooth finite force ramps and finitely many integrated readings retain this advantage. Initial preparation, metrology resolution, force calibration, sensor bandwidth, dynamic range, computation, occupancy and reuse are explicit resources.
4. For the simple binary pair, an exactly specified fourth-order differential annihilator removes *both models' entire unknown initial-state output spaces*. One bipolar force and a polynomial readout weight then attain the same `lambda^(-2/3)` decision-time scaling. This does not require passive equilibration or private timing; it pays the known two-state structure, model precision and finite metrology range. It also prevents incorrectly interpreting the cost of a generic readiness construction as an impossibility theorem for structured decisions.

## What this contributes to selection

Readiness and finite-horizon prediction do not make an infinite-time classification uniformly observable. Conversely, absence of readiness need not obstruct a decision when the nuisance dynamics are known and can be removed in the observation itself. These conclusions follow from complete operations and a lower bound, rather than from a fitted response table.

The equally informed ordinary comparator is strong: known-model matched Gaussian testing and initial-state elimination already provide this operation. The exact experiment comparison is the most general statement here; no historical-priority claim is made. This line should remain a preserved companion while a programme with a stronger new consequence receives concentration.

## Primary comparators

- Blackwell, *Comparison of Experiments* (1951), original Berkeley proceedings: <https://digicoll.lib.berkeley.edu/nanna/record/112749/files/math_s2_article-08.pdf?registerDownload=1&version=1&withMetadata=0&withWatermark=0>.
- *Bayesian Input Design for Linear Dynamical Model Discrimination*, Entropy **21**, 351 (2019): <https://www.mdpi.com/1099-4300/21/4/351>. Its energy-constrained problem has different optimal inputs; the present nonnegative contrast and pointwise envelope conditions matter.
- Noom, Soloviev, Smith and Verhaegen, *Online input design for discrimination of linear models using concave minimization*: <https://arxiv.org/abs/2401.05782>. Adaptive linear-model discrimination is an established strong comparator.
- Rothermel et al., *A method for determining the parameters in a rheological model for viscoelastic materials by minimizing Tikhonov functionals*: <https://arxiv.org/abs/2102.13610>. Generalized-Maxwell parameter acquisition is a broader and more costly target than the binary decision constructed here.

The source list supports the comparison and context. All new mathematical claims in this package have their proofs in `theorem.md`; they do not rely on an unacquired oracle or the historical novelty of a name.
