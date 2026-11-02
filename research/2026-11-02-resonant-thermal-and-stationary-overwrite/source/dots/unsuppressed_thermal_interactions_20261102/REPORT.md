# Unsuppressed thermal interactions: independent constructor pass

Date: 2026-11-02. Status: useful exact diagnostics and an implementation obstruction; **not** a completed replacement compiler.

## Starting construction, derived from target before consulting parent proofs

The perturbative expression `J0=2 t^K / Delta^(K-1)` suggests deleting detuning rather than optimizing it. A resonant finite-dimensional mediator can detect stabilizer parity as a holonomy/flux of a hopping graph. This uses genuine two-body mediator–data interactions, fixed local dimension, fixed strength, and does not discard any mediator level. The important question is its **free-energy** contrast, not its ground-state gap.

A second representation move attempts to make this mechanism compatible with CSS checks: duplicate each data qubit into Z-check incidence clusters, regard each cluster as one qudit, impose ZZ copy constraints, and implement X checks by hopping operations which flip an even number of qubits within every Z-check cluster. This makes Z checks onsite and every hop mediator–cluster two-body. All problematic noncommutation is then concentrated in copy constraints. The resulting shielding test below is decisive.

## 1. Exact all-level thermal calculation for one resonant check

Let `S=P_0 ... P_(K-1)` be a Pauli check, with mutually commuting P_j, each supported on one hardware qudit. Set

`H=-t Σ_j (|j+1><j| ⊗ P_j + h.c.)`, indices modulo K, K>=3.

A block-diagonal controlled-prefix unitary gauges away all links but one. In syndrome `S=s`, the mediator is a K-cycle with flux 0 (s=+1) or pi (s=-1). Its **entire** spectrum is

`E_m(s)=-2t cos((2 pi m + phi_s)/K)`.

Consequently, tracing the entire mediator gives the exact syndrome free-energy penalty

`DeltaF_beta = beta^-1 log(Z_+/Z_-)`,

`Z_± = Σ_(m=0)^(K-1) exp[2 beta t cos((2 pi m + phi_±)/K)]`.

The corresponding coefficient in a convention `H_eff=-J_beta S` is `J_beta=DeltaF_beta/2`. There is no large-gap expansion and no projection onto a mediator band.

At zero temperature,

`DeltaF_infinity=2t[1-cos(pi/K)] ~ pi² t/K²`.

The negative-flux ground state is doubly degenerate, so at low temperature `DeltaF_beta=DeltaF_infinity-(log 2)/beta+...`.

At small x=beta*t,

`DeltaF_beta ~ (4/beta) x^K/K!`.

This follows from the exact Bessel identity

`Z_±=K[I_0(2x)+2Σ_(ell>=1)(±1)^ell I_(ell K)(2x)]`.

Thus resonance removes the detuning suppression but **does not remove thermal winding suppression**. In a large-ring diffusion regime the flux contrast is exponentially small until beta*t reaches order K². The attached script uses arbitrary precision and the Bessel representation to avoid subtracting nearly equal partition functions.

Selected exact values (DeltaF_beta/t):

| K | beta*t=1 | beta*t=10 | beta*t=100 | beta*t=1000 | T=0 |
|---|---:|---:|---:|---:|---:|
| 4 | 0.0890704 | 0.516472 | 0.578855 | 0.585093 | 0.585786 |
| 8 | 4.86042e-5 | 0.0834941 | 0.145309 | 0.151548 | 0.152241 |
| 16 | 8.89385e-14 | 0.000781010 | 0.0314980 | 0.0377363 | 0.0384294 |
| 180 | 8.78278e-330 | 7.93591e-158 | 2.01213e-35 | 1.21834e-6 | 0.000304610 |

**Positive actionable target:** short, resonant holonomy loops (K around 4), not merely zero detuning. Grouping data into genuinely native qudits can shorten K; its physical local dimension and control matrix complexity must be charged. A formal fixed dimension such as 2^90 is not a practical resolution.

## 2. Exact shielding-arity implementation test

For the proposed duplication representation, let `C_e=Z_(q,a) Z_(q,b)` enforce equality of two copies of original q. Let m_i denote the prefix position of X-check clock i. Define

`f_(e,i)(m_i)=(-1)^[number of endpoint flips caused by prefix i mod 2]`.

In the controlled-prefix gauge,

`U† C_e U = C_e Π_i f_(e,i)(m_i)`.

