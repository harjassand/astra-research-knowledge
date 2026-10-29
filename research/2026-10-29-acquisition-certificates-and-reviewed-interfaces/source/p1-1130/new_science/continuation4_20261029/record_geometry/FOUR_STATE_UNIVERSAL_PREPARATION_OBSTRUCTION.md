# Exact visible-only preparation can require infinite mean even in four rapidly mixing states

29 October 2026. Astra P1, existing record-geometry complementary role.
Self-contained constructive obstruction; no priority claim.

## 1. Consequence

There is no universal visible-only stopping rule that exactly prepares a
nontrivial visible reweighting of the full microscopic law, from one warranted
stationary specimen, with finite expected native-call count, even for the
explicit four-state family below. Every native kernel is strictly positive,
reversible for the same known uniform microscopic law, and has a common
Doeblin constant. The impossibility is not a slow-mixing lower bound, a
conserved-sector mismatch, or uncertainty about the stationary masses.

More precisely, any one rule that is almost surely finite and exactly correct
for every member of this family has infinite expected length on the family's
independent-visible-bit sources. These sources have completely ordinary iid
visible records; their hidden bit still evolves.

The result concerns one unknown actual operation and a noninvasive visible
bit. It does not forbid finite-mean exact preparation with independent fresh
baseline trials, additional microscopic observations, a known kernel, or a
stronger structural interface. It also does not imply inefficient finite-
tolerance preparation. Section 7 gives a logarithmic-in-tolerance upper bound
for this same uniformly mixing family.

## 2. Interface and explicit family

