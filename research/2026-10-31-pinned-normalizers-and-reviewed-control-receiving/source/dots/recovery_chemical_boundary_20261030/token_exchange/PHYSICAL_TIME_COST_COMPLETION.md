# Physical time cost when the phase scale has a certified positive floor

30 October 2026. Optional local completion; not part of the three-note receipt.

The phase-scaled exchange rule deliberately does not infer holding-time control from its bounded trace reward. If the ACTUAL physical-time excursion generator is Q_y=s(y)Q0-diag(k), and a separate certificate proves s(y)>=s_min>0 on every admitted entrance and transient phase, such control is available.

Solve -Q0 v=1 and set M=max_p v_p/s_min. The stopped supersolution v/s gives E_p tau<=v_p/s<=M. The same bound applies conditionally after every interior stopping time because the ordinary fiber and s are frozen. By the strong Markov property and the tail-integral identity, induction gives

    E_p tau^k <= k! M^(k-1) E_p tau <= k! M^k,

for every integer k>=1. In detail, tau^k=k integral_0^tau (tau-u)^(k-1)du, and the conditional remaining moment is <=(k-1)! M^(k-1). Thus E exp(theta tau)<=1/(1-theta M) for 0<=theta<1/M.

With the actual trace entrance bound lambda_e<=s ell_e, aggregate costs satisfy

    sum_e lambda_e E_e tau <= ell dot v,
    sum_e lambda_e E_e tau^k <= k! M^(k-1) ell dot v.

These compensate all repeated entries through their true entry counts; they do not require a small return probability. They are LOCAL physical-duration costs. Events during the excursion must still be represented in Q_y or retained as actual terminals. An immigration or seed mark cannot simply be omitted because it changes the frozen fiber.

A positive rational coefficient times an enabled integer monomial has a positive floor; a divided-clock expression or a rational function need not. The floor must refer to the physical generator, not be inferred from positivity of a trace-clock rate. If s can approach zero, none of the displayed uniform time bounds follows. This completion does not supply the missing whole-network signed-cycle or large-B trial arguments.
