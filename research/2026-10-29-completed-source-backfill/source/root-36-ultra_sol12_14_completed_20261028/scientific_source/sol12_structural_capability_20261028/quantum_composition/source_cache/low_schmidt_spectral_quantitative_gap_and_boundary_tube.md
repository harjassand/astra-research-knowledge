# Quantitative low-Schmidt spectral gap and a uniform rigid-boundary tube

27 October 2026. Derived from the received arbitrary-source low-Schmidt top anchor, not from the high-white condition-number gate.

## 1. All fixed low-Schmidt spectral sources

Let X≥0 on C3⊗C^d, finite d, have an orthonormal eigenbasis consisting of vectors of Schmidt rank at most two. For X≠0,

Δ(X)≥||X−EX||_HS²/(24||X||).                       (1)

There is no condition-number restriction. Section 4 of index_six_maximum_principle_and_rank_two_anchor_theorem.md gives, for an effect U and a low-Schmidt top vector ψ,

g_N(U;Pψ)≥(1/12)(1−⟨ψ,EUψ⟩).

To verify quantitative integration, first replace X by X+εI. Along its spectral clipping path

X_t=εI+min(X,tI), 0≤t≤||X||,

the derivative is the cumulative top projection P_t, except at finitely many breakpoints. Its chosen eigenbasis remains fixed and low-Schmidt. Write z=ε+t and Q(t)=||X_t−EX_t||_HS². Scaling the actual top gradient by z cancels all scalar logarithm terms, so

dΔ(X_t)/dt≥(1/12)[TrP_t−Tr(P_t EX_t)/z],
Q'(t)=2z[TrP_t−Tr(P_t EX_t)/z]≥0.

The nonnegativity follows from EX_t≤zI. Therefore

dΔ(X_t)/dt≥Q'(t)/(24z)≥Q'(t)/(24(||X||+ε)).

The initial scalar source has Δ=Q=0. Integrating over every spectral segment gives (1) for X+εI, with denominator ||X||+ε; the squared deviation is exactly unchanged. Entropy continuity sends ε to zero and proves (1). Degenerate levels, a zero eigenvalue, and non-low-Schmidt linear combinations within a degenerate eigenspace cause no issue: only the fixed low-Schmidt basis projectors are used in the positive decomposition of P_t.

## 2. Uniform positive margin for the rigid family

On C3⊗C3 let

X=c(I⊗sqrt T)P_sym(I⊗sqrt T), T≥0, c>0, TrT=S>0.

A reference eigenbasis diagonalizes T without changing Schmidt ranks, and the explicit pair eigenvectors all have Schmidt rank at most two. This includes singular T by either direct choice of the pair basis or continuity. Its norm and traces satisfy

||X||=c t_max,
TrX=2cS,
TrX²=c²(5TrT²+S²)/4,
Tr(EX)²=(4c²/3)TrT².

Hence

||X−EX||²=c²(3S²−TrT²)/12≥c²S²/6,
Δ(X)≥cS/144=TrX/288.                              (2)

This is uniform over arbitrary reference conditioning, including singular limits. It is a strict entropy margin on this particular family, not an equality characterization for all low-Schmidt spectral sources.

## 3. Explicit trace-distance stability tube

Normalize X and Y to trace one, and let Y be any member of the rigid family in Section 2. If

ε=(1/2)||X−Y||_1≤1/20000,

then X obeys

Δ(X)≥1/288−13/5000=157/180000>0.                  (3)

No relative-peak condition, spectral eigenbasis condition, or positive minimum eigenvalue is imposed on X in this tube. The argument uses ordinary finite-dimensional entropy continuity, not reference whitening: E and N are trace-preserving CP contractions of trace distance, and all three states live in dimension nine. The entropy bound |S(A)−S(B)|≤h2(ε)+εlog8 yields

|Δ(X)−Δ(Y)|≤4[h2(ε)+εlog8]
≤4ε[log(8/ε)+1].

The last expression increases on the relevant interval. At ε=1/20000 it is (log160000+1)/5000<13/5000, since e^12>160000. The latter comparison has an exact positive Taylor-polynomial certificate. The same entropy-continuity receiver is used in wh3_small_tail_whole_face_entropy.md; here it is applied to the new explicit boundary margin.

The tube is a sufficient neighborhood, not a characterization of all sources at relative peak3/2. Turning approximate output-kernel information into distance to this family would require an additional quantitative rigidity theorem; no such inference is silently made.
