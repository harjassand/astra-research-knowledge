# Independent review: commutator-controlled effective logical channel

## Scope and exact source

I read the entire `COMMUTATOR_CONTROLLED_EFFECTIVE_CHANNEL.md`, initially 16,428 bytes SHA-256 `b9c22896f3b234ffe4c78f05b0dce325115f73f6d07cfcc3ceea0a7dfd7122bc`. I also read both complete added Sections 9 and 10 and verified the final source: **20,340 bytes, SHA-256 `4d6d102c0c03804d550a78a1c70ddf55ddb374855a488a53c3feab364b16a042`**. This is the binding version.

Verdict: mathematical PASS for the declared SYSTEM/reference/system-only-record output task and the explicitly acquired known-source model. This is a useful ordinary effective-channel receiver, not source-output equivalence, a general bath replacement, a quantum computational separation, or a novelty claim. The source is discarded, controls are prescribed-time system-only instruments, and their actual implementation costs remain.

## 1. Complete norm and initial-input contract

The observable algebra is the direct sum over classical source labels of system operators, with arbitrary reference amplification. A source-independent observable is embedded by P. Its dual output map discards the source. The exact CQ generator and the effective generator below both generate completely positive unital propagators on their respective algebras. Their complete operator norms are therefore at most one, as are the retained-record adjoints of the specified instruments.

The intertwining estimate compares the two maps from a final system observable to the full initial source-indexed algebra. Pairing this uniform bound with ANY initial CQ/system/reference state proves the claimed final trace-norm bound. In particular, initial source/system correlations are not silently replaced by a stationary product law. The effective simulator acts on the same initial reduced system/reference state and does not receive the source label. No effective preparation of the analysis correctors is required.

This scope does not include source-conditioned interventions, source readout or retained microscopic paths. System-record feedback is permitted only in the specified uniformly bounded record-controlled instrument class; rare-outcome conditioning is not an unconditional channel bound.

## 2. One-spin and centered-pair closure

Direct heat-bath action gives Qs=M s with the displayed nearest-neighbor coefficients. The rational weak-bond formulas and boundary rates have the correct orientation. The absolute row-sum certificate for B implies the infinity-norm semigroup bound exp(-kappa*t), by the logarithmic norm of -I+B. Integrating proves the R1 row-sum bound without requiring symmetry of M itself.

For i!=j, only one spin changes in each update, so the product formula for Q(s_i s_j) is exact. Repeated-spin terms become constants; subtraction of the stationary covariance removes them. In the distinct-pair basis they are zero terms, not extra diagonal rates. The diagonal is -2 and the remaining absolute row sum is at most 2(1-kappa), also for signed bonds. This proves the M2 contraction and R2 bound. The centered pair functions have sup norm at most two. For n=1 this space is absent and F2 is zero.

The identity |(x+y)/2|+|(x-y)/2|=max(|x|,|y|) gives the stated two-neighbor row bound when |J|<=1/40. Thus kappa=19/20 is valid independently of n. It is a spin-closure constant, not the earlier native energy-Lyapunov kappa.

## 3. Covariance orientation and actual GKSL generator

With Qs=M s, the solution of QR=-I is R s_i=sum_j R1_ij s_j. This is a row-oriented formula. Applying V to F1 and averaging gives coefficient sum_j C_kj R1_ij=(C R1^T)_ki on D_k D_i. Reversibility gives M C=C M^T, hence C R1^T=R1 C. No transpose has been lost.

D_int=R1 C is positive semidefinite: for f=sum_i v_i s_i its quadratic form is the reversible integrated correlation form <f,(-Q)^(-1)f>_pi. The source functions are centered by global zero-field spin flip. Consequently the real symmetric coefficient matrix produces the stated double-commutator GKSL generator. Factoring D_int=S^T S and using sqrt(2) times its Hermitian operator combinations gives exactly the displayed dissipator. There is no missing antisymmetric Hamiltonian correction.

The complete norms follow by summing coefficient absolute values, not by the dimension of the source space: ||F1||<=2b/kappa, ||F2||<=4b^2/kappa^2 and ||D_eff||<=4b^2/kappa. The factors in F2 are the first resolvent row bound, the pair resolvent row bound, centered-function norm two, and ||D_k D_i||<=4alpha_k alpha_i. The sum b itself can scale with the supplied couplings; the theorem does not claim arbitrary extensive coupling is dimension-free.

## 4. Exact residual and endpoint accounting

