# Binding finite-bit completion for a variable number of telegraph modes

31 October 2026. Candidate for independent mathematical review. No implementation, optimal cost, practical advantage, or novelty is asserted.

This note completes `FACTORIZED_MANY_MODE_EXTENSION_CANDIDATE.md`. It preserves, without changing scope, the separately reviewed two-mode source `FINITE_BIT_FIRST_EVENT_COMPLETION.md`, SHA-256 `794534e9852ac931dfbbe0b2c19a75159e50f80eaf53f472b5cb2850993294b0`. The exact damped-ancilla representation and jump-count MGF are premises at their proved scopes. The extension below must be reviewed separately.

## 1. Target and scalar normalizers

There are r independent telegraph modes, r a finite input parameter, bounded Hermitian operators A_i, and H0. Different A_i need not commute. Their precision-capable controlled block encodings, normalizations a_i, and costs are supplied. The initial damping ancillas are all ground and independent of the system/reference. External instruments occur at prescribed times and cannot inspect damping ancillas or internal event records.

Put v_i=sqrt(gamma_i lambda_i), Gamma_i=gamma_i a_i^2, Gamma=sum Gamma_i, and g_i=v_i a_i. The positive virtual-path majorant factors as

    E(t)=tensor_i E_i(t),   E_i(t)=exp(M_i t),
    M_i=[[0,g_i],[g_i,-2lambda_i]].

Use control-free windows of length at most 1/(4r Gamma) when Gamma>0, and split at prescribed controls. The number of windows satisfies W<=ceil(4r Gamma T)+p+1. For Gamma=0 the physical ground-source system evolves only under H0 and its controls and can be compiled directly; the factorization statements below also have explicit zero-coupling cases.

For a fixed window tau define

    c_i=exp(Gamma_i tau/2)(1+sqrt(Gamma_i tau/2)),
    C=product_i c_i.

Every row and column sum of E_i(t), 0<=t<=tau, is at most c_i. Indeed, with omega_i=sqrt(lambda_i^2+g_i^2) and s_i=omega_i-lambda_i,

    (E_i)00 <= exp(s_i t),
    (E_i)01 <= min(g_i t,g_i/(2lambda_i)) exp(s_i t)
             <= sqrt(Gamma_i t/2) exp(Gamma_i t/2),

and (E_i)11<=(E_i)00. Consequently

    C <= exp(Gamma tau/2+sqrt(r Gamma tau/2))
      <= exp(1/8+1/sqrt(8)) < 1.62 < 2.

The fixed no-event normalizer is R=2. Outward approximations of c_i can be chosen with sufficient slack to preserve C<2.

For an actual jump of color k, define

    F_k(t)=tensor_{i!=k} E_i(t) tensor B_k(t),
    B_k(t)=2sqrt(lambda_k)|0><1| E_k(t).

This is the nonnegative matrix majorizing J_kK(t). Use the squared envelope

    w_k(t)^2=4096 exp(Gamma tau)
             [lambda_k exp(-4lambda_k t)+Gamma_k].

Let z_k(t)=w_k(t)/4. The row and column sums of B_k are at most z_k: the sum of its only nonzero row is at most

    2 exp(Gamma tau/2)[sqrt(Gamma_k)+sqrt(lambda_k)exp(-2lambda_k t)]
    <=2sqrt(2) exp(Gamma tau/2)sqrt(Gamma_k+lambda_k exp(-4lambda_k t)),

whereas z_k has coefficient 16. Thus the product factor bound

    C_k(t)=z_k(t) product_{i!=k} c_i

is less than w_k(t)/2. Both normalizations have substantial slack.

For lambda_k=0 remove the zero event arm. For Gamma_k=0 and lambda_k>0, analytically cancel the shared exp(-2lambda_k t) in B_k/z_k; its only nonzero normalized entry is exp(-Gamma tau/2)/8. Never divide two separately underflowed exponentials.

## 2. Actual left and right isometries

First consider E(t). In a common endpoint workspace denote output endpoints by j and input endpoints by i. The right isometry on physical input i prepares accepted amplitudes

    R_E |i> = sum_j sqrt(E_ji/R) |j,i,good> + right-failure terms.

The left isometry on physical output j prepares

    L_E |j> = sum_i sqrt(E_ji/R) |j,i,good> + left-failure terms.

