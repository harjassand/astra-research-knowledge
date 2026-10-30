# Unknown gains: a sharp scope boundary for the cubic construction

This continuation proves two obstructions and a finite, coarse-accuracy
construction. It does **not** settle arbitrary-accuracy native control in
the enlarged gain box. Diamond norms are full norms, with no factor of 1/2.
Let F=Z1 X2 and h=g_A g_B g_C, so h ranges over [1,8].

## 1. The completed primitive does extend, but its coefficient is h

Use exactly the ten chronological native segments in the checkpoint, with
fresh signs s_A,s_B and s_C=s_A s_B. The simultaneous interaction-frame
memory triple S_j(t) remains norm one and 1-Lipschitz. The actual handles
are g_j P_j tensor S_j(t), hence norm at most two and 2-Lipschitz. In
particular the fixed, unknown static gains do not break the sign identities.

For 0<delta<=1/100, the checkpoint argument, retaining the gains throughout,
gives a bath anti-Hermitian K with

    || E_s Ad_U - Ad_( exp(-4 i h delta^3 F) tensor exp(K) ) ||_diamond
        <= 50000 delta^4.                                      (1)

Here are explicit bounds, so (1) is not an appeal to a gain-calibrated
theorem. With L=10 delta, define

    G_j = g_j integral f_j(t) S_j(t) dt,
    Q = -sum_j g_j^2 integral_(t>s) f_j(t) f_j(s) S_j(t)S_j(s) ds dt,
    K=(Q-Q^dagger)/2.

The exact identity Q+Q^dagger=-sum_j G_j^2 still holds. Therefore
||Q-K||<=466 delta^4 and ||K||<667 delta^3. The frozen cubic is
-4 i h delta^3 F. Midpoint freezing its three factors costs at most
10000 delta^4. The Dyson tail from degree four costs less than
8143 delta^4, using exp(20 delta)(20 delta)^4/24.

Put X=K-4 i h delta^3 F; ||X||<699 delta^3. Its exponential remainder
is less than 25 delta^4 on this range of delta. Consequently

    ||E U-exp(X)|| < (466+10000+8143+25)delta^4
                   =18634 delta^4.

For every sign, freezing costs at most 50 delta^2. The frozen unitary
minus I is bounded by 32 delta^3+8143 delta^4, and exp(X)-I by
699 delta^3. Thus ||U-exp(X)||<59 delta^2. Expanding the averaged
channel about exp(X) gives

    2*18634 delta^4+59^2 delta^4 =40749 delta^4 <50000 delta^4.

This controls the actual channel variance. It is uniform in the bath,
spectator dimension and initial DMR correlations. Fresh coins allow the
same joint-channel telescoping as in the checkpoint. In particular,
N cycles approximate exp(-4 i N delta^3 h F) on data with error
50000 N delta^4. Reversing one handle convention changes the sign of the
logical coefficient while keeping the bath term memory-only.

For a specified rational alpha, choose a dyadic delta and the integer
N nearest |alpha|/(4 delta^3). The ideal reduced-channel error against
exp(-i alpha h F) is at most

    50000 N delta^4 + 32 delta^3.                               (2)

The second term allows h<=8 and rounding the angle by at most
2 delta^3. All parameters depend on alpha and the requested tolerance,
not on h. This uses 10N segments, duration 10N delta, and two private
bits per cycle. Timing errors eta per segment add at most 4m^2 eta
in diamond norm, m=10N: compare switching times in the drift interaction
frame, where adjacent handles differ in norm by at most four. A sufficient
choice for an extra error budget b is eta=b/(4m^2).

Thus every fixed unknown-product phase alpha*h is available to arbitrarily
small error with finite resources. This fact alone cannot flatten h.

## 2. A positivity obstruction for every randomized phase-only program

Consider the ideal interface consisting of arbitrary completed operations

    exp(-i alpha h F) tensor B,

where alpha is chosen without gain information and B is any bath unitary,
possibly depending on the gain, bath, time, and private classical branch.
Products of such operations remain a single data phase exp(-i a h F)
times a bath unitary. Allow **any** probability law mu for a, even one with
infinite support. After discarding memory the data channel is

    Phi_h = integral Ad_exp(-i a h F) dmu(a).                   (3)

