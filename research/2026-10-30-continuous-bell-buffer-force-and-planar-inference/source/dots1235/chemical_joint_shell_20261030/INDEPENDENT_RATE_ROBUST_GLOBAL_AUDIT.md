# Independent audit: bounded state-dependent rate extension

Reviewed 2026-10-30. Source: `RATE_ROBUST_GLOBAL_EXTENSION_CANDIDATE.md`.

**Verdict: passes this separate child-level audit.** The extension does not follow merely by citing the frozen base result; the new uniformity and controlled-value arguments below were checked. The conclusion is for the same hard reaction graph and a fixed strictly positive compact coefficient box. It is not arbitrary-network recurrence, novelty clearance, or a separate whole-proof review of this stronger scope.

## 1. Uniform bulk dissipation

The compact-box version of the killed-complex lemma is valid. In a hypothetical failure sequence alpha_n tending to zero, positive edge contributions divided by alpha_n remain uniformly bounded because coefficient upper bounds are fixed. A positive limiting simplex coordinate at a killed vertex would produce a nonvanishing negative term, forcing that coordinate to zero. A path from the nonempty positive support to killing therefore has a first edge leaving the support. Its coefficient has a fixed positive lower bound and its negative term divided by alpha_n diverges in magnitude. This contradiction is unaffected by variation of the coefficients.

There are finitely many proper supports. One sufficiently small fixed alpha works for all of them and every coefficient vector in the box. Joint continuity on the coefficient box and simplex then gives a uniform fixed-alpha negative margin. Primal factorial comparison errors use only the fixed source/target orders and coefficient upper bounds, so they too are uniform.

The orientation matters: this is a PRIMAL generator assertion. Each term uses the coefficient at the current state, hence state discontinuities or unrelated coefficients at neighboring states create no additional ratio or derivative. The pointwise complex-graph inequality accepts the entire coefficient vector at that state. One must not transfer this argument to an adjoint product measure without further work; the candidate does not do so.

## 2. Controlled low-B value and the delicate return cancellation

At B<4 the actual exit path has at most four jumps, its total rate is at least m_I, and C is unchanged. The terminal-plus-running-cost supremum is therefore finite and factors as C!^alpha f_B(A). Backward induction is legitimate because every enabled jump strictly increases B. For a fixed continuation vector each coefficient enters the displayed quotient linearly in numerator and denominator; its derivative has constant sign with the other coefficient fixed. A maximum is attained at a box corner. This proves the exact endpoint Bellman recursion, including arbitrary adapted controls.

For each admissible row, multiplying its Bellman inequality by its total rate gives L_k F<=-V0. Terminal factorial data are at least the starting V0, so F>=V0. Bounded path length, bounded mean holding time, and bounded factorial shifts give a uniform polynomial upper ratio F/V0.

The leading clearing-return cancellation really survives maximization. Put T_b(a)=((a+2)!(b+3)!)^alpha for b=1,2,3. In the b-th quotient the activation continuation is exactly T_b, since b+3>=4. Its denominator contribution is v ab. Backward induction gives the immigration continuation divided by T_b at most C a^alpha, while the running-cost ratio is O(a^-2alpha). Since u and v have positive lower and finite upper bounds,

    1-C/a <= quotient/T_b <= 1+C a^(alpha-1),

uniformly over the endpoints and all large a. Maximizing preserves these bounds. At b=0 the formula is exactly

    f_0(a)=f_1(a+1)+(a!)^alpha/m_I.

Consequently f_0(a)=((a+3)!4!)^alpha[1+O(a^-delta)] with delta=min(1-alpha,3alpha), uniformly. In particular the B=4 clearing return ratio tends to ONE, not to a coefficient-dependent constant greater than one. Multiplying its O(A^-delta) excess by a bounded clearing coefficient leaves only O(A^(3-delta)) feedback. At B=5,6,7 the return ratio remains O(A^-alpha). No smoothness of the maximizing policy is used.

## 3. Uniform extreme-composition drift

