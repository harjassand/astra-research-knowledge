# Full-cycle resource and finite-error audit

Bounded audit of the supplied three-site nonmagnetic inelastic spin sorter.
The operation is spin sorting by energy exchange with a nonmagnetic two-level
system (TLS), not net spin creation and not a claim about the microscopic
origin of the static spin-orbit phase. No device or acquired performance is
asserted.

## Scattering energy ledger

Take the TLS Hamiltonian as H_TLS = Delta |1><1|, with Delta>0, and let
p_in and p_out be its excited-state populations before and after one
scattering event. The static electron-ring-plus-TLS Hamiltonian conserves
total energy. Thus, for a monoenergetic incident electron of energy E,

```text
mean outgoing electron energy = E - Delta (p_out - p_in),
change in TLS energy          = Delta (p_out - p_in).
```

For an initially ground-state TLS, p_in=0. If P_exc is the total
probability of outgoing channels with the TLS excited, the electron exits at
E-Delta on those channels and at E on the others; its mean energy loss is
exactly Delta P_exc. The sum includes both transmitted and reflected
channels. Inelastic excitation probability is therefore an energy-transfer
ledger, not a free by-product of spin sorting.

If the TLS is returned to its input population p_in, its energy change over
scattering plus reset is zero. With positive Q_out denoting heat delivered
to reset reservoirs and positive W_out work extracted during reset, the
first law for a reset with decoupled endpoints is

```text
Q_out + W_out = Delta (p_out - p_in).
```

For an initially ground TLS and a passive ground-reset bath, the
complete-reset limit gives Q_out=Delta P_exc if no work is extracted. If
work recovery is used, the
same transferred energy can be divided between work and heat. This identity
does not assert that all excitation energy must become heat, nor does it
assign an efficiency: that depends on the reset protocol, bath, and
correlations. Since the TLS may be correlated with the outgoing electron,
reset also disposes of those correlations. A local trace-preserving reset
does not change the electron's reduced state after the electron has left, but
the used reset ancilla/bath must still be returned or discarded.

## Finite-temperature reset and stock

For a thermal TLS stock at inverse temperature beta, the excited
population is

```text
p_T = 1 / (1 + exp(beta Delta)).
```

A finite-rate thermal reset with downward/upward rates r_down,r_up gives
p(t)=p_T+(p(0)-p_T) exp[-(r_down+r_up)t]. It approaches its finite-T stock
only asymptotically; a finite wait leaves a residual error. The net energy
flow during reset is Delta (p(0)-p(t)) to the reservoir under the stated
fixed-gap Markov model.

An exact finite-operation reset to a finite-temperature stock is available
in the model by swapping the ring TLS with a supplied, same-gap thermal TLS
ancilla. The target then has population p_T; the used ancilla carries the
target's pre-swap state and any correlations with the outgoing electron. Its
energy changes by `Delta (p_out-p_T)`; the target changes by the opposite
amount, so the pair's total energy is unchanged because the gaps match.
This is an ideal excitation-conserving SWAP with decoupled endpoints; any
physical implementation's coupling-switch work belongs in the ledger.
Re-thermalizing or discarding that spent ancilla is part of the cycle. The
swap transfers the target's correlations with the outgoing electron to the
spent ancilla. Its entropy and correlation must be exported or erased before
that ancilla is reusable; `p_out` alone does not specify that entropy cost.
For a diagonal TLS marginal the entropy is `h_2(p_out)`, while a coherent
marginal requires its full von Neumann entropy. A pure ground-state
ancilla would instead make an exact ground reset, but supplying and restoring
that pure stock is an additional resource; it is not furnished by a
finite-temperature bath at finite time.

For repeated operation, the required stock is one fresh thermal ancilla per
scatter/reset or an explicit rethermalization line for each used ancilla.
The stationary reservoir temperature, ancilla preparation error, exchange
time, and disposal/rethermalization cost are parameters of the operation.
The ideal ground-state calculation is only a benchmark, not an acquired
finite-temperature cycle.

The electron source is also part of the cycle: an initially ground TLS
returns an electron with mean energy lower by `Delta P_exc`, so maintaining
the same incident energy in later runs requires replenishing that energy in
the source, or accounting for recovery from the outgoing electrons. No such
source/recovery apparatus or efficiency is specified here.

## Finite-width input and finite-temperature continuity

Let F_0(E) be the signed transmitted spin flux per normalized incident
electron for a ground-state TLS, with the supplied one-energy result
F_0(E_*)=F_* ~= 0.010535 > 0. Let F_1(E) denote the same observable for
an initially excited TLS. Since it is a difference of probabilities,
|F_0|,|F_1|<=1. For a thermal diagonal TLS state, linearity gives

```text
F(E,p_T) = (1-p_T) F_0(E) + p_T F_1(E),
F(E_*,p_T) >= F_* - 2 p_T.
```

Thus any finite-temperature stock with p_T < F_*/4 retains at least
F_*/2 flux at the center energy. For the quoted point value, this sufficient
condition is p_T < 0.00263375, or beta Delta > log((1-p_T)/p_T) at the
boundary (approximately 5.94). This is a continuity margin, not a claimed
temperature or measured operating window.

For finite bandwidth, choose a compact interval around E_* that stays away
from all lead-channel thresholds and scattering poles, with every channel
needed for the thermally populated input open. For a finite graph coupled to
regular leads, its finite-dimensional lead-self-energy scattering formula
is continuous on such a regular open-channel interval. Hence there is a
nonzero width w for which |F_0(E)-F_*|<F_*/4 throughout
|E-E_*|<=w. Combining this with p_T<F_*/8 gives
F(E,p_T)>F_*/2 there. Any normalized smooth packet with nonzero finite
spectral width supported in that interval therefore has integrated signed
spin flux

```text
F_packet = integral |h(E)|^2 F(E,p_T) dE > F_*/2 > 0.
```

The one-point value alone does not certify that E_* is away from a threshold
or singularity; this regularity is a condition to verify in the stated lead
model. The width is existential because the supplied result gives no
derivative or distance-to-threshold data. The finite-width sufficient bound
p_T<F_*/8 corresponds to beta Delta greater than about 6.63. This establishes persistence of
nonzero flux under sufficiently small finite packet width and thermal
population in the stated scattering model; it does not establish a practical
bandwidth, a device rate, a useful polarization, or net spin generation.

## Scope boundary

The whole outgoing electron includes transmitted and reflected parts. With
the stated spin-conserving static Hamiltonian, polarization is redistribution
between outgoing channels; it is not spin creation. The given reciprocity
relation S_- = S_+^T and the supplied inequality
T_avg |P_T| <= P_exc,reflection <= P_exc,total mean that the transmitted
spin imbalance is accompanied by reflected/inelastic accounting; do not
describe it as creation of net spin from an unpolarized input. Reset energy,
thermal stock, finite packet width, and reflected output remain part of the
operation. The formulas above are conditional resource accounting for the
specified static model, not a general lower bound on heat or a hardware
demonstration.

