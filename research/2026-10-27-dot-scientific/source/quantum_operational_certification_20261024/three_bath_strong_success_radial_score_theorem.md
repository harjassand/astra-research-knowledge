# Arbitrary three logical baths: a strong-success radial score theorem

Status: analytic proof, awaiting independent receipt. Logical dimension is arbitrary finite. This is a source-linked radial score theorem, NOT a whole VALUE theorem.

## Source and conclusion
Let C>0 and D₁,D₂,D₃≥0 be logical matrices, with no commutation assumptions. On physical C³ and reference C³⊗Cʳ set

X=P_Ω3⊗C+I₃⊗diag(D₁,D₂,D₃),
S(C;D)= d/dt Δ(P_Ω3⊗tC+I₃⊗diag(D_i))|_(t=1).

If C≥3D_i for every i, then

S(C;D) ≥ (3log2−2) Σ_i TrD_i ≥0.                 (1)

Since log2>2/3, the bound is strictly positive whenever the reset is nonzero. More generally, with η_i=||C^-1/2 D_i C^-1/2|| (zero terms interpreted continuously),

S(C;D) ≥ Σ_i TrD_i [log(1+3η_i)/η_i−2].         (2)

A separate quadratic bound, useful for a common product bath, is

S(C;D) ≥ Σ_i TrD_i −(9/2)Σ_i Tr(D_i C^-1 D_i). (3)

For D_i=a_iB, (3) is nonnegative if C≥(9/2)(Σa_i²/Σa_i)B. Equation(1) instead requires C≥3(max a_i)B. For three nonnegative a_i, the quadratic sufficient threshold is always at least this clean threshold, so it does not improve the product-bath dominance region. Its useful role is the explicit inverse-mass error term for integration along tC.

## Actual source blocks and exact gradient
Write
M=diag(D₁,D₂,D₃)+ones₃⊗C,
R_i=C+3D_i,
L_ij=[[C+2D_i,−C],[−C,C+2D_j]],
V=[I;I;I], W=[I;−I], κ=log(4/3).

The input has M plus two copies of each D_i. The unscaled WH output has the three blocks2D_i and the three L_ij; the reference has the R_i. Thus the exact C-gradient is

G_C=V*log(M)V+Σ_i logR_i−Σ_(i<j)W*log(L_ij)W+3κI,
S=Tr(C G_C).

The derivative constants cancel:3+3−6=0. This is the original homogeneous entropy objective with its trace correction, not a normalized substitute.

## Compression payment
Initially take all D_i>0, and put H=(ΣD_i^-1)^-1. Woodbury gives V*M^-1V=(C+H)^-1. Jensen for log applied to the isometry V/√3 and to M^-1 yields

V*log(M)V ≥3log[3(C+H)].

Jensen for log applied directly to L_ij with W/√2 yields

W*log(L_ij)W ≤2log[2C+D_i+D_j].

The scalar constants cancel because3log3+3κ−6log2=0. For
h_C(E)=Tr C[log(C+E)−log C],
we obtain the exact lower comparison

S ≥3h_C(H)+Σ_i h_C(3D_i)−2Σ_(i<j)h_C((D_i+D_j)/2).  (4)

All matrices here are actual source compressions; no independently varying clocks, spectral orientation minimization, or commuting approximation is used. In particular h_C(H)≥0 can safely be dropped.

## Weighted logarithm lemma
For C>0 and E≥0,

0≤h_C(E)≤TrE,
h_C(E)≥TrE−(1/2)Tr(E C^-1 E).                    (5)

If E≤kC, k>0, then the stronger bound is

h_C(E)≥[log(1+k)/k] TrE.                         (6)

Proof: let N_t=C+tE and L_N denote the Fréchet derivative of log at N. Cyclicity in an eigenbasis gives Tr N L_N(E)=TrE, so

d/dt h_C(tE)=TrE−t Tr E L_(N_t)(E).              (7)

The quadratic form Tr E L_N(E) is nonnegative and at most Tr(E N^-1 E). In an eigenbasis of N, this follows from
(logu−logv)/(u−v)≤(1/2)(1/u+1/v),
with the usual diagonal limit; sum the squared matrix entries of E. For(5), the resolvent representation also shows Tr E L_(C+tE)(E)≤Tr E L_C(E)≤Tr(E C^-1E): the sandwiched inverses decrease in Loewner order, and their squared traces decrease. Integrating(7) proves the quadratic lower bound and the upper bound.

For(6), E≤kC implies N_t≥(t+1/k)E. Hence Tr(E N_t^-1 E)≤k TrE/(1+tk). Equation(7) is at least TrE/(1+tk), whose integral from0 to1 is(6). The inverse inequality remains valid for singular E by congruence/support restriction. Positivity h_C(E) follows directly from operator monotonicity of log.

## Finish
Apply the upper bound(5) to the three pair averages in(4). Each D_i occurs in two pairs, giving total negative payment−2ΣTrD_i. Apply(6) to E=3D_i with k=3η_i to obtain(2). If η_i≤1/3, the decreasing scalar function log(1+k)/k is at least log2, proving(1). Alternatively apply the quadratic lower bound(5) to the three3D_i terms to obtain(3).

Singular D_i follow from D_i+εI and continuity of the compressed log expressions. For example, M≥V C V* ensures the main-code logarithmic compression has no divergent component as ε→0; similarly L_ij≥W C W*. Equivalently use the standard finite-dimensional one-sided entropy derivative on the fixed main support. Since C>0 is fixed, the explicit right sides converge. For a dominance assumption with equality, use C_ε=C+3εI and D_i,ε=D_i+εI, which preserves C_ε≥3D_i,ε and tends to the original source. The source entropy and its main-support derivative converge.

## What this does not prove
A positive radial derivative in a strong-success region does not by itself establish the deficit's sign at the entrance to that region. No whole three-bath VALUE statement, universal radial monotonicity, PSD C-gradient, isotropic-success monotonicity, or endpoint reduction follows. The theorem is an explicit region where a negative radial score cannot occur; it is suitable for a future full stationary-source or compact-core argument.
