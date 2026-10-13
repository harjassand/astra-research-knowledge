# A parity-free proof of the bare-current floor

13 October 2026. Internal reconstruction of standard accretive-resolvent
linear algebra, applied to the spectral intake. No historical novelty or
physical implementation is asserted. This strengthens theorem A's stated scope,
not theorem B's staggered finite-hopping competitive ratio.

On the real Hilbert space of Hermitian observables let S be self-adjoint
nonnegative, A skew-adjoint, J Hermitian and S_lambda=S+lambda I for lambda>0.
For B_lambda=S_lambda+A,

    sym(B_lambda^-1)
      =B_lambda^-* S_lambda B_lambda^-1
      =[S_lambda+A* S_lambda^-1 A]^-1.

The first equality follows by multiplying B_lambda+B_lambda*=2S_lambda;
the second follows by inversion and cancellation of cross terms. Consequently

    <J,B_lambda^-1 J>
      =sup_f {2<J,f>-<f,S_lambda f>
                         -<A f,S_lambda^-1 A f>}.

No odd/even decomposition or real matrix entries of the Hamiltonian are needed.
The inner product is real on the Hermitian-observable space.

Suppose H=D+epsilon T, A=-i[H,.], D diagonal, and a Hermitian bare current J0
obeys [T,J0]=0. Then A J0=-i[D,J0] has no population component. If S is a
positive-width diagonal Schur dephaser on all off-diagonal observables, the
lambda-down-to-zero limit of the trial f=epsilon a J0 is well defined. Scalar
optimization gives

    kappa_Q >= epsilon^2 <J0,J0>^2 /
           [<J0,SJ0>+<A_D J0,S^+ A_D J0>].

This is precisely the spectral report's theorem-A bound. Its usual connected
finite-sector assumptions still justify the trace-zero pseudoinverse/current
definition. This proof supplies no thermodynamic limit or transient settling
bound.

For a periodic homogeneous hard-core ring with a uniform Peierls phase theta
per bond, take

    T=-t sum_i [e^(i theta) s_(i+1)^+ s_i^-
                            +e^(-i theta) s_i^+ s_(i+1)^-],
    J0=i t sum_i [e^(i theta) s_(i+1)^+ s_i^-
                            -e^(-i theta) s_i^+ s_(i+1)^-].

In every fixed-particle sector the Jordan–Wigner one-particle matrices are the
symmetric and antisymmetric parts of the same twisted cyclic shift. Therefore
[T,J0]=0 and the hopping-current norm remains
`m0=2t^2 K(n-K)/[n(n-1)]` for n>=4. The source's common-D symmetric phase-noise
resistance bound therefore yields the same absolute floor with this flux:

    kappa_Q,M >= .97 epsilon^2 t^2 K(n-K)/[W n(n-1)],

and the finite pulse variant inserts (1-delta). Each hopping detuning still has
to be acquired/bounded by W>=eta. Arbitrary graph geometry, nonuniform hopping,
generic observables and uncharged coherent pulse errors are not covered.

The spectral report's narrower exclusion of complex flux was appropriately
conservative; it is not a source error. This alternate proof removes that
particular exclusion for the absolute-current theorem. It does not establish
the staggered competitor ratio in a flux sector or an engineering benefit over
allowed coherent cancellation/uniform-dephasing controls.
