# Completed wider pure-flow obstruction

For the exact symmetric strict ROC target in `SYMMETRIC_TARGET.json`, no
constant real second-order output-coupled operator with uniformly positive
symmetric principal symbol admits the specified closed-quadratic/
bilinear-SOS heat certificate. This includes every real skew-mixing
coefficient and every nonnegative determinant-square removal.

`PRIMARY_PROOF.md` gives the full theorem. Actual target symmetries reduce
all 12 operator coefficients to \(a\Delta+2bJ\partial_{12}\), with \(a>0\).
After normalization, \(b\) is unrestricted. One exact rational rank-one
witness bounds minor removal by \(25117/10^8\). An exact affine dual family
has positive moment endpoints, annihilates the mixed term identically,
and has strictly negative energy Bernstein coefficients over that entire
interval. No grid of parameter values is used as proof.

The final data are `EXACT_FLOW_FAMILY.json` and `GAMMA_BOUND.json`.
Read-only local replay:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_flow.py
```

The replay uses standard-library arithmetic and the included literal
polynomial helper. It rebuilds all Hessians and mixed maps, all 120
exterior-basis identities, 48 moment pivots, the strict ROC certificate,
the gamma witness, all parameter identities and all 12 operator-basis
projections. Its saved final computation took 0.1274 seconds after imports.
A separate parent implementation, using SymPy QQ and no author code,
passed in 0.328 seconds. The complete theorem is internally accepted at
the stated coercivity and representation scope.

This is a **pure-target** theorem. It does not average an unknown energy
component and its unknown operator as if dissipation were linear in both.
The arbitrary PC/unknown-flow combined class remains unproved. General
nonnegative corrected densities, norm-multiplied heat certificates,
rational/nonpolynomial supports and QC itself are not excluded. The
preceding common-cone theorem and both earlier positive theorems remain
frozen unchanged.
