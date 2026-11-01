# A constructive common-seed support theorem via sampled core events

**Ordinary proof; independent full-source receipt governs review status.** Pure mathematical CTMC research. This
file is separate from the accepted inverse-mass package and is not included in it.

## 1. Statement and raw conditions

Let n>=2. The only nonconservative reactions are `0->A` and `A->0`, with rates
lambda,mu>0. Every other nonnull channel conserves total count and contains at least
one A in both its source and target. Strip one common A from each such channel;
call the resulting conservative network Q on coordinates `(r,B_1,...,B_(n-1))`.
Let p>=2 be its maximum source molecularity. Rates are unchanged; propensities use
falling factorials without implicit combinatorial divisors. Assume:

1. The full raw network is weakly reversible.
2. Using **only order-p channels of Q**, forward support closure from every singleton
   contains r. Forward closure repeatedly adds product species of a channel whose
   entire source support is already present.

**Theorem.** Every communicating class of the full CTMC is closed and
positive recurrent. Every stationary probability has every finite exponential
total-count moment. For rational raw rates, finite raw recognition/support witnesses
acquire the qualitative conclusion. Explicit scalar rational calculations acquire
sampled-core Foster constants and a continuous-time stationary moment bound, without
enumerating fibers, finding a stationary fiber distribution, or materializing a
polynomial corrector. Numerical scalar powers can nevertheless be enormous and their
cost is charged separately. No claim of general weak reversibility or completeness
of this sufficient structural condition is made.

This includes arbitrary dimension, multiple internal linkage classes, arbitrary
stripped top degree p>=2, arbitrary positive rates, and lower-order conservative
channels. It includes the previously reviewed mediated cubic lift and the opposing
pure-ray lift that has **no inverse-linear mass profile**. The method uses an ordinary
time change, a quantitative finite-time fluid approximation, and an embedded-chain
Foster argument. Its conclusion is not inferred from generic fluid stability.

## 2. Exact common-seed time change

On A>=1 set `r=A-1`, y=(r,B), and M=sum y=N-1. For a stripped source u,

    (A)_(u_A+1)=A(A-1)_(u_A).

Thus the internal generator is exactly `A Q`, not an asymptotic approximation.
Internal jumps preserve A>=1. At A=0 all internal propensities vanish.

During a seeded interval, use the operational time `d tau=A dt`. In tau time:

* the internal process has generator Q on its fixed mass-M fiber;
* A death has constant rate mu, including death of the last A at r=0;
* immigration has rate `lambda/(1+r)`.

Until the first core (immigration/death) event, construct an unrestricted Q chain
`Y_tau` on the finite mass-M fiber, independent of `D~Exp(mu)`. An independent unit
exponential threshold applied to the cumulative hazard
`integral lambda/(1+(Y_s)_r) ds` defines a potential immigration time I. Up to min(I,D)
this is exactly the time-changed full process. This counterfactual unrestricted chain
is used only to bound the first-event probabilities; no path after an actual core
event is incorrectly kept on the old fiber.

## 3. Raw support earns a uniform finite-time activation bound

Write `S=sum all stripped rates`, `k_min=min order-p rates`, and

    C=max(1,p^3 S),             T=1/(4C).

On the unit simplex Delta, the top homogeneous vector field is

    v(z)=sum_(|u|=p) kappa z^u (v_target-u).

It preserves Delta. In the infinity norm, with induced row-sum Jacobian norm,

    v_i(z)>=-C z_i,       ||Dv(z)||_infinity<=C.        (1)

Indeed negative i-increments require u_i>=1, so their monomials contain z_i;
|stoichiometric increment|<=p, and the sum of differentiated monomial degrees is p.
The polynomial ODE has a unique global solution on compact Delta.

Define rational levels

    ell_0=3/(4n),
    ell_(j+1)=min(ell_j, T k_min ell_j^p/(4n)),
    delta=ell_n>0.                                    (2)