The failure spaces are disjoint: an OR of local failure bits sets a global tag RFAIL on the right and LFAIL on the left. SELECT preserves these tags and has zero good block there. They therefore contribute no unwanted overlap. Endpoint strings are never measured.

These isometries are built, not assumed. For each right endpoint bit i_l prepare its two possible j_l with probabilities (E_l)_(j_l,i_l)/c_l, with a third failure outcome. The left preparation uses row probabilities (E_l)_(j_l,i_l)/c_l. Local preparations factor across l. Append a global success flag of probability C/R on BOTH sides. Accepted amplitudes are exactly those displayed because the product of local factors contributes sqrt(E_ji/C). Their failure probabilities are nonnegative by the row and column bounds. The old endpoint is copied in its computational basis into the common workspace by a reversible isometry; this preserves arbitrary quantum superpositions and is not a measurement or cloning of arbitrary states.

For F_k, use the same construction with B_k/z_k on bit k and E_l/c_l on the other bits, then a global flag of probability C_k/w_k. It yields accepted amplitudes sqrt((F_k)_ji/w_k). The right side prepares OUTPUT bit j_k=0 when accepted; the left side has no accepted term for j_k=1. The virtual bridge, however, ends at the PRE-jump bit 1. Both sides compute the same pre-jump endpoint string j_pre, obtained from j by setting bit k to 1. The subsequent overlap implements the lowering matrix unit, not a bridge ending at 0.

All local vectors have at most three amplitudes. To prepare them with uniform absolute error z, compute their probabilities to O(z^2), clip to nonnegative values and normalize the resulting constant-dimensional vector. Its Euclidean error is O(z), by |sqrt(x)-sqrt(y)|<=sqrt(|x-y|). Sequential rotations may ignore a residual branch of mass O(z^2); otherwise its denominator is bounded below by that quantity. This pays only O(log(1/z)) bits and avoids division by an exponentially tiny residual probability. At zero coupling, use the analytic normalized formulas above. Computing entries of E_i uses bounded positive exponentials exp(s_i t), negative exponentials and stable expm1; s_i t<=Gamma_i tau/2. No exp(lambda_i t) intermediate is required.

Choosing each local preparation error at most beta/(C r) makes the error of the product isometry O(beta) by unitary/isometry telescoping. This accounts for local clipping separately from the relative bridge-error bound below. Product and global-flag probabilities are evaluated with corresponding guard precision. Work registers are included and uncomputed.

## 3. Matching the SAME bridge seed on both sides

Conditioned on a common endpoint pair (i,j_pre), append on BOTH preparation sides the identical uniform finite-word register. Compute exactly the same capped bridge routine and its classical path/transcript into additional registers. On accepted branches this defines identical seed/path basis vectors on both sides. SELECT leaves these labels untouched and applies the chronological normalized system word, its (-i)^number_of_flips phase, and ordinary H0 evolutions. Product block encodings use fresh success registers and are projected only in the final good block.

For each endpoint pair, the overlap therefore equals

    (E_ji/R) E_seed[normalized chronological operator word]

for no event, and the analogous (F_k)_ji/w_k expression for a first jump. The result is K(t)/R or J_kK(t)/w_k(t), respectively. There is no summation circuit enumerating 2^r endpoints. The isometry inverses remove the INNER source words and path transcripts. The OUTER first-event label and time words are retained; those are different registers.

Incorrectly using different seeds on the two preparation sides would multiply independent averages instead of integrating the desired operator word. Incorrectly using j_k=0 as the pre-jump bridge endpoint would implement a different matrix. Both identifications are mandatory.

## 4. Weighted Schur control, without an exponential entry count

Suppose every endpoint-conditioned bridge word mean has operator-norm error at most eta. Then its unnormalized matrix-of-operators error has entries bounded by eta E_ji. For a vector with system components psi_i,

    ||(Delta psi)_j|| <= eta sum_i E_ji ||psi_i||.

The scalar Schur bound gives

    ||Delta|| <= eta sqrt(max_row_sum(E) max_column_sum(E)) <= eta R.

Consequently the normalized no-event block error is at most eta, independently of the number of endpoints. The identical argument with F_k and w_k proves the event-block bound.