The full microscopic state is x=(y,h) in {−1,+1}². Only y is observed. Let
mu be uniform on all four states, so the visible baseline mass is exactly
known to be one half. For 0<lambda<1/2, let

    P_0,lambda((y,h),(y',h')) = (1+lambda h h')/4.

This independently refreshes y to a fair sign at every call and evolves h
with one-step correlation lambda. Let S be the deterministic swap

    S(y,h)=(h,y),

and for 0<=delta<=1/4 define the actual native call

    P_delta,lambda=(1−delta)P_0,lambda+delta S.        (1)

The decomposition is a description of the hidden source. The controller is
not told which part occurred and cannot choose the parts separately.

Both P_0,lambda and S are symmetric stochastic matrices. Thus every (1) is
mu-reversible and has the same full stationary baseline. Every matrix entry
is at least

    (1−delta)(1−lambda)/4 >= 3/32.                    (2)

In particular P_delta,lambda(x,.) >= (3/8)mu(.) for every x. All four states
communicate, there are self transitions, and hidden memory mixes at a common
geometric rate. There are no distinct invariant sectors to reweight.

Fix any a in (−1,1)\{0}. The desired full law is

    nu(y,h) = (1+a y)/4.                            (3)

For arbitrary unequal positive binary weights W, this is their normalized
tilt with a=(W(+1)−W(−1))/(W(+1)+W(−1)). The target satisfies
E_nu Y=a and E_nu H=0.

A controller starts at X_0~mu, has independent auxiliary randomness whose
law does not encode delta or lambda, sees only Y_0,Y_1,..., and stops at an
adapted integer tau>=0. Its output is the actual state X_tau. Its stopping
decisions may use the entire observed prefix and unlimited computation or
randomization. Counting a calibration prefix in tau includes any learning
done on this same initially stationary specimen. Giving precomputed data
whose law depends on the unknown kernel is a different input interface.

Mandatory execution tau>=1 is a special case, not an escape.

## 3. The theorem

**Theorem.** Suppose the same controller is almost surely finite and has
Law_mu(X_tau)=nu for every delta in [0,1/4] and every lambda in (0,1/2).
Then E_mu tau=+infinity when delta=0, for every lambda in that interval.

At delta=0 the visible record is an iid fair-sign sequence for every lambda.
The controller therefore has exactly the same stopping-time distribution
for all those lambda. Assume for contradiction that its common mean is
finite, and denote its iid visible record by Y_0,Y_1,... .

For each l>=0 set

    c_l = E[1_{tau>=l+1} Y_{tau−l−1}].              (4)

These coefficients are absolutely summable:

    sum_l |c_l| <= sum_l P(tau>=l+1) = E tau < infinity.

The proof has two steps. Exactness forces every c_l to vanish. Optional
sampling instead makes their sum equal to −a.

## 4. Rare-swap coupling; no unjustified likelihood derivative

Realize (1) using independent Bernoulli(delta) selectors B_s at the native
steps s>=1. B_s=1 means swap; B_s=0 means P_0,lambda. Let s be the first
swap index. Before it, the hidden process is independent of all visible
refreshes and is a fair sign marginally. At the first swap, the new visible
value H_(s−1) is therefore a fresh fair sign independent of all earlier
visible values. After that swap, as long as there is no second swap, each
new visible value is another independent fair refresh.

Construct a reference iid visible sequence as follows: use the ordinary
visible refreshes except at the first swap, where its reference value is
the actual pre-swap hidden sign. At all subsequent swap indices, supply
fresh independent reference signs instead. Conditional on the complete
selector sequence, this reference sequence is iid fair. It is consequently
independent of the selector sequence. Use the same controller seed for the
actual and reference records.

Let tau denote the reference controller stopping time. Until the second
swap, actual and reference visible histories agree. If no second swap has
occurred by tau, the actual controller stops at that same time. All possible
disagreement is contained in the event B of at least two swaps by reference
time tau. Independence just established gives

    P(B) = E[1−(1−delta)^tau−tau delta(1−delta)^(tau−1)].

The bracket is zero at tau=0. For each fixed integer t, this expression
divided by delta tends to zero. It is bounded by t, because the chance of
at least two swaps is at most the chance of at least one, itself at most
delta t. Dominated convergence using E tau<infinity proves

    P(B)=o(delta).                                  (5)

On the no-swap event, the terminal hidden sign has mean zero conditional on
the reference visible stopping history. If exactly one swap occurs at step
s<=tau, it places Y_(s−1) into the hidden coordinate. With no later swaps,
its conditional terminal mean is lambda^(tau−s)Y_(s−1). Therefore

    E_delta,lambda H_(actual stop)
      = delta E[(1−delta)^(tau−1)
                 sum_(s=1)^tau lambda^(tau−s)Y_(s−1)] + R_delta,
    |R_delta| <= P(B)=o(delta).                     (6)

The expression with the sum is defined as zero when tau=0. This derivation
does not assume a second moment of tau, analytic stopped likelihoods, a
finite expected actual stopping time at delta>0, or a uniform tail bound.
The actual stopping time only needs to be almost surely finite there, so
its terminal hidden sign is defined and bounded.

Exactness requires the left side of (6) to be zero. Divide by delta and let
delta decrease to zero. The sum is bounded in absolute value by tau, so
dominated convergence yields

    A(lambda):=sum_(l>=0) c_l lambda^l = 0
                    for every lambda in (0,1/2).    (7)

The power series is absolutely convergent on the unit disk. Uniqueness of
power-series coefficients gives c_l=0 for every l. An elementary version
suffices here: let lambda decrease to zero in (7) to obtain c_0=0, divide
by lambda, repeat, and use convergence of the remaining series at each
stage. No source with lambda near one is part of the family or required by
the argument. The common fast-mixing bound (2) remains in force throughout.

## 5. Optional sampling contradiction

Because the reference visible signs Y_j, j>=1, are independent fair
increments and E tau<infinity,

    E[sum_(j=1)^tau Y_j]=0.

This follows directly by writing the sum as
sum_(j>=1) 1_{tau>=j}Y_j: the event {tau>=j} is decided before Y_j is read,
and absolute summability follows from E tau<infinity. Initial Y_0 and the
controller seed may be included in the initial filtration.

Consequently

    sum_l c_l
       = E[sum_(j=0)^(tau−1) Y_j]
       = E Y_0 − E Y_tau
       = −a.                                      (8)

The same identity holds on tau=0 paths. Equation (7) made every c_l zero,
contradicting a!=0. This proves the theorem.

### The obstruction has an entirely visible later-service witness

It is not necessary to demand direct access to the terminal hidden bit.
For this family,

    (P_delta,lambda Y)(y,h)=delta h.

The target (3) therefore has current visible mean a and mean zero after
one further actual native call. For delta>0, requiring that latter visible
mean to be zero forces E H_tau=0. The proof above consequently also rules
out a universal finite-mean preparation protocol that exactly matches just
these two visible means for every family member: the completion label and
one fresh later label. A claim about complete later records is stronger.

At delta=0 the hidden direction is invisible, but an arbitrarily small
unknown delta makes it predictively active. No microscopic measurement is
needed to state the failed service requirement.

## 6. What fails in the ordinary first-label proposal

An attractive proposal is to draw a desired visible sign D with mean a,
independently of the specimen, then wait until Y=D. It prepares the correct
visible marginal for every irreducible source and is finite mean on every
four-state kernel here. It need not prepare the correct hidden law.

For the iid visible source its expected count is one: with probability one
half the initial label already matches; otherwise the fair-label hitting
time has mean two. Its coefficients in (7) give

    A(lambda)=−a/(2−lambda),                        (9)

which is nonzero. Thus even an arbitrarily rare unobserved swap introduces
a hidden endpoint bias. The visible target remains correct. The executable
companion computes the exact finite-delta absorbing law as a check.

In fact, put b=delta/(2+delta−lambda). The ordinary first-label controller's
exact joint endpoint law is

    rho(y,h)=(1+a y)(1−b y h)/4.

Its total-variation error relative to (3) is b/2, its hidden mean is −ab,
and its mean native count is 1+delta²/[(1−delta)(2+delta−lambda)]. For
a=1/3, delta=1/8 and lambda=1/4, these give TV=1/30, hidden mean −1/45
and mean count 106/105. The exact endpoint vector in state order
(−,−),(−,+),(+,−),(+,+) is (7,8,16,14)/45.
One further native call has visible mean −a delta²/(2+delta−lambda),
which equals −1/360 in this fixture; the target reference mean is zero.

With full microscopic state observations, the situation changes. Classical
unknown finite-chain stationary stopping can recognize each microscopic
state and collect its exits. Applying such a method to a warranted
irreducible compiled kernel preserving nu is a legitimate ordinary
alternative. Its required microscopic state recognition is precisely what
the visible-only interface above does not supply.

Fresh independent baseline rejection is another legitimate escape. If every
trial really begins in mu conditional on the entire rejected history, accept
with probability W(Y)/max W. The successful full law is nu and the expected
number of baseline trials is max W/mu(W). Replacing a rejected specimen by
more correlated native calls does not provide that conditional baseline.
One initial baseline trial gives exact nu conditional on success, but its
failure branch does not complete unconditional preparation.

## 7. Finite tolerance is a different resource question

For a concrete comparison take W(−1)=1, W(+1)=2, so a=1/3. The preserved
binary excursion compiler with N=2 gives a kernel K with exact invariant nu.
Let A={Y=−1}, B={Y=+1}. Its blocks satisfy

    K_AA=P_AA²,  K_AB=P_AB+P_AA P_AB,
    K_BA=P_BA(I+P_AA)/2,
    K_BB=P_BB+P_BA P_AB/2.

Each native entry is at least c=3/32. Both A and B have two microscopic
states. Thus each entry of K is at least 2c²=9/512 (the AA block is the
smallest universal lower bound). Hence

    K(x,.) >= (9/128)mu(.).

The ordinary common-minorization coupling contracts total variation by at
most 119/128 per macro. From any initial law, including the warranted mu,

    TV(Law(X after n macros),nu) <= (119/128)^n.       (10)

Each macro uses at most two native calls. Finite error epsilon therefore
costs at most 2 ceil(log(epsilon)/log(119/128)) native calls, with the
appropriate zero-step convention. The phase selector is a fair bit and
every output remains the actual state.

This comparison is deliberately strong. The impossibility theorem is an
exact universal stopping boundary; it does not establish a practical
advantage for an infinite-mean exact controller over a finite-error program.
The uniform microscopic minorization used in (10) is a structural promise
of this explicit family, not an inference from its iid visible baseline.

## 8. Source relation and remaining scope

The stopped-occupation identity, unknown finite-chain stationary stopping,
and Palm/extra-head allocations are established primary predecessors.
PRIMARY_PREDECESSORS.md records what was actually inspected. The rare-swap
four-state construction and its proof above were developed here. A source
search has not established historical priority for this precise obstruction.

The theorem is stronger than merely exhibiting a slow source: all tested
kernels share the same explicit positive-entry lower bound and stationary
law. It does not say that any particular fully specified member has no
finite-mean exact stopping rule. It says one visible-only rule cannot
achieve both universal exactness over this unknown family and a finite mean
on their common iid-visible record. Extra actuator access, conditional
regeneration, full state identification or kernel-dependent input data can
change that boundary.
