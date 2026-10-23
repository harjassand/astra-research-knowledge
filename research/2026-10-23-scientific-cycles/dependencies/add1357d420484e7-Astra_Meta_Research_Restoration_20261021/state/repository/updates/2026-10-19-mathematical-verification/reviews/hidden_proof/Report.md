> Public selected edition of the 19 October audit. Original review SHA-256: `8a33aea35381cd76b034e30239e5c45e4de95743463bd70c3ba58bc6368712f4`. Original scientific inputs are retained unchanged. Navigation and historical-receipt pointers are adapted to the selected public subset; mathematical statements, caveats and attribution are retained. Past private-audit statements describe that audit, before approved publication. Current reproduction and retained-file hashes are in the release README and FILES.json.

# Independent analytic review of the hidden-state entropy theorem

The stated finite-state H1 and H2 estimates survive this adversarial reconstruction. No mathematical gap or validated counterexample was found. In particular, the linear total-variation comparison is valid for the symmetrized path law; it does not require a square-root Pinsker loss. The constants, including the factor 4 and the observed `p_min`, are consistent with the normalizations below.

This is an independent model-based mathematical check, not external peer validation, formal verification, physical validation, or a novelty determination. The path-affinity mechanism H3 is already present in Astra capital N512/LA235 and must be credited as such. The fractional-compression bound H1 and its particular two-lag application H2 can be treated as separate candidate content, without inferring historical priority.

## Independence and pinned input

The reviewed private source is `sources/pro/hidden_state/proof.tex`, SHA-256 `b30f74046317dabb24f0b0022cff7e336dd6218c267a45456d2dfad450f96dd0`.

Initial full reads were restricted to definitions/statements and displayed example constants: source lines 1–56, 90–97, 110–137, and 193–224. An initial heading/keyword search additionally exposed isolated line 149 (the advertised linear entropy bound) and line 162 (the epsilon definition), plus proof labels/conclusion snippets. Those two scalar expressions were also specified in the assigned task. The review was therefore not fully blinded to them. No proof paragraphs or mechanisms had been read when the complete decisive derivation was saved in `independent_reconstruction.md`; full source proof lines 57–88, 98–108, and 138–190 were read afterward. The source package's pre-existing hidden-entropy audit was never read. No supplied scientific script was executed. All numerical execution used the new `audit_checks.py` in this review directory.

The parent subsequently supplied the N512 route. Its proof was compared only after the independent derivation had been recorded. The N512 indexed source payload hashes were checked against their wrappers. Source files and public repository files were not modified.

## Exact model and normalizations

The source uses row generators: `q_ij >= 0` for `i != j`, `Q 1 = 0`, and `mu Q = 0`. The hidden CTMC is finite, stationary, and time homogeneous, with strictly positive `mu`; no upper bound on its finite state count or rates is imposed. Observation is a fixed deterministic partition `Y_t = g(Z_t)` into nonempty classes, and `p_i = Pr(Y_t=i)>0`.

Take a positive sampling lag `tau`. All matrix norms below are Euclidean operator norms. Total variation is one half the L1 distance between probability densities or probability arrays. Logarithms are natural; the entropy rate is in nats per model-time unit. The source's entropy convention is

\[
\sigma(Q)=\sum_{i<j}(\mu_iq_{ij}-\mu_jq_{ji})
                   \log\frac{\mu_iq_{ij}}{\mu_jq_{ji}}.
\]

There is no missing factor 2 in this convention: summing `mu_i q_ij log[(mu_i q_ij)/(mu_j q_ji)]` over ordered distinct pairs produces exactly this unordered-pair expression. Zero-zero flux contributes zero; a one-way positive flux makes the rate infinite.

For H1 the hidden generator is reversible. With

\[
H=D_\mu^{1/2}QD_\mu^{-1/2},\quad T=e^{\tau H},\quad
V_{zi}=1_{g(z)=i}\sqrt{\mu_z/p_i},
\]

one has `H=H*<=0`, `0<T<=I`, and `V*V=I`. Thus

