# Boundary information that is complete for an equilibrium mean

29 October 2026, Brisbane. Root construction; ordinary mathematics, acquisition
obligations and conventional comparators. The previous acquired-record,
geometric and coarse-indicator results remain unchanged.

## Scientific choice

The larger question is what information can replace a system for a specified
consequence under later composition. A representation need not reproduce its
whole dynamics. The present consequence is a mean first-passage time from
equilibrium conditioned outside an absorbing set. The goal is a composable
information record, with a native acquisition route, whose sufficiency does
not assume a Markov law on coarse labels.

The comparison opening was a predictive-operation realization for arbitrary
legal quantum intervention programs. The alternative branch reads current
Astra N1148/N1166 and constructs a well-conditioned rank-three phase example
with an acquisition-depth/precision tradeoff. A short well-conditioned core
does not supply long-program precision. That is valuable information theory,
but the boundary route supplies the more immediate positive bridge here.

## 1. Exact task record

Let Q be an irreducible reversible finite continuous-time generator with
positive invariant weights w (not necessarily normalized), D=diag(w), and
L=-DQ. Partition vertices into nonempty resolved ports B and hidden interior
I. Every interior component must connect to B, so L_II is positive definite.
The words port and boundary refer to individually distinguished states, not
unresolved labels containing many entrance points. Define

    S = L_BB - L_BI L_II^{-1} L_IB,
    b = w_B - L_BI L_II^{-1} w_I,
    c = w_I^T L_II^{-1} w_I,
    W = sum(w) = sum(b).

S is a conductance Laplacian, b is positive and c is nonnegative. The retained
port weights w_B are also needed when targets may be arbitrary subsets of B.
All these quantities scale together with the arbitrary choice of scale for w.

For a nonempty A subset B, put R=B\A and suppose the remaining chain is
absorbed almost surely. Then

    T_A = [c + b_R^T (S_RR)^{-1} b_R] / [W - sum_{a in A} w_a].       (1)

The empty quadratic term is zero when R is empty. The denominator must be
positive. This is the mean from the true invariant distribution conditioned
outside A, not an arbitrary start or a physical equilibrium-preparation claim.

Proof. The killed Poisson equation is L_CC h=w_C, C=I union R. Eliminate I:
h_I=L_II^{-1}w_I-L_II^{-1}L_IR h_R and S_RR h_R=b_R. Substitution into
w_C^T h gives c+b_R^T S_RR^{-1}b_R. Divide by sum(w_C). Positivity follows
from the nonsingular M-matrix inverse. This is standard block elimination;
the task-complete record and its acquisition/substitution scope are the
objects developed here, not a claim to a new Schur identity.

For a fixed retained mass, the companion note proves that (S,b,c) is exactly
the information needed for equality of all means after arbitrary passive
external attachments and nonnegative external population loads. Two modules
may have different dynamical memory yet be indistinguishable for this whole
task family. It also proves cellwise composition for absorbing unions of
regions: every cross-region edge must have retained endpoints, and absorbed
regions are removed before assembling the surviving boundary problem.

## 2. Memory is compressed according to the consequence

The dynamic boundary response is

    K(z)=L_BB+zD_B-L_BI(L_II+zD_I)^{-1}L_IB.

The relevant contractions of its zero-frequency derivatives are exactly

    K(0)=S,  K'(0) 1=b,  -1^T K''(0) 1 / 2=c.                    (2)

This does not identify K(z) at other frequencies. It identifies the static
conductance, the redistributed population and an interior residence term.
The companion exact example has the same record but a different third
derivative and different survival law. A full dynamical memory kernel is
therefore excessive for this consequence, whereas static conductance alone
is insufficient.

For retained subsets A, the w_B entry is independently retained. For passive
attachments to a closed module, W=sum b and the normalization convention
must be consistent across components. Unknown relative module scales are
not supplied by an algebraic composition rule.

## 3. Native acquisition without an interior equilibrium sampler

At a resolved state i, the source is genuinely prepared at i. Observe its
native initial holding time (mean 1/lambda_i), its first jump, then run
uninterrupted until the next B hit. Let J be that endpoint and sigma be
the time spent away from B after the initial jump. A direct jump to another
port has sigma=0. Returning to i is allowed. The interface reports whether
the source is still outside B; an outside report is never a reset.

