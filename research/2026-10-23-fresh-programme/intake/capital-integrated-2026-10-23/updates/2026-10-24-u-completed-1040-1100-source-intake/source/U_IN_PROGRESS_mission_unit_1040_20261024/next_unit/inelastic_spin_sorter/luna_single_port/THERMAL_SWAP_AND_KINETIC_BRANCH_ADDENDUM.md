# Thermal-SWAP completion and kinetic-branch correction

Scoped addendum to the full-cycle audit. It checks an ideal same-gap TLS
reset completion and the specified independent-beam kinetic-energy
convention. The earlier single-energy thermal-mixture expression applies
only when its branch energies are held fixed as defined there; for the
current fixed-kinetic-energy beam, use the branch relation below.

## Exact ideal SWAP and its work ledger

Let A be the ring TLS and B a supplied same-gap TLS,
`H_A+H_B=Delta(n_A+n_B)`. Let W be the full Hermitian SWAP, so
`W=W†`, `W²=I`, and `[W,H_A+H_B]=0`. Under
`H(t)=H_A+H_B+J(t)W`, all Hamiltonians commute at different times, and

```text
U(T) = exp[-i(H_A+H_B)T] exp[-i W integral_0^T J(t) dt].
```

A smooth envelope with J(0)=J(T)=0 and area `integral J dt=pi/2`
therefore gives the full SWAP up to the free evolution. The thermal stock
`tau_beta` is stationary under that free evolution. If B begins in
`tau_beta`, A ends exactly in `tau_beta` and uncorrelated with the
departed electron; the old A state and its electron correlations move to the
spent B.

The control-work contribution in this ideal Hamiltonian model is exactly

```text
W_on = integral_0^T Jdot(t) Tr[rho(t) W] dt = 0.
```

Indeed, `[W,H(t)]=0` makes `Tr[rho(t)W]` constant and J has equal,
zero endpoint values. This is zero *net work for the declared control
Hamiltonian*, not a claim about the real driver's losses, coupling
implementation, or ancilla supply. For `|J|<=Jmax`, the pulse duration
obeys `T >= pi/(2 Jmax)`; its finite duration and the thermal ancilla stock
remain part of the cycle. If the target population before swap is q and the
stock population is p_T, the swap transfers energy
`Delta(q-p_T)` from A to B; the pair's energy is conserved. Rethermalizing
B to `tau_beta` costs/exports that energy according to the same heat/work
ledger as in the main note. The spent B also carries A's entropy and
correlations; it must be rethermalized or disposed of before reuse.
The exact reset assumes B is independently prepared in `tau_beta`. If its
actual stock `sigma_B` has trace-norm error at most `eta_B` from `tau_beta`,
the ideal SWAP transfers exactly that same state error to A; the population
error is at most `eta_B/2` and its energy error at most `Delta eta_B/2`.
The spent B retains the pre-swap A correlations. These are input-stock and
disposal errors, not covered by the zero control-work identity.
If the realized pulse area has error `delta_theta`, then
`||exp[-i(pi/2+delta_theta)W]-exp[-i pi W/2]||<=|delta_theta|`; the
resulting pair-state trace-norm error is at most `2|delta_theta|`.

## Finite packet and finite-delay interface

The exact product-reset statement assumes the electron has departed the
ring before the swap. A finite-width normalizable packet does not have a
strictly finite departure time. For a finite interaction region coupled to
regular continuum leads, a smooth packet supported away from thresholds,
with no bound-state component, has local interaction-region amplitude given
by decaying Fourier integrals and tending to zero asymptotically. A finite-delay
implementation needs an actual tail bound at the chosen swap time; overlap
with a nondecaying ring-bound state would invalidate the departure premise.

A precise finite-error interface is: if the actual joint state at reset/readout
differs from the ideal asymptotic scattering state by trace norm at most
`eta`, then the expectation of any bounded signed spin-flux effect differs
by at most `eta` (with the observable normalized to operator norm at most
one). To claim finite-time preservation, bound the residual packet/ring
interaction or directly bound this trace-norm error. The smooth finite
SWAP itself preserves the outgoing electron marginal once the ring and
electron are decoupled. Narrowing the packet to secure energy continuity can
lengthen its temporal envelope and the required delay; no delay or dwell-time
number is supplied here.

## Fixed-kinetic-energy thermal beam

For the supplied independent-beam convention, the incident electron kinetic
energy is `E_in` in both TLS branches. The initially excited TLS branch
has total incident energy `E_in+Delta`; the reciprocity relation supplied
for this model gives its signed transmitted spin flux as
`-F_0(E_in+Delta)`, not `F_1(E_in)` at the same total energy. Thus

```text
F_thermal(E_in) = (1-p_T) F_0(E_in) - p_T F_0(E_in+Delta).
```

There is no universal tanh factor or cancellation: the two ground-stock
responses are evaluated at different electron energies. A tanh expression
would require the extra flat-response premise
`F_0(E_in+Delta)=F_0(E_in)`.

For a normalized packet with kinetic-energy amplitude h(E), the corresponding
time-integrated flux is

```text
F_packet,beta = (1-p_T) integral |h(E)|^2 F_0(E) dE
                - p_T integral |h(E)|^2 F_0(E+Delta) dE.
```

Assume the ground-stock scattering response is regular near E_* and the
packet support is chosen in an open-channel interval where
`F_0(E) >= F_* - epsilon`, with `F_*=F_0(E_*)>0`. Since each signed
spin-flux difference is bounded in magnitude by one,
`|F_0(E+Delta)|<=1`; hence

```text
F_packet,beta >= (1-p_T)(F_* - epsilon) - p_T.
```

For `F_*=0.010535`, take `epsilon=F_*/4` and `p_T<F_*/8`
(`beta Delta > about 6.63`). This sufficient bound gives
`F_packet,beta>F_*/2>0`, regardless of the sign or detailed energy
dependence of the excited-stock branch. The condition on the ground-stock
interval is the only continuity requirement for this bound; verify the
shifted branch's open-channel/reciprocity premises in the actual lead model.
The width remains existential, not a practical bandwidth claim.

This gives a finite-temperature, finite-width, model-level nonzero-flux
condition under the stated kinetic convention. It does not establish an
acquired beam, reset device, finite-delay bound, efficiency, or performance
advantage.

