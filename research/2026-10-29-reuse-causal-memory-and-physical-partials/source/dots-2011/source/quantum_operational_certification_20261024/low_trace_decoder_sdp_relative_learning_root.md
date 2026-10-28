# Low-trace decoder SDP: relative learning without Bell-band projection

2026-10-27. Root new construction, independent receiving requested. This supersedes no received file. It gives an alternative reusable decoder and a possible robust interface.

Let E(rho)=p V(rho tensor sigma)V*+(1-p)Tr(rho)tau, with rank sigma<=r. First assume orthogonal reset; later identities do not require orthogonality. Use normalized qutrit Choi J, omega=I3/3 tensor E(I3/3), H=J-3omega, A=J+3omega. The acquired relative operator estimate obeys -eta(A+tI)<=Hhat-H<=eta(A+tI), t=p0/r, eta<=1/4.

## Convex operational decision set
Optimize Tr Hhat F over
 F>=0, Tr_A F<=I_B/3, TrF<=r.
Each such F is EXACTLY (id_A tensor D_acc^dagger)(Phi3) for a completely positive trace-nonincreasing accepted decoder D_acc:B->C3. Add erasure with the missing trace to obtain a CPTP instrument. Conversely every such decoder with Tr D_acc^dagger(I)<=3r belongs to this set. From the standard positive partial-trace bound F<=3I_A tensor Tr_A F, every feasible F<=I_AB. This is a finite semidefinite optimization of a linear objective; no nonconvex rank constraint, unknown subspace or exact diagonalization gap is used.

Define f=Tr J F and a=9Tr omega F. Direct adjoint duality gives f=<Phi3|J_(D_acc E)|Phi3> and a=Tr J_(D_acc E). Thus utility TrHF=f-a/3. The factor9 follows Tr_A F=D_acc^dagger(I)/3.

For the orthogonal-reset source, the true code inverse has feasible F=Pi, the rank<=r positive Bell projector of H, and TrH_+=2p/3. Let h=2p/3 and L=h-TrHFhat. Since 0<=Fhat<=I, L>=0. Furthermore
 Tr|H|Fhat<=h+L,
 Tr|H|Pi=h.
Indeed write positive and negative H parts, use TrH_+Fhat<=h, and note TrH_-Fhat<=L. Since A<=2|H|, variational optimality yields
 L<=eta[2(h+L)+2h+2tr],
 hence L<=10eta p exactly as for the received projector receiver. An additive SDP optimization tolerance delta adds delta/(1-2eta) to this risk bound and can be paid explicitly.

## Utility is an operational error loss, even with overlapping reset
Decompose accepted decoded Choi into genuine and reset branches. Write a_s,f_s for genuine acceptance and entanglement overlap and a_n,f_n for reset. The reset branch is input independent, hence f_n=a_n/9 exactly. Since 0<=f_s<=a_s<=p,
 L:=2p/3-TrHF
   =(2/3)(p-a_s)+(a_s-f_s)+(2/9)a_n >=0.        (1)
This holds for EVERY feasible decoder, regardless of reset overlap or spectral rank. Thus
 p-f_s<=(3/2)L,   a_n<=(9/2)L.
The genuine complete accepted-plus-erased Choi has trace p. Its unhalved trace distance from pPhi3 is <=2sqrt[p(p-f_s)] by the purified-state fidelity bound. The normalized-Choi-to-diamond inequality in input dimension3 therefore bounds genuine complete error by6sqrt(3pL/2). The reset's complete deviation from erasure is exactly2a_n<=9L. Consequently
 ||D E-G_p||_diamond <=6sqrt(3pL/2)+9L.          (2)
No postselection normalization or small-success denominator is hidden.

For orthogonal reset and exact SDP, L<=10eta p, so error<=p[6sqrt(15eta)+90eta]. The same eta=nu²/100000 from the received acquisition assembly gives substantial slack. In particular the original O(sr/(p0 nu^4) polylog) source cap remains valid, now with a direct computed CPTP decoder and linear SDP rather than nine sequential spectral tests. Quantum realization/circuit costs remain separate.

## Candidate robust comparison interface
Equation(1) also implies a=a_s+a_n<=p+(9/2)L and f<=a, hence TrAF=f+a/3<=4a/3. Suppose ANY comparator feasible F_* has true utility loss L_* (not assumed zero). Learned variational optimality and relative errors imply
 Lhat-L_* <=eta[TrAFhat+TrAF_*+2tr]
 <=eta[(8/3)p+6(Lhat+L_*)+2p0].
For eta<1/6,
 Lhat <=[(1+6eta)L_*+(14/3)eta p]/(1-6eta).       (3)
Thus near-ideal feasible decoding need not come from a nearby exact-erasure Choi state. It can be transferred directly through the learned utility. An actual comparator with controlled L_* must still be CONSTRUCTED from the source promise; equation(3) alone is not an entropy recovery theorem.

Source of covariance/acquisition: acquired_regularized_relative_operator_estimator.md and its separate receipts. This note's new content is the low-trace operational decision set and error-loss receiving, not a claim to invent generic channel-fidelity SDP optimization. Independent proof and finite matrix checks are requested before adoption.
