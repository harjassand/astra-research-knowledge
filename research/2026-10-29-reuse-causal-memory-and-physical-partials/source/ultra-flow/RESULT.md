# Result

Constructed and executed an exact solver-to-continuum transport-floor certificate for a public 3D pore image. Conserved face currents are compactly smoothed into continuous, divergence-free no-slip fields while retaining winding/mean flow. Exact support, polynomial energy and dyadic divergence repair give a full Loewner lower bound without validating a large numerical solve or truncating a Fourier tail.

The single centered 48^3 public-image case has 54912 currents. Exact postprocessing took about 0.70 s after a 58.22 s ordinary spline-Stokes solve; it retains that SAME trial-space prediction to 4.88e-14 relatively. The solve used a large 206.5-million-nonzero LU factor, so no generic fast/low-memory solver claim is made.

The exact matrix proves the concrete all-direction model floor K>=0.01h^2I. It also applies to every coercive periodic geometry containing the nominal pore union eroded by a half-voxel cube. That is a conditional fabrication/measurement-tolerance receiver; the public segmented image does not warrant its physical premise. The figure 4.88e-14 is NOT relative continuum accuracy.

The first local face-bubble attempt was decisively rejected: artificial internal walls force K<=h^2/pi^2 under physical refinement. The continued construction uses established divergence-conforming spline mathematics; no new homogenization principle or historical novelty is claimed. It is a working finite certificate interface, not a qualified physical material or an acquired discovery multiplier.

Governing files: PROOF.md, FAILED_LOCAL_LIFT.md, build_transport.py, consume_transport.py and TRANSPORT_CERTIFICATE.json. PRIOR_AND_COSTS.md preserves sources, the equally informed ordinary comparison and physical/RVE/model debts. Independent review status is recorded in FINAL_RECEIPT.json and any reviewer-authored note.
