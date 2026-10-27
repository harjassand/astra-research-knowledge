# Determinant-one covariance correction

Let h0,hc be symmetric tangent half-Hessian forms. Suppose d is the root-branch revelation direction, hc d=0, d^T h0 d=0, and u=h0d is nonzero. For this tree-completable family these identities follow exactly: revealing only the root branch scales both child conditional laws without changing them; proper-child quadratic gradients annihilate the full tangent, while the root conditional means have a null difference.

Take any SPD Kb with Tr(hc Kb)=0. One explicit choice is

    Kb=I-[Tr(hc)/Tr(hc^2)] hc.

For rank-two indefinite hc with nonzero eigenvalues a>0>b, its two nontrivial eigenvalues are b(b-a)/(a^2+b^2) and a(a-b)/(a^2+b^2), both positive; kernel eigenvalues are1. The source point is independently checked by exact principal minors. For a more general feedback domain, Kb positivity must remain guarded rather than assumed from an unreceived rank assertion.

Set L=Tr(h0 Kb), w=-L u/(2u^T Kb u), and B=I+d w^T. Then w^Td=0, so det B=1 and B^-1=I-dw^T. The congruence Kraw=B Kb B^T is SPD. Because hc d=0, its conditional trace is unchanged and zero. Its global trace is L+2w^T Kb h0d+(w^TKbw)d^Th0d=0. Dividing by Tr Kraw preserves positivity and both trace constraints.

This is a closed rational covariance repair, not a numerical optimizer or parameter sweep. The negative-helper source receipt gives exact d,Kb,w,K and verifies all identities. A stopped feedback needs explicit guards keeping posterior probabilities, the fixed chart pivot, Tr(hc^2), u^T Kb u, the normalized covariance and mean rank away from degeneracy. The diagnostic used one such corrective choice, but no occupation estimate from it is certified.

The time-capped shear diagnostic accumulated roughly1.14e-4 root-weighted negative-region occupation, with445/1024 paths still active at the cap; it is censored and has unreceived sampling/exit error. More importantly, the exact helper-hull bound limits ALL possible finite-bulk credit in this particular frontier to3.366e-5. Therefore this test is closed as nonmaterial despite the larger occupation trace. The algebraic covariance identity remains available for a broader frontier.