\[
S=V^*TV>0,\quad U=V^*T^2V,\quad a_0=\lambda_{\min}(S)>0.
\]

For H2 the hidden generator may be irreversible, all hidden states are even under time reversal, and the **exact observed pair kernels** are `P_tau=P` and `P_2tau=P^2`, where `P` is reversible and has positive spectrum. Hence `S=D_p^(1/2) P D_p^(-1/2)` is a positive contraction. The observed process need not be Markov at other times. Here `p_min` is the minimum **observed** class mass, not the minimum hidden mass.

## H1 reconstructed

Complete V to an orthogonal basis, writing

\[
T=\begin{pmatrix}S&B^*\\B&C\end{pmatrix}.
\]

Then

\[
\Delta=U-S^2=B^*B\succeq0.
\]

Positivity of T and invertibility of S give `C-B S^(-1) B* >= 0`. For `lambda>0`, therefore,

\[
D_\lambda=C+\lambda I-B(S+\lambda I)^{-1}B^*\succeq\lambda I.
\]

The block inverse identity gives

\[
R_\lambda=V^*(T+\lambda I)^{-1}V-(S+\lambda I)^{-1}
=(S+\lambda I)^{-1}B^*D_\lambda^{-1}B(S+\lambda I)^{-1}\succeq0,
\]

and in particular

\[
0\preceq R_\lambda\preceq\lambda^{-1}(S+\lambda I)^{-1}
\Delta(S+\lambda I)^{-1},\qquad
\|R_\lambda\|\leq\frac{\|\Delta\|}{\lambda(a_0+\lambda)^2}.
\]

Use the positive-matrix functional-calculus integral, for `0<alpha<1`,

\[
x^\alpha=\frac{\sin\pi\alpha}{\pi}
\int_0^\infty\lambda^{\alpha-1}\frac{x}{x+\lambda}\,d\lambda.
\]

The isometry identity `V*V=I` cancels the identity terms, yielding

\[
S^\alpha-V^*T^\alpha V
=\frac{\sin\pi\alpha}{\pi}\int_0^\infty\lambda^\alpha R_\lambda\,d\lambda\succeq0.
\]

The norm bound has the exact coefficient

\[
\frac{\sin\pi\alpha}{\pi}\int_0^\infty
\frac{\lambda^{\alpha-1}}{(a_0+\lambda)^2}\,d\lambda
=a_0^{\alpha-2}\frac{\sin\pi\alpha}{\pi}
\Gamma(\alpha)\Gamma(2-\alpha)
=(1-\alpha)a_0^{\alpha-2}.
\]

This is the claimed compression estimate. Nothing here depends on the number of hidden states or on a hidden spectral floor. The observed spectral floor `a_0` is indispensable to the stated constant.

Moreover `T^alpha=e^(alpha tau H)` is the Euclidean similarity transform of a hidden transition matrix at a genuine positive time, so it is entrywise nonnegative. V is entrywise nonnegative as well. Hence any negative off-diagonal entry of `S^alpha` has magnitude at most the gap norm. This proves H1 with

\[
m_\alpha(S)\leq(1-\alpha)a_0^{\alpha-2}\|U-S^2\|.
\]

The qualitative corollary also follows: diagonal similarity preserves the sign of an off-diagonal entry of `log P`; the corresponding entry of `S^alpha=I+alpha log S+O(alpha^2)` is negative for small positive alpha. Exact `U=S^2` then contradicts H1. The unique real logarithm of a positive self-adjoint hidden transition matrix causes no nonprimary-logarithm ambiguity in this reversible argument.

Source comparison: definitions lines 14–35, theorem lines 37–55, proof lines 57–88, corollary and proof lines 91–108. The written proof agrees with the reconstruction.

## H2 reconstructed

### Why the path comparison is linear

Let `Q*=D_mu^(-1) Q^T D_mu` and `R=(Q+Q*)/2`. For each hidden state i, stationarity gives

\[
\sum_{j\ne i}q^*_{ij}
=\mu_i^{-1}\sum_{j\ne i}\mu_jq_{ji}
=-q_{ii}=\sum_{j\ne i}q_{ij}.
\]

