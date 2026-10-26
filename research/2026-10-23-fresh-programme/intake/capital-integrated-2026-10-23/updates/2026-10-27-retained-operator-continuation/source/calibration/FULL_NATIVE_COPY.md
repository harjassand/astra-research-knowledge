## ASTRA Pro3 — Self-calibrating experimental interfaces

The next construction removes a significant assumption from the previous single-port acquisition method: the strength of the experimental coupling no longer needs to be known in advance.

Suppose the instrument applies a nominal coupling \\(\lambda\\), but its actual strength is \\(\kappa\lambda\\), where \\(\kappa\\) is unknown and remains fixed across experiments.

For a hidden positive-definite response \\(T\\), the scalar reaction obeys

\\[ R\_\lambda(v)=R_0+ \frac{\kappa\lambda}{1+\kappa\lambda\\,v^\top T^{-1}v}. \\]

Rearranging gives

\\[ \boxed{ \frac{1}{R\_\lambda(v)-R_0} =v^\top T^{-1}v+\frac{1}{\kappa\lambda}. } \\]

This turns hardware calibration and scientific inference into one linear acquisition problem.

### Exact experimental requirement

For a hidden \\(r\\)-port symmetric response, let \\(d=r(r+1)/2\\) be the number of independent matrix coefficients.

| What is known before acquisition?   | Required scalar experiments |
| ----------------------------------- | --------------------------- |
| Coupling gain and baseline reaction | \\(d\\)                     |
| Baseline known, gain unknown        | \\(d+1\\)                   |
| Neither baseline nor gain known     | \\(d+2\\)                   |

The last two counts are both achievable and necessary for universal exact identification over an interior source class, including deterministic adaptive experiment selection.

I executed the constructions through actual synthetic boundary-reaction evaluations, not by supplying the hidden matrix to the learner.

| Hidden ports | Unknown gain, known baseline | Unknown gain and baseline |
| ------------ | ---------------------------- | ------------------------- |
| 2            | 4 calls                      | 5 calls                   |
| 3            | 7 calls                      | 8 calls                   |
| 5            | 16 calls                     | 17 calls                  |

All six exact-rational controls recovered the hidden response and instrument parameters. They also correctly predicted later, previously unspecified coupling configurations and a nonsymmetric-controller response with zero additional learner calls.

The gain must genuinely remain common across readings. The next tests examine what can still be learned without that calibration, and what fails when the instrument gain changes.

### A stronger result: some scientific questions need no gain calibration

The reciprocal observation has a nuisance parameter \\(h=1/\kappa\\). That nuisance cancels from appropriately designed signed measurements.

For a future linear scientific task \\(\operatorname{tr}(CH)\\), where \\(H=T^{-1}\\), the exact minimum number of scalar shunt measurements is

\\[ \boxed{ q^\*(C)= \begin{cases} 0,&C=0,\\\ \operatorname{rank}(C),&C\text{ is indefinite},\\\ \operatorname{rank}(C)+1,&C\ne0\text{ is semidefinite}. \end{cases}} \\]

This theorem assumes a known baseline, a stable unknown gain, freely selectable real probe amplitudes of norm at most one, and exact reactions. It includes deterministic adaptive procedures in its lower bound.

The distinction is meaningful: indefinite tasks contain positive and negative contributions that can be arranged to cancel calibration uncertainty. Nonzero semidefinite tasks cannot achieve that cancellation with only \\(\operatorname{rank}(C)\\) rank-one measurements.

Exact-rational controls passed for seven different task signatures, including full-rank four-port signed tasks. A two-reading procedure also recovered an off-diagonal hidden coupling while leaving the coupling gain unidentified.

With sensor error at most \\(10^{-3}\\), that two-reading procedure certified the previously unknown coupling inside

\\[ [-0.052901,\\,-0.049685], \\]

containing the exact test-source value \\(-4/79\\).

This is an example of operation-specific learning: identify only the physical information a future question requires, instead of paying to identify every source and instrument parameter.

### Jointly sharp predictions despite sensor noise

The noisy experiments produced a further result. After transforming each scalar reaction into a reciprocal interval, the learner retains a single feasible set of hidden matrices and common hardware gains.

In all three four-experiment controls, I verified that all 16 corners of the reciprocal-data box are physically admissible under the stipulated spectral and gain contracts. Convexity then proves that every intermediate point is admissible too.

Consequently, the 24 later scalar-reaction intervals generated in those controls are sharp: both ends are attainable by a source and instrument calibration compatible with all four historical readings.

The finite experiment-design comparison is:

| Calibration strengths       | Public certified error bound for \\(H\_{11}\\) | Mean later reaction-interval width |
| --------------------------- | ---------------------------------------------- | ---------------------------------- |
| 0.5 and 4 — selected        | 0.00373                                        | 0.00629                            |
| 0.25 and 4 — extreme range  | 0.00425                                        | 0.00724                            |
| 1 and 1.25 — closely spaced | 0.04034                                        | 0.01704                            |

The first design minimizes the specified public error upper bound among 120 allowed strength pairs. It is not claimed globally minimax over all continuous hardware settings.

The result also supplies a contract-falsification procedure: three strength measurements on the same configuration must follow an affine law after reciprocal transformation. A deliberately corrupted third-reading record was rejected with a certified incompatibility margin.

### Remaining obstruction: calibration drift

The strongest impossibility result concerns an instrument whose gain can change between configurations.

I constructed two different positive-definite hidden sources that produce identical scalar responses for every permitted experimental configuration, provided the gain is allowed to change within its declared range. No number of adaptive experiments can distinguish them under that observation contract.

A bounded temporal-drift assumption provides a partial repair. Reference calibration experiments at different times constrain the intervening gain.

In the executed control:

| Calibration reference times | Calls for calibration | Certified width for a later hidden coupling |
| --------------------------- | --------------------- | ------------------------------------------- |
| Beginning and end           | 2                     | 0.040                                       |
| Beginning, midpoint and end | 3                     | 0.010                                       |

One strategically placed calibration reading reduced uncertainty by 4×, without repeating the three scientific measurements.

An explicit indistinguishable-source pair also establishes a sharp error floor of 0.02 for the midpoint experiment when only the two endpoint calibrations are available.

### Hardware constraints matter

A final experiment restricted every coupling vector to unit Euclidean norm. The same four-call acquisition remained algebraically sufficient and its later reaction intervals remained sharp, but reduced excitation increased average uncertainty by 2.49× in the selected design.

Thus the compiler now distinguishes experimental identifiability, actual measurement precision, hardware calibration and intervention limits.

### Preserved research

Complete mathematical proofs and research findings

Exact theorems, gain-free task acquisition, joint noisy-source consistency, drift limits, counterexamples and scope.

Reproducible research bundle

Six executable investigations, actual results, independent verifier, clean replay and required source-code dependency.

All six research programmes and the independent verifier passed isolated, byte-identical replay. The archive's 19 files passed integrity and SHA-256 checks.

Scientific assessment: The strongest contribution is a self-calibrating experimental procedure that also recognizes when calibration can be avoided entirely for a scientific question. Its mathematical ingredients have established antecedents, and an equally informed classical system-identification algorithm can reproduce the results.

The next substantive frontier is joint source drift and instrument drift: distinguishing genuine changes in physical mechanisms from changes caused by the act of measuring them.

No physical apparatus or new law has yet been demonstrated. The research is preserved locally; the Astra GitHub repository was not modified.