# Clamped Kawasaki preparation and full-cycle ledger

Bounded audit of the six-site binary ring, with periodic edges and the
full relative two-network energy. Set `J=h S m^2/4`, `sigma_i=±1`,
`sum sigma_i=0`, and
`m_i=m(sigma_i+sigma_(i+1))/2`. During the three proposed exchanges hold
both network displacement fields at `u=v=0`; this is a temporary clamp
control, not an added on-site substrate potential.

## Exact swap costs at the clamp

At `u=v=0`, an edge with `sigma_i sigma_(i+1)=p` has energy

```text
e_i = h C m^2/4 + B p,
B   = h(C-S)m^2/4.
```

Equivalently, an unlike edge costs `J`, while a like edge costs
`h C m^2/2-J`; changing unlike to like costs `2B`. For `C>S`, such a
change is uphill. In the stated sequence,

```text
sigma:       +-+-+-   ++--+-   ++-+--   +++---
sum p_i:       -6       -2       -2        +2
swap:           —      (2,3)    (4,5)     (3,4)
Delta E:        —       4B        0         4B
```

The first swap changes edges `(1,2)` and `(3,4)` from unlike to like; the
central exchanged edge `(2,3)` remains unlike. The second changes `(3,4)`
from like to unlike and `(5,6)` from unlike to like, so its pair changes
`-2B,+2B` cancel exactly; `(4,5)` stays unlike. The third changes `(2,3)`
and `(4,5)` from unlike to like; `(3,4)` stays unlike. Thus the total
clamped potential increase is `8B=2h(C-S)m^2`, and the intermediate first
step costs `4B=h(C-S)m^2`. The conditions `h/xi<1/2` and `m<m_c r_h`
belong to the separate interface/trial argument; they do not remove these
swap costs or provide Kawasaki rates.

For `C>S`, a passive zero-temperature Kawasaki rule cannot execute the first
uphill exchange from the alternating state. A controller or another explicit
energy source must induce it; the endpoint potential changes above are the
minimum ideal work for reversible state changes, before activation barriers,
finite-rate dissipation, or clamp overhead. The full cycle ledger below
includes all clamping and exchange-control work in `W_swap` (and its losses
in `D_swap`); these costs can be split out if desired. If `C<=S`, the sign
changes as the formula states, but that does not itself specify a physical
exchange mechanism.

## Network motion and energy accounting

After reaching `+++---` at `u=v=0`, take the prescribed path
`u_s=s w_star`, `v_s=0`, with
`w_star=h m[-1,0,1,1,0,-1]` and `0<=s<=1`. Its full energy is

```text
E(s) = 2 h C m^2 (1-s)^2
       + 4 h V0 [1-cos(beta h m s)] - 2J,
beta = 2 pi/d.
```

At `s=1`, the relative displacement increments match `h m_i`, the second
network strain is also at its target, and both elastic-square costs vanish.
The endpoint energy change for this move is
`Delta E_move=4 h V0[1-cos(beta h m)]-2 h C m^2`. Along this one-coordinate
path the generalized conservative force is `dE/ds`, bounded in magnitude by
`4h C m^2+4h V0 |beta h m|`. If the overdamped Rayleigh loss is
`Gamma_u h sum_i dot(u_i)^2`, then `sum_i (w_star_i)^2=4h^2m^2` and

```text
D_move = 4 Gamma_u h^3 m^2 integral(dot(s)^2 dt)
W_move = Delta E_move + D_move.
```

This is a work identity for the stipulated controlled path, not evidence
that local material forces, clamps, or a physical binary rearrangement have
been built. The selected path has zero mean displacement, but real clamps and
actuators still belong in the resource ledger.

From the original alternating ring (`E_initial=6J`) to the target endpoint,
the total stored-energy change is
`E(1)-E_initial=4hV0[1-cos(beta h m)]-2h S m^2`, equal to the sum of the
clamped swap change and `Delta E_move`. This is a useful sign/accounting
check; it need not be positive.

During the subsequent uncontrolled overdamped/zero-temperature stage, if
each accepted Kawasaki exchange is energy-nonincreasing, then
`Delta E_release=-D_release<=0`, where `D_release` includes mechanical
viscous loss and the energy surrendered by accepted swaps. The pattern need
not remain `+++---`; the trial state and an interface lower bound do not
select a kinetic endpoint.

For a true cycle returning every `sigma_i,u_i,v_i` and clamp state to its
initial value, write work into the system as `W` and all dissipated/exported
energy as `D>=0`. The closed ledger is exactly

```text
0 = Delta E_cycle = W_swap + W_move + W_reset -
                    (D_swap + D_move + D_release + D_reset).
```

Thus a complete cycle needs net input equal to total dissipation. Reversing
the exact swap path at `u=v=0` changes the stored energy by `-8B`; that energy
is recoverable only with an explicit regenerative controller, otherwise it
is dissipated. If release ends in a different binary pattern or displacement,
the reset work is `W_reset=E_initial-E_release+D_reset` and cannot be assigned
without the actual release endpoint and reset protocol.

## Material interpretation boundary

The sigma exchange is exact for an abstract neutral binary degree of freedom
with a physical nearest-neighbor pair-swap actuator. It is not automatically
a literal atomic operation. In a strictly one-dimensional occupied chain,
two atoms cannot pass through one another; exchanging their site labels
requires vacancy/interstitial motion, a bypass path, or some other explicit
transport mechanism. If the two species carry different charge/valence,
local exchange also needs a charge-compensation and electrochemical-work
ledger. For actual atoms, the vacancy/defect states, barriers, attempt rates,
charge compensation, and external clamp/reset work must be included before
calling the three swaps an acquired preparation. No finite-temperature
assembly or rate claim follows from the zero-temperature energy construction.
