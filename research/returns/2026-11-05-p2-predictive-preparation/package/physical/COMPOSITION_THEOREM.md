# A completed forward construction: acquired modules under later convex network assembly

## Status

This is an independently selected forward construction. It turns the accepted scalar passive acquisition operation into a reusable network component interface. It is a theorem and a finite implementation prescription, with an exact algebraic boundary example. It is not a claim of a new foundational passivity principle, a civilization-changing result, or an executed physical network. Existing monotone-system contraction, compositional abstraction, and passivity-preserving reduction machinery substantially anticipates the stability argument.

The accepted scalar construction is used within its conditions. In particular, it supplies finite physical kernel acquisition, a retained-force estimate, finite release, an actual force-delivery port, and a numerical residual contract. It does not supply arbitrary unknown interconnections or hidden-mode resets.

## 1. Endpoint and resources

There are n accessible physical modules. Module i has an observed coordinate x_i, known scalar local law V_i', calibrated unit local drag, and an unknown positive Maxwell measure nu_i on [0,infinity), of mass at most B_i. Its hidden coordinates satisfy

    y_i,lambda' = lambda (x_i-y_i,lambda).

The local visible law is strongly monotone: (V_i'(s)-V_i'(t))(s-t) >= mu_i |s-t|^2, where mu_i >= mu > 0. Local upper curvature/evaluation bounds are supplied on the reachable range. Initial hidden energies and physical meter/actuator contracts are those in the accepted scalar operation. The measures may differ arbitrarily among modules and may contain frozen mass. There is no common-rate, common-kernel, finite-hidden-dimension, or spectral-gap assumption.

Initially, the modules can be calibrated separately through their declared local ports. This isolation is an extra physical resource. After calibration, a known graph of pairwise connectors can be installed. A connector e=(i,j) has potential

    kappa_e(t) Phi_e((x_i-a_i)-(x_j-a_j)),

where kappa_e(t) >= 0, Phi_e is convex, Phi_e'(0)=0, and the finite program, evaluation/curvature bounds, calibration error, force and stiffness slew, attachment/routing, and work are supplied and paid. The rest offset a_i-a_j is physically set. Convexity makes the connector restore differences of the observed displacements. An arbitrary passive multiport does not automatically have this form.

Write u_i=x_i-a_i and

    W_t(x) = sum_i V_i(x_i) + sum_e kappa_e(t) Phi_e(u_i-u_j).

Deployment obeys

    x_i' + partial_i W_t(x) + P_Ki(x_i-a_i) = f_i + g_i,

