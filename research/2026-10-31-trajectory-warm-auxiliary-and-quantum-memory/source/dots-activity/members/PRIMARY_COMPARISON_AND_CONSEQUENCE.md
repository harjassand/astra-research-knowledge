# What the graded rapid-loss compiler adds—and what it does not

31 October 2026. Focused primary comparison and constructive ordinary comparator. This note does not claim priority, an implementation, a practical speedup, or literature completeness. The accepted mathematical source is `../graded_reservoir_opening_20261031/GRADED_SECTOR_FIRST_EVENT_RECEIVING.md`, SHA256 93731752d0d34c2fcfa1e7fb0b6812b88f90d301083d32ecd60525cee5b543c9, with whole receipt 8aa67eda1b857be0fccb55e6c711ffc1e2c783787030e117266a159e3a9ccd65.

## 1. Bottom line first

The defensible capability is a succinct physical-channel compiler for the specified vacuum-initialized, common-loss, grade-preserving model, retaining its private memory across prescribed system interventions. It resolves finite-rate corrections to arbitrarily prescribed channel error without a microscopic-rate loop, subject to actual coupling and H_f circuit costs. It is not a universal reduced-model theorem and does not make an arbitrary interacting Hamiltonian easy.

There is NO demonstrated practical crossover. For small systems, a dense exponential already has logarithmic dependence on the microscopic generator norm at high precision; a direct trajectory sampler is not the strongest ordinary comparator. At fixed accuracy and sufficiently rapid loss, a certified second-order eliminated model can be substantially cheaper. Special exact high-order elimination and process-tensor/auxiliary-memory methods are genuine alternatives. The present bounded literature pass did not supply an off-the-shelf theorem with exactly the same large-system, arbitrary-input, retained-control, finite-rate and paid-access conjunction for the interacting Kerr/hard-core class. That is an unresolved comparison, not evidence of novelty.

## 2. Primary results actually checked

### 2.1 Adiabatic reduction is not restricted to a crude second-order heuristic

Azouit, Sarlette and Rouchon, *Adiabatic elimination for open quantum systems with effective Lindblad master equations*, explicitly constructs first-order formulas and Lindbladian second-order corrections for a specified fast dissipative setting. Its all-order physicality statement is a conjecture, not a general compiler guarantee. The primary abstract was read: https://arxiv.org/abs/1603.04630 .

Le Régent and Rouchon, *Heisenberg formulation of adiabatic elimination for open quantum systems with two time-scales*, treats an exponentially relaxing fast subspace and arbitrary small Hamiltonian/decoherence perturbations, using a center-manifold approximation lemma; the stated detailed expansion is second order and preserves quantum structure to that order. Primary abstract: https://arxiv.org/abs/2303.17308 . This is a strong route when a certified finite-accuracy reduction suffices; its abstract does not state the full high-precision circuit/input/control theorem considered here.

Sarlette et al., *Quantum adiabatic elimination at arbitrary order for photon number measurement*, is a particularly important positive comparator, not a paper to dismiss by citing only second-order work. Full primary HTML Sections 2–3 and Theorems 3–4 were inspected. Its Eq.(1) is a two-qubit building block with Hamiltonian Omega sigma_x/2 + Delta sigma_z/2 - chi tilde_sigma_z tensor sigma_z/2 and damping kappa D[sigma_minus]. Conserved photon-number sectors reduce the original setting to this block. It obtains an exact invariant reduced model and a completely positive assignment for that special structure, beyond a timescale-separation restriction. It does not by that fact furnish arbitrary controlled histories of a generic interacting Kerr register. https://arxiv.org/html/2001.02550v1 .

