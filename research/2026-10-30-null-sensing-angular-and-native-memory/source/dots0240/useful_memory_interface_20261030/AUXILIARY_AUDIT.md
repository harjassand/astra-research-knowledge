# Independent audit of three auxiliary ordinary consequences
2026-10-30. Sources were read in full. These are scope/proof checks, not novelty assessments.

## Verdict

**PASS in the stated fixed-port, delayed-global-basis, and fixed-decoder scopes, with the clarifications below.** No mathematical counterexample was found within those models. No extra apparatus or reliable-control theorem is supplied.

## 1. BARE_PORT_NO_GO.md

The first/last-event proof is valid. The decisive facts are that the port depolarizations have an independent exogenous state-independent Poisson record, and both intervening dynamics being compared are CPTP. For a normalized joint state at the last kick s, Duhamel gives

    ||Phi_(T,s)-Psi_(T,s)||_diamond
       <= integral_s^T ||K_Q(u)||_diamond du <= g(T-s),

where Phi is the non-depolarizing base evolution and Psi is the evolution with K_Q removed. A bounded full-system generator norm is unnecessary: CPTP contraction bounds both propagators, while only the local difference K_Q is norm-bounded. This is why arbitrary apparatus size and preexisting correlations do not produce an N factor.

An explicit hypothesis should be retained: **L_notQ+K_Q generates well-defined CPTP evolution between the independently specified port kicks.** The fact that the sum INCLUDING a depolarization generator is GKLS would not by itself imply this after subtraction. In the manuscript's intended exogenous-kick model this condition is implicit and natural, but stating it eliminates a logical ambiguity.

Conditioning on the first/last independent port event is harmless. One should not additionally condition on rare internal measurement records and then apply CPTP contraction to a normalized postselected evolution. Arbitrary adaptive controls may be retained by including their classical records and controller hardware in the joint state; the averaged base dynamics must satisfy the stated CPTP/g bound. The maximally entangled reference is untouched throughout.

Immediately after a port depolarization, the port is maximally mixed and independent of all other registers. In retrieval the comparison evolution keeps it so. In loading the comparison depolarization leaves the untouched reference maximally mixed and independent of the entire accessible apparatus. Any subsequent CPTP operation on that apparatus preserves this product structure. Bell overlap is therefore exactly 1/d^2 in the comparison, and at most 1/d^2+g delta in the actual bad-event branch. Averaging its exogenous probability q proves the stated fidelity floor. The diamond lower bound follows by the binary test consisting of the target Bell projector and its complement.

The theorem intentionally concerns a fixed physical port and an operation lasting at least a fixed delta. It does not automatically cover an adaptively selected output location among a growing number of ports, postselection conditioned on heralded success, a shrinking-duration operation, or a source/reference with additional correlated accessible side systems. Those are different resources/models, not counterexamples to the fixed-port statement.

## 2. DELAYED_BASIS_GAME.md

The exact optimum is correct:

    P_measure-first = (1+d^(-1/2))/2.

Every arbitrary collective measure-first strategy with unlimited classical storage can be coarse-grained by its two eventual answers. Randomized postprocessing can be absorbed in the outcome label or derandomized without increasing the optimum. For each answer pair, the sum of the two mutually unbiased rank-one projectors has eigenvalues 1+1/sqrt(d), 1-1/sqrt(d), and zeros. Completeness of the POVM then gives the upper bound without a locality, computational-complexity, or entanglement-breaking-output restriction.

For the real Hadamard bases, the proposed top-eigenvector effects form a valid POVM. The two diagonal contributions sum to 2d I, and the two phase-aligned cross contributions sum to 2sqrt(d) I. Division by 2(1+1/sqrt(d)) gives d I, and the extra 1/d factor normalizes the effects. Every effect saturates its eigenvalue bound, so the upper bound is attained.

The basis bit is one GLOBAL choice between the all-Z and all-X k-qubit bases. Independent delayed basis choices for each of the k qubits define a different game. The source supplies one encoded state; the result does not solve its noisy physical preparation. Both quantum and classical competitors receive that same input, and a scheduled protected quantum memory enjoys the same winning strategy.

## 3. SUBTHRESHOLD_ACCESS_BOUNDARY.md

The KSW application and constants are correct when the physical environment is disjoint from the retained memory registers used by the decoder. Dilate the decoder, retain the actual environment, and enlarge the dilation space if necessary. A physical dilation of the recovered channel can then be compared with an identity dilation I tensor |eta> at isometry distance at most sqrt(delta). The complementary-channel distance is at most twice that distance. Tracing the decoder's discarded registers and any auxiliary enlargement yields the claimed actual-environment channel bound 2sqrt(delta), with no logical-dimension prefactor.

The equal-prior discrimination estimate follows from the triangle inequality and Helstrom's formula: the two environment output states differ in trace norm by at most 4sqrt(delta), hence success is at most 1/2+sqrt(delta), trivially capped by one. The diamond claim also includes entangled spectator references; it does not erase information already held in a recipient's independently supplied side information.

The gate obstruction is a direct triangle inequality for the **fixed original mathematical decoder**. It forbids a physical nonidentity logical channel under that decoder while the logical-identity guarantee still applies. It does not rule out changing software Pauli-frame conventions or reinterpreting later classical outcomes. Such relabelling is not a counterexample to the fixed-decoder assertion, and its classical reliability or eventual physical access remains separately accounted for.

The noise scopes are correctly kept separate: native local Poisson-CPTP perturbations do not become general weak continuous Hamiltonians merely because one calls them control. An actively controlled terminal Bell interface escapes by changing the nominal operating mode, not by simultaneously satisfying and defeating the original logical-identity guarantee.
