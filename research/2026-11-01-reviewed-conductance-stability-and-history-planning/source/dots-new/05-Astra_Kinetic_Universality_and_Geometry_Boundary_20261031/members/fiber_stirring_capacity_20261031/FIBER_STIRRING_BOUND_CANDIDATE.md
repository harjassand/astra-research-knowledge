# What stationary angular stirring cannot change

Status: new ROOT candidate, UNREVIEWED. This is a conditional mathematical bound for static nonreversible diffusion, not a physical control implementation, general mixing-time claim, or historical-priority result. No existing reversible executable is promoted to a nonreversible receiver by this note.

## 1. Exact model and observable

Let mu be a smooth, normalizable Gibbs probability density for a conservative reversible isotropic diffusion with generator

  S=beta^(-1)Delta-grad F.grad,
  E(f,g)=beta^(-1) integral grad f.grad g dmu.

Use the full-fiber basins A={y<=-b}, B={y>=b}, with transition slab Omega=(-b,b) times R^m. Assume in the slab

  y partial_y F(y,z)<=0.

This is true for both the admitted homogeneous F=[1+kappa(1-y^2)^2]U(z), U>=0, and the stated monotone-Gaussian bottleneck families at b=1/2. Assume the reversible process's nonexplosion/invariant law have already been established for the ACTUAL potential.

Add an actual static smooth, bounded, compactly supported vector field c(y,z) satisfying

  c_y=0,     div(mu c)=0.

Define L=S+c.grad. The source of nonreversibility is explicit; no change of potential, diffusion tensor, target basins or physical coordinates is allowed. The amplitude of c may be any finite number. The task is standard nonreversible equilibrium capacity divided by mu(A), not a specified-initial-state first-passage time, angular equilibration, or mixing time.

The compact-support/boundedness condition is a sufficient receiving interface used to close the functional analysis below. Unbounded polynomial stirring needs additional domain/nonexplosion receiving and is NOT automatically included.

## 2. The committor is earned in the actual slab

Let T(y)=b^2-y^2 on Omega. Since c_y=0,

  L T=S T=-2/beta+2y partial_y F<=-2/beta.

Thus the actual process exits the slab almost surely, with mean exit time at most beta*b^2/2 from any point. This is not the rare passage time from a basin; entering this low-equilibrium-mass slab can be rare.

For a smooth compactly supported zero-boundary test f, the standard ground-state identity gives

  E(f,f)=beta^(-1) integral T^2 |grad(f/T)|^2 dmu
          + integral [-(S T)/T] f^2 dmu
        >=2/(beta*b^2) ||f||_(L2(mu))^2.

It extends to the zero-trace weighted H1 closure. Hence energy is a coercive norm on that space without assuming a fiber spectral gap.

The bilinear form

  a(f,g)=E(f,g)-integral(c.grad f)g dmu

is continuous in that energy norm because c is bounded and the preceding Poincare bound controls ||g||_2. Weighted divergence-freedom, c_y=0 at both planes, and compact transverse support make the drift form skew. Thus a(f,f)=E(f,f).

Choose any scalar admissible u0(y) with boundary0 on A,1 on B and finite energy. Lax–Milgram gives a unique h-u0 in the zero-trace space satisfying a(h,g)=0 for every zero-trace g. Testing truncations and using skewness gives0<=h<=1. Local elliptic regularity and the finite exit estimate identify h with the actual L-committor Pr(hit B before A). No committor oracle is used by the rate computation; this establishes the analysis object and its finite energy.

The same assumptions preserve mu as the invariant density. The reversible global Lyapunov bound survives a bounded compact drift with an additional finite compact-region term, so there is no explosion or hidden boundary flux. Ordinary bounded-drift diffusion theory then receives the stationary process.

## 3. A fixed subspace of trial functions supplies the upper bound

Every admissible scalar u(y) is annihilated by c.grad. Taking g=u-h in the weak equation and using skewness,

  E(h,u-h)=integral(c.grad h)(u-h)dmu=0.

