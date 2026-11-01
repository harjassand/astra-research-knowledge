# Independent proof review: uniform activation-or-removal block

## Verdict and source boundary

**PASS for the stated uniform OR-target hitting law, with no source correction or constant change.** Exact theorem: `UNIFORM_ACTIVATION_OR_REMOVAL.md`, SHA256 `c1d2ed0820d4f92ea236dcb27eab1cd29e27665f9b1a2e826617cc34e3c3fda8` (8,500 bytes). This earns the mathematical component, not a runtime probability receiver, interior-entry theorem, full population-reduction block, recurrence, or stationary-moment consumer.

The dependency is exactly the accepted full-generator initial-growth theorem SHA256 `90a80f12bfc045350b5254a4c8d731f506da5520ee161ccd9e7cbb11df82329e`, with independent receipt `a1eb22f7376fb8cfd138908629f7242edc164dc721476be0999dde4716de67e8`, review `70cf81fd5d27fe68bc90bf32ac1b21cd254fecfe1e56a049ec28fdb0998d3e00`, and audit manifest `e4e73437f7958c35e339617dc14cef6595c7138cdccc20cbe393336ae3f2a6d8`. Its read-only verifier rechecked all 19 payloads and 4 original-source bindings before this review was sealed. The author's phrase 'pending independent review' is historical; no dependency theorem or code is silently substituted.

Fix a nonnegative integer state with initial total `N>=10^40`. N is this fixed initial total, not a running value recomputed later. Set `S=A+B+C+D+E`, `R=C+D+E`, `M=A+min(C,D)`, `m=floor(sqrt(N)/20000)`, `ell=floor(m/2)`, `T0=10^12`, and `H=8m+T0`.

The accepted target is the first actual occurrence of `S<=3N/4 OR R>=B/100`. The upper exit `S>2N` is a globally active ADVERSE stop throughout the seed phase, every excursion, and the charged phase. Section 3 explicitly stops the construction there. It is not a third service output; it must be included in all later uses of 'main boundary' and is charged once over the original episode. This interpretation is already required by the source's stated stop and its S<=2N calculations.

## 1. All twelve actual channels and exact U marks

Use falling-factorial propensities and the actual factor two on CD->AE. Let `U=E-A/10`, `Z=exp(-U/10)`. The exact marks are:

| Channel | Actual rate | delta U |
|---|---:|---:|
| 0 -> A | 1 | -1/10 |
| A -> 0 | A | +1/10 |
| 2A -> AC | A(A-1) | +1/10 |
| AC -> 2A | AC | -1/10 |
| 2A -> AD | A(A-1) | +1/10 |
| AD -> 2A | AD | -1/10 |
| 2A -> AE | A(A-1) | +11/10 |
| AE -> 2A | AE | -11/10 |
| AE -> CD | AE | -9/10 |
| CD -> AE | 2CD | +9/10 |
| CD -> AB | CD | -1/10 |
| AB -> CD | AB | +1/10 |

In particular both AE losses are retained, their marks are different, and the two CD sources carry total coefficients 2 and 1. No target transition is killed when it crosses the composition boundary. U and Z are global functions, evaluated at the actual target.

Summing rate times mark gives the global polynomial identity

`LU = (17/10)CD+(13/10)A^2-(6/5)A-1/10 + A[B/10-(C+D)/10-2E]`.

Summing rate times squared mark gives exactly

`Gamma_U = (1+A)/100+(123/100)A(A-1)+A(C+D)/100+AB/100+(163/100)CD+(101/50)AE`.

The mark bound is `|delta U|<=11/10`. These are actual full-generator identities, not fluid approximations or identities after deleting failed returns.

## 2. Uniform composition payments and exponential-generator bound

On `R<=B/100`, `(C+D)/10+2E<=2R<=B/50`, hence the bracket in LU is at least `2B/25`. Define

`P=(CD+A^2)/2+(2/25)AB`.

The scalar reserve is valid with slack:

`(13/10)A^2-(6/5)A - (A^2/2-1/2)`

`=(4/5)(A-3/4)^2+1/20 >=0`.

Thus `LU>=P-3/5`. For `r=min(C,D)`, `CD>=r^2` and `A^2+r^2>= (A+r)^2/2`, proving

`LU>=M^2/4+(2/25)AB-3/5`.

This requires no C/D balance. An independent exact residual calculation, writing the nonnegative composition slack as `t=B/100-R`, gives

`LU-(P-3/5) = [(4/5)(A-3/4)^2+1/20] +(6/5)CD+(19/10)A(C+D)+2At`.

