# Portable thermodynamic input certificate

The original HEAT_CONTRACT_CHALLENGE.md is retained unchanged. This supplement supplies reproducible inputs and closes its heat-capacity and speciation proofs. Run `python verify_thermo_bounds.py` and `python check_ledger.py` inside this directory; neither requires network access or third-party packages.

## Inputs and provenance
`inputs/nist_shomate.csv` contains the actual A–H coefficients, valid temperature intervals, exact official NIST URLs and retrieval date for N2, O2, NO, NO2. These were transcribed from the cited low-temperature coefficient columns. With t=T/1000, cp=A+B*t+C*t^2+D*t^3+E/t^2 in J/(mol K). All four valid intervals cover 298.15–500 K. This is a gas-phase frozen-composition calculation; condensation, dimerization, reactions or unlisted significant species are outside the certificate.

`inputs/digitized_experiments.csv` is an exact copy of the originally used electrodeless_evidence/digitized_experiments.csv, NOT the parent's observed_operation/digitized.json. Its SHA-256 is 38408e7153d30e5a561a827345483f78d0f8c32257a096b6912c2d7f95564dd8. `INPUT_MANIFEST.json` records both local-input hashes and original path. The verifier checks both hashes. Small differences from a separately selected graphical transcription are not concealed or reconciled. No redigitization was performed.

## Analytic interval proof, not a grid check
Cover t in [0.29815,0.5] by two closed intervals [0.29815,0.4] and [0.4,0.5]. For each interval [a,b], monotonicity of positive powers and reciprocal powers gives

    cp(t) <= A + sum over (v,k) of max(v*a^k, v*b^k),
    (v,k) = (B,1), (C,2), (D,3), (E,-2).

Every calculation uses Python Fraction on the exact decimal coefficient strings. Thus no untested point between samples remains. The respective interval upper bounds in J/(mol K) are:
- N2: 29.936386 and 30.449959.
- O2: 33.534180 and 35.328931.
- NO: 31.139044 and 31.189934.
- NO2: 45.241057 and 48.639076.

Displayed upper numbers are rounded upward to six decimals; exact rational results are saved in thermo_verification.json. Every bound is strictly below 50. The antiderivative A*t+B*t^2/2+C*t^3/3+D*t^4/4-E/t gives exact rational sensible enthalpy differences, multiplied by 1000 for J/mol: approximately 5910.727 (N2), 6083.997 (O2), 6057.331 (NO), 8098.948 (NO2). Each is below 50*(500-298.15)=10092.5 J/mol. Constants F and H cancel in these differences; using differences avoids small fitted reference offsets. Unchanged monatomic ideal argon has cp=5R/2<50; arbitrary inert species are NOT automatically covered.

## Product enthalpy monotonicity
Use the rounded tabulated formation enthalpies A=90290 and B=33100 J/mol as in the original ledger. These are intentionally distinguished from the slightly different Shomate-fit H constants. At fixed measured x and original F,

    Hchem(z)=F*[A*x+(B-A)*z]/(1+z/2),
    dHchem/dz=F*[(B-A)-A*x/2]/(1+z/2)^2 < 0.

The sign holds for every x>=0 because F>0, A>0 and B<A. Consequently z=x gives the minimum and z=0 the maximum used in the ledger. The verifier checks the derivative numerator and both exact endpoint identities on all eight pinned observations, plus the midpoint ordering. The algebra supplies the full continuous sign proof; the finite checks merely guard implementation.

## Measured execution resources, not research cost
The final successful exact-rational verifier took 0.065374126 s elapsed, 0.057297 s user CPU, 0.007594 s system CPU, and peak child RSS 9984 KiB. The portable eight-row ledger took 0.020867516 s elapsed, 0.004194 s user CPU, 0.016401 s system CPU, and peak child RSS 9344 KiB. These are single-run Linux child-process measurements, not stable benchmarks. Fresh wrapper executions used perf_counter and resource.getrusage(RUSAGE_CHILDREN); raw records and the measurement wrapper are included.

Total research, model inference, web lookup, tool overhead, other workers, and their memory/compute costs were not instrumented and are unknown. The very small arithmetic cost does not characterize those costs. The first verifier attempt failed because an integer zero entered a division as float; converting z to Fraction corrected the exact-comparison implementation. Failed-run output/resources are retained. This did not change the analytical proof or ledger values.
