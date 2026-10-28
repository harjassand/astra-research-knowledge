# Operator-valued Gram normalization for hidden classical-sector noise

28 October 2026. **Unreviewed ancillary derivation, not the canonical operator-metric source.** This was drafted concurrently with the root-owned operator-metric construction; no separate receipt, priority or completed acquisition claim is attached. Consult the root operator-metric source and its exact review status. This is a different mechanism from scalar Hilbert–Schmidt whitening. It addresses correlated changes of logical noise and spectator state that invalidate the scalar common-factor theorem. It is deliberately stated for a known finite physical patch, with its full matrix/control costs. No supplied readable flag or microscopic environment model is used.

## 1. Actual model and why the earlier route fails

A known d=2^w dimensional physical patch carries one unknown fixed logical qubit and an emitted gauge: U:C² tensor G -> P. Define B_j=U(sigma_j tensor I_G)Udagger for j=X,Y,Z. The learner prepares the logical qubit in ordinary uniformly random XYZ axes/signs and measures all w physical outputs in ordinary independent Pauli bases. It does not control or read a supplied gauge basis. An unknown payload is introduced only after acceptance.

On each allowed prior history h, the actual reduced signed contrast is

    Delta_(j,h)=sum_k B_k K_(k,j,h).                           (1)

The operators K_(k,j,h) are Hermitian, K_(k,j,h)=K_(j,k,h), commute with every B_l, and the 3-by-3 OPERATOR BLOCK matrix K_h=[K_(j,k,h)] is positive semidefinite on C³ tensor P. Impose the separate classical-sector condition: all entries K_(j,k,h), over all axes and every reached history in a bank, lie in the SAME unknown commutative *-algebra inside the logical commutant. No sector projector, weights, positive numerical margin or noise matrix is supplied.

A concrete realization is

    K_(j,k,h)=sum_a (T_(a,h))_(j,k) R_(a,h),                  (2)

where each T_(a,h) is real symmetric positive semidefinite, every R_(a,h)>=0 commutes with the own Pauli algebra, and all R_(a,h) across a and reached histories commute. Product positivity makes K_h>=0. T and R may be correlated and change with memory/history, so a common scalar-factor decomposition Delta_j=(T column dot B)R is NOT required.

Actual outputs must be positive normalized states; thus ||Delta_(j,h)||op<=1. The complete source may retain quantum memory/coherent records; the promise concerns its reduced contrasts at every reached prior state. The matrices are not arbitrary invented signed outcomes. It does not establish structural membership from finite data.

The classical-sector condition is about the ACTUAL measured physical patch. Commuting global spectator matrices can acquire noncommuting partial traces, so it must not be inferred for an arbitrary smaller envelope. This first construction uses a supplied whole patch, or disjoint supplied patches whose local condition is separately proved. Unknown minimal support discovery is not assumed solved here.

## 2. Matrix-valued normalization preserves the information scalar traces lose

Average a reached fresh bank predictably. The same fixed B factors out, Kbar remains positive and its entries still commute. Set D_j=average Delta_j and form the observable operator blocks

    G_jk=(D_j D_k+D_k D_j)/2.                                 (3)

Because Pauli generators anticommute and every Kbar entry commutes with all other entries and the B's,

    G_jk=sum_a Kbar_(a,j)Kbar_(a,k),
    G=Kbar².                                                  (4)

All off-diagonal Pauli commutator terms cancel; this is exactly where the commutative-sector hypothesis is used. If Kbar is strictly positive on the full 3d-dimensional block space, then its positive square root is Kbar, not an unknown polar rotation. Hence

    C_j=sum_k D_k (G^(-1/2))_(k,j) = B_j.                     (5)

This is an operator-valued calculation: G is a known 3d-by-3d Hermitian matrix assembled from ordinary acquired d-by-d contrasts. It does not first take a Hilbert–Schmidt trace. The normalization adapts to all hidden sectors simultaneously without being given a sector decomposition. A final sign extraction makes the perturbed learned controls exactly physical.

The distinction is substantive. For a mixture of different positive T_a correlated with different spectator sectors, the scalar Gram Tr(D_j D_k) averages T_a² with sector purities, and one shared numerical inverse generally cannot undo every T_a. Equation (5) instead preserves the sector-dependent matrices. The root counterexample in `variable_contraction_whitening_boundary_20261028.md` is a useful test instance, not a contradiction to this new hypothesis.

## 3. Finite acquired certificate

Use the actual importance-weighted signed shadow record 3*1{input axis=j}*sign*Z_P. The same three-axis matrix-martingale variance/increment bounds as the received positive-Bloch source apply: variance<=3*3^w I, centered increment<=6d. Finite fresh banks and declared union logarithms give simultaneous ||Dhat_j-D_j||op<=a. Source effects may drift; the predictable average retains the fixed logical algebra and common commutative-sector structure.

