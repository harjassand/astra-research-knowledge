# Independent finite-sector temperature-scaling audit — 2026-10-08

Complement to RESULT_AND_RESTART.md. Numerical diagnostics only; no proof or priority certification.

For each N, the irreducible-spin weights from the initially maximally mixed state are computed without a dense 2^N matrix:
w_(N,j)=(2j+1)^2 binom(N,N/2-j)/(2^N(N/2+j+1)).
Within spin j, compare p_(beta,j)(m)=exp(-beta m)/Z_j(beta) to the uniform distribution on {-j,...,j}. Because the blocks are orthogonal, the exact half trace distance to I/2^N is
D(rho_(N,nu),I/2^N)=sum_j w_(N,j) TV(p_(beta,j),uniform_j).
Stable gammaln and logsumexp arithmetic evaluates it in polynomial time.

For nu=N^alpha:
| N | alpha=1/4 | alpha=1/2 | alpha=3/4 |
|---:|---:|---:|---:|
|16|0.28816|0.17109|0.09264|
|64|0.38771|0.17979|0.06857|
|256|0.49205|0.18450|0.04932|
|1024|0.59035|0.18701|0.03511|
|4096|0.67614|0.18831|0.02489|

All 15 evaluations satisfy the PROVED bound D(rho,I/2^N) <= (sqrt(3N)/4)*log(1+1/nu). The alpha=1/2 sequence appearing to approach a nonzero constant is consistent with the unresolved critical window but DOES NOT settle distance to the nearest fully separable state. TV to I/2^N is only an upper bound on distance to full SEP. The alpha=1/4 sequence increasing toward 1 likewise is NOT a substitute for the separate local-measurement lower theorem.

Code: verify_thermal_scaling.py; locally computed full 15-row JSON was also saved during the conversation. Source and code should be replayed in an independent environment if used for publication.