This covers arbitrary signs, sizes, repetitions and outer mixtures at the
ideal phase-only interface. A physical compilation is covered whenever its
averaged reduced channel is within a known residual b of a channel (3).
For checkpoint-based compilation, one valid class is a fixed finite
composition, or an outer random choice independent of all the fresh inner
cycle signs. Reusing inner signs in later decisions is not automatically
covered by the checkpoint's averaged-channel comparison.

In the +/- eigenspace decomposition of F, (3) preserves diagonal blocks
and multiplies the upper off-diagonal block by

    phi(h)=integral exp(-2 i a h) dmu(a).

The desired E=exp(-i pi F/4) has multiplier -i. Exactly,

    ||Phi_h-Ad_E||_diamond = |phi(h)+i|.                        (4)

For the upper bound, factor the phase of phi(h)+i out as a unitary
rotation and use the off-diagonal projection (id-Ad_F)/2, of diamond norm
one. For the matching lower bound, input the equal superposition of one
normalized vector in each F eigenspace. Its output difference is a 2x2
Hermitian matrix with off-diagonal entry (phi(h)+i)/2 and trace norm
|phi(h)+i|. Tensoring a fixed memory state makes this an admitted DMR
input, so (4) also witnesses the original output contract.

Let m_k=phi(k), k=1,...,8, and m_-k=conjugate(m_k), m_0=1.
These are moments of Z=exp(-2ia), a unit-modulus random variable. Therefore
the 9x9 Toeplitz matrix

    T_jk=m_(j-k),             0<=j,k<=8,                        (5)

is positive semidefinite: its quadratic forms are expectations of squared
absolute values of polynomials in Z. All eight tested products h=k are
admitted, for example by setting every g_j=k^(1/3). No bath is needed for
this obstruction; H_M=0 already suffices.

The desired target moment matrix T_* has diagonal one, entries +i above
the diagonal, and -i below. For n=9 and

    v_j=exp(i pi j/n)/sqrt(n),

direct geometric summation gives

    T_* v = (1-cot(pi/(2n))) v.

If |m_k+i|<=e for k=1,...,8, every off-diagonal entry of T-T_* has
absolute value at most e. Since every |v_j|=1/sqrt(n),

    0 <= v^*Tv
       <= 1-cot(pi/(2n)) + (n-1)e.

Consequently every probability law mu satisfies

    max_(1<=h<=8) ||Phi_h-Ad_E||_diamond
      >= c_* := (cot(pi/18)-1)/8
       = 0.583910227... .                                     (6)

In particular a physical program with phase-only comparison residual b
has worst-case error at least c_*-b. Sending b to zero cannot yield the
requested arbitrary-accuracy gate. This is a channel-positivity result,
not an assertion that averaging angles or averaging unitaries is sufficient.

## 3. A constructive coarse upper bound within the same ideal interface

The class in Section 2 is not empty or limited to deterministic phases.
Choose a>=0 from an exponential distribution of mean a0. Then

    phi(h)=1/(1+2 i a0 h).

Writing x=2a0 h, the exact squared error is

    |phi(h)+i|^2 = 1-(2x-1)/(1+x^2).

The function (2x-1)/(1+x^2) first increases and then decreases on x>0.
Set the endpoint values at h=1 and h=8 equal. The positive solution is

    x0=(63+sqrt(10241))/224,    a0=x0/2.

It gives the uniform bound

    max_(1<=h<=8) |phi(h)+i|
        <= sqrt(1-(2x0-1)/(1+x0^2)) < 0.836.                   (7)

This ideal law can be made into a genuinely finite legal randomized
program. Given an extra budget eta>0, truncate a at L and round down to
a mesh Delta. Truncation changes every multiplier by at most
2 exp(-L/a0); rounding changes it by at most 16 Delta because h<=8.
Take L>=a0 log(8/eta) and Delta<=eta/64. Round the finitely many branch
probabilities to a common dyadic denominator so their l1 difference is
at most eta/4. Their mixture channels then differ by at most eta/4.
Compile each finitely many rational mesh phases using (2), to diamond
error at most eta/4. The total additional error is at most eta.

All duration and switch requirements are explicit finite quantities:
for mesh alpha_j=j Delta choose a dyadic delta_j<=1/100 and
N_j=nearest(alpha_j/(4 delta_j^3)) satisfying

    50000 N_j delta_j^4+32 delta_j^3 <= eta/8,

