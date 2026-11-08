# Precise proposed combined result and dependency boundary

> Release-copy note: this historical proof/review snapshot has presentation-only edits recorded in SOURCE_PROVENANCE.json. Mathematical content is unchanged. Current status and superseded steps are identified in START_HERE.md and DEPENDENCY_MAP.md at the package root.

8 November 2026. New patch proof and one-level substitution have passed one independent review. A separate fresh end-to-end review of the older dependencies is in progress. This opening records the status before the final reviews.

## Proposed uniform qualifying-time sampler theorem

Fix a rational upper bound rho_0 on the coupling-to-noise ratio and fix the two-body square-lattice locality convention. Let n qubits occupy a finite square-lattice region. Geometrically disconnected components are processed independently, with a divided TV error budget; no padding across arbitrarily large encoded coordinate gaps is allowed. Only connected activity/parent patches use the O(N^2) bounding-rectangle padding argument. The Hamiltonian is static, with one grouped rational Hermitian onsite term per site and one grouped rational Hermitian two-qubit term per nearest-neighbor edge, each of norm at most a supplied rational bound h. If the input supplies several contributions on the same physical support, they are first summed; h bounds that grouped sum, not each member of an arbitrarily long term list. A computable constant-dimensional entrywise bound can be used instead, changing only the fixed ratio constant. The input is an arbitrary rational product density, pure or mixed. Every qubit undergoes replacement noise at the same positive rational rate gamma:

    L(rho)=-i[H,rho]+gamma sum_i(E_i(rho)-rho),
    E_i(rho)=I_i/2 tensor Tr_i(rho),
    h/gamma<=rho_0.

If h=0, use the independent one-qubit replacement-noise law directly, with paid finite precision for exp(-tau), rather than dividing by a vanishing Hamiltonian scale in a regularity parameter. Equivalently a safe nonzero coefficient bound max(h,gamma) can be used in intermediate norm lemmas. Let T>=0 and 0<epsilon<=1/2 be rational, tau=gamma T, and let P be the full joint computational-basis output distribution after time T.

Use the original b=8 sufficient accumulated-noise contract, with Delta=5:

    r_8(tau)=307584+ceil(12 rho_0 Delta tau),
    tau>=76932+2ceil(log_2 r_8(tau)).

Equivalently one may choose a fixed integer tau_0(rho_0) large enough that this inequality holds for all tau>=tau_0. Exact rational comparisons and integer logarithm ceilings can implement the test. The global entropy-mixing shortcut remains separately available whenever its own TV bound is small enough, including small-n instances.

The combined construction would produce a randomized finite-bit classical sampler with unconditional output law Q satisfying

    TV(P,Q)<=epsilon

in at most

    poly(B_input) * (n/epsilon)^(C_rho_0)

bit operations and random bits, for a finite constant C_rho_0 independent of n, epsilon and the supplied time. All branches obey the same resource cap; discovery failures and finite-random-bit errors are included in the TV budget. The final guarantee uses sequential coupling: conditioned on the actual preceding prefix and internal history, fresh scalar queries have their uniform per-query failure bound, and each next-bit kernel differs from the true one by at most its good-estimate error plus failure probability plus rounding error. Summing these stepwise errors proves the unconditional TV guarantee. The proof does not condition the entire output law on a global event that all estimates succeeded. B_input includes the rational Hamiltonian/state/noise/time/accuracy encodings and site list. Rational normalization by gamma is charged in B_input, not as an unbounded numerical inverse-gamma factor. All sufficiently long times are handled by mixing before any large-time computation.

For a uniform choice of all regularity parameters across the promised input class, expand each grouped term into its finitely many Pauli terms, omit global identities, and use d=63, k=2, J_bound=gamma*max(rho_0,1). Then a_0=1/[252 max(rho_0,1)], p=2/(1+a_0), u=a_0/2 and theta=a_0/4 are fixed computable constants. The polynomial degree is not claimed uniform when rho_0 itself grows with the input.

This is a general noncommuting two-body 2D late-regime statement: it does not require conserved controls, Gaussian closure, weak bridges, feedback positivity, a random input ensemble or a restricted final output set. It DOES require the stated static, uniform replacement-noise, rational product-input model and the accumulated-noise contract.

