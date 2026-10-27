# Whole VALUE for flat mixed success and an arbitrary coherent rank-one reset hole

Status: analytic proof plus exact finite polynomial certificate, awaiting independent receipt.

## The whole family
Let r≥2 be arbitrary finite, ψ any unit vector in reference C³⊗Cʳ, and

Y=a(I_(3r)−p|ψ><ψ|),   a>0, 0≤p≤1,
X=P_Ω3⊗I_r+I₃⊗Y,

where Ω₃ is unnormalized. Then

Δ(X)>0.                                         (1)

At a=0 the pure flat mixed-isometric main has Δ=0. The reset may be fully coherent between reference code and logical coordinates; p=1 gives rank3r−1 and is included. The main has rank r and its physical marginal is [r+a(3r−p)]I₃, so these are actual TP-channel Choi sources after homogeneous normalization. Arbitrary main mass d>0 follows by scaling a/d. The r=1 case is already paid by the received pure-main/qutrit-reset theorem.

This is an arbitrary ONE-DIMENSIONAL HOLE in white reset, not an arbitrary reset matrix, arbitrary two-level projector, or nonflat logical main.

## 1. Exact clock and scalar allocation function
For s>0 put x=1/(s+a), y=1/[s+a(1−p)], β=y−x≥0. Then the actual Gram clock is

K=xI_(3r)+β|ψ><ψ|.

Let λ₁,λ₂,λ₃≥0 sum to1 be ψ's Schmidt probabilities, padding with zero when its Schmidt rank is below3. For r=2 the physical domain has one zero entry. The nonzero eigenvalues of (W₃⊗id)|ψ><ψ| are(1−λ_i)/2, allowing zero entries in this list; the remaining3r−3 eigenvalues vanish. The actual reference marginal has eigenvalues λ_i on the active logical span.

Define the following analytic extension to the full three-simplex:

F₂^ext(x,β;λ)=2Σ_i log[1+x+β(1−λ_i)/2]+6log(1+x)
 −3log[1+(x+β)/3]−15log(1+x/3)
 −Σ_i log[1+3x+βλ_i]+log(1+3x).                  (2)

On the actual r=2 domain this equals the true determinant kernel. For r≥3, the actual kernel is exactly

F_r(K)=F₂^ext(x,β;λ)+(r−2)f₀(x),                 (3)
f₀(x)=6log(1+x)−9log(1+x/3)−log(1+3x).

The extension(2) is only an analytic LOWER-OPTIMIZATION device for r=2. The point λ=(1/3,1/3,1/3) is not claimed to be a realizable Schmidt allocation at r=2. No negative spectral multiplicity is interpreted as a physical operator.

## 2. Proved allocation minimum (special coupled heads only)
The λ-dependent part of(2) is Σg(λ_i), where, for β>0,
z=β/2, A=1+x+z, B=1+3x,
g(t)=2log(A−zt)−log(B+2zt).

We prove its minimum on the three-simplex occurs at one of
(1,0,0), (1/2,1/2,0), (1/3,1/3,1/3), up to permutation.

