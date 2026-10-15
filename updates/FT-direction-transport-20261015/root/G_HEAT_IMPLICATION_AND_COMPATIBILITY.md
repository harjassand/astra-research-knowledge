# Independent heat implication and a quantitative incompatible-law neighborhood

15 October 2026. Root reconstruction. Exact source: nonlinear_qc/G_EXACT_HEAT_CERTIFICATE.json SHA2564004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000. This is internal analytic/algebraic review, not external certification or historical priority clearance.

## 1. Universal implication reconstructed without the discovery search

Write A=[[a,b],[c,d]], u=a²+c², v=b²+d², j=ad−bc and G=3(u+v−2j)²+(35/24)u²+j²−(5/2)ju. Root's separate Fraction-based verifier reconstructed from the portable JSON alone: the18 positive exact LDL pivots, all576 entries of Q=C S Cᵀ, the full quartic coefficient identity, and all four closedness equations. The verifier imports no worker acquisition or search code. These are exact universal polynomial/PSD checks, distinct from finite matrix samples.

For a smooth periodic map φ and arbitrary constant B, put A=B+Dφ. Its x and y derivatives are exactly the compatible six-jet pattern in the certificate. The corrected density is

    d1 D²G(A)[A_x,A_x]+d2 D²G(A)[A_y,A_y]+Ω_A(A_x,A_y)=ZᵀQZ≥0,
    d1=4897/5000, d2=5103/5000.

Closed quadratic Ω on R4 has polynomial primitive α=(1/4)i_EΩ: Cartan's identity gives d(i_EΩ)=4Ω, since coefficient degree2 plus form degree2 equals4. Thus ∫T²Ω_A(A_x,A_y)=∫T²d(A*α)=0. This holds for every B; the map Bx+φ need not itself be periodic.

Evolve φ by the constant elliptic heat operator d1∂xx+d2∂yy. Compatibility is preserved. Differentiation and periodic integration by parts give

    d/dt ∫G(B+Dφ_t)=−∫Z_tᵀQZ_t≤0.

All nonzero gradient Fourier modes tend to zero, so the limiting energy is |T²|G(B). Hence the full all-background Jensen inequality holds, not merely a selected phase/profile condition. Strong W1,4 approximation passes it to periodic Sobolev maps. A compactly supported perturbation can be embedded in a sufficiently large torus; outside its support the gap is zero. W0¹,⁴ density then gives the inequality on every bounded Lipschitz domain. No numerical trajectory, finite frequency test, scalar minimized branch or prior QC premise is used.

The source also gives a direct whole-plane heat proof. The periodic proof above independently resolves its boundary and long-time obligations. It proves this G, not every member of the full left-invariant cone. Zero acoustic curvature at I along e12 forbids subtracting any positive multiple of |A|⁴; no strict Fstar margin is obtained.

## 2. Exact lifted law and non-polyconvexity

Let ν put total weight1/1297 on ±36I, equally split, and1296/1297 on ±diag(1,−1), equally split. Direct arithmetic gives

    Eν A=0, Eν detA=0, Eν G(A)=−1350/1297,
    Eν |A|⁴=5184, ||A||L4(ν)=6sqrt(2)<9.

All lifted first moments of(A,detA) agree with the zero matrix, yet the G moment is negative. Convex Jensen in the lifted variables therefore rules out polyconvexity. This four-point law is not a compatible gradient law. The all-background heat theorem is consistent with that obstruction.

## 3. New quantitative consequence: an excluded W4 ball

For every matrix A, the elementary invariant estimates imply

    |DG(A)|≤60|A|³.

Indeed |u+v−2j|≤2|A|² and |D(u+v−2j)|≤4|A|; the four terms in G contribute at most48,35/6,1,5 times|A|³. Their sum359/6 is below60. Consequently

    |G(A)−G(C)|≤60(|A|+|C|)³|A−C|.

For any coupling of matrix laws μ,ν with finite fourth moments, Holder gives

    |EμG−EνG|≤60(||A||L4(μ)+||C||L4(ν))³ ||A−C||L4.

If μ is a law of a zero-mean periodic gradient (or a fourth-moment-integrable limit of such laws), the heat theorem gives EμG≥0. Let d=W4(μ,ν). Minkowski gives ||A||L4(μ)≤6sqrt(2)+d. Therefore

    1350/1297 ≤60(12sqrt(2)+d)³ d.                       (3.1)

In particular every such compatible law obeys the explicit rational separation

    W4(μ,ν)≥ [1350/1297]/[60·19³] >0.                   (3.2)

For d≤1 use6sqrt(2)<9 and2·9+1=19; for d>1 the displayed small bound is automatic. Infima over couplings preserve the inequality; no optimal-map oracle is needed. The bound is conservative, not asserted sharp.

This is a quantitative compatibility obstruction beyond the affine/minor first moments. It is not a measurable new physical observable or a practical W4 estimator. Fourth-moment/tail control and a legal gradient representation are essential supplied/acquired information. Weak convergence or finitely many low moments cannot be substituted for W4. The rare large atoms make that cost visible rather than negligible. Historical novelty of this particular bound is UNKNOWN; polynomial moment separation is standard machinery applied to the new exact G certificate.

## 4. What is now closed and what remains

The specific full compatible cubic-plus-quartic G inequality retained in FS is now a corollary. The arbitrary-cone phase problem remains open. The exact negative reduced Schur example remains valid because reduced convexity is stronger than the global all-background Jensen comparison. The conditional physical adjoint and clamp programmes receive no automatic physical validation from this mathematical theorem.
