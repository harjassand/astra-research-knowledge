# Whole challenge of the collective-critical canonical readout

29 October 2026. **ACCEPTED at the stated finite-source, high-occupation,
bounded-output mathematical scope.** No substantive correction requested.
The final input hashes are bound in RECEIPT.json. The producer confirmed
its 20-file snapshot stable before this handoff.

I whole-read LOWER_OPERATOR_PROOF.md, TRIAL_NORMALIZATION.md,
THERMAL_READOUT.md, MATRIX_ACQUISITION.md, ALL_M_COST_AND_SCOPE.md and the
complete current compile_readout.py. I also read the execution binding,
actual input/receipt fields, current/result account and prior/cost account.
This is an independent analytical reconstruction, plus an exact consumption
of saved scalar intervals. It is not a new run of the producer, a numerical
matrix-function replay, Fock calculation, stochastic experiment or independent
physical validation.

## 1. Exact lower operator: signs, coefficient and pressure

For A=b0^dagger b_j one has

    A^dagger A+AA^dagger=2n0 n_j+n0+n_j
                         <=(2K+1)n_j+K.

The four retained quadratures therefore give exactly the coefficient
8K+4 in front of Hhop and 8K Tr(T) in the additive term of C1. No
one-body diagonal/normal-order term is lost. The one-particle matrix of
i[Q_j,J_-j] is

    u(e_j^2)^T+(e_j^2)u^T-2e_j e_j^T/sqrt(M).

Resolving e_j^2 into its uniform and Q components gives C2, including
the COMMON position-quadrature term. Summing its coefficients weighted by
sqrt(t_j) yields E^T diag(sqrt(T)), and the square-completion cost is
d^T T^+ d, independent of eigenbasis choices or degeneracies.

For Y=sqrt(U)Q-i sqrt(a t)J the identity is

    UQ^2+a t J^2=Y^dagger Y+sqrt(U a t) i[Q,J].

Thus the leading commutator has the POSITIVE sign displayed in C3.
The negative depletion contribution is paid by the separately reserved
epsilon Hhop using Hhop>=lambda Nexc. This is an operator estimate on the
whole fixed K,K sector; it does not assume small depletion. Completing the
remaining common-position squares subtracts exactly (U/4)d^T T^+ d.
The other squares stay positive, and in particular

    H >= L_K I + sum_j Y_j^dagger Y_j

is valid with the stated C3 constant. Expanding its elementary scalar
factors gives C4 with the conservative C/2 allowance. Keeping Y^dagger Y,
rather than the opposite order, is crucial to the later GNS argument.

For the trimer, eigenvectors (1,-1,0),(1,1,-2) give eigenvalues 2,12.
They also give d^T T^+d=(7-2sqrt(6))/36. Hence C=2sqrt(2)+2/sqrt(3),
cbar=5 and the all-K constant 24 are valid; small K is paid by positivity.

The native all-M matrix gate can be reconstructed directly. A trimer
block is >=2Q, whereas its two-edge path Laplacian is <=3Q. With
epsilon_bus=1/100000, the complete matrix is therefore >=epsilon_bus
times the full M-site path Laplacian, and <=(12+4epsilon_bus)I.
The elementary path gap gives lambda>=4epsilon_bus/M^2. This verifies the
supplied one-particle gap/norm promise without a floating eigensolve or a
many-body gap assumption.

## 2. Matching normalized upper: no overlap or relative-CLT oracle

The categorical covariance is I/M-11^T/M^2 in d=M-1 integer coordinates;
its determinant is M^(-M). The paired difference has characteristic
chi^K, while the centered residual K-1,K difference has
chi^(K-1) psi^*. Both facts follow from the finite multinomial source.

I reconstructed the global Fourier decay, central-ball fourth-moment
estimate and logarithm bound in N1. For example, a centered categorical
variable satisfies E Y^4<=M(EY^2)^2, and the difference of two copies gives
the (M+3)/12 remainder. The displayed b factor is harmless uniformly in
d: -(d/2+2)log(1-1/(24d))<=5/46<log2. The residual factor uses
|1-psi|<=u/2. Outside the central ball, splitting the remaining exponent
and integrating a full Gaussian gives the stated B_M and tau_M, including
the Gaussian comparison outside the Fourier torus. The estimate is absolute
and uniform over all lattice points, not a false relative local limit.

The A_d lattice has covolume sqrt(M); its integer embedding has squared
OPERATOR norm M. Poisson summation with the stated dual bound consequently
pays every affine shift in N2. Only the unshifted sum is differentiated
for N3. The dual derivative is nonnegative, so the discarded contribution
has the required sign for the upper second-moment inequality.

