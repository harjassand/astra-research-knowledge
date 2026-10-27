# Parametric source-relative contraction from the compact two-face determinant proof

27 October2026. Direct quantitative extension of the independently received all-reference relative-peak-three mechanism. Independent receiving requested; this is not an arbitrary two-source contraction claim.

Let N=W3⊗id and τ=EX for any positive source X on a finite reference. If X≤kτ for some k>1, then

D(NX||τ)≤[k/(k+3)]D(X||τ).                       (1)

The inequality is strict for X≠τ. No lower source bound or marginal condition-number bound is required. For1<k<3 this yields

Δ(X)≥[(3−k)/(k+3)]D(X||τ),                       (2)

while at k=3 it gives the whole reduction-positive VALUE theorem. At k=9/5 the coefficient in(2) is1/4, stronger than the earlier conservative monotone-pencil margin. As k decreases to1, the contraction coefficient tends the exact local value1/4. The case k=1 forces X=τ by trace and is trivial.

## 1. Weighted determinant functional

For β>1 define

F_β(X)=βlogdet(NX)−logdetX−(β−1)logdet(EX).

The coefficients sum to zero, so exact reference-congruence invariance is unchanged. On the compact slice εI≤M≤cI, EM=I, with0<ε<1<c<3/(β−1), the gradient is

G_β=βN((NM)^(-1))−M^(-1)−(β−1)I.

The two-face normal decomposition and congruence identity give exactly

G_β=cE(S_+)−S_+−εE(S_−)+S_−,

with S_± positive and supported on the c and ε eigenspaces. In particular the formula does not depend on β after the multiplier is eliminated.

Subunital Schwarz for cE on the upper corner gives Tr(S_+G_β)≤0. Actual inverse Jensen gives

G_β≥4β(M+3I)^(-1)−M^(-1)−(β−1)I=f_β(M),
f_β(m)=(m−1)[3−(β−1)m]/[m(m+3)].

Since f_β(c)>0, S_+=0. Every eigenvector with m>1 then has G_β expectation−ε⟨E(S_−)⟩≤0, contradicting f_β(m)>0. Therefore M≤I; trace forces M=I. This proves F_β≥0 with unique faithful equality I for every strict cap below3/(β−1), in every finite reference dimension. Neither boundary coercivity nor the inverse-trace conjecture is used.

## 2. Original-source integral and endpoint

Choose β=1+3/k. For s>0, the actual resolvent-normalized source

M_s=(τ+sI)^(-1/2)(X+sI)(τ+sI)^(-1/2)

is faithful, satisfies EM_s=I, and has strict cap M_s<kI, because

k(τ+sI)−(X+sI)=(kτ−X)+(k−1)sI>0.

The exact trace-entropy Bregman identity gives

D(X||τ)−βD(NX||τ)=∫_0^∞ F_β(M_s)ds.

All linear terms vanish because E(X−τ)=0. The source may be singular; each s>0 head is faithful, the zero endpoint has only integrable logarithmic singularities, and the tail is O(s^(-2)). Reference congruence is used inside an exact determinant integrand, never to replace entropy by whitened entropy.

Each integrand is nonnegative and is strictly positive whenever X≠τ, since M_s≠I. This proves(1), its strictness, and(2).

## Scope

This is a source-specific comparison against the ACTUAL τ=EX. It does not compare arbitrary pairs of input states, nor assert an unrestricted half-contraction beyond the reduction-positive region. Bounds at k>3 remain valid but have coefficient greater than1/2 and therefore do not prove the original VALUE target there. Existing more specialized paid families remain independent.
