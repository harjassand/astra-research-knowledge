# A practical global upper-ratio barrier from an exact tilted source kernel

**Author construction, pending independent receipt.** This is a materially new
actual-source operation, not a repair by repeated local excursions. The earlier
linear-quotient construction and its exact counterexample to the original F1
remain intact in
`HISTORY_PRACTICAL_ONE_SIDED_QUOTIENT_V1_ccab7011.md`; its scripts and certificates
are unchanged. In particular, the earlier negative-drift calculation was not
itself a global barrier. The construction below closes that particular joining
gap, conditionally on the stated actual entrance and remaining physical gates.

## 1. Result and its exact scope

Use the literal rate-2 chain, integer reference `N>=10^5`, and

    S=A+B+C+D+E, L=A+(C+D)/2, R=E²/(NL).

The pre-stop domain is

    L>0, R<2, E<=N/100, L<=N/5000,
    A<=L/100, |S-N|<=12 N^(1/5).                         (D)

There is **no lower R gate, no lower E gate, no lower L gate, no supplied
fast-A law, and no firing-count budget**. Physical nonnegative integer species
are understood. This ratio barrier needs neither a separate B floor nor a Z
bound; those may still be necessary for the subsequent progress/clearance
consumer.

Define, mathematically, `H_N(0)=1` by the adjacent ratios

    H_N(e+1)/H_N(e) = [1+e/(4N)]/[1-(e+1)/(2N)].         (1)

Only the range `0<=e<=N/100+1` is used. Set

    Phi(A,L,E) = 2^(-L) H_N(E) [1-E/(2N)]^A.            (2)

Then the **complete actual finite-jump generator** satisfies

    G Phi/Phi <= -1/2 - AL/2                            (3)

throughout (D). Thus the process stopped on leaving (D), including the actual
exit jump, is a nonnegative supermartingale. Its definition is not an
instruction to materialize an E-term product. All proof and use below require
only adjacent ratios and closed log bounds; no loop of length E, N, or the
number of firings is required.

Let `eta` be any actual stopping-time entrance into (D), with actual entrance
state `x`. Let `tau_R` be the first subsequent `R>=2`, `tau_cap` the first
`E>=ceil(N/100)` or `L>=N/5000`, and `sigma_A,sigma_S` the first failures of the
A and original narrow-count gates. An arbitrary declared horizon may also be
included. A simultaneous ratio/gate/cap exit is counted as an upper-ratio hit.
Then

    P_x(tau_R <= tau_cap wedge sigma_A wedge sigma_S)
       <= min(1,Phi(x)).                                (4)

In particular, the practical actual entrance condition

    R(x)<=9/5                                           (5)

implies

    P_x(ever reaching R>=2 before the other stops)
       <= exp[-L(x)/100].                               (6)

The bound is for **one original stopped path over all of its excursions**. No
reset, union over attempts, conditional-independent Poisson law, stationary
preparation, or deterministic bound on its event count occurs.

Entrance (D),(5) must actually be received. The theorem does not acquire that
entrance, prove persistence of A/Z gates, receive a new population seed, or
supply a practical final clearance/CDF algorithm. The accepted count event is
still limited to the **original** cap or original time `4N^(1/5)`; see section 7.

## 2. Every actual jump and its exact tilted ratio

Write

    p=1/2, c=1/2, u=cE/N, q=1-u, t=c/N,
    g=1-t/q, k=1+t/q, d=1+(u-t)/2.

The exact source rows are below. A ratio attached to a zero-rate row need not
be evaluated; in particular E-decreasing rows are active only at E>=1.

