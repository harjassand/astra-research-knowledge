# Critical check of the qubit MI pinching argument

24 October 2026. Independent check of mi_qubit_root_independent_check.md. The argument is sound with arbitrary finite quantum reference. No novelty claim is made.

1. Diagonalize the physical marginal, not the joint state. Then dephasing Delta preserves both marginals. The exact MI decomposition follows from D(rho||Delta rho)=S(Delta rho)−S(rho), and the same decomposition remains valid after depolarization. This requires no commutativity between reference blocks.

2. The diagonal MI pair is Delta rho versus rho_A⊗rho_R. It has the same reference marginal, so the established binary CQ complete coefficient lambda² applies. The comparison state is carried to the product of the output physical marginal and the unchanged reference marginal.

3. For k=(1+lambda)/2 and theta=lambda/k, inspect a joint 2-by-2 operator block matrix. The mixture k Gamma_theta(rho)+(1−k)X Delta(rho)X has off-diagonal block lambda rho_01 and diagonal block k rho_00+(1−k)rho_11. These are exactly depolarization's blocks. Dephasing this identity supplies the second mixture needed for joint convexity. The unitary X acts on A alone.

4. The use of the two-sector pinching theorem is legitimate. The pair Gamma_theta(rho), Delta rho has identical Delta images; its conditional denominator is exactly D(rho||Delta rho), and its numerator is D(Gamma_theta(rho)||Delta rho). There is no false identification of a general conditional BKM quotient with a zero-marginal tangent quotient.

5. Joint convexity and the pinching bound give coherence contraction k theta²=lambda²/k. Combining the two nonnegative MI summands yields eta_MI≤lambda²/k. Rank-deficient states do not invalidate this: regularize rho by a positive identity product, apply the faithful result, and use finite-dimensional entropy continuity. Alternatively, relative entropy to its pinching always has the requisite support inclusion.

6. For the lower construction, perturb a faithful diagonal product baseline by t(|00><11|+|11><00|). Both partial traces of the perturbation vanish, so its MI is exactly relative entropy to the unperturbed product. For fixed positive baseline parameters first let t tend to zero; then let the rare reference probability tend to zero and finally the physical population tend to one. The local ratio approaches lambda² p/[lambda p+(1−lambda)/2], and then lambda²/k. This is a sequence of finite faithful states, not an attained boundary state. A diagonal sequence of sufficiently small t values realizes the iterated limits as ordinary states.

Therefore the pinching application and arbitrary-reference extension pass the load-bearing check. The exact coefficient is 2lambda²/(1+lambda), with endpoints checked directly. The theorem does not imply a uniformly conditioned or nonvanishing-information maximizer.
