# Pointwise PPT admissibility: exact dependency closure

9 October 2026. This records an established-input proof chain needed to select an admissible singular family. The general pointwise conclusion is also the stated first result of Park, arXiv:2608.13551 (2026); no priority or historical claim is made here. Only this dependency chain is checked, not that manuscript's other claims.

## Published input

Hanson, Rouze and Stilck Franca, *Eventually Entanglement Breaking Markovian Dynamics: Structure and Characteristic Times*, Annales Henri Poincare 21 (2020), 1517-1571, Theorem 3.14:

A PPT CP map Phi with strictly positive matrices X,sigma satisfying

 Phi*(X)=spr(Phi) X,
 Phi(sigma)=spr(Phi) sigma

is eventually EB. This is the arbitrary-CP formulation. Theorem 3.10 gives the TP faithful-invariant-state formulation; Theorem 3.11 is a related structural characterization, not the exact theorem used here.

Primary source: https://link.springer.com/article/10.1007/s00023-020-00906-4
Preprint identifier: arXiv:1902.08173v2.

The source's proof uses the CP similarity

 P_X(Phi)=spr(Phi)^(-1) Ad_(X^(1/2)) Phi Ad_(X^(-1/2)),

which is TP and has a faithful invariant state. Its powers telescope, and invertible CP local filters preserve both PPT and EB. There is no independent left/right Sinkhorn replacement.

## Reduction for arbitrary PPT CP maps

Proceed by induction on dimension. If spr(Phi)=0, Phi is nilpotent as a linear operator on the d^2-dimensional matrix space, so Phi^(d^2)=0 is EB.

If Phi is irreducible and has positive spectral radius, the finite-dimensional Perron theorem for irreducible positive maps gives strictly positive left and right Perron eigenmatrices. The published Theorem 3.14 applies directly.

Otherwise choose a nonzero proper invariant projection P, with Q=I-P. Kraus operators have blocks [[A_i,B_i],[0,C_i]]. The cross transfer T(X)=sum A_i X C_i* vanishes because Phi is PPT. Indeed, for p in PH and q in QH, the product vector q tensor conjugate(p) has zero expectation against the positive partially transposed Choi matrix. Positivity forces that vector into its kernel. Its matrix elements against vectors from PH tensor conjugate(QH) are exactly the coefficients of T.

As proved in EXACT_BOUNDARY_REDUCTION.md, T=0 makes the Kraus-environment coefficient spans of the A_i and C_i orthogonal. A unitary Kraus rotation therefore gives a CP split

 Phi=F+G, F output-supported on P, G input-supported on Q, GF=0.

The compressed corner maps Phi_P and Phi_Q remain PPT. By induction choose finite EB exponents N_P,N_Q for these individual maps. No uniform exponent over a family is assumed. The factor identities imply that F^(N_P+1) and G^(N_Q+1) are EB. Since

 Phi^n=sum_(j=0)^n F^(n-j)G^j,

every term is EB for n=N_P+N_Q+1. Thus Phi has a finite EB power.

## What this establishes for the current investigation

Every finite-dimensional PPT CP map, including arbitrary non-TP filtered maps, has a finite EB power by this chain. Consequently any CP mapping cone contained in the PPT cone satisfies the pointwise premise of the uniformization question. The proof supplies no common exponent near primitive degenerations: its irreducible input has map-dependent mixing and separability margins. No limit of depolarizing approximations is used.

The PPT-specific cross-support and CP corner splitting overlap Park's Section 3 and are credited there in EXACT_BOUNDARY_REDUCTION.md. The present purpose is to make the admissibility dependency explicit using the published faithful theorem, rather than importing an unexamined all-PPT statement as an assumption.