First,
g'''(t)=−4z³/(A−zt)³−16z³/(B+2zt)³<0.
Thus g' is strictly concave and a stationary allocation has at most two distinct positive values. If g'(u)=g'(v), u<v, then g''(u)>0 and g''(v)<0. Repeating v twice gives a negative Hessian direction between those entries, so an interior nonuniform minimum could only have the form(u,u,v), v=1−2u,0<u<1/3.

For this remaining case, exact subtraction gives

g'(u)−g'(v)=−2z²(u−v)N(u,v)/D(u,v),
N=−2A²+B²+2z(A+B)(u+v)+2z²uv,
D=(A−zu)(A−zv)(B+2zu)(B+2zv)>0.

Along v=1−2u,
(d/du)N(u,1−2u)=−2z[A+B−z+4zu]<0,
because A+B−z=2+4x>0. The positive prefactor in the derivative of2g(u)+g(1−2u) therefore makes its second derivative STRICTLY NEGATIVE at any nonuniform stationary point. Such a point is not a minimum.

On an edge, an unequal stationary pair u<v similarly has g''(u)>0. Since g'' is decreasing, g'(0)<g'(u). Moving mass from u into the zero coordinate is a feasible strictly decreasing direction. Thus unequal edge points are not full-simplex minima. Only the three displayed flat-rank allocations remain. When β=0 the allocation dependence vanishes and the claim is immediate.

This is a proof for the displayed coupled logarithms. It is NOT the generic coherence or orientation endpoint principle, which has been decisively disproved elsewhere.

## 3. Exact pointwise positive region
For each of the three allocations, form exp(F₂^ext)=N_j(x,β)/D_j(x,β) from the positive linear heads in(2), with positive denominator. The exact certificate
`flat_mixed_success_arbitrary_reset_hole_clock_certificate.py`
expands N_j−D_j as a polynomial in β and receives every coefficient polynomial in x on0≤x≤3/2.

For a coefficient P(x)=Σ_(i=0)^n p_i x^i, the substitution x=(3/2)u/(1+u) gives

(1+u)^n P((3/2)u/(1+u))
 =Σ_(k=0)^n [Σ_(i=0)^k p_i(3/2)^i binom(n−i,k−i)]u^k.

ALL346 resulting rational coefficients are nonnegative. The β⁰ row is nonzero and strictly positive for u>0, and its endpoint P(3/2)>0 is checked separately. Hence all three log kernels are strictly positive for0<x≤3/2, β≥0. The full coefficient lists are saved in the adjacent JSON proof object; the text replay reports the exact count and endpoint checks. No floating-point tolerances or sampled roots are used.

By Section2 this pays F₂^ext for every allocation. Also f₀(x)>0 for0<x≤3/2: its derivative is12x(1−x)/[(1+x)(3+x)(1+3x)], and f₀(3/2)=log(250000/216513)>0. Equation(3) therefore pays the actual kernel for EVERY r≥2 in this region.

If a≥2/3, the actual x(s)≤3/2 for all s>0. Integrating the exact source kernel proves Δ(X)>0, including the singular p=1 case by its integrable clock.

## 4. Original radial score in the complementary regime
Use the received coherent-reset compression theorem with C=I_r. Dropping its nonnegative harmonic term yields

S≥Tr log(I+3Y)−2Tr log[I+(W₃⊗id)Y].             (4)

The reset has a with multiplicity3r−1 and a(1−p) once. The output compressed bath has a with multiplicity3r−3 and a[1−p(1−λ_i)/2] for the three listed eigenvalues. Concavity of the ordinary scalar log gives

Σ_i log{1+a[1−p(1−λ_i)/2]}
 ≤3log[1+a(1−p/3)],

because Σ_i(1−λ_i)=2. Thus(4) implies

S≥L_r(a,p),
L_r=(3r−1)log(1+3a)+log[1+3a(1−p)]
    −(6r−6)log(1+a)−6log[1+a(1−p/3)].           (5)

For0<a≤2/3, L_r≥L₂: their difference is
3(r−2)log[(1+3a)/(1+a)²]≥0.

L₂ is strictly concave in p, since its second derivative is
−9a²/[1+3a(1−p)]²+(2/3)a²/[1+a(1−p/3)]²<0.
Its endpoints are both positive on0<a≤2/3:

L₂(a,0)=6log[(1+3a)/(1+a)²]>0,
L₂(a,1)=5log(1+3a)−6log(1+a)−6log(1+2a/3).

The derivative of the latter is
−3(14a²+13a−5)/[(1+a)(3+2a)(1+3a)],
so it has only one interior maximum. It starts at0 and at a=2/3 equals
log[3^23/(5^6·13^6)]>0,
since94143178827>75418890625. Consequently S>0 throughout0<a≤2/3, uniformly over ψ and r≥2. The concavity endpoint payment is for an explicitly valid LOWER bound, not for the entropy itself.

## 5. Anchor the mass flow; do not leave an unpaid sign
Fix ψ,p and the already-paid reset at a₀=2/3. Increase its original flat main mass t≥1. Its effective ratio a=a₀/t lies in Section4, so its radial derivative is strictly positive. Homogeneity gives

Δ(X_(a,p,ψ))≥(a/a₀)Δ(X_(a₀,p,ψ))>0
for0<a≤a₀.

Together with Section3 this proves the entire a>0 domain. Singular p=1 is included by the received main-support score limit (C=I_r remains faithful), or by continuity from p<1 followed by the strict positive anchor/radial bound.

## Exact scope and dependencies
The main is flat logical isometric success, not an arbitrary mixed input. The reset is white minus ONE arbitrary rank-one projector, not an arbitrary spectral hole or arbitrary PSD matrix. It lives on the full covered C³⊗Cʳ reference. The proof uses actual source-linked clocks and the received coherent-reset radial compression bound. It does not infer a filtered-source anchor, complete-instrument order, GLS failure/success, or unrestricted WH₃ closure. The positive-bump/white family for arbitrary Schmidt allocation is a separate problem; only the maximally entangled bump family has been paid by the separate one-crossing theorem.
