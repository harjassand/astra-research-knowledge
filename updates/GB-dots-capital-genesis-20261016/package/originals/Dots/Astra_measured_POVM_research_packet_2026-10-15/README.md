# Measured POVM conditional risk reversal research packet

2026-10-15. Public calibration-data reanalysis with exact deterministic certificates.

## Result and scope

Huang's published θ=π/4 elegant joint measurement (EJM) tomography fit admits a **conditional local-preparation risk reversal** for the specified binary squared-loss experiment. The construction uses two independent local preparation rotations and four frozen classical scores. It uses no global EJM-to-Bell transformation.

For every physical POVM whose real and imaginary matrix components lie in the declared box around those printed effects:

| Component tolerance | Target risk upper bound | Source q | Source minus target lower bound |
|---|---:|---:|---:|
| ±0.0005 | 0.86587001068001228841 | 0.45 | 0.00024569179932655457 |
| ±0.001 | 0.86746321638049581055 | 0.43 | 0.00460289932198352829 |

At q=0.45 and ±0.001, the same bound is negative (approximately −0.00134751390115697). Thus this certificate establishes a positive q=0.45 gap only for the tighter of these two declared boxes. A negative lower bound is inconclusive, not proof that reversal fails. The q=0.43 option changes the source experiment and is explicitly a separate design; it leaves the target, local rotations and scores unchanged.

Both boxes are physically nonempty, as proved by exact rational positive-definite complete POVM witnesses. **Neither box is a paper-derived statistical confidence region. Actual apparatus membership is unestablished.** This is not a new experiment, an observed reversal, or a statistically established or loss-inclusive apparatus advantage.

The separately acquired Welte conditional Bell POVM fails the specified fixed test: predicted risk 1.0056355173125497 against source risk 0.8661157024793389. Refitting only the four scores gives 0.9624734837175528, still worse. This is a negative result for that preparation and fitted receiver; it does not rule out all rotations, other tasks, or that hardware generally.

## What is included

- `RESEARCH.md`: complete mathematical contract, evidence boundary, closest experimental precedents, missing operation and decisive test.
- `data/`: unaltered public Welte numeric CSVs and archive metadata; Huang printed-matrix transcriptions in CSV and NumPy formats; diagnostic results.
- `certificates/`: frozen rational design, exact symbolic bound expressions, exact rational feasibility witnesses and constructor inputs.
- `checks/`: portable constructors, transcription replay, Welte calculation, and independent algebraic/vertex-enumeration audits.
- `PROVENANCE.json`: primary links, acquisition hashes and original archive MD5 verification.
- `SHA256SUMS.txt`: checksums for all packet files except the manifest itself.
- `REPLAY_REPORT.txt`: fresh-extraction verification result and environment versions.

No full papers, screenshots, private notes or external filesystem dependencies are included. Primary sources remain linked below. The provided `figure4_info.txt` is the dataset's short basis description.

## Reproduce

Python 3 with NumPy and SymPy is required. No solver, network connection, GPU or proprietary package is needed. Install dependencies in your preferred environment if necessary:

```sh
python -m pip install numpy sympy
python replay.py
```

The replay verifies the SHA-256 manifest, copies the packet into a temporary working directory, regenerates Huang transcriptions and diagnostics, checks CSV/NumPy consistency and Welte archive checksums, regenerates exact certificates and runs independent audits. It does not modify the extracted packet. Exact SymPy assertions control the mathematical certificates; displayed floating-point values are only summaries. Welte's public floating-point fit is a numerical calculation, not an exact statistical certificate. Runtime depends on SymPy version.

`frozen_design.json` is preserved verbatim. Its `physical_gap_lower_tau_0005` and `physical_gap_lower_tau_001` fields are older, weaker diagnostic bounds, not the final completeness-aware result. The exact final bounds are in `tight_box_certificate.json`; frozen stereographic coordinates and scores in the design file remain authoritative. A small earlier floating-point center diagnostic is likewise superseded by the exact certificates.

## Primary sources

- Huang et al., generalized elegant joint measurement: [arXiv 2203.16207](https://arxiv.org/abs/2203.16207), [Physical Review Letters 129, 030502](https://doi.org/10.1103/PhysRevLett.129.030502). The numerical matrices are in Appendix A, pages 7–8 of arXiv v1.
- Welte et al., distant-atom Bell measurement: [Nature Photonics paper](https://www.nature.com/articles/s41566-021-00802-1), [public dataset](https://zenodo.org/records/4604775), [dataset DOI](https://doi.org/10.5281/zenodo.4604775).
