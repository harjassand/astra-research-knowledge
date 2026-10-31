# Separate loss-to-coupling corollary review

31 October 2026. Scoped mathematical PASS after full read of
`LOSS_TO_COUPLING_RESOURCE_COROLLARY.md`, 4,228 bytes, SHA-256
`403e142105400b6cdc5e0f4d7a5b8b62663e79dfd13aa36632206ae6ab7fa77f`.
This receives, and does not replace, the frozen occupation source `0b0bd7ff...` and whole receipt `5d9fd86e...`.

Writing the actual coupling as c=sqrt(lambda)b, the backward forcing is r=2Rc/lambda. The squared-history exponent is C=2rg(1+a tau)/gamma. Thus C/2+R epsilon_ctl=R[2cg(1+a tau)/(gamma lambda)+epsilon_ctl], exactly the stated h. The general contour bound exp(Rh)/(R-1) is valid whenever 1<R<=gamma lambda/(8c).

For R0=gamma lambda/[8cg(1+a tau)], g>=1 and a tau>=0 ensure the original radius cap. With no control mismatch, R0 h=1/4. When R0>=2, replacing 1/(R0-1) by 2/R0 gives precisely 16 exp(1/4)cg(1+a tau)/(gamma lambda).

For R=min(R0,1/(2epsilon_ctl)), source and control exponents are bounded by 1/4 and 1/2. Therefore 2exp(3/4)/R equals the maximum of the two displayed terms, not their sum. The source and control contributions were already combined in the exponent; no additive implementation error was dropped. R>=2 remains an explicit admission premise. The separately stated sufficient loss/control inequalities are correct with that premise, and no optimized threshold is implied.

This is a genuine sharpening of the earlier sufficient constant: it eliminates an avoidable exponential activation-budget dependence by choosing a smaller contour radius. It does not remove physical injection, gate duration, transport margin, control discrepancy or actual coupling costs. In particular, a growing with lambda can leave or worsen a finite leading cost; the formula itself must be evaluated. The control quantity is integrated unwanted Hamiltonian norm, not average infidelity or an arbitrary channel distance.

The initialized Markov-field, fixed-support, bounded incidence, arbitrary finite source/system/reference input, and amplitude-not-probability qualifications of the full receipt remain binding. No new fault-tolerance theorem, hardware acquisition, calibration protocol, simulator, or practical/novelty claim is accepted. The author's separate comparison note is outside this short formula receipt.
