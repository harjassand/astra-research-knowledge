# Finite-energy local-Zak bridge — candidate direct derivation

Status: freshly derived 2 November 2026; independent review pending. This is a bridge for a fixed strict ideal GKP code margin, not a newly positive noise point or practical device claim.

## Proposed operation

Let Lambda be a full-rank commuting displacement lattice with logical dimension d, Gamma=Lambda^perp, and C a bounded fundamental domain of Gamma with 0 in its interior. Its joint stabilizer spectral representation is a direct integral of d-dimensional fibers over C. In a local neighborhood of zero choose the basis |b,s>=D(s)|b,0>. The symbols at s=0 are generalized vectors; the actual encoder below is a normalizable wavepacket, not preparation of those vectors.

For normalized phi in C_c^infinity(C), supported in a radius-r neighborhood of zero, define the isometry V_phi using the direct-integral function s -> phi(s)|b>. This has exact V_phi^*V_phi=I_d. There is no Gram matrix inversion.

In a measurable canonical section, a displacement xi acts as

    D(xi)|b,s> = scalar phase * W_gamma |b,s_out>,
    s_out = section(xi+s mod Gamma),
    gamma = xi+s-s_out in Gamma.

W_gamma is the logical Pauli represented by gamma mod Lambda. Its scalar phase drops out after syndrome measurement/trace. For additive noise density f_v(xi), the actual encoded/reference-preserving decoded channel is thus EXACTLY the ideal logical-plus-analog-syndrome decoder with displacement density

    f_eff(z) = integral_C |phi(s)|^2 f_v(z-s) ds.

This follows by setting z=xi+s after the syndrome partial trace: off-diagonal syndrome amplitudes vanish. It is not replacing a coherent output state by its average before the measurement.

Consequently half the diamond distance to the ideal f_v decoder is at most

    TV(f_v * |phi|^2, f_v)
      <= integral |phi(s)|^2 TV(N(s,vI),N(0,vI)) ds
      <= r/(2 sqrt(v)).

The last inequality is Pinsker applied to KL=|s|^2/(2v). A slightly sharper exact Gaussian translation formula is available. The reference dimension can be arbitrary for the channel bound.

## Why the encoder has finite energy: explicit one-mode canonical chart

Take logical dimension d, q-stabilizer period L=d a, p-stabilizer period 2pi/a. The dual cell has u-width a and v-width b=2pi/(d a). For q=j a+m d a+u, j=0,...,d-1, m integer, u in (-a/2,a/2), set

    (V_phi|j>)(q) = b^(-1/2) integral_{-b/2}^{b/2}
                  phi(u,v) exp[i v(j a+m d a+u/2)] dv.

The formula applies to the q strips labelled j; it is zero in strips belonging to other logical labels. Compact u-support away from boundaries makes the assembled functions smooth. Fourier-series Parseval gives exact orthonormality. Compact smooth v-support gives rapid decay in m, hence finite q energy. Explicit integration by parts gives

    <q^2> = integral |(i partial_v+u/2)phi|^2 du dv,
    <p^2> = integral |(-i partial_u+v/2)phi|^2 du dv.

Both are independent of j. The same differential operators preserve the logical label, so energy is bounded uniformly on every logical superposition. For a scaled smooth bump phi_r(s)=r^(-1)phi_1(s/r), the energy is O(r^-2+r^2), with explicit bump-derivative constants.

Tensor products give the canonical multimode case. Integer symplectic normal form and a metaplectic unitary take any commuting lattice to this form. A physical quadratic-energy bound picks up the squared norm of that fixed symplectic transformation. This constant must be reported for any proposed lattice; existence is not low cost.

## Capacity consequence if the ideal margin is actually acquired

If an ideal d-dimensional inner code has coherent information Delta>0, choose r so that, with delta=r/(2sqrt(v)),

    2 delta log_2 d + (1+delta) h_2(delta/(1+delta)) < Delta.