For every initial z in Delta, some species has count fraction at least 1/n. Its
coordinate stays at least ell_0 throughout [0,T], since `exp(-CT)>=1-CT=3/4`.
Choose its finite support witness to r, which uses at most n-1 support-enlarging
reactions, and divide [0,T] into n equal blocks. Once every source species of the
next witness channel is bounded below by ell_j, its production of each newly added
species is at least k_min ell_j^p. Variation of constants using (1) gives at least
`(T/n) k_min ell_j^p (3/4)` at the block end. Future decay retains at least another
factor 3/4. Formula (2), with 1/4 instead of 9/16, is conservative. Previously
established lower bounds remain valid. Padding unused stages only decreases delta.
Consequently

    (phi_T(z))_r >= delta for every z in Delta.        (3)

This is a finite raw support calculation, not an assumed positive equilibrium,
persistence theorem, or compactness-only existence of an activation constant.

## 4. Uniform finite-fiber martingale estimate with explicit constants

Let the unrestricted Q chain have integer mass M>=p. Normalize

    Z_s=Y_(s/M^(p-1))/M,            0<=s<=T.

Its drift is

    b_M(z)=sum_channels kappa nu (Mz)_u/M^p.

For an integer mass-M state and q=|u|<=p,

    |(Mz)_u-(Mz)^u| <= q(q-1) M^(q-1)/2.              (4)

One proof expands a telescoping product replacing each factor `x_i-j` by x_i.
When M>=p, every factor's absolute value is at most M, including any factors after
a zero factor; the sum of offsets is at most q(q-1)/2. This also treats disabled
falling-factorial sources without evaluating negative propensities.

For leading channels use (4); lower-degree channels contribute at most
`kappa p/M` to each drift coordinate. The generous C above therefore gives

    ||b_M(z)-v(z)||_infinity <= C/M.                  (5)

Write the compensated jump martingale as J_s, so
`Z_s=Z_0+integral_0^s b_M(Z_u)du+J_s`. A coordinate jump is nu_i/M and its scaled rate
is `M^(1-p) kappa(Y)_u`. Thus

    E <J_i>_T <= CT/M.                               (6)

All statements are on a finite fiber, so martingales are square-integrable without
stationarity assumptions. Doob's inequality and a union bound give

    P(max_i sup_(s<=T)|J_i(s)| > delta/4)
          <= 64 n C T/(M delta^2).                  (7)

Gronwall, (1) and (5) imply

    sup_(s<=T)||Z_s-phi_s(Z_0)||_infinity
       <= exp(CT)[max_i sup|J_i|+CT/M].

Since `exp(1/4)<=4/3`, if

    M>=M0:=max(p,ceil(8CT/delta)),

then on the complementary event in (7) the error is at most delta/2. Combining with
(3), and setting

    K0=64 n C T/delta^2,    w_M=T/M^(p-1),

we obtain the **uniform** bound

    P_y((Y_(w_M))_r < delta M/2) <= K0/M              (8)

for every state y on the mass-M fiber. The right side need not be less than one for
small M; the inequality is still valid, and the eventual Foster threshold is larger.

For every s>=w_M, condition on the state at s-w_M and apply (8) over the final window.
No mixing time or invariant fiber law is involved. With `K=K0+2/delta`, this proves

    E_y[1/(1+(Y_s)_r)] <= K/M,
    P_y((Y_s)_r=0) <= K/M,               s>=w_M.       (9)

## 5. First-event probabilities: both immigration and failed seed are paid

For M>=M0, the exact potential-event construction in Section 2 gives

    p_up=P(I<D)
      <=lambda integral_0^infinity exp(-mu s)
                     E[1/(1+(Y_s)_r)] ds
      <=lambda[T+K/mu]/M.                           (10)

In the initial window use the bound one. Its length is
`w_M=T/M^(p-1)<=T/M`, where p>=2 is essential to this displayed bound. Similarly,

    p_loss=P(D<I and (Y_D)_r=0)
          <=mu integral_0^infinity exp(-mu s)P((Y_s)_r=0)ds
          <=[mu T+K]/M.                             (11)

Let

    a=(lambda+mu)T+K(1+lambda/mu).

Then `p_up+p_loss<=a/M`. The seed can die; its probability is not set to zero and
the return cost is not omitted. A subsequent seed-restoring immigration will be
bundled into the sampled transition below.

## 6. Acquired sampled-core drift

