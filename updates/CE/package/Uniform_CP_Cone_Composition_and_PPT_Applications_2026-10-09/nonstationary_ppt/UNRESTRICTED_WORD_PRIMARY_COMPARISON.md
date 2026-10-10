# Primary-source comparison: unrestricted PPT words

Checked 9 October 2026. Narrow theorem-statement comparison, not a proof audit, exhaustive literature search, priority certification, or current-status determination for PPT-square.

## Result

No unconditional primary-source theorem with the complete target quantifiers was located in this search:

For every fixed d, there is N(d) such that every serial word of N(d) arbitrary PPT CP maps M_d -> M_d is EB, without normalization, common-state, stationarity, commutativity, or finite-alphabet assumptions.

The sharpest explicit published-question boundary located is Park's **Question 4.3**, which asks even the weaker dimension-uniform equal-map question. The closest genuine arbitrary-factor results located have extra cone restrictions or a conjectural hypothesis. These facts support a carefully qualified distinction from the checked sources; they do not certify novelty or correctness of the internal candidate.

## 1. Park: an explicit weaker question and mixed-map overlap

Sang-Jun Park, *Every PPT channel has finite entanglement breaking index*, arXiv:2608.13551v2, **17 August 2026**; [version and date](https://arxiv.org/abs/2608.13551v2), [primary full text](https://arxiv.org/html/2608.13551v2).

- **Theorem 1.1:** each PPT CP map has a finite equal-map EB index, allowed to depend on that map.
- **Question 4.3:** for each d >= 4, is there n(d) such that Phi^n(d) is EB for every PPT Phi on M_d? The paper explicitly distinguishes this from Theorem 1.1.
- **Theorem 5.5:** the tuples (PPT, DSP_2, PPT) and (PPT, DSP_3, PPT, DSP_3, PPT) are EB-composable. Here DSP_k = SP_k + transpose o SP_k. These are genuinely mixed-map assertions, not only equal powers. **Remark 5.6** permits different intermediate dimensions.

Thus the unrestricted candidate would settle Question 4.3 by choosing equal factors. Theorem 5.5 does not supply unrestricted words because its intermediate cones are restricted. These are statements in the preprint, not independent certification of its proofs.

## 2. CMHW: arbitrary-factor iteration, plus a conditional route

Matthias Christandl, Alexander Müller-Hermes, Michael M. Wolf, *When Do Composed Maps Become Entanglement Breaking?*, arXiv:1807.01266v2, **17 June 2019**; [version and date](https://arxiv.org/abs/1807.01266v2), [primary full text](https://arxiv.org/html/1807.01266v2).

- **Theorem II.1:** arbitrary CP n-EB factors become EB after ceil((d-1)/(n-1)) compositions. For n=2 this is d-1 factors, with no TP or unitality assumption.
- **Section II.2:** an explicit PPT map on M_4 is not 2-EB, so substituting all PPT maps into that theorem is invalid.
- **Corollary III.1:** any two qutrit PPT maps compose to EB.
- **Conjecture II.1, Lemma II.2, Theorem II.2:** the conjectured PPT Schmidt-number bound supplies a sandwich reduction; the displayed theorem applies it to equal powers.

**Comparison inference, not a stated theorem:** if Conjecture II.1 holds in all dimensions through d, Lemma II.2 also applies to two *different* outer subwords. Starting at length L_1=1 and recursively using L_(k+1)=2L_k+1 gives Schmidt number <= d-k for every word of length 2^k-1. Thus the same hypothesis would yield arbitrary-word EB length 2^(d-1)-1. This is conditional overlap, not an unconditional predecessor.

## 3. Ekblad: nonidentical products with probabilistic assumptions

Owen Ekblad, *A Multiplicative Ergodic Theorem for Bistochastic Ergodic Quantum Processes with Applications to Entanglement*, arXiv:2502.14997v2, **4 August 2025**; [version and date](https://arxiv.org/abs/2502.14997v2), [primary full text](https://arxiv.org/html/2502.14997v2).

**Theorem 4** establishes almost-sure asymptotic EB for a bistochastic ergodic process with positive probability of a PPT factor. **Theorems 5–6** concern eventual EB and its stopping-time index; Theorem 6 assumes the additional independence condition and scalar stabilized multiplicative domain. The text preceding Theorem 6 leaves the general eventual-EB classification open.

These are neither deterministic all-word statements nor an N(d) uniform over arbitrary factors. Almost-sure conclusions leave exceptional trajectories; an almost-sure finite stopping time is not a common bounded time.

## 4. Earlier equal-map results: boundary confirmed only

- Kennedy–Manor–Paulsen, arXiv:1710.08475v2, **7 December 2017**, **Theorem 3.5**: a single unital or TP PPT map has iterates approaching EB. [Version/date](https://arxiv.org/abs/1710.08475v2); [theorem text](https://arxiv.org/html/1710.08475v2).
- Rahaman–Jaques–Paulsen, arXiv:1801.05542v2, **11 June 2018**, **Theorem 4.4**: a single unital PPT channel has finite EB index. Here a channel is TP, so this is the bistochastic case. [Version/date](https://arxiv.org/abs/1801.05542v2); [theorem text](https://arxiv.org/html/1801.05542v2).

Neither theorem states a uniform arbitrary-word bound.

## Search and wording limits

Targeted searches covered arbitrary products/sequences/words, uniform or dimension-dependent EB index, and generalized/asymptotic PPT iterations. The theorem statements above were opened directly. No unofficial math index or machine review supplies any conclusion here.

One potentially misleading older search hit was checked against its current primary version: Majewski's *On PPT Square Conjecture*, arXiv:2108.01588v3, **12 August 2026**. The [arXiv record](https://arxiv.org/abs/2108.01588v3) says that earlier Section 4 statements were corrected; the [current text](https://arxiv.org/html/2108.01588v3) gives cone analysis and restricted results, not the target uniform-word theorem. Its manuscript date line differs from its arXiv submission date; the date recorded here is the verified submission date.

Safe conclusion: **the unrestricted deterministic uniform-word claim was not found in the checked primary sources; its quantifiers go beyond their unconditional statements.** Do not replace this with “first,” “new theorem,” “literature exhausted,” or a present-day PPT-square status claim. The internal proof candidate still needs independent mathematical review.
