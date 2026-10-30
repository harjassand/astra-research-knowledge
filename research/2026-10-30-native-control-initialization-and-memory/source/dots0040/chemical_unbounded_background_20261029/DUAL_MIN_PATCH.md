# Exact minimum patching for dual certificates

Let L be a countable-state jump generator with finite exit rates and nonnegative off-diagonal rates. Let positive functions mu_i be defined on the whole state space, and set mu(x)=min_i mu_i(x) for finitely many i. At any minimizer i at x,

    (L*mu)(x) = sum_(y!=x) q(y,x)mu(y)-q(x)mu(x)
             <= sum_(y!=x) q(y,x)mu_i(y)-q(x)mu_i(x)
              = (L*mu_i)(x).

Thus if outside finite K at least one minimizer at each x has a strictly negative local adjoint defect, then mu has strictly negative defect there. If sum mu q and sum mu are finite, the finite-measure excursion argument yields recurrence of closed communicating classes, subject to its ordinary holding-time conditions.

This is an elementary positive-operator comparison, not claimed new. Its potential advantage for chemical recurrence is exact hard patching: there is no derivative smoothing or error from a jump crossing between selected regions.

The essential missing premise is **selector validity**. It is not enough that each mu_i works somewhere and those regions cover the exterior. Their pointwise minimum must select a certificate valid at that state. Defining a certificate only on its region also fails: the incoming adjoint sum uses neighboring values outside that region. Global summability/exit-rate integrability must be proved for the minimum. No general selector-valid chemical construction is supplied here.
