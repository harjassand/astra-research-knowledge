# Matched comparators and charged physical resources

Date: 16 October 2026. All source versions and hashes are in `SOURCE_RECEIPTS.json`; exact reading locations are in `READ_LEDGER.md`. This ledger supplies mathematical inferences about explicit architecture models, not experimental feasibility or a general no-go theorem.

## 4D adjacency placed in ordinary 3D

Assume an injective placement of 4D lattice cells into R^3 with at most rho cells in any unit-volume ball, up to fixed geometric constants. A cell has fixed onsite Hilbert dimension; if its internal degrees are themselves spread nonlocally, that is already an additional resource. Let ell be the maximum physical range of a native nearest-neighbor cell interaction.

For 1<=r<=cL, a graph ball contains at least a r^4 cells. Any of its cells can be reached by at most r native edges, so its image lies in a physical ball of radius r ell. Bounded density gives

    a r^4 <= C rho (1+r ell)^3.

Taking r proportional to L yields

    ell = Omega(rho^(-1/3) L^(1/3)).

Equivalently, constant interaction range requires density Omega(L), under these placement assumptions. The physical diameter of a bounded-density data block is at least Omega(L^(4/3)), although its native graph diameter is O(L). This validates the producer's packing obstruction and states its exact quantifiers.

This is a bound on the **maximum** edge range, not on every edge or an average wire length. It does not prohibit long-range couplers, optical links, moving qubits, synthetic dimensions, higher local density, or a different 3D code. Those choices change the resources. It does not imply a lower bound on a useful device size or on an experimentally achievable error rate.

If a native edge is simulated by at most s elementary bounded-range edges of physical length r0, the same argument gives s=Omega(L^(1/3)/r0). With finite signal speed, some native interaction needs a growing latency unless another resource changes. This does not by itself prove a universal correction-rate scaling law: pipelining, contention and noise in the mediators require a hardware-specific analysis. The instantaneous fixed-rate native jump model cannot simply be retained through that simulation without proving a replacement theorem.

## Conditional mediator-space bound

A stronger statement can be made when the hardware is a bounded-density fixed-range spatial network H with N total sites, and the whole 4D cell grid is implemented as a graph minor of H, for example by dedicated internally disjoint mediator paths. The minor assumption is additional; it is not implied by arbitrary time multiplexing or a shared nonlocal bus.

