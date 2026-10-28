# Bounded-matrix and terminal-stage refinement for growing selectors

28 October 2026. **Separate strengthening candidate; independent review pending.** The base `ordinary_growing_selector_active_effect_acquisition_20261028.md` is frozen at SHA `136c4f8a83c81ad28f097f3f35adaf1299b0113d4435e860be119ca0668ed202`; its elementary Frobenius/majority proof is unchanged. This note keeps exactly the same ordinary input/control interface and rational preconditioner, but replaces its conservative matrix estimator and accuracy schedule. No new source samples or hardware claims.

The target is high-probability relative selection for an unknown real PSD effect0<=A<=I_m from actual Bernoulli probes p(x)=x^T A x, using a finite cap

    O_tilde(m^3/(gamma epsilon)),

instead of the base O_tilde(m^4/(gamma^2 epsilon)). This is active effect tomography for a frozen physical receiver, not arbitrary circuit optimization or a new matrix concentration theorem.

## 1. The ACTUAL acquired matrix has bounded operator variance

Use the base rational polynomial preconditioner C, which commutes with a certified known B in[tau I,4I], satisfies CBC<=I and C^−2<=2B. Sample the same even fourth-moment z, prepare x=Cz/||Cz||, obtain its single Bernoulli y, and record

    Y=y s T(z), s=||Cz||^2,
    T(z)=m(m+2)zz^T/2−mI/2.

Conditional on a good prior history A<=B, F=E Y=CAC<=I. Besides the base Frobenius bound, the actual random variable satisfies

    E Y^2=E[s(z^T Fz)T(z)^2]
             <=tau^−1 E T(z)^2=(S_m/tau)I,
    S_m=m^2(m+3)/4.

Each T(z)^2 is positive, and0<=s(z^TFz)<=1/tau, so this operator inequality uses no commutation of F with the sampled T. Centering gives E(Y−F)^2=E Y^2−F^2<=S_m I/tau. Also

    ||Y−F||<=m(m+1)/(2tau)+1<=R_m/tau,
    R_m=m(m+1).                                        (1)

These are properties of the recorded ordinary Bernoulli estimator, not an imported quantum matrix-query oracle.

## 2. Primary bounded matrix Bernstein import and a finite count

