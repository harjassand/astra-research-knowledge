# Randomized compiling: experiment and hidden-channel qualification audit

Checked 2026-10-16. **Best public reanalysis lead: Ware et al. None of the three sources, as checked, establishes the requested physical hidden random-Z channel on arbitrary joint system–bath inputs.** This is a qualification gap, not a claim that randomized compiling has no physical effect.

## 1. Ware et al.: strongest open data, but a consequential frame caveat

The work appeared as arXiv:1803.01818 in 2018 and as *Physical Review A* **103**, 042604 (2021). [Paper, especially Sections II, IV and “Access to data”](https://arxiv.org/pdf/1803.01818).

- One transmon, long-sequence GST, 1,000 randomizations per original circuit, one shot per randomization, seven interleaved randomized/unrandomized runs.
- Pauli operations are fused into adjacent Cliffords. Each resulting Clifford has two physical 50 ns Xπ/2 pulses and three Z-frame updates. Equal gate durations avoid a pulse-length confound.
- The reported tests concern the compatibility of pooled observed statistics with effective Markovian/Pauli gate-error models. They do not directly tomograph a system–bath channel or an inserted standalone dephasing operation.

**Raw data verified, not merely promised.** [Author repository](https://github.com/matthewware/RGST-analysis), [data directory](https://github.com/matthewware/RGST-analysis/tree/9afedca174dbcb14d52c245cf7504a834816fc39/data), and [Zenodo 4609459](https://zenodo.org/records/4609459). The archive is 14.6 MB and provides analysis code, GST counts, and reconstructed operators. I downloaded and parsed `data/gst_1.gst` and `data/rgst_1.gst`: each has 3,505 sequence rows, each with two outcome counts totaling 1,000. These are counts aggregated under original GST sequence labels. The inspected repository tree does not contain shot-by-shot randomizer labels, executed waveform traces, or all experimental branch CSVs. It includes a generator and precomputed `.npz` reconstructions. Thus it is suitable for reproducing the published GST fits, not recovering hidden-branch physics directly. [Repository README](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/README.md).

**Important positive lead:** the public [randomization script](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/scripts/rand/randomize.jl#L1-L24) explicitly includes a final I/Z draw in the correction and fixes a reproducibility seed in the provided generator. [Its README](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/scripts/rand/README.md) and [notebook](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/notebooks/Randomize.ipynb) explain that the final logical sequence is equivalent up to I or Z, leaving computational-basis populations unchanged. This is more relevant than generic RC, but still only a logical-channel lead.

**Compiler audit:** the public [QGL.jl diatomic implementation](https://github.com/BBN-Q/QGL.jl/blob/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/src/pulses.jl#L169-L203) maps Clifford 1 (I) and Clifford 9 (Z) to the same first four operations; only the terminal Z-frame angle differs. ZPulse has [zero length](https://github.com/BBN-Q/QGL.jl/blob/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/src/pulses.jl#L82-L85). The [APS2 translator](https://github.com/BBN-Q/QGL.jl/blob/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/src/APS2.jl#L281-L288) emits an UPDATE_FRAME instruction for it; it does not emit an additional qubit-drive waveform. [GST generation](https://github.com/BBN-Q/QGL.jl/blob/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/src/GSTsequences.jl#L45-L64) then appends measurement.

**Inference:** a terminal logical I/Z label can therefore leave the same physical drive history before Z readout. This is a concrete reason not to infer physical pinching from the generator alone. Earlier virtual phases can change later physical pulse axes, so it would also be wrong to call all PFR “just bookkeeping.” The inspected repository revision is not proven to be the exact archived experimental compiler build.

## 2. Hashim et al., PRX 11, 041039 (2021)

[Published paper, Sections II, VI and Appendices](https://escholarship.org/content/qt4fp0c2nb/qt4fp0c2nb.pdf); [publisher record](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.11.041039).

Actual superconducting experiments include state tomography, cycle-error reconstruction, four-qubit QFT, and variable-depth random circuits. The protocol inserts logical twirling operations, inverts them in subsequent cycles, and compiles the whole dressed easy gate. Averaging pooled results gives the tailored error channel while preserving the intended ideal circuit. The paper calls the inserted twirls virtual; that does not establish that all resulting physical pulses are unchanged.

The state-tomography example pools 12 variants, 500 shots per measurement basis each. Data availability points to the article, supplement, or corresponding author on request. No openly downloadable raw shot/circuit repository was verified. Supplemental figures/data should not be described as a verified machine-readable raw dataset.

**Qualification:** useful experimental evidence for noise tailoring; neither an independently discarded random-Z intervention nor a certificate on correlated system–bath inputs. Lower priority than Ware for a strictly public-data reanalysis.

## 3. Winick et al., “Concepts and conditions…”

[Primary paper](https://arxiv.org/html/2212.07500v1), especially Sections II, III.B–C and IV. The verified record is **arXiv:2212.07500v1, December 14, 2022**, not a verified 2023 journal publication.

Experiments use IBM Melbourne, including physical identity hard cycles, parallel single-qubit gates and CNOTs; final twirling is handled through classical postprocessing. No raw-data archive, branch records, or pulse-level experiment specification was identified in the inspected paper.

Theorem 3 assumes gate-independent easy-gate errors and concerns effective local stochastic Pauli errors, allowing bath-dependent coefficients. The paper itself gives a failure mechanism when gate-dependent errors leak twirl information to the environment; one parity bit can suffice for coherent accumulation. This directly matters to a requirement that the random choice remain hidden from the bath.

**Qualification:** strongest of these for explaining necessary assumptions and why “non-Markovian RC works” is not an unconditional physical-refresh certificate; not a qualifying raw-data route.

## What would close the gap? (analysis)

The desired operation is an intervention at a fixed physical boundary:

D_Z^S(ρ_SB) = [ρ_SB + (Z_S ⊗ I_B)ρ_SB(Z_S ⊗ I_B)]/2.

To infer this from implementation, establish the actual branch operations, their common timing/bath action, independence of the classical choice from the input/bath, absence of branch-dependent compensation in subsequent controls or analysis, and the specified treatment of the classical record. Merely twirling an error superoperator, changing a frame convention, or fitting a reduced-system Pauli channel does not imply this equality. Even D_Z^S preserves classical S–B correlations; it is not a full bath-memory reset.

For Ware specifically, the decisive next public evidence would be the exact executed compiler/waveform revision plus a phase-sensitive measurement after the purported random-Z boundary using a common physical reference. Existing computational-basis counts cannot distinguish physical terminal Z dephasing from a terminal frame update.

## Local evidence files

Downloaded public evidence only; no third-party code executed: `rgst_1.gst`, `ware_data_gst_1.gst`, repository-tree JSONs, Ware generator/README/notebook, and QGL.jl pulse/compiler/GST/APS2 source files in this directory. No outreach or canonical edits performed.