and use m_j=10N_j segments with total duration m_j delta_j. Supply
duration tolerance eta/(32 m_j^2) for the remaining eta/8 per-branch
budget. There are finitely many branches, bounded phase L, and a finite
dyadic coin sampler. This constructs a uniform gate approximation of
error less than 0.836+eta, for all initial correlations and admitted moving
baths. It is not a route to arbitrarily small error; (6) forbids that
within this class.

The executable `phase_schedule.py` uses an equivalent rational construction
to avoid irrational sampling parameters. Set a0=11/30. Direct evaluation
of the same endpoint formula gives base error sqrt(5554/7969)<0.835.
For an integer d>=1 put p=2^-d, r=1-p and
Delta=a0/(2^d-1). A geometric failure count J_0 has mean r/p; therefore
the random phase alpha=Delta J_0 has characteristic multiplier

    phi_geom(h)=1/[1+(a0/Delta)(1-exp(-2 i Delta h))].

Both this denominator and 1+2ia0h have modulus at least one. The Taylor
remainder |1-exp(-iy)-iy|<=y^2/2 shows that their inverse multipliers
differ by at most 2a0 h^2 Delta<=128a0 Delta. Choose d so this is <=eta/4.
Let b satisfy 2^-b<=eta/8 and cap the failure count at J=2^d b. The
omitted tail changes a multiplier by at most 2r^J<=2^(1-b)<=eta/4,
since r^(2^d)<=exp(-1)<=1/2. This law has a finite sampler using at most
dJ fair bits: stop at the first all-zero d-bit block, or after J failures.
There are J+1 rational phases, and all inner cycle coins are fresh after
this outer sampler finishes. The generator selects a common dyadic delta
whose maximum branch synthesis error is <=eta/8 and a duration tolerance
costing <=eta/8. Thus all four error contributions total at most 3eta/4,
which is below the stated excess eta. Every bound is checked exactly
using rational arithmetic before a plan is returned.

For small eta, this explicit version has maximum phase O(log(1/eta)),
q=1/delta=O(eta^-1 log(1/eta)), maximum physical duration
O(eta^-2 log(1/eta)^3), maximum native segment count
O(eta^-3 log(1/eta)^4), and O(log(1/eta)) absolute timing bits. These
are resources to approach a constant error ceiling, not to approach zero.

## 4. Why a fixed higher-order native word cannot inherit a smooth-bath remainder

There is a separate, quantitative obstruction to a direct replacement of
the old high-regularity estimate by first-motion regularity. It concerns
one fixed finite normalized native word, with its global four-sign
variants and a common duration scale delta. It is not a lower bound for
all possible multiscale policies.

Let its normalized total duration be L, its real bounded waveforms be
f_A,f_B,f_C, with disjoint active supports and |f_j|<=1. Assume:

1. Every handle is balanced: integral_0^L f_j=0.
2. At a frozen bath the word has U_s^frozen=I+O(delta^3), for all four
   global even-sign choices. In particular its full second coefficient
   vanishes, as it does for flat commutator words of degree >=3.
3. Handle A is used nontrivially.

Define the primitive and its positive area

    F_A(x)=integral_0^x f_A(u)du,
    c_A=integral_0^L |F_A(x)|dx >0.

Choose the following **coin-independent admitted bath**, in the bare
mediator-qubit subcase:

    H_delta(t)=(1/2) r(t/delta) sigma_z,
    r(x)=sign(F_A(x)),               0<=t<=L delta.             (8)

Set sign(0)=0. For piecewise-constant finite words this bath is itself
piecewise constant with finitely many switches. It has
||[H_delta,sigma_j]||<=1, with no higher-regularity claim. It knows the
public policy and scale but no realized private signs. The task requires
uniformity over precisely such scale-dependent adversarial instances.

Let theta(x)=integral_0^x r. In the bath interaction frame,

    S_x(delta x)=X-delta theta(x)Y+O(delta^2),
    S_y(delta x)=Y+delta theta(x)X+O(delta^2),
    S_z(delta x)=Z.

Integration by parts uses F_A(0)=F_A(L)=0 and gives

    integral f_A theta = -integral F_A r = -c_A.

The first Dyson term therefore contains

    delta^2 s_A L_A,
    L_A=-i g_A c_A X1 tensor Y.                                (9)

The B term has the form delta^2 s_B L_B, with
L_B=+i g_B c_B X2 tensor X and
c_B=integral F_B(x)r(x)dx; C has no such term. All frozen second-order
terms vanish by assumption, while their bath-motion corrections are
O(delta^3). Thus

    U_s=I+delta^2 L_s+delta^3 M_s+delta^4 N_s+O(delta^5),
    L_s=s_A L_A+s_B L_B.                                       (10)

