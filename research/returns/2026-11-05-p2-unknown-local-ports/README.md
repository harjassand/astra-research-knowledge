# Rare-failure inference with unknown correlated local transitions

The supplied construction learns initially unknown transition support inside declared bounded-size reciprocal ports and propagates its finite local observation uncertainty into a relative interval for the full mean time to first failure. It combines prepared collision trials, an operational product-invariant refresh backbone, a global form bound and a succinct all-terminal network computation. Complete proofs are supplied in the [report](package/rare_failure_research.pdf), [editable report](package/rare_failure_research.tex), [theory supplement](package/theory_supplement.txt) and [physical supplement](package/physical_supplement.txt).

| Distinct operation | Direct route |
|---|---|
| Unknown-support acquisition, global uncertainty and fixed-start computation | This page |
| Finite reciprocal collisions, clocks and verified ancillary factories | [Physical interface and error theorem](physical-interface.md) |
| Deliberately prepared equilibrium-safe start | [Separate corollary and initial-write costs](equilibrium-safe-start.md) |
| Original evidence | [ZIP](original/rare_failure_research_package.zip), [complete captured return](P2_STEERING_COMPARISON_20261105_RETURN.txt), [provenance and hashes](SOURCES.json) |

The package reports a completed in-session mathematical construction with independently developed and checked arguments by three collaborators. Its proof supplements and actual reported checking scope are retained. Capital performs no new scientific audit or rerun. The synthetic examples are not physical measurements; historical priority, a practical advantage and a civilisation-changing physical capability are not established.

## Earned model and observation operation

A register has `m` binary occupation/failure bits, a known failure rule and a constructed or independently calibrated **product invariant law** `pi`. Product equilibrium does not mean independent dynamics. A native independent refresh backbone with positive rates `gamma_i` remains active during operation. Each additional unknown port acts only on its declared block of at most `k` bits, without outside-state dependence, with fresh ancillas and reciprocal amplitudes. The set of positive transitions inside each block is not assumed known. The polynomial computation specializes to connected undirected all-terminal graph disconnection; the form/perturbation machinery has the broader stated predicate scope.

Prepare every local input, remove preparation controls, isolate and execute one actual operating port collision, dephase and read its output. Preparation stress left on during the pulse would change the measured kernel. Measure each unordered transition pair from its lower stationary-weight endpoint, and infer the other direction by detailed balance. All microscopic paths between the same endpoints are aggregated. Input writes, fresh ancillas, isolation, service duration and readout accuracy are resources.

For fixed `n_alpha` shots per local input, `J=sum_alpha binom(2^|S_alpha|,2)` oriented pairs and `L=log(3J/alpha_acq)`, probability intervals use half-width `sqrt(L/(2n_alpha))`; zero counts also admit the upper bound `L/n_alpha`. Retain a **positive upper interval for every unobserved channel**. A union bound gives simultaneous coverage at least `1-alpha_acq`, despite multinomial dependence within a row. Input/output contamination, attempt-rate uncertainty and finite-factory bias enlarge these bands; sampling confidence does not remove systematic bias. Fixed shot counts are assumed; adaptive sampling needs a valid confidence sequence or allocated stages.

Common absolute probability accuracy `h` costs `O(number_of_ports * 2^k * h^-2 * log(number_of_ports * 4^k/alpha_acq))` physical trials. There is no inverse uphill transition probability in that count, but every prepared local input and complete collision service is paid. Fitted off-diagonal rates form a reversible generator; row reconstruction can exceed an original stochastic row cap, requiring either enforced constraints or an enlarged computational uniformization bound.

## Unknown-support global certificate

Absolute local rate errors define reversible error envelopes `H_alpha`; let `r_alpha` be each envelope's maximum exit rate. For every full-register function `f`, simultaneously,

```text
|E_true(f,f)-E_fit(f,f)| <= rho E_backbone(f,f),
rho=max_i [2 sum_(alpha containing i) r_alpha/gamma_i].
```

A uniform downhill rate radius `delta_alpha` gives `r_alpha <= (2^|S_alpha|-1)delta_alpha`. The proof bounds each local error form by `2r_alpha Var_block` and uses conditional product-variance tensorization. It does not require identical extra transition support, a lower bound on every unknown positive channel or an observed rare forward event. The backbone supplies the coercivity; installing it only for calibration does not justify an operating lifetime prediction.

For `rho<1`, killed conductance forms have the corresponding Loewner sandwich. A specified-start mean is a bilinear inverse, so a separate condition factor is paid:

```text
M_x=e_x^T L^-1 pi_A,
|M_true/M_fit-1| <= [rho/(1-rho)] B_x.
```

