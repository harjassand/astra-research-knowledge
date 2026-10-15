# Follow-up: the anisotropic G certificate passes the receiving audit

Date: 2026-10-15. Root explicitly authorized this follow-up after `REPORT.md` and `DECISION_DERIVATIONS.md` were frozen. The new proof was read only after that freeze. The earlier independent report remains unchanged.

The new mathematical route survives this internal audit. The impossible premise `G−epsilon|A|^4` quasiconvex is replaced by a verified **anisotropic** convex subtraction, elliptic on compatible gradients. This supplies pure fourth-power Jensen coercivity with constant `1/2500000` and pairwise Lipschitz required-supply storage on every bounded strong critical-trace ball. The source's exact negative-entry construction also survives and preserves the weak-topology and finite-observation obstruction. External mathematical correctness, historical priority, computational tractability, and physical capability remain unestablished.

The result changes the continuation recommendation for G. Retain the exact new margin and use its quantitative trace consequences where the actual input trace/tail is supplied or acquired. Do not keep attempting the disproved isotropic subtraction. Do not promote the required-supply infimum to an obtained finite evaluation operation.

## Exact evidence checked

The authorized source is `R/workers/qc_genesis_astra`, where R is `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-regularization-clock-pressure-v1`.

| Evidence | Exact read/check |
|---|---|
| Original `G_EXACT_HEAT_CERTIFICATE.json` | SHA `4004e6144335150a5b3569dfb7b4d0b836f2776497c271e7f31b2faf52830000`; raw source copied unchanged. |
| New `REPORT.md` | Read the complete 447-line first snapshot, SHA `f0e02e09ea79c52a574de3c7f0e9eeff02f392ba8c58baccc8f173bcb1c21e04`, then the author's nine-line abstract-transfer addition. Both versions are retained separately; `QC_REPORT_ADDITION.diff` records the delta. |
| New `verify_distortion_margin.py` | Read all 242 lines, SHA `0eb13671d3682008eecbe76a73b2a968e02ca55d3855407c5746bcf6dcbf4773`; it reads its copied source and writes only in its own run directory. |
| Outside-copy replay | `qc_replay/`: exit 0, nine exact algebra groups pass, including full original identity/closedness/primitive, 18 positive updated LDL pivots, rank-two subtraction, and the averaged rational Gram/form identity. This is an author-verifier replay reviewed by another role, not an independently implemented formal proof. |
| New certificate | `DISTORTION_MARGIN_CERTIFICATE.json`, SHA `620c37c6ff9cb8d7cccd051197c431dc6b5348bda334e6cf9cd448249aba358e`; replay regenerates identical bytes. |
| External analytic premise | Retrieved the original Bañuelos–Janakiraman PDF and visually inspected page 2, Theorem 1.1(1.4). It states the complex-valued `Lp` norm bound `sqrt(2(p^2−p))` for p≥2, hence `sqrt24` at p=4. [Primary PDF](https://www.math.purdue.edu/~banuelos/Papers/Beur_Ahl.pdf). Local SHA `430876e18a0941fdfbdf30d33dc73dd876cccd39c2d38cc735610fcc45363a66`; rendering and receipt are in `qc_external/`. |

No newer sharp-norm result is a premise. A recent arXiv metadata result surfaced during source search, but its proof was not audited or imported.

## Why the certificate gives the required margin

Let `r=a−d`, `s=b+c`, and `H(A)=(r^2+s^2)^2`. In the original Heat18 basis `ell=C^T Z`, the exact identities

\[
\ell_0-\ell_{12}+\ell_{16}=r(z_0-z_4),\qquad
-\ell_{13}+\ell_{17}=r(z_1-z_5)
\]

put the heat Hessian of r⁴ inside a rank-two update of the reduced Gram. With

\[
K=12[d_1v_1v_1^T+d_2v_2v_2^T],\qquad \epsilon=1/2000,
\]

the exact matrix `S−epsilon K` is positive definite. The unchanged closed two-form and updated Gram give an exact heat certificate for `G−epsilon r^4`. Its analytic all-background heat/Stokes implication has the same hypotheses as the earlier G proof; no search trajectory, finite frequency check, or approximate eigenvalue enters.

Left output rotation preserves G and compatible gradients. Averaging angles 0, π/4, π/2, 3π/4 replaces r⁴ by `(3/8)(r²+s²)²`, so

\[
G-\kappa H\text{ is quasiconvex at every background},
\qquad \kappa=3/16000.
\]

The averaged rational Gram and closed form are checked directly in the replay. Their positivity also follows from their explicit finite average of positive-factor Grams. This avoids silently transferring a result between different integrands.

## Receiving analysis and constants

For `f=phi1+i phi2`, the CR defect is `C Dphi=2 partial_bar f`, and

\[
|D\phi|^2=2(|\partial f|^2+|\bar\partial f|^2).
\]

The complex Beurling bound and Minkowski therefore give

\[
\|D\phi\|_4^4\le\frac{625}{4}\|\mathcal C D\phi\|_4^4.
\]

The affine quartic Bregman remainder satisfies

\[
|x+h|^4-|x|^4-4|x|^2x\cdot h\ge|h|^4/3.
\]

The exact remainder SOS in the new proof checks, so quasiconvexity of `G−kappa H` yields

\[
\int[G(B+D\phi)-G(B)]
\ge\frac{\kappa}{3}\int|\mathcal C D\phi|^4
\ge\frac1{2500000}\int|D\phi|^4.
\tag{1}
\]

This is compatible with zero rank-one **quadratic curvature** at `(I,e12)`: it is fourth-power control. It does not assert a uniform `|B|² ||Dphi||₂²` term.

I reconstructed the width-independent strip extension separately. Zero-endpoint W^(1,4) strips extend by zero in x without a derivative-matching requirement. After periodic repetition in y, multiplication by `chi(y/N)` permits use of the plane CR estimate. For each fixed finite strip, main fourth-power integrals scale as N; derivative-cutoff errors vanish after that normalization. No Poincare constant depending on strip width is used. The all-background Jensen inequality holds on the closed strip by periodizing in x and using Sobolev density in the periodic heat proof. Moving transverse means cause no incompatibility.

The growth constants in the report also check analytically. For G's four polynomial terms, the Hessian norm contributions are bounded by `144`, `35/2`, `3`, and `15`, times |A|²; their sum is `359/2<180`. Integrating the Hessian gives

\[
|Df_B(A)|\le180(|B|^2|A|+|B||A|^2+|A|^3),
\]

and its second integral gives `90|B|²|A|²+60|B||A|³+15|A|⁴`, bounded by `120(|B|²|A|²+|A|⁴)`. Thus the sharper author constants C0=120, C1=180 are valid; the larger constants in my conditional reconstruction were merely conservative.

Glue any incoming path to the fixed unit-width reflected return. Equation (1) and the return bound yield

\[
J_B(\Phi)\ge\gamma\|D\Phi\|_4^4-M_B(U),\qquad
M_B(U)=120[|B|^2 e_2(U)^2+e_4(U)^4].
\]

Since `|p_B(U)|≤M_B(U)`, an eta-minimizer obeys

\[
\|D\Phi\|_4^4\le\gamma^{-1}[2M_B(U)+\eta].
\]

To compare U,W, prepend zero padding if necessary and perturb **only the terminal unit slab** by the fixed extension of W−U. There, L2 and L3 factors are bounded by L4 on unit measure. The source's formula (11) follows with `h=C_E||W−U||_X`, and its displayed formula (12) is a finite pairwise Lipschitz constant on `||U||_X,||W||_X≤R`. Using full-strip L2 norms instead would leave a width-dependent gap; the source correctly avoids that step.

The original-action storage must retain `DG(B):(mean(U)|0)`. Constant-shift invariance of the adjusted storage follows from arbitrarily slow ramps in a path class that allows moving means. These boundary and normalization details are present in the proof. A full independently reconstructed receiving implication is saved in `CONDITIONAL_RECEIVING_PROOF.md`; the premise left conditional there has now passed the exact certificate audit.

## Negative entry and finite-information boundary

The two-piece compatible radial entry has exact action

\[
\frac{137}{120}\left(\frac14\right)^4
-\frac{1-(1/4)^4}{96}
=-\frac{727}{122880}.
\]

Its fourth-power gradient energy is `3853/3840`. Reversing x and y produces the same negative action from the opposite winding to zero, so incoming storage at the two profiles lies on opposite sides of zero by at least `delta0=727/122880`. Concatenation with a negative exit proves the lower bound on the opposite profile; the exit itself is not an incoming upper bound.

The scaled profiles `N^(−3/4)(cos Ny, ±sin Ny)` stay bounded at critical W^(3/4,4) regularity and converge weakly to zero. The quartic entry action is scale-invariant; at nonzero B the quadratic correction is O_B(N^(−1/2)) and the cubic transverse average vanishes by oddness. Consequently both weak lower and weak upper semicontinuity fail at zero, while the newly proved strong bounded-ball Lipschitz continuity remains consistent. Fixed finite Fourier observations miss both high-frequency profiles; their storage separation forces worst-case error at least delta0 on that bounded critical ball.

The new margin therefore closes a meaningful mathematical consequence of the retained G proof. It does not remove the cost of obtaining a trace-tail bound, an optimizer for the arbitrary-duration value, or a finite representation sufficient for a scientific decision.

## Updated method conclusion

This is a concrete case of compounding retained capital: the exact original Gram reveals a rank-two convex subtraction, output symmetry turns it into an elliptic margin, and a standard analytic estimate supplies the missing receiving coercivity. The consequence is stronger than merely confirming the original G theorem. It changes an explicitly recorded open storage claim while retaining the exact counterexample and unresolved computational boundary.

The observation remains a single successful mechanism chain. It does not identify a causal advantage of longer context, fresh prompting, a model, or additional workers without matched controls. The useful continuation is to keep the exact proof chain and test whether a declared trace/optimization task has paid inputs and an implementable certificate—not to count this result as an achieved physical capability.

## Final source-text pin

The author's final 481-line report is SHA `f4d07b1ef9b4fdeceb58182b49acf5bfd357c1ad5be456fa266f4477604b9cfa`, preserved at `qc_source_snapshot_v0003/REPORT.md`. I separately read its added explicit whole-plane heat/decay argument and constructive periodized-mollifier trace extension. Both preserve the stated proof and constants: quartic Taylor growth and L2/L3/L4 heat decay justify the energy limit, while the differentiated-kernel bound has the critical Slobodeckij denominator |h|⁴. The script and exact certificate remain byte-identical to the replayed versions, so no repeated replay is needed for these expository additions. `QC_REPORT_EXPOSITION_ADDITION.diff` and its receipt retain the complete revision delta.
