# Receiver-owned absorbing rail: an exact destructive quantum transfer

30 October 2026. New explicit finite-dimensional physical primitive and canonical table, developed with the parent. No complete encoded, delayed-arrival or universal-composition theorem is asserted.

## 1. Actual two-site Hamiltonian and onsite dissipator

Source A has basis {v,0,1}. Receiver B has basis {v,e0,e1,d0,d1,x}. The unused x level makes dim(A tensor B)=18=2 times 9; it is an explicit extra physical level, not a hidden logical assumption.

Set

    H = Omega sum_(b=0,1) [ |v,e_b><b,v| + |b,v><v,e_b| ],
    J = sqrt(kappa) I_A tensor sum_(b=0,1) |d_b><e_b|,

with fixed positive Omega,kappa. H is a genuine two-site Hamiltonian on A/B. J is one receiver-onsite jump that resets the transfer phase without resolving the logical label b. Replacing it by separate b-resolved jumps would dephase the unknown qubit and is NOT permitted.

From |psi>_A tensor |v>_B, the dynamics remains in source, intermediate and done copies of the same unknown qubit. A completed J jump leaves |v>_A tensor |psi>_(B,d), including any reference entanglement. The receiving done subspace is absorbing under the declared nominal transfer generator.

This is dissipative state transfer, not a claim to invent one-way quantum transport. Its particular value here is the exact old-source firewall and full finite canonical factor below.

## 2. Full canonical table, including every garbage state

Let the canonical gauge basis be

    e_v,e_0,e_1,d_v,d_0,d_1,s,f0,f1.

Define a basis unitary V from canonical logical qubit b times this nine-state gauge to physical A/B by:

    V|b,e_a> = |a,e_b>       for a in {v,0,1};
    V|b,d_a> = |a,d_b>       for a in {v,0,1};
    V|b,s>   = |b,v>;
    V|0,f0>  = |v,v>;        V|1,f0> = |v,x>;
    V|0,f1>  = |0,x>;        V|1,f1> = |1,x>.

All 18 physical basis states occur exactly once. Directly,

    V* H V = I_L tensor Omega(|e_v><s|+|s><e_v|),
    V* J V = I_L tensor sqrt(kappa) sum_a |d_a><e_a|.

Thus the ENTIRE declared transfer generator is identity on the canonical logical qubit, on the full Hilbert space, not only on the admitted source sector. The f sectors and unused e_0,e_1 states are not claimed to encode the original source qubit or to reach the desired output from arbitrary startup. Canonical factorization does not imply canonical initialization.

Admitted encoded loading: A contains the encoded unknown qubits and each B is v. Then every canonical gauge is exactly s and the canonical logical state is exactly A's input. A receiver-vacuum reset performed BEFORE loading preserves the A marginal and can prepare this interface. It is not a free reset during live transfer or after output.

## 3. Uniform nominal completion from the admitted source sector

On the active gauge pair (s,e_v), write P_e=|e_v><e_v| and H_a=Omega sigma_x. The no-done adjoint has a positive Gramian

    R = [[2/kappa+kappa/(4 Omega^2), -i/(2 Omega)],
         [i/(2 Omega),              2/kappa]],

satisfying i[H_a,R]-(kappa/2){P_e,R}=-I. Let r=1/||R|| and C=||R||/lambda_min(R). The probability that no done jump has occurred by t is at most C exp(-r t), uniformly over the logical input and reference. Conditional done output is exactly the input qubit. In the nominal admitted process, the old source is vacuum after completion.

The clock-tail calculation is a local nominal bound. Arbitrary receiver or source perturbations can populate the other gauge sectors. A sustained-noise moment/basin argument for the full code apparatus has not been proved here. In particular the f sectors are stationary for the transfer generator, so an all-state finite-time hitting claim is false without additional physical handling.

## 4. Exact post-transfer source firewall

Let P_D=I_A tensor (|d0><d0|+|d1><d1|). Then

    H P_D = P_D H = 0,       J P_D = 0.

Every operator supported on the old source A preserves P_D. Within P_D the physical decomposition is literally B's logical qubit tensor A's gauge. Consequently an arbitrary later CPTP map on old A and its retained environment cannot change the B marginal when no later interaction couples that environment to B. No source-side DONE bit or source program state is trusted to enforce this: the absorbing rail is at B itself.

For a shared bath with later weak interactions at B, this statement is a structural firewall, not a denial of bath-mediated influence. All future B-touching perturbations still carry their actual norm budget. Old-source actions can change the bath but cannot turn the declared source-router coefficients into a new strong B-data interaction; those coefficients annihilate P_D identically.

If a canonical memory generator on logical qubits/controllers is conjugated by the product of V_i, its coefficients restricted to every done B rail act on B DATA and the retained memory controllers, independently of old A. This gives an exact possible memory interface. Group each A/B pair as one explicitly capable fixed-dimensional column, so arbitrary canonical column operators remain onsite and hub/column terms remain two-site in that grouped hardware. It is not elementary-qubit locality. The retained memory controllers have not disappeared or become a detached output device.

## 5. Why this is not yet a composable unrolled processor

### Dormant receiver poisoning

If B is prepared vacant long before its genuine input arrives, a single local fault can put it in d0. The absorbing rule then refuses the later genuine input. Under a persistent positive false-done rate, this preactivation error probability grows with the entire waiting time. The exact firewall therefore trades reentry protection for a fresh-vacant-input obligation. It does not by itself remove the earlier dormant-bank accumulation problem.

Unconditional scrubbing of done B would fix false done but erase a genuine unknown output. An unconditional fill/timeout can likewise occupy a bank before its real input arrives. Source-only restart commands must not be assumed able both to repair every false done and to leave every real done immutable.

The indistinguishability is exact when two histories reach the same local state, one holding a genuine |0> output and one a premature false |0> with no arrival. A local Markovian rule with the same retained controller state cannot erase the latter while preserving the former. A fresh reliable arrival/history record, a physically qualified pre-ARM window, or a different encoding must separate those histories. This is not an impossibility theorem for sufficiently redundant protected control.

### Old and new memory engines

Conjugating one memory by V gives a single paired apparatus. It does not prove that an independently running previous memory can export into a new memory while both act on partly transferred DATA. On done rails old A-only action is harmless. During the mixed source/intermediate/done epoch, source checks, receiver checks, partial native prefixes, locks, and reset operations require a common canonical basin or a finite-window error bound. Generic native compilation can hide unsafe B actions in intermediate prefixes; the explicit dark-rail restriction must hold at the actual coefficient level, not only for a completed target channel.

### Arbitrary future gates

The preset target-dressed gate comparator remains valid only with its full correctable-span premise. A global gauge on successive identity routers cancels earlier frames; it does not accumulate arbitrary computation. This receiver rail supplies destructive export from an admitted input, not a physical command scheduler or universal logical gate.

## 6. Exact next proof obligation

Construct a real preactivation/loading mechanism that makes the receiver vacant immediately before its unknown source is exposed, and a joint source/receiver-memory transition whose bad DATA span stays local under the same continuous-noise budget. Preserve the post-done coefficient annihilation rather than weakening it to a noisy cached DONE. The present exact table makes that target concrete; neither source preparation nor multi-module composition is already earned.
