# Paid near-solid critical-width window extension

This extends only the restricted short-anchor source family. It does not assert that every large filled droplet has such a window.

At theta4,phi4/R,L8R set m=2R+1 and k=floor(R/8). Let H contain actual non-target states with a horizontal or vertical length-m window containing at most k minus sites. There is at least one plus site. Choose deterministic ties and fill the window from an existing plus interval, skipping already-plus sites; every birth has at least one plus neighbor. Each of at most k births changes physical weight by a factor at least exp(-4theta), since the positive field helps.

For a fixed labeled window, at most S_k=sum_(j<=k) binom(m,j) source patterns are erased. Thus both endpoint congestion during this first stage and its exact terminal unnormalized arrival density are bounded with

 T=S_k exp(4theta k) <=(k+1)binom(m,k)exp(16k).

Outside-window source bits are retained and readable; the combinatorial factor pays every lost window pattern. This is not a Gibbs reset.

Now append the open-rectangle and full-column stages of RESULT.md. Their exact terminal mass dominations compose to TQ_mh w, with h=L-1. Window filling, rectangle filling, and full-column continuation use disjoint physical coordinates: respectively the chosen row segment, the rest of its width-m band, and sites outside that now-full band. Therefore the stage congestion combines by a maximum, and the same global label/current bound becomes

 N_H <=4n² T Q_mh J_line C.

All paths stop at first ORIGINAL B; earlier-target sources are removed from subsequent positive arrival sums. Original A,kappa,v,C and physical rate-one clocks are unchanged.

Here delta=8m/R-16=8/R, so
 (1-exp(-delta))^(-1) <=1+1/delta=1+R/8.
The open-partition estimate remains valid for this small positive delta; there is no need to impose delta>=2.

Since k<=m/2 and m/k<17 at the four stated instances, binom(m,k)<=(em/k)^k and exp3>17 give
 T<=(k+1)exp(20k).
Together with the previous rational bounds,
 logQ <=m(L-1)/2980+log m+log(1+R/8)+5R/12+2m/2979.

`dense.py/json` pays all factors and gives:
- R80, m161,k10: occupation/ZA <=exp(-313).
- R200,m401,k25: <=exp(-1018).
- R1000,m2001,k125: <=exp(-1918).
- R10000,m20001,k1250: vacuous; no result asserted.

## Exact conditional coverage interface
For a specified actual filled domain, partition each geometric row interval into disjoint length-m windows. If no such window belongs to H, each contains at least k+1 actual minus sites. Therefore the actual interior-minus volume is at least
 (k+1) sum_intervals floor(interval_length/m).
This is a deterministic count, not a probabilistic independence claim. Arbitrary nonconvex domains may have few such windows even at large area; row-geometry control and a valid marked-hole source-weight bound are still needed. Bridge is pursuing that distinct complement. No new high-mass separation from existing dense-window/Gibbs results is claimed here.
