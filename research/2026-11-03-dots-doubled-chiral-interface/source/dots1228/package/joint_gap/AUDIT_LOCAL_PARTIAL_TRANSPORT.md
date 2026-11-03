# Independent audit: acquired local charged endpoint transport

2026-11-03. Audited `LOCAL_PARTIAL_TRANSPORT_PROOF.md` as first saved today, including its actual Wilson inputs and local acquisition rather than a supplied state oracle.

## Verdict

The construction survives substantive audit. Under the paid endpoint/index estimates, additional normal thickness, and corrections/clarifications below, it constructs one bounded-support, finite-stencil, norm-at-most-one charged operator whose endpoint ground-state matrix element has magnitude at least 1-epsilon, uniformly over allowed matching exteriors. No interpolation gap or global occupied-state oracle is used. This is an endpoint operation only: it does NOT establish consistent signs around loops, a fluctuating-rotor gap, or a practical algorithm.

Required small fixes:
1. In section A, **d must be the number of included normal layers**, d>=1, namely w=0,...,d-1. Then the far-profile exponent L-d is correct. The displayed notation `chi_depth<=d` instead includes w=d and is off by one; interpreted literally it requires b_*^(L-1-d). The factor 1100 does not absorb 1/b_* (about two million). Use layer counts throughout, or increase the thickness by one.
2. Choose the certified full-gap lower bound p<=g (reduce a valid bound if necessary); several section B simplifications explicitly use this. This costs nothing.
3. For finite arithmetic, do not require deciding the exact largest empty gap and exact equality ties. Select a deterministically certified gap with the promised half-margin. Uniform termination follows from the existence of a larger gap. Exact-largest selection can demand arbitrarily fine comparison of near-ties.
4. Degenerate occupied eigenspaces require only a basis of the whole rounded occupied space, not individually tracked eigenvectors. State/Fock errors concern rays. The statement never supplies a common positive phase for different moves.

## 1. Uniform far leakage really is an operator estimate

The near/high Sylvester inequalities in A are valid and dimension-free. With g=M/10 their numerical coefficients are

  x <= 14.546 delta + 7.273 z,
  z <= .005015(x+delta).

Solving gives x+z<16 delta, so the advertised 32 delta has room. Split the positive and negative near/high spectra, apply the semigroup integral on each separated ordered pair of spectral intervals, and add the two norms. This applies to the complete low spectral subspace; it is not an estimate on individual eigenvectors subsequently summed over volume.

For the first d layers, the free-far geometric tail is bounded by a constant times b_*^(L-d); the exact singular-vector error is O(b_*^L). Together with x+z<=1024 b_*^(L-1), this fits 1100 sqrt(d+1)b_*^(L-d) for d>=1. Fourier orthogonality makes the far-profile strip norm a maximum over momenta, not a sum. Restricting laterally can only decrease it.

It is essential that final L exceed the entire operator-support depth d_R, not just the changed mass depth. The draft pays this correctly. The extra coefficient-acquisition buffer can be larger still; its range must be recorded even though the operated-on fermion modes remain in R. All radii are fixed by local input bounds and epsilon before the logarithmic p^-1 thickness increase. No volume-dependent compiler radius is hidden.

## 2. Trace-local resolvent acquisition closes

For V=Ha-Hb, the sign-resolvent identity has the stated positive sign. Insert the physical support projection of V on both sides and use

  ||R_i chi_S0|| <= (g^2+t^2)^(-1/2) + eta (p^2+t^2)^(-1/2).

Then ||Ra V Rb||_1 is bounded by v times the product of these two operator bounds. Integrating gives the draft's v/(2g), mixed logarithmic, and v eta^2/(2p) terms. The mixed integral is bounded by [asinh(g/p)+1]/g. Thus B=2+2v/g is safe with the selected eta. No full-volume trace error enters.