| channel | rate | (Delta A,Delta L,Delta E) | Phi(next)/Phi |
|---|---:|---|---|
| 0->A | 1 | (1,1,0) | pq |
| A->0 | A | (-1,-1,0) | 1/(pq) |
| 2A->AC | A(A-1) | (-1,-1/2,0) | 1/(sqrt(p)q) |
| AC->2A | AC | (1,1/2,0) | sqrt(p)q |
| 2A->AD | A(A-1) | (-1,-1/2,0) | 1/(sqrt(p)q) |
| AD->2A | AD | (1,1/2,0) | sqrt(p)q |
| 2A->AE | A(A-1) | (-1,-1,1) | (1+u/2)g^(A-2)/(pq²) |
| AE->2A | AE | (1,1,-1) | pq(q+t)k^A/d |
| AE->CD | AE | (-1,0,-1) | k^(A-1)/d |
| CD->AE | 2CD | (1,0,1) | (1+u/2)g^A |
| CD->AB | CD | (1,0,0) | q |
| AB->CD | AB | (-1,0,0) | 1/q |

For example the `CD->AE` row uses simultaneously the actual E change, the
actual A increment, and the change in the base of its A-dependent factor.
The two AE channels are both present. No slow variable is frozen in this table.

### Exact CD-source cancellation

The two CD-source channels contribute exactly

    2CD[(1+u/2)g^A-1] + CD(q-1)
      = 2CD(1+u/2)(g^A-1) <= 0.                         (7)

This is the tilted immigration/branching kernel cancellation. It is exact for
finite N and arbitrary actual integer A, not a leading-order average. At A=0
it vanishes exactly. In particular there is no accumulated positive CD/N
remainder to pay over the enormous future firing count.

### Actual AB and both AE rows

For active AE rows, A,E>=1, so `q+t<=1`, `d>=1`, and `q>=199/200`.
Moreover

    (A-1)t/q <= At/q <= 1/995000 <1/2.                  (8)

Here `A/N<=1/500000` follows directly from the two A/L and L/N gates.
The elementary binomial/geometric bound

    (1+x)^m <= 1/(1-mx) <= 1+2mx  (m integer, mx<=1/2)

therefore gives `k^(A-1)<=1+2At/q`. The combined AE ratio-minus-one is

    [(p(q+t)^2+1)/d] k^(A-1)-2
       <= -c+4At/q.                                    (9)

Combining the actual AB row **before** taking absolute values, and using
`B=S+A-2L-E`, gives

    (AB and both AE contributions)
       <= (cAE/q)[(S-N)/N +5A/N-2L/N-pE/N]
       <= (cAE/q) |S-N|/N.                             (10)

The leading finite-tilt AE cost is canceled using `c=1-p`, not by replacing
`1-p` with `-log(p)`. Formula (10) retains the actual B/E/L parameter motion.

If A>0, integrality and `A<=L/100` force `L>=100` and hence `N>=500000`.
By `E²<=2NL` and the original count gate,

    (|S-N|/N)(E/L)
       <=12 sqrt(2)/(N^(3/10) sqrt(L)) <1/20.            (11)

One exact scalar proof is `48^10<500000^3`, `sqrt(L)>=10`, and `sqrt(2)<2`.
Consequently (10) is at most `3AL/100`. If A=0 it is identically zero.
No lower-ratio inequality is used in (8)--(11).

## 3. Remaining source rows and continuous-domain sign

The following rational inequalities hold on `q>=199/200`, `u<=1/200`:

    1/(pq)-1 <= 11/10,
    2[1/(sqrt(p)q)-1] <= 9/10,
    (1+u/2)/(pq²)-1 <= 11/10,
    sqrt(p)q-1 <= -29/100.                              (12)

They follow, without numerical sign sampling, from `7/10<sqrt(1/2)<71/100`.
Since `C+D=2(L-A)`, the actual AC/AD rows contribute at most
`-29 A(L-A)/50`. The three actual 2A rows contribute at most `2A²`:
for the E-changing row `A(A-1)>0` implies `A>=2`, so its factor `g^(A-2)<=1`.
The immigration contribution is at most `-1/2`. Combining these bounds with
(7),(10)--(12),

    G Phi/Phi
       <= -1/2 +(11/10)A +(129/50)A² -(11/20)AL.        (13)

