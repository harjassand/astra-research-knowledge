# Finite-bit completion of the two-mode first-event compiler

31 October 2026. Mathematical candidate for independent review. No circuit implementation, novelty, or practical advantage is asserted. This is a binding completion of `METZLER_BRIDGE_FIRST_EVENT_COMPILER_CANDIDATE.md`, not a replacement for its exact dilation, majorant, or normalization proofs.

## 1. Contract and notation

There are exactly two bounded Hermitian noise operators, not necessarily commuting, and a bounded Hermitian H0. The damping representation starts with both ancillary qubits in their ground states, independently of the system and reference. System instruments occur at prescribed times; every external outcome is retained. Neither the damping ancillas nor any internal jump time is exposed to the consumer.

Write vi=sqrt(gamma_i lambda_i), ai for supplied operator-encoding normalizations, Gamma_i=gamma_i ai^2, and Gamma=sum Gamma_i. Positive rates and nonzero normalization parameters have finite descriptions. Zero couplings are handled explicitly below. Precision-capable controlled encodings, their implementation costs, and ordinary high-precision simulation of H0 are supplied and charged.

Let

    D = -i(H0 + sum vi Ai Xi) - 2 sum lambda_i Pi,
    K(t)=exp(Dt),                 Ji=2 sqrt(lambda_i) sigma_minus_i.

K is a contraction. Define bounds

    hE = ||H0|| + sum vi ai + 2 sum lambda_i,
    Lambda = 1 + 2||H0|| + 2 sum vi ai + 8 sum lambda_i.

Lambda bounds the diamond norm of the full Lindblad generator. Its potentially large numerical value enters the construction only through cutoff lengths and precision bits, not a number of time steps proportional to Lambda T.

Take windows of length at most 1/Gamma when Gamma>0, split additionally at every prescribed control time. Let W be their number, so W<=ceil(Gamma T)+p+1. When Gamma=0, use only the control-defined windows. A positive remaining duration is denoted tau.

The root constants are retained:

    alpha0(tau)=16 exp(Gamma tau/2),
    wi(t)^2=4096 exp(Gamma tau) [lambda_i exp(-4 lambda_i t)+Gamma_i],
    A=256.

For Gamma tau<=1, alpha0^2+sum integral_0^tau wi^2 < A^2. Padding with a zero good-block arm gives a fixed normalizer A.

## 2. A deterministic global call budget

The exact controlled dilation has the already derived count bound

    E exp(N_T) <= exp[Gamma T(e-1)].

Choose

    M = ceil(Gamma T(e-1)+log(100/epsilon))+1,
    S = M+W+2,
    e_step = epsilon/(100 S).

Then the exact probability of reaching the count cap is at most epsilon/100. Stop and use a fixed CPTP continuation on that event. This costs at most twice that probability in output trace norm. It does not assert a tail bound for the approximate simulator.

There are at most M event calls and W no-event calls before the deterministic cap. Introduce a remaining-window cutoff

    tau_min = min(T, e_step/(100 Lambda)).

A smaller positive remainder is advanced by identity to the prescribed window boundary, with error at most Lambda tau_min. Such an advance consumes a window, so it does not create an unbounded loop. If T=0 there is no evolution to compile.

All subsequent per-call estimates are uniform over tau in [tau_min,tau_max], where tau_max is the maximum prescribed window length. All logarithms of positive cutoffs below have polynomial bit length in the input, the physical resource bounds, and log(1/epsilon).

## 3. The complete first-event block, including its records

For arbitrary system/damping-ancilla input, not merely ground ancillas,

    K(tau)^*K(tau) + sum_i integral_0^tau K(t)^* Ji^*Ji K(t) dt = I.

Use independent uniform outer coordinates to select the no-event arm with probability alpha0^2/A^2, the event arm i with probability integral wi^2/A^2, and the padded zero arm otherwise. Within event arm i, use the explicit mixture whose density is wi(t)^2/integral wi^2. It is a mixture of a uniform time and a truncated exponential of rate 4 lambda_i. The component choice and uniform coordinate are retained as private records.

