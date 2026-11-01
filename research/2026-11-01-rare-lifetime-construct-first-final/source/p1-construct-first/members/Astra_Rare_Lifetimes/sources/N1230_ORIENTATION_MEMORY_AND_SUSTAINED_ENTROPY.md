# Stored orientation information can hide sustained dissipation

29 October 2026. Root construction following the entropy-completion and
metric-tree results. This is an identifiability theorem under a declared
physical-reversal class, not a low-heat implementation of an arbitrary
process. Physical heat claims require additional thermodynamic structure.

## 1. The new obstruction

For the all-even class, small stationary entropy forces finite path laws
close to equilibrium, yielding the complete tree-witness theory. For
arbitrary hidden parity, a stationary preparation can itself distinguish
forward from reversed paths. The sustained rate alone need not control
finite-window irreversibility.

**Theorem.** Let Q be any finite irreducible CTMC with n states, stationary
law pi, and deterministic finite-alphabet readout g. For every finite
horizon T, accuracy delta>0 and sustained-rate target eta>0, there exists
an irreducible 4n-state CTMC and a physical-reversal involution Theta such
that:

1. The readout is even: g(Theta z)=g(z).
2. Its stationary observed path law on [0,T] is within delta in total
   variation of the stationary observed path law of Q.
3. Its intrinsic stationary Theta-reversal divergence rate is below eta.
4. Every microscopic state has the SAME escape rate Lambda, where Lambda
   depends on Q but not on delta or eta.

The cost is not hidden dimension or an increasing maximum clock. The
stationary preparation's parity divergence can grow, and orientation
relaxation can become arbitrarily slow. Resolved singleton reset states
fixed by reversal, a known preparation-divergence bound, or an all-even
microscopic model are additional information that excludes the construction.

Consequently every finite-source coarse path law has robust sustained-
entropy floor zero in this unrestricted-parity/preparation class, even
when its observed law has a clear time arrow. This statement concerns
finite-window approximation. It does not assert a zero-rate irreducible
model that reproduces the full target path law exactly.

## 2. Two orientations of one source

Use row generators. The stationary adjoint has rates

    q*_(xy)=pi_y q_yx/pi_x,

the same stationary law pi, and the same escape rates lambda_x as Q.
Let epsilon in (0,1/2), alpha=1-epsilon, d=1-2epsilon, and kappa>0.
Make states (x,+),(x,-). Within + use Q; within - use Q*. At fixed x,
switch orientations at rates

    a=kappa epsilon  (+ to -),
    b=kappa alpha    (- to +).                              (1)

The stationary law is

    rho(x,+)=alpha pi_x,   rho(x,-)=epsilon pi_x.            (2)

Each orientation's internal traffic is stationary, and alpha a=epsilon b
balances switching traffic. The chain is irreducible. Set

    Theta(x,+)=(x,-),     readout(x,s)=g(x).

This is a mathematical physical-reversal contract. It is not inferred
from the source's readout and is not an available microscopic operation.

For a stationary finite generator L and involution Theta, its intrinsic
reversal-divergence rate is

    sigma=sum_z rho_z [sum_w!=z l_zw log(l_zw/l_Theta(w),Theta(z))
                                      +lambda_Theta(z)-lambda_z]. (3)

Along internal edges of +, reversed rates in - give logarithms
log(pi_y/pi_x); the corresponding statement holds in -. Their stationary
means vanish by stationarity. Each orientation-switch edge is its own
Theta-reversed edge, so its jump logarithm is zero. Paired total escape
rates differ by b-a. Therefore

    sigma_2n=kappa d^2.                                    (4)

The preparation divergence is independent of kappa:

    B=D(rho || rho Theta)=d log(alpha/epsilon).              (5)

For a stationary path window of length T the FULL microscopic divergence
is B+T sigma_2n. It would be incorrect to delete B when relating this
finite-window divergence to observable information.

## 3. Full observed-path approximation

Start the target Q process from pi. Couple it with the lifted process
whenever the latter starts in orientation +, using the same initial x and
all internal Q jumps. Until the first orientation switch, their complete
x paths, and hence all readouts, agree.

The + switching hazard a is independent of x. Thus the probability of
coupling failure is at most

    TV(P_lift[0,T],P_Q[0,T])
       <= epsilon+alpha(1-exp(-kappa epsilon T))
       <= epsilon+kappa epsilon T.                        (6)