Expanding L_lambda T-T L_eff cancels the sqrt(lambda) term via QF1=-VP and the order-one term via QF2=-(I-Pi)VF1. The remaining terms are exactly those in the source. There is no discarded asymptotic remainder beyond this explicit finite algebraic identity.

[L0,D_i] is minus the commutator derivation generated by [H0,A_i], of complete norm at most 2d_i. Therefore [L0,F1] costs 2d/kappa. VF2 and F1D_eff each cost 8b^3/kappa^2. Expanding [L0,D_kD_i] yields 8bd/kappa^2 after the same row-sum and centered-function bounds, while F2D_eff costs 16b^4/kappa^3. This verifies both C1 and C2.

Contractive Duhamel bounds the intertwined propagators by elapsed time times the residual norm. Although T need not be positive or contractive, it is not separately norm-bounded inside the integrand: the integrand contains the explicitly bounded residual between two genuine contractive propagators. At the two ends, ||T-P||<=2b/(kappa*sqrt(lambda))+4b^2/(kappa^2*lambda). Only these two endpoint corrections are needed.

The absence of ||H0|| from this admission estimate is legitimate because the commutators are expanded before taking norms. It does not make simulation of H0 free. With fixed A_i and a bounded time-dependent H0, the same residual proof uses the time integral of its acquired commutator bounds and real access to that evolution.

## 5. Controls and complete retained records

For a system-only retained-record instrument, scalar source functions commute with its adjoint. Expanding its defect with F1 gives gamma_j/kappa. Expanding the defect with each D_kD_i gives 4b gamma_j/kappa^2. The derivation works between the appropriate input/output record algebras; all reference factors remain arbitrary.

Telescoping the full controlled composition through the SAME T gives the sum of interval residuals and one defect per instrument. Both surrounding propagator/control products are contractions. It does not produce a pair of endpoint errors at every control. This establishes precisely the final source formula, with only two endpoint defects and min(2,...) from the channel-distance ceiling.

The universally safe gamma_(j,i)<=4alpha_i follows directly from contraction and ||D_i||<=2alpha_i. For a unitary, conjugating A_i gives the sharper stated bound. These are acquired upper bounds, not an assumed oracle for an optimal CB norm. All actual control gates and retained outcome processing are paid. Direct source-conditioned controls are outside this argument even if implemented by a short circuit.

## 6. Acquisition and concrete admission

For rational tanh(J), all nearest-neighbor coefficients, covariance entries and the n-dimensional inverse solve are finite rational operations. The model supplies the bonds; no unknown-law learning or exponentially large source table is implicit. Pair closure is needed for the proof and need not be explicitly inverted during execution. General operator families may require a dense n-dimensional PSD factor and actual coefficient-list/stack operations; these costs are retained. A numerical factorization must preserve an actual GKSL construction, with its coefficient/factor perturbation paid separately. It does not require an exact zero-eigenvalue oracle.

For a single nonzero A_l, solving (-M)v=C[:,l] and taking v_l has the correct orientation and gives D_int,ll. With a qubit system this supplies an ordinary four-dimensional Liouville generator. Certified dense channel evaluation and, if requested, a CP channel representation/synthesis are the relevant ordinary methods. A large system still requires paid execution of its resulting effective Lindbladian; an n-dimensional source coefficient solve is not a universal classical simulation of an exponentially large system.

For the displayed localized fixture, direct rational arithmetic gives

U=9440/361=26.1495844875...,
W=310400/6859=45.2544102639....

Hence the error certificate at lambda=10^8 is 0.002615410993... and at lambda=10^12 is 0.000026149629742.... The source's slightly larger decimal bounds are valid. They leave the claimed numerical error budgets for epsilon 0.01 and 0.0001, independently of chain length when b=1,d=2 remain fixed. This is a rigorous admission statement for the weaker output task, not a fitted error or stationary-start claim. For smaller lambda or tighter demanded error the method can simply fail its certificate.

## 7. Independent diagnostics and ordinary prior comparison

I read and reran `check_complete_cq_channel.py` without writing its saved JSON. All 32 n=1,...,4, rate/control cases completed. It checks every initial source label, with and without a noncommuting midtime unitary, using full reduced-system channel Choi matrices rather than one stationary input state. Complete CQ input distance is the maximum label-conditioned diamond distance; the unnormalized Choi trace norm is an upper bound and half of it is an entangled-input lower bound for these qubits. The script's lower-bound assertion is a diagnostic necessary check, not an SDP or certified diamond computation. Double-precision trace defects up to 1.91e-10 are explicitly reported.

