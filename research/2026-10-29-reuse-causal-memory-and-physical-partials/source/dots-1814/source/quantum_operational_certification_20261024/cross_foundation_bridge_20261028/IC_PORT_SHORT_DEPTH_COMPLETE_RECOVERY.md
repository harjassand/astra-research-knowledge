# Ordinary short-depth calibration of a finite-memory quantum port

28 October 2026. **New constructive candidate; independent receiving pending.** This closes a specific gap left by the classical short-word theorem: complete quantum prediction and full-CPTP recovery, when the **accessible input/output ports actually admit informationally complete ordinary preparations/readouts**. It does not promote a classical-only native library to coherent access. The source memory is never prepared, measured or tomographed. The construction is finite and potentially astronomically expensive; no generic efficient learner, novelty, hardware execution or sample advantage is claimed.

## 1. Physical interface, not an inferred permission

A stationary source has inaccessible memory M of supplied dimension at most d. Every episode starts with the same unknown density rho, independently of all caller systems conditional on the fixed source model. There is a finite native action library. Action a has known accessible input A_a of dimension p_a, accessible output B_a of dimension q_a, and at most b_a classical outcomes o. Its unknown physical instrument is

    V_(a,o): L(M tensor A_a) -> L(M tensor B_a),
    V_(a,o) CP,       sum_o V_(a,o) TP.                  (1)

Maps and rho are stationary but otherwise unrestricted, including rank/CP boundaries. A forward-only memory action is included by taking p_a=q_a=1. The source supplies no inverse, hidden-memory gate, hidden flag or free waiting call. Every invocation counts as one native call; all local controls, preparation, readout, storage and reset costs are additionally paid.

**Acquisition access.** On each quantum port the caller can prepare a declared finite informationally complete family of input densities and measure a declared informationally complete output POVM. The input is freshly prepared without a retained source-input reference; the measured output is discarded before the next fresh input. The hidden memory is **not** reset between those calls. Whole-process restarts occur only between episodes and are paid. This is ordinary prepare/measure access on the accessible systems, not environmental access.

**Deployment access.** The same native maps may be surrounded by allowed caller-local quantum operations, retained quantum registers, entangled inputs, recycling, measurements and feedback. Native action labels are selected classically, not coherently superposed. The source memory is initially independent of the caller, the future payload and any inaccessible payload reference. We certify the complete unnormalized/averaged output, including classical records if retained; no guarantee conditional on a rare postselected record is asserted.

The general theorem compares all such controllers using at most H native calls. The recovery corollary below can retain the earlier task's fixed-time, identity-input, exactly-one-payload-USE service. No new deployment USE or service-time choice is needed for that corollary.

This interface is available for the explicit quantum USE port when arbitrary qubit preparation/readout is supplied. It is **not** implied by the older finite classical instrument interface, a four-real-coordinate encoder alone, or a promise about hidden-memory dimension. Applying the theorem elsewhere requires checking these accessible controls explicitly.

## 2. A finite rational informationally complete alphabet

In dimension n, use the following n^2 density matrices:

    |j><j|,
    (|j>+|k>)(<j|+<k|)/2,
    (|j>+i|k>)(<j|-i<k|)/2,          j<k.              (2)

Their Hermitian real span is all of Herm(n). Their matrix-entry real/imaginary parts are rational; no irrational state coordinate is used in the model polynomials. State-synthesis and measurement implementation remain separate paid controls.

For input dimension p_a take these preparations rho_(a,u). For output dimension q_a let Q_v be the matrices (2) and choose

    E_v=Q_v/(2q_a^2),        v=1,...,q_a^2,
    E_0=I-sum_v E_v.                                   (3)

Every E_v is positive and `E_0>=I/2`, because each Q_v<=I. Thus this is an actual POVM with q_a^2+1 outcomes and an informationally complete subset. A one-dimensional output can instead use its sole deterministic effect I.