Write P_ij=Pr_i(J=j), u_i=E_i sigma, v_i=E_i sigma^2. The return chain P is
reversible and irreducible. Its stationary event vector s can be normalized
arbitrarily. From native data alone,

    w_i=s_i/lambda_i,
    S=diag(s)(I-P),
    b_i=s_i(1/lambda_i+u_i),
    c=(1/2) sum_i s_i v_i.                                    (3)

These are weights in a common arbitrary scale. The global stationary
normalizer and the hidden conditional equilibrium distribution need not
be acquired. Full boundary coordinates and state preparations still are
an access requirement. The acquisition proof in acquisition_frontier gives
the time-reversal/Poisson identities underlying (3).

The last equality is the decisive equilibrium-initialization correction.
Long excursions are overrepresented at a random stationary observation
time. A first-passage MEAN can thus depend on a SECOND excursion moment.
It is the familiar residual-life effect made into a complete reusable
boundary record, not a claim that renewal theory has a new identity.

Known lambda is a calibrated clock warranty. If lambda is unknown, native
holding-time data and their confidence intervals are additional acquisition.
The source dimension is not inferred or supplied to the consumer.

## 4. A simultaneous finite certificate

Suppose one confidence event supplies positive intervals for the event
weights s_i, holding means, first and second excursion moments, and each
undirected trace conductance -S_ij. Construct conductance Laplacians S_lo,
S_hi from the respective edge endpoints. Then S_lo <= S <= S_hi in
quadratic-form order. Let b_lo<=b<=b_hi and c_lo<=c<=c_hi componentwise.

For A subset B the denominator can be written without subtractive
cancellation:

    D_A = sum_{i notin A} s_i/lambda_i + sum_i s_i u_i.

With positive interval endpoints D_lo,D_hi, sound bounds are

    T_lo=[c_lo+b_lo,R^T (S_hi,RR)^{-1} b_lo,R]/D_hi,
    T_hi=[c_hi+b_hi,R^T (S_lo,RR)^{-1} b_hi,R]/D_lo.             (4)

Loewner inverse order controls S and the nonnegative M-matrix inverse
controls b. A singular lower grounded Laplacian or zero lower denominator
prevents a finite upper release. No spectral-gap estimate or claimed
rarity advantage is inserted. The same event covers every subsequent
choice of target set; simultaneous coverage follows from information
coverage, not from a union bound over target sets.

For modular composition the same comparison survives summing local edge
forms, loads and residence terms, and then grounding the chosen absorbed
regions. To obtain uniform relative precision, the acquired local boxes
must actually be sufficiently narrow. This theorem does not give that
precision from a count of moments.

## 5. Executed experiment and epistemic separation

The adjacent native_excursions files implement and consume an unknown
four-port source. The private generator has twelve states; the consumer
receives only four port names, counts, recorded durations, calibrated port
clock information and a supplied hidden-excursion tail envelope. The
hidden topology, state count, weights and rates are excluded from inference.

The finite acquisition uses a fixed censor horizon H and a supplied bound
Pr(sigma>t)<=exp(-gamma t). The endpoint missing mass is at most exp(-gamma H).
Missing first and squared moments are at most exp(-gamma H)/gamma and
2 exp(-gamma H)(H/gamma+1/gamma^2). Bounded-data concentration and a separately
charged timestamp allowance produce finite intervals. Native observations
are sampled rather than replaced by aggregate binomial outcomes.

This tail warranty is not learned from silence or a finite record. The
acquisition-frontier countermodels show why rare long excursions require
further information. The executable certificate is conditional on ideal
independent source trials and the stated sensor/clock/tail contracts;
pseudorandom software is a reproducible synthetic execution, not an
experiment on physical equipment.

## 6. Strong comparators and actual addition

Exact milestoning already retains first-hitting points and local time
information. MacKay--Robinson aggregation and ordinary stochastic/Schur
complementation already eliminate states while preserving relevant mean
quantities. A competent method supplied the same complete record can use
the same positive solve; no exclusive computational speedup is claimed.

The addition being established is a precise equivalence class for a family
of consequences under composition, its connection to contractions of
eliminated memory, and a native scale-free way to acquire it without an
interior equilibrium preparation. The second time moment supplies a
specific missing initial-residual contribution. Means for unions of
regions require retaining every cross-edge endpoint or an independently
justified further compression. An exponentially large physical boundary
has not been made small by renaming it.

Current primary sources and exact Astra source/correction receipts are
recorded separately. Initial literature already makes broad novelty claims
for elimination, milestoning or state reduction untenable. A narrower
historical priority claim for the complete theorem is not established.
