# Executed finite Jensen certificates

Exact rational endpoints and receiving constraints are in finite_results.json. Unit beta,kappa,d_min, chain coupling 20. Producer timings start from an in-memory raw dictionary; fixture/import/JSON creation are additional. All saved certificates were actually replayed by check_finite.py, not merely compared against a formula.

| Physical dimension | Raw terms | Requested ratio | Exact ratio display | Total scalar evaluations | Largest extra power bits | Producer seconds | Full-rate display interval |
|---:|---:|---:|---:|---:|---:|---:|---|
| 3 | 9 | none | 1.014079967 | 1922 | 69 | 0.032 | [0.4423569301, 0.448585301] |
| 5 | 21 | none | 1.016040956 | 1794 | 153 | 0.032 | [0.5642822879, 0.5733339152] |
| 17 | 93 | none | 1.037655168 | 2050 | 673 | 0.049 | [0.1659358763, 0.1721842197] |
| 65 | 381 | none | 1.049502460 | 4098 | 2945 | 0.193 | [0.0001437503878, 0.0001508663857] |
| 129 | 765 | none | 1.027742589 | 16386 | 6913 | 1.517 | [4.537633246e-09, 4.663518939e-09] |
| 257 | 1533 | 103/100 | 1.016526811 | 16386 | 13825 | 3.789 | [2.158019791e-18, 2.193684977e-18] |
| 513 | 3069 | 101/100 | 1.006729780 | 131074 | 33793 | 81.276 | [2.369045058e-37, 2.38498821e-37] |

The 513D run uses N=32768 per monotone piece, cutoff T=2, 1664-bit dyadic precision, 98,305 inherited scalar points plus 32,769 extra evaluations. Its acquired raw polynomial has 3,069 monomials, each represented by 513 exponents; acquisition alone took 0.285 seconds in that run. The largest extra powered numerator/denominator is 33,793 bits. None of these counts is whole-program peak memory.

The target is full equilibrium capacity/mass, not inverse MFPT. The rare rate is not compared only against blind crossing simulation: the strong ordinary variational/capacity/channel comparators remain in the inherited ledgers. An equally informed ordinary implementation with this theorem gets the same bound. The integer-root prototype is not optimized; for dimensions divisible by 4, direct rational powers followed by outward rounding may be faster.

All 2,458 new author checks pass, including replay of every saved result. Independent review remains separate.
