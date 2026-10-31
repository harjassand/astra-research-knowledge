# Sharper complete first-event assembly: a paid high-rate refinement

Status: candidate for independent review. This is a replacement of three assembly bounds, not a modification of any frozen source theorem or resource audit. It retains the same high-rate fixtures, actual jump stack, count cap, window cap, private source memory, and prescribed controls. It is not a quantum gate backend, a practical crossover, or a new source family.

## 1. Received interfaces and unchanged scope

The received whole native compiler is `native_lyapunov_source_20261031/NATIVE_FULL_FIRST_EVENT_RECEIVING.md`, SHA256 f503c80089c85006856e6ca1ea8b536bb36e0aa4931db071320a33a056a07192, with whole receipt 0fa56f50ca5160cbbbe9dc51c360f2b34b9e9e301894dc49c9ce6288d8cafeed. We use its exact acquired operators and normalization, complete-reference error convention, conditional two-state source and finite arithmetic, and count-augmented private-clock hybrid. We do NOT replace its kernel by a free oracle.

After gap/time normalization, let Q<=H<=hQ, physical generator -i[TH0+cK/b,.]+mu G, c=sqrt(mu B), H= L†L/2, and acquired stack normalization alpha_L. The high-rate premise implies r=mu/2>=8c (the frozen fixture actually has much more slack). Let tau_max<=1/(128B), and retain the frozen count/window total call cap S. Positive B and mu are supplied; zero cases and the low-rate branch remain the frozen construction, not the formulas below.

Define delta=r-2c, nu=sqrt(delta²+8c²), d=(nu+delta)/2, s=2c²/d. Thus d-s=delta, d+s=nu. The exact positive word matrix is

    E(t)=exp([[0,c],[2c,-r+2c]]t) diag(1,2),
    E00=(d e^{st}+s e^{-dt})/nu,
    E01=E10=2c(e^{st}-e^{-dt})/nu,
    E11=2(s e^{st}+d e^{-dt})/nu.

Every virtual Hamiltonian insertion carries (-i), including QQ insertions; the source Q-dwell block is the acquired F(mu t)=Q exp[-mu t(H-Q/2)]Q/2, with its scalar factor 2 exp(-mu t/2) priced in E. Projected K/b blocks, actual jump L/alpha_L, retained physical source and colors, and all underlying synthesis costs are unchanged.

## 2. Rectangular complete-block amplification has linear local stability

Let B be the good block of ANY acquired unitary/isometry dilation with clean initial work, and suppose ||B-V/A||<=beta, where V†V=I and integer A>=1. The output space can be rectangular and include arbitrary reference registers and continuous private uniform coordinates. Put x=A beta<=1/4 and C=AB. All singular values of C lie in [1-x,1+x], so C has full column rank. Let U be its polar isometry, used only in the proof. Then

    ||U-C||=max_j |1-sigma_j(C)|<=x,
    ||U-V||<=2x.

Set theta=pi/(4A+2), attenuation a=A sin(theta), and d_A=2A+1. Since a<=pi/2 and actually a<1, the attenuation is an acquired contraction. The usual A oblivious Grover iterations on this ATTENUATED complete block have good singular amplitudes sin(d_A arcsin(a sigma_j(B))), with the same left/right singular vectors as B. This is the ordinary two-projector rotation identity; it does not require assumptions on the unitary dilation's other blocks. The ideal value is sin(d_A theta)=1.

For |epsilon_j|<=x, a sigma_j(B)=sin(theta)(1+epsilon_j). Since theta<=pi/6 and x<=1/4, the arcsine argument is at most 5/8. Its derivative is at most 1/sqrt(1-25/64)<1.282. Also d_A sin(theta)<=pi/2. Therefore

    |d_A arcsin(a sigma_j(B))-pi/2|<=3x.

The good block differs from U by at most (9/2)x², and its entire coherent failure component has norm at most 3x, by unitarity and the cosine of the same angle. Consequently the full amplified output isometry differs from V embedded in the good subspace by at most

    2x+(9/2)x²+3x < 7x <=32 A beta.

