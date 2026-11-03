# Explicit joint-locality acquisition for the canonical parent

This supplies the operator-norm input to PRODUCT_FRAME_STABILITY_AND_SYMMETRIC_TRUNCATION.md. It uses the actual uniformly gapped two-massed-face Wilson family, not a fiberwise eigenvector oracle.

Let h(phi) be finite range r0 with ||h||<=R and h²>=g², uniformly for every allowed rotor configuration and volume. Rotor dependence of an entry is supported within a fixed stencil rho of its endpoints. Keep normal-direction sites explicit. Set q=1-g²/R²<1 and c_k=binom(2k,k)/4^k<=1. Then the EXACT spectral expansion is

 sign(h)=sum_(k>=0) T_k(h),
 T_k(h)=(h/R)c_k(1-h²/R²)^k,
 ||T_k(h)||<=q^k,
 ||sign(h)-sum_(k=0)^n T_k(h)||<=q^(n+1)/(1-q).

This is just the convergent scalar binomial series for x^(-1/2), applied to h²/R². No spectral choices, gap-selection oracle, smoothness in phi, or supplied eigenvectors enter.

A matrix entry [T_k(h(phi))]_(xy) is an exactly computable polynomial in local hoppings. It vanishes for d(x,y)>(2k+1)r0. Its coefficient depends only on rotors within distance (2k+1)r0+rho of x. The global operator-norm bound implies the uniform bound on EACH coefficient, including as a bounded multiplication operator on rotor L² spaces. One evaluates the polynomial as a grouped matrix expression; expanding its monomials and bounding their absolute coefficients would introduce a spurious exponential factor and is NOT the argument.

Use every such entry as a controlled quadratic interaction term, supported on that ball (and both fermion endpoints). For fixed onsite orbital multiplicity m, bounded-degree polynomial-growth graph v(r)<=C(1+r)^d, its norm is at most C_m q^k. The number of y for each x is O((k+1)^d); the number of anchors x whose ball contains a given physical site is O((k+1)^d). Additional support-volume factors in interaction norms cost further polynomial powers. Hence, for any requested finite polynomial support moment p and any mu>0 with exp(4mu r0)q<1, one has an explicit finite bound of the form

 sup_z sum_(X containing z) |X|^p exp(mu diam X)||Phi_W(X)||
 <= C(m,rho,r0,C,p) sum_(k>=0)(k+1)^(2d+pd) [q exp(4mu r0)]^k < infinity.

The finitely many radius offsets change only C. This is a JOINT rotor–fermion interaction estimate: its support includes every rotor on which a coefficient depends, not merely its fermionic endpoints. It is uniform in thickness and lateral volume. Coarse boundary refinement changes fixed constants, not dimension growth.

The canonical purification generator is a fixed numerical linear combination of flattened Majorana covariance entries. Applying the expansion above to the free covariance and adding the exactly finite-range decoration covariance gives its acquired interaction Phi_W. Evolving this bounded interaction for the fixed purification angle produces the joint quasilocal automorphism W by bounded-interaction Lieb–Robinson estimates. In particular it controls conjugations of bounded rotor heat-bath projectors. Discontinuous cochain-rounding walls cause no difficulty: these are bounded measurable coefficient functions, and no phi derivative has been taken.

The same expansion acquires the counterterm. Since |h|=h sign(h), the k-th term in |h| has norm <=R q^k and degree2k+2. Its diagonal internal trace has norm <=m R q^k and finite rotor support. Thus E0=Tr(h-|h|)/2 is a sum of explicitly local scalar densities with summable weighted tails. The bound is per onsite trace m; no full-volume trace-error estimate is used. Subtract a phi-independent reference bulk energy. Outside the boundary's degree2k+2 hopping neighborhood, the corresponding density difference vanishes exactly. Therefore its rotor-dependent interaction is localized near the interface, with exponentially summable normal-direction tails.

A finite compiler need only retain finitely many T_k, evaluate their finite hopping-path matrices on enlarged patches, and use finite-patch time evolution for Wq_xW†. Every coefficient is obtained from actual Hamiltonian entries and the paid g,R bounds. Exact group averaging supplies symmetry. The separate stability proof, not this polynomial convergence alone, protects the collective gap after finite-range truncation.

Resource warning: q can be extremely close to one because the endpoint construction has huge R/g. These estimates prove finite volume-independent ranges, not practical ranges or affordable resources.
