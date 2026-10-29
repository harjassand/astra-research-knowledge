# Physical-parity echo: targeted precedent and scope review

Date: 2026-10-29. Supplement to `PARITY_LIFT_LITERATURE_REVIEW.md`. Root construction under review: a known, faithfully executable state involution is applied once at the midpoint, while the same stationary stochastic dynamics runs before and after it. The measured record is a coarse endpoint pair. No physical pulse or experiment has been executed.

## Assessment

Echo protocols, reversal-based entropy formulas, and overlap bounds are established. The strongest sources located do not contain the proposed combination of (i) a fixed physical-parity operation, (ii) a completely positive constraint on the stationary coarse endpoint-pair matrix, and (iii) a hidden-dimension-independent entropy certificate from a copositive witness. The bounded search therefore supports a carefully delimited candidate addition, not a claim that echo-based irreversibility inference itself is new.

The information distinction is substantive: a mathematical adjoint dynamics can always furnish a suitable probabilistic reversal in familiar settings. A faithful, specified parity pulse followed by the unchanged generator is a different resource. It can exclude hidden completions that a passive symmetric record leaves admissible.

## Closest primary sources

### 1. Noh: controlled stochastic echo and dual dynamics

[Jae Dong Noh, *Stochastic Echo Phenomena in Nonequilibrium Systems*, Journal of the Korean Physical Society 64, 504 (2014); inspected arXiv:1212.2706v2](https://arxiv.org/pdf/1212.2706), sections II–IV, especially equations (9), (10), and (25)–(27).

Noh measures echo mismatch by the path relative entropy between an original overdamped Langevin system and a time-reversed, protocol-controlled system. Minimizing this quantity over available controls can give a perfect stochastic echo. For a steady state with density \(p_{ss}=e^{-\phi_{ss}}\), a dual force

\[
f_{dual}=-f-2T\nabla\phi_{ss}
\]

produces the reversed path ensemble exactly. The dual force depends on the stationary distribution and changes the dynamics. This is a strong antecedent for controlled echo and entropy-related path comparison, but not for the proposed coarse copositive certificate under one specified state-space involution and unchanged generator. It also gives a decisive qualification: perfect echo under arbitrary redesigned dynamics does not diagnose equilibrium of the original dynamics.

### 2. Becker et al.: echo initial conditions for fluctuation theorems

[Becker, Willaert, Cleuren, and Van den Broeck, *Echo states for detailed fluctuation theorems*, Physical Review E 91, 012101 (2015), DOI 10.1103/PhysRevE.91.012101; inspected arXiv:1405.6064v2](https://arxiv.org/pdf/1405.6064), sections II–III, equations (3), (5), (14), and (19)–(20).

The paper separates reversed driving, adjoint dynamics, and their combinations. An echo state obeys \(p_0=W_R W_Fp_0\): the reversed process returns the final distribution to the original initial distribution. This makes the detailed fluctuation relation compare the entropy variables of the forward and transformed processes with appropriate boundary conditions. The mathematical requirement concerns initial distributions and propagator composition. It is not a universal positivity constraint on an observed endpoint-pair matrix after a physical parity pulse. It does reinforce that initial/prepared distributions are part of the theorem, rather than an omitted experimental detail.

### 3. Murashita, Kura, and Ueda: velocity reversal with finite precision

[Murashita, Kura, and Ueda, *Entropy production of a closed Hamiltonian system via the detailed fluctuation relation*, Physical Review Research 3, 033224 (2021), DOI 10.1103/PhysRevResearch.3.033224](https://journals.aps.org/prresearch/pdf/10.1103/PhysRevResearch.3.033224), section II and Figure 1.

This is the closest located intervention protocol: evolve for a time, apply velocity reversal together with Gaussian phase-space smearing, and evolve again. Comparing the returned state with the initial state yields an information-theoretic entropy quantity and a Rényi-0 lower bound. The authors explicitly distinguish that quantity from thermodynamic entropy production. Exact unperturbed Hamiltonian reversal would instead give their trivial zero result. The paper therefore anticipates an operational reversal test and finite-resolution accounting, but its observable, physical regime, and entropy target differ from stationary hidden Markov dissipation bounded through the CP cone.

### 4. Hasegawa: Loschmidt overlap and Hellinger bounds

[Yoshihiko Hasegawa, *Irreversibility, Loschmidt Echo, and Thermodynamic Uncertainty Relation*, Physical Review Letters 127, 240602 (2021), DOI 10.1103/PhysRevLett.127.240602; inspected arXiv:2101.06831v5 HTML](https://arxiv.org/html/2101.06831v5), results through equations (8)–(12).

Hasegawa treats the overlap of joint system/environment trajectory states for original and perturbed quantum Markov dynamics. A two-sided Lindblad generator computes that overlap; classical chains are an included limit. Fidelity is bounded by the classical Bhattacharyya affinity of measurement outcomes, and Hellinger inequalities relate the result to observable means and variances. Thus overlap-based irreversibility inequalities and their geometric transition-weight operators are established machinery. The paper does not supply the proposed classical copositive constraint for coarse endpoint pairs under a fixed physical-parity pulse. Its full-system overlap is also not automatically supplied by the proposed endpoint record.

The arXiv PDF and publisher PDF returned access errors through the retrieval tool. The complete main-paper HTML was available and the cited mathematical passages were read there. The HTML's regenerated displayed date is not used as a publication date.

## The candidate addition stated without overclaiming

Let \(Q\) be a finite row generator with stationary law \(\pi\), \(\Pi=\operatorname{diag}(\pi)\), and \(\Theta\) a supplied permutation involution satisfying \(\pi\Theta=\pi\). Let \(E\geq0\) encode even sensor outputs, so \(\Theta E=E\). The acquired protocol is: prepare the stationary state, observe its coarse label, run \(Q\) for \(t/2\), apply the faithful \(\Theta\) operation once, run the same \(Q\) for \(t/2\), and observe the final coarse label. Its pair matrix is

\[
C_{echo}(t)=E^T\Pi e^{tQ/2}\Theta e^{tQ/2}E.
\]

Under generalized equilibrium \(Q^*=\Theta Q\Theta\), the even sensor and parity-invariant measure give

\[
C_{echo}(t)
= (e^{tQ/2}E)^T\Pi(e^{tQ/2}E),
\]

which is a nonnegative Gram matrix, hence completely positive. The root's prospective quantitative result uses a copositive separator and the geometric path-weight operator to turn violation into a lower bound on the specified stationary generalized entropy rate. Its candidate addition is this observed-record implication and finite-sample certificate, with its operation and model class attached. The lift, adjoint construction, ordinary Gram factorization, geometric overlap, and path-relative-entropy framework each have prior foundations.

## Consequential limitations and equally informed comparison

- **The pulse is the additional information-bearing resource.** A control called reversal is insufficient. Its action must actually be the physical involution on all relevant hidden variables. Replacing it by the unknown stationary adjoint generator would change the allowed task and invoke Noh's dual-dynamics loophole.
- **Preparation matters.** Both stochastic halves are stationary because \(\pi\) is stationary and parity-invariant. Without that property, the protocol KL needs the appropriate changing distributions and boundary terms; it cannot be assigned \(t\sigma_\Theta\) by inspection.
- **The entropy target is explicit.** The certificate is for the KL rate under the supplied physical reversal. Whether that rate equals a device's thermal entropy requires its physical stochastic-thermodynamic interpretation. The mathematical identity does not account for the implementation work or entropy of the external pulse apparatus.
- **An equally informed conventional route exists.** The measured echo pair law can immediately be compared with its transpose to obtain a data-processing lower bound from its observed time asymmetry. A complete hidden-model optimization can use the same parity and pulse constraints. The copositive route is valuable only to the extent it certifies beyond the observed asymmetry, or provides a scalable analytic certificate without learning all endpoint probabilities or solving that hidden-model optimization. The proposed bounded-score acquisition should therefore be compared at its actual native interface.
- **No completeness claim follows.** Passing all selected copositive tests is not a proof of physical equilibrium, nor a construction of one consistent full equilibrium process. It merely avoids the corresponding obstruction.

The search covered stochastic echo, echo states, Loschmidt echo, physical velocity/momentum reversal, entropy inference, and targeted reflection-positivity/copositivity combinations. It stopped after reading the strongest directly relevant passages. No claim of an exhaustive priority search is made.