This includes coherent failures; it is stronger than a scalar singular-value derivative claim. No polar decomposition is implemented. Exact projector reflections are received operations. Numerical attenuation/reflection phases are synthesized so the SUM of their circuit operator errors is <=e_step/100, for example O(e_step/d_A) per repeated phase. Errors inside each base block are counted in beta, not charged again as arbitrary whole-dilation errors. This replaces the old global polynomial/O(sqrt(beta)) argument only near a COMPLETE isometry.

## 3. Positive endpoint weights remove uniform-arm padding

Define S0(t)=sum_{i,j} Eji(t) and S1(t)=E10(t)+E11(t). Prepare the four no-event endpoint arms with probabilities Eji(t)/S0(t), apply their endpoint-conditioned virtual word, and unprepare those endpoint/path source registers. The resulting no-event block is K0(t)/S0(t). This is ordinary positive LCU, not normalized postselection. At zero coefficients choose the zero arm explicitly.

For the event arm use the two initial-sector weights E1i(t)/S1(t), their conditioned words, followed by the ACTUAL acquired L/alpha_L. Its good block is J K0(t)/(alpha_L sqrt(mu) S1(t)). Pre-jump endpoint is Q; the post-jump source is not reset, and the jump-stack color remains an output. Projected sector blocks are real operators on the source, not fictitious rank-one sector reset gates.

For all t>=0,

    S1(t)=a e^{st}+b1 e^{-dt},
    a=2(c+s)/nu, b1=2(d-c)/nu>0,
    S0(t)=u e^{st}+v e^{-dt},
    u=(d+2s+4c)/nu, v=(2d+s-4c)/nu>0.

Positivity follows from d>=delta>=6c. S0(0)=3 and S0 is convex, so max_{0<=t<=tau_max} S0(t)²=max(9,S0(tau_max)²).

The exact event proposal density is

    w(t)=alpha_L² mu S1(t)²
        =alpha_L² mu [a² e^{2st}+2a b1 e^{-delta t}+b1² e^{-2dt}].

All three coefficients are nonnegative. The component label is retained as a PRIVATE orthogonal Kraus coordinate. Every component uses the SAME inner block J K0(t)/sqrt(w(t)), not division by its individual component density. At fixed t, component k therefore contributes sqrt(w_k(t)/w(t)) J K0(t); the squared weights sum to one. This preserves the physical instrument without unpreparing that outer label. Its mass on [0,tau] is explicitly

    I(tau)=alpha_L² mu [a² tau exprel(2s tau)
                       +2a b1 tau exprel(-delta tau)
                       +b1² tau exprel(-2d tau)],
    exprel(z)=(e^z-1)/z, exprel(0)=1.

This is a three-component truncated-exponential mixture, including a gently increasing exponential, not an assumed density oracle. Evaluate exprel and mixture weights with stable expm1/log1p or certified cutoff arithmetic. Positive growing exponent 2s tau is bounded by a constant on these windows. Decaying exponents beyond the precision cutoff are clipped with an explicit absolute error, rather than enumerating lambda-sized integers.

Let Zmax=max(9,S0(tau_max)²)+I(tau_max). Choose an integer A>sqrt(Zmax), using certified interval upper bounds (ceil of an upper bound plus one is sufficient). For each actual remaining tau<=tau_max use atom weight S0(tau)², event density w, and the nonnegative zero-arm remainder A²-S0(tau)²-I(tau). Distinct failure flags implement that zero arm. The resulting COMPLETE block is exactly V_tau/A, where

    V_tau† V_tau=K0(tau)†K0(tau)+integral K0†J†JK0 dt=I.

The outer time/type/uniform coordinate remains coherent through amplification. Only the inner positive LCU registers are unprepared. The exact squared normalizer remains O(1+alpha_L²), but the acquired finite sum above removes the very large uniform padding constants.

## 4. Aggregate virtual tail, not a rare-endpoint tail

Let Vword count every off-diagonal and QQ Hamiltonian insertion. Multiply every insertion weight by z=2, equivalently replace c by 2c in BOTH off-diagonal entries and the QQ diagonal addition. Let E_2, S0,2 and S1,2 be the preceding formulas with that replacement. The tilted fast decay is delta_2=r-4c>=r/2; all formulas and positivity remain valid. Define

    Z2max=max(9,S0,2(tau_max)²)
           +alpha_L² mu integral_0^{tau_max} S1,2(t)² dt.

