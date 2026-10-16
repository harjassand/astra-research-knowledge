# Reconstructed import lemmas and their exact boundaries

Author: `ge_primary_prior`, assigned by the parent investigator on 16 October 2026. These are self-contained mathematical reconstructions, not independent specialist certification or historical originality claims. They are provided so that an import is a checkable argument rather than a title match. No acquired executable code was run.

## 1. Interchange survival and two-sided perturbation

Let a finite undirected graph have fixed nonnegative symmetric exchange rates `r_e`. A configuration is a positions-to-labels permutation `sigma`; an edge acts by right multiplication by its transposition `tau_e`. Put `A_e=I-T_e`, `L_r=sum r_e A_e`, and `P_r(t)=exp(-tL_r)`.

Start two copies with configurations `sigma` and `sigma tau_e`. Until coalescence there are exactly two discrepant sites. Use common clocks except on the edge joining those sites, where use independent clocks in the two marginals. A jump on that joining edge coalesces the copies. All marginal edge rates remain correct. The unordered discrepant sites move as two independent graph walks killed on meeting: an allowed single-site move has the physical edge rate, and an occupied joining edge has killing rate twice that rate. Thus, for its killed generator `H_r`,

`S_r,e(t)=[exp(-tH_r)1]_e`

bounds the endpoint TV distance from an initial transposition, uniformly in labels. This is the weighted form of the Aldous-Fill interchange coupling (Chapter 14.5, Proposition 14.30 proof).

The group kernel is `P_r(t)(sigma,eta)=p_r(t,sigma^-1 eta)`. Uniform reversibility gives `p_r(t,g)=p_r(t,g^-1)`. Changing variables by inversion in the row finite difference therefore gives

`||delta_sigma P_r(t) A_e||_1 <= 2 S_r,e(t)`.

The direct initial-transposition coupling gives, by duality,

`||A_e P_r(t)f||_infinity <= 2 S_r,e(t)||f||_infinity`.

For another rate vector `q` on the union of the two edge sets, finite-dimensional Duhamel and `A_e^2=2A_e` give

`P_r(1)-P_q(1) = integral_0^1 P_r(u)(L_q-L_r)P_q(1-u) du`,

`TV(delta_sigma P_r(1),delta_sigma P_q(1))`

`<= sum_e |r_e-q_e| integral_0^1 S_r,e(u) S_q,e(1-u) du`.

Indeed the integrand paired with `||f||_infinity<=1` is at most `2 S_r,e(u)S_q,e(1-u)`, and TV of a zero-mass measure is one half the dual supremum. The bound allows zero rates and added edges. It is an upper bound, not necessarily the optimal coupling distance. Its inversion step is specific to the group model; generic reversible occupancy chains do not inherit it merely from reversibility. Color/exclusion projections contract TV after the full-permutation bound is obtained.

This reconstructs the supplied pair theorem from its actual assumptions. Aldous-Fill supplies the coupling, but the exact finite-difference product certificate and its historical priority are separate questions. No exact prior equivalent was established by the bounded source review.

### The stopped local Green bound

For an edge of current rate `w>0`, suppress boundary edges of a connected positive-rate vertex cluster `C` containing its endpoints. Restrict the unordered killed pair chain to the communicating domain of its initial state `z`; let its size be `M`. It is finite, symmetric, and has direct killing at `z` of at least `2w`. Every state in the communicating domain can reach `z`, so eventual killing has probability one and `G=H^-1` exists with nonnegative entries.

Set `h(a)=G(a,z)`. The killed maximum principle gives `0<=h(a)<=h(z)`: a positive maximum off `z` propagates along any nonkilled neighbors until it reaches `z` or a killing boundary. At `z`,

`1=(Hh)(z)=k_z h(z)+sum_a q_za(h(z)-h(a)) >= 2w h(z)`.

Symmetry then gives

`E_z tau=sum_a G(z,a)=sum_a h(a)<=M/(2w)`.

This also handles disconnected ambient graphs, because only the reachable internal domain was inverted. With `c=M/2`, and with the total external discrepancy exit hazard bounded by `b` before internal meeting, the integrated hazard bound is

`P(exit before tau)<=E integral_0^tau b ds<=bc/w`.

Hence the physical, unsuppressed interchange coupling satisfies

`a_e(t)<=min(1,(c/w)(1/t+b))`.

Only this bound is localized; the physical semigroup in the inversion and Duhamel argument remains unchanged. Taking `M<=binomial(|C|,2)` yields `c=|C|(|C|-1)/4`. The correct `b` is the sum of the two largest external weighted degrees in `C`.

For `q=c/w<=1/2`, `f_q(t)=min(1,q/t)` obeys

`integral f_q=q(1+log(1/q))`,

`integral f_q(t)f_q(1-t)dt=2q[-q log q-(1-q)log(1-q)]`

`<=2q^2(1+log(1/q))`.

Using `a_e<=f_q+qb` and integrating the resulting rate derivative from `K>=2c` to infinity yields precisely the supplied local cap

`B_local(K;c,b)=(c^2/K)[b^2+2(1+b)(2+log(K/c))]`.

