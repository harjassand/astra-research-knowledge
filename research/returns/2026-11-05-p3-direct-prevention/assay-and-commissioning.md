# Finite boundary-rate acquisition and bounded operating commissioning

The direct [mean-lifetime decision](README.md) needs the arithmetic mean of actual boundary recovery rates, not the unknown global rarity. The [finite-hold theorem](package/next6_root/finite_hold_theorem.tex), [grouped-wait PDF](package/next6_rate_assay/finite_rate_assay.pdf), [complete assay proof](package/next6_rate_assay/rate_assay_body.tex) and [safe-start proof](package/next6_root/safe_start_preparation.tex) supply these interfaces with finite errors and exposure.

## Actual local measurements

The endpoint-read realization chooses a component uniformly, sets only its local neighbours failed on a faithful copy, pins the focal bit failed, applies the actual intervention, releases for a finite hold and reads recovery. It does not prepare the whole installation globally failed. Pin/context/read errors, random-coordinate precision and actual hold-time uncertainty are priced. The preferred timer may depend on previous trials but is exogenous to the current focal trajectory; a weaker alternative covers more responsive timing. Those are different service contracts.

The second realization groups **four waits at the same chosen component**, then averages across components. For S the sum of four exponential exit waits, the classical estimator has `E[3/S]=lambda_i` and second moment `3lambda_i²/2`. Pooling heterogeneous waits first and inverting their overall mean would estimate a different quantity.

Finite censoring, clipping, timestamps/deadlines, arithmetic and conditional setting/pin/detector errors are included, including the chance timer error changes a censor decision. Discarded trials retain their prior dwell/preparation costs. For local rate contrast kappa and K menus, a sufficient group count is `ceil(40kappa eta^-2 log(2K/delta))` per menu. Uniform conditional service bounds permit dependent reused cells; fixed calibration faults are a separate confidence event, not made independent by repetition. Expected ideal dwell is at most `4/lambda_-` per group, with finite actual caps and timer tolerance of order `eta^(5/3)lambda_-/lambda_+²`.

The [assay status](package/next6_rate_assay/STATUS.txt) distinguishes the final direct-mean schedule from the preserved earlier median-of-means implementation. The classical estimator and concentration methods are credited, not claimed new.

## Uniform safe-start means replace equilibrium preparation here

The supplied theorem gives explicit A*,B* with

```text
A* M_u <= E_(x,Q^u)tau_b <= B* M_u, every x!=b.
```

For **any** actual initial law nu_u with `nu_u(b)<=f`, assigning a failed start zero lifetime gives `(1-f)A*M_u<=E_(nu_u,Q^u)tau_b<=B*M_u`. This avoids using TV closeness to infer the expectation of an unbounded hitting time.

A graphical comparison with independent worst-case bits bounds the probability of being all failed after ordinary repairable operation. Its clocks are proof devices, not extra controls. With `a_w=r_-(1-qbar)`, `c_w=r_+qbar` and

```text
q_dom(t)=c_w/(a_w+c_w)+a_w exp[-(a_w+c_w)t]/(a_w+c_w),
q=q_dom(D_-), Delta_D=D_+-D_-,
chi_D=min{1,q^N+N c_w Delta_D q^(N-1)},
```

chi_D covers an entire certified mission-start window, including bounded adaptive terminal timing. The procedure installs/settles the selected intervention, runs the repairable system for that bounded interval, then starts the mission. It does **not** certify the individual specimen certainly safe. Installation, slew, settling, timer fidelity and summed component exposure are paid.

Combining estimation, correction and actual commissioning gives the selected/best **actual** mean ratio at least `(1-chi_D)(A*/B*)(ell/U)(1-eta)/(1+eta)`. Every factor must meet the target tolerance. The one-bit inspection alternative and stronger relative-equilibrium preparation remain separate operations with their own read, latency, retry and exposure contracts; they are not silently free resources here.

No physical apparatus or local service was executed by Capital. Producer runs are synthetic and their underlying contract assumptions remain inputs. [Full package/source metadata](SOURCES.json), [evidence and calibration bill](information-and-execution.md).