Multiplying the uniform absolute CLT error by the full Gaussian filter and
summing gives N4 with the determinant ratio Rdet. The same unshifted
moment bound gives N5, without deducing an unbounded moment from TV.
The residual annihilation formula for hopping is exact; its Gaussian
completion includes the extra shift penalty sigma_ij<=M/(4K).
Thus N6 pays numerator AND denominator errors. Since T1=0,
sum T_ij a_ij=-2Tr(TG). The absolute entry sum in N7 correctly handles
frustrated signs. No positive-bond Dirichlet-form shortcut is used.

The choice G=sqrt(MU/2) T_Q^(-1/2) makes the two leading energies add to
C sqrt(K). The acquired norm need not be physically sampled: N4 bounds
it analytically. A tiny filter success probability is not silently made
free for a trial-preparation task, because this operation never claims
to prepare that trial. It calculates its energy for a variational bound.

## 3. Passage to ACTUAL Gibbs and the finite-query theorem

The actual finite canonical Hilbert dimension is D^2, D=binomial(K+d,d).
The variational free-energy bound F_beta<=Etr and S(rho)<=2log D give
E_rho H<=Eup. Together with the retained lower squares, this gives the
actual-Gibbs depletion and annihilation-defect bounds T2. No trial/Gibbs
trace-norm comparison, relative partition function or mixing promise is
being inferred.

The one-body GNS estimate T3 follows from Nexc^2<=2K Nexc and exact
number-conserving creation/annihilation identities. Its final constant
2+2sqrt(2)<5 is correct. The mixed one-particle commutator has norm<=2
and uniform expectation 2delta_lj/sqrt(M), paying T4.

In the Duhamel expression for [Jtilde_j,F_t], the centered commutator
appears as Tr rho F_t C plus an OPERATOR-norm conjugation error. The former
is bounded by ||C||_rho with the stated ordering. No invariance of rho
under the phase rotations is assumed. This yields T5 with the displayed
sqrt(d) factor and the conservative constant 8.

The exact Stein identity uses A_j^dagger F_t and F_t A_j. BOTH are
bounded by ||A_j||_rho: they are respectively the GNS inner products
<A_j,F_t> and <F_t^dagger,A_j>. There is no unjustified substitution of
||A_j^dagger||_rho. Summing squares uses exactly the available
sum E_rho A_j^dagger A_j<=Bfast/sqrt(K). The derivative sign and covariance
Sigma_K in T7 follow. Integrating on s t for 0<=s<=1 gives T8: the three
radial integrals are 1,1/2,1/3, and the final Gaussian factor is <=1.

This proves actual characteristic-function errors for the stated bounded
queries. The Fejer instrument is positive and normalized exactly by finite
Fourier orthogonality. Its Gaussian proxy is the SAME instrument averaged
under a normalized scalar Gaussian, so positivity is not guessed from a
truncated Fourier sum. The harmonic-weighted error A1 and the dyadic table
error then give a genuine finite-output TV bound. Choosing a query first
from a supplied finite distribution is covered; simultaneous full Gibbs
sampling or arbitrary-query joint laws are not inferred.

The free-energy interval T9 has width O(log K) at fixed M. It is NOT a
relative-Z estimate and does not acquire an occupation/full-state sampler.

## 4. Matrix enclosures, growing M and actual software

The Newton--Schulz residual recurrence and its square-root/inverse-root
tails are correct for the actual spectral interval of T+P. The Arb
operations enclose the exact polynomial iterates; their rounded outputs
are not asserted to commute exactly. Adding the analytic tail to every
entry is conservative. Exact uniform-projector removal, centered pressure,
full-dimensional determinant ratios and query quadratic forms preserve
the correct null mode. The determinant proxy is a trial normalizer, not
the interacting Gibbs Z.

I checked the sufficient all-M gates. The Poisson exponent bound pays
log(8dK) by separately allocating the two square-root-K gates. The CLT
tail gate pays B_M exp(-tau_M K)<=1/K despite the possible size of B_M.
The bounds delta<=13M^3/K, gamma<=G0/K, Rup<=Rbar and then T8's
K^(-1/8) sufficient rate follow with the stated conservative constants.
This gives explicit polynomial joint K(M,error^-1) for the declared
polynomial conditioning/query inputs. It is not fixed density.

