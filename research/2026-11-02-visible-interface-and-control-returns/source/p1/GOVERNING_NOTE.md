# P1 continuation (independent): task-contrast causal interfaces
**Status:** new research note, separate from the frozen killed-excursion/two-mode packet. 2026-11-02. **No claim of new experimental realization or unique discovery.**

## Decision contract and obstruction

Let `H` be an arbitrary, possibly uncountable hidden physical history/mode, and `W` the indicator that a process has completed its upstream milestones. In the inherited stationary-mode instance, `P(W=1|H)=p(H)^(L-1)`. For two terminal actions `a,b`, their unmodified target contrast is

`Delta_original = E[ W {A(H)-B(H)} ]`.

The exact-two-mode sign result from the frozen P1 work is valid, but no finite passive assays rule out a rare third mode of mass `epsilon`. Formal coupling: if two sources differ only when a sampled experiment encounters an event `C` of probability at most `epsilon`, their `n`-trial transcript total variation is at most `1-(1-epsilon)^n <= n epsilon`. Any adaptive sequence with per-experiment encounter bounds `epsilon_i` has TV at most `sum epsilon_i` by sequential coupling. Thus neither higher-order fitting nor a different estimator can extract a guaranteed sign when all permitted experiments miss a sign-reversing mode.

There are only two operational exits in this construction: **illuminate** the rare relevant region with a properly reweightable experiment, or **neutralize** its influence by changing the physical operation. The second route is developed here, because the first is already substantially established enhanced-sampling methodology.

## New physical operation: a task-contrast cut

After the upstream process reaches a *digitally verifiable task state* `z`, it passes only this task code to an isolated downstream actuator/assay. The downstream physical carrier, bath and driving noise are drawn independently of the upstream source. Actions `a,b` are now implemented by this downstream actuator. Define

`d(h,z) = E[reward(a)-reward(b) | W=1, H=h, Z=z, physical cut used]`.

A *task-contrast isolator* is weaker than a complete state reset: it needs only `|d(h,z)-d0(z)| <= e(z)` for **every** upstream hidden state `h` compatible with `z`. It does **not** require a correct Markov model, latent rank, full prepared upstream state, or mode detection. Its decision theorem is:

`Delta_cut = E[W d(H,Z)] >= E[ W {d0(Z)-e(Z)} ]`.

If the task only permits one canonical `z` and `d0(z)>e(z)`, action `a` is better *conditional on reaching the terminal decision* for **every** upstream source, including one with a 10^-9 persistent mode. This statement remains true at any finite horizon, without measuring `P(W)`; strict improvement in unconditional reachability additionally requires `P(W)>0`. For several `z`, a uniform positive lower bound works, or a `z`-specific action can be chosen at the actual observed checkpoint.

The interface can be **strongly causal** (`X_downstream = F(z, independent_fresh_carrier, independent_bath, action)`), in which case `e=0` by construction *inside that physical model*. The experimental challenge is to enforce that structure: flush/replace the sample, prevent upstream material from entering the downstream assay, transmit the task state via a fixed-format digital signal, remove timing and analog side-channels, and qualify shared temperature/field contamination. A detector result or a successful flush alone cannot establish this bound at 10^-9.

## Conditional quantitative physical error, not a free assumption

In a tractable downstream subsystem, suppose the reference path under action `v` follows

`dX_t = b_v(X_t) dt + sqrt(2D) dB_t`, `0 <= t <= T`,

and an unknown upstream mode `h` enters only by an extra drift `c_{v,h}(t,X_t)` whose **physical** worst-case magnitude is bounded by `gamma`, with unchanged diffusion coefficient `D>0`. Suppose the fresh carrier's actual starting distribution differs from the calibrated reference by total variation at most `rho`. A task-code decoding error has probability at most `chi`, uniformly over the upstream hidden state.

By Girsanov, conditioned on a fixed fresh start,

`KL(P_{v,h} || P_{v,0}) <= gamma^2 T / (4D)`.

Pinsker, data processing and the initialization/coding coupling yield for each action with a bounded `[0,1]` terminal reward:

`|E reward(v)|_actual - E reward(v)|_reference| <= eta`,