The operator amplitude in the no-event arm is K(tau)/alpha0. In an event arm it is Fi(t)=JiK(t)/wi(t). Thus the good block B, expressed on the common uniform-coordinate output space, satisfies B^*B=I/A^2. Recording the mixture component merely refines the private Kraus decomposition; summing over it gives the same physical first-event channel.

Inner matrix-entry and virtual-bridge random words are different: they must be unprepared to form the operator average. No outer branch, time, or mixture register is measured before complete-isometry amplification. All contraction/block-encoding work remains coherent until then.

The inner circuit selects the 16 damping-sector matrix units uniformly, computes their scalar coefficient, and uses a further uniform word for a Bernoulli acceptance. On rejection or a numerical/source failure, SELECT has zero good block. This avoids assuming an arbitrary amplitude-state-preparation oracle. Products of Ai/ai blocks use fresh success registers. Ordinary H0 propagators are inserted in chronological order. Unpreparing the inner seeds produces the required mean block.

## 4. Outer-time quadrature: common uniforms, not timestamp TV

A discrete timestamp distribution is not close in total variation to its continuous counterpart. No such claim is used. Embed each finite uniform bin as its normalized indicator in L2 of the continuous uniform coordinate. Compare operator amplitudes there, before tracing the private coordinate.

The following bounds give uniform finite-bit control. For Gamma_i>0,

    wi(t)>=64 sqrt(Gamma_i),
    |wi'(t)/wi(t)|<=2 lambda_i,
    ||Fi'(t)|| <= sqrt(lambda_i) hE/(32 sqrt(Gamma_i)) + 2 lambda_i =: Bi.

We used ||K'||<=hE and ||Fi||<=1, the latter following from its contraction LCU realization. The logarithm of Bi is input-bit bounded even when Gamma_i is small.

There is an essential zero-coupling exception to the preceding estimate. If Gamma_i=0, do not divide separate exponentially small terms. Exact factorization gives

    JiK(t)=2 sqrt(lambda_i) exp(-2 lambda_i t) sigma_minus_i tensor K_rest(t),
    Fi(t)=(1/32) exp(-Gamma tau/2) sigma_minus_i tensor K_rest(t).

Its derivative is bounded by the remaining effective-generator norm divided by 32. This cancellation prevents spurious exp(lambda_i tau) precision. An exactly zero jump rate has no event arm and is removed. Zero virtual couplings likewise have only the diagonal no-flip bridge.

For an exponential component with rate a=4lambda_i, its quantile is

    Q(u)=-log[1-u(1-exp(-a tau))]/a.

On u in [sigma,1-sigma],

    Q'(u)<=tau/sigma,
    min(Q(u),tau-Q(u)) >= c sigma min(tau,1/a)

for an absolute positive c. The uniform component has the same type of bounds. Evaluate the displayed expression using nonpositive exponentials and a stable log1p/expm1 implementation. No exp(+a tau) intermediate is needed.

Choose a small internal block-error budget beta, specified in Section 7, and sigma=beta^4. Exclude outer uniforms in the two tails of length sigma and narrow strips around outer arm/component thresholds. Since every normalized good-block amplitude is a contraction, their contribution to the L2 block error is O(sqrt(sigma)), not a conditional-probability assertion about accepted timestamps. Their contribution to the physical first-event isometry is at most A times this bound.

On the retained coordinates, event times lie in [t0,tau-t0], where one may take

    t0 = c sigma min(tau_min, 1/(1+4lambda_1+4lambda_2)).

Choose an absolute time error dt satisfying

    dt <= min(t0/10, beta/[100(1+B1+B2)], e_step/[100 Lambda]).

Uniform midpoints, certified threshold comparisons and quantile arithmetic then achieve this error with a number of bits polynomial in log(1/sigma), log(1/dt), log(1+lambda_i tau_max), and the input lengths. Outer arm/component probabilities need only absolute accuracy O(sigma); small positive component normalizers can be evaluated with their input-bit and tau_min-dependent guard precision. The zero cases are explicit.

The resulting outer good-block error is O(beta), uniformly over inputs. This is an operator-norm bound in the common L2 record space, not a claim about continuous-versus-discrete timestamp distributions. The representative finite timestamp is used only privately for subsequent remaining-window arithmetic; its effect on that continuation is accounted for in Section 8.

