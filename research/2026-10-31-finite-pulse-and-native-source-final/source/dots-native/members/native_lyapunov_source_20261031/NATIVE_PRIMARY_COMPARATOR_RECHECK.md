# Native-source comparator recheck

31 October 2026. Primary texts inspected afresh for the native dark-Lindblad receiving candidate. This is a bounded comparison, not a priority or practical-advantage finding. The native compiler remains subject to its separate whole receipt.

## Primary statements actually checked

1. Shang–França, *Hamiltonian dynamics from pure dissipation*, arXiv2604.18533v2 (4 October2026), Section4, equations19–20: changing jump gauge can substantially reduce norm-based simulation cost without changing the generator. The text also cautions that replacing a finite dissipative evolution by its effective Hamiltonian leaves a fixed error. This is a constructive competitor; a poor original jump normalization is not evidence of computational advantage. [Primary](https://arxiv.org/html/2604.18533v2)

2. Borras–Marvian, *Quantum simulation algorithms based on quantum trajectories*, arXiv2509.10425v2 (8 April2026), equations19–20, Section3 and Section4: the compiled trajectory algorithm assumes scalar total jump square, sum L_mu†L_mu=Gamma I. Its holding times are then state-independent exponentials. It constructs the jump operation by amplification, not by knowing the input state. Lemma7 explicitly excludes amplitude damping from the scalar-rate representation class. This is substantially relevant ordinary trajectory machinery, but its stated premise is not the present dark stack. [Primary](https://arxiv.org/html/2509.10425v2)

3. Chen–Gao–Wang–Zhou, *Query-Optimal and Gate-Efficient Lindbladian Simulation*, arXiv2609.18757v1 (16 September2026), Section1.1: the acquired input is a Hamiltonian block and rectangular stacked-jump encoding. The diamond-error query bound is optimal in normalized action tau=(alpha_H+alpha_B²)T, with nearly linear additional gates up to polylogarithms. This is a strong general-purpose fallback with the same kind of stack access, not a dimension-enumerating straw comparator. Its displayed action bound does not replace alpha_B² by a driven-state Lyapunov activity estimate. [Primary](https://arxiv.org/html/2609.18757v1)

4. Kitchen, *Causal Query Compression for Lindblad Dynamics*, arXiv2609.31312v1 (25 September2026), Sections1.1,5 and6: the general query theorem prices supplied Hamiltonian and individual-jump oracle action. The local gate theorem fixes local normalization parameters. Adaptive Markovian controls and classical records are explicitly included; compression works with occupied simulation-bath inputs. These are genuine competing capabilities. The stated action/local-normalization assumptions do not by themselves give logarithmic dependence on an unbounded rapid-loss multiplier. [Primary](https://arxiv.org/html/2609.31312v1)

## Direct substitutions, rather than title-based absence

The actual native input is lambda sum D[L_a] plus the centered drive -i[H0+sqrt(lambda)K,.], with known pure dark P, acquired source energy H=sum L†L/2, spectral bound gQ<=H<=hQ, and energy drift G†H<=-kappa H. The common classical/quantum interface is a full joint channel, with prescribed instruments. Any ordinary full-diamond-channel simulator composes with these instruments by telescoping; retaining controls is not an exclusive advantage of this construction.

With the supplied representation, the generic stacked-query action is at most

    T(alpha_0+sqrt(lambda)b+lambda alpha_L²).

The individual-jump oracle action has the analogous sum of normalization squares. Rescaling physical time transfers lambda into this action; it does not remove it. A local theorem with fixed term norms cannot silently take lambda to infinity while keeping its hidden local constants fixed. Conversely, if a better acquired gauge or special channel formula lowers the real action, that improvement must be offered to the ordinary comparator too.

For the present nontrivial dark stack, scalar total rate cannot hold in the SAME representation: sum L†L annihilates psi, whereas Gamma I does not unless Gamma=0. This alone does not rule out other representations. There is, however, an elementary exact test case.

Take a source qubit, L=sqrt(2)|0><1|, H=|1><1|. Then G†H=-2H and g=h=1. At physical rate lambda, every usual gauge with unitary/isometric jump mixing and identity shifts has the form

    L'_a=u_a sqrt(2lambda)|0><1|+c_a I,
    sum_a |u_a|²=1,

allowing extra zero/identity channels. On input |1>, the two output source directions are orthogonal, so

    sum_a ||L'_a|1>||²=2lambda+sum_a |c_a|² >=2lambda.

Thus the acquired stack normalization, if it correctly bounds this stack, is at least sqrt(2lambda); sum of individual operator-norm squares is at least2lambda. A compensating Hamiltonian gauge term does not negate this positive stack-square lower bound. Hence identity-shift gauge optimization alone cannot make this example's standard norm action logarithmic in lambda.

Crucially, this is NOT a lower bound on simulating amplitude damping: its exact channel is a small circuit with an exponentially decaying rotation parameter, and its source-only dynamics is trivially fast-forwardable. It isolates the limitation of one proposed general reduction, not a practical winner or a complexity separation. A continuously coupled large system may also admit a cheap exact reduced-memory solution; its actual construction and memory costs must be compared on the chosen task.

## What the present conjunction would add, and what remains unestablished

The native candidate uses additional acquired certificates not supplied to those general theorems: a dark projector, positive gapped no-jump energy, and a Lyapunov inequality. Ordinary LCHS supplies the scaled fast no-jump block. A positive two-sector word construction then gives an integrable complete-first-event proposal, with actual source/color output retained, and a tilted count estimate bounds the number of physical events. Complete-isometry amplification, private-time coupling and capped continuation are the assembly needed to turn these facts into a finite channel circuit. Small expected jump count alone is not that assembly.

None of the inspected theorem statements directly performs that substitution for this certificate interface. This limited conclusion does NOT show that the assembly is new, that no existing trajectory or interaction-picture proof can be adapted to it, or that it beats optimized ordinary methods in any practical instance. Its ingredients are standard and the resulting polynomial overhead is conservative. The strong general algorithms are suitable low-rate fallbacks, and special reduced equations, exact channels, elimination with certified boundary maps, and dense solvers remain preferable where their full acquisition and execution costs are smaller.

The next consequential assessment should therefore be an end-to-end retained-observable task with explicit encodings, certificate acquisition, errors and actual resource constants—not another model extension or an inference of novelty from a short literature screen. All earlier denied-source restrictions remain unchanged; this recheck accessed only the four linked primary arXiv texts.
