# Whole relative peak9/5 via the source-weighted monotone pencil

27 October 2026. A separate extension of the received peak3/2 theorem. Independent receipt requested. Individual eigenvector pencil overlaps need not be monotone; the weighted source trace is, and that distinction supplies the extra payment.

## Statement

For the physical qutrit WH channel N and any finite-dimensional reference, let X≥0, τ=EX, and assume

X≤(9/5)τ.

On the actual product support of τ let P0 be the kernel of X. Then

Δ(X)=D(X||τ)−2D(NX||τ)≥(1/2)Tr(P0τ)≥0.

Equality Δ(X)=0 holds exactly when X=τ, including the zero source. The retained marginal may be arbitrarily ill-conditioned, and singular X is allowed. This is not the unrestricted theorem.

## 1. Source-weighted pencil monotonicity

Work on the retained support, so τ>0. Put T=TrX=Trτ and, using a right-continuous representative at the finitely many crossings,

P(t)=1_(0,∞)(tτ−X), Q(t)=Tr[X P(t)].

Then Q is nondecreasing. Here is an elementary variational proof that avoids differentiability. For t2>t1>0, let P1,P2 be the corresponding positive spectral projections. Each maximizes Tr[(tτ−X)P] over effects P. Thus, with δa=TrX(P2−P1), δb=Trτ(P2−P1),

δa−t1δb≥0,   t2δb−δa≥0.

It follows that (t2−t1)δb≥0 and δa≥t1δb≥0. This proves monotonicity. Choosing either zero-eigenspace convention at an isolated crossing does not change the ordinary integrals; the right-continuous version defines the positive Stieltjes measure dQ.

The order assumption gives Q(t)=T for t>9/5. At t=0, Q(0+)=0. The positive measure dQ therefore has total mass T and support in(0,9/5].

## 2. Exact Stieltjes representation and singular moments

The same-pencil log and reciprocal-moment identities, summed over positive eigenvectors of X, give

∫Q(t)/t²dt=Tr(P_suppX τ)=T−K,  K=Tr(P0τ).

The singular limit is controlled explicitly: for any Uψ=ψ and H=tB−U,

(H+I)ψ=tBψ,
q(t)=||P_+(H)ψ||²≤t²||Bψ||².

The inequality follows by inverting H+I on its positive spectral subspace, where it is at least I. It provides a uniform near-zero dominator for q/t² under the common faithful regularization. Since B is faithful, the finite set of generalized eigenvalue crossings is harmless; the tail is bounded by1/t². Thus the singular moment identity is exact, not merely formal.

Set

L(t)=log[16t/(t+3)²],
J=TrX[logX+logτ−2log((X+3τ)/4)].

The already received summed log identity is

J=∫[(t−3)/(t(t+3))][Q(t)−T1_(t>1)]dt.

Because L'(t)=(3−t)/(t(t+3)) and L(1)=0, Stieltjes integration by parts yields

J=∫L(t)dQ(t).

The boundary term at0 vanishes by Q(t)=O(t²); above9/5 the subtracted integrand is zero. Define the positive measure dν(t)=dQ(t)/t. Integrating the reciprocal moment by parts gives

∫dν=T−K,   ∫t dν=T.

Consequently

J=∫ t log[16t/(t+3)²]dν(t).                       (1)

This uses ONE original source-weighted pencil. It does not assume individual q_i(t) are monotone and does not replace quantum entropy by a whitened entropy.

## 3. Exact scalar supporting-line certificate through9/5

Let

f(t)=t log[16t/(t+3)²]−(t−1)/2.

Then f(1)=f'(1)=0 and

f''(t)=−(t²+6t−9)/[t(t+3)²].

The second derivative is positive up to α=3sqrt2−3∈(1,9/5), then negative. Thus f>0 on(0,1), f increases from zero on(1,α], and is concave on[α,9/5]. Its right endpoint is strictly positive:

f(9/5)=(9/5)log(5/4)−2/5>2/1215>0.

The last strict rational bound follows from the first two positive terms of log(5/4)=2atanh(1/9). A concave function on[α,9/5] lies above the chord joining its positive endpoint values. Hence

f(t)≥0 for0<t≤9/5, with equality only at t=1.

Combining this with(1) gives

J≥(1/2)∫(t−1)dν=K/2.

## 4. Actual channel receiving and equality

The actual unital-channel Jensen inequality and N²X=(X+3τ)/4 give

Δ(X)≥J.

For singular NX, the weighted log limit is legitimate because NP_i≤NX/λ_i for each positive source eigendirection. This is the same original-source support receiver used in the root peak3/2 theorem.

If X is singular on the faithful actual marginal support then K>0, proving strict positivity. If X is faithful and Δ=0, both the actual Jensen defect and ∫f dν must vanish. The scalar certificate forces dν to be supported at t=1, hence Q=T1_(t>1) almost everywhere. Since Q is the positive-eigenvalue-weighted sum of individual overlaps q_i∈[0,1], this implies q_i=0 below1 and q_i=1 above1 for every source eigenvector. Limits from both sides annihilate the positive and negative parts of τ−X on every eigenvector, yielding X=τ. Conversely X=τ gives Δ=0.

The earlier peak3/2 top theorem, whole-source theorem, singular-output boundary geometry, local-cap counterexamples, and clipping failure remain valid. This extension does not claim monotonicity of arbitrary vector overlap or a preserving clipping flow.
