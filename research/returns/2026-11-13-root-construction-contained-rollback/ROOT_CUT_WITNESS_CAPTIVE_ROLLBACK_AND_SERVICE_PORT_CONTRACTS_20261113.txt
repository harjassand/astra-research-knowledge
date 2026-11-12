ROOT physical-cut witness, captive rollback and service-port contracts
13November2026Brisbane/12NovemberUTC. Independent conditional mechanics and source constructions; no physical execution or qualified invention.

1. Available engineering constructions and remaining operations

The P1 available load-transfer return proposes six axial bypass legs, each with two independently operable release/catch stages, two service-joint families, individual force observations and three local pads on each opposing face. The P2 available construction return proposes separate pin-plane and remote shank observations, controlled proof/unloading and finite bypass/tool stocks. Both preserve the distinction between a connection's commanded state and the actual path carrying force. Their hardware, installed errors, complete trajectories and repeated physical service remain unconstructed.

The P1 model's72 gap channels follow from6legs*2stages*2faces*3pads. Its direct measurements do not by themselves exclude sidewall, wire or tool bridges. A positive gap needs a topology in which every admitted force-carrying contact crosses the observed cut. P2's remote witness rejects several false-seat classes but an actively counterheld jam can leave the remote shank unloaded while the failed connection remains internally loaded. These are different evidence contracts.

2. Original six-axis reaction and deadband calculation

ROOT executed OWN ROOT_CUT_WITNESS_CAPTIVE_ROLLBACK_AND_SERVICE_PORTS_20261113.py, pure Python standard library, independently of producer code. Reconstructing the P1 alternating-radius six-leg geometry from its available main return gives lengths.377140705/.403513569m and exact linear wrench matrix W, with columns(n_i,B_i cross n_i).

Over simultaneous Euclidean balls ||F||<=1000N and||M||<=250Nm, row_i(W^-1) gives maximum axial force1000*||forcepart||+250*||momentpart||. The resulting even/odd1348.8124/1122.6762N agree at this static geometry scope. No bearing, joint, pad, lock, nonlinear contact, stiffness or collision property is thereby supplied.

With J=W^T, enumerating all64 introduced leg-deadband corners of+/-65um gives maximum translational norm.181335mm in this linear geometry. It is NOT the producer's dynamic catch, dog-coast, temperature and permanent-set budget1.000509mm. A small quasistatic corner cannot replace its energy/dynamic bound or establish the full1mm service.

A seventh hidden axial force path has wrench h. Its force s can be canceled by changing the six represented leg reactions by-W^-1*h*s, leaving the exterior wrench unchanged. The script constructs h alongz and closes equilibrium to8.33e-17. This simple cancellation is not a universal sensor impossibility theorem. Individual branch measurements, geometry changes or physically removing all parallel paths can resolve the restricted ambiguity.

3. A portable gap witness needs a physical validity interval

For an observed gap ghat, installed error bound b, conservative closure-rate bound v and observation age tau:
g_true(t)>=ghat-b-v*tau.
With INTRODUCED ghat20um,b5um,v100um/s, the witness remains strictly positive for less than.15s. At.1s the guaranteed gap is5um; at.5s no positive separation is established. The actual drift is not measured here.

Thus replacing72 concurrent measurements with one travelling probe is not automatically equivalent. A shared witness may work if a manufactured latch or another actual operation freezes the relevant cut, or if all relevant gaps retain adequate margin under finite load/temperature/rate changes through the complete scan and proof. A probe or feeler that itself bridges the gap must be withdrawn and accounted for. Kinematic repeatability is not complete installed force/gap calibration.

4. Capturing a failed second-end attachment as a removable stressed unit

The following is a positive but INTRODUCED coaxial model, not a built cartridge. A previously supported frame node has stiffness kf=2MN/m and external force1000N. A first-end-supported workpiece has axial stiffness kb=5MN/m and natural endpoint offset.1mm. Their unloaded relative positions are xB=.5mm,xC=.1mm.

