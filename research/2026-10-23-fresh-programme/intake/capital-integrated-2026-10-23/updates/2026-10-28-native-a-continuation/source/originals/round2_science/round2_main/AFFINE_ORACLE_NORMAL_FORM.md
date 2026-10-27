# Constructed Gaussian reserves and compatible center responses

27 October 2026. A representation theorem for finite affine value-query
programs, not an assumption about arbitrary current laws or rejection samplers.

Let external x be in R^d and let Z have s standard Gaussian d-vector slots.
A fixed program makes physical queries

    q_i=u_i+b_i x+sum_{j<i}a_ij g(q_j)+sum_k B_ik Z_k,

and returns a p-slot output

    Y=c x+v+sum_j f_j g(q_j)+D Z.

All displayed coefficients are known and independent of x,Z and source
values. Known scalar Gaussian transformations and affine composition preserve
this class; source-dependent branches and nonlinear coefficients need not.
All program and coefficient-acquisition costs remain charged.

Write B^dagger for the Moore--Penrose inverse and P=B^dagger B. Suppose
b is in range B. Define

    U=b x+B Z,    a=c-D B^dagger b,    R=D(I-P)D^T.

Induction over the queries shows that every q_i and returned source value is a
function of U. Orthogonal Gaussian decomposition therefore gives the EXACT
representation

    Y=a x+Psi(U)+D(I-P)Z,
    Psi(U)=v+D B^dagger U+sum_j f_j g(q_j(U)).           (1)

The last term is N(0,R tensor I_d), independent of U. Its covariance is
constructed from code by finite known linear algebra. It is the largest
reserve obtained by removing a linear seed subspace preserving every
physical query. Source-specific additional cancellations are not excluded.

The minimum-norm query-preserving center gauge is v0=-B^dagger b. For all
x,Z,Delta, the change (x,Z)->(x+Delta,Z+v0 tensor Delta) leaves all queries
unchanged and changes Y by the KNOWN affine response a Delta. Thus

    Y0(x,Z)=Y(x,Z)-a x

has a zero-output center gauge v0 and the same exact reserve. If R>0, set

    W=(I-P)D^T R^{-1}.

Then BW=0, DW=I, W^T W=R^{-1}, and v0^T W=0. Shifting seeds by W tensor h
leaves every source query unchanged and shifts the output by h. Both the
reserve and the compatible response have been constructed, with no source
mean, derivative, fitted field, or conditional-distribution operation.

For the original, unmodified output, a zero-output center gauge orthogonal
to this reserve exists exactly when a=0. If a is nonzero, the general gauge
v0-Wa spends a reserve component. Requiring orthogonality without checking
this condition would be a false closure claim.

## Hidden-center use

If Q(t) approximates N(m(t),S^2 I) uniformly, Q(t)-a t approximates
N(m(t)-a t,S^2 I) with unchanged error, queries, and noise. At the hidden
affine center t=b_i+sum_j A_ij m_j, compile this residual child first. The
original mean is the known affine combination

    [m(t)-a t]+a b_i+sum_j a A_ij m_j.

Use the retained old Gaussian record for the latter terms, propagating its
complete covariance and correlations. Linear postprocessing preserves TV
and any PROVED reserve inequality R>=rho C. No noisy term may be discarded.
Subtracting a t may worsen center Lipschitz bounds, and the final variance
may exceed its budget; neither cost is automatically small.

## Alternate orthogonality repair, without changing the target

For any one-center gauge V and output response W, append one unused Gaussian
slot. If V is nonzero, take

    V_aug=(V,||V||),
    W_aug=(W,-V^T W/||V||).

They have the same pathwise effects on all queries and outputs, and are
orthogonal. Their costs are explicit:

    ||V_aug||^2=2||V||^2,
    W_aug^T W_aug<=2 W^T W.

For V=0 no augmentation is needed. A reserve lower-bound fraction can
therefore lose a factor two per such nested repair; this factor is not free.
The companion round2_reuse proof constructs reserve/response propagation
through joint absorption. This simple repair closes its orthogonality
metadata condition at a paid cost.

## Costs and scope

Construct B,D,b,c by symbolic scalar-affine propagation through the known
program, with no g evaluations. Gaussian elimination on a full-rank basis
constructs the projections and inverses in polynomial arithmetic in the
number of queries, seed slots and output slots. Exact rational metadata
permits exact rational certificates. Finite precision needs rank and
conditioning margins and its own output perturbation budget.

The construction supplies a usable representation. It does not prove that
the complete original N687 recursion has polylogarithmic queries, favorable
precision, or a uniformly large reserve. Those quantitative obligations
remain and are stated in the main continuation report.