For the squared marks, `A(C+D)/100+(101/50)AE <=(101/50)AR<=(101/5000)AB`. Therefore the stated upper envelope

`Gbar=1/100+(31/25)A^2+(163/100)CD+(151/5000)AB`

is valid. One may verify it without discarding a questionable sign: after substituting B=100(C+D+E+t),

`Gbar-Gamma_U = A^2/100+(61/50)A+(201/100)A(C+D)+(101/50)At >=0`.

Also

`4P+1/100-Gbar = (19/25)A^2+(37/100)CD+(1449/5000)AB >=0`.

Consequently `Gamma_U<=4P+1/100<=4LU+241/100`. This pays the adverse AE marks and their variance through the actual AB reserve; no occupation estimate is being assumed.

For any real mark v with |v|<=11/10, Taylor's integral remainder gives

`exp(-v/10)-1 <= -v/10 + (v^2/200) exp(11/100) <= -v/10+v^2/100`.

For example `exp(11/100)<=sum_{k>=0}(11/100)^k=100/89<2`, which proves the constant without a floating approximation. Summing this inequality against all nonnegative actual intensities,

`LZ/Z <= -LU/10+Gamma_U/100`

`<=-(3/50)LU+241/10000`

`<=-(3/200)M^2-(3/625)AB+601/10000`

`<=-M^2/100` whenever M>=4,

because `(1/200)M^2>=16/200>601/10000` in that range. The source discards the additional favorable AB term. At M=4 the claimed estimate already has positive slack. No smoothness issue or cutoff derivative enters this exponential step.

## 3. Exact scales and the re-received initial-growth strip

Write s=sqrt(N). Since s>=10^20,

`m=floor(s/20000)>=s/40000`, `m<=s/20000`, and `m>=1`.

The lower bound follows from floor(x)>=x-1>=x/2 for x>=2. Further, `m+1<=s/20000+1<=s/10000`, hence `N>=10^8(m+1)^2`; this is the exact condition of the accepted source. It remains valid for nonsquare N. Also `m<49N/200`, `ell>=4`, and every integer M>ell satisfies M>m/2.

Before either service output or the adverse upper exit, S>3N/4, R<B/100, and S<=2N. If also M<m, then A<=M<m and

`3N/4<S=A+B+R<m+(101/100)B`.

If B<=N/2 this would give `S<m+101N/200<3N/4`, a contradiction. Thus B>N/2. The initial-growth source's exact global V_N therefore has its full drift inequality on this entire strip with the same fixed N.

If initial M<m, let theta be the first actual M>=m, service output, or adverse upper exit. At all pre-stop states M<m, and every M jump has size at most one. Consequently every actual terminal target, including an upper/lower population exit, has M<=m. The source's lower bound `V_N>=2^(-m)` holds throughout `t wedge theta`, not just on a terminal value already presumed finite. The same stopped exponential-Dynkin argument gives

`P(theta>8m)<=(101/100)exp(-m)`.

If M>=m initially, seed time is zero. A seed hit simultaneous with a service or adverse boundary never suppresses that boundary; no post-seed phase is started outside its valid region. No B-half exit is treated as service by itself. If M<m and B<N/2 at a target, that target cannot remain in the survival/inactive region just shown; the explicitly named boundaries cover it.

The reference N is not changed when S changes, nor is a fresh state sampled at theta. Only the mathematical elapsed clock changes between phases.

## 4. Persistence: actual lower excursions and conditional event counting

Condition on any admitted post-seed stopping state with S<=2N, M>=m, and no service output. A hit M<=ell within the next T0 must be preceded by an actual downward crossing from m to m-1, since all M jumps are -1,0,+1. This covers initial states with M much larger than m as well as exact seed hits.

Index the successive actual entrance times into these excursions. Each is a stopping time. Stop an excursion on M>=m, M<=ell, any service boundary, the global adverse upper exit, or the remaining deadline. At its interior states ell<M<m the B-rich strip proved above applies, so the accepted source gives `LV_N<=-V_N/4<=0`. At entrance,

`V_N<= (101/100)2^(-(m-1))`.

At a lower hit the integer unit-jump property gives M=ell and `V_N>=2^(-ell)`. Optional stopping of the nonnegative V_N therefore gives, conditionally on the complete actual entrance history,

`P(lower hit during this excursion | entrance history)`

`<= (101/100)2^(ell-m+1) <= (202/100)2^(-m/2)`.

Other stopped values need only be nonnegative; none is assigned a fictitious zero value in the generator. The upper exit remains active, and no lower hit after a service stop is charged. The finite horizon and population tube already bound all rates and function values; ordinary finite localization would give the same inequality.

