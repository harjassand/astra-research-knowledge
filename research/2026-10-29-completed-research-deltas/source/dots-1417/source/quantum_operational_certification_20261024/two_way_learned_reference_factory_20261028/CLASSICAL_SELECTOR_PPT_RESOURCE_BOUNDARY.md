# The PPT boundary for two-way reference generation within a classical-selector qubit family

28 October 2026. Short mathematical companion to the finite NPT front end. This is a scoped capability boundary, not a finite-data exact decision procedure. Its constructive side remains conditional on receiving the finite factory.

Restrict EVERY source call used for resource generation to a classically selected qubit channel E_x from the supplied family. Logical inputs may be entangled across uses or with sender memory, and both parties may use arbitrary local instruments, quantum memories and two-way classical communication. No initial shared entanglement, quantum bypass, coherent encoder-selector source input, or access to a different physical input family is allowed. A coherent Gamma preparation is a separately stronger interface and is not included in this converse merely because its anchors belong to the family.

## 1. Necessity: all PPT family channels cannot generate the reference resource

Suppose every normalized J(E_x) has positive output partial transpose. Equivalently T_B composed with E_x is CP. Starting from a state PPT across sender:receiver, a use of E_x on a sender logical register L preserves PPT. Indeed, if A denotes the remaining sender registers and B_old the prior receiver registers,

    [(id_A tensor E_x tensor id_Bold)(rho)]^(T_Bnew T_Bold)
       =(id_A tensor(T composed E_x)tensor id_Bold)(rho^(T_Bold))>=0.

The right side is CP applied to a positive operator. This statement includes arbitrary correlations with A and previous receiver memory; product source inputs are not assumed. Local CP branches preserve PPT under the corresponding transposed Kraus conjugation. Classical communication, source-independent random seeds, adaptive choices of x and coarse postselection flags preserve it branchwise. Thus every finite allowed protocol starting with no shared entanglement produces a PPT resource on every unnormalized branch, not only after discarding flags.

For a normalized PPT state rho on two D-dimensional output systems,

    <Phi_D|rho|Phi_D>
       =Tr[rho^(T_B) Swap/D]<=1/D.

The Bell-projector test consequently gives

    ||rho-Phi_D||_1>=2(1-1/D).

For D=2 even a single reference transfer therefore has unhalved complete error at least1: apply the proposed transfer to half of a locally prepared Bell pair at the sender and include its retained half in the test. No finite-round LOCC processing, adaptive classical selector or normalized favorable branch evades this. The statement is about the declared family, not every use of the underlying physical source outside that family.

## 2. Sufficiency with an explicit strict margin

If some family channel has non-PPT Choi state, its reference dimension is two, so any negative partial-transpose vector has Schmidt rank at most two. The neighboring ordinary NPT front end constructs local contractions from such a witness and proves the quantitative identity

    a(2F-1)=-<v|J_x^(T_A)|v>.

For a supplied strict witness-gap promise, that front end learns the encoder and witness using actual ordinary probes, certifies it on fresh ordinary outputs, pays all filter failures and supplies fixed-margin Bell-diagonal pairs. The finite recurrence/code-teleportation factory then transfers any prescribed finite number of reference qubits to any prescribed positive complete-error tolerance, at its displayed deterministic call/control/memory cap. All post-warm entangled-half inputs and two-way classical messages are explicit resources.

Thus, at the level of whether this classical-selector qubit family can supply arbitrarily accurate two-way reference transport at all, the relevant boundary is whether at least one E_x is NPT. The finite acquired algorithm requires a rank bound, a positive public gap and trusted resources; it is not a uniform useful near-boundary rate. Non-PPT is not equivalent to non-entanglement-breaking when the receiver dimension is larger than three: PPT entangled Choi states remain on the impossible side for this transport task.

## 3. Important distinctions

* This is not an unassisted quantum-capacity classification; the amplitude-damping and depolarizing fixtures are antidegradable yet pass the assisted side.
* It does not solve arbitrary higher-dimensional NPT distillability: Schmidt rank at most two is supplied here by the LOGICAL INPUT dimension, not assumed for arbitrary bipartite states.
* It does not decide exact PPT versus arbitrarily tiny NPT from finitely many noisy samples without a gap. A stagewise shrinking-gap search needs its own finite horizon, false-qualification allocation and stopping/resource statement.
* It does not cover coherent source encoder selectors, unknown source memories, pre-shared entanglement, source interfaces outside the family, or free local fault tolerance.
* It does not change the strongest conventional comparison: with the same assistance, directly code-teleporting payloads is simpler than learning a new one-use decoder when communication alone is the objective.

The converse is the elementary CP/partial-transpose preservation argument above. The filtering and distillation concepts are established prior art; the new finite acquisition composition is documented separately and carries its own receiving status.
