# Reconstructed finite four-corner flow refinement

This is a reconstruction from the delivered exp(52) archive and inherited descriptions, not recovery of missing exp(36) files. It reproduces the earlier numerical receipt independently. All original geometric/model dependencies of the archive remain. This is NOT a uniform polynomial-time estimator or a practical-transition-time result.

## Native setting
R=200, theta=4, phi=.02, t=2phi=.04, q=exp(-t), L=1600, n=L², original soft-source kappa and original r5 core. d=131, K=263, M=600. Keep the archive's monotone corner-growth paths, but replace deterministic central interval fill by the uniform-interval flow. Four corner laws are q^area/Z, Z=GaussianBinomial(2d,d;q). The original thermal normalization bound exp(1e-6) and clock bound kappa^-1<exp(2593.6) are retained, not reinterpreted.

## Uniform interval flow, exactly acquired
For m sites in a line, choose the first site uniformly. Given a length-j occupied interval starting at i, add left with probability i/(m-j), right with probability (m-j-i)/(m-j). These are explicit rational probabilities; endpoints are unchanged. Every length-j interval has probability 1/(m-j+1). Its layer sum of squared edge currents is

 c_j=(2(m-j)+1)/(3(m-j)(m-j+1)), j=1..m-1,

and birth-layer value is 1/m. Heatbath resistance for native energy E is exp(Eold)+exp(Enew). The exact isolated central-side resistance, divided by exp(Egroup), is

 F(m)=(1+exp(16-t))/m + exp(16)(1+q) sum_(j=1)^(m-1) q^j c_j.

The exp(16) factor on subsequent central growth is essential. An initial reconstruction omitted it; that scratch error was corrected BEFORE any certificate/result was shared. The directed code includes it.

## Completed corner fibers
A corner lambda has support p and completed profile mu=(lambda-1)_+. Let r be mu's support. For fixed mu, p ranges r..d and area(lambda)=area(mu)+p. Thus

 S_r=sum_(p=r)^d q^p,
 G_0=1, G_r=q^r GaussianBinomial(r+d-2,r;q), r>=1.

G_r is the positive q-area sum over mu of support r and width <=d-1. Define

 U_p=q^p sum_(r=0)^p G_r S_r,
 V_s=sum_(p) U_p U_(s-p).

All are finite positive sums, no infinite-partition approximation. Conditional original supports have probability q^p/S_r. Once both positive corners have been processed, all lambda in one mu-fiber occupy the SAME physical state. Convexity of flow resistance can therefore average their central interval flows without a worst-case count penalty. Two stationary corners contribute 1/Z², active corners contribute V_s/Z4. A macro side length h therefore contributes at most

 (2/n Z6) exp(Erect) sum_s V_s F(h-s),

where Erect=16(w+h)-twh. The factor 2 charges possible right/up overlap; translations are divided by n only because the core bbox is uniquely anchored below L/2. The macro list is right expansion (a,a) with side a, then upward expansion (a+1,a) with side a+1, a=K..M-1.

Group recoverability: remove the new outer row/column from a central-phase configuration; the two completed mu profiles and stationary corners are exposed. Within each direction the macro stage is fixed by its unchanged dimension. Different groups cannot silently share a physical edge. This invokes the archive's fixed-diagonal, separated-corner geometry. It is a proof obligation, not inferred solely from tests.

## Positive-cut steps
Those additions have two neighbors, energy decrement t. For each channel, their total side resistance is at most exp(Erect) q^-A (1+q)/(1-q). On a positive edge, original active support lengths parameterize independent geometric subsequences in the two ambiguity corners, because the prescribed flipped row fixes the processed-interval endpoint. Thus a probability-sensitive Cauchy bound replaces cardinality by

 B=min(2(d+1)^2, 2((1+q)/(1-q))²).

This bound requires the CARTESIAN fiber description; it is not asserted for an arbitrary subset of corner labels. Therefore all positive-cut core steps contribute

 B/(n Z4) * (1+q)/(1-q) * sum_macros exp(Erect).

Positive and central edges are disjoint within a macro/direction; the single factor 2 above already charges the right/up squared-sum overlap.

## Other phases and exact arithmetic
Prefix/merge/late formulas are retained from the archive. Their plus-count ranges are mutually disjoint, so Rest=Rpre+Rmerge+Rlate. Core may overlap them, charged by

 Rphysical <= (1+epsilon)Rcore+(1+1/epsilon)Rest,
 epsilon=1/10000.

The shared reservoir edge is added separately and never translation-discounted. Multiplication by exp(1e-6) is upper bounded by 1/(1-1e-6).

`certify_reconstructed_pushforward.py` uses exact Fraction Taylor enclosures for exp, positive Gaussian/support recurrences, 80-digit outward Decimal arithmetic, and explicit rational c_j coefficients. Denominator Z is rounded down; all positive numerator operations round up. It yields

 Rnormalized/exp(6251) <= 0.9985603049375931724335344104544049887 < 1.

Hence CONDITIONAL on the geometry/physical-flow proof and recovered model dependencies,
 C_kappa/Z_A > exp(-6251),
 W_cut/C_kappa < exp(36)
using the delivered corrected W_cut/Z_A<=exp(-6215). This is a finite formula certificate, not an externally peer-reviewed theorem or efficient full prediction algorithm. Arithmetic runtime was .67 seconds; full flow-channel construction is still ~n/2 physical additions per path.

## Next potentially consequential step
Do not assume all remaining gap can be closed by increasing this lower bound. Area-cut energy counts fast k2 corner fluctuations, whereas bbox expansion often requires slow k1 births. A trial based on component bbox/semiperimeter may suppress irrelevant corner recrossings. It must handle nonconvex configurations, multi-domain mergers, wrapping, thermal-core/source and target terms exactly. No such global upper is constructed here.