Apply [Tropp, User-friendly tail bounds for sums of random matrices, arXiv:1004.4389v6](https://arxiv.org/pdf/1004.4389v6), Theorem6.1(ii), pp21–22, separately to the centered matrices and their negatives. The imported theorem concerns independent bounded self-adjoint summands, their zero mean and operator variance. It supplies the two-sided sample-mean bound

    Pr(||Fhat−F||>delta)
      <=2m exp[−N delta^2/(2S_m/tau+(2/3)R_m delta/tau)]. (2)

Within one batch B and C are fixed by the PREVIOUS history, and reset calls plus fresh z make the actual Y independent. Conditional application followed by the first-failure union bound is legitimate; no assertion of independence across adaptive envelopes is used.

For at most H matrix estimates, set

    P_m=2S_m+R_m,
    L=ceil log2(4mH/beta),
    N(tau,delta)=ceil[P_m L/(tau delta^2)], 0<delta<=1.   (3)

Because2S_m+(2/3)R_m delta<=P_m and e^−L<=2^−L, each estimate fails with probability at most beta/(2H). The ordinary arithmetic sample mean is exactly rational. No medoid, heavy-tail guarantee, noncommutative robustness theorem or extra source observation is needed. All integer/logarithm caps are known before observations.

## 3. Constant-accuracy envelopes, then ONE fine terminal estimate

First suppose epsilon<gamma. Let

    J=ceil log2(gamma/epsilon), H=J+1,
    tau_j=2^−j, c0=1/16, delta0=c0/4=1/64,
    B_0=2I.

For j=1,...,J, take ONE matrix average of N(tau_(j−1),delta0) actual Y observations. Use the base reconstruction C^−1 Fhat C^−1, its fixed largest-dyadic update rounding, and exact PSD accept-or-safe-abort guard, but with the CONSTANT c0 rather than gamma/16. The identical proof gives, on simultaneous success,

    A+tau_j I<=B_j<=(8/7)A+2tau_j I.                    (4)

Thus the endpoint tau=tau_J obeys epsilon/(2gamma)<tau<=epsilon/gamma. The coarse procedure is not run down to epsilon at gamma-level accuracy.

Freeze B_J. Build its known rational C and take a fresh terminal sample mean at

    delta=gamma/64, N_terminal=N(tau,gamma/64).

Reconstruct the rational symmetric M=C^−1 Fhat C^−1. It need not be PSD. On terminal success,

    −2delta B_J<=M−A<=2delta B_J.                        (5)

Compute a known unit vector x with certified Rayleigh slack

    x^T M x<=lambda_min(M)+epsilon/16.                   (6)

This is a finite known-matrix eigensolve; no source query, matrix completion, hidden eigenvalue gap or global optimization oracle is used.

Let p_*=lambda_min(A), u=gamma/28 and v=gamma tau/16. Equations(4)–(5) give the UNIFORM scalar inequality

    |x^T(M−A)x|<=u p(x)+v.

Applying it both at the selected x and a true minimizing direction, then using(6), yields

    p(x)<=[(1+u)/(1−u)]p_*+[2v+epsilon/16]/(1−u).

Since u<=1/28 and v<=epsilon/16,

    p(x)<=(1+2gamma/27)p_*+7epsilon/36
         <=(1+gamma)p_*+epsilon/4.                      (7)

This is why a terminal gamma-precision estimate only needs a floor of order epsilon/gamma. Simply using gamma-level precision at every epsilon-floor stage would retain the unnecessary gamma^−2 factor.

## 4. The additive regime epsilon>=gamma

No envelope construction is needed. Use C=I, x=z and the same matrix record Y=y T(z), whose mean is A and whose bounds(1) hold with tau=1. Put H=1, delta=epsilon/16, and take N(1,delta) actual calls. Return an approximate minimum-eigenvector of the resulting rational sample mean with Rayleigh slack epsilon/16. On the matrix event,

    p(x)<=p_*+3epsilon/16<=(1+gamma)p_*+epsilon/4.

This costs O(m^3/epsilon^2), which is at most O(m^3/(gamma epsilon)) in this regime. One must not keep a gamma-precision terminal batch when epsilon is much larger than gamma.

## 5. Deterministic cap and inherited physical controls

For epsilon<gamma, sum_j tau_(j−1)^−1<2gamma/epsilon and tau_J^−1<2gamma/epsilon. Equations(3) give

    T_coarse<=J+8192P_m L gamma/epsilon,
    T_terminal<=1+8192P_m L/(gamma epsilon),
    T_total<=H+16384P_m L/(gamma epsilon).               (8)

For epsilon>=gamma,

    T_total<=1+256P_m L/epsilon^2
            <=1+256P_m L/(gamma epsilon).               (9)

Here P_m is a degree-three polynomial in m. All-history finite caps and safe aborts are retained. The first-failure union over at most H estimates costs at most beta/2, hence at most beta; source/reset/physical implementation errors remain in a separately specified whole-process discrepancy, not in the matrix event.

The base rational binomial-series preconditioner, exact dyadic rounding/PSD certificates, fixed finite arithmetic, capped integer/sign samplers and known selector amplitude synthesis remain unchanged. Replace its T_max by(8) or(9) when allocating their full failure and gate-precision budgets. The terminal rational M has a known polynomial all-history norm bound, so its gap-free eigensolve and final normalized-state compilation have a fixed polynomial cap even on bad statistical histories. No fitted covariance or empirical eigenvalue is allowed to select an uncharged accuracy.

The selector still needs arbitrary known dimension-m state control, not poly(log m) gate cost. It occupies ceil log2 m input qubits but requires O(m) known two-level state-preparation rotations before native compilation, precision and routing. Global q-logical test preparation/readout, the frozen receiver, collective decoder-learning banks, memory and one final payload remain paid. All finite sampler/compiler discrepancies are charged over the COMPLETE combined schedule.

## 6. End-to-end scope

Replace only the selector primitive in Section7 of the frozen base theorem. Its complete m-anchor definition of rho, supplied operator margin, factor-m decoder regret, exact/approximate local geometry and structural floor remain unchanged. Use its same primitive tolerance[d/(d+1)]epsilon/8 and confidence allocations; the stronger high-probability bound(7) has more than the required additive reserve. Consequently the frozen base's full relative comparator and explicit floor still hold, while its selector term T_max becomes O_tilde(m^3/(gamma epsilon)).

In particular, no factor4 is restored: decoder regret transfer remains m ell0, and approximate tails are weighted by the NEW m-anchor rho. Finite-time local-evolution widths must still suppress the full m qA_geom tail and pay4^w. The same conventional active-effect learner can implement this strengthening. This is not a minimax lower bound, a generic circuit-encoder theorem, a new bounded-matrix concentration result, a non-reset guarantee or an acquisition/hardware experiment.
