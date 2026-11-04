# A control-speed law for reading initially unencoded quantum systems

This result extends the inherited weak-control bound to **every fixed finite control/noise ratio at fixed interaction order**, including genuine measured classical feedback with per-record control budgets. It also supplies matching local readers for specified parity/GHZ promises and the joint peak/slew scales for polynomial specimen cost. Read the [complete proof report](package/Astra_Control_Speed_Law.pdf), [editable report](package/control_speed_law.tex), [detailed derivation](package/derivations/ALL_STRENGTH_ACCESS_PROOF.md) and [separate corrected collaborator proof check](package/derivations/independent_quantum_proof_check.md).

The package supplies completed internal collaborative mathematical proof checks and finite numerical diagnostics. Their actual scope is credited; Capital performs no new reproof or rerun. Experimental demonstration, historical priority and competitive hardware performance remain unestablished. A separate [finite-temperature effusion/intervention result](effusion-intervention.md) is independent of this quantum theorem.

## Exact access and full-feedback theorem

The unknown specimen starts **unencoded**, with arbitrary external reference, independently of apparatus and protected memory. It experiences actual independent inaccessible Markov `Z` noise `lambda sum_i(Ad_Zi-id)` from arrival. Every noncommuting source interaction is charged: `h_a=2||H_a||`, its source commutation support `B_a` has size at most `k`, and the **summed per-site term-norm budget** is at most `Omega(t)` in every classical record. Free maps must preserve each relevant Z-parity sector on the full retained instrument, including apparatus, records and flags. Uncharged branch information is not a free covariant operation. The original source is discarded at acquisition's end rather than declared a protected output.

Let `P_R=product_(i in R)(id-Ad_Zi)/2` and `A(t)=integral_0^t Omega(u)du`. The chronological full classical-feedback proof gives, for `k A(t)<=1`,

```text
||N P_R||_diamond <=
[exp(-2lambda t)+(1-exp(-2lambda t))(k A(t))^(1/k)]^|R|.
```

For constant positive peak `Omega`, choose `t=1/(2k Omega)` to obtain

```text
q_CQ=exp[-lambda/(k Omega)]
     +(1-exp[-lambda/(k Omega)]) 2^(-1/k) < 1,
||N P_R||_diamond <= q_CQ^|R|.
```

This is uniform in eventual acquisition time, arbitrary reference/protected quantum memory, collective processing, measured feedback and heralding when all consumed specimens are counted. There is no imposed initial noise layer or delay before finite-rate access. A random adaptive stop flag is handled within the classical record; data processing gives the acquired-output bound.

The proof represents hidden noise as independent rate-`2lambda` full-dephasing clocks. Every hit transverse site needs paid interaction before its first hidden deadline. Chronological Duhamel recursion removes all sites touched by the current insertion, and the branchwise weighted direct-sum norm is bounded before records are summed. This yields the support exponent without allowing a later support choice to select an earlier differentiated site.

### Stronger global budget is a different theorem

For an actual full-operator/global Hamiltonian decomposition, the decorated-trajectory proof gives fixed-history factor `A(t)^ceil(|S|/k)` for `A(t)<=1`, yielding the sharper constant `q_global=exp(-lambda/Omega)+(1-exp(-lambda/Omega))2^(-1/k)`. **Do not assign this sharper coefficient to branchwise-only classical budgets.** The preliminary extension had an unjustified future-dependent support-selection step; the supplied independent check documents that issue and verifies the separate chronological proof with its weaker constant. This is a proof limitation for the stronger constant, not a constructed counterexample to it. The final published statement retains the distinction.

## Copy lower bounds and matched fixed-order resource law

For known transverse Pauli `P` of weight `w`, states `(I+-aP)/2^n`, and decision error `zeta<1/2`, every allowed acquisition procedure needs `M>=(1-2zeta)q_CQ^-w/a` specimens. GHZ+ versus its diagonal mixture needs `M>=2(1-2zeta)q_CQ^-n`. This pair also gives a **worst-case universal purity lower bound** at additive accuracy below `1/4`; it is not a matching universal-purity acquisition algorithm or upper bound.

