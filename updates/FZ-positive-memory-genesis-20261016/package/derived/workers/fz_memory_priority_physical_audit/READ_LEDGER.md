# Actual primary reading ledger

This audit read targeted portions of the actual primary files below. It did not re-prove all cited papers or the producer's sweep/envelope proof. Source TeX was used for formula fidelity. A range records targeted reading in that range, not a claim of uninterrupted line-by-line reading. Some primary bytes were copied read-only from the producer's acquisition; those are distinguished from new independent downloads in the receipts. Version-history checks were independent live reads.

| Source | Material actually inspected | Purpose |
| --- | --- | --- |
| 1809.10145v1 | `Toom_prl6.tex` 150-390 | Trailing rule, simultaneous sweep lemma, static-error/perfect-syndrome theorem, repeated-noise numerical boundary |
| 2610.05589v1 | `submission.tex` 1720-1798, 2225-2510 | Codeword shift/initialization, asynchronous reduction/equivalence, synchronous 4D and Floquet theorems and schedule dependence |
| 2601.20818v3 | `SM.tex` 1250-1355; main source acquired | Entire continuous-time sections VII.1-VII.2, explicit outline status, finite clocks/repair, Poisson channels, additional-unitary-only noise |
| 1010.2901v2 | `DissipativeQMemory.tex` 95-204, 205-270, 328-343, 515-590 | Poisson channel generators, rigorous nonlocal concatenation, numerical local 4D model, old completion/inactive projector, ancilla/bath assumptions |
| 2212.08437v2 | `KCM-CP_v2.1.tex` 621-675 | Decorated-set theorem and Corollary 9.5, infinite-volume upper-invariant spacetime tail, radius dependence |
| 0811.0033v1 | `top-magn6.tex` 310-455 | Davies/KMS, Gibbs inner product, thermal ancillary fidelity proposition |
| 0907.2807v2 | `arXiv.02.tex` 1046-1128 | Exact thermal encoding/decoding construction and distinction from ground-space encoding |
| 2507.10976v1 | `main.tex` 1860-1995 | Conditional-block rapid-mixing theorem, cold-start reduction, reachable states and one-step small-loop escape lemma |
| 2605.10943v1 | `paper.tex` 250-310, 484-520, 1250-1295 | Thermal memory theorem, bounded-density/finite-range 3D claim, explicit initialization gap and encoding formula |
| 1303.4744v4 | `result.tex` 1-120; `proof.tex` 175-245 | Unique-fixed-point/rapid-mixing assumptions, local-observable perturbation theorem, support dependence and proof |
| 1711.02999v3 | `jaemo36.tex` 130-265, especially 180-264 | AutoQEC condition/error bound, full-state construction, known-Hamiltonian cancellation |
| 2103.05007v1 | `Paper.tex` 165-306 | AutoQEC definition, finite-system norm prefactor, order-c claim, explicit global error-space jumps |
| 2307.09512v2 | `main.tex` 453-565; accepted published text acquired and searched | 4D local model, rate changes, finite-lattice stabilizer autocorrelation evidence rather than decoded lifetime theorem |
| Yu-Wei 2026 | published PDF text 490-585, 626-653; searches across main/SI | Linear soundness/extensive barriers, precise Prop. II.1/II.2 initialization, variation and Gibbs conditions |
| quant-ph/9604034v1 | `tqecp` 735-825, 948-1015 | Recovered scalar-Kraus criterion, linear closure, entangled input exact correction |
| quant-ph/0111064v1 | `part1` 115-165 | Original positive-Choi offset by depolarization |
| 1008.5056v3 | `source.tex` 487-545 | Explicit nonpositive-map regularization and full-rank Choi interval |
| 0711.3172v2 | `snapshotfinal3xxx.tex` 407-455 | Isotropic depolarizing generator used to restore the Lindblad condition |
| 2308.16233v2 | `quantum_main.tex` targeted model/result searches at 181-226, 330-378, 448-454, 894-919, 2020-2033, 2154-2185 | Global versus local recovery, rate scaling, strict error reduction, nonlocal support |
| 2609.20537v1, independently acquired | `main_arxiv1_clean.tex` 254-285, 2713-2778 and targeted model/theorem searches | Fixed minimum-weight decoder, coherent/local-CPTP code-capacity threshold, polynomial prefactor and distance exponent |
| 2609.38139v1, independently acquired | `main.tex` 82-108, 160-215, 280-293 and result/numerics searches | Perfect syndrome, Z-only/real-message model, offline-no-further-noise boundary, Poisson feedback |
| 1112.3252v1, independently acquired | `memorytime.tex` 214-277, 300-363, 558-640 | Genuine ground-space Davies initialization, finite-size trace-norm bound/cutoff, final decoder |
| 2609.39959v1, independently acquired | `main.tex` 113-139, 126-138, 345-352 and rate/model searches | Current fixed-temperature cubic-code rapid-mixing theorem claim and rate assumptions; not independently re-proved |
| 2403.10599v3, independently acquired | `arxiv.tex` 430-550, 555-669, 850-920 targeted, 962-1039 | Quantum theorem is slow mixing from Gibbs-weighted decodable ensemble A; rate retuning for specified Pauli/circuit noise; graph versus geometric locality |
| 2510.06659v2, independently acquired | `arxiv_v2.tex` 270-342 plus targeted precise-theorem/cutoff searches | 3D cold-start Davies partial memory and size/temperature cutoff; efficient decoder distinction |
| 2507.21396v1, independently acquired | `v1.tex` 50-70, 314-373, 627-711 targeted, 759-769 | ZSZ numerical threshold status, same-model 4D comparison, nonlocal atom routing and scratch space |
| MTTV 1997 author PDF, independently acquired | PDF pp. 1,3,4,5 text; rendered and visually inspected PDF p.4 | Theorem 2.2.1 O(k^(1/d)N^(1-1/d)) sphere separator, exact balance; used only under explicit physical-network/minor assumptions |

Additional live primary search leads that were not completely proof-audited are not promoted into stronger theorems. The inspected-set absence of a matching sweep theorem is not an exhaustive history certificate. The primary LSS proof was not reacquired or audited by this worker, and this worker does not upgrade the producer's named LSS import/access boundary.

Source-access correction: the original and independently retried `1008.5056v3.source` both have a gzip checksum failure. The saved extracted TeX was therefore cross-checked against independently retrieved versioned primary HTML for the actual nonpositive-map/full-rank-Choi statements. No valid archive-member claim is made for that file. This affects a redundant historical SPA-tool reference, not the sweep sources or their named classical import. The bad bytes/HTTP receipt are preserved.
