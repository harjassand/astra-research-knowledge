# Finite positive singleton compression for anisotropic rotation kernels

29 October 2026. Root construction, independent review PENDING. This changes
the specified kinetic kernel; it is not a silent claim for every Boltzmann
cross section, spatial transport, or an acquired physical gas.

## 1. Supplied elastic rotation law

Let rho be sampleable on real3x3 rotations, with computable SECOND matrix
moments. An explicit class is rho=eta Haar+(1-eta)rho_fin, eta>0 known,
rho_fin a finite rotation/probability list. Collide independent V1,V2 by
A V1+B V2, A=(I+R)/2,B=(I-R)/2,R~rho. Its partner is B V1+A V2. The pair
conserves velocity sum and kinetic energy for every R: relative velocity
is rotated by R. This is a specified homogeneous elastic quadratic process,
not an assertion that all physical angular kernels have this representation.

The complex norm-weight/binomial moment hierarchy of root_complex_collision
persists BEFORE angular integration. Under the Haar component, Jensen gives
>=1/3 separating probability for q>=2; other components contribute >=0.
Every raw iteration ends or splits with probability >=eta/3, uniformly over
complex direction. Thus expected attempts <=3/eta per nonsingleton block,
and O(q/eta) overall, apart from the singleton operation paid next.

## 2. Singleton as a finite unital completely positive map

The common-input one-collision covariance map is

    Phi(M)=E_R[A M A^T+B M B^T]=(M+E_R R M R^T)/2.

It is real, unital, completely positive and trace preserving. The singleton
evolution Psi_t=exp[t(Phi-I)] is again real unital CPTP, by its Poisson
mixture of powers of Phi. Compute it as the exponential of a supplied9x9
real superoperator, not a t-length random rotation history. Its Choi matrix
is real positive9x9; real spectral factorization supplies <=9 Kraus matrices:

    Psi_t(M)=sum_j K_j M K_j^T, sum_j K_j K_j^T=I.

For complex Hermitian-unit z, p_j=||K_j^Tz||^2 are nonnegative and sum1.
Draw j, set z_j=K_j^Tz/sqrt(p_j), and call the bounded initial degree1
terminal routine at z_j. The result has modulus<=1 and mean
sum_j p_j F_1^0(z_j)=z^T Psi_t(M_0)z. No initial covariance oracle is needed.
The observable uses TRANSPOSE; only probabilities use Hermitian norms.

This exact ideal operation has fixed matrix dimensions independent of t.
Matrix-exponential/factorization precision and time-input bits are costs.
A floating Choi factorization is a diagnostic, not finite-bit certified
Kraus synthesis. Positivity follows from the CP identity, not eigenvalue
clipping. The operation compresses one expectation, not a whole angular path.

## 3. Full-law consequences and limits

Use this q1 rule, and sample rho at q>=2, in the direct complex dual. The
same binomial/Duhamel proof gives bounded unbiased moments, <=q initial
terminal queries, and O(q/eta) expected collision draws. Covariance intervals
remain invariant. Thus its bounded density-ratio query, exact b<2a ideal
factory receiver, and arbitrary-contrast positive approximate receiver
apply to this ANISOTROPIC rotation-law process.

Gaussian-normalized actual velocity moments give the same hierarchy for
centrally symmetric initial data with a bounded complex terminal routine at
scale kappa. The declared resolved law mu_t*G_s, s>kappa, therefore has the
same ideal exact receiver. Gaussian convolution commutes with the gain
because AA^T+BB^T=I. Energy and mean zero pay its Jensen lower envelope.

Ordinary machinery includes finite CP/Kraus factorization, matrix exponentials,
marked branching, contour queries and a credited Bernoulli factory. The
new interface retains a bounded singleton expectation without an unending
rotation history. Supplied rho/moments, input-law acquisition, general cross
sections, finite-bit output, native calibration, practical superiority and
historical novelty remain distinct gates.

## 4. Stronger input and simpler executed operation: a Haar reset

The retained kinetic researcher supplied a cheaper positive construction
before any Choi consumer was executed. For the stated eta Haar+(1-eta)rho_f
law, even the computable-second-moment input is unnecessary. Let
D(M)=Tr(M)I/3 and R_f(M)=E_(rho_f) RMR^T. D commutes with every orthogonal
conjugation. Therefore exactly

    Psi_t=(1-e^(-eta t/2))D
                 +e^(-eta t/2) exp[(1-eta)t(R_f-I)/2].

With probability1-e^(-eta t/2), draw a fresh real uniform unit n and return
(z^Tz) times the bounded initial F1(n) query. Otherwise draw
N~Poisson((1-eta)t/2), compose N sampled rho_f rotations on z, and call the
initial F1 at that complex unit vector. Both branches have modulus<=1 and
the required mean. Covariance-mixture implementations may equivalently use
(Tr E0/3)z^Tz on the reset branch.

Expected sampled finite rotations are

    e^(-eta t/2)(1-eta)t/2 <=(1-eta)/(e eta).

This counts the rare expensive branch and is uniform in elapsed time. It
avoids matrix exponentials/Kraus conditioning and needs only a sampleable
rho_f plus the known Haar mixture weight. The Choi construction remains a
valid alternate interface for more general supplied finite moment maps;
it is not claimed as executed by the reset consumer. All full-law results
of Section3 inherit this simpler singleton operation. Numeric/bit and
time-input qualifications remain explicit.
