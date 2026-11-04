# Prepared equilibrium-safe start without the rare-branch starting-mass factor

This is a distinct prepared operation with complete [standalone derivation](package/equilibrium_start_corollary.txt) and [integrated proof](package/rare_failure_research.tex). It changes the initial law explicitly; it does not replace the [specified all-working/fixed-start question](README.md) by implication.

Let the exact product law be `pi`, failure set `B`, safe set `A`, `p=pi(B)<=1/2`, and target initial law `nu=pi(.|A)`. Freeze operating ports, draw all independent Bernoulli labels digitally, prepare/read the register and reject failed configurations. Acceptance is at least `1/2`, so at most two full preparations are needed on average. Pay every bit write, verification, failure-predicate test and protected setup. A short total-variation mixing argument is not an exact substitute for this preparation contract. No efficient rejection preparation is claimed when safe configurations are exponentially rare.

The mean is `M_nu=M_pi/(1-p)`. At exact common `pi`, killed-form comparison directly yields

```text
M_fit,nu/(1+rho) <= M_true,nu <= M_fit,nu/(1-rho),
```

because this mean is the quadratic inverse `pi_A^T L^-1 pi_A/pi(A)`. No inverse starting-atom mass `kappa^-1` is needed in this comparison.

For lazy uniformized updates, use `l=ceil((log(1/xi)+2)/g)` and rare gate `p<=xi/[2(l+1)]`. The conditional reverse no-return statistic `D_l=p E[Z]` has `(1-2xi)lambda<=D_l<=(1+xi)lambda` and useful probability `E[Z]>=g(1-2xi)`. Together with `1/lambda-1/g<=M_pi,*<=1/lambda`, it gives the conservative `1-4xi<=M_nu,* D_l<=1+4xi` for `xi<=0.01`. A positive confidence interval `[D_L,D_U]` therefore yields physical-generator interval `[(1-4xi)/(R D_U),(1+4xi)/(R D_L)]`, with the actual fixed-clock conversion retained. This rare branch removes the `kappa` parameter; the static counting, conditional sampler, gap, precision and confidence costs remain.

## Finite initial writes

For known `p_L>0` below `pi(B)`, a conservative choice is `pi_min` for any nonempty failure set. The supplied physical-generator bound is

```text
V=1/R+[1+0.5 log(1/pi_min)]/(gamma_min p_L).
```

If actual initial preparation couples to the ideal safe law with error `delta_init`, its mean differs by at most `delta_init V`. Since the ideal safe mean is at least `1/R`, `delta_init<=epsilon_init/(R V)` suffices for the allocated relative error, including accidentally prepared failed states with zero first hitting time.

Under the same strong independent/stable/nondemolition/nonbackacting verification and protected-idle contract as the [factory construction](physical-interface.md), a union bound requires order `log(m/delta_init)/(1-2e)^2` checks per written bit, plus retries and real service. Even when `p_L` is exponentially small, logarithmic precision cost is polynomial in product-probability bit length, `m`, log inverse gap and log inverse accuracy. This conclusion relies on the stated verification model; ordinary additive readout quality does not establish it.

Allocate initial preparation and operating-factory errors separately. The ratewise forest comparison applies simultaneously to every start and can then expand the ideal-model interval. No lifetime-scale waiting, unrestricted hardware calibration, physical implementation or historical priority is established by this corollary. [Complete original package and provenance](SOURCES.json).
