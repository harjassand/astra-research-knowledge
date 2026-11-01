# Constant-physical-time actual removal from a paid macro persistence floor

**Author construction, pending independent review.** This is an exact count-generator/output-clock receiver, not a mixing theorem or a claim of novelty for entropy itself. No external source was retrieved. It retains the original rate-2 dynamics, continuing immigration, and actual deaths. The existing small-strip harmonic proof is used only in its actual `m0<=10^-6` strip.

## 1. Two explicit services

Let `S=A+B+C+D+E`, `M=A+min(C,D)`, and let `N` be a fixed positive integer. The original channels are unit `0<->A`, `2A<->AC`, `2A<->AD`, `2A<->AE`, `AE->CD`, `CD->AE` at coefficient 2, and `CD<->AB`; binary propensities are falling factorials.

Fix rational `0<m0<=10^-6` and require

```
N >= max{32 h, 2000/m0}.
```

Every actual initial state with `3N/4<S(0)<=17N/16` and `M(0)>=m0 N` satisfies, for physical time `h=5`,

```
P[S(5)>13N/16]
 <= 160 N^2 exp(-m0 N/1000)
    +324480/(m0^2 N)+exp(-N/64)+exp(-N/96).       (T5)
```

For the wider old entrance `3N/4<S(0)<=5N/4`, with the same M hypothesis, physical time `h=8` gives

```
P[S(8)>13N/16]
 <= 256 N^2 exp(-m0 N/1000)
    +823296/(m0^2 N)+exp(-N/32)+exp(-N/96).       (T8)
```

The occupation terms in T5/T8 can be replaced by the smaller exponential alternatives in Section 6.1. Bounds may of course be capped at one. A state initially at or below `3N/4` is immediate removal, with its whole-horizon immigration still charged. There is no hidden deterministic entrance or stochastic equilibrium preparation. The old `400/m0^2` physical horizon is replaced by 5 or 8; the polynomial population/error cost is explicit and remains severe when the only paid floor is `m0=10^-6`.

For example, (T5) with `m0=10^-6,N=10^20` has occupation error exactly `0.0032448`; the other displayed errors are negligible, so the bound exceeds 99.6755% success. This is a certified finite-N prediction, not an SSA runtime or physically calibrated preparation claim.

## 2. A conditional receiver that exposes the persistence input

For any `0<m<=10^-3`, let `p_M` be a separately PAID bound on hitting `M<m S` before physical time h or the mass exits `S<=3N/4`, `S>2N`. Assume the initial state lies in that M region and `S(0)<=5N/4`. Let `b>0` and `h/6>b`. The actual occupation clock obeys

```
P[ no lower mass hit by h, no upper mass hit by h,
   no M-floor exit by h, integral_0^h A(t)dt < bN ]
 <= B_occ(m,h,b)
 := 2h(4+33h) / [3 m^2 N (h/6-b)^2].             (C)
```

This is valid for `N>=32`. To turn it into endpoint removal, add `p_M`, the whole-horizon immigration error, and the appropriate death-clock lower tail. No stronger macro persistence is claimed here. A receiver with an independently acquired larger m can use (C) directly, without paying the universal `m0/8` floor.

## 3. Factorial entropy and exact original/competitor inequality

Put

```
s=(sqrt(7)-1)/2, t=2-s, alpha=2/9,
q=alpha(1,s^2,s,s,t),
V_N(x)=sum_i [log(x_i!)-x_i log(q_i N)+q_i N].
```

Here `sum q_i=1`. `V_N>=0` on EVERY count state: `log(k!)>=k log k-k`, with the usual convention at zero, bounds it below by a sum of nonnegative unnormalized relative entropies. For `S<=5N/4`,

```
V_N <= S log[S/(q_* N)]+N <=4N.                  (1)
```

Indeed `q_*=alpha s^2>1/7` and `log(35/4)<12/5`. The potential is separable and discretely convex because its A second difference is `log[a/(a-1)]>=0` at `a>=2`.

Use the already supplied drift-equivalent internal complex-balanced competitor: reduce `2A->AC,2A->AD` to s, add `2A->CD` with coefficient `1-s`, and leave all other channels unchanged. The actual generator satisfies the EXACT count identity

```
(L_original-L_competitor)V_N
 =(1-s)A(A-1)[2g_A(A-1)-g_A(A-2)-g_A(A)] <=0,    (2)
```

with both sides zero for `A<2`. This uses neither the competitor's stochastic stationary law nor a stationary law for the actual chain.

## 4. Exact zero-count and shifted-target costs

