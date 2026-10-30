# Independent local review: seeded dormant-face triangle

2026-10-30. Reviewer: `producer-workspace/review_chemical_global_foster`.

## Verdict and strict stopping boundary

**PASS for the exact three local files below.** The seeded-D exit kernel, uniform operational clearing means, small dormant-return probability, paired incoming profile, weighted dormant feedback and incoming-dependent physical mean are valid with the stated conventions and completing arguments below.

**This is not a full connector recurrence theorem.** The non-small D=0 block's exponential-residual return operator, coefficient-one global section margin and associated forcing remain open. A local inverse-A profile contraction does not provide that same-exponent global return norm. No general weakly reversible recurrence or novelty upgrade is made.

The operational chain has species counts `(a,c,d)` with n=a+c+d and reactions

```
2a -> a+d       rate k1(a)_2
a+d -> 2a      rate k2 a d
a+d -> c+d     rate k3 a d
c+d -> a+d     rate k4 c d
clearing kill  rate k0(a)_2
```

All five coefficients are fixed positive constants. Active means an enabled fast source; every fast firing preserves activity. The physical interface has a0>=2, A=a+a0, m=a0+2 and the positive common factor `(A)_a0(B)_q`. **All physical time/division claims require B>=q**, as confirmed by the author. The physical first-event episode stops at clearing or either actual connector birth; inactive states are not included in the active-state claims.

## 1. Pinned sources and dependency closure

Source directory: `producer-workspace/chemical_missing_pure_source_20261030`.

| File | SHA-256 |
|---|---|
| `SEEDED_D_EXIT_KERNEL_CANDIDATE.md` | `4370dd036c6b2446f3285b24f6405ff3429c34f2877ff4340ef74aa491598235` |
| `DORMANT_TRIANGLE_UNIFORM_FAST_MEAN.md` | `6e90a213006409b566aa17d512f28213df1af8921945c8bbda2192784e05c641` |
| `TWO_COORDINATE_BRANCHING_PROFILE_CANDIDATE.md` | `a3ac1531255696449791d668025245e48fee36b48b6a4464ede80cbeec988460` |

The author confirmed these bytes frozen. Copies and input hashes are retained here. No other dormant note or numerical output is used. The cited older crude polynomial absorption estimate is independently supplied in Section 2, so this receipt does not rely on an unidentified prior theorem. Previous receipts and source files remain unchanged.

## 2. Finite active-shell absorption and the exact geometric budget

On a fixed finite n-shell, each active state enables one of the three complexes. A complex path to 2a has at most two fast edges, followed by clearing. If x enables source y, every intermediate state `x-y+y_j` is nonnegative and enables the next path edge. All active propensities have a positive fixed lower bound when enabled, and total propensity is at most Cn^2. Thus a prescribed path plus clearing succeeds within at most three events with conditional probability at least cn^-6. Stop an attempt at its first deviation or success. Each attempt has bounded expected duration because an active state always has total rate bounded below. Failed fast jumps remain active. Conditional geometric iteration proves the explicit crude bound

`sup_active E tau_clear <= C n^6`.

No state-level irreducibility or mixing is required. This also establishes all finite-shell means used in subsequent supremum inequalities.

The D-creating edge and clearing have exactly proportional `(a)_2` propensities. Mark their combined clock with independent Bernoulli labels of clearing probability `p=k0/(k0+k1)>0`. Even before proving eventual clearing, the probability of k creations without clearing is at most `(1-p)^k`; stopping earlier only decreases it. Therefore creation count before clearing has a uniform geometric tail. Since creation is the only D-increasing channel and the only channel decreasing R=a+c, this one exact budget controls both exceptional faces below.

## 3. Seeded excursion until clearing or a recorded D exit

Set `J=floor(n^(1/8))`, `K=floor(n^(1/4))`, and start at d=1, arbitrary a. Stop at clearing, d=0 or d>=J. Statements are asymptotic for large n; floors only alter constants.

### Low-A segment

For a<K and 1<=d<J, c>=n/2. The C+D->a+D channel gives positive a drift at least cnd. Adverse contributions are at most C(a^2+ad), so `Qa>=cn` for large n.

For a valid hitting-time proof, first stop the **unkilled fast chain** at a>=K or either D boundary. Its terminal a is between zero and K+O(1), and the positive drift remains valid before that stop. Bounded stopped Dynkin gives expected duration at most CK/n and proves finiteness. Add clearing as an independent hazard; this only shortens the segment. One must not assign cemetery a=0 and retain the same positive drift—that would be wrong.

Compensators now give low-segment D-loss probability at most

`C KJ(K/n)=CJK^2/n`,

and clearing probability before reaching K at most `C K^3/n`.

### High-A segment

Starting at a>=K, stop at clearing, a<K/2 or a D boundary. Until then clearing intensity is at least cK^2, giving mean duration <=CK^-2. The clearing compensator gives `E integral(a)_2<=1/k0`. Since d<J and a>=K/2,