The integral has the same three-exponential closed form. Each word is a contraction after removing its positive scalar weight. Dropping all words with Vword>K gives no-event operator error at most 2^{-K} S0,2(tau) and event error at most 2^{-K} alpha_L sqrt(mu) S1,2(t). Hence the WHOLE direct-sum first-event isometry block error is at most

    (sqrt(Z2max)/A) 2^{-K}.

There is no original endpoint probability in this inequality. Choose

    K=ceil(log2[8 sqrt(Z2max)/(A beta)])+2.

The discarded aggregate block norm is then <=beta/32. This bound concerns the weighted mean block, NOT a norm approximation of each conditional source state. It is therefore legitimate to have rare endpoint branches with large conditional overflow probability. Their word sampler runs to the fixed cap and selects the ZERO contraction on overflow, never resampling or pretending that their conditional tail is small.

The received exact Doob bridge still supplies all retained words: up/down rates s,d; QQ self-insertions are Poisson(2c times fast residence). Capped inverse-CDF recursion and finite Poisson CDF scans have polynomial cost in K and bit precision. If cap is exceeded at any stage the selected word is zero. In particular one need not generate all events to discover overflow. This is the algorithmic use of the aggregate estimate, not just a better formal tail bound.

## 5. Finite precision: endpoint rarity remains paid in arithmetic

Set e_step=epsilon/(1000 S), beta=e_step/(128A), eta=beta/10000, sigma=(beta/100)². Thus the sharp lemma charges <=e_step/4 for the base-block perturbation; phase errors and the existing count/clock/output budgets fit within the original generous per-step allocation. Beta's allocation includes the aggregate tail, finite inner means, endpoint weights, outer masses, and timing errors.

The exact conditional bridge is not replaced by an unpriced oracle. Retain the original bound Lphys=1+2Hs+2c+2mu alpha_L² and x_min=min(1,e_step/(100Lphys)); an actual remaining time shorter than x_min is advanced by identity with the counter-augmented error paid. For each of the three event-density components remove uniform endpoint strips of width sigma. Their contribution to the normalized outer isometry is <=sqrt(2sigma), not their probability alone. Three components are orthogonal mixture arms; even summing their separate norm bounds is O(sqrt(sigma)) with an explicit constant below ten.

All retained event times satisfy t,tau-t>=t0, where

    t0=(sigma/4) min(x_min,1/(1+2nu)).

For a decreasing truncated exponential rate at most 2nu, this follows from its density bound <=2nu+1/tau; the increasing component is its reflected version. Uniform limiting cases are treated directly. Inverse-CDF derivatives on retained uniforms are at most tau/sigma. With positive c, all four bridge endpoint probabilities are at least a certified downward-rounded

    p0 <= s t0/(1+nu t0).

We still pay log(1/p0) bits. It is removed from K, not from numerical precision.

Use qrate=nu+2c, and the original near-tie/boundary cut

    zeta<=min(t0/20,eta p0/[100(1+qrate+qrate²)]).

This includes both colors and QQ self-insertions. Before conditioning, dominating-clock probability bounds apply; after conditioning divide ONCE by p0. All other source changes below are measured uniformly on the retained input endpoints. On remaining durations >=zeta/2 set

    pz <= s(zeta/2)/(1+nu zeta/2),
    Lker=16(1+qrate)²/pz².

The received finite first-event atom/density formulas have TV duration Lipschitz constant Lker. Capped inverse CDF uses the same raw uniform for its no-event atom and its unconditioned event CDF, not division by a tiny conditional event mass. Fixed bisection comparison strips and Poisson-CDF error allocations remain eta/[100(K+1)²] or smaller. Self-insertion means change in TV by at most 2c times the duration error. K capped recursions add these errors, not multiply inverse-quantile derivatives.

Choose

    h_time<=min(zeta/[100(K+1)],
      eta/[100(1+Lker+2c)(K+1)²],
      beta/[100(1+Hs+mu(alpha_H+1))(K+1)²]).

This prices fast source-kernel time derivatives and crossing/order errors, not just H0. Each virtual insertion still has its (-i) phase. The finite uniforms and threshold arithmetic have bit lengths polynomial in log(1/pz), log(1/eta), K, log mu and acquired input lengths. A scan through the remaining K Poisson probabilities uses stable log probabilities and sends missing mass to overflow; it does not cost the untruncated Poisson mean.