The discarded interval [0,tau], tail above T, quadrature error, and Neumann-polynomial product error each satisfy their stated bounds. In particular e<=1/tau gives 2e/tau+e^2<=3e/tau, so the product-polynomial allocation costs at most 3 eta0/100. Their sum is comfortably below eta0. The geometric resolvent approximation is valid uniformly on [-W,W], and its degree depends on W,tau,T and the local trace tolerance, not p or lateral volume.

Every polynomial sandwich q(Ha)Vq(Hb) has both matrix legs within a finite hopping neighborhood of S0. All coefficient paths lie in a fixed finite stencil. Thus the same M is acquired for every exterior agreeing on that stencil; it is not a separate optimization using each exterior ground state. Individual P_i are not approximated in global trace norm anywhere.

## 3. Cutoff rank and margins have no circular dimension cost

The trace bound, rather than physical patch dimension, limits the number of relevant |M| eigenvalues: r<=rmax<=ceil((B+1)/t). This is essential. Using patch dimension here could create an unsatisfiable precision/radius feedback loop; the draft avoids it.

The largest-gap argument earns distance at least 2 gamma0 from all |M| eigenvalues. Weyl perturbation at BOTH thresholds +c and -c preserves the true tail rank because eta0<<gamma0.

Do not invoke an operator-Lipschitz inequality for absolute value: that inequality is not generally available. Instead apply Sylvester/Davis–Kahan directly to the union of the two signed tails. Project (Delta-M)S_R onto S-perp and split M|S_R into positive and negative parts. Their spectra are separated from Delta|S-perp by at least gamma0. This yields

  s0 := ||S-S_R|| <= 2 eta0/gamma0

with a conservative factor 4 also safe. Equal ranks identify this with the cross-projection norm. This is much better than the draft's permitted factor 20 and does not use an artificial gap near eigenvalues +/-1.

Because Delta^2 commutes with both endpoint projectors, true S reduces both. All unmatched rank modes have Delta eigenvalue +/-1 and are retained. Consequently complement ranks agree exactly. Small Hilbert–Schmidt error alone would not prove that rank statement, but the reducing-space argument does.

On the complement, sum sin^2(theta_j)=||Delta_tail||_HS^2/2<=tB. Its Slater overlap is therefore at least 1-tB, independently of the number of discarded modes.

## 4. Explicit Fock error constants fit the budget

Here is a concrete closure of the draft's C,C' targets. Let s0<=4 eta0/gamma0. A canonical one-body unitary W sends S to S_R, differs from identity on at most 2r modes, and satisfies ||W-I||<=2s0. Its canonical Fock lift obeys

  ||Gamma(W)-I|| <= 4 r s0.

Apply W to both endpoint Slaters for analysis only; this unitary is not a supplied or implemented nonlocal operation. Their compressed occupied projectors on S_R differ from the unrotated compressed P_i by at most 4s0. If local data accuracy is zeta, write e0=4s0+zeta. Rounding at 1/2 has the correct rank and projector error <=2e0, since e0 is far below 1/4. A unitary within the r modes relating exact and rounded occupied spaces has norm distance <=4e0; its Fock error is <=4r e0 per endpoint.

Combining both endpoints yields amplitude loss at most

  tB + 8r s0 + 8r e0
      = tB + 40r s0 + 8r zeta
      <= tB + 160r eta0/gamma0 + 8r zeta.

Thus C'=200 suffices; the draft's 1000 safety allowance is ample. The specified eta0 makes this much smaller than epsilon. This estimate uses finite-rank Fock lifting, not a dimension-times-max-angle bound on the exterior.

Gamma(Ub) C Gamma(Ua)^dagger indeed maps the canonical source occupied wedge to the target occupied wedge up to a phase. Products of unmatched creation/annihilation operators have norm one and definite number charge. Orthogonal principal pairs are harmless. A rank-one Fock partial map on the retained modes would be an equally valid alternative.

## 5. Local acquisition of compressed projectors