When A>0, `L>=100` and `A<=L/100` yield

    (11/10)A +(129/50)A² -(11/20)AL
       <= [11/1000+129/5000-11/20] AL
       = -(1283/2500)AL <= -AL/2.                      (14)

When A=0, all rows except immigration and CD rows vanish, and the CD sum is
exactly zero; (3) follows directly. This also explains why no externally
supplied lower-L gate is needed.

## 4. Closed log bounds: no E-length construction or computation

Summing only elementary inequalities, not computing H term by term, gives
for integer `0<=E<=N/100`

    log H_N(E) <= (377/1000) E²/N + E/(8N).             (15)

For every one-step target, `E<=N/100+1<=N/50`, and

    log H_N(E) >= (187/500) E²/N.                       (16)

Here is the full remainder calculation. With `c=1/2`, the sum of the linear
terms is exactly

    c E(3E+1)/(4N) = 3E²/(8N)+E/(8N).

For the lower bound use `log(1+x)>=x-x²/2` and `-log(1-y)>=y`; the discarded
quadratic sum is

    c² E(E-1)(2E-1)/(48N²) <= c² E³/(24N²).

Thus on `E/N<=1/50` the coefficient of E²/N is at least
`3/8-1/4800>187/500`. For the upper bound use
`-log(1-y)<=y+y²/[2(1-y)]` and `log(1+x)<=x`. For E>=1 its extra term is at most

    c² E(E+1)(2E+1)/(12N² q)
       <= c² E³/(2N² q)
       <= E²/(796N).

Since `3/8+1/796<377/1000`, this proves (15); E=0 is exact.
All these bounds use a fixed number of arithmetic operations on the encoded
state. Computing exact rational upper/lower bounds is polynomial in its bit
length. Optional logarithmic evaluation of the displayed final exponential
cost is not an event simulation.

The elementary expansion of `log 2` at 1/3 gives

    56/81 <= log 2 <= 25/36.                            (17)

For the lower bound retain the first two positive terms in
`2 sum_(j>=0) [(1/3)^(2j+1)/(2j+1)]`; for the upper bound replace every
`2j+1`, j>=1, by 3 and sum the geometric tail. Thus these are explicit
rational certificates, not floating-point logarithm tests.

At an actual entrance satisfying `R<=9/5`, (15),(17), `A log q<=0`,
`E/N<=1/100`, and physical `L>=1/2` give

    log Phi <= [-56/81 +(377/1000)(9/5)]L +1/800
             <= -L/100.                               (18)

For a specified entrance one can instead retain the sharper closed expression

    log Phi <= -(56/81)L +(377/1000)E²/N +E/(8N),        (19)

or a rigorously enclosed actual log Phi. No preparation oracle is hidden in
(18) or (19).

## 5. The actual upper-hit endpoint, including simultaneous failures

At a first R>=2 endpoint reached from (D), all components are still actual
nonnegative integers. Its L value is positive: if pre-jump A>0 then L>=100
and L' >=99; if A=0, every active L-changing row is immigration, which
increases L. Therefore physical `L'>=1/2`. Also

    E'/N<=1/50,  q'>=99/100,
    A'<=A+1<=L'/100+101/100.                            (20)

