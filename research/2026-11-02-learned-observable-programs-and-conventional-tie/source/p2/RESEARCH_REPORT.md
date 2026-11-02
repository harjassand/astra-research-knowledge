# Acquiring executable observable calculi from finite experiments

**Research completed 2 November 2026.** This package is an independent construction and reproducible synthetic study. It earns a data-acquired, reusable observable-transforming program with a finite-data error certificate and genuinely held-out larger-system deployment. Its direct Fourier–Walsh retaining comparator matches and improves its error bound. **No historically new algorithmic learning principle or empirical physical instrument is claimed.**

## Precise result and scope

We implemented a local-experiment learner of a Boolean spin process on an arbitrary ring. The complete microscopic generator and true local rate formula are **not** visible to the fitting or execution programs. The admissible model class is **supplied**: each active spin has a single-site flip clock; the rate depends on its state and the states of its two nearest neighbours, with one of three physical mode settings. Every site carrying the same mode has the same local function; changing modes is assumed to introduce no cross-talk. These assumptions are strong, and the fourth-neighbour counterexample at the end proves why they cannot be inferred from the restricted experiments.

The learner's actual inputs consist of the eight requested configurations of three pinned spins, a known exposure `E=2,000,000` per configuration and mode, and noisy event counts `K ~ Pois(E c_mode(configuration))`. Only the fixed alphabet, three-site locality radius, controllable mode labels, preparation and the generic arithmetic/finite-program-search library are given. Not provided: the rate polynomial, its coefficients, a duality identity, a target-specific transition grammar or a known hidden state representation. The source fixture in `source_device.py` is **held by the experiment simulator**, not the code in `synthesize.py` or `independent_verify.py`.

The output is a frozen Python-executable local rewrite program, its per-mode finite-data residual bounds, retained measurement records, and a sign/kill interpretation. `execute.py` and `signed_execute.py` never consult true source rates. New time-varying, spatially heterogeneous open-loop mode schedules on 9, 2048, 4096, and 8192 sites were not passed to program synthesis. The `heldout_contract.json` and `signed_heldout_contract.json` files record the decision thresholds and case definitions, respectively. Full microscopic reference generators are computed **only** in evaluation at 9 sites.

This is a kinetic interacting-spin task relevant as a mathematical model of stochastic spin, catalytic-neighbour or information-propagation dynamics. It is **not** a calibrated magnetic material, physical reactor or validated experimental platform.

## 1. Actual acquisition and failure-driven search

The generic search considers simple local unary codes `d:{-1,+1}->{-1,0,+1}` and a generic multiplicative fold over arbitrary finite index sets. No spin-product duality function is supplied: it is one candidate among four invertible local codings. The task's ordinary single-spin probability is linearly expressible using any of them; the family also contains pair observables. For each code, the learner constructs the matrix of all `2^3` local basis evaluations and measures, via the acquired rate table, whether the resulting local observable transform can be represented by nonnegative stochastic rewrites with bounded cemetery rate. Occupancy codings fail this test through significant negative off-diagonal elements; `d(-1)=-1,d(+1)=+1` succeeds. This is selection from a **restricted factorized grammar**, not discovery from all possible programming languages.

With the selected code, define `D_S(s) = product_{i in S} s_i`. For each setting `m`, the generic search enumerates all seven nonempty three-site toggle masks `B`, computes their signed coefficients from local experiment records and greedily selects those reducing the worst-case finite-data residual, with a nonnegative termination/cemetery rate. Nothing like a predefined "repair at site 0" is included. In the first two modes, the observed progression is:

| Rules selected | Initial mode local residual bound | Interpretation |
|---:|---:|---|
| 0 | 0.7556 | No interaction rules |
| 1 | 0.3980 | One neighbour-current toggle |
| 2 | 0.0802 | Both oriented neighbour-current toggles |
| 3 | **0.010828** | Acquired neighbour-neighbour toggle, which can create two particles |

`frozen_programs.json` was hashed to `3581c7c1f8de3d8db9e11e634cc38c15b7f38a2574d0d3df8897f4becbdbde95` **before** the first held-out intervention stage. Its learned `baseline` rules were toggle offsets `[-1,0]` at 0.3600395, `[0,1]` at 0.3198725, `[-1,1]` at 0.06937325; the cemetery rate is 0.8503795. The second mode independently acquired an analogous three-rule program and its own residual certificate.