where `eta = min{1, rho + chi + gamma sqrt(T/(8D))}`.

Consequently `e(z) <= 2 eta` if the same bounds cover both actions. This statement holds for arbitrarily many upstream modes, even modes the experiment never samples. **But** `gamma`, `rho`, `chi` must come from a physically justified worst-case channel model, geometry and actuator/bath calibration; finite negative samples cannot certify a uniform bound on unobserved modes. If any unintended chemical or information path escapes the bounded-drift model, the theorem does not apply.

For context, a radius-0.75-um bead in water has a Stokes-Einstein diffusivity of roughly 0.29 um^2/s at room temperature. For `T=1s`, demanding a dynamical TV contribution below 0.02 requires `gamma<0.0305 um/s`, equivalent to a stray force below approximately `4.3e-4 pN` under Stokes drag. That is a demanding isolation specification, not a measured achievement. It illustrates why merely drawing two chambers on a diagram is insufficient.

## Finite assays, explicit statistical certificate and resources

Run `n_a` independent downstream reference trials using `a` and `n_b` using `b`. Let their binary success frequencies be `p_hat_a`, `p_hat_b`. With confidence at least `1-delta` (simultaneous Hoeffding), the physical-cut contrast is positive if

`p_hat_a-p_hat_b > sqrt[ln(4/delta)/(2n_a)] + sqrt[ln(4/delta)/(2n_b)] + eta_a + eta_b`.

Here `eta_a,eta_b` are **independently qualified** worst-case reference-to-actual arm errors. If both equal `eta`, the term is `2 eta`.

An **illustrative** numerical arithmetic check (`3100/5000` vs `2500/5000`, `delta=0.01`, each-arm `eta=0.02`) yields observed contrast `0.12`, simultaneous statistical error `0.048955`, physical error `0.04`, and positive conditional margin `0.031045`. No experimental data or physical isolation qualification have been supplied; this is a worked acceptance threshold, **not** a certified experiment.

Physical cost comparison is `C_total = (n_a+n_b)(C_fresh + C_assay + C_read) + C_cut_design + C_cut_qualification` plus `C_cut_run` for each real run and any upstream production cost. Time, energy, throughput, capital expense and irreversibility of replacement are not negligible. The cut is only useful if the downstream task can truly be executed from the transmitted `z` without consuming an irreplaceable upstream physical state.

## Task fidelity trade-off: cannot quietly claim this solves the original source

Let `g_v(h)` denote the *original* terminal action mean and `g_tilde_v(h)` the redesigned mean for each `v` in `{a,b}`. If the redesign preserves each original action with uniform error at most `kappa`, and its new action contrast is within `e` of a constant `d0`, then for all hidden states `h,h'`:

`|{g_a(h)-g_b(h)} - {g_a(h')-g_b(h')}| <= 4 kappa + 2 e`.

Proof: apply the triangle inequality through `g_tilde_a-g_tilde_b` at each end, then through `d0` between them. Therefore if the original contrast swings strongly across rare/common modes, **no small-error contrast-erasing interface can also preserve both original mode-conditioned action responses**. The cut changes the physical implementation; its justification must be that it still performs the *specified consequential task*, not that it computes the unmodified `E[p^(L-1)a]` more accurately.

A material synthesis route requiring the original molecule to pass through all stages cannot adopt a purely digital cut unless it actually resynthesizes a task-equivalent intermediate at the receiving stage. Such resynthesis/purification could be more expensive than studying the rare modes. An autonomous sequence of independent measurements, whose state is a digital experiment result, is a more natural early source.

This trade-off is closely related to classical task sufficiency, Blackwell information order and causal abstraction; it is not being presented as a newly proven general no-go theorem.

## Physical source selection: what has actually been demonstrated

