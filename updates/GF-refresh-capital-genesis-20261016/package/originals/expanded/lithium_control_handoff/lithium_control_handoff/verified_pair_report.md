# Verified Figure 4c binary comparison

## Result
The exact named 179.6 mg CC and 4 s discharge / 8 s rest files are decodable and reproduce the workbook. The negative-stage dose is unequal: CC 2.87215 mAh (10.3397 C), versus P4-8 1.38684 mAh (4.99264 C), a ratio of 0.48286. These are sums of negative recorded charge increments, not net charge after subtracting positive increments, Li-specific charge, ICP yield, or Faradaic efficiency. CC net negative charge is2.83675615 mAh; P4-8 net negative charge is1.38684370 mAh, giving a separate net-charge ratio0.48888. Within a stored interval, unresolved positive/negative current fluctuations cannot be separated.

CC includes galvanostatic discharge followed by a long negative-potential hold. Comparing the pulse dose only with CC galvanostatic discharge gives 0.62525, still unmatched. The prior statement that whole-run charge cannot be reconstructed is now superseded for these two files. A complete instantaneous-current reconstruction is still unavailable; energy estimates require the voltage-configuration and quadrature qualifications below.

## Exact provenance and validation
Workbook: `figure 04/analysis/raw data.xlsx`, Figure 4c.
- CC: A/B full time/voltage; AH/AI current excerpt. Filename `Ch1-20251103-LFPC-duo-179,6mg, non-pulsed method_C01.mpr`.
- P4-8: T/U time/voltage; AT/AU current excerpt. Filename `Ch1-20251107-LFPC-duo-179,6mg, pulsed method-4s discharge 8s rest_C01.mpr`.
Both read from the LFPC-duo-pulased subfolder; the latter also exists one folder above. Filenames and signal correspondence establish plot linkage, not sample/ICP linkage or identity of initial electrode state.

All 51 CC and 176 pulse current excerpt points match 3600*dq/dt to <8.4e-8 mA and their timestamps to <1e-11 s. All 489 CC voltage points match. All 2866 exported pulse voltage points match; that export begins at 1800 s and omits the first 18 binary points. Maximum voltage mismatch <1e-15 V, time mismatch <1e-10 s. Hence exported current values are mA, despite the workbook header '<I>/mA/mg'. Protocol Is=-1.796 mA independently corroborates scale. Filename 179.6 mg corresponds to nominal 10 mA/g; template active mass 7000 mg is not used to normalize.

No installed galvani/eclabfiles/yadg/ixdat parser was available. Wrote a narrow reader for the observed layout using field-layout documentation in the primary galvani source https://raw.githubusercontent.com/echemdata/galvani/master/galvani/BioLogic.py . No acquired source executed, no installs, no pickle. This is independently verified reverse-engineered parsing, not manufacturer-certified decoding. The file uses v2 module headers and v0 data with u16 IDs at offset6, data offset1007, 49-byte records. The modern IDs467/468 must be retained; byte-slicing them would silently alias older IDs.

## Measured stages
CC:
- Preparation: first recorded point0.0482 s to negative-stage start142.779596 s. Accumulated positive charge0.2082746 mAh. This is preparation, not product recovery.
- Constant negative-current phase142.779596–4665.111690 s:4522.332093 s;2.21806312 mAh=7.98502724 C;mean1.76568794 mA.
- Negative-potential hold approximately4665.112890–8018.198249 s (first transition interval included in table):3353.08656 s;negative0.65408499 mAh, positive0.03539196 mAh, net-negative0.61869303 mAh. Last three recorded intervals are positive charge at negative potential; do not erase them.
- Combined negative protocol:7875.418653 s;negative2.87214811 mAh, net-negative2.83675615 mAh. Whole acquisition8018.150049 s.

P4-8:
- Preparation0.0482–2964.827325 s:2964.779125 s, positive1.20570460 mAh. Distinct preparation dose versus CC; not matched initial state established.
- Negative protocol2964.827325–11529.184207 s:8564.356881 s, negative1.38684370 mAh=4.99263733 C, mean0.58295531 mA.
-714 pulse starts. Stored start-to-end negative pulse intervals sum2855.71356 s. Last pulse ends11524.968607 s; file ends4.2156 s later during rest. Do not replace this realized count by programmed1000 cycles. Whole acquisition11529.136007 s.

## Charge integration and boundary handling
Use recorded cumulative Q differences at each interval, rather than trapezoids on sparse exported current points. The separate dq field exactly reconstructs exported mean-current values within ordinary intervals but drops charge at some transitions. Across preparation-to-negative transitions, cumulative Q contains an additional0.0221900 mAh CC and0.0213256 mAh P4-8 not represented by the transition-row dq alone. In the pulse negative stage, cumulative increments exceed the sum of negative dq by0.000137115 mAh (0.0099%), principally small pulse-to-rest transition increments. Sum-negative-dq is1.38670659 mAh versus cumulative1.38684370 mAh. The first pulse starts with tiny−4.72e-8 mAh dq embedded in a larger positive preparation interval; the reported cumulative stage starts at that row and omits that tiny increment. Acquisition has no complete current waveform within these transition gaps.

These are total electrochemical charge, including capacitive and any competing-ion/side-reaction contributions. Charge does not establish recovered Li. No recovery-file linkage or species inventory inferred from folders. In particular positive preparation charge cannot be counted as recovered product.

## Energy: configuration-dependent electrical-work quadratures
Primary methods section2.4 describes the extraction channel between working and YP-80F counter electrodes, a separator/membrane and two current collectors; no third reference electrode is described in that extraction paragraph. Source: https://pubs.acs.org/ascecg/article/doi/10.1021/acssuschemeng.6c04447/5448237/Selective-Electrochemical-Lithium-Ion-Extraction?searchresult=1 . This supports the reported two-electrode configuration without confirming instrument lead wiring.

The files retain Ewe. Instrument settings say "Electrode connection: standard", "Potential control: Ewe", and CE–WE compliance±10 V; they do not explicitly document reference-lead wiring. In the paper's reported two-electrode extraction configuration, Ewe may represent WE–CE cell voltage if the reference lead is tied to CE. The field name alone does not establish a different electrode-reference voltage and must not be used to claim cell voltage is absent. Conditional on that configuration applying to these traces, weighting cumulative charge increments by left/right stored Ewe estimates cell electrical work; otherwise these remain Ewe-referenced electrical-work proxies. These are alternative quadrature estimates, not rigorous energy bounds:
- CC negative protocol signed Ewe work1.07025/1.07593 mWh; absolute Ewe work1.17057/1.17077 mWh.
- P4-8 negative protocol signed Ewe work0.19730/0.21725 mWh; absolute Ewe work0.28779/0.29623 mWh.
Ewe can change sign; signed and absolute quantities differ. These quadratures alone do not establish full-process-energy cost, energy-per-recovered-Li, or net energy savings; they do not include auxiliaries or establish matched recovered output. Pulse4s voltage transients are not fully sampled; quadrature disagreement understates possible unresolved-waveform error.

## Artifacts
`recover_mpr_pair.py`: narrow reader; `verify_pair.py`: workbook comparison; `quantify_pair.py`: stage integration. `CC_decoded.csv`, `P4-8_decoded.csv`: decoded fields. `verified_pair_metrics.json`: exact filenames, hashes, stages, charges, quadrature estimates.

## Conclusion
This closes the two-file dose/elapsed-time question and strengthens the unmatched-dose caution. It does not validate causal rest benefit, a novel control schedule, matched-SOC superiority, product recovery, or total-energy superiority. Stop at this verified pair; no need to decode other487 files.
