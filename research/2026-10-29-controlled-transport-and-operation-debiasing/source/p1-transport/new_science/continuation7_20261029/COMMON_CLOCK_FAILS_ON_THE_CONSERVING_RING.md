# A shared fast clock can retain the wrong rare-transport law

29 October 2026. Root's next constructive attack after the action
receiving proof. This is an actual conserving-ring counterexample,
not a heat-bath relabeling. It separates independent local control
from one common Poisson pi clock under the same permitted nonlocal
kinetic amplitudes. No apparatus or priority claim is attached.

## 1. The reversible ring with a collective parity coordinate

Take N even, sites indexed 0,...,N-1, c=s/2, and 0<alpha<1. Put

    delta_i=eta_i-eta_(i+1), a_i=delta_i^2,
    A(eta)=sum_i a_i,
    p(eta)=(-1)^(sum_i i eta_i).                         (1)

Every actual nearest-neighbor particle/hole exchange flips p, including
the bond from N-1 to 0 because N is even. Let sigma be one common
orientation, flipped by a fresh independent Poisson clock at physical
rate gamma_N. Define u=sigma p and the actual native rates

    r_i=c[1+alpha u delta_i].                           (2)

Only active bonds delta_i!=0 produce a change or a signed current
increment. Null attempts are not counted as exchanges in this proof.

This is a member of the controlled amplitude family: alpha_i(eta)
=alpha p(eta)delta_i is bounded and invariant under its own exchange,
since both factors change sign. Consequently the instantaneous native
generator is reversible for uniform occupancies, for each sigma.
The joint generator including sigma flips is reversible for uniform
occupancies times a fair common sign, separately in every particle
sector. Hidden z is unnecessary for this counterexample; the allowed
nonlocal amplitude itself supplies the collective memory.

Around a ring, sum_i delta_i=0. Therefore the total active native
intensity and total signed current drift are exactly

    sum_(active i)r_i=c A,
    sum_i r_i delta_i=c alpha u A.                      (3)

The common clock can become arbitrarily fast in physical units while
remaining slow compared with the collective native event rate O(N).
Assume

    gamma_N ->infinity, gamma_N/N ->0.                  (4)

For example gamma_N=sqrt(N) satisfies both conditions.

## 2. An exact current decomposition

Let J(t) be the total signed native current by physical time t. At a
native exchange, u flips and define the increment

    d_i=delta_i-alpha u_pre.                            (5)

The sum M(t) of these increments over native exchanges is already a
martingale: (3) implies sum_(active i)r_i d_i=0 exactly.
Its predictable quadratic variation is

    <M>_t=c(1-alpha^2)int_0^t A(eta_v)dv.               (6)

Indeed expanding d_i^2 and using (3) gives
sum_(active i)r_i d_i^2=c A(1-alpha^2). Its jumps are bounded by two.

Let K(t) be the common sign's Poisson count and

    C_gamma(t)=int_0^t u_(v-)dK(v)-gamma_N int_0^t u_vdv.
                                                               (7)

This is a martingale with bracket gamma_N t. Since every native
exchange and every common-clock event reverses u,

    J(t)=M(t)+(alpha/2)[u_0-u_t]
                 -alpha C_gamma(t)-alpha gamma_N int_0^t u_vdv.
                                                               (8)

This pathwise identity is the central construction. The collective
memory cancels a fraction of native current fluctuations even when
the common sign itself is randomized frequently.

## 3. The remainder is negligible at the rare-event scale

Observe physical time N^2 T and let Q_N=J(N^2T)/N^2. The boundary term
in (8), divided by N^2, is at most alpha/N^2.

For the clock martingale, the bounded-jump exponential estimate gives,
for every fixed real b,

    log E exp[b alpha C_gamma(N^2T)/N]
       <=gamma_N N^2 T
            [exp(|b alpha|/N)-1-|b alpha|/N]
       <=C_b gamma_N T.                               (9)