A failed second-end contact with stiffness kj=5MN/m can carry T=kj*(xB-xC)=2000N. A self-reacting tool force u=-2000N makes the outer resultant R=T+u=0. The remote shank reads zero, although the failed contact still carries2000N. Returning the tool to zero is not a release certificate. Opening the wrong path can reapply those internal forces to the frame and workpiece.

One possible mechanical organization is two removable carrier halves coupled by the failed contact and by an independently mechanically retained counterholder. All their mutual forces close inside this captured unit. Once its two outer service interfaces have demonstrably unloaded, the whole carrier/contact/counterholder can be removed without first opening the jam. This preserves the preceding frame and supported-workpiece state in the scalar model. It transports stored energy rather than making it vanish.

At introduced counterholder stiffness10MN/m, internal stored energy is T^2/(2kj)+u^2/(2kt)=.6J. The cartridge, positive retention, rack deenergization, quarantine/refurbishment and replacement stocks must be manufactured and paid. Removing only the faulty contact or leaving the counterholder attached to the host does not perform the same operation. Any jam or wire crossing the declared carrier boundary invalidates the containment assumption.

For a residual outer force bound80N, frame and workpiece displacement bounds are40um and16um, respectively; their relative bound is56um. These are static stiffness bounds, not release dynamics or a six-axis capture certificate. Hidden outer-interface self-stress, moments, friction, gravity cradles, extraction access and all mechanically retained states remain indispensable physical design work.

5. Observation-only controlled return within the bounded model

ROOT additionally executed36 cases with hidden kj=.5,2,5MN/m, initial internal force500,1500,2500N, remote-sensor bias+/-30N and actuator bias+/-5N. The plant obeys
R=(T0+u)/[1+kj*(1/kf+1/kb)].
The controller receives only observedR and its command history. It adjusts command opposite observedR, caps increments at100N and commands within+/-2990N, terminating at|observedR|<=20N. It receives neither T0,kj,trueR nor a fault label.

All36 bounded cases terminate within29 updates. Maximum actual counterholder force2560.962N, maximum represented internal joint force2547.415N and maximum residual outer force49.2706N. Adding the admitted20N drag stays below80N. No control sampling/settling or dynamic deadline is supplied by the iteration count.

This requires a mechanically retained3kN-class capture tool and actual installed metrology; the P2 candidate's2kN C-tool cannot simply inherit these results. Saturation, an unbounded jam or an unavailable outer release leads to retained support and an incomplete operation, not a hidden success. The feedback and contained-energy extraction form a possible rollback construction at this scalar scope; they do not complete the2m three-dimensional construction service.

6. Move service access out of a crowded node: a bounded geometric opening

ROOT enumerated the26 unit directions of a cubic grid's axial, face-diagonal and body-diagonal bars. Distances are to rays, not infinite lines, so opposite directions are treated correctly. The smallest neighbouring-ray separation at axial station s is s/sqrt(3).

For30mm square tube its circumradius is21.2132mm. With INTRODUCED service-tool outer radius40mm and an18.5mm relative displacement allowance composed of3.5mmplacement+15mmprefixdrift, a station needs to exceed138.067mm for nonnegative local clearance. At150mm the represented clearance is6.88934mm; at180mm it is24.2098mm. At90mm it is negative27.7517mm.

The18.5mm allowance is an introduced RELATIVE bound, not implied by two independently moving nodes each bounded by15mm. With30mm relative drift plus3.5mm positioning, the zero-clearance station rises to164.048mm;150mm has negative8.11066mm margin, while180mm retains9.20985mm. Actual correlated relative motion may be bounded differently, but must be derived.

This supports investigating a service collar displaced along a member rather than placing every release actuator inside the hub. It does not construct the collar, a straddling bore, a drive route through the end, a robot wrist path or a carried-bar trajectory. A real hub, clamps, cables, holder and neighbouring service hardware must all be included. For.5m members, two150mm end regions occupy300mm; overlap with force witnesses, splices and grippers must be checked. No full access certificate follows.