The all-input bit argument is condition-sensitive. The coarse polynomial
coefficient growth bound is polynomial in condition NUMBER and requested
log accuracy, not a general polynomial in the binary length of an
arbitrarily bad condition number. The native family has the admitted
polynomial-M gap, so its stated all-M conclusion is paid. The saved
executable is fixed to M3/M32, U=beta=1 and 2048 bits with width checks;
it is not an executed universal adaptive precision/gate selector.

The M32 readout uses +17 on the first 15 sites and -15 on the other 17.
It is exactly constant on each complete trimer, so its unconnected-core
quadratic form vanishes. The bus supplies its nonzero response. It is a
chain-wide query, not a repeated first-trimer observable. K=2^192 and its
detector's dyadic phase coefficient are explicit; that occupation is not
a useful single-band material claim.

The saved current code differs from the exact executed source ONLY by the
declared K>=4d+4 guard, true on every candidate. The independent consumer
checks that byte identity. It then consumes the saved variance endpoints
using Fraction arithmetic, an outward sqrt(5), and an exponential Taylor
remainder; it imports no producer function. It reproduces sufficient total
TV bounds <0.002131 and <0.000783 and the M32 first-outcome bound <0.4544.
It also verifies both normalized 48-bit tables and the exact published
rounding-error identities. This is saved-input scalar consumption, not a
new source/matrix/Fock run. See EXACT_CONSUMER.json.

The producer's final compilation took 0.982223625 internal seconds,
0.838030541 after imports, with M32 matrix work 0.800949917 seconds.
Its initial weaker local-query run and the stopped endpoint-serialization
and failed 768-bit attempts remain charged in SOURCES_AND_COSTS. Those
historical costs are producer reports, not new reviewer measurements.
The review consumer took 0.17275591600628104 internal seconds after its
imports. Its first serialization attempt stopped at Python's decimal-digit
limit after the first case's arithmetic checks; the replacement emits
outward 80-bit dyadic summaries rather than giant decimal Taylor LCMs.
No producer run or scientific source changed. Analysis/source-reading wall
time was unmetered; no samples, dynamics, Fock states or physical data were
generated by the review.

## 5. Strong ordinary comparator and judgment

Ordinary number/phase theory already supplies the same result at leading
order. Writing p=(theta_b-theta_c)/2 conjugate to q and expanding hopping
around uniform density K/M gives the relative harmonic operator

    Hrel=sum_j [U q_j^2+(2K/M)t_j p_j^2].

Its vacuum energy is C sqrt(K), and the covariance of q/K^(1/4) is
diag sqrt(t_j/(2UM)). At fixed beta>0 its harmonic thermal correction is
the ordinary coth(beta sqrt(2UKt_j/M)) factor. Thus the key law and
squeezing scale are not new predictions obtained by defeating a bare-pair
approximation. The actual finite-K covariance used here is a paid small
scalar modification of that ordinary leading covariance.

Primary comparison was checked against Mora--Castin
[cond-mat/0212523v2](https://arxiv.org/html/cond-mat/0212523v2), Introduction
and phase-density construction, and Lingua--Penna
[1706.03804v1](https://arxiv.org/html/1706.03804v1), model and continuous-
population spectral treatment. Those supply serious collective methods
for the ordinary route. Lewin--Nam--Serfaty--Solovej
[1211.2778v4](https://arxiv.org/html/1211.2778v4) is a rigorous spectrum/
positive-temperature comparator. Its fixed 1/(N-1) interaction scaling
and Hartree assumptions do not transfer automatically to this fixed-U
critical family. This bounded check establishes no historical absence.

Canonical ED/tensors and any qualified importance/MCMC or effective rotor
method receive the same Hamiltonian and query. The Hilbert dimension
>2^11678 at M32 is a literal full-basis cost warning, not a lower bound on
all those methods. No practical advantage is established by it.

The earned operation is nevertheless real: the normalized trial/lower
operator/GNS chain gives explicit finite-source error control for ACTUAL
canonical bounded readouts, without acquiring full Gibbs/Z or assuming
the harmonic closure. It handles fixed positive U with all the displayed
large-occupation and conditioning costs. This is substantive mathematical
acceptance at that scope; it is not weakened because a stronger physical
or fixed-density claim remains unpaid.

Native matrix coefficients and uniform zero-mode symmetry are exact model
inputs, with numerical acquisition uncertainty outward enclosed. This
does not acquire experimental parameter calibration, a microscopic
high-occupation material, readout apparatus, finite-density phase,
state preparation, real-time dynamics or a general Gibbs algorithm.
Historical novelty and practical usefulness remain UNKNOWN. No additional
case, simulation or audit is required for the acceptance stated here.