## 5. Uniform finite bridge source

For each nonzero virtual coupling, retain the root definitions

    omega_i=sqrt(lambda_i^2+gi^2),
    si=gi^2/(omega_i+lambda_i),
    di=omega_i+lambda_i,          nu_i=si+di.

The Doob chain has rates 0->1 equal si and 1->0 equal di. Its explicit transition matrix has nonnegative entries

    P01(t)=si/nu_i (1-exp(-nu_i t)),
    P10(t)=di/nu_i (1-exp(-nu_i t)),
    P00(t)=di/nu_i+si/nu_i exp(-nu_i t),
    P11(t)=si/nu_i+di/nu_i exp(-nu_i t).

On t>=t0, all entries have a common positive lower bound

    p0 = min_i c (si/nu_i) min(nu_i t0,1),

with c chosen conservatively, for example 1/4. Omit zero-coupling factors from this minimum. If none remain, there is no bridge sampling.

An unconditioned two-color path has at most 2 Poisson[(s1+s2)t]+2 virtual transitions under a standard dominating up-clock construction. Since (s1+s2)t<=Gamma tau_max/2<=1/2, its exponential count moment is bounded by an absolute constant. Endpoint conditioning divides probabilities by at most p0^2. Therefore a deterministic total virtual-event cap

    Kcap = ceil(C+log(1/(eta p0^2)))

has conditioned failure at most eta for a suitable absolute C. This cap is logarithmic in inverse endpoint probabilities, not proportional to lambda_i t.

Let q=max_i(si,di) and choose

    zeta <= min(t0/10, eta p0^2/[C(1+q+q^2 tau_max)]).

Unconditioned jump intensities are bounded by 2q. Poisson domination bounds the probability of an event within zeta of an endpoint, or any pair of events within zeta, by C(q+q^2 tau_max)zeta. Divide by the ORIGINAL endpoint probability product, at least p0^2. Thus the conditioned probability of these geometric bad paths is at most eta. This includes different-color coincidences and is indispensable for noncommuting operators.

On the good paths, every recursive remaining time is at least zeta. After a small accumulated numerical perturbation it remains at least zeta/2. A common denominator bound for every recursive transition kernel is therefore

    pz = min_i c (si/nu_i) min(nu_i zeta/2,1).

No recursively shrinking precision promise is required.

### 5.1 Actual holding-time acquisition

Given current state i, final state j and remaining duration t, the survival function before the first event is

    S(u)=exp(-q_i u) Pij(t-u)/Pij(t),       0<=u<t.

For i=j there is a separate no-event flag of mass exp(-q_i t)/Pii(t). Draw ONE uniform U. If U is at least 1 minus that flag mass, return the flag. Otherwise invert the FULL event CDF F(u)=1-S(u) using the SAME unrenormalized U and fixed-depth bisection. Do not divide by the potentially tiny event probability or introduce a conditionally rescaled uniform. Each evaluation uses only the displayed nonpositive exponentials, products, and divisions by Pij(t)>=pz. Never expand it into a product containing an exponentially large positive exponential.

There is no rejection loop waiting for an unlikely final endpoint. The complexity of absolute CDF accuracy eps_cdf is polynomial in input length, log(1/pz), log(1/eps_cdf), and log(1+q tau_max). Stable elementary series and cutoff of negligible negative exponentials suffice.

### 5.2 Changed recursive duration and ordering

On t>=zeta/2 the first-event density is

    q_i exp(-q_i u) P_(1-i),j(t-u)/Pij(t),

plus the separate no-event flag. Differentiating in t, integrating the density derivative, and including the moving-endpoint strip and flag derivative gives a total-variation Lipschitz constant bounded by

    L = C(1+tau_max)(1+q)^2/pz^2.

This follows directly from |P'|<=q, P>=pz, and integration of q exp(-q u). It is a distributional bound, not an inverse-density lower bound.

Choose each sampled waiting-time accuracy h so that

    h <= min(zeta/[10(Kcap+1)],
             eta/[C L(Kcap+1)^2],
             beta/[C(1+||H0||)(Kcap+1)^2]).