Thus Q, Q*, and R have the same escape rate at every state, the same stationary initial law mu, and R is reversible. This identity is essential; a generic reversal construction without stationarity would not justify the next step.

For finite entropy, forward and reverse jump supports coincide. With stationary path densities f, f*, and r for Q, Q*, and R over `[0,t]`, respectively, all initial and holding factors coincide on a fixed path. Edgewise arithmetic-geometric mean therefore gives

\[
r\geq\sqrt{ff^*},\qquad h=(f+f^*)/2\geq\sqrt{ff^*}.
\]

Writing `A=int sqrt(f f*)`, both nonnegative residual densities `r-sqrt(f f*)` and `h-sqrt(f f*)` have mass `1-A`. Consequently,

\[
\operatorname{TV}(h,r)\leq1-A.
\]

Jensen under f gives

\[
A=E_f\exp[-\tfrac12\log(f/f^*)]
\geq e^{-D(f\Vert f^*)/2}.
\]

The identical holding rates cancel from the log path-density ratio. Taking expected jump counts in stationarity gives

\[
D(f\Vert f^*)
=t\sum_{i\ne j}\mu_iq_{ij}\log\frac{q_{ij}}{q^*_{ij}}
=t\sigma(Q).
\]

Therefore

\[
\operatorname{TV}((f+f^*)/2,r)
\leq1-e^{-t\sigma(Q)/2}\leq t\sigma(Q)/2.
\]

This proves H3 as used. A direct linear bound between f and r is neither needed nor asserted. That is why replacing this step by a generic Pinsker estimate would give a weaker result, not expose a flaw. If the entropy is infinite, H2 is immediate.

### Endpoint symmetry, factor 2, and p_min

For ordinary all-even reversal, the Q* observed endpoint-pair law is the transpose of the Q law. At `t=tau,2tau`, these laws are symmetric because `D_p P` and `D_p P^2` are symmetric. Thus the endpoint pushforward of the mixture h equals that of f at the two required lags. No time-reversal invariance of the entire observed process is required.

Let `J_t,Jbar_t` be the Q and R joint probability matrices for the observed endpoints. Both have observed stationary marginal p. Their normalized-kernel difference is exactly the congruence

\[
D_p^{-1/2}(J_t-\bar J_t)D_p^{-1/2}.
\]

It obeys

\[
\|D_p^{-1/2}(J_t-\bar J_t)D_p^{-1/2}\|
\leq\frac{\sum_{ij}|(J_t-\bar J_t)_{ij}|}{p_{\min}}
\leq\frac{t\sigma(Q)}{p_{\min}}.
\]

The intermediate factor is `2 TV/p_min`; H3 contributes `TV<=t sigma/2`, so those factors 2 cancel. Set `epsilon=tau sigma/p_min` and write `Sbar_1,Sbar_2` for R's normalized kernels. Then

\[
\|\bar S_1-S\|\leq\epsilon,\qquad
\|\bar S_2-S^2\|\leq2\epsilon.
\]

All required reversible endpoint matrices are contractions. Consequently,

\[
\|\bar S_2-\bar S_1^2\|
\leq2\epsilon+\|S(S-\bar S_1)+(S-\bar S_1)\bar S_1\|
\leq4\epsilon.
\]

The factor 4 is correct. Using a minimum hidden stationary mass here would introduce an unnecessary dimension dependence; the proof correctly uses observed p_min.

### The noncommuting power estimate and the two cases

For positive matrices `A,B>=c I`, the resolvent identity gives

\[
\|A^\alpha-B^\alpha\|
\leq\frac{\sin\pi\alpha}{\pi}\|A-B\|
\int_0^\infty\frac{\lambda^\alpha}{(c+\lambda)^2}\,d\lambda
=\alpha c^{\alpha-1}\|A-B\|.
\]

The integral evaluates to `c^(alpha-1) Gamma(alpha+1) Gamma(1-alpha)` before multiplication by `sin(pi alpha)/pi`. The estimate applies to noncommuting matrices; no scalar mean-value argument is being substituted for operator Lipschitzness.

