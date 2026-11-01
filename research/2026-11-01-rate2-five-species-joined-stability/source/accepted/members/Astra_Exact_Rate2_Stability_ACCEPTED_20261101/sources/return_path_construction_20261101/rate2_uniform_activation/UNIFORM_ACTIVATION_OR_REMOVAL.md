# A fully retained uniform activation-or-removal block

**Author theorem candidate; pending independent review.** This proves an actual
uniform hitting law, not full population removal, recurrence or a stationary
moment. Every competing channel, failed return and A death is retained.

## 1. Model, output and explicit cost

Use the rate-2 tree on A,B,C,D,E: unit 0<->A, 2A<->AC, 2A<->AD,
2A<->AE, AE<->CD and CD<->AB, except CD->AE has coefficient two.
Binary propensities use falling factorials. Write S=A+B+C+D+E,
R=C+D+E and M=A+min(C,D). For every initial state with total N>=10^40,
put

    m=floor(sqrt(N)/(2*10^4)), T0=10^12, H=8m+T0.

Let tau be the first actual time at which either

    S<=3N/4                 (actual fractional removal), or
    R>=B/100               (activated composition).

Then H<=sqrt(N), and the claimed uniform bound is

    P_x(tau>H) <=4 exp[-sqrt(N)/160000].                 (1)

The activated output is not itself asserted to give removal or interior entry.
It is exactly the region of the separate three-profile local drift certificate.
No ordinary deterministic attraction result supplies a stochastic step here.

The only previously constructed component used below is the exact initial-growth
function in `../rate2_uniform_initial_growth/UNIFORM_FULL_GENERATOR_INITIAL_GROWTH.md`,
SHA256 90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e.
That component is author-frozen and pending independent review. The receiving
argument below rechecks its domain at every actual use.

## 2. Exact exponential charging mechanism

Define on all states U=E-A/10 and Z=exp(-U/10). For R<=B/100, exact generator
algebra gives

    LU=(17/10)CD+(13/10)A^2-(6/5)A-1/10
          + A[B/10-(C+D)/10-2E].                        (2)

Since `(C+D)/10+2E<=2R<=B/50`, the last bracket is at least `(2/25)B`.
For nonnegative integer A,

    (13/10)A^2-(6/5)A >= A^2/2-1/2.

Consequently, with P=(CD+A^2)/2+(2/25)AB,

    LU>=P-3/5>=M^2/4+(2/25)AB-3/5.                     (3)

The last inequality uses `CD>=min(C,D)^2` and
`A^2+min(C,D)^2>=M^2/2`. This does not assume balanced C,D.

All U jumps have absolute size at most 11/10. Its exact predictable squared-mark
intensity is

    Gamma_U=(1+A)/100+(123/100)A(A-1)
        + A(C+D)/100+AB/100+(163/100)CD+(101/50)AE.     (4)

The actual AE losses are part of this identity. As
`A(C+D)/100+(101/50)AE<=(101/50)AR<=(101/5000)AB`,
and `A<=A^2` for integer A>=0,

    Gamma_U<=1/100+(31/25)A^2+(163/100)CD+(151/5000)AB
           <=4P+1/100<=4LU+241/100.                    (5)

For |v|<=11/10, Taylor's integral remainder gives
`exp(-v/10)-1<=-v/10+v^2/100`, because exp(11/100)<2.
Combining (3)-(5),

    LZ/Z <=-LU/10+Gamma_U/100
          <=-(3/50)LU+241/10000
          <=-(3/200)M^2+601/10000
          <=-M^2/100,       whenever M>=4.             (6)

This is an actual whole-generator exponential inequality on the composition
region. The AB phase reserve pays both the competing AE loss and its variance.
It invokes neither an A occupation oracle nor a quasi-stationary fiber law.

## 3. The small-M domain is automatically B-rich

Stop the construction if S<=3N/4, R>=B/100 or S>2N; the last is an adverse exit.
At every pre-stop state with M<m, A<=M<m and

    3N/4<S=A+B+R <m+(101/100)B.

Thus B>N/2, since m<49N/200. The source's global function

    V_N=2^(-M)[1+(16/N)phi(M,R)A^2],
    phi=clip_[0,1]((96-R/(M+1))/48)

therefore has its actual full drift `LV_N<=-V_N/4` throughout each such strip.
The parameter condition N>=10^8(m+1)^2 holds for the chosen scale. Targets use
the same global function, and no channel is killed in this inequality.

If M<m initially, apply the source's stopped argument until the main stop or
M>=m, with either main boundary taking priority over a simultaneous seed hit.
Every terminal M is at most m. Therefore the probability this phase takes more
than 8m is at most

    (101/100)exp(-m).                                     (7)