In a subsequent new **weak applied-field** mode, the old spin-product representation was retained, but its nonnegative-only rewrite proposal had a large mismatch. A *signed* extension enumerated the same seven generic local toggle words, admitted negative offdiagonal operators with a tracked sign and kept only trajectories whose absolute-rate cemetery quantity remained nonnegative. The returned fourth rule toggles only the centre and changes the sign of the estimator, at absolute rate `0.28038`. It is learned from the new eight measured Poisson cells. The signed residual fell `1.03595 -> 0.67991 -> 0.36025 -> 0.08060 -> 0.0107434` through four selected operations. The old program and its measured data were retained unchanged. `signed_frozen_v2.json` was hashed to `893cbb5ca0cf8790d5abb28ea54e5f2069a61534b4ecdc8372826fd04bf7be96` before the second held-out stage.

**Important comparator boundary:** The generic candidate grammar already contains factorized spin observables and XOR mask indexing. The learned content is the chosen encoding, which local words exist, their signs, parameters, stopping/viability certificate and useful cost. The method does **not** autonomously create its universal language operators from scratch.

## 2. Acquired local residual: finite experiments, not an inserted theorem premise

For mode m and local spin triplet `u=(s_{i-1},s_i,s_{i+1})`, count `K_{m,u}~Pois(E c_m(u))`. An explicit two-sided Poisson Bernstein event of probability at least `1-2 exp(-x)` is

```
K - E*c <= sqrt(2 E*c*x) + x,
E*c - K <= sqrt(2 E*c*x).
```

It implies the conservative *observed-count-dependent* rate interval

```
c in [ max(0, (K - sqrt(2 K x) - x)/E),
       (K + sqrt(2 K x) + 2 x)/E ].
```

`x=22` for all cells, so the 24 cells across original and extended modes have joint confidence at least `1 - 48 exp(-22) > 0.9999999866`. `synthesize.py` constructs conservative rational endpoints using an exact integer square root with upward rounding on a denominator `10^12`. `independent_verify.py` recomputes them from saved counts, with no simulator or true rate formulas. This is exact *arithmetic* for the local model class. The stated probability is a statistical theorem for ideal Poisson counts; producing the counts in this project uses NumPy PRNG, not a physical instrument.

The compiled program stores exact rational `a_m` and signed rule coefficients `q_{m,B}`. The rule set has a cemetery rate

```
k_m = 2*a_m - sum_B abs(q_{m,B}),  k_m >= 0.
```

The program executes a CTMC on *subsets* of lattice indices: for each active site i and toggle B, it makes `S -> S XOR (i+B)` at rate `abs(q_{m,B})`, multiplying a trajectory sign by `sign(q_{m,B})`. A cemetery event kills the estimator. All stored feature values satisfy `|D_S(s)|<=1`.

The original physical generator satisfies

```
L_m D_S(s) = -2 sum_{i in S} c_m(s_{i-1},s_i,s_{i+1}) D_S(s).
```

The proposed signed rule generator instead gives

```
Ghat_m D_S(s) = sum_{i in S} D_S(s) *
       (-2*a_m + sum_B q_{m,B} product_{j in B} s_{i+j}).
```

For a local triplet u, the **entire unknown-rate uncertainty** is in the one scalar `c_m(u)`. Thus the learned program's per-site residual is exactly bounded by

```
rho_m = max_u max_{c in [lo(m,u),hi(m,u)]}
        abs( -2*c + 2*a_m - sum_B q_{m,B} product_{j in B} u_j ).
```

This is a maximum of an affine function of `c`, so checking both rational interval endpoints for all eight u is **sufficient and exact**. There is no free model equivalence oracle or hidden generator inspection. Because external product factors have absolute value one,

```
sup_s abs(L D_S(s) - Ghat D_S(s)) <= sum_{i in S} rho_{m_i} <= rho*|S|.
```

The bound holds simultaneously for arbitrarily large rings, arbitrary subsets S and all spatial schedules of the **three calibrated modes** on the one joint confidence event. If physical locality/stationarity fails, it is not a valid guarantee.

Independent checked outputs:

| Mode | `rho_m`, exact-rational value displayed in decimal | Number of rewrite rules | Negative rules |
|---|---:|---:|---:|
| Baseline | 0.0108280417574 | 3 | 0 |
| Reduced noise | 0.0108081996260 | 3 | 0 |
| Weak applied field | 0.0107434090482 | 4 | 1 |

Deleting the third branching rule and falsely retaining its old claimed certificate is rejected by the independent local verifier.

## 3. Acquired execution-cost and global prediction-error certificate

