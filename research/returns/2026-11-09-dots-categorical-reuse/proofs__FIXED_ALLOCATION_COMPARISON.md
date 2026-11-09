# All fixed per-source batch allocations

This separate analytic strengthening concerns the exact empirical-coupling comparator in N1691. It is not a lower bound for arbitrary adaptive stopping rules. Let d>=2 and let r>=1 P records (including the supplied X) and s>=1 Q records be fixed in advance. The new-call budget is r+s-1. Under the N1691 fixed-batch characterization, no alternate processing of these same records has smaller expected disagreement than their empirical total variation.

For P=Q uniform on d labels, put

    t=r+s, u=rs, k=(d-1)/d^2,
    D=Bin(r,1/d)/r - Bin(s,1/d)/s,

where the binomials are independent. Then the optimal disagreement is delta=d E|D|/2. Independent centered Bernoulli moments give

    v=E D^2=k t/u,
    E D^4=3v^2+k(1-6k)(r^(-3)+s^(-3))
          <=3v^2+k(r^(-3)+s^(-3)).

Holder interpolation yields E|D|>=v^(3/2)/(E D^4)^(1/2). Since (r^(-3)+s^(-3))/(r^(-1)+s^(-1))=(t^2-3u)/u^2, this becomes

    delta >= d k t/[2 sqrt(t^2+3u(kt-1))].

If kt>=1, use u<=t^2/4 to obtain

    delta >= [(d-1)/d]/sqrt(1+3kt).

If kt<1, the denominator in the preceding expression is at most 2t, hence delta>=(d-1)/(2d). Thus for any target eta<(d-1)/(2d), delta<=eta necessarily implies

    t >= (d-1)/(3 eta^2) - d^2/[3(d-1)].

At d=16 and eta=1/100, this is t>=49,994+14/45, so the integer total-record count is at least 49,995 and there are at least 49,994 NEW draws. For balanced r=s, t is even, and at least 49,995 new draws are required. These are lower bounds, not claimed exact optimal counts.

The proposed adaptive factory's uniform guarantee at L=100 remains 3,169 expected new calls. This strengthens the comparison from balanced fixed batches to every fixed per-source allocation; it still compares an expected stopping budget to a deterministic fixed-batch budget. It does not exclude a better adaptive categorical construction, establish minimax optimality, or compare actual runtime.

No experiment or numerical calculation has been run to obtain these bounds.
