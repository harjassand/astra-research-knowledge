# Finite reciprocal collisions, operating clocks and ancillary-factory errors

This construction earns the physical observation/control interface used by the [unknown-local-support rare-failure theorem](README.md). Its complete proofs are in the [physical supplement](package/physical_supplement.txt), [main report](package/rare_failure_research.pdf) and [editable report](package/rare_failure_research.tex). It is a specified engineered collision architecture, not a laboratory realization or a completeness theorem for unrestricted natural noise.

## Reversible local kernels with unknown correlated routes

A bounded register block meets a fresh matching Gibbs ancilla. The joint pulse conserves combined uncoupled energy and obeys reciprocal transition probabilities `|<v,b|U|u,a>|^2=|<u,a|U|v,b>|^2`; dephasing and readout occur at the registered endpoint. Fresh ancillas have no memory of past register/controller states. Energy conservation plus reciprocity gives product-law detailed balance after summing **all** microscopic routes. Energy conservation alone does not imply the required reciprocity. One fixed real-symmetric energy-conserving interaction pulse suffices; an arbitrary noncommuting sequence of symmetric Hamiltonians need not.

A stricter digital architecture conserves each matched register-plus-ancilla occupation number. Exact rational ancillary probabilities `p_i=A_i/D_i` then define the product invariant law without estimating an extremely rare Gibbs population from passive occupancy. Unbiased-bit integer rejection uses fewer than `2 ceil(log2 D_i)` random bits in expectation with logarithmic storage. The requested physical occupation still has to be written, verified and protected. This is an engineered reservoir, not an assertion about all thermal baths.

Full occupation SWAPs with fresh matching ancillary bits supply a native independent refresh backbone. It must operate in deployment, and its actual selection weights and durations are included. Unknown extra correlated rates may be tiny or zero; they are not assumed to have a fast reverse channel.

## Exact clocked first-failure meaning

Use fixed finite cycles of duration `T`, with specified port selection weights and padded service. The endpoint Markov matrix is `P=sum_j w_j K_j`, and the analytical generator `Q=(P-I)/T` has exactly the same endpoint first-failure mean: `M_lab=T E[N]=(-Q_A)^-1 1`. Under a separate rate normalization, apply the stated `T Lambda` conversion. Continuous-time generator notation does not make pulses instantaneous or grant free parallel service.

Cap integer-sampling, write/verification and port-selection retries. **A timeout performs a null tick; every branch is padded to the same duration.** Resampling desired ancillary patterns for free or conditioning the operating clock on successful preparation would change the kernel. Pay collision time, factory retries, detector service, dephasing, reset and protected idles. There is no claim about a failure occurring inside an unobserved coherent pulse; failure labels are classical registered endpoints.

## Finite-factory error and a nonreversible perturbation theorem

The finite extension assumes stable basis states, a write success lower bound `w0>0`, independent conditional label errors `e<1/2`, nondemolition/nonbackacting checks, actual dephasing, protected idle storage and memory removal between preparations. Repeating verification gives wrong-majority probability `nu<=exp[-2r_chk(1/2-e)^2]`; conditional wrong accepted write is at most `nu/[w0(1-nu)]`. Thus target error `xi_bit` costs order `log(1/(xi_bit w0))/(1-2e)^2` checks, with real sensor time and retry factors.

For maximum local size `k`, `p_min=min_i p_i>0`, choose `xi_bit<=zeta p_min^k/(4k)` and allocate uniform timeout loss per requested pattern. The successful dephased ancillary subprobabilities are within `1+-zeta` of the intended product weights. Actual ancillary bits can be correlated and their induced kernel slightly nonreversible, yet every off-diagonal operating rate satisfies `(1-zeta)q(x,y)<=q_actual(x,y)<=(1+zeta)q(x,y)`. The support is preserved by this construction. Label-error probability without dephasing would not control coherent amplitudes in the same way.

For `n_safe=|A|`, a positive directed tree/forest expansion gives **for every safe start**, without requiring actual reversibility,

```text
(1-zeta)^(n_safe-1)/(1+zeta)^n_safe
  <= M_actual/M_ideal <=
(1+zeta)^(n_safe-1)/(1-zeta)^n_safe.
```

Hence log-mean error is at most `(2n_safe-1)[-log(1-zeta)]`. With `n_safe<=2^m`, `zeta=epsilon_fac/(4*2^m)` suffices. The sensitivity coefficient is exponential, but the specified independent QND verification suppresses error exponentially in the number of checks: required log precision is `O(m+k log(1/p_min)+log(k/epsilon_fac))`. Paid finite service can grow polynomially, including quadratic factors in `m`; this is not a generic hardware claim of exponentially precise preparation for free.

Acquisition bands include the finite-factory bias of the data-producing apparatus; the operating-factory ratewise comparison is a separate budget. Clock tolerance and starting-write errors are also separate. This extension does not cure arbitrary leakage, readout backaction, coherent residual errors, common causes, ageing or unknown baths. The [equilibrium-safe start result](equilibrium-safe-start.md) separately accounts for its deliberate initial law. No source program or physical experiment was rerun here. [Original package and provenance](SOURCES.json).