Let `Y_t` be the learned signed/cemetery process on finite active index sets. The sign multiplier has modulus one. All retained rates obey a nonnegative cemetery intensity, so the program evaluation is bounded by one and does not require an uncharged exponentially growing importance weight.

A toggle of the two neighbours that does not include the current active centre can add at most two active indices; centre-neighbour toggles cannot add active sites. For each physical mode, the certified upper positive-count drift of one active particle is

```
b_m = sum_B abs(q_{m,B}) * max(0, |B| - 2*1_{centre in B}).
```

The cemetery process kills at an intensity `k_m` per active site, which decreases the count by at least one on any killing event. For `V(S)=|S|`,

```
Ghat V(S) <= -(k_m - b_m) |S|.
```

In particular the **acquired**, not inserted, uniform margin is

```
kappa = min_m (k_m - b_m) = 0.21142375 > 0.
```

Dynkin's inequality yields `E|Y_t| <= |S| exp(-kappa*t)` under arbitrary time/spatial switching among calibrated modes. With `rho = max_m rho_m`, a standard variation-of-constants argument for the physical and acquired semigroups yields

```
abs(E_physical[D_S(X_T)] - E_program[sign_T D_Y(X_0)])
       <= rho |S| (1-exp(-kappa*T))/kappa.
```

The actual estimate is automatically valid for multiple time blocks by executing the local program in **reverse order** of the physical controls. At `T=1.2` and a one-site query, it is about `0.01147634`. An independent exact-rational version uses the conservative inequality `exp(-v)<=1-v+v^2/2` to bound the time integral, returning `0.0114847462544`. These conclusions are conditional on the measured Poisson confidence event and the supplied three-local physics interface. No mixing gap or unknown growth coefficient is granted.

If `lambda_max = max_m(k_m+sum_B abs(q_mB))`, then the total *expected number of executed rewrite events per query trajectory* obeys

```
E[#events] <= |S| lambda_max (1-exp(-kappa*T))/kappa,
```

which equals `1.6961` or less for `|S|=1` and `T=1.2`. This bound is independent of lattice size, but physical control-map storage and reading the initial configuration/marginals still cost their actual size. The expected number of site scans is not identical to the event bound; the Python interpreter scans active sites on each event, and reports that cost separately. The worst-case trajectory can still be arbitrarily large because the process may branch: the guarantee is **expected** cost, not a deterministic per-run cap.

For a Monte Carlo prediction using `N` independent ideal signed paths, outputs are in `[-1,1]`, so

```
P(abs(MC_mean - E_program) > eta) <= 2 exp(-N eta^2/2).
```

The experiment preallocated total Monte Carlo failure probability at most `0.001` for each six-case stage. Across both stages, adding the finite-data event gives joint failure below `0.002000014`, under the ideal stochastic experiment/sampler assumptions. NumPy random-number quality, float arithmetic during simulated trajectories, real-device control/calibration, and a physical materials claim are **not** machine-certified by this calculation.

## 4. Frozen, genuinely held-out questions

The two source modes were frozen before any held-out schedules. The later signed field extension was frozen independently before the second set. Site counts 2048, 4096 and 8192 are not used in acquisition. Mode changes vary both in space and chronological order; the output of a single-site question is `(1+E[s_i(T)])/2`. These are meaningful *model-based* decisions, not real-world decisions.

**Stage I: original two-mode program.** Decision threshold for probability of spin + is 0.70.

| New question | Exact configuration count | Learned interval for P(spin +) | Certified side |
|---|---:|---:|---|
| n=2048, no control | 2^2048 | [0.60926, 0.62924] | below 0.70 |
| n=2048, new heterogeneous intervention schedule | 2^2048 | [0.71066, 0.73063] | above 0.70 |

Additional 9-site one-spin and two-spin observables were evaluated against a full `512`-state microscopic generator, with both predictions inside their declared model-plus-MC intervals. The `8192`-site pair-correlation task was predicted using the same frozen three-rule program; the reported interval for the parity correlation is `[0.17632, 0.24725]` (not a positivity event probability).

**Stage II: signed field extension.** Independent policy threshold for P(spin +) is 0.59.

| New question | Exact configuration count | Learned interval for P(spin +) | Certified side |
|---|---:|---:|---|
| n=4096, no field | 2^4096 | [0.60920, 0.62952] | above 0.59 |
| n=4096, new spatial/temporal field schedule | 2^4096 | [0.50586, 0.52618] | below 0.59 |

The nine-site full-generator signed reference gives `E[s_i(T)] = 0.0457632348` under field versus the learned signed estimate `0.041465`; this is within the submitted interval `[0.01299,0.06994]`. A new `8192`-site pair-correlation under mixed field/noise also runs with a properly charged signed estimator.

