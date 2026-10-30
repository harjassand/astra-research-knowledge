# Exact clean committed transaction instrument
2026-10-29 22:12 UTC. Root derivation; requires independent review and the corrected transactional generator.

## Model and statement
A private hub has acquisition endpoint A_k and distinct computation positions C_0,...,C_L. The complete irreversible commit instrument is J_s=sqrt(kappa_c)|C_0,0><A_k,s|. In the clean owner-history range, A_k has every resource in its fixed read footprint owned by that hub. There is no coherent C-to-A edge. Computation and computation-origin abort labels retain ownership claims until a complete terminal/abort reset to Q_0. Every payload gate checks its actual resource tag.

The computation Hamiltonian is a finite Feynman path with edge payload unitaries U_t and positive finite hopping amplitudes g_t. Clock-position monitor/reset instruments are diagonal in computation position and do not inspect the workspace. The terminal instrument has separately resolved channels sqrt(kappa_T)|Q_0,0><C_L,s| for every workspace basis s, with equal rates. All nonterminal computation losses are clock-only. Clean consistency forbids abort drives. Workspaces are private.

Claim: for a committed clean transaction with arbitrary data/reference input, the unnormalized first-terminal-reset DATA instrument at elapsed time t is

  dI_t = f(t) dt Phi,
  Phi(rho) = Tr_W[V_L (rho tensor |0><0|_W) V_L^dagger],
  V_t=U_t ... U_1.

Here f is a nonnegative scalar first-reset density independent of the DATA input. The same factorization holds for any specified workspace-blind clock-monitor record, with a record-dependent scalar density. This does not assert an exponential waiting law, nor correctness of the uncompleted bare-data marginal.

## Proof
Use the full unitary gauge W=sum_t |C_t><C_t| tensor V_t, with V_0=I. On the committed, consistent sector, W^dagger H W is the ordinary scalar hopping path tensor identity on DATA/workspace. Every clock-diagonal monitor commutes with W. The summed terminal loss is kappa_T |C_L><C_L| tensor I, hence also gauge-invariant. Thus the killed no-terminal evolution, including any workspace-blind monitor record, acts only on the clock in this gauge. Starting at C_0 with workspace0 gives a scalar C_L amplitude/probability multiplied by V_L on DATA/workspace. Summing the separately resolved terminal workspace labels applies exactly the partial trace, proving the factorization.

The terminal record's total probability is f(t) dt because Phi is trace preserving. An additional unresolved clock-record sum preserves factorization. A single coherently summed workspace reset would not give this channel and is excluded.

## Overlapping hubs and serial clean records
In the clean range, two committed hubs sharing a resource cannot coexist: a resource lock has one owner label. A commit event is a genuine reset instrument; after it, all tags on the committing hub's footprint are fixed to that owner on the surviving clean branch. Competing acquisitions cannot alter those tags. Until its terminal reset, all other committed DATA operations therefore have disjoint footprints and commute with this transaction's internal circuit. Acquisition dynamics may evolve, but touch payload data only after their own commits.

Consequently, conditional on an actual sequence of commit and terminal reset locations/times, clean completed DATA channels compose in the corresponding conflict-respecting serial order. Concurrent disjoint transactions can be ordered arbitrarily. Clock probabilities can depend on the history of locks and completed transactions but not on the encoded DATA input. This representation includes the environment's ordinary jump record as a mathematical unraveling; it does not assume a noiseless external classical controller measures or acts on that record.

## Limits
A local kick can leave a hub outside the clean history range, change tags, or create coherent phase branches. The above gauge proof then does not apply to that owner. Reset-before-release helps isolate such episodes but does not turn the complete noisy process into this clean renewal model. A bounded-region, finite-lifetime quantum-comb/fault contract and actual no-regeneration tails remain required. Finite-time bare output must also account for unfinished clean prefixes.

This lemma constructs clean operation semantics using maintained reset and fixed gate interactions. It does not discover the correct recovery rule, remove its implementation cost, establish a noise threshold, or show advantage over a conventional scheduled Feynman/Stinespring realization.