The first TV can refer to the x path or any deterministic readout of it.
This is stronger than matching a few moments or sampled time points.
Finite observations on any grid, event counts and measurable bounded
path statistics are covered by the same contraction bound. Unbounded
consequences such as a mean first-passage time still require their own
integrability guarantee; path TV on a fixed horizon does not supply one.

## 4. Remove escape-clock asymmetry without increasing the rate ceiling

Choose a fixed c_0>0 in rate units and set

    Lambda=max_x lambda_x+c_0,
    c_x=Lambda-lambda_x >= c_0,
    0<kappa<c_0.

Duplicate each lifted state with a bit h in {0,1}. All preceding real
transitions preserve h. At (x,+,h), toggle h at rate c_x-a; at (x,-,h),
toggle at rate c_x-b. These rates are strictly positive. Every row now
has escape rate EXACTLY Lambda. The stationary bit is uniform, so the
stationary distribution is rho(x,s)/2. Set Theta(x,s,h)=(x,-s,h).

The projection forgetting h is strongly lumpable onto the 2n-state
process: every real aggregate transition has its original rate, independent
of h, and the bit transitions are invisible. Thus the full x path law and
the TV estimate (6) are unchanged, not merely approximately preserved.

All escape terms in (3) now vanish. Internal jump terms still telescope;
switch edges are still self-reversed. Only bit-toggle terms remain. Writing
u_x=c_x-kappa epsilon and v_x=c_x-kappa alpha gives

    sigma_4n=sum_x pi_x [alpha u_x log(u_x/v_x)
                                  +epsilon v_x log(v_x/u_x)]
             =sum_x pi_x d c_x log[(c_x-kappa epsilon)
                                      /(c_x-kappa alpha)].  (7)

Since log(u/v)<= (u-v)/v for u>=v>0,

    0<=sigma_4n
       <= kappa d^2 sum_x pi_x c_x/(c_x-kappa alpha)
       <= kappa d^2/(1-kappa/c_0).                         (8)

The preparation divergence remains exactly B in (5). The maximum rate
and every paired escape clock are fixed as accuracy improves. The
construction uses 4n states at every positive epsilon,kappa.

For a concrete choice with 0<delta<1, take epsilon=delta/2 and

    0<kappa<min(c_0/2, 1/T, eta/2).

Equations (6) and (8) give TV<delta and sigma_4n<eta (for T=0 omit 1/T).
Its preparation divergence is

    B=(1-delta)log[(2-delta)/delta] < log(2/delta).         (9)

This is a sufficient construction cost, not a universal optimal memory
cost. Orientation has an exact relaxation eigenvalue -kappa, so no
uniform relaxation or stationary-preparation time is supplied.

## 5. The robust inference consequence

Fix any finite list of observed time windows and any positive error
tolerances. Use their largest horizon and smallest tolerance in the
construction. Let eta tend to zero. Every such neighborhood of the target
record contains an irreducible finite model with arbitrarily small
intrinsic sustained entropy. Indeed the approximation is in full finite-
window path TV, stronger than the rational-cylinder topology used for
the tree hierarchy.

There can therefore be no universally valid positive lower bound on the
sustained rate that is lower-semicontinuous in this observation topology
for the unrestricted hidden-parity/preparation class. This is not a
statement that more observations never help. For each fixed lifted model,
sufficiently long observations can reveal switching. The failure is a
uniform inference claim over a class allowing indefinitely slow hidden
orientation relaxation and arbitrarily large preparation asymmetry.

For N independent stationary preparations, the joint record TV difference
is at most N times (6). Hence a finite statistical protocol can be made
arbitrarily unable to distinguish the source from a model with arbitrarily
small sustained entropy, unless it acquires or imposes an additional
physical/preparation restriction. Timing resolution alone does not remove
the obstruction: (6) already compares complete continuous-time paths.

The order of limits matters. Finite-window path convergence does not imply
convergence of the infinite-time KL rate. In the limiting construction,
the hidden orientation relaxation time diverges and the preparation
divergence grows; those are distinct from the bounded microscopic escape
clock and the fixed finite state count.

## 6. Stored and sustained irreversibility have different roles

For a stationary finite CTMC with involution Theta, the exact identity is

    D(P_hidden[0,T] || R_Theta P_hidden[0,T]) = B+T sigma,
    B=D(rho || rho Theta).                               (10)

If the observation is even and commutes with path reversal, data
processing gives

    D(P_obs[0,T] || R P_obs[0,T]) <= B+T sigma.            (11)

Thus observed finite-window irreversibility constrains a sum of stored
orientation information and sustained generation. It cannot in general
identify the sustained term without information about the boundary term.
The new fixed-state, fixed-clock construction shows that omitting that
information is not a harmless technicality.