For a binary competitor reaction `y->z`, write `w_yz=k_yz q^y`,
`u_y=(x)_y/q^y`, and similarly `u_z`. At an enabled source define

```
v_yz=(x+z-y)_z/q^z.
```

Both u_y and v_yz are then positive, and the literal factorial increment is
`Delta V_N=log(v_yz/u_y)`. For a disabled source define `v_yz=u_z`; its actual contribution is zero. The elementary inequality

```
u log(v/u) <= v-u-(sqrt(u)-sqrt(v))^2
```

extends to u=0 by continuity. Therefore it can be summed over ALL channels, including disabled ones. Complex balance cancels `sum w_yz(u_z-u_y)=0` exactly.

Write `delta_yz=v_yz-u_z`. The inequality
`(r-s')^2 >=(r-s)^2/2-(s'-s)^2`, together with
`(sqrt(v)-sqrt(u_z))^2<=|v-u_z|`, yields

```
L_comp,int V_N <= -D_f(x)/2 + (3/2)sum w_yz |delta_yz|,
D_f=sum w_yz(sqrt(u_y)-sqrt(u_z))^2.              (3)
```

No logarithmic estimate near zero, derivative remainder, or omitted source is used. For enabled edges, the following table gives the exact numerator shift `q^z delta_yz` and weight `w_yz/q^z`:

| Edge | Shift | Weight |
|---|---|---|
| 2A->AC | A-C-1 | 1 |
| AC->2A | 2A | s |
| 2A->AD | A-D-1 | 1 |
| AD->2A | 2A | s |
| 2A->AE | A-E-1 | 1/t |
| AE->2A | 2A | t |
| AE->CD | C+D+1 | t/s^2 |
| CD->AE | A+E+1 | 2s^2/t |
| CD->AB | A+B+1 | 1 |
| AB->CD | C+D+1 | 1 |
| 2A->CD | C+D+1 | (1-s)/s^2 |

Disabled-edge delta is zero, hence the same absolute-value bounds remain valid. Expanding absolute values by triangle inequality and using `2s^2+2s=3` gives the exact coefficient envelope

```
sum w_yz |delta_yz|
 <= (8+sqrt(7))A+B+4C+4D+2E+8
 <= (32/3) S+8.                                      (4)
```

The last coefficient bound follows from `sqrt(7)<8/3`.

Define the ordinary, homogeneous square dissipation

```
D(x)=sum_yz w_yz [sqrt(x^y/q^y)-sqrt(x^z/q^z)]^2.  (5)
```

Only the 2A monomial differs between D_f and D. Uniformly for all integer A>=0,
`|sqrt(A(A-1))-A|<=1`, interpreting the falling factorial as zero at A=0.
The total directed flux incident on 2A is `2(s+2)alpha^2`. Thus

```
D_f >= D/2-2(s+2),
L_original,int V_N <= -D/4+16S+15.                (6)
```

Every count boundary has now been charged explicitly.

The ACTUAL port contributes

```
L_port V_N=log[(A+1)/(alpha N)]+A log(alpha N/A),
```

where the death term is zero at A=0. On S<=2N the first term is at most 3; the second is at most `alpha N/e<=N/9`. Consequently, for N>=32,

```
L_original V_N <= -D(x)/4+33N.                    (7)
```

This is a fixed-reference potential. It is not asserted to contract to zero when S differs from N; only its nonnegativity and its output dissipation are used.

## 5. Explicit global OUTPUT coercivity on the M region

For S>0 set `r_i=x_i/q_i`, `z_i=sqrt(r_i)`. Let

```
u0=r_A, uC=z_A z_C, uD=z_A z_D, uE=z_A z_E,
uB=z_A z_B, v=z_C z_D.
```

Combining reciprocal directed edges in (5), and discarding the added nonnegative 2A->CD term, gives

```
D/alpha^2 >=2s[(u0-uC)^2+(u0-uD)^2]
 +(3-s)(u0-uE)^2+(5-3s)(uE-v)^2+2s^2(v-uB)^2.
```

Cauchy-Schwarz along paths of lengths 1,2,3 implies

```
(u0-uE)^2+(u0-v)^2+(u0-uB)^2
 <=6(u0-uE)^2+5(uE-v)^2+3(v-uB)^2.
```

Since `3-s>=2`, `5-3s>=5/3`, `2s^2>=1` and `2s>=1/3`,

```
D >= (alpha^2/3) [r_A sum_(i!=A)(z_i-z_A)^2
                         +(r_A-sqrt(r_C r_D))^2].   (8)
```