## Why the exponent becomes time-uniform

Let L=O(log(n/epsilon)) include the old scalar accuracy and failure allocations. Outside the scalar/mixing shortcut, tau=O(L). The old outer activity decomposition has at most exp(O_rho L) required work/queries, quantum patches N_parent=O_rho(tau^2+tau L), and physical scalar log precision O_rho L under the pinned-KP budget.

For a parent patch, the old warm-boundary construction uses dimensionless action

    sigma=s_base+2ceil(log_2(tau+2))=O_rho(log(L+2)).

The old discovery and sparse propagation require exp(O_rho L) membership queries, each a normalized positive product-input/product-effect scalar at sigma, with one-level log budget L'<=A_rho L. That fixed factor is retained; it is not falsely set to one.

Re-expand each such scalar at its OWN time sigma using the same qualifying activity theorem. Its physical activity patches have

    N_child<=K_rho(sigma^2+sigma L')=O_rho(L log(L+2)).

Only these child patches are sent to the new direct static evaluator. The whole parent patch is NOT directly evolved densely at sigma. Arbitrary switched shapes are retiled with deleted edges preserved; padded decoupled identity factors affect only the logarithmic global budget.

For a child scalar error eta=exp(-O_rho L), a diamond approximation error eta*2^(-N_child) pays the positive output-effect norm. Its logarithmic channel accuracy is E=O_rho(N_child+L). The exact rational coefficient-MPO algorithm has work exp[O_rho(N_child^(7/8) polylog N_child)] in the relevant polylogarithmic-time regime. For N_child=O_rho(L log L) this is exp(O_rho L), uniformly in L. If N_child=O_rho L, ordinary dense computation already fits the same bound; no subexponential asymptotic estimate is needed in that branch.

The child expansion therefore has exp(O_rho L) cost. Multiplying by the exp(O_rho L) outer membership/activity count still gives exp(O_rho L). There is no further time descent, so the old A_rho factor does not repeat at log* depth. All classical Ursell, clipping, finite-bit and prefix-sampling costs remain in the existing polynomial budget.

## Improvement over the previously delivered bound

The earlier constructive qualifying-time bound was

    poly(paid inputs) * exp[L exp(O_rho(1+log* tau))].

Its polynomial exponent was not uniformly bounded as tau and n grew. The proposed replacement gives exp(O_rho L) throughout that same qualifying-time regime. This is a real asymptotic improvement when tau grows with n; fixed qualifying tau was already polynomial before. The older proof and archives should be retained as prior stages, not silently relabeled as having proved the new result.

## What remains open

The interval of unqualifying early/intermediate times below tau_0(rho_0) is NOT covered, except individually solved subclasses, the trivial initial-time law, and instances already handled by mixing. Although this is a bounded dimensionless interval at fixed rho_0, no general polynomial algorithm for it is supplied here. Therefore the full all-time B goal remains unresolved.

The constants in the accepted accumulated-noise condition and resulting polynomial exponent are extremely large. This is not a practical implementation, a demonstrated runtime improvement on useful lattice sizes, or an end-to-end production sampler. The prototype tests validate algebraic primitives only.

The new proof has not established a noise threshold improvement, an extension to general nonunital noise, time-dependent Hamiltonians, arbitrary entangled inputs, or an original-B hardness result.

## Prior and review history

The polynomial cut-count/MPO construction is based on Mackay et al., arXiv:2609.27497v1. Exact skeleton/TT interpolation is established prior (Oseledets–Tyrtyshnikov2010). The growing-layer dimension accounting, paid rational-gauge reset and specific warm-time closure are set out so that their use can be checked; no scientific priority/novelty clearance is claimed.

The independent new-step audit is independent_audit/AUDIT.md. It clears the new Sections2–4 and the algebraic Section5 substitution, conditional on the older contracts. Fresh end-to-end audits of those dependencies were subsequently completed; see the release status.

The completed result closes a specific previously unpaid operation and strengthens the asymptotic construction with a reusable exact-rational evaluator proof. Its scope is uniform polynomial sampling in the qualifying late regime; early times remain open. No practical or novelty claim is made.
