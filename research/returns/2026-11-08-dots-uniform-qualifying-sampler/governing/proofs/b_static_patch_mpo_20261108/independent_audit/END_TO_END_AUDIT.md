# Fresh end-to-end audit of the combined qualifying-time sampler

> Release-copy note: this historical proof/review snapshot has presentation-only edits recorded in SOURCE_PROVENANCE.json. Mathematical content is unchanged. Current status and superseded steps are identified in START_HERE.md and DEPENDENCY_MAP.md at the package root.

8 November 2026. This review goes beyond the earlier conditional audit of the new patch evaluator. I rechecked the older regularity, discovery, propagation, activity, normalization, precision and sampling arguments rather than inheriting their earlier audit labels. A separate reviewer independently checked the combined geometry and retiling. This is mathematical research review, not formal verification or an implemented large-system sampler.

## Verdict and exact scope

**The revised combined theorem is supported. No remaining mathematical obstruction was found within its stated scope.** The new step removes the repeated logarithmic-time recursion and gives a time-uniform polynomial bound in the old qualifying regime. It does not prove all-time B.

The model is essential:

- Qubits on a finite subset of the square lattice, with static onsite and nearest-neighbor two-qubit Hamiltonian terms.
- A bound h on each term after grouping all contributions with the same physical support.
- Independent replacement by the maximally mixed one-qubit state at the same positive rate gamma on every site.
- A compact rational product input, pure or mixed; rational real and imaginary parts of all supplied matrix entries.
- Fixed rational ratio bound `h/gamma <= rho_0`. The polynomial degree is not uniform when rho_0 grows with the input.
- Computational-basis joint output, with total-variation error `0 < epsilon <= 1/2`.

With `tau = gamma T`, the sufficient nontrivial regime is exactly

    r_8 = 307584 + ceil(60 rho_0 tau),
    tau >= 76932 + 2 ceil(log_2 r_8).

The theorem promises a finite-bit randomized sampler whose unconditional output law is within epsilon in TV, using

    poly(B_input) (n/epsilon)^(C_rho_0)

operations and random bits for a finite computable constant C_rho_0 independent of n, epsilon and T. A sufficiently late mixing shortcut is used before any large-time computation. The enormous cutoff and exponent do not constitute a practical-runtime claim.

Geometrically disconnected components must be separated before bounding-box padding; arbitrary encoded gaps between components are not charged as physical lattice volume. Dividing epsilon among at most n components changes logarithmic budgets only by a constant factor. For h=0 the independent-noise law is immediate; alternatively the fixed positive bound below avoids dividing by h.

## 1. Physical hypercontractivity and the late shortcut