This is a reconstruction of `LOCAL_SATURATION_PROOF.md`, not a new claim. The constants charge cluster size and boundary hazard; no cluster-discovery, calibration or practical-speed result follows.

### Late improvement: classical reversed Chebyshev removes the logarithm

For any nonnegative nonincreasing integrable functions `s,v` on `[0,T]`, set `f(u)=s(u)` and `g(u)=v(T-u)`. The functions `f,g` have opposite monotonicity, so

`T integral_0^T f(u)g(u)du - (integral_0^T f)(integral_0^T g)`

`= (1/2) integral_0^T integral_0^T (f(u)-f(z))(g(u)-g(z)) du dz <=0`.

This is the classical reversed Chebyshev integral inequality. Applied to survival functions with finite means `mu_s,mu_v`, it gives the exact inequality

`integral_0^T s(u)v(T-u)du <= (1/T)(integral_0^T s)(integral_0^T v) <= mu_s mu_v/T`.

No independence between the corresponding lifetimes is required, because only their marginal survival functions appear. The parent independently received an interval-overlap proof of the same inequality; that proof is another elementary derivation, not evidence of historical originality. A primary published use explicitly stating the reverse inequality for opposite monotonicity is Mondal-Akel (2018), equation (3.6) and the following sentence on page 11. This is a source for the classical ingredient, not an asserted first historical source.

For the physical killed pair on a finite graph, the preceding Green proof on its reachable communicating domain gives `mu_r,e<=c_e/r_e`, with `c_e=M_e/2`. A uniform choice valid across all rate vectors is `c=binomial(n,2)/2`. The already reconstructed two-sided interchange certificate therefore implies, for positive rates on every changed edge,

`TV(P_r(T),P_q(T)) <= (c^2/T) sum_(e:r_e!=q_e) |1/r_e-1/q_e|`.

Different valid constants for the two rate vectors can replace `c^2`. Edges absent from both vectors contribute nothing. A change involving a zero rate has no finite reciprocal estimate from this formula, though the original survival certificate still applies. This is an absolute endpoint-TV upper bound and may exceed one.

In particular, capping `m` rates above `K>0` at `K` gives `TV<=m c^2/(T K)`. The logarithm and the original condition `K>=2c` disappear from this coarse global cap. This is a consequential source-relative improvement over the supplied N727 envelope, derived here from the exact supplied two-sided certificate and a classical inequality. Historical priority of this *interchange composition* remains UNKNOWN.

The local stopped bound also sharpens directly. Let `tau_C` be the internal meeting time, with mean at most `c_C/w`; let the pre-meeting boundary-exit hazard be at most `b`. The physical pair survival is bounded by `P(tau_C>t)+P(exit before tau_C)`. Integrating only to `T` gives

`integral_0^T S_physical,e(t)dt <= (1+bT) c_C/w`.

Applying reversed Chebyshev to the two *physical* nonincreasing survival functions therefore gives the local finite-change bound

`TV <= sum_e [c_r,e c_q,e/T] (1+b_r,e T)(1+b_q,e T) |1/r_e-1/q_e|`.

Each cluster must contain the edge endpoints and be connected through positive internal rates in its own physical rate vector; the two clusters and their constants may differ. This argument alters an upper estimate and preserves both original physical generators. Cluster selection, joint controller hypotheses and numerical usefulness remain separate obligations.

## 2. Ordered-path exterior powers and classical Pfaffian survival

Let `L` be the weighted nearest-neighbor path Laplacian on `n` ordered vertices and `K(t)=exp(-tL)`. For `k<=n`, let `H_k` be the killed generator of `k` independent walkers, represented by ordered occupied sites `X=(x_1<...<x_k)`, killed at the first collision.

The derivation `d_k L` on the exterior basis `e_x1 wedge ... wedge e_xk` has diagonal `sum_i L_xixi`. Every allowed nearest-neighbor jump preserves particle order and has off-diagonal `-r`; an attempted jump into another occupied vertex vanishes in the exterior algebra while its diagonal exit rate remains. Thus `H_k=d_k L` entrywise, including collision killing. Since exterior powers intertwine exponentiation,

`exp(-tH_k)=wedge^k K(t)`,

`[exp(-tH_k)]_X,Y=det[K_xi,yj(t)]_(i,j=1..k)`.

Summing over `Y=(y_1<...<y_k)` gives the no-collision survival `S_X(t)`. This is the finite weighted-path form of classical Karlin-McGregor noncollision machinery. It does not describe the original interchange endpoint as independent walkers.

Define the `n` by `n` antisymmetric matrix `J_uv=sign(v-u)`. For even `k`, the Pfaffian minor-summation identity gives

`Pf(A J A^T)=sum_{|Y|=k} det(A_:,Y) Pf(J_Y,Y)`.

One proof is to apply the linear map with matrix `A` to the exterior two-form `sum_{u<v}J_uv e_u wedge e_v` and compare its `k/2`th exterior-power coefficient. Multilinearity gives the minors on one side and the Pfaffian expansion on the other. For every ordered even `Y`, `Pf(J_Y,Y)=1`: expanding in the first row reduces inductively to `sum_{j=2}^k(-1)^j=1`. Therefore, with `A=K_X,:`,