The first term on the right is -integral h(c.grad u)dmu=0, and the second is zero by skewness. Therefore

  E(h,u)=E(h,h),
  E(u,u)=E(h,h)+E(u-h,u-h).                             (1)

For these elliptic full-fiber boundaries, the usual nonreversible capacity equals E(h,h); this also follows from Green's identity because c has no normal component at either basin boundary. It is the capacity of the ACTUAL L, not of the projected y process.

Let cap_0 be the reversible capacity. Its Dirichlet minimum is over all admissible functions, so cap_0<=E(h,h). On the other hand (1), or Cauchy–Schwarz, gives E(h,h)<=E(u,u). Minimize over scalar u to obtain

  cap_0(A,B) <= cap_c(A,B)
             <= [beta integral_-b^b 1/p(y)dy]^(-1).     (2)

Adding stationary circulation cannot reduce this capacity below the reversible value, and circulation that leaves y unchanged cannot exceed the free-energy variational upper bound. Neither statement says the capacity is monotone in every stirring parameter, nor that all other kinetic quantities improve.

This uses ordinary nonreversible potential theory. Landim–Mariani–Seo, https://arxiv.org/html/1701.00985 , Sections2–3, supplies general variational principles and the equilibrium-potential energy identity. Its displayed coercive-potential/bounded-basin assumptions do not directly cover our flat-valley, unbounded-fiber model. The slab coercivity and receiving argument above are therefore supplied explicitly, rather than importing that theorem outside its hypotheses.

## 4. Reuse of the received rare-conductance certificate

Suppose a received reversible calculation gives

  k_free/C <= cap_0(A,B)/mu(A) <= k_free,

where k_free is the scalar expression above divided by mu(A). Equation (2) gives the SAME interval for every admitted static c, independently of its amplitude:

  k_free/C <= cap_c(A,B)/mu(A) <= k_free.                 (3)

No new integration or sampling is needed once the actual c_y=0 and div(mu c)=0 interface has been checked. This is reuse of a mathematical certificate, not permission to omit model verification or a claim that physically implementing large c is free.

For the unit-parameter coupled-quartic family, the reviewed radial certificate has C=157/125. If the separate parallel-channel theorem and its consumer are received, its smaller C can replace this one. This note does not assume an unreviewed replacement factor.

Thus arbitrarily strong admitted stationary stirring, or any change of the static nonnegative quartic graph at the same m and unit-parameter lower coercivity class, cannot produce an arbitrarily large change in this particular full-fiber conductance. This is not a restriction on arbitrary algorithms, trajectory control, basin changes, angular targets, or time-dependent drives.

## 5. An explicit bounded stirring constructor

For the homogeneous model, let J be any constant antisymmetric m by m matrix, and choose smooth compactly supported scalar cutoffs psi(y) and chi(U). Set

  c_y=0,
  c_z=M psi(y) chi(U(z)) J grad U(z),

with any finite amplitude M. Coercivity of U makes the support in z compact. Antisymmetry gives grad U.J grad U=0 and Tr(J Hess U)=0, so

  c.grad F=0,   div c=0,   div(mu c)=0.

This verifies the ACTUAL added generator class. It can change angular dynamics and generate stationary circulation, while preserving the capacity bound. The cutoffs and J/amplitude are input controls that must be specified and checked; merely calling an arbitrary drift angular is insufficient.

A piecewise-polynomial C3 cutoff such as (1-y^2/Y^2)_+^4 and (1-U/R)_+^4, with positive Y,R, is a possible finite description. Its exact regularity, boundary receiving and full input representation should be checked before it is used in an executable constructor. This note does not already provide that parser.

## 6. Boundaries that matter

- If c has a y component, scalar u is no longer annihilated and the upper-bound proof fails.
- If c changes the invariant density or diffusion tensor, the same E and k_free cannot be reused.
- If targets select only part of a fiber, scalar u cannot satisfy their boundary values.
- If coefficients vary with time, a stationary capacity need not be the relevant quantity.
- Unbounded c without a proved form/domain interface is excluded here.
- No result concerns physical controller quality, energy expenditure, finite-deadline transition probabilities, or arbitrary-start mean waiting times.