If `epsilon>=a_0/2`, the first branch already gives H2. Otherwise Weyl's elementary eigenvalue bound gives `Sbar_1>=(a_0/2) I`. Apply the displayed power estimate and H1 to R:

\[
\begin{aligned}
m_\alpha(S)
&\leq\|S^\alpha-\bar S_1^\alpha\|+m_\alpha(\bar S_1)\\
&\leq\left[\alpha(a_0/2)^{\alpha-1}
 +4(1-\alpha)(a_0/2)^{\alpha-2}\right]\epsilon
=C_\alpha\epsilon.
\end{aligned}
\]

Thus in every case

\[
\sigma(Q)\geq\frac{p_{\min}}{\tau}
\min\{a_0/2,m_\alpha(S)/C_\alpha\}>0.
\]

Source comparison: assumptions and definition lines 112–129, H2 lines 123–136, path comparison lines 138–154, endpoint estimates lines 155–170, operator estimate and conclusion lines 171–190. The written proof agrees with this reconstruction.

## Existing Astra capital: H3 is N512 reuse

`frontier/dossiers/N512.txt` explicitly records the exact H3 mechanism at lines 30–31 and keeps its `source_derived_unreviewed` / external, formal, empirical, and priority limitations at lines 4–6 and 27. It is linked to LA235.

The located original source is `updates/BP/package/work/sol/observable_separation/v3.txt`, preserved in `frontier/proof_ranges/3e65bae9372526aba0b977bd.txt`. Its source payload SHA-256 was independently checked as `a686a18a369c6e57fea1d1a3107c0141a0b2bc8b34f5e9ac80d12bbb21189752`. The original named path is absent from this checkout; the exact-range wrapper contains all 60 source lines with four wrapper lines prepended.

| Existing source content | Original source lines | Wrapper file lines |
|---|---:|---:|
| Same stationary adjoint, equal holding rates, geometric-density domination, affinity/Jensen, and `TV<=1-exp(-T sigma/2)` | 13–31 | 17–35 |
| Linear transfer for every pointwise reversal-even finite-window test | 33–42 | 37–46 |
| Prior-ingredient and no-historical-novelty qualifications | 59–60 | 63–64 |

The supporting `hidden_realization/v4.txt` source payload also matched its declared SHA-256 `0314e0e687a656807cbe2f9e1c3ff972c9011a7d7a4c3cc97217d59a8b0b2373` in wrapper `frontier/proof_ranges/84bc17da3f17619b3a928fea.txt`. Its original source lines 11–15 (wrapper 15–19) summarize the already-existing linear dissipation transfer; original source lines 19–27 (wrapper 23–31) retain acquisition and validation limits.

The present H2 uses reversible endpoint-pair laws to make the mixture's endpoint laws equal to the target laws. This is a particular application of the same symmetrization mechanism; N512 instead displays it for pointwise reversal-even statistics. H1's fractional compression estimate and the specific `C_alpha` / two-lag composition are additional content relative to those inspected N512 proof ranges. This comparison does not establish their historical novelty or validate N512's unrelated closure, polygon, or seven-time separation arguments.

Attribution correction for any synthesis: identify H3 as **existing Astra capital N512/LA235 reused in this application**, rather than a newly discovered H3 mechanism. The mathematical check here does not upgrade N512 to externally verified status.

## Independent numerical stress checks

The new script uses seed 20261019, NumPy 2.5.3, its own small-matrix exponential, and Python Decimal for the displayed constants. It executes no supplied source code. `numerical_checks.json` records every targeted case and full high-precision values.

