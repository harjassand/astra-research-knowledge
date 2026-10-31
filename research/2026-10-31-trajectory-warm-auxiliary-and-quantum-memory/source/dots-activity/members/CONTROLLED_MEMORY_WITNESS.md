# A finite-rate controlled-memory witness, not a simulation lower bound

31 October 2026. Analytic candidate for independent check. This is a deliberately elementary one-mode comparison control. It does not require an interacting Kerr term to act, and does not establish a computational advantage.

## Model and exact finite invariant space

A system qubit starts in |e>, and a private reservoir starts in vacuum |0>. Let

    H = g (sigma_minus a^dagger + sigma_plus a),
    J = 2 sqrt(lambda) a, lambda>0, g>0.

The one-excitation space is invariant except for a loss into |g,0>. Thus the same calculation holds for a bosonic mode or a single lossy hard-core register. A diagonal Kerr term U n(n-1) is zero on this invariant space. No approximation or Fock-tail argument is involved.

In the ordered no-jump basis (|e,0>,|g,1>), the amplitude generator is

    A = [[0,-i g],[-i g,-2lambda]].

All jumps land in the absorbing |g,0>, which cannot contribute to a later excited-system measurement. Write tau=1/lambda, delta=g^2/lambda^2, and assume 0<delta<=1/4. Put s=sqrt(1-delta). The exact no-jump propagator at tau has first row (u,-iv), where

    u = exp(-1) [cosh(s)+sinh(s)/s],
    v = sqrt(delta) exp(-1) sinh(s)/s.

Its first column is also (u,-iv)^T. The no-jump state from |e,0> at tau is u|e,0>-iv|g,1>; the unconditional state adds lost weight in |g,0>.

## Two prescribed system interventions

At time tau choose either identity or Z with Z|e>=-|e>, Z|g>=|g>. The reduced system state immediately before and after either operation is exactly

    rho_S(tau)=u^2 |e><e|+(1-u^2)|g><g|.

The two total states differ only by the sign of their system-reservoir off-diagonal coherence; they have the same reservoir marginal too. After another interval tau under the same actual joint dynamics, the final excited-system probabilities are

    P_I = (u^2-v^2)^2,
    P_Z = (u^2+v^2)^2.

This follows by applying the first row of the no-jump propagator to (u,-iv) and (-u,-iv), respectively. A jump before or after the intervention produces |g,0> and cannot later excite the system. Therefore the formulas are unconditional, not normalized postselection probabilities.

Their difference is

    Delta = P_Z-P_I = 4 u^2 v^2.

Since u>=exp(-1) and sinh(s)/s>=1,

    Delta >= 4 exp(-4) delta.

As delta tends to zero,

    Delta = (1-exp(-2))^2 delta + O(delta^2).

At fixed diffusion strength Gamma=g^2/lambda, delta=Gamma/lambda. The effect is algebraically small in the rapid-loss scale, not identically absent.

## Exact excluded replacement class and error bound

Consider a replacement that retains ONLY the system density matrix between slots, applies the consumer's actual I or Z at the slot, and uses the SAME linear CPTP future map Phi for the next interval in both experiments. There is no hidden memory or branch-dependent future map. The replacement is required to approximate the physical process uniformly, including termination or arbitrary measurements at the intermediate slot as well as at the final slot. Use trace norm (not half trace norm) for the uniform error eta.

Let sigma be its state at tau, common before choosing I or Z, and let rho=rho_S(tau). Uniform accuracy entails ||sigma-rho||_1<=eta. Since Z rho Z=rho,

    ||sigma-Z sigma Z||_1<=2eta.

CPTP contractivity gives ||Phi(sigma)-Phi(Z sigma Z)||_1<=2eta. Each simulated final state is within eta of its corresponding exact final state. The exact final system states are diagonal with excited probabilities P_I,P_Z, so their trace-norm distance is 2Delta. The triangle inequality yields

    2Delta <= eta+2eta+eta,
    hence eta >= Delta/2 >= 2 exp(-4) Gamma/lambda.

Equivalently, a scheme agreeing exactly at the intermediate state and retaining no memory cannot distinguish the histories at all. This statement is about one common time-local system-state representation. It does NOT prohibit a history-aware algorithm, a quantum/classical auxiliary memory, an assignment map with a retained transient coordinate, or different scheduled future maps chosen using the intervention history. Those are different representations, and their acquisition and memory costs must be compared honestly.

The requirement of intermediate accuracy is essential: merely fitting two terminal probabilities is not a controlled-process approximation. Nor does this prove a lower bound against all numerical adiabatic expansions. A high-order method that carries the needed correlation/transient information can reproduce this witness.

## Ordinary solution and execution cost

This instance is analytically solved above or by a constant-size matrix exponential. Evaluating u,v to b bits costs polynomial in b and the encoded parameters with standard elementary-function arithmetic. It is NOT a useful quantum-advantage benchmark. It serves only as a source/controls/error test that a proposed memoryless approximation must pass.

For estimating the small probability difference experimentally or by repeated independent simulator runs, the cost of statistical estimation is separate from channel synthesis accuracy. A high-precision channel circuit does not make a scalar expectation available with logarithmic sample count. Likewise the consumer's Z, initial-state preparation and final measurement are real operations, albeit constant-cost here.

The calculation belongs to the accepted vacuum-source and prescribed-control domain. It does not require public bath measurements, adaptive intervention times, thermal initialization or a stationary joint preparation. No conclusion about general Kerr/hopping complexity is inferred from the one-excitation example.
