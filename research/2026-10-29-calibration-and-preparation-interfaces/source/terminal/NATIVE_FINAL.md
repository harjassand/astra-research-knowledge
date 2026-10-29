**I completed a robustness construction: for an autonomous finite-state stochastic program, the precision needed for conditional terminal inference can depend on its memory rather than its running time or the rarity of its terminal evidence.** I derived the bound, implemented a computable certificate, and established matching worst-case acquisition costs.

This is a useful completed result. Its foundations are classical, and I have not established historical novelty or a foundational breakthrough.

### The completed result

Consider two fixed, homogeneous stochastic models with the same possible transitions. Count **all model, controller, and monitoring configurations** in the \(K\) transient states. Suppose every positive local transition probability has relative error at most \(\alpha<1\).

For every possible terminal evidence event \(E\), the conditional terminal-output distributions satisfy

\[
\operatorname{TV}\!\left(P(Z\mid E),\widehat P(Z\mid E)\right)
\le
\tanh\!\left(
\frac K4\log\frac{1+\alpha}{1-\alpha}
\right).
\]

**There is no expected-running-time factor and no \(1/P(E)\) factor.**

The mechanism is a positive spanning-forest representation of absorption probabilities. Conditioning cancels its common normalization. Model error then becomes bounded reweighting of forest weights. A sharper bound uses the actual range \(\Delta\) of their log-likelihood ratios:

\[
\operatorname{TV}\le\tanh(\Delta/4).
\]

I implemented a rigorous enclosure of \(\Delta\) using integer directed-arborescence optimization and rational logarithm bounds. The forest identity and the relevant positive-polynomial robustness machinery have substantial prior art; this limits what can responsibly be claimed as discovery here. :chatgpt-content-reference{index="0"}

### Acquisition remains explicit—and costly

With independent sampling access to each source row and a promised lower bound \(\beta\) on positive local probabilities, one calibration supports **every admitted controller and terminal evidence event**, including choices made after examining the data.

For accuracy \(\varepsilon\), the sufficient sample count per source row is

\[
O\!\left(
\frac{K^2}{\beta\varepsilon^2}
\log\frac{M}{\delta}
\right),
\]

where \(M\) bounds the number of source cells and \(1-\delta\) is the confidence level. Total acquisition also pays for the number of rows and their reset costs.

A three-symbol source driving a finite-memory gambler’s-ruin controller gives a matching
\(\Omega(K^2/(\beta\varepsilon^2))\) lower bound at constant confidence. Thus unlimited computation cannot generally remove this calibration cost. Global guarantees for learned Markov models are themselves an established research direction; this construction does not supply hidden-state access or discover a compact model automatically. :chatgpt-content-reference{index="1"}

### Executed example

The standalone implementation passed exact checks covering **11,145 forests and 840 conditional posterior inequalities**. Its worked example used a 95-state controller:

| Quantity | Result |
|---|---:|
| Raw calibration samples | 47,457,349 coin bits |
| Terminal evidence probability | \(2^{-40}\) |
| Mean waiting phase, after passing the gate | \(2^{41}-2\) steps |
| Actual posterior TV error | \(0.0009477973\) |
| Data-only, controller-specific error bound | \(0.0042070489\) |

The draw was a seeded PRNG demonstration; physical independence remains an acquisition assumption. The astronomical waiting time was calculated exactly, not simulated. Predictions used the ordinary absorbing-chain linear solver, which obtains the same answers. **No advantage over an equally informed conventional solver is established.**

### The boundary and the remaining obstacle

I also constructed a three-state **external-deadline counterexample**: local relative error \(1/H\) produces a rare-conditioned posterior error tending to approximately \(0.380797\). An external clock must therefore be charged as additional configurations. The broader unconditioned fixed-time question remains unfinished, and its exploratory calculations are preserved as such.

I screened intervention design and conditional-query learning before choosing this precision question. The obstacle to substantially greater reach is now concrete: **acquiring a small positive model with reliable support from realistic observations**. The completed construction transports that certificate to difficult terminal questions once the model exists. It does not acquire the representation, eliminate an exponential state count, or remove full-history output costs.

The preceding completed result remains preserved as the supplied baseline; its originals were not modified or independently replayed.

**Completed work:**

- [FINITE_MEMORY_TERMINAL_CALIBRATION.tex](https://chatgpt.com/library?file_id=libfile_093a1132fd148191be15a54cd9316ba3&account_id=personal) — full derivation, acquisition bounds, counterexample, and limitations.
- [stopped_calibration.py](https://chatgpt.com/library?file_id=libfile_076d913f45208191baa80660972d1d4e&account_id=personal) and [stopped_calibration_results.json](https://chatgpt.com/library?file_id=libfile_7f1e8e9b88008191a24ba403aa160c42&account_id=personal) — self-contained implementation and recorded results.
- [RESEARCH_STATUS.txt](https://chatgpt.com/library?file_id=libfile_f321588f7b588191800ccad623f49ff5&account_id=personal) and [research_sources.json](https://chatgpt.com/library?file_id=libfile_1e08dcde570c8191a08d320c503cffc4&account_id=personal) — precise status, provenance, and preserved failure descriptions.