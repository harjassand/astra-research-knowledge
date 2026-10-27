# Exact inverse-trace receiver for scalar or classical reference

27 October2026. Pointwise inverse-trace theorem, distinct from the previously known integrated entropy VALUE. No noncommuting-reference pinching lift is claimed.

For every positive3×3 physical M with TrM=3,

R(M)=TrM^(-1)−2Tr(NM)^(-1)+3≥0,

with equality only at M=I3. No upper bound M≤2I is needed. Consequently the pointwise reverse-logdet inequality also holds by radial integration. Direct orthogonal sums give the same statements for a reference-classical source M=direct-sum_j M_j with TrM_j=3.

## Exact scalar proof

Let the eigenvalues be m1,m2,m3>0, sum3. The physical WH output has eigenvalues(3−m_i)/2. Put e2=sum_(i<j)m_i m_j and e3=m1m2m3. The denominator e3(3e2−e3) is positive, and

R·e3(3e2−e3)=3e2²+4e2e3−36e3−3e3².

Write a_i=m_i−1, sum a_i=0, p=(sum a_i²)/2, q=a1a2a3. Then e2=3−p, e3=1−p+q and the numerator becomes

F(p,q)=4p²+2pq+8p−3q²−30q.

Here0≤p<3. If q<0, put s=−q. Positivity of e3 gives p+s<1, so

F=4p²+8p+s(30−2p−3s)>0.

If q≥0, F decreases strictly with q because ∂F/∂q=2p−6q−30<0. The real-root discriminant inequality for a1,a2,a3, or elementary optimization at fixed sum and square-sum, gives

q≤2(p/3)^(3/2).

Set r=sqrt(p/3)<1. Substituting this upper bound yields exactly

F(p,q)≥F(3r²,2r³)=12r²(1−r)^3(r+2)≥0.

For p>0 the final expression is strictly positive, so equality requires p=0 and all m_i=1.

## Consequences and boundary

For M_s=I+s(M−I),0≤s≤1, the exact radial derivative of

2logdet(NM_s)−logdet(M_s)

is R(M_s)/s, so the pointwise determinant difference is nonnegative and is zero only when M=I. Orthogonal reference-classical sums preserve both R and the logdet difference.

This theorem cannot be extended to general sources by claiming that physical or reference pinching decreases R. The root's exact physical pinching example already disproves that direction. Its role is to receive the genuinely classical stationary/base sector, not to remove coherent reference interactions for free.
