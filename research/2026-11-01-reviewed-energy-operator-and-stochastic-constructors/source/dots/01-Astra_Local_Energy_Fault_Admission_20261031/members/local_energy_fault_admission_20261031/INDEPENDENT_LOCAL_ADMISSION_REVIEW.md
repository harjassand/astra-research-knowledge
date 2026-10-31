# Independent review: quantum occupation local fault-amplitude admission

31 October 2026. Reviewer: challenge_graph_profile_compiler. **Scoped mathematical PASS** for the declared finite lossy-qubit model and initialized Markov jump-history dilation. This is not a threshold theorem, a gate backend, a fixed-diffusion result, or a practical/novelty finding.

## Source binding and work performed

Full source read and SHA-256 checked:

`QUANTUM_OCCUPATION_LOCAL_ADMISSION_CANDIDATE.md`, 15,414 bytes,
`a5bfe396a5082f9b2d6ddd3e580a18c1399c7fb977ed0b98876798a06f33682d`.

The review independently checked every displayed inequality and the analytic fault extraction, rather than inferring validity from earlier energy or sign-randomization results. No author source was edited. No numerical experiment is used as theorem evidence. AGP Section 11.1, especially Definition (59), and its subsequent inclusive-amplitude receiving argument were directly inspected at https://arxiv.org/html/quant-ph/0504218v3 . The other references and historical internal source hashes in the author's Section 8 were not independently re-audited in this receipt.

## 1. What is actually proved

There is one fixed common jump-record output space for all complex settings z. On the input Hilbert space consisting of the finite source, system, and arbitrary reference/retained records, the inclusive operator obtained by taking a difference in each selected location has norm at most eta^k. All unselected real unwanted couplings, source hopping, loss and injection remain present. Arbitrary warm and entangled inputs on this input space are allowed.

The loss and injection reservoirs must implement the specified Markov Lindblad channels. Their dilation inputs are fixed as prescribed by that model. The result is an operator-norm bound for this initialized jump-history isometry; it is not a bound on an arbitrary unitary extension acting on arbitrary correlated input fields. This distinction was sent to the author and parent as a binding receiving precision. No arbitrary non-Markovian loss-reservoir extension is earned.

The all-location inclusive bound supplies the norm premise used in the ordinary fault-path/linearity argument for such an initialized dilation. It does not assert that a generic unitary extension has the same bound on its entire ancillary domain. Gadget correctness, preparation, measurement, schedule, and any postselection premises of an actual threshold consumer remain separate.

## 2. Product weight and coherent hopping

For V=product_i(1+u_i n_i), its derivative with respect to u_i is n_i V/(1+u_i). Direct two-state calculation gives the stated loss and injection expressions. These identities hold as operator identities, not merely on diagonal states.

On the edge one-excitation sector {|10>,|01>}, the commutator has zero diagonal and off-diagonal magnitude |J_ij| |u_i-u_j| V_rest. The proposed upper bound is |J_ij|(u_i+u_j)V_rest times the identity on that sector, and dominates it since |u_i-u_j|<=u_i+u_j. On the zero-excitation sector both vanish; on |11> the right side is positive and the commutator is zero. Thus the edge operator inequality is valid for complex J, arbitrary exterior quantum state, and arbitrary u>=0. Summing gives the local coefficient d_i u_i+sum_j B_ij u_j.

For a complex multiplier z on a Hermitian selected coupling, the non-TP evolution has adjoint Hamiltonian term i H(z)^dagger V-i V H(z). Every real source-independent system term and every real n_i A_i commutes with V. The imaginary part of z contributes an anticommutator bounded by 2|Im z| sqrt(lambda) b n_i V. The source-independent mismatch contributes at most 2R ||Delta_l|| V. No norm of the real exterior system interactions or total number of exterior locations enters this step.

The one-active-location condition is load-bearing. D_l is an actual fixed support set of size at most g (or a common enclosing support of that size under coherent control), not a branchwise small set whose coherent union has unbounded size. Otherwise v_i=r would fail to dominate the selected terms.

## 3. Backward potential and exterior-volume independence

Writing s=lambda(T-t), the stated backward ODE is exactly the coefficient needed to cancel the n_i V/(1+u_i) terms. At u_i=0 its derivative is nonnegative. At the first u_i=1 with every other component in [0,1], it is at most -1+2 beta+2r. For r<=gamma/4 this is negative. Hence the box [0,1]^|V| is invariant, including piecewise measurable selected forcing.

A=-I+diag(d)+B is Metzler. Symmetry of B makes both its row and column sums at most -gamma. Positivity and the column bound give ||exp(sA)||_1<=exp(-gamma s). Because v_i(1+u_i)<=2v_i, variation of constants/comparison gives u<=2 exp(A .)*v.

At any time ||v||_1<=r g k, while its total rescaled-time integral is at most lambda r g k tau. Consequently sum_i u_i at the initial physical time is at most 2r gk/gamma, and its physical-time integral is at most 2r gk tau/gamma. This accounts for both arbitrary initial excitations and continuing injection. It holds for repeated use of the same source at different selected times, arbitrarily separated selected locations, and arbitrary computation duration outside those locations. No independence or probabilistic hopping picture is used.

With V(T)=I and V(0)<=exp(sum_i u_i(0)) I, the weighted evolution yields

||W(z)||^2 <= exp{[2r g/gamma](1+a tau) k+2R epsilon_ctl k}.

