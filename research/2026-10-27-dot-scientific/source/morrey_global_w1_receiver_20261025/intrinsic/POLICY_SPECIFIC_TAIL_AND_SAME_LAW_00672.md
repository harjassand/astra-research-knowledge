# Exact policy-specific tail: SAME finite17-law upper below.0672

**Independently audited PASS.** See `INDEPENDENT_STATIONARY_LYAPUNOV_TAIL_AUDIT.md`. The prior17-law
chain was independently accepted at.06738397494526557<.0674. The improvement
here is precision only for the EXACT SAME21504-cutoff law and AC completion.

New received same-law upper: **.06718566499649657 < .0672**.
No new root weights, controls, source coupling, cutoff or AC parameter are used.

## The inexpensive missing certificate

The inherited variance argument bounded expected ordinary steps by768 and gave
a uniform21504-cutoff conditional W1 tail payment1/4096. That bound applies
widely, but ignores this particular frozen controller's terminal decisions.

For its substochastic ordinary-transition matrixP, a numerical sparse solve
selected a vector. That solve is NOT a proof and is not repeated by the receiver.
The saved dyadic vector (denominator2^20) is now checked by exact rational
arithmetic at EVERY3844 state and3338 directed transition edge:

    1 <= v <= 958733/65536 < 15,
    v(root) = 3233431/262144 < 13,
    P v <= (15/16) v.

The minimum exact row slack is89843/1048576>0. All probabilities and target
indices come from the actual policy file; every row's stopping and ordinary
probabilities sums exactly to1. The policy's physical null/full-completion
validity is the independently accepted parent premise, identified by hash.

Since1<=v andP is positive,

    P^n 1(root) <= P^n v(root) <= 13 (15/16)^n.

This bounds the probability of still executing ordinary controls at stepn.
Couple the finite and a.s.-complete policies identically until the finite
counter forces its already specified full chord completion. They differ only
on that tail event, with Euclidean displacement at most4 in[-1,1]^3. Thus

    W1(finite_N, complete) <= 52 (15/16)^(N-1).

UsingN-1 is conservative for either before/after-transition counter convention.
No assumption about final chord orientation or density is needed for this
bounded-diameter coupling. Exact integer power comparisons receive:

- SAME existingN=21504 instance: conditional W1 tail<=2^-1024.
- SAME existingN=19968 instance: conditional W1 tail<=2^-1024.
- OPTIONAL DIFFERENTN=1024 instance: conditional W1 tail<=2^-80.

The1024 statement is a reusable shorter-controller consequence, NOT silently
adopted into the current law. The main result only reprices the existing21504
instance. A future chosen1024 instance must have its own finite-law provenance.

## Received scalar consequences

Multiply the conditional tail by the exact root probability of the stationary
baseline component. Keep each already received raw-law source upper and the
separate10^-24 whole-law AC cost unchanged. This gives:

- SAME previous16-law finite+AC upper.06755186814622662;
- SAME new17-law finite+AC upper.06718566499649657<.0672.

The former16→17 raw-law distance decrease against the SAME rational finite
source was.0003954267442488992. The old crude two-tail transfer was negative
(-.00000272724), correctly recorded as a failure at that time. With the newly
received SAME-law tails, the finite+AC distance decrease is now at least
**.0003954267344509399** against that SAME finite source. This does not order the
true cosine-source distances; their upper certificates improve separately.

Raw atomic laws and their AC completions remain distinct. A finite atomic tree
is not assigned positive affinity to the continuous source.

## Frozen small replay

- `stationary_tail_lyapunov_vector.json`: proposed exact rationals, policy hash.
- `receive_stationary_tail_lyapunov.py`: exact rows and integer powers,~.04s.
- `stationary_tail_lyapunov_receipt.json`.
- `receive_stationary_tail_same_law_transfer.py`: root weights, parent hashes,
  unchanged cutoff/AC, exact scalar consequences,~.01s.
- `stationary_tail_same_law_transfer_receipt.json`.

The floating proposal in `stationary_tail_lyapunov_proposal.npz` is archival
selection evidence only. Neither its solve nor any optimizer is needed for
replay. Original audited source receipts are left byte-for-byte unchanged.