Tokieda, Elouard, Sarlette and Rouchon, *Complete positivity violation of the reduced dynamics in higher-order quantum adiabatic elimination*, gives genuine counterexamples to a general all-order Lindblad-plus-CP-assignment expectation. Full primary Sections I, IV and V.2 were inspected. The Jaynes–Cummings counterexample in Section IV has a FINITE-TEMPERATURE damped oscillator; it must not be misrepresented as a theorem about our vacuum case. Section V.2 explains why discarded transients and correlated invariant-manifold states matter, and why the original product-state full dynamics remains CP. Thus the paper does not prove that high-order numerical elimination is unusable, nor that retaining suitable memory is impossible. https://arxiv.org/html/2303.04495v2 .

A recent positive control is Grigoletto et al., *Approximate Reduced Lindblad Dynamics via Algebraic and Adiabatic Methods* (v2 August 2026). Primary full introduction and framework were inspected. It supplies CP-preserving algebraic reductions with explicit finite-time leakage bounds, given a tractable unperturbed center manifold, and connects them to first-order adiabatic elimination. Its authors explicitly distinguish accuracy, physicality and algebraic interpretation. This is not a general arbitrary-order controlled-process circuit bound, but is a concrete route to better ordinary reductions rather than a missing-CP straw comparator. https://arxiv.org/html/2603.11982v2 .

### 2.2 Retained memory and arbitrary interventions are already standard objects

The OQuPy primary abstract describes a process tensor carrying all environmental effects and algorithms for multitime correlations, control optimization, multiple environments and interacting open-system chains. We therefore cannot claim retained controls themselves are a new objective. The question is the cost of acquiring and applying the representation at the requested norm/error, not whether such a representation exists. https://arxiv.org/abs/2406.16650 .

Vilkoviskiy and Abanin give a rigorous constructive influence-functional MPS bound for the zero-temperature Ohmic spin-boson model, using damped-mode approximation and occupation truncation. Their advertised bound is D proportional to T^4/epsilon^2 for the bond dimension controlling physical-observable error. This is valuable constructive prior machinery; it is a different source/model/error interface from arbitrary interacting Kerr baths and a polylog-precision channel circuit. It is not a lower bound on more favorable tensor networks or other algorithms. https://arxiv.org/abs/2307.15592 .

Rosenbach et al. combine TEDOPA and transfer tensors, learning a compact propagator from trajectories covering the bath correlation time and then extending to long times with linear effort. The primary author/institutional record was read. Acquisition of the short-time data and the intended input/control domain must be counted before using that representation as a channel oracle. This is not a reason to disregard it for the observables and initial conditions it is designed for. https://dspace.mit.edu/entities/publication/827cc8f3-ac03-41d5-be91-c8d4038b5feb .

### 2.3 Existing fast-forwarding results must be compared by operation, not title

Shang, An and Shao's primary abstract describes purely dissipative UNITARY jumps, with a special block-diagonal-Pauli structure allowing exponential depth fast-forwarding via parallel access while preserving the stated query count. Annihilation jumps plus noncommuting interacting Hamiltonian are not that input class. Depth versus total query count is also important. https://arxiv.org/abs/2509.09517 .

Angrisani et al.'s September 2026 primary abstract gives strong dissipation-assisted classical and quantum algorithms for bounded-degree Pauli-noise dynamics, local-observable/2-norm guarantees and suitable random input or Hamiltonian ensembles. Its local-observable bounds are meaningful, but do not by themselves imply a uniform channel guarantee for unknown/reference-entangled inputs under retained controls in our loss-register model. https://arxiv.org/abs/2609.40174 .

## 3. A constructive ordinary comparator: dense scaling and squaring

This argument is elementary and is supplied here rather than claimed as a new numerical method. Fix a certified finite physical cutoff. Let d be the FULL system-plus-reservoir Hilbert dimension, and let L be the explicitly acquired d^2 by d^2 Liouville matrix of its Lindbladian. Suppose a certified bound B>=||L||_diamond is available. All dense matrix entries, input bit lengths and acquisition costs are paid.