If an independent physical argument or acquisition establishes B<=B_max,
then any valid lower bound I_T on the observed path divergence gives

    sigma >= max(0,(I_T-B_max)/T).                        (12)

Parity-symmetric stationary preparation has B=0. This is different from
all states being even, which supplies the stronger reversible-semigroup
geometry of the tree result. A supplied bound on B is also different from
knowing a resolved regenerative event interface.

At kappa=0, the 2n-state model is a stationary mixture of Q and Q*, with
weights alpha and epsilon. It has zero intrinsic rate and boundary B,
but is reducible. If the two stationary observed path measures become
mutually distinguishable at long times (for example, the full x readout
has a nonzero ergodic current separating Q from Q*), the observed path
divergence of this mixture tends to B. The observation eventually learns
which fixed orientation was prepared; it need not learn an entropy
generation rate. For positive kappa, the finite model is irreducible and
pays the small rate in (4) or (7). The main theorem uses only these
positive-kappa models.

For an irreducible finite model, exact zero intrinsic rate forces equality
with its stationary Theta-reversed generator. Uniqueness of the stationary
law then forces rho=rho Theta and B=0. The theorem therefore asserts an
infimum in a finite-accuracy class, not an attained nonreversible zero-rate
irreducible source.

## 7. Why the native-event entropy floor survives

The resolved native interface in `ENTROPY_COMPLETION_CONVERSE.md` supplies
singleton microscopic ports fixed under Theta, their holding clocks and
stationary flux normalization. Every return to such a port is a true
Markov renewal state. Excursion-flux reversal KL equals the intrinsic
entropy, with endpoint weights cancelling by traffic balance. This gives
the nonzero robust floor J when the native law is irreversible.

The present lift has TWO orientations under every visible configuration.
No visible symbol is a singleton microscopic reset fixed under Theta.
Revisiting that symbol does not remove its hidden orientation memory.
Treating a visible return as a native reset would change the declared
interface and falsely identify coarse events with regenerative events.

Even an injective readout on the original source Q does not certify that
there is no hidden orientation in an alternative explanation. If the
physical interface actually certifies complete microscopic configurations,
or an even singleton reset, the alternative lift is inadmissible. That
extra information is precisely what the two theorems distinguish.

## 8. Resource and physical interpretation ledger

The constructive inputs are Q and pi, from which Q* can be calculated.
They are supplied for the existence proof. A passive coarse record does
not acquire them or prepare either copy. This is an impossibility result
for inference over compatible models, not a procedure that identifies
the native system or operates a new device.

The explicit model uses 2n states, or 4n for equal fixed escape clocks.
It needs the stationary orientation population (alpha,epsilon), a uniform
bit in the 4n version, and switch rates as small as kappa epsilon. The
maximum rate remains Lambda, but the minimum relevant rate and spectral
gap can tend to zero. Realization precision and the time or work needed
to prepare the stationary population have not been obtained for free.
The mathematical B is measured in nats of parity distinguishability; it
is not automatically a heat or work cost.

In particular, relative entropy of the orientation distribution to an
unbiased orientation is

    alpha log(2alpha)+epsilon log(2epsilon)
                  =log 2-H_binary(epsilon) <= log 2,

while B diverges. The construction uses one orientation bit, not an
unbounded number of stored bits. A bound on state count or on relative
entropy to this unbiased reference does not supply a bound on B. Any
interpretation of that reference divergence as preparation free energy
needs an independently justified equilibrium energy model. Likewise,
the exact -kappa relaxation mode is not a lower bound on the time of
every possible externally assisted preparation protocol.

The construction remains within a path-reversal divergence model class.
To interpret sigma as a physical entropy-production or heat rate, one
must know the actual reversal, relevant odd external fields, reservoir
model and local detailed balance. The theorem does not supply a physical
source class realizing every arbitrary Q lift under those stricter
requirements. A known thermodynamic class may exclude these completions
and support stronger inference.

An equally informed existing route can of course build Q*, add a slowly
switching orientation and uniformize with hidden null transitions. These
ingredients are not claimed new. The substantive addition under review
is the universal fixed-state/fixed-clock construction with its exact
entropy, preparation and path-TV accounting, and the resulting separation
between coarse passive records, resolved regenerative access, and
physically constrained hidden explanations. Historical priority is not
established.

Companion executable controls and the independent review are in
`orientation_memory/`. No trajectories, physical preparations or equipment
operations were acquired in this continuation.

