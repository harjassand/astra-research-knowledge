# Independent audit: coarse-grained formation converse

Date: 2026-10-21. Scope: exact first Bell block, approximate return of the complete normal memory, and globally approximate iid LOCC formation. All logarithms are natural. This audit writes only in this directory. The initial operator-basis view was formed before reading other agents' work. The root subsequently supplied the stronger stopping-measurement baseline, which this audit independently checked and sharpened below.

## Verdict

The proposed coarse-graining inequalities and coefficient `1/(3 ln 2)` are **valid**, conditional only on the explicitly imported primary product log-Sobolev theorem. The normalizations match. The positive-operator to arbitrary-coefficient extension must be explained; the paper's all-operator hypercontractivity supplies it.

The approximate iid formation step is valid and needs neither additivity of entanglement of formation nor entropy continuity in the infinite memory. In fact, the finite pure-state witness is affine in output test probabilities, so even finite-output entropy continuity can be avoided.

However, **this is not an improvement of the available universal converse**. The direct stopping test across all preparation copies already gives the stronger finite bound

\[
 E_C(\tau)\ge m\sum_{i=1}^N[1-(i-1)\delta]_+
 -\ln\{1+(N-1)(1-D^{-1})\},\qquad m=\ln D. \tag{S}
\]

In particular,

\[
 E_C(\tau)\ge \frac{m}{2\delta}-\ln(1/\delta)+\frac m2-\ln(1+\delta),
 \quad 0<\delta\le1, \tag{S2}
\]

and every permitted family obeys `liminf_(δ→0) δ E_C(τ_δ)/ln D >= 1/2`. This stronger result has a proof using only finite-dimensional formation input, finite output measurement, and relative-entropy data processing. It does not assume a product separable comparator. Proofs are given below.

Historical novelty and external correctness certification remain **UNKNOWN**. This audit verifies an argument and its imported constants; it is not a literature-exhaustive novelty assessment.

## 1. Exact operational setup and inherited probabilities

Let `T` be the same fixed complete normal LOCC block channel from the bipartite memory to a released `D x D` output and the complete retained memory. Assume

\[
 T(\tau)=\Phi_D\otimes\tau_1,\qquad
 \tfrac12\|\tau_1-\tau\|_1\le\delta.
\]

The tensor product follows from the exact pure output. The measurement-success map

\[
 S(x)=\operatorname{Tr}_{Q}\big[(\Phi_D\otimes I)T(x)(\Phi_D\otimes I)\big]
\]

is normal CP and trace nonincreasing. It is not assumed LOCC or separability preserving. For the first `i` consecutive Bell tests in a real `N`-block output experiment,

\[
 p_i=\operatorname{Tr}S^i(\tau),\qquad p_1=1,
 \qquad p_i\ge[1-(i-1)\delta]_+.
\]

Indeed, `0 <= (S*)^j(I) <= I`, and the trace-zero difference `τ-τ_1` has positive-part trace at most `δ`. Telescoping `Tr S^i(τ-τ_1)` proves the claim. Future blocks act only on memory, so all Bell tests can be deferred. Later outputs may be correlated and need not be identical.

For `t` independent target memories, apply this experiment independently to each copy. Only the target initializer is iid. No assumption of independent comparison states or independent actual approximate-preparation outputs is made.

## 2. Coefficient dictionary

Write `d = D^(Nt)` and use the normalized matrix trace `tr_d = Tr/d`, distinct from the memory state `τ`. Every pure finite output vector has a unique coefficient matrix

\[
 |\psi_X\rangle=(X\otimes I)|\Phi_d\rangle,
 \qquad \operatorname{tr}_d(X^*X)=1.
\]

Its entanglement entropy and entropy deficit are

\[
 S(\psi_{X,A})=\ln d-\operatorname{Ent}(X),\qquad
 \operatorname{Ent}(X)=\operatorname{tr}_d(X^*X\ln(X^*X)). \tag{1}
\]

For chain `a` and prefix length `i`, let `E_ai` reset all matrix tensor factors `(a,1),...,(a,i)` to identity using normalized partial trace. Explicitly, for a set `R` of sites,

\[
 E_R(X)=\frac{I_R}{D^{|R|}}\otimes\operatorname{Tr}_R X.
\]

The actual Bell-prefix projection probability of this vector is

\[
 P_{ai}(X)=\|(\langle\Phi_{D^i}|\otimes I)|\psi_X\rangle\|^2
 =\|E_{ai}(X)\|_{2,\operatorname{tr}_d}^{\,2}. \tag{2}
\]

