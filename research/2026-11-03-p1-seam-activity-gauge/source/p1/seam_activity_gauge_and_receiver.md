# Source-indexed seam payment, exact event-count gauge, and renewal composition

**Scope:** six-species stochastic mass action with all ten rate constants positive; complete nonexplosion is accepted as a programme prerequisite. Uses Sol's fixed high-return law and N1671 global service inequality, and Sol's common-background renewal (commit c53cdb1). No assertion of full positive recurrence.

## A. Exact reaction-count currency

Set `ell=3(A+D)-4(C+F)` and `B0=alpha0+beta0`. The ten reaction increments in the order I0,I1,I2,I3,II0,II1,II2,II3,core forward,core backward are

`(+3,-1,-1,-1,+3,-1,-1,-1,0,0)`.

Thus, pathwise at every physical time, with `N0` counting both constant-input channels and `Jnc` counting all genuine noncore channels,

`Jnc(t)=4 N0(t)+ell(X_0)-ell(X_t)`.

In generator form, `L ell = 4B0-qnc`. For any stopping time T with E T<infinity and E|X_T|<infinity, constant-rate counting compensators and monotone localization give

`E Jnc(T)=4 B0 E T+ell(x)-E ell(X_T)`.

Since |ell|<=4|x|, this is finite and at most `4B0 E T+4|x|+4 E|X_T|`. For any integer r>=1, the pathwise estimate `Jnc(T)<=4 N0(T)+4|x|+4|X_T|` combined with the stopped-Poisson BDG inequality gives polynomial moments whenever T and X_T have polynomial moments. The term N0 counts only genuinely constant sources, not a postulated effective clock. Core jumps can be arbitrarily numerous; none are incorrectly counted as noncore.

For the high boundary B={min(A,D)<N}, write `H_W(y)=E_y[tau_B+Jnc(tau_B)+W(X_tau_B)]`. Then the *exact* gauge reformulation is

`H_W(y)-ell(y)=E_y[(1+4B0) tau_B+(W-ell)(X_tau_B)]`.

**NOTE:** the extra coefficient `1` is retained because H_W here includes physical residence time as well as the noncore event reward. If the high value is defined without residence time, the coefficient is instead `4B0` exactly. The generator identity is `L(H_W-ell)=-(1+4B0)` on high states. This is an algebraic equality, not an inequality or stationary approximation. As W is proper and quadratic, `W-ell` is bounded below and proper (add a finite constant if desired).

The same count gauge applies to any finite family of C3 ports with reactions 0->Ai+Bi->2Ai+Bi+Ci->3Ai+2Bi+2Ci->0 and pair-transferring core edges conserving the sum of Ci. It makes noncore activity a constant-rate input currency plus a state coboundary, regardless of the core graph or pair-transfer rates.

More strongly, for any integrable actual stopping operation with output X_T, the *entire* event-count Foster deficit is equal to a time-only Foster deficit:

`E[T+Jnc(T)+W(X_T)]-W(x)`
`= E[(1+4B0)T+(W-ell)(X_T)]-(W-ell)(x)`.

There is no discarded nonnegative reward, and the same transformed receiver works for all source-resolved endpoints. This exact gauge equivalence is the most reusable composition result here. It does **not** assert that the right side is nonpositive.

The underlying linear-algebra template is a directed m-step reaction circuit with increments nu_0,...,nu_{m-1} and a covector w such that `w.nu_0=m-1`, `w.nu_j=-1` for j>0 and `w.nu_core=0`. If source 0 has constant physical rate lambda0, then `J_count=m N0+w(x)-w(X_t)` and `q_count+L w=m lambda0`. This template is not claimed for arbitrary weakly reversible networks: existence of the covector is a genuine structural restriction.

In fact there is a four-gauge family for the four source types. Write T=A+D and S=B+C+E+F, and define

`ell_0=3T-4(C+F)`, `ell_1=3T-4(B+E)`, `ell_2=-5T+4S`, `ell_3=-T`.

For each j, the j-th source (in either port) changes ell_j by +3, while all other noncore sources change it by -1; every core change is zero. Hence the exact pathwise family

`Jnc(t)=4 N_j(t)+ell_j(x)-ell_j(X_t)` for j=0,1,2,3.

Their sum is identically zero: `ell_0+ell_1+ell_2+ell_3=0`. Source counts therefore differ from the constant-input count by *endpoint coboundaries*:

`N_j(t)-N_0(t)=[(ell_j-ell_0)(X_t)-(ell_j-ell_0)(x)]/4`.

In any invariant probability law for which the corresponding first moments and fluxes are integrable, this forces the expected total propensities of **each** of the four source types (summing the two ports) to equal B0. This is a necessary flux identity, not an existence proof for an invariant probability.

