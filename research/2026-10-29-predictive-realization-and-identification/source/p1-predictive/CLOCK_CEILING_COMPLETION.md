# Positive predictive completion with finite clock ceilings

29 October 2026, Brisbane. Root's next attack after the unrestricted-clock
transport theorem. Mathematical input is an exact calibrated oriented
mean record. This theorem pays a substantive execution constraint:
prescribed ceilings on native state-changing departure rates.

## 1. The exact criterion

Use the notation of `POSITIVE_PREDICTIVE_REALIZATION.md`: an irreducible
Eulerian port Laplacian S, positive port weights w_B, nonnegative hidden
loads v_R,v_L with equal total V>0, and scalar c. Let F_ij=-S_ij for
i!=j and d_i=sum_{j!=i}F_ij. Prescribe a finite positive hidden-state
rate ceiling Lambda and positive port ceilings ell_i. These are upper
bounds, not fixed native holding rates.

There is first an unavoidable port budget:

    a_i=w_B,i ell_i-d_i >= 0.                           (1)

Define T_a as the nonnegative transportation matrices with row sums v_R
and column sums v_L, off-diagonal support restricted to F_ij>0, and
M_ii=0 whenever a_i=0. Positive diagonal transport is otherwise allowed.

For x>=0, f>0, write u=Lambda*x/f and n=floor(u), and define

    psi_Lambda(x,f)=f(n+1)(2u-n)/Lambda^2
      =max_{n in {0,1,...}}
        [2(n+1)x/Lambda-n(n+1)f/Lambda^2].              (2)

Set psi(0,0)=0 and psi(x,0)=infinity for x>0. Let

    J_cap=min_{M in T_a} [sum_{i!=j}psi(M_ij,F_ij)
                         +sum_i psi(M_ii,a_i)].         (3)

**Theorem.** A finite irreducible CTMC realizes the exact mean record,
with every hidden departure rate <=Lambda and each port departure rate
<=ell_i, if and only if (1) holds, T_a is nonempty, and

    2c >= J_cap.                                       (4)

Equality is attainable. This differs from the strict free-clock
criterion 2c>J_*. For V=0, c must be zero and the port budgets still
apply; the direct chain suffices. Off-diagonal rates may be zero.

The optimization is an ordinary finite linear program in an epigraph
representation. Since 0<=M_ij<=V, only finitely many lines in (2) can
be active for each positive fixed f. A separation implementation can
add just the line indexed by floor(Lambda*M_ij/f) at each candidate.
There is no claim of a new LP algorithm or cost-free numerical precision.
The fully expanded LP can have many lines when a flow is small; this
finite formulation alone is not a polynomial bit-complexity result.

## 2. Why a clock ceiling creates this envelope

Uniformize the killed hidden process at rate Lambda. Conditional on its
embedded jump chain and terminal port, the duration sigma is a sum of N
independent exponential(Lambda) ticks. Tick durations are independent
of the embedded transitions, including virtual self transitions.
N is an integer >=0, with N=0 possible only for a direct port jump.
Therefore

    E sigma=E N/Lambda,
    E sigma^2=E[N(N+1)]/Lambda^2.                       (5)

The piecewise-linear convex interpolation of n(n+1), n=0,1,..., gives
the minimum second moment at a specified real E N=u. It is attained
by mixing N=n and N=n+1 with probabilities 1-(u-n), u-n.
Multiplying by endpoint flux f proves (2). This proof also covers
endpoint conditioning: the endpoint depends on the embedded chain,
not on its independent uniformization tick durations.

For a hidden self-return N>=1, so its actual flux f_i obeys
f_i<=Lambda*M_ii. The native port budget also gives f_i<=a_i. Since
psi(x,f) is nonincreasing in f at fixed x, its contribution is at least
psi(M_ii,a_i). This lower value is attainable with actual self-return
flux

    f_i=min(a_i,Lambda*M_ii).                           (6)

