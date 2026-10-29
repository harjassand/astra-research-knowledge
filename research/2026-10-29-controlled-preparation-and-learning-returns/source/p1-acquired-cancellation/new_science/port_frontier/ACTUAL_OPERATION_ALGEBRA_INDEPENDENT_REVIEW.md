# Independent review of the acquired actual-operation algebra

29 October 2026. Port-information agent review of NEW root work, at the exact
versions below. This does not re-audit unchanged predecessor science. Ordinary
analytic checks are given here; no hardware, native samples or solver replay.

## Reviewed versions and conclusion

* ACTUAL_OPERATION_ALGEBRA.md:
  d45b664203b432b1d70bce4cbacf11502a32a0ada7b671e58bb8ac1091198015.
* FINITE_PULSE_CAUSAL_CLOSURE.md:
  248b0044bf7c9130dd9673cdc596be2e94681daf886352fbbd938d53f4bc9ee2.
* ADJOINT_WORD_ACQUISITION_AND_EXPANSION.md:
  4f8b91f56835f33e98501d967da9881d7caa5c8f308de9692129bc836e3f57b5.

Exact copies are preserved in port_frontier/reviewed_versions/.

**Conclusion:** The actual-menu generalization is valid at the stated common
hidden-space, weighted-reversibility, switching and baseline-preparation
interface. It genuinely removes the fixed kinetic-prefactor relation BETWEEN
operations. The complete visible-path statement, generator leakage conversion,
and displayed signed L1 bounds (4)--(5) survive the detailed challenge below.
The kernel-only corollary also survives with its endpoint-only interface.

Two qualifications should be explicit when the main note stands alone:

1. In (5), e_init is the error in representing the BASELINE pi expectation on V.
   It does not by itself certify a different physical initial distribution by
   matching only its V moments. A physical preparation TV error beta adds 2beta
   to full-path L1. A general L2 initial density needs its norm in front of the
   leakage term. An explicit failure of the broader interpretation is in §7.
2. zK,zJ bound errors in the actual approximate killed/jump OPERATORS. Formula
   (5) then concerns their exact time-ordered evolution. Additional numerical
   exponential/ODE quadrature error must be included via its own error bound or
   a warranted effective-generator perturbation, not called zK automatically.

These do not invalidate (4)--(5) from the supplied baseline pi with the stated
operator-error interpretation. Data-selected dictionaries also retain the fresh
service/joint calibration-state qualification in the companion finite-pulse note.

## 1. Kinetic-premise removal is real, with a precise remaining premise

For each actual operation j, Q_j is independently a conservative bounded
generator, reversible for the unnormalized measure pi w_j(Y). It may have
arbitrary unknown symmetric prefactors, including different internal same-label
kinetics. None of the argument below compares those prefactors across j.

This is weaker than the canonical formula q^h_xy=q_xy h(Y_y)/h(Y_x): an energy
ratio alone is not used to predict an unmeasured generator. The theorem covers
only the measured menu and actual implemented mixtures. Unmeasured amplitudes
still need the separate canonical identity; that distinction is correct.

There remains one shared physical state space, and switching acts by changing
the generator with no extra kick or hidden apparatus update. If a real operation
has a transition/preparation map at its boundary, that map has to be acquired
too. The observed record does not certify reversibility, the weights, the clock
law, the source rate cap or the switching interface.

## 2. The weighted chronological acquisition identity

Write W_j=M_(w_j), H_j=W_j^(1/2), and <.,.>_j=<.,W_j .>_pi. Detailed balance
implies S_j^* W_j=W_j S_j, where * is the baseline adjoint. Hence

    S_j^*=W_j S_j W_j^-1.

An adjoint word reverses the order of its factors and replaces every pulse by
this weighted forward pulse. Every W_j and W_j^-1 is multiplication by a known
function of the visible label. Consequently, for f_i=O_i1,

    <f_i,T f_l>_pi = <1,O_i^* T O_l1>_pi

is an ordinary expectation from baseline pi of ONE chronological experiment.
It is not a joint law of independently sampled futures from a hidden state.
All left-word weights are attached to measured endpoints of actual forward
pulses. Their maximal growth is at most r_j^2 per corresponding pulse.

No pi w_j stationary preparation is required for this identity. The initial
preparation is baseline pi; the weights perform numerical reweighting. With
two center pulses, separate independent exponential clocks produce S_j^2;
one doubled exponential duration does not.

Because V is label-local, P commutes with every label multiplier. This makes
the SAME P orthogonal in every weighted space. Thus, with F the dictionary map,

    G_j=F^*W_jF,  K_j=F^*W_jS_jF,  D_j=F^*W_jS_j^2F,
    R_j=D_j-K_jG_j^-1K_j
       =F^*S_j^*W_j(I-P)S_jF >=0.

The final equality follows from weighted orthogonality of P and S_j's weighted
self-adjointness. K_j is symmetric. The normalized residual is exactly
epsilon_j^2=||(I-P)S_jP||_j^2, with the compression eigenvalues understood in
the G_j metric, not the raw Euclidean norm of a nonsymmetric coefficient matrix.

