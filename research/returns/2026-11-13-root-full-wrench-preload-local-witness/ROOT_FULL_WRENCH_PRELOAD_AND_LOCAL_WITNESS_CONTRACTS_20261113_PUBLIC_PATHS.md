ROOT full-wrench preload and local reaction-witness contracts
13November2026Brisbane/12NovemberUTC. Bounded mechanical models for useful connection exchange; no qualified device.

1. Why an external wrench and compliance need not certify internal members

ROOT executed ROOT_FULL_WRENCH_PRELOAD_AND_LOCAL_WITNESS_SCREEN_20261113.py. An introduced rigid plate connects through three identical isotropic point springs k=1MN/m on an equilateral ring r=.1m. Its linear rigid-body stiffness is diagonal:
(3e6,3e6,3e6,15000,15000,30000),
with translationalN/m and rotationalNm/rad units.

UnderFz=1000N,Mx=250Nm, its relative translation is.333333mm and rotation.0166667rad=.95493degree. Net point reactions alongz are333.333,1776.709,-1110.042N. Thus the imposed resultant-force envelope does not itself bound each local member force.

Split EACH point spring into two half-stiffness branches. With no hidden preload their individual force magnitudes are166.667,888.355,555.021N, each appearing twice. Now add equal-and-opposite700N axial preload within each pair. The complete net reaction at each point, external six-component wrench and complete linear stiffness stay unchanged, while branch magnitudes become:
866.667,533.333,1588.355,188.355,144.979,1255.021N.
For an introduced1000N individual-member limit, the unpreloaded system passes, each preloaded pair passes at zero external load, but the loaded preloaded system has two overloaded members. Identical exterior measurements do not imply identical internal capacity.

This has a concrete one-dimensional realization contract. For concentric/coaxial branches with matching force-law slopek and rest lengthsL0+P/k andL0-P/k:
k(L-L0-P/k)+k(L-L0+P/k)=2k(L-L0).
Their total force law is independent ofP for everyL in the assumed elastic range. Tensile/compressive branches, matching laws, attachment, compression stability and finite installation strains must actually be constructed. The equation does not supply those properties. If paired branch forces act at the same effective point their preload cancels locally, including its resultant moment. Finite spacing or a deliberately measured internal strain may expose it.

The script also contains a weaker frozen-geometry radial-preload illustration. That example explicitly neglects geometric stiffness; a real spatially separated preload can change tangent response and become observable. It must NOT be used as a general physical proof that all external stiffness probes fail. The opposed-pair cancellation is the more useful ambiguity construction. Both are ordinary restricted mechanics, not a universal sensor impossibility theorem or claimed new tool-changer technology.

The practical issue is that a structural controller must know which individual load path can fail. A whole-joint force/torque sensor may be insufficient even when all six components are observed. Internal preload, bypass paths and local force limits must enter the device model, measurement or physical constraints.

2. A possible physical witness and its quantified requirements

One constructive direction is to put an independently measurable, mechanically guarded flexure in a selected load path, and ensure no parallel contact bypasses the witness while it is being relied on. A designed open gap, with another verified support carrying the load, can provide a physically defined zero-reaction state for calibration. Free-space zeroing of a sensor does not establish a loaded fixture's friction or zero drift. The supporting bridge, actual gap, release sequence and return to service are paid operations.

An INTRODUCED rectangular cantilever flexure l30mm,w40mm,t5mm,E200GPa carrying2kN has:
I=4.16667e-10m4;
end stiffness9.25926MN/m;
nominal end displacement.216mm;
nominal root bending stress360MPa;
surface strain1800microstrain.
An introduced factor2 against nominal yielding therefore requires an actual material/preparation state with at least720MPa yield, before notch, clamp, cross-axis, fatigue, corrosion and fabrication allowances.

A total force uncertainty of5N corresponds to only4.5microstrain in this geometry. This is the complete error budget, not ADC resolution. An introduced uncompensated10microstrain/K thermal sensitivity alone would produce11.111N/K apparent force. Temperature compensation, hysteresis, adhesive creep, fatigue drift, wiring, excitation and calibration therefore cannot be omitted. No strain gauge, electronics or prepared material is supplied by this calculation.

This flexure is a single-force-path screen, not a three-axis load cell or a qualified1kN/250Nm exchange module. Several sensor axes and attachments change compliance and available access. Its result must not be spliced into the independently assumed rigid-plate model as a jointly validated device. Mechanical load limiting could be an alternative to sensing, but its actual force law, hysteresis, wear, stored energy and failed-lock behavior need construction.

A discriminating later experiment would impose the SAME exterior wrench on two assemblies with controlled opposite internal preloads, then compare whole-joint sensing with independent branch metrology. Operate the support-transfer sequence with unknown-to-controller preload and an apparent engagement failure, measuring whether it accepts an overloaded member. Deliberately changing branch contact, breaking the matched-law symmetry or measuring the guarded internal path can test when ambiguity disappears. Actual load fixtures, witness calibration, preload preparation, catching support, power loss and reset must be paid. No experiment has been executed or purchased.

3. Source/access scope

The parameters above are introduced. A completed dependent local identity/alias/hold check preceded the FIRST primary lookup of exact:
https://d1io3yog0oux5.cloudfront.net/_71375c3255dfa5f1bcebb6ff91bd4659/clevelandcliffs/db/1190/10503/file/CLF_ProductData_17-4-PHSS_052021.pdf
It returned not accessible via this tool. SAME Cleveland-Cliffs May2021 17-4PH product-data identity is HELD against retry, changed hash/host/version/provider/AKSteel/ARMCO/author/title/PDF/catalogue/export recovery. No governing material condition, modulus, yield, heat treatment, fatigue, manufacture or price passage was read. Search tables and remembered properties are not imported. This is not evidence against that material. No alternate bulletin was followed.

Every earlier known/unknown source/access/transfer hold persists, including the distinct new exact Srinivas2017 multistrand dynamical2017science PDF failure recorded in currentREADME. Existing NASA PASS and Capral scopes retain only their actual earlier read limits; they do not supply this witness module.

4. Executable scope

The owned script calculates both preload examples, point-force equilibrium,100 finite diagnostic probe comparisons and the flexure/error-budget equations. Script execution confirms the stated finite model outputs, not physical ambiguity across every nonlinear real joint, calibrated sensing, mechanical strength, life or a useful integrated invention.