I also independently constructed small n=1,...,4 signed-bond examples with several noncommuting Pauli A_i and checked the exact intertwiner residual and covariance orientation numerically. Maximum residual was 5.38e-15; covariance symmetry residual was below 1.88e-16 and the computed integrated matrices were positive. These checks support sign/index inspection but are not the proof or a numerical certification backend.

This is ordinary Poisson-corrector/adiabatic-elimination machinery. I directly inspected the accessible primary Le Regent--Rouchon paper's setup and Lemma 3 (https://arxiv.org/html/2303.17308v2), and the Grigoletto et al. setup and first-order reduction discussion (https://arxiv.org/html/2603.11982v1). They establish strong existing Heisenberg/reduced-Lindblad approaches; I do not attribute this exact arbitrary-CQ, reference-and-control constant to an unseen theorem. The concrete acquisition here is the first two spin closures and complete-norm residual/control bounds for this known chain. Neither this review nor the bounded primary comparison establishes originality.

The decisive consequence is positive for the ORDINARY comparator: the localized qubit logical channel is admitted through a small effective generator at the stated rates and tolerances, without invoking the expensive retained-source compiler. It does not reproduce source records/interventions or arbitrarily fine finite-rate corrections. Those different output tasks must not be conflated in either direction.

## 8. Native quantum-input extension

The added lemma is correct for the SPECIFIC acquired direction-merged native generator. Locally its two jump recycling terms on diag(a,b) add to (a+b)Pi, and its anticommutator is -{Pi,diag(a,b)}. Their off-diagonal entries cancel exactly, leaving diagonal entries r0(b-a), r1(a-b). Scalar source coefficients give the same identity for system/reference-valued blocks. Context merging does not create cross-context entries from a source-diagonal observable.

Therefore native source evolution, the diagonal coupling, H0, and system-only retained-record adjoints all preserve the relevant source-diagonal observable algebra. Every backward logical observable remains there. Its expectation in an arbitrary quantum source/system/reference state equals its expectation after initial source dephasing, and that dephasing preserves the initial reduced system/reference state. Applying the already proved CQ estimate gives the same logical output bound for arbitrary native quantum initial correlations. This is a proof identity, not an operation or preparation performed by the effective simulator.

It is not equality of raw source states, source or jump records, or processes permitting source interventions. A different quantum lift having the same stationary state or merely the same diagonal transition rates need not satisfy the required adjoint-algebra identity. This extension receives that actual identity from the frozen geometric source, not from a stationary-state analogy.

## 9. Local scalar coefficient acquisition

The added local coefficient bound also checks. Starting from l, a length-k term in (B^k C)_ll uses B rows only at distances at most k-1. For k<=R those rows agree with the open radius-R subchain, and the terminal covariance entries agree by the path-product formula. Thus the first R+1 Neumann terms match, including signed bonds. Deleting an outside bond cannot increase the absolute row sum because the two-neighbor sum is tanh(|Jleft|+|Jright|), while a remaining boundary row has tanh(|Jremaining|).

Both residual tails are bounded by r^(R+1)/kappa, giving the displayed factor two for the coefficient difference. Contractive effective-generator perturbation gives the stated logical-channel cost 8 alpha_l^2 T r^(R+1)/kappa through the same controls. The local coefficient remains positive as an actual integrated covariance, so this reduction does not introduce a non-CP effective channel. If the whole physical chain is retained the error is zero; for r=0 the radius-zero solve is exact. These zero-tail cases must not be confused with an unnecessarily positive geometric bound.

For kappa=19/20 and R=4, the coefficient upper error is exactly 1/1,520,000 and the time-one, alpha_l=1 generator/channel error is at most 1/380,000. A chain of at most nine sites therefore suffices for this additional coefficient allocation in the displayed useful regimes. This statement requires paid local data access and an already acquired global family/row-sum certificate. Arbitrary n-entry input validation cannot be replaced by inspecting nine sites. The final source states that acquisition boundary explicitly. No implicit QRAM, unknown-model learning, or general local-to-global verification is used.

## Final status

All final source additions have been read, and the final hash above is verified. The theorem and its native restricted-algebra/local-coefficient consequences pass in their stated output/access scope. Subsequent executable coefficient or channel code requires its own audit; this receipt does not claim it exists or has been tested. The full retained-source compiler remains a different and more demanding task.
