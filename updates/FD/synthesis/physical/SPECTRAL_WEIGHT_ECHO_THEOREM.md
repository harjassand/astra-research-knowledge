# Sharper local-reset echo certificate under the original assumptions

14 October 2026. Internal proof independently reconstructed by the physical
audit agent after the root/critic supplied the key maximal-eigenvector argument.
External correctness and historical priority UNKNOWN. Original source bytes
are preserved. This supersedes the intermediate product-norm proof in the same
folder; no product-decomposition assumption or extra physical operation is needed.

## Contract and theorem

Use the producer's exact contract. The finite host factors as S⊗O, dim(S)=d;
R=r⊗I is Hermitian, B=U†K1U-wI=K0+R, ||r||<=Rcap. All terms of K0 touching S
have summed operator norm at most J_S. Put Lambda=2J_S+Rcap and hbar=1. The
coherent comparison echo is E(t)=exp(iK0t)exp(-iBt). Before every trial reset S
to I/d; the outside tau is arbitrary and can depend on all preceding outcomes.
The producer proves the relative operator-norm remainder

    ||D(t)|| <= Lambda t² ||r||/2,
    D(t)=E(t)-I+itR.                                      (1)

For EVERY tau and 0<t<2/Lambda, the destructive-label probability obeys

    p_tau(t) >= c_new(t)||r||²,
    c_new(t)=t²(1-Lambda t/2)²/(4d).                       (2)

This replaces the producer's
c_old(t)=t²(1/sqrt(d)-Lambda t/2)²/4, valid only at
t<2/(Lambda sqrt(d)). At its optimum t*=1/Lambda, (2) gives

    p_tau(t*) >= ||r||²/(16 Lambda² d).                    (3)

The original theorem had denominator16 Lambda² d². Physical interrogation
time now depends on Lambda and is independent of d. The time1/Lambda must
still be available within the device's actual coherent-control bandwidth.

## Short proof

Let |v> be a normalized eigenvector of r with eigenvalue lambda satisfying
|lambda|=||r||. For every normalized outside |psi>, (1) and the reverse
triangle inequality give

    ||(E-I)|v psi>||
      >=t||R|v psi>||-||D(t)|v psi>||
      >=t(1-Lambda t/2)||r||.                             (4)

For rho=I/d⊗tau, decompose the collar identity in an eigenbasis of r and tau
in any spectral decomposition. The exact echo-failure expression is

    p_tau=Tr[rho(E-I)†(E-I)]/4.

Every term in that trace decomposition is nonnegative. Retaining the collar
eigenvector |v> term, with its weight1/d, and summing the outside decomposition
proves (2) from (4). Neither |v> nor tau needs to be known or prepared. The
maximally mixed reset already gives |v> its required weight. Optimizing the
quadratic t(1-Lambda t/2) gives t*=1/Lambda and (3). QED.

The derivative proof underlying (1) is unchanged:
E''(s)=exp(iK0s)([K0,R]-R²)exp(-iBs),
||[K0,R]||<=2J_S||r||, ||R²||<=Rcap||r||.
Common outside-only terms cancel from the commutator, even if interacting and
extensive. Integration proves (1); no outside mixing assumption is inserted.

## Conditional finite-sampling inference and costs

Assume each observed failure probability differs from ideal by at most gamma,
uniformly over outside states and past histories. Then

    Pr(Y_j=1|past)>=max(0,c_new(t)||r||²-gamma).

For a FIXED predeclared n, Bernoulli conditional-probability domination and
one-sided binomial-tail inversion give, with coverage at least1-alpha,

    radius=sqrt[(q_up+gamma)/c_new(t)],
    DeltaF_beta in [w-radius,w+radius] for ALL beta>0,

including the same ground-energy comparison. Intersect radius with Rcap and
add all required scalar-reference/model/sector uncertainties. Repeated
data-dependent candidate selection and optional stopping still require a
simultaneous confidence budget or a separately justified confidence sequence.

At t*=1/Lambda, zero failures and gamma=0 admit the sufficient count

    n=ceil[16 Lambda² d log(1/alpha)/epsilon²].             (5)

The apparatus-only floor is 4Lambda sqrt(d gamma). Thus both the shot cost and
the squared calibration burden improve by one factor of d. Since d=2^ell,
general collar scaling remains exponential. No promised sign determination or
finite successful runtime for arbitrary devices follows.

A rank-one residual with K0=0, r=delta|v><v| and no outside coupling has

    p(t)=sin²(delta t/2)/d.

For small delta t this is delta²t²/(4d). Therefore a dimension-independent
coefficient is impossible for this mixed-reset null protocol. Distinguishing
this alternative from the exact zero-failure null at fixed t requires order
d/(delta²t²) trials at fixed error; this statement concerns the specified
protocol, not arbitrary quantum algorithms with other legal preparations.

## Exact reanalysis of the retained-memory source record

The original source quantum-instrument trajectory propagated the same unreset
outside spin. It has n=100,000,000 and s=7 failures, and was inconclusive under
the original bound even with gamma=0. It remains SIMULATED data.

Keep its original coarse supplied inputs and time:

    J_S=779/100, Rcap=2, Lambda=879/50, d=8, t=1/50, w=1/5.

Now

    c_new=16982641/2000000000000
         =0.0000084913205.

Exact arithmetic proves that q=161/10^9 is a valid 99% one-sided endpoint:
the binomial lower tail at s=7 is bounded above by

    [sum_(j=0)^7 (nq/(1-q))^j/j!]
       /[sum_(j=0)^100 (nq)^j/j!] < 1/100.                 (6)

The numerator bounds the binomial polynomial and the denominator is below
exp(nq). For gamma=1/10^8, exact squaring gives radius<142/1000 and hence

    DeltaF_beta in [58/1000,342/1000].                     (7)

For gamma=1/10^7, radius<176/1000 gives [24/1000,376/1000]. Both exclude zero
on the conditional 99% event. The script verifies all constants and source
hashes; the decimal coefficient above is merely a displayed exact rational.
If a displayed constant and executable rational check disagree, the check
must fail rather than silently change the source record.

The favorable producer three-failure conditional-probability generator is
unnecessary for this reanalysis. No favorable trajectory was generated, no
laboratory experiment was conducted, and the required uniform apparatus-error
contract remains unverified on a physical device. Knowing the exact local
matrices makes direct residual evaluation cheaper than acquisition in this
synthetic fixture; matched total-resource advantage remains UNKNOWN.

## Precise scope of the advance

The previous need for Gibbs preparation is bypassed only for comparisons with
the declared useful coherent local witness. This does not solve N788/N790
equilibrium acquisition for generic thermal interventions; their hidden-sector
and rare-reference-weight obstructions have different legal access. N778/N779
channel comparisons can be strictly more general than a unitary witness, and
their acquisition gates are not closed by (2). A single weak echo at a long
unqualified time cannot establish (2); locality, coarse bounds and the finite
time restriction are essential.

The decisive next test is an independently specified interacting device with
an acquired compiled witness, calibrated support/norm bounds, uniform reset/
control/readout error and an independently measured comparison margin. Total
preparation/search/calibration/reset/readout costs must be compared with direct
equilibrium thermodynamics and equally informed Hamiltonian learning. The
new proof makes that test less demanding; it does not demonstrate it.
