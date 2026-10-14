# Adversarial boundary: local response needs remote precision

15 October 2026, Brisbane. Independent adversarial investigation as instructed in `BRIEF.txt`; isolation from other workers was instructed, not technically enforced. No other current worker report was consulted. **Capability status: NOT ACHIEVED.** The new result here is a self-contained counterfamily and an access-model lower bound, not a winning physical or computational operation. Originality of the counterfamily is **UNKNOWN** pending a dedicated literature review.

## Scientific output and exact interface

The consequential target is a *certified, material-specific zero-temperature local static response* near a small excitation scale, enough to distinguish a factor-two difference (say a ±20% response interval). Such a response is the curvature of ground energy under a local field and can inform field-tuned quantum critical physics. This relevance is supported by the primary quantum-critical susceptibility analysis of [Fischer and Rosch, Phys. Rev. B 71, 184429 (2005)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.71.184429). Our exact models below are engineered spin chains, **not** acquired materials or evidence of a new quantum-critical experiment. We do not assert that current methods cannot measure susceptibility in actual materials: [experimental susceptibility at a field-tuned transition](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.094413) already exists. The missing output is a *rigorous local zero-temperature interval from an uncertain microscopic input* at an independently demonstrated useful cost.

For a positive local Hamiltonian `H` with unique normalized ground vector `psi`, and local Hermitian `V` with zero ground expectation, the convention is `b=V psi`, `chi=<b,H^+ b>`, and ground-energy second derivative `E''(0)=-2 chi` for `H+lambda V`. Two input models matter:

1. **Exact symbolic rows supplied:** coefficients of all local terms and the ground state are exact. A conventional solver may inspect every row and use any exact algebra.
2. **Unknown physical generator acquired only through controlled evolution:** all known controls, preparation, measurements and ancillas are allowed, but dependence on the unknown `H` enters through evolutions of total interrogation time `tau` (summed over parallel copies). Additional direct coefficient metrology is a different acquisition channel whose precision, preparation, calibration and cost must be charged. The lower bound below applies only to this stated model.

