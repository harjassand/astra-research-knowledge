# Constructive hereditary hybrid receiver

29 October2026. Independent contribution to the root MW receiver; no new
model/trajectory/parameter fixture. The improvement is a general physical
operation/quantifier, not a new claim to have invented coherent FT.

## 1. Two identities, with different input strengths

For any one consistent family G_M on finite labels V, define
B(R)=sum_(M superset R)G_M. For disjoint forced T and forbidden Z,

    H(T,Z)=sum_(M: T subset M, M intersect Z=empty)G_M
          =sum_(U subset Z)(-1)^|U| B(T union U).        (1)

Thus an inclusive-only bound ||B(R)||<=epsilon^|R| gives
||H(T,Z)||<=epsilon^|T|(1+epsilon)^|Z|. Neither independence nor positivity
of G_M is required. The boundary factor is genuinely paid in that abstract
argument; it cannot be dropped merely by calling the other terms benign.

There is another exact identity when Phi[K]=sum_(M subset K)G_M:

    H(T,Z)=sum_(U subset T)(-1)^|U| Phi[(V\Z)\U].       (2)

This follows by summing the Mobius coefficients, or by inclusion--exclusion
inside the active set A=V\Z. Importantly, an inclusive estimate proven only
for the full active set V need not hold after arbitrary Z are disabled.
A HEREDITARY physical proof is needed. Equations(1) and(2) are not interchangeable
norm assumptions.

## 2. Independent Gaussian data baths supply the hereditary proof

Let the total Hamiltonian be

    H_good(t) tensor I_data_baths + I tensor sum_j H_Bj
           +alpha sum_j A_j(t) tensor B_j,

where H_good acts on source, clocks and SEPARATE nominal environment. It
acts trivially on the data-noise baths. Each A_j acts only on the good
system, is Hermitian and has norm<=1. The independent data baths start
centered Gaussian, factorized from that good system, with specified free
correlations C_j(t,s). Their free Hamiltonians are source independent.
They must not also be hidden as strong check-conditioned interactions
inside H_good. Such an interpretation would invalidate the free-C Wick
resummation, even though the support algebra could still hold.

Use one slot per seed over the WHOLE interval[0,Twin], and define Phi[K]
by physically switching off the couplings outside K, all with the same
initial state and nominal dynamics. These are mathematical comparison
experiments, not a granted oracle or an exponential set of acquisitions.

For the hybrid(2), switch off all forbidden seeds Z first. In active set
A=V\Z use as reference the physical background with A\T coupled. Gaussian
correlation-variation resummation retains this whole background in exact
norm-one unitary propagators. The only selected correlation pairs belong
to the independent seeds in T. Inclusion--exclusion cancels any family
missing a marked seed. Each pair belongs to ONE seed, so at least |T|
pairs are needed. No evolved-bath Gaussian-state assumption is made.

With the uniform overpay

    eta=8alpha^2 max_j integral_[0,Twin]^2 |C_j(t,s)|dt ds,

the scalar majorant is sum_(k>=r)(r eta)^k/k!, r=|T|. For eta<=1, Chernoff
with z=1/eta gives (e eta)^r. This proof is independent of A,Z:

    ||H(T,Z)||_diamond<=epsilon^|T|,
    epsilon=e eta<=1.                                 (3)

No norm or relaxation rate for the marked/unmarked background is imported;
its exact unitary propagation is why strong clock cooling is retained.
The separate H_good may include arbitrary-strength memoryful CLOCK-only
baths if its source action is check diagonal and logical identity.

By contrast, a source-syndrome-changing DATA bath cannot be hidden in the
nominal reference merely because it is useful for cooling. Its disturbances
must be marked in the support theorem. That is why the earlier exact
fresh-bath-memory comparison alone was insufficient for this application.

## 3. Encoded support and the MW consequence

If H_good=sum_s Pi_s tensor H_s and each A_j has fixed SOURCE support X_j,
propagation by H_good keeps source Pauli labels, adding only check/environment
coefficients. The initial source is in the code sector and its environment
is independent of the logical input. Every Phi[K] therefore has, on encoded
input, a Pauli-pair expansion supported on union_(j in K)X_j. Mobius inversion
immediately gives the declared encoded-support property for G_M. It does not
require every interaction-picture source operator to have bounded spatial
support. Quantum environment coefficients become scalar coefficients after
the fixed environment is traced; none depends nonlinearly on the input.

Adopt Han et al., arXiv2609.20537v1 AppendixC's syndrome selectors and
minimum-weight density argument. If each source support has size<=q and
total slot incidence per qubit<=D, the hereditary bound(3) gives

    L_phys=2^D epsilon^(1/(2q)),
    ||Lambda_MW-id||_diamond<=2[exp(Xi)-1],
    Xi=sum_(connected K, |K|>=distance) L_phys^|K|.

This removes the generic forbidden-boundary factor while retaining arbitrary
nonfactorization of G_M. It is the stronger actual physical input, rather
than a formally stronger estimate assumed for free. It still assumes a
perfect FINAL global syndrome extraction/MW correction and no unproved
reapplication to later correlated-bath windows.

The accepted fixed passive band has g0<=4A0, A0=4C_B, uniformly at inverse
temperature>=1. Consequently M0=integral_R|C|<=g0^2<=16A0^2 and a rational
sufficient noise parameter is epsilon_phys=384alpha^2 Twin A0^2. No bath
fixture was run to acquire this: it is a direct convolution consequence
of the already frozen scalar filter bound.

## 4. Strong ordinary bounded-Hamiltonian alternative

For arbitrary shared environment, let every FULL perturbation V_j(t) be
bounded in norm by alpha. Holding Z off, interpolate the forced amplitudes
x_j in[0,1]. The hybrid(2) is the mixed finite difference, hence the integral
of the r-fold mixed derivative. Multi-Duhamel yields r! insertion orders of
commutator maps of complete norm<=2alpha. Their simplex volume is Twin^r/r!,
and all intervening propagators at real x are joint unitary channels.
Thus, with no Gaussian or bath-independence assumption,

    ||H(T,Z)|| <=(2alpha Twin)^r.                       (4)

This is the equally informed conventional local-Hamiltonian incumbent, not
new generic fault tolerance. It still needs the same separate encoded-
support property to feed the MW theorem. The Gaussian result matters for
unbounded oscillator fields, finite correlation-based input and zero-mean
quadratic weak-coupling scaling. It is not asserted to beat an applicable
bounded-Hamiltonian method or to implement a decoder economically.
