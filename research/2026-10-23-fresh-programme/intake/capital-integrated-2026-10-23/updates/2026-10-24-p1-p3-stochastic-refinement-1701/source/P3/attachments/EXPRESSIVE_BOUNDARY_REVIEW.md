# Expressive boundary: linear stochastic quotients, species partitions, and fragments

Private bounded theoretical challenge, 2026-10-24. This follows the earlier source and root work; it is not blind. No new model search, worker, performance campaign, or scientific efficacy fixture was used. The small authored network below is a theorem counterexample only.

## Bounded conclusion

Three different comparisons must be kept separate.

1. **Species partitions on the unchanged source:** arbitrary rational-linear quotients are strictly more expressive. On the pinned nominal phosphorylation source, the exact optimum among species partitions preserving the six acquired observables is twelve variables, while the overlapping linear quotient uses six. Both candidates were checked exactly.
2. **Compilation to a globally valid population CTMC with polynomial propensities and the same linear fibers:** even a positive integer observation can obstruct this compilation. A four-channel, nonexplosive mass-action counterexample is proved below. Redundant nonnegative affine linear coordinates cannot repair it.
3. **An executable quotient program on its attainable image, or general fragment/Markov abstraction semantics:** the obstruction does not apply. The polynomial circuit already implements the image-constrained quotient. In the counterexample, a one-line nonnegative guard also gives a globally valid one-variable program. No separation from arbitrary fragment abstractions or a retaining program library has been established.

The defensible candidate contribution remains a finite exact acquisition/refinement operation over rational row spaces. These results do not establish a new notion of stochastic abstraction, a general superiority over rule-based fragment methods, or an architecture advantage.

## 1. Exact species-partition preservation criterion

Let L be a rational observation matrix, and let P record the sums of species populations in disjoint partition blocks. Then Lx can be recovered from Px for every x in N^n if and only if the columns L_i and L_j are equal whenever species i and j share a block.

**Necessity holds even with a nonlinear decoder.** If i and j share a block, the unit population states e_i and e_j have the same partition totals. Any decoder preserving L must give the same answer on them; hence L_i=L_j.

**Sufficiency.** For each block take its common L-column. These columns define a matrix D with L=DP, giving a linear decoder.

Therefore the partition into classes of equal L-columns is the coarsest partition that preserves these observations, before any dynamics is considered. If that partition is itself stochastic, its number of blocks is the exact minimum among stochastic species partitions preserving L.

### Application to the pinned phosphorylation source

The six rows are free E, free F, and the U/E/P/F site counts. Their distinct columns form these twelve blocks:

| Block | Species |
|---|---|
| Free kinase | S0 |
| Free phosphatase | S1 |
| UU | S2 |
| EU or UE | S3, S4 |
| EE | S5 |
| PU or UP | S6, S7 |
| EP or PE | S8, S9 |
| FU or UF | S10, S11 |
| EF or FE | S12, S14 |
| PP | S13 |
| PF or FP | S15, S16 |
| FF | S17 |

The checker directly reparses the pinned source and verifies both fixed candidate row spaces. It groups projected jumps, sums propensities with the source rate parameters kept independent, and checks every gradient coefficient row by exact rational rank.

| Candidate | Rank | Nonzero projected jump groups | Exact gradient-row checks |
|---|---:|---:|---:|
| Acquired overlapping site-count quotient | 6 | 6 | 20 |
| Equal-column species partition | 12 | 24 | 38 |

Thus the comparison is exactly six versus twelve for this source and these observables. This is an information-representation comparison; it is not a runtime claim. Existing fragment descriptions can track overlapping molecular features and may attain the six-variable representation. That possibility is credited rather than assumed absent. The root's noise intervention separately forces the full eighteen-dimensional universal rational-linear refinement, so this nominal comparison is not evidence of a retained compression advantage after that intervention.

## 2. A nonnegative quotient that has no globally polynomial population realization

Consider two source species A,B and these four reactions:

| Reaction | Stochastic propensity |
|---|---|
| 2A → B | 4 A(A−1) |
| A+B → 2A | 12 AB |
| 2B → A+B | 9 B(B−1) |
| B → A | 3 B |

All are ordinary stochastic mass-action channels. With binomial propensity convention, their kinetic constants are respectively 8,12,18,3. Each rate is nonnegative at every nonnegative integer source state and vanishes whenever a consumed population is insufficient.

Define the positive integer observation

\[
y=2A+3B.
\]

Every reaction changes y by −1. Their total propensity is

\[
\begin{aligned}
q(A,B)
&=4A(A-1)+12AB+9B(B-1)+3B\\
&=4A^2+12AB+9B^2-4A-6B\\
&=(2A+3B)(2A+3B-2)\\
&=y(y-2).
\end{aligned}
\]

The image is the additive monoid

\[
M=\{2A+3B:A,B\in\mathbb N\}=\{0,2,3,4,\ldots\}.
\]

On M, q is nonnegative; the projected transition is y→y−1. It stops at y=2 or y=0. This is a universal strong stochastic quotient. The source is nonexplosive because every jump decreases the nonnegative integer y by exactly one, so any path makes at most its initial y many jumps.

### Impossibility proposition

