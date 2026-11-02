# Resource-bound correction: an even syndrome packet has a second-order error

This improves the conservative continuity estimate in `FINITE_ENERGY_ZAK_BRIDGE_DRAFT.md`; it is not a new encoder, decoder, or capacity witness.

Let the physical displacement density be the centered isotropic Gaussian f_v on R^(2m). Let h(s)=|phi(s)|² be normalized, have zero mean and finite second moment. The exact stabilizer-subsystem logical-and-syndrome channel from the common-packet construction is the ideal channel with displacement density f_v*h. Any finite flag quantization is a postprocessing of that channel.

Taylor's formula and E_h s=0 give

    f_v*h - f_v = E_s ∫_0^1 (1-t) sᵀ (∇²f_v)(·-ts) s dt.

For any unit direction u,

    ||∂_u² f_v||_1 = E|Z²-1|/v = 4 φ_standard(1)/v,

where φ_standard(1)=exp(-1/2)/sqrt(2π). Therefore

    TV(f_v*h,f_v) ≤ φ_standard(1) E|s|² / v.

The half diamond distance of the actual and ideal decoded logical/flag channels obeys the same bound, uniformly on reference-entangled inputs. For a nonsingular Gaussian covariance Σ, replace E|s|²/v by E[sᵀΣ^(-1)s]. No differentiability of h is required for this channel comparison.

For the real cosine packet from the earlier note, with each of 2m canonical coordinates supported in [-a,a],

    c = 1/3 - 2/π²,
    E|s|² = 2m c a²,
    δ ≤ 2m c φ_standard(1) a²/v,
    mean photon number = mπ²/(4a²) + mc a²/4 - m/2.

Thus the leading error-energy product is bounded by

    δ N ≲ m² π² c φ_standard(1)/(2v),

rather than the earlier O(N^(-1/2)) continuity estimate. This is an O(1/N) bound for a fixed mode count and fixed lattice shape. General symplectic squeezing still incurs its explicit energy/covariance factors; it is not free. The reference-dimension continuity estimate and finite receiver approximation costs from the earlier note remain required. In particular, an ideal analog decoder has not become a physically efficient finite-energy instrument by improving this inequality.

This cancellation also means that a tiny already-established ideal rectangular-code margin must not automatically be described as requiring the much larger photon count implied by a first-order support-radius bound.