| Check | Scope and result |
|---|---|
| H1 compression norm | 320 reversible-CTMC cases; hidden dimensions 3–12, observed classes 2–5, alpha in `{1/64,0.1,0.5,0.9}`. Largest gap/bound ratio 0.991993662. Smallest numerical gap eigenvalue -1.75e-15 and defect eigenvalue -2.74e-16, within floating-point rounding. |
| Negative fractional-power witness | 20 cases for the reversible four-state line with its middle states merged; 17 had a negative fractional-power entry. At `tau=0.1, alpha=0.5`, entry `(0,2)=-0.0005185484453`, while H1's bound is 0.0045544288824. |
| Noncommuting operator Lipschitz | 336 positive-matrix cases in dimensions 2–8. Largest actual/bound ratio 0.999999930. |
| Linear symmetrized endpoint comparison | 60 irreversible balanced-flux CTMC cases in dimensions 3–7. Largest endpoint-TV/affinity-bound ratio 0.0570493. Adjoint escape-rate row error at most 2.23e-16. |
| Uniformized path-mixture comparison | Four balanced three-cycle cases, enumerated under a common Poisson clock through 10 events. Unenumerated total-variation contribution at most 1.197e-15 per case. Common-density domination, affinity, and linear bounds passed. The virtual-event conditional law is common because escape rates agree. |

The path tests distinguish the relevant laws. At three-cycle asymmetry `delta=0.001` and time `t=0.2`, mixture-versus-reversibilization TV is about `9.05e-9`, direct forward-versus-reversibilization TV is about `9.09e-5`, and the linear entropy upper bound is `2.00e-7`. A proposed direct-forward linear bound would fail this test; the source correctly bounds the mixture. The cycle endpoint tests compare symmetrized endpoint laws, not a claim that these examples satisfy H2's exact reversible two-lag target hypothesis.

The line example also checks an important logical boundary. Its hidden Q is reversible and the observation has three classes with `p=(1/4,1/2,1/4)`, yet the one-lag fractional power has a negative off-diagonal entry. Its second-lag defect is nonzero, as H1 requires. Thus the second-lag premise cannot be silently dropped. The source does not drop it.

These finite checks support implementation sanity and attempted falsification. They are not proof certificates for the general estimates.

## Example constants and claim limits

Independent 90-digit Decimal evaluation of the source's displayed inputs gives

\[
\alpha=1/64,\quad a_0=2^{-18},\quad p_{\min}=1/4,\quad\tau=1,
\]

\[
m=0.0027825868330900103069\ldots,
\quad C_\alpha=881032897935.83185365\ldots,
\]

\[
\frac{m a_0^{2-\alpha}}{1-\alpha}
=4.9988832366564808\ldots\times10^{-14},
\]

\[
\zeta=3.1583234174448206\ldots\times10^{-15},\qquad
\frac{p_{\min}}{\tau}\zeta
=7.8958085436120515\ldots\times10^{-16}.
\]

The minimum selects `m/C_alpha`, far below `a_0/2`. This numerical evaluation is separate from the companion exact-rational certificate, which this reviewer did not execute or audit. The hidden-dimension-uniform floor is approximately `7.89e-16`; the distinct same-four-state optimization value `26.1789...` cannot replace it.

The conclusion covers every compatible **finite** hidden CTMC, with no preassigned finite dimension bound. It does not assert a theorem for arbitrary infinite-state processes, unbounded generators, explosive chains, or limiting realizations without an additional path-measure/functional-calculus argument.

H2 is an exact two-lag theorem. Finite experimental data do not establish exact equality to P and P². A statistical use needs a separate robust margin calculation, uncertainty in p and the operator-norm estimates, and justified stationarity, sampling/dependence, observation, parity, and time-calibration premises. H1's roughly `5e-14` defect threshold and H2's tiny model-time floor alone give no useful finite-data acquisition guarantee.

Time-dependent dynamics, nonstationarity, a physical reversal involving odd coordinates, and an observation apparatus with unmodeled memory are outside the proved interface. A mathematical path-irreversibility rate is not by itself a measured heat/work/chemical entropy production rate. The source already states these boundaries at lines 217–223.

No mathematical correction is required for H1 or H2 as scoped. For clarity one may state `tau>0` explicitly and replace the phrase “diagonal similarity” in the joint-law step by the exact `D_p^(-1/2) (J-Jbar) D_p^(-1/2)` congruence; neither changes the valid bound. The substantive provenance correction is to credit H3's existing N512/LA235 capital. External expert/formal validation, historical novelty, robust experimental inference, practical value, and an infinite-state extension remain unestablished by this review.
