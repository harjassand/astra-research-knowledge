# Closed sampling family and decisive ordinary-method comparison

The phase-sampler and overlap interfaces can both be constructed for a finite union of bounded perturbations of affine Gaussian phases. In this fully closed family, ordinary global rejection is at least as efficient as the transport race in the underlying Gaussian-proposal count. This prevents claiming a new complexity breakthrough for this family.

Let phase i have coordinates x=m_i+A_i z, A_i invertible, and unnormalized weight

w_i(x)=exp[-c_i-||z||^2/2-V_i(z)], with known L_i <= V_i(z) <= U_i.

Write W_i=V_i-L_i in [0,R_i], R_i=U_i-L_i,

B_i=exp[-c_i-L_i] |det A_i| (2 pi)^(d/2),
s_i=E_{z~N(0,I)} exp[-W_i(z)], and Z_i=B_i s_i.

## Constructive phase sampler

Repeatedly draw z~N(0,I) and accept with probability exp[-W_i(z)]. Return m_i+A_i z. It samples the conditional phase exactly in the ideal random-real model, uses no unknown partition function, and requires 1/s_i <= exp(R_i) expected Gaussian proposals. Certified finite precision yields the corresponding controlled approximation; NumPy experiments below are numerical verification rather than a claim of exact real arithmetic.

## Constructive map and overlap

T_ij(x)=m_j+A_j A_i^{-1}(x-m_i). In z-coordinates the common normal base aligns exactly. Choose the race's source-i probability q=B_j/(B_i+B_j), which is known before sampling. The source-i acceptance is min(1, exp[W_i(z)-W_j(z)]), and source-j acceptance is min(1, exp[W_j(z)-W_i(z)]).

Let I=E_phi min(exp[-W_i],exp[-W_j]) and D=(B_j/s_i+B_i/s_j)/(B_i+B_j).

The race success probability is lambda=D I. One race attempt uses D expected underlying Gaussian proposals because it first obtains one conditional phase sample. Consequently one accepted exact phase label costs exactly

E[number of underlying Gaussian proposals]=D/(D I)=1/I <= exp(max(R_i,R_j)).

An additional independent phase-conditional sample is required for a full exact equilibrium configuration. All affine solves and potential evaluations must also be counted. Per-call arithmetic is O(d^2) for dense factors after O(d^3) factorization, plus the cost of V_i evaluations. If R=O(log d), this is polynomial; if R grows proportionally to d, it is exponentially costly.

## Ordinary global rejection dominates this closed family

A directly evaluable normalized proposal is already available: choose phase i with probability B_i/(B_i+B_j), draw z~N(0,I), accept exp[-W_i(z)]. Its output is an exact complete equilibrium configuration. Its acceptance probability is

s_global=(B_i s_i+B_j s_j)/(B_i+B_j),

so its expected Gaussian-proposal count is 1/s_global. Pointwise,

min(exp[-W_i],exp[-W_j]) <= (B_i exp[-W_i]+B_j exp[-W_j])/(B_i+B_j).

Therefore I <= s_global and

1/s_global <= 1/I.

The direct method generates an entire configuration with no more expected underlying Gaussian proposals than the race spends on the phase label alone. It also evaluates only the selected potential for each proposal. This is an equally informed, ordinary rejection method, not an unfair comparator.

## Consequence for the independent forward programme

The exact history-adaptive phase-label theorem remains valid and potentially useful when conditional samplers are externally supplied and their normalizing constants unavailable. But for the explicit broad family above, completing the physical/computational access reveals an ordinary method with equal or better complexity. Generic convex-basin alternatives would require an actual learned-map complexity theorem and would face established log-concave integration/annealing, Bennett/bridge sampling, and Bernoulli races. I cannot currently justify a new consequential scientific endpoint beyond that literature from this construction. It should be retained as a correct lemma and an access-model diagnostic, not sold as a metastability solution or new general free-energy algorithm.

## Allocation caveat and stronger full-configuration comparison

The phase-label cost inequality above uses the explicitly chosen q=B_j/(B_i+B_j); it is not a universal bound over branch allocations. For arbitrary exact phase-label selection followed by a fresh conditional rejection sample, however, the expected cost of the final conditional sample alone is p_i/s_i+p_j/s_j=(B_i+B_j)/(B_i s_i+B_j s_j)=1/s_global, exactly the complete direct-rejection cost. Phase selection adds to that. Consequently the full-configuration dominance survives arbitrary online branch adaptation within this architecture.
