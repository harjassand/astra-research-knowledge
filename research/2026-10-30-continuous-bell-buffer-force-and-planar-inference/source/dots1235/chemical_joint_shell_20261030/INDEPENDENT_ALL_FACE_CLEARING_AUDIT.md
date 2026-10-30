# Independent audit: all-face factorial drift and bounded-oscillation clearing

Reviewed 2026-10-30. Sources:
- `UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME.md`;
- `producer-workspace/BOUNDED_OSCILLATION_KILLED_FIBER_LEMMA.md`.

**Verdict: both results pass under their stated structural hypotheses.** The first supplies those hypotheses for the specified strongly connected homogeneous fast graph containing every pure complex. Neither result is a mixing theorem or a global recurrence statement for the coupled process.

## 1. The boundary margin really covers every simplex face

For a proper nonempty coordinate support S, let U be the complexes supported in S. U is nonempty because S contains a species and its pure mX_i complex is present; U is proper because a missing species has a pure complex outside U. Strong connectivity makes every vertex in U reach an edge leaving U. Thus the restricted finite complex graph is transient when exits are killed, including cases where U itself is disconnected.

At a point of the corresponding face, write z_y=t^y. The homogeneous fractional-factorial functional is exactly the killed functional on U: an edge from zero source contributes zero, an edge leaving U contributes its negative source loss, and internal edges give z_y^(1-alpha)z_y'^alpha-z_y. Normalize by Z=sum_{y in U}z_y. The finite killed-complex lemma supplies a strictly negative normalized margin for sufficiently small alpha, uniformly on its closed simplex. There are finitely many coordinate supports, so a common alpha works for all of them.

Crucially, normalization does not hide a vanishing factor. Some coordinate is at least 1/k, and its pure complex belongs to U, giving Z>=k^-m (indeed a stronger bound is available). Therefore E_alpha has a uniform absolute negative margin on the entire composition-simplex boundary. Continuity gives a fixed boundary neighborhood with the same sign. The already audited homogeneous factorial limit is uniform on every integer composition, including disabled counts. It transfers this margin to LV/V<=-cN^m whenever min x_i<=epsilon N for all large N. A fixed positive compact coefficient box is handled by the uniform finite killed-complex lemma and uniform finite-product errors.

This argument does not merely check vertices, assume all face coordinates grow, or require a stationary distribution on a supported subgraph. The pure-complex and strong-connectivity hypotheses are doing substantive work.

## 2. Exact entropy range and stochastic interior entrance

The multinomial coefficient is between 1 and k^N, so

    -alpha N log k <= log V_N-alpha log N! <=0.

The displayed U_N is therefore nonnegative and bounded above by alpha N log k, exactly. Its shellwise constant terms disappear under L_N. The pointwise inequality L log V<=LV/V is the termwise log u<=u-1 inequality, with no integrability issue on a finite shell.

Stopping at the interior set gives cN^m E(tau wedge t)<=U_N(x)<=CN. Monotone convergence proves the O(N^(1-m)) hitting-time bound. It also rules out a closed boundary class at those large N; interior accessibility is a consequence of the actual drift certificate, not an extra assumption. Choose epsilon smaller than 1/k and increase the large-N threshold as necessary.

## 3. Killed supersolution and root's stronger survival estimate

For f=1+U_N/N, 1<=f<=1+alpha log k. Outside the interior,

    (L_N-kill)f<=-cN^(m-1).

Inside it, A>=epsilon N makes the clearing rate at least c'N^m for sufficiently large N. The parent note's global bound |L log V|<=CN^m log(N+1) is sufficient: after division by N, the killing term dominates its N^(m-1) log N upper bound.

The sharper root interior hypothesis is also earned here. At an interior source and every bounded reaction shift, each factorial log factor is log N+O(1). Conservation cancels the total log N coefficient because sum_i nu_i=0. Thus each log-V jump is O(1), while total rate is O(N^m), giving L log V<=C_1N^m on the interior. This establishes the root lemma's assumption 3 without a logarithmic loss.

