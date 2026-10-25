# Astra Chemical Invention — Two-register DNA–thioester escrow and selective molecular commitment

**26 October 2026.** Continuation of Astra chemical-invention role. Analytical and computational study. **No new chemical system has been fabricated or tested.** The data files below are design calculations, not experimental kinetics. The original question is independent instruction advancement upon *the correct organic covalent bond*, with harmless retries and no double incorporation.

## 1. Physical observation supporting a changed mechanism

Jennifer Frommer et al., *A New Architecture for DNA-Templated Synthesis in Which Abasic Sites Protect Reactants from Degradation* (Angew. Chem. Int. Ed. 2024; DOI **10.1002/anie.202317482**) measured internal-abasic-site DNA-templated acyl transfer of a DNA-linked **TAMRA thioester**, with a primary amine on a second DNA strand. For a particular abasic geometry, **n=-3**, the thioester hydrolysis rate was reduced by **more than 100-fold**. Positions **n=+1/+2** favored acyl transfer. Toehold-driven replacement of a protective 'keeper' strand with an acceptor strand initiated amide formation after up to **48 hours protected storage**. Storage was assayed at **pH 11, 5 C** and subsequent acyl transfer at **pH 11, 15 C** (other preliminary acyl-transfer observations also at pH 11 at room temperature). Crucially, changing the hydrophobic TAMRA group to hydrophilic biotin removed the hydrolysis-protective effect. This shows a **substrate-dependent switchable ester environment** and does **not** demonstrate that a donor becomes completely inert to all amines in the protected state.

M. L. McKee et al., *Peptidomimetic bond formation by DNA-templated acyl transfer* (Org. Biomol. Chem. 2011; DOI **10.1039/C0OB00753F**) established acyl transfer involving DNA-thioester donors under some mild aqueous near-neutral reaction conditions, in a different substrate/geometry. It does not prove the new abasic-site switch operates there.

One **proposed**, not demonstrated, donor is `N3-PNA4-C(O)-S-(cleavable DNA escort)` attached to a long DNA-address sidecar plus an abasic-site 'keeper'. It would transfer `PNA4-C(O)` onto `Root-NH2` and leave a `DNA-escort-SH` group. The newly incorporated PNA amine remains masked with N3, preserving Joshi et al.'s single-incorporation barrier in principle. Protected/unprotected amine/thiol chemistry, position of hydrophobic ligand, rooted product geometry, and selective reduction remain unmeasured and might make the combination fail. The observed protection comes from TAMRA on the *cargo side* of the thioester; moving a hydrophobe solely onto the DNA leaving-group side has **not** been demonstrated to preserve shielding.

## 2. Exact two-register continuous-time mechanism

**Transient states:** S, protected by keeper duplex; A, geometrically reactive/authorized by DNA strand exchange. Rates:

- S->A `q`, protected-state wrong permanent reaction `wS`, harmless hydrolysis `hS`, irreversible root destruction `dS`.
- A->S `r` (resheltering), A->intended root amide `k`, active wrong irreversible reaction `wA`, harmless hydrolysis `hA`, irreversible root loss `dA`, donor escape `e`, with wrong reaction following escape with probability `chi`.

Let `DS=q+wS+hS+dS`, `DA=k+wA+hA+dA+e+r`, `D=DS*DA-q*r`. Then exact absorption probabilities for initially shielded donor:

```
P_C = q*k/D
P_W = (wS*DA+q*(wA+e*chi))/D
P_H = (hS*DA+q*(hA+e*(1-chi)))/D
P_D = (dS*DA+q*dA)/D
E[duration to any outcome] = (DA+q)/D
```

All are verified with independent `(-Q)^-1 R` matrix computations and stochastic trajectories in `astra_chemistry_two_register_20261026.py`. They sum to one and retain their physical scopes.

**Theorem: chemical protection alone does not imply fidelity improvement.** From these formulas:

```
P_W/P_C = (wA+e*chi)/k + (wS/q)*(DA/k).
```

In particular, `hS` cancels exactly. Consequently, if every harmless donor hydrolysis permits immediate, independent replenishment without parent damage, the eventual probability of a correct rather than wrong permanent bond is independent of `hS`. The mean duration until any permanent event also has exact expression

