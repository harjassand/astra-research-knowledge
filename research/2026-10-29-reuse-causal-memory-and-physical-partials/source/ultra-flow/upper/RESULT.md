# Same-image continuum transport bracket

The original periodic 48^3 pore cell now has a finite exact tensor enclosure

    L <= K_original <= U <= (231/20) L,

where L is the frozen, root-reviewed solenoidal-spline lower tensor. These are Loewner inequalities for every force vector, with the gradient-form unit-viscosity convention and total-cell volume normalization. Root whole-read and accepted the upper proof, numerical generator, separate exact consumer and actual receipts at this model-side scope; see ROOT_REVIEW.txt. The large solve and exact consumer were not rerun for review.

In voxel-squared units the upper tensor is approximately

    [[0.1586469283364664, 0.0101268402014091, 0.0130005654853557],
     [0.0101268402014091, 0.1226683579942858, 0.0138108808826480],
     [0.0130005654853557, 0.0138108808826480, 0.1240937185715633]].

All entries are stored as exact rational numbers in UPPER_CERTIFICATE.json. The sharp generalized factor for these two retained tensors lies in [11.542365186920506,11.542365186945062]; the simple certified factor is 11.55. The broad interval does not establish high-accuracy continuum permeability. The existing lower floor K >= .01 h^2 I remains valid, with the supplied h=5.345 micrometres.

## Acquired operation

Nine row-wise RT0 stress fields are defined on every original voxel face adjacent to fluid. No pore erosion or stress smoothing is used by this upper. Each fluid-cell divergence is repaired to the exact prescribed force using an integer tree-to-wall correction; the solid supplies the necessary counterforce on the periodic torus. A separate consumer checks all original faces, all nine integer force components, the wall totals and the original public image, then integrates the full deviatoric RT0 energy exactly. It imports neither numerical producer. This makes the result a continuum upper rather than a finite-element point prediction.

The ordinary scalar-Poisson initializer gives the exact isotropic upper 1.8556044293307536 I in voxel-squared units. Taking its deviatoric part gives a tensor with all-force bracket factor 151.24. The optimized, exactly repaired tensor Loewner improves that starting tensor and reduces the factor to 11.55. This is a comparison with the implemented initializer, not evidence of superiority over established equilibrated Stokes/FEM/FFT methods.

The numerical stress system has 470892 mixed unknowns. Its algebraic V-cycle uses a dense solve only for a 27-by-27 coarsest matrix. All three MINRES solves reached the fixed 800-iteration cap and returned nonzero status. No requested convergence tolerance or optimality claim is consumed. Exact equilibrium and energy checks establish the upper regardless of those caps. New producer time was 60.421907 seconds and its exact consumer took 1.248836 seconds. Including the previously recorded lower solve and all three lower consumer runs, completed computation totals 123.953246 seconds, excluding source/network, interpreter startup, proof development and review time. Peak resident memory was not measured. No new image, crop, physical experiment, paid compute or public write was used.

## Standard energy-error consequence

For force f, let v_f be the optimal combination of the retained three-column primal span and sigma_f the same force combination of the equilibrated stresses. Its normal equations give

    <|grad v_f|^2> = f dot <v_f> = f^T L f.

Integration by parts gives <dev sigma_f:grad v_f>=-f dot <v_f>. Consequently

    <|grad v_f + dev sigma_f|^2> = f^T(U-L)f,
    <|grad(u_true-v_f)|^2> = f^T(K_original-L)f <= f^T(U-L)f.

This is the established hypercircle/complementary-energy consequence, independently checked by root, with total-cell averages and the same h scaling. It needs no pressure observation or exact continuum reference solve. The broad retained gap gives a broad error bound.

## Scientific and physical boundary

The upper closes the missing two-sided mathematical interface for this one original periodic image. It does not qualify an actual rock. Transferring both bounds requires warranted inner AND outer physical pore inclusions, the periodic/RVE interpretation, no-slip continuum flow law, fluid calibration and scale. The image alone supplies none of those geometric or physical warrants. No general convergence rate, tightness guarantee, historical novelty, incumbent computational advantage or practical discovery multiplier is claimed. See PRIOR_AND_COSTS.md for the equally informed ordinary comparison.
