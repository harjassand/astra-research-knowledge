# Independent receiving review: objective-specific response is not tensor-compositional
2026-10-29. Reviewer: producer-workspace/sharpen_noreset_acquisition_certificate.

## Decision and scope
ACCEPT the two specified governing notes at their stated mathematical scope. The new obstruction does not alter the accepted one-use information-support recovery theorem. It proves neither novelty, a capacity separation, a coding advantage, nor a lower bound requiring full channel/environment tomography. The optimized quantity in the example is recovery fidelity **after the fixed specified repetition encoder**, not optimization over all encoders.

## Algebraic quotient argument
For fixed finite input and output spaces, equality on traceless operators gives N−M=Tr(.)Δω. If any traceless Hermitian H has common nonzero image Y, the traceless tensor input H⊗I/d gives tensor difference Y⊗Δω. A nonzero tensor factor has zero tensor product only if the other is zero. Thus tensor-response equality forces Δω=0, hence N=M. If the traceless response is identically zero both channels are replacements, and every tensor power is again a replacement, so this exception really survives. Hermitian traceless operators span the complex traceless space. For d=1 only the replacement case exists.

The quantitative bound follows from exact trace-norm multiplicativity on tensor products and ||I/d||1=1. The unit sphere of the finite-dimensional traceless Hermitian space is compact, so the supremum s is attained when that space is nontrivial. The claim concerns the induced norm restricted to traceless Hermitian inputs, not a normalized channel distinguishability convention; no factor 1/2 belongs in its stated bound.

## CPTP and predecessor boundary
I independently reconstruct both channels from their normalized input-first Choi matrices using N(A)ab=2 sum_ij Aij J_(ia,jb). Both have partial output trace I/2 and nonnegative exact spectra. Their identity outputs differ but each sends X,Y,Z to X/5,Y/5,Z/5. For every TP recovery R, its adjoint is unital positive, hence −I≤R*(Pauli)≤I. The three response terms are at most 2/5 each, and identity recovery attains them. Thus single-use Fopt=1/4+3(2/5)/8=2/5.

The first channel is explicitly the convex combination (1/5)D_X+(1/5)D_Y+(1/5)D_Z+(2/5)Replace(I/2), where each D_P(A)=(A+PAP)/2 is rank-one Pauli measurement/repreparation. This independently proves EB without a separability solver. The second Choi partial transpose has eigenvalue (2−sqrt(5))/10<0, so the channel is not EB: applying it to half a Bell state produces an entangled state. Exact spectra and all four matrix-unit identities are in the independent check.

For context the primary Horodecki separability paper https://arxiv.org/abs/quant-ph/9605038 explicitly states PPT sufficiency in 2×2/2×3, and Horodecki–Shor–Ruskai https://arxiv.org/abs/quant-ph/0302031 studies EB and its equivalent characterizations. Their abstracts were read in this review; the explicit decomposition/negative-PT witness above is self-contained and does not require importing their nontrivial sufficiency proof.

## Exact all-recovery optimum of the encoded channel
For any qubit-input completed channel C, Fe(I/2,RC)=1/4+(1/8) sum_P Tr[P R(C(P))]. This follows by expansion in the orthogonal Pauli basis; trace preservation fixes the identity contribution, regardless of the output background.

The independent Choi-first tensor calculation gives, on the repetition subspace, Delta_X=(|00><11|+|11><00|)/25, Delta_Y=(−i|00><11|+i|11><00|)/25, and Delta_Z=diag(1+t,−t,−t,−1+t)/5. Thus on 0≤t≤4/5 their trace norms are 2/25,2/25,2(1+t)/5. Each response term is bounded by its norm using the unital-adjoint argument. This is an analytical bound over **all** CPTP recovery maps, not a numerical optimizer result or merely a tested decoder.

The three specified Kraus operators have sum K†K=I4 and attain each norm simultaneously. Hence Fopt=1/4+[4/25+2(1+t)/5]/8=8/25+t/20. Endpoint values are 8/25 and 9/25. A direct logical Choi reconstruction and Bell overlap independently agrees, avoiding reliance only on the response expansion. The physical interpolation 0≤t≤4/5 is CPTP by convexity between the checked endpoint Choi matrices.

The norm-one witness (X/2)⊗(I/2) has tensor-output difference (X/10)⊗(−2Z/5), trace norm 4/25. This saturates the stated lower bound for these maps (s=1/5 and background separation 4/5).

## Reproducibility and qualification
`independent_check.py` uses exact SymPy algebra, a Choi-first implementation different from the author's Bloch-first tensor routine, explicit EB decomposition, a symbolic interpolation, and direct Choi fidelity checks. Both author scripts were copied into `replay/` and rerun without editing original sources; JSON matches are recorded separately. Diagnostics do not constitute physical execution. No claim about worst-case recovery, channel capacity, Petz-map identity, or universal task sufficiency is inferred from this objective-specific result.
