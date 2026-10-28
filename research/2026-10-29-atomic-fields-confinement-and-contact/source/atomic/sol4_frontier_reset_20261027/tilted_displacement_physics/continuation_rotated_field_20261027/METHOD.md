# Rotated-field calculation method

The original accepted `../REPORT.md` is frozen. This continuation tests incoming local fluence, not displacement hazards or defect retention.

The candidate is the previously selected layer-8 parked beam with incident direction proportional to `(tan(1 degree), tan(10 degrees), 1)` in crystallographic `(a,b,c)` coordinates. An orthonormal rotation maps that incident vector to laboratory `+z`; the target lies at the center of the transverse box. The finite original crystal contains all six CIF basis atoms in all 16 layers and a central lateral patch. Its coordinates are rotated rigidly, then placed in a larger orthogonal vacuum box. `periodic=False` is used; the actual transformed and padded atom lists are checked against the original list. No affine strain or tilted periodic-cell wrapping is permitted.

The comparison supplies both controllers with the same incident electrons, target vacuum focus, 200-keV energy, and 32-mrad aperture. The ordinary source actuator is a sinusoidal native-Cr-to-S/Br `+b` scan. A parked on-axis reference is also evaluated. Three probe completions are applied to each controller:

1. Ideal coherent, uniformly filled 32-mrad pupil, about 0.403 Å vacuum FWHM.
2. A coherent Gaussian pupil apodization within that aperture, giving a 0.8 Å intensity FWHM.
3. The ideal pupil with Gaussian incoherent position spread, giving a 0.8 Å effective FWHM. Its inferred source standard deviation is about 0.296 Å. This is one physically defined completion of the source width, not an acquired microscope source distribution.

The density operator of the third model is evaluated analytically in the finite reciprocal pupil. Its correlation factor is

`K(k,k') = exp[-2 pi^2 sigma_source^2 |k-k'|^2]`.

For the sinusoidal `+b` scan, the `b` factor is additionally multiplied by

`exp[-2 pi i (b/4) Delta k_b] J0[2 pi (b/4) Delta k_b]`.

Both factors are positive kernels. One-dimensional eigendecompositions followed by tensor products give positive coherent components; retaining components accounting for more than `1-10^-6` incident trace avoids storing the full two-point density matrix. The components need not be mutually orthogonal after circular aperture clipping. Their intensities are summed incoherently with their original weights; the omitted trace is not renormalized into the retained modes. This is also an exact temporal scan average within the input model, rather than a small set of arbitrarily chosen scan phases.

A preliminary Gauss-Hermite source-position quadrature was rejected as the final input model. Its 9 by 9 nodes reproduce the FWHM closely but have a large error in the coherence characteristic function at the aperture's largest reciprocal separation. Its outputs are retained as preliminary only. The analytic kernel removes this quadrature ambiguity.

Finite IAM atomic potentials are integrated through each slice using the installed abTEM runtime. Incoming intensity is sampled at the beginning of the slice containing each atom. This is at most one slice thickness before its center; finite-potential contributions before that plane are included. All Cr, S, and Br atoms in the simulated crystal are measured. Primary fluence uses a 0.4 Å radius disk with subpixel area weights; a 0.2 Å disk and a bilinear point diagnostic expose sensitivity to the local sampling functional. None of these is an acquired scattering-to-displacement law.

Two-thread streaming propagation prevents retaining a stack of full waves at every depth. Atomic site fluences and a few intensity planes are saved. Checks include input norms, coherence trace, numerical norm loss, box-border fluence, rigid frame geometry, atom-list identity, a larger crystal and box, finer grid and slices, and a matched vacuum-propagation control. Rotating the atoms leaves the incident pupil near-axis; the second-order Fresnel propagator is used consistently.
