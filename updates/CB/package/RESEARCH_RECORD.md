# Full union-closed sets conjecture: unresolved investigation

**Research session:** 10 October 2026, Australia/Brisbane.  
**Mission status:** unresolved. No foundational mathematical breakthrough is established.  
**Universal assertions introduced below:** unproved.  
**External mathematical verification / historical priority:** not established.

This record preserves a proof attempt, its rejected steps, and reproducible finite tests. It is not a manuscript claiming a resolution of Frankl's conjecture. Neither the number of tests nor the exact arithmetic changes that status.

## 1. The actual target

For every integer n >= 1 and finite family F of subsets of [n], assume:

1. F contains a nonempty set;
2. A union B belongs to F whenever A and B belong to F.

The target is to prove that some coordinate i belongs to at least |F|/2 members of F. This is the unrestricted union-closed sets conjecture. The family {empty set} is excluded. A singleton family containing a nonempty set satisfies the target directly.

The investigation screened union-closed sets, Komlos-type vector balancing, and general polynomial identity testing before focusing on the full union-closed conclusion. No claimed resolution in the other two directions is made. Improving a constant below 1/2 was not adopted as a substitute objective.

## 2. Pinned prior-art comparison

### Repository revisions actually accessed

- Astra: `8aed7fd74eb14622ed5a0a3635a799374296e32a`.
- OpenAI/math: `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

Astra navigation was discovered at the pinned root and followed through `00_START_HERE.txt`, `agent/topics.txt`, `agent/routes.tsv`, and the relevant review/status cards. The entry point reports 604 scoped cards and explicitly distinguishes source-derived claims from certification. No theorem was accepted merely because a repository listed it.

The closest inspected Astra material was:

**N376, regular antichain generators and rare elements.** The review card describes a family of graph-star unions with an arbitrarily rare central coordinate, despite regular, irredundant antichain generation. It also identifies an abundant petal coordinate. This is an auxiliary counterexample to an every-coordinate assertion, not to the existential Frankl statement. The current investigation did not extend that construction or treat its status label as independent proof verification.

**N501--N506, self-coupled join reachability.** N506 and its status JSON were inspected. The original note's rendered UTF-8 route, `web/pages/d-7cab6fa4a5c68622.html`, was subsequently located and its main formulation and explicit Frankl limitation were read. The literal historical source path and the listed original object path returned 404; this does not mean the rendered source was unavailable. The source states that the all-family half-frequency inequality is still missing and that uniformity already maximizes entropy on the union-closed support. Its tight-cut reachability theorem does not supply the necessary strict entropy comparison. This investigation imports none of that theorem's conclusions as proof premises and does not claim to have audited the entire note.

The pinned OpenAI README and manuscript map were consulted. Targeted searches of the map for `Frankl` and `union-closed` returned no matches. That is a limited catalogue observation, not a certificate that no equivalent statement occurs anywhere in the repository.

### Contemporary primary literature

[L1] Simone Costa and Ankan Sadhu, *Beyond Liu's 0.382709 threshold for the union-closed sets conjecture*, arXiv:2610.02295v1, submitted 1 October 2026. The preprint reports the lower bound 0.3828852549667978 through protocols within Liu's framework. Its numerical/computer-assisted proof was not independently replayed here. The full 1/2 conclusion is not supplied by this result.

[L2] Jingbo Liu, *Improving the Lower Bound for the Union-closed Sets Conjecture via Conditionally IID Coupling*, arXiv:2306.08824v1. This distinguishes the sharp iid-coupling constant (3-sqrt(5))/2, further dependent-coupling improvements, and the then numerically supported 0.38271 threshold. It would be incorrect to call (3-sqrt(5))/2 a barrier to every entropy argument.

[L3] David Ellis, *Note: a counterexample to a conjecture of Gilmer which would imply the union-closed conjecture*, arXiv:2211.12401v1. Its abstract was inspected as a warning against promoting a plausible stronger entropy assertion to a theorem. No detailed construction from this paper is imported.

The proposed tests below use globally frequency-ordered projections or first-difference counts. They are not another optimization of the scalar coupling constant. However, a different formulation is not proof of historical originality, and no priority claim is made.

## 3. Notation

Let m=|F|. Let X be uniform on F, represented as a Boolean vector. Set

\[
c_i=|\{A\in F:i\in A\}|,\qquad p_i=c_i/m.
\]

Choose a coordinate order with p_1 >= ... >= p_n. Ties may be broken arbitrarily. All Shannon entropies in the mathematical discussion are in bits.

## 4. Main attempted inequality: ordered Shannon information

Define

\[
h_i=H(X_i\mid X_1,\ldots,X_{i-1}),\qquad
S(F)=\sum_{i=1}^n(2p_i-1)h_i.
\]

**Unproved assertion S:** every union-closed F satisfies S(F) >= 0.

If established for all n, this would imply the complete target. For m>1, the chain rule gives sum_i h_i=log_2(m)>0 and all h_i are nonnegative. If every p_i<1/2, then every coefficient is strictly negative, so S(F)<0. The singleton case is handled separately.

This implication is elementary. It does not establish assertion S and is not claimed as the requested breakthrough.

### 4.1 Why sorting is mathematically justified

For an arbitrary fixed law, compare two adjacent coordinates i,j after a previously revealed set T. Let their fixed weights be w_i=2p_i-1 and w_j=2p_j-1. The difference between revealing i then j and revealing j then i is

\[
\begin{aligned}
&w_iH(X_i\mid X_T)+w_jH(X_j\mid X_T,X_i)\\
&\quad-w_jH(X_j\mid X_T)-w_iH(X_i\mid X_T,X_j)\\
&=(w_i-w_j)I(X_i;X_j\mid X_T)\\
&=2(p_i-p_j)I(X_i;X_j\mid X_T).
\end{aligned}
\]

The histories of all subsequent coordinates have the same joint information after either order, so their contributions are unchanged. Since conditional mutual information is nonnegative, swapping an inversion cannot decrease the score. Repeated adjacent swaps prove that descending frequency maximizes this weighted entropy expression over fixed coordinate orders. Ties do not change the score.

This argument uses no union closure. Its limitation is exactly that it establishes an optimizer, not the sign of the optimum.

### 4.2 Equivalent integral identity

Let T_t={i:p_i>=t}. Except at finitely many endpoints, T_t is a prefix of the selected order. Therefore

\[
\int_0^1 H(X_{T_t})\,dt
=\sum_i p_i h_i,
\]

because the term h_i is included for exactly an interval of length p_i. Consequently assertion S is equivalently

\[
\int_0^1 H(X_{T_t})\,dt\ge\tfrac12 H(X).
\]

This identity is proved; its claimed universal lower bound is not.

## 5. A counting-based alternative

For distinct ordered pairs (A,B) in F^2, let their first differing coordinate be taken in descending frequency order. Let D_i count the ordered pairs whose first difference is i. Then

\[
D_i\ge0,\qquad\sum_iD_i=m(m-1).
\]

Define

\[
C(F)=\sum_i(2c_i-m)D_i.
\]

**Unproved assertion C:** every union-closed F satisfies C(F) >= 0.

Again, for m>1 this would prove Frankl: all c_i<m/2 would make every nonzero summand negative, and at least one D_i is positive.

The first differing coordinate of a pair has maximum frequency among its differing coordinates. Thus the same quantity is

\[
C(F)=2\sum_{\{A,B\}\subseteq F,\ A\ne B}
\left(2\max_{i\in A\triangle B}c_i-m\right).
\]

Equivalently, assertion C says that the average, over unordered distinct pairs, of the maximum frequency of a coordinate in their symmetric difference is at least 1/2.

For computation, let q_i be the sum of squared prefix-fiber sizes after revealing the first i coordinates. Then q_0=m^2, q_n=m, and

\[
D_i=q_{i-1}-q_i.
\]

Indeed, q_i counts ordered pairs agreeing on the first i coordinates. Subtracting removes exactly those whose first disagreement is i. This proves the counting formulas without numerical approximation.

No implication between assertions S and C is established here. They are two separate unproved sufficient assertions.

## 6. Exact rejection of the symmetric-weight precursor

The first proposed information weight was the permutation average

\[
s_i=\frac1{n!}\sum_\pi H(X_i\mid X_j:\ j\text{ precedes }i\text{ in }\pi).
\]

The proposed sign condition sum_i(2p_i-1)s_i >= 0 is false, even for a three-member chain.

Take

\[
F=\{\varnothing,\{1\},\{1,2,3\}\},\qquad L=\log_2 3.
\]

This family is union-closed, and its frequencies are (2/3,1/3,1/3). Coordinates 2 and 3 are identical. Their one-coordinate entropy, and that of coordinate 1, is L-2/3. Revealing either of coordinates 2 or 3 leaves conditional entropy 2/3 for coordinate 1. Revealing coordinate 1 leaves conditional entropy 2/3 for coordinate 2 unless coordinate 3 was already revealed, in which case it leaves zero. Averaging the six coordinate orders gives

\[
s_1=L/3+2/9,\qquad s_2=s_3=L/3-1/9.
\]

Hence

\[
\sum_i(2p_i-1)s_i=\frac{4-3L}{27}<0.
\]

The sign is exact because 3^3>2^4. This rejects the proposed symmetric-weight proof, not Frankl: coordinate 1 is abundant. Its historical novelty is neither established nor important to the mission.

Descending frequency instead gives h=(L-2/3,2/3,0), hence S=L/3-4/9>0. This only explains why the rejected example does not reject assertion S.

## 7. The decisive unresolved proof step

Conditioning on a coordinate preserves union closure of each fiber. But it changes frequencies, whereas the proposed score uses global frequencies. A local sign statement with a fiber's own frequencies cannot be substituted for a global-weighted conditional term.

An explicit demonstration is

\[
F=\{\varnothing,\{1\},\{1,2\},\{1,3\},\{1,2,3\}\}.
\]

The global frequencies are (4/5,2/5,2/5). On the fiber X_1=1, coordinates 2 and 3 are independent fair bits. Their local weights would be zero, but their inherited global weights are both -1/5. Their inherited conditional score inside that fiber is therefore -2/5, not a nonnegative number.

The full score of this example is positive:

\[
S(F)=\frac35 H_2(4/5)-\frac8{25}>0.
\]

The example does not falsify assertion S. It shows why discarding the negative conditional contribution would be an invalid induction.

For a reveal order starting with coordinate j and with 0<q=P(X_j=1)<1, let p_i^b be the conditional frequency in fiber b and let h_i^b be conditional entropy increments in one fixed residual order. Choosing j to be the first globally sorted coordinate makes the full score below S(F). If S_b denotes the residual score using that fiber's own frequencies and that same order, direct expansion gives

\[
\begin{aligned}
S(F)={}&(2q-1)H_2(q)+(1-q)S_0+qS_1\\
&+2q(1-q)\sum_{i\ne j}(p_i^1-p_i^0)(h_i^0-h_i^1).
\end{aligned}
\]

There are two gaps in applying this as a proof: the residual order need not be optimal for either conditional law, and the cross term has no established favorable sign or sufficient universal bound. Also, assuming the globally largest q is at least 1/2 would assume the target itself.

A counting injection was also tested. For A lexicographically smaller than B with pivot i and i absent from Z, the map

\[
(\{A,B\},Z)\mapsto(\{A\cup Z,B\},B\cup Z)
\]

stays inside a union-closed family and produces a positive-pivot triple. However, it is not injective. In F={empty set,{1},{1,2}}, the distinct inputs (A={1},B={1,2},Z=empty set) and (A={1},B={1,2},Z={1}) have identical outputs. Consequently this map does not prove C(F)>=0. No Hall-type replacement or alternative injective construction was established.

A separate module entropy comparison was also falsified by finite enumeration; its executable and receipt are preserved in `module_probe.py` and `module_probe_results.txt`. None of these rejected steps is treated as an impossibility theorem for all approaches.

**The missing result remains a universal consequence of exact union compatibility that controls these global-weighted information or first-difference quantities. No such result is proved in this record.**

## 8. Executed finite verification

The exact checker enumerated every nonempty union-closed family on labelled ground sets of sizes 1 through 5. Unused coordinates and singleton families were included. The counts are not counts up to isomorphism.

| Ground-set size | Nonempty union-closed families | Negative S or C found |
|---|---:|---:|
| 1 | 3 | 0 |
| 2 | 13 | 0 |
| 3 | 121 | 0 |
| 4 | 4,959 | 0 |
| 5 | 2,771,103 | 0 |

The n=5 enumerator visited 1,385,552 union-closed families containing the empty member, then tested each both with and without that member, omitting the empty family. Adding or deleting the empty member preserves union closure, so the resulting count is twice the first count minus one.

These tests do not establish either assertion for unrestricted n. No new finite-case Frankl result is claimed.

### 8.1 Exact Shannon signs, not just floating-point tests

Let N_{i,k} count prefix fibers of size k after i coordinates. The exact formula is

\[
m^2(\ln 2)S(F)=\sum_{k=1}^m e_k\ln k,
\qquad
e_k=\sum_i(2c_i-m)k(N_{i-1,k}-N_{i,k}).
\]

All e_k are integers. The sign can therefore be decided by comparing the integer products of k to their positive and negative exponents.

To avoid constructing those products in every case, `certify_log_bounds.py` generates rigorous bounds on ln(k) with common denominator 2^48, using exact rational Taylor sums. These bounds give integer-certified positive signs. Cases whose intervals include zero are checked for exact equality by prime factorization; a big-integer comparison fallback is available but was not needed in the recorded run. There are no floating-point sign decisions in `exact_exhaustive.cpp`.

For 0<=z<=1/3, the logarithm series and its tail bound are

\[
\ln\frac{1+z}{1-z}=2\sum_{j=0}^{N-1}\frac{z^{2j+1}}{2j+1}+R_N,
\quad
0\le R_N\le\frac{2z^{2N+1}}{(2N+1)(1-z^2)}.
\]

The tail bound follows by bounding every omitted denominator below by 2N+1 and summing the geometric series. Writing k=2^t y with 1<=y<2 keeps the required z=(y-1)/(y+1) within [0,1/3]. The script uses N=40 and verifies with `Fraction` arithmetic that both bounds imply the same scaled logarithm floor for every 1<=k<=32.

### 8.2 Enumeration logic and separate implementation

The C++ enumerator uses the closure operator that adjoins all pairwise unions and the empty member. At a closed family A, consider each possible new member i from largest to smallest. Close (A restricted to earlier members) union {i}, and accept the first result B whose earlier-member prefix agrees with A. This is the next closed family in lectic order.

To see completeness, take any closed C later than A and let k be their first differing index. C contains the prefix of A before k and contains k, so closing that prefix together with k gives a subset of C with the same earlier prefix. Thus k is eligible. Choosing the largest eligible pivot yields a family no later than C, proving that no intervening closed family is skipped. Starting at the least closed family and ending at the full one enumerates all closed families once.

A separate Python program brute-forced all candidate families for n<=4. It compared the complete family lists, computed C directly from unordered pairs, and computed Shannon signs directly by integer products rather than logarithm intervals. All lists and signs agreed. This is a separate implementation within this session, not external peer review or a proof-assistant certificate.

### 8.3 Exploratory numerical searches

The saved adversarial search proposed 100,000 generator mutations each at n=6,8,10,12, with seed 2701839. It found no negative Shannon score. Proposals may repeat the same family and the search often reaches Boolean cubes. These are not 400,000 distinct uniformly sampled families and supply no exhaustive guarantee. Initial floating-point exhaustive diagnostics were superseded by the exact check and are not included in the principal package.

## 9. Reproduction

Run from this directory:

```sh
python3 certify_log_bounds.py
g++ -O3 -std=c++17 exact_exhaustive.cpp -o exact_exhaustive
for n in 1 2 3 4 5; do ./exact_exhaustive "$n"; done
python3 independent_check.py
```

The exact C++ checker uses header-only Boost.Multiprecision for its fallback. The Python certificate and separate checker use only the standard library. The C++ implementation uses GCC/Clang integer built-ins and `__int128`; it is not a claim of portability to every C++ compiler.

Recorded outputs are in `exact_exhaustive_results.txt`, `log_bounds_results.txt`, `independent_results.txt`, and `independent_results.json`. Supporting exploratory sources and receipts are included separately. `MANIFEST.json` records source pins, the proof status, and file hashes.

## 10. Final status boundary

The exact algebraic identities, the rejected symmetric-weight counterexample, and the finite computations are reconstructible. Assertions S and C for all finite union-closed families are not proved. The original half-frequency theorem is not proved. There is no external certification or established historical originality. The mission remains unresolved.

## Source identifiers

- [L1] `https://arxiv.org/abs/2610.02295v1` (the investigation inspected the v1 HTML earlier in the session; a later HTML retry returned a cache miss, while the primary search abstract remained available).
- [L2] `https://arxiv.org/abs/2306.08824v1`.
- [L3] `https://arxiv.org/abs/2211.12401v1`.
- Astra entry: `https://github.com/harjassand/astra-research-knowledge/blob/8aed7fd74eb14622ed5a0a3635a799374296e32a/00_START_HERE.txt`.
- Astra N376: `https://github.com/harjassand/astra-research-knowledge/blob/8aed7fd74eb14622ed5a0a3635a799374296e32a/frontier/review_cards/N376-Frankl-regular-antichain-rare-element.txt`.
- Astra N506 status: `https://github.com/harjassand/astra-research-knowledge/blob/8aed7fd74eb14622ed5a0a3635a799374296e32a/frontier/cards/N506-join-Petri-tests-and-priority-boundaries.json`.
- Astra original join note, rendered text: `https://github.com/harjassand/astra-research-knowledge/blob/8aed7fd74eb14622ed5a0a3635a799374296e32a/web/pages/d-7cab6fa4a5c68622.html`.
- OpenAI manuscript map: `https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/CONTENTS.md`.
