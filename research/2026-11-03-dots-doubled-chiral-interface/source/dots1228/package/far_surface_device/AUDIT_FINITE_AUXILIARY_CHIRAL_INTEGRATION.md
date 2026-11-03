# Final independent integration audit: finite auxiliaries with the exposed far band

2026-11-03. Audited `FINITE_AUXILIARY_CHIRAL_DEVICE_INTEGRATION.md` against the corrected global-norm rest transfer, shared-rotor disentangler, and finite-auxiliary minmax construction.

## Verdict

The integration passes. This closes the previously missing connection between the bounded-rotor exposed-band device and a NEW finite-auxiliary/coercive model. It does not assert preservation of the old excited rotor spectrum. The argument re-earns a rest gap for the new model and retains a full-norm comparison to its free target factor.

## Exact factorization survives the operations

The actual D_g consists of rotor shears/cochain phases and decoration-Majorana rotations. It does not act on free Wilson fermions. Fixed free-copy basis identifications were already incorporated in the definition of the compatible target projector; they are not additional angle-dependent gates in D_g. Thus D_g acts identically on F. Its gates are even, so no graded tensor-product sign is hidden.

The physical Fourier cutoff and the new sum L_j^2 act only on rotor factors. They likewise commute exactly with F. Consequently the bounded difference

 H_device-C_ref-(H_F+K_Q)

keeps norm <=delta after unitary conjugation and compression. Adding the SAME unbounded kappa K to both conjugated operators leaves this bounded difference unchanged, on their common standard kinetic domain. This is valid even though D_g itself does not preserve a bare kinetic domain: K is introduced only AFTER the conjugation, not transformed through D_g.

The full symmetric target momentum ball, complete species, and conjugate/real-structure compatible second-copy/hole projectors are essential. They supply a valid fixed CAR/BdG decomposition and the correct compensated rest parity. The canonical doubling multiplicity remains physical and is not removed by the factorization.

## Actual Q-ground regularity and the new minmax gap

Since Q is fixed in rotor configuration,

 ||partial_j(QhQ)||_1<=||partial_j h||_1.

The uniform compressed fast gap therefore supplies the same trace-norm sign derivative and phase-fixed Gaussian-vector derivative bounds as before. Spatial nonlocality of Q does not spoil this estimate. The disentangler's local chamber/shear bookkeeping then gives the actual Q-ground Fourier tail tau_N<=A_Q/N. No unknown strict-parent ground vector or ground-response oracle is used.

The norm bound B_Q=2 n_fast R_fast+m is conservative when all copies, decoration scales, and reset weights are included. For N0>=max(2A_Q,4B_Q A_Q/e), the normalized projected canonical trial has rest energy <=e/2. Choosing kappa<=e/(2mN0^2) keeps total trial energy <=e. Positivity and minmax give, for EVERY L>=N0,

 0<=lambda0(R_kappa,L)<=e,
 lambda1(R_kappa,L)>=Delta,
 gap>=Delta-e.

For a polynomial coercive-regulator resource statement, take the explicit value kappa=e/(4mN0^2). Kappa=0 is also valid for the already finite compressed model. Arbitrarily smaller positive choices should not be advertised as giving the same polynomial cutoff bound.

The same inequalities hold before compression for positive kappa by the closed-form construction and compact rotor resolvent. The original discontinuous ground need not lie in the kinetic form domain; only the finite Fourier trial does.

## Energy conventions and low spectral content

The absolute cutoff statement requires the convention

 H_F=dGamma(h_F)-E_F,0>=0.

The known free Fock ground energy E_F,0 must be included in the overall C_ref convention. The constructor has incorporated this clarification and explicit one-body reference-energy acquisition formulas. Without that normalization an absolute cutoff below Delta would be incorrectly shifted by an extensive negative free ground energy.

The new rest ground energy E_rest is only known to lie in [0,e]. It is NOT silently zero. Below the rest threshold the comparison states are exactly target free Fock excitations tensored with this unique new rest ground. At a cutoff below Delta-delta, separated by more than delta from the comparison spectrum, bounded-perturbation continuation preserves the finite spectral-projection rank. Relative excitation errors are at most 2delta; a conservative rest threshold is Delta-e-2delta.

A known absolute counting/QPE window must charge the full E_rest interval or choose e below its desired resolution, as well as any numerical C_ref error. C_ref can be acquired from the explicit finite fixed-texture one-body matrix, with the correct nonredundant/BdG normalization; that is not an interacting-state oracle.

Full finite-device ground uniqueness additionally requires

 2delta<min(Delta-e,p_min,lattice).

There is no volume-independent full gap at an exposed Weyl surface. The rest gap and the far finite-size level spacing must not be conflated.

## New-model response

The comparison Hamiltonian, INCLUDING the kinetic addition and compression, remains H_F plus an even Q/rotor operator. Hence target CAR evolution is exactly free in that comparator. Bounded-perturbation Duhamel gives the stated

 4|t|delta ||f||||g||

anticommutator error for every state of the new device. This remains valid before finite rotor compression for positive kappa because the two unbounded Hamiltonians differ by a bounded operator and share the same kinetic domain. No old-model low-energy or thermal approximation is being invoked.

The continuum dispersion allowance remains separate. Gauge-field dynamics, continuum renormalization, and practical resource claims are not consequences.

## Resource and package scope

A_Q and B_Q are polynomial in the actual finite volume with fixed microscopic parameters; N0 and the explicit inverse kappa are therefore polynomial. The inherited physical range/thickness is volume dependent, of squared-logarithmic form with astronomical constants. Local rotor dimension and logical qubit counts are paid; total Hilbert dimension remains exponential.

Compilation error adds directly to delta, provided the already-audited valid-code, Hermiticity, charge-pinch, and moving-wall quadrature corrections are retained. This gives a finite-volume ungauged existence/operation package, not a fixed-range/fixed-local-dimension thermodynamic chiral-gauge theorem.
