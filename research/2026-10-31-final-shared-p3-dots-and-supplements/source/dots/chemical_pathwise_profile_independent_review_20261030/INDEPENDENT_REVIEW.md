# Independent common-seed pathwise-profile review

2026-10-30. Reviewer: `producer-workspace/review_chemical_global_foster`.

## Verdict and version boundary

The exact common-seed clock, operational exponential moment, all-event incoming-profile transport, and physical good-region barrier in `PATHWISE_GRAPH_PROFILE_TRANSFER_V1.md` **pass** independent checking. Its interface to the repaired whole-cycle theorem omits one required estimate: incoming-dependent mean time, used to charge a fast immigration to the first inverse-m profile. Uniform p0 plus terminal profile transport are not, without an argument, a substitute for that bound.

Section 5 below supplies a full independent completion. The author then froze the matching additive `PATHWISE_INCOMING_MEAN_REPAIR_V2.md`, which I also checked directly. **V1 alone has an incomplete interface; exact V1 plus this V2 addendum passes**, including its interface to the repaired six-file whole-profile theorem. This does not retroactively assert that V1 explicitly supplied the missing estimate.

Scope: a0>=2, v>=2, m=a0+v, q>m, fixed dimension and fixed positive coefficients. Every degree-m fast complex contains at least a0 A; the strongly connected graph contains mA and a0 A+vX_i for every reservoir species. Immediate A-producing edges are **not** required. The common qB catalyst and connector `0->A+B->mA+qB->0` remain unchanged. No dormant-face, v=1, arbitrary-rate-control, generic weak-reversibility or novelty conclusion is included.

## 1. Exact inputs

- New pathwise source SHA-256: `3d2299db29e5aaa4c3b393ad2fd7e212dcfb5a31951d5dcc318309e805b23c51`.
- Additive `PATHWISE_INCOMING_MEAN_REPAIR_V2.md` SHA-256: `cf841fb80ca52e83e66ba5a34c3375d13097145781c67a1f2c2ffb2ae79f29d4`.
- Repaired whole-profile receipt: `9a5ccf84b8ef206384403ca10df7371120316c83f7523d2c404dd96d9a0bf550`.
- Strict-power operational clearing receipt: `ffe4918940dd02794a71c5fb653ca390850ce81aa8cddf0080b8d831144f49b9`.

Copies are retained under `inputs/`. The strict-power proof was reread at its actual fixed-graph, all-large-shell scope, including the critical exponent and uniform block survival estimate. The repaired whole-profile result is used only with its explicit inactive-wrap stopping rule and its completed coefficient-one/near-one repair arguments. No previous source or receipt was edited.

## 2. The clock is an exact factorization, not averaging

On A>=a0 put A'=A-a0 and n=N-a0. Subtract a0 A from each composition complex. The residual graph is strongly connected, homogeneous of degree v, and contains every pure vX_i, including vA'. For every residual source z,

`(A)_(a0+z_A)=(A)_a0 (A-a0)_(z_A)`.

Other species factors are unchanged. Fast jumps preserve A>=a0. The actual clearing propensity factorizes as `(A)_m=(A)_a0(A')_v`. Thus, before clearing, physical fast/clearing dynamics are exactly the residual killed chain run with speed `(A)_a0(B)_q`.

For each fixed large shell the speed is finite and bounded away from zero on A>=a0. The time change is therefore well-defined without irreducibility. It is a stopped-fiber identity, not a claim that the entire connector process has one global deterministic clock.

The reviewed pure-source theorem applies to the degree-v residual graph and supplies delta>0 and b=v-1+delta such that

`P(tau_op>t)<=C exp(-c n^b t)`, `E tau_op<=C n^-b`.

For its graph-production exponent L>=1 one may take delta=1/(vL+1), hence 0<delta<=1 and b<=v<m-1. Large N and n are comparable; finitely many small active states are excluded from this asymptotic use.

Physical immigration/activation become state-dependent nonnegative operational hazards `k_I/[(A)_a0(B)_q]` and `k_T AB/[(A)_a0(B)_q]`. Coupling their independent exponential marks to the residual fast path gives their first-event time sigma<=tau_op. No constant operational competitor assumption is needed.

## 3. Operational survival and incoming profiles