Starting from a seeded state A>=1, observe the process until its first core event.
If immigration occurs, record that state. If death occurs with A>=2, record its
seeded target. If death kills the last A, wait at A=0 until the next immigration
(the only enabled channel), and record the re-seeded state. Repeat. This defines
a Markov chain Z_k on seeded states, with kernel P. Its total count changes by

    +1 with probability p_up;
    -1 with probability 1-p_up-p_loss;
     0 with probability p_loss.

The zero case includes the forced restoring immigration exactly once. It does not
silently turn that immigration into a negative-count transition.

For any rational t>1, V=t^N satisfies

    P V/V <= t^(-1)+(t-t^(-1))a/M,   M=N-1>=M0.       (12)

Put

    rho=(1+t^(-1))/2,
    M_cut=max(1,M0,ceil(2a(t+1))),
    B=(t-rho)t^M_cut.

The identity `(t-t^(-1))/(1-t^(-1))=t+1` shows contraction by rho for N>=M_cut+1.
At every other seeded state N<=M_cut, count increases by at most one, so `PV<=tV`.
Therefore

    P V <= rho V+B 1_(N<=M_cut).                     (13)

The head has `binomial(M_cut+n-1,n)` seeded states on the full lattice, obtained
by summing compositions of N-1 for N=1,...,M_cut. This state count can be retained
symbolically; **no head or fiber is enumerated**. The Foster constant B is likewise
kept as a prefactor and a power, not expanded if its output would be enormous.

## 7. Closed classes and discrete-chain recurrence

Only immigration increases N in physical time, so `N(s)<=N(0)+Pois(lambda s)`.
Finite count sublevels have finite state spaces and bounded finite rates; this proves
nonexplosion of the full CTMC independently of (13). Core observation times cannot
accumulate in finite physical time.

Weak reversibility makes every full-chain communicating class closed: translate a
complex-graph return path by the nonnegative surplus population. Every class meets
the seeded states because A-zero states have positive-rate immigration.

The seeded states in each such full class communicate under P. Take a finite enabled
full reaction path between two seeded states and group it at core events. Any visit
to A=0 is followed necessarily by immigration, exactly matching the bundled rule.
If the path ends in an internal-only segment, append immigration and then death,
returning to that desired seeded endpoint. Every prescribed finite segment has
positive probability before any unwanted reaction. Thus P has the same class
partition on seeded states and each class is closed.

Ordinary discrete Foster theory applied to (13) makes each such class positive
recurrent and yields its unique stationary law pi_e. For completeness, iteration
gives `P^k V<=rho^k V+B/(1-rho)`; V is normlike, so empirical laws are tight and a
subsequential invariant law exists. Finite-support test functions pass under weak
convergence on this discrete space; the Markov operator of a bounded function is
bounded. Irreducibility gives positive recurrence and uniqueness. Fatou gives

    pi_e(t^N) <= L_t:=B/(1-rho).                     (14)

One may equivalently integrate truncated concave functions of V to obtain (14)
without assuming its integrability. The construction is repeated for every rational
t>1, always for the same sampled kernel P and unique classwise pi_e. Thus pi_e has
every finite exponential moment, not just one selected exponent.

## 8. Exact physical holding and stationary occupation transfer

Let H_x be one bundled cycle's physical duration from a seeded state x. Before the
first core event, A>=1 and physical time is `integral d tau/A<=tau`. Since that event
occurs by the independent tau death clock D,

    E_x H_x <= 1/mu+1/lambda=:H.                    (15)

The second term pays a possible last-copy death followed by the A-zero waiting time.
It is an upper bound, not an assertion that the two waits are independent or always
both incurred. Before the first core event, physical total core hazard is at most
lambda+mu N, because N is fixed and A<=N. Hence

    E_x H_x >=1/(lambda+mu N).                      (16)

Within the seeded portion, total count is the starting N. In the possible A-zero
portion it is N-1. A terminal immigration changes N only at the endpoint, a set of
zero duration. Thus

    E_x integral_0^H_x t^(N(s)) ds <= t^N E_x H_x.    (17)