This relative entrywise estimate is used ONLY for bridge/source-word errors. Absolute errors in preparing tiny endpoint amplitudes are instead bounded by the isometry-telescoping estimate in Section 2. They are not incorrectly assumed to have a relative bound. Combining these two controls gives a polynomial-r finite-precision block encoding.

## 5. Uniform many-mode bridge caps and arithmetic

The fixed-r finite source proof is used with explicit r-dependent budgets, as follows. The Doob rates are s_i and d_i=omega_i+lambda_i, with nu_i=s_i+d_i. Zero virtual couplings have a deterministic no-flip path and are excluded from probability denominators.

After outer-coordinate tail exclusions, all bridge durations t are at least t0>0. For each active color choose

    p_i = c(s_i/nu_i) min(nu_i t0,1),
    P0 = product_active_i p_i,
    q = sum_active_i max(s_i,d_i).

Each positive p_i is a lower bound on every endpoint transition probability for that color. Its logarithmic inverse has polynomial input and cutoff bit length. Although P0 can be exponentially small in r, log(1/P0)=sum_i log(1/p_i), which is polynomial in r and those bit lengths. Products are evaluated with outward certified bounds; their binary representations do not require exponentially many bits.

Before conditioning, the total virtual transition count is bounded by

    r + 2 Poisson((sum_i s_i)t).

Here (sum_i s_i)t<=Gamma tau/2<=1/(8r). An exponential Markov bound therefore gives a total virtual cap

    Kcap = O(r+log(1/eta)+log(1/P0)).

Endpoint conditioning divides probabilities by at most P0. This is used only to choose precision/caps; no rejection sampler waits for a rare endpoint. Source loops may allocate Kcap slots per color, costing O(r Kcap), but a global counter selects zero good block if the total cap is exceeded.

Choose

    zeta <= min(t0/10, eta P0/[C(1+q+q^2 tau_max)]).

Poisson domination of total event intensity bounds near-endpoint and near-coincident event pairs, before conditioning, by C(q+q^2 tau_max)zeta. This includes every cross-color pair. Divide by P0. Thus the conditioned bad-path probability is at most eta, and the order of noncommuting insertions is stable away from this set.

For every recursive first-event kernel, remaining duration is then at least zeta/2 after small errors. Define

    pz = min_active_i c(s_i/nu_i) min(nu_i zeta/2,1),
    L = C(1+tau_max)(1+q)^2/pz^2.

The first-event survival function remains

    exp(-q_i u) Pij(t-u)/Pij(t).

Use ONE raw uniform to select the no-event atom or invert the FULL event CDF 1 minus that survival function. Do not renormalize by a possibly tiny event probability. Certified bisection uses nonpositive exponentials and division only by the priced endpoint denominator. Its bit cost is polynomial in log(1/pz), log(1/error), log(1+q tau_max), and input lengths.

The derivative-in-duration argument in the fixed-r completion gives TV Lipschitz constant L for each kernel, including its no-event flag and moving support. Choose waiting-time error

    h <= min(zeta/[10(Kcap+1)],
             eta/[C r L(Kcap+1)^2],
             beta/[C(1+||H0||)(Kcap+1)^2]).

Couple exact kernels at true and rounded durations stepwise. The duration mismatch after k steps is at most kh, and the total distributional mismatch is at most C r L Kcap^2 h. Fixed-depth CDF bisection comparisons are protected by a union over their finite possible thresholds; J=O(log(1+tau_max/h)) levels require only O(J+log(rKcap/eta)) additional arithmetic/uniform bits. No lower density or inverse-CDF Lipschitz premise is needed.

Bad, capped, or mismatched bridge paths cost at most twice their probability in the operator mean. On good paths the same color order is preserved, and the H0 word changes by at most C||H0||Kcap^2 h. Per-factor block/gate errors are allocated O(beta/(Kcap+1)). Thus eta a small multiple of beta yields the uniform endpoint-word error needed by Section 4.

The precision may be very fine numerically, but all logarithms above are polynomial in r, encoded inputs, and target precision. No loop is proportional to 1/P0, 1/zeta, q tau, or any switching count.

## 6. Complete first-event normalization and outer source

