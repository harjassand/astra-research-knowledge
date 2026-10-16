# Read-only audit after independent freeze

The requested root Erlang composition (E)/(F) and finite-bit residual interface
pass this same-team independent audit, conditional on direct certificate (D).
No root implementation was imported/executed, and no root source was edited.
This audit does not constitute external validation of the direct-limit theorem.

The normalization checks are:

- C(T)/T is nonincreasing: the atom contributes a nonincreasing S_r,e(T)/T;
  after scaling t=Tv, both nonnegative survival factors in each boundary
  integrand are nonincreasing.
- E[S_r,e(Gamma(k,s))/Gamma(k,s)] equals
  s/(k-1)[P_r^(k-1)1]_e. The coefficient s/(k-1) is necessary and present.
- The boundary convolution has exactly the positive 1/(k-1) sum from the
  independently derived Erlang/beta identity. Symmetry of H_r justifies the
  displayed 1^T P_r^j form; nonsymmetry of coarse K is harmless because its
  actions remain positive substochastic and are solved exactly.
- The fixed-point original actions enter only through exact original-matrix
  residuals; all Green coefficients, coarse solves and CDF lower bounds are
  rational and nonnegative in the executed receipts.

`audit_root_composition.py` independently reconstructs components by union-find
and pair matrices by physical-edge actions. It solves every local Green RHS
with integer fraction-free Bareiss elimination, rechecks those equations,
rechecks every delivered original shifted residual and every exact coarse
resolvent equation, then recomputes the atom, boundary and total bound.

It exactly reproduces the root saved receipts:

| Root receipt | Direct averaged endpoint TV bound |
|---|---:|
| DIRECT_PATH6.json | 0.016335173365107793 |
| DIRECT_BRANCH6.json | 0.006724071995019676 |
| DIRECT_PATH20.json | 0.04734215393997101 |

Exact fractions and input hashes are in `root_composition_audit_receipt.json`.
The path20 independent audit took about 0.206 seconds. This checker time is
separate from the root generation receipt and is not silently included in it.

The first checker development run failed an exact Green equation assertion
because its own last back-substitution division used Python integer division
to produce a float. The checker was corrected to construct a Fraction before
division, then all three receipts passed. No root result was accepted through
that failed check and no root change was needed.

The direct measure limit, model acquisition, historical priority and best
validated-incumbent comparisons retain their separate obligations.
