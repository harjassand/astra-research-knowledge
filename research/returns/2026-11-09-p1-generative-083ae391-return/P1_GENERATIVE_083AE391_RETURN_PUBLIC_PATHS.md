# P1 completed return

- Chat: https://chatgpt.com/c/6aed70fd-ec00-83ec-ae10-3af342cad0e6
- Prompt: producer-workspace/P1_FULL_GENERATIVE_AFTER_UNITAL_READER_UNRELEASED_20261108.txt (sent turn 083ae391-7a8d-4244-b313-9f75f30616d4; sent copy omits its terminal newline)
- Model displayed at dispatch and collection: 5.6 Pro. Actual model throughout is not independently established.
- Completed return collected 2026-11-08 UTC. No new ZIP supplied; the individual Markdown attachment was not downloaded. Existing source and transfer holds remain.

## Complete response

## Conditional negative resolution

The proposed universal positive theorem is **false under a precise native noisy-IQP average-case hardness assumption and noncollapse of the polynomial hierarchy**.

The obstruction preserves the complete physical contract:

- two-dimensional nearest-neighbour geometry;
- rational, piecewise-constant Hamiltonians;
- fixed positive \(g=J/\gamma\);
- continuously active replacement depolarization;
- rational product preparation;
- finite one-site POVMs;
- no postselection, fresh ancillas, feedback, reset oracle or conditional-probability access;
- constant requested total-variation accuracy.

The nonunital terms are set to
\[
\eta_z(t)=0.
\]
That choice is legal for every proposed neighbourhood
\[
0\le \eta_z(t)\le \eta_{\mathrm{sample}}.
\]
Therefore hardness of this unital subclass at one fixed \(g_0\) rules out any positive \(\eta_{\mathrm{sample}}(a,k,d,g_0)\).

This is a **conditional computational resolution**, not an unconditional lower bound. Unconditionally, generic intermediate-time two-dimensional full-output sampling remains open in the supplied research record. :chatgpt-content-reference{index="0"} The accepted global-product predictor is materially weaker: it supplies additive product means but explicitly not a full-distribution sampler. :chatgpt-content-reference{index="1"}

---

## 1. A fully native hard-family assumption

Fix a finite \(g_0>0\), constants \(d_0\in\mathbb N\), \(\alpha>0\), and \(\beta>0\).

For each \(n\), let \(\mathfrak C_n\) be an efficiently samplable ensemble of \(d_0\)-layer IQP schedules on an \(L\times L\) square grid, \(n=L^2\). Each interval has

\[
H_\ell=
\sum_i \phi_{i,\ell}Z_i+
\sum_{\{i,j\}\in E_\ell}\theta_{ij,\ell}Z_iZ_j,
\]

where \(E_\ell\) is a nearest-neighbour matching and all coefficients and interval lengths are rational with polynomial binary descriptions. The bounds

\[
k=2,\qquad a=1,\qquad d=O(1),\qquad |h_a|\le J
\]

are fixed.

The preparation is

\[
\rho_0=|+\rangle\!\langle+|^{\otimes n},
\]

and every qubit is measured in the \(X\) basis. During every interval the evolution is exactly

\[
\mathcal L_\ell(\rho)
=
-i[H_\ell,\rho]
+
\gamma\sum_i(E_i(\rho)-\rho),
\qquad
\frac{J}{\gamma}=g_0.
\]

Let \(p_C(x)\) be the resulting exact continuous-time output probability.

### Assumption N2D-IQP\((g_0)\)

1. **Anticoncentration**
   \[
   \Pr_{\substack{C\sim\mathfrak C_n\\x\sim\mathrm{Unif}}}
   \left[p_C(x)\ge \alpha 2^{-n}\right]\ge\beta.
   \tag{1}
   \]

2. **Average-case probability hardness**

   Unless the polynomial hierarchy collapses to its third level, no
   \(\mathrm{FBPP}^{\mathrm{NP}}\) algorithm approximates \(p_C(x)\) within relative error \(1/4\) on a \(\beta/2\) fraction of pairs \((C,x)\).

This is the exact continuous-noise counterpart of the standard IQP anticoncentration plus average-case probability-hardness framework used to derive additive-TV sampling obstructions. :chatgpt-content-reference{index="2"}

It is an additional conjecture. Existing results do not already prove it:

- The current noisy-IQP depth-transition result establishes a below-threshold **exact-sampling** obstruction, not the required additive-TV obstruction. :chatgpt-content-reference{index="3"}
- Current noisy random-circuit additive-TV hardness applies when the local noise decreases as \(O(\log n/(nd))\), rather than at a fixed positive continuous noise ratio. :chatgpt-content-reference{index="4"}

---

## 2. Native obstruction theorem

### Theorem

Assume N2D-IQP\((g_0)\) and that PH does not collapse.

Then no uniform classical algorithm can, for every instance at ratio \(g_0\), sample within total-variation error

\[
\epsilon_0=\frac{\alpha\beta}{128}
\tag{2}
\]

using polynomial worst-case bit work.

Consequently, no positive constant

\[
\eta_{\mathrm{sample}}(a,k,d,g_0)>0
\]

can satisfy the full neighbourhood proposition in the question.

### Proof

Assume such a sampler exists. On input circuit \(C\), let its output law be \(q_C\). Then

\[
\operatorname{TV}(p_C,q_C)\le\epsilon_0,
\]

so

\[
\sum_x|p_C(x)-q_C(x)|\le2\epsilon_0.
\tag{3}
\]

Worst-case polynomial bit work implies a polynomial upper bound on the sampler’s random-bit tape after padding shorter executions. Stockmeyer approximate counting therefore supplies an \(\mathrm{FBPP}^{\mathrm{NP}}\) algorithm that estimates \(q_C(x)\) within multiplicative error \(1/16\).

