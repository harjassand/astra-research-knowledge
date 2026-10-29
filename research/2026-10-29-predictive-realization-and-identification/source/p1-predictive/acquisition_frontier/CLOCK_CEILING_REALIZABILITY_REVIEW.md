# Independent review: exact mean-record realization under rate ceilings

29 October 2026. This reviews the root's new rate-constrained characterization. No raw acquisition is re-audited and no source is sampled. Rates are real nonnegative CTMC transition rates, all state weights are positive, and absent edges may be zero. Port ceilings constrain the prepared module's actual departure rates; additional exterior attachments need their own remaining budget.

## 1. Result

Let the oriented record have irreducible Eulerian directed trace Laplacian S, retained weights w_B>0, hidden-load margins v_R,v_L>=0 of common total V>0, and c>0. Write F_ij=−S_ij for i≠j, d_i=sum_{j!=i}F_ij. Prescribe a hidden-state exit-rate ceiling Lambda>0 and port departure ceilings ell_i>0. Put

    a_i=w_B,i ell_i−d_i.

Require a_i>=0. The transport matrix M has row v_R, column v_L, and its usual support: all off-diagonals only where F_ij>0, plus diagonals only where a_i>0.

For x>=0,f>0 define u=Lambda*x/f, n=floor u, and

    psi(x,f)=f(n+1)(2u−n)/Lambda²
            =max_{n>=0}[2(n+1)x/Lambda−n(n+1)f/Lambda²].

For f=0 only x=0 is allowed, with cost zero. Define

    Jcap=min_M [sum_{i!=j}psi(M_ij,F_ij)
                         +sum_i psi(M_ii,a_i)].              (1)

Then the root's exact claim is sound:

    finite realization respecting both ceilings exists
    iff all a_i>=0, the constrained transport set is nonempty,
    and 2c>=Jcap.                                             (2)

Equality in (2) is attainable. For V=0, only c=0 is possible, and the core S alone works exactly when the port budgets are nonnegative. The free-clock strict threshold is therefore replaced by an attained, rate-dependent boundary.

## 2. Necessity by hidden uniformization

For an actual endpoint-conditioned excursion, uniformize the hidden CTMC at Lambda. Virtual self transitions are allowed in this proof; they are not physical port self jumps. The interior time has the form

    sigma=E_1+...+E_N,

where the E_r are independent exponential variables of rate Lambda, independent of the discrete uniformized path and its endpoint. Conditioning the endpoint affects N and the path, not the independent clock variables. Thus

    E sigma=E N/Lambda,
    E sigma²=E[N(N+1)]/Lambda².

For off-diagonal endpoints N may be zero because a direct port jump is legal. For a return to the same port N>=1: a genuine state-changing departure cannot immediately return without an interior hold.

The lower convex envelope of the integer values n(n+1) joins consecutive points. For any mean u>=0 it is g(u)=(n+1)(2u−n), n=floor u, achieved by N in {n,n+1}. Conditional Jensen gives a channel's weighted second moment at least psi(M_ij,Fall_ij).

The actual self-return flow f_i satisfies f_i<=a_i from the port ceiling. It also satisfies f_i<=Lambda M_ii because its conditional N is at least one. For fixed x, psi(x,f) is continuous and nonincreasing in f; on each segment its derivative in f is −n(n+1)/Lambda². Hence the actual self cost is at least psi(M_ii,a_i), even when a_i>Lambda M_ii. Summing all channel costs yields 2c>=Jcap, while endpoint support and the two margins give transport feasibility.

Useful identities are

    psi(x,f)=x²/f+x/Lambda
              +(f/Lambda²)theta(1−theta),
    theta=Lambda*x/f−floor(Lambda*x/f),
    psi(x,f)>=2x/Lambda.

In particular every such record satisfies c>=V/Lambda. The ceiling contributes information beyond the free-clock transport cost.

## 3. Attainment of the minimum without a zero-duration self return

The constrained transportation set is compact and psi is continuous, so a minimizer exists. For each positive diagonal M_ii choose the ACTUAL self flow

    f_i=min(a_i,Lambda M_ii).

If a_i>=Lambda M_ii, both psi(M_ii,a_i) and psi(M_ii,f_i) equal 2M_ii/Lambda. Otherwise f_i=a_i. Thus this choice attains the diagonal objective while ensuring its conditional mean is at least 1/Lambda. A zero diagonal mass gets no self channel.

For each positive-time channel with actual flow f, use conditional mean mu=M/f, u=Lambda mu, n=floor u. A mixture of Erlang-n and Erlang-(n+1), with probabilities 1−(u−n) and u−n, gives the minimum second moment. All hidden exit rates equal Lambda. When n=0 the zero component is a direct port jump and is allowed only off diagonal. Diagonal channels have u>=1, so no forbidden instantaneous self jump is introduced.

The Erlang alternatives may share their first n stages; the final stage routes either to the endpoint or through one extra exponential stage. Each phase's invariant weight is its flow divided by Lambda. Channel hidden mass is M. Diagonal channels preserve port flow balance by themselves, and the off-diagonal flow is balanced because S is Eulerian. The port's actual rate is (d_i+f_i)/w_B,i<=ell_i. Thus the resulting finite irreducible CTMC has exactly the requested S,w_B,v_R,v_L and c=Jcap/2.

## 4. Every larger residence scalar is reachable

Keep an optimizing M and select any positive-M channel, which exists since V>0. Add the entire required weighted second-moment excess 2c−Jcap to it. The constructions below prove there is no unattainable interval above the minimum.

### Off-diagonal channel, fixed flow

