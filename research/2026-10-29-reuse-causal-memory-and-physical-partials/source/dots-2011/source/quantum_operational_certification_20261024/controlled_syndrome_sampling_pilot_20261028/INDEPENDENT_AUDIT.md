# Independent audit: sampled controlled-syndrome calibration pilot

28 October 2026. Reviewer `producer-workspace/review_repeated_service_factorization`.

**PASS as a reproducible floating sampled-calibration pilot, not a certified acquisition theorem or hardware result.** All 512 saved banks reproduce exactly from their declared seeds using independently constructed Born probabilities. All 1,024 decoder evaluations reproduce within 4.6e-15. Author scripts, raw counts and result files were preserved; no author helper code was imported or executed by the reviewer.

## 1. What was actually simulated

The fixed source is the three-qubit repetition/syndrome subsystem followed by one dense, fixed unitary V. With representatives `e_g in {000,100,010,001}`,

`U|l,g> = V |e_g xor (111 l)>`.

The native preparation uses g=0. Active calibration first encodes the logical X± or Z± input and injects the chosen representative bit flip **before** the native independent physical bit flips and before V. Each of the three physical error bits is Bernoulli(p). Each call then selects a uniformly random product-Pauli setting and samples an actual output outcome from its eight-outcome Born distribution.

This is genuine per-call pseudorandom sampling, vectorized for computation—not a population-mean substitution or a direct draw of aggregate estimator statistics. The simulation includes random input axis, sign, active injection label when applicable, three error bits, measurement setting and measurement outcome for every call. The saved count tensor retains the learner-visible axis/sign/injection/measurement labels; it does **not** expose the sampled error pattern to the learner.

The calibration records are sampled. The subsequent performance scores are deterministic full-matrix evaluations of the learned receiver on the known simulated source, not additional sampled payload trials. V and p enter generation and posthoc scoring only. The estimator functions use the saved actual counts and known control labels.

One source V is reused throughout. The independently sampled banks are not independent draws of different sources, and the pilot does not establish behavior over an ensemble of unknown encodings.

## 2. Exact bank and replay accounting

| Dataset | Independent banks | Sampled calibration calls | Decoder evaluations |
|---|---:|---:|---:|
| Main, N=512/2,048/8,192 | 384 | 1,376,256 | 768 |
| Larger, N=65,536/262,144 | 128 | 20,971,520 | 256 |
| Total | **512** | **22,347,776** | **1,024** |

The main experiment has sixteen banks per `(p,N,active)` condition; the larger continuation has eight. All 512 bank seeds are distinct. The three active estimators share each active bank. Native banks are separate, and banks at different N are independent rather than nested prefixes. Therefore 1,024 receiver evaluations must not be described as 1,024 independent acquisition trials.

`independent_audit_check.py` independently rebuilds the encoding/injection/error maps and product measurement vectors, then replays the declared RNG call order. Every saved count tensor matches exactly. Count sums equal N, native banks have zero injected-label counts outside g=0, the stated total calls and evaluations match, and all stored summaries recompute from the individual records. Both stored source-V matrices agree and reproduce the declared source seed.

The reviewer replayed the same 22,347,776 call records. Those are **not new independent banks** and must not be added to the original sample size. No physical source or hardware was accessed.

## 3. Born law and actual one-copy shadow estimator

The independently checked physical state is

`V X_error X_injection V_repetition |input>`.

All product-basis Born distributions normalize. Averaging the local product shadow `tensor_j(3|b_j><b_j|-I)` over the actual settings/outcomes reproduces every one of the 128 underlying input/injection/error states, with maximum floating residual 7.8e-16.

The fitted axis matrix has factor 2/N because the requested X or Z input axis occurs with probability one half. Signs and injection weights then multiply the actual observed shadows. No separate incompatible measurement is presumed for each logical statistic; all active estimators recompute from the same measured bank.

The input-sign probability is already part of the signed contrast. The code does not confuse that contrast with a normalized conditional state, and does not use the hidden error labels or true V to orient its fitted reflections.

## 4. Population laws and why label-aware active baselines matter

Put `c=1-2p`, `Zsum=Z1+Z2+Z3` and `Zprod=Z1 Z2 Z3`, in the known pre-V physical basis. Directly summing the actual generation law gives the active population matrices

