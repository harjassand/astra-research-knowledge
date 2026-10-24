# Equal-marginal obstruction to the saturated resolvent compiler

24 October 2026. This rules out specified compiler architectures, not the general channel-order equivalence.

## Source actually checked

N675, EXTRACTED_TEXT.txt lines154–325, especially its equations8–12. This note uses only the displayed finite-dimensional filter construction, not the source's unreviewed hardness assertions.

The source chooses α=ρ⊗τ and β(t)=(ρ⊗W+tH⊗L)/TrW, where W is diagonal, τ=vv* is coherent on auxiliary leaves, and L couples a centre to the leaves. The two channels have identical relative entropy at t=0 because the physical baseline is the same. The denominator Hessian contains the squared coherent filter |Σ_k c_k/(s+λ_k)|². Signed residues allow localization at s=1 and produce the SLD kernel.

If Tr_A H=0, equal reference marginals still require τ=W/TrW. This removes the coherent offdiagonal entries of τ in W's eigenbasis. The Hessian therefore loses cross-leaf terms: it is an incoherent sum of positive single-leaf contributions. The signed-residue concentration mechanism no longer exists. Adding an untouched classical flag does not fix this, because equality of the entire reference marginal holds separately in each flag block.

More generally, any same-reference pair that is saturated universally for all channels must be identical. Apply saturation to the identity channel versus the replacer: D(α||β)=D(α_R||β_R)=0, so α=β. Thus universal saturation with equal marginals inevitably returns to ordinary same-point BKM Hessians. Non-product constructions may still work; this is not a no-go theorem for all constructions.

## Positive tensor-product metric compilation cannot isolate SLD either

Consider a fixed product baseline σ⊗W, W>0 diagonal, and tangent H⊗C with C=C*. The BKM kernel in an ordered physical eigenpair (a,b) is a positive sum of kernels

k_{w,z}(a,b)=[log(aw)−log(bz)]/(aw−bz).

There are no negative coefficients, because the tensor tangent contributes |C_kl|². Direct substitution in the scalar resolvent identity gives

k_{w,z}(a,b)=∫_0^∞ dt /[(w t+z)(a+b t)].

Thus any finite positive combination has Stieltjes density h(t)=Σ c_j/(w_j t+z_j), c_j>=0. The density is decreasing. Normalizing the compiled kernel by its value at (a,b)=(1,1) yields a probability measure with density proportional to h(t)/(1+t), still decreasing. In contrast, normalized SLD kernel 2/(a+b) corresponds to the point mass δ_1 in this representation, since
K(a,b)/K(1,1)=∫(1+t)/(a+bt) dμ(t).

No sequence of decreasing probability densities can converge weakly to δ_1: for 0<ε<1, its mass in [1−ε,1+ε] is at most 2ε/(1+ε). Pointwise convergence of the normalized Stieltjes transforms to 2/(a+b), for all a,b>0, would force precisely that weak convergence, including exclusion of mass escaping to0 or∞ by the endpoint limits and uniqueness of Stieltjes transforms. Hence fixed tensor-product baselines and positive sums of tensor-product tangent metrics cannot universally approximate SLD this way.

This obstruction permits arbitrary finite ancillary spectra and tangent matrices, and finite positive sums of such compilers. It does NOT cover baselines correlated between the physical system and the auxiliary reference, coefficients that depend on the physical spectral pair, or order arguments that do not approximate kernels by a universal positive mixture.

## Consequence for the live problem

The implication equal-reference Umegaki comparison => equal-reference BKM comparison follows by local differentiation. Complete equal-reference SLD comparison => unrestricted conditional comparison follows from the team's exact SLD gauge and auxiliary-qubit integral. The missing reverse BKM-to-SLD implication is not supplied by N675's coherent denominator filter or by a positive tensor-product BKM mixture. A successful proof must exploit genuinely correlated baseline geometry, or a different order-theoretic argument.