If a_i>Lambda*M_ii, both values lie in the n=0 or boundary n=1 part of
the envelope and equal 2M_ii/Lambda. Equation (6) avoids an instantaneous
self-jump. Using a_i itself as a self-return event flux in this case
would be an invalid CTMC construction.

The joint entrance/exit residence matrix of every actual source has the
required margins and support, as proved in the free-clock theorem.
Summing (5) gives 2c. This proves necessity of (1), T_a and (4).

## 3. Attaining the minimum with an actual finite CTMC

Choose an optimizer M in (3); compactness and continuity on the allowed
support guarantee existence. For each off-diagonal channel use total
event flux F_ij. For positive diagonal entries choose (6).

For any selected channel of flux f and occupation mass x, put
u=Lambda*x/f, n=floor(u), t=u-n. If n>=1, create n serial hidden phases
at rate Lambda. At the final phase, exit to the destination port with
probability 1-t or pass through one extra exponential(Lambda) phase
with probability t. Equivalently, split its outgoing stationary flow
into f(1-t) and ft. Each prefix phase has stationary weight f/Lambda;
the optional extra phase has weight ft/Lambda. The total is x.

For n=0 use a direct edge of flow f(1-t) and a single hidden exponential
branch of flow ft. This case occurs only off the diagonal. Delete zero
flow branches and zero weight states. The construction has at most n+1
hidden states per channel; it shares the Erlang prefix rather than
duplicating both complete serial branches.

Every hidden phase has departure rate Lambda. At each port the total
native departure flux is d_i+f_i<=w_B,i ell_i. Every hidden node is
balanced; the port graph's Eulerian flow balances its ports. The fixed
positive port weights and constructed hidden weights define Q by
dividing flows by source weights. Irreducibility follows from that of S.
The resulting S,b_R,b_L,w_B are exact and its scalar is J_cap/2.

## 4. Every larger scalar can also be attained without breaking ceilings

This step is needed: a lower envelope alone is not a sufficiency theorem.
Choose one positive-duration channel and increase its weighted second
moment by Delta=2c-J_cap, preserving all first-moment margins.

If it is off diagonal, keep its event flux f and mean mu=x/f. Its
baseline conditional second moment is q0=psi(x,f)/f. Choose a finite
D>max(mu,1/Lambda,(q0+Delta/f)/(2mu)). A distribution with direct-zero
probability 1-mu/D and an exponential of mean D with probability mu/D
has mean mu, second moment 2mu D, and hidden rate <=Lambda. Mix this
law with the baseline channel using the weight that makes the desired
second moment q0+Delta/f. Split the outgoing flux to implement the
mixture. Port flux f, total hidden mass x and endpoint remain unchanged.
The construction needs at most one additional hidden exponential branch.

If all positive residence is diagonal, select one such channel with
mass x>0 and desired weighted second moment q=psi(x,f)+Delta. Here
q>=2x/Lambda. Put

    z=Lambda*q/x, n=floor(z-1)>=1,
    f_new=Lambda*x*[2(n+1)-z]/[n(n+1)].                 (7)

Then Lambda*x/(n+1)<f_new<=Lambda*x/n, with the lower endpoint obtained
by an equivalent adjacent interval at ties. Direct substitution gives
psi(x,f_new)=q. The envelope is continuous and strictly decreasing in
f on 0<f<=Lambda*x, so f_new<=f<=a_i. Use the adjacent-Erlang channel
at this new flux. Its first moment times flux is still x, its native
port flux has decreased, and all hidden rates remain Lambda. The scalar
is now exact. All parameters and state counts are finite.

For rational data this adjustment uses rational numbers and an integer
floor; it does not require an irrational moment-calibration oracle.
It is a sufficient construction, not a minimum-state synthesis.

