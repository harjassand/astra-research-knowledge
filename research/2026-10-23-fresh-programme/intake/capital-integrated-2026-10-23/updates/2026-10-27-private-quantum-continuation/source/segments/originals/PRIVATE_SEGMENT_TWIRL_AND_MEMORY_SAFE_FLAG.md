# ASTRA — Private-segment fault paths and bath-speed-free coherent-check protection

**26 October 2026 · Pro1 interim scientific continuation.** This is a research derivation and reproducible finite-dimensional mathematical experiment. It is **not** a hardware measurement, demonstration of a new quantum device, or established claim of priority.

## Scientific decision

The preceding dual-rail encoded check-flag construction (source: `DECOHERENCE_FREE_COHERENT_CHECK_FLAG.md`, supplied in this conversation) is exactly immune to collective flag dephasing, but still requires bounded *differential* flag-bath disturbance across the long coherent check. Its aggregate error budget was `d + l^2/2`; the differential component `d` could be fatal and was not physically acquired from a short calibration. The strongest new attack is to act **during the complete untrusted interval**, not merely add later tests.

Two positive constructions were derived and executed:

1. A symmetric encoded swap-echo gives a **full-memory second-order amplitude error bound** under *local interaction-picture regularity*, without a norm bound on the bath Hamiltonian. It also protects an active conditional-`ZZ` control gate when paired with a target pulse.
2. A stronger alternative uses **fresh private encoded Pauli frames in each short physical interval**. For a flag-only error Hamiltonian of norm at most `v`, this yields an **exact positive Pauli fault-path decomposition** with total bad-path probability at most `v^2 T^2/N`, even for arbitrary bath bandwidth, persistent noncommuting memory, input–bath correlations, and arbitrary `H_0(t)` independent of the flag. One private bit per interval suffices for known `Z_F`-only coupling; two bits suffice for arbitrary three-axis flag coupling. This does **not** work if the key is reused or known to the device as an advance classical control.

A third, *different-scope* result holds during an **active gate**: use paired flag and target frames so that the ideal gate is unchanged. With suitable control-group covariance the completed **average channel** has half-diamond error at most `v^2 T^2/N`. This does **not** generally give an exact positive *ideal gate* Kraus branch. An explicit Choi-support obstruction distinguishes the two contracts.

These directions are not being represented as new dynamical decoupling or randomized compiling. Foundational prior work includes Viola–Knill (2005), Wallman–Emerson (2016), Winick et al. (2022), Uhrig–Lidar (2010), and recent non-Markovian twirling studies (2026). The programme-specific progress is exact scope, boundary assumptions and full-memory task integration, with executable counterexamples.

## 1. Physical interface and inherited capital

There is one *encoded flag qubit* `F` in the physical two-spin code `|0_F>=|01>, |1_F>=|10>`, one target register `D`, and an unrestricted quantum memory `M` that may be correlated with `D` and untouched references. The flag's logical operators are

```
X_F = (X_f X_g + Y_f Y_g)/2,
Z_F = (Z_f-Z_g)/2  (restricted to the code).
```

`X_F` is an encoded swap, `Z_F` a differential phase rotation. Collective flag `Z_f+Z_g` noise is zero on this code. The check uses physical controlled-`T` before and after a target–bath operation `K`, with `T=X_p X_q Z_a`, and accepts flag `|+_F>`. The ideal accepted Kraus map is `(K+TKT)/2` for each complete target–memory Kraus operator. An output pointer code projector and completed Bell/teleportation retirement from the governing work remain required; an initially out-of-code pointer is not repaired by this research.

**Trust boundary for the new theorem:** During intervals between the controlled-`T` gates, the ideal reference Hamiltonian `H_0(t)` acts on `D,M` but not on the encoded flag. An unwanted flag coupling `V(t)` is bounded by a supplied, physically justified **full operator norm** `||V(t)||<=v`. The bath Hamiltonian and its bandwidth are not bounded. The physical randomized Pauli frame is applied and inverted through *real encoded quantum controls*, not software tracking; its classical key is fresh and independent of the entire current bath, and inaccessible as advance classical information to the physical apparatus. Corrections and fine frame records are retired before the bath can act on them in later rounds. Calibrated port errors, leakage out of the flag code, and source/test role mismatch must be charged separately. A finite sequence of good test outcomes does **not** prove these assumptions.

