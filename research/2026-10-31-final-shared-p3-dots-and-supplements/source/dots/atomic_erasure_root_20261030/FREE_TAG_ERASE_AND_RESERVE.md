# Atomic free-tag erase and reservation
2026-10-30. Root local construction; actual modified-alphabet review pending. It is a physical safety alternative to trusting an adapter's cached ACK. It does not prove the entire purge protocol or logical computation.

## Hardware operation
At a DATA resource cell r, enlarge its fixed finite owner-tag alphabet by one distinguished reservation label ERASE. Let P_free be its actual FREE-tag projector. An onsite erasure/reset instrument has resolved Kraus operators

 J_a = sqrt(kappa) |ERASE><FREE|_tag tensor K_a,data,
 sum_a K_a† K_a=I_data.

Additional local adapter control conditions may further restrict this source, but MUST NOT replace P_free. The tag reservation and DATA operation occur in the SAME actual jump, not as a later acknowledgment. The source effect is kappa P_free. All native acquisition edges must accept exactly FREE, not ERASE. Existing code/owner cleanup tests must be rechecked for the new tag.

## Exact clean-prefix exclusion
Assume the actual native machine has the already-used properties:
1. Every mechanically clean C or inverse-B prefix owns every resource it can affect, and retains those owner tags until its true terminal retirement.
2. Every nominal payload operation, including malformed/dirty prefixes, acts only on its actual owned resources; it cannot use an unowned DATA register by interpreting a corrupt program value.
3. Acquisition before commitment has no DATA action.

For every clean live prefix h using r, its projector has tag_r=o_h, orthogonal to P_free. Therefore J_a P_clean,h=0 exactly. No adapter clock state, stale verification bit, or incorrect ERASE request can make this erasure hit that clean live prefix.

An acquisition/erasure race is linearized by the mutually exclusive tag sectors: the erasure acts only on the still-FREE branch and reserves it; the already-owned branch is not erased. Until release, ERASE blocks every new nominal acquisition. This is valid for coherent tag/clock superpositions, since it is an operator source-support statement, not a trajectory ordering assumption.

If a physical fault has already freed a tag after a prefix used r, that owner is mechanically dirty by the actual consistency definition. Subsequent erasure can then affect it, but that is a charged dirty-owner propagation case, not erasure of a clean prefix.

## What is not earned
The jump may still erase useful unknown DATA when an erroneous request arrives while the resource is free. Thus semantic authorization, fault-locality and correction remain necessary. It does not make an arbitrary erasure logically harmless.

The reserved tag needs actual release/healing rules. An orphan ERASE label can block useful work; a false release can violate a larger frozen-collar protocol. Neither liveness nor a truthful completed purge is supplied by this lemma. A malformed adapter can emit repeated free-tag erasures unless its own return/healing mechanism is earned. Complete adapter recovery may still be needed to bound the number of such errors.

The entire composite DATA/control resource remains a fixed-dimensional hardware site. The physical erasure jump is onsite; it does not condition a jump on a remote collection of PARK states or introduce a multisite dissipator. Its utility is precisely replacing a fragile cached authorization for clean-prefix exclusion by a local physical reservation. Any additional global ACK or epoch conclusion requires a separate construction.
