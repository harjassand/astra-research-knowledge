# Astra research snapshot: doubled chiral interface and implementation gates

Snapshot prepared 3 November 2026. This is a proof/code package, not a publication, a peer-review claim, a Standard Model regulator, or a practical device proposal.

## North star and present judgment

The mission is a civilisation-changing scientific foundation or enabling capability. This programme now has an explicit microscopic construction for a difficult chiral-interface problem. That is substantial foundational progress, but it does NOT yet meet the full mission: fixed-coupling gauged physics, continuum control and useful physical resource costs remain open. Conservative proved constants are astronomical. Existing free-Weyl propagation and generic Gaussian preparation are not claimed as new capabilities.

## Strongest completed construction in this snapshot

For the specified DOUBLED same-chirality four-Weyl building blocks, construct an exactly symmetry-preserving, topologically trivial, strictly finite-range gapped interface to the rotor/Majorana model. Local rotor Hilbert spaces remain infinite in this volume-uniform theorem. The original quadratic free bulk is retained literally outside the finite interface strip.

The proof joins the following actual operations:
1. A local periodic/vector-covariant barycentric SU(2) texture with exact degree equal to cochain self-linking, and uniform nonvanishing bound.
2. A finite-range Wilson-to-spectral-localizer inertia bridge, including every UV mode and both faces, with the occupied-charge sign fixed independently.
3. A two-massed-face static family with a uniform gap for every normal thickness L>=2, allowing a controlled half-space limit.
4. Phase-fixed canonical Gaussian doubling, with explicit graded Bell conventions and no state/eigenvector phase oracle.
5. An actual-bulk parent H_fast−E0+W H_rot W†, whose reference-frame fast excitation sectors give an exact collective gap.
6. Symmetry averaging with the SAME invariant ground, explicit joint rotor–fermion locality, and a specialized filtered-spectral-flow stability proof to strictly finite interaction range.

Separate audits did not find a remaining gap in this stated theorem. This is not a substitute for external mathematical review.

## Governing reading order

- `BARYCENTRIC_TEXTURE_CONSTRUCTION.md`
- `AUDIT_BARYCENTRIC_QUATERNION_TEXTURE.md`
- `index_bridge/WILSON_LOW_HIGH_LOCALIZER_TRANSFER.md`
- `index_bridge/EXACT_TOEPLITZ_ORIENTATION.md`
- `index_bridge/TWO_MASSED_FACE_WILSON_BRIDGE.md`
- `index_bridge/AUDIT_TWO_MASSED_FACE_BRIDGE.md`
- `joint_gap/GRADED_PURIFICATION_AND_STABILITY_ENTRY.md`
- `joint_gap/ACTUAL_FAST_PARENT_AND_COERCIVITY.md`
- `joint_gap/EXPLICIT_JOINT_POLYNOMIAL_LOCALITY.md`
- `joint_gap/PRODUCT_FRAME_STABILITY_AND_SYMMETRIC_TRUNCATION.md`
- `joint_gap/AUDIT_CANONICAL_PARENT_AND_STRICT_RANGE.md`

`ROOT_CANONICAL_DOUBLE_PARENT.md` records the synthesis; its Section6 is the stronger bulk-retaining parent and supersedes the need to physically flatten the free bulk. Earlier failed constructions and preliminary notes remain for reuse and should not override the governing files.

## Finite-resource continuation and its exact scope

The concrete anomaly-free 3+1D U(1) test uses layers (A,V)=(1,2),(-4,1). Their initial left-Weyl charges are (3,-1,-1,-1) and (-3,-5,4,4), each doubled. The vectorlike +/-3 pairs can be removed only by an explicitly added ordinary mass; until then they remain in the stated spectrum. The residual doubled charge set would be {-5,-1,-1,-1,4,4}.

The shared-rotor disentangler uses ONE shear per doubled building block, bosonic axial weights2A, and two fermion factors of weightA. Its declared convention is positive cochain phase, positive shear, and OUTPUT-matching fermion rotation. Direct compact-angle algebra and exact-rational checks replace reliance on ambiguous printed sign/order conventions.

See:
- `joint_gap/SHARED_ROTOR_DOUBLE_DISENTANGLER.md`
- `joint_gap/FINITE_AUXILIARY_COERCIVE_REGULATOR.md`
- `joint_gap/AUDIT_FINITE_AUXILIARY_AND_SHARED_DISENTANGLER.md`

