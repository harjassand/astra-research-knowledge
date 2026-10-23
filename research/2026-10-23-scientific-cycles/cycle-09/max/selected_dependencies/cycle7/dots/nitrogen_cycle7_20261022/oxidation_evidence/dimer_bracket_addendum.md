# Dimer bracket adjudication

2026-10-22. Restricted evaluated model, not a claim of measured outlet composition.

The IUPAC NOx23 evaluation does **not** prescribe a product-inhibition term. Its preferred-value discussion reports insensitivity to added NO2; its Mahenc experimental annotation also reports independence from NO2/N2O4. Its warning about dimerization requires accounting for product detection and molecular inventory, not addition of an inhibitory term. Older composition-dependent reports are not the adopted evaluated model.

For initial NO/O2/N2 only, let total feed be F0, inlet NO fraction a, O2 fraction b, NO conversion X, and D=F_N2O4/F0. Then:

F_NO/F0=a(1−X)
F_O2/F0=b−aX/2
F_NO2/F0=aX−2D
0≤D≤aX/2
Ft/F0=f=1−aX/2−D
1−aX≤f≤1−aX/2.

With C=P/(RT), event k in concentration-consistent units, and ideal gas:

dX/dV = [2k C³ a/F0] (1−X)²(b−aX/2)/f³.

Therefore, for b−aX/2>0 and X<1:

F0/(2k C³a) integral_0^X [(1−az)³/((1−z)²(b−az/2))] dz
≤ V(X) ≤
F0/(2k C³a) integral_0^X [(1−az/2)³/((1−z)²(b−az/2))] dz.

This pointwise endpoint bracket requires no dimerization constant and remains true if D varies arbitrarily along the permitted interval. The lower-volume endpoint is complete dimerization; upper is no dimerization. It bounds volume for a given NO conversion, not monomer NO2 yield.

At298K use IUPAC tabulated k=3.95e−38 cm6 molecule−2s−1 and stated Δlog10k=±0.2. Algebraically k_lo=2.4922815107e−38 and k_hi=6.2603281102e−38. For a combined evaluated reliability/speciation envelope, use k_hi in the lower-volume integral and k_lo in the upper-volume integral. This is an evaluator-reliability/model envelope, not a confidence guarantee, and does not cover arbitrary unmodeled side chemistry.

For20standardL/min at22.414standardL/mol, F0=20/22.414/60=0.0148716576mol/s. Temperature and pressure of that declared standard reference need not equal reactor conditions; use reactor298K and1bar in C. Verify endpoint input definitions in the parent calculation.

Source attribution: IUPAC Subcommittee for Gas Kinetic Data Evaluation, NOx23, last evaluated2017, https://iupac-aeris.ipsl.fr/datasheets/pdf/NOx23.pdf . Rate-convention guide official indexed text available; direct guidePDF returned404. Original Hisatsune full text not independently inspected. No numerical equilibrium constant is asserted here.
