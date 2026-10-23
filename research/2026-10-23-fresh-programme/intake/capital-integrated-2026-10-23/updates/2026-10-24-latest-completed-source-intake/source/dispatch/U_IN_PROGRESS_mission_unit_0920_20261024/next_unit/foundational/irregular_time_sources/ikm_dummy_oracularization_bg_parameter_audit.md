# Dummy-question oracularization: exact BG parameter audit

## Scope and conclusion

I checked one primary construction: Ito, Kobayashi, and Matsumoto,
“Oracularization and Two-Prover One-Round Interactive Proofs against
Nonlocal Strategies,” arXiv:0810.0693v1 (2008), Section 4.1, Lemma 8, and
Section 4.3. It does give a two-prover commuting-operator soundness theorem,
but its quantitative gap depends quadratically on the number `Q` of PCP proof
positions. Thus it does **not, by its stated guarantee, turn the BG classical
gap into a constant commuting gap** when `Q` grows. It is not a no-go theorem
for other transforms or for the actual value of this particular game.

For the direct encoding of the repeated full-string BG game described below,
the classical all-win probability transfers with no loss, but `Q=3 k^n` and
the lemma's guaranteed commuting gap is only
`c(1-w)^2/(9 k^(2n))`. This lower bound on the gap is exponentially small
in `n`, so it yields no dimension-independent constant-gap conclusion. If the dummy
transformation is applied only to the base game, `Q=3k`, and its stated gap is
of order `k^-2`; this version is also not a constant-gap result. Neither
calculation proves that the transformed game's actual commuting value is
close to 1.

## Primary theorem and exact query pattern

The source defines a nonadaptive 3-query PCP game by a proof string in
`A^Q`, a distribution on triples of distinct locations in `[Q]`, and a
predicate on the three queried symbols (Section 2.2, “Nonadaptive three-query
PCP games”). Its dummy-question oracularization (Section 4.1) samples two
independent query triples from the PCP distribution, picks one location `q`
uniformly from the first triple as the real consistency question, and picks
one location `q_tilde` uniformly from the second triple as dummy. It sends the
first triple to prover 1 and the unordered-by-role pair `{q,q_tilde}` to
prover 2 (encoded in increasing order). Prover 1 returns three `A` symbols;
prover 2 returns two `A` symbols. The verifier checks the PCP predicate on
prover 1's triple and checks equality of the two answers at the hidden real
location; the dummy answer is ignored. The dummy and real questions have the
same marginal law, and the second prover is not told which is which.

Lemma 8 states, for every such PCP `G` and its transformed two-prover game
`G'`, with `w(G)` the classical PCP value,

\[
w(G)\leq w_{\rm unent}(G')\leq 1-\frac{1-w(G)}{3},
\qquad
w_{\rm com}(G')\leq 1-\frac{c(1-w(G))^2}{Q^2},
\quad c=(1+15\sqrt2)^{-2}.
\]

The co/commuting bound applies to all commuting-operator provers, hence also
to finite-dimensional entangled provers. The answer alphabet `A` does not
appear in the gap bound. The relevant size cost is `Q`, the number of proof
locations. The source itself calls the soundness “weak”; its NEXP corollary
has soundness `1-2^{-poly}` against commuting provers, while retaining
constant soundness against unentangled provers (Theorem 2). This is a useful
warning against reading the two-bit answer result as a constant quantum gap.

## Applying it to BG without losing the repeated classical event

Braverman–Garg's graph game has questions `x,y∈[k]`, and answer alphabet
\[
\mathcal A_k=[k]^r\times[r],\qquad r=k^{1/3},
\]
so one answer symbol has length
`log |A_k| = r log k + log r = Θ(k^(1/3) log k)`. Their Theorem 7.1 and
Lemma 7.2 give, for `r | n`, a classical repeated-game strategy with

\[
\omega_c(G_k^n)\geq \left(\frac{1}{2k^{1/5}}\right)^{n/r}.
\]

One may encode that actual `n`-fold game as a 3-query PCP as follows. Use
three disjoint proof-location blocks, each indexed by a vector in `[k]^n`,
so `Q=3k^n`. At location `A_x`, the proof stores Alice's full `n`-round
answer for input vector `x`; at `B_y`, it stores Bob's full answer for `y`;
the third block `D_t` supplies an ignored dummy symbol. The verifier samples
independent uniform `x,y,t∈[k]^n`, queries `A_x,B_y,D_t`, and checks the
entire `n`-round BG win predicate using only the first two symbols. The
queries are distinct because the blocks are disjoint. Every proof location
has positive query probability. A proof table is exactly a pair of local
deterministic response functions, so the PCP value is
`w(G)=ω_c(G_k^n)`; randomizing the proof cannot increase that maximum.

The first and second transformed provers now answer three and two symbols
from `A_k^n`, respectively. Each such symbol has length
`n(r log k + log r)`, so transformed answer lengths remain
`Θ(n k^(1/3) log k)` up to the constant factors three and two. By the lower
inequality in Lemma 8, the BG repeated classical all-win probability is
retained in the transformed game's unentangled value, with **no event loss**.

But Lemma 8's commuting bound uses `Q=3k^n`:

\[
1-w_{\rm com}(G')\ \geq\
\frac{c(1-\omega_c(G_k^n))^2}{9k^{2n}}.
\]

Since `ω_c(G_k^n)≤ω_c(G_k)=β_k` by taking a coordinate marginal (sampling
the other question pairs as shared randomness), the numerator is bounded
below by `(1-β_k)^2`; BG has `β_k≤k^{-1/20}`. Nevertheless, the theorem's
guaranteed lower bound on the gap decays as `k^{-2n}`. It therefore supplies no constant
commuting gap while carrying this full-vector response table. It may be
possible that this specific transformed game has a stronger actual gap; the
quoted theorem does not establish one.

For `n=1`, the same construction has `Q=3k` and gives the bound
`w_com(G')≤1-c(1-β_k)^2/(9k^2)`. Again, the answer-size independence is real,
but it does not remove the question-position penalty.

## Boundaries

- The source theorem is for an oracularized **single-prover, nonadaptive
  three-query PCP**, not a black-box transformation theorem for arbitrary
  two-player games. The PCP encoding above is an explicit route for BG; it
  enlarges the location universe to index the full repeated input vectors.
- The result proves a soundness upper bound with a `Q^-2` term; it does not
  show the actual transformed commuting value is `1-O(Q^-2)` or rule out a
  stronger analysis.
- Applying the base-game transform and then repeating it is not the same as
  the direct transform of `G_k^n`. No claim is made here that the original
  chunk strategy lifts through repeated hidden real/dummy choices in the
  base-transformed game.
- This is one checked mechanism, not an impossibility result for all
  consistency or commutativity gadgets.

## Primary references

- Tsuyoshi Ito, Hirotada Kobayashi, Keiji Matsumoto, “Oracularization and
  Two-Prover One-Round Interactive Proofs against Nonlocal Strategies,”
  [arXiv:0810.0693](https://arxiv.org/abs/0810.0693), especially §4.1,
  Lemma 8, §4.3, and Theorem 2. The exact parameter bound and definition are
  also visible in the [primary PDF](https://arxiv.org/pdf/0810.0693).
- Mark Braverman and Ankit Garg, “Small Value Parallel Repetition for General
  Games,” ECCC TR14-095 rev. 1, §7, Theorem 7.1 and Lemma 7.2,
  [primary report](https://eccc.weizmann.ac.il/report/2014/095/).