There is no finite population CTMC on all N^k, with fixed integer jumps and globally nonnegative polynomial propensities, whose population state is a nonnegative affine linear function F(A,B) carrying exactly the same information as y, and whose law agrees with F(A_t,B_t) for all source initial populations.

**Proof.** Write F(x)=Cx+d. Because F maps every nonnegative integer population to a nonnegative integer population, d and the columns of C are integral, and the columns of C are nonnegative. The source states (3,0) and (0,2) have the same y, so equal fibers require

\[
3C_A=2C_B.
\]

Hence C_A=2c and C_B=3c for a nonnegative integer vector c. Thus F(x)=cy+d, with c nonzero because F must distinguish different y values.

Every visible transition of F has increment −c. Let Q(z) be the sum of the compiled channel propensities with that increment. It is a polynomial that is nonnegative on all N^k. Agreement with the source for all attainable y requires

\[
Q(cy+d)=y(y-2)\qquad\text{for every }y\in M.
\]

Both sides are polynomials in one variable and agree at infinitely many values, so they agree identically. At y=1 this gives

\[
Q(c+d)=-1.
\]

But c+d is a valid nonnegative integer population, contradicting global rate nonnegativity. This proves the proposition, even with arbitrarily many redundant nonnegative affine linear population coordinates. Extra channels with other increments cannot change this particular grouped-rate contradiction. ∎

The obstruction is not caused by negative source rates, signed observations, explosion, a fixed-initial-state restriction, or unboundedly many reaction channels. It is caused by a gap in the attainable image and the polynomial identity forced by infinitely many attainable points.

### The ordinary program-library escape

The obstruction does **not** prevent a low-dimensional executable quotient. On its actual state domain M, the ordinary circuit `q(y)=y*(y-2)` is already correct.

There is also a globally valid one-variable guarded implementation:

```python
def rate(y):
    return max(0, y * (y - 2)) if y >= 1 else 0

# The only jump is y -> y - 1.
```

It agrees with the quotient on M, is valid on every nonnegative integer y, and is nonexplosive because it only decreases y. The previously unattainable state y=1 simply becomes another absorbing state. Thus the counterexample separates globally polynomial population-rate syntax from image-constrained or guarded programs. It does not separate the construction from a retaining program learner or compiler with ordinary branching.

No compilation that retains the entire original source state is excluded either. Allowing arbitrary extra hidden information would make a broad polynomial-overhead simulation claim immediate from the original source itself; that is not a comparison of equally informative quotient representations.

## 3. What “proper nonnegative” changes

The terminology must be specified.

- If **proper** means a disjoint partition of species with unit-weight sums, the observation class is precisely the species-partition class. On mass-action inputs, established species-equivalence theory already characterizes this class. Restricting both candidates and outputs to it removes the expressive distinction.
- If **population-like** means only nonnegative integer or rational rows, weighted or overlapping observations remain possible. Both the six-row source quotient and L=(2,3) meet that broader condition. The two strict boundaries above survive it.
- If a framework permits arbitrary functions of fragment counts, image constraints, guarded rates, or additional retained state, it is a broader comparison. The present propositions do not exclude such implementations. A blanket claim that rational-linear lumping strictly extends all fragment or program representations would be unsupported.

## 4. Primary-source boundary check

[Cardelli et al., 2021](https://arxiv.org/pdf/2101.03342), Definition/criterion (1) and the reduced-network construction, explicitly uses disjoint species-block sums and ordinary mass-action networks. The source twelve-versus-six comparison is directly against that stated observation class.

[Feret et al., 2010/2012](https://arxiv.org/pdf/1011.0496), Definitions 15–18, distinguishes concrete Kappa fragments, quotient classes of valid mixtures, and a general abstraction of weighted transition systems. Its abstract state set is not stipulated to be every arbitrary fragment-count vector. Therefore the missing-image-state counterexample does not prove separation from that framework. Its particular weak/reconstructive criteria also should not be identified with every strong stochastic quotient. The [2013 author summary](https://www.di.ens.fr/~feret/publications/IJSI.shtml) explicitly describes weak stochastic fragment semantics; no stronger claim about that full framework is inferred here.

The root already compiles a verified quotient into finitely many jump vectors and factored circuits q_delta(Ry), with a supplied valid initial lift. This is an executable structural description on its image. Whether a particular Kappa fragment syntax discovers or expresses the same quotient with polynomial overhead requires a separately fixed syntax, encoding size, domain convention, and certification contract. The bounded results above settle the unchanged-source species-partition comparison and one precise polynomial-population boundary; they do not settle that more general compilation question.

## Files and verification

- `verify_expressive_boundary.py`: standard-library exact checker; no root implementation imported.
- `EXPRESSIVE_BOUNDARY_CHECKS.json`: source matrices/groups/check counts and the exact counterexample identity.
- Source Git blob SHA1: `2cd6d9f9238b5e26ad87e8543c84a0fc078d43c0` at pinned CLUE commit `0576e9b8477bc511e3fea29a3c296c5d30b688aa`.

The checker completed successfully. Its source comparison is calibration on an exposed independent model. The four-channel example is a proof boundary, not evidence of scientific efficacy, acquisition repayment, or a learner advantage.
