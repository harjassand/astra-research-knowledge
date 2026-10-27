# Global compact tensor potentials are complete for negative-mass exhaustion

Status: new analytic proof, pending independent audit. This is a representation/receiving theorem, not an obtained exhaustion sequence or a resolution of source membership.

Fix the received finite L1 symmetric signed stress S0 supported in E with J:S0=0 and DivDiv S0=μ-δ0. It can be the canonical Green stress or the two-jet version. Write K(H)=ΔH-I DivDiv H for trace-free, J-null symmetric matrix potentials H.

## Theorem

The following are equivalent:

1. There is a finite PSD J-null full-endpoint stress for μ, supported in E.
2. There is a sequence of smooth compactly supported trace-free J-null potentials H_n on R³ such that the total negative spectral trace mass of S0+K(H_n) tends to zero.

The finite-stage potentials and stresses in (2) may extend outside E. Their exact endpoint and null identities remain unchanged. The positive limiting stress is forced back into E. This allowance is essential: local symbol completeness alone did not prove compact-support surjectivity inside E.

## 1 implies 2: mollify, then cut off the Newton potential

Let S* be a feasible PSD stress and T=S*-S0. Then T is a finite compactly supported matrix measure, J:T=0 and DivDiv T=0. Testing with quadratic polynomials, using a compact cutoff equal to one near E, gives ∫T=0 as a matrix.

Set B=T-(tr T)I/3 and H=Δ^-1 B, using the scalar Newton kernel -1/(4π|x|) componentwise. Then tr H=J:H=0 and

DivDiv H=Δ^-1[-Δ(tr T)/3]=-(tr T)/3,

so K(H)=T. These equalities are distributional; the convolution identity follows directly from the fundamental solution and compact support, with no unproved stochastic or support theorem.

First mollify: H_ε=H*ρ_ε and T_ε=T*ρ_ε. Then K(H_ε)=T_ε, while

S0+T_ε=S**ρ_ε+(S0-S0*ρ_ε).

The first term is PSD. Hence its negative spectral trace mass is at most ||S0-S0*ρ_ε||L1,nuclear, which tends to zero because S0 is L1. No regularity of S* beyond finite positivity is needed.

Since ∫B=0, the Newton monopole cancels. Outside twice the fixed support radius, direct subtraction of the kernel at x gives uniform tail bounds

|H_ε(x)|≤C|x|^-2, |DH_ε(x)|≤C|x|^-3, |D²H_ε(x)|≤C|x|^-4,

uniformly for small ε. The constants depend on the support radius and total variation of T, not on smoothness of T.

Let η_R be a smooth cutoff equal to one on the radius-R ball and zero outside radius-2R, with derivatives O(R^-1),O(R^-2). If R contains the support of T_ε, then

||K(η_RH_ε)-T_ε||L1≤C/R.

Indeed the discrepancy is confined to the cutoff annulus and consists of DH_ε Dη_R and H_ε D²η_R terms, each O(R^-4), over volume O(R³). Thus choose ε→0 and R→∞ to obtain (2), while preserving trace-free/J-null potential constraints exactly.

## 2 implies 1: compactness and an actual support receiver

Put S_n=S0+K(H_n). Exact compact-potential integration gives ∫tr S_n=3/4. If N_n is its negative spectral mass, then ||S_n||nuclear-TV=3/4+2N_n. The uniformly bounded finite measures have a vaguely convergent subsequence on R³. The limit S is a finite PSD matrix measure because N_n→0. The exact J-null and distributional endpoint identities pass to the limit against compactly supported smooth tests. No tightness assumption has been silently inserted.

To receive support, construct a C² convex function f that vanishes on E, has bounded Hessian, and has positive definite Hessian at every point outside E. One explicit construction is

f(x)=∫_{S²} φ(n·x-h_E(n)) dω(n),

where h_E is the support function and φ=0 on (-∞,0], with φ''(s)=s²/(1+s²) for s>0 and φ(0)=φ'(0)=0. Convexity and bounded Hessian are immediate. Outside E, the violating normals form a nonempty open subset of the sphere, so the integral of φ'' nn^T is positive definite.

Although f is not compactly supported, it has quadratic growth and linear gradient growth. Apply the endpoint identity to f times large compact cutoffs. The Hessian errors on the distant annuli are uniformly bounded and their pairing tends to zero because S is finite. Thus ∫D²f:S=Eμ f-f(0)=0. Positivity implies S gives no mass outside E. Now a quadratic test equal to |x|²/2 near E also recovers its exact total trace3/4. The prior stress-to-paid-closure receiver applies on E.

## Finite parameterization and honest algorithmic scope

The smooth compact potentials can be approximated in C² by rational polynomial matrix potentials multiplied by a fixed rational C⁵ cutoff on a sufficiently large ball. Keep coefficients in a rational basis of the four-dimensional trace-free J-null symmetric matrix space. The K-image error tends to zero in L1 on the fixed ball. Therefore a countable rational library of global compact tensor potentials is also complete in the above sense.

Turning this into an executable lower-primal search requires a received upper evaluation of the true negative spectral mass, including S0's vertex/radial geometry and every cutoff region. The exact radial polynomial compiler is an initial interface, not that complete evaluator. A successful vanishing sequence would prove source membership; a failure of a finite library, a sampled objective, or a nonterminating search proves neither nonmembership nor a Morrey counterexample.