For the last term, put V_N=alpha gamma_N sigma p on macroscopic time.
There is only one sign coordinate. Its integration-by-parts identity
gives |<V_N,f^2>|<=sqrt(2) alpha gamma_N sqrt(D_sigma(f))
for ||f||_2=1. The native form is nonnegative, and the common-clock
part of the macroscopic generator is N^2 gamma_N times the sign form.
Feynman--Kac therefore gives exactly

    log E_mu exp[bN int_0^T V_N dt]
        <=alpha^2 b^2 gamma_N T/2.                     (10)

The reference mu can be uniform occupancies times a fair sign, or
uniform within a fixed particle sector times a fair sign. An arbitrary
deterministic initial occupancy/sign law costs at most 2^(N+1) against
the former, which adds only (N+1)log2 to the exponent. An arbitrary
retained initial record is therefore permitted pointwise as well,
provided the entire future conditional native-and-clock generator
remains the declared law. Clock freshness alone is insufficient if
the old record exposes future native innovations.

Divide (9)--(10) by N, use (4), apply Chernoff for each fixed b, then
let b increase. The two remainders in (8) are superexponentially
negligible at speed N. Thus Q_N and M(N^2T)/N^2 are exponentially
equivalent at that speed. This is not obtained from a central limit
theorem or a variance comparison.

## 4. A strict rare-current upper bound disproves the reference action

Assume only that the conserved mass m_N tends to m in (0,1). The
one-block activity upper bound in the root receiving proof applies
here because r_i>=c(1-alpha)>0 and own-swap reversibility holds.
It permits arbitrary initial occupancies and the retained common
orientation. Consequently, for every epsilon>0,

    P(int_0^T A(eta_(N^2t))/N dt>2chi(m)T+epsilon)
          is superexponentially small at speed N.       (11)

The exponential martingale for M has compensator

    B_N(b)=int_0^(N^2T) sum_(active i)
                    r_i[exp(b d_i/N)-1-b d_i/N]dv.     (12)

Its normalized quadratic expansion, using (6), is

    B_N(b)/N=(b^2 c(1-alpha^2)/2)
                    int_0^T A/N dt+O_b(N^-1).          (13)

The error is deterministic: all d_i and rates are bounded, and the
physical horizon times the total rate is O(N^3). Exactly as for the
ordinary scalar-current upper bound, (11)--(13), the mean-one
martingale and exponential equivalence yield

    lim_(delta down to 0) limsup_N N^-1 log P(|Q_N-q|<delta)
       <=-q^2/[2s chi(m)(1-alpha^2)T].                  (14)

For every q nonzero, this is strictly smaller than the logarithmic
probability -q^2/[2s chi(m)T] produced by independent local kicks.
Hence the common-clock process cannot have that reference LDP.
A matching lower bound or a complete common-clock action is not
needed for this contradiction and is not claimed in (14).

The initial occupancies may be the same deterministic configurations
with flat empirical density used by the independent-control theorem.
All initial signs may be recorded +1. In that matched comparison,
the independently kicked physical family has the known reference
action for any gamma_N->infinity, whereas applying one common kick
at gamma_N=o(N) fails. The difference is a real actuation supplier,
not a distinction between two algorithms given the same supplier.

## 5. A matching current-variance diagnostic under a warranted stationary law

For an additional exact limit, initialize uniform canonical occupancy
with M_N particles and a fair common sign. This is a specified
stationary joint law, not an initializer supplied by the theorem.
Then

    E[A/N]=2m_N(1-m_N)N/(N-1), Var(A/N)=O(1/N).         (15)

The variance statement follows directly by counting adjacent and
disjoint bond pairs under sampling without replacement. Stationarity
and Jensen imply that the integrated activity in (11) converges in
L2 to 2chi(m)T, with no temporal mixing assumption. Equations (6)
and the bounded-jump martingale central limit argument give

    M(N^2T)/N^(3/2) -> Normal(0,s chi(m)(1-alpha^2)T).   (16)

