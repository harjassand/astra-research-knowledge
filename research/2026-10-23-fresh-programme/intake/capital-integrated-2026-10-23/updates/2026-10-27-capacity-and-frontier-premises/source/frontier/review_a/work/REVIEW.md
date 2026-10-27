# Independent mathematical review of L31 and L84

27 October 2026. **Neither endpoint proves all-copy Werner positivity or supplies a negative admissible Werner witness. Both contain correct substantive mathematics beyond the frozen initial state. L84 completes its declared conditional local theorem; L31 supplies a valid generic obstruction and an exact global output reformulation, without deciding its reachability obligation.**

This review is **not blinded**. The unchanged endpoint prose says “Warm continuation” (L31) and “Fresh continuation” (L84), and refers to frozen stages. I saw that language. I did not inspect a treatment key, protocol/hypotheses, the other pair, private programme files, or live researchers' folders. Scope: the supplied initial/L31/L84 copies, common public packet, complete pinned N525 proof, the permitted read-only `git show`, and the primary papers cited below. This is a substantive internal mathematical review at that scope; external specialist approval is not a prerequisite for the conclusions below.

## Initial knowledge and prior overlap

The [initial result](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/review_a/inputs/initial/RESULT.md) already proves the full Hessian normal form at every `diag(uv*,uv*,0)` and the equivalence of PSD Hessians over that family with the complete lower-copy assertion `W_m`. It explicitly leaves the cubic/quartic compatibility obligation open. Its singular-value margin is a stronger unproved attempt, with only a boundary case completed.

The common [CT source](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/public/astra/updates/CT/package/work/COORDINATOR_NPT_LOCAL.txt:21) already proves an all-orders local theorem for its moving binary spin-flip family; lines 144–167 give the exact repeated-block lift and a critical zero outside that family. The [BD source](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/public/astra/updates/BD/package/npt/RESEARCH_RECORD.md:67), Sections 3–4, already supplies the crossed identity and the restricted transverse lift. These do not prove L84's arbitrary-tangent transfer at arbitrary entangled repeated blocks.

The complete [N525 prior](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/review_priors/N525_RESEARCH_PROOF.md), Sections 3–5, already constructively transfers any negative arbitrary complex rank-two witness to rank-two PSD matrices and then flat orthogonal projections after padding, with an explicit error bound and persistent unscaled negative-gap dichotomy. Thus unrestricted-support global reduction was already available: L31 is not the first such reduction. N525 does not supply L84's Gram-slice theorem or L31's particular fixed `6×6` output construction. Its SHA256 is `9b15f562766a5622fd971730a05d056cc5f5ae12c7729f186fcca33d26d905a3`; it exactly matches the permitted pinned `git show`.