Write `K=sum_(i!=A)(z_i-z_A)^2`. Since `sum q_i r_i=S`, weighted Cauchy-Schwarz gives

```
(A-alpha S)^2 <=2alpha(1+alpha) S K,
D >= [3A/(22S)] (A-alpha S)^2.                    (9)
```

Now suppose `M>=m S`, `0<m<=10^-3`.

* If `A>=44m^2 S`, (9) gives `D>=6m^2(A-alpha S)^2`.
* If `A<44m^2 S`, both C,D are at least `m(1-44m)S`. Using `s<=5/6`,

```
sqrt(r_C r_D)-r_A
 >=(mS/alpha)[(1-44m)/s-44m]
 >=(mS/alpha)[6/5-(484/5)m] >=mS/alpha.
```

Equation (8) gives `D>=m^2 S^2/3`. Also `0<=A<=44*10^-6 S<2alpha S`, so `(A-alpha S)^2<=alpha^2 S^2`; hence
`D>=(27/4)m^2(A-alpha S)^2>=6m^2(A-alpha S)^2`.

Thus the uniform, boundary-valid output inequality is

```
D(x)>=6m^2(A-(2/9)S)^2,  M>=mS, 0<m<=10^-3.     (10)
```

No coordinatewise interior lower bound, attraction time, spectral mixing estimate, or exponential Gronwall factor appears.

## 6. Actual stopped occupation and its finite-N probability cost

Stop the FULL continuing process at the first of time h, `S<=3N/4`, `S>2N`, or `M<mS`. On its source region, (7),(10) give

```
L V_N <=-(3/2)m^2(A-alpha S)^2+33N.
```

The stopped state set and its one-jump targets are finite. Dynkin's formula, `V_N>=0`, and (1) therefore give

```
E integral_0^tau (A-alpha S)^2 dt
 <=2N(4+33h)/(3m^2).                               (11)
```

The stopping jump is evaluated with the same globally nonnegative V_N. None of the estimates is conditioned on a future good event. If no stop occurs before h and the actual A occupation is below bN, then `alpha S>N/6` throughout and Cauchy-Schwarz forces

```
integral_0^h(A-alpha S)^2dt >=N^2(h/6-b)^2/h.
```

Markov's inequality applied to the nonnegative stopped integral proves (C). This is a direct output service, not full-state approximation.

### 6.1 Optional exponential probability bound, with every actual entropy mark paid

The polynomial Markov bound can be strengthened without changing its physical horizon. Let `ell=log(6N)`. Every ACTUAL binary jump has

```
|Delta V_N| <=2ell.
```

Indeed every enabled source and target factorial monomial is at least one; source counts are <=2N, target counts <=2N+2; and `q_max/q_min=t/s^2<2`. Thus both directions of the ratio in the exact factorial increment are at most `4(2N+2)^2<=36N^2` for N>=2. Actual port marks satisfy the same bound: their ratios are `(A+1)/(alpha N)` or `alpha N/A`, and their reciprocals, with A>=1 for an enabled death. The fixed-N linear terms are therefore fully included.

Before the upper mass stop, the actual total intensity is at most `13N^2` (in fact `q_all<=3S^2+1`). Hence the stopped entropy martingale has jump bound `2ell` and predictable bracket at most

```
v=52h N^2 ell^2.
```

On the no-stop/low-occupation event of (C), set

```
R=N^2(h/6-b)^2/h,
x=(3/2)m^2 R-N(4+33h).
```

Equations (7),(10), the lower bound V_N>=0, and the initial bound V_N<=4N imply that this event forces the stopped entropy martingale to be at least x. For x>0 the bounded-jump exponential-compensator/Freedman inequality gives

```
B_exp(m,h,b)
 =exp{-x^2/[104h N^2 ell^2+(4/3)ell x]}.
```

For x<=0 take B_exp=1. Thus (C) holds with `min{1,B_occ,B_exp}`. This is a martingale tail for the exact entropy potential, not a Poisson law conditioned on an occupation path or an equilibrium assumption.

For the actual harmonic receiver `m=m0/8`, the two x values simplify to

```
T5: x=m0^2 N^2/1920-169N,
T8: x=m0^2 N^2/3072-268N.
```

At `m0=10^-6,N=10^19`, T5's exponent is greater than 23 (use the certified rational upper bound `log(6N)<46`). At `N=10^20`, it is greater than 2200 (use `log(6N)<48`). Thus these examples have occupation errors at most `exp(-23)` and `exp(-2200)`, respectively, plus the separate displayed persistence/death/immigration errors. The supporting checker verifies both claims with rational exponential-series lower bounds and exact fractions; no floating-point probability is needed for these examples.