No positivity or normality of `X` is assumed. The relation follows by contracting the Bell bra: its residual coefficient is `Tr_R X / sqrt(d D^|R|)`. Taking its ordinary Hilbert-Schmidt norm gives (2). The entropy in (1) follows from reduced density `XX*/d` and equality of nonzero spectra of `XX*` and `X*X`.

Define the hierarchical energy

\[
 H(X)=m\sum_{a=1}^t\sum_{i=1}^N[1-\|E_{ai}X\|_2^2]. \tag{3}
\]

## 3. Chunk comparison is correctly oriented

Let `N=bq`. Divide each chain into `q` consecutive chunks of `b` sites, of local dimension `Q=D^b`. Let `F_aj` be the normalized complete reset on chunk `j` of chain `a` and define

\[
 \mathcal E_{\rm ch}(X)=\sum_{a=1}^t\sum_{j=1}^q
 [1-\|F_{aj}X\|_2^2]
 =\langle X,\sum_{a,j}(I-F_{aj})X\rangle_2. \tag{4}
\]

Use an orthonormal product operator basis whose local index `0` is identity and all other local basis operators are traceless. Both quadratic forms are diagonal in this basis. For a basis string in one chain:

* If the chain is inactive, both energies vanish.
* If the first active site is `r`, the number of killed prefix expectations is `N-r+1`.
* If there are `k` occupied chunks, the earliest occupied chunk is `j_0` and `k <= q-j_0+1`. Also `r <= b j_0`. Hence

\[
 N-r+1\ge b(q-j_0)+1\ge bk-(b-1). \tag{5}
\]

Sum over chains and average the basis eigenvalues with squared coefficient weights. This proves

\[
 \boxed{H(X)\ge bm\,\mathcal E_{\rm ch}(X)-t(b-1)m.} \tag{6}
\]

The subtraction is paid once per chain, not once per chunk. For inactive chains (6) uses a harmless extra subtraction. A refined comparison can subtract `(b-1)m` times the squared mass of active basis strings per chain, but that refinement is unnecessary here.

## 4. Primary LSI constant and arbitrary coefficient matrices

