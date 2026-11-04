ASTRA P1: BOUNDED-COMPONENT QUANTUM ACQUISITION
5 November 2026, Australia/Brisbane

READ FIRST

Astra_P1_Bounded_Component_Acquisition.pdf is the integrated scientific return.
Its LaTeX source is included. construction/ contains complete independent notes
and audits. verification/ contains reproducible finite numerical checks and actual
results. continuation_handoff.txt preserves the warm construction and its limits.

COMPLETED OPERATION

For the specified interacting source with actual pure coherent Weyl ports,
r > beta, and no unbudgeted inaccessible noise, a deterministic output-only
receiver transfers the original arbitrary unknown register and all reference
correlations. Each material absorber is a qubit with bounded coupling norm.
Local control-response poles stay fixed. Accuracy costs polynomial hardware,
real propagation, precision, stationary memory and quantum gates.

The actual interface uses static coherent spatial dilution, delayed two-level
absorber cascades, a derived Laguerre field-to-register map, finite fixed-response
readout, binary occupation registers, local Kraus conversion, and the preserved
reverse-reset decoder. The field is not assumed to be buffered or transduced.
An explicit parameter prescription resolves all guard/hardware dependencies.

NEW LOSS AND SPECTRAL BOUNDARIES

For independent H=0 qubit Weyl sources, uniform collection efficiency eta implies
F_Bell,n <= [1-c_L(1-eta)^2]^n, c_L=(1-exp(-2))^2/256, even after arbitrary
collective decoding. The same bound applies to success times conditional Bell
fidelity. A finite-time, noncausal spectral-access comparison gives a necessary
aggregate half-bandwidth Omega(r sqrt(n/epsilon)). A separate sharp ordinary
amplitude-emission example has its own Omega(n gamma/epsilon) law.

Uniform attenuation BEFORE capture has an explicit attainable-operation error
allowance as well: the SAME deterministic receiver adds at most
2sqrt(1-exp[-2R_p A(1-sqrt eta)]). It is not a fixed-loss threshold theorem.

SCOPE AND COST

This is a construction in a calibrated chiral Markov interface, not a demonstrated
device, economic advantage or historical-first claim. Fixed local response does
not mean a fixed common hard optical passband or microscopic ultraviolet completion.
Raw capture is uncoded; later error correction cannot undo arbitrary earlier
leakage. Noise, storage, transport, calibration stability and protection remain paid.
The conservative bounds are enormous: one n=1 scalar test gives >10^112 capture
cells. These are sufficient proof bounds, not lower bounds or a proposed build.

PRESERVATION

preserved/Astra_P1_Scalable_Many_Body_Acquisition_Package.zip is unchanged:
SHA256 c7bc392421457f3c807516bdd06b9458954e1cb621f62f8cfbb826d69507cb55

It preserves the full continuous-Hamiltonian theorem, source-plus-field comparison,
reverse decoder, finite implementation, stopping certificate, diagonal extension,
and the nested interaction-order theorem, meters and both original companions.
Their premises and proof boundaries are unchanged.

The current N1732/N1733 governing cards and retrieved complete visible source
return are in provenance/. Their Git blob identities were checked. Source SHA256:
8ebad29946fa6ede7167e544c89d26e356deceb017592bfff92460622fcef819

REPRODUCTION

Run python3 verification/verify_bounded_acquisition.py for finite diagnostics.
Compile the LaTeX source twice with pdflatex to rebuild the report. The numerical
checks are not asymptotic proofs or interval-certified hardware validation.
SHA256SUMS.txt covers final package contents, excluding itself and the ZIP.