The induced hidden-memory branch is

    Phi_(a,u,o,v)(sigma)
       =Tr_(B_a)[(I_M tensor E_v)
                    V_(a,o)(sigma tensor rho_(a,u))].  (4)

It is CP: equivalently sandwich the joint output with sqrt(E_v) before tracing B_a. For each fixed (a,u), summing over o,v is TP. Consequently the ordinary calibration experiment is a finite physical HQMM on memory dimension d. Its branch alphabet has size at most

    s=sum_a p_a^2 b_a(q_a^2+1).                        (5)

Every full word probability is polynomial of degree at most length+1 in the source state/Choi coordinates. No posterior normalization, division by rare events or source matrix oracle appears.

Let S(theta) contain all these probabilities for words of length at most

    L=2d^2-1.                                         (6)

The pool contains at most `K=sum_(ell=1)^L s^ell` uncertain event probabilities. This bound is deliberately crude and can already be huge. Each acquired event uses an independent whole-process episode with at most L native calls.

## 3. The load-bearing upgrade: classical IC words determine the full process

### 3.1 Finite-memory word equivalence

For two physical sources theta,theta' of memory dimension at most d, put their induced maps (4) on the direct sum of real Hermitian memory spaces. Its dimension is at most 2d^2. The reachable span from `(rho,rho')` stabilizes by word length `2d^2-1`: if a stage does not grow, it is invariant under every branch map. If the row `(Tr,-Tr)` vanishes on all words through L, it vanishes on the whole reachable span. Hence

    S(theta)=S(theta')
       => all ordinary IC word probabilities agree.   (7)

This is the conventional finite-dimensional automaton argument, not a new equivalence-length claim.

### 3.2 Recovering all input/output kernel coefficients algebraically

Fix any finite native action schedule `a_1,...,a_h` and native outcome string `o_1,...,o_h`. Before contracting any caller operations, tracing the final hidden memory defines the source's h-slot Choi kernel W on

    tensor_(t=1)^h (A_(a_t)^ref tensor B_(a_t)).

Use unnormalized maximally entangled links for this **mathematical definition**, not as acquisition experiments. With the consistent input-transpose convention, an ordinary product preparation/readout has joint probability

    p(u_1,v_1,...,u_h,v_h;o_1,...,o_h)
       =Tr[ W tensor_(t=1)^h
                    (rho_(a_t,u_t)^T tensor E_(a_t,v_t)) ].  (8)

The hidden memory remains coherent throughout. Equation (8) is simply the repeated CP-map contraction; it does not assume a product source process or a finite Markov order.

At each slot, the rho_u^T span Herm(A_a), and the E_v span Herm(B_a). Their tensor products therefore span Herm(A_a^ref tensor B_a). Tensoring over slots spans Herm of the complete kernel space, including operators entangled across times and between input/output legs. Thus equality of every scalar in (8) implies

    W_theta=W_theta'                                  (9)

as actual operators, for every schedule and native-outcome string. One may exhibit dual operator bases to reconstruct W, but reconstruction is unnecessary for the proof and is **not** executed at horizon H by the learner.

The local causal breaks in calibration do not erase what is being inferred: their effects span the multilinear input/output kernel. Missing imaginary-direction preparations, or a non-IC output readout, would destroy this implication. Section 8 gives an exact physical counterexample.

### 3.3 Entangled inputs, coherent recycling and adaptive testers

Any allowed caller circuit acts by contracting its local CP maps and retained registers with the source kernels W. The contractions may connect an earlier quantum output coherently to a later input, carry an untouched reference, entangle inputs across times, or keep measurement outcomes unmeasured in a dilation. Equality (9) implies equality of the resulting accessible density operator, before a final measurement.

Classically adaptive choices of the native action or stopping time are handled by retaining the complete classical record. Each fixed record determines a schedule and a CP caller contraction; sum the equal unnormalized branch operators. There is no division by branch probability. Native coherent superpositions remain excluded because their cross-action kernels are not part of (1) or (8).

We have proved the complete implication

    S(theta)=S(theta')
      => identical outputs for every finite allowed
         quantum controller, including references.     (10)

It is (8)-(10), **not** the mere fact that training records are classical, that permits a coherent guarantee. The original classical-only short-word theorem lacks this spanning premise and remains limited to its stated interface.

## 4. Compact physical model class and computable stability

Use one dimension-d model class K, with rho>=0, Tr rho=1, and unnormalized Choi matrices J_(a,o)>=0 satisfying

    sum_o Tr_(M_out B_a) J_(a,o)=I_(M_in A_a).          (11)

Each J has input dimension dp_a and output dimension dq_a, and `Tr J_(a,o)<=dp_a`. Hence K is a compact rational semialgebraic set. Smaller memory models embed into dimension d with an arbitrary fixed TP completion on the unused block; no extra physical access is inferred from that mathematical embedding.

Real/imaginary Hermitian coordinates are metrized with their Frobenius weights. On A=K times K define

    F(theta,theta')=||S(theta)-S(theta')||_2^2,
    Z={(theta,theta') in A:F(theta,theta')=0},
    g(y)=dist(y,Z)^2.                                  (12)

Z is the relation of complete operational equivalence by Section 3, not equality of hidden-memory matrices. Gauge-related or unobservable models can be far apart in coordinates while already belonging to Z.

The same compact semialgebraic error-bound argument used in the received classical short-word source gives integers n,C>=1 with

    g(y)^n<=C F(y),             every y in A.           (13)

Here this argument is applied to the new physical port class (11) and IC vector S; the old source's particular constants are **not** reused. Compute valid n,C by finite-diagonal enumeration of positive integer pairs and exact real quantifier elimination of

    for every y in A, there exists z in A such that
        F(z)=0 and ||y-z||^(2n)<=C F(y).               (14)

Compactness makes the distance minimum attained, so this is exactly the required sentence. Each test terminates, and the compact semialgebraic inequality guarantees eventual success. All variable counts, polynomial degrees, tested pairs, coefficient precision and solver work are charged. No generic quantifier-elimination computation has been run here.

## 5. Complete-port hybrid: no exponential horizon norm conversion

Let `z=(bar_theta,bar_theta') in Z` attain the pair distance and put

    a=||y-z|| <= [C F(y)]^(1/(2n)).                    (15)

For one parameter displacement u, the initial-state half trace distance is at most `sqrt(d)u/2`. For a native action with at most b_a outcomes,

    (1/2)|| instrument_theta - instrument_bar ||_diamond
       <= (d/2) sqrt(p_a q_a b_a) u.                 (16)

To see this, for each Hermiticity-preserving branch difference use

    ||Delta V||_diamond <= ||Delta J||_1
                        <= d sqrt(p_a q_a)||Delta J||_F,

then sum over its classical outcome blocks and apply Cauchy-Schwarz. The first inequality follows from the Choi positive/negative decomposition: a CP map's diamond norm is the operator norm of its adjoint on identity, bounded by the trace of its positive Choi matrix. Thus the normalization accounts for both physical port dimensions and all outcomes.

For an arbitrary H-call quantum controller, replace the source initial state and ports one at a time. At each replacement, source memory may be correlated with the controller, previous quantum outputs and references; the complete norm in (16) covers exactly those correlations. All later CPTP caller/source operations contract trace distance. Stopping earlier only removes terms. The native action register is classical, so an adaptive call is bounded by the maximum of the per-action constants, not by a sum over all possible schedules. This is a complete-output bound, not a normalized branch estimate.

Set the integer

    B=max_a(p_a q_a b_a),       M_H=d(1+B H).           (17)

The two individual coordinate displacements sum to at most sqrt(2)a. The deliberately loose rational M_H dominates both outer hybrids. The middle comparison is exactly zero for the **same quantum controller**, by (10). Therefore

    D_H(theta,theta')
       <= min{1, M_H [C F(theta,theta')]^(1/(2n))}.     (18)

D_H is the supremum of accessible output half trace distance over all allowed H-call controllers, all initially independent caller input states, and arbitrary untouched references. It includes retained classical records and quantum outputs. Equation (18) is uniform in the controller, so it remains valid for a controller or decoder selected after calibration.

No reconstruction of an H-slot tensor and no tensor-power IC-frame condition number appears in (18). The cost is instead the global physical-model modulus n,C, which can be atrocious. This is a trade in the proof and resource interface, not a claim that long-horizon classical planning or recovery compilation is inexpensive. Unrestricted infinite-time control is not covered by the finite-H statement.

## 6. A finite ordinary count learner

Given rational target complete error eta>0, confidence beta>0 and finite H:

1. Compute/certify n,C for the entire promised class by (14).
2. Choose a positive dyadic w satisfying the exact rational inequality

       4 C K w^2 M_H^(2n)<=eta^(2n).                  (19)

3. Acquire each of the K short event probabilities using at least

       N_event >= log(2K/beta)/(2w^2)                 (20)

   independent episodes, with an outward-certified integer cap. An event indicator is zero on every incompatible outcome; all failed branches and restarts remain paid. Inputs use (2), and output records use (3), with no retained input reference.
4. Impose the simultaneous empirical intervals of half-width w on one model in the **physical** class K. Exact real-algebraic feasibility/sampling returns an algebraic candidate hat_theta, or a resource-capped implementation returns UNKNOWN. On the confidence event the actual source is feasible, so the unlimited exact procedure succeeds even at rank/CP boundaries.

Both source and fit lie in the same intervals, giving `F<=4Kw^2`; (18)-(19) prove `D_H(theta,hat_theta)<=eta` on the confidence event. No fitted latent coordinate is asserted close to the actual environment, and no environment state has been physically observed. The model is an operationally adequate representative, not a hidden-memory tomography certificate.

A simple acquisition ledger is K N_event independent starts, at most L K N_event native calls, at most as many ordinary input preparations and output POVMs, and all classical record/storage/control costs. Counts are finite but may be enormous. The maximum episode length depends on d, not on H; samples depend on H through the paid modulus/precision. Source-synthesis, algebraic candidate evaluation, optimizer accuracy, local receiver memory and final decoder compilation are additional costs. None is silently replaced by an oracle.

## 7. Fixed-service full-CPTP recovery, beyond a finite decoder menu

Fix in advance an actual finite service circuit with at most H native calls and a finite-dimensional output register Y. The future p-dimensional payload and its inaccessible reference are initially independent of calibration and fresh source memory. The service circuit is the same for the source and model and does not change after seeing the source's unknown label.

For example, retain the previous restriction: a prescribed forward-only prefix, followed by **exactly one** quantum USE on an identity-encoded payload at the prescribed time, with the received output and any allowed classical prefix record supplied to the decoder. The result is not achieved by taking an earlier USE, resetting memory during deployment, or coding across extra payload calls.

Let N_theta and N_hat be the induced channels from the payload to Y. They may include an exponentially large declared classical record, whose representation cost is paid. Since the service circuit is an allowed tester,

    (1/2)||N_theta-N_hat||_diamond<=eta.               (21)

For every CPTP decoder R:Y->C^p, contractivity and triangle inequality imply

    | e_theta(R)-e_hat(R) |<=eta,
    e_theta(R)=(1/2)||R N_theta-id_p||_diamond.        (22)

Compute a **physical full-CPTP** decoder Rhat with certified model slack zeta:

    e_hat(Rhat)<=inf_(R CPTP) e_hat(R)+zeta.

For the fixed known candidate channel this is a finite convex recovery problem: the recovered channel is affine in R's Choi matrix, and the diamond-norm epigraph has a finite SDP. A finite exact/interval method with certified feasibility and objective slack is sufficient; arbitrary approximate solver output is not a certificate. All dimensions, numerical precision and synthesis are paid.

Equations (21)-(22) give the actual regret guarantee

    e_theta(Rhat)<=inf_(R CPTP)e_theta(R)+2eta+zeta.    (23)

The comparator uses the **same fixed service**, not a better service time or encoder. The arbitrary decoder class is not a finite supplied menu. No Pauli twirl or Bell-to-diamond conversion is needed: the learned certificate is already complete. A parallel Bell-loss statement follows by the Bell effect, but (23) directly addresses half-diamond regret.

Bad calibration histories cost at most beta because every returned fallback decoder is CPTP and half-diamond error is at most one. Thus expected regret is at most `2eta+zeta+beta`; the averaged deployed channel obeys the corresponding bound by convexity. Add one separately budgeted complete implementation error once. Calibration outputs do not bypass the future payload, and the decoder cannot access its reference.

This is a constructive unknown-source result for the supplied finite-memory port class, not just a two-known-world decision. Its resource advantage is only a maximum-calibration-depth existence statement. It does not establish a useful generic sample rate, an efficient environment-learning method, near-perfect correctability, or quantum advantage over an equally informed conventional protocol.

## 8. Exact failure of an inadequate alphabet, and small diagnostic scope

Consider memory dimension one and qubit ports `U_+=diag(1,i)` and `U_-=diag(1,-i)`. Suppose both the allowed calibration preparations and measured effects have only real matrix entries. For every such rho,E,

    Tr(E U_+ rho U_+^dagger)
       =Tr(E U_- rho U_-^dagger).

All ordinary causal-break words then agree at every length, since there is no retained source memory. Nevertheless a Bell input gives orthogonal pure output states: `Tr(U_+^dagger U_-)=Tr Z=0`. An entangled tester distinguishes perfectly, so their half-diamond distance is one. Adding the imaginary-direction preparations/readouts in (2)-(3) exposes the difference. This is why real-coordinate or single-basis classical statistics cannot be promoted to complete process equality by terminology.

`ic_port_complete_kernel_check.py/.json` verifies rational IC spans/dual frames, this counterexample, and full two-slot kernel reconstruction from ordinary scalar probabilities for a memory-qubit port. It contracts the reconstructed kernel with an entangled-input coherent recycling controller and with a retained-record adaptive instrument, comparing exact output Choi matrices with direct physical circuit calculations. These finite fixtures stress the new input/output-spanning step; they do not execute the generic modulus, acquisition, recovery SDP or long-horizon theorem.

## 9. Governing imports and close prior art

The compact-equivalence-relation construction and confidence ledger extend the method in the received `SHORT_WORD_SEMIALGEBRAIC_PHYSICAL_PREDICTION.md`, SHA256 `b5f83e2d812b7dd64f0e244b7a55093f78f8d02feaff30026d9bfc86468d37fb`. Its classical guarantee is not retrospectively changed. The new work needing review is the explicit port alphabet, its complete-kernel span, the rectangular complete-port hybrid, and the full-CPTP fixed-service selection consequence. No previous receipt is inherited.

The short-basis equivalence mechanism is established prior art: [Wang–Li–Ying, *Equivalence Checking of Sequential Quantum Circuits*, Theorem 5.1](https://arxiv.org/pdf/1811.07722) proves a finite input-basis and quadratic internal-dimension witness for quantum Mealy machines. Its stated model is not silently treated as a theorem about every external coherent tester; Section 3 supplies that additional operator-span argument for the present IC input/output interface.

Ordinary informationally complete operations and process-tensor reconstruction are also established, not new: see [White et al., *Non-Markovian Quantum Process Tomography*](https://doi.org/10.1103/PRXQuantum.3.020344). Finite memory **dimension** here is not finite quantum Markov order. The proposed increment is only the fully scoped composition into a computable short-depth complete-strategy certificate and unrestricted final-decoder guarantee, with all potentially catastrophic costs exposed. No priority claim is made for this composition.