For outer timing, nu<=mu under the high premise, so a>=2c/mu and alpha_L sqrt(mu) S1(t)>=2alpha_L sqrt(B). The normalized exact event operator J K0(t)/(alpha_L sqrt(mu) S1(t)) therefore has derivative bounded by the conservative

    Lout=1+nu+sqrt(mu/B)(Hs+c+mu h).

The acquired stack normalization cancels. The logarithmic derivative of S1 is bounded by max(s,d)<=nu. Set

    du<=min(t0/10,beta/[100(1+Lout)],e_step/[100Lphys]).

Endpoint-arm weights are computed at that numerical time using stable nonnegative E entries. To prepare their square-root probabilities, require total absolute probability error <=(beta/100)², and rotation errors <=beta/100. S0>=1 and S1>=2sqrt(B/mu); hence division costs logarithmic in mu/B, not inverse-probability repetitions. The same squared probability tolerance applies to outer mixture/atom weights. Approximate probabilities are normalized with a nonnegative remainder, not allowed to give invalid amplitudes. Positive growing exponentials are bounded; tiny decaying terms use certified clipping.

Every operator encoding, reflection, local Hamiltonian piece, arithmetic primitive and controlled rotation receives beta/(10^4 N_op), where N_op is the ACTUAL capped primitive-call count for the chosen finite circuits. Kernel LCHS/SVA internals further subdivide their tolerance. The ledger below does not pretend N_op equals K+1: its kernel bit column is only a necessary floor. An explicit circuit implementation must instantiate those remaining counts.

## 6. Complete process and execution costs

Couple continuous exact and finite outer time sources by a COMMON retained uniform coordinate and compare L² Kraus amplitudes. Continuous versus discrete timestamp TV is not used. Private time only selects continuation up to the next prescribed instrument boundary. The exact counter-augmented future channel is Lphys-Lipschitz in the remaining duration, which prices the du change even near the physical count cap. Numerical failures and caps remain CPTP; physical source and jump labels persist between calls. Artificial records are not consumer outputs.

The count cap and window cap are unchanged, so sum of at most S per-step errors plus the unchanged physical overflow and short-window budgets obeys the same final full controlled-process error convention as the received compiler. Arbitrary joint initial states, retained references, prescribed instruments and their actual costs are unchanged. No statement about arbitrary consumer access to artificial timestamps is made.

Each complete call uses d_A=2A+1 base calls, K+1 padded fast/H0 interval slots, and the actual finite source/LCU circuits. Every variable interval is implemented by binary fixed-time controlled simulations; charge each slot its worst local window, not a realized-path duration. All LCHS, coupling, jump-stack, arithmetic, source-reflection, and instrument costs remain paid. The refinement removes padding, not the kernel's real complexity.

## 7. Same-fixture diagnostic ledger and stopping boundary

`sharp_ledger.py` recomputes the SAME n=4,8,16, epsilon=10^-2/10^-4, lambda threshold through10^24 fixtures as the frozen ledger, using mpmath 90-digit interval arithmetic. Counts and windows are inherited unchanged. Caps round up, tolerance and endpoint bounds down; A is ceil(sqrt(certified Zmax))+1. New JSON is separate; no old file is overwritten.

At n4/epsilon.01, A=8, degree17, K=44, S=4151 and padded kernel-slot proxy=3,175,515, versus frozen 3.12–3.26 billion. At n16/epsilon.0001, A=14, degree29, K=55 and proxy=73,844,904, versus frozen 80.6–83.3 billion. These are neither gates nor lower bounds. Numerical precision is still substantial; all expensive primitive implementations remain uncounted.

The ordinary small dense solver and effective model already beat the frozen construction on its n4 test, and this revised stage proxy does not overturn that fact. The same generic stack action and classical trajectory count remain listed for scope, not as directly comparable gate counts or lower bounds. No quantitative crossover or practical advantage follows without complete costs on both sides. The useful algorithmic result, if independently checked, is that complete-isometry conditioning and aggregate word mass eliminate an avoidable roughly thousandfold padded stage overhead on these exact fixtures. It does not establish a new physical capability by itself.
