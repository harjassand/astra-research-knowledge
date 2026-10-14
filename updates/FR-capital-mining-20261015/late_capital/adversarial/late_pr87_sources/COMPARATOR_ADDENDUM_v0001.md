# Skinner–Dunkel numerical and occupancy-TUR competitor screen

15 October 2026. This addendum is separate from the frozen campaign packet. It checks only the [Skinner–Dunkel 2021 paper](https://math.mit.edu/~dunkel/Papers/2021SkDu_PRL.pdf), its [supplement](https://arxiv.org/pdf/2105.08681), [published code/data](https://github.com/Dom-Skinner/EntropyProductionFromWaitingTimes), and the primary source of the occupancy bound, [Harvey–Lahiri–Ganguli](https://arxiv.org/html/2002.10567). No new network optimization was run.

## Exact target inputs and numerical curve

For the $q=1/20$ three-state ring's *complete* alternating visits, the exact visible statistics are
$$
a=\mathbb ET_A=\frac{20}{21},\qquad
b=\mathbb ET_B=\frac{40}{21},\qquad
c=\frac{\operatorname{Var}T_B}{b^2}=\frac{481}{842}=0.5712589073634204\ldots.
$$
The normalized second moment passed to the [published MATLAB interpolator](https://github.com/Dom-Skinner/EntropyProductionFromWaitingTimes/blob/main/Code/gamma_precomp.m) is $\theta=1+c=1323/842=1.5712589073634204\ldots$, **not** $c$ alone. The prefactor in [Skinner–Dunkel Eq. (7)](https://math.mit.edu/~dunkel/Papers/2021SkDu_PRL.pdf) is $2/(a+b)=7/10$ when $k_B=1$. Their notation calls the two-hidden-state block $A$; here it is the ring's $B$, so the labels must be swapped in applying their curve.

At Git commit [d99931dbb365cc3a7a1eb85c1625b1222e932c0e](https://github.com/Dom-Skinner/EntropyProductionFromWaitingTimes/tree/d99931dbb365cc3a7a1eb85c1625b1222e932c0e), the [MATLAB table Data/nvars_comb.mat](https://github.com/Dom-Skinner/EntropyProductionFromWaitingTimes/blob/d99931dbb365cc3a7a1eb85c1625b1222e932c0e/Data/nvars_comb.mat) contains the 119-by-2 array used by gamma_precomp. Its SHA-256 is 6987de5456bb51c39fc0f40b6529b2ce6f45adab38be3b4042cb6df85d823182. The adjacent stored points are $(\sigma_{\rm canonical},\theta)=(2.4,1.5776002415576655)$ and $(2.5,1.5656218066479508)$. Reproducing the code's piecewise cubic Hermite (PCHIP) interpolation gives
$$
\Lambda_{\rm code}(1323/842)\simeq 2.45264662975114,\qquad
\sigma_{T,\rm code}=\frac7{10}\Lambda_{\rm code}\simeq1.71685264082580
$$
in the ring's time units. The separate saved fine finite-$N$ sweep yields about $1.7151$, consistent at display scale. These are **published-code numerical estimates**, much larger than the campaign's analytic bound $(21-4\sqrt5)/30\simeq0.4018576030$.

**Certification limit.** Skinner–Dunkel's supplement, “Numerical convergence,” explicitly says the exact curve requires $N\to\infty$; their finite-$N$ values appear to converge exponentially and the limiting curve is *estimated by a fitted exponential*. The code uses saved nonconvex-search data and interpolation; it supplies no global-optimality proof, interval lower enclosure or all-$N$ truncation bound at $\theta=1323/842$. A feasible finite-$N$ numerical point is an upper bound on the *moment-constrained* minimum at that $N$; it cannot by itself certify that the unrestricted minimum is at least $1.7168$. The paper calls its curve a universal estimator, so it remains a serious incumbent **numerical** comparator. The located table does **not** certify a rigorous $>0.4$ floor.

## Rigorous primary explicit comparator: occupancy TUR

[Harvey–Lahiri–Ganguli Eq. (8)](https://arxiv.org/html/2002.10567) derives for a general stationary finite CTMC with a pool of visible states, in the long-time limit,
$$
\operatorname{Var}(q_A^T)\,[T\sigma+4\bar N_T]\ge
8[p_A(1-p_A)]^2,\qquad
q_A^T=T^{-1}\int_0^T\mathbf1_{\{Y_t=A\}}\,dt.
$$
Here $\bar N_T$ is the mean number of $A\to B$ events over $T$. The statement does not require a known hidden state count or a nonzero visible current. It is an asymptotic long-trajectory relation; [Skinner–Dunkel supplement Eq. (S55)](https://arxiv.org/pdf/2105.08681) writes the same result as
$$
\sigma\ge\frac{8p_A^2p_B^2}{\lim_{T\to\infty}T\operatorname{Var}(q_A^T)}
-\frac4{\mathbb ET_A+\mathbb ET_B}.
$$
Both assume the standard stationary CTMC entropy-production convention ($k_B=1$). The data needed are the stationary pool masses, block-crossing rate, and long-run occupation fraction variance; the latter is a property of the *full visible time series*, not of one fixed three-snapshot law.

For this **exact alternating-renewal target**, $p_A=a/(a+b)=1/3$, $p_B=2/3$, $\bar N_T/T=1/(a+b)=7/20$. Independence of successive $A,B$ visits gives the renewal-reward variance
$$
D:=\lim_{T\to\infty}T\operatorname{Var}(q_A^T)
 =\frac{b^2\operatorname{Var}T_A+a^2\operatorname{Var}T_B}{(a+b)^3}
 =\frac{280}{1263}.
$$
This exact $D$ was cross-checked directly from the ring generator by solving its stationary Poisson equation. Substitution into the primary TUR yields the **rigorous**, dimension-independent analytic floor
$$
\sigma\ge \frac{8(1/3)^2(2/3)^2}{280/1263}-4\frac7{20}
=\boxed{\frac{361}{945}=0.382010582010582\ldots}.
$$
Every compatible all-even finite CTMC has the same complete visible law and hence the same $p_A$, block-crossing rate and $D$. This bound is about $0.0198470$ below the campaign's $(21-4\sqrt5)/30\simeq0.4018576$, a roughly **5.2%** improvement by the campaign's analytic certificate over this *particular* rigorous primary comparator. The numerical Skinner–Dunkel estimate is about 4.27 times the campaign certificate, but that comparison is **estimate versus theorem**, not two certified floors.

## Information and acquisition accounting

The published Skinner–Dunkel numerical estimator requires complete $B$-dwell means and second moments plus both block means. The occupancy TUR requires a long visible trajectory's occupation-time variance and crossing rate. Both statistics are available from the supplied exact full path law. Acquiring them physically requires resolved block transitions or long trajectory monitoring, stationarity, timing calibration, and uncertainty control for dependent records; the numerical curve additionally inherits solver/interpolation/extrapolation uncertainty. The campaign's three-snapshot bound uses only three binary readouts at matched gaps and a prespecified score; its exact-law strengthening above $0.4$ invokes arbitrarily short gaps, so physical bandwidth, readout error, and sample cost remain separate. No sample-efficiency or device advantage follows from the constants alone. Under **same full-law information**, the numerical incumbent may be much stronger, while the primary analytic occupancy TUR is slightly weaker. This screen finds no certified Skinner–Dunkel/Harvey bound above $0.4$ in the inspected sources and does not establish global novelty clearance.
