# An actual sublinear landing layer, rather than a fictitious central entry

This is an additional constraint and receiving calculation for the unit-rate blocks with the conservative pair2/1. Start at the star's actual unclean output

    x_n=(3,2,2,1,n+1,n).

Until the first noncore event sigma, B=C and E,F=n+O(1)-B. In the range B=o(n), genuine rates have

    core up g=3(E)_2(F)_2 ~3n^4,
    core down f=6(B)_2(C)_2,
    terminal h_T=f,
    other noncore h_O=O(n+B^2).

For every fixed 0<epsilon<1/5,

    P[n^(4/5-epsilon)<=B_(sigma-)
                       <=n^(4/5+epsilon),
      first noncore source is I3] ->1.                    (L1)

The terminal output subtracts2 from B,C, so has the same exponent. In particular a phase3 overlap does NOT generally enter a reference-central band of size proportional to n before its first noncore event.

## All-path bounds proving the layer

Take a=2 n^(4/5-epsilon), b=n^(4/5+epsilon), with integer/parity rounding. Pure-core drift of B is >=c n^4 until a, giving E tau_a<=C a/n^4. The probability of ANY noncore event before that pure-core hit is at most

    C[a^5/n^4+a^3/n^4+a/n^3]=o(1).                       (L2)

This is the actual killed coupling estimate, not a stationary approximation. Once at a, falling below a/2 before reaching b or stopping has exponentially small probability: throughout B<=b the down/up ratio is at most r_n=C(b/n)^4->0, and r_n^(B/2), killed at sigma, is a nonnegative supermartingale. The lower-bound crossing probability is at most r_n^(a/4+O(1)).

For the upper tail, in B in [b/2,b] the terminal/up ratio is at least c(b/n)^4. Reaching b requires at least b/4+O(1) upward transitions from that interval. The stopped process

    [1+c(b/n)^4]^(number of those upward transitions)
          *1_(no noncore event yet)

is a nonnegative supermartingale: its upward gain is paid by h_T, and every other noncore event only decreases it. Thus

    P(tau_b<sigma)<=exp[-c b^5/n^4].                     (L3)

All downward paths and arbitrary repeated visits are included. Equations(L2),(L3) and the down/up supermartingale prove the count bounds in (L1). The terminal-source probability tends to1 by the already proved twin-hazard guard argument (or by integrating h_O/h_T above the lower guard).

There is also a paid physical mean bound

    E sigma<=C n^(-16/5+epsilon)+exp[-c n^(5epsilon)]/2.  (L4)

Indeed stop at sigma or tau_b; its mean is bounded by the pure-core mean hit Cb/n^4. On the exponentially rare tau_b-first branch, the genuine constant total zero-source hazard2 pays the remaining mean by1/2.

This layer is useful because it shows exactly why the clean-band activation proof cannot be reused at phase3. The terminal-port construction instead receives this actual unbounded, noncentral landing and sends it to the earned phase1 star operation. No equilibrium, fixed landing profile, or infinite-rate passage is substituted for the physical process.