* X contrast: `V XXX V† /8`;
* unlabelled Z contrast: `V(c Zsum-c^3 Zprod)V† /16`;
* injection-sum-weighted Z contrast: `V(c Zsum)V† /8`;
* separately label-weighted site i: `V(c Zi)V† /8`.

These identities were independently evaluated at all four p values; maximum residual was below 2.0e-16. For p<1/2, their noiseless matrix-sign directions recover the corresponding true reflections. The third estimator signs each individual Zi estimate, sums those three learned reflections, then signs their sum. In the population limit that gives the logical majority-Z reflection. At finite counts the three estimated reflections need not commute, but signing their Hermitian sum still defines a reflection.

The label-sum and label-triple procedures are ordinary label-aware estimators using information already present in active records. The unlabelled active estimator is not the strongest equally informed comparator by itself. The pilot correctly includes both label-aware alternatives without acquiring additional banks for them. Nothing here compares against every possible conventional estimator or a fully optimized measured-data decoder.

For the native bank, the population X and Z matrices instead contain the occupied syndrome weights `gI+gX` and `gI-gX`. At p=0 only one gauge sector is populated: strong recovery on that occupied sector does not identify the other gauges. At small positive p, rare sectors can remain poorly estimated. Active injection populates all sectors, while at p=.4 the Z signals are weak and extra estimation variance can outweigh that coverage benefit. The data show precisely these tradeoffs, not a universal improvement.

## 5. The learned receiver is a coherent physical reference architecture

For any Hermitian involutions Sx,Sz, the code constructs

`Cz = ((I+Sz)/2) tensor I + ((I-Sz)/2) tensor X`,

`Cx = I tensor |0><0| + Sx tensor |1><1|`,

and uses `W=Cz Cx Cz`. Each factor is unitary without requiring the two estimated reflections to anticommute. The ancilla starts in I/2; after W, all three original physical qubits are discarded and the ancilla is the recovered qubit. Thus the exact-reference prescription is CPTP even on poor fits. With the true logical Pauli pair, this is the familiar three-controlled-reflection logical SWAP and yields exact extraction for every gauge.

The independent audit constructs the entire 16-dimensional circuit and evaluates its Bell projections directly rather than importing the author's decoder-Kraus/effect helper. It verifies the true-frame T0=I test, every learned effect POVM normalization, positivity and the receiver unitary. Maximum observed normalization and unitarity residuals are 4.3e-15 and 4.7e-15, respectively.

These are floating spectral-sign and matrix-circuit diagnostics. A dense learned three-qubit reflection and its controlled implementation are not free local pulses. The pilot does not execute a finite rational Jacobi routine, synthesize these controlled gates, validate mixed-ancilla preparation, or deploy hardware. It supports the mathematical reference architecture and numerical performance calculation, not a certified finite implementation tolerance.

## 6. Native-source oracle versus all-gauge extraction score

For the native g=0 source, write

`gI_g = p^wt(e_g)(1-p)^(3-wt(e_g))`,

`gX_g = p^(3-wt(e_g))(1-p)^wt(e_g)`.

Every tested p is at most 1/2, so `gI_g>=gX_g` for each syndrome. The full-CPTP Bell-fidelity optimum is therefore the true logical extraction: positive Pauli-resolved decoder effects cannot beat the larger I weight in any gauge sector, and true extraction attains the sum of those weights. Its native loss is

`sum_g gX_g = 3p^2-2p^3`.

This is the appropriate **same native source** informed oracle, not zero error and not the actively injected training mixture. The learned native fidelity is exactly

`sum_g [gI_g (T0)_gg + gX_g (TX)_gg]`.

An independent calculation passes each of the eight physical error patterns through the full recovered Bell circuit before any syndrome decomposition. It agrees with that formula within 6.7e-16 across all evaluations. Every reported native excess is reproduced and is nonnegative to the stated floating tolerance.

The different diagnostic

`b = 1-lambda_min(T0)`

is the worst virtual extraction loss over **all** gauge densities, including coherent gauge states. Computing the full T0, rather than its diagonal, is essential. This score is a posthoc property of the learned receiver relative to the true U. It is not the native source loss, not its excess over the native oracle, and not a confidence-certified number available to the learner. No unseen future-memory experiment was sampled; the interpretation is state-uniform virtual extraction under the same U, not empirical validation of arbitrary future source drift.