## 2. Deterministic smooth-bath comparator: symmetric two-swap echo

Let, on the flag code, `H(t) = I_F ⊗ H_0(t)+Z_F ⊗ B(t)`. In the interaction picture of the entire intended `H_0`, write `B_I(t)`. Assume operator-norm differentiability with uniform

```
kappa = sup ||d B_I/dt||,
eta   = sup ||d² B_I/dt²||,
gamma = sup ||[B_I,d B_I/dt]||.
```

Two instantaneous `X_F` swaps per cycle, at times `tau/4` and `3tau/4`, produce the toggling pattern `y=+,-,+`. Let `T=N tau`. The joint-unitary error obeys

```
epsilon_echo <= (eta/24 + gamma/32) T^3/N^2
                 + kappa^2 T^4/(32 N^3).               (E1)
```

**Proof (per cycle, including the bath and all references).** Freeze `B_I` at the cycle midpoint `t_c` to `B_c`. The exactly solvable toggling propagator generated by `y(t) Z_F B_c` is `W_c(t)=exp[-i Z_F B_c F(t)]`, where `F(t)=integral_cycle_start^t y(s) ds`; `F(t_end)=0`. In this toggled frozen frame, the residual generator is `y W_c^† Z_F[B_I(t)-B_c]W_c`. Taylor expand about `t_c` with second derivative norm `eta`. Its quadratic remainder has integrated norm at most `eta tau^3/24`. The unconjugated linear term integrates to zero because `integral y(t)(t-t_c) dt=0`. Its conjugation error is bounded by `gamma * integral |t-t_c| |F(t)| dt = gamma tau^3/32`. Finally, the second-order unitary Dyson remainder for the residual has norm at most `(kappa tau^2/4)^2/2 = kappa² tau^4/32`. Unitary telescoping through `N` cycles proves (E1). No `||H_0||` appears; constant even very strong coupling `B` cancels exactly if its interaction-picture derivative vanishes.

The ordinary two-window Hahn echo has the weaker bound `kappa T²/(4N)` under the same assumptions. In one 8-dimensional full target–bath example with `T=1.45`, `N=64`, the respective observed complete operator errors were `0.0044301` and `0.0000239135`; the palindromic theorem's bound was `0.0000578837`. Fifteen independently generated noncommuting 8-dimensional models passed the same inequality. See `palindromic_full_memory.py` and its actual JSON result.

**During a gate:** When an actual closed-window Hamiltonian contains the intended `h Z_F Z_D`, the flag-only `X_F` echo also reverses and can destroy that gate. Instead pulse **both** `X_F` and `X_D`, which preserves `Z_F Z_D` but reverses differential `Z_F ⊗ B_M` noise. The same theorem then applies if other reference couplings commute with the paired pulse; pulse errors are separately charged. In a 16-dimensional encoded-flag–target–bath reference, at `N=16` and an irrelevant off-code Hamiltonian strength 240, the paired version's error was `0.00018743` below bound `0.00039991`, whereas flag-only echo had error `0.76554`. See `paired_pulse_protected_gate.py`.

**Non-smooth-bath failure:** The autonomous bath `H_M=Omega X`, differential coupling `g Z_F Z_M`, with `Omega=pi N/T`, resonates with the palindromic pulse periodicity. With `T=1,g=0.4`, the symmetry-odd erroneous-check acceptance effect approaches `0.063456` rather than decaying as `N` grows. This is a **family of time-independent** Hamiltonians whose frequency grows with `N`, not a single bath that adapts to the key; the regularity constants also grow with frequency. See `resonant_bath_no_go.py`.

## 3. Strongest result: independent private frame per short interval