The initial-state factor is essential: dropping it would incorrectly claim the same estimate without paying warm inputs. The injection parameter is the actual physical rate a, not lambda a. A lambda-dependent injection rate must be inserted literally and can destroy usefulness.

## 4. Analytic common dilation and complete norm

For finite source/system dimensions and finite total time with integrable bounded coefficients, each no-jump propagator is entire in the selected parameters. The common output space is the direct sum over jump colors and ordered jump times, with jump operators and no-jump damping terms identical across parameter settings. Compact parameter sets have a finite exponential majorant for the sum of squared history norms. Dyson derivatives have the same type of majorant. This gives locally uniform convergence in the history Hilbert-space norm, and hence an entire operator-valued W(z). Large system gates can instead be treated as finite source-independent unitary punctures, which do not change the weight.

For complex z, the history map remains of the form sum K_history(z) rho K_history(z)^dagger. It is positive/CP but not TP. Its weighted trace obeys the displayed differential inequality. Taking the supremum over positive normalized input states is exactly ||W(z)||^2, because W(z)^dagger W(z) is the corresponding effect. Tensoring a reference changes none of these operator inequalities. This is stronger than a reduced-state trace estimate and avoids assuming a normalized tilted state or applying Jensen to one.

The same history space and the same phases must be retained for every z. Independently choosing arbitrary Stinespring dilations at different settings would not justify their subtraction or analyticity. The canonical construction in the source meets this requirement.

## 5. Fault extraction and constants

The product of (evaluation at 1 minus evaluation at 0) removes exactly all multivariate Dyson terms lacking an insertion at any selected location. It is the inclusive sum, with other locations unrestricted, not a claim of independent or positive fault probabilities. Removing selected K_l does not remove the underlying source channels or hopping. When all couplings are removed the system follows its intended source-independent circuit, while the bath can continue evolving.

For R>1, the operator-valued contour identity with kernel 1/[z(z-1)] has norm factor at most 1/(R-1). Iterating it gives

eta=exp{C/2+R epsilon_ctl}/(R-1), C=[2r g/gamma](1+a tau).

With r=gamma/4, R=gamma sqrt(lambda)/(8b), C=g(1+a tau)/2. For R>=2, 1/(R-1)<=2/R gives the stated 16b/(gamma sqrt(lambda)) prefactor. For nonzero epsilon_ctl, reducing R to min(gamma sqrt(lambda)/(8b),1/(2epsilon_ctl)) keeps the same C as a conservative upper bound and makes the strength O(b/sqrt(lambda)+epsilon_ctl), with the displayed paid constants. The b=0 case must be handled directly as stated; R<=1 is not admitted by the contour formula. R between 1 and 2 gives no automatic useful threshold.

The example beta=1/4, g=2, a tau=1, b=1 has gamma=1/2, C=2, R=sqrt(lambda)/16, and eta=e/(R-1). At lambda=10^12 this is about 4.35e-5. This is a sufficient amplitude number only, not an asserted threshold for a particular architecture.

## 6. Scope and strongest ordinary receiving

AGP Definition (59) is precisely an inclusive sum-of-amplitudes norm condition; it is not an all-subset stochastic-probability bound. Their subsequent fault-path combinatorics and linear gadget-correctness argument are the ordinary intended receiver. The initialized-isometry qualification above does not change the supplied inclusive norm estimate or its application to the actual initialized computation. No threshold value or gadget construction is supplied here.

The microscopic admission is specific: subcritical bounded-incident coherent number-conserving hopping, independently specified Markov loss and bounded incoherent injection, dark-annihilating number-controlled system couplings, finite location incidence, and acquired source-independent control mismatch. Source-creating sqrt(lambda) couplings, fixed-diffusion injection, arbitrary source control, shared unbounded fanout, or arbitrary quantum initial loss fields are not covered. Real system backaction and noncommuting local system operators are covered because they commute with the source weight.

Earlier shared-source counterexamples remain intact: their unbounded fanout or different injection/coupling assumptions violate this admission, and this theorem does not manufacture Pauli probabilities. Known preparation/control costs, actual support assignments, rate calibration, analog realization, and threshold overhead remain paid. The ordinary tools are positive weights, a Metzler comparison, common jump-history dilation and Cauchy extraction. Historical novelty and practical advantage are not established.

## Verdict

No load-bearing algebraic or analytic gap was found in the declared theorem. Accept the source-bound local inclusive-AMPlitude admission with the explicit initialized-Markov-reservoir and fixed-support qualifications above. Do not promote it to a general reservoir theorem, stochastic fault model, full fault-tolerant implementation, or fixed-diffusion result.

## Final source binding after explicit qualifications

The author subsequently added the initialized-field/isometry qualification explicitly in Sections 1–2, specified the fixed finite registers for analytic convergence, and allowed an acquired occupation-diagonal source Hamiltonian. I read these changed paragraphs and verified the final source hash:

`QUANTUM_OCCUPATION_LOCAL_ADMISSION_CANDIDATE.md`, 16,316 bytes,
`0b0bd7ffa77e9c90323be91d5dec929b5bbd66d0c059ad783357838bf5ba010e`.

The added diagonal Hamiltonian commutes with every V_u, so contributes zero to the weighted derivative; finite-dimensional bounded/integrable evolution still supplies the compact analytic majorants. Its size may affect implementation costs but not the stated inequality. No other proof change is relied upon. The PASS above binds this final version as well. The author's separate double-precision diagnostic is not necessary for, and is not promoted by, this review.
