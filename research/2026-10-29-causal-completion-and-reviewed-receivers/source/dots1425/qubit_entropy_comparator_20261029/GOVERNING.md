# Explicit entropy comparators for unital qubit broadcasting and correlated spin products
2026-10-29. New scoped analytic construction; independent receiving review and historical novelty assessment pending. The unrestricted N371 problem remains open.

## Question
Can information that survives distribution to two receivers be made classical without losing substantially more information? Astra N371 identifies a missing entropy comparator; its existing quadratic covariance comparators do not justify a nonlinear entropy bound. We construct an explicit common projective measurement for unital qubit channels, and a separate reference-stable tensor-product theorem covering correlated input states and correlated priors. No fitted encoder, unknown-environment reconstruction or recovery architecture is being optimized here.

All logarithms are natural. Phi is a unital CPTP qubit channel with a full-domain two-output extension whose two marginals equal Phi (self-compatibility). Write its Bloch matrix by proper-rotation singular-value decomposition as T=O_out diag(lambda1,lambda2,lambda3) O_in, allowing signed diagonal entries, with |lambda1|>=|lambda2|>=|lambda3|. Let n be the leading right singular axis. Delta_n is the rank-one projective measurement in that axis followed by preparation of the measured eigenstate. This is a single known EB channel on all input states.

## 1. Compatibility gives the decisive singular-value inequality
Measure the two orthogonal leading output Pauli observables on the two separate outputs of the extension. Pulling the joint measurement back to the input gives compatible unbiased binary qubit observables with Bloch vectors a,b, orthogonal and of lengths |lambda1|,|lambda2|.

For completeness, write their four joint effects as G_st=(gamma_st I+g_st.sigma)/2. Positivity gives |g_st|<=gamma_st, normalization gives sum gamma_st=2 and sum g_st=0, and marginal conditions give a+b=g_++-g_--, a-b=g_+--g_-+. Hence |a+b|+|a-b|<=2. Orthogonality implies

 lambda1^2+lambda2^2<=1.                              (A)

This standard joint-measurability necessity is derived here directly. Related primary source: Busch–Heinosaari, Approximate joint measurements of qubit observables, arXiv:0706.1415 / QIC8(2008)797–818. No sufficiency or full characterization of self-compatible channels is assumed.

## 2. Sharp local factor 2 for this dephasing comparator
For every qubit density rho,

 S(Delta_n rho)-S(rho) <=2[S(Phi rho)-S(rho)].          (B)

Equivalently D(rho||I/2)-D(Delta_n rho||I/2) is at most twice the corresponding Phi loss. Phi need not be self-adjoint or normal; output rotations preserve entropy.

Proof. Put c(r)=ln2-h((1+r)/2)=sum_(k>=1) r^(2k)/[2k(2k-1)], 0<=r<=1. It is increasing, and c(r/sqrt2)<=c(r)/2. For input Bloch vector r write x=(n.r)^2, y=|r|^2-x. If lambda1^2<=1/2, then |Tr|^2<=(x+y)/2. Otherwise (A) gives |Tr|^2<=t x+(1-t)y, t=lambda1^2 in[1/2,1], which is at most max{x,(x+y)/2}. Therefore in both cases

 2c(|Tr|)<=max{2c(sqrt x),c(sqrt(x+y))}
            <=c(sqrt x)+c(sqrt(x+y)).

Rearranging is (B). The constant2 is attained asymptotically for this fixed-axis dephasing choice by the phase-covariant cloner with signed singular values (1/sqrt2,1/sqrt2,1/2), a weak Bloch vector in the second leading axis, and r→0. This is not an optimality claim over all possible EB comparators.

## 3. Separate COMPLETE comparison, constant 2+sqrt2
The scalar Bloch proof above is NOT applied to quantum references. Instead, an exact channel decomposition proves, for any finite reference R and ANY joint state rho_AR,

 S((Delta_n tensor id)rho)-S(rho)
 <=[1/(1-|lambda2|)] [S((Phi tensor id)rho)-S(rho)]
 <=(2+sqrt2)[S((Phi tensor id)rho)-S(rho)].             (C)

To prove it, first work in the input/output unitary gauges in which Phi is a Pauli channel with probabilities p0,p1,p2,p3. Pair the four Pauli indices into cosets of the subgroup {I,sigma_n}: (0,n) and the remaining pair (j,k). Within each pair, remove its equal weights m=min(p_a,p_b). The removed two terms are precisely 2m times a Pauli-conjugated Delta_n channel. All remaining terms are nonnegative-weight unitary channels. The total pinching weight is

 alpha=2[min(p0,pn)+min(pj,pk)]
      =1-|p0-pn|-|pj-pk|
      =1-max(|lambda_j|,|lambda_k|)=1-|lambda2|.

Since lambda2^2<=1/2 by (A), alpha>=1-1/sqrt2. Each pinching branch has output entropy S(Delta_n rho), even with reference, because its final Pauli is unitary. Each residual branch has entropy S(rho). Concavity of von Neumann entropy therefore gives S(Phi rho)>=alpha S(Delta_n rho)+(1-alpha)S(rho). This proves (C), without any commutativity or independence assumption on the input/reference. Local output rotations and input basis changes preserve the statement. No complete factor2 result is claimed.

