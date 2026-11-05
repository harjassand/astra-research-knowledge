# Robust preparation of interacting one-dimensional Gibbs states

P3's completed visible return supplies a structural theorem and compatible noisy preparation operation: at fixed finite temperature and bounded local interaction range/strength, one-dimensional Gibbs states admit positive local-noise precompensation with a radius independent of chain length and requested accuracy. Noncommuting terms and entangled thermal states are included. The sufficient constants are prohibitive; no practical threshold or total-resource advantage is earned.

The [complete visible return, prompt and expanded activity](P3_NOISY_PREPARATION_CONSEQUENCE_20261105_RETURN.txt) are published byte-for-byte. The native reader's notation-preserving first 20,000 characters accompany the complete rendered response, whose later sections contain additional deductions and audits. The [original ZIP](original/Astra_Robust_Many_Body_Preparation_Research_Package.zip) arrived through the existing local transfer during intake. All 23 members are published, including the [22-page report](package/Astra_Robust_Many_Body_Preparation.pdf), [definitive structural proof](package/research/comparators/robust_1d_block_opening.md), [operation and resource ledger](package/research/operation_and_consequences.md), [independent proof audit](package/research/noncommuting/robust_1d_independent_audit.md), [composition audit](package/research/noncommuting/operation_audit.md), code and recorded checks. The [complete accepted predecessor ZIP](package/accepted_predecessor/Astra_Noisy_Thermal_Interface_Research_Package.zip) matches its published original byte-for-byte. All 22 supplied member checksums match; see the [package guide](package/README.txt), [manifest](package/MANIFEST.json) and [source metadata](SOURCES.json). The capture's historical pending-transfer header remains unchanged.

## Exact structural consequence

For `H=sum_j h_j` on an `N`-qubit chain or ring, assume bounded term density, `||h_j||<=1`, support on at most `r` consecutive sites, and fixed finite `beta>=0` and `r`. There are computable constants `B(beta,r)<infinity` and `eta(beta,r)>0`, independent of `N` and accuracy, such that

```
rho_beta = E_mu tensor_(A in P_mu) tau_(mu,A)
|A| <= B
tau_(mu,A) >= eta I_A / 2^|A|.
```

Each partition consists of contiguous blocks. The states and partitions have constructive classical descriptions. Unlike a pure-block decomposition or the exponentially small global Gibbs eigenvalue, this full-rank block floor provides a volume-independent margin.

For arbitrary single-site channels satisfying `||Lambda_i-id||_diamond<=delta`, the sufficient radius

```
delta_0 = 1-(1+eta/2^(B+1))^(-1/B) > 0
```

keeps every block inverse `Lambda_A^-1(tau_A)` positive, with at least half its original floor. Averaging those positive preimages gives a state whose product-channel output is exactly `rho_beta`. Heterogeneous, nonunital and non-Pauli channels are allowed in this mathematical range theorem. It does not implement an inverse channel on arbitrary unknown inputs.

The [full-rank construction and physical operation](full-rank-blocks-and-noisy-operation.md) distinguish that broad mathematical theorem from the narrower apparatus model. The [boundaries, costs and additional deductions](boundaries-factories-and-costs.md) retain the exact endpoint obstruction, cold-temperature limits and separate local-factory contract.

## Scientific scope and provenance

The completed physical route inherits protected computation, acquired independent product endpoints, stationary independent Pauli primitive faults, the specified shared component law, prescribed export time, noisy Bell/tree interfaces, and paid nonlocal links, acquisition, reset and cooling. Within that model it supplies arbitrary global trace accuracy at fixed sufficiently small positive primitive noise. Arbitrary near-identity channel positivity alone does not commission a general unknown apparatus.

The target Hamiltonian is supplied digitally. A target holding Hamiltonian, isolatable target-check couplers and target Davies bath are therefore unnecessary for this preparation task. Learning an unknown material Hamiltonian is still a separate operation. Earlier [noisy thermal-interface](../2026-11-05-p3-noisy-thermal-interface/README.md) results are reused at their earned scopes. The [continuous-time noisy-controller dossier](../2026-11-05-autonomous-quantum-correction-opening/README.md) retains its open global quantum gate-order/protected-idle theorem, and earlier Gibbs records remain unchanged.

The source reports completed separate algebra/physical-composition audits, two passing finite verification suites and a passing final finite-arithmetic audit. Their stated scopes are preserved; no new scientific audit or replay was imposed. Finite identities and examples are not physical experiments, a threshold measurement or a favorable resource demonstration. Original audit/check files are included unchanged in the delivered package.
