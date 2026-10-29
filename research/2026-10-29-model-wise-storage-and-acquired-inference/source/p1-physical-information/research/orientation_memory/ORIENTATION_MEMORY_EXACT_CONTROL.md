# Exact control for orientation memory with a constant microscopic clock

29 October 2026. Complementary executable control for root's orientation-memory construction. No trajectories were sampled and no equipment was operated.

## Verdict

The proposed 2n-state sustained reversal-divergence formula and the 4n-state constant-clock formula both check. The exact control uses a nonuniform stationary law and unequal native escape rates. It verifies stationarity, irreducibility, physical reversed support, generator intertwining for the bit projection, and the complete path-KL decomposition.

The decisive scope condition is that the stationary lifted law is NOT invariant under the physical reversal involution. Consequently

    D(P_lift[0,T] || physical_reverse(P_lift[0,T]))
      = B + T sigma,

not merely T sigma. The rate can approach zero while B diverges. The construction does not make the full finite-window reversal divergence small.

## 1. Nonuniform nonequilibrium input

Use row-generator convention and

    pi = (1/2, 1/3, 1/6),

    Q = [[-1/2,  1/3,  1/6],
         [ 1/4, -3/4,  1/2],
         [ 1,    1/2, -3/2]].

The escape rates are (1/2,3/4,3/2). The three clockwise stationary fluxes are 1/6 and the reverse fluxes are 1/12, so pi is stationary, Q is irreducible, and its ordinary all-even entropy rate is

    sigma_ordinary(Q) = (1/4) log 2
                     = 0.17328679513998632735430803... .

Thus the fixture does not obtain cancellations by assuming uniform pi or one common original clock.

The chosen reserve gives

    Lambda = max_x lambda_x + 1 = 5/2,
    c_x = Lambda-lambda_x = (2,7/4,1).

Rates are numerical values in the stated model time unit. With a general reserve rate rho>0, replace the added one by rho and the condition kappa<1 by kappa<rho.

## 2. Orientation lift and the boundary term

Write u=1-epsilon, v=epsilon, d=u-v, a=kappa v, b=kappa u.

The plus orientation runs Q, the minus orientation runs the stationary adjoint Q*, and orientation changes preserve x:

    plus -> minus at a,
    minus -> plus at b.

The stationary law is mu(x,+)=u pi_x, mu(x,-)=v pi_x. The involution Theta exchanges orientations and leaves x unchanged. Every original observable g(x) is Theta-even.

For a finite stationary generator L with stationary mu, its physically reversed process starts from Theta mu and has generator

    R = Theta L* Theta.

The general likelihood identity is

    D(P_L^mu[0,T] || P_R^{Theta mu}[0,T])
      = D(mu || Theta mu)
        + T sum_z mu_z [
            sum_{w!=z} L_zw log(L_zw/R_zw)
            + lambda_R(z)-lambda_L(z)].

In this lift the real Q/Q* transitions are unchanged in R, while the orientation rates a,b are exchanged. The switch-log contribution is zero because

    u a log(a/b) + v b log(b/a) = 0,
    u a = v b.

The holding contribution is

    u(b-a)+v(a-b) = kappa d^2.

The initial parity divergence is

    B = u log(u/v)+v log(v/u)
      = d log(u/v).

Therefore the sustained rate is exactly

    sigma_orientation = kappa(1-2epsilon)^2.

This calculation must retain holding terms. Dropping them because both processes are stationary would be incorrect: they have different stationary distributions, and their escape rates at the same oriented state differ.

## 3. Constant-clock bit lift

Duplicate every oriented state z with a bit r in {0,1}. Preserve that bit on every real transition of the orientation lift. Add a bit toggle at rate

    Lambda-lambda_L(z).

Since c_x>=1 and kappa<1, every toggle rate is strictly positive. Every microscopic escape rate is now exactly Lambda. The stationary distribution is mu(z)/2, and Theta changes orientation while preserving the bit.

Let J map functions on oriented states to functions constant on their two bit copies. The checker verifies the exact matrix identity

    L_clock J = J L_orientation.

The stationary law also projects to mu. The exponential power series then gives

    exp(t L_clock) J = J exp(t L_orientation)

for every t. Strong lumpability yields the same entire projected orientation path law, hence the same visible g(x) path law. This is not just a match at selected lags.

## 4. Where the sustained divergence moves

Physical reversal of the constant-clock process still exchanges a and b, but now it also exchanges the two invisible toggle rates

    r_+(x)=c_x-kappa epsilon,
    r_-(x)=c_x-kappa(1-epsilon).

The real-transition contributions remain zero. Switch logs cancel as before. All holding terms are zero because both physical directions have the same clock Lambda. The remaining toggle contribution is

    sum_x pi_x [u r_+(x)-v r_-(x)] log[r_+(x)/r_-(x)].

The bracket equals d c_x. Therefore

    sigma_clock
      = sum_x pi_x d c_x
          log[(c_x-kappa epsilon)/(c_x-kappa(1-epsilon))].

