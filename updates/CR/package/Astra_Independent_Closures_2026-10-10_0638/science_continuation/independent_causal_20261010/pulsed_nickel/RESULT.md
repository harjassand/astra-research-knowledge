# Result: no new catalyst mechanism identified

Primary source: Greenwell et al., JACS 145, 15078–15083 (2023), https://doi.org/10.1021/jacs.3c04811; open article https://pmc.ncbi.nlm.nih.gov/articles/PMC10360055/.
Public raw archive: https://doi.org/10.17638/datacat.liverpool.ac.uk/2272, actual file https://datacat.liverpool.ac.uk/2272/1/DataCat.zip.

The paper already attributes pulsed selectivity to oxidation/regeneration of a poisoned Ni-cyclam intermediate. It also shows an approximately Cottrell-like anodic transient. Neither is new here. The distinct candidate tested here was that a *finite pulse leaves a spatial diffusion profile* that predicts the shape of the following cathodic transient as the pulse duration changes.

## Frozen comparison
- Discovery: all three -0.3 V, 0.2 s pulse runs, fixed elapsed-time interval 1,800–3,600 s.
- Validation: -0.3 V pulse durations 0.04 and 1 s, same interval.
- Cathodic time fixed at 5 s; comparison grid 0.2–4.8 s after the anodic pulse.
- Only scale and offset come from two prespecified endpoints in each trace. This is a conditional shape prediction, not prediction of absolute current.
- The local-reset alternative uses tau=0.415123 s, fixed from discovery runs 1/2. No validation shape parameters are fitted.
- Phase bins use timestamps modulo the prescribed period; voltage is not recorded in the deposited files.

## Results
Normalized RMSE on the 22 interior points (diffusion versus fixed exponential):
- Training 0.2 s run 1: 0.0372 versus 0.0403
- Training 0.2 s run 2: 0.0318 versus 0.0389
- Validation 0.04 s run 2: 0.1153 versus 0.0756
- Validation 0.04 s run 3: 0.0854 versus 0.0644
- Validation 1 s run 1: 0.0326 versus 0.0259

The ordinary fixed-timescale reset model predicted every usable held-out duration profile more closely. This defeats a claim that the cross-duration data favor the proposed finite-pulse diffusion-memory law. It does NOT uniquely establish a surface-inventory reaction: ordinary reaction/transport mixtures remain compatible.

## Acquisition limitations, reported rather than imputed
Training run 3 has no resolved positive anodic phase; its phase-dependent range is only 0.23 microamp against approximately 1.48 microamp within-phase noise. It cannot inform the imposed sub-cycle current transient.

The 0.04-s validation run 1 has zero samples in most prespecified phase bins. The 1-s validation runs 2/3 are sampled at 0.8-s spacing on an offset grid and have zero samples on all prespecified 0.2-s grid targets. They are not silently interpolated into additional validation data. The three usable held-out runs have approximately 44–45, 357–358, and 300 observations per phase bin, respectively.

No formal significance test is claimed. Within-run cycles are correlated and are not independent experimental replicates. Unknown measured-voltage timing, stirring, mixed Faradaic currents, and reporter-free chemical-state uncertainty prevent elementary-mechanism identification. No optimization was pursued after the failed cross-duration comparison. The FE product-selectivity tables and other voltage conditions remain unexamined.

Files: preanalysis.md records the original hypothesis/split and the training-only acquisition decision; train_results.json, validation_results.json, acquisition_audit.json contain all reported numbers; extract_trace.py and analyze_*.py reproduce the calculation using system Python NumPy/SciPy. Plots are diagnostic only.
