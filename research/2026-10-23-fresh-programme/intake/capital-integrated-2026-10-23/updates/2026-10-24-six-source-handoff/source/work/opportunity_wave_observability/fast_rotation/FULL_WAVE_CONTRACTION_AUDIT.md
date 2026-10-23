# Independent check: finite-volume scalar Helmholtz scattering bound

**Verdict: the stated bounds and constants check out under the stated free-space, real scalar-potential model and angular-measure convention.** The Neumann-series estimate needs only `q∈L∞` supported in a measurable finite-volume set; it does not extend by itself to an arbitrary resonant background, Maxwell operator, or hard obstacle. A real static contrast gives a unitary one-particle scattering operator, which can be second-quantized as a number-preserving bosonic scalar-wave channel. Calling that an *optical* implementation requires additional physical modeling; as written it is most accurately an ideal scalar-wave access model.

## Contraction and constants

Use ordinary surface measure on `S²` (area `4π`) and the outgoing Green function

`G(x)=e^(ik|x|)/(4π|x|)`, so `(Δ+k²)G=−δ`.

Then `(Δ+k²)u=−k²q u` yields the stated plus-sign Lippmann–Schwinger equation

`u = uin + T_Du`, `T_Du(x)=k²∫D G(x−y)q(y)u(y)dy`.

For any `x`, the Hardy–Littlewood rearrangement bound is attained by placing the full volume in a ball centered at `x`. With `R=(3V/(4π))^(1/3)`,

`∫|z|≤R (4π|z|)^(−1) dz = R²/2 = c0 V^(2/3)`,

where `c0=0.5(3/(4π))^(2/3)`. Therefore `||T_D||∞→∞ ≤ k²Q c0V^(2/3)=θ`. If `θ<1`, the restriction of the LS equation to `D` has a unique `L∞(D)` solution by a convergent Neumann series and

`||u||L∞(D) ≤ ||uin||L∞(D)/(1−θ)`.

This is an actual finite-size weak-scattering condition, not a low-frequency expansion truncated at first order. The estimate uses `|G|=1/(4πr)`, so its constants are independent of oscillatory cancellation and of the shape of `D`.

For `uin(x)=∫S² e^(ikd·x)g(d)dΩ`, `|e^(ikd·x)|=1` and Cauchy–Schwarz give

`||uin||L∞(D) ≤ ||g||L1(S²) ≤ √(4π)||g||L2(S²)`.

With far field convention `us(r xhat)=e^(ikr)F g(xhat)/r+o(r^(−1))`, the Green asymptotic gives

`Fg(xhat)=(k²/(4π))∫D e^(−ik xhat·y)q(y)u(y)dy`.

Hence for each `xhat`, `|Fg(xhat)|≤(k²/(4π))QV ||u||∞`. Taking the output `L²(S²)` norm adds `√(4π)`; the input Herglotz bound contributes another `√(4π)`, which cancels the denominator `4π`. Thus

`||F||L²(S²)→L²(S²) ≤ k² Q V/(1−θ)`.

For Petkov's 3-D convention `S(k)=I+(ik/(2π))F(k)`,

`||S−I|| ≤ k³ Q V/[2π(1−θ)]`.

Changing the time-harmonic or outgoing-wave convention can conjugate/sign-flip the amplitude relation; it does not alter these norm bounds. Since the real, lossless scattering operator is unitary, one can also append the trivial cap `||S−I||≤2`.

## Scope of the scattering map

Here `q` is a real, static, bounded contrast with compact support, and `1+q>0`; there is no absorption or frequency conversion in the model. The outgoing scattering solution has conserved flux, and its on-shell angular scattering matrix is unitary with the matching flux normalization. Therefore it is mathematically valid to lift `S(k)` to bosonic Fock space by `Γs(S(k))`: this is a passive, number-preserving linear transformation of the monochromatic scalar-boson modes. This does not mean that arbitrary such `q` is available as a material or that the construction has been experimentally realized.

The safest label is **ideal lossless bosonic scalar-wave probe**. It is an optical-like access model at the level of monochromatic wave scattering, but it is not yet an optical device theorem: actual photons have vector/polarization structure, material permittivity is dispersive and may absorb, and Maxwell interface/derivative operators are not bounded by this scalar volume estimate. A physical acoustic scalar field could also motivate the equation, but a specific medium must still realize the assumed coefficient and flux normalization. A full wavepacket/Fock implementation would need the frequency-dependent direct-integral scattering map and a causal dispersive material model; the single-frequency result alone makes no such broadband claim.

The contraction applies to free-space `G` and its scalar multiplicative potential. It does not imply a small norm for `k²q` composed with a known-background resolvent near resonance, nor for obstacle boundary integral operators or Maxwell systems. In those settings a separate resolvent/operator estimate is required.

Normalization reference: Petkov's author PDF, p. 2, gives the 3-D relation between the angular scattering matrix and scattering amplitude in the convention used here ([author PDF](https://www.math.u-bordeaux.fr/~vpetkov/publications/Weyl.dissipative5.pdf)). The sign is tied to the outgoing `e^(ikr)/r` convention; the norm claim is insensitive to it.