At step k, maximally couple the exact kernel at the exact remaining duration to the exact kernel at the rounded duration. Conditional on agreement, add the numerical waiting-time error at most h. The remaining-duration discrepancy is at most kh, and the sum of mismatch probabilities is at most C L Kcap^2 h. This is additive, not an exponential iteration of inverse-CDF derivatives.

For a fixed duration, a bisection depth J=O(log(1+tau_max/h)) suffices. Across all possible bisection branches there are at most 2^(J+1) CDF thresholds. Given the past, the new uniform is independent. Exclude strips of width eps_cdf+2^(-B) around those thresholds and the no-event threshold. Taking

    (eps_cdf+2^(-B)) 2^(J+1) <= eta/[C(Kcap+1)]

controls all ambiguous comparisons. Thus B and the CDF precision grow only linearly in J and logarithmically in Kcap/eta. This direct threshold argument avoids any hidden inverse-CDF Lipschitz assumption. Equivalently, monotone-quantile coupling gives E|Q(U)-Q(U_B)|<=tau_max 2^(-B), but it is not necessary to assume a positive density.

Good event times remain separated after rounding, and their cross-color chronological order is unchanged. Absolute event-time discrepancies are at most Kcap h. Replacing H0 propagation intervals in the selected word therefore changes it by at most C||H0|| Kcap^2 h; all Ai/ai blocks are contractions. Bad/capped/mismatched paths change the mean block by at most twice their probability. Taking eta a sufficiently small constant multiple of beta gives a uniform O(beta) inner operator-block error. Approximate H0 evolutions and supplied Ai block encodings to O(beta/(Kcap+1)) per selected factor. Every event sort, bit operation, bisection step and block query is included.

This proves the actual finite-word virtual holding-time source and its operator integration bound. It does not assert total-variation closeness of rounded event-time measures.

## 6. Finite circuit assembly

For each call with given finite tau:

1. Prepare finite uniform outer registers and compute the no-event/event/zero arm and, when applicable, its mixture component and representative time. Retain these registers coherently.
2. Prepare the 16-entry inner selector and the capped bridge random words. Compute scalar entry coefficients with certified arithmetic. Use uniform-threshold Bernoulli acceptance, selecting zero contraction on rejection/failure.
3. For an accepted entry, compute both conditional virtual bridges, sort their events, and SELECT the chronological H0 and Ai/ai product with its phase and damping-sector matrix unit. For a first-jump arm, compose the appropriate lowering matrix unit. Use fresh block-success work for products.
4. Reverse all INNER source arithmetic and seed preparations. The outer source registers and physical damping ancillas remain.
5. Apply known-success-amplitude oblivious amplification to the COMPLETE padded good block, then measure or retain the private outer records. Only now update the event counter and remaining window.

The entry coefficient for JiK is bounded by wi/16 using the root envelope. The no-event coefficient is bounded by alpha0/16. All real parameters are computed to absolute accuracies sufficient for the block budget. Uniform-threshold selection avoids assuming a free square-root amplitude-preparation oracle; required fixed amplification phases are synthesized with their gate cost paid.

## 7. Robust amplification and the per-call error

The ideal good block has B^*B=I/A^2 with A=256. A fixed-degree generalized amplitude-amplification sequence maps it to its complete isometry; a phase-adjusted final step permits the known amplitude 1/A. Its degree and all stability constants depend only on this fixed A.

For completeness, the robustness needed here is weak. The amplified good block is a fixed noncommutative block polynomial of the form B p(B^*B), with degree and coefficients determined only by A and the chosen amplification phases. If B differs from the ideal embedded block by at most beta in operator norm, telescope each product in this polynomial; all intermediate factors are contractions, so its operator-norm perturbation is O_A(beta). This directly controls singular vectors as well as values; a scalar singular-value derivative argument alone would not suffice. The failure norm is then O_A(sqrt(beta)) by unitarity and exact normalization of the target isometry. The total implemented isometry differs from the desired embedded isometry by O_A(sqrt(beta)), plus the synthesized-phase errors. No amplification of K alone is invoked.

Choose beta as a sufficiently small fixed fourth power of e_step; for example beta=(e_step/C_A)^4 for a sufficiently large absolute constant C_A depending only on A and the fixed amplification sequence. Choose all inner source and arithmetic constants above to deliver block error at most C beta, and all phase/unitary-synthesis errors at most e_step/C_A. The resulting isometry error is at most e_step/10 after increasing C_A if needed. These conservative powers only multiply log(1/epsilon) precision by a constant.

