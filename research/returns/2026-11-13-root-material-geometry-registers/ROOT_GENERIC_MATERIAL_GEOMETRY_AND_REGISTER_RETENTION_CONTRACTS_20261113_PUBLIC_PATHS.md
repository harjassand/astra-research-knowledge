ROOT MATERIAL GEOMETRY, GENERIC RAIL FEED AND FROZEN REGISTRATION CONTRACTS
13 November 2026 Brisbane. Science, source scopes and introduced physical models.

1. The operation under examination

A physical forming head would take the SAME generic material inventory and write a useful load-bearing spatial geometry, then recover and rewrite that inventory. This is different from manufacturing a shape-specific strip first and repeatedly deploying its already encoded shape. Both can be useful; the second does not supply the first operation.

The geometry model below constructs ONLY an ideal planar differential-feed kinematic interface. The segmented-register stiffness and homogeneous intact-tape storage calculations are SEPARATE surrogates; no common material/interface architecture combines their favourable properties. A real adjustable register, cross-link, forming head, loaded release/reacquisition sequence and renewed stock are not supplied. Equal-pitch, one-to-one closure of undeformed identical rails cannot acquire unequal offset-curve lengths from motor commands alone. Sliding, elastic strain, alternate pairing or a different physical organisation could supply those lengths, but must itself be constructed. This is not an all-zipper or all-construction impossibility result.

2. Introduced constructive kinematics

Take three rail centroids at equilateral-section radius r=25 mm. In one bending plane their offsets are y=(25,-12.5,-12.5) mm, with S=sum(y_i^2)=0.0009375 m^2. For an untwisted planar centreline of curvature kappa(s), a parallel rail has dL_i=(1-y_i*kappa) ds when 1-y_i*kappa>0. This is an exact planar offset-curve length relation in the declared geometry, not a three-dimensional contact or material theorem.

A shared head with 50 stations over 1 m, at 20 mm centreline pitch, could encode:
- Straight: feeds (1,1,1) m and endpoint (1,0), angle zero.
- Quarter-turn: constant kappa=pi/2 per metre; feeds (0.960730092,1.019634954,1.019634954) m; endpoint (0.636619772,0.636619772) m and angle pi/2. The largest local departure from equal-pitch feed is 0.785398 mm, or 3.92699%.
- Opposite-curvature halves: kappa=+2 for the first 0.5 m and -2 for the second. ALL total rail feeds are 1 m, yet the endpoint is (0.841470985,0.459697694) m with zero final angle. The local feed departure reaches 1 mm, or 5%.

The inverse kappa_j=-sum_i[y_i*(dL_ij-p)]/(p*S) reconstructs these introduced profiles to 3.78e-15 per metre; endpoint arithmetic discrepancies are at most 1.55e-15 m. These are numerical consistency checks, not physical accuracy, useful-device function, a new inverse-design algorithm or fabrication validation. The same-pitch constraint is restricted to the explicitly undeformed one-to-one registry, not every reconfigurable strip.

3. What a feed record can and cannot observe

In a discrete register-rest-length surrogate introduce errors of +/-20 micrometres per station. This is not a derived slip law for an uninterrupted tape. Opposite errors in the two halves conserve every total rail length. The constructed history has exactly correct final feed totals and essentially zero final angle, but a 13.33307 mm endpoint position error and 0.5 mm maximum interior accumulated phase error. It is a coherent geometric rest-length example, not evidence that an actual tape/clip assembly can realise that slip history under its force and continuity constraints.

A stronger observation can avoid this accumulation. If the ACTUAL cumulative material phase e_i,j is bounded by epsilon at EVERY frozen checkpoint, with initial phase known, then station errors are e_i,j-e_i,j-1. The integrated angular error telescopes:
  |delta theta_j| <= epsilon*sum_i|y_i|/S.
With epsilon=20 micrometres, the all-prefix angular bound is 0.001066667 rad and the 1 m position bound is 1.066667 mm. The finite example gives 1.05600 mm. All eight phase-sign corners reproduce the analytical angular bound.

