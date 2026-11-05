# Private clock, finite meter, initialization and reuse

This page gives the physical service bill for the [local thermal intervention theorem](README.md). Read the supplied [finite-pointer construction](package/thermal/FINITE_POINTER_REALIZATION.md), [reference and reuse review](package/uncertainty/PRIVATE_TRIGGER_REFERENCE_REVIEW.md), and [campaign resource laws](package/CAUSAL_CAMPAIGN_AND_RESOURCE_LAWS.md). The actual trigger, measurement and controller must supply their stated independence, precision, force, initialization and isolation properties. An abstract reset or point-time sample is not substituted for them.

## Clock with an actual continuous arrival law

A calibrated source-independent Poisson arrival clock, with rate r and timeout H, has abort probability `alpha_c=exp(-rH)`. Conditional on arrival its density is bounded by `C_g=r/(1-alpha_c)`. For thermal error allocation delta_th, sufficient choices are

```text
r=4 gamma(1-alpha_c)delta_th^2/D0,
H=D0 log(1/alpha_c)/[4 gamma(1-alpha_c)delta_th^2].
Expected occupancy, including timeout: (1-alpha_c)/r.
```

An actual independent arrival detector need not store an infinitely precise timestamp. Independent finite latency preserves the density bound. Standby power, privacy, coupling, watchdog and detection errors are paid contracts. A finite list of digital point times is not justified by this continuous-density proof. Timeout is a heralded abort, never an experiment launched at a timeout atom. Measurement schedules must retain the source-independence used by the theorem rather than adapt timing to current source readings.

## Momentum inferred over finite position windows

Two position windows of width b and separation ell produce `p_hat=M(Y1-Y0)/ell`. The noiseless estimate is a positive average of actual momentum. The logical intervention time is the window's end; the source is not assumed frozen at its beginning. With supplied local drift, moment and sensor bounds,

```text
e_p <= B_star(ell+b)+sqrt(2 gamma sigma^2(ell+b))
       +2M e_x/ell+M sqrt(2 nu_x/(b ell^2)).
```

The assignment probability's Lipschitz constant L_a converts this to arm error at most `L_a e_p`. Overflow has a separate probability charge. Here B_star bounds local drift in mean square, e_x includes finite readout error and nu_x is the declared white detector-noise density.

Each window uses a fresh canonical pointer `(Q,P)` and a smooth finite interaction

```text
H_int(t)=-G w(t) chi_x(x) chi_P(P),
w(t)=[1-cos(2 pi t/b)]/b.
```

Saturations equal the identity only on declared finite ranges and have bounded derivatives. On that good event the detached pointer has exact signal `Q(b)=Q0+b P0/m_d-G integral w(t)x(t)dt`. Energy and force remain finite. Backaction acts only in the thermostatted momentum direction, with two-pointer action and full hidden/reference path comparison

```text
J_u=E integral u^2dt <=3 G^2 v_P/b,
delta_back <=sqrt(J_u/(8 gamma sigma^2)).
```

Finite peak force is at most `2G P_cap/b`, coupling slew at most `2 pi G/b^2`, and switching work per window at most `4G X_cap P_cap/b`. The Girsanov/Pinsker bound controls the full path, rather than only a visible marginal.

A known isolated harmonic Langevin pointer reset has a finite convergence time from a bounded second moment. Temperature, trap preparation, finite release, readout, refrigeration, protection and disposal all remain paid. Imprecision and backaction share one covariance tradeoff. A quantum pointer must satisfy `v_Q v_P>=hbar^2/4`; fixed hardware therefore has an accuracy floor. This classical construction does not bypass measurement uncertainty.

## Complete error budget

Conditional on clock success, the one-shot error is bounded by

```text
epsilon_one <=sqrt(C_g D0/(4 gamma))+L_a e_p+delta_back
 +eta_overflow+eta_clock+eta_num+2^-L+eta_init+eta_cal.
```

Initialization and calibration allowances are actual terms, not presumed zero. Timeout remains separately heralded. The bill includes source/reference preparation, waiting occupancy, finite bandwidth and ADC, force action and switching, pointer cooling/reset, initialized memory and random bits, finite arithmetic/processing latency, fine-record isolation/disposal, later outcome work, and updated reuse budgets.

One sufficient two-position scaling has `b=O(epsilon_m^2/gamma)` and `e_x=O(sigma b epsilon_m/M)`; after this time choice the sufficient white position-noise density may scale as epsilon_m^8. These severe sufficient costs are not an optimality claim. Extremely cold pointer nonequilibrium free energy is an accounting lower bound, not actual refrigerator work; achievable efficiency, power and time need their own service.

## Reuse does not create fresh specimens

Appending a retained b-bit report adds at most `b log(2)` to the relevant entropy budget. At fixed or source-independent endpoints, controlled forcing has Girsanov charge `E integral u^2dt/(4 gamma sigma^2)`; a conservative entropy estimate uses denominator `2 gamma sigma^2`. A source-state-dependent stopped endpoint does not automatically get the same stationary comparison.

Adaptive campaign error is at most the sum of per-round errors via kernel comparisons evaluated on actual histories. Conditional history-dependent clock caps require `E(C_h D_h)`, rather than silently replacing it by `E(C_h)E(D_h)`. Long campaigns can demand very large waiting and precision bills. Reused hidden states may remain correlated, and fine preparation data cannot leak into later timing or controls.

For outcomes in [0,1], actual score `X_i=2 A_i Y_i` estimates the average history-dependent ideal contrast. With average one-trial TV errors epsilon_i, confidence at least `1-alpha-eta` gives radius `sqrt(8 log(2/alpha)/n)+4 epsilon_bar/eta`. The eta allocation is needed because the entropy certificate controls average histories; it disappears only with a separate per-history bound. Timeout and outcome quantization add their own budgets. This is not an iid confidence interval.

With per-round action J_u and b retained bits, a safe entropy budget is `D_i<=D0+(i-1)c`, `c=J_u/(2 gamma sigma^2)+b log(2)`. A conservative total maximum clock-occupancy bill is

```text
log(1/alpha_c)/[4 gamma(1-alpha_c)epsilon_th^2]
 * [n D0+c n(n-1)/2].
```

It is a sufficient quadratic campaign bill, not an optimality theorem. All calibration, initialization, future experiments, readout, memory and reset costs add to it. The source also gives finite classical memory-barrier and reset-contact models; they are declared device models, not universal hardware laws or free consequences of Landauer's lower bound.

Persistent nonthermal torque u gives a free rotor stationary momentum `N(u/gamma,sigma^2)`, at TV distance `2 Phi(|u|/(2 gamma sigma))-1` from centered Maxwell. A marking-only instrument leaves that marginal unchanged. Waiting cannot remove this nonthermal floor. Equilibrium heat and continued nonthermal work are different premises.