The boundary divergence remains exactly B. The bit changes where the sustained path-likelihood cost appears; it does not remove the preparation asymmetry.

For 0<epsilon<=1/2,

    log[(c-kappa epsilon)/(c-kappa(1-epsilon))]
      = log[1+kappa d/(c-kappa(1-epsilon))]
      <= kappa d/(c-kappa(1-epsilon)).

Using c>=1 gives

    sigma_clock <= kappa d^2/(1-kappa).

For a reserve rho rather than one, the dimensionally explicit bound is

    sigma_clock <= kappa d^2/(1-kappa/rho).

The opposite inequality sigma_clock>=kappa d^2 follows from the same log ratio written as an integral; it is also certified by the intervals for all three executed cases. Both rates tend to zero as kappa tends to zero.

## 5. The visible finite-horizon coupling

Start the target Q process and the lifted process from the same x with distribution pi. With probability 1-epsilon the lift starts in its plus orientation. On that event, couple the x dynamics exactly to Q until the first orientation switch.

That first plus-to-minus switch has constant hazard a=kappa epsilon, independent of x. Consequently

    TV(P_visible_lift[0,T], P_visible_Q[0,T])
      <= epsilon+(1-epsilon)(1-exp(-kappa epsilon T)).

The bit lift leaves the visible law unchanged. Every further deterministic observation g contracts this distance.

The code verifies the exact initial wrong-orientation mass and the constant plus-to-minus hazard used by this analytic argument. It evaluates the displayed upper bound with certified rational exponential intervals. It does not estimate an actual path TV distance by samples or claim equality in the coupling bound.

## 6. Executed finite controls

The checker used epsilon=kappa in {1/4,1/16,1/64}. Every orientation model has 6 states; every constant-clock model has 12 states and escape rate 5/2 at every state.

| epsilon=kappa | sigma_clock, displayed approximation | B, displayed approximation | T=10 visible-path TV upper bound |
|---|---:|---:|---:|
| 1/4 | 0.0677177278841 | 0.549306144334 | 0.598553928611 |
| 1/16 | 0.0487837334613 | 2.369543925964 | 0.098415060995 |
| 1/64 | 0.0147337252321 | 4.013661766192 | 0.0180253279973 |

The JSON contains outward-rounded certified intervals; these short table entries are only readable summaries.

For epsilon=kappa=1/64, the full hidden physical-reversal KL on T=10 is strictly greater than 4.1609990185, even though the sustained rate is below 0.014733725233 and the visible path law is within the displayed coupling bound of the original Q law. This explicitly checks the boundary-versus-rate distinction.

The orientation eigenfunction, with value epsilon on plus and -(1-epsilon) on minus, has eigenvalue -kappa in both lifts. The orientation relaxation time is therefore 1/kappa. The mean plus-orientation sojourn is 1/(kappa epsilon): 16,256,4096 for the three controls. The fixed microscopic escape clock does not bound either of these memory scales.

## 7. Exact arithmetic and replay

Run

    python3 check_orientation_memory.py

from this directory, or use its absolute path.

All generator identities use Python's standard-library Fraction. Logarithms of positive rational arguments are expanded into rational coefficients of log(prime); equality of those coefficient dictionaries proves the claimed log cancellations exactly. A range-reduced atanh series gives rational enclosing intervals for the surviving logarithms. Exponential bounds use a Taylor remainder with known sign, and decimal endpoints are rounded outward.

The result files are:

- ORIENTATION_MEMORY_EXACT_CHECKS.json: checks, certified scalar intervals, and scope.
- ORIENTATION_MEMORY_EXACT_GENERATORS.json: all exact 6-state and 12-state generators, stationary laws, and reversal involutions.
- check_orientation_memory.py: generic lift and likelihood routines plus this nonuniform input.

The executable controls establish the finite identities for the three named parameter pairs. The general formulas, semigroup implication, and path coupling are ordinary proofs stated above; script success is not a substitute for those arguments.

## 8. Scientific reach and limits

For each fixed finite Q and each fixed finite horizon, epsilon and kappa can decrease so that the visible law approaches Q's while the sustained physical-reversal-divergence rate approaches zero. The state count 4n and common microscopic escape ceiling max(lambda_Q)+1 stay fixed.

The resources that diverge include the initial parity divergence B, the orientation memory scale, inverse rare-switch rates, and possibly the cost of preparing independent stationary records. The smallest stationary mass also tends to zero. No acquisition of these hidden parameters or the biased stationary preparation follows from observing the original coarse process.

This is a mathematical completion construction. It does not assert a native Hamiltonian implementation, local-detailed-balance realization of all rates, a heat or work cost, or an equipment protocol. A thermodynamic interpretation needs the corresponding physical assumptions. It also cannot be substituted into earlier theorems assuming Theta-invariant stationarity without paying the boundary term and rechecking their intervention assumptions.