`S_X(t)=Pf(K_X,: J K_X,:^T)` for even `k`.

For odd `k`, append one phantom initial and terminal vertex with its only transition to itself. The same even identity yields

`S_X(t)=Pf([[K_X,: J K_X,:^T, K_X,:1],[-(K_X,:1)^T,0]])`.

For a conservative path `K1=1`, the added column is all ones. These formulas are classical variable-terminal-point Pfaffian machinery (Stembridge 1990, Theorem 3.1 and its odd-size phantom-vertex remark; the paper also explicitly credits Okada's minor summation). The argument here avoids assuming that an arbitrary synchronous discrete-time walk has the same collision rule as the continuous-time chain.

For `k=2`, this is exactly the supplied bilinear pair survival. If approximate rows have l1 norm at most one and individual row error at most `epsilon`, telescoping the two factors gives error at most `2epsilon`. For higher Pfaffians, a separate finite-precision error analysis is required; the pair error budget cannot simply be reused.

### Cycle twist and parity qualification

For a weighted connected cycle, replace the one-walker wrap-edge off-diagonal by its ordinary value multiplied by `(-1)^(k-1)`, retaining the ordinary degree diagonal; call this matrix `L^(k)`. A legal wrap jump moves one coordinate past the other `k-1` coordinates in the ordered wedge, so its exterior sign cancels this twist. Therefore `H_k=d_k L^(k)`.

For even `k` this is the antiperiodic one-walker matrix. Its heat kernel is the first-half minus second-half projection of the ordinary positive `2n`-cycle heat kernel, by the explicit intertwiner `T=[I;-I]`. For odd `k` the ordinary periodic kernel is used. The same minor-summation identities apply to the appropriate signed kernel.

In particular, an odd-`k` cycle Pfaffian uses the *periodic* kernel bilinear matrix, not the physical two-walker survival matrix (which uses the antiperiodic kernel). This parity distinction prevents a false all-particle extension by reusing one pair-survival array. Cycle parity twists and the distinction between one-body flux and exchange phase are established machinery, closely reflected in Harrison-Keating-Robbins (2011), Sections 3d-3e and 4b.

### Restricted branch obstruction

On the positive three-leaf star, the unordered-pair loop

`(1,2),(0,2),(2,3),(0,3),(1,3),(0,1),(1,2)`

exchanges the labelled walkers. Hence the exterior reordering signs multiply to `-1`. Each physical star edge is traversed once in each direction, so every fixed Hermitian one-particle U(1) edge gauge contributes product `+1`. A pair-basis diagonal gauge also telescopes to `+1`. The mismatch therefore cannot be repaired by a fixed one-particle edge gauge plus a diagonal pair-basis gauge. Extra graph edges do not remove this existing loop. This is the exchange-cycle versus Aharonov-Bohm distinction explicit in Harrison-Keating-Robbins, especially Section 4c. It is not an obstruction to larger configuration covers, nonlocal transformations or other algorithms.

## 3. What finite controller reachability actually buys

This elementary lemma isolates one step invoked in arXiv:2601.20818v3, SI VII.2. It does not prove that that paper's clock rule, or any proposed controller, satisfies its premise.

Suppose a finite local continuous-time Markov controller has a designated completion event. Before completion, assume every possible state admits a path to completion of at most `L>=1` allowed transitions, every transition along that path has rate at least `r>0`, and the total update rate, including prescribed transitions, is at most `R<infinity`. For a controller coupled to an exterior, require the chosen path to remain allowed with these rate bounds throughout the interval under every admitted continuation of the exterior history. The conditional event-density bound below must hold uniformly in that influence. A path that exists only with a frozen boundary does not meet this stronger premise.

Choose `0<Delta<=1/r`. For a path of length `ell<=L`, the event that exactly its prescribed transitions occur in order during `Delta`, with no competing event, has probability at least

`exp(-R Delta)(r Delta)^ell/ell! >= p`,

`p=exp(-R Delta)(r Delta)^L/L! >0`.

The first bound follows by integrating the Markov path density over the ordered simplex of event times, whose volume is `Delta^ell/ell!`. The second uses `r Delta<=1`. Already-completed states have success probability one. Reapplying this conditional bound in successive fresh blocks gives

`P(tau>m Delta)<= (1-p)^m`, `E tau<=Delta/p`.

An independent noise stream of total local rate `nu` has probability at most

`E[1-exp(-nu tau)]<=nu E tau<=nu Delta/p`

of firing before noiseless completion. This supplies an explicit version of an `O(nu/v_*)` estimate under the stated path premise.

Finite state space alone gives none of the path premise, absence of closed traps, validity under exterior influence, or useful constants. A marginal per-location fault bound also does not supply the joint conditional local-stochastic fault model needed by an exRec/Toom renormalization proof. Overlapping neighborhoods, random waiting intervals, clock faults, repair spread and causal readout require separate arguments. Consequently this lemma does not complete the continuous-time threshold outline or turn the periodically driven construction of arXiv:2610.05589v1 into a time-independent one.
