# Conductance without identifying the transverse relaxation matrix

Status: NEW conditional model-family corollary, not yet independently reviewed.
The existing isotropic source freezes and receiver schemas remain unchanged.
This is derived from the accepted parallel mechanism, NOT the radial current.

## 1. A precise universally quantified task

Fix a received potential F(y,z)=v(y)U(z), v=1+kappa(1-y^2)^2, in its acquired
physical Euclidean coordinates; the concrete consumer is the accepted coupled
quartic grammar with m>=2. Fix beta>0. Consider the FAMILY indexed by every
finite, constant symmetric positive-definite m by m matrix M:

  dy = -v'(y)U(z)dt + sqrt(2/beta)dW_y,
  dz = -v(y)M grad U(z)dt + sqrt(2M/beta)dW_z.

The Brownian parts have zero cross covariance. Longitudinal mobility is exactly1;
the same M occurs in transverse dissipative drift and noise, so fluctuation-
dissipation and reversibility are part of the interface. M is constant, not an
unknown function of y,z or time. M need not be diagonal, well-conditioned, bounded
above/below uniformly over the family, or numerically identified.

The requested output is one interval containing cap_mu,M(A,B)/mu(A) for EVERY
member of this family, with A={y<=-1/2}, B={y>=1/2} and full fibers. This is a
universally quantified mathematical family certificate. It does NOT assert that
a raw potential parser verified the kinetic structure of a particular physical
system. An application must independently justify the block-SPD/FDT interface;
this certificate intentionally does not learn the entries or relaxation rates.

## 2. Same invariant law and conservative global process, for each M

Each fixed M is SPD, so its diffusion is nondegenerate and has smooth local
polynomial coefficients. Constant symmetric block mobility gives reversible
Gibbs density proportional exp(-beta F); the finite normalization follows from
the already acquired homogeneous scaling and longitudinal tail. No M-dependent
partition function appears.

For a homogeneous degree p polynomial U>=0, take

  V_M=1+y^2+K z^T M^(-1)z,  K=1+kappa/p.

For each fixed SPD M this V_M is coercive, although its equivalence constants
with Euclidean norm may depend arbitrarily on M. Its generator is

  L_M V_M
    = -2[yv'+K p v]U + 2(1+K m)/beta.

Indeed the transverse drift pairing is -2K v z.grad U=-2K p vU, and the diffusion
trace is beta^(-1)Tr(M*2K M^(-1))=2Km/beta. Since yv'>=-kappa and v>=1,
yv'+Kpv>=p. Therefore L_M V_M<=2(1+Km)/beta. The stopped Lyapunov argument proves
nonexplosion for each M; finite Gibbs and symmetry yield the conservative
reversible process used below. The proof does not require the algorithm to
compute M^(-1): it exists for every member of the quantified SPD family.

This is existence/conservativity for each finite M, not a uniform equilibration
or arbitrary-start Lyapunov-time claim as its eigenvalues approach0 or infinity.
Exactly singular M is excluded from this stated process theorem.

## 3. Both full-capacity bounds discard all transverse kinetic information

The actual reversible Dirichlet energy is

  E_M(h)=beta^(-1) integral [h_y^2+(grad_z h)^T M grad_z h]dmu.

For the upper bound choose the same y-only trial function. Its transverse term
is zero, so cap_mu,M<=1/(beta Q R0), independently of M.

For the parallel lower bound, M>0 makes its transverse term nonnegative. Drop it,
then apply the accepted weighted one-dimensional Cauchy inequality separately at
each fixed z. This produces EXACTLY the same parallel lower integral, homogeneous
energy pushforward, Gamma/Jensen comparison and fixed-profile contraction as in
the accepted theorem. No transverse speed, current cost, angular gap or relaxation
estimate enters. Therefore for every M,

  1/(beta MA R_plus) <= cap_mu,M(A,B)/mu(A) <=1/(beta MA R0),
  R_plus=int_-b^b [a^2/(2a-v(y))]^(m/p)dy, a=1+kappa.

The weaker explicit factor is likewise uniform:

  k_free/sqrt((16+23kappa)/(14(1+kappa)))
    <= cap_mu,M(A,B)/mu(A) <= k_free.

The finite-Jensen scalar quantities are independent of M. Once this corollary
and a separately declared family receiver are received, the same computed scalar
interval can be valid for arbitrarily slow/fast/anisotropic transverse kinetics
without estimating those hidden rates. Potential acquisition, homogeneous degree,
coercivity/normalizability, beta, longitudinal profile and full-fiber basins are
still fully paid and essential.

## 4. Information access and receiving boundary

There are two different admissible uses; they must not be confused:

1. A universal family task supplies only the complete potential and explicitly
   asks for a bound for ALL fixed SPD M under the stated block/FDT interface.
   No particular matrix entries are required because the theorem quantifies over
   all of them. The current isotropic certificates have NOT yet been relabeled
   with this family scope; a new schema/receiver must bind it explicitly.
2. A specific known rational M can be acquired by reading every entry, checking
   symmetry and exact positive definiteness, then joining this theorem to that
   actual model. That extra input/verification cost is paid even though entries
   disappear from the scalar answer. This constructor is not yet implemented.

An unknown physical process cannot receive this result from F alone if its
kinetic interface is unverified. Neither a hidden mixing oracle nor a claim of
universal dynamics identification has been substituted for that missing premise.
The scientific consequence is conditional information reduction: for this
specified equilibrium observable, these particular kinetic parameters need not
be identified AFTER the structural model family has been justified.

## 5. Real exclusions

- Longitudinal mobility changes rescale or otherwise alter the scalar energy;
  the present rate/time units require its coefficient exactly1.
- Cross-mobility cannot simply be dropped. For example D=[[1,1],[1,1+epsilon]]
  is SPD for epsilon>0, but the gradient(1,-1) has energy epsilon, smaller than
  its longitudinal squared derivative1. Thus the critical discarded-energy
  inequality fails even with an SPD full matrix. No cross-mobility guarantee is
  inferred from this theorem.
- Variable M requires different drift/divergence and global-process arguments;
  it is not silently included even where a formal Dirichlet expression resembles
  this one. Singular matrices, nonreversible drifts, time-dependent controls and
  unverified fluctuation-dissipation are outside the stated family.
- Full-fiber equilibrium capacity is not arbitrary-start MFPT, angular mixing,
  a finite-time crossing CDF, or a guarantee that reservoirs equilibrate quickly.

The ingredients—reversible Dirichlet energy, positivity of its discarded term,
homogeneous scaling and a quadratic Lyapunov function—are ordinary mathematics.
The corollary is an explicit information-reduction consequence of the accepted
parallel certificate, not a priority claim or an earned physical application.