## B. One fully paid ready seam

Use N1671's W=eta1 A^2+eta2 D^2-J1 v1-J2 v2+R S^2, S=B+C+E+F, J1=floor(min(B,C)/2), J2 analog. Let `Cprof` denote N1671's one-unit profile constant. Choose R as prescribed and put `K0=4R-3*Cprof/4>0`.

For ready port i (anchor a_i>=3 and both hidden counts>=2), define terminal T_i, total growth G_i and `P_i=(a_i-2)(b_i-1)(c_i-1)`. The raw factorial divisions give

`G_i/T_i <= g_i/P_i,  (1+a_i) J_i G_i/T_i <= t_i`, with

`g_i=(rate_i0/24+rate_i1/4+rate_i2)/rate_i3`,
`t_i=(rate_i0/6+rate_i1+4*rate_i2)/rate_i3`.

For the second bound the term with rate_i2 uses `(1+a)/(a-2)<=4` and `J/((b-1)(c-1))<=1`; rate_i1 and rate_i0 have stronger denominators. The first uses `(a-1)c>=4` for source1 and `a(a-1)bc>=24` for source0.

N1671's terminal/core service inequality is sharpened directly by its displayed derivation to

`L_service W <= -K0 S (T1+T2)`.

For a growth on port i, the Q increment is at most eta_i(2a_i+1), radial RS^2 increment at most 5RS, positive off-diagonal profile cost at most Cprof*S/4, and the own positive profile cost at most Cprof(1+a_i)J_i. Newly created packet value is nonpositive. Therefore

`L W <= sum_i T_i[-K0 S+(2 eta_i+Cprof)t_i+(5R+Cprof/4) S g_i/P_i]`.

Choose explicit finite `P_*`, `S_*` such that

`(5R+Cprof/4)max_i g_i/P_* <=K0/4`,
`max_i ((2 eta_i+Cprof)t_i)/S_* <=K0/4`.

When both ports are ready, `P_i>=P_*`, `S>=S_*`, it follows that

`L W <= -(K0/2) S T`, T=T1+T2. Increasing S_* further makes this `<=-1-qnc` and reserves a fraction of the margin for a seam jump; this is possible since T has a positive raw lower bound and G/T<=max g_i/P_*.

Let x have A=N-1, D>=N, with N>=6. Only its A source0/1/2 can cross B into high. Write `Gcross=alpha0+alpha1 A B+alpha2 (A)_2 B C`. The high physical residence-and-count law gives, for the already constructed quadratic constant KH,

`0<=H_W(y)<=KH(1+|y|)^2` for all high y.

At any such seam state, all its other one-jump endpoints have value W, including terminal and core endpoints. None is in the double-low corner. Consequently

`L Hhat(x)=L W(x)+sum_cross lambda(x,y)(H_W(y)-W(y))`
`<=L W(x)+Kpartial(1+|x|)^2 Gcross`, with `Kpartial=16KH` sufficient.

Thus the complete source-indexed high-return error is paid whenever

`Kpartial(1+|x|)^2 Gcross <=(K0/4)S T`.

With both ports ready and P_i,S above their thresholds, the resulting common receiver obeys `L Hhat<=-(K0/4) S T`; after the stated S threshold it obeys `L Hhat<=-1-qnc`.

A concrete noncompact sufficient cone: fix any K>=1; choose N additionally large enough that N-2>=P_*. Require A=N-1, D>=N, B,C>=m, E,F>=2, and `D<=K(B+C)`, `E+F<=K(B+C)`. Write `a=N-1`, `h_N=alpha0/4+alpha1*a/2+alpha2*a*(a-1)` and `c_N=4*h_N/[alpha3*a*(a-1)*(a-2)]`. Exact factorial bounds give `Gcross<=h_N BC` and `T1>=[alpha3*(a)_3/4]*(BC)^2`, hence `Gcross/T1<=c_N/(BC)`. Choose m large enough for the ready and physical-time thresholds, and additionally

`m>=max{a, 8*Kpartial*(K+3)^2*c_N*(1+K)/K0}`.

Indeed `1+|x|<=(K+3)S` and `S/(BC)<=2(1+K)/m`, so the seam cost/service ratio is at most `2*Kpartial*(K+3)^2*c_N*(1+K)/m <=K0/4`. This explicit finite arithmetic closes the whole cone, including arbitrarily large hidden inventories and arbitrarily large peer anchors satisfying the stated ratios.

Also, for any fixed ready B,C,E,F with P_A>=P_* and S>=S_*, the states A=N-1 and D->infinity eventually satisfy the seam inequality: Gcross is fixed, high envelope O(D^2), peer terminal T_D is order D^3, and P_D->infinity. Thus the criterion also covers a second noncompact extreme-ratio family.

