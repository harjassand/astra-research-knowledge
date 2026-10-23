# Dots contact intervention — v2 resistance correction

This append-only update preserves v1 as historical evidence and adds its v2 correction. The v1 ideal parallel-pin resistance statement is superseded; the other v1 results retain their stated scope. The correction does not establish an electrochemical rate or production gain.

## Corrected result

The proposed design keeps the same hematite batch and preparation, 10 M NaOH, 353 K, Ni36Fe64 anode, and cathode at −1.4 V versus the original Ag/AgCl reference. It replaces one disk with four separately contacted subpellets. The design preserves oxide volume and the projected circular envelope but increases pellet depth from 2 mm to about 2.914 mm. The total active pin volume is held fixed in the idealized geometry.

For radius ratio \(k=1/(1+\sqrt{2})=0.41421356\) and height ratio \(H=1/(4k^2)=1.45710678\), each ideal pin's length and cross-section change while total pin volume stays constant. The parallel axial resistance ratio is therefore

\[
\frac{R_{\mathrm{new}}}{R_{\mathrm{old}}}=\frac{H}{4k^2}=H^2=2.12316017.
\]

The v1 statement that the ideal parallel resistance was unchanged is wrong. The v1 report, code, and results remain byte-preserved under `source/d_contact/v1/`; the corrected v2 files are under `source/d_contact/v2/`. Extra headers, contacts, supports, mechanical constraints, and the increased bare pin area (2.41421×) are not included in that ideal ratio.

## Model hypotheses and limits

The source compares radial-front time proportional to radius (\(p=1\)) or radius squared (\(p=2\)) against axial pore-transport time proportional to height squared. Under its additive-times model, faster completion requires the original radial-time fraction \(\alpha>0.65722368\) for \(p=1\), or \(\alpha>0.57551111\) for \(p=2\). \(\alpha\) is unknown. An axial-dominated admissible case predicts a 2.12316× slowdown. The favorable radial limits also require about 2.14–2.41× mean current for \(p=1\) or 4.89–5.16× for \(p=2\); no voltage or supply response was measured.

The source retains competing explanations: radial charge access, axial pore access, local dissolved-iron transport or nucleation, and added hydrogen/side current. Its normalized geometry-grid “HER proxy” is a deterministic arrival-distance calculation, not measured hydrogen evolution or actual electrolyte kinetics. The v2 replay reproduces the source outputs; it does not validate those transport laws or show improved metallic-iron recovery.

## Evidence boundary

The source manifest pins the v2 archive and its embedded v1 archive, with the selected files and exclusions listed separately. Both archives passed CRC and manifest checks. Both v2 scripts exited successfully on a disposable copy, and their scientific/result fields matched the supplied outputs after excluding elapsed seconds and peak RSS. This checks the geometry identities and code/result consistency only.

The v2 packet has no receipt-time public-disclosure field. The direct human task instruction on 23 October authorizes this selected source-bounded release. Operational `START_HERE` and `PROCESS_RECORD` files are excluded. The coordinator’s review is exposed coordinator analysis, not independent physical validation or priority clearance. No measured gain, validated electrochemical kinetics, hardware, external novelty, or priority is established; practical advantage remains `UNKNOWN`.

## Next evidence that could change the decision

Use compatible existing spatial/time observations if available; otherwise acquire spatially resolved conversion histories at fixed local cathode potential together with absolute metallic output, integrated hydrogen, dissolved/escaped iron, full-cell voltage, and charge. Compare the radial, axial, dissolved-transport, and side-current predictions against ordinary thinner-pellet and mesh/foil controls at matched material and power. No such acquisition is part of this handoff.
