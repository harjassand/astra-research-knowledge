# Independent review: acquired power-contraction kernel

31 October 2026. Mathematical-existence local PASS, not a complete source/process compiler or an implementation claim.

## Exact source binding

I read all ten sections of `GROUPED_POISSON_KERNEL_CONSTRUCTION.md` in the original workspace, including its final nilpotent-shift limitation, and checked the final bytes: 14,750 bytes, SHA-256 `150152b77d81cb47781d97d600f55d0b8d0d0a9c35a0891009cce58936792b4a`. This receipt binds that version, not the earlier 14,335-byte candidate.

The interface is substantive: a contraction A with an acquired normalization-one controlled block encoding and inverse; an acquired reflection about a reducing orthogonal projector P; and an actual certified integer m with ||A^m Q|| <= 1/4, Q=I-P. These are not obtained merely from a spectral gap or an unspecified mixing assertion. Costs of all supplied circuits and their precision are additional.

## 1. Positive expansion and time cutoff

For q=2^(-1/m), a'= (1-q)/2, B=2 A^m Q, n=km+r, the identity A^n Q=2^(-k) B^k A^r Q is correct, including k=0 when the terminal Q must remain. Substitution in the exponential gives exactly the displayed nonnegative weight exp(-a't) Pr[Poi(qt)=n] 2^(r/m-1). Its total is at most exp(-a't), and every selected product is a contraction. This is a genuine matrix-product expansion for nonnormal A, not functional calculus on its singular values.

The elementary inequality a' >= 1/(8m) is sufficient for the stated T_*=8m ell. On t>=T_* the exact zero block has error at most exp(-ell). On the active branch the Markov bound using E 2^N=exp(qt), K=2(T_*+ell), gives the claimed uniform tail. Thus K=O(m ell), J=O(ell); there is no loop proportional to an arbitrarily large t. The derivative F'=(A-I+a'I)F has norm at most 3, so optional finite time rounding is paid in absolute operator norm.

## 2. Amplification, products and normalization

The product construction for A^m Q uses fresh block ancillas. Uniform singular-value amplification with constant slack can approximate 2A^m Q to error eta_B with O(log(1/eta_B)) uses of that product encoding. Only this scaling is a singular-value operation. Subsequent powers of its top block are ordinary products, and contraction telescoping gives error at most k eta_B. The stated eta_B and maximum k=J pay this error uniformly.

SELECT with padded conditional loops, fresh factor ancillas and the final Q is valid. No intermediate success measurement, reset of failed ancillas, or amplification of the final small-norm output is implicit. A residual probability arm with an orthogonal success-flag flip is a zero block. Hence PREPARE-dagger SELECT PREPARE encodes the sum at normalization exactly one.

These steps use standard QSVT/amplification and block-encoding tools, not new general primitives. The primary framework is Gilyen, Su, Low and Wiebe, https://arxiv.org/abs/1806.01838 . The receipt does not claim novelty for their use.

## 3. Finite arithmetic and coherent input time

All active-branch arguments, retained factorial indices and data-array lengths are polynomial in m and ell. Absolute interval evaluation avoids demanding relative accuracy of negligible weights. Nonnegative dyadic lower weights make the residual probability nonnegative by construction. Their total deficit bounds the squared distance of square-root preparation states; the two-sided PREPARE perturbation is therefore paid by the stated conservative precision.

A binary tree of dyadic prefix probabilities is an explicit finite preparation, with separate branches for zero sums. Nonzero sums are at least 2^(-b), so division precision is polynomial in b, not inverse probability. This deliberately unoptimized O(K) preparation is sufficient. Uniform deterministic arithmetic controlled by a finite binary t register gives a block-diagonal error bound valid on superpositions. The source is an acquired coherent preparation, not a free stochastic oracle.

The clean query theorem presumes exact supplied unitaries. For synthesized circuits, every controlled, forward and inverse use must be approximated so their accumulated unitary error meets the ledger. A fixed noisy encoding without refinability does not inherit the gate theorem. That qualification is explicit in the source and remains binding.

## 4. Resources and strongest scope

The displayed A-query count O(m ell log((ell+1)/epsilon)+m) follows from J amplified m-fold products plus the remainder powers. Workspace, arithmetic, reflection and rotation costs are polynomial in m, ell and finite input lengths; actual encoding costs multiply query counts. The claim is polynomial in m, not logarithmic in m. An output-state preparation still pays inverse success norm; a retained-memory CP compiler still needs all its other branches and complete-isometry construction.

The contour comparison is a sound analytic interface observation: the same power certificate implies ||(zI-AQ)^(-1)|| <= 4m on |z|=q, with the spectrum strictly inside. The stated scalar function and derivative bounds are uniform in t. The additional norm slack ||F|| <= 1/sqrt(2) follows by combining the Poisson contraction bound with the positive grouped bound. This makes an ordinary contour/resolvent route a strong comparator; this receipt does not independently certify its optimized gate schedule or all bibliographic claims in Section 9.

The unilateral nilpotent shift limitation is correct: its first qualifying power can be dimension-sized despite spectrum {0}. Therefore this theorem does not fast-forward arbitrary spectrally stable nonnormal operators from spectral information alone.

## Verdict

No load-bearing mathematical or finite-arithmetic gap found in this local construction under its explicit acquired-input and precision conventions. It supplies the scaled, decaying contraction block that an unscaled mixing estimate alone did not supply. Source realization, stationary-state acquisition, jump-stack access, complete CP assembly and a uniform controlled-process error theorem remain separate obligations. No new whole compiler, novelty, practical speedup, implemented circuit, or dimension-free acquisition claim follows from this receipt.
