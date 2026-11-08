# B research capital: uniform polynomial sampling after the qualifying noise time

**Release date: 8 November 2026.**

**Result:** a finite-bit, randomized, uniform-polynomial full-output sampler in the explicit qualifying-time regime below. This closes the previous repeated-recursion complexity gap. **The full all-time B goal remains open:** the unqualifying early/intermediate-time interval is not covered.

This is a theoretical construction, with two independent end-to-end mathematical reviews and reproducible checks of its algebraic components. It is not a formal machine-checked proof, a production sampler, a demonstrated practical speedup, or a historical priority claim. Human expert review is appropriate before an external theorem claim.

## The precise supported statement

Fix a rational constant rho_0 >= 0. The input consists of:

- n qubits on a finite subset of the square lattice;
- a **static**, rational Hermitian Hamiltonian with onsite and nearest-neighbor two-qubit terms;
- a rational bound h on each **grouped physical support**: sum all terms on the same site or edge before imposing this bound;
- an arbitrary rational product density matrix, pure or mixed;
- the same positive rational replacement rate gamma at every site, with h/gamma <= rho_0;
- rational time T >= 0 and requested total-variation error 0 < epsilon <= 1/2.

The evolution is

    L(rho) = -i[H,rho] + gamma sum_i (E_i(rho)-rho),
    E_i(rho) = (I_i/2) tensor Tr_i(rho).

Let tau = gamma T. A sufficient qualifying condition is

    r_8(tau) = 307584 + ceil(60 rho_0 tau),
    tau >= 76932 + 2 ceil(log_2 r_8(tau)).

For every fixed rho_0, all sufficiently large tau satisfy it. A separate late mixing shortcut also handles instances for which its certified error is small, even if the displayed condition is not needed. The h=0 case is the independent one-qubit noise law.

Within this scope, the construction samples the **entire joint computational-basis output distribution**, with unconditional TV error at most epsilon, using

    poly(B_input) (n/epsilon)^(C_rho_0)

bit operations and random bits. C_rho_0 is a finite computable constant, independent of n, epsilon and the supplied time. B_input includes all rational encodings and the site list. The polynomial degree is not claimed uniform if rho_0 grows with the input.

Disconnected geometric components are handled separately; no algorithm pads an exponentially large coordinate gap between them. Work is bounded on every randomized branch, including failed estimates. Sequential coupling, rather than conditioning the whole output on success, pays estimation failures and coin-rounding error in the final TV bound.

## What changed

The previous constructive bound in the same qualifying regime was

    exp[L exp(O_rho(1 + log* tau))],  L = O(log(n/epsilon)).

Its exponent was not uniform in time. The new ingredient is an exact-rational coefficient-MPO evaluator for static patches, with explicitly paid growing-width rank and bit complexity. Its subexponential patch cost is used only on **child activity patches** of size O_rho(L log L), at numerical action O_rho(log L).

This stops the old warm-boundary recursion after one level. The one-level precision enlargement is still paid; it is not assumed to disappear. The resulting cost is exp(O_rho L), uniformly throughout the qualifying regime. Fixed qualifying action was already polynomial before; this is the improvement when time and system size grow.

## Read in this order

1. `DEPENDENCY_MAP.md`: the complete proof chain and which older statements are superseded.
2. `proofs/b_static_patch_mpo_20261108/THEOREM_AND_COST.md`: the reviewed theorem, scope and parameter map.
3. `proofs/b_static_patch_mpo_20261108/PROOF_DRAFT.md`: the new patch construction, rank accounting and exact-rational gauge algorithm. The historical filename is preserved.
4. `proofs/b_static_patch_mpo_20261108/combined_audit/COMBINED_AUDIT.md`: first fresh combined review.
5. `proofs/b_static_patch_mpo_20261108/independent_audit/END_TO_END_AUDIT.md`: second fresh end-to-end review.
6. `CORRECTIONS.md`, `SOURCES_AND_PRIORITY.md`, and `REPRODUCING.md`.

The theorem/proof snapshots contain pre-review phrases such as “proposed,” “would,” and “review target.” Their mathematical content is unchanged; presentation-only edits remove operational wording, relocate paths and label historical status. SOURCE_PROVENANCE.json records every original source hash, packaged hash and edit. **Those historical status phrases are superseded by the two final reviews and this release note.** Older reports' then-current limitations should be read using the dependency map.

## Important limitations

- The unqualifying early/intermediate action interval remains unresolved. Its bounded length at fixed rho_0 does not imply an algorithm.
- The sufficient cutoff and polynomial exponent are enormous. Many ordinary finite-size instances have already mixed before the cutoff. This is asymptotic theoretical capital, not evidence of useful runtime.
- There is no claimed extension to arbitrary time-dependent Hamiltonians, higher-body interactions, nonunital or nonuniform noise, or arbitrary correlated initial states.
- The code implements and checks mathematical primitives, including a small coefficient-MPO dynamic program. It does **not** implement the whole asymptotic sampler.
- The tools are substantially prior art. The checked nearest results do not directly subsume this assembly, but no exhaustive novelty or priority clearance has been made.

## Original reviewed source identities

- Theorem SHA256: `aa2164737f3847e21cdb17d0160b3f147e21c32f98b24c5c758a324935bfd27f`
- New proof SHA256: `9dd686f76130f5bf1edaa78376c9a53f50835c8401ea9699a907fca0d6399662`
- First combined review SHA256: `358dd674249a8311593b5a88d7a99bab5dc061824618aa957ed28f00367647ae`
- Second end-to-end review SHA256: `e18422e01fba658933aea6d341873d9418025c8c220672f07e7010e98cc045ee`

These are the original reviewed hashes, not hashes of the presentation-edited release copies. SOURCE_PROVENANCE.json maps both versions.

Run `python VERIFY_MANIFEST.py` to check the complete release, and see `REPRODUCING.md` for clean diagnostic reproduction. The package includes the complete project proof dependencies and review snapshots; externally established mathematical results are explicitly identified and linked rather than silently treated as new proofs.
