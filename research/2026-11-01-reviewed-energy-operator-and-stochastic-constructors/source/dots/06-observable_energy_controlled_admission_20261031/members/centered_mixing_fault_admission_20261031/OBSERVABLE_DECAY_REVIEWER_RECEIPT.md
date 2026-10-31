# Independent whole review: observable-decay local admission

## Source binding and verdict

Reviewed the entire `OBSERVABLE_DECAY_LOCAL_ADMISSION_CANDIDATE.md`, SHA-256 `faedb2f2f8ec0c491f4ade4d71a4075df143eb7fa2489c8f0e8c091a0af5d37e`, including the final examples paragraph. **PASS as a finite-register, finite-schedule initialized-dilation local-amplitude theorem under its stated locality, actual-generator, derivative/residual and instrument premises.** This does not promote the source to a complete hardware or fault-tolerant implementation. No mathematical correction is required.

This is a fresh full review, not reliance on the author's earlier receipt against c2905f13. Frozen source and author's receipt remain untouched.

## 1. Single-patch calculation

For z=x+iy and V=I+2yK/r, the tilted Hamiltonian contribution is exactly 2yKV. Since G*I=0 and G*K=-rK+J, its linear term cancels the source drift. The remainder is 2yJ/r+4y²K²/r. The sign of the imaginary coupling and the sign of the weight are therefore consistent.

Time differentiation and intended Hamiltonian add (2y/r)(partial_t K+i[H0,K]). Hermiticity permits an upper bound by its norm times I. With q=2Rc/r<=1/2, I<=V/(1-q)<=2V, yielding precisely the coefficients 8R²c²/r and 4R/r in equation (1). No estimate of a stationary state, spectral gap of the whole source, or Gaussian moments occurs.

The residual premise is substantive. A data-only term has J=rK; choosing a fictitious large r then does not suppress its contribution. Time variation and noncommuting gates likewise remain in d. The norm c bounds the total patch interaction, not each summand independently.

## 2. Product weights, outside interactions and source reuse

The product argument uses disjoint source AND data supports of simultaneous patches, not statistical independence. For a source generator confined to one such block, its adjoint applied to the product equals its action on that factor times the other factors. Multiplication of the single-factor Loewner inequality by these commuting positive factors is legitimate. Outside real unwanted interactions commute with the selected factors by the actual patch-support premise, so they stay ON without an uncharged contribution. Intended controls must meet the same commuting-support or explicitly charged-commutator requirement.

A generic interacting source generator spanning two simultaneously different patches is outside this proof even if its stationary state happens to factorize. Shared coherent controller or spectator operators are not automatically disjoint: their commutators must actually vanish as stipulated. Classical recorded adaptive branches can be treated blockwise when the prescribed common schedule and uniform bounds hold. The theorem does not license arbitrary coherent common-control operators by calling them records.

Initial entanglement among source blocks, data and reference does not affect an operator inequality. At any time, it can be applied to the actual unnormalized tilted state. No conditional source-state reset is used.

Insertion at a location start costs 1+q in squared norm; removal at its end costs (1-q)^-1. Removing all ending factors before inserting new factors also works for immediate reuse of the same source. These are comparison steps on the same state, not physical operations. An internal jump in K costs at most 1+4R||Delta K||/r, bounded by the stated exponential; the total variation is charged in d. Finite intended unitaries within a location cannot be treated as zero-cost time intervals.

System-only instruments at common weight-free boundaries are contractions in their initialized, record-retaining Stinespring implementation. At such a boundary V=I, so their norm-one action is sufficient. An instrument while another selected weight remains active is not covered merely because it is system-only; the source correctly requires a separate weighted inequality. These qualifications make the boundary telescoping sound.

## 3. Analytic history dilation and inclusive faults

For a finite register and a well-defined finite-rate, piecewise bounded Markov generator on the finite time horizon, choose the same initialized jump-history spaces for all complex couplings. The no-jump propagators are entire in the selected variables, and so are products separated by jumps and fixed initialized instrument isometries. On any compact polydisc, the k-jump sector norm is bounded by a constant times sqrt((T sum_j sup_t||L_j(t)||²)^k/k!). The sector-norm sum converges. Thus the full history isometry continuation is operator-norm analytic; equivalently a direct finite-horizon bounded-coefficient Dyson construction suffices. No uniform bound on arbitrary incoming field states is inferred.