For fitted starting mass `pi(x)>=kappa`, a full gap lower bound `gamma`, lazy uniformization rate `R`, and `g=gamma/R`, the proved general bound is `B_x<=4/(sqrt(g)kappa)`. In the certified rare regime `lambda_killed/gamma<=kappa/16`, it improves to `2/sqrt(kappa)`. The improved rare bound is not silently used at arbitrary parameters. Product-weight and backbone calibration have a separate proved envelope: with total log-weight error `Delta` and log-refresh error `b`, the form radius is `eta=Delta+b-log(1-rho)`. For a proved fitted factor `C` and `u=C(exp(eta)-1)<1`, the mean lies between `exp(-Delta)(1-u)M_fit` and `exp(Delta)(1+u)M_fit`. This is a mean-time statement, not a relative guarantee for every deadline CDF.

## Computation without lifetime-scale trajectories

For rational local tables and product probabilities on the known all-terminal network, the constructed confidence interval has endpoint ratio at most `1+epsilon` and work polynomial in graph size, table/input bit length, `2^k`, local incidence degree, `g^-1`, `kappa^-1`, `epsilon^-1` and log inverse confidence. Actual numerical gap/starting-mass dependence is charged. This extends the [earlier independent-network result](../2026-11-05-p2-first-failure/README.md) to correlated product-invariant kinetics.

Karger's corrected static all-terminal unreliability FPRAS supplies `p=pi(B)`. Sequential edge contraction/deletion and allocated counting tolerances construct an approximate `pi(.|B)` sampler with at most `2m` static calls per draw. This is a computational sampler, not a physical ability to prepare a rare failed configuration. The generic Karger component is invoked published machinery and **is not implemented by the supplied diagnostic code**.

Short reverse trials start in that conditional law and return `Z=1` only if all subsequent window updates are safe. Reversibility gives `D_l=p E[Z]` as a positive first-entry spectral quantity. The supplied rare gate and logarithmic gap-scale window ensure `(1-2xi)lambda <= D_l <= (1+xi)lambda`, `E[Z]>=g(1-2xi)`, and `1-3xi<=M_*D_l<=1+3xi` in uniformized units. Thus a static rare factor multiplies an inverse-polynomial-probability sampled event. Conditional-sampler bias and all counting/trial confidence are allocated. A new spectral starting-state correction handles the loss of monotone coupling. The nonrare branch has an explicit capped direct-simulation work bound; no late-time plateau is presumed. Local table updates and connectivity tests remain real work.

## Supplied numerical evidence and comparators

The [original program](package/rare_failure_experiment.py) and [recorded counts/results](package/results.json) contain two small synthetic examples. Counts were drawn directly with NumPy multinomial sampling: **4,000,000 and 256,000,000 are represented collision sample sizes**, not individually executed trajectories or laboratory shots. Mean solves use 90- and 125-digit Decimal arithmetic. High-precision agreement and rounding safeguards are diagnostics, not machine-checked directed arithmetic.

| Model | True model mean | Supplied 99% ideal interval | Independent-only overestimate |
|---|---:|---:|---:|
| Two redundant bits with unknown cooperative port | `3.0223145490e23` | `[2.9261012e23,3.1177482e23]` | `2` |
| K4, four overlapping three-bit star ports | `5.7646157694e16` | `[5.6122300e16,5.9168462e16]` | `1.6666650772` |

Both examples observed zero forward cooperative events yet retained uncertainty over every admitted local pair. Each ideal example has 99% simultaneous coverage, at least 98% jointly by union bound. These are native-refresh model time units, not predictions in laboratory seconds. Finite-factory, clock and hardware errors are omitted from these ideal synthetic intervals and must be added for a physical implementation. [Recorded figure](package/intervention_results.png), [smaller physical-collision example](package/physical_collision_example.py).

An ordinary exact small-state solver is the better computation for these examples. Reverse-kinetics inference, temperature-accelerated dynamics, reciprocal collision models, form comparison, tree/forest formulas and Karger counting are prior machinery. The candidate increment is their complete finite observation/control interface and zero-support-tolerant global risk calculation, not a demonstrated computational or device advantage over every ordinary method.

Undeclared baths, larger ports, common causes, leakage, ageing, long-lived memory and systematic sensor floors remain outside the constructed class. Silence does not exclude an independent catastrophe clock. Physical failure is defined at registered classical endpoints: this construction does not certify safety during an unobserved coherent pulse. The [physical result](physical-interface.md) pays the full clock and verified-factory costs; the [equilibrium-safe corollary](equilibrium-safe-start.md) changes the initial law explicitly. Generated current retrieval has not been rebuilt for this return; the proofs and entries are directly public on GitHub.