Choose s so that B t/2^s<=1. Compute a polynomial/Taylor approximation X_0 of exp(tL/2^s) to diamond-norm error delta_0, then square s times. A Taylor truncation at k=O(log(1/delta_0)+1) is conservative on this unit-norm argument. Entrywise errors convert to diamond error with only dimension-polynomial factors, so a polynomial number of guard bits in log d suffices.

Let X_j approximate E_j=exp(2^j tL/2^s). Since E_j is a channel, ||E_j||_diamond=1. Exact squaring gives

    e_(j+1)<=2 e_j+e_j^2, e_j=||X_j-E_j||_diamond.

Thus, absent rounding, 1+e_s<=(1+delta_0)^(2^s). Choosing delta_0<=epsilon/(4*2^s), and allocating the same weighted budget to arithmetic errors at each squaring, yields final error O(epsilon). This requires O(s+log(1/epsilon)+log d) precision/guard information, not exp(Bt) digits. There are s=O(log(2+Bt)) dense squarings. The algorithm pays a polynomial in d, which is often the dominant cost.

The approximate matrix need not be CP at intermediate steps. If an ACTUAL quantum channel circuit is required rather than a classical propagated vector, form its approximate Hermitian Choi matrix, project negative eigenvalues to zero, and normalize its partial trace by conjugation with the inverse square root of that marginal. For sufficiently small initial error the marginal is close to I and this correction is well conditioned. Dimension-polynomial norm conversions and positivity projection costs are paid; requesting a more accurate initial exponential absorbs them. Diagonalization/square-root arithmetic gives a dense Stinespring isometry, then ordinary dense unitary synthesis supplies a circuit. Small eigenvalues require a square-root accuracy allocation, not inverse-eigenvalue postselection. All these costs remain polynomial in d and precision bits, though unsuitable for an arbitrary succinct many-body input.

Prescribed controls can be inserted between such compiled joint channels without resetting the private reservoir. Arbitrary reference-entangled inputs are allowed because this is a channel construction, not merely a classical state fit. The same retained-memory domain is therefore available to the dense alternative. This defeats any blanket assertion that logarithmic damping dependence alone is new or useful for small systems.

For a bosonic global cutoff, d=d_S binomial(r+L,L); for hard-core registers d=d_S sum_(n<=min(r,L)) binomial(r,n). The graded compiler avoids enumerating this dimension, using occupation/bit registers and actual succinct operations. It has not proved that every competing compressed method must enumerate d.

## 4. What a high-order elimination competitor would actually have to provide

A useful comparator could keep a high-order invariant-manifold assignment, transient variables or an exact reduced memory kernel. There is no demand that it be a memoryless Lindblad equation on the original system alone. To imply the same task it must provide:

1. An acquisition algorithm for the needed resolvents/coefficient operators from the supplied F_i and H_f encodings, without silently forming a d_S^2-dimensional matrix.
2. A controlled truncation/remainder bound uniform on the admitted system/reference input domain, including vacuum startup and the transients recreated by prescribed instruments.
3. A physical output-channel implementation (or an explicitly weaker observable estimator with its sampling cost), including any normalization, reconstruction and auxiliary-memory costs.
4. Complexity in expansion order, mode number, precision, coefficient norms and the number of controls. Convergence of a formal series is not an implementation bound.

Conversely, none of these costs is automatically large. Suppose an ordinary method earns a convergent geometric remainder C q^(k+1), q<1 bounded away from1, and polynomial-in-k acquired coefficient/CP-memory circuits. Then k=O(log(C/epsilon)) would match the sought precision scaling. A bare count of r^k symbolic words is not a lower bound: coherent sums, recurrences and compressed resolvents may avoid it. Our proof's source/LCU machinery is itself an example of avoiding word enumeration.

Large known diagonal frequencies or Kerr coefficients do not alone defeat elimination: they can be included exactly in fast resolvents or an interaction frame. The source compiler's advantage is an earned interface for them, not proof that ordinary approaches cannot acquire another such interface.

## 5. Concrete controlled-memory test and its limit

