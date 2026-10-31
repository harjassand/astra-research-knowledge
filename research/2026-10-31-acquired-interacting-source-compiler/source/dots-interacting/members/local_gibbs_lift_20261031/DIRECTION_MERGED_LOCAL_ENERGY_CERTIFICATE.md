# A local-energy return certificate for direction-merged Ising heat-bath jumps

31 October 2026. Author derivation, pending independent review. This is a quantitative certificate for the stated continuous quantum generator, not a new general quantization theorem or an automatically accepted fast-source compiler. Quantization by classical couplings is established machinery (Temme–Wocjan2504.02651v2); the direction-merged realization below is analyzed directly, without presuming its pair-coordinate transform is a positive classical coupling.

## 1. Exact model and acquired local operators

On n binary spins s_i in{+1,-1}, let

    pi(s) proportional to exp[sum_{i<j} J_ij s_i s_j + sum_i h_i s_i],

with finite real fields and symmetric pair interactions. For acquisition below use exactly represented rational coefficients and a bounded-degree interaction graph. Let r_i(s)=pi(s^i)/(pi(s)+pi(s^i)) be the heat-bath flip rate, where s^i flips spin i. Thus the two rates at a fixed neighbor context satisfy r_i(0,z)+r_i(1,z)=1 and detailed balance.

For each context z define normalized vectors

    u_i(z)=(sqrt(r_i(1,z)), sqrt(r_i(0,z))),
    v_i(z)=(sqrt(r_i(0,z)), -sqrt(r_i(1,z))),
    Pi_i=|v_i><v_i|,

with neighbor control implicit. Define the TWO direction-merged jumps per site

    L_i,0=|1_i><v_i|,       L_i,1=-|0_i><v_i|.

The source generator is G=sum_i D_i, where

    D_i(rho)=sum_(a=0,1) L_i,a rho L_i,a^dagger - {Pi_i,rho}.

Each jump has norm1, sum_a L_i,a^dagger L_i,a=2Pi_i, and each annihilates psi=sum_s sqrt(pi(s))|s>. Detailed balance cancels the offdiagonal contributions on diagonal observables, so the adjoint restriction is exactly the continuous classical heat-bath generator with flip rates r_i(s). Operator-valued diagonal observables obey the same identity, receiving the usual prescribed diagonal-algebra-preserving controlled process.

The local neighborhood has degree+1 spins. Its rates and dark vectors are acquired by bounded logistic arithmetic and controlled one-qubit rotations, with all site selection, neighbors and coefficient bits paid. A jump-stack normalization sqrt(2n) is a safe acquired bound. These facts do not require the global partition function or pi_min.

## 2. Parent Hamiltonian and exact self-drift

Set H=sum_i Pi_i. If Q_cl denotes the classical column generator, direct comparison of diagonal entries and spin-flip offdiagonals gives

    H = -diag(pi)^(-1/2) Q_cl diag(pi)^(1/2).

Consequently H has unique zero vector psi and its first positive eigenvalue is the classical reversible gap g_cl. Also H<=n I. This identity alone does NOT prove quantum return.

At fixed context, sum_a <a|Pi_i|a>=1. Hence

    D_i^dagger(Pi_i)=Pi_i-2Pi_i=-Pi_i.                   (1)

If sites i,j are not adjacent, their jumps/projectors commute: each can flip only its own central spin and has only diagonal controls on the others. Thus D_i^dagger(Pi_j)=0 for nonadjacent centers, even when their neighborhoods share a third spin.

## 3. A pairwise cross-drift inequality

Fix adjacent i,j and freeze every other spin. The operators of interest are block diagonal in those frozen spins and act on just the two central spins. Let J=J_ij and remove ONLY that edge to define reference local jumps L_i,a^0,L_j,a^0 and projectors Pi_i^0,Pi_j^0. All external fields, including other neighbors' fixed contributions, are retained.

Write the conditional field as t. For the normalized conditional dark vector v(t), elementary differentiation gives

    ||dv/dt|| = (1/2) sech(t) <= 1/2.

Removing J changes the conditional field by at most |J|. Therefore, uniformly in arbitrary external fields,

    ||L_i,a-L_i,a^0|| <= |J|/2,
    ||Pi_i-Pi_i^0|| <= |J|/2,                           (2)

and likewise for j. The projector bound follows from the rank-one projector angle bound; all jump norms are1.

Let A_ij=D_i^dagger(Pi_j), a Hermitian operator. The edge-removed reference cross drift is zero. For general perturbations delta_i,delta_j in (2), the two recycling terms change in norm by at most4delta_i+2delta_j, and the anticommutator by at most2delta_i+2delta_j. Thus

    ||A_ij|| <= 6delta_i+4delta_j <= 5|J|.               (3)

The kernel of Pi_i+Pi_j is exactly the one-dimensional conditional two-spin Gibbs vector in every frozen-context block. Indeed the two local annihilation equations impose the positive conditional Gibbs amplitude ratio across every edge of the connected two-spin square; consistency is supplied by the Gibbs law. No other solution exists. Both A_ij and its adjoint annihilate this kernel: L_i annihilates it, and both projectors do also.

The reference Pi_i^0+Pi_j^0 has eigenvalues0,1,1,2. Its norm difference from Pi_i+Pi_j is at most |J|. By the min-max eigenvalue bound, for |J|<1 the latter is at least1-|J| on the complement of its actual kernel. Combining this with (3) yields the operator inequality

    D_i^dagger(Pi_j)
       <= [5|J_ij|/(1-|J_ij|)] (Pi_i+Pi_j).            (4)

