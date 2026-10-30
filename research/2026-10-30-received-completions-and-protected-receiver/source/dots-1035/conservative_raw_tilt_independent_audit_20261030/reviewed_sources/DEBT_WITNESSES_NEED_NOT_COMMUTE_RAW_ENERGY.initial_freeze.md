# Actual semantic-debt witness can fail to commute the raw DATA energy
2026-10-30. Exact small counterexample to a prospective shortcut, not a defect in the reviewed own-corner moment argument.

## Result

The actual nominal derivative of a combined semantic/history debt projector can have raw-stabilizer off-diagonal entries. Therefore its finite-time resolvent and local polynomial witness cannot be assumed to commute the raw energy. A controller-only multiplicative-credit argument requires a new weighted CP construction; ordinary pointwise debt moments do not supply one.

## Actual malformed source

Take an Alice two-qubit read of S=X_0 X_1 with raw commuting check T=Z_0 Z_1 also present. Its accepted elementary gate word is H_b, controlled-X_0, controlled-X_1, H_b. The onsite H_b rail edge uses resource 1 as its native partner. In an ownership mask missing resource 0 and owning resource 1, the missing controlled-X_0 edge breaks the clock path. The terminal forest component is exactly

    V=H_b controlled-X_1.

This entire terminal source is mechanically bad because ownership is incomplete. Its combined Q projector is therefore I on this source, for all workspace and DATA inputs. Suppose other parent histories are good and every other private token location is empty. The actual terminal retires this parent and writes HOLD(DATA(y)), where y is the final b computational value. The target combined debt effect is just

    F_false=(I-Z_b S)/2.

Complete source-resolved terminal erasure pulls it back to

    V^* F_false V = (I-X_b X_0)/2.

Thus the terminal's healing effect on this source is

    D_heal=(I+X_b X_0)/2.

It is positive, but it does not commute with the raw contribution U_T=(I-T)/2. Their commutator has Frobenius norm sqrt(2) in the three-qubit example. All the other nominal terms have zero Q drift in this bad-source block: C-to-B rollback keeps the parent bad; failed-test transitions stay bad; monitors commute; idle communication can be chosen absent by empty locations. Hence this is an actual noncommuting derivative block, not an arbitrary target observable imported from outside the machine.

In particular, E_t^*Q=Q-t kappa D_heal+O(t^2) has nonzero commutator with U_T at first order. Its short-time integrated resolvent inherits this obstruction. It is still supported in its OWN Q corner; here that corner is the entire bad source. No conflict exists with positivity or the invariant zero range.

## Surviving statements and next boundary

The current debt proof uses products only on separated supports and ordinary Holder only on the commuting Q_i, not on overlapping Z_i. It needs no commutation between Z_i and U. The raw exponential inequality also survives: this wholly bad terminal is paid by its healed mechanical weight, without claiming prefix normalization.

A possible future route is the actual V-weighted CP transform O -> V^{-1/2} L^*(V^{1/2} O V^{1/2}) V^{-1/2}, which is subunital because L^*V<=0 and remains local because V is an exponential of commuting bounded local terms. That observation alone is NOT a service theorem: local weighted killing, own-corner transport, multiplicative witness rules and continuous-noise bounds must all be earned in the transformed generator. No such extension is accepted by this note.

Regression: check_debt_witness_raw_noncommutation.py / .json. Formula error 1.11e-16; healing-effect spectrum [0,1] to roundoff; commutator norm 1.4142135623730947. The example is exact algebra; numerics only verify the implementation.