The separate `CONTROLLED_MEMORY_WITNESS.md` gives an exact vacuum JC/hard-core test. Starting |e,0>, after tau=1/lambda, a system I or Z leaves the same reduced system state but changes a retained coherence. A second identical dwell produces excited-state probabilities differing by

    Delta=4u^2 v^2 >= 4 exp(-4) Gamma/lambda,

for Gamma/lambda<=1/4, with explicit u,v there. A common system-only CPTP future representation accurate also at the intermediate slot must incur trace-norm process error at least Delta/2. It cannot supply arbitrarily small finite-rate error by merely declaring the fast reservoir absent.

This does NOT exclude an elimination scheme carrying the missing correlation or transient, a history-aware memory representation, or the constant-size exact solver. The witness is analytically easy and must not be advertised as a speedup example. It diagnoses a specific interface mismatch: a slow-state model is not automatically an arbitrary-instrument process model.

## 6. A fair useful task specification, not an advantage claim

A clean target for further comparison sets H_sys=0, avoiding attribution of pre-existing closed-system Hamiltonian hardness to this result. Use many system qubits and r private hard-core registers initially all0. Let F_i be explicitly supplied local noncommuting lowering/Pauli combinations, with sum f_i^2=g^2 and fixed Gamma=g^2/lambda. Take a known diagonal bath Hamiltonian

    H_f=sum_i Omega_i n_i+sum_(i<j) V_ij n_i n_j,

with rational encoded coefficients, possibly comparable to or larger than lambda. Give a prescribed finite sequence of system gates or instruments and ask for an implementation of its joint output/record channel within epsilon, retaining the private registers between slots. Unknown input/reference correlations are part of the promise. The goal can subsequently be a protocol fidelity or correlation, but producing that scalar has a separate statistical budget.

Our theorem provides a conditional polynomial-overhead circuit for this explicitly acquired model. Diagonal H_f phases can be computed by finite arithmetic; there is no hidden generic within-sector solver and no H_sys action to exploit. Cutoff and activity are separately bounded, and finite-rate corrections are retained rather than dropped. The same source can have nonlinear cross-excitation phases, unlike an assumed Gaussian influence functional. This is an interface improvement over replacing the bath by a leading Markovian generator, not a proof that the example is classically hard or that its nonlinear effect is experimentally large.

A fair execution ledger must still include: vacuum/source preparation; the actual F_i/adjoint and coefficient access; finite occupation registers; all coherent source arithmetic and failure caps; OAA calls; prescribed consumer gates; numerical input precision; and final readout. For a bounded observable, ordinary repeated-run estimation has the usual inverse-square accuracy sampling burden, even when synthesizing each channel uses only precision logarithms. Amplitude-estimation improvements require their additional reversible/purified access and are not free consequences of a channel theorem.

If epsilon exceeds a certified elimination error and the source/control assumptions match, the ordinary reduced model should normally be used. If the cutoff joint dimension is modest, dense exponentiation or a mature process-tensor/HEOM solver is the natural numerical baseline. Only in the succinct large-system, precision-below-finite-rate-correction regime does the present interface suggest a distinct asymptotic opportunity. No constants, executable benchmark or speedup proof currently establish a practical regime there.

## 7. Strongest next scientific question

For this concrete H_sys=0 diagonal-interaction hard-core family, can an ordinary high-order elimination or compressed process-tensor construction be ACQUIRED with polynomial cost in mode count, physical action and log(1/epsilon), uniformly under the same prescribed instruments, while preserving a physical channel? A positive construction would substantially explain or subsume the current advantage in representation; a quantitative obstruction must concern acquired memory/normalization cost, not merely non-CP truncated coefficients or a large dense matrix. This is more consequential than adding another reservoir model to the existing theorem.

## 8. Evidence scope

This is a focused primary-source comparison, not a comprehensive novelty review. Scientific comparison and proof scopes remain as stated above.
