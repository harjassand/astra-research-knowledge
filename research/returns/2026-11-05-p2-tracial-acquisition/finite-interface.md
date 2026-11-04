# Finite mixed-bath collector, routing, qualification and error costs

This [physical supplement](package/physical_interface.txt) implements the [partial-SWAP output-only receiver](partial-swap-decoder.md) with finite registers and local exchange controls. It pays actual source encounter windows, routing, initialization, calibration, storage and isolation. The complete [report](package/tracial_acquisition.pdf) uses half diamond errors throughout. A finite schedule under specified control/noise resources is not a demonstrated platform meeting those budgets.

## Local register and operation count

A qubit module has an `N+2`-cell nearest-neighbour junction: source, `N` fresh bath cells and a separate maximally mixed dummy. During capture round `j`, collide the source with the next fresh logical token and route its output through the remaining fresh cells using `N-j` full SWAPs. Earlier output correlations remain intact; routing only permutes tensor factors, preserving logical input freshness. At capture's end outputs are in reverse chronological order.

Close the source port. Inverse-collide the receiver dummy with the newest output, move the dummy by a full SWAP, and continue through the older outputs; omit the final move. Thus

```text
capture routing = N(N-1)/2 full SWAPs,
decoder routing = N-1,
total two-qubit gates G=(N^2+5N-2)/2,
peak operation qubits = N+2.
```

A strict one-dimensional line adds `N` routing SWAPs. One unknown payload is consumed, without postselection. Full-SWAP routing is an allowed receiver operation; it is not a new source interaction.

Source pulse duration is `theta/J_S`. Signed receiver exchange uses inverse duration `theta/J_M`; positive-only exchange can instead use `(pi-theta)/J_M`. Each full routing SWAP costs `pi/(2J_M)`. Switching/addressing/settling and actual initialization are additional. The supplied serial layout takes `O(N^2)` operation time and `O(N^3)` coherent memory space-time at fixed hardware speeds. No optimal wall-time or storage claim is made.

The **weak source port** additionally has a maximum encounter window `tau_enc` and bounded coupling `J_S`, so whole encounter action is at most `J_S tau_enc`. The receiver cannot extend that encounter, return its token or concatenate nominal weak rounds on the same token. Switchable exchange alone does not enforce this restriction: permitting duration `pi/(2J_S)` supplies a full source SWAP, which is the simpler matched-access alternative.

## Whole-environment initialization and finite physical error

For independent actual bath/dummy inputs `tau_j`, put `x_j=d Tr(tau_j^2)-1`. Their whole-input preparation error is at most `sqrt(product_j(1+x_j)-1)/2`. For `L` qubit inputs with Bloch norm at most `beta`, `beta=O(epsilon_init/sqrt(L))` suffices. The comparison replaces the **whole initial environment once**, retaining all later output correlations; good local marginals do not certify a correlated preparation.

Independent ideal Pauli twirls can make exact mixed product cells with two random bits per cell, provided every operating preparation key is inaccessible. Keeping the key changes physical access. Approximate twirls acting on correlated raw inputs need composable channel bounds, not a marginal-state argument. Factory random bits, Pauli pulses, key disposal, memory and source/dummy preparation are resources.

Sufficient total error is the intrinsic `c r` plus whole initialization error, the sum of actual gate half-diamond errors, source and correlated-memory noise exposures, and source-off isolation error. A residual coherent source/retained-memory coupling supplies forbidden feedback unless bounded; a sufficient error term is `integral ||H_off(t)||dt/hbar` over every nominally closed interval, including decoding. Long routing makes isolation substantive. Quoting only a single-qubit coherence time does not establish a bound for correlated retained outputs.

## Paid qualification

Under a closed, stationary, context-independent two-qubit CPTP gate model and trusted state preparation/readout, prepare the tested gate's normalized Choi state using two input/reference Bell pairs and measure 255 nonidentity four-qubit Pauli observables on separate trials. A direct coefficient-error certificate bounds half diamond distance by `(q/2)sqrt(sum_P coefficient_error_P^2)` for gate input dimension `q=4`, including statistical and known systematic widths. These calibration references are paid laboratory resources, not accessible operational bath purifiers. There is no need to treat a nonphysical fitted channel as the certificate.

Conservative single-module qualification costs are `O(N^5 epsilon^-2 log(N/alpha))` gate trials and `O(N^2 epsilon^-2 log(N/alpha))` independent-factory trials. For `m` modules with a global error target, the supplied bills grow as `O(m^3 N^5 epsilon^-2 log(mN/alpha))` and `O(m^2 N^2 epsilon^-2 log(mN/alpha))`. Reused pulse configurations can reduce some constants, but actual gate configuration, references, readout, precision, trial time and confidence allocation remain paid.

These conditional calibration procedures do not certify exact tracial freshness, absent preparation keys, absence of arbitrary hidden ports or coherent return interactions. The product-module theorem still requires product emission, although final collective decoding and entangled payloads are allowed. The [main converse](README.md), [exact receiver](partial-swap-decoder.md) and independent companions retain their separate scopes. No diagnostic code, hardware experiment or new Capital audit was run. [Original package and hashes](SOURCES.json).