where K_i(t)=integral exp(-lambda t) d nu_i and P_Ki e=K_i(0)e-(-K_i')*e. The old reference force g_i contains the actual retained hidden state after assembly and release.

## 2. Simultaneous calibration contract

Run the accepted scalar acquisition on each module, allocating failure probability alpha_i with sum alpha_i <= alpha. The sum of all physical exposures, resets of instruments, preparation, memory, and processing is paid. Parallel operation changes wall-clock time only if n sets of the relevant apparatus and independent port reach are actually supplied.

The resulting data are positive finite models Khat_i and certificates

    ||K_i-Khat_i||_L1(0,T) <= zeta_i.

The representation cost is sum_i O(log^2(B_i T/zeta_i)) positive modes and sum_i O(log^3(B_i T/zeta_i)) encoded model bits, plus scale, node, graph, and force-law bits. The previous operation's large experimental costs remain. Allocating alpha_i=alpha/n introduces log(n/alpha) into statistical precision costs. The hidden dimension of each module does not enter the representation count except through the supplied mass/energy parameters.

Acquisition is completed before the topology is selected. The single calibration event is independent of that later choice. The topology and connector schedules must be known to the simulator and must obey the physical connector contract.

## 3. Finite assembly and retained initialization

After each scalar calibration, bring every observed coordinate into a common tube |x_i-a_i| <= delta using its finite trap. Hold there and read each surviving local bath force c_i with finite error eta_i. No connector is present during these force measurements, so the accepted local residual meter is used without an unpriced network-force subtraction.

Next install/ramp the selected connectors from zero to their desired strengths over finite time tau_c while keeping the local traps on. Connector kappa_e remains nonnegative throughout. At a first maximum of u_i, every connector incident on i points inward; at a first minimum it also points inward. Thus the scalar trap tube remains invariant under the assembly, using the same maximum-principle bounds and no extra unknown-bath premise.

If |Phi_e''| <= L_e in the tube, the connector force is at most 2 kappa_e L_e delta. Its programmed-stiffness contribution to force slew is at most 2 |kappa_e'| L_e delta, and its position-motion contribution is bounded using the declared coordinate speeds. Connector switching work is bounded by

    sum_e sup_{|s|<=2 delta} |Phi_e(s)| TV(kappa_e).

Its reference geometry, hardware count |E|, routing, local force tolerances, and per-node sum of force errors are physical costs. More edges can require proportionately tighter per-edge calibration if a fixed total node-force error is desired.

After assembly, release every local trap over finite time tau_r using the accepted smooth release, while starting each actual additive drive. Because the convex pair connectors point inward at a maximal displacement, the uniform observed-coordinate bound becomes

    delta_in = delta + tau_r max_i (G_i + F_ri + |V_i'(a_i)|).

Here G_i is a valid local retained-force envelope, and F_ri includes force delivery error during release. Assembly itself does not increase the common tube. The old-force forecast error at deployment is bounded by

    gamma_i = eta_i + 2 B_i delta + B_i delta_in
              + G_i (b_i + tau_c + tau_r + T)/(e (H_i-b_i)).

The final local hold has duration H_i and measurement support b_i. The extra assembly duration is explicitly in the aging error. The formula uses the same hidden-state solution and lambda exp(-lambda t) <= 1/(e t) as the accepted scalar proof. Very slow and frozen forces remain in c_i.

The whole construction is conditional on the available local ports and connectors. It does not obtain this access by inference from observed correlations.

## 4. Network error theorem

Let qtilde be the actually emitted numerical network path, with qtilde_i(0)=a_i. Define its residual using the acquired models and the actual chosen connector program:

    rho_i = qtilde_i' + partial_i W_t(qtilde)
            + Khat_i * qtilde_i' - f_i - c_i.

Let xi_i bound the total node-force discrepancy in the physical deployment, including local drive, connector, and residual trap errors. Put

    R_i = zeta_i ||qtilde_i'||_infinity + gamma_i
          + ||rho_i||_infinity + xi_i.

Then on the simultaneous calibration/initialization event,

    max_i ||x_i-qtilde_i||_infinity,[0,T]
       <= max{delta_in, max_i R_i/mu_i}.

This bound contains no multiplying factor for node count, graph degree, coupling strength, or graph topology. Those quantities still appear in acquisition, routing, force precision, derivative bounds, and numerical execution. It is not a zero-cost large-network claim.

### Proof

Let e_i=x_i-qtilde_i. The local restoring-force difference is a_i(t)e_i with a_i(t)>=mu_i. For each connector, the mean-value identity gives

    kappa_e [Phi_e'(u_i-u_j)-Phi_e'(q_i-a_i-q_j+a_j)]
       = c_e(t) (e_i-e_j),  c_e(t)>=0.

This identity also holds with a secant slope for a strongly monotone nonsmooth derivative wherever the equations are interpreted appropriately; the implementation contract uses locally Lipschitz forces.

The error equation is therefore

    e_i' + a_i(t)e_i + sum_{j adjacent i} c_ij(t)(e_i-e_j)
          + P_Ki e_i = r_i(t),       |r_i|<=R_i.

Take M larger than delta_in and every R_i/mu_i. At a first crossing e_i(t)=M, every other current e_j<=M, and every past e_i(s)<=M. Consequently,

    sum_j c_ij(e_i-e_j) >= 0,
    P_Ki e_i >= [K_i(0)-integral_0^t (-K_i'(s))ds]M
              = K_i(t)M >=0.

Hence e_i'(t)<=R_i-mu_i M<0, which excludes the crossing. Apply the same argument to -e for the lower barrier, and let M decrease to the asserted maximum. Integrability of -K_i' follows from positivity and total mass <=B_i, even if its value at zero is infinite. Standard limiting/barrier arguments handle nonsmooth time points of finite schedules. This proves the theorem.

## 5. Quantifiers and useful deductions

The calibration event supports every later graph and finite connector/force program satisfying the declared class and error budgets. It need not be chosen before calibration. Actual assembly, initialization uncertainty, finite input delivery, and numerical residuals must be recomputed for the selected program; they are not held fixed while physical costs change.

For maximum-node safety specifications, any margin larger than the certificate transfers directly to the connected physical system, without a sqrt(n) loss. The result permits local component calibration followed by system-level counterfactual planning. Each physical deployment consumes its prepared state. A second physical run needs a new declared preparation/initial-force measurement, while purely numerical queries reuse the acquired models.

Even time-varying additions and removals of convex connectors satisfy the comparison as long as kappa_e>=0 and the simulator uses the same known program. Such changes are active physical operations and their switching work and metrology are charged; passivity is not claimed for cost-free time-varying stiffness.

## 6. Finite numerical implementation and cost

On a step of length Delta with candidate endpoint Q, use constant coordinate slopes v_i=(Q_i-q_i)/Delta. Each retained convolution state updates exactly by the exponential formula in the accepted compiler, enclosed at finite rational precision. Form the diagonal coefficients

    A_i=1/Delta + sum_j w_ij psi(lambda_ij Delta),
    C_i=sum_j w_ij exp(-lambda_ij Delta) r_ij.

For a fixed connector program over the endpoint evaluation, solve

    A_i (Q_i-q_i) + partial_i W_{t+Delta}(Q)
       + C_i - f_i(t+Delta)-c_i = 0.

This is the gradient equation of a strongly convex function of Q. Its strong convexity is at least 1/Delta+mu. A local/global upper curvature bound on the reachable box is at most

    L_step = 1/Delta + B_max + L_V,max
             + 2 max_i sum_{e incident i} kappa_e L_e.

Projected gradient descent on a certified enclosing box, or any certified strongly convex solver, reaches a prescribed endpoint residual in finite work. With exact-or-bounded-error gradients and a standard step 1/L_step, the contraction factor is at most 1-(1/Delta+mu)/L_step; finite evaluation/rounding errors are allocated below the desired final residual. A safe iteration count is proportional to

    [L_step/(1/Delta+mu)] log(initial_error/target_error).

One gradient evaluation costs O(n+|E|) known local/connector force evaluations. Per-step modal work is O(sum_i m_i), and per-step nonlinear-solve work has the displayed condition-number factor. No efficient general-purpose nonlinear solver is assumed as an oracle.

A within-step residual is bounded by endpoint residual plus Delta times a bound on its derivative. The i-th row Lipschitz constant is

    L_row,i = L_V,i + 2 sum_{e incident i} kappa_e L_e.

Thus the accepted scalar residual formula applies with L replaced by L_row,i, plus the known explicit-time term sum_e |kappa_e'| sup|Phi_e'|. The retained rate moment sum_j w_ij lambda_ij is finite and explicitly charged. Refining time steps and arithmetic terminates for every supplied computable piecewise-Lipschitz force/connector schedule and locally Lipschitz force laws on the certified compact reachable set.

For bounded degree/curvature and fixed error, the per-step work is linear in the number of retained modes, nodes, and edges up to solver iterations. Dense graphs, strong edges, stiff retained rates, small error, and expensive force-law evaluation retain their actual costs.

## 7. Strong convexity alone does not supply this local-error law

The absence of node-count amplification is not a consequence of strong convexity by itself. There is an exact counterexample with no hidden memory and uniformly bounded visible curvature.

For integer s>=1 set n=s^2+1 and

    v=(1/sqrt(2), 1/(sqrt(2)s),...,1/(sqrt(2)s)),
    H=I+v v^T,  V(x)=0.5 x^T H x,
    r=(1,-1,...,-1).

Then ||v||_2=1, so I<=H<=2I. All entries of H are rational for this choice of n. Compare the zero trajectory with the force-perturbed system

    e'=-H e+r,   e(0)=0.

At T=log(2), functional calculus gives

    e(T)=0.5 r - 0.125 v v^T r,
    e_1(T)=(s+7)/16.

The per-node force error is one, mu=1 and the smoothness bound is two, but the first-coordinate error grows as sqrt(n)/16 at a fixed time. For n=257 it is 23/16>1. The potential is fully known and the example has no acquisition difficulty; the failure is contextual amplification. Convex pairwise-difference coupling has the required order structure and excludes this example.

This is an organizing diagnostic, not a new contraction theory. The example shows exactly which broader statement the network theorem does not claim.

## 8. Comparison and selection verdict

Ordinary monotone-system and non-Euclidean contraction theory already provide the finite-dimensional maximum/separable-barrier principle. Compositional simulation functions and dissipativity methods already transfer local approximation relations to interconnected systems. Passivity-preserving model reduction already treats subsystem and overall stability, often with error or gap-metric bounds. The present theorem adds the accepted physically acquired, unknown-dimensional Maxwell-module contract and a finite assembly/reuse account at its particular order-preserving interface.

This is a complete conditional network extension and a useful boundary. Its stability mechanism is strongly anticipated by established methods. The construction does not warrant elevation to a broad new foundational law or the requested civilization-changing endpoint by itself. It should remain a preserved independent attempt unless a stronger route consumes its physical interface for an additional consequence.

Primary comparisons:

1. S. Coogan, A Contractive Approach to Separable Lyapunov Functions for Monotone Systems, Automatica 106 (2019), 349-357; https://arxiv.org/abs/1704.04218 ; author PDF https://coogan.ece.gatech.edu/papers/pdf/coogan2017contractivemonotone.pdf .
2. A. Swikir, A. Girard, M. Zamani, From dissipativity theory to compositional synthesis of symbolic models; https://arxiv.org/abs/1710.05585 .
3. L. Poort, B. Besselink, R. H. B. Fey, N. van de Wouw, Passivity-Preserving, Balancing-Based Model Reduction for Interconnected Systems; https://arxiv.org/abs/2311.13214 .
4. C. Guiver, M. R. Opmeer, Error bounds in the gap metric for dissipative balanced approximations, Linear Algebra and its Applications 439 (2013), 3659-3698; https://doi.org/10.1016/j.laa.2013.09.032 .
5. S. Chaturantabut, C. Beattie, S. Gugercin, Structure-Preserving Model Reduction for Nonlinear Port-Hamiltonian Systems, SIAM J. Sci. Comput. (2016); https://doi.org/10.1137/15M1055085 .

No novelty claim is made for positivity-preserving exponential compression or for the general principle of compositional error bounds. The scalar acquisition's generalized-Langevin and N1688 comparisons continue to govern its reused operation.
