# Reset-before-release is necessary for a transaction-level DATA fault contract
2026-10-29 22:09 UTC. Root working analysis, not independently reviewed.

The proposed one-way acquisition-to-computation commit eliminates coherent computation-to-acquisition rollback. It does not by itself establish transaction isolation for corrupted computations.

In the old generator, every abort label R claims no resources. Thus a corrupted computing hub can enter R, coherently release owned resources through cleanup, and reverse R -> its original computing phase while retaining its workspace. The reverse edge is enabled precisely by the original failed consistency test. A neighboring clean hub may acquire a released data resource and perform its operation before the corrupted hub finishes using its remaining resources. The corrupted workspace can carry quantum correlations across that interleaving.

This is not a counterexample to the owner-history no-creation theorem. It is a counterexample to the structural inference 'no C -> A edge therefore all data contacts occur inside one exclusive transaction'.

Repair candidate: abort labels originating in computation must retain the same claim set as their source computation until the actual complete workspace-reset jump to Q0. In particular cleanup on any owned resource must be forbidden in C and in all R_(C,j). Abort reset must precede release. Acquisition-origin abort labels can release resources without a computation claim, provided no coherent path connects them to computation before a fresh complete commit reset.

A physical fault can still directly steal or relabel a lock. That releases isolation through a charged fault, not through the clean generator. Its support determines all immediately affected owners. After such a theft, the surviving dirty owner must not acquire further resources before a reset. The intended fault object is therefore initially a bounded-region quantum comb extending to regeneration, not an instantaneous Pauli flip.

Outstanding proof: combine reset-before-release with a tail for the ACTUAL no-regeneration CP instrument. Bad-projector expectation decay alone does not bound elapsed time until workspace reset. Even a successful bound does not turn a temporally extended comb into one instantaneous SSF error unless all required isolation and serializability claims are proved.
