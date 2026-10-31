# Independent review: finite-rate controlled-memory witness
31 October 2026. Reviewer: independent internal mathematical review.

## Source and verdict
PASS. I read the complete actual source
graded_reservoir_comparison_20261031/CONTROLLED_MEMORY_WITNESS.md,
5,638 bytes, SHA-256 bf2a6e56460539c0ecd96aeffc2028ecfbbe56729baa72bd5837efba2691f9d7.
The source hash was independently verified. This is an exact controlled-memory obstruction for a specified replacement class, not a simulation-complexity lower bound.

## Physical amplitudes and unconditional probabilities
With H=g(sigma_minus a^dagger+sigma_plus a) and J=2sqrt(lambda)a, the no-jump amplitude generator in {|e,0>,|g,1>} is exactly [[0,-ig],[-ig,-2lambda]]. The factor two in the amplitude damping is correct for the stated jump convention.

At tau=1/lambda and delta=g^2/lambda^2, s=sqrt(1-delta), direct exponentiation gives
u=e^(-1)[cosh(s)+sinh(s)/s],
v=sqrt(delta)e^(-1)sinh(s)/s.
The matrix is complex symmetric, so its first row and column are both (u,-iv). For the source's 0<delta<=1/4 all displayed real quantities are well defined.

The unconditional state at tau is the no-jump rank-one contribution plus absorbed weight in |g,0>. Tracing the reservoir gives exactly diag(u^2,1-u^2). Identity and the specified Z leave that reduced state unchanged but reverse the relevant joint coherence. Both reservoir marginals also agree.

During the second interval every loss ends in the absorbing |g,0>, so only the unnormalized no-jump amplitude contributes to final system excitation. Applying the first row gives u^2-v^2 after I and -(u^2+v^2) after Z. Squaring yields the stated P_I and P_Z, unconditionally. No branch is normalized on a no-jump event.

## Constants and convention
The population difference is Delta=4u^2v^2. Since u>=e^(-1) and sinh(s)/s>=1,
Delta>=4e^(-4)delta.
The expression is four times exp(-4) times delta, not four times exp(-4delta).

As delta tends to zero, u tends to one and v/sqrt(delta) tends to (1-e^(-2))/2. Hence Delta=(1-e^(-2))^2 delta+O(delta^2), as stated. At fixed Gamma=g^2/lambda, delta=Gamma/lambda.

The exact final states are diagonal, so their TRACE NORM distance is 2Delta; their usual half-trace-distance is Delta. The source consistently uses trace norm for its error eta.

## Restricted replacement and error floor
A replacement retaining only the system state has a common state sigma just before the intervention and uses one common CPTP future map Phi. Uniform intermediate accuracy implies ||sigma-rho||_1<=eta for the true diagonal rho. Since ZrhoZ=rho, ||sigma-ZsigmaZ||_1<=2eta.

Contractivity bounds the separation of the two simulated final states by 2eta. Adding eta error at each final output gives 2Delta<=4eta. Thus eta>=Delta/2>=2e^(-4)Gamma/lambda.

If the intermediate state is exact, the two replacement inputs are identical and their common future cannot distinguish them. The source appropriately uses the weaker Delta/2 bound when both intermediate and final errors are allowed.

The requirement of intermediate accuracy is substantive. A model fitting only selected terminal numbers is not thereby a controlled-process approximation. Conversely, the argument does not rule out a history-dependent future, a classical or quantum auxiliary memory, a retained transient/correlation coordinate, or a higher-order scheme that carries that information. Those do not satisfy the excluded common-state-only representation.

## Boundaries and ordinary comparator
The invariant space is constant dimensional, and its exact matrix exponential or the displayed elementary functions solve the example efficiently. Bosonic and hard-core realizations coincide on this space; a diagonal Kerr term vanishes there. No non-Gaussian computational hardness or general quantum advantage follows.

Channel synthesis precision is different from the sampling cost of estimating a small expectation difference. The witness does not remove preparation, control, measurement or statistical estimation costs. It remains within the vacuum-source, prescribed-system-control domain and makes no thermal, public-bath or adaptive-time claim.

This receipt establishes the exact finite-rate memory effect and the scoped error floor only. It makes no novelty, practical advantage, general adiabatic-method impossibility or algorithmic lower-bound claim.
