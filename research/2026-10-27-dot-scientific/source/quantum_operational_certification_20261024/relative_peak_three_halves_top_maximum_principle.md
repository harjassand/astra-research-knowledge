# Finite-support pencil maximum principle at relative peak 3/2

27 October 2026. A route that does not use the false relative-peak-to-local-variance transfer.

## Abstract theorem

Let U,B be effects on a finite-dimensional Hilbert space, let Uψ=ψ for a unit ψ, and suppose U≤(3/2)B. Then, with supported logarithms,

⟨ψ,[logB−2log((U+3B)/4)]ψ⟩≥(1/2)(1−⟨ψ,Bψ⟩)≥0.    (1)

This uses no tensor product, variance cap, or global upper bound on an auxiliary V.

First take U,B faithful. Put

q(t)=⟨ψ,1_(0,∞)(tB−U)ψ⟩, q0(t)=1_(t>1), μ=⟨ψ,Bψ⟩.

The already received same-pencil identities are

h(s)=⟨ψ,log(U+sB)ψ⟩=∫_0^∞ s q(t)/[t(t+s)]dt,
∫_0^∞ q(t)/t² dt=μ.

These are the renormalized positive-part identities in index_six_maximum_principle_and_rank_two_anchor_theorem.md; the second follows by differentiating D(B||U) along Pψ. In particular h(s)−log(1+s) is the integral with q−q0.

The relative order implies q(t)=1 for t>3/2, since tB−U≥(t−3/2)B>0. Faithfulness of U also makes q=0 for sufficiently small t. Thus q−q0 has compact support bounded away from zero. Taking s to infinity in the subtracted identity is ordinary dominated convergence and gives

⟨logB⟩=∫(q−q0)/t dt.

Subtracting twice the s=3 identity yields exactly

j=⟨logB−2log((U+3B)/4)⟩
 =∫_0^∞ [(t−3)/(t(t+3))](q−q0)dt.               (2)

Let r(t)=t(3−t)/(t+3). Direct factorization gives

r(t)−1/2=−(t−1)(2t−3)/[2(t+3)].

Therefore r≤1/2 on (0,1), and r≥1/2 on (1,3/2). The integral after3/2 vanishes. Since q≥0 and1−q≥0, (2) implies

j≥(1/2)[∫_1^(3/2)(1−q)/t²dt−∫_0^1 q/t²dt]
 =(1/2)(1−μ).

No monotonicity of q is used. The sign-changing kernel and the finite support cutoff are both essential.

For singular U,B regularize both as (1−ε)U+εI and (1−ε)B+εI. The top condition, effect constraints, and U≤1.5B all survive. Both logarithm heads dominate a fixed positive multiple of Pψ, so the same supported-log limit as in the received maximum principle applies. Equivalently their inverse expectations along ψ are uniformly bounded, controlling the log tail. Passing to the limit proves (1).

## Original physical top-score consequence

For N=W3⊗id and E as usual, let X>0 satisfy X≤1.5EX and choose any unit top vector ψ. Normalize U=X/||X|| and B=EU. Actual unital-channel operator Jensen gives

g_actual(X;Pψ)≥⟨logB−2log N²U⟩,
N²U=(U+3B)/4.

Thus the actual top score is at least (1/2)(1−⟨B⟩), independently of Schmidt rank and reference dimension. Singular limits follow using X+εI. This is a genuine top-score theorem, not yet a whole VALUE theorem for the peak region.

## Receiver boundary

Ordinary spectral clipping need not preserve X≤1.5EX; an exact physical3/reference2 witness is saved in relative_peak_spectral_clipping_failure.md. Therefore the top-score theorem cannot be promoted to whole VALUE by an unverified peak-preserving clipping argument. The original source/marginal is unchanged in the top-score proof, and no entropy whitening is involved.

## Stationary exclusion (not a whole-region VALUE claim)

The existing fixed-reference minimizer stationarity receiver says that at a negative normalized global minimizer of Δ, every actual top anchor equals Δ(X)/TrX<0 (using the support-preserving two-sided top-eigenprojector variation). Consequently no such negative global minimizer can satisfy X≤(3/2)EX. Its relative maximum eigenvalue must exceed3/2 on the retained support. This is a valid necessary condition on a negative stationary minimizer, even though the theorem does not imply every nonstationary source in the peak region has nonnegative VALUE.