## 3. Exact closure and the improved leakage conversion

The exit ceiling and weighted reversibility give

    spectrum(Q_j) subset [-2Lambda_j,0],
    a_j I <= S_j <= I,  a_j=alpha_j/(alpha_j+2Lambda_j)>0.

Therefore zero residual is equivalent to S_jV subset V. Its finite-dimensional
restriction is positive definite and invertible, so S_j^-1 preserves V as
well. The identity Q_j=alpha_j(I-S_j^-1) proves generator invariance. The
converse follows from the resolvent. This uses neither a state-count bound nor
unmeasured kinetics. With C_j=P S_jP|V, the represented restricted generator is
alpha_j(I-C_j^-1), as claimed.

For approximate closure, write B_j=(I-P)S_jP and c_j=lambda_min(C_j). From
S_jP=P C_j+B_j, multiply by S_j^-1 and project to V-perp:

    (I-P)S_j^-1P=-(I-P)S_j^-1 B_j C_j^-1.

Hence

    ||(I-P)Q_jP||_j <= alpha_j epsilon_j/(a_j c_j)=d_j.

Since c_j>=a_j, the safe alpha_j epsilon_j/a_j^2 follows. Confidence lower
bounds on a_j,c_j and upper bounds on epsilon_j must be used after acquisition.
With r_j=max sqrt(w_j)/min sqrt(w_j), changing to the baseline norm costs at
most r_j, so ||(I-P)Q_jP||_pi<=D=max_j r_j d_j.

The inverse-compression approximation alpha_j(I-C_j^-1) is not exactly P Q_jP
when the residual is nonzero. The companion bound alpha_j epsilon_j^2/a_j^3
must therefore be included in zK,zJ when those are the matrices used in the
predictor. The main note correctly labels (4) as comparison with the TRUE
compression rather than silently identifying the two.

## 4. Arbitrary visible-history switching and full visible paths

Fix a finite label history with ordered jump times. Conditional on the external
policy random seed and that visible prefix, the selected operation is a
deterministic measurable function of time until the next visible jump. The
policy may use waiting times and arbitrarily many operation switches; it cannot
use hidden-state events or future visible jumps. The predictable operation just
before a visible jump sets its jump intensity; later observed labels may choose
the next operation without an unmodeled physical kick.

For label a, the killed generator A_(j,a)=E_a Q_j E_a on E_a L2(pi) is
self-adjoint nonpositive: w_j is constant within that label, so the weighted
and baseline inner products differ only by a scalar. Its time-dependent
propagator is a contraction. The same is true of C_(j,a)=P A_(j,a)P on V_a.
Bounded measurable switching has a standard bounded-operator evolution; a
uniform exit cap also constructs the native process without explosion.

The cross-label jump operator J_(j,ab)=E_a Q_j E_b has weighted norm <=Lambda_j.
One direct Schur test uses the nonnegative off-diagonal rate block, its row sum
<=Lambda_j, and detailed balance for the reverse row bound. Converting from
label b to a gives

    ||E_a Q_j E_b||_pi
       <= Lambda_j sqrt(w_j(b)/w_j(a)) <= J=max_j r_j Lambda_j.

Because P commutes with every E_a,

    ||(I-P)E_a Q_j E_bP||<=D,
    ||(I-P)A_(j,a)P||<=D.

When all defects vanish, both killed and jump operators preserve V. Their
chronological products are precisely the densities of every complete visible
path with respect to label-word counting and ordered-jump-time Lebesgue measure.
Compression therefore reproduces each density under the SAME history-selected
program. Integrating jump times and external randomness gives the exact theorem.
This does not require the program to be Markov in the current visible label.

Even when the compressed matrices are signed, these chronological products
define a finite signed path measure: their absolute series is dominated by
k exp((k-1)JT) on a finite horizon. A numerical version has the analogous
bound below. A signed predictive realization is not automatically a positive
finite-state physical model.

## 5. Detailed derivation of the main signed L1 bound

Let U_A(t,s) and U_C(t,s) be source and compressed killed propagators along
one label interval. Duhamel, acting on V_a, gives

    U_A(t,s)P-PU_C(t,s)
       =int_s^t U_A(t,r)(I-P)A(r)P U_C(r,s)dr.

Thus its norm is <=(t-s)D. This is a comparison on inputs in V; it does NOT
claim that the full source propagator is close in operator norm to its finite
rank compression on arbitrary hidden inputs.

For a path with m visible jumps, telescoping the operator word from the right
ensures that every replaced-factor discrepancy acts on an input in V. Killed
factors are contractions and jump factors have norm <=J. The sum of interval
lengths is T. Hence the density difference is bounded by

    T D J^m + m D J^(m-1),

with the second term omitted when m=0. Initial and terminal indicators have
baseline L2 norms <=1, so no missing norm factor occurs for baseline pi.

There are k(k-1)^m visible label words and a jump-time simplex of volume T^m/m!.
Summing the absolute density error gives

    k T D exp((k-1)JT)
      +k(k-1)T D exp((k-1)JT)
       =k^2 T D exp((k-1)JT).