The large microscopic spaces were **not enumerated**, so these are analytic/simulation *within-model* certificates, not a measured full-state speedup or independently known true values.

## 5. Full resource accounting

| Item | Completed observed/declared cost |
|---|---|
| Three locally calibrated modes | 24 independent spin-triple configuration/exposure cells |
| Physical exposure in model units | **48,000,000** summed local site-time units |
| Events represented by simulator's Poisson reports | **34,395,129** (would require apparatus detection/reset costs in reality) |
| Initial two-mode search | 4 local site feature codings; all 7 candidate masks; 3 accepted per mode; 0/1/2-rule failures retained |
| Field extension | 7 masks examined, 4 accepted incl. 1 signed rule; retained old programs/records |
| Source uncertainty processing | Exact rational 24-cell Poisson interval construction and local endpoint checks |
| Actual stage I prediction simulation | 1,118,929 rewrite events across 6 holdouts; ~4.72 s local Python runtime |
| Actual stage II prediction simulation | 1,105,236 rewrite events across 6 holdouts; ~2.93 s local Python runtime |
| Combined learner future executions | 2,224,165 rewrite events in this recorded suite |
| Stored learned program JSON | 9,413 bytes original + 2,609 bytes field extension, plus measurements 1,895 + 835 bytes, before runtime metadata |
| Development, external experimental setup, maintenance and materials | **not measured**; not counted as zero |

The 24 scalar calls **do not** mean 24 cheap experiments; each call pays two million exposure units. The training fixture obtains Poisson aggregates without individually simulating 34 million events, which is efficient *simulation*, not actual physical preparation. Execution reports include stochastic events and active-set inspections, not just oracle calls.

## 6. Strong ordinary comparator: the central negative result

Both methods can retain **the complete same local-rate experiment table, all programs, calibration information, physical controls and knowledge of site locality**. The conventional method identifies the eight rates per mode and simply applies the full Boolean Fourier–Walsh transform. It needs no program search beyond eight coefficients and can instantiate all signed spin-parity rewrite operators directly. Its source calibration is exactly the same 48 million exposure units. It obtains a 7-rule program per mode instead of our 3- or 4-rule sparse one; it can also prune coefficients using the same task-specific bounds, so this smaller learned rule set is not necessarily an exclusive benefit.

Actual strongest-comparator calculations in `matched_comparison.py` are:

| Mode | Our local error `rho` | Conventional full-Walsh `rho` | Our retained rules / ordinary |
|---|---:|---:|---:|
| Baseline | 0.0108280 | **0.0099075** | 3 / 7 |
| Reduced noise | 0.0108082 | **0.0087197** | 3 / 7 |
| Weak field | 0.0107434 | **0.0105124** | 4 / 7 |

Both have the same **total per-active-site event intensity** (2a_m) because the conservative program's cemetery rate compensates for omitted small rules. The ordinary full-Walsh global bound for a one-site T=1.2 query is `0.0111658`, versus `0.0114763` for our learner. Ordinary symbolic expansion is also cheaper than our candidate-search computations. Neither has an extra oracle expense, and both can use the same signed-dual executor. No total-cost advantage against the strongest retaining ordinary approach survives this check.

Graphical backward constructions also exploit the locality of spin systems, and learned factorized dualities are well-established mathematical objects. Exact large-state enumeration is an intentionally weak strawman. Our method's exponentially smaller *representation* alone does not establish a new contribution beyond those.

This is the important scientific **selection correction**: the learned executable program is real, but the *full computational capability* is also available from existing symbolic machinery. Adopt that machinery rather than rebranding it.

## 7. Explicit negative regimes and impossibility

