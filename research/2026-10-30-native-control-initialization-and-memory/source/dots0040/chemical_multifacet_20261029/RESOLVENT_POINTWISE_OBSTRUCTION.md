# A bounded killed-shell inverse does not supply a pointwise comparison

Status: internally derived analytical example, unreviewed.

Consider the weakly reversible network A→B→0→A, all rate1, with the additional reverse edge B→A of rate1. The positive normal w=(1,1) exposes face{A,B}. Its killed shell on a+b=n retains A→B and B→A and kills upon B→0. In coordinate b its rates are

    b→b+1: n−b; b→b−1: b; kill: b.

Starting at allA, this is n independent two-state particles, stopped at the first particle death, where each particle has subgenerator

    Q=[[-1,1],[1,-2]].

The mean first death is≤3, because it is bounded by the death time of one chosen particle started inA (mean3). The same bound holds from every state, so ||(−Q_n)^−1||_infinity≤3 uniformly in n.

Now use unit forcing concentrated at allA, and let v_n=(−Q_n^T)^−1 e_allA be its occupation measure. For one particle

    p_B(t)=(exp[(-3+sqrt5)t/2]−exp[(-3−sqrt5)t/2])/sqrt5.

Let q=max_t p_B(t)<1. (For example p_B(t)≤1/sqrt5<1 for all t.) Exact independence gives

    v_n(allB)=integral_0^infinity p_B(t)^n dt
             ≤ q^(n−1) integral_0^infinity p_B(t)dt
             = q^(n−1),

because expected time inB before death is1. Meanwhile v_n(allA)≥1/n from the initial holding time. Hence

    v_n(allB)/v_n(allA)≤ n q^(n−1).

Thus even a uniformly bounded exact shell inverse admits exponentially disparate coordinate weights on a growing conservative shell. No polynomial Harnack/pointwise comparability follows from the inverse norm. Strictly positive forcing can approximate the point source arbitrarily closely; one must use quantitative properties of a specifically chosen forcing rather than positivity alone.

This does not say adjacent-shell ratios for a carefully designed factorial forcing are necessarily bad, nor does it refute recurrence (this network is linear and recurrent). It isolates the precise information lost by the polynomial absorption argument. A general dual construction needs forcing-sensitive pointwise estimates or a genuinely norm-level way of controlling all inter-shell feedback, rather than silently upgrading an l1 inverse bound into coordinatewise control.
