# Executed global quaternion oracle with exact certificates and complete fallback
2026-10-29. Author construction, receiving review pending. No new SOS optimization principle or general fast semialgebraic solver is claimed.

## Exact physical feedback representation
For one star edge, the retained probe bank has integers B_ab=sum yz and C_abcd=sum yzuv, indexed by the actually chosen output/input axes, and probe countN. The cumulative estimated loss is
 sum hatdelta(q)=3N/4−(9/4)sum B_ab R_ab(q)−(81/4)sum C_abcd R_ab(q)R_cd(q)
for a unit quaternion q=(w,x,y,z), V=wI−i(xX+yY+zZ), R_ab=Tr(sigma_a V sigma_b V†)/2. Let Q(q)=sum q_i² and use the homogeneous quadratic rotation matrixR(q), e.g.R_12=2(xy−wz). The exact homogeneous quartic
 F(q)=3N Q(q)²−9Q(q)sum B_ab R_ab(q)−81sum C_abcd R_ab(q)R_cd(q)
is FOUR times the cumulative estimated loss on the unit sphere. Thus the90 integer bank coefficients compress to35 quartic monomial coefficients; no environmental density matrix is reconstructed. Empirical minima may be negative because the estimator is signed; this is not negative physical error.

## Fast certificate, not free SDP rounding
Let z2(q) be the10 quadratic monomials. A symmetric10×10 Gram matrix has55 entries; matching the35 quartic coefficients leaves20 linear free parameters. The executable builds that exact affine space by grouping monomial products. It searches for a lower boundlambda satisfying
 F(q)/scale−lambda Q(q)²=z2(q)^T G z2(q), G positive definite.
A custom small log-det Newton search proposeslambda and the20 free parameters. Its floating iterates are NOT evidence of nonnegativity. They are rounded to rationals;lambda is moved down until exact Fraction LDL has strictly positive pivots. The35 coefficient identities are then checked exactly. This proves the lower bound on every unit quaternion.

Separately, multistart numerical minimization proposes a quaternion. It is converted to an EXACT rational unit quaternion through stereographic coordinates, and its objective is evaluated as a rational upper boundU. Only the EXACT interval[lambda,U] certifies global accuracy. No rank extraction or rounding of an SDP matrix into a physical rotation is assumed. If the gap does not meet the requested tolerance, this fast path has not solved the oracle.

The independent `check_certificates.py` does not import the optimizer. It reconstructs the bank polynomial in SymPy, checks the actual rational rotation satisfiesR^T R=I,detR=1, verifies the full Gram identity, and independently factorsG with exact LDL.

## Six executed physical-bank certificates
The one-axis and three-frame-drift60k source trajectories were replayed with their real sampled product probes and retained bath, capturing three star banks each. Each has29,916 probes. All six returned exact mean-estimated-loss gaps between8.66e−11 and1.74e−10. The finder plus exact verification took about0.09–0.30 seconds per bank in this execution, excluding acquisition and interpreter startup. These are SIX instances, not a uniform speed guarantee, online controller deployment or an end-to-end quantum improvement. All source capture programs, banks, rational candidates, Gram matrices and independent checks are preserved.

## A deliberate non-SOS failure
The quaternary quartic f=x²y²+y²z²+z²x²+w⁴−4xyzw is nonnegative by AM-GM and has minimum0 on the unit sphere. It is not a quadratic-polynomial SOS: absentx⁴,y⁴,z⁴ terms force the corresponding diagonal Gram entries and hence their whole PSD rows to vanish. Absentx²w²,y²w²,z²w² terms then force thexw,yw,zw rows to vanish. No remaining monomial pair can producexyzw, contradicting its coefficient−4. This is an exact obstruction, not an inference from a numerical SDP failure.

The executed fast path returns a valid lower certificate near−0.034188 and correctly fails a1e−6 target. Hence neither positivity nor fixed quaternion dimension makes this particular SOS relaxation complete.

## Complete finite fallback and its honest cost
For ANY rational homogeneous quartic f=sum a_alpha q^alpha, put L=4sum|a_alpha|. On the unit ball its gradient norm is at mostL. The rational stereographic gridu=k/m,k in[-m,m]^3 covers the unit sphere moduloq~−q with chord error at mostsqrt3/m<=2/m. Both signs represent the same rotation andf is even. An EXACT exhaustive grid minimumU therefore gives
 U−2L/m <=min_{||q||=1}f(q)<=U.
Choose integerm>=2L/epsilon. The executable `exact_grid_fallback.py` evaluates every rational point and returns that rigorous interval. A configured point-budget limit returns `budget_exceeded_no_oracle_success`, never a false optimizer. An uncapped enumeration is finite and complete; its cost isO((1+L/epsilon)^3) rational evaluations, polynomial in magnitude/inverse tolerance but NOT polynomial in their bit lengths. The4913-point demonstration checks the implementation at modest accuracy; fine fallback may be astronomical.

A total oracle can cap the optional floating certificate finder, verify any proposed fast certificate, and otherwise run this complete enumeration. For finite-horizon controller queries whoseL and1/epsilon are polynomial inT and1/p (in particular fixedp), this gives a finite polynomial-in-those-parameters fallback, potentially WORSE than the completed net learner. Fast empirical certificates are a promising efficiency mechanism, not a proof of improved worst-case or polylogarithmic runtime.
