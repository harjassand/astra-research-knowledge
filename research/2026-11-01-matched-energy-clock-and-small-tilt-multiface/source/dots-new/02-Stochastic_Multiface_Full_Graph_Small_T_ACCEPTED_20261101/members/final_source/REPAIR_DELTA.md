# Additive receiving repair — mathematical theorem unchanged

Prior source freeze: 887f0cb10b7c5c3c3f3b56e59b09100a0ba9e46f58e1a69d21cdbfa73ea2a27e.
Original folder and scalar-corollary freeze remain unchanged. This new folder is a
separate candidate and requires independent receiving before any acceptance.
The governing mathematical theorem remains SHA256
dc96226443a99ee0a8541f03cce5af28ff735a95c6855053d223cf87d5001327.

## Actual defects repaired

1. A valid positive rational rate with numerator2^20000 raised an unhandled Python
   decimal-digit-limit ValueError during normalized model hashing. Large integer
   and rational serialization now uses exact tagged hexadecimal above4,096 bits,
   with no process-wide safeguard change. Tagged rationals, integers and power
   exponents are received exactly; conservative power-bit bounds still refuse
   enormous expansion. Error-budget integers also have safe formatting.
2. Normalized certificates depended on raw channel insertion order because the
   internal tuple was unsorted. It is now canonically sorted after aggregation.
   Ordered parsed-input identity is recorded separately in the API envelope;
   normalized model identity is named explicitly. Legacy raw_sha256 aliases the
   normalized identity, not original file bytes.
3. Ordinary Python equality admitted float/Boolean replacements for exact integer
   fields. Receiving now uses guarded, iterative, exact-type comparison. The
   guard rejects excessive depth, queued/visited nodes, invalid keys/leaves,
   cycles and shared containers before canonical production. It adapts retained-
   clock v4 receiving capital rather than making a new correctness premise.
4. Explicit exact-domain validation now covers low-level mask/exponent budgets
   and expression power-bit budgets. Boolean expression leaves are rejected.
   Expression structure is guarded before recursive arithmetic as well.

## Scope and new tests

No generator formula, source cone, resource, subset weight, tilt, finite-head or
moment formula changed. The new raw receipt adds only the explicit normalized
identity field; certificate byte count changes accordingly. The old original
and old conservative-dA theorem versions are both preserved under history/.

All original author tests were rerun on the new constructor. Added regressions:
20,001-bit rate and JSON round trip;21 reordered raw lists; split duplicates;
three numeric-type mutations; exact budget domains; unchanged decimal guard;
28 finite-tree/alias/depth/pending-node checks. Malformed trees are proven not to
reach the expensive producer. These are same-author checks, not independent
acceptance and not a substitute for the global proof.
