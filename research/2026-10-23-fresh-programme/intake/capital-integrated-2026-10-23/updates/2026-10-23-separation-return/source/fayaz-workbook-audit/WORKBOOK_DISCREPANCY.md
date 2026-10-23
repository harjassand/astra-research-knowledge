# Governing arithmetic discrepancy in a candidate ordinary comparison
23 October2026,09:28UTC. This note postdates the frozen separation-return v1ZIP.

Question: Can a measured compartment/atmosphere intervention establish a credible high-conversion aqueous-iron operation, instead of assuming partial-reduction efficiency is metal-production efficiency?

Primary: Fayaz et al., ChemElectroChem2023 e202300451, DOI10.1002/celc.202300451. Actual producer workbook/code/data: https://doi.org/10.5281/zenodo.10036927. SI: https://doi.org/10.5281/zenodo.8388660. The publisher Table2 reports98.5% efficiency and10.16GJ/t for nickel/H-cell/argon, compared with80.2% and12.27GJ/t for the simpler nickel-iron/beaker/air case. Those reported boundaries exclude complete preparation and auxiliary supply. They are not full plant energy. Source reference and metadata files are preserved, not edited.

## Direct workbook observation
Sheet8, H-cell/argon row5:
F5=4085 C; G5=.98g theoretical Fe (hardcoded); C5=89.3 wt%; E5=1.08g final sample; H5=C5*E5/100=.96444g Fe; I5=H5/G5*100=98.4122449%; J5=2.4V; M5=F5*J5=9804J; O5=10.1654846GJ/t.
For Fe(III) to Fe(0), m=Q*MFe/(3F). Taking F=96485.33212C/mol and MFe=55.845g/mol,4085C corresponds to .7881226434g, NOT .98g. The same inferred product then implies122.3718171%. .98g theoretical Fe instead requires5079.5393756C. This is an internal charge/mass inconsistency, not a small rounding uncertainty. It does not establish physical Faradaic efficiency above100%, misconduct, or which source field is wrong.

## Independent execution, not producer replay
Six released H-cell/argon ASCII records acquired with published MD5 identity checks. Own streaming trapezoidal integration, no producer code execution. Column2/column3 ratios consistently correspond to6cm2, with column2 current(A) and column3 density(A/m2) inferred from source plotting labels and magnitudes. All records span about20h. Actual full-trace charge values(C):4265.0226,1842.5861,4213.4032,6576.7211,4319.9467,2385.7188, average3933.8998. This does not reproduce4085C or the5079.54C needed by G5. No per-run mass/phase pairing supplied in the workbook, so an unweighted trace mean is NOT a corrected production efficiency.

Ar4 has strongly rounded time strings, with716630 repeated adjacent time values. Literal trapezoidal integration is reported; original higher-resolution time uncertainty is not reconstructed as fact. Other records have no repeated/nonmonotone times. No source trace dropped to make an average fit. Full records and checksums retained. Original acquisition costs and independent parse wall/RSS receipts are separate.

Producer plotting code uses column3 for Ar1/Ar6 but column2 for Ar2–Ar5 before averaging the six as a current-density curve. Raw columns have an approximately1666.67 conversion factor, so that curve mixes units. This is distinct from the workbook's hardcoded theoretical mass. Correcting the plot alone cannot repair the endpoint mass/charge pair or the reported energy.

## Physical interpretation
Do not choose the membrane/argon construction on its headline98.5% alone. The observed reduction/atmosphere response survives as a source observation; its quantitative best-case efficiency requires corrected paired data. A specific ordinary competitor, nickel-iron/beaker/air, avoids the added membrane and argon. Its own charge record is being checked separately, rather than assuming the best-case defect invalidates every arm.

Even a corrected electrolysis-energy ranking would not settle full useful operation: account for sintering, heating, argon supply, membrane preparation/replacement, electrolyte/water recycle, sample cleaning, isolated metal and residual-oxide inventories. Product phase wt% and recovery of original feed iron are different. These are requirements for a total operation, not excuses to erase narrower demonstrated electrochemical reduction.

## Strong ordinary control checked,09:30UTC
Both released Ni/Fe-beaker-air current traces independently integrated with NumPy trapezoidal quadrature:5880.39610C and5001.56103C,mean5440.97856C. The workbook5405.5C differs0.66%, possibly endpoint/averaging treatment; no silent correction assigned. Unlike best-case row8, its stored theoretical mass1.043g agrees with Faraday's law(1.04288787g) at the stated workbook charge. The endpoint.8397675g corresponds to80.5233% using workbook charge, or79.9982% conditionally using the unpaired raw mean. Thus this ordinary control survives the charge-mass check. Full-cell energy, original-feed recovery and per-run uncertainty still are not independently verified. The reported best-case discrepancy does NOT invalidate the existence of useful aqueous iron reduction.

Decision: retain the simple Ni/Fe-anode aqueous operation as the strongest source-admitted starting comparator in this retrieved experiment. Do not select added membrane/argon on the internally inconsistent headline. Do not transplant its efficiency into dilute silicate/goethite or raw-ore operation. Next decisive evidence is paired retained-metal assay/current/voltage and auxiliary gas/heat data at an impurity-bearing feed, or a source-identified intervention that changes the final reduction step. Current source contains no complete matched plant comparison. No job remains running after these finite calculations.