## 7. Receiving ONLY the accepted harmonic small-strip persistence

The accepted source is
`../rate2_explicit_macro_removal/EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md`,
SHA256 `4d1ad7a929f7e3c6d81d06222bd8217eb96e06eb183e6f0cfe3f5dbca6ca16ca`, with its source-bound independent acceptance in that directory.

Use its globally defined harmonic coordinate `H=2(A+C)(A+D)/(2A+C+D)`, with H=0 at denominator zero, and its SAME phase `W=H-100A(A-1)/N`. Its independently accepted local supermartingale applies on `1000<=H<=10^-6 N`, `3N/4<S<=2N`, `N>=200000`.

Set `r=m0N`. The milder present size requirement `N>=2000/m0` implies `r/2>=1000`, N>=200000, and the entrance-to-lower-exit storage gap

```
r/2-2-100m0^2N >=(2/5)r.
```

Indeed `(1/10-100m0)r>=.0999*2000>2`. Thus the source's identical excursion proof, on the shorter horizon h, gives

```
P[H<=m0N/2 before the mass exits or h]
 <=32N^2 h exp(-m0N/1000).                          (12)
```

This is a newly written horizon/size corollary of its accepted LOCAL proof, not a claim that its displayed old service already had these thresholds. It never enlarges the admitted small-H strip. On the complement, `M>=H/2>m0N/4`; since S<=2N, this supplies the conditional receiver with `m=m0/8`.

Substituting `m=m0/8` into (C) gives

```
B_occ=128h(4+33h)/[3m0^2 N(h/6-b)^2].             (13)
```

For (h,b)=(5,1/2), this is `324480/(m0^2N)`; for (8,1), it is `823296/(m0^2N)`.

## 8. Original immigration, death, and unused physical time

Let I be the ORIGINAL rate-one immigration count over the whole deterministic interval [0,h]. For `N>=32h`, Chernoff at log 2 gives

```
P[I(h)>N/16]<=exp(-N/96).                            (14)
```

On its complement, `S(t)<=S(0)+I(h)<2N`, excluding upper mass exits. If S hit `3N/4` at any earlier time, then the continuing endpoint is at most `3N/4+N/16=13N/16`; all unused time is paid.

Otherwise, outside (12),(13), the actual occupation clock reaches bN. The exact random-time-change representation at its first such hitting time is `D_death=Y_D(bN)`, for the original unit Poisson death clock. No conditional Poisson law is assumed.

* For T5, `S(0)<=17N/16` and no low-mass hit require `D_death<3N/8`. With b=1/2, this is contained in `Pois(N/2)<3N/8`, whose probability is at most `exp(-N/64)`.
* For T8, `S(0)<=5N/4` and no low-mass hit require `D_death<9N/16<3N/4`. With b=1, this is contained in `Pois(N)<3N/4`, whose probability is at most `exp(-N/32)`.

Adding these independently valid error bounds proves (T5),(T8). The process is nonexplosive because `S(t)<=S(0)+I(t)` and bounded population gives finitely many states/rates over finite time.

## 9. Capability, costs, and exact remaining limitation

The acquired operation is an actual finite-N, finite-physical-time clearance/occupation certificate from a specified received macro state, not a stationary-preparation or microscopic-mixing oracle. Its count-boundary accounting permits entropy to be used directly as an output clock. The ordinary competitor, entropy inequality, Dynkin/Markov, harmonic persistence, and Poisson tails are components; no novelty claim is made for them individually or for ordinary ODE prediction.

The unconditional T5/T8 bounds replace `h=400/m0^2` with 5/8 using the old admitted floor. The tradeoff is an explicit polynomial occupation-error option of order `1/(m0^2N)`, or the smaller exact-martingale exponential option in Section 6.1, with the displayed constants. At the old minimum population `N=12800/m0^2`, that term exceeds one; the new bound is not falsely advertised as uniformly stronger at every old-admitted N. Larger N or separately paid stronger macro persistence is needed for useful confidence. For N=10^18,m0=10^-6, the polynomial T5 occupation term is .32448; at N=10^19 the exponential option is already at most exp(-23).

The conditional receiver (C) is materially sharper when an actual larger floor is acquired; E around .15N and initial M>=.01N ALONE are not asserted to guarantee that floor over time. No hidden global attraction constant remains in the receiver. No publication, installation, outreach, hardware, or external retrieval occurred. Independent review and any exact macro-entrance composition remain separate obligations.