Let mu=M/F>0, q0=g(Lambda mu)/Lambda². If mu<1/Lambda, q0=2mu/Lambda. Every q>=q0 is achieved by a direct zero-duration branch and an exponential branch of mean d=q/(2mu), with branch probability p=mu/d. Then d>=1/Lambda and p<=1, so its rate is below the ceiling.

If mu>=1/Lambda, then q0<=2mu². For q between q0 and 2mu², mix the baseline Erlang law and an exponential of mean mu. Both have the same mean and obey the ceiling, so their second moments fill this entire interval. For q>=2mu² use the zero-plus-exponential construction above; now d>=mu>=1/Lambda. This proves the root's proposed intermediate calibration, including the small-mu case.

There is also a universal construction with all hidden rates EXACTLY Lambda. Put u=Lambda mu, v=Lambda²q, choose k=floor(v/u)−1>=1, and set

    p_k=((k+2)u−v)/k,
    p_(k+1)=(v−(k+1)u)/(k+1),
    p_0=1−p_k−p_(k+1).

The first two probabilities are nonnegative by the choice of k. The last is nonnegative because v>=g(u)>=2(k+1)u−k(k+1). Their integer-valued N has mean u and second factorial moment E[N(N+1)]=v. Erlang branches implement it. This may use more states than the preceding slower-clock mixture; it is an existence proof, not a state-optimal recommendation.

### Diagonal channel, adjustable self flow

Start with f0=min(a,Lambda M), mu0=M/f0>=1/Lambda and weighted minimum z0=psi(M,a). Mixing the baseline law with an exponential of mean mu0 fills every weighted second moment up to 2M²/f0 without changing flow. Above that value choose a single exponential with flow f=2M²/z<=f0 and mean M/f; its rate f/M<=Lambda. Decreasing this diagonal flow changes neither S nor the hidden mass M and only frees port rate budget.

An all-Lambda alternative is also exact. For any z>=z0, let r=Lambda z/M>=2, n=floor r−1, and

    f=[2(n+1)Lambda M−Lambda²z]/[n(n+1)].

Then Lambda M/(n+1)<=f<=Lambda M/n, f<=min(a,Lambda M), and psi(M,f)=z. The adjacent Erlang law has no zero-duration branch. This follows as well from continuity and strict decrease of psi(M,f) over 0<f<=Lambda M.

Both channel cases preserve all other record entries. Together with Section 3, they establish sufficiency of (2), including equality.

## 5. The finite LP is valid, but its expanded size has a cost

Each M entry is at most V. For an entry with fixed f>0, only supporting lines indexed 0<=n<=floor(Lambda V/f) are needed. Introduce one epigraph variable per allowed entry and impose those inequalities, the transport constraints and nonnegativity. This is a finite linear programme. Its expanded number of lines can be large when f is small; finiteness alone is not polynomial complexity in binary input length. Standard convex optimization or separation-oracle methods remain comparators. No numerical LP status is used as a proof in the exact controls below.

## 6. Exact finite controls

The adjacent checker verifies supporting-line/subgradient certificates, cap-respecting moment calibrations and full CTMC records.

A nontrivial two-port LP optimum uses F01=F10=1, Lambda=1, a0=a1=1/4, v_R=(2,1), v_L=(1,2). The transport variable y=M10 lies in [0,1]; M01=1+y and both diagonal entries equal 1−y. The objective is piecewise linear and is minimized at y=3/4:

    M=[[1/4,7/4],[3/4,1/4]], Jcap=15/2.

At the diagonal kink a subgradient of 3 is legal; off-diagonal slopes are 4 and 2. Row potentials (3,2), column potentials (0,1) certify global optimality. With w_B=(1,1), ell=(5/4,5/4), a seven-state realization attains c=15/4 exactly, all hidden rates one and both port rates 5/4. The checker independently eliminates it and checks the complete oriented record and target means.

A second example has the same off-diagonal flows, balanced hidden margins (1,1), but zero diagonal port budgets. The admissible M is entirely off diagonal, Jcap=4, and c=2 is realized with four states and all rates one. A leaf-only balanced realization would violate the port budgets; routing hidden residence through existing directed trace channels solves it.

These are supplied-record constructive controls, not acquired source experiments. Rate ceilings are honored by the prepared module; they are not claimed learned from a moment count. External attachments must preserve the relevant port-rate budget, and full laws, original clocks and arbitrary hidden interventions remain outside the mean-record equivalence claim.

Executed result: `check_clock_ceiling_realization.py` and
`CLOCK_CEILING_REALIZATION_CHECKS.json` pass 108 off-diagonal and 108
diagonal exact moment controls, including the root's explicit diagonal
flux formula. Seven independently built full generators have state counts
7, 8, 14, 4, 10, 11, 46. The last three have diagonal-only hidden residence
and test equality plus two positive excesses. Every hidden rate equals its
prescribed Lambda, every port obeys its ceiling, all directed stationary
balances and full Schur records agree, and all 21 nonempty port-target means
equal the corresponding full killed-system mean. The nontrivial LP optimum
15/2 has an exact global subgradient certificate; two support/port
impossibility controls are exact. All proof-relevant arithmetic uses
fractions. The measured local run took approximately 0.251 seconds; this is
neither a physical preparation cost nor an algorithmic advantage claim.

I also read the root's `CLOCK_CEILING_COMPLETION.md`. Its equation (7)
uses n=floor(z-1) with z=Lambda*q/x, which agrees exactly with the formula
above. Since z lies in [n+1,n+2), the claimed strict lower endpoint and
non-strict upper endpoint for f_new are correct, including integer ties.
The earlier lower bound q>=psi(x,f) and strict decrease of the envelope
on 0<f<=Lambda*x prove f_new<=f. No missing intermediate moment interval,
instantaneous self-return, or ceiling violation was found.