At fixed `k`, fixed promise contrast and `Omega/lambda>=1`, for the full-weight known parity or GHZ promise,

```text
log(1+M_opt)=Theta_k(1+n lambda/Omega).
```

Thus polynomial specimen cost has necessary and achievable peak scale of order `Omega/lambda >= n/log n`; bounded specimen count uses order `n`. The fixed-k constants and actual access premises remain. A sharp joint law for growing `k` is not established; the earlier weak-regime growing-k theorem can be stronger there.

## Matching reader, zero-start slew and paid execution

Ordinary parallel one-site protected meters with allowed interaction `H_i=(omega/2) X_i Y_meter` attain the order. Transfer satisfies `a'=omega b`, `b'=-omega a-2lambda b`. At constant `Omega>lambda`, `v=sqrt(Omega^2-lambda^2)`, duration `T=atan(v/lambda)/v` and visibility `beta=exp(-lambda T)` give a sufficient GHZ count `ceil(8 beta^(-2n) log(1/zeta))`. This is an ordinary permitted reader, not a separate quantum advantage claim.

A **zero-start** envelope `Omega(t)<=min(Omega,Kt)` imposed at **each specimen's arrival** adds necessary slew scale `K/lambda^2` of order `(n/log n)^2` for polynomial copies, or order `n^2` for bounded copies. Nonnegative area-`pi/2` triangular/trapezoidal pulses have `T=Theta(max(1/Omega,1/sqrt(K)))` and `beta>=1-2lambda T`, attaining the peak/slew orders in the corresponding regime. An already biased port does not satisfy the zero-start premise.

Each specimen consumes `n` protected meters, `n` pulses, `n` readouts and `O(n)` parity processing, with finite-slew aggregate charged action `n pi/2`. Specimen preparation/delivery, meter reset, calibration, storage duration, control implementation and readout remain paid. Charged norm/action is not a claimed thermodynamic dissipation law. Full local binary-POVM calibration uses six trusted Pauli eigenstates per site. At stated bias tolerance, reference use is `O(n^3 epsilon^-2 beta^(-2n) log(n/delta))`, polynomial in the polynomial-contrast regime. Calibration failure and discrimination share the error budget. These local probes do not certify cross-site independence, absence of common causes, Markovianity or stationarity.

## Supplied evidence and preserved scope

The [coverage program](package/checks/check_coverage.py) and [recorded checks](package/checks/coverage_checks.json) contain 120 selected-operator fixed-noise-trajectory tests and seven constant-pulse ODE checks. The maximum tested norm/bound ratio was `0.20881396899958496`. The [resource program](package/compute_resource_law.py), [recorded rows](package/resource_law.json) and [figure](package/resource_law.png) contain 33 resource rows and 18 finite-slew ODE tests: six triangles and twelve trapezoids. All eighteen satisfied the stated transfer bound; maximum pulse-area error was `4.45e-16` and maximum noiseless-transfer error `1.82e-13`. These are floating-point error-finding diagnostics, not general diamond-norm evaluations, exhaustive feedback/reference tests, formal certificates or physical measurements. The curves plot bounds, not exact optima.

Noise-sensitive learning with imposed layers, fault-path/local-norm techniques, Petz/reversal and ordinary local readers have relevant prior art, credited in the report. The result derives suppression during simultaneous finite-rate access under its actual hidden-noise/instrument contract. It does not assert zero channel capacity, prohibit protected quantum computing or rule out previously protected inputs or coherently accessible pure-environment export ports. Correlated/non-Markov noise, bath-changing control, microscopic realization, generic pure-port continuous-Hamiltonian recovery and universal-purity upper bounds remain outside the claim. The [prior weak-control result and companions](../2026-11-05-p1-experimental-access/README.md) and [pure-port many-body operation](../2026-11-05-p1-scalable-many-body-acquisition/README.md) retain their distinct premises.

[Original ZIP](original/Astra_Control_Speed_Research_Package.zip), [complete captured return](P3_INDEPENDENT_COMPARISON_20261105_RETURN.txt), [provenance and hashes](SOURCES.json). Generated current retrieval has not been rebuilt; this page and the complete supplied proofs are directly public on GitHub.