```
E[time to permanent] = (DA+q) / ((wS+dS)*DA + q*(k+wA+e*chi+dA)).
```

It, too, is independent of `hS` **under instantaneous replenishment and no additional reset overhead**. Hydrolysis protection instead lowers donor consumption, the number of resets and the associated risk/cost. Claiming that 100-fold protection from hydrolysis implies 100-fold improved wrong-versus-correct selectivity is unjustified.

**Error floor.** Since `wS>=0`, `P_W/P_C >= (wA+e*chi)/k`: a protective DNA switch that leaves the productive state's intrinsic wrong-bond competition unchanged can only **increase**, not decrease, the wrong/right odds. To improve selectivity relative to an equally informed direct acyl-transfer arrangement, the switch must reject mismatched donors, lower `wA` or `chi`, or generate another physical selectivity change. Increasing reverse switching `r` increases `DA` and amplifies exposure to protected leakage `wS`.

For `L` independent correctly completed steps and target `F`, the wrong/right odds must satisfy `rho <= F^(-1/L)-1`. At `L=1000, F=.99`, the bound is **1.0050386e-5**. Thus `wA+e*chi <= 1.00504e-5*k` even if the sheltered state is perfectly safe. For illustrative `k=.02/s, wA=1e-7/s, e=2e-4/s, chi=.001`, the floor ratio is `1.5e-5` and best possible 1,000-step fidelity is **98.5112%** even if `wS=0`. The numbers are hypothetical; their value is eliminating a whole unproductive class of refinements.

## 3. Hydrolysis matters again when replacement is imperfect

Let `C,W,H,D` be the above per-donor probabilities. After harmless hydrolysis, let fraction `delta` irreversibly lose parent competence or correct registration. Let each successful recovery take additional time `tau`.

Then the exact effective per-stage probability of correct terminal outcome after arbitrary retries is

```
F_stage = C / [C+W+D+delta*H]
expected donor encounters to permanent decision = 1/[C+W+D+delta*H]
expected seconds to a permanent decision = [E[duration]+H*(1-delta)*tau] / [C+W+D+delta*H].
```

Independent finite-retry Markov analysis verifies these equalities (`astra_abasic_repair_cost_20261026.py`). For **hypothetical** `q=k=.02/s, wS=1e-9/s, wA=1e-8/s, hA=.002/s, r=.03/s, e=2e-5/s, chi=.001`, and reset damage `delta=1e-5`, outcomes for a 1,000-stage chain:

| protected hydrolysis `hS`, 1/s | per-encounter hydrolysis | F1000 with reset damage |
|---:|---:|---:|
| 0.1 | 92.91% | 87.57% |
| 0.01 | 58.36% | 98.45% |
| 0.001 | 18.77% | 99.61% |
| 0.0001 | 10.23% | 99.72% |

Ideal `delta=0` correctness is **99.8371%** in all rows, reinforcing the theorem. Unremoved hydrolyzed PNA can poison DNA occupation, so treating every hydrolysis as harmless is itself a strong separate assumption from the previous waste-poisoning theorem.

## 4. Exact multistep checkpoint leakage with finite optimum

For each donor identity class `i`, consider `n` sequential DNA checkpoints. At each checkpoint, advance at rate `gamma`, dissociate harmlessly **with full checkpoint reset** at `u_i`, or make a wrong permanent bond at rate `ell`. At the authorized state, correct-position acyl transfer proceeds at `k`, wrong-site transfer at `b`, or hydrolysis at `hA`. Let `s_i=gamma/(gamma+u_i+ell)`.

Per donor encounter:

```
P_authorized_right_i = s_i^n * k/(k+b+hA)
P_wrong_i = [ell/(u_i+ell)] * (1-s_i^n) + s_i^n * b/(k+b+hA)
E[encounter time] = (1-s_i^n)/(u_i+ell) + s_i^n/(k+b+hA).
```

