# Finite-temperature rare-rate acquisition by isotropic forcing

This independent companion constructs an exact force/intervention protocol for a specified classical thermal-effusion model. It has a [complete standalone derivation](package/companion/effusion_companion.md), [original diagnostic code](package/companion/check_effusion_companion.py) and [recorded diagnostic](package/companion/effusion_diagnostic.json). It is independent of the [quantum control-speed theorem](README.md). The completed supplied mathematical construction is not an experimental demonstration, general materials-failure law or established priority claim; no companion-specific independent review is inferred from the quantum proof check.

## Actual transport and control contract

A maintained stationary Poisson thermal-flux source injects classical particles into an unknown finite or countable set of straight separable collisionless guides. Guide directions and channel labels need not be observed; total incident flux is finite. Each guide has length `L` and longitudinal potential `U_j>=0`, with maximum `B_j` in a **certified common shell** `[ell-w,ell+w]` and `B_j>=B_min>F L`. Potential is zero outside the shell, or a proved equivalent height margin keeps the maximum there under every permitted force. This is a promise about every route, not something established by a few detected exits.

Ports supply a calibrated static force vector `|f|<=F`, an input shutter and actual clearing/reset between force blocks. Incoming thermal flux is shielded/maintained independently of force or its variation is bounded. Transmissions are detected at absorbing guide ends; unsuccessful particles cannot affect later trials. Collisions, tunnelling, inelastic walls, unbounded detector errors and clearing failures are outside the ideal class unless separately budgeted.

The incident **flux-weighted** longitudinal energy is exactly exponential with inverse temperature `beta`. Consequently transmission has exact threshold `E>=max_x[U_j(x)-x f.v_j]`, without low-temperature or Kramers approximation. Saddle motion remains inside the shell and changes the threshold from `B_j-ell f.v_j` by at most `Fw`.

For unknown baseline rate `a_j=nu_j exp(-beta B_j)`,

```text
exp(-beta Fw) a_j exp(beta ell f.v_j)
 <= k_j(f) <=
exp(beta Fw) a_j exp(beta ell f.v_j).
```

No individual positive prefactor lower bound, barrier catalogue or saddle reconstruction is needed. A generic force-spectroscopy system without the shell mechanics does not inherit this response.

## Positive directional design and inferential interval

Set `s=beta F ell`, `Gamma_3(s)=sinh(s)/s` with value one at zero, and `Lambda=sum_j a_j`. Isotropically averaging static forces multiplies the total baseline rate by `Gamma_3(s)`, within the shell envelope `exp(+-beta Fw)`. Every unknown direction receives the same averaged factor. The stationary output waiting mean is `1/Lambda`. An initially empty apparatus instead has `1/Lambda<=M_empty<=1/Lambda+L sqrt(pi m_particle beta/2)`, an explicit additive first-flight correction rather than an assumed stationary start.

A finite positive quadrature uses Gauss–Legendre polar nodes and equally spaced azimuths, exact to degree `t`. Uniform error is at most `2 exp(s)s^(t+1)/(t+1)!`; `t=O(s+log(1/eta_q))` yields `q=O((s+log(1/eta_q))^2)` settings with positive dwell weights. Hold each force through injection and subsequent flight/flush. It does not require infinitely fast rotation while particles are in flight.

For energy margin `zeta>0`, all particles above barrier plus margin arrive within `tau_f=L sqrt(m_particle/(2zeta))`. They constitute exactly an `exp(-beta zeta)` fraction of successful launches. Close the shutter, keep force constant for `tau_f`, count arrivals and clear leftovers. Arbitrarily slow near-threshold particles therefore cause a bounded deficit, rather than an unpaid infinite settling time.

With independent detector efficiency in `[d_-,d_+]`, other calibrated log-rate error `alpha_c`, and log-quadrature error `alpha_q`, pooled counts over total source-open time `T` are Poisson with mean between `A_- T Lambda` and `A_+ T Lambda`, where

```text
A_-=d_- Gamma_3(s) exp(-beta Fw-alpha_q-beta zeta-alpha_c),
A_+=d_+ Gamma_3(s) exp( beta Fw+alpha_q+alpha_c).
```

An exact Poisson-mean interval `[mu_L,mu_U]` gives `Lambda` in `[mu_L/(A_+T),mu_U/(A_-T)]` and stationary mean in `[A_-T/mu_U,A_+T/mu_L]`. A zero lower count endpoint leaves an infinite upper lifetime endpoint. For zero counts, one-sided confidence `1-delta` only gives `Lambda<=log(1/delta)/(A_-T)`. Fresh validation exposure can bound aggregate unseen marked channels if the detector distinguishes novel marks; total-hazard inference itself needs no labels. Adaptive exposure needs a valid confidence sequence or allocated predetermined stages.

## Full physical bill and static-design minimax law

The systematic ratio `A_+/A_-` must already fit the desired relative width; additional shots cannot repair geometric/physical extrapolation bias. With small enough systematic error, order `epsilon^-2 log(1/delta)` accelerated detections are required, and actual source-open time scales as that count divided by `Gamma_3(s)Lambda`. For one barrier this retains exposure proportional to `exp[beta(B-Fell)]`. It is accelerated, **not lifetime-free**, and an extremely small incident prefactor still costs exposure.

Full wall time adds `q(tau_f+tau_clear+tau_slew)` to `T`. Charge all incident particles `nu_total T`, kinetic-energy supply, preparation/reset for destructive specimens, field holding/switching, detector dead time and backgrounds when making an engineering claim. Uncalibrated background dominating the signal prevents relative inference. Required force/geometry/thermometry precision includes absolute `s` error `O(epsilon)` and shell width `w/ell=O(epsilon/s)`. Actual bath-temperature drift is different from estimating the force gain: with fixed measurable total flux and bounded flux variation, the aggregate Jensen correction requires temperature stability on the scale `epsilon/log(nu_total/Lambda)`. The natural Maxwell flux factor must also be corrected when appropriate.

In the **exact sharp-shell model**, isotropic forcing maximizes the worst-direction acceleration among all distributions of static forces of magnitude at most `F`: its exact value is `Gamma_d(s)`. Averaging any design over unknown directions proves the upper bound. A single hidden Poisson channel gives the corresponding no-event exposure lower bound of order `log(1/delta)/(a Gamma_d(s))`. This is not a minimax theorem for arbitrary time-dependent forcing, which can pump extra work. Under a separate per-particle positive-work cap `W`, acceleration is at most `exp(beta W)` when `B_j>W`; at `W=Fell`, spherical gain is within approximately `2s` of that bound. Without the work cap that comparison is unavailable.

Recorded mathematical values include `Gamma_3(10)=1101.32328747`, `Gamma_3(20)=12129129.8852`, `Gamma_3(30)=178107909692`; conservative error-0.01 quadratures use 722, 2738 and 6050 settings. They are diagnostic calculations, not experimental performance predictions, and were not rerun by Capital.

Temperature-accelerated dynamics, TAMMBER, hyperdynamics and force spectroscopy are credited prior machinery. Direct counting, known-direction forcing and temperature acceleration are required baselines. A known direction obtains `exp(s)` and can beat the spherical gain by roughly `2s`; direction ignorance is a real restriction. This construction does not infer P2's topology/independence, rule out hidden mechanisms, or solve arbitrary materials, ageing, chemical-state or common-cause failure. [Original package and provenance](SOURCES.json).