[King, arXiv:1210.8412, Theorem 1 and Corollary 2](https://arxiv.org/html/1210.8412v1) cover the entire range `1 < p <= q`, not merely exponents straddling 2. Tensor depolarization contracts normalized Schatten p to q when `(q-1)/(p-1) <= exp(2 gamma t)`. Hamiltonian conjugation is an isometry at every Schatten exponent. Alternating those two maps along an increasing exponent schedule and taking the finite-dimensional product-formula limit proves the same physical inequality for arbitrary interacting H, including every deleted subset and either Hamiltonian sign.

The scalar mixing shortcut does not need a new oracle. For `R=2^n rho`, first use action `(log n)/2` of hypercontractivity to obtain `||R||_2 <= 2`. The traceless part has 2-norm below 2. Run the remaining middle interval with the depolarizing spectral gap, then another `(log n)/2` hypercontractive interval from 2 to `n+1`. Conversion to infinity norm costs at most 2. This gives, for `tau >= log n`,

    ||R_tau-I||_infinity <= 4 n exp(-tau),

so the previously used `6 n exp(-tau)` is safe. For every positive effect of normalized trace one, the normalized scalar G obeys the same `|G-1|` bound. Returning log G=0 is valid once that bound is at most half the requested log error. Outside this shortcut, `tau=O(L)`, where L includes accuracy and confidence. The final output shortcut can use this conservative bound directly; a sharper entropy statement is unnecessary for the new theorem.

## 2. Coefficient regularity, independently rederived

A uniform choice across the entire ratio-bounded class is

    d=63, k=2,
    J_bound=gamma max(rho_0,1),
    a_0=1/[252 max(rho_0,1)],
    p=2/(1+a_0), u=a_0/2, theta=a_0/4.

Then `p/(2-p)=1/a_0` and `1/theta=4/a_0` are fixed constants. The incidence bound includes all one- and two-qubit Pauli expansions after grouping.

Allocate half of each site's noise to its incident Pauli terms. Each local Hamiltonian Pauli term rotates coefficient pairs at rate at most 2J, while its nonidentity local modes have damping at least `gamma/(2d)`. The coefficient-1 logarithmic norm is at most `2J-gamma/(2d)` and coefficient-2 logarithmic norm at most `-gamma/(2d)`. Interpolation gives contractivity for all q between p and 2. The local identity sector is separate and fixed. Trotter products preserve the bound despite overlap.

The residual half-noise is diagonal, with multiplier `exp(-gamma s |P|/2)`. Hölder's inequality gives its exact norm when reciprocal coefficient exponents increase. A linear reciprocal-exponent schedule therefore yields

    ||exp(sL)||_(P,2 -> P,p)
      <= [1+3 exp(-gamma s/(2u))]^(N u).

For weighted coefficient-2 norms, the logarithmic norm of one rotated pair is at most `2J sinh(k theta)-gamma/(2d)`. The chosen theta makes this nonpositive. Residual noise pays a linear increase from weight zero to theta over action `2theta`. These are explicit coefficient-space arguments, not an accidental substitution of Schatten p for coefficient p.

The resulting warm-boundary budgets are the displayed C_p and C_theta in the earlier regularity note. For action

    sigma=s_base+2ceil(log_2(tau+2)),

with parent patch `N<=K_rho tau L`, their logarithms and the infinity-norm logarithm satisfy `O_rho(L)`. The inverse power of tau produced by sigma is sufficient even at the worst `1+4u<=3`. Both warm operators are positive and normalized, so every true Pauli coefficient lies in [-1,1].

This is consistent with, and uses the same mechanism as, [Angrisani et al., arXiv:2609.40174v2](https://arxiv.org/html/2609.40174v2). Their supplied-observable propagation guarantee should not itself be quoted as worst-case output sampling.

## 3. Product-probe discovery contains no free physical oracle

The rational one-qubit probe

    rho(a,b)=[I+(aX+bY+abZ)/2]/2

is positive for a,b in {-1,1}. For its product probe and a positive normalized operator O,

    f(s)=Tr[O rho_s]
        =sum_P c_P 2^(-weight(P)) chi_P(s),  0<=f<=B.

The Walsh attenuation is exactly `2^-weight`, including Y and Z. With coefficient threshold z and weight cutoff W, every needed coefficient has Walsh magnitude at least `lambda=z 2^-W`. Both z and W have logarithmic cost `O_rho(L)` from the norm budgets, so `1/lambda=exp(O_rho L)`.

The prefix energy is the expectation of `f(u,v) f(u',v) chi_alpha(u)chi_alpha(u')` with the same suffix v and independent prefixes. This identity follows by Walsh orthogonality. Its samples are bounded by B squared. If all membership answers are clipped to [0,B] and have error xi, product bias is at most `2B xi`. The specified xi, Hoeffding sample counts, deterministic node cap and adaptive union bound suffice. Parseval bounds retained prefixes by `4B^2/lambda^2`. Signed leaf estimation, clipping coefficients to [-1,1] and common-dyadic rounding complete the coefficient-2 guarantee.

The membership values are actually computed. For the state-side warm boundary, input rho and output effect `2^N rho_s` are compact products. For the effect-side boundary, one may use input `A/2^N` and the same probe effect with reversed H, or equivalently move the original semigroup across the trace and use input rho_s and effect A. Both remain in the exact product-input/product-effect scalar class. Deleted couplings remain deleted. No correlated restart, purity oracle, physical output-sample oracle, exact sparse-row oracle or hidden coefficient oracle is assumed.

The scalar-to-log conversion uses certified B and clips before exponentiating. Values below the small-value threshold can be returned as zero within xi. Exponentiation is confined to a bounded logarithmic interval. Therefore even a failed upstream randomized estimate cannot generate unbounded transient precision or runtime.

## 4. Supplied-list propagation is finite and stable

Each allocated local Pauli generator maps a listed Pauli string to at most two strings, through independent matrices of size at most 2. The exact local semigroups contract coefficient p and 2. A first-order product formula with M sweeps has error at most `t^2 Q^2 C/M`, where `Q=O(N(J+gamma))` and C bounds the supplied coefficient-p norm.

The prescribed M and local approximation precision give enough slack for Trotter error, approximate local maps, deletion and final rounding. Pruning at the specified threshold retains at most `(2C/z)^p` coefficients. Approximate maps can amplify earlier errors by at most a constant over all updates; that factor is included. Common-dyadic denominator storage adds at most a polynomial number of bits across the polynomially many updates.

Importantly, the discovered approximate list is supplied with the conservative norm bound `C_in=S_0`, rather than assuming that coefficient-2 approximation preserves the sharper p norm. Clipping ensures this bound even on bad discovery runs. Thus every branch has a deterministic work cap. On good runs, ordinary 2-norm contraction and two-sided Cauchy–Schwarz give the desired scalar accuracy. This refresh confirms the older sparse-propagation contract independently of its prior review label.

## 5. Activity identity and precision checks

I re-read the governing `FIRST_DISCOVERY_PROOF.md`, not the superseded source-interval import. For two-body factors, a first non-null visit discovers at most one new physical vertex. The retained first-arrival path to a target is unique. Forbidding the whole target and all future retained vertices before their designated arrivals makes the free-interval construction both necessary and sufficient. Buffer separation keeps different retained paths disjoint; enlarging the root to the buffer complement is conservative. Support-preserving noise letters insert uniquely into intervals and sum to the full original noise. This avoids the earlier incorrect claim of an exact minimum Pauli-weight invariant.

The finite-patch estimate then combines product erasure, low-weight coefficient counting, spectral-gap contraction and hypercontractivity. Its actual volume factor is paid. In the sparse-mark activity estimate, the direct-sum switch penalty, Fourier extraction, marked-subset sum, physical norm conversion and isolated-baseline inverse yield exactly the stated conservative factors. Shared switches are classical coefficients, not physical graph vertices. The dense-mark estimate uses the enlarged `V=1800r^2`. The displayed scalar cutoff has ample slack for both cases.

Boolean edge Möbius inversion factors exactly over disconnected switched components because both initial state and final effect are products. This earns a genuine signed hard-core polymer representation. The isolated normalizers are at least one half. No step divides by a rare global prefix probability.

For activity decay `exp(-b v)`, the polymer count `64^v` and tail weight `kappa=b-7` leave KP slack. Under relative activity perturbations `eta_0 exp(-b v)`, the doubled envelope retains that slack. The pinned derivative bound gives `|partial log Z/partial w_C|<=exp(v)`. Consequently physical scalar precision requires only `O(log(n/delta)+bv)` bits. With adaptive `m=ceil(L/(b-7))`, `b m=O_rho L` before mixing, including the ceiling term. The older `2^-m^2` termwise input precision must not be reinstated. `O(m^2)` bits for classical Ursell integers are a different paid arithmetic cost.

I also checked that connected cluster enumeration is exponential in total size m, not `n^m` or `exp(m^2)`: connected physical supports, bounded-degree edge subsets, and the generating-function bound on polymer multisets give `n exp(O(m))`; connected-graph integers can be computed by subset recurrence.

The separate fresh geometry review independently verifies switched-shape retiling, padding and the time/accuracy branches. Product effects beyond computational projectors are valid here: for a positive block effect of normalized trace one, `A-I` has the same required normalized 1 and `1+1/a` bounds. They are not arbitrary correlated effects.

## 6. Why one level is sufficient for every n and epsilon

All below uses normalized action, meaning the patch theorem is applied to `L/gamma` at time sigma. This prevents an artificial inverse-gamma runtime factor. Rational division costs only polynomial input bits.

Outside the late shortcut, `tau=O(L)`. The old parent construction has `N_parent=O_rho(tau^2+tau L)` and `exp(O_rho L)` work and membership calls. Its fixed precision inflation produces `L'<=A_rho L`, which is explicitly retained once.

Retiling a membership scalar at its own action sigma gives

    N_child=O_rho(sigma^2+sigma L')=O_rho(L log(L+2)).

The dense fallback for `N_child=O_rho(L')` is important. In the other branch, `N_child>L'` and hence `sigma=O_rho(log(N_child+2))`. Channel log precision is `E=O_rho(N_child+L')=O_rho N_child`. Therefore all hypotheses of the new subexponential patch theorem actually hold, even when the child is much smaller than its worst-case size bound.

Substituting the explicit patch exponent gives terms bounded by

    O_rho(L^(7/8) log(L+2)^(15/8)
          + L^(3/4) log(L+2)^(11/4)),

up to constant and lower-order terms. Each is `O_rho(L)` for all L>=1 after increasing the fixed constant. This is a genuine uniform bound, not a claim that log-star is constant. The child coefficient-MPO algorithm is deterministic exact rational arithmetic with certified analytic truncation, and its dimension and denominator costs were checked in the separate new-step audit.

Outer membership counts, child activity counts, propagation and final sampling multiply only a fixed number of `exp(O_rho L)` factors. There is no further warm-time descent. Taking per-prefix accuracy and failure budgets proportional to epsilon/n makes `L=O(log(n/epsilon))` for every allowed n and epsilon, not just inverse-polynomial epsilon.

The final sampler uses sequential coupling. At each actually reached history, fresh query randomness has its uniform failure bound. The next-bit kernel differs from the true conditional by good-estimate error plus failure probability plus coin-rounding error. Summing over n steps proves unconditional TV control. Globally conditioning on the event that all estimates succeeded is neither needed nor used.

## 7. Nearest prior and novelty boundary

- [Nelson et al., arXiv:2610.00548v2, Theorem 2.3](https://arxiv.org/html/2610.00548v2) already proves a much stronger deterministic marginal approximation for noisy discrete circuits above a noise-dependent depth. Its 2D runtime exponent depends on inverse noise per layer. With a Trotter step dt, `p=Theta(gamma dt)`: its threshold contains `log(1/p)` and its exponent diverges as dt tends to zero. It therefore does not directly prove the present fixed-physical-action statement. The polymer/log-sampling strategy remains prior.
- [Angrisani et al.](https://arxiv.org/html/2609.40174v2) already supplies coefficient regularity and sparse Pauli propagation. Its normalized-Hilbert–Schmidt and supplied/local-observable access guarantees do not themselves initialize the extensive boundaries or imply worst-case output-prefix accuracy.
- [Mackay et al.](https://arxiv.org/html/2609.27497v1) supplies the coordinatewise coefficient compression and arithmetic-model MPO recursion. The present use must retain growing width and pay rational bits; it is not a new underlying rank-filter technique.
- [Trivedi–Cirac, PRL 129, 260405](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.129.260405) already proves continuous-time sampling in a sufficiently high noise-rate regime. That rate threshold is different from waiting to a fixed sufficiently large accumulated action at any fixed positive ratio.
- Physical path resummation, hypercontractivity, Fourier heavy hitters, tensor-train interpolation, KP bounds and sequential log sampling are established tools.

The checked primary statements do **not** simply subsume the combined theorem. The closure is a substantive improvement over this project's preceding nonuniform log-star-recursive bound. However, this is not an exhaustive literature or priority clearance. Do not present it as a historical first or newly invented constituent method.

## 8. Exact diagnostic evidence

The new `check_warm_probe_closure.py` uses a rational noncommuting two-qubit Hamiltonian containing Y terms, positive product inputs/effects, and independent physical-matrix versus Pauli-coordinate calculations. It passes:

- 224 exact warm-boundary Taylor identities through order 6;
- 112 exact Walsh-attenuation checks;
- all 31 prefix-energy identities for four sign bits.

No physical value or purity oracle is used. The earlier exact gauge tests also pass redundant-bond, unreachable-direction, large cancelling-gauge and zero-tensor cases. These small checks supplement, not replace, the general proofs.

## Residual limits and delivery recommendation

No unresolved proof gap was identified in the revised restricted theorem. Remaining boundaries are substantial and must stay visible:

1. The unqualifying early/intermediate action interval remains open. A bounded interval at fixed rho_0 is not thereby classically easy.
2. The theorem is not uniform polynomial complexity in a growing coupling/noise ratio.
3. It does not cover arbitrary time dependence, nonunital noise, correlated initial states, higher arity without a new proof, or a practical end-to-end implementation.
4. Scientific priority is not established. Human expert review of this multi-source synthesis would be appropriate before an external theorem claim.
5. A deliverable should identify governing proof versions and mark superseded failed arguments clearly; old exploratory headers must not be mistaken for the current dependency state.

Within those boundaries, the reviewed result constitutes substantive theoretical research capital.
