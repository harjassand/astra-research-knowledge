PASSIVE MAGNETIC CONTACT, BACKING STABILITY AND RESET CONTRACTS
13 November 2026 Brisbane / 12 November UTC

Useful physical operation and evidence scope
A compact detachable structural interface must transmit normal force and bending without supply power, tolerate bounded imperfect contact, then release after a paid unloading operation. Electropermanent magnetism is an existing physical alternative to chemical bonding. The analysis below examines the interaction of actual magnetic contact sensitivity with a compliant carrier; it does not establish a working interface, a new magnetic material or a full repeatable service.

Primary source bindings
Wang--Stokes, Self-Aligning EPM Connector: A Versatile Solution for Adaptive and Multi-Modal Interfaces, actual version verified v1 before reading https://arxiv.org/html/2508.16008v1 . Main Results and Methods were read. Their small EPM uses AlNiCo/NdFeB magnets, steel end caps and a 120-turn, 3-ohm coil. Main force-gauge tests of two EPMs report about 14.6 N at nominal zero gap, 7.7 N at 0.1 mm and 2.34 N at 1 mm. Main switching input is described as 30 V, 10 A, 1 ms, or 0.3 J. The connector includes springs, bearings, seals, printed parts and electronics; its test and hardware boundaries differ from a structural mixed-load joint. Detailed fabrication is deferred to unread supplemental material. No supplemental material, code, images, videos or cited original was followed.

Li--Tao--Chen--Ding, High-Load-Density Electro-Permanent Magnetic Foot with Controllable Adhesion for Quadruped Wall-Climbing Robots, version verified v1 before https://arxiv.org/pdf/2605.30849v1 . Initial main pp0--5 through line466 were read. Sections II and initial III describe circular parallel-flux yokes, an AlNiCo/NdFeB circuit, passive ankle and contact-force sensing, plus a 48 V, up-to-50 A driver of stated 62 g. Table I gives a 32 mm magnetic radius and 272 g assembly. Section II-B explicitly connects contact to successful magnetization and warns that an open magnetic circuit can demagnetize AlNiCo after excitation ends. Later completed control and experimental sections were not read. Abstract force/load-to-weight claims are not a supplied experimental point, lifetime, whole switching-energy measurement or a 50 mm structural interface. No later artifact was recovered.

These are distinct sources. Neither supplies the constitutive constants in the following model. Source access limitations and unread passages do not constitute negative scientific evidence.

An introduced finite model
Use a rigid 50 x 50 mm carrier with four independent axial cell suspensions. Their centers are (x,y)=(+/-12.5,+/-12.5) mm. An introduced 20 x 20 mm cell footprint gives a 45 x 45 mm bounding square, leaving lateral clearance inside the reference footprint. No actual yoke, coil, gimbal, backing thickness, key or wiring layout is thereby supplied. The point-force model assumes cells can remain parallel to the receiver; that angular accommodation needs physical construction.

Let q_i>=h_i be each cell's magnetic gap, with h_i the nonmagnetic obstruction at its seat. Let r_i be its independently retained spring-rest setting. A cell with normal stiffness k transmits
t_i=k*(z+s_y*p_y-s_x*p_x-q_i+r_i)
to the carrier, where p_y=a*theta_x, p_x=a*theta_y and a=12.5 mm. Positive t is normal tension; a seated cell may also transmit compression, whose actual finite material limit remains unqualified.

Introduce f_i(q)=F0_i/(1+q/gc)^2, with gc=250 um and F0_i=180 N in the healthy examples. At a seat the compression reaction is N_i=f_i(h_i)-t_i>=0. A lifted cell has N_i=0 and t_i=f_i(q_i). Magnetic potential is U_i=-F0_i*gc/(1+q_i/gc), so U_i'=f_i and U_i''=f_i'<0. The 180 N amplitude over 400 mm2 corresponds to an ideal uniform Maxwell-pressure flux of 1.06347 T; this is an introduced requirement, not a measured pole-field or a supplied magnet. Coil switching, B-H hysteresis, leakage, temperature, receiver thickness and material saturation are not modeled.

The source's three small-device force points already show why this surrogate cannot be silently imported as a material law. Fitting the inverse-square law to 14.6 N and 7.7 N gives gc=265.258 um, but predicts only 0.641701 N at 1 mm against the source's approximately 2.34 N. That mismatch is a model diagnostic. The subsequent calculations use an explicitly introduced surrogate, not a reconstruction or fit of the source device.

