# Independent global no-anchor integration review

I independently checked the proposed four-branch integration and reran global_integration.py successfully. This is not an independent implementation of every scalar.

If no solid plus run of length2R+1 exists, every cyclic horizontal/vertical plus run has length at most2R; a full plus row/column would already contain an anchor and is excluded. Horizontal counting gives Nplus<=R*P_horizontal and vertical counting gives Nplus<=R*P_vertical. Adding yields Nplus<=R*P_total/2. Thus the ORIGINAL source weight relative to all-minus is at most exp(-4P_total), with no restriction on contour homology.

For a nonempty essential-wall set in the same deterministic adaptive encoding, embedded essential cycles are parallel and the total boundary homology is zero modulo2. A primitive curve is nonzero modulo2, so there are at least two cycles, each physical length at least L. Therefore P_total>=2L. A perimeter tilt1/2 and the FULL refined contour pressure at tension3.5 give mass and occupation/ZA at most2 exp(A3.5-L). Exact short-loop counts n at perimeter4 and2n at perimeter6, with100n3^p only from8 onward, remain paid; this is not a single-contour approximation.

Reading A3.5_exact from refined.json independently yields conservative exponents638,1595,7912,71308. They all dominate the chosen anchor exponents515,1521,4423,33296. The other no-anchor background branches remain2038/5122/25688/256367 and903/2257/11224/104428. Four positive branches cost less than exp(2), yielding full outside-F occupation exponents513,1519,4421,33294.

The essential-wall branch now uses a conditional no-anchor mass estimate, not the old unconditional winding-current bound. This is a legitimate source-set partition, not a change of source, core, voltage, rate or target. F remains a comparison downset containing original A, and F-minus-A normalizer error remains explicit. No relative capacity estimate or uniform growing-R theorem follows.
