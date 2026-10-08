# Astra 2026-10-08: local invisibility of dynamically generated global entanglement

**Status:** Independent algebraic corollary for the specified ideal collective-bath initial condition; self-contained and all-time. External novelty and correctness review UNKNOWN. Attach to previous `state/2026-10-08-far-from-equilibrium-near-unit-entanglement.md` and Maxwell notes; no new source claims.

## Theorem: every fixed subsystem tends to infinite-temperature noise, uniformly in time

For the `N`-spin-one-half, initial `rho_N(0)=I/2^N` collective Lindblad dynamics

`d rho/ds=(nu+1) D[J_-]rho + nu D[J_+]rho`,

where `nu>=0` can even be arbitrary as a function of `N` for THIS local-marginal result, let `rho_{N,R}(s)` be the density of any `r` selected qubits. For **every fixed integer r>=1**,

`sup_{s>=0} (1/2)||rho_{N,R}(s)-I/2^r||_1 = O_r(N^(-1/2)) ->0`.

This bound is uniform in time, in `nu`, and in the chosen subset R of size r. Its proof uses only (i) permutation invariance, (ii) conservation of the total-spin j sector weights, and (iii) maximally mixed initial weights. It remains true for any dynamics preserving these three conditions, not only the Lindbladian shown.

## Proof: permutation moments and the rare-spin Schur distribution

The initial maximally mixed state and the symmetric Lindbladian imply `rho_N(s)` is invariant under permutations, all s. `J²` commutes with both jumps, so the probability distribution over total-spin irreducible sectors remains its initial distribution, with `M=2j` and

`w_{N,M}=[(M+1)^2/(N/2+M/2+1)] binom(N,(N-M)/2)2^(-N)`.

The binomial Gaussian bound `binom(N,(N-M)/2)2^(-N) <= C N^(-1/2) exp[-c M²/N]` and the prefactor `<=C(M+1)^2/N` imply all fixed moments

`E_w[j^r]=O_r(N^(r/2))`.

(The tail estimate with these constants can be made uniform for every `0<=M<=N`; for large M, the binomial tails are even smaller.) Thus, for any sequence of indices `a1,...,ar` from {x,y,z}, the expectation of the product of collective operators is bounded by

`|Tr(rho_N(s) (2J_a1)...(2J_ar))| <=2^r E_w[j^r] = O_r(N^(r/2))`,

because each `J_a` preserves total spin j and has norm <=j on that sector, independent of state within the sector. The same holds for unordered noncommuting products, because only the operator norm bound is used.

For fixed distinct sites `1,...,r`, define the Pauli string correlator `C_{a1...ar}(s)=Tr[rho_N(s) sigma_a1^(1) ... sigma_ar^(r)]`. Permutation invariance gives

`(N)_r C_{a1...ar} = Tr rho_N(s) sum_{i1,...,ir DISTINCT} sigma_a1^(i1)...sigma_ar^(ir)`.

The unrestricted sum is exactly `product_{p=1}^r (2J_ap)`. Removing tuples with an index collision changes the operator norm by at most the number of colliding tuples `O_r(N^(r-1))` because every Pauli product has norm 1. Divide by `(N)_r∼N^r`:

`|C_{a1...ar}(s)| <= O_r(N^(-r/2)+N^(-1))` uniformly in s and bath parameters.

For `r=1`, this is `O(N^-1/2)`; for any fixed `r>=2` and a Pauli string acting nontrivially on all r sites, it is `O_r(N^-1)`.

Every r-qubit marginal admits the Pauli expansion

`rho_{N,R}(s)=2^(-r)[I^(tensor r) + sum_{P nonidentity r-Pauli strings} Tr(rho P) P]`.

Each nontrivial Pauli coefficient involves between one and r selected sites; the bound above shows all of them are `O_r(N^-1/2)` (indeed weight>=2 strings are `O_r(N^-1)`). Triangle inequality in trace norm of Pauli strings gives a finite, r-dependent constant times `N^-1/2`. QED.

### Distinction and implications

Combine this **all-time local marginal theorem** with the prior transient theorem. For any `c_N->infinity` with `c_N=o(logN)`, at `s_N=c_N/sqrtN` simultaneously:

1. `dist_T(rho_N(s_N),SEP_N)->1`: global near-maximal entanglement measured by random common-axis LOCAL product measurements of *all N spins* and one global classical sum.
2. `dist_T(rho_N(s_N),rho_N(infty))->1`: global thermal mixing has not occurred.
3. For each **fixed** r, `sup_{|R|=r}dist_T(rho_{N,R}(s_N),I/2^r)->0`: any bounded-size subsystem looks infinite-temperature/uncorrelated in trace distance.

This is global-vs-local *detectability separation*, not a quantum secret-sharing code or a proof of cryptographic data hiding against unrestricted LOCC: indeed the witness is LOCC with **N** readouts. It is also compatible with the repository's N120 all-time entanglement depth ≤2 claim, so it does not establish genuine many-particle entanglement depth.

`nu` may grow with N for the local theorem alone because the Schur sector distribution is exactly conserved regardless of jump rates; the near-unit and mixing limits require ν fixed finite. This split is crucial.

### Prior work and boundaries

Stationary reduced-marginal near-white estimates were already in Astra N130; this proof extends to **every time**, and the combination with far-from-equilibrium near-unit fullSEP distance is new within the current investigation. General permutation-invariant quantum de Finetti and representation-theoretic trace estimates may already imply local convergence; do not claim novelty without independent priority review. We do **not** assert closeness for `r` growing with N, due to the r-dependent constants in the Pauli expansion, nor immunity to fixed local depolarizing noise for the near-unit global entanglement.