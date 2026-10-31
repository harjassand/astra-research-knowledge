# Native dark-source logical reduction: candidate construction

Status: root derivation, not independently reviewed. Ordinary adiabatic elimination is the governing baseline, not claimed invented here. This extends the logical-output question beyond source-diagonal classical noise. No source output or source-directed control is promised.

## Acquired physical inputs

A finite source Lindbladian G=sum D[L_j], with no additional unpriced source Hamiltonian, has known pure dark vector psi, L_j psi=0. H=.5 sum L_j^dagger L_j obeys gQ<=H<=hQ, Q=I-|psi><psi|, g>0, and G^dagger H<=-kappa H. Preparation of psi, K and H encodings are acquired and charged. The physical generator is lambda G-i[H0+sqrt(lambda)K,.], with Hermitian K, ||K||<=b, and <psi|K|psi>=0 as an operator on the system. The potentially large H0 acts only on the system. Let d>=||[H0,K]||. Mean coupling, if present, must remain in the actual system Hamiltonian and may change d; it cannot be discarded.

## Complete source return and resolvent

For any source/reference input, p=Tr(Q sigma_t)<=min(1,(h/g)exp(-kappa t)). Gentle projection followed by comparing its reference marginal with the true reference marginal gives

    ||(exp(tG) tensor id)(rho)-|psi><psi| tensor rho_ref||_1
        <=2 sqrt(p)+p.

Consequently the channel diamond distance is bounded by min(2,3 sqrt(h/g) exp(-kappa t/2)). Its integral is at most

    ell=(4/kappa)[1+log((3/2)sqrt(h/g))].

The Heisenberg resolvent R=int_0^infty(exp(tG^dagger)-Pi)dt thus has complete norm <=ell, where Pi(X)=I_source tensor <psi|X|psi>. R Pi=Pi R=0 and G^dagger R=-(I-Pi). This is a norm certificate, not a free implementation of R.

Let P embed system observables, V=i[K,.], L0=i[H0,.]. Define analysis-only maps

    F1=R V P, F2=R V F1, D=Pi V F1,
    T=P+lambda^(-1/2)F1+lambda^(-1)F2.

Because Pi V P=0, G^dagger F1=-VP and G^dagger F2=-(I-Pi)VF1. Bounds are f1<=2b ell, f2<=4b^2 ell^2, ||D||cb<=4b^2 ell. R need not be implemented for this proof.

## An actually constructive CP effective generator

The dark-coherence identity is exact:

    G(|v><psi|)=-H|v><psi|, for v orthogonal to psi,

and its adjoint counterpart. Therefore the second-order effective Schrödinger generator is

    L_eff(rho)=-i[H0,rho]+Tr_source(E rho E^dagger)
                       -.5{E^dagger E,rho},
    E=sqrt(2)(H_Q^(-1/2) tensor I) K (|psi> tensor I).

Here E is a stacked jump operator from system to source-label times system, not a channel isometry by itself. Positivity follows directly from this Gram factor; no full G inverse or inaccessible excited-density recovery is supplied to the implemented algorithm. For a decomposition K=sum A_i tensor B_i with Hermitian factors, this is the usual positive integrated-correlation matrix <psi|B_i Q H_Q^(-1)Q B_j|psi>, with the index orientation set by the displayed E formula. It may be complex and yield non-Hermitian jumps, so this is not merely classical Hermitian dephasing.

The norm bound ||E||<=sqrt(2/g)b is available, but it is not automatically an acquired encoding normalization. If the supplied encoding has normalization alpha_K, the directly composed stack normalization is sqrt(2/g) alpha_K. Obtaining K/b or a tighter stack port requires an actual construction or paid amplification; a norm certificate alone does not supply it. Actual finite inverse-square-root transformation on [g,h], psi preparation, K access, coherent source label retention/tracing and ordinary effective Lindblad simulation must be paid. The already acquired Gaussian free kernel may provide a better component, but is not required by the abstract formula. No claim of a free optimal normalization or hardware gate backend follows.

## Finite-rate and system-control error

L0 commutes with source R and Pi. Hence the exact residual identity yields

    ||L_lambda T-T L_eff||cb
    <=(2d ell+16b^3 ell^2)/sqrt(lambda)
       +(8bd ell^2+16b^4 ell^3)/lambda.

For system-only CPTP instruments C_j retaining all records, let

    gamma_j>=||C_j^dagger V-V C_j^dagger||cb

on the actual source/system/record algebra. Then

    ||C_j^dagger T-T C_j^dagger||cb
       <=gamma_j ell/sqrt(lambda)+4b gamma_j ell^2/lambda.

One common intertwiner across all intervals gives only two endpoint defects. Complete retained system/reference/record error is therefore at most2 and at most

    [4b ell+T_total(2d ell+16b^3 ell^2)+ell sum gamma_j]/sqrt(lambda)
    +[8b^2 ell^2+T_total(8bd ell^2+16b^4 ell^3)
       +4b ell^2 sum gamma_j]/lambda.

This is uniform over arbitrary initial QUANTUM source/system/reference correlations. It compares with an effective channel acting on the initial system marginal. No dephasing or stationary initial-state assumption is used. Source interventions are excluded; controls commuting with V have zero defect, regardless of their global bandwidth. H0 execution cost is still paid, despite only its coupling commutator entering admission.

## Unfinished questions and comparison requirements

The displayed algebra and CP coefficient orientation need independent checking. A concrete non-classical fixture, effective stack implementation and all-in error/cost comparison remain to be built. General effective-operator and adiabatic-elimination machinery is established; this is not a novelty claim. Reiter–Sorensen https://arxiv.org/abs/1112.2806 and Heisenberg elimination https://arxiv.org/html/2303.17308v2 are primary starting points. Both full primary sources have now been inspected. Reiter–Sorensen Sec. II Eqs. (3)–(5) and Sec. III.1 assume L_j=P_g L_j P_e, whereas the native source can have Q L_j Q recycling. This distinction does not establish novelty against the broader elimination literature. The construction's possible value is reusing the already earned dark-source energy certificate and constructive positive kernel for logical operation, rather than paying for a retained source history. A simple independently prepared ancilla or ordinary engineered reservoir may still be the stronger route to the same logical channel.
