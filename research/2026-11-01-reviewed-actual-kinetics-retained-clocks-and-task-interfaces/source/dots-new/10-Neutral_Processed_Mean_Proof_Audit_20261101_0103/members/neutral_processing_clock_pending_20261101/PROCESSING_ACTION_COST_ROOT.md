# Control robustness does not make internal processing free

Status: root cost note, independent review pending. Mathematical path-law action, not a hardware work certificate.

For the actual admitted overdamped model with diffusion matrix 2 beta^(-1)D (constant SPD D), reference drift b, and additional predetermined drift s(t)c(x), the compact smooth transverse construction makes c bounded. On every finite horizon s is locally essentially bounded, hence the Girsanov exponential satisfies Novikov's criterion. With the SAME initial law, controlled and reference un-killed trajectory laws have

 KL(P_controlled[0,T] || P_reference[0,T])
 = (beta/4) E_controlled integral_0^T s(t)^2 c(X_t)^T D^(-1)c(X_t)dt.

This is the standard Brownian change-of-drift action. For stationary initialization pi, received common invariance makes it exactly

 (beta/4) [integral_0^T s(t)^2dt] [integral c^T D^(-1)c d pi].

For conditional-basin initialization the expectation remains explicit and can be upper bounded by the maximum spatial quadratic norm times integral s^2. Stopping/recording at a killed boundary is a measurable data reduction, so the stopped-record relative entropy is no larger; do not assert equality for an arbitrary discarded/censored record.

Thus an amplitude-independent clock-error theorem is compatible with arbitrarily large control action and increasingly distinguishable full trajectories. The invariant measure or potential-energy neutrality does NOT mean zero apparatus power, zero entropy production, free switching, or a physically acquired controller. Translating this mathematical action into joules, force-generator limitations, calibration, bandwidth or noise requires an actual physical device model. None is supplied here.