If M>=m initially, the phase has length zero. An exit B<N/2 need not be inferred
to be service: within the stated survival/composition region it cannot occur
while M<m. All actual exits used here are explicitly named.

## 4. Paid persistence of the seed

Consider any post-seed state with S<=2N and M>=m, before the main stop. Set
ell=floor(m/2). During the next T0 units, a hit of M<=ell must occur within an
excursion starting at the actual downward crossing from m to m-1. All M jumps
are -1,0 or +1. Stop each such excursion on return to M>=m, on M<=ell, on a
main boundary or at the horizon.

Its interior lies in ell<M<m, so Section 3 receives the full V_N drift. At
entry V_N<= (101/100)2^(-(m-1)); at a lower hit V_N>=2^(-ell). Conditional
optional stopping therefore bounds the lower-hit probability of EACH actual
excursion by

    (101/100)2^(ell-m+1) <=(202/100)2^(-m/2).             (8)

There is no independence assumption between excursions. Before S>2N, the sum
of all twelve actual intensities is at most 32N^2. Hence the expected number
of downward entry crossings during T0 is at most 32N^2 T0. Sum the conditional
bound (8) over their actual stopping times to obtain

    P(hit M<=ell before main stop within T0)
        <=65N^2 T0 2^(-m/2)<=exp(-m/4).                  (9)

The last inequality is uniform for N>=10^40. Indeed
`m>=sqrt(N)/(4*10^4)`; `log N<=N^(1/4)` in this range; and
`log(65T0)+2log N<=3N^(1/4)<=m/16`.
Finally `log2>=2/3` gives `log2/2-1/16>1/4`.
Counts and compensators are bounded before the upper stop, so the conditional
sum uses ordinary stopped counting-process expectation, not a hidden mixing law.

## 5. Charged composition crossing

Stop the post-seed process at the first main boundary, M<=ell or T0. At each
pre-stop state M>ell, hence M>m/2 and M>=4. By (6),

    LZ<=-[m^2/400] Z.                                    (10)

All pre-stop totals are <=2N. Initially U>=-N/5, so Z<=exp(N/50).
If the stop has not occurred by T0, then `U<=E<=R<B/100<=N/50`, so
`Z>=exp(-N/500)`. The actual exponential-supermartingale inequality thus gives

    P(no such exit by T0)
        <=exp[11N/500-m^2 T0/400]<=exp(-N).              (11)

Here `m^2>=N/(16*10^8)` and T0=10^12, so the exponent is at most
`(11/500-25/16)N<-N`. No terminal-value limit exchange or unpriced exposure
estimate is used. Equations (9)-(11) show that, except for the upper total exit,
the post-seed phase hits either activated composition or actual fractional
removal within T0, with conditional failure at most exp(-m/4)+exp(-N).

## 6. Immigration, clocks and the uniform conclusion

Internal channels conserve total and the sole count increase is unit-rate
immigration. Consequently S(t)<=N+I(t), with I the actual unit Poisson immigrant
count. H<=N/4 for N>=10^40. An upper exit S>2N by H requires I(H)>=N, and
Chernoff with parameter log2 gives

    P(upper exit by H)<=exp[H-Nlog2]<=exp(-N/3).          (12)

This prices the whole episode, including correlations between entry time,
failed excursions and immigration. There is no fresh independent immigration
clock attached to the random phase entrance.

Combining (7), (9), (11), (12), and `m/4>=sqrt(N)/160000`,

    P(tau>H) <=(101/100)e^(-m)+e^(-m/4)+e^(-N)+e^(-N/3)
              <=4 exp[-sqrt(N)/160000].

Also `H<=sqrt(N)` on the stated range. This proves (1), uniformly over every
initial composition with total N. States already in the target have tau=0.
Nonexplosion follows from S(t)<=N+I(t); stopped Dynkin and the finite-time
conditional compensator sums used above are legitimate after ordinary finite
localization, with Fatou for nonnegative exponential supermartingales.

## 7. Exact scope and costs

The time and count thresholds are explicit but deliberately enormous existence
constants. Function evaluation requires only the actual five counts, rational
arithmetic, a clipped linear cutoff and an exponential with rational exponent.
The proof is uniform in all imbalance and does not enumerate population paths.
The excursion union costs only the explicitly bounded expected event count.

This theorem supplies an exponentially priced activation-or-removal receiver at
scale sqrt(N), not the sharper N^(1/5) entrance. It does not provide macro-positive
B,C,D,E simultaneously. The local activated drift, the independently supplied
interior-removal theorem and the root sampled-kernel consumer remain DIFFERENT
components with unreceived interfaces. In particular no recurrence or stationary
exponential moment follows from this statement alone.