Outer tails contribute O(sqrt(sigma))=O(beta^2) before amplification. The retained-coordinate time perturbation contributes at most (B1+B2)dt<=beta/100. Threshold errors and ordinary gate errors are allocated similarly. Thus the claimed per-call bound includes every outer and inner source operation rather than presuming a Kraus oracle.

## 8. The global private-time hybrid

The event timestamp is private and used only to determine the remaining duration of the current window. It is not a freely observable output on which an arbitrary external controller may act. This restriction is essential.

A useful comparator is the EXACT count-augmented dilation, with the dynamics frozen after count M. Its Hamiltonian is controlled on count<M and its jumps are Ji tensored with the count shift. Their operator norms, hence the generator diamond-norm bound Lambda up to a fixed constant, are independent of M. The exact capped future is consequently Lambda-Lipschitz in the remaining duration of the current control-free window. After that boundary, all fixed prescribed controls and later channels are CPTP contractions.

Use a backward hybrid against this capped future. At a call, compare the ideal continuous first-event isometry and finite implementation in their common uniform-coordinate space. Their state error is at most twice the isometry error. On retained coordinates, replacing t by its representative changes the exact capped continuation by at most Lambda dt. On excluded coordinates use the already charged L2/isometry bound and channel contraction, not a timestamp-TV claim. A tiny remaining window is separately charged by Lambda tau_min.

This also avoids an uncapped-future/capped-algorithm mismatch: the future used in the hybrid is a genuine CPTP count-augmented process. The internal source record can be dephased after amplification for classical iteration; dephasing and tracing the private records are contractions. For the analysis only, a finite uniform bin is tensored with a fresh continuous residual coordinate, allowing its identification with a piecewise-constant function in the same L2 space. No such continuous register is implemented or exposed.

Over at most S calls, the total source/amplification/timing/cutoff error is bounded by a fixed multiple of

    S [e_step/10 + Lambda dt + Lambda tau_min],

which is less than the allotted epsilon fraction by the choices above. Add the exact initial-ground count-tail error at most epsilon/50 and the remaining gate/parameter budgets. Adjusting fixed numerical constants gives total unconditional output trace error at most epsilon. The bound is uniform over input references and prescribed system instruments; all external outcomes remain retained. The two damping ancillas are preserved between every event, no-event boundary, and system control.

## 9. Complexity and exclusions

Kcap, J, B, log(1/zeta), log(1/pz), and the outer quantile precision are polynomial in the encoded input lengths, log(1/epsilon), log(2+lambda_1 T+lambda_2 T), and logarithms of the physical resource bounds. Small nonzero couplings are charged through their actual description lengths; exact zeros use explicit factorizations. No positive exponential in lambda_i T is evaluated. All loops are event caps, bit-arithmetic loops, and bisection depths.

The actual call count is O(1+Gamma T+p+log(1/epsilon)). Within each selected virtual word, the H0 intervals have total duration at most tau. This pathwise fact does not by itself optimize a coherent implementation's gate count. A simple implementation simulates each of at most Kcap+1 variable-duration slots with worst-case bound tau, and is charged (Kcap+1) alpha_H0 tau plus its polynomial precision overhead. This remains inside the stated polynomial bound; no additive, optimized physical H0 cost is claimed without a separate variable-time implementation. Fixed 16-entry selection and fixed-A amplification multiply this by constants. All finite source registers can be prepared with ordinary uniform qubits, so this compiler does not require the earlier unlimited-path finite-independence argument.

Subject to the supplied precision-capable operator encodings and the root exact dilation/majorant proofs, this completion therefore targets a polynomial gate/workspace bound in

    1+alpha_H0 T+Gamma T+p,
    input/register lengths,
    log(2+lambda_1 T+lambda_2 T), log(1/epsilon),

with the operator-encoding costs paid. No optimal dependence, variable-number-of-modes efficiency, exposed jump-time approximation, experimental claim, or novelty claim follows. All statements in this completion remain candidates until its full argument is independently reviewed.