For fixed \(C\),

\[
\mathbb E_{x\sim\mathrm{Unif}}
|p_C(x)-q_C(x)|
\le
\frac{2\epsilon_0}{2^n}.
\]

By Markov’s inequality, except on a \(\beta/4\) fraction of uniformly random \(x\),

\[
|p_C(x)-q_C(x)|
\le
\frac{8\epsilon_0}{\beta 2^n}
=
\frac{\alpha}{16\,2^n}.
\tag{4}
\]

Intersect (4) with the anticoncentration event (1). The intersection has probability at least

\[
\beta-\frac{\beta}{4}
=
\frac{3\beta}{4}.
\]

On that intersection,

\[
|p_C(x)-q_C(x)|
\le \frac{p_C(x)}{16},
\]

and hence

\[
\frac{15}{16}p_C(x)
\le q_C(x)\le
\frac{17}{16}p_C(x).
\tag{5}
\]

Let \(\widetilde q_C(x)\) be the Stockmeyer estimate, satisfying

\[
|\widetilde q_C(x)-q_C(x)|
\le\frac{q_C(x)}{16}.
\]

Combining this with (5),

\[
\begin{aligned}
|\widetilde q_C(x)-p_C(x)|
&\le
|\widetilde q_C(x)-q_C(x)|
+
|q_C(x)-p_C(x)|\\
&\le
\frac{17}{256}p_C(x)+\frac1{16}p_C(x)\\
&<
\frac14p_C(x).
\end{aligned}
\tag{6}
\]

After assigning the Stockmeyer failure probability sufficiently small, this produces a relative-\(1/4\) estimator on at least a \(\beta/2\) fraction of \((C,x)\), contradicting N2D-IQP\((g_0)\) unless PH collapses.

Finally, every claimed positive neighbourhood contains the choice

\[
\eta_z(t)=0.
\]

Therefore a sampler for all \(0\le\eta_z\le\eta_{\mathrm{sample}}\) would sample the native hard family above, proving the contradiction. ∎

---

## 3. Why the reduction preserves the exact input model

No limiting or oracle operation is hidden:

- **Rational data:** all Hamiltonian coefficients, switching times, initial density matrices and POVM effects are rational.
- **Fixed locality:** only one-site \(Z_i\) and nearest-neighbour \(Z_iZ_j\) terms are used.
- **Fixed strength ratio:** \(g_0=J/\gamma\) is a constant independent of \(n\).
- **Continuous noise:** replacement depolarization acts throughout each Hamiltonian interval; it is not replaced by a final readout-noise channel.
- **Constant accuracy:** the contradiction uses the fixed error \(\epsilon_0\), so no exponentially small \(\epsilon\) or exponential \(1/\epsilon\) work is concealed.
- **No added resources:** the reduction uses no intermediate measurements, classical feedforward, postselection, clean ancillas or nonunital cooling.
- **Complete input cost:** a circuit instance has \(O(n)\) local terms and polynomially many coefficient and coordinate bits.

Polynomial-bit rational approximations to conventional non-Clifford IQP angles can be incorporated into the ensemble itself. Alternatively, N2D-IQP may be stated directly for a fixed rational angle alphabet; the theorem above only uses the exact native probabilities of the chosen rational family.

---

## 4. Consequence for the requested phase diagram

The full statement in the question has the logical form

\[
\forall g>0\quad
\exists\eta_{\mathrm{sample}}(g)>0
\quad
\forall\text{ allowed instances}\quad
\text{polynomial classical sampling}.
\]

The obstruction needs only one fixed \(g_0\):

\[
\text{N2D-IQP}(g_0)
\;\Longrightarrow\;
\neg\exists\eta_{\mathrm{sample}}(g_0)>0.
\]

Thus, under the stated assumption and PH noncollapse, the answer to the universal question is:

\[
\boxed{\textbf{No.}}
\]

Weak nonunitality is not the determining issue. The obstruction is already present at the center of every proposed neighbourhood, \(\eta=0\).

---

## 5. Unconditional scientific status

The obstruction is complete **conditional on N2D-IQP\((g_0)\)**. The conjecture itself is not currently proved. Existing exact-sampling hardness, additive product-mean prediction, short-time native sampling, qualifying-time sampling, patch compilers and signed-law constructions do not establish or refute it.

Therefore the defensible status is:

\[
\boxed{
\begin{array}{l}
\text{Conditional on native noisy-IQP average-case hardness: negative resolution.}\\[2mm]
\text{Without that assumption: the arbitrary-schedule full-TV question remains open.}
\end{array}}
\]

:chatgpt-content-reference{index="6"}[Full theorem and reduction](producer-workspace/native_2d_sampling_conditional_obstruction.md)

## User-visible activity

Worked for 20m 53s

Clarified the research task

Resolved the sampling route

Assessing hardness

Refining the hardness argument

Estimated circuit complexity

Checked noisy hardness

Formulated a conditional result from known results

Bridged assumptions and formulated native hardness definitions

Assessed anticoncentration and geometric hardness of sampling consequences

Assessed tracking errors, continuous faults, and final status

Formulated conditional hardness

Searched 27 websites

Formalized the conditional sampling-hardness obstruction

The full question still hinges on fixed-window 2D dynamics. I found a model-preserving conditional negative route reducing any sampler to average-case estimation of exact continuously depolarized output probabilities.

This conditional obstruction already applies to the unital subclass, so any positive nonunital neighborhood theorem must overcome it there first.

No associated subagent activity tree was displayed for this turn.

