# Uniform quantitative contraction throughout the clean peak9/5 region

27 October 2026. Separate refinement of relative_peak_nine_fifths_monotone_pencil_theorem.md; no optimization of the peak endpoint is attempted.

Under the same source assumptions X≤(9/5)τ, τ=EX faithful on the retained support, define K=Tr(P_kerX τ). Then

Δ(X)≥D(X||τ)/200+(99/200)K,
D(NX||τ)≤(199/400)D(X||τ)−(99/400)K.

In particular the whole peak9/5 class has a source-specific contraction coefficient at most199/400<1/2, uniformly over arbitrary finite reference dimensions and arbitrary marginal conditioning. Equality Δ=0 holds only for X=τ. These are actual source-relative statements, not arbitrary two-source channel contraction claims.

Use the positive measure ν received in the monotone-pencil theorem. It has massT−K and first momentT, with

D_in=∫tlogt dν,
J=K/2+∫f(t)dν,
f(t)=tlog[16t/(t+3)²]−(t−1)/2.

Let g(t)=tlogt−t+1. The exact scalar strengthening is

f(t)≥g(t)/200, 0<t≤9/5.

To prove it, set h=f−g/200. Then h(1)=h'(1)=0 and

h''(t)=[1791−1206t−201t²]/[200t(t+3)²].

The numerator is strictly decreasing for t>0 and changes sign once, at a point β strictly between1 and9/5. Consequently h is positive below1, increases from zero on(1,β], and is concave on[β,9/5]. The right endpoint is positive by simple exact estimates:

f(9/5)>2/1215,
log(9/5)<3/5,
g(9/5)<7/25,
h(9/5)>2/1215−7/5000>0.

The logarithm upper bound follows from e^(3/5)>1+3/5+(3/5)²/2+(3/5)³/6=227/125>9/5. The lower bound on f is the existing two-term atanh certificate. The same convex/concave shape argument as the whole-source theorem establishes h≥0 throughout the interval, with equality only at1.

Finally ∫g dν=D_in−K. Therefore

Δ≥J≥K/2+(D_in−K)/200,

which is the claimed combined margin. In particular the earlier K/2 lower bound is not lost: the exact measure identity itself shows D_in≥K, so the refinement is at least K/2. For faithful X the coefficient1/200 is a conservative certified positive margin, not an optimized value.
