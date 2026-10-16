# Existing equal-duty grid tests the scalar witness family

## Result

The final Figure 2 source contains exact equal-duty pairs. Its point values are inconsistent with N887's **shared-fixed-rate scalar family** across those protocols, conditional on comparable calibrated molar-flow regimes. This does not refute the theorem about endpoints plus one mean, and does not exclude general slow hidden states. No statistical significance is claimed: the source supplies no replicate identities or error bounds for these grid values.

## Primary values and definitions

Source: publisher MOESM20 XLSX, freshly downloaded, SHA256 47a571bed2750c89ba2cf38cc75235f1e7497727c57e2b9b28fc3fdfc667a3fe.
https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41557-026-02107-8/MediaObjects/41557_2026_2107_MOESM20_ESM.xlsx

The two sheets report conversion and selectivity for the same 30-condition (6 by 5) duration grid, not separate duration sweeps. Sheet Figure 2 c columns B,C,D are t1.5V / s, t-0.1V / s, Conversion / %. Sheet Figure 2 d has the same B,C durations and D=Selectivity / %. The following four rows all have h/d=10, with the same commanded +1.5/-0.1 V levels:

| Row | h seconds | d seconds | Period seconds | Conversion % (2 c!Drow) | Selectivity % (2 d!Drow) | Reconstructed ethane/Ain |
|---|---:|---:|---:|---:|---:|---:|
| 7 | 0.01 | 0.001 | 0.011 | 89.524 | 59.997 | 0.5969012737303532 |
| 13 | 0.1 | 0.01 | 0.11 | 88.031 | 72.211 | 0.3387701955380760 |
| 19 | 1 | 0.1 | 1.1 | 85.970 | 77.288 | 0.2526330918124418 |
| 25 | 10 | 1 | 11 | 82.298 | 78.329 | 0.2276908881767927 |

Exact condition cells are Figure 2 c!B7:C7, B13:C13, B19:C19, B25:C25; matching Figure 2 d B:C values were checked, not inferred. Conversion/selectivity pairs are D7/D7, D13/D13, D19/D19, D25/D25 across the respective two sheets.

Use the paper's branching definition S=a/(a+b), not conventional net selectivity. With X and S expressed as fractions and common molar-flow normalization, b/Ain=X(1/S−1). This is a conditional material-balance reconstruction, not native chromatogram-derived flux. No interpolation, mixing with preprint values, or use of the distinct Figure 2 b optimum row is involved. Primary final SI section 5 independently corroborates the unusual convention: its no-potential example gives conversion 89.3%, selectivity 35.1%, acetylene semi-hydrogenation 1.81e-5 mol/min and ethylene hydrogenation 3.35e-5 mol/min; 1.81/(1.81+3.35)=0.350775, matching the stated selectivity. SI Table 1 explicitly notes conversion of conventional net-selectivity literature values into this paper’s convention. The formula is therefore not a substitution of standard net selectivity.

For the requested longest pair, h=1,d=0.1 to h=10,d=1, ethane/Ain decreases by 0.0249422036356490, or 9.87289648% relative to the shorter waveform. Across all four, it decreases by 61.85451461%. The h/d=100 group independently declines: rows 12,18,24 at (0.1,0.001),(1,0.01),(10,0.1) s give 0.3490513704,0.2585536100,0.1955297537. Again, point differences, not error-bounded significance.

## Stronger than a slow-limit check

For fixed positive rates mu,lambda, fixed endpoints b+=1,b-=beta, and h=t h0,d=t d0, let P0=h0+d0, a=lambda d0, c=mu h0. The model's mean suppression relative to its static duty mixture is

F(t) = [(1−exp(−at))(1−exp(−ct))] / [mu t P0 (1−exp(−(a+c)t))]
     = 2 / [mu P0 t (coth(at/2)+coth(ct/2))].

The duty-mixture baseline (h0+d0 beta)/P0 is constant. Each term t coth(kt) strictly increases for t>0, because its derivative coth(x)−x csch²(x) is positive, equivalently sinh(2x)>2x. Therefore F(t) strictly decreases and the mean ethane rate strictly increases with absolute period. The observed point estimates decrease, the opposite sign. Unknown beta cancels in this fixed-duty comparison.

In the limiting lambda/mu=k, mu→0 regime, suppression is duty-only and hence equal across these periods. That limit also fails the distinct point values. Allowing new independently chosen mu/lambda for every waveform would evade the check by abandoning a shared physical model; the one-mean theorem permits those independent witnesses, but it does not supply a joint mechanism.

## Qualification and next consequence

Same commanded levels do not guarantee identical effective interfacial fields or rate laws at millisecond versus second pulses. Electrical settling, local gas composition, membrane state, different samples or histories, flux calibration and nonrepresentative averaging can invalidate the fixed-rate comparability premise. The only acquired dense electrical trace is the separate h=10,d=1 protocol; no matched dense trace for every pair was acquired. Grid uncertainty and calibration covariance are missing, so a formal error-aware rejection remains unquantified.

Nevertheless, the existing grid is already a substantive diagnostic. Do not use N887's arbitrarily slow family as an explanation of the full Xu dataset without confronting this reversal. Broader causal nonidentification and the need for controlled fresh-carbon/common-hold measurements remain. No general multimode conditioning or washout bound follows from this model-class mismatch.

Own reproducible calculation: check_equal_duty.py. Structured exact pairs: equal_duty_results.json. No acquired code executed.
