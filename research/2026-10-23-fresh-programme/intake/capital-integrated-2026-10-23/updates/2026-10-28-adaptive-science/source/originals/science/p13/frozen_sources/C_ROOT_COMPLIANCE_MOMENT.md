# General CM compliance and a negative spectral moment

24 October 2026. Root derivation extending the scalar rank-one setting away
from exact optimality. This is a mathematical candidate for independent review,
not a novelty claim or an acquired physical device.

Use any connected positive finite internal spring graph, backbone mass m,
total mass M>m, side mass ms=M-m, one intercell spring K, and S=4K. Write

    D(q)=D0+s(q) vv^T, s(q)=4K sin^2(q/2),
    z=sqrt(masses)/sqrt(M), v=Mass^(-1/2)e_b,
    u=v-z/sqrt(M), w=-(M/ms)u.

The local relative internal CM coordinate Y has force vector w. In particular,
w is perpendicular to z. None of this assumes the optimal two-pole response.

## 1. Compliance is independent of Bloch wave number for every cell

For q!=0, let D(q)x=w. Taking the inner product with z gives
s(q)(z^T v)(v^T x)=0, hence v^T x=0. Therefore D0 x=w and

    x=D0^+ w+a z,
    w^T D(q)^(-1)w=w^T D0^+ w=:C_CM.

The translation-free q=0 inverse gives the same contraction. Thus Fourier
averaging proves the same local compliance on any finite periodic ring.
The harmonic Gibbs inequality gives Var(Y)>=k_B T C_CM. This remains a Gibbs
statement, not a general nonequilibrium variance assertion.

Let the positive visible spectral residues of D0 at r_j^2 be c_j. Then

    q(t)=v^T(D0+tI)^(-1)v=1/(Mt)+sum_j c_j/(t+r_j^2),
    tau=sum_j c_j/r_j^2=u^T D0^+u,
    C_CM=(M/ms)^2 tau.

This includes repeated visible frequencies after combining residues and all
dark modes after cancellation.

## 2. Exact negative-cubic spectral moment

For active squared band endpoints 0=alpha0<beta0<alpha1<...<betaL,

    R(t)=1+S q(t)=product_j(t+beta_j)/product_j(t+alpha_j).

Expanding log R as t decreases to zero gives

    log R(t)=log[S/(Mt)]+(M/S+M tau)t+O(t^2),
    sum_j 1/beta_j-sum_(j>=1)1/alpha_j=M/S+M tau.

Let chi be the active band indicator and Omega^2=S/M. Since chi and
1_[0,Omega] both equal one near zero, their difference is integrable against
omega^-3. Endpoint integration yields

    integral_0^infty [1_[0,Omega](omega)-chi(omega)]/omega^3 d omega
      = M tau/2
      = ms^2 C_CM/(2M).

Thus compliance is a THIRD exact moment constraint supplementing the trace
and logarithmic moment constraints. It is not confined to exact optimality.
Units agree: each side has units time^2; C_CM has units time^2/mass.

For the one-pendant case C_CM=1/k and the identity reduces to
(1/p^2-1/r^2+1/s_end^2-1/Omega^2)/2=ms/(2m r^2).

## 3. Scientific consequence to investigate

A displacement/compliance cap can be imposed on the complete attainable
finite band family as an additional signed moment inequality. This can test
whether constrained optimal topology remains a single resonance or develops
additional active resonances. A bare stiffness cap and a CM-compliance cap
are different constraints; do not identify them for arbitrary graphs.

No solution of that three-moment extremal problem is claimed here. The graph
class is still scalar/rank one, so this identity alone does not remove the
programme's multiple-link, vector-elasticity, contact, or material limitations.
