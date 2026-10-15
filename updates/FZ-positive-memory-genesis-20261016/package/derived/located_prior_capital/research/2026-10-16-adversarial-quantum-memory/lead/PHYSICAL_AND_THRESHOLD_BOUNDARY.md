# Physical resources and threshold limits

16 October 2026. These are consequences and limitations of the mathematical
model, rather than acquired hardware properties or a historical priority claim.

## What the theorem supplies

The supplied architecture uses 6L^4 plaquette qubits and stores six logical
qubits. There are 14L^4 syndrome-conditioned correction terms, each supported
on at most 24 data qubits and writing at most two. Its graph range and rates
are constant with L. There is no extra implemented controller, block grid,
or physical global clock. Arbitrary logical inputs are already exactly encoded.
Final syndrome extraction and the fixed mathematical recovery are perfect.

The promised exponential is in linear dimension L. With n=6L^4 physical
qubits it is exp(O(n^(1/4))), not exp(O(n)). The code distance L^2 is a separate
quantity and does not change the proved lifetime exponent.

## What can currently be said about the threshold

The proof constructs a strictly positive rate threshold implicitly:

    epsilon = delta_* / [18 C b ((2R+5)b+3)^4],

where C=10 log(8)+2, R>=ceil(280 e C)+10, p_* is below HT's tolerance for
the chosen map and connectivity, delta_* is an LSS tolerance for the fixed
dependence radius, and fixed b suppresses both clock-tail terms. No useful
number is supplied for p_*, delta_* or b. Reporting a simulated crossing or
choosing favorable values for those constants would not extract this bound.

The displayed conservative recipe already takes R=17360, connectivity k=69444
and a sufficient coarse size margin M>=88897536. Even at the merely necessary
b>=4 used in that recipe, L=355590144 would correspond to approximately
9.59*10^34 data qubits. Actual sufficient b is not calculated and could be much
larger. These are loose sufficient proof margins, NOT lower bounds on useful
devices, the actual threshold, or optimal finite-size performance. They show
that the present proof is qualitative and cannot support engineering estimates.
Arithmetic and its exact scope are saved in THRESHOLD_AND_GEOMETRY.json.

A meaningful quantitative continuation must replace the giant forcing sets
and abstract domination tolerances by explicit local contour constants or
another verified finite-size bound. It must preserve continual faults and
all-time-in-slab coverage. Simulations could test a specified finite device
afterwards, without substituting for the universal estimate.

## A direct embedding cannot keep all 3D resources fixed

Assume injective placement in physical three-dimensional space at bounded
density rho, fixed cell dimension, and that every required edge of the supplied
4D interaction graph is realized with Euclidean length at most ell. A graph
ball of radius r<=const*L has at least c*r^4 cells. Its physical images lie
inside a Euclidean ball of radius r*ell. Bounded density gives

    c*r^4 <= C*rho*(1+r*ell)^3.

At r=Theta(L), this requires ell=Omega(rho^(-1/3)*L^(1/3)). Thus an unbounded
family of this directly embedded graph cannot simultaneously retain bounded
3D density, fixed local dimension and constant physical interaction length.
This elementary volume-growth deduction is not a new no-go theorem for
quantum memory. Synthetic dimensions, nonlocal couplers, mediated reservoirs
or growing internal dimension change the interface and need their own costs.

## Interfaces still needed for a physical memory

| Interface | Supplied by the mathematical theorem | Acquired physical evidence |
| --- | --- | --- |
| Geometry | Ideal 4D bounded-range interaction graph | None in this campaign |
| Local correction | Exact stabilizer-conditioned 24-qubit jump support | No reservoir construction or calibration |
| Preparation | Arbitrary code-space logical/reference state | No preparation-error threshold or measured fidelity |
| Continual noise | Specified local Pauli proposal class | No measured device noise spectrum or leakage model |
| Dissipation and reset | Constant abstract jump rates | Energy, entropy removal, reset and bath costs unknown |
| Readout | Perfect syndrome extraction and deterministic recovery | No noisy-readout threshold or latency study |

The restricted Pauli perturbation corollary supplies robustness to some
stochastic control errors under the named imports. The separate completed and
depolarization-regularized construction also has a fixed local-generator
tolerance for coherent Hamiltonian drift and general dissipative errors,
as reconstructed in REGULARIZED_ROBUST_MEMORY.md and separately audited in
trajectory/CPTP_REGULARIZATION_AUDIT.md. Its floor and dephasing terms are
additional real model resources, with possibly larger bounded support and a
very small tolerance. A universal radius-one cell patch has 486 qubits, so
its Choi bound contributes the factor 2^(-972); smaller specified patch types
give a less severe fixed dimension factor. Robustness of the original generator, leakage, noisy
preparation/readout and an acquired physical implementation remain unresolved.
Strong ideal mathematics and remote hardware feasibility are compatible
assessments.
