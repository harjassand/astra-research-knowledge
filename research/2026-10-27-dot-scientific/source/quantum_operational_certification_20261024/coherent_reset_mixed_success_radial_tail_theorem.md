# Arbitrary coherent reset and faithful mixed isometric success: radial bound and explicit VALUE tail

Status: analytic proof, awaiting independent receipt. This strictly extends the three-bath result; no physical block diagonality or logical commutation is assumed.

## Actual source and theorem
Let C>0 on Cʳ, Y≥0 on reference C³⊗Cʳ, and

X_t=P_Ω3⊗tC+I₃⊗Y,
C̃=I₃⊗C,
d=TrY,
b=(9/2)Tr(Y C̃^-1 Y).

The input physical system is C³. The main is a maximally entangled isometry with mixed logical flag C, not an arbitrary mixed bipartite main. The reset Y may have arbitrary coherence between all reference code and logical coordinates. These are actual TP-channel Choi sources after division by tTrC+TrY; the theorem uses their original homogeneous entropy deficit.

For every t>0,

t(d/dt)Δ(X_t)≥d−b/t.                             (1)

If tC̃≥3Y, the stronger clean inequality is

t(d/dt)Δ(X_t)≥(3log2−2)d.                        (2)

Consequently, for t≥1,

Δ(X_t)≥Δ(X_1)+d logt−b(1−1/t).                  (3)

If d>0, the deficit is strictly positive for the entire tail

t≥exp{[b+3log3(TrC+d)]/d}.                       (4)

If d=0, Δ(X_t)=0. No uniform threshold through singular C is asserted. Equations(1)–(4) do not close the intermediate-success regime.

## Source-faithful compression identity
Write N=I_phys⊗Y, V=|Ω₃>⊗I_r, so V*V=3I_r and X=VCV*+N. Choose a fixed isometry U_anti:C³→C³⊗C³ onto the antisymmetric physical/code subspace and set U=U_anti⊗I_r. Thus UU*=P_anti⊗I_r and, crucially, U(I₃⊗C)U*=P_anti⊗C. The logical tensor factor is preserved; U is not an arbitrary range-equivalent isometry mixing logical eigenvectors. With C̃=I₃⊗C,

R=Tr_physX=C̃+3Y,
L=2(W₃⊗id)X=2U C̃ U*+2N.

The actual radial score S=t∂_tΔ(X_t)|_(t=1) is

S=Tr[C V*logX V]+Tr[C̃ logR]−2Tr[C̃ U*logL U]+3log(4/3)TrC. (5)

Derivative identity constants cancel because the main masses are3TrC,3TrC,6TrC. Nothing is discarded or re-normalized.

Initially suppose Y>0. Define

H=(V*N^-1V)^-1>0,
Z=U*NU≥0.

Woodbury gives V*X^-1V=(C+H)^-1. Jensen for the concave log, applied to X^-1 and the isometry V/√3, yields

V*logX V≥3log[3(C+H)].

Jensen applied directly to L and U yields

U*logL U≤log[2(C̃+Z)].

Moreover TrZ=TrY=d: the physical partial trace of P_anti is I₃. This trace identity is valid for coherent Y; it does not require a physical diagonalization of Y.

For h_A(E)=Tr A[log(A+E)−log A], the scalar constants and baseline logC terms in(5) cancel exactly. Therefore

S≥3h_C(H)+h_C̃(3Y)−2h_C̃(Z).                    (6)

This is the key generalization. All three quantities arise from the SAME original source. Z is not replaced by an independently optimized bath; only its exact trace is used below.

## Weighted logarithm payment
For A>0, E≥0,

0≤h_A(E)≤TrE,
h_A(E)≥TrE−(1/2)Tr(E A^-1 E).                  (7)

If E≤A, then

h_A(E)≥log2 TrE.                                (8)

These inequalities are proved in full in `three_bath_strong_success_radial_score_theorem.md`: with M_s=A+sE,
(d/ds)h_A(sE)=TrE−s Tr E Dlog_(M_s)(E),
and 0≤Tr E Dlog_M(E)≤Tr(E M^-1E). The latter follows entrywise from the logarithmic divided-difference bound by the mean of reciprocal endpoints. Resolvent monotonicity receives the fixed-A quadratic bound; M_s≥(1+s)E under E≤A gives(8) after integration. Thus no generic operator order for products or powers is assumed.

Drop the nonnegative3h_C(H), apply(7) to3Y and the upper bound to Z, and use TrZ=d. This gives S≥d−b. If C̃≥3Y, use(8) instead to get S≥3log2 d−2d. Applying the same statements with C replaced by tC proves(1) and(2).

## Singular reset
The proof extends to Y≥0. The radial perturbation is supported on the fixed main support; any kernel vector of X lies in kerV*, and any kernel vector of L lies in kerU*. Thus the compressed logarithmic traces in(5) have finite limits under positive regularization. For example Y_ε=Y+εI and C_ε=C+3εI preserve C̃_ε≥3Y_ε when that condition holds. C_ε remains uniformly positive; the quadratic right side converges. Finite-dimensional spectral calculus on the positive limiting supports and the vanishing main overlap with limiting nullspaces receive the limit in the score. This is not an assumption of unrestricted log continuity at zero.

## Integrate and receive VALUE tail
Integrating(1) from1 to t gives(3). For any qutrit-input source of mass m, the antisymmetric Stinespring isometry has equal output and environment marginals, so its normalized deficit is

Δ(X)/m=I(output:environment|reference)−log3.

Strong subadditivity gives Δ(X_1)≥−3log3(TrC+d). Substituting at(4) into(3) leaves at least b/t>0 when d>0. The lower bound increases thereafter. This proves an explicit entire tail without an uncharged accepted branch or an auxiliary-source comparison.

## Guards
The logical main C must be faithful, and Y lives on its full reference code C³⊗Cʳ. Additional reset-only spectator reference dimensions are not included by pretending C̃ is invertible there. No arbitrary mixed-main theorem, universal radial monotonicity, finite instrument inequality, or unrestricted WH₃ closure follows. The exact endpoint and isotropic-success monotonicity counterexamples remain valid; they concern different directions or regimes.
