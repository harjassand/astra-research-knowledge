# Control granularity can be exchanged for clock bandwidth

29 October 2026. Root's constructive continuation after the independent
action theorem and conserving common-clock counterexample. This gives
the stronger ordinary implementation rather than treating independent
ports as the only possible supplier. All previous source distinctions
and actual operation costs remain in force.

## 1. Actual grouped operation

Partition the N bonds into nonempty groups G_g of sizes n_g. There is
one orientation sigma_g in {-1,+1} per group. A supplied clock flips
all kinetic orientations in that group simultaneously at physical
rate gamma_g, leaving occupancies and frozen z unchanged. The group
clocks have independent fresh innovations. Native rates are

    r_i=(s/2)[1+beta_i(eta,z)sigma_(g(i))],
    |beta_i|<=1, beta_i(eta^i,z)=beta_i(eta,z).          (1)

This is an actual selective operation menu, not a decomposition of
one observed kernel into fictitious controls. Amplitudes can be
arbitrarily nonlocal, and native zero rates are permitted. The common
mean s is supplied/warranted as in the other constructions.

The full reference density/current action in
`CONTROLLED_MACROSCOPIC_ACTION.md` holds if

    r_N := max_g n_g/gamma_g ->0.                      (2)

The same fixed deterministic initial-profile sequence, physical horizon
N^2T, initial-record scope and actual-noise premises apply. Conditional
on an old record, the complete future native-and-clock generator must
remain the declared law; clock freshness alone is insufficient if the
record exposes future native innovations. Every initial joint
occupancy/orientation law is dominated by 2^(N+#groups) times its
uniform product reference, at most 4^N. No orientation key needs to
be forgotten or initially randomized.

## 2. Exponential phase cancellation

For a current test, write the unwanted drift as

    H_N=sum_g sigma_g v_g(eta,z),
    v_g=sum_(i in G_g) v_i, ||v_i||_infinity<=C.        (3)

The sign identity, weighted Cauchy--Schwarz and completion of squares
against N^2 sum_g gamma_g D_g give

    log E_mu exp[bN int_0^T H_Ndt]
        <=(b^2 T/2)sum_g ||v_g||_infinity^2/gamma_g
        <=(C^2 b^2 T/2)sum_g n_g^2/gamma_g
        <=(C^2 b^2 T/2)N r_N.                         (4)

The native reversible form is nonnegative and was discarded in this
estimate. No amplitude derivative or locality estimate is used.
Equation (2), Chernoff, and then b increasing give superexponential
replacement at speed N. The exp(O(N)) initial density factor is
harmless for that conclusion. Time grids give the integrated-residual
supremum version, as before. Quadratic-compensator sources have still
smaller coefficients. Weak-current likelihood L2 transfer is unchanged.

The averaged quantity N^-1 sum_g n_g^2/gamma_g tending to zero already
suffices for this phase estimate alone. The maximum condition (2)
also gives the uniform occupation-form control needed below. This
document does not silently replace (2) in the full theorem by only
the weaker averaged condition at zero native rates.

## 3. The same operation supplies missing exchange energy

For each bond repeat the proof in
`INDEPENDENT_CONTROL_OPENS_ZERO_RATE_GATES.md`, now flipping its whole
group. A group flip still commutes with native exchange. Summation
gives

    D_ex <=(4/s)D_native+4 sum_g n_g D_g.               (5)

It follows that

    D_native+sum_g gamma_g D_g
        >=min{s/4, min_g gamma_g/(4n_g)} D_ex.          (6)

Under (2), the coefficient is s/4 for all sufficiently large N.
Thus the classical occupation variational problem has the same
fixed positive exchange-form bound, including when some instantaneous
native gates have zero rate. The rest of the receiving action proof
uses only (4), this form bound, bounded native rates, the exact
continuity relation and the actual initial law. It therefore applies
without changing its action or adding an assumed physical weak tilt.

## 4. Explicit useful programs

For groups of size at most L_N and a common group-clock rate gamma_N,
the sufficient condition is gamma_N/L_N ->infinity.

| Actual architecture | Sufficient physical clock scaling |
|---|---|
| One independent clock per bond | gamma_N ->infinity |
| Groups of at most L_N bonds | gamma_N/L_N ->infinity |
| One common clock for all N bonds | gamma_N/N ->infinity |

The last row is a constructive common-control alternative for the
same arbitrary-context model, not just an obstruction. The conserving
parity construction proves that replacing its condition by merely
gamma_N->infinity cannot work uniformly: when gamma_N/N->0 it has
a strictly altered rare-current upper rate, and when alpha_N->1 its
nonzero circulation is superexponentially suppressed. The crossover
gamma_N of order N and necessity for every intermediate grouping or
particular kinetic model are not claimed here.

For finite-range amplitudes, the complementary deterministic gauge
construction can do better with a common rotation. That alternative
uses a locality/influence premise absent from this uniform nonlocal
family. The table is a sufficient worst-case program, not a universal
hardware lower bound.

## 5. Physical accounting and consequence

During physical time N^2T, expected group-clock events equal
N^2T sum_g gamma_g. The number of addressed bond flips equals
N^2T sum_g n_g gamma_g. These are different quantities. If all groups
have size L and gamma=L h_N with h_N->infinity, the former is
N^3T h_N while the latter is N^3T L h_N. A common bulk actuator may
have a different energetic cost from separate local drives; neither
count determines its work, bandwidth, communication or sensing cost
without an actual supplier.

At a fixed per-bond sign-flip rate, common and independent implementations
have identical individual sign-process laws, but different joint
correlations and potentially different macroscopic current actions.
Increasing shared-clock bandwidth can recover the uniform action.
Thus both the spatial correlation of the actual control and its
physical event rate belong in a rare-transport specification.

The useful scientific capability is prediction of a macroscopic
transport action without identifying the arbitrary hidden amplitudes,
using a stated operation granularity and rate. Ordinary controllers
with these same operations can implement it. This does not establish
that calibrating a device, using feedback, or directly simulating a
known model is inferior at any supplied practical cost.
