# Distributed VALID-HOLD interlock: no single release bit is authority

Status: new fixed-hole controller candidate. Its logical safety argument is exact under the stated honest-bank/fault-domain contract; the actual native bad-bank multiplicity and whole overlapping-epoch theorem remain to be proved. This is not a change to any frozen accepted source.

## 1. Why the ordinary beacon phase is insufficient

A single corrupted release phase can otherwise expose an entire tentatively filled hole whose clock values are still arbitrary. Read-only compilation does not prevent this logical fanout. A replicated copied 'valid' bit would not help if all copies were produced from one faulty source.

Instead use m independently implemented validator banks at DISTINCT physical sites. Each bank has its own native controller and its own held pause-reservation bit at every REPAIR owner. No bank copies another bank's PASS result. All banks independently inspect the actual clock constraints while the repair writers are physically parked.

## 2. Source-level interlock contract

Each bank has INVALID, CHECK, VALID-HOLD (and honest FAIL/retry) program states. A structurally honest bank:

* starts CHECK only after a fresh actual reset and actual PARK+W0 verification of every relevant REPAIR writer while its own pause bits are held;
* checks the actual causal clock constraints using current native snapshots, not a cached completion message;
* enters VALID-HOLD only after that check succeeds;
* keeps its own pause reservations held for the whole VALID-HOLD interval;
* becomes INVALID BEFORE releasing those reservations for a new repair epoch.

Every ordinary COMPUTE attempted channel independently reads the actual states of ALL m banks, and is enabled only when all are VALID-HOLD, in addition to its ordinary causal and invalid-halo guards. No shared authoritative enable bit is inserted. A bad COMPUTE hub can bypass its own test only as a bounded local dirty retirement, not authorize all other hubs.

Every nominal tentative-clock or purge write requires the repair mode in which the banks are invalidated. In particular, old VALID-HOLD results cannot coexist with a clean new purge/fill that changes their source clocks. Actual DATA erase additionally uses the native FREE/ERASE or fresh PARK adapter source guard; a classical mode alone is not permission to cut a quantum prefix.

## 3. Safety with at least one honest held bank

If all banks currently say VALID-HOLD and at least one bank b is structurally honest, take b's most recent entry into that state. At that point it saw a valid clock field and every REPAIR writer was quiescent. Its reservations have remained held since then. Thus no subsequent CLEAN repair write can invalidate that field. Clean ordinary COMPUTE updates preserve causal validity by their own current guard.

Any remaining invalid clock values must therefore arise from a direct physical root or a dirty native writer after that validation, not from an unchecked whole-hole repair phase. Such writes retain their own bounded root footprints. A fault to a shared clock after validation is not hidden as an honest certificate: it is precisely a new clock root, and the ordinary invalid-halo guard still applies.

The conclusion uses actual held reservations, not merely a historical certificate. Repeated reads of one stale source bit cannot manufacture an honest validation: each bank performs its own ground-truth check, and nobody converts another bank's bit into its own VALID-HOLD.

## 4. What replication number would suffice, and what is still owed

If one physical root can directly or through a single straddling native retirement corrupt at most b validator domains, then m>b leaves an honest bank after one root. The correct b is NOT automatically q, the number of physical sites in the perturbation. A resource root can also straddle an active verifier, and owner-tag coherences need a common-span analysis. Exclusive ownership/read-only gates suggest a fixed multiple of q rather than the number of sequential readers, but that actual statement must be proved.

For k roots, m>bk is a possible finite safety budget. This alone is not a threshold: increasing m may enlarge footprints/overlap constants, and a noncircular physical norm theorem is still required. The candidate must not silently choose k larger than an exponent that grows with its own hardware.

Startup must provide actual fresh INVALID banks or charge their bad preparation. Arbitrary extensive initial VALID labels are not accepted as certificates. Partial release, component merging, forged provenance and retry liveness remain explicit construction obligations.
