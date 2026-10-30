# Phase-weighted Green: combine low launch with its preceding clearing

30 October 2026. Explicit finite-shift detail for the exp(lambda B) extension.

In a high-A Green block that clears from B=b>=q to B=b-q<q, the low approach must be composed with that clearing BEFORE its exp(lambda B) ratio is bounded. Calling the low approach merely bounded would introduce a fixed multiplier on every block and could destroy contraction.

With no noncompulsory low immigration:
- If b=q, clearing reaches 0, the compulsory neutral immigration reaches 1, and activation returns to q. Net B change is zero.
- If q<b<2q, immediate low activation returns to b-1. Net B change is minus one.

Thus the ordinary no-race combined block has nonincreasing B. Extra low races have probability O(1/A), with a bounded possible B overshoot, and contribute only O_lambda(1/A) to its weighted norm. If the low approach consists entirely of immigrations until B=q, its terminal B is at most the original b; it is harmless for the phase weight as well.

An INITIAL low-phase input, without a preceding clearing, pays a fixed exp(lambda q) multiplier once. It does not recur as a multiplier on every high block. Consequently the high-A nonseed continuation remains `1-p+O_(theta,lambda,s)(1/A)<1`, as required by the phase-weighted Green proof.
