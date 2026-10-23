# Closest primary prior: source-dependent reversible local maps

**Primary source.** Benjamin Hellouin de Menibus, Ville Salo, and Ilkka Törmä, “Symbol Frequencies in Surjective Cellular Automata,” arXiv:2504.06058v2 (2025), later in *AUTOMATA 2025*, pp. 154–170. [Full primary text (arXiv HTML)](https://arxiv.org/html/2504.06058v2), [arXiv record](https://arxiv.org/abs/2504.06058). The closest result is Theorem 3.1 and its proof, lines 78–121 of the HTML (sections 2–3).

## Exact overlap with the opening

Theorem 3.1 constructs a fixed parameter $0<p<1$, a sequence $F_n$ of reversible binary cellular automata, and a finite word $w$ such that the image measures of the iid Bernoulli source $\mu_p$ lose full support in the limit: the frequency of $w=1111$ under $F_n\mu_p$ tends to zero. Thus it is a primary example of **source-dependent, reversible local transformations that drive a local record frequency to zero**, while preserving reversibility and entropy. It is close to the typical-set/reversible-encoding ingredient of the proposed construction.

The mechanism is different. For each $n$, the authors use a rare marker $w_n=(10)^n0$, whose occurrences partition almost every $\mu_p$-configuration into intervals. They classify intervals by length and, for each “common” medium-length interval, use an injection $E_k:A_k\to B_k$ to map typical contents into contents avoiding $1111$. They extend this map to an involution by applying $E_k^{-1}$ on its image and leaving all other intervals unchanged. The resulting $F_n$ is reversible, with two-sided radius $\alpha(n)+|w_n|$, where $\alpha(n)=n/\mu_p(w_n)+|w_n|$. The proof bounds the non-common interval probability by short-, long-, and Hoeffding-type terms that all vanish, forcing $(F_n\mu_p)([1111])\to0$.

## Boundary of the prior

This result does **not** approximate a one-site translation, hide a nontrivial QCA/GNVW index in a reversible source code, or establish finite-depth/range efficiency for the desired translation task. It is a sequence of CAs with source- and $n$-dependent rules; the marker interval/radius scale grows on the order of the inverse probability of an exponentially rare word, so it is not an $O(L)$-range counterpart to the proposed fixed-block construction. The theorem targets the vanishing frequency of one cylinder, not a uniform per-site error to a translated process or joint-record distance.

The bounded search did not find a primary theorem directly establishing or obstructing **source-dependent approximate translation with a prescribed QCA index**. This paper is the closest match found for reversible typical-set manipulation, not a priority or novelty determination for the opening.
