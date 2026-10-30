# Independent read-off support-window review
30 October 2026. Source ROOT_READ_OFF_QUANTUM_WINDOW.md frozen with SHA 0738762ef6ce33a9d355e604337ca922a66f56ecf8a103c237faa10daa9b1849.

## Scoped verdict
PASS for the finite-dimensional bounded-generator statement, interpreting the actual time-local dynamics as having CPTP propagators on EVERY interval. A CPTP map only from the initial time would be insufficient: the argument requires the instantaneous generator to be a legitimate time-local CP-divisible generator almost everywhere. Piecewise continuous/bounded measurable regularity with the relevant ordered propagators suffices. Infinite-bath or unbounded-generator versions require the expressly retained domain/existence hypotheses.

The construction does not delete signed HP noise and pretend the remainder is CP. Its maximally mixed reduction repairs exactly that issue. The resulting Dyson support bound is bath-volume independent. No source/capture/factory conclusion beyond the stated fixed read-off window is certified.

## Reduced generator
E:rho_B -> I_S/d_S tensor rho_B and R=Tr_S are CPTP with RE=Id. For a legitimate fixed-time generator L, the short-step channel R exp(hL)E has expansion Id+hRLE+O(h²). Its repeated product limit gives exp(tRLE), a CPTP semigroup. Pointwise/time-ordered approximation gives the bounded time-dependent version. This is not a claim that R exp(tL)E equals exp(tRLE) at finite t.

If N_e has S support X_e, R N_e E traces only X_e nontrivially. Therefore Id_S tensor R N_e E has no S action at all, and Delta_e=N_e-Id_S tensor R N_e E has support contained in X_e. Complete trace-norm contraction of E,R gives ||Delta_e||diamond<=2||N_e||diamond. Centering and Hermiticity preservation follow linearly. The reference bath generator itself may be nonlocal or depend on N; only its CPTP contraction, not a locality bound on it, is needed.

## Dyson support
All reference intervals have complete trace norm1 and act trivially on S. Integrating ordered insertion norms yields the exponential series bound A^k/k!. A finite local S matrix-unit expansion of Delta_e establishes the support union statement; its coefficient norms are NOT used to estimate the tail. Keeping those two arguments separate prevents an unnecessary basis-size factor in A.

If the incoming state is supported in the common operator-error module of radius r0, every order k with r0+qk<=r is supported in the radius-r module. This is true for coherent superpositions of locations: the radius-r space is a SPAN, not one selected support set. The low-order sum need not be positive. Its outside trace is zero; the trace of the actual positive state's outside projection is bounded by the remainder norm. The bound exp(A)(eA/K)^K is conservative but valid for K>=A. Arbitrary references are retained.

The positive projected state is within 2sqrt(tail) in trace norm. A map-level version requires an actual encoded/source input channel whose initial common-support premise and norm bounds are uniform over its inputs; it cannot be inferred merely from one chosen state or arbitrary initial logical/bath correlations.

## What still must be received
The abstract radius counts physical S support. The native theorem counts canonical BOTH-CSS-sector DATA weight plus controller/dirty/BUSY quantities. The conversion is finite-footprint and can be made explicit as in READ_OFF_WARM_COMPLETION.md, but no physical support number should be inserted unchanged into the old native energy inequality.

The projected good state's joint quantum/root moment needs a separate argument if its projector does not commute that weight. READ_OFF_WARM_COMPLETION.md supplies a finite-weight-norm/gentle repair for the O(N) boundary-port product. It is not a uniform all-bulk-subset claim.

## Regression
check_reduced_generator.py tested 100 random two-qubit GKSL generators. The induced bath semigroups had minimum Choi eigenvalue 0.0155, trace-preservation residual at most1.22e-16, and the reduced short-step derivative agreed within1.14e-6 at step1e-6. These numerical checks are supplemental channel-calculus regressions; the proof is the product-limit argument above.
