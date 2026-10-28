# Independent reconstruction of the general force obstruction

**ACCEPTED at its stated mechanism scope.** Governing parent source:
`root_raw_image_query/FORCE_OBSTRUCTION.txt`. This is mathematical intake,
not an acquired physical load or a novelty determination.

Let the fluid domain be connected, smooth, bounded and planar, with finitely
many smooth boundary components. Assume single-valued w in C2, smooth to the
boundary, `div w=Delta w=0` and constant mu>0. The planar identity

    Delta w=grad div w+J grad curl w

implies `curl w=2alpha` is constant. In complex notation W=u+iv,
`partial_z W=(div w+i curl w)/2=i alpha`. Consequently

    W=i alpha z+overline(g(z)),

where g is a globally SINGLE-VALUED holomorphic function: it is explicitly
`g=overline(W-i alpha z)`. Multiply connectedness does not require a
single-valued stream function or harmonic potential, and does not spoil this
particular representation.

For the virtual constant-pressure stress
`sigma=2mu sym grad w-p I`, direct real differentiation gives

    (sigma11+p)+i sigma12=2mu overline(g'(z)).

The complex viscous traction is this coefficient times `overline(n)`.
For either normal orientation on a closed curve, `overline(n) ds` is
`+/- i d overline(z)`. Hence its total force is

    +/-2i mu overline(integral g'(z) dz)=0.

The integral vanishes because dg is exact, even for a loop surrounding holes.
A pole of g inside an excluded hole does not turn g' into a function with a
nonzero period. Constant pressure also has zero integrated force on every
closed component. Rotation/circulation need not vanish, and torque is not
claimed to vanish.

Suppose the outer trace is zero and every inner trace is a constant vector
U_j. The virtual stress is divergence-free. Its integration-by-parts identity
therefore reads

    2mu integral |sym grad w|^2
        = integral_boundary w dot sigma n
        = sum_j U_j dot F_j=0.

Thus w is a rigid motion on the connected domain. Its zero outer trace
forces that rigid motion to vanish. No nonzero pure translating inner-wall
trace is attainable in this harmonic/incompressible single-valued field
class for any of these geometries. The argument does not assert that all
rotational traces are attainable in all geometries.

This extends the annular Dirichlet obstruction using standard complex and
Stokes energy identities. It rules out this exact quadratic-query/blur/virtual
field mechanism for those translation traces. It does not rule out calibrated
blur corrections, other kernels, boundary measurements, general pressure/force
inference or another instrument. An abstract holomorphic tensor need not have
the globally single-valued virtual-field primitive used here; that larger
tensor class is not accidentally promoted to an attainable force load.
