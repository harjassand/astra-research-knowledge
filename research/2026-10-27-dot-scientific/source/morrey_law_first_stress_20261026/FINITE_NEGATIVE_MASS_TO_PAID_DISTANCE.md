# A finite negative-mass certificate gives a paid-closure distance bound

Status: new analytic/effective receiver, pending independent audit. No numerical small-negative-mass instance or new paid law is asserted.

Let S be any finite compactly supported signed symmetric stress, possibly extending outside E, with exact J:S=0 and DivDiv S=μ-δ0. Let N be a received upper bound for its total negative spectral trace mass.

## 1. Correct the positive part's J-charge before using null convexity

Pointwise write S=P-Q with P,Q PSD and J:P=J:Q. If c=J:P≥0, add a PSD rank-one matrix R in a J-eigenvector of eigenvalue -1/2, of trace2c. If c<0, add R in the eigenvalue1 direction, of trace -c. Then P+R is PSD and J-null, and tr R≤2 tr Q because ||J||op=1.

The received null PSD decomposition implies H:(P+R)≥0 whenever the symmetric quadratic form H is nonnegative on all q-null directions. If ||H||op≤K, then

H:S ≥ -K tr R-K tr Q ≥ -3K tr Q.

The corresponding null-concave inequality is H:S≤3K tr Q. This avoids incorrectly treating P itself as J-null, and requires no unproved measurable Finsler multiplier.

Consequently, for every globally C² null-concave U with globally bounded Hessian K,

Eμ U-U(0) ≤3KN.

Quadratic growth of U permits the endpoint test by compact cutoffs; for compact S this is immediate, and finite S with bounded Hessian can also be handled by tail cutoffs.

## 2. Bounded-Hessian global extension pays the outside-E interface

The already audited positive-accuracy reward oracle produces a strict smooth null-concave majorant U on a neighborhood of E, with U≥f on the boundary and U(0)≤V_f(0)+δ. Apply the following construction to p=-U.

Choose nested convex bodies E⊂K0⊂K1⊂K2 inside that neighborhood, and a computable smooth cutoff χ equal to one near K1 and supported in K2. Let B0 bound ||D²(χp)|| globally. Replace the earlier quartic barrier by

ψ(x)=∫_{S²} φ(n·x-h_K0(n)) dω(n),

where dω is probability area measure, φ=0 on the negative half-line and φ''(s)=s²/(1+s²) for s>0. Then ψ is C² convex, is zero on K0, and ||D²ψ||op≤1 globally. Its Hessian is positive definite outside K0.

All constants can be made explicit from the annulus gap. If dist(K2\int K1,K0)≥d0>0 and |x|+sup_{y∈K0}|y|≤R0 on K2, let r=min(1/2,d0/(4R0)). On a spherical cap of chord radius r about a separating normal, the support violation is at least d0/2. The least eigenvalue of ∫cap nn^T dω is at least r⁴/128, by direct polar integration. Thus

m0=[(d0/2)²/(1+(d0/2)²)] r⁴/128

is a valid positive annular Hessian lower bound. Take M=(B0+1)/m0. Then p_global=χp+Mψ is globally null-convex, agrees with p on E, and has Hessian norm at most K=B0+M everywhere. The cutoff transition is dominated by the convex barrier; no unsupported global polynomial concavity is assumed. The cutoff and its derivative bounds can be obtained by convolving an intermediate convex indicator with a fixed compact smooth mollifier of radius smaller than the known gaps. All input bodies and p are computable and the gaps are positive.

Therefore every reward-oracle majorant can be extended with a computable finite global K, independent of the support radius of S.

## 3. A finite reward net gives an actual W1 distance bound

Let C be the compact convex closed set of complete paid boundary laws at root0. Normalize 1-Lipschitz rewards at one fixed boundary point. Choose a finite sup-norm δ-net {f_i} of these rewards. Such a net is effective: take a sufficiently fine finite boundary net, quantize its reward values in the bounded range [-diam(E),diam(E)], and use the finite collection of functions min_j(a_j+|z-z_j|). No unknown modulus of a value function is needed to form the reward net.

For each f_i obtain a strict majorant U_i from the audited positive-accuracy oracle with U_i(0)≤V_{f_i}(0)+δ, then perform the bounded-Hessian extension above. Let Kδ=max_i ||D²U_i||sup be the received bound. Section1 gives

Eμ f_i - sup_{ν∈C}Eν f_i ≤ δ+3KδN.

Approximating an arbitrary normalized 1-Lipschitz f costs at most2δ in this difference. The compact-convex Kantorovich minimax identity therefore yields

**dist_W1(μ,C) ≤ 3δ+3KδN.**

This is a finite-stage quantitative bound even when the stress extends outside E. It is not the unproved heuristic O(sqrt N): Kδ may be extremely large, and no useful power law or runtime bound is asserted.

For a target tolerance τ, choose δ=τ/6 and obtain Kδ. Then N≤τ/(6Kδ) suffices for distance at most τ. Thus there is an effective positive threshold for each requested tolerance, though no such numerical threshold has been evaluated here.

## 4. Receiving an actual complete paid approximation

Finite actual paid laws are dense in C. Once the displayed upper distance bound is received, enumerate actual finite paid policies and compute their W1 distances to μ until one is below that bound plus any prescribed positive allowance. The accepted finite-law/source-integration receiver makes these distances computable. Density and the strict allowance guarantee termination. If desired, the previously audited Brownian or algebraic completion interfaces add a separately paid small displacement to obtain the requested final law class.

This is an obtainable actual-law construction from a sufficiently strong negative-mass certificate, not a declaration that the current signed stress has achieved one. The existing coarse objective diagnostic remains unreceived and far from zero. Finite-family Farkas does not replace a global dual majorant or this full receiving chain.

Existing receiving dependencies: morrey_nested_paid_oracle_20261025/CERTIFIED_GLOBAL_POSITIVE_ACCURACY_ORACLE.md and its independent audit supply the strict local reward majorants; morrey_global_w1_receiver_20261025/GLOBAL_W1_NEAREST_PAID_LAW.md and ROOT_GLOBAL_W1_RECEIVER_AUDIT.md supply the compact paid-closure W1 minimax/actual finite-policy receiving interface. This note adds the signed-stress charge payment and the bounded-Hessian outside-domain extension, rather than assuming a new unverified stochastic stress realization.
