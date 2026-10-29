# Independent review of the root reversal projection theorem

29 October 2026. Reviewer: producer-workspace/causal_information_frontier.
Reviewed ordinary draft: ../REVERSAL_PROJECTION_AND_LOCAL_THERMALIZATION.md,
Sections 1--4 as present during this review. Later changes need review at their
new load-bearing uses. This review is mathematical and scoped; it does not
establish historical priority, a thermal implementation, a source acquisition,
or a general analytic existence theorem for diffusions.

## Conclusion

The finite-CTMC theorem, its exact Pythagorean identity, sharp scalar rate
constant, bounded Jensen--Shannon preparation term, and conditional odd-sector
thermalization implication are correct at the stated scope. I found no
substantive mathematical gap in those statements. The diffusion extension is
correct subject to the explicitly required well-posedness, physical reversal,
common covariance, Girsanov range/absolute-continuity and integrability
conditions; I did not independently establish those analytic hypotheses for
an arbitrary coefficient family. The surrogate is not automatically in a
fixed native Maxwell-bath/velocity-independent-force class.

## 1. Stationarity and generalized detailed balance

For source stationary flux f_xy=rho_x L_xy, write g_xy=f_(theta y,theta x),
F=(f+g)/2, mu=(rho+rhoTheta)/2 and Lbar_xy=F_xy/mu_x.
Both f and g are divergence free. Hence F has matching row/column sums and
mu is stationary. F is theta-transpose invariant and mu is theta invariant.
If s_x=sum_y F_xy, theta-transpose invariance plus balance gives
s_(theta x)=s_x. Thus Lbar's paired escape rates are equal. The holding-time
factors are therefore included in physical path-reversal invariance; the
argument is not merely an edge-flux check. Lbar contains every source edge
and is irreducible whenever L is.

## 2. Scalar quarter bound reconstructed

For p,q>0, a,b>=0 and m=(pa+qb)/(p+q), the claimed inequality

    p d(a||m)+q d(b||m)
       <= [p d(a||b)+q d(b||a)]/4

is valid. Independently putting s=pa+qb, alpha=p/(p+q), r=pa/s gives
left/s=D_B(r||alpha). The right numerator/s is exactly the root's J(r).
Direct differentiation gives (J-4D_B)''=(2r-1)^2/[r^2(1-r)^2], with value
and first derivative zero at r=alpha. Thus the inequality follows from
convexity; zero rates are covered by the extended limits. Near a=b with
p=q, the ratio tends to 1/4.

Applying it to the row rates of L and L^R is legitimate because Lbar is
their occupation-weighted arithmetic mean. Physical path reversal maps
the ordered pair of stationary path laws into the reversed ordered pair,
so their two KL rates coincide. It similarly gives equal rates from each
law to the reversal-invariant surrogate. Therefore I<=sigma/4.

## 3. Pythagorean identity reconstructed without a hidden symmetry step

Let H be any irreducible stationary theta-reversible CTMC on the SAME
state set and theta, with stationary nu and stationary flux G_xy=nu_x H_xy.
Put

    a_xy=log(F_xy/G_xy),      b_x=log(nu_x/mu_x).

The first is theta-transpose even and the second theta even. For any such
edge function a, sum f a=sum F a by averaging its theta-transpose.
For any theta-even state function b, the needed identity is

    sum_x (sum_y f_xy) b_x
       = sum_x (sum_y F_xy) b_x.                          (R1)

Indeed the g contribution is sum_xy f_xy b_(theta y)=sum_xy f_xy b_y,
which equals sum_xy f_xy b_x by stationary flux balance. This is the
precise reason for (R1); theta-evenness alone without balance would not
suffice.

Now expand d(L||H)-d(L||Lbar). Its jump term is sum f(a_xy+b_x).
The two identities above replace this by sum F(a_xy+b_x). Its escape
term is sum rho(lambda_H-lambda_Lbar). Both escape functions are theta
even, so rho can be replaced by mu. The resulting expression is exactly
the rate D(Lbar||H). The initial-law identity follows because
log(mu/nu) is theta even. This proves the full finite-horizon Pythagorean
identity, not only a stationary rate projection.

All source-to-surrogate KL terms are finite for the finite positive rho
setting: Lbar_xy is positive whenever L_xy is. If H has a relevant zero
edge, its theta-reversed paired zero makes both cross divergences infinite
consistently. The finite-case identity is sufficient for the minimization
statement, with the extended convention handled as in the draft.

The projection is over stationary theta-reversible Markov laws on this
specified microscopic state space. It is not a data-only projection over
arbitrary hidden explanations or Hamiltonians. This qualification is
essential and already stated in the root draft.

## 4. Boundary, odd-sector form and diffusion checks

D(rho||mu)=D(rhoTheta||mu), so it is the symmetric JS divergence and at
most log2. This is not B=D(rho||rhoTheta), which may diverge. The process
with generator Lbar is the Markov projection of the equal forward/reverse
mixture; the mixture itself need not be Markov.

For a symmetric Dirichlet form commuting with theta, the odd and even
square-root density components are form orthogonal. Therefore
lambda_odd ||f_-||^2 <= E(f_-,f_-) <= E(f,f), and
||f_-||^2=(1-affinity)/2. This yields 1-affinity<=2E/lambda_odd.
Combining the ACTUAL domination sigma>=4E yields the stated bound.
The scalar second-derivative check JS<=1-affinity is also correct.
This uses no even-sector gap and does not infer a gap from observed decay.

For the diffusion part, the occupation-weighted drift gives a stationary
mixture density because the Fokker--Planck equation is linear in density
and current with the common covariance. The stationary physical-reversal
identity makes the weighted drift reversal invariant. In the noise range,
the quadratic Girsanov cost obeys the stated quarter bound by
rho q/(rho+q)^2<=1/4. The root explicitly retains the missing analytic
conditions. In kinetic Langevin, equal forward/reversed position drift
makes the mixture preserve dq=M^-1 p dt; it does not force the new momentum
drift to be a velocity-independent conservative force with the old bath.

## 5. Independent executable controls

check_reversal_projection_exact.py was written independently of the root
exploration code. It uses Fraction arithmetic and prime-log coefficient
representations, not floating approximations. Three nonuniform-parity cases
on 3, 4 and 5 states check:

- stationary source, reverse, surrogate and comparison-generator laws;
- paired surrogate escape clocks;
- exact cancellation in initial-law and rate Pythagorean identities;
- equal forward/reverse rates and equal rates to the surrogate.

All checks passed. The execution result and executed source hash are in
REVERSAL_PROJECTION_EXACT_REVIEW_CHECKS.json. These finite controls support
the reviewed formulas; the general acceptance above rests on the ordinary
argument, not enumeration or a physical experiment.
