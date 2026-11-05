# Finite complete-map verification with actual entangling branches

The companion executable `verify_complete_map_palette.py` verifies the central
channel-valued mixture and overlapping-call mechanism in a small independent
example. It uses NumPy and SciPy. This is a mathematical consistency test, not
a hardware experiment or certification of the full all-family threshold.

## Explicit menu and noise

On a two-qubit input/output cell, normalized Choi dimension is 16. Let
J_0=I_16/16. The ideal menu contains J_0 and the 480 maps

    J_(a,b,+/-) = (I_16 +/- .9 P_a tensor P_b)/16,
    a=1,...,15, b=0,...,15,

where P_0=I and the P_a are two-qubit Pauli matrices. These maps are CPTP:
their minimum Choi eigenvalue is .1/16 and the nonidentity output Pauli makes
their output partial trace perturbation zero. Add the unitary CZ channel as
a final ideal menu entry, giving 482 maps.

For every intended menu entry J, its actual complete map is

    J_actual = .97 F[ .92 J + .08 (CZ tensor I) J (CZ tensor I)† ]
               + .03 J_0,

where F is product output depolarization with parameter .01 on each qubit.
Thus the raw selector has a nonzero error probability: on its fault event it
invokes a fixed completely depolarizing fallback. A fresh correlated CZ
fault can couple the cell's two qubits; terminal local noise is also included.
This is a fully specified toy complete-channel model. It is not inferred
from the inherited homogeneous single-wire Pauli model without an additional
physical construction.

## What is solved

An ordinary finite LP finds positive weights for two target maps:

* Inactive product channel D_.9 tensor D_.9.
* Replacement by sigma=(I+.08 XX+.06 ZI)/4.

Both LPs explicitly require a positive weight of at least .002 on the actual
CZ menu branch. Thus the entangling branch is actually used, not merely
present as an unused option. The solved weights on it are approximately
.00860194 and .04637374 respectively. The actual CZ branch acting on |++>
has partial-transpose negativity .40718347.

The test then applies the replacement map on AB and the inactive map on BC.
It starts from the maximally entangled state between three data qubits ABC
and a full three-qubit reference. This is the normalized Choi test of the
entire overlapping three-qubit process, not a test on one uncorrelated input.
Complete-map equality guarantees the same conclusion for arbitrary inputs
and arbitrary reference dimensions; numerical Choi error gives a finite
dimension-dependent diamond bound for this test instance.

## Executed results

The actual menu's minimum normalized-Choi eigenvalue was .0018810625, and
its maximum trace-preservation residual was 1.12e-16. The inactive and
replacement mixture Choi trace errors were 1.78e-16 and 2.09e-16. The full
overlap/reference Choi trace error was 7.26e-16, giving the conservative
three-qubit diamond-distance upper bound 5.81e-15. Numerical comparisons
are floating-point checks, while the general convex/scheduling theorem has
its separate mathematical proof.

The inactive parameter .9 was deliberately chosen well inside the CPTP
body so this small menu suffices. It is not the small inactive noise required
by the general mixed-block preparation, and these results do not imply an
8% native component threshold for that operation. They verify the mechanism
that an average of actual entangling and imperfectly selected branches can
equal a product inactive channel and compose correctly on overlapping
intervals with a full reference retained.