Historical novelty of either endpoint is unestablished. [Vollbrecht–Wolf, quant-ph/0201103v2](https://arxiv.org/pdf/quant-ph/0201103), equations (3)–(6), the point `tau^(5)`, and equation (8), already provide the symmetric PPT activator, Bell-filter protocol, and one of L31's product-zero constructions. [Clarisse, quant-ph/0510035v3](https://arxiv.org/html/quant-ph/0510035v3), Section III.2, already reformulates distillability through separability and tensor witnesses. These general principles and PPT-only certificate limitations cannot be credited as new discoveries here. [Fu–Gao–Park v3](https://arxiv.org/html/2607.21367v3), Theorem 1.1, reports the two-copy theorem while explicitly leaving higher copies open; it is prior, not either endpoint's contribution.

## L84: the all-orders local transfer is proved under exactly W_m

**Accept the theorem as written** in [local_transfer.md](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/review_a/inputs/L84/local_transfer.md:26). It is a genuine new restricted result relative to the initial state and supplied Astra priors. It assumes positivity for every complex rank-at-most-two lower-copy matrix; no positivity of arbitrary same-copy matrices is smuggled in.

The load-bearing argument reconstructs as follows. A rank-two chart exists near the nonzero rank-two base. A common physical unitary puts the isolated lowest eigenline of the combined factor Gram matrix in coordinate 2, imposing

`<U_i,X> + <V_i,Y> = 0`, `i=0,1`, where `X=U_2`, `Y=V_2`.

There is a minor convention to keep explicit: for the conjugate-linear-first Gram matrix its transformation is `G' = conjugate(g) G g^T`. If `Q` is a nearby orthonormal eigenframe, choose `g=Q^T`. This gives the claimed slice with a physical conjugation and preserves the functional. This is a clarification of the written proof, not a repair requiring a stronger premise.

The exact first-site splitting is

`q_(m+1)(UV*) = q_binary(B) + T_P(X,Y) + q_m(XY*)/2`.

The binary term is half the sum of the six lower-copy quadratic forms obtained by contractions against the orthogonal Pauli dyads. Each contraction has rank at most two, as does `XY*`; hence these two terms are nonnegative under exactly `W_m`. Positivity of the binary ambient operator alone would not suffice, but the supplied separable decomposition does suffice.

At the base, `T_0` is the sum of crossed squares of `x_a tensor v - u tensor y_a`. Its kernel is exactly `(x_a,y_a)=(lambda_a u,lambda_a v)`. The slice removes this kernel. With `delta=2^-m`, binary factor perturbation `epsilon`, and `w²=||X||²+||Y||²`, the proof's estimates are valid:

`T_0 >= delta(1-epsilon²/2)w²`,

`|T_P-T_0| <= [(2 sqrt(2)+1)epsilon + 5epsilon²/4]w²`.

For `epsilon <= delta/10`, their difference is greater than `delta w²/2`. The exact worst-case coefficient is `353/400 - sqrt(2)/5 > 1/2`. Smooth factor charts and the isolated eigenline ensure every sufficiently nearby rank-two matrix admits this slice; proximity to the rank-two base excludes rank-one singularities. Therefore the whole neighborhood is nonnegative, and every nearby zero has a common physical binary plane. No lower-copy zero classification is required.

This is more than a PSD Hessian assertion: it controls all nearby matrices, so for every frozen factor-curve direction with `Q=0`, both signs of small real `t` force the cubic coefficient to vanish and its constrained quartic to be nonnegative. The quartic conclusion concerns only those kernel-constrained products; it is not an assertion about arbitrary rank-two matrices at `m+1` copies. The known exact lift gives the converse over all repeated blocks. Thus local stability of this entire family is equivalent to `W_m`, and does not yield free induction. For `m=1` it is unconditional; importing the reported two-copy theorem gives the corresponding local three-copy statement, never global three-copy positivity.

The [global discriminant](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/review_a/inputs/L84/global_obligation.md:8) is also correct: under `W_m`, arbitrary factors give `a+t²T+t⁴d/2` with `a,d>=0`, whose positivity for all real `t` is exactly `T>=-sqrt(2ad)`. This is an equivalent unproved global obligation, not a certificate. The exact negative sliced `T`, negative two-plane, and normalized PPT activation countermodel all replay correctly. They refute the stated generic simplifications; none refutes the actual Werner target.

## L31: valid local-geometry countermodel and constructive output normalization

**Accept the auxiliary theorem and countermodel** in [RESULT.md, Section 1](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/review_a/inputs/L31/RESULT.md:24). For `B,B^Gamma>0`, the initial Hessian identity has kernel exactly tangent to `M={P_E tensor uv*}`, of real dimension `4N+2`. The upper-block normal norm is `||H00-H11||²/2+||H01||²+||H10||²`; each transverse square dominates the distance to the common-plane directions. Thus the Hessian is positive on the normal complement. Every point of M is a critical zero. Adapted coordinates and Taylor's integral formula give actual local minima and the local zero manifold; compactness gives a uniform radius on normalized M. This familiar Morse–Bott reasoning is sound here, rather than an inference from isolated Hessian tests.

The displayed `sigma6` is exactly the normalized local qubit compression of Vollbrecht–Wolf's `tau^(5)` activator. The compression has trace `7/15`. Its PT decomposition is correct, and mixing gives `B,B^Gamma>=I/360`. Independent direct operator contraction recovers the **whole** polynomial

`Q_B(C(t)) = (1409/5040)t² - (73/840)t⁴`,

with factor Grams `(1+3t²)I_2`, so rank is exactly two for every real t. At `t=2` it is `-49/180`. The same path in the actual qutrit functional is `6t²+(33/2)t⁴`, with value `288` at `t=2`. Consequently even a positive-definite PPT base, all these local minima, and a uniform local radius do not imply global positivity after adding K. This is a useful exact obstruction beyond the initial handoff, built from known activation theory; it is not a Werner counterexample or a no-go theorem for tensor-specific arguments.

**Accept the fixed-output equivalence**, [Sections 2–3](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/review_a/inputs/L31/RESULT.md:82). For every rank-two `C=u0 v1* - u1 v0*`, the specified filters acquire it by the fixed Bell/singlet contraction. Bob's transpose is correct: `B^T=conjugate(B*)` supplies the conjugated right factors in vectorization. Direct contraction gives

`<xi,(rho^Gamma tensor s^Gamma)xi> = ell/90`,

`q_(m+1)(C) = (15/2)^(m+1) ell/5`.

The four-sector twirl retains this functional. The converse produces rank at most two. Cone generation, adding a spare filtered copy, and closure do not introduce a new negative sign, so `ell>=0` on the resulting cone is exactly the original target. The explicit acquisition maps make this more than an unsupported assertion that an auxiliary object exists. **However, the definition does not construct an invariant or compute the reachable cone:** arbitrary filters still have `6×3^m` entries, and the four coefficients have no proved closed recursion. It is a global representation with an unresolved target-specific acquisition problem.

The separable zero state z and its coefficients are correct. Its eigenvalue bounds `z>=I/144`, `z^Gamma>=I/192`, and `ell(z)=0` yield, at `t=1/386`, `tau>=I/288`, `tau^Gamma>=I/384`, and `ell(tau)=t ell(s)<0`. Separable preparation and stochastic branch mixing require no free entangled resource. Conversely an SLOCC output has product-Kraus branches, and a negative average has a negative branch; appending one Werner copy gives an ordinary finite-copy witness. Thus the strict-PPT reachability equivalence is valid, including finite exact twirling. It removes output PPT-boundary conditioning but supplies neither a uniform negative `ell` margin, controlled success probability, nor bounded filter-acquisition cost. The positive-subtraction optimality/nondecomposability arguments from full-rank z and z^Gamma are correct but overlap established tensor-witness/activation theory. No impossibility or reachable filters deciding this equivalence are supplied.

## Verification and disposition

Four copied endpoint scripts completed under `python -B -O`; their stdout/stderr receipts are in `L31/` and `L84/` here. My independently written [exact checker](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/review_a/work/independent_exact_checks.py) verifies the binary operator identity and coercivity constant, the full L31 polynomial with a separately constructed operator/partial transpose, its actual Werner control, and the prior compression. One additional complex `6×9` filter pair checks the acquisition map at three total copies by direct subset partial traces: `q3=603/4`, `ell=134/75`, exact residual zero. These finite identities support the algebra; they do not certify the open target. [Receipt](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-next-20261027/frontier_trial/review_a/work/independent_exact_checks.json).

No endpoint proof repair was needed. The explicit Gram transformation and independent checks above are reviewer work and are not credited as endpoint inventions. All 31 frozen input files retained their hashes; no mathematical replay errors occurred. No external novelty audit or full audit of the cited two-copy paper is claimed.

**Disposition:** L84 has a completed conditional all-orders local transfer that closes the initial local compatibility obligation, plus valid global obstructions; its all-copy obligation remains. L31 has a completed generic local/global countermodel and a correct fixed-output, uniformly strict-PPT global reduction, largely using established activation/separability principles; its coherent-filter reachability obligation remains. Neither is a completed foundational proof/counterexample, and neither should be downgraded to merely numerical evidence or upgraded to a global solution.