### 3a. Exact CP fault paths for an arbitrary bounded flag coupling

At the *current complete flag–target–bath boundary*, during interval `j` of length `tau_j`, suppose

```
H_j(t)=I_F ⊗ H_0,j(t)+V_j(t),
V_j(t)=sum_{a=X,Y,Z} sigma_a^F ⊗ B_{a,j}(t),
||V_j(t)|| <= v_j.
```

All operators may act on a large noncommuting `D,M` joint space, except the factorized identity on the flag in `H_0`. `H_0` and `B_a` need no rate, dimension, stationarity, gap, memory or commutator bound. A finite Stinespring unitary can include unobserved ancillary degrees of freedom. For each `j`, *freshly and privately* draw uniform `P_j in {I,X,Y,Z}`, apply it physically before the call and its inverse afterward, then retire its record from all future-accessible system/control ports.

Expand the complete unitary of the physical call:

```
U_j = sum_{s=I,X,Y,Z} P_s^F ⊗ A_{s,j},
A_{s,j} = (1/2) Tr_F[(P_s^F ⊗ I) U_j].
```

Pauli character orthogonality proves the exact **whole-boundary channel equality**

```
(1/4) sum_P Ad_(P_F) o Ad_(U_j) o Ad_(P_F)
   = sum_s Ad_(P_s^F ⊗ A_{s,j}).                    (E2)
```

All four summands are CP and include the target, memory, future-accessible records and arbitrary reference entanglement. Their trace effects add to identity. The nonidentity aggregate fault effect is

```
W_j = sum_{s≠I} A_{s,j}^† A_{s,j} <= (v_j tau_j)^2 I. (E3)
```

**Proof of quantitative strength without bath bandwidth.** Let `U_0,j=I_F ⊗ U_{M,j}` be the propagator generated by the possibly extremely fast `H_0,j(t)`. Full-boundary unitary Duhamel gives `||U_j-U_0,j|| <= integral ||V_j(t)||dt <= v_j tau_j`. Pauli Parseval gives

```
(1/2) Tr_F[(U_j-U_0,j)^†(U_j-U_0,j)]
   = (A_I-U_M)^†(A_I-U_M) + W_j
   <= ||U_j-U_0,j||² I,
```

so (E3) follows. Crucially this bounds a *positive effect operator*, not a fictitious stochastic microscopic bath. Every actual current memory state and every previous refined positive path sees at most this fault probability. Distributivity of CP composition therefore yields

```
Pr(any internal flag-fault branch over N calls)
   <= sum_j (v_j tau_j)^2 .                         (E4)
```

For equal cells and uniform `v`: `<= v² T²/N`. The all-clean path acts as identity on the flag and allows the originally intended target–bath CP operation to proceed. Consequently an original coherent `T` checker filters symmetry-odd target errors **on that all-clean branch**, while every internal flag fault is conservatively classified bad. This does not claim the unknown target operation itself has been perfected.

For a *verified `Z_F`-only* interaction `V_j=Z_F B_j`, the same result needs only fresh one-bit frames `{I,X_F}` and has exactly two CP paths `I_F ⊗ A_j` and `Z_F ⊗ C_j`, where `A=(U_++U_-)/2`, `C=(U_+-U_-)/2`, `||C^†C||<=v²tau²`. There is no spectral smoothness requirement. A two-spin logical encoding supplies both `X_F` and `Z_F` physically under the governing native-style controls.

### 3b. Composable physical checker validation

The executable `private_frame_fault_paths.py` uses independent, strongly noncommuting target–bath Hamiltonians of norms **12,32,52,72** and preserves one bath across four calls. All **16** binary fault paths reproduce the complete four-round channel to operator residual `7.17e-16`; actual worst bad-path effect `0.01119`, upper `0.04016`.

`universal_private_frame_fault_paths.py` includes arbitrary logical `X,Y,Z` coupling, a noncommuting bath whose reference-Hamiltonian norms are **10,41,72,103**, and **256** complete four-round positive paths. The channel identity residual is `1.48e-15`; bad-path effect `0.02207` against bound `0.12694`.