The actual total event intensity is

`qtot=1+A+3A(A-1)+A(C+D)+2AE+3CD+AB`.

An independent coefficient comparison gives `qtot<=3S^2+1`, so on S<=2N it is at most `12N^2+1<=13N^2<32N^2`. The source's 32N^2 bound is therefore conservative. Count only genuine downward excursion entries before the stopping boundaries; this count is bounded by the count of all actual jumps. Its conditional expected value over a T0 window is at most `32N^2 T0` by the stopped compensator identity.

For clarity, this is not a union over a deterministic number of independent attempts. For the j-th actual entrance time theta_j, the indicator that theta_j occurs before the horizon is measurable at theta_j. Conditional optional stopping supplies the same probability bound at that time despite all past failed excursions. Conditional expectation and Tonelli give

`P(any lower-hit excursion) <= E sum_j 1_{theta_j occurs} P(lower hit_j | F_{theta_j})`

`<= (202/100)2^(-m/2) E[# entries]`

`<=65N^2 T0 2^(-m/2)`.

There is no reset, mixing, stationary fiber law, or independence assumption. The intensity budget pays repeated failed returns as well as all other actual channels.

### Uniform absorption of the event-count prefactor

Let y=N^(1/4)>=10^10. Then log N=4 log y<=y: at y=10^10, log10<3 gives 4 log y<120<y, and the derivative of y-4 log y is positive for y>4. Also log(65T0)<33<=y; an exact certificate is `exp(1)>8/3` and `(8/3)^33>65*10^12`. Therefore

`log(65T0)+2log N<=33+2y<=3y`.

Since y>=10^10>1,920,000 and m>=y^2/40000,

`3y<=y^2/640000<=m/16`.

Finally `log 2>=2/3`. This follows, for example, by integrating the tangent bound `1/x>=4/3-4x/9` on [1,2]. Hence

`log(65N^2 T0 2^(-m/2)) <=m/16-(m/2)log2`

`<=-(13/48)m<=-m/4`.

This is a uniform analytic bound for all N>=10^40, not a numerical check at the endpoint. All rounding goes in the stated direction.

## 5. The charged phase and terminal sign

Let zeta be the first service boundary, global adverse upper exit, or lower hit M<=ell after the admitted seed; use the stopped process at `t wedge zeta` for 0<=t<=T0. Before zeta, integer M>ell implies M>m/2 and M>=4, so the actual generator inequality gives

`LZ<=-(m^2/400)Z`.

At the admitted seed, S<=2N and E>=0 imply `U=E-A/10>=-N/5`, hence `Z<=exp(N/50)`. On the event zeta>T0, the actual state at T0 remains inactive and within the tube, so

`U<=E<=R<B/100<=N/50`, and `Z>=exp(-N/500)`.

Thus the nonnegative stopped exponential supermartingale gives

`E[e^((m^2/400)(T0 wedge zeta)) Z(X_{T0 wedge zeta})] <= Z(X_0)`

and therefore

`P(zeta>T0) <= exp[11N/500-m^2 T0/400]`.

Notice the correct use of the lower bound on Z only on the NO-EXIT event; no sign or size of a service terminal value is needed beyond nonnegativity. Values at an actual boundary target are still the global Z. A boundary hit at the deadline is an output, not part of zeta>T0. Stopping and localization are legitimate because the pre-stop tube and its one-jump targets have bounded total, all rates are finite, and the time interval is bounded.

By `m^2>=N/(16*10^8)` and T0=10^12,

`11N/500-m^2 T0/400 <= (11/500-25/16)N<-N`.

Accordingly a post-seed continuation fails to achieve service within T0 only by a lower excursion, a no-boundary deadline, or the adverse upper exit. The first two conditional probabilities are at most exp(-m/4) and exp(-N), uniformly over all admitted seed states and histories.

## 6. Original-episode immigration headroom and nonexplosion

Every internal channel conserves S; only unit-rate immigration increases it and A death decreases it. On the same actual trajectory,

`S(t)<=N+I(t)`

for the original unit-rate Poisson immigrant count I. This is not a new clock attached to the random seed time, and no independence from seed formation or excursion outcomes is asserted.

The deterministic total horizon satisfies

`H=8m+T0<=s/2500+10^12 <=s(1/2500+10^(-8))<s=sqrt(N)`.

Since N>=10^40, sqrt(N)<=N/4, so H<=N/4. An upper exit S>2N by time H implies I(H)>=N (indeed at least N+1 for integer N, but the weaker event suffices). The exact Poisson generating function gives