For a classwise sampled stationary law pi_e, define the occupation law

    pi_c(f)= E_pi_e integral_0^H_x f(X_s)ds / E_pi_e H_x.

The denominator is finite by (15) and strictly positive. The usual cycle Dynkin
identity shows pi_c is stationary: for finitely supported f, Lf is bounded and the
stopped identity is integrable by (15); its endpoint expectation vanishes because
pi_e is P-invariant. Exit-rate integrability also holds: during a cycle the total
rate is bounded by a network-dependent polynomial in starting N, and pi_e has an
exponential moment, while the conditional mean holding time is bounded by H.
Thus the infinitesimal stationarity identity defines an invariant probability for
the nonexplosive CTMC. It is supported on the corresponding irreducible full class,
so that class is positive recurrent and this invariant law is unique.

Jensen applied to (16), (14), and `N<=(t^N-1)/(t-1)` give the explicit bound

    E_pi_e H_x >=1/[lambda+mu(L_t-1)/(t-1)],

    pi_c(t^N) <= H L_t [lambda+mu(L_t-1)/(t-1)].       (18)

Every quantity on the right is acquired from raw rational data and t, although
powers may remain factored. Repeat t over positive rational bases and dominate any
real `exp(theta N)` by a larger such t^N. Global thresholds are uniform over classes;
each class intersects a fixed finite V sublevel, so only finitely many classes occur.
Stationary mixtures therefore retain all these finite moments and uniform bounds.

## 9. What is gained over the inverse-linear receiver

For the opposing-ray lift

    0 <-> A,
    A+2B <-> A+B+C <-> A+2C,
    A+B+C <-> 2A+B,

pure B support creates C and then r; pure C support creates B and then r. The raw
top support test succeeds. No inverse-linear profile `R=A+w_B B+w_C C` can satisfy
the preceding certificate's pure-source signs: one requires w_C>w_B, the other
w_B>w_C. The present construction does not ask for that impossible profile. It uses
finite raw support witnesses and uniform stochastic activation at a sampled core
boundary. Setting `A+B+C->A+2C` to rate two and all other rates to one gives a
non-complex-balanced example: leaf pure-B and pure-C balance would demand b=c and
c=2b simultaneously.

The theorem does not provide a normlike one-step physical-generator function F(A,N).
Indeed the accepted mediated lift has a proved no-go for **every** such geometric
Foster function on one closed satellite class, yet is covered by this sampled-core
theorem. This is a substantive change in method, not a claim that the old no-go was
a stability obstruction.

## 10. Limits, costs and conventional credit

Support closure is only sufficient. A stable negative control is the all-unit-rate
common-A lift of `r<->B`, `r<->C`, `2B<->2C`, together with `0<->A`. Its stripped
top order-two support never reaches r, but unit concentrations are complex balanced
and ordinary Poisson product form proves all exponential moments. Failed support
must therefore report stability UNKNOWN, not instability or impossibility of another
sampled certificate.

The qualitative receiver needs only strict raw input recognition, weak-reversibility
returns and finite support scans. It need not evaluate (2), simulate Q, solve an ODE,
solve any stationary law, or materialize a scalar Foster power. It relies on this
retained ordinary theorem as reusable proof capital.

Numerical receiving separately evaluates the n rational support-level recursions,
their degree-p powers, C,T,K0,K,a,M_cut, and factored bounds. Degree or power-bit
budgets may stop this calculation with numerical UNKNOWN while preserving a certified
qualitative result. Such a budget is not silently a total input/bit/memory/wall-time
budget. Very large molecularity is compactly encoded and can make numerical scalar
power expansion infeasible. Neither the finite fibers nor the enormous head is
supplied as an acquisition oracle or enumerated as hidden preprocessing.

Ordinary CTMC time change, density-dependent martingale limits, finite-time fluid
comparison, sampled-time Foster criteria, and regenerative occupation laws are the
main ingredients and receive full credit. The earned join is the explicit uniform
raw-support activation bound, the death-clock/reciprocal-A estimate, paid failed-seed
cycles, and exact qualitative/numerical receiving interface. No novelty or priority
claim is made. General weak reversibility, stripped leading-support failure, p=1,
and networks lacking a common seed remain outside this theorem as stated.
