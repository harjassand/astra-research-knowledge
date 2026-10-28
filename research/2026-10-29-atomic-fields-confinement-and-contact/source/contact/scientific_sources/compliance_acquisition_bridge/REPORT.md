# Contact-weighted compliance acquisition bridge

**Completed:** a conditional, executable map from an imperfect open/closed
compliance contrast to a bound on the largest crack's service stress
intensity, without reconstructing the crack population. **Not achieved:**
acquisition of the contact, measurement, component-model or nondestructive
load premises for a real specimen. New physical mechanism, practical method
advantage and world novelty are not established.

The result is narrower than the original preload hypothesis. Open-minus-
closed differential compliance is an existing measurement. The useful
extension constructed here retains nonzero closed-contact compliance and
turns it into an explicit radius-dependent sensitivity, rather than treating
compression as a pristine reference.

## Constructed operation

Use the peer's tension/bending convention: p=(p0,p1), stress p0+p1*r,
r=2z/H, and v(r)=(1,r). Let beta=16(1-nu²)/(3E). A circular finite disk
has the open matrix

    C_open/beta = a³ [[1,r],[r,r²+(8/15)(a/H)²]].

The positive a⁵ term is the crack's own bending extent. The peer has
corrected its physical convention and can retain this term conservatively.
I independently obtained it both by opening-displacement integration and
by integrating the primary uniform/bending energy-release rates. The
underlying source is the infinite-medium penny-crack solution of
[Nishioka et al.2008](https://doi.org/10.1299/jcst.2.34), including its
visually checked bending Eq60. This is not a finite-component correction.

Suppose every crack is open at the positive preload and its compressed
normal-contact operator obeys K>=kI, with k>0 supplied in Pa/m. A variational
projection of the ordinary resolvent identity gives the lower contrast

    (C_open-C_compressed)/beta >= h_k(a) v(r)v(r)^T,
    h_k(a)=a³ * beta*k*a/(pi+beta*k*a).

This derivation does not require rigid closure, a minimum crack size, or a
contact solve for every flaw. h_k is increasing. If an error-corrected
measured upper matrix U bounds the sum of these contact-weighted matrices,
every individual crack satisfies

    h_k(a) <= 1/[v(r)^T U^-1 v(r)].

Invert this scalar law, cap the radius geometrically, and maximize the
ordinary affine disk rim intensity over depth. `contact_certificate.py`
does this with rational interval bounds. `PRIMARY_PROOF.md` gives the
operator argument, finite-disk energy, error inflation and scope. A scalar
mean contact stiffness does **not** supply the required operator inequality.

## Declared-scale calculation

The calculation consumes the peer's **declared interface box**, not component
measurements: contrast/Mref near diag(1,.01), absolute entry error .02,
Mref=(100micrometres/sqrt(pi))³. The resulting upper is diag(1.04,.05)Mref.
Inputs are E=110GPa, nu=.34, H=10mm, a<=.5mm, |r|<=.8 and nominal service
stress 500+250rMPa. The declared limit is5MPa sqrt(m).

| Supplied condition | Certified upper, MPa sqrt(m) |
| --- | ---: |
| Ideal rigid closure, no added service residual | <4.361066 |
| k>=2e15Pa/m, no added service residual | <4.707073 |
| k>=1e15Pa/m, no added service residual | <4.922313 |
| k>=5e14Pa/m, no added service residual | <5.212425 |
| k>=1e15Pa/m, plus nuisance norm .02Mref | <4.978316 |
| k>=1e15Pa/m, plus nuisance norm .05Mref | <5.064301 |
| k>=1e15Pa/m, service residual bounded by10MPa | <5.016025 |
| k>=2e15Pa/m, residual10MPa and nuisance .02Mref | <4.847948 |

The nominal-service example and the residual10MPa acquisition screen must
not be presented as one specimen with free residual-stress removal. The
last two rows explicitly carry that uncertainty into service.

The contact/error premises would make this a useful measurement operation:
under the same declared geometry an absolute-total-compliance PSD upper
gives18.082450, and the uniform-contrast-only upper gives6.734424. These are
information comparisons. An ordinary analyst supplied the same full
contrast, contact and error information can use this construction or a
certified contact solver. No same-information optimizer advantage is claimed.

## Strong prior and a failed alternative

[Kovářík2025](https://doi.org/10.1007/s10704-025-00881-z) directly obtains
crack-added compliance from open and closed portions of a breathing-crack
vibration. It uses a continuously available closed reference and credits
earlier differential-compliance work. Its calibration uses a known specimen
and crack geometry; its validation also shows why front shape matters.
Consequently self-referencing open/closed compliance is established prior.

[Donskoy & Liu2020](https://doi.org/10.1016/j.jsv.2020.115808) demonstrate
baseline-free vibro-acoustic damage detection through amplitude dependence,
including a necessary static-load correction. This is strong prior for
nonlinear detection; it does not provide this branch's contact-coercivity
and maximum-service-K acquisition contract.

I seriously considered cancelling intrinsic load-dependent background with
two preload amplitudes, 2d(P)-d(2P). It retains an ideal step and cancels a
linear background term. For a contact with d(P)/Q=t/(1+t), t~P^m, it is
negative whenever m>1 and 0<t<1-2^(1-m). Such contacts could mask another
crack. [Kim et al.2021](https://doi.org/10.3390/ma14112988) report fitted
contact exponents .930,2.601,4.987,7.486 for four rough aluminum block
interfaces. A universal concave/Hertzian contact premise therefore fails.
Their measured mean stiffnesses and fit errors are not coercivity bounds
for hidden fatigue cracks. The retained contact-law computation tests this
failed repair; it is not treated as new experimental evidence.

The variational/parallel-sum machinery is ordinary, with
[Anderson & Duffin1969](https://doi.org/10.1016/0022-247X(69)90200-5) a
primary early source. The derived mechanical kernel and its coupling to the
population-independent service bound are constructed here. A world-prior
claim for that exact combination remains UNKNOWN.

## Acquisition costs and remaining physical gap

Two independent central-difference probes at each preload require eight
load settings, each measuring displacement and rotation. For the actual
one-mode-at-a-time protocol, bounded affine residual stress and radius give

    P > rho0+Amax*rhog+max(h0,h1*(R+2*Amax/H)).

At P=20MPa, h0=h1=5MPa, rho0=10MPa, rhog=0, the sufficient ideal switching
margin is5MPa and the test's opening-K upper is.883097MPa sqrt(m). These
inputs are hypothetical. The switching margin does not establish k, elastic
asperity seating, reversibility or a no-growth load envelope. A validated
fatigue/no-change bound, compression stability and yield limits remain
necessary; fracture toughness alone is insufficient.

For A=20mm² and L=20mm, one Mref contributes2.117691ppm of the uniform
baseline compliance, or19.25pm extra extension at50MPa. To reserve the full
.02Mref entry error for measurement alone, the deterministic individual
displacement error must be about19.25fm with5MPa probes, or.193pm with50MPa
probes. The latter require higher switching preloads. Rotation error,
force-gain mismatch, drift, probe truncation and reciprocity errors also
consume the budget. These numbers are requirements, not demonstrated
instrument performance.

Unknown linear elastic background cancels, but its load dependence can
dominate the crack signal. For illustration only, if
C_bg(P)=C_bg(0)*(1+gamma*P/E), a20MPa preload creates171.7Mref of contrast
per unit gamma in the uniform channel. Keeping it below.02Mref requires
|gamma|<1.17e-4. No such material/fixture bound was acquired. The failed
two-amplitude repair cannot remove that obligation generally.

The implementation checks thickness burial; lateral burial and all other
finite-boundary errors remain external geometric obligations. At the
reference radius the exact within-disk extent term is only about1.70e-5
of its uniform moment, but this says nothing about free surfaces, crack
interactions or orientation errors. Roughness, finite initial aperture,
fluid filling, contact relaxation, friction and normal/shear coupling need
their own validated operator/model error enclosures. Hidden cracks that do
not switch need the parent's separate load-envelope bound, not this matrix.

## Reproduction and evidence boundary

`run_bridge.py` saves exact inputs and rational leaf intervals for18
conditional certificates in `bridge_results.json`; `verify_saved.py` checks
the on-disk code binding, every interval's exact upper and continuous depth
coverage, six input guards, and the pi bracket by rational Machin series.
The final replay passed18certificates and1731coverage leaves in1.921s;
construction took5.399s. The largest saved leaf numerator or denominator
was198bits. Exact runtimes and hashes are in `replay_results.json`.
All computation is local and modest; no external solver or physical test is
used. The source files and their read scopes are pinned in
`source_manifest.json`. Astra freshness was checked selectively at revision
`1dc593a750b447be6536bafcf0be156d27767dfe` (1811 records), without preloading
the archive.

The parent independently checked the nominal k1e15 case against the
threshold5 using a separate two-dimensional rational radius/depth cover:
339visited boxes,82safe leaves and88moment-excluded leaves. Its receipt is
`../parent/contact_review/BOX_CERTIFICATE.json`. This supports the declared
conditional all-population calculation; it does not acquire its physical
premises or establish novelty or practical advantage.
The parent also independently certified the matched residual case
(k>=2e15, nuisance .02Mref, service residual10MPa) against5:299visited
boxes,71safe and79excluded leaves, max depth16, in about.0057s. That separate
receipt is `../parent/contact_review/MATCHED_BOX_CERTIFICATE.json`.
