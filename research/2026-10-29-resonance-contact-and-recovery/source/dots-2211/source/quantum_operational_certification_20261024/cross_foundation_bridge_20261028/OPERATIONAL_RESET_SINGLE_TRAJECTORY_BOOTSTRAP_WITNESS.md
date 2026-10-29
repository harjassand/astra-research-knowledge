# A noncircular single-trajectory reset witness, under a revealing pointer interface

28 October 2026. Candidate companion to OPERATIONAL_QUOTIENT_RESET_CERTIFICATE.md. This is a restricted physical bootstrap, not generic hidden-process identification. Its structural promise is stronger and unusually transparent; conventional Markov-chain methods can use the same observations.

## Physical class

The declared native action measures a memory pointer bit in the computational basis and emits that actual bit X_t, then flips the pointer with a fixed unknown probability q in(0,1), and increments an inaccessible counter. The flip is an independent classical draw each use, not an arbitrary memory-controlled rate. The counter never affects accessible behavior. Initial pointer/reference correlation is allowed. The measurement removes pointer coherences on its first use; no input or counter reset is supplied.

After N+1 consecutive calls, the actual observed transition variables

    Y_t=X_(t+1) XOR X_t, t=1,...,N

are independent Bernoulli(q) variables even when the initial pointer is unknown or correlated with a retained record. They are the source's physical flip draws, not normalized predictive states. Therefore with qhat=N^-1 sum Y_t and a=sqrt(log(2/beta)/(2N)), the interval

    [q_low,q_high]=[max(0,qhat-a),min(1,qhat+a)]

covers q with probability at least1-beta. Outward-rounded rational bounds on a suffice. Accept only if q_low>0 and q_high<1; otherwise return ABSTAIN at the declared cap. No known numerical mixing margin is required, although completion cost diverges at either endpoint.

## Acquired operational reset

Discard outputs of t further actual native actions. The classical pointer transition has eigenvalues1 and1-2q. For every positive joint pointer/reference state AFTER the initial dephasing, write it as |0><0| tensor A + |1><1| tensor B, A,B>=0 and Tr(A+B)=1. Then after t discarded actions its difference from (I_pointer/2) tensor(A+B) equals

    (1-2q)^t (Z_pointer/2) tensor(A-B).

Its half trace norm is at most |1-2q|^t/2, since ||A-B||1<=1. The counter can be arbitrarily correlated with the record; it remains invisible by the declared interface and need not reset. Every finite future accessible controller inherits this bound by contractivity and the pointer-only operational law.

On the confidence event,

    c=max(|1-2q_low|,|1-2q_high|)<1

certifies reset error at most c^t/2. The exact same actual trajectory both estimates q and then executes the reset word. The bound is uniform over the conditional pointer/reference state after that trajectory, so adaptive correlations created during acquisition do not invalidate it. Add beta and the actual whole-execution implementation debit once.

The acquisition uses N+1 native calls and the deployment reset t further calls, with all output disposal and elapsed time paid. It never samples independently restarted source episodes. This is a noncircular witness that operational reset can sometimes be acquired without microscopic reset. It does not acquire an unknown rank/core or learn arbitrary hidden transition structure.

## Why this does not close the general bootstrap

The emitted bit reveals the relevant predictive state and the fixed independent flip law is a trusted class promise. If outputs are aliased, rate depends on hidden memory, or an unobserved mode later affects the pointer, Y_t need not have conditional mean q. Finite confidence cannot certify these missing model promises. Generic unknown finite-quotient bootstrap remains open.

A slow hidden counter can be added while preserving all observations for a finite period and then change outputs if the pointer-only promise is removed. The point of the witness is a real restricted acquisition mechanism, not an inference from finite observations to universal future forgetting. The standard equally informed competitor is direct empirical transition estimation followed by classical burn-in; the scientific extension is its explicit complete-reference/operational versus microscopic reset accounting.