For the wrong identity, every authorized transfer counts as a wrong rooted product regardless of site. Let `R=lambda_wrong/lambda_correct` be aggregate wrong-to-right encounter arrivals. The exact odds between permanent wrong and correct outcomes over harmless retries are

```
rho(n)= [P_wrong_good(n) + R*(P_authorized_right_wrong(n)+P_wrong_wrong(n))]
         / P_authorized_right_good(n).
```

For `ell>0`, `s_good^n` tends to zero, but `P_wrong_good` tends to positive `ell/(u_good+ell)`; thus `rho(n)->infinity`. **Any persistent premature chemical leak makes arbitrarily deep proofreading counterproductive.** With `ell=0`, discrimination improves indefinitely in this model, but correct-donor throughput collapses as `s_good^n`. Verified against explicit `(n+1)x(n+1)` absorbing matrices and independent stochastic trajectories in `astra_checkpoint_escrow_explicit_20261026.py`.

Toy parameters `gamma=.15, u_good=.05, u_wrong=.5, k=.02, hA=.001`, 1/s, `b=0`:

| leak ell, 1/s | aggregate R | best n | F1000 at optimum | expected encounters/bond | seconds/bond |
|---:|---:|---:|---:|---:|---:|
| 1e-8 | 1 | 11 | 99.24% | 49.7 | 576 |
| 1e-8 | 255 | 13 | 74.79% | 11,311 | 23,447 |
| 1e-10 | 255 | 16 | 99.28% | 26,819 | 55,553 |

All rows are **illustrative** and omit replacement overhead and finite apparatus lifetime. A very deep proofreader may produce a pure output but at catastrophic throughput. Identity-selective **recruitment** must reduce effective `R` before checkpoints. DNA fuel-driven proofreading precedent: Mukherjee et al. 2024, DOI **10.1021/jacs.3c14673**; its experiments do not demonstrate these n-step rate values on an organic acyl donor.

## 5. Explicit 256-cargo DNA-address construction, and its structural failures

To reduce the aggregate wrong-donor encounter rate independently of PNA4 recognition, assign each of 256 canonical PNA4 payloads a longer DNA recognition address. The experimental precedent for protected abasic-site thioesters uses DNA strands; we considered a 16-base DNA barcode on the donor *escort*, encoding payload identity, not an additional PNA block attached to the final product.

`astra_orthogonal_256_escorts_16nt_20261026.py` builds a 4-dimensional **GF(4)** affine linear code of length 16 for 4^4=256 donor addresses and writes `astra_256_escorts_16nt_20261026.csv` containing the PNA4 payload, DNA escort, and intended complementary template address. A separate pairwise scan verified:

- All 32,640 distinct aligned barcode pairs differ at **at least eight nucleotide positions** (minimum Hamming distance 8).
- Reverse-complement comparisons between all 256 barcodes, including themselves, have minimum **five** mismatches in full aligned 16-base comparisons.
- **Unresolved defects:** 37 barcodes contain a homopolymer run of at least four bases; two have GC counts outside 4–12; four cross-barcode complementary contiguous 10-base occurrences exist at *shifted* registers. These must be redesigned or experimentally evaluated before treating the addresses as usable.

Under an explicitly hypothetical independent equilibrium free-energy penalty `deltaG` for *each* mismatched base, all 255 wrong donors at equal concentration are bounded by odds `255 exp(-8 deltaG/(RT))`. To achieve 1.005e-5 wrong/right odds solely from this mechanism at 298.15 K would require `deltaG >=1.263 kcal/mol` for **every** mismatch. Real duplex thermodynamics is position/sequence/environment dependent, and displaced/off-register toeholds, partial 10-base complements, rebinding and multivalent recognition can defeat this substitution-count bound. Thus the code is an **addressing prototype**, not a proven orthogonal chemical repertoire. It could be useful even if it only lowers the effective `R` by a modest factor because it reduces required proofreading depth.

The preliminary 12-base code had minimum aligned distance 6 but reverse-complement mismatches as few as 2. It was rejected as a less satisfactory physical addressing candidate (`astra_orthogonal_256_escorts_20261026.py`).