Only X checks involving q can contribute. In the copy-valid sector C_e=+1, exact shielding therefore needs the diagonal function

`J Π_i f_(e,i)(m_i)`.

If r>=3 factors are nonconstant and independently variable, this is **not a sum of pairwise functions of the individual clocks**. Choose two positions of each clock at which its sign differs; the r-fold discrete mixed derivative is nonzero, whereas that derivative annihilates every pairwise function. This is a finite, exact rejection test, not a perturbative concern.

Contributions from several edges could cancel high-order components; therefore the correct test for a concrete code is the high-order discrete Fourier/ANOVA support of the **sum** of shielding functions, not just the maximum single-edge degree. Clock regrouping can also reduce arity but must be charged in dimension, range, and degree. No such cancellation or bounded regrouping is established here.

### Why the easy degree-two escape misses the memory objective

For a CSS code with each data qubit incident on at most two X stabilizer generators, the binary X incidence matrix is a graph incidence matrix, allowing half-edges and zero columns. Its kernel consists of cycles and paths between unconstrained boundary endpoints. Any Z logical in this kernel decomposes into those elementary cycles/paths. If all components were Z stabilizers, their sum would be a stabilizer, so some component is a nontrivial logical. Build that component edge by edge: at every stage there are at most two X-check violations. Z checks commute with the entire process. With bounded generator strengths this gives an O(1) Z logical energy barrier.

This rules out using the simple degree-two condition as a route to a diverging **energy** barrier for both quantum sectors. It is not a universal theorem that a constant barrier forbids every possible entropic memory mechanism.

## 3. What happens to real copy excitations

Shielding only cancels in C_e=+1 sectors. If C_e=-1, the residual becomes `2J Π_i f_(e,i)(m_i)`, which has either sign. It is incorrect to assign an automatic +2J charge to that real auxiliary defect. A thermal proof must bound the complete interacting clock partition function in each defect sector, or establish a local positive defect certificate that survives their interactions.

A ground-state gap proves neither an extensive defect charge nor a small thermal fugacity. Even if a local cluster gap is gamma, its full partition ratio and multiplicity matter. A valid next implementation test must compare `Z_defect/Z_clean` for the full local cluster and include overlaps between neighboring defect clusters.

## 4. Primary-source comparison, scope strictly limited

- Ocko–Yoshida, https://arxiv.org/html/1107.2697 : their construction clusters plaquette spins and shields the resulting copy constraints through pairwise clock functions. The reported optimized gap is >0.075 U at t=0.375 U, J=0.09 U. Their exact decoupling is in selected invariant sectors; other sectors acquire interacting clock terms. This supplies a concrete short-loop benchmark, not a full finite-temperature theorem for the present 3D CSS family.
- König, https://arxiv.org/abs/0901.1333 : explicitly a perturbative hopping construction; it does not by itself remove the hierarchy.
- Hutter–Pedrocchi–Wootton–Loss, https://arxiv.org/abs/1209.5289 : local spin implementation relies on low-energy magnons and perturbative five-spin gadgets. Their stated noise regime requires validity of that effective description; it is not an all-auxiliary equilibrium certificate.
- Headley–Chancellor (2025), https://arxiv.org/html/2506.05323v1 : the explicit simplest defect gadget uses three-body coupling and higher-body driving. Its suggested two-body ice-like direction is not an explicit same-resource replacement available from that paper.

## 5. Recommended constructive continuation

1. Obtain the actual CSS incidence matrices and grouping geometry. Compute the total shielding ANOVA support, including cancellations, and the number of hardware clusters touched per X check. This is a cheap yes/no implementation test before undertaking stability proofs.
2. If all surviving shielding supports have arity <=2 and resonant loop lengths <=8, solve finite clock/copy-defect clusters nonperturbatively and certify **partition-function ratios**, not only gaps. Seek a polymer/fugacity bound with positive net charge after entropy, plus a bounded-spread local bath dictionary.
3. If shielding arity >=3 survives, do not claim Ocko's construction extends. A new mechanism must address exactly that local multi-clock phase without returning to a Kth-order process. Exploring a finite native high-dimensional cluster or a bounded-order hybrid could be worthwhile, but the latter is not the requested fully nonperturbative solution.
4. If K remains near 180, reject the bare resonant-ring hardware as a practical finite-temperature route even if its zero-temperature gap looks polynomially improved.

No universal unsuppressed two-body implementation, full thermal protective phase, generic-perturbation tolerance, or ideal Gibbs access is established by this pass.