For complex couplings the history map is not an isometry, but its output norm squared is the trace of the corresponding CP, non-trace-preserving tilted evolution. Applying the preceding weight inequality to that evolution, including the insertion/removal factors, proves equation (2). Positivity of the tilted evolution and finite-time bounds suffice; normalization or Jensen inequalities for a normalized state are not assumed.

The inclusive fault operator is the alternating omission sum, or equivalently the part of the common analytic expansion containing positive degree in each selected variable. Summing the Cauchy coefficient bounds over all those positive degrees gives (sum_{j>=1}R^-j)^k=(R-1)^-k. This is an operator-amplitude bound for one common initialized dilation, not a product of marginal probabilities, a bound on sampled jump counts, or a claim that a reduced channel error equals its square root.

All variables outside the selected set remain at physical value 1. The product-weight estimate is valid for every selected set, including repeatedly reused sources, because it only needs the instantaneous support assumptions and charges each selected interval's two boundaries. Arbitrary input purification is included. Actual preparation, measurement, control errors and code-specific receiving still require their own assigned locations and hypotheses; this theorem alone is not a threshold theorem.

## 4. Constants, degeneracies and examples

Taking the square root of (2) gives the stated eta. The bound atanh(q)<=2q proves (3). For d=0, the proposed R obeys 4cR/r<=1/2 and 4R²c²tau/r<=1/4. With R>=2, (R-1)^-1<=2/R, giving exactly (4). If this chosen radius is below 2, that simplified admission is unavailable, not evidence of suppressed noise. The c=0 branch is correctly separate. Positive r and finite supplied budgets are essential.

Thermal amplitude damping gives G*X=-(lambda+a)X/2 exactly. Pure Z dephasing gives G*X=-rX while conserving Z, so no primitive full-source convergence premise can be hidden in the proof. Sums of X_i tensor A_i in one patch obey the same eigenoperator identity, even with noncommuting data A_i, but require ONE weight for their total K. Their factors must not be multiplied cellwise.

For isotropic depolarization r/4 sum D[Pauli], each source Pauli decays at rate r. The exchange operator XX+YY+ZZ has eigenvalues 1 and -3, hence norm 3; the final noncommuting-source example is correct. It is a small exactly propagable fixture, not a computational advantage. The one-axis thermal example admits an ordinary classical telegraph description of its system process; source-output/coherent-source-control equivalence is not being claimed.

At fixed diffusion c=sqrt(r)b, the leading term stays proportional to b sqrt(tau). This agrees with the separately certified exact damped-qubit lower benchmark and does not evade it. Nor does this result contradict shared-bath no-go examples: simultaneous unrestricted source sharing violates its source-patch premise.

## 5. Ordinary comparisons and what is actually added

I reopened the primary [Ng–Preskill Gaussian-noise paper](https://arxiv.org/html/0810.4953) and [Preskill's collective Hamiltonian-noise criterion](https://arxiv.org/html/1207.6131), and made a focused search for operator-specific/mixing admission alternatives. This is not exhaustive novelty clearance.

Ng–Preskill already obtains microscopic all-selected fault control from Gaussian correlations, with a square-root correlation-integral noise scale. Exponential covariance gives the same c sqrt(tau/r) order. Its free-field/Gaussian structure is a real condition; an observable eigenoperator identity for a finite source does not by itself supply Wick factorization. The current proof instead establishes a complex-coupling operator bound directly. It neither invents the scale nor establishes superiority over all Gaussian methods.

Preskill's operator-norm, many-body Hamiltonian criterion supplies a strong general non-Markovian receiver with arbitrary bath dynamics. Applied directly to bounded patch coupling c, its norm accounting does not automatically acquire inverse-r suppression. A stronger transformed or coarse-grained application must earn the relevant local/all-order error bounds rather than infer them from a two-point curve. That paper expressly discusses dressed effective interactions, so it should not be caricatured as forbidding all fast-source exploitation.

The scoped mathematical addition checked here is an explicit sufficient eigenoperator/residual condition yielding finite-rate all-selected initialized-dilation bounds for this local source model, including nonprimitive and warm correlated inputs. Positive weighted estimates, tilted CP evolutions, analytic coefficient extraction and standard fault-path receiving are ordinary ingredients. Historical originality, hardware feasibility and practical benefit remain unestablished.

## 6. Executed checks

The supplied diagnostic script was read and rerun from a copy under `producer-workspace/observable_decay_reviewer`, leaving source and saved author JSON unchanged. It has 60 exact rational operator/positivity checks and three floating cross-dilation checks with source reuse and a real outside interaction. The floating checks are diagnostics, not certified numerical inequalities or proof of the theorem. The proof review above is independent of their numerical success.