## 7. Preserved findings and failures

The table gives means at N=262,144, eight independent banks per protocol. These are descriptive simulation means, not simultaneous confidence certificates.

| p | Method | Native excess | Worst-gauge virtual loss |
|---:|---|---:|---:|
| 0 | Native unlabelled | 0.000728 | 0.887902 |
| 0 | Active unlabelled | 0.002942 | 0.006107 |
| 0 | Active label triple | 0.002308 | 0.006484 |
| .01 | Native unlabelled | 0.016081 | 0.761094 |
| .01 | Active unlabelled | 0.004202 | 0.006836 |
| .01 | Active label triple | 0.002896 | 0.006235 |
| .1 | Native unlabelled | 0.007899 | 0.055048 |
| .1 | Active unlabelled | 0.004876 | 0.009767 |
| .1 | Active label triple | 0.003461 | 0.009513 |
| .4 | Native unlabelled | 0.013563 | 0.073660 |
| .4 | Active unlabelled | 0.047745 | 0.223006 |
| .4 | Active label triple | 0.023161 | 0.119347 |

The tradeoffs must remain visible:

* At p=0 active coverage dramatically improves the future-uniform extraction score but **worsens current native excess**. At N=8,192, for example, native excess is .02282 versus .09078 for active triple, while their worst-gauge scores are .90034 versus .21915.
* At p=.01 and the largest budget, active triple improves both displayed scores compared with the separately sampled native baseline. This is a result for this source and these controls, not a general active-learning guarantee.
* At p=.4 even active triple remains **worse than native** in both displayed means. It improves on active-unlabelled, not on every protocol.
* Among active estimators, triple does not uniformly beat unlabelled in worst-gauge mean. At p=0 its score is slightly higher; the paired mean difference is .000377 with descriptive standard error .000633. At p=.1 the small worst-gauge difference is likewise not resolved by these eight banks.
* Some small-budget runs perform poorly: the main pilot includes native excess as large as .87201 and worst-gauge loss as large as .97591. No favorable runs or failed fits were removed. These budgets do not constitute certified acceptance.

The audit JSON includes every reported summary with a standard error across independent banks. Active-method differences use **paired** within-bank standard errors. Active-versus-native differences use the variance sum for separate independent banks. It does not turn 1,024 correlated estimator evaluations into extra sample size, attach unsupported p-values, or claim a multiple-comparison guarantee.

## 8. Resource fairness and limits

Active calibration is not free under the native interface. It requires an additional controllable **PRE-noise syndrome-injection port**, a fresh two-bit choice among the four labels, and the corresponding known physical flip (identity or one physical X in this example). The logical preparation/encoding, three physical noisy qubits, local readout settings and all classical storage also remain resources. That port is more than downstream measurement access and is not supplied merely by knowing that a subsystem exists.

The native-only baseline and active protocols therefore differ in physical access. Their comparison diagnoses the value and cost of that extra exploration interface; it is not an information/resource-equal quantum advantage claim. The active label-aware estimators receive the same control labels and counts as active-unlabelled. The native full-CPTP oracle is stronger in source information but is a performance benchmark, not a proposed finite-data learner with artificially restricted labels.

The pilot samples stationary independent physical bit flips, not retained coherent noise memory. Its all-gauge effect diagnostic may be relevant to separately proved uniform-memory transfer theorems, but the pilot itself does not test arbitrary coherent retained-memory dynamics, model membership, source persistence, key retirement or calibration-to-service implementation errors.

## 9. Receiving conclusion and reproducibility scope

All six author input files were hash-frozen before replay and checked unchanged afterward. The saved artifacts include independent replay code/log/results, descriptive paired statistics and a hash-bound receipt. Exact count reproduction holds in this recorded numerical environment; cross-platform bit-for-bit floating linear algebra is not asserted.

Accepted evidence: actual sampled ordinary calibration laws; declared bank/call counts; same-bank estimator reuse; the learned three-controlled-reflection mixed-ancilla reference receiver; correct native oracle and all-gauge scoring; numerical reproduction; and the stated finite-source tradeoffs. Not accepted or claimed: a finite-Jacobi/gate-synthesis certificate, hardware execution, statistical acceptance theorem at these N, universal advantage, generic unknown-noise acquisition, or source-ensemble generalization. No substantive numerical or comparator error was found within this scope.