Use the maximally mixed mediator and a maximally entangled data-reference
state. For any desired clean comparison gate
G_delta=exp(-i beta delta^k F), k>=3, removing G_delta does not change
L_s. Let f_e be the resulting reduced-data entanglement fidelity. The
standard partial-trace formula here follows directly from the maximally
entangled input:

    f_e = (1/(d_D^2 d_M)) E_s
          Tr_M[(Tr_D U_s)^dagger (Tr_D U_s)],
    d_D=4, d_M=2.                                             (11)

Since Tr_D L_s=0, there is no quadratic contribution to (11) from that
partial trace. Unitarity in (10) gives

    M_s+M_s^dagger=0,
    N_s+N_s^dagger=-L_s^dagger L_s.

It follows, including sign averaging and Pauli orthogonality, that

    1-f_e = (g_A^2 c_A^2+g_B^2 c_B^2)delta^4+O(delta^5)
          >= c_A^2 delta^4+O(delta^5).                         (12)

Measuring the ideal data-reference Bell projector lower-bounds the full
trace norm by 2(1-f_e). Bath-only final evolution is already discarded
in (11). Hence the actual task's reduced-channel error in this one cycle
is at least 2c_A^2 delta^4+O(delta^5).

For completeness, this can be made an explicit finite-scale inequality.
If |beta|<=beta0, set

    r0=(6L+2 beta0+1)^(-1).

In normalized time the physical Hamiltonian has norm at most 5/2; the
interaction-frame correction contributes at most L/2. The holomorphic
extension of U_s therefore has norm <=exp(3L|z|). The corresponding
entanglement-fidelity series, with conjugate coefficients extended
holomorphically, has norm at most exp(6L|z|+2beta0|z|^k)<e on
|z|=r0. Cauchy's estimate bounds its remainder after degree four by
2e delta^5/r0^5 when delta<=r0/2. Thus

    error >= c_A^2 delta^4                                   (13)

whenever

    0<delta<=min(r0/2, c_A^2 r0^5/(4e)).

No pulse-size-dependent higher derivative bound is available: the bath
in (8) has bandwidth of order 1/delta, which the question explicitly
permits.

The exact checker constructs a 46-segment degree-five word by taking
two further commutators with A around the checkpoint's cubic word.
At a frozen bath it has

    U=I+16 i g_A^3 g_B g_C delta^5 F+O(delta^6).

Its first four coefficients vanish exactly for every global even-sign
variant. Nonetheless (13) supplies a strictly positive quartic reduced
channel error under (8). Its normalized A-area is printed by checks.py.
More specifically, c_A=65 and c_B=14. At unit gains the entanglement
infidelity coefficient in (12) is therefore 65^2+14^2=4421. The separate
8x8 diagnostic approaches this coefficient as delta decreases. For this
word one may take L=46, beta0=512 and r0=1/1301 in the explicit bound.
Therefore an asserted uniform remainder o(delta^4), and in particular
O(delta^6) or O(delta^7), for this fixed scale-dilated randomized word
would be false under the question's first-motion promise.

The same lower-order bath response is compatible with the successful
cubic primitive: N=O(delta^-3) times a quartic per-cycle error still
tends to zero. For k>=5, this quartic error destroys the *proposed
per-cycle higher-order estimate*. A per-cycle lower bound alone does
not imply a lower bound after arbitrary repeated coherent operations;
no such unjustified accumulation is claimed here.

## 5. Remaining scope

The two proved barriers leave a meaningful gap. Completed cubic phases
cannot compensate the gain product, and fixed high-order words cannot
simply import their higher-regularity remainder into this source class.
Neither theorem rules out a genuinely different native policy using
several scales, more intricate private correlations, or a new algebraic
extraction mechanism. A negative answer to the full question would need
a quantitative obstruction for all those policies. A positive answer
would need an operation outside the phase-only comparison class and a
uniform first-motion analysis of its actual channel.

All calculations use the frozen packet/checkpoint and the explicitly
supplied predecessor supplement. Polynomial gain compensation and native
sign projection were already present there; no novelty for those general
ideas is claimed. The new scope established here is the phase-channel
positivity barrier and the explicit first-motion quartic-noise witness.
