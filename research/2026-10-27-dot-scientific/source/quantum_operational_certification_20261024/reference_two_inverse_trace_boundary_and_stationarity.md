# Reference-two inverse-trace target: exact boundary classification and received stationarity

27 October2026. A concrete reduction of the unproved pointwise inverse-trace target. It does NOT prove that target or merely reprove the integrated VALUE theorem.

Work on physical C3 and reference C2. Let

C={M:0≤M≤2I6, EM=I6}, Y=NM.

For faithful M (and hence faithful Y), define

R(M)=TrM^(-1)−2TrY^(-1)+6.

## 1. Every singular-output boundary source is a rotated2×2 symmetric projector

Suppose M∈C and Y has a unit kernel vector ψ. It cannot be product. In physical/reference bases with a product ψ=|0,0>, N*(Pψ)=(I3−|0><0|)⊗|0><0|/2. The positive source M is orthogonal to this operator. Its compression to that reference line is therefore supported on one physical line, has norm at most2, but must have trace3 because Tr_A M=3I2. This is impossible.

Thus ψ has Schmidt rank two. In Schmidt coordinates write ψ=sqrt(r)|00>+sqrt(s)|11>, r,s>0, r+s=1. The positive operator

Qψ=N*(Pψ)=[I3⊗diag(r,s)−Pψ^(T_A)]/2

has rank three. Its kernel is spanned by

|00>, |11>, sqrt(r)|01>+sqrt(s)|10>.

Since TrM Qψ=⟨ψ,Yψ⟩=0, the source M is supported on this three-dimensional kernel. TraceM=6 and M≤2I force

M=2P_kerQψ.

Its partial trace is2diag(1+s,1+r), which must equal3I2. Hence r=s=1/2. Therefore, up to local Schmidt coordinates,

M=2P_sym,2

on the physical-two/reference-two block, with zero on the remaining physical line. Its actual output has eigenvalues

0 (once), 1 (three times), 3/2 (twice).

In particular its output kernel is simple. This classifies every singular-output boundary point in C, not merely one chosen zero vector.

## 2. Uniform blow-up of the inverse-trace objective along every singular boundary approach

Let a faithful sequence M_j∈C converge to a singular M0∈C. If NM0 is faithful, TrM_j^(-1) tends to infinity while the output inverse trace remains bounded, so R(M_j) tends to infinity.

Otherwise Section1 applies to M0. Let y_j be the smallest eigenvalue of Y_j=NM_j and ψ_j its unit eigenvector. Since the limiting zero output eigenvalue is simple, its spectral projector converges to the maximally entangled rank-two kernel projector. Define Q_j=N*(Pψ_j). Cauchy–Schwarz in Hilbert–Schmidt space gives the exact estimate

(Tr sqrt(Q_j))²≤Tr(M_j Q_j) Tr(M_j^(-1))
 =y_j Tr(M_j^(-1)).

At the limiting rank-two maximally entangled vector, Q0 has positive eigenvalues1/2,1/4,1/4. Therefore

(Tr sqrt(Q_j))²→(1+1/sqrt2)²=3/2+sqrt2>2.

All other eigenvalues of Y_j stay bounded away from zero by the explicit output spectrum. Consequently

R(M_j)≥[(Tr sqrt(Q_j))²−2]/y_j−O(1)→+∞.

This proves boundary coercivity along arbitrary faithful approaches, not only scalar-white regularization. Different rates at which the input and output eigenvalues vanish are handled by the Cauchy inequality rather than an unsupported kernel-count comparison.

## 3. Minimum attainment and the actual upper-face normal

The closed set C is compact and contains the strictly feasible point I6, where R=0. The boundary blow-up above implies that a minimizing sequence cannot escape to a singular source/output head. Thus R has a finite global minimum attained at faithful M and Y. In particular, if the inverse-trace target is false in reference dimension two, an actual faithful negative minimizer exists.

At such a minimizer, the lower source boundary M≥0 is inactive. The upper constraint M≤2I MUST be retained. The derivative is

G=−M^(-2)+2N(Y^(-2)).

Finite-dimensional normal-cone/KKT receiving, with the strictly feasible marginal slice, gives a reference-only Hermitian multiplier and an upper-face normal S satisfying

G+I3⊗Λ+S=0,
S≥0, S(2I−M)=0.

Using2N(Z)=3E(Z)−Z^(T_A) and absorbing the reference-only3E(Y^(-2)) term into the free marginal multiplier, the equivalent stationary equation is

M^(-2)+(Y^(-2))^(T_A)=I3⊗Λ'+S,
S≥0, S(2I−M)=0.                                (1)

The normal is supported on the actual eigenvalue-two space. It cannot be dropped unless that face is proved inactive. Equation(1), faithfulness, EM=I and0<M≤2I form a rigorous constrained-stationary receiver for any hypothetical negative minimum in reference two. They do not yet exclude such a minimum.

## Scope

The boundary classification and coercivity proof here use the two-dimensional reference essentially. Larger references can have additional reference sectors and multiple output-kernel directions; neither minimum attainment nor an analogous boundary inequality is automatically extrapolated. The integrated reference-two VALUE theorem was already known, but it does not imply this pointwise inverse-trace target. This note isolates a new finite-dimensional mechanism without claiming its final sign.