`P(I(H)>=N)<=2^(-N)E[2^I(H)]=exp(H-Nlog2)`

`<=exp[N/4-(2/3)N]<=exp(-N/3)`.

This single price covers an upper exit in either phase, including any correlation with elapsed time or failed excursions. It is not repeatedly charged or treated as favorable service.

The same domination proves nonexplosion: on any finite time interval the immigrant count is finite almost surely, leaving S in a finite population set. There are finitely many states on that set and bounded total rates, so infinitely many jumps cannot accumulate. This legitimizes the strong stopping-time and compensator uses above. For any nonnegative exponential process, finite localization followed by Fatou supplies the same bounds without assuming terminal integrability in advance.

## 7. Complete event decomposition and final prefactor

States already in the target have tau=0. Otherwise, if the seed-or-boundary phase lasts longer than 8m, charge the initial-growth failure. If it stops by 8m at service, there is nothing to prove. If it stops at the upper exit, charge the single original-episode immigration event. Otherwise it supplies an admitted seed state at an actual time theta<=8m, leaving a T0 continuation whose endpoint theta+T0 is no later than H. Condition on the full state/history there; the uniform lower-excursion and exponential deadline bounds apply. If tau>H and there was no upper exit, this continuation must have had a lower excursion or reached its deadline without a boundary. These alternatives justify the union

`P(tau>H) <=(101/100)e^(-m)+e^(-m/4)+e^(-N)+e^(-N/3)`.

There is a small but important prefactor detail: simply replacing every exponential by the final target rate would give 4.01, not 4. The source's claimed 4 is nevertheless valid because for m>=1,

`(101/100)e^(-m)<=e^(-m/4)`;

indeed exp(3m/4)>=1+3m/4>=7/4>101/100. Also `m/4>=sqrt(N)/160000`, and both N and N/3 exceed sqrt(N)/160000. Each of the FOUR terms is consequently at most `exp[-sqrt(N)/160000]`, proving the exact stated coefficient 4.

No event is missing from this decomposition. In particular a B-half crossing is not silently called removal, the upper total exit is separately charged, and a surviving lower-M excursion is not assumed impossible or independent of previous attempts.

## 8. Strict scope and costs

This acceptance stops at the first actual `S<=3N/4 OR R>=B/100` hit. The latter is a composition inequality, not a guarantee of simultaneous positive B,C,D,E. It includes boundary faces; for example the all-A state has B=R=0 and is already in the target. A state with A=D=E=0 and B=C=N/2 is likewise activated without being interior or having removed population. These are scope witnesses, not counterexamples to the stated target.

No balanced dyadic entrance, macro-positive interior, subsequent persistence, full population-reduction block from every activated point, recurrence, invariant law, or stationary moment has been received. The separately accepted local drift and interior-removal results have their own hypotheses and do not acquire a new stochastic interface from this proof. No physical intensity calibration or state preparation is certified.

The event-count price is an analytic expected-count bound, not permission to enumerate 32N^2 T0 events at unit cost. The constants and N threshold are enormous existence constants, not a practical algorithm claim. Exponentials of rational arguments in V/Z are mathematical functions; there is no frozen production API providing arbitrary-input exact transcendental arithmetic or a comprehensive work-budget receiver. The independent diagnostics use explicit outward rational enclosures only for the six constant jump exponents and do not purport to numerically evaluate the astronomically small final probability.

## 9. Independent checks, replay, and source preservation

`independent_activation_checks.py` imports no author code. It separately enters the twelve channel increments/rates; uses a small standard-library exact sparse-polynomial implementation to prove the two global identities and nonnegative coefficient residuals; checks the global total-intensity envelope; and evaluates the actual exponential generator with outward rational Taylor enclosures. It also tests imbalanced/zero-coordinate states, 14 exact nonsquare/floor-scale cases, min-jump and B-crossing behavior, and every scalar prefactor/log margin used in the uniform proof.

The saved run passed 87,563 exact assertions over 1,950 states and 15,956 enabled jumps, with 876 direct outward exponential-generator checks for M>=4. No floating arithmetic or author generator import was used. These finite assertions supplement the uniform derivation and do not replace optional stopping, event decomposition, or conditional excursion reasoning.

The copied author checker, which requires the already installed SymPy, was also actually replayed in `author_replay/`. Its two global identities, 12 marks, and 1,875 finite diagnostics reproduced the original report byte-for-byte. Author counts remain separate from independent counts. All original source and accepted dependency hashes are bound in the audit manifest and read back. No frozen source or earlier audit was edited, no counterexample was suppressed, and no external source was retrieved.