Every A-decreasing residual reaction has at least one A' in its source. Its rate is at most `C A' n^(v-1)`. For `f_s(A)=(1+A)^-s`, a positive bounded-jump increment is at most `C_s f_s(A)/A`, including the finitely many small A cases. Hence

`Q_op f_s<=lambda_s f_s`, `lambda_s=C_s n^(v-1)`.

The upper bound allows the wrong drift sign; no directional-production premise has reappeared. The process `exp(-lambda_(2s)t)f_(2s)(A_t)` is a nonnegative supermartingale on the underlying **unkilled** finite-shell path. Independent connector marks enlarge the filtration without changing this property. Localized optional stopping at sigma, then Fatou, gives the corresponding bound at the pre-connector state.

Immigration and activation increase A. At clearing, A_before>=m and the fixed-shift inequality `f_s(A_before-m)<=C_(m,s)f_s(A_before)` applies. Thus

`E[exp(-lambda_(2s)sigma)f_s(A_after)^2]<=C_s f_s(A_in)^2`.

The actual survival estimate gives, for large n,

`E exp(lambda_(2s)sigma)
 <=1+C lambda_(2s)/(c n^b-lambda_(2s))<=C_s`.

This follows by integrating the exponential survival tail; the denominator is positive because delta>0. Cauchy–Schwarz, without any independence between terminal A and sigma, proves the actual full first-connector kernel estimate

`E[f_s(A_after)]<=C_s f_s(A_in)`.                    (M)

For a subevent of probability <=epsilon, applying Cauchy–Schwarz to (M) at 2s gives its f_s-weighted mass <=`C_s sqrt(epsilon)f_s(A_in)`. These are exactly the incoming-profile norms used in the repaired stage enumeration. Constants may depend on each fixed exponent; only finitely many are needed in that enumeration.

## 4. Actual occupations and the good-region barrier

Physical time and A-occupation until the same first connector event satisfy

`T=E integral_0^sigma [(A_s)_a0(B)_q]^-1 ds`,
`U=E integral_0^sigma A_s[(A_s)_a0(B)_q]^-1 ds`.

Both A-dependent reciprocal factors are uniformly bounded on A>=a0. Therefore `T+U<=C N^-b/(B)_q`. Actual event probabilities are k_I T and k_T B U; clearing-first probability tends uniformly to one over B>=q. The actual clearing-output inverse-m moment is at most `C(B)_q T`, by `(A)_m/(1+A-m)^m<=C_m` and the clearing compensator. Thus the uniform reset scale is p0(r)=Cr^-b, not an inherited immediate-production estimate.

For the good-region ratio, fix K growing slowly and start at A>=K. Stop at the first connector or first fast entrance into A<=K/2. Before that stop, T_pre<=2U_pre/K. Put s=a0-1>0 and

`G_K(A)=[(K/A)^s-1]_+`.

It is initially zero and is bounded below by a positive constant at a lower entrance. Only A-decreasing fast edges can increase it. Their operational total rate is at most `C A N^(v-1)`, and their positive G increment is at most `C K^s A^(-s-1)`, including the positive-part kink. Restoring the clock gives

`L_fast G_K<=C(B)_q K^s N^(v-1) A`,

because a0-s=1. Connector killing sends G_K to zero and only improves this upper bound. Stopped Dynkin yields

`P(lower entrance before connector)<=C(B)_q K^s N^(v-1)U_pre`.

At that entrance the fast chain still has A>=a0 and unchanged N,B. Its remaining physical time is uniformly at most `C N^-b/(B)_q`. Strong Markov therefore proves

`T/U<=2/K+C K^(a0-1)N^-delta`.                       (G)

The clocks cancel exactly. This is an actual occupation comparison; it does not insert N into an activation rate. Choosing K=N^gamma with gamma(a0-1)<delta makes the ratio vanish on good inputs. Nothing is asserted for bounded A, where the previous scalar-gap obstruction remains valid.

## 5. Missing interface estimate: full independent completion

The repaired whole-cycle proof charges a **fast immigration** by `C f_m(A_entrance)`, then transports that profile back through earlier stages. Its earlier directional proof obtained this from an incoming-dependent mean bound. V1's listed replacement inputs omit that bound. The following derivation repairs the interface without immediate production.

### 5.1 Survival-weighted operational occupation

At deterministic operational time t, the generator inequality gives

`E f_(2a0)(A_t)<=exp(lambda_(2a0)t) f_(2a0)(A_in)`.

Cauchy–Schwarz with `P(sigma>t)<=C exp(-cN^b t)` yields

`E[f_a0(A_t)1_{sigma>t}]
 <=C f_a0(A_in) exp[-(cN^b-lambda_(2a0))t/2]`.

Since `1/(A)_a0<=C f_a0(A)` on A>=a0, integration proves the stronger incoming-dependent estimate

`(B)_q T <=C N^-b f_a0(A_in)`.                      (O)

No independence of survival and A_t is used.

### 5.2 Low and high incoming A

Work in time normalized by the constant factor (B)_q, retaining its nonnegative competitor killings. Let

`L_N=R N^((v-1)/v)`

with fixed R chosen large. For A<=L_N, (O) implies

`(B)_q T/f_m(A) <=C N^-b(1+A)^v
 <=C R^v N^-delta`,

so the required bound already holds.

For A>L_N, the normalized physical killed generator applied to f_m obeys

`K_phys f_m
 <=C N^(v-1)(A)_a0 f_m-k_D(A)_m f_m
 <=C N^(v-1)A^-v-c0`.

Here A is large, so `(A)_m f_m>=c0/k_D>0`. Choose R so the positive term is at most c0/2. Multiplying f_m by a fixed D gives generator <=-1 above L_N.

Stop at the first connector or first downward fast entrance into A<=L_N. The latter lands in `[L_N-v,L_N]` up to integer rounding, because the residual fast A-jump is bounded by v. At that entrance, (O) bounds the remaining normalized mean divided by f_m by `O(N^-delta)`. Thus D f_m dominates the remaining mean for all large N. Stopped Dynkin above L_N, followed by Strong Markov, gives the high-input bound too:

`T<=C f_m(A_in)/(B)_q` on every large active shell.      (I)

The relevant stopping time is dominated by the already finite first connector time; finite-shell localization has no circular return assumption. Additional competitor killing helps both supersolutions.

Consequently actual fast-immigration probability `k_I T<=C f_m(A_in)` uniformly B>=q. This restores the precise profile charge needed for (E), rather than replacing it with the weaker uniform p0 envelope. All other designated branches are charged by (M), including the repaired inactive-wrap rule.

## 6. Exact interface to the repaired whole-profile theorem

Set `g(r)=p0(r)=Cr^-b` and choose

`0<gamma<min(b/m,delta/(a0-1))`.

Then p0K^m->0 and the actual good-region ratio eta(r), given by (G), tends to zero. The first output moment at B=q still satisfies t<=CT, with the constant catalyst absorbed. The full-cycle argument can now be repeated without an unproved input:

- (M) transports every required inverse-A profile and supplies rare high-activation norms.
- (I) charges fast immigration by the incoming f_m profile.
- The clearing moment and inactive-wrap indicator charge all inactive high entrances; physical seeding is unchanged.
- The exact J(B) count separates nonrare low activations from active high activations and sums unbounded high-B histories.
- The exact immigration/clearing count keeps safe first-clearing paths below their initial r; the near-one terminal supersolution preserves the activation discount.

Hence the actual bad-entry estimate is the same formula with the new p0:

`P[w(r_next)1_bad]<=C K^m[T+p0 U]w(r)`.

The bad-return norm in gw is O(p0K^m)->0. Good-side Neumann leakage divided by U w is at most `C p0K^m(eta+p0)->0`. Thus the corrected composition-dependent section potential is earned from actual kernels, not assumed.

At the section, clearing-first probability tends to one and the pointwise clearing/activation comparison still gives `U>=c r^[-(m-1)]`. Since b<=v<m-1, g is no smaller than an inverse r^(m-1) scale. Repeating the correction directly for the polynomial enlargement r^(m-1)w pays the actual cycle costs and constructs W_r with the same bounded threshold leakage.

The complementary Z proof needs uniformly bounded normalized active T,U, small inactive clearing output, finite active-state access and actual seeding of the unbounded inactive strip. These have all been earned here or are unchanged exact graph/connector facts. Its finite-head and large-strip protocols therefore remain applicable. Nonexplosion is still proved independently by the linear-total-count generator estimate. The two actual values give normlikeness, absorb infinite-strip leakage and yield the same closed-class positive recurrence and every invariant exponential population moment as the repaired theorem, now without immediate A-producing edges.

## 7. Preserved restrictions

This review does not import dormant-face notes, numerical evidence, or a v=1 extension. Common removable seed, homogeneous conserved shell, residual pure-source coverage, strong connectivity, q>m and fixed positive coefficients remain genuine assumptions. The earlier scalar-gap and inactive-wrap failures remain preserved. No external publication or upload occurred, and no novelty verdict is attached to the completed mathematical interface.