A more economical standard continuation is available for the diagonal
case, and should be preferred when reducing prepared state count matters.
Let f0=min(a,Lambda*x), C0=psi(x,a)/2 and C_E=x^2/f0. Mix the equality
law with an exponential of mean x/f0 to attain every C in [C0,C_E].
For C>=C_E use a single exponential with flow f=x^2/C and hidden rate
r=x/C. Then f<=a, r<=Lambda and the occupation mass is x. This avoids
the unnecessary growth in phase count of (7) at large c. This ordinary
phase-fitting improvement was supplied by the independent review in
`native_review/CLOCK_CEILING_INDEPENDENT_REVIEW.md`; it does not change
the network feasibility criterion.

### A common hidden rate is sufficient

The independent construction in
`acquisition_frontier/CLOCK_CEILING_REALIZABILITY_REVIEW.md` strengthens
existence: every feasible record can be realized with every hidden
departure rate exactly Lambda. Slower clocks can save states, but are
unnecessary for existence. The diagonal formula (7) already has this
property. Off diagonal, given conditional mean mu>0 and second moment
q>=psi(x,f)/f, put u=Lambda*mu, v=Lambda^2*q and

    k=floor(v/u)-1 >= 1,
    p_k=((k+2)u-v)/k,
    p_(k+1)=(v-(k+1)u)/(k+1),
    p_0=1-p_k-p_(k+1).

The first two probabilities are nonnegative by the choice of k. The
last is nonnegative because v is at least every supporting line
2(k+1)u-k(k+1). Their count N on {0,k,k+1} has EN=u and
E[N(N+1)]=v. Its positive components are Erlang channels at rate Lambda;
zero is a direct port jump. Zero-probability branches are omitted.
This can increase phase count and routing-probability precision costs.

## 5. Consequence and resource distinctions

`OPEN_MODULE_COMPLETION.md` proves the extension to directed modules
that carry boundary current. Individual modules need not be stationary
in isolation: their preserved port flow imbalance cancels only after
the unchanged cross-region flows are restored. Port budgets subtract
those cross flows as well as internal trace flow.

This completion preserves the oriented mean record exactly, so it
preserves every declared passive-context equilibrium mean and all
boundary-started mean fields. For whole-region transitions apply the
construction to each supplied separator record, keeping its c_j and
left population load separately. Neither full survival probabilities
nor arbitrary hidden preparations follow from these guarantees.

Rate ceilings apply to the prepared module. A subsequent exterior adds
its own outgoing flows at ports; its execution must fit the remaining
port budget. A mean-composition formula does not authorize exceeding a
hardware clock ceiling after attachment.

A useful universal consequence is

    c >= V/Lambda,

because N(N+1)>=2N. The full transportation LP is stronger: finite port
budgets can prevent the source and exit population margins from being
connected at all, or can raise the minimum scalar above V/Lambda.

In the two-port record with unit trace flow, v_R=(1,0),v_L=(0,1), and
c_n=(1+1/n)/2, port ceilings at least 1 are sufficient. The hidden-clock
criterion holds **exactly when Lambda>=n**. Thus this same family
requires at least n hidden states and a hidden clock ceiling at least n.
The original equilibrium mean is bounded, so neither obligation comes
from a huge mean lifetime. Rescaling all flows by 1/n moves the burden
to physical time and gives rate-1 witnesses, as recorded in the earlier
nonreversible note. A rescaling is not a free improvement at fixed time
calibration.

Fixed port ceilings remain substantive even as Lambda increases: the
diagonal cost approaches M_ii^2/a_i, not zero. Recovering the completely
free-clock criterion requires also freeing the relevant port flux
budgets. This distinguishes hidden phase clocks from native port clocks.

## 6. Executed constructive check

`clock_capped_transport.py` proposes transport optima using conventional
SciPy/HiGHS LP solves, adds violated envelope planes, and then checks
all primal constraints and the full implicit envelope with rational
arithmetic. It reconstructs rational duals, checks their signs and
reduced costs, and verifies exact equality of primal and dual values.
No floating optimizer status is accepted as a certificate by itself.