1. **Unwarranted locality cannot be learned from these probes.** Two models can agree under every admitted three-site calibration and differ by a fourth-neighbour rate term `h*(1-sigma[i+2])/2`. If calibration always has the fourth spin clamped +, their 24 Poisson laws are identical. In deployment with that spin -, the derivative of the observable `E[s_i]` for a currently positive central spin differs by exactly `-2h`. The program cannot certify its arbitrary-size projection from finite three-site experiments without an independent physical locality warrant or an expanded probing interface. The executable counterexample `assumption_attack.py` records this obstruction.
2. **Universal positivity is false and unnecessarily restrictive.** The observed field mode has a genuinely negative off-diagonal observable coefficient. A signed Markov path with a trackable sign still works because the **absolute** rule intensities leave a positive cemetery rate. A generic positive-rewrite-only learner rejects an otherwise useful programme.
3. **Signed weights can be intractable.** If `2a < sum_B |q_B|`, the nonnegative cemetery construction fails. A weighted Feynman–Kac representation may still be correct but can have exponential variance. This implementation rejects rather than hiding its unproven cost. Arbitrary local spin dynamics are **not** certified cheap.
4. **Hidden physical cross-talk or nonstationarity** defeats all held-out claims. The fact that control modes are compositional and local across system size is not certified by the reported noisy three-spin data.
5. **Long/highly branching trajectories** can make conservative bounds vacuous. This dataset benefits from a measured strict drift margin 0.2114, not a universal guarantee.
6. **No online feedback claim:** adapting a control to the unobserved microscopic history changes the source process. The certificates address open-loop schedules only.
7. **No broad novel library-learning result:** generic source->Walsh transformation and restricted factorized dualities are established. This study does not learn unrestricted new grammars, fundamental quasiparticles, tensor categories, integrable structures or new computation-complexity classes.

## 8. Where the foundational question actually remains

The construction settles a useful but restricted learning cycle: finite local observations -> acquired executable code -> sound all-size conditional residual -> fully paid held-out intervention predictions. The **next missing operation is not another fitted Fourier representation.** It is *learning a computationally efficient change of mathematical language which is not already derivable at lower cost from ordinary identification plus the available symbolic calculus*, and then earning transfer to new tasks with a local or otherwise affordable certificate.

A meaningful future challenge must make the best existing symbolic Fourier, graphical ancestry, tensor-network, probabilistic-program and library-learning systems first-class comparators. Promising targets involve truly **nonfactorized or nonlocal variable-size programs** or the **discovery of algebraic resummations** that change the execution complexity of meaningful rare-event/strongly-correlated observables. It is currently unresolved whether a finite-experiment learner can acquire those and justify their cost; this archive contains no such purported success. An equally informed conventional winner is a valuable stop signal, not a reason to inflate a narrower result.

## 9. Sources and precedents actually used

- Roy Glauber (1963), *Time-Dependent Statistics of the Ising Model*, J. Math. Phys. 4, 294, https://doi.org/10.1063/1.1703954; kinetic spin stochastic dynamics and correlation calculations.
- Redig & Sau (2018), *Factorized Duality, Stationary Product Measures and Generating Functions*, https://doi.org/10.1007/s10955-018-2090-1; explicit prior factorized duality classification.
- Redig & Sau (2018/2019), *Stochastic Duality and Eigenfunctions*, https://arxiv.org/abs/1805.01318 ; duality as an algebraic operator identity.
- Gupta, Ferrari & Iqbal (2025), *A Machine Learning Approach to Duality in Statistical Physics*, https://proceedings.mlr.press/v267/gupta25b.html ; machine-learning duality discovery in an **equilibrium lattice Hamiltonian** setting, not this exact stochastic algorithmic acquisition question.
- Ellis et al. (2021), *DreamCoder*, https://doi.org/10.1145/3453483.3454080; actual prior program-library learning.
- Bowers et al. (2023), *Top-Down Synthesis for Library Learning (Stitch)*, https://doi.org/10.1145/3571234; efficient precedent for program-library acquisition.
- Astra public archive, current relevant packets N1515/N1521 and U1321-backward-reset-ancestry-to-local-stationary-marginal: https://github.com/harjassand/astra-research-knowledge. N1515/N1521 already demonstrate stable scalar-return computations with conditional costs; U1321 has distinct known reset-driven quantum backward ancestry and no installed full native proof/implementation in that public card.
- Previous retained stochastic population-count compiler and quadratic certificate: sibling `producer-workspace/RESEARCH_REPORT.md`; it was not overwritten and is not included as a newly earned contribution here.

## 10. Reproduction

Required: Python 3.10+ with NumPy and SciPy. No external service or GPU. From this directory:

```bash
python train.py
python signed_extension.py
python independent_verify.py
python evaluate.py
python signed_evaluate.py
python matched_comparison.py
python assumption_attack.py
```

The two frozen source-code outputs and experiment fixtures have been reproduced in this session. Re-running training is deterministic with supplied seeds and the NumPy version; exact platform-independent RNG identity is **not** claimed. `independent_verify.py` reads stored experiments and frozen programs and uses exact rational integers; the local mathematical identities are independent of NumPy's synthetic physical source. Only `reference.py` and `signed_reference.py` import hidden fixture rates for small-state **evaluation**; the synthesizer and deployable interpreters do not.