## 4. Correlated product-system theorem
Let Phi= tensor_(i=1)^n Phi_i, with every Phi_i unital self-compatible qubit, possibly with different axes and singular values. Let Delta=tensor_i Delta_ni and alpha*=min_i(1-s_i,2). For arbitrary joint rho_(A1...An R), with finite reference R,

 S((Delta tensor id_R)rho)-S(rho)
 <= alpha*^(-1)[S((Phi tensor id_R)rho)-S(rho)]
 <= (2+sqrt2)[S((Phi tensor id_R)rho)-S(rho)].           (D)

Proof. Expand the exact local channel decompositions from section3. A branch of the product is a local Pauli output conjugation of Delta_S, the channel dephasing a subset S of sites; the inclusion probability of site i is alpha_i. Quantum entropy concavity gives

 S(Phi rho)-S(rho)>=E_S f(S),
 f(S)=S(Delta_S rho)-S(rho).

The set function f is normalized, monotone and submodular. Indeed its increment at i is the Holevo information of the binary equiprobable unitary ensemble {rho_S, Z_i rho_S Z_i}. Applying another commuting dephasing Delta_j to both members cannot increase that Holevo information, by data processing. Hence increments decrease as S grows. This argument includes arbitrary correlated quantum references.

For an elementary bound avoiding any unjustified independent-sibling assumption, fix a site ordering. Submodularity gives, for EVERY subset S,

 f(S)>=sum_(i in S)[f({1,...,i})-f({1,...,i-1})].

The bracket terms are nonnegative. Averaging therefore gives E f(S)>=alpha* f(all). Independence of subset membership is not even needed for this final inequality; the actual product channel supplies it, but the proof does not infer independence of quantum outputs. This proves (D).

## 5. Actual-prior Holevo consequence and its precise limitation
For any finite ensemble {p_x,rho_x} on these n qubits let bar_rho=sum p_x rho_x, delta=chi(E)-chi(Phi E), and kappa=S(Phi bar_rho)-S(bar_rho)>=0. Entropy algebra gives

 sum_x p_x[S(Phi rho_x)-S(rho_x)]=delta+kappa.

Dephasing satisfies D(rho||Delta rho)=S(Delta rho)-S(rho). Pinsker and Jensen applied to the EXPLICIT product-basis EB map Delta yield

 sum_x p_x T(rho_x,Delta rho_x)
 <=sqrt[(delta+kappa)/(2alpha*)]
 <=sqrt[(1+1/sqrt2)(delta+kappa)].                     (E)

For any stationary barycenter Phi(bar_rho)=bar_rho, kappa=0. In that case (D) also forces Delta(bar_rho)=bar_rho, and the measurement Holevo loss is at most (2+sqrt2)delta. In particular this holds when bar_rho=I/2^n, while the individual states and label priors may be arbitrarily correlated across sites. For one qubit the local (B) sharpens (E) to average error<=sqrt(delta) under the same stationary/maximally mixed barycenter condition, and measurement Holevo loss<=2delta.

This is NOT the unrestricted N371 theorem: globally nonfactorable channels, nonunital local channels, and arbitrary nonstationary barycenters are not covered by a delta-only assertion. The explicitly visible kappa term cannot be discarded. No independent product prior is required. This is stronger in that respect than the replacement-channel/independent-prior exclusion in the read N371 source, but remains a restricted channel class.

## 6. Tests and open obligation
check_comparator.py generates100 actual self-compatible channels by Pauli-twirling isometries into the symmetric two-qubit subspace, including40 near-classical limits. It tests24,000 local/reference states (reference dimensions1,2,4). The local factor2 passes; numerical reference factor2 was not violated but is NOT proved. check_tensor.py independently reconstructs the probability pairing and tests100 three-qubit/reference2 correlated states, all subset-submodularity inequalities, the entropy-mixture step and final complete bound. Probability reconstruction residual<=5.56e-17. These are floating diagnostics, not proof-assistant or hardware evidence.

The phase-covariant boundary and possible complete factor2 improvement need targeted adversarial work. More important is replacing the factorable-unital structural premise with an intrinsic acquisition/entropy condition. A general correlated Pauli channel with a supplied decomposition into Pauli-conjugated partial-dephasing channels and minimum site coverage alpha also obeys the same proof; self-compatibility alone has not been shown to acquire such a decomposition. That is a concrete missing mechanism rather than a generic optimizer task.

## Provenance and scientific significance
Astra Research search was attempted first but timed out. Pinned GitHub revision d5366275f4886a027526b70997e75db2c19e4efa was used. Current N371 packet and actual governing sources were read: web/pages/d-5f6386197dd232a0.html (entropy-tree obstruction), web/pages/d-fe3fa46d60aa1856.html (sharp exponent obstruction and failed routes). They explicitly distinguish prior-average Holevo loss from worst-case preservation and warn that quadratic comparisons do not imply entropy comparisons. The present argument uses exact convex channel decompositions and entropy-data-processing submodularity instead. N353/N368 bounded-capacity closure is not being reopened. No historical-priority claim is made; quantum entropy-comparison and logarithmic-Sobolev literature must be compared before any novelty assertion.