The finite-volume cutoff is not a fixed local-dimension thermodynamic theorem. It uses a volume-dependent finite range and paid Fourier cutoff after the desired subgroup is actually onsite. Adding a small physical angular-momentum-square term is a NEW coercive UV completion, not an approximation to every low-energy state of the old infinitely degenerate reset model.

Structured quantum term compilation has passed the stated proof audits after the moving-wall square-root-dimension correction, exact valid-code projection, Hermiticity and charge pinching. Ungauged finite-volume ground preparation also passed its audit, with the far-level spacing, reference-energy offset and compiled-Hamiltonian eigenvector error explicitly retained where applicable. Polynomial logical costs hold at fixed enormous microscopic constants; they do not mean a practical simulator. The archive contains small executable checks, not an executed full compiler.

## Exposed far surface and gauging

The far-surface files distinguish a state-independent finite-time target-band response from the stronger rest-sector statement. The corrected finite-volume global-norm transfer has passed its audit: the physical device is close to the explicit far Fock band plus a gapped interacting rest, modulo an explicitly separated scalar. This uses O(log²(volume/accuracy))-range and thickness, not a new fixed-range thermodynamic device theorem. Actual multiplicities remain doubled. Individual lowest-level resolution also requires error below the far level spacing. The finite-auxiliary integration now has a separate audit: the actual disentangler, rotor cutoff and matched kinetic addition commute with the far CAR factor. A new rest gap is re-earned by an explicit Fourier trial and minmax. This preserves the paid far-band comparison for the NEW regulated model; it does not assert that the old rotor spectrum is unchanged. See `far_surface_device/FINITE_AUXILIARY_CHIRAL_DEVICE_INTEGRATION.md` and its audit.

The quantum-gauge files preserve the unresolved central consequence. Standard gauging is implementable but does not automatically preserve the mirror-decoupling certificate. In particular, the A-retained/V-reversed conjugate doubling used at zero gauge field does not remain a literal conjugate pair for the physical gauged subgroup A a+V v at nonzero links. Replacing it by a vectorlike gauged pair would change the target and is not allowed. Gauge vacuum energy, Berry/Born–Huang terms, finite charge ranges and light–mirror coupling all remain charged. An attempted unconditional weak-curvature magnetic-gap transfer to the discontinuous rotor/cochain family was withdrawn; the first line of its note records the correction. The gauging folder is a research frontier, not part of the completed ungauged capability.

## Resources and comparisons

The deliberately conservative Wilson proof uses aM<=10^-6 and Lambda/M=1000. Already this can require at least order10^21 slab sites per coarse cell, before additional local compilation constants. The elementary sign-polynomial and locality bounds can be much larger still. They establish finite existence and specified asymptotics, not attainable engineering performance.

`joint_gap/DOUBLED_INTERFACE_PRIMARY_COMPARATOR_AUDIT.md` records strong current alternatives, including TPF, Gaussian/Choi parent machinery, overlap formulations, mirror SMG and the October2026 disk Hamiltonian framework. No exhaustive novelty or civilisation-breakthrough claim is made.

## Reproduction

Python checks use NumPy/SciPy and standard-library exact rational arithmetic. They check matrix identities, actual finite Wilson failures, graded purification, cochain cocycles, quadrature and small compiler components. They are NOT executions of the astronomical full construction. Preserve the failed periodic-zero-mode diagnostic as a failed diagnostic; do not count numerical signs of exact zero eigenvalues as charge transfer.

All scientific scope restrictions in the individual proofs remain part of this package.

Selected small checks can be run with `python run_smoke_checks.py` after installing NumPy/SciPy. The runner uses a temporary relocatable copy and does not execute the astronomical full construction.

A further actual gauging obstruction is recorded in `quantum_gauge/ROOT_CHARGED_JUMP_GATE.md`: the uncut on-sited canonical ground has orthogonal free-charge-sector jumps along some charged rotor directions, hence infinite local gauge-charge variance. Naive gauge dressing would require infinite electric energy. This does not invalidate the completed finite-cutoff ungauged operation, but makes a fixed-capacity/coercive gauged repair an essential next step.