The clock remainder's L2 norm at this scale is O(sqrt(gamma_N/N)).
For the occupation remainder, apply (10) with a general exponential
multiplier: its centered scaled value has a sub-Gaussian variance
proxy alpha^2 gamma_N T/N. Its L2 norm has the same vanishing order.
The deterministic boundary term also vanishes. Therefore

    sqrt(N) Q_N -> Normal(0,s chi(m)(1-alpha^2)T).        (17)

This final-time fluctuation result and the strict rare-current upper
bound are distinct proved claims. The former does not by itself
establish or contradict an LDP; the exponential calculation (14)
does that work.

## 6. Consequence and open next connection

The example puts the collective-control obstruction inside the
same conserving-ring language as the positive action theorem.
It gives a macroscopic integrated-current output and permits the
same deterministic flat initial profile. It shows why arbitrary
nonlocal kinetic contexts make actuator independence consequential.
It does not assert that all common-control programs fail, that
gamma_N>>N is necessary for every model, or that deterministic
rotation has the identical threshold without its separate proof.

A promising stronger question is the full common-clock action.
The exact current correction suggests a nonlocal mobility modification
in the spatially uniform current component. That suggestion is not
a proved action and is kept separate from (14)--(17).

## 7. The same construction can suppress all speed-N circulation events

Let alpha=alpha_N tend to one, allowing alpha_N=1 exactly. Assume
the same common-clock regime gamma_N/N->0. The identity (8) and
the exponential remainder bounds (9)--(10) continue to hold uniformly.
At alpha=1, M is identically zero: every permitted native exchange
has delta_i=u_pre, so its corrected increment (5) vanishes.

More generally, without any occupation replacement or native
ellipticity, A<=N and (6) imply the native martingale exponential bound

    limsup_N N^-1 log E exp[b M(N^2T)/N]
          <=limsup_N [c b^2(1-alpha_N^2)T/2+O_b(N^-1)]=0.
                                                               (18)

Together with the remainders and Chernoff, this proves for every
epsilon>0,

    limsup_N N^-1 log P(|Q_N|>epsilon)=-infinity.         (19)

The statement holds from arbitrary initial occupancies and a retained
initial sign. The proof uses only bounded rates, reversibility, and
the supplied common clock; no local-equilibrium initializer is needed.

By contrast, the independently kicked version of exactly these
amplitudes has the ordinary nontrivial circulation rate
q^2/[2s chi(m)T], even at alpha=1. The receiving extension
`INDEPENDENT_CONTROL_OPENS_ZERO_RATE_GATES.md` supplies the exchange
form from the independent sign operation itself, so native zero rates
do not invalidate that positive comparison.

Each bond's marginal sign process has the same flip rate gamma_N in
the common and independent implementations. Their joint control
correlations differ. With gamma_N->infinity and gamma_N/N->0, those
correlations select between the reference rare-transport law and
superexponential suppression of nonzero circulation in this family.
This is a mathematical control mechanism before any device claim.
Joint actuation and timing, including their records and costs, are
material physical premises.

## Subsequent receiving result and actual reviews

The strict upper bound and endpoint suppression were independently
reviewed in `record_geometry/COMMON_CLOCK_AND_ZERO_RATE_REVIEW.md`
and `physical_mechanism/receiving_review/COMMON_CLOCK_RECEIVING_REVIEW.md`.
Exact reviewed snapshots remain alongside those reports. The requested
complete conditional native-and-clock-law clarification is incorporated
above; final receipts distinguish it from the earlier snapshot.

The subsequent root theorem `COMMON_CLOCK_MATCHING_RARE_TRANSPORT.md`
adds a matching scalar lower bound and SCGF under its actual canonical
initial-law premise. It uses a corrected-current tilt with an O(1)
adjoint entropy source. It does not retroactively give the arbitrary
deterministic-initial upper bound here a matching lower bound, and it
does not identify the entire shared-clock spatial action.
