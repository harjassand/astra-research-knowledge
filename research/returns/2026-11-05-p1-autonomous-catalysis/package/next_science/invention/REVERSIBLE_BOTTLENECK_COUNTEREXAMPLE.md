# A small net turnover does not bound the degree of control of a fast step

Use two chemical states E and I and two distinct reversible channels. A precursor channel E→I has rate c, its reverse I→E has rate d. A product channel I→E has rate a, its reverse E→I has rate b. Count only the product channel as signed product. Impose ca/(db)=exp(A), so all channels are thermodynamically consistent with one total chemical affinity A.

The net product current is exactly J=(ca−db)/(a+b+c+d). Lowering the product-channel transition barrier scales both a and b by r, preserving all thermodynamic ratios. The degree of control at r=1 is

\[
X={\partial\log J\over\partial\log r}={c+d\over a+b+c+d}.
\]

There is no bound X≤J/a. Set a=1046.4659/s, c=1000/s, d=10^6/s and A=1.2eV/(kB×298K). The required reverse product rate is b=ca exp(-A)/d>0. Then J≈1.0443/s but X≈0.99896, whereas J/a≈0.000998. The rare intermediate I repeatedly returns through d before its product channel succeeds. The product barrier controls the escape probability from this pre-equilibrium; a small stationary I population is not a small degree of rate control.

This is a complete finite reversible counterexample, not an empirical model of the reported catalyst. It preserves reverse rates, the total ORR-sized chemical affinity, and symmetric barrier perturbation. It invalidates importing the irreversible series waiting-fraction bound J/a into an arbitrary reversible catalytic network. The actual physical pre-equilibrium, state free energies and reverse rates remain to be acquired.
