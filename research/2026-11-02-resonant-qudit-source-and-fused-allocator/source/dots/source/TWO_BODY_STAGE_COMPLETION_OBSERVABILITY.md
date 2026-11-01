# Uniform conditional completion of a coherently driven two-body stage

Reconciled derivation, 2026-11-01 17:32 UTC. Parent supplied the apparatus-ground/excited microscopic proposal. This note proves its conditional stage-completion bound; it does not assume independent clocks or classical neighbor states. No external sources accessed.

## 1. Precise model and admissible environment

Restrict the target apparatus to one live phase with ground g and excited e (each carrying its probe/cache internal multiplicity). Its Hamiltonian is
 H_drive=g(|e><g| tensor U + |g><e| tensor U†),
where U is unitary on the carried probe and the indicated data qubit. For the parent's controlled-Pauli factor, U=sum_b |b><b| tensor P^b. The target completion channel satisfies L_out†L_out=gamma |e><e| tensor I and transfers e coherently to the next ground phase.

All remaining ideal dynamics acts on the environment and preserves this target stage before its completion. Let H_env denote its Hamiltonian, possibly time dependent and of arbitrarily large total norm. Require ONLY
 ||U† H_env U-H_env|| <= B
uniformly in time, after excluding target completion. A sufficient physical condition is bounded total strength of terms incident on the data/probe support of U; all disjoint terms cancel in this difference. For neighboring apparatus Hamiltonians with bounded degree and strength g_q, B<=2 sum_(incident q) ||H_q|| plus any other incident controls.

Other apparatus decay/reset/readout channels act on other apparatus only and commute with U. They may be retained by unitary dilation into an environment: their potentially large bath couplings then cancel from the same commutator. This does NOT justify omitting a data-noise bath or any bath coupling that fails to commute with U. Such local noise is excluded from this ideal bound or must be separately charged. No finite global environment norm is assumed.

## 2. Gauge and exact no-completion equations

Gauge the excited block by U, so the drive becomes g X between g/e. The environment Hamiltonian becomes a common H_env plus an excited-block difference D, with ||D||<=B. Go into the common environment interaction frame. Purify any initial mixed apparatus/environment state; write its no-target-completion amplitude as (a(t),b(t)). Then exactly
 a'(t)=-i g b(t),
 b'(t)=-i g a(t)-i D(t)b(t)-(gamma/2)b(t),
where D(t) is Hermitian and ||D(t)||<=B. Initially ||a0||²+||b0||²=1, with arbitrary phase coherence and entanglement.

The probability of at least one target completion by T is
 P_out(T)=gamma integral_0^T ||b(t)||² dt.
This is a first-completion calculation; subsequent stages are irrelevant to this probability.

## 3. Volterra observability inequality

Set f(t)=b0-i g t a0. Eliminating a gives
 b(t)=f(t)-g² integral_0^t (t-s)b(s)ds
            -i integral_0^t D(s)b(s)ds
            -(gamma/2) integral_0^t b(s)ds.
Young's inequality for these Volterra kernels gives
 ||f||_(L2[0,T]) <= [1+(B+gamma/2)T+g²T²/2] ||b||_(L2[0,T]).

The exact two-vector Gram matrix of f has trace T+g²T³/3 and determinant g²T⁴/12. Thus its least eigenvalue is at least determinant/trace, giving for EVERY normalized initial pair (a0,b0)
 integral_0^T ||f(t)||²dt >= g²T³/[12(1+g²T²/3)].
This includes adversarial initial ground/excited coherence; assuming an initially pure ground state would give a weaker scope.

Combining the two inequalities proves
 P_out(T) >=
 gamma g² T³ /
 {12(1+g²T²/3)[1+(B+gamma/2)T+g²T²/2]²}.

In particular, take T=1/(g+B+gamma). Then gT<=1, (B+gamma/2)T<=1, and g²T²/2<=1/2. Therefore the convenient conservative bound is
 p := gamma g²/[100(g+B+gamma)³] <= P_out(T).
All constants depend only on the actual local strengths, not memory size, environment dimension, or neighboring quantum state. There is no exact dark state with zero completion probability under these hypotheses; unbounded incident detuning/dephasing is precisely what would destroy a uniform constant and is not hidden.

## 4. Uniform conditional tail, not merely an average rate

After any time block with no completion, the normalized conditional state is again an arbitrary allowed joint stage/environment state. The same bound applies. Conditioning is on the past, not on an arbitrarily postselected future neighbor measurement record. Hence
 P(tau_stage>nT | any past history, live target stage) <=(1-p)^n.
Consequently E[tau_stage | history]<=T/p. For any theta>0 satisfying (1-p)exp(theta T)<1,
 E[exp(theta tau_stage)|history]
 <= p exp(theta T)/[1-(1-p)exp(theta T)].

For m sequential stages, each with a common lower p and block T, the conditional tower property gives the m-th power of this exponential-moment bound. NO independence between stages or neighbor clocks is used. Therefore a full finite extraction has a uniform exponential completion tail with constants independent of total memory size. Heterogeneous stages use their own factors.

Finite preparation/readout/controller stages still need their own physical completion bounds and noise charges. If specified as onsite TP jump channels of rate kappa, their waiting times have exact state-independent hazard kappa and can be appended. If only an eventual detector response is asserted, that assertion cannot substitute for a finite response bound.

## 5. Whole-apparatus phase coherence and scope

Different live stage blocks are orthogonal. The Hamiltonian is block diagonal across those blocks; separate decay channels transfer each completed excited block forward. Therefore diagonal phase populations form a closed block evolution, and initial coherences between distinct stage blocks do not contribute to stage-completion counting probabilities. Within each g/e block, arbitrary coherence was explicitly included in the proof. One can apply the bound to each initial block and sum, or condition on the past recorded stage completion. This does not require an initially valid single-particle sector.

If a proposed device instead has coherent couplings BETWEEN different stage blocks beyond the stated e_j->g_(j+1) decay, or a common coherent decay channel merging multiple stages, the block-closure statement must be checked again. The proof is for the explicitly supplied separate-stage channel structure.

Earned: uniform conditional stage and finite-extraction completion for the stated two-body Hamiltonian plus local coherent-preserving decay primitives, with bounded incident commutator B. Not earned here: a complete readout-device realization, stationary duty-cycle independence, a finite-patch positive Poisson compiler under interacting quantum clocks, or a memory lifetime theorem.