The no-event block uses R=2. For events, retain the envelopes w_i from Section 1. Their total squared mass is

    4 + sum_i integral_0^tau w_i(t)^2 dt
      <= 4+4096 exp(Gamma tau)[r/4+Gamma tau] = O(r+1).

Choose an integer power of two A satisfying

    256 sqrt(r+1) <= A < 512 sqrt(r+1).

Pad with a zero good-block arm to that exact known normalizer. Prepare the outer arm by uniform thresholds with probabilities 4/A^2 and integral wi^2/A^2, and the remaining zero probability. Compute the r weights by finite arithmetic and a linear cumulative scan, or a controlled tree; its O(r) cost is paid. Each conditional time source is still a uniform/truncated-exponential mixture. Retain the outer uniforms, component, color and time record until amplification is complete.

Let e_step=epsilon/(100S), with S specified below, and d=2A+1. A conservative block budget is

    beta = (e_step/(10^6 d^2))^4,
    sigma = (beta/(100 A(r+1)))^4.

All local/isometry/source budgets above are chosen as small fixed fractions of beta. Exclude outer uniform tails and threshold strips of width sigma. There are only polynomially many such thresholds, and the L2 block error from their union is O(sqrt(poly(r)*sigma)), less than the allocated beta. This is a common-uniform isometry comparison, not TV between continuous and finite timestamps.

For Gamma_i>0 the normalized amplitude Fi=JiK/wi obeys

    ||Fi'|| <= sqrt(lambda_i) hE/(32sqrt(Gamma_i))+2lambda_i,
    hE=||H0||+sum_i v_i a_i+2sum_i lambda_i.

For Gamma_i=0 use exact cancellation

    Fi(t)=(1/32) exp(-Gamma tau/2) sigma_minus_i tensor K_rest(t),

whose derivative has no positive exponential in lambda_i t. On retained uniforms, the truncated-exponential quantile has derivative at most tau/sigma, and both endpoint distances are at least c sigma min(tau,1/(4lambda_i)). Uniform components satisfy the corresponding simpler bound.

Thus one uniform bridge-duration floor is

    t0=c sigma min(tau_min,1/(1+4sum_i lambda_i)).

Choose representative outer-time error dt no greater than t0/10, beta divided by a sufficiently large polynomial multiple of 1+sum_i||Fi'||, and e_step/(100 Lambda). This requires only polynomial bit precision. It bounds both the normalized-amplitude error and the later private-duration error. Small positive mixture normalizers are evaluated with their priced input/tau_min guard precision; exactly absent components are handled directly.

## 7. Polynomial-r amplification robustness

The ideal padded good block B satisfies B^*B=I/A^2. The normalizer is no longer constant. The following explicit amplification avoids using a hidden fixed-A stability constant.

Let m=A, theta=pi/(4A+2), and c=A sin(theta). Since c<pi/4<1, a known flag rotation can attenuate the entire good block to C=cB. The ideal success amplitude is sin(theta). Exactly m STANDARD oblivious Grover iterations amplify it to unit success because

    (2m+1)theta=pi/2.

This uses O(A)=O(sqrt(r+1)) base calls and reflections. The attenuation rotation is synthesized with its precision/gate cost paid. Reflections act on designated source/success work, not on the unknown system or physical damping state, and require only polynomially many elementary gates.

There is an explicit polynomial operator robustness bound. For a rectangular contraction C, introduce its selfadjoint block dilation

    H_C=[[0,C],[C^*,0]].

The amplified good block is, up to a fixed sign, the off-diagonal block of T_d(H_C), d=2A+1. For selfadjoint contractions X,Y, write Delta=X-Y. The Chebyshev recurrence gives

    T_d(X)-T_d(Y)
      = U_(d-1)(X) Delta
        +2 sum_(k=1)^(d-1) U_(d-1-k)(X) Delta T_k(Y).

Since ||T_k(Y)||<=1 and ||U_j(X)||<=j+1, its norm is at most d^2||Delta||. This is a noncommutative product identity; it controls operator directions as well as singular values. Therefore a base-block error beta causes amplified good-block error O(d^2 beta). Unitarity and normalization of the target isometry bound the failure norm by O(d sqrt(beta)).

