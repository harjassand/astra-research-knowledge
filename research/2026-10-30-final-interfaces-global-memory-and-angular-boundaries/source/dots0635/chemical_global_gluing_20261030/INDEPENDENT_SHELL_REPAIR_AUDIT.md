# Independent audit: exact conservative-shell repair

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review only.

## Verdict

The exact stationary profile and all stated neighboring-shell bounds pass. Constants are loose but correct. Endpoint enabling is valid for every N≥3 and B≥4; no mixing, spectral-gap, deterministic-equilibrium, or averaging premise is used. Connector feedback remains unproved.

## Exact rates and endpoints

At a=A,c=N−a, the increasing-A contributions are 6(c)_3, a(c)_2, and 7(a)_2 c, apart from the common factor (B)_4. Their sum is cP_N(a). At a+1 the decreasing-A contributions sum to (a+1)Q_N(a), exactly as stated. Consequently detailed balance gives w_N(a+1)/w_N(a)=[(N−a)/(a+1)]P_N(a)/Q_N(a), yielding the binomial-product formula.

For j=0,...,N−1, put p=c−1≥0 and q=j≥0, so p+q=N−1≥2. The terms X=p(p−1), Y=pq, Z=q(q−1) are nonnegative integer quantities. They cannot all vanish: if p,q≤1 then p=q=1 and Y=1; otherwise X or Z is positive. Thus all P_N,Q_N are positive. All interior birth/death edges are enabled. At a=0 the outward death rate is zero and birth is positive; at a=N the outward birth rate is zero and death is positive. The fast chain is irreducible on the full finite shell and its normalized detailed-balance distribution annihilates the fast adjoint, including endpoints. N<3 is intentionally excluded because its fast chain degenerates. The factor (B)_4 is strictly positive for B≥4 and changes time only.

## Uniform product comparisons

The coefficient ratios for (X,Y,Z) in P/Q are (1/2,1,7), giving 1/2≤P/Q≤7. Also

    X+Y+Z=(N−1)²−pq−(N−1)
           ≥(3/4)(N−1)²−(N−1)
           ≥(N−2)²/2

for N≥3. Thus both P,Q have the stated lower bound. At fixed j their N-increments are exactly 12(c−1)+j and 24(c−1)+j. Bounding these by 12N and 24N and using N²/(N−2)²≤9 proves the ratios 1+216/N and 1+432/N.

For each product factor, its N-to-N+1 ratio lies between (1+432/N)^−1 and 1+216/N. There are a≤N factors. The inequalities (1+s/N)^N≤e^s give the product bounds e^−432 and e^216. Multiplication by the exact binomial ratio proves the same-a comparison. Multiplying once more by the exact shell-(N+1) birth/death ratio cancels N+1−a and gives the a-to-a+1 comparison, including a=N.

## Normalization and explicit normalized constants

Summing the same-a lower bound over a=0,...,N gives Z_(N+1)≥e^−432 Z_N. On the lower half of shell N+1 the same-a upper factor is at most 2e^216. On the upper half the comparison to shell-N state a−1 is at most 14e^216. Summing each half against its corresponding subset of shell-N weights and bounding each subset by Z_N gives the valid upper bound 16e^216 Z_N. A possible shared shell-N midpoint state does not invalidate this bound.

Consequently the normalized inequalities can be written explicitly as

    (e^−648/16) (N+1)/(N+1−a)
      ≤ sigma_(N+1)(a)/sigma_N(a)
      ≤ e^648 (N+1)/(N+1−a),

and

    (e^−648/32) (N+1)/(a+1)
      ≤ sigma_(N+1)(a+1)/sigma_N(a)
      ≤ 7e^648 (N+1)/(a+1).

These constants are independent of N,a,B. On compact interior composition intervals the rational factors are bounded above and below, as claimed. The estimates permit exponentially unequal weights at distant points on the same shell; they concern neighboring shells and specified neighboring compositions only.

## Scope

Multiplying sigma_N by any N,B-dependent weight still cancels the fast conservative adjoint exactly, because N and B are conserved by those reactions. This provides a genuine replacement for the failed frozen fast-composition diagonal. It does not determine the sign of the remaining connector adjoint, nor establish a compatible radial/B envelope, nor solve multidimensional conservative-face comparisons. The manuscript preserves these distinctions correctly.

Reviewed source SHA-256: `554616569f57ea0b052ccd0e633f2b2dd6c2711ffdd1557ebdaf8a3f9fdd228a`.