For the root's general conditional lemma, its algebra is correct. Outside C_N one has (Q-k)f<=-c_0N^(m-1). Inside, the bound is <=C_1N^(m-1)-c_1N^m. For large N and after using the bounded range of f, both imply

    (Q-k)f<=-c_2N^(m-1) f.

The positive finite killed semigroup then gives P_t^kill f<=exp(-c_2N^(m-1)t)f. Since 1<=f<=1+C_0,

    P_x(tau_clear>t)<=(1+C_0)exp(-c_2N^(m-1)t).

Integration yields the uniform mean bound. No conservative-chain irreducibility or spectral mixing gap is needed. The same conclusion holds under adapted coefficient controls if the generator inequality is common to the coefficient box, using the killed exponential supermartingale instead of a time-homogeneous semigroup.

The root's more general oscillation formula with fixed linear fugacity is also correct: factorial oscillation is at most alpha N log k and the linear term has range N(max b_i-min b_i). That formula does not, by itself, supply boundary drift for arbitrary fugacity; the root note correctly keeps that as a separate hypothesis.

## 4. Common catalyst and competing events

For fixed N,B during the conservative episode, multiplying both fast rates and clearing by a_B=(B)_q is an exact time change. The exponential decay rate gains that factor, and the mean bound is divided by it. A finite bound therefore requires B>=q. For B<q the whole common-clock process is disabled, and no finite clearing claim is available from this lemma.

The coupled connector must not be included in the conservative generator without accounting for its changes of N,B. Stop additionally at the first immigration or activation and assign that event cemetery value zero. This only adds a nonpositive term to the supersolution generator, so the same stopped-time bound applies. At fixed active N>=m and B>=q, the competing total intensity is <=C(1+NB), yielding

    P(birth before clearing)
       <= C(1+NB) N^(1-m)/(B)_q
       <= C B^(1-q) N^(2-m).

Bounds may be truncated at one. This is an actual hazard/stopped-process estimate, valid compositionwise, not a frozen equilibrium average. Subsequent changes of N or B require a fresh conditional application; neither note silently includes them in the fiber process.

## 5. Small-state qualification

For sufficiently large N, all compositions are covered. For the finitely many smaller N, the extension is only over ACTIVE STATES/components: complex-path access gives finite clearing time there. A shell can contain both active states and inactive holes, as the earlier N=3 example demonstrated. Inactive states have no fast move and no clearing because A<m, and cannot be included in a finite clearing-time supremum. The large-N formulas in the source are correct; wording about small “active shells” should be read or amended to active-state restrictions.

## Scope

This proves a dimension-independent exponent O(N^(1-m)) for each fixed graph/dimension, with graph- and dimension-dependent constants, and exponential killed survival on that scale. It does not imply equilibrium mixing, a uniform spectral gap for the conservative chain, or full coupled-network recurrence. The subsequent physical competition/gluing obligations remain separate.

## Reviewed source hashes
e69b10c97b53a7d98d2219c0adce38957a6ee5640a60c8db22a69da5b491cd04  chemical_joint_shell_20261030/UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME.md
aeed1fe99558de772a37003be1f25631440075d677d12274365a00eb703ac501  producer-workspace/BOUNDED_OSCILLATION_KILLED_FIBER_LEMMA.md

### Corrected v2 receipt

Reviewed the separate `UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME_V2.md`; its SHA-256 matches the supplied bf2dfd46e12d16bb6f18ab2f8471c152a9243f08b5bcd57e9e3fb670fd60339a. The only mathematical-scope changes explicitly restrict small-N enlargement to active states/components and require B>=q for finite catalyst-rescaled clearing times. The example 2A<->2C at N=2 with inactive (1,1) correctly illustrates the distinction. Both review qualifications are resolved. Final verdict on v2 and the root conditional survival lemma: **pass**. The pinned original was not changed.

Corrected source hash:
bf2dfd46e12d16bb6f18ab2f8471c152a9243f08b5bcd57e9e3fb670fd60339a  chemical_joint_shell_20261030/UNIFORM_FAST_INTERIOR_AND_CLEARING_TIME_V2.md
