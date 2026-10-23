# Finite local preparation-force check

24 October 2026. This checks only the exact prescribed-control step in `PREPARATION_CONSTRUCTION_BEFORE_PRIOR.md`. It is a model-level compatibility result, not evidence of an actuator or a physical implementation. No source review was needed.

## Does the force generate the requested history?

For the stated two-component oscillator and field, the equations during control are

```text
q_ddot + omega0^2 q + gamma |q|^2 q = g u(0,t) + f(t),
u_tt - c^2 u_xx + omega_c^2 u = g q(t) delta(x).
```

Set the field to the causal zero-state solution driven by the prescribed `q_d`. In one dimension its local retarded trace is

```text
u_d(0,t) = (g/(2c)) integral_0^t J0(omega_c (t-s)) q_d(s) ds.
```

This trace depends only on past and present local source history. Substituting

```text
f(t) = q_d''(t) + omega0^2 q_d(t)
       + gamma |q_d(t)|^2 q_d(t) - g u_d(0,t)
```

into the oscillator equation makes `q=q_d` an exact solution on `[0,T]`; under the construction's well-posedness/uniqueness premise and zero initial state, it is the trajectory from empty state. There is no anticipatory field or spatially distributed control. The field occupies only `|x|<=ct` at finite time, so the state at `T` still differs from the infinite-tailed dressed state.

## Boundedness, work, and release

For fixed finite `T`, smooth flat-ended `chi`, finite `A,Omega`, and finite model parameters, `q_d`, `q_d'`, and `q_d''` are bounded. Since `|J0(z)|<=1` on the real axis and `|q_d|<=A`,

```text
|u_d(0,t)| <= g A t/(2c),
|f(t)| <= A[T^-2 ||chi''||_infty
            + 2 Omega T^-1 ||chi'||_infty
            + omega0^2 + Omega^2 + gamma A^2]
            + g^2 A T/(2c),   0<=t<=T.
```

This coarse bound is finite for each finite `T`; it is not a uniform resource bound as `T` grows. In particular, it grants exact force cancellation and does not price a practical actuator's force, bandwidth, or error tolerance.

Flatness at both ramp endpoints makes `q_d(0)=q_d'(0)=0`, and at release `q_d(T)=A exp(i Omega T)` with `q_d'(T)=i Omega q_d(T)`. The target oscillator plus its *target* stationary field would require zero force at `T`, but the actual ramp-generated field generally differs there. Hence `f(T-)=-g[u_d(0,T)-u_*(0,T)]`, generally nonzero; setting `f=0` after `T` creates a finite force step. A bounded step changes acceleration but has no impulse, so `q,p` and the field state stay continuous. The oscillator reaches the target's instantaneous `q,p` exactly; the full dressed field is only approximately acquired, and the unforced oscillator need not remain on the exact target orbit.

The net work is finite because `f` and `q_dot` are bounded on a finite interval. In the assumed energy-conserving coupled model, `dH/dt=f dot q_dot`, so from the empty state `integral_0^T f dot q_dot dt=H(T)`. This is signed net work; it does not bound gross positive driver work or imply recovery of the energy after release.

## Exact-control assumptions

Exact trajectory tracking assumes exact `A,Omega,T,chi`, oscillator coefficients, field parameters and coupling, a known empty initial field, and a force law with exact timing and the required local field trace. A feedforward implementation could compute the retarded convolution from the commanded history; feedback instead needs a perfect local trace measurement and exact realization of the cancellation force. Any initial incoming wave, parameter error, sensor error, or force error breaks exact tracking. The construction therefore passes the mathematical finite-force test for every fixed finite `T`, while physical controllability, robustness, and the gross energy/cost budget remain unestablished.

**Conclusion:** the formula is a causal, finite, non-impulsive model force that enforces the prescribed oscillator history from zero state under the stated exact equations. It proves exact local-coordinate acquisition through `T`, not exact global-field preparation or an acquired physical controller.

## Optional smooth force shutdown

The step at `T` can be replaced by a finite smooth taper without changing the prepared-state logic. Continue the *auxiliary* target circle after `T` and let `w_aux` be the free KG field equal to the field mismatch at `T`; the force that would keep this auxiliary circle exact is `f_aux(t)=-g w_aux(0,t)`. Apply

```text
f(t) = zeta((t-T)/tau_s) f_aux(t),  T<=t<=T+tau_s,
```

where `zeta` is smooth, lies in `[0,1]`, equals one with all derivatives flat at the start, and reaches zero flat at the end. This is a precomputed feedforward waveform from the exact field mismatch at `T`; it is not a correction computed from the actual post-T trajectory. The actual state may depart from the auxiliary circle, but the exact rotating-frame balance remains `D_dot=f dot (p-Omega Jq)`, so `|D_dot|<=|f| sqrt(2D)`. The free-field mismatch obeys `c delta |w_aux(0,t)|^2<=D_T` by the one-dimensional trace inequality and conservation of its positive rotating-frame field energy. Therefore

```text
sqrt(D_final) <= sqrt(D_T) + (1/sqrt(2)) integral_T^(T+tau_s) |f(t)| dt
              <= sqrt(D_T) [1 + g tau_s/sqrt(2 c delta)].
```

For fixed finite `tau_s`, this preserves a vanishing preparation-error bound as `D_T -> 0`; it removes the force discontinuity without an impulse or exact state reset. It does not establish a specified actuator bandwidth, robustness, or lower gross work. Causality/model access still assumes the mismatch at `T` is known from the exact zero-state history and parameters; although this can be computed from the past command and the known target, it is not a measurement-free result for an unknown incoming field or uncertain model. Thus the smooth shutdown is a valid mathematical refinement under the same exact-model premise, not acquired hardware.