Thus end-of-run spool counts alone do not authenticate interior geometry, while suitably measured material registry at each checkpoint could be an accumulating physical control. Commanded motor position does not establish actual material registry after slip, tension-dependent strain, temperature changes or post-lock relaxation. No sensor, calibration, harmless probing operation or continuing bound is installed by this calculation. Alternative direct shape measurement remains possible.

4. A separate segmented-register load-path screen

For a SEPARATE deliberately segmented axial-rail surrogate introduce E=70 GPa, width 20 mm and thickness 0.6 mm: EA=840 kN per rail. No source material is fitted by these values. Give EACH segmented rail a serial axial register spring of stiffness k at every station of pitch p=20 mm. This is NOT a constitutive law for an uninterrupted tape held only by external clips; a continuous-ribbon design needs its actual shear-transfer and boundary analysis. The two topologies cannot silently inherit each other's stiffness or storage properties. In the declared serial-joint surrogate a segment has axial compliance p/EA+1/k, so
  EA_eff = 1/(1/EA+1/(k*p)),
  EI_eff = EA_eff*S.
This separates the intact-rail stiffness from the stiffness of the actual written and retained registry.

For a straight, fixed-base 1 m cantilever with a 20 N transverse tip load:
- Rigid ideal registers: EI=787.5 N m^2; linear tip deflection 8.46561 mm.
- k=1e8 N/m per rail/station: EI=554.577 N m^2; linear tip deflection 12.02116 mm.
- k=5e8: EI=726.476 N m^2; linear tip deflection 9.17672 mm and bending strain energy 0.0917672 J.
- The introduced 10 mm load-deflection limit alone needs k>=2.31724e8 N/m with the other values fixed.

The script also prints softer-register screening cases and linear Euler values. Large-deflection rows leave small-deflection validity and are not nonlinear predictions or buckling certificates. The load calculation does not qualify the programmed curved profiles.

The 20 N m base moment requires rail forces (533.333,-266.667,-266.667) N in this axial-rail model. Their one-pitch changes due to the 20 N shear are only (10.667,-5.333,-5.333) N; the small force increment is not permission to ignore the much larger carried axial forces. Cross-link strength, slip, torsion, local instability, snap-through, lock opening and the forming transition under these forces remain unconstructed. Even a conditional load-deflection pass leaves independent shape error and every other deformation/cost term to pay.

In a separate homogeneous intact-tape storage calculation, introduced density 2700 kg/m^3 gives 97.2 g for three bare rails. This excludes all locks, cross-links, feed head, reels, drives, sensing, base, power, stock preparation and renewal. A flat 0.6 mm rail coiled at 50 mm radius has an introduced outer-fibre strain of 0.006 and linear-elastic stress 420 MPa at E=70 GPa. No yield or fatigue allowance is supplied. Introduced stress ceilings of 100/200/400 MPa would require coil radii 210/105/52.5 mm. Flexible/articulated rails could change this trade, but their closed-state structural stiffness is then a different physical construction.

5. Actual strong fabrication predecessor

Goshtasbi et al., Weld n'Cut, arXiv:2502.06361v1, 10 February 2025.
Actual metadata was verified BEFORE the versioned HTML:
https://arxiv.org/abs/2502.06361
https://arxiv.org/html/2502.06361v1
Actual main lines40--106, including Materials/Methods and Results/Discussion/Conclusion, read. The authors combine a 500 W ultrasonic welder and oscillating knife on a CNC gantry. External PTFE sheets protect placed fabric; magnets hold the stack. No removable INTERNAL masking sheet is needed. Welding speeds depend on fabric weight (200/160/100 mm/min for selected lightweight/medium/heavy textiles). They fabricate different inflatable motions and test particular pressure ramps and a small lifting example. They explicitly leave automatic connector attachment and protecting reusable PTFE during cuts as future operations.

This is an existing automated cut-and-bond construction, not a newly invented generic-film factory. A 1 m path at the reported medium-fabric welding speed alone takes 6.25 min; this arithmetic excludes placement, cutting, ports, testing and tool renewal. The previously read Decker separator-withdrawal operation is specific to that process, not a universal obstacle to inflatable fabrication. Linked code, equipment pages, videos, figures and cited originals were not followed or executed. No whole-cell cost, long life or autonomous complete-production yield is supplied.