1. Give each physical site a ball of fixed radius covering its neighbors. Bounded density makes these balls a constant-ply system. [Miller-Teng-Thurston-Vavasis, Theorem 2.2.1](https://www.cs.cmu.edu/~glmiller/Publications/Papers/MiTeThVa97a.pdf) gives a balanced separator O(N^(2/3)) in R^3. This also holds for every induced subnetwork. Recursive separators yield treewidth O(N^(2/3)). The theorem was checked on the original PDF page 4, including its 4/5 balance in d=3.
2. The 4D side-L grid has treewidth Omega(L^3). Here is an elementary separator count: a balanced separator S leaves two unions A,B of components each containing a constant fraction of L^4 vertices, unless S already has Omega(L^4) vertices. For every pair (a,b) in A x B, use the path which changes the four coordinates in fixed order. It must hit S. A fixed vertex lies on at most 4L^5 such ordered paths: at a chosen coordinate stage, three free endpoint coordinates and two choices along the changing coordinate give at most L^5 pairs. Hence |S|4L^5 >= |A||B| = Omega(L^8), so |S|=Omega(L^3). Every tree decomposition has a balanced separator of size at most its width plus one.
3. Treewidth is monotone under graph minors. Thus L^3=O(N^(2/3)), giving

    N = Omega(L^(9/2)) = Omega(n_data^(9/8)),  n_data=6L^4.

This is a conditional spatial-overhead lower bound for faithful minor-preserving routing, not a bound for every implementation of the channel family. Shared resources can evade the minor assumption by paying time, bandwidth, contention, precision, interaction range or another resource. No claim is made that this bound is optimal or achievable for the actual jump predicates.

## Corrector and floor accounting

| Resource | Exact-model mathematical supply | Physical quantity still needed |
| --- | --- | --- |
| Data | n=6L^4; six logical qubits; d=L^2 | Fabrication/placement, loss, leakage, addressability, state preparation |
| Original corrector | 14L^4 active terms; support at most 24 data qubits; rate scale kappa | Syndrome-conditioned selectivity, multi-qubit coupling, bath bandwidth, crosstalk, calibration |
| Completed corrector | kappa(C_v-Id); active Kraus Q_O Pi_O plus inactive projector (or inactive splitting) | Actual completion/dephasing is part of the engineered channel; no claim that all 256 syndrome labels need separate hardware |
| Fault catalog | Fixed support types and summed local proposal-rate budget | Every extra patch/overlap/channel must be charged; a bound per term without multiplicity control is insufficient |
| Full-patch floor | nu(D_patch-Id); D_patch has normalized Choi matrix I/d^2 | Real channel implementation and its errors, correlated timing, entropy/randomness/ancilla resources |
| Perturbation radius | ||E_patch||_diamond <= nu/d^2, E HP and trace annihilating | A measured local-generator discrepancy including coherent drift and non-Pauli errors; not a gate-fidelity number without conversion |
| Readout | Fixed perfect syndrome recovery, with analytical global fallback | Noisy syndrome acquisition, decoding work, communications and latency, final correction/readout fidelity |
| Clock law | Independent state-independent correction/fault proposals | Bath Markov approximation and timescale separation; correlations, finite-memory effects and lost operations need separate bounds |

Complete depolarization on m qubits has d=2^m, so the stated sufficient radius is nu*2^(-2m). Some illustrative factors are:

| Floor support | Choi radius factor delta/nu | Interpretation |
| --- | --- | --- |
| One qubit | 1/4 | Covers arbitrary one-qubit generator terms only |
| Two qubits | 1/16 | Covers arbitrary terms on those two qubits |
| 24-qubit correction support | 2^(-48), about 3.55e-15 | A smaller specified catalog can avoid the much larger radius-one universal patch, but the overlap/rate budget and support envelope must be checked for that catalog |
| Radius-one universal 4D cell patch | m=6*3^4=486, factor 2^(-972) | An extremely conservative sufficient radius; no useful numerical tolerance follows from its positivity |

These are sufficient proof factors, not upper bounds on physically tolerable noise and not device lower bounds. The separate small total floor/proposal-rate requirement still applies. In particular, a tiny Hamiltonian/generator radius is not the same as a large Pauli stochastic threshold. No quantitative optimization of the producer's enormous coarse constants was established here.

The floor map factorizes as a product of on-qubit complete-depolarization channels **at the same patch proposal event**. A Pauli Kraus expression has 4^m labels, but that is not a hardware lower bound: randomization or a mixed-ancilla swap can realize depolarization by another architecture. Conversely,

    D_patch-Id != sum_(i in patch)(D_i-Id).

Replacing the correlated patch-clock generator by independent single-site floors does not retain the same full-patch Choi-interior argument for arbitrary multiqubit E. The locality, proposal timing and floor cost must all be kept explicit.

For a concrete calibration conversion, if an ideal jump J is replaced by J+Delta, then a direct multiplication/anticommutator estimate gives

    ||D[J+Delta]-D[J]||_diamond
       <= 4||J|| ||Delta|| + 2||Delta||^2.

With ||J||=sqrt(kappa) and ||Delta||<=r sqrt(kappa), this is at most kappa(4r+2r^2) per jump. All changed jumps on a patch must be summed before comparing with nu/d^2. This is a conservative sufficient conversion, not a measured implementation tolerance.

[Pastawski et al., Section VI and ancilla appendix](https://arxiv.org/html/1010.2901v2) already make the engineering assumptions concrete: many-body system-ancilla couplings, damped ancillary qubits, bath correlation time much shorter than couplings, small elimination parameters, and errors beyond leading-order effective dynamics. Writing a desired Lindblad term does not acquire those interfaces.

## Best available matched comparator, by assumption

There is no single winner after silently changing initialization, bath and geometry. A fair benchmark must state which resource is relaxed.

| Comparator | Match to cold start / continual noise / final ideal recovery | What must be charged |
| --- | --- | --- |
| 3D layer-code partial memory, [2510.06659v2](https://arxiv.org/html/2510.06659v2) | Cold arbitrary code input and ideal final syndrome/Pauli recovery match; bath is Davies, not independent nonthermal Pauli additions; lifetime theorem is limited to a beta-dependent size regime | Temperature/cooling, actual code Hamiltonian and bath rates, size cutoff, decoder cost; fixed-beta asymptotic memory is unproved by the partial result |
| 3D thermal family, [2605.10943v1](https://arxiv.org/html/2605.10943v1) | Exponential-in-n^eta retention and true bounded-density 3D locality; preparation is thermal encoding, not code-space cold start | Preparing the logical-state-times-Gibbs ancillary state, reset/cooling, Hamiltonian engineering, final recovery; its initialization gap is stated by the authors |
| HGP Gibbs memory, [2403.10599v3](https://arxiv.org/html/2403.10599v3) | Graph-local thermal quantum bottleneck and Pauli/circuit-fault compensation; proof uses a Gibbs-weighted decodable ensemble and compensation rates depend on specified errors | Nonlocal graph interactions, ancillas/resets, scheduled gate depth or ideal instantaneous jump assumption, calibration/retuning; no free 3D realization |
| ZSZ numerical passive/MFQEC, [2507.21396v1](https://arxiv.org/html/2507.21396v1) | Repeated faulted circuits with greedy local decisions and final decoding provide a useful finite-code experiment plan; numerical rather than theorem comparator | Nonlocal Tanner adjacency, O(log ell)+O(m) atom moves, scratch traps, routing noise/idling, scheduled syndrome cycles and reset |
| qLDPC repeated perfect recovery from [2609.20537v1](https://arxiv.org/html/2609.20537v1) | Arbitrary cold input, independent Pauli bath and ideal syndrome recovery can match at each interval Delta. For p small, ideal recovery error per round is <=C n e^(-c d). m rounds give <=m C' n e^(-c d) by diamond-norm telescoping | Repeated perfect measurements/corrections and their latency are additional resources; minimum-weight recovery may be expensive; good qLDPC adjacency is generally nonlocal in 3D. The theorem's noise is bounded-depth local channels, not autonomous recovery |
| Static global autonomous recovery, [2308.16233v2](https://arxiv.org/html/2308.16233v2) | Encoded input, static correction and continual Pauli noise can match abstractly | Macroscopic global support and growing recovery rate; its lower bounds do not apply to a distributed fixed-rate local sweep |
| 4D PCC model, [1010.2901v2](https://arxiv.org/html/1010.2901v2) | Closest exact-model physical specification: static local 4D engineered correction, continual depolarization, ideal final recovery; local lifetime evidence numerical | Same 4D connectivity problem, engineered ancillas, different predicate, finite-size numerical evidence |

An especially clear same-code active baseline is repeated perfect syndrome recovery on the 4D toric code itself. Because it is bounded-degree qLDPC with distance L^2, the code-capacity local-channel theorem gives exp[-Theta(L^2)] per sufficiently weak fixed noise interval, rather than the candidate's exp[-Theta(L)] lower guarantee. It pays for global recovery repeatedly. This demonstrates that C0/C1's potential value is fixed unscheduled local maintenance, not the best qubit-count lifetime when ideal repeated global recovery is allowed.

At the exact joint requirements of arbitrary cold input, independently added unheralded Pauli noise, a fixed unscheduled bounded-range finite-dimensional architecture in physical 3D and a fixed ideal final recovery, **no complete matching theorem was identified in this inspected set**. This is not evidence that none exists anywhere. None of the comparisons establishes practical advantage for the sweep candidate.
