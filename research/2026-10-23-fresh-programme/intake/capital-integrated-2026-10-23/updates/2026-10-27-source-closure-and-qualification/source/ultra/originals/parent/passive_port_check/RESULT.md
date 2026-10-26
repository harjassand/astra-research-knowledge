# Independent source-model check and the internal-resource boundary

The shorted-coil construction in
`connection/passive_isolation_physical_bridge/SHORTED_COIL_H_MATRIX_PASSPORT.md`
passes this independent mathematical check at its stated source-model scope.
No physical passport or historical-priority claim is added.

Starting with the external carriage and internal proof-mass equations, eliminating
the latter gives exactly

    a = -omega² [m0 + mr h/(h-mr omega²)],
    h = k+i omega c+i omega g²/(R+i omega L).

The independent code does not import the producer implementation. It uses exact
Sturm root exclusion on the rational frequency enclosure instead of Bernstein
coefficients. The degree10 dominance and degree9 loss polynomials have no roots
in the enclosure and are positive at its left endpoint. This verifies the
278000 N/m modulus margin and157000 N/m imaginary-part floor. The paid30000
N/m **unacquired** local-error gate gives exactly
650301001/81127045001 for the stipulated two fixed connectors. The all-rigid-
mass-allocation witness was separately derived from the two physical node
equations and agrees exactly with the producer's squared lower bound.

These two-cell statements specialize the portable connection family to the
actual two25000 N/m +25 Ns/m connectors. They do not assert that any connection
weights satisfying only a50000 N/m incident sum give the same two-cell number.

There is also a positive internal-cost result for the **nominal** source model:
an exact band proof gives |r-q|/|q|<5 for its internal mass. Direct4DOF solutions
at31,31.5,32 Hz independently satisfy mechanical dissipation plus coil Joule
heat = the condensed port's loss. At1 mm base amplitude, the32 Hz diagnostic
has0.3398 mm first-cell relative stroke,0.3440 A peak short-circuit current,
0.1112 W first-cell mean internal dissipation and26.65 N peak network base
reaction. These are three model diagnostics, not continuous-band ratings or
measured hardware performance. An arbitrary external residual does not acquire
the nominal internal-motion law.

The subsequent `RECIPROCAL_LOSS_QUALIFICATION.md` was also read completely.
The power inequality, same-operating-loop reciprocal measurement and dissipative
finite-fixture bound are correct under their stated port assumptions. The code
here independently verifies the exact nominal identity

    Im a = omega R |I/v|² + omega c |(r-q)/q|².

The producer's uncertain-node rational interpolation includes visible-tail
contamination of the measured samples and the final lower gain envelope. Its
three/four-cell cost uses the weaker loss-only margin. This is a completed
internal mathematical check of that reduced operation, not physical acquisition.
Finite magnitudes need the declared core/tail/settling and metrological promises;
no such complete laboratory envelope was acquired in this programme.

## A small port residual need not bound hidden internal motion

Fix a band with0<omega<=W and select omega0 inside it. Redistribute mass mu from
the carriage into a passive parallel oscillator with spring mu omega0² and
damper mu gamma, gamma>0. The total static mass is unchanged. Its net change to
the carriage dynamic stiffness is

    Delta a = -mu omega⁴/(omega0²-omega²+i gamma omega).

Choose mu=epsilon gamma/W³. Since the denominator's magnitude is at least
gamma omega, |Delta a|<=epsilon throughout the band. Nevertheless its relative
internal harmonic displacement at omega0 is omega0/gamma times the port
displacement. Its mean kinetic energy for a fixed harmonic port amplitude grows
as1/gamma. Every member is a finite, passive linear construction. The saved
numerical family illustrates the exact formula; it is not an inferred hidden
defect of the published device.

The increasingly high steady response also takes increasingly long to establish:
the settling scale is1/gamma. This is not unbounded energy or damage in a fixed
finite experiment. It establishes that small external band discrepancy, static
mass and passivity alone do not provide a universal internal steady-state stroke
or stored-energy rating. A separately justified amplitude/time/thermal contract
is needed if the portable operation promises durable physical use. The external
small-signal attenuation certificate can remain valid without identifying every
hidden coordinate. The distinction preserves its useful scope.

Executed artifacts: `check.py` and `results.json` in this directory. Mathematical
correctness checked here does not establish acquisition cost, novelty, full
mechanical-port qualification or practical advantage over robust substructuring
and tuned passive isolators.
