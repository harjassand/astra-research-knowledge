# Uniform same-exponent dormant Green for the nonbalanced extension

30 October 2026. Self-contained working proof. No full-network recurrence inference. This replaces no reviewed bytes and is not yet independently reviewed.

Fix m=a0+2>=4, q>m, positive connector rates i,t,d and total seed rate s=k1+k5>0. On D=0, C is frozen. The process has immigration `(A,B)->(A+1,B+1)` at rate i, activation `(A,B)->(A+m-1,B+q-1)` at rate tAB, clearing `(A,B)->(A-m,B-q)` at rate d(A)_m(B)_q, and seed killing at s(A)_m(B)_q. A true seed preserves N=A+C+D, leaves B unchanged, and changes A by -1 or -2. Define H(0)=0 and H(B)=j(m-1)+v when B=j(q-1)+v, 1<=v<=q-1. Set r=C+A-H(B).

For fixed theta>0 and exponent alpha>=0, set `W=exp(theta r)(1+A)^-alpha`. The claim is a uniform constant C_(theta,alpha) such that, from EVERY nonnegative A,B,C,

`E[integral_0^tau_seed W(X_t)dt + W(actual seed output) + sum_section_visits W] <= C_(theta,alpha) W(input)`.       (G)

Section visits are entries to B=q at jump epochs; the initial visit can be included once. For the terminal W, use the conserved total N including newly created D. This is essential: the actual seed is not the reference clearing post-state.

## 1. Independent finite-input values

The pre-seed law is the ordinary connector with enhanced clearing rate d+s, stopped at the first independently seed-marked clearing, mark probability p=s/(d+s). The enhanced connector has three complexes, one linkage, rank two and deficiency zero. Its positive complex-balanced point solves ab=i/t, a^m b^q=i/(d+s), which has a unique positive solution because q>m. Its classwise invariant law is conditional product Poisson.

Nonexplosion does not follow from a fictitious globally linear birth rate. For V=1+A+B, the negative high-degree clearing term absorbs the positive tAB activation term where both A>=m and B>=q. On the complementary strips AB<=C(A+B). Thus LV<=CV, yielding nonexplosion independently. The product-Poisson law has every polynomial-exponential moment.

From each fixed finite input, regeneration at a reachable fixed state in its class yields finite expected pre-seed W occupation and section-visit reward: the classwise return-cycle reward is finite by its invariant polynomial-exponential moment, and each cycle has a positive chance to encounter a seed-marked clearing. Every class can reach an enabled clearing via finitely many immigrations and activation. Starting-state reward is likewise finite by irreducible return-cycle decomposition. A section-entry reward is bounded by the jump-intensity occupation with a polynomial-exponential envelope. This earns actual finite-corner boundary values; it assumes no recurrence for the full nonbalanced network.

## 2. Large A block bound

Choose A0 large depending on theta,alpha and rates. At A>A0,B>=q, births before the next seed/clearing have probabilities O(A^(1-m)) for activation and O(A^-m) for immigration, uniformly in B. On a clearing, r never increases and the inverse-A ratio is 1+O(1/A). A seed terminates; its terminal profile ratio is bounded (indeed 1+O(1/A)).

If a clearing lands below q, include the entire next low-phase approach in the same block. During that approach A only increases. At positive low B, immigration-before-activation has probability O(1/A); at B=0 one compulsory immigration is neutral in r. There are at most q immigrations before a high phase, or a preceding activation. Thus the low approach has expected terminal W ratio 1+O(1/A), bounded W-running cost, and bounded visit multiplicity. An r-increasing wrap is not compulsory: it needs an immigration race at positive B.

After summing the rare high births, the nonseed block continuation norm is at most `1-p+O(1/A)<=rho<1`. Block running, terminal-seed and section rewards have W-normalized bounds C. Stop additionally at A<=A0. Truncated block iteration gives a large-A value bound

`G_high <= C1 + C2 H_head`,

where these are suprema of normalized values on the corresponding regions. Crossing into the head has bounded overshoot and W multiplier. Initial B<q is covered by its low approach. The block proof also pays the initial waiting time; none of the low-phase O(1) waits is mislabeled A^-m.

## 3. B-large bounded-A head

For A<=A0 and B>=B0, collapse the following actual paths into steps:

- A>=m: next seed or clearing;
- 1<=A<m: activation, then seed or clearing;
- A=0: compulsory immigration, activation, then seed or clearing.

Any competing birth is an error endpoint. Intermediate A may exceed A0 but is kept INSIDE the collapsed step until seed/clearing/error. For B0 large, each error probability is O(1/B0), uniformly on the finite A alphabet; all error weight multipliers and A overshoots are bounded constants.

The error-free nonseed endpoint maps are `(A-m,B-q)`, `(A-1,B-1)`, and `(0,B)`, respectively. Each has survival factor 1-p. Their r never increases; A decreases to zero and then remains zero. Therefore the n-step weighted leading kernel P0 obeys

`||P0^n||_W <= (1+A0)^alpha (1-p)^n`.

This proves its Green norm is finite, even if a one-step row sum exceeds one. Leading paths that cross below B0 enter a fixed finite corner and receive the actual values from Section 1. Error endpoints enter the head or high region with bounded overshoot. Multiplication by the earned leading Green gives

`H_head <= C3 + eta G_high + eta H_head`,

where eta can be made arbitrarily small by increasing B0. Choose it so eta<1/2 and, after moving eta H_head, the resulting high/head coupling product is <1. The actual finite-corner constant can grow with B0; this does not affect the small coupling coefficient.

Combine with Section 2 and pass from truncated positive kernels by monotone convergence. This earns a finite uniform normalized value. The finite-input reference proof independently identifies the actual stopped process and rules out circular use of an assumed global Green.

## 4. Terminal marks and rewards

At the true seed, r is unchanged, and A loses one or two with A>=m, so the terminal W ratio is bounded. Both marks are included in s and have fixed conditional probabilities. Every collapsed step contains at most three prescribed events; errors begin a new step. Low approaches contain boundedly many events. Consequently section visits have bounded multiplicity per block/step. In the finite corner, polynomial-intensity occupation pays all visits. This establishes all three rewards in (G).

The proof applies to any fixed theta and alpha, with constants that can be enormous. It does not show a uniform bound as theta varies, practical rate constants, or positive recurrence of the full process once D can evolve and C is no longer frozen.