These inequalities use only pre-jump gates; they remain true if this same
jump exits the A/count/cap gates. By `log q'>=-1/99`, (16),(17), and `R'>=2`,

    log Phi(x')
      >= [187/250-25/36-1/9900]L' -101/9900
      >= 3L'/100 >0.                                   (21)

The final inequality is an exact rational scalar check for `L'>=1/2`.
Thus every actual ratio-hit endpoint has Phi>=1, without assuming the
post-jump A gate or silently dropping simultaneous exits.

For a globally positive extension, set `K=ceil(N/100)+1` and replace E by
`min(E,K)` only in H and q outside the used range. Keep the actual A and L.
This changes none of the pre-stop generator rows or terminal values above.
For fixed N the stopped domain and its one-step targets are finite (the count
band also bounds B), so this stopped positive function is bounded and its
supermartingale is integrable. Optional stopping first at a finite time and
then Fatou proves (4). An unbounded physical waiting time is therefore not
an uncharged cost; all repeated excursions are contained in the same test.

## 6. A useful fully actual entrance-scale corollary

Let the real stopping-time entrance satisfy (D),(5), `L>=m`. Then the conditional
upper-hit cost is at most `exp(-m/100)`. If in addition the actual entrance
has `E>=e0 T³`, `T=N^(1/5)`, then (5) implies

    L>=5e0² T/9,
    upper-hit cost <= exp[-e0² T/180].                  (22)

These are consequences of a **received actual entrance**, not a theorem that
such an entrance occurs. Formula (19) also handles a specified fixed-L source
state directly: the charge is its real L and E, not a restarted average A or
a newly supplied conditional fiber distribution.

### Sharper price for the actual fixed-L startup now being received

If the separate actual-source entrance construction receives

    N>=10^20, L0=400, A0<=2, E0<=8*400³=512,000,000,

then the exact closed entrance bound (19), evaluated at the worst N and E,
is

    log Phi0 <= -56*400/81
                +(377/1000)(512,000,000)²/10^20
                +512,000,000/(8*10^20)
              < -276.5422 < -276.                      (24)

Thus its conditional ever-hit cost is at most `exp(-276)`, not the much looser
`exp(-4)` obtained by discarding the actual E information in (6). Even the
conservative ceiling `E0<=128*400³` gives `log Phi0<-276`. This is a direct
rational certificate using the real entrance state; it does not create or
acquire that state. The startup construction's own failures, A/Z continuation
costs, and original count/horizon charges remain payable separately. The
exact rational values are saved in the certificate; the decimals here are
only a readable summary.

The kernel supplies only upper-ratio protection. The accepted buffered progress
coordinate `E-A/2+L/100` can use it without a lower R gate once the other actual
A/imbalance/positive-progress gates and the entrance have been received.

## 7. Original ledger, horizon, and residual obligations

The accepted `ACTUAL_NARROW_COUNT_BAND.md` and its receipt supply, from the
original preparation `(0,N,1,1,0)`, for `T=N^(1/5)`, the joint event through
original `tau_cap wedge 4T` at cost

    epsilon_S = exp(-N/6200)+exp(-T)+exp(-5T).           (23)

They do not supply a fresh interval of length 4T after eta. To join this result,
condition the supermartingale theorem on the actual past-measurable entrance,
stop it at the actual original deadline, and add (23) **once**. For example,
if entrance occurs by the original deadline with `L>=m`, the upper-ratio hit
before that deadline, the cap, or the first A failure has unconditional cost
at most `exp(-m/100)+epsilon_S`, plus the separately stated probability of
failing to acquire the entrance. No conditioning on a future count-good event
is used to alter a generator or produce an independent counter law.

Persistence of `A<=L/100`, imbalance protection, actual entrance probability,
progress/time-budget fitting inside the remaining original horizon, and the
future harmonic/clearance receiver remain separate receiving obligations.
If they have respective proved costs, they can be added once by an ordinary
failure-event union. No such costs are invented here. In particular this note
makes no claim of physical reset, supplied controller, changed rates,
stationary preparation, final short-clearance theorem, or practical CDF law.

## 8. Ordinary evidence and preservation

`tilted_kernel/check_tilted_kernel.py` verifies the literal twelve stoichiometric
rows, the exact local-ratio identities, the source-group identities, and all
rational inequalities in the continuous-domain argument and endpoint/log
certificates. `tilted_kernel/tilted_kernel_certificate.json` is its replayable
output. No sampled sign test is used as acceptance. The finite scalar checks
support the displayed ordinary proof; they are not an exhaustive enumeration
of physical states.

The old quotient note and old author manifest are preserved verbatim as
`HISTORY_*_V1_*`. All old quotient code/certificates and the complete-cubic
construction remain unchanged. The new author freeze labels this as a pending
independent-receipt, conditional global upper-barrier component, not a complete
rate-2 timing capability.