Conditional-entropy continuity with finite reference dimension d then preserves positive coherent information for the physical finite-energy code. No output-dimension entropy cutoff is needed. The continuous syndrome can subsequently be quantized: bounded smooth Gaussian image densities on a compact syndrome cell imply convergence of conditional logical entropy under refining finite partitions. An explicit bin count and physical decoder cost remain to be supplied for a practical architecture.

## Crucial scope

- This does NOT establish rho>beta for any new seed/noise regime.
- The encoder/decoder is an exact Hilbert-space operation; no efficient circuit, finite-resolution experimental syndrome instrument, photon-number preparation recipe, or useful rate is asserted.
- The local chart avoids bundle-boundary singularities by compact support; a global smooth trivialization is not assumed.
- Decoder outputs a finite logical register and syndrome record. It does not physically project onto a nonnormalizable GKP vector.
- Exact bounded-displacement correction in this construction would not contradict the impossibility of correcting unbounded Gaussian displacement tails. Gaussian-envelope GKP states have noncompact syndrome tails and are not the same encoder.

## Finite implementation existence, with potentially terrible costs

The ideal stabilizer decoder itself must not be called a finite-energy laboratory instrument: Shaw–Doherty–Grimsmo explicitly warn that exact syndrome extraction needs ideal ancillas. A separate finite-dimensional receiver approximation avoids silently granting it.

For m physical modes and encoder mean-energy bound E_in, additive displacement noise gives E_out<=E_in+m v. Project the receiver onto total photon number <=M, replacing its complement by an erasure flag. Markov plus a gentle-projection estimate bounds the additional reference-preserving trace-distance error by sqrt(E_out/(M+1))+E_out/(M+1). Thus an error budget delta can be reached with M=O(E_out/delta^2). The retained Hilbert space has dimension binom(M+m,m); it is finite but can be enormous.

Quantize the analog syndrome into finitely many cells. Replacing each logical-Pauli joint syndrome density by its average on each cell gives a finite instrument followed by classical within-bin randomization. The channel error is bounded by the total L1 histogram error. Gaussian convolution gives integrable derivatives: integral |grad f_v| <=sqrt(2m/v). Standard histogram Poincare/translation bounds then make this error vanish with cell diameter; a concrete lattice chart determines the geometry constant. Finite output dimension d times the bin count and the Fock cutoff admit a finite Stinespring implementation. This establishes finite-resource existence, not a short circuit: generic unitary synthesis, bin count, cutoff dimension, energy and preparation all remain paid.

Primary antecedents: Shaw, Doherty, Grimsmo, *Stabilizer Subsystem Decompositions for Single- and Multimode GKP Codes*, PRX Quantum 5, 010331 (2024), https://arxiv.org/abs/2210.14919; Pantaleoni, Baragiola, Menicucci, *Zak transform as a framework for quantum computation with the GKP code*, PRA 107,062611 (2023), https://arxiv.org/abs/2210.09494. Compact-support syndrome filters and finite-energy fault-tolerance are also used in the 2026 primary https://www.nature.com/articles/s41467-026-69036-5 . No novelty of subsystem encoding or physical GKP existence is claimed.

## Explicit finite-energy syndrome bump

A C_infinity bump is unnecessary for finite mean energy. Take f_r(x)=r^(-1/2) cos(pi x/(2r)) on |x|<=r, zero outside, and phi(u,v)=f_r(u)f_r(v), with its square strictly inside the canonical syndrome cell. This belongs to H1 and is sufficient for both quadrature second moments. Direct exact integrals are

    integral f_r²=1,
    integral |f_r'|²=pi²/(4r²),
    integral x² f_r²=r²(1/3−2/pi²).

Therefore one canonical mode has, uniformly over logical states,

    <N> = pi²/(4r²) + r²(1/3−2/pi²)/4 −1/2.

For m tensor-product canonical modes multiply by m; a physical symplectic transformation pays its quadratic-energy condition factor. The support radius in 2m-dimensional physical canonical phase space is r sqrt(2m), so the earlier channel-error bound is at most r sqrt(m/(2v)) before the symplectic-coordinate conversion. This displays the energy/error trade rather than concealing it behind 'finite energy'.
