# Finite release into a separate output memory, without resetting the retained source

31 October 2026. Unreviewed companion to FINITE_RATE_COHERENT_ERASER_CANDIDATE.md. This closes a specific output-time gap conditional on explicitly supplied tunable receiver and SWAP/isolation services. It is not a claim those services have been built or calibrated. The stronger ordinary telegraph receiving below is credited; the generic all-selected amplitude theorem is not forced into a case where the exact ordinary calculation wins.

## 1. Why tracing the source at T is not itself release

The continuing source/cavity remains correlated with the data and keeps interacting. A small reduced-channel error at T cannot be composed as though that environment was reset for the next noncommuting gate. We instead specify a physical handoff:

1. Run the commuting phase service for time T with the actual source and finite receiver.
2. During an additional interval t_sw, ramp the receiver's data-conditioned shift chi(t) from k/2 to zero, keeping |chi(t)|<=k/2. Source coupling and loss remain ON. All other parameter/control changes must be in the actual model or a supplied residual budget.
3. Once the receiver is DATA INDEPENDENT, perform a source-blind SWAP of the data D into a separate memory M in finite time tau. The original source still couples to Z_D, not to M directly. The downstream receiver may retain its state and continue processing the source field.
4. Turn off the intended D-M gate coupling. M must thereafter have no uncharged coupling to the original source, D, cavity, controller or their output fields. Its own continuing noise over the desired holding/consumer interval has an explicit budget.

The source, old data and receiver may remain arbitrarily correlated with M at the end. If no subsequent coupling to M remains, later trace-preserving evolution on that old apparatus cannot alter M's reduced state. Thus the physical isolation condition, not a fictitious reset, licenses the output channel.

An ideal SWAP does not require a pure initial M state: it moves the old D state to M and moves M's old state to D. A real swap/isolation service must cover its actual input-state range, reference correlations and imperfections. If a cold new memory is assumed by its implementation, its preparation is paid separately.

A tunable chi-off operation is a NEW explicit control requirement. If the physical receiver has fixed non-switchable dispersion or tuning changes the source/port model uncontrollably, this handoff is not earned. This is not permission to switch off the unwanted source coupling; that coupling remains on throughout.

## 2. Conservative finite ramp bill

In the coherent comparator with arbitrary real |chi(t)|<=k/2,

    alpha_+'=-(k/2+i chi(t))alpha_+ +2ib sqrt(eta k_e),
    alpha_- = alpha_+^*,
    (log f)'=-8b^2-2i chi(t)alpha_+^2.

Starting from cavity vacuum, the amplitude inequality gives |alpha_+|<=4b sqrt(eta k_e)/k, so |alpha_+|^2<=16b^2/k. Since |f|<=1 for the actual coherent channel,

    |f(T+t_sw)-f(T)|<=24b^2 t_sw.                    (R1)

This deliberately conservative bound charges emission, field/cavity evolution and deterministic phase during the switch. The finite-source coherent overlap must be recomputed at T+t_sw, not left at T. With R_const>=|1-f_coh(T)|, use

    R_release=R_const+24b^2 t_sw,
    delta=1-a(T+t_sw)^2,
    epsilon_before_swap<=R_release+2delta+2sqrt(2delta R_release).

A direct coherent-amplitude propagation for a fully supplied ramp can be stronger; no particular perfect shape is assumed here. Residual chi after the ramp is not ignored: it must be separately received as an actual interaction or covered by the full implemented-control error budget. The switch slope/slew and hardware bandwidth are paid; the absence of a proof variation penalty does not supply them.

## 3. Exact source-blind SWAP receiving with the ACTUAL initial correlations

After chi=0 the downstream cavity/field operation is data independent. By the unidirectional network ordering it is the same postprocessing isometry on retained environment and future source-output field for actual and ideal SWAP comparisons. It can therefore be ignored for the output-memory norm bound without resetting it. Its initial correlations are allowed. The source input field remains the initialized vacuum Markov port.

Let rho be the actual joint source and D,M,reference state at the start of SWAP, including any source/data correlations from the preceding layer. Define

    R(t)=Tr_source rho(t),   Y(t)=Tr_source[X_s rho(t)],
    K=c X_s Z_D,             r=lambda/2.

For ANY bounded source-blind target Hamiltonian H0(t) implementing SWAP, the exact closed moment equations are

    R'=-i[H0,R]-ic[Z_D,Y],
    Y'=-i[H0,Y]-ic[Z_D,R]-rY.

They follow from G*X_s=-rX_s and X_s^2=I; no elimination or reset is used. In the target interaction picture, R(t) remains a positive normalized state. Hence

    ||Y(t)||_1 <= exp(-rt)||Y0||_1+(2c/r)(1-exp(-rt)),
    ||R(tau)-R_ideal(tau)||_1
      <=(2c/r)||Y0||_1+4c^2 tau/r.                  (R2)

All identities and norms include an arbitrary reference. For positive source-block density rho=[[A,B],[B^dagger,D]], the off-diagonal block satisfies ||B||_1<=sqrt(Tr A Tr D). Thus

    ||Y0||_1<=2sqrt(p0(1-p0))<=2sqrt(p0).

The actual preceding diagonal operation and chi ramp retain the exact source energy bound p0<=4b^2/lambda. Therefore, with c=sqrt(lambda)b,

    epsilon_SWAP_source <=16b^2/lambda+8b^2 tau.      (R3)

This is a complete trace-distance bound for the actually reachable initial joint family. It is not a source-state-independent reduced map silently composed after a trace. Applied for every data/reference input of the full preceding process, triangle inequality yields the complete input-to-released-memory channel bound. Known source/data correlations are explicitly received through p0 and Y0.

For an exact implementation, H_SWAP=(pi/(2tau)) SWAP_D,M realizes SWAP up to a global phase. Equivalently its nontrivial two-body Pauli couplings have coefficient pi/(4tau) in XX+YY+ZZ. Those control strengths, finite gate errors, control switching and output isolation are genuine supplied resources. No source-conditioned gate is required. Source-blind controls may be complicated without changing (R2), but their actual implementation error is not zero by declaration.

## 4. Full released-operation budget and scope

If epsilon_impl bounds all extra preparation, finite ramp/control errors, SWAP implementation and post-SWAP isolation/holding errors over their actual exposure intervals, a sufficient complete error is

    epsilon_release <= R_release+2delta+2sqrt(2delta R_release)
                       +16b^2/lambda+8b^2 tau+epsilon_impl.   (R4)

All parameters and exposure lengths are paid. This is not a promise of a noiseless indefinite memory. For the declared example lambda4096,b=1/5,k128,zeta0.998001,T1, choose t_sw=1/10000 and tau=1/1000. The switch starts at chi64 and reaches0; its average required slope is640000 in these units. The two-body SWAP coefficients are pi*250. With a SUPPLIED epsilon_impl=0.001, the exact rational certificate is below0.01 (see release_budget_certificate.json). These are required service specifications, NOT experimentally acquired values. The same output-memory service and control information must be offered to ordinary DD/QEC/coherent-feedback alternatives.

This closes the mathematical 'trace and pretend reset' gap for a specified physically isolated output path. It does not solve the more fundamental architecture-selection question: the X_s Z_D source in this branch is unwanted noise while desired graph gates are independently supplied. Avoiding the source altogether may be cheaper if physically possible. No evidence says it is unavoidable. Before deeper optimization, a stronger capability task should require the mediator to supply an otherwise unavailable useful interaction; ordinary no-knowledge feedback and quantum-bus gates then deserve the same access and costs.