Near A/N=0, the pure-C creation reaction has rate at least cN^3 after removing (B)_4. Every opposing fast contribution carries a boundary A factor; after its factorial jump multiplier, its relative order still tends to zero as A/N tends to zero because alpha<1. The analogous pure-A depletion channel controls the other endpoint. Fixed lower and upper coefficient bounds therefore permit fixed narrower endpoint cones with a uniform negative cN^3(B)_4 F margin.

Immigration, activation, and the just-checked clearing-return excess retain the same lower-than-cubic population exponents as in the base proof, with changed constants only. Low B has the uniform Bellman negative margin, and balanced high B has the uniform primal bulk margin. Thus the full F coverage and quantitative margins needed by the entropy comparison remain valid.

## 4. Uniform controlled traces

The r-trace already allowed arbitrary adapted coefficients. On A>=epsilon N, actual activation and clearing coefficients divided by the projected falling factorials remain in a strictly positive compact interval depending only on epsilon and the original box. Fast reactions leave the r-value's arguments N,B unchanged exactly. Off-cone positive drift bounds use only source rate upper bounds and fixed-shift value bounds.

For the complementary trace's fixed 45-state head, all endpoint policies have the same enabled graph and positive leading rate degrees. Positive Schur exponents therefore do not change with the endpoints. Finite-policy affine improvement must include the exit reward as part of the altered row; with that understood, it produces common up/tail supersolutions. Expected-time bounds may alternatively be obtained directly from three prescribed immigrations, with uniform probability and holding-time constants. These statements hold for adapted controls, not only for a stationary maximizing policy.

The shell absorption proof is also uniformly robust. For a<=epsilon N, the controlled birth-minus-death drift is >=cN^3 if epsilon is sufficiently small: the pure-C birth channel stays bounded below, and all deaths have an a factor. Total fast rate is <=CN^3, and killing is >=m_D(a)_3. For W_N(a)=(a+N^(3/4))^-3, the same three-region Taylor argument proves Q_k W_N<=-c_0 uniformly. In the bulk a>=epsilon N, even the absolute fast contribution is O(1/N), while killing supplies a fixed negative amount. Stopped Dynkin gives controlled mean clearing time <=CN^-9/4/(B)_4.

Competing birth controls may depend on the entire observed history. This does not invalidate the hazard bound: stop the shell test function additionally at the first birth and assign cemetery value zero. This adds a nonpositive killing term, so the same expected stopped-time bound holds. Integrating the bounded birth intensity then gives the same risk estimate. Summing over successive clearing stages and restarting after neutral births is uniform over adapted controls, as every conditional starting composition and policy satisfy the same estimates. Thus the complementary trace is genuinely controlled at every composition.

## 5. Common values, global closure, and conclusions

Define both residual values as suprema of stopped costs over adapted controls, with the previously proved uniform trace contraction and time bounds. These establish finite costs and stopped nonexplosion before the values are used as barriers. Holding any allowed row until the first jump, then choosing epsilon-optimal continuations at its finitely many targets, proves the common generator inequalities. No optimal policy, policy regularity, exact lumpability, or physical cone invariance is needed.

All global comparisons use only uniform constants: the binary-entropy gap can be chosen after fixing the narrowed uniform endpoint cones; threshold leakage stays bounded for the r-value and at most C AB for the s-value; actual clearing-return and bulk margins were checked above. The same three-function sum therefore gives a finite normlike common Foster function and the factorial-size negative margins outside a finite set, uniformly over the coefficient box.

Finite-rate localization proves nonexplosion. For time-homogeneous generators the Foster inequalities imply positive recurrence on each closed class and all exponential population moments by the same stopped regeneration argument as in the base proof. Strictly positive state-dependent coefficients preserve every enabled reaction edge and its enabled weak-reversibility return path, so the closure of communicating classes is unchanged. For adapted time-dependent controls, the common generator inequality and nonexplosion remain meaningful, but stationary recurrence and stationary moments are not asserted, correctly.

No additional gap was identified in this extension. A separate whole-proof review of the strengthened coefficient scope remains appropriate before promoting beyond this audit.

## Reviewed source hash
977654a672ace19d04dcca9077aaa7dadb6930a3303d9cc1603aeb304985d38c  chemical_joint_shell_20261030/RATE_ROBUST_GLOBAL_EXTENSION_CANDIDATE.md