6. Other actual exposures and source-access limits

Baines--Patiballa--Kramer-Bottiglio 2021, Rapidly Reconfigurable Inextensible Inflatables, DOI10.1109/RoboSoft51838.2021.9479435:
https://www.eng.yale.edu/faboratory/publications/conference/2021/Baines%20et%20al.%20-%202021%20-%20Rapidly%20Reconfigurable%20Inextensible%20Inflatables.pdf
Initial actual main pp0--1/lines0--149 read: prepatterned conductive-fabric heaters use vacuum compression for internal seal formation and heating/inflation for release; perimeter, port and leads are prepared. The text identifies lead-count/precision costs. FIRST governing followup145 returned400Timeout. Later peel data, detailed controls, cycles, FEA and limitations UNREAD. The initial described reversible-sealing construction is not a qualified rewritable pressure vessel or arbitrary generic-stock geometry machine.

Rezanejad et al. 2026, Vacuum--Laser Fabrication of Programmable Soft Actuators, DOI10.1002/advs.202522500:
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202522500
Actual initial intro through183 read; FIRST governing followup184 returned400Timeout. Main manufacturing2.1 onward/Methods/test maps/SI UNREAD. Abstract production/material-cost/response/pressure numbers are not imported as jointly qualified operating premises.

Collins--Yim, Design of a Spherical Robot Arm with the Spiral Zipper Prismatic Joint:
https://www.modlabupenn.org/wp-content/uploads/2017/12/collins2016spiralzipper.pdf
Actual initial main pp0--2/lines0--258 read: helically interlocking strip/slider, tension/moment play and tethers to maintain compression, geometric feed and drive organisation. FIRST governing followup258 returned400Timeout. Later build/test/force/mass/life data UNREAD. The file labels an accepted ICRA2016 article while pointing to DOI10.1109/URAI.2016.7487363; that bibliographic label discrepancy is preserved. Cited commercial predecessors are not original manufacturer reads.

Li et al. 2026, Y-zipper: 3D Printing Flexible--Rigid Transition Mechanisms for Rapid and Reversible Assembly:
https://hcie.csail.mit.edu/research/y-zipper/y-zipper.html
The author's project main0--205 was read in the initial request set: shape-specific printed strips, manual slider priming, moving/fixed actuation, pre-encoded spatial primitives and the author's descriptions of load/fatigue evaluations. These remain project-page descriptions, not read paper Methods or transferable structural ratings. FIRST supported PDF click:
https://groups.csail.mit.edu/hcie/files/research-projects/y-zipper/y-zipper.pdf
returned400Contentlengthtoolarge28642262bytes. No governing paper-PDF passage read. No autonomous generic-stock shape rewriting or complete fault-recovery apparatus follows from the project description.

Each of these FOUR failed identities is HELD against further lookup/retry/URL-normalisation/alternate author, host, provider, version, title, PDF, component/range/compression, SI, image, video or export recovery. No inaccessible passage is reconstructed from search snippets or memory. Earlier read scopes remain only at their actual exposure. Failures are access/observation limits, not scientific negative evidence. All earlier known/unknown source/access/transfer holds persist.

7. Executable ownership and scope

ROOT_GENERIC_RAIL_GEOMETRY_WRITING_AND_REGISTER_RETENTION_SCREEN_20261113.py
9603 ASCII bytes; SHA256 dba01e57cc4c00dc8ef9b9454e9a3badd00d9efe761f0de338f1640ae83a62b1.
ROOT_GENERIC_RAIL_GEOMETRY_WRITING_AND_REGISTER_RETENTION_SCREEN_20261113.json
8654 ASCII bytes; SHA256 531d820cf7f25e704b4d741d23c0c568211e3da1ba487a53b54d07c25ec57f67.
Both are ROOT-owned independent introduced calculations. No producer code, report, archive or linked artifact was recovered or executed. No qualified material, adjustable clamp, actuator, installed sensing, manufacturing head, working structure, autonomous renewal or comparative operational advantage has been established. These contracts can inform further physical mechanism research without granting an unconstructed interface.