## 9. A certified memory-erasure condition restores a rate bound

The failure suggests a different sufficient input from a bound on B.
One can bound how slowly the PHYSICALLY REVERSED hidden dynamics forgets
its initial state. This remains a substantive mathematical/physical input,
not something acquired from a few visible correlation times.

Let L be a finite irreducible generator with stationary rho, and let
R=Theta L* Theta, where L* is the rho-stationary adjoint. R has stationary
rhoTheta. Define the Dobrushin coefficient beta(t) of exp(tR) as the
largest TV distance between two of its rows. Suppose a certified bound
beta(t)<=beta<1 is supplied at a known t>0.

The same-initial-law path divergence is

    D(P_L^rho[0,t] || P_R^rho[0,t])=t sigma.              (13)

The rates of R introduce a log(rhoTheta) gradient into the likelihood
ratio; its stationary mean under L is zero, leaving exactly the intrinsic
rate. Endpoint data processing and Pinsker give

    TV(rho,rho exp(tR)) <= sqrt(t sigma/2).

Put d_0=TV(rho,rhoTheta). Stationarity of rhoTheta for R and contraction
give d_0<=sqrt(t sigma/2)+beta d_0, hence

    d_0<=sqrt(t sigma/2)/(1-beta).                         (14)

On an observation window of length T, compare the L law first with the
R law having the SAME initial rho, and then change the latter initial law
to rhoTheta. The first comparison costs at most sqrt(T sigma/2); the
second costs at most d_0. The final law is the physical reversal of the
stationary L path law. For an even readout, if

    Delta_T=TV(P_obs[0,T],R P_obs[0,T]),

then

    sigma >= 2 Delta_T^2 /
                    [sqrt(T)+sqrt(t)/(1-beta)]^2.         (15)

A certified lower bound on Delta_T can be used instead. For example, an
algebraically reversal-odd statistic f with |f|<=1 has
Delta_T>=|E f|, which can be validated from independent stationary path
records with ordinary bounded-score concentration. An irregular sampled
grid must include its reflected grid to evaluate reversal consistently.

The orientation construction has an exact -kappa relaxation mode, so
its reversed kernel has beta(t)>=exp(-kappa t). A fixed nontrivial bound
beta<1 at fixed t therefore excludes the kappa-to-zero shielding limit.
Neither a fixed number of states nor an upper escape-clock ceiling gives
this bound. A genuine lower-rate, minorization, or physical forgetting
argument would have to supply it.

Equation (15) is a qualified recovery lemma built from standard path-KL
perturbation, Pinsker and Dobrushin contraction. It does not acquire R,
provide a reverse operation, prove a speedup, or identify a native
thermodynamic class. Its purpose is to show precisely which missing
memory information can change the conclusion after the counterexample.

The SAME bound follows from a supplied Dobrushin contraction for the
FORWARD hidden kernel exp(tL). Indeed physical path reversal is an
involution, so the stationary path divergences and their intrinsic rates
are equal for L and R. Apply (13)--(14) with their roles interchanged.
This alternative needs no operation implementing R, but still requires
a quantitative uniform hidden contraction premise, not visible correlation
decay. The ordinary independent review is
`entropy_completion_review/MEMORY_ERASURE_RECOVERY_REVIEW.md`.

## 10. Primary antecedents and proposed addition

Kim, Lee and Jeong, Physical Review Research 4, 023051 (2022),
https://arxiv.org/pdf/2112.04681, already separates the stationary parity
boundary from additive entropy in equations (3)--(14). Its Section III
contains the oriented ring with arbitrary sign-switch rates; our 2n
construction specializes exactly to that model for a uniform directed
cycle. The boundary correction and orientation-sign mechanism are not
new discoveries of this continuation.

Andrieu and Livingstone, Annals of Statistics 49 (2021), DOI
10.1214/20-AOS2008, Section 3.3, supplies adjoint sign lifting and switching
as sampler machinery. Degunther, van der Meer and Seifert, Physical Review
Research 6, 023175 (2024), explains the physical additive boundary
distinction for odd variables. The detailed primary comparison and current
memory-aware inference comparator are in
`orientation_memory/ORIENTATION_LITERATURE_REVIEW.md` and its source receipt.

The proposed addition is the arbitrary-source quantitative completion,
the 4n common-clock construction, and its universal finite-record inference
consequence with the remaining preparation and memory resources exposed.
No direct prior statement of that combined theorem was found in the
bounded primary reading; historical priority remains unestablished.
