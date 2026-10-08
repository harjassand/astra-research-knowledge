# Exact finite-N singlet marginal certificates and dimension-dependent obstruction

**Date:** 2026-10-08 (Brisbane). This is a continuation of draft PR #7, not a field-breaking claim. The all-d macroscopic 1/(d+1) separability threshold in RESEARCH_STATE.md is a distinct, internally derived theorem candidate. No independent expert review or priority certification. The explicit finite identities below were newly rederived and independently evaluated using exact rational arithmetic in this session.

## Definitions and self-contained character certificate

For d|N let Omega_N be the normalized SU(d)-invariant projector on (C^d)^tensor N; Omega_(N,k) its marginal on k sites. The exact Schur–Weyl Young-shape weights are

p_(N,k)(lambda)=f^lambda f^mu / f^(r^d), r=N/d,
mu_i=r-lambda_(d+1-i), lambda_i<=r,

with f^lambda=k! prod_(i<j)(lambda_i-lambda_j+j-i)/prod_i(lambda_i+d-i)!. The state commutes with global SU(d) and site permutations, and is scalar on each Schur–Weyl summand, so **matching all Young-shape weights is equality of quantum states**, not only equality of chosen observables.

For qubit Bloch vectors r_1,...,r_k in the unit sphere S², set P(r)=(I+r.sigma)/2 and let Twirl(r_1,...,r_k) mean the joint average of tensor_i P(r_i) under global SU(2) rotations and site permutations. Twirl(...) is exactly fully separable.

The spin-j Young-sector probability of this twirl is

q_j=(2j+1) integral_(S³) U_(2j)(u0) prod_(i=1)^k (u0+i vec(r_i).vec(u)) dOmega(u),

where Haar SU(2) is S³, U_m Chebyshev of second kind. Each integral is a finite polynomial combination of exact sphere moments

E[prod_(a=0)^3 u_a^(2m_a)]=prod_(a=0)^3 (1/2)_(m_a) / (2)_(sum m_a),
and odd powers have zero expectation.

The companion `verify_finite.py` uses ONLY Python standard library fractions and arithmetic in Q(sqrt(3)) to compute these integrals exactly; no Monte Carlo, symbolic-algebra black box, or external assumptions.

## Certified case I: N=10,k=4

Frames:
- Tetrahedron T: r=(±1,±1,±1)/sqrt(3) with sign product +1.
- Balanced double-antipode Z: (+z,+z,-z,-z).

Exact spin-sector probabilities j=2,1,0:
- q(T)=(1/9,2/3,2/9)
- q(Z)=(1/6,1/2,1/3)
- p_(10,4)=(5/42,9/14,5/21).

**Exact identity:**

Omega_(10,4) = (6/7) Twirl(T)+(1/7) Twirl(Z).

Thus this marginal is fully separable, even though the global Omega_10 is very far from the fully separable set in the large-N limit (different assertion).

## Certified case II: N=16,k=6

Three balanced frames:
- D: three +z followed by three -z.
- H: two copies of the planar equilateral triple (1,0,0),(-1/2,+sqrt(3)/2,0),(-1/2,-sqrt(3)/2,0).
- P: equilateral triple at z=+1/2 with points (sqrt(3)/2,0,1/2),(-sqrt(3)/4,+3/4,1/2),(-sqrt(3)/4,-3/4,1/2), and reflected copy at z=-1/2.

Spin weights for j=3,2,1,0:
- q(D)=(1/20,1/4,9/20,1/4).
- q(H)=(11/320,15/64,189/320,9/64).
- q(P)=(233/10240,539/2048,5877/10240,287/2048).
- p_(16,6)=(7/286,75/286,81/143,21/143).

**Exact identity:**

Omega_(16,6) = (201/3289) Twirl(D)+(16/3289) Twirl(H)+(3072/3289) Twirl(P).

All mixing coefficients are positive, sum to 1, and each term is a convex mixture of tensor products of six qubit states.

## Exact obstruction: naïve all-d FINITE-N strengthening is false

Let d=3,N=9,k=3. Then Schur weights corresponding to (3), (2,1), (1,1,1) are

p=(5/42,16/21,5/42).

For any fully separable three-qudit state sigma and the projector P_sym on the symmetric subspace,
Tr(P_sym sigma)>=1/3! =1/6.

Proof: for a pure product the overlap is per(G)/3!, where G is the three-by-three Gram matrix of its normalized single-site vectors. Marcus's established permanent-diagonal inequality gives per(G)>=prod diag G=1. Extend to all fully separable sigma by convexity.

Since Tr(P_sym Omega_(9,3))=5/42, the two-outcome test P_sym versus I-P_sym yields

**dist_T(Omega_(9,3),SEP_3) >= 1/6 - 5/42 = 1/21.**

The second-order collective Casimir witness is *exactly saturated* at this (d,N,k), so it cannot certify this entanglement. This disproves the tempting claim that finite-N separability is equivalent in every dimension to (d+1)k<=N+d. It does not refute the earlier ASYMPTOTIC fixed-d threshold.

## Novelty and significance boundary

- The two qubit identities and the qutrit witness are exact mathematical deductions; their priority relative to prior spin-separability/de Finetti literature is UNKNOWN.
- The separate 1/(d+1) asymptotic theorem candidate needs external specialist review of compact-group Fourier/heat-kernel arguments.
- The finite statements are not a universal separability criterion and do not imply quantum advantage or deep entanglement.
- Markus/Marcus permanent diagonal bound predates these deductions and is not new.
- Highest-value continuation within this subject: prove/disprove the **qubit-only** exact conjecture Omega_(N,k) is fully separable iff N>=3k-2 for all even N,k; the verified cases k=2,4,6 do not settle it. Avoid extrapolation to d>=3; the counterexample is decisive there.

## Broader high-upside scan from same single-agent run

Independently examined Lieb's permanental-dominance conjecture (1966) and Lavi's September 2026 quadratic strengthening implying both Lieb and Chollet, as well as arbitrary-dimensional weakly reversible stochastic recurrence. These remain OPEN. A numerical scan of n=6 irreducible symmetric-group Fourier blocks of random complex Gram matrices did not find a counterexample to the quadratic strengthening; that is finite negative evidence only, NOT a proof. Published Li 2026 n<=15 and Lavi Sept 29 progress through n<=17 preempt naive finite-order novelty claims. Source: https://yair-lavi.com/mincs-list/conjecture-42/index.html and https://yair-lavi.com/publications/quadratic-permanent-conjecture/index.html .

No new field-breaking theorem was established; do not promote this draft PR as one without historical novelty and independent correctness certification.
