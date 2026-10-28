# Unknown orthogonal reset: relative learning to reusable decoding

2026-10-27. Root construction, independent audit requested. Acquisition lemma is being constructed separately; the deterministic receiver bridge below does NOT assume an unknown whitening oracle. No novelty claim.

Source E(rho)=p V(rho tensor sigma)V*+(1-p)Tr(rho)tau, tau V=0, rank sigma<=r, p>=p0>0. Ambient output dimension s is known. J is normalized Choi, omega=I3/3 tensor E(I3/3), T=(J+3omega)/4. Receiver-local labelled samples of T and omega cost one source use each.

## Relative Hermitian learning interface
For every known Weyl label j let H_j=J_j-3omega=4T_j-6omega, A_j=J_j+3omega. Suppose the learned classical Hermitian Hhat_j satisfies
 -eta(A_j+t I)<=Hhat_j-H_j<=eta(A_j+t I), t=p0/r, eta<=1/4.
The projectors used below are computed from Hhat_j, not supplied. The same acquisition of T and omega can be Weyl-rotated; failure is a single training event.

The positive spectral projector Pi_j of H_j has rank<=r. On its Bell code band H_j has eigenvalue 2p sigma/3; on the other eight code bands it is -p sigma/3; on reset it is -2(1-p)tau/3. Thus |H_j|>=A_j/2, Tr(H_j)_+=2p/3. All nine true Pi_j are orthogonal and give exact teleportation recovery with known Weyl correction.

Let P_j be the projector onto at most r largest positive eigenvalues of Hhat_j. It maximizes Tr Hhat_j P among projectors of rank<=r. Put
 L_j=Tr(H_j)_+-Tr H_j P_j=Tr|H_j|(Pi_j-P_j)^2.
The last identity uses commutation of Pi_j and H_j, not commutation of P_j.
Optimality gives L_j<=Tr E_j(P_j-Pi_j). Relative order and ranks bound this by eta[Tr A_j P_j+Tr A_j Pi_j+2tr]. Since A_j<=2|H_j|,
 Tr A_j Pi_j<=2 Tr(H_j)_+,
 Tr A_j P_j<=2[Tr(H_j)_++L_j].
Consequently L_j<=[(8/3)eta p+2eta tr]/(1-2eta)<=10 eta p.
This bound pays arbitrarily tiny flag eigenvalues and arbitrary unknown reset spectra.

## Complete sequential receiver
Create a local normalized qutrit Bell ancilla, measure P_1,...,P_9 sequentially on its first half and the physical datum, retain the registers after each rejection, apply the known correction on first acceptance, and erase after all failures. Discard measured registers after acceptance. All P_j have classical descriptions; no new source queries/programs are used at deployment.

Split omega=omega_code+omega_reset, with masses p and 1-p. From the exact spectral structure, |H_j|>=3 omega_code and |H_j|>=2 omega_reset. Thus Tr omega_code(P_j-Pi_j)^2<=L_j/3 and Tr omega_reset P_j<=L_j/2.

For arbitrary logical datum entangled with an external reference, the original success branch has mass p and measured-register marginal <=3 omega_code. Under any ideal preceding rejections this domination remains true, because the ideal Pi_j commute with omega_code. Compare the retained binary measurement isometries W_P=|yes> P+|no>(I-P) and W_Pi. Their squared difference on a state is 2Tr(P-Pi)^2 rho. A hybrid with ideal prefixes and actual suffixes therefore bounds total success-branch unhalved trace distance by
 2 sqrt(p) sum_j sqrt(2 L_j)<=18 sqrt(2p Lmax).
This is uniform in the external reference, hence a complete bound. Known corrections and discarding registers are contractive.

For reset compare the actual sequential measurement isometry with the always-reject isometry. On a purification of omega_reset, each hybrid difference has norm sqrt(2Tr P_j omega_reset). Projecting the final difference onto the accepted outcome subspace gives total accepted reset mass <=2*9 sum_j Tr P_j omega_reset<=81 Lmax. Replacement by erasure costs twice the accepted mass, <=162 Lmax. No arbitrary rejected-state domination or ordinary gentle square-root noise bound is used.

Combining,
 ||Dhat E-G_p||_diamond<=18 sqrt(2p Lmax)+162 Lmax
 <=p[18 sqrt(20eta)+1620eta].
For example eta=nu^2/100000, 0<nu<=1, makes the good-event error <nu p/2. With training failure probability <=nu p0/4, the averaged complete error is <=nu p. The decoder is a reusable classical device; a joint multi-use guarantee still charges accumulated good-event error and the one-off bad-training event.

## Proposed acquisition reduction, not yet received
Learn T and omega with individual relative order error eps(state+tI). Then E_H=4E_T-6E_omega is bounded by eps(4T+6omega+10tI). Since 4T+6omega=J+9omega<=3A, this is <=10eps(A+tI). Thus eps=eta/10 suffices. Proposed acquired-relative tomography cost is O(d/t eps^-2 polylogs), d=3s, yielding O(sr/(p0 nu^4) polylogs). This final complexity statement is conditional until the independent geometric-preconditioner construction is received. It does not claim efficient collective measurement, gate synthesis, or efficient historical novelty.
