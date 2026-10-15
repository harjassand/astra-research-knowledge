# Conditional collateral-loss diagnostic

This calculation concerns the original blind isotope-overwrite construction. It does not bound an isotope-informed controller, adaptive survivor selection, arbitrary local correlations, or the root's later renewal proposal. It is elementary kinetic arithmetic; priority is UNKNOWN.

Assume a fully repaired, well-mixed lattice. Its heavy fraction is x. Each primary ejection chooses a light atom at rate sigma_L(1-x) or a heavy atom at rate sigma_H x per unit uniform fluence. Every removed site is immediately filled independently from a reservoir with heavy fraction p. Let each primary ejection additionally cause a mean m collateral removals whose heavy fraction equals x, independently of the initiating event. This last equality is a diagnostic assumption, not a fact measured in graphene.

The primary contribution is p sigma_L(1-x) - (1-p) sigma_H x. The total primary event rate is R=sigma_L(1-x)+sigma_H x. Collateral replacement contributes m R(p-x). Therefore

    dx/dD = p sigma_L(1-x) - (1-p) sigma_H x
             + m [sigma_L(1-x)+sigma_H x](p-x).

Normalize sigma_H=1 and write r=sigma_L/sigma_H >1, b=pr+1-p. The right side becomes

    F(x)=m(r-1)x^2 - Bx + C,
    B=b+m[r+p(r-1)], C=(1+m)pr.

For m>0, F(0)>0 and F(1)=-(1+m)(1-p)<0. The smaller quadratic root lies in (0,1), the larger lies above 1, and the smaller root is the unique stable equilibrium on [0,1]. A numerically stable expression is

    x_m = 2C / [B+sqrt(B^2-4m(r-1)C)].

For m=0 the equilibrium is x_0=pr/(pr+1-p). For any desired q with p<q<x_0, reaching or maintaining q from x=p requires

    m <= [pr(1-q)-(1-p)q] / { [r(1-q)+q](q-p) }.

This follows directly by requiring F(q)>=0. If equality holds, q is approached asymptotically rather than reached at finite fluence.

As r tends to infinity with fixed m>0, F(x)/r tends to

    (1-x)[p+m(p-x)].

The stable reachable limit is min(1,p(1+1/m)). In particular, one random collateral removal per initiating ejection caps the ideal limiting heavy fraction at 2p for p<1/2, even if the primary isotope selectivity becomes arbitrarily high.

Using p=.01109 and the central measured 95 kV ratio .0566/.0021 gives:

| m | Equilibrium heavy fraction |
|---:|---:|
| 0 | .23210059 |
| .001 | .22855098 |
| .01 | .20015732 |
| .1 | .08683322 |
| 1 | .02137044 |

To sustain q=.20 needs m<.01005573 in this model. This is a requirement to measure, not a claim that the experiment's m has this value.

If a vacancy heals at rate h and its first collateral sputtering occurs at rate c, independent exponential competing clocks give a first-collateral probability c/(h+c). Achieving a probability below .01005573 requires h>98.45c. No acquired paper here measures this race in a natural-feed isotope-overwrite experiment. Spatial scanning, beam blanking, defect reconstruction and nonexponential healing can change the model; these must be measured rather than folded into a fitted h.

Meyer2012 identifies a dangling neighbour after primary monovacancy creation and a possible second ejection with a much lower threshold. That observation motivates the diagnostic; it does not establish the assumed well-mixed collateral law or m=1 under an optimized protocol. The later adaptive renewal construction requires a different state/history model.
