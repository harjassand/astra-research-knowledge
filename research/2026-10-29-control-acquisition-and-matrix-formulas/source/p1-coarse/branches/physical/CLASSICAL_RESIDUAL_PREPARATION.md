# Classical residual preparation: what one port can and cannot supply

28 October 2026. Physical-interface assessment and ordinary proofs. No hardware
operation is proposed or performed.

## Finding

For one time-invariant mode, a polynomial residual can be prepared exactly by
Horner injections if calibrated signed additions of the preparation vector are
available during evolution. This is a concrete classical construction with
cost proportional to polynomial degree. It does not require identifying the
hidden state.

The current reset-and-read port does not imply those additions, a total-energy
measurement, or an efficient finite-time energy dump. For noncommuting
dictionaries, one accumulator generally cannot combine separate histories;
parallel copies and physically aligned state mixing would add substantial
access. Even a positive energy measurement does not improve precision scaling
when its noise has a fixed additive floor.

## 1. Single-mode Horner preparation

Assume one actual contraction A and a control operation x -> x+u b for any
specified signed scalar u, without resetting the current x. Let

    p(z)=c_0+c_1 z+...+c_d z^d.

Start from x=c_d b. For j=d-1,...,0, perform x <- A x+c_j b.
Induction gives the final state x=p(A)b. The operation requires d applications
of A and d+1 calibrated injections. There is no inverse A, state measurement,
or finite hidden-dimension assumption.

For the Krylov dictionary V=[b,Ab,...,A^(r-1)b], the residual

    A Vx - VTx = p(A)b

has degree at most r. Its coefficients are obtained by shifting the entries
of x by one power and subtracting the entries of Tx. Thus Horner prepares the
actual residual, rather than subtracting two measured energy estimates.

This is ordinary linear-system superposition/input shaping, not a new
principle. The useful question is whether the source already supplies the
required injection control. A repeatable pulse allowed only after reset does
not. In an electrical RC network, adding calibrated signed charge at the
matched port is a valid linear input operation; it requires a source that
implements that input on the occupied circuit. In a heat network, negative
temperature increments require cooling relative to the working equilibrium;
a heater alone does not supply both signs.

### Preparation errors and range

If each actual injection differs by a vector e_j with ||e_j||<=eta_j, true
contraction gives final error at most sum_j eta_j. If the pulse coefficient
errors are delta_j with the same profile b, this is at most
||b|| sum_j |delta_j|. Dynamic implementation errors also propagate through
the intermediate states and must be budgeted; no source precision is acquired
by the algebra.

Intermediate norms are bounded by ||b|| sum_j |c_j|, so coefficient growth
sets a dynamic-range and linearity requirement even when the final residual
is tiny. The paid operation includes dwell time, pulse duration and energy,
reset, input calibration, linear-range checks and eventual readout.

## 2. Why arbitrary noncommuting dictionaries need more control

With one accumulator, zero initial state, a selected chronological control
sequence i_1,...,i_N, and injections u_t b between operations, the final state
is exactly

    x_N = sum_(t=0)^N u_t A_(i_N)...A_(i_(t+1)) b.

Every generated dictionary word is a suffix of the SAME chronological master
sequence. The empty suffix is the final injection. The formula follows by
iterating x_t=A_(i_t)x_(t-1)+u_t b.

Consequently this operation set directly realizes a suffix chain, not an
arbitrary branching noncommutative polynomial. In the free-word representation,
even A_1 b+A_2 b cannot be assembled by a single fixed control/injection program:
there is only one suffix of length one. Longer suffixes do not supply the
missing distinct degree-one monomial. Special source identities or a learned
finite-state controllability model may change reachability, but those are
additional premises and computations, not consequences of superposition.

Thus a scalar Krylov residual has a valid Horner implementation; a generic
switched-word residual does not inherit it. One could restrict dictionaries
and coefficient maps to physically preparable chains, paying any loss in
approximation quality. General branching needs stored intermediate states,
multiple source copies, a state adder, or some other explicit operation.

## 3. Paired copies and state mixing are a conditional classical route

Suppose two physically matched electrical networks have the same capacity
matrix C, corresponding state coordinates, and separately prepared voltages
u,v. Suppose their internal dynamics can be held fixed while corresponding
nodes are connected through a known positive conductance matrix G. The
equalization equations are

    C xdot = -G(x-y),       C ydot = G(x-y).

The mean remains (u+v)/2; the difference decays. If all difference modes
decay, the total electrical energy dissipated in the coupling is exactly

    [||u||_C^2+||v||_C^2]/2 - ||(u+v)/2||_C^2
      = ||u-v||_C^2/4.