1. **SmartTrap (Nature Methods 2026)** shows autonomous particle acquisition, three-dimensional tracking, force sensing, digital experiment-state tracking, programmable feedback and microfluidics. In its DNA-tweezer experiments, it flushes and replaces a particle after each run; parts and code are open-source with Zenodo materials. This establishes practical availability of **some components** of a fresh-carrier digital interface. It does **not** establish an isolated two-chamber task cut or uniform leakage/semantic-fidelity certificate.
2. **Tal-Friedman et al. (J. Phys. Chem. Lett. 2020)** physically implemented resettable colloidal diffusion using holographic optical tweezers and measured resetting energy costs. Reset is a real manipulation, and is not thermodynamically free. Restoring the *position* of one bead does not guarantee that every hidden property of that bead has been erased; particle replacement is a distinct, stronger operation.
3. **Balaban et al. (Science 2004)** and **Umetani et al. (2025)** give an alternative biological setting with pre-existing and heterogeneous persister modes. Cells cannot generally be swapped mid-treatment while preserving the same infection task. It is a stringent counter-test, not a qualified example of this cut.

Source links: https://doi.org/10.1038/s41592-026-03129-3 ; https://zenodo.org/records/18507341 ; https://doi.org/10.1021/acs.jpclett.0c02122 ; https://doi.org/10.1126/science.1099390 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12074638/ .

## Strongest ordinary competitor and selection verdict

**Same passive aggregate data:** exact milestoning, moment-Hausdorff bounds, task-focused finite mixtures and Bayesian extrapolation cannot uniformly resolve the established ε-rare indistinguishability, regardless of solver quality.

**Same force-biased data:** conventional equilibrium umbrella sampling and kinetic reweighting can exploit force-biased initialization if the source is equilibrated, the bias is a known Hamiltonian perturbation, and rare states overlap a force-coupled coordinate. For `H_F=H_0-Fz` and an *unbiased subsequent original* dynamics after bias quench,

`sign Delta_original = sign E_{pi_F}[ exp(-beta Fz) (R_a-R_b) ]`.

This exactly retains arbitrary hidden modes conditional on equilibrium and complete path execution. It is an established importance-sampling identity, not a discovery; the need to find and reach any rare mode invisible to `z`, equilibrate deep basins and bound finite-sample variance remains. Source references: https://doi.org/10.1073/pnas.2113533118 ; https://doi.org/10.1103/PhysRevE.109.024404 .

**Same redesigned source and qualified causal cut:** any competent conventional causal/experimental-design method immediately obtains the same one-stage decision factorization and can use sharper exact binomial intervals than Hoeffding. No estimator superiority is claimed. The research opportunity is to **physically compile a task-sufficient contrast isolator, with a qualified bound, at an acceptable performance/energy cost**, not to rebrand standard statistics.

## Decisive next physical experiment / earned and unpaid

**Testbed:** SmartTrap-style automated optical-tweezer microfluidics, two physically isolated sample paths controlled by a digital logic gate. Let the upstream particle have an unknown residence-time distribution and produce a certified binary completion event. Only that event is transmitted in a fixed format/time slot. A *new* downstream particle is then selected from a separate reservoir and undergoes randomized short terminal protocol `a` or `b`.

1. Acquire the *real* per-action downstream success counts and preparation costs. Replay with deliberately different upstream bead types, traps, dwell histories and heating/optical loads; search for leakage. Negative tests **do not** establish uniform leakage, but can falsify a proposed physical model.
2. Measure geometry, shielding, force-sensor linear range, thermal coupling, diffusion/drag and cross-channel actuation. Convert them into a conservative **all-upstream-state** drift bound; do not set unmeasured channels to zero. The 2026 open code may support control and logging, but would need adaptation.
3. Audit task equivalence: does the digital `z` carry all information needed for the real terminal goal? If the original goal requires continuing the same molecule, mark this interface **INVALID** rather than claiming it resets that molecule's rare modes.
4. Apply the conditional statistical certificate. Report total optical power, sample throughput, preparation, sample replacement, failure handling, capital expenditure and confidence, and compare to **the same instrument** using ordinary conditional trials and optimal experimental design.

**Current state:** theorem and fail-closed arithmetic implementation complete; instrumentation components from primary sources verified; **no actual dual-chamber experiment, source-derived worst-case leakage, or task-preserving reconstitution demonstrated**. No civilisational breakthrough earned. The higher-value question now is whether task-sufficient physical interfaces can be **automatically designed and physically certified** for useful chemical/biological operations without transmitting all latent microstates. That interface construction—not more synthetic Markov modes—is the research frontier.