Existing response competitors include correction-vector DMRG, MPS linear response, Lanczos/Gauss quadrature, exact low-dimensional inversion and gap/SDP certificates. [Nakatani et al.](https://arxiv.org/abs/1311.1646) give established DMRG linear-response algorithms; [Golub and Strakoš](https://doi.org/10.1007/BF02142693) treat inverse quadratic forms using Gauss-type quadrature. A new finite-moment or local-row method cannot claim priority for response or inverse-form bounds by rephrasing these operations.

## Exact local frustration-free counterfamily

Let `m>=2` qubits form an open chain. Put `n_i=sigma_i^+ sigma_i^-`, and for `1<=i<m` define the **local** annihilation row

```text
q_i = sigma_i^- - [i/(i+1)] sigma_(i+1)^- .
H_(m,e) = sum_(i=1)^(m-1) [(i+1)/i] q_i^* q_i + e n_m,
V = sigma_1^+ + sigma_1^- ,       e>0.
```

All coefficients are rational when `e` is rational. Every term is positive and has support on at most two adjacent qubits. The vacuum `psi=|0...0>` is annihilated by all rows and is a bond-one MPS. It is the **unique** ground vector: zero energy forces `sigma_m^- phi=0` and every `q_i phi=0`; these linear equations propagate backwards to `sigma_i^- phi=0` for all `i`, whose common kernel is just the vacuum. Neighboring row terms need not commute. The source is exactly `b=|1>` in the one-excitation sector, with `||b||=1` and no ground-space ambiguity.

On basis `|1>,...,|m>`, `H_(m,e)` is the rational tridiagonal `J_(m,e)` with off-diagonal `-1`, diagonals `2` for sites `1,...,m-1`, and terminal diagonal `(m-1)/m+e`. Its first `k<m` leading principal determinants are `k+1`; the full determinant is `m e>0`. Sylvester's criterion gives strict positivity in this source sector. The bottom-right `(m-1)`-square minor has determinant `1/m+(m-1)e`, so Cramer's rule gives the **exact response**

```text
chi_m(e) = <1|J_(m,e)^(-1)|1> = (m-1)/m + 1/(m^2 e).       (A)
```

Thus two chains `H_(m,e)` and `H_(m,2e)` have identical product ground states, every row except the terminal `e n_m` term identical, and operator-norm separation `||H_(m,2e)-H_(m,e)||=e`, yet their responses approach a ratio of two as `e -> 0`. More generally `e` versus fixed `c>0` gives an unbounded ratio while retaining identical source-near rows; that comparison has a constant-size remote difference, so it is an information-locality counterexample, not a precision lower bound.

Their source moments `M_k=<b,H^k b>` are **identical for every `0<=k<=2m-2`**. In the walk expansion of `(J^k)_(1,1)`, a term using the changed terminal diagonal must take `m-1` hops to site `m`, use one terminal diagonal step, then take `m-1` hops back. The first possible difference is exactly

```text
M_(2m-1)(2e) - M_(2m-1)(e) = e.                       (B)
```

No method whose acquired input consists only of those exact moments, or only rows on sites `1,...,m-1`, can return ±20%-accurate `chi` uniformly for sufficiently small `e`: its inputs are identical while the valid answer intervals are disjoint. This is a **restricted-information impossibility**, not a computational hardness result. Full exact rows expose `e`, and the same-information incumbent computes (A) by a tridiagonal recurrence in `O(m)` rational operations. Supplying that exact row therefore immediately defeats a claimed advantage based on missing gap information.

The conditioning is also exact:

```text
d chi_m / d t = -1/[m^2 (t-(m-1)/m)^2],  t=(m-1)/m+e.
```

An absolute uncertainty interval for the terminal coefficient containing both `t_c+e` and `t_c+2e` cannot support a response interval narrower than `[chi_m(2e),chi_m(e)]`. A ground-state MPS witness and exact low-order moments do not repair this coefficient-acquisition requirement.

## Physical acquisition lower bound

In the evolution-only unknown-generator model, the two Hamiltonians differ by `e n_m` of norm `e`. Duhamel's inequality gives `||exp(-it H_1)-exp(-it H_2)||<=e |t|`. Telescoping through arbitrary known controls and adaptive queries (purify measurements) bounds the final trace distance by `e tau`, where `tau` is summed unknown-H evolution time. A protocol returning disjoint ±20% response intervals with success at least `2/3` in each world would distinguish the worlds with success at least `2/3`; Helstrom's bound requires trace distance at least `1/3`. Hence

```text
tau >= 1/(3e).                                        (C)
```

With physical units this is `hbar/(3e)`. Parallel copies can lower wall-clock duration but not summed interrogation time; preparation, controls, readout and calibration only add cost. The bound has the expected Heisenberg precision dependence. [Huang, Tong, Fang and Su](https://arxiv.org/abs/2210.03030) already give Hamiltonian learning at total evolution time `O(1/e)` together with a matching lower-bound scope. This source supports treating the order `1/e` benchmark as incumbent performance, not our novelty. The elementary proof above is a specific two-world derivation.

Equation (C) does **not** constrain a supplied exact symbolic Hamiltonian, a trusted direct coefficient measurement, a control that changes the unknown coupling, or an oracle that reveals `e`. Those are different access models. Likewise, a direct static curvature assay must state perturbation amplitude, energy resolution, thermal floor and instrument calibration; it may be useful but is not free information and was not performed here.

| Resource or uncertainty | Exact symbolic interface | Unknown physical generator interface |
|---|---|---|
| Hamiltonian acquisition | Full rational rows supplied; this is an explicit favorable premise | Terminal coefficient must be learned to `O(e)` absolute precision or bypassed by a distinct response measurement |
| Ground preparation | Product vacuum is given analytically; checkable by local rows | Repeatable state preparation is required; no time/copy estimate is asserted for a real sample |
| Response computation | Tridiagonal rational solve `O(m)` arithmetic; coefficient bit length and conditioning still matter in finite precision | At least `1/(3e)` summed coherent evolution time to distinguish this pair; an established learning method reaches `O(1/e)` order under its own assumptions |
| Calibration, precision and output quality | Exact arithmetic certifies (A) for the model; physical interpretation depends on model fidelity | Readout, energy scale, temperature, decoherence, control error and model mismatch remain unmeasured; no physical ±20% interval exists here |
| Energy, memory, failure probability | Small exact memory in this fixture; no matched hardware energy budget | Beyond the time lower bound, all complete-system budgets and failure rates are **UNKNOWN** |

## Replay and exact finite values

`verify_boundary.py` uses only standard-library rational arithmetic. It reconstructs the matrix from local positive rows, checks the full moment identities and first differing moment, solves the source linear system independently, and verifies formula (A) for `m=3,5,8` with `e=10^-6`. Its saved output is `results.json`. At `m=5`, the exact responses are `200004/5=40000.8` and `100004/5=20000.8`, while moments `0,...,8` coincide and moment `9` differs by exactly `10^-6`. The lower bound is `tau>=333333.333...` in inverse-energy time units for the two-world physical-evolution interface. These are finite exact checks plus the displayed all-`m` proof, not independent external review.

## N816 and deepest reusable failure

Capital was read at HEAD `5ddabf53324159aa6c88e4fef3b75bc7b8b6c4ff`. The [N816 dossier](/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-frontier-genesis/frontier/dossiers/N816.txt) reports exact fixed-width AKLT response completion, but no all-`N` theorem or acquired-material capability. The decisive source [principal derivation](/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-frontier-genesis/updates/FN/package/frontier_genesis_v1/source/root/PRINCIPAL_DERIVATION.txt) lines 200–232 constructs a four-spin rational gap from the **same** rows; `gamma=1/10` and the same six-step primal give an N6 certified upper `1.4537037411509957`, below the local-dual upper `1.457001657709544`. The source [correction](/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-frontier-genesis/updates/FN/package/frontier_genesis_v1/source/root/CORRECTIONS_v0001.txt) also preserves the physical-row metric repair and narrow right-placement failure. These are internally derived/unreviewed source statuses.

The broad recurring failure is an **access-model substitution**: an algorithm is evaluated after a favorable representation, exact state, gap absence, hidden action, source path, or calibration is silently supplied, while its incumbent is denied the cheap acquisition or the same data. The AKLT gap is the sharpest mathematical example: absence from the input list was mistaken for an unavailable certificate. The present family sharpens the other side of that lesson: when a remote coefficient really is uncertain, a factor-two local response distinction can demand `Omega(1/e)` physical interrogation time even though the exact symbolic solve is trivial. A useful new capability must therefore either create a genuinely new physical measurement/control channel with its costs and matched incumbents, or show an algorithmic advantage after **both** methods receive the same fully acquired rows/state and accuracy obligation. This is a consequence of the two specific models, not a blanket impossibility for quantum response.

## Output status and decisive next action

| Claim | Status |
|---|---|
| FF nearest-neighbor rational counterfamily, unique product ground, formula (A), moment identity (B) | Proved here algebraically; exact finite replay for `m=3,5,8` |
| Evolution-only two-world interrogation lower bound (C) | Proved under stated black-box access model |
| Material-specific ±20% response of an actual unknown sample | **Not obtained**; no specimen, Hamiltonian calibration, ground preparation or response measurement |
| Advantage over correction-vector DMRG, Lanczos, exact tridiagonal solve or Hamiltonian learning | **Not established**; exact-input comparator solves this toy family cheaply, physical learning matches `1/e` order |
| Originality of this exact counterfamily or broader theorem | **UNKNOWN**; focused sources checked, no priority clearance |

The clearest actionable boundary is to require a proposed source-specific response method to pass a **paired-input test**: hold all acquired data and uncertainty sets equal, let the incumbent derive cheap gap/sector certificates and use the same raw measurements, then identify a scientific sample and precision target where the new output is certified at lower complete cost. For any proposed physical workaround to (C), specify the extra information channel and quantify its energy/time/copy/control costs. No such workaround or qualifying new capability was found in this investigation.

**Primary-source access limits.** The arXiv author abstracts of [Nakatani et al.](https://arxiv.org/abs/1311.1646) and [Huang et al.](https://arxiv.org/abs/2210.03030), and APS abstracts of [Fischer and Rosch](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.71.184429) and the [BiCoPO5 experiment](https://journals.aps.org/prmaterials/abstract/10.1103/PhysRevMaterials.6.094413), were accessible during this pass; full paper bodies were not audited. [Golub and Strakoš](https://doi.org/10.1007/BF02142693) was accessible through indexed publisher abstract, while direct DOI opening failed. Our mathematical proof does not import an unstated theorem from those papers; citations delimit comparator and scientific relevance, and priority remains open.