This is a direct positive mismatch-energy operation. A specified finite-time
tail bound and a meter collecting all coupling dissipation would make it
operational. It does not require subtracting two large measured energies.

But a matched scalar port does not give coordinate-by-coordinate pairing,
matched hidden capacities, global coupling, storage or isolation of internal
losses. Manufacturing two nominally identical sources does not certify their
hidden dynamics agree to the desired residual tolerance. Preparation and
copy mismatch would themselves contribute to the measured difference.

More than two word histories can be prepared on separate copies and combined
by a known state mixer. Equal-capacity charge sharing implements their
average, with a known normalization; signed initial injections can supply
negative coefficients. This requires the same global coordinate alignment.
Moreover mixing dissipation generally measures disagreement among the
branches, not the small norm of their signed sum. A final total-energy readout
or an appropriately prepared pair of branch sums is still needed.

## 4. Energy is an extra observable; a finite dump must be certified

For electrical capacitor voltages, stored energy is exactly

    H(x)=x* C x/2.

If a dump evolution C xdot=-L_dump x has L_dump>=kappa C with known kappa>0,
then H(T)<=exp(-2 kappa T)H(0). A meter collecting ALL dissipated energy sees
D(T)=H(0)-H(T), giving the valid finite-time upper bound

    H(0) <= D(T)/(1-exp(-2 kappa T)).

Without a known decay or completion bound, the observed finite-time
dissipation is only a LOWER bound on stored energy. An arbitrarily slow mode
can hide energy beyond the integration window. If only a port load is metered
while internal resistors also dissipate, the port energy is not total loss.
One-port output integration instead gives an observability-weighted norm;
turning it into the C-norm requires an appropriate lower observability bound.
No such bound follows merely from passivity or collocation.

The thermal case needs additional care. For heat capacities C_j and
temperatures T_0+theta_j, ordinary excess heat is sum_j C_j theta_j, whereas
the linear heat equation's quadratic Lyapunov quantity is
sum_j C_j theta_j^2/2. Near equilibrium, thermodynamic availability is

    Delta U - T_0 Delta S
      = sum_j C_j[theta_j-T_0 log(1+theta_j/T_0)]
      = sum_j C_j theta_j^2/(2T_0)+O(theta^3).

Thus calorimetry of net heat does not automatically measure the Hilbert norm.
For two bodies equalizing internally, heat energy is conserved while entropy
increases. A temperature-square/availability measurement is an additional
observable or thermodynamic operation, not ordinary total-heat collection.

## 5. A positive energy does not imply vanishing measurement noise

Let the actual residual state be r+e with ||e||<=zeta. Suppose an energy meter
gives a valid upper bound H_upper for ||r+e||^2/2. Then

    ||r|| <= sqrt(2 H_upper)+zeta.

This is a sound certificate. To resolve norm epsilon, the energy uncertainty
must be of order (epsilon-zeta)^2. If each energy reading has fixed additive
noise standard deviation sigma_E, averaging n independent readings gives
energy precision of order sigma_E/sqrt(n), hence n of order
sigma_E^2/epsilon^4, with the appropriate confidence factor. A deterministic
energy calibration floor sets an irreducible norm floor. Background
subtraction can also reintroduce signed cancellation.

An ideal count-like detector whose variance vanishes with residual energy can
have the more favorable epsilon^-2 behavior. This is a different instrument
noise contract, not a consequence of positivity. Classical electrical
conductors at nonzero temperature have thermal fluctuations; an equilibrium
capacitor's equipartition scale is <v^2>=k_B T/C in the classical regime.
This identifies a physically relevant background to analyze, not an asserted
universal lower bound for every possible cooled or driven detector.

The Horner construction therefore removes one algebraic subtraction but does
not, by itself, remove the metrological limitation. Any claimed advantage
must include signed-source precision, dynamic range, total-energy access,
integration completion, thermal/readout noise and repeated preparation cost.

## Primary physical context

- Eberard, Maschke and van der Schaft, *Energy-conserving formulation of
  RLC-circuits with linear resistors* (2006),
  [author-hosted paper](https://www.math.rug.nl/~arjan/DownloadPublicaties/EberardMTNS06.pdf).
  Uses capacitor charge and inductor flux as energy variables and models
  electrical stored energy and resistor dissipation. The elementary identities
  used above are proved explicitly for the required linear special case.
- Nyquist, *Thermal Agitation of Electric Charge in Conductors*, Physical
  Review 32, 110 (1928),
  [DOI](https://doi.org/10.1103/PhysRev.32.110),
  [primary paper scan](https://123.physics.ucdavis.edu/johnson_files/nyquist_1928.pdf).
  Establishes thermal voltage fluctuations and their resistance/temperature
  dependence; it is the cited background, not a claim that every residual
  meter has the same noise spectrum.