Form exactly rational Hermitian block matrix Ghat_jk={Dhat_j,Dhat_k}/2. Unlike a scalar Gram, Ghat need not be positive on every record. Bound each block error by 2a+a², so

    ||Ghat-G||op<=g=3(2a+a²).                                 (6)

Test positive definiteness of Ghat by exact rational principal-minor/LDL arithmetic; otherwise reject the bank. With q=max(1,Tr Ghat), halve h from q/2 until Ghat-h I is positive definite. Its first passing value has h>=lambda_min(Ghat)/2. Require h>g.

The rational binomial-series construction in the finite positive-Bloch source now operates on the KNOWN 3d-by-3d Ghat: with A=I-Ghat/q and r=1-h/q, approximate q^(-1/2) sum b_k A^k to certified operator error u, using bounded exact rational arithmetic. This yields exactly rational Hermitian block W0 with ||W0-Ghat^(-1/2)||op<=u. The dimension and conditioning costs are paid; no hidden inverse of an inaccessible channel is invoked.

Set Ctilde_j=sum_k Dhat_k (W0)_(k,j). Individual Ctilde_j need not be Hermitian because estimated blocks need not commute. Explicitly hermitize H_j=(Ctilde_j+Ctilde_jdagger)/2. Since the true B_j is Hermitian, hermitization cannot increase the error. The operator row-norm and inverse-root integral bounds give

    ||H_j-B_j||op<=E,
    E=sqrt(3)a/sqrt(h)
       +sqrt(3)g/[2(h-g)^(3/2)]
       +sqrt(3)(1+a)u.                                       (7)

Here the coefficient multiplication is BLOCK multiplication. Bound the row [D_X,D_Y,D_Z] by sqrt(3), the error row by sqrt(3)a, and each relevant inverse column by its whole operator norm. No commutation is assumed of estimated matrices.

Apply finite rational Jacobi to H_j with Frobenius residual v, obtaining rational-unitary Q_j and rational diagonal L_j. Let e=E+v and ell_j=min|L_j,kk|. Accept an X/Z pair only when both strict raw-sign guards hold:

    ell_j>e,  2e<=delta(2ell_j-e),
    Shat_j=Q_j sign(L_j)Q_jdagger.                             (8)

On the simultaneous event, ||Shat_j-B_j||op<=delta. Every produced Shat_j is a physical reflection on every record, whether or not the statistical event holds. The conditional source promise does not become a posterior record-by-record guarantee. Missing gaps produce finite ABSTAIN.

Under a persistent lower bound Kbar>=kappa I on reached banks (not supplied to the algorithm), G has minimum at least kappa². Since the target C_j=B_j has sign gap exactly one, sufficiently funded geometric stages with a,u,v small compared with delta and kappa certify the receiver. The explicit call count is the paid shadow bank size 16*3^w*L/a² plus preceding geometric banks; inverse-series degree, d-dimensional matrix arithmetic and finite control synthesis are separate. No favorable practical scaling or rank discovery is claimed.

## 4. Actual coherent receiver and future memory

Use the same literal three-controlled-reflection SWAP extraction with one fresh mixed receiver qubit. Replacing the true Z/X/Z reflections by the learned ones changes the unitary by norm at most 3delta. Tracing the emitted physical patch therefore changes the extracted channel from Tr_G Ad_Udagger by half-diamond at most 3delta, uniformly for arbitrary gauge/reference/source-memory correlations. This is the complete-operator-norm fallback, not the sharper Pauli CP-domination route.

An arbitrary finite common causal controller using J later services pays at most 3Jdelta plus the one bad-certificate probability, calibration-record discrepancy and whole-service implementation error. The comparison targets the PARTICULAR exact logical extraction, which need not correct the native non-Pauli noise or be an optimal decoder. No Pauli twirl or leaking frame is used. The actual initialization, local controls, routing, storage, bounded ternary random samplers, all source blocks and acceptance/abort handling remain paid.

## 5. Sharp limits

Noncommuting K entries leave extra Pauli commutator terms in (3); G is then not generally K², so equation (5) is not proved. Matrix positivity of K alone is insufficient for this argument. A finite data check that a particular empirical G is positive does not certify the missing commutativity/source promise. Unexcited hidden sectors can make K singular even when the currently occupied logical state is recoverable; full future-gauge extraction then remains unacquired.

The strongest equally informed conventional learner can use this same observable operator Gram. The proposed addition is a constructive representation that preserves correlated hidden-sector contraction information discarded by scalar traces. It remains a scoped mathematical/algorithmic candidate until its separate review and reproducible checks are complete.