**Coding–contour geometry warning:** sixteen bases span approximately 5.44 nm of axial distance on straight B-form DNA, much more than the contour added by one short conventional chemical monomer or PNA4 segment. This barcode cannot simply be repeated as a stationary straight DNA ruler alongside a permanently rooted growing chain. A local stationary reaction site with moving/folded information strands, or otherwise compensated spacing, remains necessary. The codebook solves only an *aligned symbolic identity-separation* problem, not DNA mechanical registration or chemical kinetics.

## 6. Strongest comparators and experiment-facing falsifiers

1. **Staged masked-NHS PNA4** (Joshi, Romanens, Winssinger, 2025 DOI **10.1021/jacs.5c00708**): genuine measured protected-terminus extension with two globally staged cycles. Fewer proposed interfaces, demonstrated chemistry; does not yet provide independently asynchronous program advancement. Its NHS ester differs significantly from the thioester tested by Frommer. If chemistry is already selective enough, added gating is disadvantageous.
2. **Protected DNA–TAMRA thioester** (Frommer 2024): already demonstrates shield/switch/amide at two DNA registers; Astra must add true PNA cargo, chemically competent parent-rooted transfer, mixed-code specificity, product-qualified advancement and retry without wrong bond, not claim the basic pocket mechanism as original.
3. **Enzymatic CoA ligase + N-acyltransferase** (Schaub et al., Nature Catalysis 2026 DOI **10.1038/s41929-026-01576-x**): demonstrated >120 different on-DNA amides and >91% average conversion in an enzymatically assembled DNA-encoded chemical library at DNA-compatible conditions. Enzymes naturally manage activated intermediate recognition and are a stronger comparator for near-term molecular diversity. However, a 120-product substrate scope does **not** establish arbitrary sequence-by-sequence polymer synthesis in a 256-donor common solution, or independently progressing chemical programs.
4. **DNA autonomous walker** (He/Liu Nat Nanotechnol 2010 DOI **10.1038/nnano.2010.190**) and later acyl-transfer implementation (He/Liu JACS 2011 DOI **10.1021/ja201361t**): DNA motor motion must be chemically product-qualified; donor linkage loss alone can be mimicked by hydrolysis.

**Minimal discriminating physical tests (not performed):** compare rooted parent + identity-matched versus mismatched shielded donors, with and without a free competing amine. Quantify separately (a) protected-state hydrolysis, (b) wrong **aminolysis while protected**, (c) active-state correct amide rate, (d) active-state escape plus wrong reactions in other programs, (e) incomplete donor ejection and template site poisoning, (f) repeated retry retention of the original rooted amino terminus, and (g) correct instruction advancement only after root-connected, correct-site product. Denaturing root capture plus site-sensitive MS/MS or orthogonal bond analysis is needed; donor-strand release/fluorescence/mass alone is insufficient. Compare exactly the same chemical loads and number of steps against staged masked-NHS PNA and enzyme-assisted on-DNA amidation wherever compatible.

**Current physical bottleneck:** obtain a substrate-general, automatically and reversibly shielded **DNA-linked N3-PNA4 thioester** with low off-target aminolysis and correct rooted-amide coupling under a *single compatible* buffer/temperature/catalysis regime. The 2024 result motivates but does not establish it. Identity-selective activation, rooted product qualification, and return-to-protected after temporary undocking remain unacquired. No fully autonomous, fault-tolerant chemical manufacturer has been demonstrated by Astra.

### Executable assets

- `astra_chemistry_two_register_20261026.py`: exact state-switch rate analysis and stochastic checks.
- `astra_abasic_repair_cost_20261026.py`: finite donor-replacement cost/damage renewal analysis.
- `astra_checkpoint_escrow_explicit_20261026.py`: explicit multistep proofreading, absorption matrices, Monte Carlo, throughput.
- `astra_orthogonal_256_escorts_16nt_20261026.py`, `astra_256_escorts_16nt_20261026.csv`: reproducible address construction (sequence warning above).
- Earlier `astra_dna_escort_absorption_20261026.py`, `astra_chemical_escrow_integrated_20261026.py` retain distinct prior bounds on transient PNA undocking, washing and chemically conditioned advancement.
