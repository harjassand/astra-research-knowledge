# Missing input-isotropy hypothesis in the encoded trace bound

28 October 2026. Independent reviewer audit_clock_and_bound identified a missing displayed hypothesis in NORMALIZATION_AND_STRUCTURED_CODE_v1.md Section1. Preserve that source; this addendum governs the correction.

The full-row identity BB†=(dN/D)I_D and normalization lower bound need only the displayed output isotropy. However the claim ||B(I_N tensor C)||_F²=KN for every code C also requires

    sum_i F_i†F_i=N I_d.

Add this input-isotropy hypothesis whenever using equation (2), its sqrt(d/K) trace-bound comparison, or any claim that the encoded-row Frobenius norm is KN. Under it, Tr(W†W)=Tr[C†(sum_iF_i†F_i)C]=NK, as required.

The missing implication is genuinely false without it: d=2,D=1,N=1,F_1=[sqrt(2),0] satisfies normalized HS orthonormality and the stated output-isotropy identity, but C=|1> makes W=0. This counterexample rejects the incomplete hypothesis, not the corrected statement.

The complete invariant Schur reference frames motivating the analysis have BOTH isotropy identities, by Schur's lemma and trace normalization. The flag-dephasing example also has both. Thus the corrected interface comparison applies there. The separate mutual-information normalization barrier uses only the unencoded row and is unaffected by this missing hypothesis. No additional decoder-hardness claim is introduced.