The primary source is [Dong, Gao, Ou, Yao, Zhou, arXiv:2606.17729v3](https://arxiv.org/html/2606.17729v3), revised 25 July 2026. Section 2.4 defines `α_2 Ent_2 <= E_2`, with `E_2(X)=<X,LX>`; Theorem 3.12 gives the tensor-power factor `β=2/(3 ln 2)` uniformly in the number of factors. The complete reset generator `L_Q=I-tr_Q(.)I` is primitive, tracial reversible, and PODS, with full-rank invariant state `I/Q`.

The exact one-site value is independently confirmed in [Beigi, Datta, Rouzé, arXiv:1804.10100v2, Theorem 25](https://arxiv.org/html/1804.10100v2):

\[
 \alpha_2(L_Q)=\frac{1-2/Q}{\ln(Q-1)},\qquad \alpha_2(L_2)=\frac12. \tag{7}
\]

Thus the proposed inverse constant is exactly

\[
 A_b=\frac1{\beta\alpha_2(L_Q)}
 =\frac{3\ln2}{2}\frac{\ln(Q-1)}{1-2/Q},\qquad
 A_b\big|_{Q=2}=3\ln2. \tag{8}
\]

There is no missing factor of two. For example the exact local qubit inequality is `Ent <= 2 E`, while the imported approximate product bound gives `Ent <= 3 ln2 E`.

The LSI definition in the paper initially uses positive inputs. A general pure coefficient `X` need not be positive, so it is insufficient merely to quote that definition. Use the paper's all-operator hypercontractivity (Theorem 3.1, or Corollary 3.13 with Lemma 3.2). Put

\[
 \alpha_{\rm eff}=\beta\alpha_2(L_Q),\qquad
 r(s)=1+e^{4\alpha_{\rm eff}s}.
\]

For all complex `X`,

\[
 \|e^{-sL_{\rm ch}}X\|_{r(s)}\le\|X\|_2.
\]

At `s=0` equality holds. Differentiation in the tracial setting at normalized `X` gives

\[
 0\ge \alpha_{\rm eff}\operatorname{Ent}(X)
 -\operatorname{Re}\operatorname{tr}_d[X^*L_{\rm ch}(X)].
\]

Hence for arbitrary `X`, including nonnormal matrices,

\[
 \boxed{\operatorname{Ent}(X)\le A_b\mathcal E_{\rm ch}(X).} \tag{9}
\]

The finite-dimensional Schatten-norm derivative exists at exponent 2; zero singular values cause no problem because `x ln x -> 0`. The tracial left/right entropy terms coincide by equality of singular values. This audit imports the functional inequality, rather than claiming an independent proof of that paper's tensorization theorem.

## 5. Resulting pure and mixed output witness

Set

\[
 a_b=\frac{A_b}{bm}.
\]

Combining (6) and (9) in the correct direction gives

\[
 S(\psi_{X,A})\ge tNm-a_bm\sum_{a,i}[1-P_{ai}(X)]
 -a_bt(b-1)m. \tag{10}
\]

The right side is affine in the finite output state. Therefore every decomposition of a mixed output `ω` satisfies the same average lower bound, and taking the convex roof yields

\[
 E_F(\omega)\ge tNm-a_bm\sum_{a,i}[1-P_{ai}(\omega)]
 -a_bt(b-1)m. \tag{11}
\]

This step uses the definition of `E_F`, not additivity.

Let a complete normal LOCC preparation turn `Φ_(M_t)` into `τhat_t` with

\[
 \tfrac12\|\widehat\tau_t-\tau^{\otimes t}\|_1\le\varepsilon_t,
 \qquad \varepsilon_t\to0.
\]

Compose with the independent `N`-block extraction experiments and discard memory, obtaining a finite output `ωhat_t`. Normality and trace-norm contractivity give a global output error at most `ε_t`, so each individual prefix-test probability differs from the target probability by at most `ε_t`. Thus

\[
 \sum_{a,i}[1-P_{ai}(\widehat\omega_t)]
 \le t\delta\frac{N(N-1)}2+tN\varepsilon_t. \tag{12}
\]

Also `E_F(ωhat_t) <= ln M_t`. One rigorous way to avoid any infinite-dimensional trajectory claim is to view the complete composite map as a finite-input, finite-output LOCC channel. Its Choi state is separable across `(Alice output, Alice reference):(Bob output, Bob reference)`: local reference Bell states are initially product across parties, and complete LOCC preserves separability. Finite-dimensional separable Choi decomposition gives product Kraus operators. On `Φ_(M_t)` each pure Kraus branch has Schmidt rank at most `M_t`, and hence entropy at most `ln M_t`. This also covers intermediate normal infinite memory and discarded local registers.

Combining (11)-(12), dividing by `t`, and taking the formation limit at fixed `N,b` gives

\[
 \boxed{E_C(\tau)\ge m\left[N-a_b\delta\frac{N(N-1)}2
 -a_b(b-1)\right].} \tag{13}
\]

The explicit per-copy preparation-error term before the limit is `a_b m N ε_t`. There is no `t ε_t` requirement, no memory-dimensional continuity assumption, and no interchange of an increasing `N` with the formation limit.

## 6. Asymptotic optimization of the coarse bound

For fixed `D>=2`,

\[
 a_b=\frac{3\ln2}{2}\frac{\ln(D^b-1)}{b\ln D\,(1-2D^{-b})}
 \longrightarrow c=\frac{3\ln2}{2}.
\]

For any family with `δ -> 0`, first apply (13) for each fixed member with finite chosen `N,b` and take its formation limit. Then choose `b=b(δ)` with `b -> infinity` and `δ b -> 0`, and choose `N` as a multiple of `b` within `b` of `1/(a_b δ)+1/2`. Completing the square shows the rounding error in `δ` times the bound is `O((δb)^2)`, while the subtracted chain correction contributes `O(δb)`. Therefore

\[
 \liminf_{\delta\downarrow0}\frac{\delta E_C(\tau_\delta)}m
 \ge\frac1{2c}=\frac1{3\ln2}=0.4808983469\ldots. \tag{14}
\]

For example `b=floor(δ^(-1/2))` is adequate, with an eventual minimum of one. This verifies the proposed optimization. The coefficient is below the stronger stopping value `1/2`.

## 7. Stronger stopping baseline without any entanglement additivity

Let `K in {0,...,N}` count initial consecutive Bell passes in one extraction experiment. The target distribution is `π`, with

\[
 \pi_0=0,\qquad \mathbb E_\pi K=\sum_{i=1}^Np_i.
\]

For `t` target copies the actual distribution is `π^(tensor t)`. For approximate formation let its measured distribution be `P_t`, within total variation `ε_t` of this iid target.

Compare the formation input with the explicitly separable state

\[
 \chi_{M_t}=\frac1{M_t}\sum_{j=1}^{M_t}|jj\rangle\langle jj|,
 \quad D(\Phi_{M_t}\Vert\chi_{M_t})=\ln M_t.
\]

Its image under formation and all extraction channels is globally separable across all Alice versus all Bob output registers. Let `Q_t` be its stopping distribution. For every subset `A` of chains and every choice `i_a>=1`,

\[
 Q_t(K_a\ge i_a\ \forall a\in A)
 \le D^{-\sum_{a\in A}i_a}. \tag{15}
\]

The event is a joint Bell projection of total Schmidt rank `D^(Σ i_a)`, tensored with identities on untested output registers. A globally separable state has overlap at most its inverse Schmidt rank. The proof uses the unconditioned full output state. Conditional memory need not remain separable, and `Q_t` need not factorize.

As a quick version, each stopped cell obeys `Q_t(kvec)<=D^(-Σ k_a)`. Data processing and elementary Shannon continuity give

\[
 \frac{\ln M_t}{t}\ge m\sum_i p_i-H(\pi)
 -[mN+\ln(N+1)]\varepsilon_t-\frac{h_2(\varepsilon_t)}t.
\]

Hence `E_C >= mΣp_i-H(π)`, and `H(π)<=ln N` since `π_0=0`.

The sharper finite constant in (S) also follows. Fix `L>0` and define

\[
 g_L(0)=e^{-L},\qquad g_L(k)=D^k\quad(1\le k\le N),
 \quad f_L(\mathbf k)=\sum_{a=1}^t\ln g_L(k_a).
\]

Expand each `g_L(K_a)` as its positive constant plus positive increments times the tail indicators `1_{K_a>=i}`. Applying (15) term by term gives

\[
 \mathbb E_{Q_t}e^{f_L}
 \le Z_L^t,
\]

where

\[
 \begin{aligned}
 Z_L&=e^{-L}+\sum_{i=1}^N[g_L(i)-g_L(i-1)]D^{-i}\\
 &=1+(N-1+e^{-L})(1-D^{-1}). \tag{16}
 \end{aligned}
\]

The classical variational bound and quantum data processing give

\[
 \ln M_t\ge D(P_t\Vert Q_t)
 \ge \mathbb E_{P_t}f_L-t\ln Z_L.
\]

The function `f_L` has range width `t(mN+L)`. Since `π_0=0`, its iid target expectation is `tmΣ_i p_i`. Thus the fully explicit finite-error statement is

\[
 \boxed{\frac{\ln M_t}{t}\ge m\sum_i p_i-\ln Z_L
 -(mN+L)\varepsilon_t.} \tag{17}
\]

At fixed `N,L`, let the formation error tend to zero, and only afterward let `L -> infinity`. This yields (S). The auxiliary `L` is only a bounded classical test penalty, not a physical resource or postselection step. For `N=ceil(1/δ)`, use `Σ_i[1-(i-1)δ]_+ >=1/(2δ)+1/2` and `ln Z_0 <= ln N <= ln((1+δ)/δ)` to obtain (S2). For `δ=0`, sending `N -> infinity` forces `E_C(τ)=infinity`.

## 8. Deterministic checks and scope boundaries

`check_inequalities.py` completed successfully and wrote `CHECK_RECEIPT.json`:

* 576,650 operator-support patterns through `N=16`, for all chunk divisors, satisfy the eigenvalue comparison; minimum gap is zero.
* 56 finite coefficient matrices across four `(D,N,t,b)` cases include nonnormal complex matrices, positive matrices, identity, and rank-one diagonal matrices. Bell contraction versus conditional-expectation norm agrees within `3.34e-16`; all tested coarse and imported-LSI inequalities pass.
* Local diagonal extremizers `diag(Q-1,1,...,1)`, after normalization, reproduce the exact inverse local constant for `Q=3,...,20`.
* The positive-increment moment formula (16) matches its closed form in four independent parameter cases.

These checks detect normalization or indexing errors; they do not prove the imported tensorization theorem, universal theorem correctness, historical novelty, or physical advantage. The product LSI paper is a primary mathematical input, while the stopping proof (15)-(17) is independent of it. The separate exact-factory optimality theorem is not re-audited here. A sufficient explicit iid-formation upper bound is checked in the addendum below.

## 9. Source receipt and claim status

Primary sources read live and saved as HTML in `sources/`:

1. Dong et al., arXiv:2606.17729v3: definitions of normalized norms, entropy and Dirichlet form; Theorem 3.12; Theorem 3.1 and Lemma 3.2 for arbitrary operators.
2. Beigi, Datta, Rouzé, arXiv:1804.10100v2: Theorem 25, exact local constant in every finite dimension.

Firecrawl returned an out-of-credits error; no fetched content came from that failed call. Source verification continued through direct arXiv browsing and the exact primary HTML. No account change, publication, external message, or other chat action was taken.

Status axes:

| Claim | Status |
|---|---|
| Coarse spectral comparison | PROVED in this audit |
| Pure coefficient and Bell probability normalization | PROVED and finite-checked |
| Quoted primary LSI constant and hypotheses | VERIFIED against live v3 and local-constant primary source |
| Independent proof of imported product LSI | NOT_ATTEMPTED |
| Approximate iid formation transfer at fixed tests | PROVED; no additivity or continuity assumptions |
| Proposed `1/(3 ln 2)` asymptotic law | VALID but DOMINATED |
| Stronger finite universal stopping converse (S) | PROVED and independently cross-audited |
| Removal of logarithmic penalty / exact critical tensor witness | NOT_ESTABLISHED |
| Historical novelty / external correctness certification | UNKNOWN |

## 10. Requested fresh audit of principal `PROOF.txt`, sections 1-2

The principal proof was read after the initial independent analysis and after writing the substantive audit above. Its Theorem 1, refined `Z_(N,L)` calculation, and operational limit order all pass. In particular the statement uses actual complete normal LOCC channels and actual nested output-prefix probabilities; it does not infer LOCC merely from normality. All joint-tail events use the unconditioned separable comparator state. The range in its equation (5) means range width `t(Nm+L)`, which is the correct total-variation coefficient. The limits are taken first in the formation sequence at fixed `N,L`, then in `L`; the optimization in `N` is a subsequent choice of a finite test.

The finite optimal-cost bracket in its equation (7) follows, with an upper bound that needs no maximally-correlated-state additivity theorem. Here is a complete sufficient argument.

Let `d` be the elementary Bell rank and `J` the exact elementary output count, so `m=J ln d`. Set `L=ceil(J/δ)` and `M=J+L-1`. On an `M`-pair memory initialize

\[
 \widetilde\tau=\frac1L\sum_{k=J}^{J+L-1}
 \Phi_d^{\otimes k}\otimes\chi_d^{\otimes(M-k)},
 \quad \chi_d=\frac1d\sum_{a=0}^{d-1}|aa\rangle\langle aa|.
\]

The same local shift-and-append-`χ_d` device emits the first pair on each call. All first `J` outputs are exact on every rung. After `j<=J` calls, the complete memory has the same form with uniform rungs shifted down by `j`; the original and shifted classical uniform rung distributions have total variation `j/L` because `L>=J`. Applying their common preparation map gives

\[
 \tfrac12\|\widetilde\tau_j-\widetilde\tau\|_1\le j/L\le\delta.
\]

There is no accessible retained rung flag in `τtilde`.

Expand each separable `χ_d` factor in its explicit product-pure ensemble. A pure branch at rung `k` has entanglement exactly `k ln d`. For `t` independent initializers sample the rung and separable labels for all copies. With probability tending to one, the total sampled stock is at most `t(EK+η)` by the ordinary bounded-variable law of large numbers. On those branches prepare all required Bell stocks from one fixed rank `d^ceil(t(EK+η))` Bell input, using local operations, and prepare the product tails freely. On the vanishing-probability exceptional branches output any fixed state. The resulting global half-trace error is at most that exceptional probability. Genuinely erase the sampled initializer flags at the end. Sending `t -> infinity`, then `η -> 0`, gives

\[
 E_C^{\rm op}(\widetilde\tau)\le (\mathbb E K)\ln d
 =\left[J+\frac{L-1}{2}\right]\ln d
 \le\frac{m}{2\delta}+m. \tag{18}
\]

The fixed Bell input can prepare any smaller uniform Schmidt rank deterministically by LOCC; alternatively take an integer number of elementary Bell pairs large enough for the sampled stock. Local randomness and communication carry no incoming shared entanglement. The shift factory itself uses no new shared entanglement after initialization.

Combining (18) with the universal lower bound (S2) yields, for both terminal and all-elementary-prefix return optima,

\[
 \frac m{2\delta}-\ln(1/\delta)+O_{J,d}(1)
 \le E_C^{{\rm op},*}\le\frac m{2\delta}+O_{J,d}(1).
\]

Consequently the coefficient `1/2` is sharp for optimal operational iid formation in this model. This does not determine the negative logarithmic subleading term. No stronger baseline in the arguments audited here removes it for generic memories: an exact expected-cost theorem with an immutable preselected initializer flag is a different operational obligation, and additivity on a maximally correlated support is a restricted-state theorem. This addendum does not claim an exhaustive external search proving that no such theorem is known.
