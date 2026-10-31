# One-bit contrast: conservative general calibration counts are not intrinsic

31 October 2026. Separate author diagnostic derived from the parent's one-bit specialization; pending independent review. It does not change the reviewed general robustness theorem or the executable calibrator, which still uses its general constants.

Consider x'=x xor r on one bit, with iid Bernoulli(p) innovations. F=G=1, m=1; uniform pi is stationary for every p. Compare with p0=1/2. Then

    eta=||Pp-P0||_1=2|p-1/2|,
    P0|Q=0,       Pp|Q=1-2p.

Take centered system Hamiltonians H_+=B, H_-=-B, with ||B||<=b and arbitrary common H0. On two-block CQ space, Pi(X+,X-)=(S/2,S/2), Q(X+,X-)=(D/2,-D/2), where S=X++X-, D=X+-X-. Hence ||Q||=1 in complete CQ trace norm. For q=(Y,-Y), Vq=(-i[B,Y],-i[B,Y]) lies in P, so QVQ=0 exactly. This holds for arbitrary references and regardless of [H0,B]. The QQ semigroups therefore decay at rates lambda and 2p lambda, without a high-rate threshold.

Let gamma=min(1,2p)>0. The same block variation-of-constants proof gives BOTH facing bounds

    ||E_i(t)|range Q|| <= exp(-gamma lambda t)+2b/(gamma sqrt(lambda)),
    ||Q E_i(t)||      <= exp(-gamma lambda t)+2b/(gamma sqrt(lambda)).

Consequently for lambda>0,

    ||E_p(T)-E_0(T)|| <= eta [lambda T exp(-gamma lambda T)
        + 4b(1-exp(-gamma lambda T))/(gamma^2 sqrt(lambda))
        + 4b^2 T/gamma^2].

This can also be minimized with the ordinary bound eta lambda T and with2. It is uniform in system/reference dimension. At lambda0 the two processes coincide.

Using x exp(-x)<=1/e and 1-exp(-x)<=sqrt(x) gives a rate-uniform coefficient

    C_sharp = 1/(e gamma) + 4b sqrt(T)/gamma^(3/2) + 4b^2 T/gamma^2.

For a fully rational conservative coefficient use e>=2 and gamma<=1:

    C_rat = 1/(2 gamma) + 4b sqrt(T)/gamma^2 + 4b^2 T/gamma^2.

An acquired rational upper bound on b sqrt(T) suffices. If calibration is restricted to eta<=1/4, then p>=3/8 and gamma>=3/4, so substitute gamma=3/4 without knowing p. This is a new specialized proof, not an application of an unverified small norm of the general Q perturbation.

Concrete contrast, one interval, b^2 T=1/100, epsilon_model=1/10, delta=1/1024:

    C_rat = 326/225,
    eta_target = min(1/4, epsilon_model/C_rat) = 45/652,
    radius = eta_target/4 = 45/2608.

The same exact rational Hoeffding guard N radius^2>=2(2+10) is satisfied by N=80,613. At the uniform model, the empirical test passes with probability at least1-delta. The general theorem's corresponding sufficient count in calibration_sample_cost_examples.json is489,982,526. Neither number is a lower bound; both are ordinary sufficient estimates from different proven constants. This example shows why the larger general counts must not be interpreted as an inherent sample barrier.

For prescribed interventions, telescope intervals as before. For s intervals with total time T, an optional conservative coefficient is s/(2 gamma)+4b sqrt(s T)/gamma^2+4b^2 T/gamma^2 by Cauchy–Schwarz. Instrument costs and model-promise restrictions remain unchanged. No generic multi-bit improvement, implementation speed claim, or practical quantum advantage follows from this one-bit contrast.
