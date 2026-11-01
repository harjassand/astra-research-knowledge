# Independent exact receipt: regularized weighted source storage

Source: `../REGULARIZED_WEIGHTED_SOURCE_BUDGET.md`, SHA-256 `38973f8baacbadb5c8fdf63cac93e2aed49b7831883cd4c3943aff3e3ac10b2b`.

**PASS. No repair required.** The literal full-generator identity, drift inequality, every enabled jump, stopped bracket, budget tail, and uniform occupation constants are correct. This is a conditional source budget from the actual raw corner and original horizon. Its gate admission, actual timing/clearance and any later-start version remain separate. The source was not changed.

## 1. Exact full-generator calculation

Write `H=T³`, `w=E+H`, `phi=H²/w²`, and `W=H²[A/w²+k/w]`, with `k=8/5`. The twelve rates, in the fixed reaction order, are

`1,A,A(A-1),AC,A(A-1),AD,A(A-1),AE,AE,2CD,CD,AB`.

All actual A marks are `+/-1`. The only E-changing channels are:

| Channel | Delta A | Delta E |
|---|---:|---:|
| `2A->AE` | -1 | +1 |
| `CD->AE` | +1 | +1 |
| `AE->2A` | +1 | -1 |
| `AE->CD` | -1 | -1 |

For E-increasing rows, the exact W mark is `Delta A*phi+(A+Delta A)d_+phi-k alpha_+`. For E-decreasing rows it is `Delta A*phi+(A+Delta A)d_-phi+k alpha_-`. All other rows have mark `Delta A*phi`.

Summing these twelve literal marks times their actual rates gives exactly the source's displayed identity. In particular the two E-consuming rows together contribute `2A²E d_-phi+2kAE alpha_-`; their coefficient is the actual count E, not `w`. The only rate-two edge is `CD->AE`.

The three displayed normalized ratios are exact. In addition, `|d_+phi|/phi=(2w+1)/(w+1)²`.

## 2. Drift and all scalar comparisons

For `w>=H>=1000`,

`w(2w-1)/(w-1)²<=5/2`,
`alpha_+/phi>=100/101`, `alpha_-/phi<=100/99`.

The first inequality is certified by `(5/2)(w-1)²-w(2w-1)=(w²-8w+5)/2>=0`; the other two reduce to `w>=100`.

Since `E<=w`, the positive derivative term is at most `5A²phi`. Meanwhile the base term, after `A(C+D)=2AL-2A²`, is

`phi[1+2A+2AL-5A²-AB+3CD]`.

The quadratic terms cancel in the required upper bound. The d-plus terms are nonpositive: their coefficients are `(A-1)A(A-1)>=0` and `2(A+1)CD>=0` on actual nonnegative integer counts. The remaining negative a2 term is also favorable. Finally

`3-2k(100/101)=-17/101`.

These facts give the displayed intermediate drift inequality. The admitted caps imply

`(2+2L+2k(100/99)E)/B`
` <=[2/10^5+1/2500+16/495]/(9/10)<1/20`,

so `GW<=phi-(19/20)AB phi-(17/101)CD phi` uniformly for `T>=10`. No A/L or imbalance bound was used.

## 3. Every enabled jump, including adverse targets

The increment bounds are

`|d_+phi|/phi<=2/w`, `d_-phi/phi<=(5/2)/w`,
`alpha_+/phi<=1`, `alpha_-/phi<=100/99`,
`(A+1)/w<=2+1/1000`.

For every E-increasing enabled row, the normalized absolute mark is at most

`1+2(2+1/1000)+8/5=3301/500<8`.

For every E-decreasing enabled row, it is at most

`1+(5/2)(2+1/1000)+(8/5)(100/99)=301699/39600<8`.

Rows with unchanged E have absolute mark exactly phi. These bounds use the **pre-jump** gate but include the complete physical successor weight and its changed denominator; they do not require the successor to remain admitted. Active E-consuming rows have `E>=1`, so their target is a nonnegative count state, with `w_target>=H>=1000`. All actual target storages remain strictly positive. Thus neither an exit overshoot nor a singular E=0 target is omitted. Disabled rows are not treated as physical jumps.

## 4. Full rate and bracket

The displayed `q_A` is the sum of all twelve actual rates (and also the bracket rate for A, whose marks all have square one). The first rate comparison has nonnegative slack

`[1+AB+A(3L+2E)+3CD]-q_A=A(L-A)+2A>=0`.

The caps give `(3L+2E)/B<=103/4500<1/20`, proving the second comparison. Since `phi<=1`, every squared W jump is at most `64phi²`, so

`q_W<=64phi[1+(21/20)AB+3CD]`.

The largest source-coefficient ratio is `3/(17/101)=303/17`, which also dominates `(21/20)/(19/20)`. Hence, at the same actual stop,

`<M_W><=64[t+(303/17)Q]<=64[4T+(303/17)Qbar]`.

This is a predictable-bracket statement for the stopped process itself, not a bracket bound after conditioning on favorable histories.

## 5. Stopping, positivity and uniform Freedman tail

Start at the actual integer corner `A=E=0` (with reference N matching the count preparation), where `W_0=(8/5)T³`. Stop at the first Q-budget hit, original time `4T`, or any actual domain exit. The compensator Q is continuous and nondecreasing, so it has no budget overshoot: `Q_stop<=4T³`. The drift inequality holds before this stop, and globally positive W is evaluated at its actual terminal state.

On a budget hit before the other stops,

`M_W>=4T³-(8/5)T³-4T=(12/5)T³-4T>=2T³`.

For `T>=10`, the stopped bracket satisfies

`<M_W>/T³ <=64[4/T²+(303/17)4]`
`              <=1940288/425<4600`.

The jumps are bounded by eight. Thus one-sided Freedman at `x=2T³`, `v=4600T³`, `j=8` gives

`P(budget hit)<=exp[-(3/6908)T³]<=exp(-T³/2500)`.

Both numerical comparisons are exact and uniform over `T>=10`. All initial storage and original-horizon terms are included. Domain exits are not silently declared successful service; simultaneous adverse exits belong to the separately charged failure accounting. Finite-horizon population/Poisson domination justifies the actual stopped Dynkin martingale as in the preceding received model components.

## 6. Uniform source-time tails and receiving scope

At the same stop, Q bounds the occupation integrals pathwise:

`integral A phi dt <=4T³/[(19/20)(9/10)T^5]=800/(171T²)`,
`integral CD phi dt<=4T³/(17/101)=(404/17)T³`.

The inequalities include the stopped paths at budget/failure exits, but do not extend their time domain after the stop. No independent Poisson fiber law or restarted source preparation is assumed.

The additional gate is exactly equivalent to the proposed unbuffered lower barrier:

`A/(E+T³)<=2` if and only if `U0=E-A/2>=-T³`.

The source correctly does **not** assert that this barrier has been acquired from the raw corner. A later entry must use its actual storage and the remaining original horizon; it cannot automatically reuse `(8/5)T³` as its initial charge. The regularization changes only the test function, never any actual reaction rate.

No mathematical repair was required. Executable exact checks reconstruct the full generator and every mark, certify all scalar constants, and bind the reviewed source. No dependency/cache experiment or new source retrieval was performed.
