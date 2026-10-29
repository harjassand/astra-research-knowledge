# Limited-measurement obstruction for rotated parity records
2026-10-29. Exploratory exact observation, NOT a general sample-complexity lower bound or new recovery theorem.

Let O=⊗_(j=1)^n (v_j·sigma), real unit Bloch vectors v_j, and rho_+=(I+O)/2^n. This is a valid state with maximally mixed proper marginals for n>=2. It arises as the encoded logical-Z training state of a parity-type classical reversible encoder with maximally mixed junk, followed by local rotations; this observation alone does not specify a complete logical recovery architecture.

Measure each site pair of two IDENTICAL copies rho_+ tensor rho_+ in the standard Bell basis |Phi_P>=(I tensor P)|Phi>, P in{I,X,Y,Z}. For a tuple of outcomes P_j,
 p(P_1,...,P_n)=4^(-n)[1+prod_j a_j(P_j)],
 a_j(P)=Tr[(v_j·sigma)^T P†(v_j·sigma)P]/2.
Explicitly a=(1-2v_y²,1-2v_z²,-1,1-2v_x²) in the I,X,Y,Z convention. The transpose is essential: no unavailable complex-conjugation operation is assumed. With conjugated second copies the alternative b=(1,2v_x²-1,2v_y²-1,2v_z²-1) appears, but those copies are NOT supplied here.

The single-site sums of a vanish. Relative to the uniform outcome distribution u=4^-n, the exact chi-squared divergence is
 chi²(p||u)=prod_j[(sum_P a_j(P)^2)/4].
When every squared Bloch component is1/3 this is3^-n. More generally the local factor is sum_l v_l^4, since sum_P a(P)^2=4 sum_l v_l^4. The outcome law loses component signs identically, not merely approximately.

For M independent identical two-copy measurement blocks, chi²(p^M||u^M)=(1+chi²(p||u))^M-1; TV<=sqrt(chi²)/2. Thus for the isotropic-axis case this restricted fixed measurement cannot even distinguish the nonzero parity state from the maximally mixed state at constant bias with M=o(3^n) blocks. This concerns only the stated measurement and testing alternatives, not ALL collective quantum strategies, adaptive local measurement choices, or all training states of an encoder. The maximally mixed alternative need not belong to a promised exactly correctable encoder family.

This illustrates why importing mixed-stabilizer Bell learning unchanged can fail under continuous local rotations: at coordinate-axis Bloch vectors the factor is1, whereas balanced non-Clifford vectors give exponential attenuation. It does NOT establish a quantum advantage, a universal impossibility, or a practical new recovery mechanism. A meaningful continuation must exhibit a stronger physically supplied collective statistic or prove a suitably broad measurement lower bound; neither is supplied by this note.