`E integral a d <=C(J/K) E integral(a)_2 <=CJ/K`.

This bounds D-loss probability and the expected number of all aD-channel events. Losing at least K/2 units of a requires many negative jumps. Creation jumps have a geometric tail; the other negative jumps are aD->cD events. Consequently high-to-low restart probability is at most `CJ/K+Cexp(-cK)`. Positive a jumps, including excursions toward the a-dominant face, do not invalidate any estimate.

### Conditional restart and exits

The restart probability tends to zero. Truncating the number of stages and summing the positive kernel bounds yields a bounded expected number of low/high segments, then finite actual stopping time by monotone passage. Thus

```
E sigma <= C(K/n+K^-2) <= C n^-1/2,
P(d=0 exit) <= C(JK^2/n+J/K) <= C n^-1/8,
P(clearing with a<K/2) <= C K^3/n <= C n^-1/4.
```

Reaching d>=J from d=1 requires at least J-1 creations, independently of this restart analysis. Therefore its mass is <=Cexp(-c n^(1/8)). Every exceptional outgoing face remains explicit; none has been assigned a favorable return law.

## 4. Uniform operational means, including the opposite face

### Small positive D and D=0 feedback

The same seeded proof holds uniformly for 1<=d<=J if the upper stop is moved to 2J. The upper exit then needs at least J creations. If M_small is the full clearing mean supremum on this strip and M_0 the active d=0 supremum, the strong Markov property and Section 2 give

`M_small<=Cn^-1/2+Cn^-1/8 M_0+Cn^6 exp(-cJ)`.

At active d=0, a>=2. Only clearing and D creation are enabled, with fixed relative probabilities and mean waiting time <=C. A creation enters d=1. Hence

`M_0<=C+(1-p)M_small`.

The finite supremum inequalities solve to `M_0<=C` and `M_small<=Cn^-1/8`. Finiteness was earned independently, not assumed as part of the solution.

### Logarithmic growth near the D-dominant corner

Let R=a+c and S=a+eta c, with eta<1 close enough to one. Activity implies R>=1; R cannot reach zero because its sole decreasing reaction needs a>=2. The three linear-in-D channels have S jumps +1, -(1-eta), +(1-eta). Exact bounded logarithmic-jump inequalities give

`Q_lin log S >= d/S[c1 a-C1(1-eta)a+c2(1-eta)c] >= c d`.

The creation channel contributes at worst `-C(a)_2/S>=-CR`. Thus `Q log S>=c'n` whenever R<=epsilon n. Stop the underlying fast chain at R>=2M sqrt(n). For large n this whole pre-hit region lies in R<=epsilon n, log S is bounded below by log eta, and its stopped upper value is O(log n). Dynkin gives mean growth time <=C log(n)/n. Clearing only shortens this stage. No stationary A/C fraction is used.

### Bounded killed corrector after growth

For R>=M sqrt(n), d>=J, let `w=1+beta c/R`. The creation contribution to Qw is at most `C beta(a)_2/R`; the reverse creation channel decreases w. The conversion pair contributes exactly

`beta d[k3 a/R-k4 c/R]`.

If a<=epsilon R, this is <=-c beta d. The positive creation term is absorbed by a fixed fraction of clearing killing for large R. If a>epsilon R, clearing has rate at least cR^2, which dominates possible O(d) positive drift once M is large, since R^2>=M^2 n>=M^2 d. Thus

`(Q-k0(a)_2)w<=-c d<=-cJ`.

Stop at clearing, d<J or R<M sqrt(n), setting terminal w to zero. This only decreases generator values. Bounded killed Dynkin proves mean high-stage time <=C/J.

Enter this stage at R>=2M sqrt(n). Reaching its lower-R boundary requires at least M sqrt(n) creations, so its mass is <=Cexp(-c sqrt(n)). Its actual continuation costs at most Cn^6. A d<J exit lands at J-1 and is covered by M_small. Any initial d>=J state either begins above the reserve threshold or first uses the logarithmic stage. Therefore

`sup_active,d>=1 E tau_clear<=Cn^-1/8`,
`sup_active,d=0 E tau_clear<=C`.

### Uniform dormant return probability

From d=1, the seeded exit estimate bounds return to zero by Cn^-1/8 plus the exponentially small upper-exit mass. From any d>=1, a path to zero must first visit d=1, since D jumps have size one. Strong Markov gives

`sup_active,d>=1 P(hit d=0 before clearing)<=Cn^-1/8`.

This is a probability statement, not an assumed integrable cost for an unspecified outgoing face.

## 5. Paired incoming profile across both reservoir faces

Use physical A=a+a0, and for each fixed s>0 choose eta<1 close enough to one. Put

`f_s=(1+A)^-s`, `h_s=(1+A+eta c)^-s`.

For the linear-in-D channels, bounded power-jump inequalities give

`Q_lin h_s <= d h_s/(1+A+eta c)[-c_s k2 a+C_s(1-eta)k3 a-c_s(1-eta)k4 c]`.

