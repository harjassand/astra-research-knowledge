# Gap-free cumulative encoder learning from shared star-swap losses
2026-10-29. Author construction, independent review pending. No historical novelty, small practical runtime, or unrestricted-noise completeness claim.

## Target
Replace identification of a unique full frame by cumulative protection loss. A fixed unknown product frame makes every actual joint source Kraus operator commute with the corresponding star swaps S_(i,0), at every history. Source memory is arbitrary, need not reset, and may choose different collective operations causally. Current private role, product-probe settings, fresh sampled candidate frames and permutation keys must not leak through external controls. The source map is chosen before these current private choices, though it can of course act on their quantum inputs. Endpoint operations/record retirement retain the earlier explicit trusted-boundary conditions.

Identity noise and one-axis collective noise need not have an identifying singular gap. No positive gap is assumed below. There is no guarantee for a separately chosen future untested channel; the bound concerns the actual interleaved sequence.

## 1. One bank gives all candidate losses
For candidate C in SO(3) on star edge i define S_C=(I+sum_ab C_ab sigma_a^(i) sigma_b^(0))/2 and
 delta_i,t(C)=1−Tr[S_C N_t^*(S_C)]/D, D=2^n.
This is in[0,2]. The true C_i* has delta=0 at every history under the structural promise. Use the previously accepted independent product-Pauli preparation/local-readout bank on probe rounds. If input axes/signs are(c,d;u,v), output axes/signs(a,b;y,z), one sample estimates every candidate's loss by

 hatdelta(C)=3/4−(9/4)yz C_ab−(81/4)yzuv C_ab C_cd.

This is exactly the expansion of the pair-adjoint swap correlation, including the identity row needed for nonunital channels. Its expectation conditional on the pre-call history is delta(C); it requires no reconstruction of the source memory. Bound |hatdelta|<=24. A direct square expansion, averaging input/output axes and input signs (the squared output sign disappears), gives E hatdelta²=747/16+(3/2)delta<=795/16<50. All star edges share one physical probe bank; their correlations need not be independent.

Each candidate rotation has Frobenius norm sqrt3. For any two rotations C,C', operator norm ||S_C−S_C'||<=3||C−C'||F/2, so |delta(C)−delta(C')|<=3||C−C'||F. An epsilon-net of SO(3), made by a three-angle Euler grid, has M=O(epsilon^-3) elements. A nearest net point to the unknown true rotation has loss<=3epsilon at EVERY history.

## 2. Independent edge experts produce consistent frames
Fix horizon T and probe probability p in(0,1). Maintain one exponential-weights distribution on the same net for each of n−1 star edges. At every round independently sample its candidate C_i,t using fresh private coins. Set the root frame toI and site frame O_i,t=C_i,t. These independently sampled star relations define a consistent physical product frame; there is no unresolved global rotation-synchronization rounding step.

A private independent coin chooses PROBE with probabilityp or SERVICE otherwise. A probe produces the full bank record above; service uses the candidate encoder, actual private physical permutation orbit, inverse permutation and matching decoder. Update EVERY edge expert using importance-weighted feedback ellhat_t(C)=1[probe] hatdelta_t(C)/p (zero on service). Thus conditional mean is delta_t(C), |ellhat|<=24/p and conditional second moment<=50/p.

Use w_(t+1)(C) proportional to w_t(C) exp(−eta ellhat_t(C)), initialized uniformly. For eta<=p/24, exp(−x)<=1−x+x² on[-1,1] gives the deterministic estimated-loss bound
 sum_t <w_t,ellhat_t>−sum_t ellhat_t(C0) <= logM/eta + eta sum_t <w_t,ellhat_t²>.
Taking expectation, using fresh hidden sampling/nonanticipation and the fixed nearest true-net comparator, gives per edge
 E sum_t delta_t(C_i,t) <=3epsilon T + logM/eta+50eta T/p.