`private_frame_completed_checker.py` inserts the physical `T`-sandwich, an intentionally symmetry-odd target operation, and a reused fast quantum bath. The complete **accepted** CP subinstrument reconstructed from fresh-key physical calls equals the sum of positive paths to residual `4.23e-19`. Its all-good accepted effect is zero within floating point (`4.88e-35`), while its actual bad accepted effect `0.00036075` is below uniform ceiling `0.142805`. An exact Heisenberg effect recursion at 128 calls verifies the same all-prefix-compatible effect structure while changing the bath frequency with call count.

### 3c. Tightness and real failures

The `1/N` order in (E4) cannot generally be improved using only `v`, `T`, fresh independent Pauli frames and that positive-path counting method. For a static scalar `V=v Z_F`, the exact virtual probability of at least one erroneous branch is

```
1-[cos²(vT/N)]^N ~ v²T²/N.
```

At `vT=0.845,N=64`, its actual value is `0.01109496`, within 0.56% of upper `0.01115664`. **Without** independent renewal, the coherent phase-error probability is `sin²(0.845)=0.55946`. This distinction is *not* about bath memory disappearing; it is about genuinely refreshing the **control key**.

Reusing the *same* private one-bit key for ten coherent `0.04`-radian calls produces `sin²(0.4)=0.15165`, whereas an invalidly assumed fresh-key count would charge only `10 sin²(0.04)=0.01599`. An externally leaked key is equally fatal: a device choosing its interaction sign conditioned on the current key makes the corrected unitary the same coherent `e^{-i0.04 Z_F}` each call, defeating the twirl completely. Both are executed algebraic witnesses.

A second independent no-go delimits the **noise algebra**. The one-bit encoded `X_F` echo cannot suppress an unwanted term `X_F⊗B`: it commutes with the swap control. In an explicit `T=Z_D` checker, a coherent `e^{-i theta X_F⊗Z_M}` passes the plus check with probability one, while applying `cos(theta)I-i sin(theta) Z_D Z_M` to the logical task. At `theta=pi/2`, it silently applies a *complete logical Z fault*. A full two-bit flag twirl handles all three flag axes, but only under a bounded full norm and trustworthy Pauli controls. See `logical_commutant_and_universal_dd.py`.

### 3d. Biased keys, key exposure and finite physical controls

Exact uniform key sampling cannot be silently replaced by approximate fairness. For independent, conditionally known probabilities `p_s`, put `r=4 min_s p_s` (two-key case: `r=2 min(p,1-p)`). The actual key mixture contains an **exact positive** uniformly twirled component of weight `r`; the remainder is a valid CPTP suboperation of weight `1-r`, conservatively marked faulty. Thus the current uniform fault-effect allowance becomes

```
q_j <= (1-r_j) + r_j (v_j tau_j)^2.                (E5)
```

If a separately justified *stochastic, physically identifiable* key-exposure component has weight at most `lambda_j`, its entire CP branch can also be marked faulty; with fixed `r,lambda`, a sufficient N-interval budget is

```
N [lambda+(1-lambda)(1-r)]
 + (1-lambda) r v² T²/N.                            (E6)
```

With `r=1`, the continuous optimum is `N≈vT/sqrt(lambda)`, minimum upper allowance `≈2vT sqrt(lambda)`. For `vT=.85, lambda=1e-4`, the integer optimum is **85** and the conservative bound **0.016999**. With key distribution `[.251,.249,.25,.25]`, `r=.996`, the optimal purely fault-count bound is **0.10735** at 13 cells: even modest key bias can overwhelm the quadratic suppression. Executed Choi positivity confirms the biased-key minorization in an arbitrary coherent target–bath channel.