Thus (4) is correct. Feedback changes the chosen factors as a function of the
prefix, but every displayed bound is uniform over that choice, so the same
dominating sum applies. No policy derivative, mixing rate, or finite branch
alphabet is needed. The observed label alphabet itself remains finite.

## 6. Numerical operator and baseline-functional errors

Let the actually used approximate killed blocks differ from the true compressed
ones by <=zK, and approximate jump blocks by <=zJ. Label projectors and constant1
remain consistent with the known label-local dictionary. Then

    ||U_hat_a(t,s)||<=exp(zK(t-s)),
    ||J_hat_ab||<=J+zJ.

Duhamel gives killed discrepancy <=(t-s)(D+zK)exp(zK(t-s)). Jump discrepancy
on V is <=D+zJ. The same right-to-left telescoping yields, for m jumps,

    exp(zK T){T(D+zK)(J+zJ)^m
                         +m(D+zJ)(J+zJ)^(m-1)}.

If ell_hat differs from the baseline functional <1,.>_pi on V by dual norm
e_init, its additional per-word error is <=e_init exp(zK T)(J+zJ)^m. Summing
the counting/simplex series gives exactly

    k[e_init+T(D+zK+(k-1)(D+zJ))]
                exp([zK+(k-1)(J+zJ)]T).

This verifies (5), including its numerical/initial FUNCTIONAL terms. It bounds
the L1 difference of the source law and a finite signed path prediction. For
bounded g, the payoff bound is ||g||_infinity times this expression. Dividing
by two gives a TV distance only when the compared signed object is itself a
probability measure. Scalar clipping does not establish that positivity.

## 7. The physical-initialization qualification is essential

If the source begins from mu with density g=dmu/dpi in L2(pi), the argument
instead gives

    k[e_init+||g||_2 T(D+zK+(k-1)(D+zJ))]
                exp([zK+(k-1)(J+zJ)]T),                    (A)

where e_init now compares ell_hat with <g,.>_pi on V. A TV bound
TV(mu,pi)<=beta gives the simpler additive 2beta full-path L1 correction to
(5), by common-policy data processing. For calibration-dependent deployment,
the analogous bound concerns the actual JOINT source/controller-record law.

Matching V moments alone is insufficient under approximate closure. Here is a
concrete finite example, with epsilon in (0,1/2):

    pi=(1/2-epsilon, epsilon, 1/2),
    labels A={1,2}, B={3},
    q_23=1, q_32=2epsilon, all other off-diagonal rates zero.

The generator is reversible and has exit cap one. V=span{1_A,1_B}. Its true
compression has A<->B rates 2epsilon and stationary label law (1/2,1/2).
Direct calculation gives generator leakage

    ||(I-P)QP||=2sqrt(epsilon(1-2epsilon)) ->0.

Prepare mu=(0,1/2,1/2). It matches pi on EVERY feature in V, so its restricted
initial-functional error is zero. Nevertheless its B probability at time T is

    1/2 + [(1/2-epsilon)/(1+2epsilon)]
                                  (1-exp[-(1+2epsilon)T]),

whose gap from the compressed prediction 1/2 tends to (1-exp(-T))/2>0.
The L2 initial-density norm diverges, exactly as required by (A). The example
does not challenge the main theorem's baseline-pi premise; it prevents replacing
that physical preparation by a feature-matching assertion.

## 8. Kernel-only smaller interface

For fixed actual reversible kernels T_j, the same adjoint-word acquisition
gives R_j=F^*W_jT_j(I-P)T_jF. No positivity of the spectrum or invertibility
is necessary: zero residual directly means T_jV subset V. Consequently every
finite program of these exact calls and common endpoint label measurements has
the exact represented joint law. The existence of a bounded generator is not
used. Negative or zero eigenvalues of T_j cause no issue here.

This theorem does not recover arbitrary durations, between-call trajectories,
or a discarded native clock side record. Those would be different operations.
All finite prefixes also determine an infinite endpoint sequence law if the
discrete causal program is well-defined; no uniform finite-error infinite-call
claim follows from the finite-m statement.

For completeness, one conservative explicit finite-error version is as follows.
Let D_K=max_j r_j ||(I-P)T_jP||_j and J_K=max_j r_j. Let every approximated
label-to-label kernel block have additional operator error <=z. For exactly m
calls from baseline pi, the same word telescoping gives

    L1 <= k^(m+1)[e_init(J_K+z)^m
                         +m(D_K+z)(J_K+z)^(m-1)].           (B)

The m=0 second term is omitted. Padding stopped programs by a common identity
kernel gives the analogous at-most-m statement. This is deliberately loose and
makes no favorable scaling claim. It substantiates the smaller-interface
corollary without importing a hidden exit-rate or clock promise.

## 9. Review scope

This review establishes the new actual-menu algebra and its consequence bounds
at the stated native interface. It does not establish small predictive rank,
practical Gram conditioning, cheap weighted-depth acquisition, any source bath
or reset certification, a positive reduced simulator, or physical advantage.
It does not replay the root's ongoing finite-precision acquisition executable.
Those are separate claims and should retain their own evidence.
