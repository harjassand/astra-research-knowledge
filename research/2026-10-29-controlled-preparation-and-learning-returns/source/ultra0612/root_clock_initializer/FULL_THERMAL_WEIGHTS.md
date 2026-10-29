# Full thermal syndrome weights at fixed couplings

29 October 2026. Root extension, independent review PENDING. This is the
missing bridge between the positive bond sampler and B's conditional FULL
clock Gibbs preparation. The ground-energy marginal alone would be wrong.

## 1. Precise target and strengthened cylinder gate

Keep lambda,Delta=1/(4lambda^L),beta fixed, independent of n. The correct
classical syndrome energy is

    F_beta(s)=-(1/beta)log Tr_clock exp[-tH_s(lambda)],
    t=beta Delta,
    F_beta(s)=Delta E_s-Theta_t(s)/beta.

The frozen clock_thermal theorem supplies the exact second identity. We
strengthen its KP gate to retain a spatial-support weight, rather than infer
that weight from sign incidence. Let h in (0,1) be the fixed bond-activity
parameter of PROOF.md, and put A_h=2+ln(1/h).

Use its fixed-slab construction with a LARGER fixed delta0 and smaller
fixed lambda so

    b_h=Kst^2 exp(A_h+1) epsilon_slab <=1/[2(Kst+1)].

This is possible: epsilon_slab=L2^d max(w^(1/q),exp(-delta0)); first enlarge
delta0, then decrease lambda. The same ordinary KP proof, applied to
activities exp(A_h |B|)z_B, gives the rooted bound

    sum_(C: union C contains x)||Phi_C|| exp(A_h mass(C))<=Bstar.

All norms now ALSO retain independent formal hopping-amplitude monomials,
in addition to free check parity. The exact Dyson proof already bounds the
absolute coefficients with sum_m a_e^m/m!, so extending its commutative
coefficient algebra to l1(N^hops) tensor l1(Z2^checks) costs no new factor.
KP multiplication and contraction apply in this Banach algebra. This
extension is explicit; a bound only on final check parity would not suffice.

## 2. Weighted excited-clock correction

The frozen temporal-lifting proof cancels all clusters of mass<M/2 between
the M-cycle and M times the infinite-line pressure, where M=floor(t/delta0).
For the remaining cylinder/line clusters, let B_C be the spatial projection
of the union. It is connected and |B_C|<=mass(C). Since
h^(-|B_C|)<=exp[(A_h-2)mass(C)], the strengthened rooted bound gives

    sup_i sum_(thermal terms: i in B_C)
               ||coefficient|| h^(-|B_C|)
       <=2 M Bstar exp(-M).                              (T1)

There are M time anchors for a given spatial i; line orbits can be anchored
at time zero, with the same M multiplier. This is the old temporal lift
with TWO spare units of exponential mass, not an exchange of limits.
It is uniform in spatial volume at fixed lambda. Take real parts of the
coefficient terms if individual ordered cluster contributions are complex:
the total log of the positive physical trace is real, and real projection
contracts the absolute norm. No signed scalar cluster is treated as a
positive state or sampled directly.

## 3. Connected hopping increments and the positive-bond admission

For a set C of retained hopping labels, let F_C(s) be the FULL finite-clock
free energy with only those hops present, and all onsite penalties retained.
Outside clocks factor out and contribute only a sign-independent scalar.
Define eta_A^F=sum_(C subset A)(-1)^(|A|-|C|) F_C. Disconnected A vanish by
Hamiltonian factorization. Each increment groups exactly the amplitude
monomials whose distinct hopping-label set is A. This equality follows
first in the absolutely convergent analytic series, then at the chosen
physical lambda. Grouping is only inside its declared connected A.

Set B_A to the union of the native supports of A. It is connected for
connected A, contains all its sign variables, and |A|<=d |B_A|, since a
clock meets at most d native labels. The scalar-free energy expansion,
after removing the nominal -(1/2)sum_c s_c, is

    F_beta(s)=scalar-(1/2)sum_c s_c+sum_b r_b S_Xb.

The fixed ground KT weighted bound from PROOF.md and (T1), retaining the
amplitude labels before grouping, imply

    sup_i sum_(b: i in B_b)|r_b| h^(-|B_b|)
        <=Gamma:=C_h lambda+(2M Bstar/beta)exp(-M).        (T2)

For the thermal terms B_A is contained in the cluster's spatial projection,
so replacing the latter by B_A only weakens its weight. Disconnected label
increments cancel exactly before they are used. Pure thermal terms with no
symbols are discarded as scalars, not as physical states.

Choose lambda sufficiently small that Gamma<=1/(16beta), in addition to
the weighted KP, KT, and conditional-cooling gates. Since M grows as a
fixed positive multiple of lambda^-L, the thermal term tends to zero faster
than any power. All these are simultaneous FIXED positive gates. Equation
(T2) gives the same positive bond augmentation and activity/mixing theorem
as PROOF Sections4--6, now for the CORRECT full Gibbs syndrome law.

## 4. Acquisition and truncation do not need an infinite time oracle

Retain connected distinct-hop sets |A|<=K. A discarded set has
|B_A|>K/d. Summing (T2) over m spatial anchors and using h<1 bounds its
global energy tail by

    e_K<=m Gamma h^(K/d).                                (T3)

Thus K=O(log(m/epsilon)), with fixed h,d, suffices for 2beta e_K<=epsilon/16.
There are m C^K connected A. Compute each F_C on <=qK clock cells, matrix
dimension <=L^(qK), for every subset C and its formal sign assignments.
Evaluate ALL finite eigenvalues by rational Hermitian inertia/eigenvalue
isolation to requested intervals, then use stable log-sum-exp for the FULL
trace. Precision O(log(t)+log(1/delta)+poly(K)) bits suffices for energy
error delta; offset the least eigenvalue before exponentiation. Its tiny
Boltzmann terms may be bounded and truncated, never silently underflowed.
The temperature input is computable from dyadic lambda and beta=4ln B0.

Subset/Fourier sums cost exp(O(K)) and O(K) extra cancellation bits, as in
PROOF.md. No full-n diagonalization, temporal-orbit enumeration or pressure
oracle is needed. Intervals determine signs or permit an explicitly charged
omission; downward rational bond weights and the common-denominator sampler
are unchanged. Therefore classical acquisition/sampling has polynomial
cost in m,1/epsilon for fixed qualified parameters. The literal gates and
huge fixed exponents are not evaluated or experimentally useful receipts.

## 5. What can be composed once the independent reviews finish

Sample the full corrected syndrome law by this positive gas. Conditional
on that CLASSICAL s, B's clock_preparation operation prepares the full
sigma_t,s, including all excited clock levels. Apply the paid nominal source
encoder/recovery and inverse prefix gauge. This prepares the actual full
Gibbs thermal encoder at fixed couplings, preserving arbitrary unknown
logical inputs and references. Classical-law and conditional quantum trace
errors add. The existing fixed-coupling exact CKG storage theorem can then
use an inverse-polynomial initializer error without multiplying it by the
storage time. This would close that MODEL-WISE initialization interface.

Acceptance is pending on BOTH this bridge and the conditional quantum
simulation receipt. Native baths, useful couplings, noisy hardware, unknown
charged-error autonomy and a civilisation-level capability remain open.