Choose 1-eta small so both a and c coefficients are negative. On active positive-D states, a+c>=1 and `(a+c)/(1+A+eta c)` is uniformly bounded below. Hence `Q_lin h_s<=-c_s' d h_s`.

Also

`Q_lin f_s<=d f_s/(1+A)[C_s a-c_s c]`.

On c>=M(1+A), the latter is <=`-c d c f_s/(1+A)`. On the complementary region, f_s<=C_M h_s. Therefore choosing C2 sufficiently large relative to C1 makes

`F_s=C1 f_s+C2 h_s`

have nonpositive linear drift everywhere and a strict negative margin: order d h_s on the complementary region, and order d c f_s/(1+A) on the C-rich region. Since A+eta c>=A, `F_s<=C_s f_s`; this is still an incoming-A upper profile despite using two coordinates internally.

The creation channel decreases A and A+eta c by one and gives `Q_seed F_s<=C_s aF_s`. At clearing the physical output is A_after=a-2. For a>=2 its terminal f_s reward g_s satisfies `g_s<=C_(a0,s)f_s`. Choose C1>=2C_(a0,s), so F_s-g_s>=F_s/2. Consequently

`(Q-k0(a)_2)F_s+k0(a)_2 g_s
 <=Q_lin F_s+C_s aF_s-c(a)_2F_s`.

For a above a fixed threshold, the negative quadratic term dominates. For bounded a and large n, either c is large (the negative dc term is at least order n) or c is bounded and d is large (the negative d h_s term is order n). Thus the inequality is nonpositive on **every active positive-D state** for sufficiently large n, including both reservoir-dominant faces.

## 6. Stopped kernels and actual dormant feedback

Stop a positive-D episode at clearing, first connector birth or first d=0 entrance. That entrance is through aD->2a, so A increases by one; its terminal f_s reward is at most the corresponding F_s boundary value. Connector immigration/activation increase both profile coordinates and their terminal rewards are paid by their killing terms. Restoring the positive physical clock preserves the inequality. Stopped Dynkin gives the actual joint bound

`E[f_s(A_out)]<=C_s f_s(A_in)`                         (P+)

for positive-D inputs. It is not conditional on the observed output.

Time change preserves fast/clearing event order, and extra connector stopping can only reduce the dormant-hit event. Combining the return probability from Section 4 with (P+) at 2s by Cauchy–Schwarz gives

`E[f_s(A_out); d=0 exit]<=C_s n^-1/16 f_s(A_in)`.       (D+)

At active d=0, the first event is clearing, creation or a connector birth. Direct terminal rewards are bounded by C_s f_s. A creation decreases A by one but has a uniformly bounded f_s shift ratio and enters positive D. It is **not** assigned a small probability or profile norm.

Let its profile norm be M_s and the positive-to-dormant norm be epsilon_s(n)=C_s n^-1/16. Truncate the number of dormant/seeded cycles. The two actual kernel equations have direct terms <=C_s f_s and a return-product norm at most M_s epsilon_s(n)<1 for large n. Positive iteration therefore earns the full first-connector/clearing profile bound uniformly over all active inputs, including d=0. No stationary phase law is inserted.

## 7. Incoming-dependent physical time

Take s=m=a0+2. For large a, the negative killed drift above, after restoring the clock, has magnitude at least

`c(A)_a0(a)_2 F_m = c(A)_m F_m >=c'>0`

after normalization by (B)_q. For bounded a and large n, the strictly negative linear term is order n while the common A-factor is bounded below. Thus a fixed multiple of F_m pays unit normalized elapsed time until the positive-D stopping boundary. Setting its terminal value to zero only improves the drift. Therefore

`(B)_q E tau_+<=C f_m(A_initial)`.

At active d=0, the first physical waiting time is at most `C/[(A)_m(B)_q]<=C f_m(A)/(B)_q`. The seeding output has bounded f_m profile norm; positive-D return has the small norm (D+) at s=m. The same truncated two-kernel equations, now with these actual running-time terms, yield

`(B)_q T<=C(1+A_initial)^-m`

for the full first-connector/clearing episode. Fast immigration can genuinely be charged to the incoming inverse-m profile.

Finally, the operational mean bounds and bounded factors `1/(A)_a0`, `A/(A)_a0` imply

```
T+U<=C n^-1/8/(B)_q   from active d>0,
T+U<=C/(B)_q          from active d=0.
```

The second bound is deliberately non-small. It cannot be replaced by the positive-D vanishing scale.

## 8. What is not concluded

The exact local proofs supply an operational seed/return kernel and a physical inverse-A profile/time interface. They do not control the complete connector's exponential-residual return through a non-small dormant block. In particular, an f_s-weighted return contraction and finite moments of separate exits do not imply the required same-exponent global residual norm or coefficient-one section drift.

No global recurrence claim for this dormant triangle is approved by this receipt. Earlier general-WR restrictions, counterexamples, fixed-source assumptions and exact receipts remain unchanged. No external upload or publication occurred. No local mathematical blocker remains in the stated three-file scope.
