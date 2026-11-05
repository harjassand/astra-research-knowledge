# A small folded tensor statistic need not be a physical causal receiver

The [exact crossed-statistic construction](package/online/crossed_statistic_obstruction.txt) folds the all-output reverse decoder into a tempting two-qubit virtual bond. It reproduces a family with the correct final marginal but fails a necessary physical data-processing condition when treated as the complete source-plus-memory state. This is a construction-specific obstruction, not a general two-qubit memory theorem.

With `c=cos(theta), s=sin(theta)` and Bell-initialized receiver R,A, the virtual update uses `V_AE=cI-2is Phi_AE`. It is completely positive but generally not trace preserving. On its particular initialized full input family each prefix has unit trace, and a global folded isometry exists. Neither fact makes the local map a physical CPTP update after prior carriers have been discarded.

The exact family closes using four functions `u=c^(2n)`, `v=(1-s^4)^n`, `w=[c^2(c^2-s^2)]^n` and `h=n c^(2n-1)s^3`. Its joint source/receiver distinguishability for orthogonal input states decreases and later increases. Any physical continuation of the **complete** retained state, with fresh independent carriers, is CPTP and cannot do that, even when the inaccessible true source is included in the tracked state.

At `.1`, prefix n=2,896 gives distinguishability at most about `.250005499`; matching that exact complete virtual state forces every later recovery to have error at least `.374997251`. Per-input half-trace approximation error eta weakens this bound by eta. Additional correlated quantum or classical records change the state being specified and can evade it. [Closed-form verification](package/online/crossed_statistic_verification.json).

The optional extension SDP found a feasible first step and numerical second-step difficulties; solver infeasibility without a dual certificate is **not** used as proof. The analytic trace-distance argument supplies the obstruction. Source programs, versions and the finite receipt are retained without rerunning the solver.

## Measured failure histories and coherent flags have different scopes

A physical filter can implement success `K=(cI-2is Phi)/sqrt(g)`, `g=1+3s^2`, and a complementary failure. If flags are measured or dephased and every success retains exactly the specified folded statistic, the [all-continuation theorem](package/schur/CLASSICAL_SPARSE_FAILURE_BOUND.md) allows arbitrary quantum memory and continuation on failure branches yet gives

```text
epsilon >= g^(-n)(1-D_n)/2,
```

where D_n is the exact all-success source-plus-memory distinguishability. The source may even be granted at this prefix for the converse. A weak-angle specialization gives a positive floor exceeding `.014`; the `.1`, n=25 fixed-matrix illustration is about `.0433357`, not a hardware experiment or interval certificate.

Fully coherent success/failure histories retain off-diagonal operators and evade this classical direct-sum argument. The isometric completion has a bounded one-flag probability and an abstract sparse-Hamming-weight subspace, but two operations remain unproved: payload recovery after discarding spent carriers, and efficient causal coherent compression with bounded local gates. Sparse occupation alone establishes neither. Extra coherent success records are also outside the stated failure theorem. [Final status and physical candidates](package/schur/PURE_BASELINE_AND_FINAL_STATUS.md), [instrument/cost page](physical-instruments-and-costs.md).

No additional scientific run, new audit or broad impossibility claim was introduced by publication. [Complete original package and provenance](SOURCES.json).
