# Exact evaluator handoff

## Inputs and interpretation
Data root: measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/d5_at_q8_7/X/.

| Condition | Shots | Measurements | Detectors | Sweep | Observable | Bytes/shot M,D,S,O |
|---|---:|---:|---:|---:|---:|---|
| r50 | 50,000 | 1,225 | 1,200 | 25 | 1 | 154,150,4,1 |
| r13 | 50,000 | 337 | 312 | 25 | 1 | 43,39,4,1 |

Every b8 row is independently byte-aligned, little-endian within each byte. Padding must be zero. Original row i aligns between measurement, sweep, detection, actual observable, and all published prediction streams. Row order is not established wall-clock chronology. circuit_ideal.stim defines the normative interface; maps in measured_syndrome_audit expose the exact measurement-index, sweep-mask and independently simulated reference-offset equation for each detector and observable.

## Frozen split
For each original zero-based r50 row i in 0..49999, compute SHA256 of the ASCII bytes `astra-willow-split-v1:` + the unpadded base-ten representation of i. Sort ascending by raw digest (equivalently its hexadecimal representation). First 25,000 rows are diagnostic; remaining 25,000 reserved. The supplied text files retain digest order, one decimal index plus LF per line.

- measured_syndrome_audit/diagnostic_indices.txt: 80d49493e16e51d3f2cfe8574ec3316ded74e0a51ae49865165e9def979ee2ae
- measured_syndrome_audit/reserved_indices.txt: 3353cbe6f4b1c6ad12045e77b1e0e9d93a01e04e676007580d9f86f621abdbf0

The packet carries the original full labels for reproducibility; the reserved indices are a protocol boundary, not access-control encryption. This handoff authorizes no new reserved analysis. Before any future confirmation, freeze the hypothesis, feature restrictions, algorithm/model parameters, score, comparator, multiplicity correction, statistical assumptions, and stopping rule. Do not use diagnostic-selected effects as though their diagnostic p-values were confirmatory. r13 is separate calibration, already associated with publisher prior optimization.

## Established results and limitations
The existing scripts are read-only with respect to publisher inputs. They reconstruct measurements, verify published outputs, reproduce the fixed diagnostic family, and reproduce the completed r13 calibration/control audits. No decoder fitting, parameter optimization, additional stratification, new hypotheses, hardware work, or external communications are included.

Any future decoder comparison should be paired on exactly the same held-out shots and report uncertainty without treating round outcomes within a shot as independent samples. The five acquired predictions are available comparators. The stronger published AQ1/AQ2 neural comparison remains unavailable as an authoritative exact per-shot artifact; disclose that gap rather than downgrading the incumbent.

Do not give a decoder unrestricted final raw data measurements: the actual logical observable is an explicit parity of them. The initial raw syndrome frame may carry useful information, but usefulness, transfer, and novelty are separate questions. Initial noisy gauge tags are not true fault/state labels. Ten preparation settings do not identify a local intervention; more repeated shots of the same settings do not supply missing causal contrasts.

No timestamps, shot cadence, guaranteed temporal order, physical fault labels, rejection flags or complete selection audit are supplied. No result certifies a microscopic non-Markovian model, quantum mechanism, uniform fault norm, local-stochastic theorem, 4D hardware implementation, or net-beneficial physical feedback.

## Integrity and replay boundary
MANIFEST_SHA256.json hashes every packet payload except itself and the replay log. Source SHA256SUMS and preserved_archive_entries.json verify unchanged publisher bytes and recorded ZIP CRC/size. The original independent audit directly parsed the acquired central directory. The portable replay omits that unused binary directory and checks the extracted selected-entry metadata instead; it does not claim to redownload or independently authenticate the archive. The publisher's complete-archive MD5 was never verified.

The runner makes a disposable copy before executing scripts. Exact JSON/CSV comparisons exclude only documented runtime, memory and path/script provenance fields where necessary. A successful exit plus PASS establishes a successful replay of this packet's specified checks, not broader scientific certification.
