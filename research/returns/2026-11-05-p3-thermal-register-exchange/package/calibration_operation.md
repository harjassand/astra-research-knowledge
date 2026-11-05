# Acquiring thermal weights without a rare-lifetime experiment

This is an explicit calibration route under the same coherent control and bath-isolation access used for writing. It does not infer the validity of a commuting-Pauli Hamiltonian or Davies bath from finitely many measurements. Those remain model premises. The route is optional when calibrated coefficients are supplied with the device.

Let H=sum_a J_a(I-S_a)/2, with known distinct nonidentity stabilizers, bounded check overlap and J_a in a fixed declared positive interval. Exact duplicate terms can be combined by adding their coefficients; this preserves the Hamiltonian and is not replacement by an independent stabilizer basis. A one-site Pauli P anticommutes with a set B(P) of at most d checks, with d fixed.

Prepare a known ground eigenstate psi_0 with the Clifford encoder, and apply a Pauli R. Let R^dagger S_a R=chi_a(R) S_a. The known eigenstates R psi_0 and P R psi_0 have gap

    Delta_P(R)=sum_{a in B(P)} J_a chi_a(R).

Measure this without controlled-H access: prepare an ancilla in |+>, controlled-apply P, evolve the data under H for time tau, controlled-apply P again, and measure the ancilla's phase. Take tau<=pi/(4 d J_max), so inverse sine is uniformly Lipschitz and there is no phase wrapping. Coherent bath-isolated evolution and known control pulses are charged resources.

In the usual Pauli-Y convention the mean readout is -sin(tau Delta). A fully specified finite-sample estimator is -arcsin(clip(Ybar,[-1/sqrt(2),1/sqrt(2)]))/tau. For M<=m 2^d total settings, n>=4/(tau^2 delta_J^2) log(2M/alpha) shots per setting suffice. Timing and control bias are included in the gap-error budget.

Uniform Pauli R induces a uniform law on the attainable local sign patterns chi_B. There are at most 2^d patterns; binary Gaussian elimination finds each attainable pattern and a representative R. Pauli-character orthogonality for distinct checks yields E_R[chi_a chi_b]=delta_ab. Therefore

    J_a=E_R[chi_a(R) Delta_P(R)], a in B(P).

One anticommuting probe per check, shared where convenient, recovers all coefficients from these local gap measurements. This neither resolves the complete spectrum nor estimates a rare lifetime, generator or marked event law.

Independent projective measurements need O((tau delta_J)^(-2) log(m 2^d/alpha)) repetitions per local pattern to estimate all J_a within absolute error delta_J, with joint failure probability <=alpha. There are O(m 2^d) patterns. At fixed degree, temperature and coupling bounds, delta_J=O(epsilon_cal/m) gives the conservative bound

    O(m^3 epsilon_cal^(-2) log(m/alpha)) Ramsey shots.

Every shot includes its actual Clifford preparation, routing, interrogation, readout and reset. Multiply the shot count by those compiled time/energy/gate costs. This is an explicit polynomial route, not an optimal Hamiltonian-learning claim.

For lambda_a=beta J_a, use the accepted bound

    TV(p_lambda,p_lambdahat)<=min(1,(1/4)sum_a|lambda_a-lambdahat_a|).

If beta needs acquisition, include C_beta(delta_beta,alpha), the cost of a supplied calibrated thermometer, and choose beta delta_J+J_max delta_beta+delta_beta delta_J<=4 epsilon_cal/m. A two-level probe of known gap E_*, whose excited occupation r=(1+exp(beta E_*))^(-1) stays bounded away from 0 and 1 on the declared range, needs O(delta_beta^(-2) log(1/alpha)) independent occupation samples. Its actual relaxation time, access to the same bath and reset/readout costs remain additional hardware parameters. A mere upper bound on BDL bath rates does not guarantee a fast thermometer.

Certified coherent-control or isolation bias is added to each measured gap's error. A polynomial shot count is a full polynomial acquisition cost only if the supplied control and thermometer primitives attain their requested accuracies at the stated paid costs. No constant-rate noisy-gate threshold follows from this argument.

Finite-time thermometer bias and any dependence between its nominal samples also belong in the thermometer access and uncertainty contract; the independent-sample expression does not grant a free bath-mixing bound.

The resulting calibration error and failure probability enter the retained-background register guarantee once. They are not multiplied by passive holding time or by the number of ideal logical uses.
