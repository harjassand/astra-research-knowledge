# Complete seed-interrupted dormant section source

30 October 2026. Working proof coupled to DORMANT_GREEN_NONBALANCED_V2.md. No full positive-D return or global recurrence claim.

Start D=0,B=q,A>=m. Stop at the first true seed, or the first subsequent entry to B=q after the initial high connector phase is left. Let sigma denote this stop and w=exp(theta r). The proposed bound is

`E[(w(X_sigma)-w(X_0))_+] <= C_theta w(X_0)(1+A_0)^-m`.       (S)

Seed terminal r uses conserved total composition and its actual B phase. Its B is NOT reset to q. The following proof prices the source as a complete stopped path, not by integrating positive raw immigration drift.

## 1. Exact phase budget

Label low immigrations at positive B<q as L, high immigrations B>=q as I, and high activations as H. A compulsory immigration at B=0 is unlabeled and r-neutral. Low activation is also unlabeled. Before any seed or section return:

- If I>=1, the path has a high-immigration rare factor.
- If H>=2, it has two high-activation factors.
- If H>=1 and L>=1, it has both factors.
- If I=H=0, positive terminal r requires L>=q-1.

For the last assertion, initial clearing sends B=q to B=0 without changing r. Every low activation followed by clearing maps low B=l to l-1 and changes A by -1; this is r-neutral. If a seed interrupts that pair, the activation was r-neutral and no positive r is created. Hence the only positive r event is a low immigration wrap from q-1 to q, requiring at least q-1 noncompulsory immigrations from a B=0 launch; deaths can only increase the number. It is then a section return. Finally, if L=I=0, all immigrations are compulsory and neutral, while activations are neutral and clearings are nonincreasing, so positive r is impossible regardless of H.

Thus EVERY path with positive terminal r lies in

`{I>=1} union {H>=2} union {H>=1,L>=1} union {L>=q-1}`.       (P)

Since q-1>=m and 2(m-1)>=m, its minimum rare-factor degree is m. This handles seed interruptions without inventing a reset phase.

## 2. Uniform tilted block enumeration above half the input

Write a=A_0 and stop additionally at first A<a/2. While A>=a/2, each low positive-B immigration race has probability at most C/a. Each active high phase has activation-before-seed/clearing probability at most C a^(1-m), and immigration-before-seed/clearing probability at most C a^-m. These estimates are uniform over arbitrary B>=q.

Group one low approach, when present, and the following high phase until a seed/clearing mark. The low approach contains at most q immigrations or an earlier activation. High births can be iterated before the mark; their total probability is small. Conditional on a seed/clearing mark, the seed probability p=s/(d+s) is fixed. Therefore a surviving-clear block has weighted continuation norm at most `1-p+O_theta(1/a)<=rho<1`, with the tilt factor exp(theta h) attached only to labeled immigrations. Compulsory immigrations and activations are r-neutral. Clearing can only reduce the tilt.

More explicitly, marking L,H,I by formal nonnegative variables l,h,j, the block bounds are analytic near (1,1,1) and have rare coefficients of orders a^-1,a^(1-m),a^-m. The geometric sum over surviving blocks converges in a fixed neighborhood of (1,1,1) once a is large. Differentiating its nonnegative coefficient series yields the ACTUAL tilted factorial-moment bounds

`E[w_sigma/w_0; I>=1] <= C a^-m`,
`E[w_sigma/w_0; H>=2] <= C a^(2-2m)`,
`E[w_sigma/w_0; H>=1,L>=1] <= C a^-m`,
`E[w_sigma/w_0; L>=q-1] <= C a^(-(q-1))`,

for paths stopped before the half-input boundary. These are joint weighted path estimates. They do not multiply unrelated marginals or impose independence on observed outputs. By (P), they prove (S) on that stopped portion.

## 3. Weighted half-input entrance

On D=0, only clearing lowers A; each clearing lowers it by m. Thus reaching A<a/2 needs at least floor(a/(2m)) clearings before seed. The same TILTED surviving-block norm rho<1, not merely the unweighted seed-mark probability, gives

`E[w_at_half; half boundary reached before sigma] <= C w_0 rho^(a/(2m))`.

At the actual boundary input, continue to seed or section return. The alpha=0 dormant Green from DORMANT_GREEN_NONBALANCED_V2.md bounds the expected terminal weight by C times the ACTUAL incoming weight: a seed is its terminal reward and a first section return is bounded by the sum of all section-visit rewards. Strong Markov therefore bounds the exceptional continuation by `C w_0 exp(-c a)`, which is O(w_0 a^-m). This is a weighted entrance-law calculation, not probability times a separately averaged moment.

## 4. Bounded input

For bounded a, f_m(a) has a fixed positive lower bound. The same uniform alpha=0 Green controls the terminal reward uniformly in frozen C; hence it supplies the finite-input constant. This proves (S), conditional on the independent correctness of the explicit Green proof.

## What is and is not supplied

The signed source is now bounded above by O(w f_m), because E[w_stop-w_start] is at most its positive part. It does NOT yet include a negative useful-activation margin. Nor does it continue a seed through the positive-D processor back to the original section: sigma's seed phase is retained and must be used by that continuation. The accepted occupation-normalized dormant return estimate is therefore relevant, but further complete-cycle composition is still required. No global recurrence follows from (S) alone.