The beta chosen in Section 6 makes these errors smaller than e_step after allocating the polynomial-r local constants. Approximate attenuation/phases and all O(A) base calls have their synthesis error apportioned accordingly. The required precision is logarithmic in 1/beta, hence polynomial in r and logarithmic target precision. No constant-A assumption or exponentially expensive amplitude amplification is hidden.

## 8. Count/window caps and private remaining time

The exact actual-jump MGF is unchanged:

    E exp(N_T)<=exp[Gamma T(e-1)].

Take M=ceil(Gamma T(e-1)+log(100/epsilon))+1 and S=M+W+2. The exact count-cap error is O(epsilon); no tail is assumed for the approximate implementation. At most S first-event/no-event calls occur. Use

    Lambda=1+2||H0||+2sum_i v_i a_i+8sum_i lambda_i,
    tau_min=min(T,e_step/(100Lambda)).

Tiny remaining windows are advanced to their fixed boundary by identity with charged error Lambda tau_min.

As in the fixed-r completion, compare against the EXACT count-augmented Lindblad process frozen at count M. Its Hamiltonian is controlled on count<M and its jumps are Ji tensored with the count shift. Its generator norm is bounded by Lambda up to a fixed constant, independently of M and the Hilbert-space dimension. Thus its capped future is Lambda-Lipschitz in the remaining duration of the current control-free window. Later prescribed controls and channels contract.

Use the same outer uniform coordinates to compare ideal and finite first-event isometries, then charge representative-time changes inside the capped future by Lambda dt. On removed coordinates use the L2/isometry budget. There is no diamond-norm approximation claim exposing a finite timestamp as an approximation to a continuous timestamp. The private records are measured or retained only after amplification, then used solely for internal iteration. Physical damping ancillas are never reset at no-event or control boundaries.

A backward hybrid through at most S calls sums the per-call isometry error, Lambda dt, and Lambda tau_min. Together with the exact count-cap bound and the allocated gate/source budgets, this gives unconditional controlled-output trace error at most epsilon. It is uniform over references and all prescribed system instruments with their outcome records retained. Arbitrary consumer functions of private jump times are outside scope.

## 9. Explicit cost accounting and conclusion

There are O(1+r Gamma T+p+log(1/epsilon)) calls. Each uses O(sqrt(r+1)) base calls for amplification. Row/column preparation costs O(r) constant-dimensional preparations plus polynomial bit arithmetic, without endpoint enumeration. Bridge generation uses at most O(rKcap) padded sampling slots; sorting Kcap colored events can use any reversible polynomial-size sorting network. Time and color registers, source words, and all uncomputation are included.

If only individual A_i encodings are provided, a selected-color application can use a linear scan of all r controlled encodings. Charge the sum of their gate costs (or r times the maximum), not a free SELECT oracle. Each selected word has at most Kcap insertions. For H0, a simple coherent implementation charges (Kcap+1) times the cost of simulating a duration bounded by tau, rather than inferring an optimized additive time cost from a pathwise sum of interval lengths. Supplied encoding precision is chosen uniformly for these polynomially many operations.

Concretely, encode a duration by B binary fractional bits relative to a fixed known enclosing bound tau_max (or T). Apply the B controlled fixed-time evolutions exp(-i H0 tau_max/2^k), with the ordinary per-piece error allocated as the slot budget divided by B. Rounding to this time grid is included in the timing budget. This realizes a coherent variable-duration evolution without a free preprocessing table over 2^B durations. Charging every slot at the enclosing bound, rather than its particular remaining tau, is an allowed looser polynomial bound; all B controls and precision overhead are paid.

The total bounds are therefore polynomial in

    r, 1+alpha_H0 T+Gamma T+p,
    encoded input and register lengths,
    log(2+sum_i lambda_i T), log(1/epsilon),

with the supplied operator-encoding costs included. This bounds simulator overhead, not the implementation complexity of arbitrary consumer instruments: operations at the p prescribed control slots are external, or their actual implementation costs must be added separately. The uniform controlled-process error guarantee over these instruments is unchanged. Every potentially very small probability appears only through its logarithm in caps/precision, never as an expected rejection count. This is a candidate mathematical-existence theorem for variable r. Its validity rests on the explicit isometries, weighted Schur estimate, finite source/clock comparison, and polynomial amplification argument above; none may be replaced by an assumed Kraus or time-ordered noise-frame oracle.