It holds uniformly over the frozen context, hence on the full Hilbert space and with any tensor reference. No dimension-dependent norm conversion or pi_min was used.

## 4. Summed energy drift and quantum return

Define

    kappa = 1 - 10 max_i sum_(j adjacent i) |J_ij|/(1-|J_ij|).

Assume all |J_ij|<1 and kappa>0. Summing (1) and (4), with both orientations of each edge counted, gives

    G^dagger(H) <= -kappa H.

Positive semigroup comparison then gives e^(tG^dagger)H<=e^(-kappa t)H. Since H>=g_cl Q, Q=I-|psi><psi|,

    e^(tG^dagger)Q <= (n/g_cl)e^(-kappa t) I.

The positive operator on the left annihilates psi, because psi is exactly stationary and pure. Therefore this strengthens to

    e^(tG^dagger)Q <= min{1,(n/g_cl)e^(-kappa t)} Q.     (5)

This is the actual uniform-input quantum pure-return certificate. It does not assert trace-distance mixing merely from an eigenvalue diagnostic. The operator inequality automatically receives arbitrary entangled references as a source-return effect bound.

## 5. An elementary acquired classical-gap lower bound

For these heat-bath rates, changing neighbor j changes the conditional update probability at i by at most c_ij=tanh|J_ij|. Couple two classical chains by rate-one update clocks at each site and common uniform update variables. The expected Hamming distance has drift at most

    -[1-max_j sum_i c_ij] times the current distance.

For a single disagreement, its own update removes it and other sites create disagreements with probabilities bounded by c_ij. The general inequality follows by telescoping the conditional probabilities, or path coupling. Symmetric J makes maximum column and row sums equal. Put

    g0=1-max_i sum_j tanh|J_ij|.

If g0>0, the Markov semigroup contracts the Hamming-Lipschitz seminorm at least as e^(-g0 t). Apply this to a nonconstant eigenfunction of the reversible classical generator: its nonzero Lipschitz seminorm implies its eigenvalue has magnitude at least g0. Thus g_cl>=g0. This is an ordinary Dobrushin/path-coupling argument, not a new classical mixing theorem.

For an open or periodic one-dimensional chain of degree at most2 and |J_ij|<=1/40,

    kappa >= 19/39,       g0 >= 19/20.

Therefore

    t_return = (39/19) ln(320 n/19)

suffices in (5) for a1/16 return effect. Arbitrary finite local fields h_i are allowed; the bound has no pi_min dependence. Constants are deliberately conservative, not optimized or practically benchmarked.

## 6. Acquiring the reference in one dimension

For a known open finite-range one-dimensional Gibbs model, standard transfer-matrix elimination computes suffix partition functions and sequential conditional probabilities. Nearest-neighbor binary interactions use2-by-2 messages. Prepare spin1 according to its marginal, then spin i coherently according to its conditional law given the previous spin and the remaining suffix. Multiplying these conditional amplitudes yields exactly sqrt(pi(s)) in the ideal arithmetic model. The construction is a known coherent version of classical sequential sampling, not an unknown-distribution learner.

Periodic chains can first prepare one spin's marginal, then run the conditional open-chain recursion with that spin retained as a boundary control. Fixed finite interaction range uses a fixed-width boundary register; cost is exponential in that range if it is allowed to grow. No free generic two-dimensional Gibbs sampler is inferred.

For rational input energies, use log-domain messages. Each recurrence is a bounded-size log-sum-exp; write it as max plus log(1+exp(-absolute_difference)). Large negative exponents can be clipped below the allocated tolerance. Exact energies may be large, but their magnitude is represented in binary and no exponentially large partition function is formed. With each message's absolute error at most eta_step, accumulated logit error is O(n eta_step). Square-root probability/rotation state error is bounded conservatively by its square root, so choosing eta_step polynomially smaller than epsilon_prep^2/n^3 gives total state error at most epsilon_prep. Arithmetic and rotation synthesis costs are polynomial in n, coefficient bit lengths and log(1/epsilon_prep), for fixed range. This is an existence/resource construction, not implemented preparation code.

Future source-diagonal coupling means can be block-encoded by compression against the acquired psi. A nontrivial system mean contributes actual sqrt(lambda) action and remains paid; no numerical partition-function expectation oracle or free exact mean-zero test is supplied.

## 7. Receiving limits and prior machinery

The exact source analyzed here is the continuous generator G. It is NOT automatically of the previously accepted form lambda(Phi-I) with an acquired discrete Stinespring channel. Choosing Phi=exp(t0 G) changes the classical event kernel; a finite-time channel's acquired coherent dilation and precision conventions would need a real implementation argument. No circular appeal to the desired fast interacting-source compiler is permitted.

The threshold-environment lift and the random-scan partial-heat-bath collision model being developed separately are different representations with their own certificates. Do not combine this energy bound with their classical laws without proving the interface matches.

Temme–Wocjan, Quantized Markov Chain Couplings that Prepare Qsamples, arXiv2504.02651v2, supplies established quantum coupling machinery; see the separate prior-art correction. Pure-state dissipative engineering and invariant-subspace methods are also ordinary comparators (Kraus et al0803.1463; Ticozzi–Viola0809.0613). The present local energy calculation may be useful as a pi_min-free certificate for this specified realization, but no novelty or advantage over stronger existing rapid-mixing stability methods has been established. Its complete acquisition-to-fast-controlled-simulation consumer remains a separate obligation.
