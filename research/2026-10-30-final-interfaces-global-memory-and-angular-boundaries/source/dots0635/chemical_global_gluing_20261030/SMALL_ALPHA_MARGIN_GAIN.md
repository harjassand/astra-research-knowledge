# A stronger consequence of the killed-generator compactness proof

For the finite killed Q of FRACTIONAL_FACTORIAL_BULK.md, let

    eta(alpha)=−max_(z in simplex) E_alpha(z).

Then not only eta(alpha)>0 eventually, but

    eta(alpha)/alpha → +infinity as alpha→0.

Proof: otherwise there are alpha_n→0 and z^n with E_(alpha_n)(z^n)≥−C alpha_n for a fixed C. The same uniform O(alpha_n) bound on positive terms forces limiting support away from killed vertices. An edge leaving that nonempty support contributes negative/alpha_n→−infinity, while positive/alpha_n remains bounded. Contradiction.

This permits fixed O(alpha) perturbations of the finite functional without losing contraction. It does not give an effective rate; long paths and extreme fixed coefficients can make the gain grow extremely slowly. It does not by itself resolve the strip-width/small-alpha circularity, because the graph and its rates change when the strip grows.