The F_sigma estimate is correct. The small-spectrum contribution to S_R^*(P-F_sigma(H))S_R is bounded by eta_dR^2, not by its square root, since the bounded low spectral function is sandwiched by the support projection on both sides. On the high spectrum the error is <=sigma/(pi g). A uniformly bounded real polynomial approximation to F_sigma then supplies the finite compression to zeta without a full-volume trace conversion. Sigma and polynomial degree can be fixed independent of p; p enters only the required thickness.

The draft's layer-count-adjusted final L controls both S0 resolvent leakage and all exceptional-mode support. Finite torus edge cases may use the entire torus if it fits within the prescribed fixed-radius stencil; they do not require a global oracle on arbitrarily large systems.

## 6. Decoration, covariance, parity, and computational qualifications

A patch closed under both endpoint Majorana matchings has rank-one pairing ground projectors. A local monomial basis is complete. In a D-dimensional local Fock factor, at least one unitary Majorana-basis monomial has overlap magnitude >=D^(-1/2), by Hilbert–Schmidt completeness. Choosing a certified near-maximizer pays a finite normalization bound; one need not divide by an unspecified tiny nonzero number. Only monomials with the required parity have nonzero overlap. This uses the already-established pairing/self-linking parity relation and bounded matching closure.

The decoration map and free map have opposite exact axial charges and equal parity change, hence their graded product is even and axial-neutral. Products of odd factors must be interpreted in the graded CAR algebra, not an unqualified tensor product. Their norms multiply and the endpoint magnitude remains the product of magnitudes. The unchanged-anchor compiler supplies exact vector covariance without averaging away a complex matrix element. Global rotations of the exterior cause no problem: exterior factors commute with the local even operator.

All threshold/basis choices are made on the anchored local data, so they are common to matching exteriors. Near degeneracies within occupied/empty clusters do not affect the rounded projector or amplitude bound. A deterministic local frame can use pivoted columns of the occupied projector instead of unstable individual eigenvectors; largest-minor bounds give a finite precision cost in the retained rank. Exact equality comparisons should be replaced by certified overlapping choices.

As throughout the rotor construction, branch walls require a specified one-sided/measurable convention. There is no uniform finite bit complexity for resolving arbitrary inexact real rotor inputs arbitrarily close to discontinuity walls without such a convention or chamber data. This does not invalidate the bounded measurable coefficient operator, but should not be advertised as a uniform continuous-input numerical algorithm.

The real antiunitary allows the free local coefficient matrices to be symmetrized into its real form without increasing error. It restricts phases to signs; it does not prove trivial sign holonomy or its cancellation by the decoration.

## Scope earned

A finite-range/high-body-order endpoint term with locally acquired coefficients and uniformly large endpoint magnitude is supported by the proof. Resource dependence is catastrophic but finite and explicitly volume-independent in operator/stencil radius; normal thickness has an additional log(p^-1) cost. All earlier Wilson endpoint hypotheses, compensated orientation, and the astronomically small lattice spacing remain necessary. No collective gap, global phase consistency, efficient preparation, or full chiral-gauge interface has been inferred.

### Finite cutoff selection: explicit implementation refinement

The initial revision's phrase "half the guaranteed interval width" earns midpoint margin gamma0, not 2 gamma0. The constants above remain valid with margin gamma0. A completely finite rule is: use candidate centers in [t+gamma0,2t-gamma0] on a mesh of spacing at most gamma0/4; compute |lambda(M)| to certified absolute error gamma0/8; choose the first center whose computed distances exceed 5gamma0/4. A true gap of width 4gamma0 guarantees a candidate within gamma0/8 of its midpoint, so some center passes with room. Any accepted center has true margin at least 9gamma0/8. This uses O(rmax) centers and a predetermined eigenvalue precision, with no exact tie or largest-gap decision. The signed-tail Sylvester and Fock constants already allowed above cover this margin.