Choose eta=1/[sqrt(50T/(p logM))+24/p]. Then the bound is at most
 L_T=3epsilon T+2sqrt(50T logM/p)+24logM/p.

This is a gap-free cumulative loss bound, not a claim that the chosen parameters converge to a unique true frame. It permits changing, nonunital and memory-correlated source channels with the same exact hidden swap algebra.

## 3. Star Dirichlet transfer to the actual protected operation
For the current candidate frame let P be its full singlet projector, d=Catalan(n/2). The unnormalized star-transposition conjugation generator
 L(A)=sum_(i>0)(A−S_i A S_i)
has spectral gap at least1 off its fixed algebra. This follows from the interchange-process spectral-gap theorem of Caputo–Liggett–Richthammer (arXiv0906.1238, Theorem1.1): the unweighted star graph's random-walk Laplacian has eigenvalues0,1 (multiplicityn−2),n. Every unitary representation inherits the regular-representation lower bound. This is a known group Poincare theorem, not a source-noise excitation assumption.

Let E_comm be Hilbert–Schmidt projection to the swap commutant. For source Kraus K_a,
 sum_a ||K_a−E_comm(K_a)||F² <= sum_a <K_a,L K_a> = D sum_i delta_i.
On P the commutant acts as scalars. Minimizing the scalar residual therefore gives full-singlet raw bad weight
 p_bad=1−sum_a |Tr(PK_aP)/d|² <=(D/d) sum_i delta_i.
The already reviewed physical-permutation orbit converts this fullP quantity into a CP bad-branch effect for ANY fixed K-dimensional subcode and arbitrary current source memory, without d/K. No complete environment model or full-frame accuracy certificate is needed.

Hence for the actually serviced sequence,
 E[number of virtual bad service slots] <=(1−p)(D/d)(n−1)L_T.
Here a virtual branch is a mathematical CP instrument, not an observed fault label. D/d=2^n/Catalan(n/2)=O(n^(3/2)); taking epsilon=T^(-1/2) makes expected cumulative bad weight O(n^(5/2) sqrt(T logT/p)), with no occupation-gap denominator.

## 4. Consequence and limitations
With an actual outer code correcting t service-slot errors, Markov gives bad-event probability at most the displayed expected count/t. Under the exact structural promise this is an unconditional completeness route; under arbitrary noise outside that promise retain the separate model-free guard for accepted soundness. A high-probability online-learning refinement may improve the confidence dependence but is NOT proved in this version. Fixed service count, role cap, complete correlated-memory outer-code channel composition and finite arithmetic must be explicitly supplied before calling this an executed complete protocol.

The algorithm avoids an exponential product net by learning n−1 independent constant-dimensional edge experts, then using the star Poincare transfer. Naive cost is O(n T M), memory O(nM), M=O(T^(3/2)); this is polynomial but very large. No competitive practical complexity claim follows. Candidate single-qubit gates, private frame sampling, physical permutation routing, trusted endpoint storage, outer correction and SPAM are additional. Finite rounding/sampling errors can be budgeted, but this first proof uses ideal mathematical weights/controls; a compiled finite version is an open obligation.

Fresh frame draws MUST be private. If the source can choose its current loss after seeing the selected action through an external control leak, the expectation of realized loss need not equal the weights' expected loss and this standard online proof fails. Quantum response to the supplied input alone is already included in the fixed current channel and is not such a leak.

## Primary dependencies
- Accepted Astra nonunital product-probe bank, GOVERNING_v1.md and current matrix-confidence review, used only for its actual shot interface/first moments.
- Accepted physical-permutation orbit theorem PHYSICAL_PERMUTATION_TWIRL_v3.md, for the current-memory CP bad effect and subcode operation.
- Caputo, Liggett, Richthammer, Proof of Aldous' spectral gap conjecture, JAMS23(2010), arXiv0906.1238, Theorem1.1. The unnormalized generator convention matters.
- Exponential weights is established online-learning machinery; the displayed elementary potential proof is included to make signed importance-weighted feedback assumptions explicit.