The saved run, `CLOCK_CAPPED_TRANSPORT_RESULTS.json`, certifies 11 LP
optima and two exact impossibility cases. Each feasible case builds the
full positive generator at equality, checks every rate ceiling and
stationary balance, eliminates its hidden states, and checks all
nonempty boundary-target means. There are 57 full killed-system mean
comparisons and 15 exact clock-threshold checks for the Erlang witness.
No random draws, source observations, or source preparations were used.

A directed three-port cycle with balanced hidden load (1,1,1), unit
trace flows, unit port weights and hidden ceiling 4 gives:

| Port rate ceiling | Exact minimum c | Hidden states in this construction |
|---|---:|---:|
| 1 | 15/8 | 12 |
| 2 | 9/8 | 12 |
| 5 | 3/4 | 3 |

These counts describe the explicit construction and are not asserted
to be minimum state counts. With port ceilings 1 and balanced load
(1,2,1), the same strongly connected trace graph has no feasible
transport: zero spare departure budget forbids every self-return.
This is a support failure, not failure of a numerical optimizer.

The prototype's exact rational reconstruction is an acceptance check,
not an algorithm guaranteed to recover certificates from every floating
LP output. It fails explicitly if reconstruction fails. Its complete
coefficients, duals, constructed generators and measured runtime are
preserved; runtime on these small supplied records is not a complexity
advantage over an equally informed conventional solver.

### Connection to information actually acquired in this branch

The earlier public 12-state representative already has an executable
clock certificate, checked in `native_excursions/certify_prepared_clocks.py`.
All its six hidden departure rates are <=1, and all its six port rates
are <=3/2. The largest port rate is approximately 1.34903243; the largest
hidden rate is approximately 0.85968840. These are certified bounds of
the prepared generator, not assertions about the unknown original source.

The generator was prepared from 6,291,456 recorded native excursions,
with the supplied reset/clock/tail/timestamp premises, and supports the
previously certified 12 source-union/target-union means. It has rational
coefficients up to 3184 numerator/denominator bits. The new rate check
reads only that frozen public representative, uses no new source
observations or preparations, and preserves its original uncertainty.
Its native port clocks differ from the source's supplied unit clocks.
No physical realization or rounding-stability experiment is claimed.

## 7. What has changed and what remains open

The free-clock theorem separated a finite sufficient record from positive
state complexity. The clock-constrained theorem further separates that
record from executable timing resources. The same incomplete excursion
information can be tested for exact compatibility with an explicit rate
budget by a finite convex calculation, then completed constructively.

The new ingredient claimed here is this stationary network feasibility
link, at the stated mean interface. Uniformization, integer convex
envelopes, adjacent Erlang phases and linear programming are conventional.
The scalar envelope has a particularly close published antecedent in
Bobbio, Horvath, Scarpa and Telek (2003), Section 4, Theorem 2, which
restates the discrete phase-type minimum-variance theorem attributed
there to Telek (2000). Its adjacent-count equality law becomes adjacent
Erlangs under uniformization. The off-diagonal zero-count case also
follows directly from (N-n)(N-n-1)>=0. This scalar result is not claimed
as new here. Exact primary reading scope and URLs are preserved in
`boundary_challenge/RATE_CAP_PRIMARY_COLLISION.md`.
The extension does not establish historical priority, a physical device,
an acquisition speedup, or a simulation advantage for evaluating means.
An equally informed boundary linear solver remains the strong baseline.

Acquisition is still separate. Resolved native excursion endpoints,
times and clock/tail calibration supplied the earlier reversible records.
Unknown rate ceilings, unknown separators, exact support zeros and
endpoint-duration correlations cannot be manufactured from this theorem.
Their certified acquisition under incomplete observations is a remaining
information problem; it has not been silently assumed solved.