An *unheralded coherent* frame-pulse implementation defect is **not** a stochastic event with rate `lambda`: it needs a complete-boundary channel comparison. If each physical randomized frame has half-diamond implementation deviation `delta_p`, telescoping across `m` implemented pulses pays at most `m delta_p` to an output-event probability, **not** an exact virtual fault count. Pulse finite duration, output key isolation, encoded preparation, and post-operation key retirement are physical resources. Consecutive ideal Pauli frames can be combined algebraically at boundaries, but this cannot substitute for actual physical frames when the intervening noise is unknown.

## 4. Active entangling gate: a related but strictly weaker theorem

During an intended `H_gate=h Z_F Z_D`, use the four *paired* frames

```
G={I_F I_D, X_F X_D, Y_F X_D, Z_F I_D}.
```

They commute with the intended `Z_F Z_D` generator. Suppose the complete reference `H_ref(t)` (which may contain a large, noncommuting bath Hamiltonian) commutes with every `g∈G`; and the unwanted `V(t)` has `||V||<=v` and `1/4 sum_g g^†V(t)g=0`. Conjugating the whole physical interval by a fresh `g` preserves the intended reference gate. Let `U_g` and `U_ref` be the corresponding full memory propagators.

In the interaction picture of `U_ref`, the first Dyson terms `D_g` in the *amplitude* average cancel exactly. Unitary Duhamel gives `||U_g-U_ref||<=v tau` and `||average_g(U_g-U_ref)||<=v²tau²/2`. Expanding the averaged quantum channel around `U_ref` therefore gives the **complete-boundary**

```
(1/2)|| average_g Ad_Ug - Ad_Uref ||_diamond
       <= v² tau², and over N equal cells <= v²T²/N.    (E7)
```

There is no bath-speed bound. The key must be fresh; paired target pulses, trusted physical framing and the exact gate covariance are required. The 8-dimensional target–bath simulation (`active_gate_private_frames.py`) has a bath frequency increasing with N; at 64 cells, completed-gate normalized Choi trace distance `0.001114` is below the half-diamond ceiling `0.009531`.

**Do not turn (E7) into an exact ideal-gate fault path.** A two-unitary Kraus-support counterexample takes `H_ref=h Z_F Z_D` and `V=g X_F`. After averaging sign frames, the two Kraus operators are

```
U_± = cos(r tau)I - i sin(r tau)(h Z_F Z_D ± g X_F)/r,
r=sqrt(h²+g²).
```

The intended ideal `U_ref=cos(h tau)I-i sin(h tau)Z_F Z_D` is generally not in the span of `U_+,U_-` (unless a special trigonometric equality happens to hold), so **no nonzero positive ideal-unitary CP subbranch exists**. At `h=.7,g=.45,tau=.38` the normalized Kraus-span projection residual is `0.0025856`. This is why randomized *active-gate channel integrity* and the exact *idle-flag positive fault count* are reported separately.

A strong conventional controller having the same Pauli controls, coupling bound and secret keys can perform (E1)–(E7). Nothing here establishes an exclusive Astra-specific advantage, nontrivial fault-tolerance threshold, indefinite renewability or hardware quantum capacity.

## 5. Comparison and next physical experiment

The practical hierarchy is now:

- For rigorously known **single-axis differential** flag noise with bounded interaction-picture commutators, the two-swap palindrome suppresses coherent amplitude at `O(N^-2)` with two swaps per cycle. With ideal gates, the inherited forbidden accepted effect is bounded by its **square**; include separately the `l²/2` amplitude penalty from off-code flag leakage.
- If bath frequency or noise axis is unknown but full flag coupling has a physical operator-norm bound `v`, use **fresh private Pauli frames**: one bit for `Z_F`-only, two bits for arbitrary in-code flag coupling. This gives exact positive fault paths at `O(v²T²/N)` and needs no bath model or spectral smoothness.
- During a necessary **active** controlled gate, compensate the target as well as the flag to preserve the intended coupling. Here only the robust *averaged complete-channel* error bound is general; an exact ideal-gate CP subbranch is obstructed.
- A key-conditioned apparatus, reused keys, strong errors in the Pauli-twirl commutant, code-space leakage and untrusted finite pulse widths defeat unsupported stronger claims.

