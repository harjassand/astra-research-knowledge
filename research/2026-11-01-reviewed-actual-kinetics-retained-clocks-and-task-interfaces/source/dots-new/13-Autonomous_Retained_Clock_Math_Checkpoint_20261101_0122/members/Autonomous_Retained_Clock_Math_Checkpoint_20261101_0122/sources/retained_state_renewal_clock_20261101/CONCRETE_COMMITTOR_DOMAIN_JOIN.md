# Concrete domain/local-time join for the new stationary count proof

This expands, without changing, Section 5 of the frozen global-odd candidate.
It addresses the premises in the independent **conditional** count receipt;
that receipt by itself does not receive this concrete model.

The already received global diffusion has smooth polynomial drift, a finite
constant positive-definite diffusion tensor, nonexplosion and finite invariant
probability pi. Local ellipticity gives positive transition densities on the
connected whole space (localization and the support/heat-kernel argument are
enough; global bounded drift is not required). Thus invariant events have
probability zero or one. The stationary process is ergodic, and the two-sided
ergodic theorem gives visits to the positive-mass A and B arbitrarily far in
the past and future. The Markov conditional law given X0 is the ordinary
future diffusion. Conditioning the two-sided stationary law on X0 in A
therefore gives exactly the declared once-only full Gibbs|A forward process,
and its retained initial label is certainly A. No surface entrance law is used.

## Dirichlet equilibrium potential without a boundary condition at infinity

Work in the closed weighted Sobolev Dirichlet form on finite pi, equivalently
unnormalized w. Minimize energy over functions equal to 0 on A and 1 on B.
The supplied scalar transition makes the class nonempty with finite energy.
Truncation to [0,1] preserves the boundary values and cannot increase energy.
A minimizing sequence so truncated has bounded L2 norm and energy. Weak
compactness in the Hilbert form domain, closure of the affine boundary-value
constraints (which hold on open basin interiors), and lower semicontinuity
give a minimizer q. Its energy is at most the scalar trial energy C0.

The minimizer is unique: the difference of two minimizers has zero gradient,
therefore is constant on the connected space, and its zero basin values force
that constant to vanish. Interior Euler--Lagrange equations make q harmonic
on S. Standard local elliptic regularity, including regularity at the two flat
smooth boundaries with constant Dirichlet values, gives a smooth representative
in S, continuous up to the boundaries, with local one-sided C1 normal traces.
The constant extension into the basins is consequently a locally piecewise
smooth continuous function. No assertion about uniform derivative bounds as
|z| tends to infinity is needed here.

For almost every starting point under pi, the first hit of A union B is finite
by stationary recurrence and disintegration. The bounded harmonic function
q stopped before that hit is a bounded local martingale after compact
localization. Nonexplosion removes compact exit localization on finite times;
bounded convergence removes the time stopping. Hence
q(x)=P_x(tau_B<tau_A) for pi-almost every x, which is sufficient for every
stationary/path-integrated assertion here. Local regularity gives the usual
pointwise version at regular interior starts as well. There is no unreceived
absorbing boundary at infinity and no substitution of an arbitrary solution
to the harmonic PDE.

## Boundary finite variation is earned locally before Fukushima shorthand

For this locally piecewise smooth q and a smooth uniformly locally elliptic
diffusion, generalized Itô--Tanaka under compact localization gives a continuous
local martingale plus conormal local-time terms on the two basin boundaries.
Their variations are finite on each compact localization interval; they are
continuous and supported on the respective boundaries. The carré du champ is
exactly beta^-1 grad q^T diag(1,M_z) grad q. Thus the decomposition used by the
count proof is genuine local finite variation, not the unjustified assertion
that every zero-energy Fukushima term has that property.

One can also earn the finite global charges explicitly. Locally, the minimum
principle gives positive outward charge at A and negative at B. Let chi_R be
smooth full-space cutoffs tending to 1, equal to 1 on radius R, with derivative
O(1/R). Finite w and finite constant mobility give E(chi_R)->0. Testing the
local distributional identity against chi_R q charges only B. The form
E(q,chi_R q) tends to E(q,q): its principal part converges by dominated
convergence, and its cutoff cross term is at most
sqrt(E(q)) sqrt(E(chi_R)) because |q|<=1. Nonnegative charge and increasing
cutoffs then give B-charge exactly cap. Testing against chi_R(1-q) gives
A-charge exactly cap. A monotone family of cutoffs can be selected; otherwise
the same conclusion follows by Fatou plus the obtained limits.

The subsequent count-square argument does not require a global bound on
normal derivatives. It localizes first, cancels boundary local times because
q equals the retained label on their support, and removes localization using
the finite stationary expectation of the martingale bracket and energy.
It earns E N before taking the stationary expectation of the final identity.
Only after this join may the conditional count/coupling receipt be applied.
