# Internal audit: finite stiffness and the extra-mode onset

27 October 2026. Decision: **PASS at the declared mathematical scope**, with one minor convergence-wording clarification noted below. No substantive gap was found in FINITE_STIFFNESS.md or the appended numerical checks. The sharp optimizer under simultaneous compliance and spring-sum caps remains open, as the parent states.

The reviewed snapshot is preserved in `finite_budget/FINITE_STIFFNESS.md`, SHA256 fb1bac75dcbeb85c6e893319c235b6d556b1871ca27df44606019974015e868a. The updated certificate was copied unchanged into `finite_budget/certify.py`, SHA256 b40b5ec048c673d7fb60bdb1c4b50695d9104c1e28e01f0ce71290bc2ff20dca, and executed only in that owned directory. Every assertion passed. Its output is `finite_budget/CERTIFICATE.md`, SHA256 95ee53a4748778f74604f8b4b82e6525d4f0133b559e01ed63834173dc896f09.

## 1. General-graph static threshold

The physical force vector agrees exactly with frozen C/A's normalized relative-CM readout: mass normalization sends f_b=-1,f_j=m_j/ms to w_b=-1/sqrt(m), w_j=sqrt(m_j)/ms. Since its total force is zero, the static translation ambiguity does not affect C=f^T L^+f.

For x solving Lx=f, energy gives C=sum_e k_e(x_u-x_v)^2. The backbone force equation has magnitude one. Weighted Cauchy-Schwarz at that coordinate therefore yields 1<=kappa_inc C<=kappa_total C. This holds for every finite connected positive graph, not just stars. Hence kappa_total>=1/Cmax is necessary under C<=Cmax, and the pendant with spring 1/Cmax shows it is sufficient.

At equality every intervening inequality is equality. Because C>0, kappa_inc=kappa_total; no positive nonincident edge remains. The graph is a star after combining parallel springs. Cauchy-Schwarz equality makes all backbone-to-side static displacements equal. The side force equations then give k_j/m_j constant, so all branch natural frequencies k_j/m_j agree. Eliminating the side coordinates combines their response into one side mass ms and spring sum kappa_total. The remaining side modes are dark. Thus the exact feasibility boundary cannot hide a useful additional active mode.

## 2. Exact branch-splitting derivative

The proposed three-band family preserves trace, log product and inverse endpoint sum exactly by the same algebra already audited in PROOF.md. At delta=0 it reduces to the k=20 pendant, with t0=40, p0²+s0²=44 and p0²s0²=80. H=64 lies strictly above s0², so small positive delta gives strictly interlacing bands and positive finite inverse synthesis. The moment denominators are nonzero near zero and all endpoints depend smoothly on delta.

For the full spectrum, all three resource derivatives vanish. Subtracting the endpoint-zero dual therefore gives exactly

J'(0)=R0(sqrt(H))/(2sqrt(H)).

The low endpoint terms vanish because R0 is zero there; the newly opened high interval has width derivative 1/(2sqrt(H)). This uses the full Bose integral and does not omit a compensating band.

I independently differentiated the inverse-moment equation. At delta=0,

A_l'= -1, B_l'=-2/H,
t'(0)=880/H-20-1600/H².

For fixed trace four the star stiffness is (E-16)/8, where

E=2t(A_l-B_l)+A_l²+2H delta+delta².

It follows that

kappa'(0)=H/4-21+460/H-800/H²
          =(H-40)(H²-44H+80)/(4H²)
          =(H-r0²)(H-p0²)(H-s0²)/(4H²).

At H=64 this equals exactly 255/128. The interval check encloses the same value positively. The certified R0(8)<0 therefore implies J'(0)<0 while kappa(delta) tends to 20 from above. For every positive budget overhead, sufficiently small positive delta simultaneously gives a legal finite positive star, stiffness below the stated budget, exact compliance cap and strict full-spectrum gain. This justifies the claimed sharp onset of strict extra-mode advantage, without asserting a finite gain uniform as the overhead tends to zero.

## 3. Explicit matched-budget construction

The rational data at delta=1/100,H=64 agree with the general formulas. The updated exact interval certificate proves strict interlacing and positivity of both branch masses and springs. The response's reciprocal decomposition is the same positive-residue construction audited previously. It has backbone mass one and exact total mass two, since tH/d=2 algebraically; the exact logarithmic and inverse endpoint identities give C_CM=1/20.

The exact stiffness fraction is below 20.02. Both this star and the optimized one-pendant are therefore admitted by the same C<=1/20 and kappa<=20.02 budgets. The one-pendant still minimizes at k=20 because frozen F places its unique unconstrained stationary point strictly below that value and its objective increases afterwards.

The full Bose interval rerun gives

J_pendant-J_star in [0.000000182670737317172171,
                     0.000000182670737317172172],

and kappa in [20.019991588639055804289563,
             20.019991588639055804289564].

Thus the gain is strictly positive at genuinely matched declared budgets. Its tiny size and the very small second side mass are explicitly retained. Robustness, connector mass and material costs remain outside the comparison.

## 4. Fixed finite stiffness excludes escape-infimum approximation

For the sharp severe-cap lower-bound dual, a=0 and nu<0. If J_n tends to j*, the nonnegative dual terms force

I_n=integral |Rhat| |chi_n-chihat| tending to zero.

On every compact interval separated from zero and the three roots, |Rhat| has a positive minimum, so indicators converge in L1 there. **Minor wording clarification:** this is the precise convergence provided by the argument; pointwise convergence of the entire sequence is not needed and is not implied merely by I_n tending to zero. L1 is sufficient for all following moment conclusions. Neighborhoods of the roots have arbitrarily small trace measure because indicators are bounded by one.

A common total spring bound implies a common incident spring bound. Frozen F gives

E_n=A0²[1+2 kappa_inc,n/S],

so E_n is uniformly bounded. The trace tails satisfy the displayed bounds

integral_0^epsilon 2w chi_n dw<=epsilon²,
integral_R^infinity 2w chi_n dw<=E_n/(2R²).

Together with compact L1 convergence this makes the entire trace converge to Ahat<4, contradicting the exact trace four of every original physical cell. Hence no sequence with a fixed finite spring cap approaches the escape infimum. If its feasible set is nonempty, its objective infimum is separated strictly above that value. This also excludes schemes distributing the escaped trace over arbitrarily many small high-frequency bands.

The argument establishes a positive gap, not a quantitative rate in the stiffness budget, finite-order attainment, a sharp joint-budget optimizer or physical performance. Those distinctions in the parent's final scope are correct.

This remains an exposed internal mathematical audit, with the same frozen spectral foundations and limitations as AUDIT.md. Historical priority, external acceptance, fabrication and practical-device advantage were not established.