7. Whole-service and hardware compatibility constraints

Using P1's rounded available labor ledger16.556h versus76.667h assisted, the tenfold threshold is7.6667h, requiring8.8893h less work. Its initial+periodic calibration9.333h is large enough that a hypothetical completely free elimination leaves7.223h and10.6143x. This is NOT a constructed calibration solution; equivalent force/gap evidence, manufacture, maintenance and faults must still be paid. It also does not by itself beat the competent automated whole-service cost.

P2's3.014 versus3.448 total paid human hours gives1.14399x. This differs from in-window intervention. Its112000USD pins+19950USD shank witnesses are131950USD of introduced capital. A portable-witness price challenge does not supply equivalent measurements or all-port access.

The P1 deployed module85kg weighs833.85N,8.3385times P2's100N retained-tool allowance. Hypothetically applying42kg P1service nodes to all32P2nodes adds1344kg versus209.18kg original above-pedestal mass. Actual mounting may differ, but these numbers exclude treating the P1 hardware as a supplied lightweight P2 component. A topology idea may transfer while dimensions, loads, sensors and hardware do not.

8. Governing primary exposure and limits

After completed local identity/alias/hold checks, ROOT read selected actual US8997873B2 description for mechanically pinned/clamshell load transfer, flexible-link replacement, load return and apparatus removal. This is existing disclosed shoring/retention machinery, not new autonomous jam recovery, a patent-novelty judgment or a qualified six-axis cartridge. Exact https://patents.google.com/patent/US8997873B2/en. No cited patent/PDF followed.

ROOT read WHOLE SITEMA TI-A21-EN-01/2023 three-page spring-base sheet, exact https://www.sitema.de/downloads/SITEMA-TI-A21-EN.pdf. Its unloaded-release condition, compliant base travel and mounting-force requirements show that a load-holding component does not supply arbitrary loaded release or negligible catch travel. Its6--8mm spring-base stroke is not a1mm handoff component. No linked assembly manual, product purchase or contact followed.

ROOT read Maskur--Kiyokawa--Harada arXiv2603.04760v1 mainIII--V after actual version verification, exact https://arxiv.org/html/2603.04760v1. A3D-printed servo/cam-pin coupling, passive lead-ins, rotating depot and planned six-axis arm trajectories were physically exercised. Alignment tests used manual insertion/five trials per condition; autonomous exchanges were10/10fixed and9/10rotated. This credits passive alignment and automated exchange without supplying loaded structural retention, a500cycle campaign or persistent-jam recovery. No cited original/code/PDF/component followed.

MIT/ABB interchangeable-subassembly page exact https://pergatory.mit.edu/kinematiccouplings/case_studies/ABB_Robotics/ABB%20Kinematic%20Coupling%20Robotic%20Components.htm was read as an actual statement of work and historical coupling discussion. Its master-interface/calibration-transfer proposal is not a measured maintenance-free interchangeability or installed sensor-error result. Its repeatability/instrumentation statements are not imported as joint qualification. No linked paper/image/patent followed.

Exact https://wp.optics.arizona.edu/optomech/wp-content/uploads/sites/53/2016/10/Slocum-1988B.pdf opened as a9pagePDF with zero readable lines. No governing experimental passage was read. Treat SAME Slocum--Donmez1988PartII/DOI10.1016/0141-6359(88)90029-3 identity as HELD/unread: no retry/alternate/provider/version/title/PDF/image/export or unavailable governing import from search metadata. Failure to read is not evidence against the coupling. Every older known/unknown source/access/transfer hold persists.

No unqualified feedback, captured-energy cartridge, local access calculation or primary component is an integrated physical invention. No producer program, library deliverable, ZIP, linked report, archive, SI or attachment was executed or recovered.