Reverse A,D obtains the symmetric result.

## C. Neutral renewal glued to *actual* high return

Set a=N-1 and start from any physical state x with A=a. Let T be Sol's first wrong-I-source stop after any number of successful complete I words 0,1,2,3, with the whole D-block/core background live. For each success, A returns to a, although background populations can change arbitrarily. Sol's original theorem proves

`E T^r <=C_r(1+|x|)^(28r)`, and `E(1+|X_T|)^p<=C_p(1+|x|)^p`.

The activity gauge now yields **all noncore activity**, not merely I-source activity:

`E Jnc(T) <=4B0 E T+4|x|+4E|X_T| <= C(1+|x|)^28`.

For the terminal wrong-source state Y=X_T, if Y lies in high, continue with the actual Sol high return to B; otherwise stop immediately. Let T' be the combined time. The retained endpoint lies in B. Strong Markov, Sol's second output moment and the quadratic high bound give the complete finite polynomial receiving contract

`E_x[T'+Jnc(T')+W(X_T')] <=C(1+|x|)^28`.

No high value is charged at every intermediate clean-word crossing, so the artificial repeated seam evaluation disappears. The only high value used is the actual high return after the final wrong source. This is a complete finite-valued stochastic operation with all core, D and source channels live, not a negative-drift claim.

This composed value is proper as a function of initial x: if the final population is >= |x|/2, W at the endpoint is large; otherwise at least |x|/(14) noncore reactions were required because core conserves population and one noncore event changes population by at most seven. This is a genuine polynomially bounded proper receiver on the seam. Its coefficient-one comparison with the input receiver is *not* proved.

## D. A decisive failure of the naive global quadratic gauge

Consider unit block rates, kf=2,kb=1, eta1=eta2=1, W using any fixed R>0 and the N1671 profile. Try a global candidate `W+lambda S ell` with constant lambda. Core leaves both S and ell unchanged.

At x_n=(A=3,B=n,C=0,D=3,E=F=0), only I0,I1,II0 fire. Here W=18+Rn^2 and ell=18. Directly,

`L W=(3n+2)[7+R(2n+1)] =6R n^2+O(n)`,
`L(S ell)=-3n^2+57n+42`.

Thus a nonpositive large-n drift would require lambda>=2R.

At z_n=(A=3,B=C=n,D=3,E=F=0), the I terminal has rate `6(n)_2^2`, while core transfer preserves W's nonradial part exactly at this state because v1=v2=9. The terminal's nonradial part also cancels exactly. Its increments are

`delta W=R(-16n+16)`, `delta(S ell)=14n-68`.

All other channels contribute lower order in n, so

`L(W+lambda S ell)(z_n)=(84lambda-96R)n^5+O(n^4)`.

A nonpositive large-n drift would require lambda<=8R/7. This contradicts lambda>=2R. Therefore **no constant lambda makes W+lambda S ell pointwise Foster on both unready and ready large-inventory faces**, even in the unit-rate diagnostic. The linear activity gauge is a powerful event-accounting identity, not itself the missing global Lyapunov geometry.

## E. What is still missing

The full arbitrary-rate six-species positive recurrence theorem is not established. The high-return seam is now paid at coefficient one on noncompact ready sectors using genuine high-exit envelopes; full noncore count and neutral-word/high composition are acquired globally at each fixed input with polynomial bounds. An unready strip with source1/2 activation can have positive instantaneous W drift and the wrong-source neutral output can carry unpaid growth before downstream terminal service. The remaining operation must continue through the *joint* activation/cascade until these source-induced inventories are actually repaid at the same receiver. No statement here equates polynomial finiteness with an inward drift.

## Primary source bindings

- Sol high elimination and actual receiver: `https://github.com/harjassand/astra-research-knowledge/blob/487bfb76526a4218c71990cd32dda8e0a52478c7/research/2026-11-02-sol-high-region-exit-receiver/source/sol/COMMON_RECEIVER_BY_ACTUAL_EXIT_VALUE.md`
- N1671 global service: `https://github.com/harjassand/astra-research-knowledge/blob/23d0ada35f0340d1460403d23503620e3686c2d0/research/2026-11-03-sol-global-service-receiver/source/sol/GLOBAL_SERVICE_RECEIVER.md`
- Sol common-background source renewal: `https://github.com/harjassand/astra-research-knowledge/blob/c53cdb1c534aef14de99e44532cc69d3935576a7/research/2026-11-03-sol-common-background-renewal/source/sol/COMMON_BACKGROUND_SOURCE_RENEWAL.md`
