# Exact approximate-lowering-operator thermal bound

Root, 2026-11-02. A conventional spectral alternative to the unfinished quantum contour construction. No novelty or full memory-stability claim.

Let rho=exp(-beta H)/Z in finite dimension, beta>=0. Let F be any operator and Delta>0. Define R=[H,F]+Delta F. For any 0<a<1,

 Tr(rho F†F) <= exp(-beta a Delta) Tr(rho FF†)
                  + Tr(rho R†R)/[(1-a)^2 Delta²].

Proof: in an eigenbasis H|b>=E_b|b>, split matrix elements F_ab according to E_b-E_a>=a Delta. In the first class, Gibbs probabilities obey p_b<=exp(-beta a Delta)p_a. In the complementary class, |Delta+E_a-E_b|>(1-a)Delta and R_ab=(Delta+E_a-E_b)F_ab. Summing p_b|F_ab|² separately over both classes proves the inequality, with no assumption on signs or commutation of F†F with H.

For a partial isometry F with F†F=P_W and FF†<=I, choose a=1/2:

 Tr(rho P_W) <= exp(-beta Delta/2)+4 Tr(rho R†R)/Delta².

If H=H0+V and F is an exact lowering operator of H0, [H0,F]=-Delta F, then R=[V,F]. This is a beta-uniform bound with the correct possible virtual-excitation floor. The thermal term and the perturbation term cannot generally be collapsed into an effective Boltzmann factor.

For a valid removable syndrome tau of a uniform commuting-check Hamiltonian H0=-J sum S_a, let P_W require all tau checks occupied and let E_tau flip exactly those checks. Then F=E_tau P_W has Delta=2J|tau| and FF†<=I. This statement is for that commuting reference only. It cannot silently replace the actual noncommuting native clock Hamiltonian by its static free energy: the latter is not an operator energy ladder.

The obvious norm bound ||[V,F]||<=2 sum_{x: support(V_x) meets support(F)}||V_x|| may grow with the entire correction/filling region. Even if it grows only linearly in witness mass, dividing by Delta² gives a constant virtual floor, not exponentially small probability in mass. In the actual hierarchical decoder the filling can be polynomially larger, so a uniform fixed perturbation strength may not even make this estimate small. This direct same-question alternative therefore does not by itself supply the rare-witness estimate needed for scalable memory. A further multiplicative local factorization or normalized quantum-excursion theorem is essential.

Retain this lemma as a precise benchmark and failure diagnosis, not a substitute result promoted to the north-star capability.