Eliminate the three rigid-carrier degrees of freedom using force and two moment balances. With the order (-,-),(-,+),(+,-),(+,+), define v=(1,-1,-1,1). Then
t_i=tpart_i-(k/4)*v_i*S,
S=sum_j v_j*(q_j-r_j),
tpart_i=Fn/4+s_y*Mx/(4a)-s_x*My/(4a).
The reduced gap Hessian is
H_gap=(k/4)*v*v^T+diag(f_i'(q_i))
on freely opening cells. With two or more strictly open live cells, there is a nonzero perturbation orthogonal to v and the quadratic form is negative. Thus, in this restricted four-cell, three-carrier-DOF, decreasing-force model, a strictly stable local equilibrium has at most one strictly open cell. This is not an all-magnet or all-interface impossibility: extra constraints, different force-gap behavior, more supports, backing bending or a mechanical latch change the model.

For exactly one open cell j, other gaps stay at h. The scalar stationary equation is
C-(k/4)*q_j-f_j(q_j)=0.
Its decreasing-side root is locally stable exactly when k/4+f_j'(q_j)>0; all other seat reactions must still be nonnegative. The executable enumerates all nondegenerate seated states and these single-open minima using a concave scalar root. Exact zero-reaction seated degeneracies need unilateral second-variation analysis and are not certified. The equilibrium's existence does not show that an engagement trajectory reaches its basin.

Concrete outcomes, without a capacity relabel
For a clean array at k=1 MN/m under Fn=500 N, each t is 125 N and carrier translation is 125 um. Pure 5 Nm bending about a face axis gives +/-100 N and 200 um extreme corner movement. Arbitrary in-plane moment direction matters: diagonal 5 Nm gives 141.421 N maximum tensile cell force and 282.843 um extreme corner motion. Under the convex normal/bending envelope Fn/500+sqrt(Mx^2+My^2)/5<=1, the clean force maximum is 141.421 N, not the sum of the separate normal and moment maxima.

Now insert a 100 um obstruction at one cell. Its seated surrogate force drops to 91.8367 N. The sum of all four nominal available seat forces is still 631.837 N, above the 500 N applied normal load, but total force alone does not construct a stable distributed equilibrium.
At k=1 MN/m no nondegenerate stable state is found for that pure normal case, with either unadjusted rests or ideal independent rest resetting.
At k=2 MN/m with unadjusted rests, a seated state exists: t=(75,175,175,75) N and maximum absolute carrier-corner motion is 187.5 um. The same case with independently reset r=h has no certified nondegenerate state.
At k=8 MN/m with unadjusted rests no certified nondegenerate state is found. With ideal independently reset r=h, a single-open-cell equilibrium exists: the faulty gap becomes 121.810875 um, t=(81.37825,168.62175,168.62175,81.37825) N and maximum absolute corner motion is 42.888594 um.

Thus an unqualified instruction to make the backing softer, stiffer, or perfectly leveled is not enough. Stiffness, reset state, gap-force slope and redistribution interact. The grid uses five stiffnesses, six fixed obstruction patterns, two rest-setting choices and 80 sampled normal/bending loads per combination. For k=8 MN/m with one 100 um obstruction, ideal resetting gives a stable state within 0.2 mm for all 80 sampled loads; unadjusted rests do so for only 34. These are finite conditional existence results, not reliability probabilities, a continuous-envelope proof, a transition trajectory or physical tests.

Resetting is itself a physical operation
Ideal r_i=h_i represents conforming each cell to its seat and retaining the resulting reference length. It is not a supplied actuator or free calibration. With all cells seated, independent rest errors bounded by e create a worst-case |delta t_i|<=k*e through the checkerboard mode. For the clean k=8 MN/m array, the 180-141.421 N static margin permits only e<=4.82233 um before other uncertainties. A 5 um per-cell error can add 40 N and exceed the clean 180 N capacity. This bound applies to that clean seated linear margin, not the nonlinear defective equilibrium.

A concrete candidate operation is therefore a cell suspension that first conforms, then captures a measured local force/rest state without creating excessive locked-in mismatch, while remaining stiff during the passive hold. That requires actual retained geometry, creep/backlash bounds, load/gap observation and a reset path. A compliant differential or force-sharing tree is an existing alternative, but it must also transmit the required moments. Pure total-flux or total-force observation cannot supply the missing individual state. No retained carrier from a different, much heavier apparatus is assumed compatible.

Shear, release and energy remain real interfaces
The normal model supplies no 1000 N shear joint. With an introduced friction coefficient 0.3, pure friction needs 3333.33 N normal clamp. Even an ideal uniform field over the entire 2500 mm2 face would then require 1.83058 T before leakage or inactive area. This is a conditional requirement, not a universal field limit or a measured friction coefficient. Positive shear keys can change it, but their receiver, bearing area, cam-out, backlash, release access, wear and force path become the actual joint.

The introduced four-cell magnetic mechanical-potential depth is 0.18 J. It does not determine purchased switching energy. In particular, the source's small 0.3 J switching event cannot be combined with the introduced 180 N cells as if that higher-force array were built. Off-state remanence, a steel receiver's retained flux, trapped particles and mechanical key friction also affect the <=20 N release port. No energy, 24 h hold, 500-cycle renewal or complete-service cost endpoint is established here.

A discriminating later experiment
A reviewable first test would separate two operations. First measure individual assembled cells' force-gap curves and magnetic state after a pulse is removed, including bounded shims, receiver lots and return to the separated state; record purchased electrical energy rather than only a pulse product. Then use four measured cells on interchangeable measured suspension stiffnesses, with unadjusted and independently set/retained rests. Apply a bounded small normal force and moments through a paid supported fixture while measuring each cell gap, transmitted force, carrier motion and capture/reset error. Increase only within the fixture and cell limits actually measured. One approximately 100 um shim and a loss of one cell discriminate summed capacity from redistribution; repeated rest setting discriminates a real conform-then-lock operation from a supplied setting oracle. The measured f'(q), k and geometry predict the local opening boundary before the array test. No material recipe, actual rig, access booking, quote, purchase or physical execution is supplied or authorized by this calculation.

Executable and limits
ROOT_PASSIVE_MAGNETIC_CONTACT_AND_BACKING_STABILITY_20261113.py:10333 bytes, SHA256 25c00adbe813156c92e21360817a24a7dcdd9372be6b853c363c23970a1cd2ef
ROOT_PASSIVE_MAGNETIC_CONTACT_AND_BACKING_STABILITY_20261113.json:32025 bytes, SHA256 541e8f6b970b99faf315868935c83964aedb18473fe6529ff7ae7b3660b928ec
Both are independent owned calculations. Internal checks reproduce the closed-contact force/moment solution, the geometric cell bounding box and stationary balance; maximum shown equilibrium residual is at numerical roundoff. Full time-domain dynamics, contact hysteresis, stiffness after locking, finite compression strength, self-loads, in-plane loads, real sensing, receiver manufacture, restoration, ageing and whole-service economics remain unresolved. Stable local existence with a chosen reset state is not an operational invention.