**Next experiment of greatest leverage:** instrument and measure the *actual physical encoded Pauli pulses and their electromagnetic classical side channels* while the same bath-coupled service runs. Establish a complete-boundary bound for their failures plus fresh-key causal independence, not merely a standalone average gate fidelity. With those operations independently secured, a physically motivated rough norm bound on the unwanted flag coupling is enough to replace the earlier speculative bath-bandwidth requirement. Finite favorable observations cannot by themselves certify arbitrary future operator-norm bounds; the hidden-clock obstruction from the user-supplied governing work remains intact.

## Reproducibility, source scope and prior art

- `palindromic_full_memory.py`: 12 N choices + 15 random full-target–bath cases, all operator bounds checked.
- `resonant_bath_no_go.py`: autonomous fast-bath counterexample and static-coupling exact echo.
- `encoded_flag_complete_checker.py`: 36 complete physical two-spin encoded checker cases with off-code energies up to 210, leakage and physical pulse errors.
- `logical_commutant_and_universal_dd.py`: exact invisible fault, 4-frame deterministic universal comparator and physical pulse/toggling equivalence.
- `paired_pulse_protected_gate.py`: 18 full encoded-gate tests with strong off-code dynamics and a failed flag-only comparator.
- `private_frame_fault_paths.py`: full four-round CP equality, exact memory fault-effect bound, biased key leakage/reuse failures.
- `private_frame_completed_checker.py`: entire accepted-channel CP equality with a symmetry-odd target and an adaptive full-memory effect recursion to 128 intervals.
- `universal_private_frame_fault_paths.py`: four-axis path identities across all 256 length-four fault labels.
- `active_gate_private_frames.py`: full-memory corrected-gate Choi checks and Kraus-support no-go.
- `bias_and_resource_tradeoff.py`: exact biased-key CP minorization, tightness witness and integer cost optima.

The scripts have been executed, and each writes an actual `*_results.json`. The archive's `RUN_VALIDATIONS.sh`, `validation.log` and `SHA256SUMS.txt` preserve reproducibility and file integrity. No GitHub push has been made and no physical device was operated.

**Governing premises read:** user-supplied `ACQUIRED_TASK_INTEGRITY_WITH_QUANTUM_MEMORY`, `COMPOSED_POSITIVE_SERVICE_FAULTS`, latest `DECOHERENCE_FREE_COHERENT_CHECK_FLAG.md`, and Astra's N1004 task-first packet and its corresponding source. These premises remain *conditional*, not independently acquired hardware facts.

**Substantial prior science for scope and priority:**

- L. Viola and E. Knill, *Random Decoupling Schemes for Quantum Dynamical Control and Error Suppression*, Phys. Rev. Lett. **94**, 060502 (2005), https://doi.org/10.1103/PhysRevLett.94.060502.
- J. Wallman and J. Emerson, *Noise tailoring for scalable quantum computation via randomized compiling*, Phys. Rev. A **94**, 052325 (2016), https://doi.org/10.1103/PhysRevA.94.052325.
- A. Winick et al., *Concepts and conditions for error suppression through randomized compiling*, https://arxiv.org/abs/2212.07500 (2022/2023); non-Markovian noise and limitations.
- G. S. Uhrig and D. A. Lidar, *Rigorous Bounds for Optimal Dynamical Decoupling*, Phys. Rev. A **82**, 012301 (2010), https://doi.org/10.1103/PhysRevA.82.012301.
- J. Kattemölle, B. Gulácsi, G. Burkard, *Non-Markovianity induced by Pauli twirling*, npj Quantum Information **12**, 138 (2026), https://doi.org/10.1038/s41534-026-01345-5: twirling does not imply Markovianity of hidden memory.
- G. Paz-Silva et al., *Frame-Based Filter-Function Formalism for Quantum Characterization and Control*, PRX Quantum **2**, 030315 (2021), https://doi.org/10.1103/PRXQuantum.2.030315: independent frame-adapted noise-characterization methods.
