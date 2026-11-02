# The physical recurrence contract, without an activity or exponential-tail demand

Same-principal continuation. This is the ordinary stopped-Lyapunov/Filonov foundation, not a claimed new recurrence criterion. The exact source-switch/repayment operation needed to satisfy it for general weak reversibility remains to be constructed. Completed predecessor packets are unchanged.

## 1. A sufficient common contract at the intended conclusion

Construct the embedded raw-channel chain first, with its actual independent Exp(q(x)) holding times. On an active closed irreducible marked class let U>=0 have finite sublevel sets and let K be finite. A selected episode starts outside K, includes at least its first genuine jump, and ends after an almost surely finite number of genuine jumps. It may have INFINITE expected jump count. It must have a proved finite physical mean and a complete actual-output bound

    E_x[ sigma + U(actual endpoint)]<=U(x).                   (P1)

The same rule is restarted at the actual new marked state. No q occupation, unit drift per episode, uniform multiplicative contraction or return MGF is required. For a more demanding physical reward f>=1, replace sigma by integral f dt only when that bound has actually been proved.

Finite-head successors must have finite physical hitting cost under the same construction. This is automatic when the raw list is finite and every outside starting state has bound (P1). A finite irreducible trace then closes actual return, as below.

## 2. Why this weaker skeleton still rules out explosion and pays return

Until an endpoint enters K, U(Y_n) plus accumulated physical episode time is a nonnegative supermartingale. Its finite-stage expectations are part of (P1), not an assumed optional-stopping extension. It converges almost surely and expected accumulated physical time is <=U(x).

If there were infinitely many outside episodes, convergence of the nonnegative supermartingale would bound U(Y_n), hence would confine all episode-launch states to a random FINITE set. On a fixed finite set their genuine rates are bounded above. Every episode includes its first actual holding time, whose conditional law is Exp(q(Y_n)), independently of its next channel. Infinitely many such nonoverlapping holds cannot have finite total time: conditionally each exceeds any fixed small a>0 with probability at least exp(-a q_max)>0. Conditional Borel-Cantelli, followed by a countable union over finite sublevels, supplies the contradiction.

Thus the head is reached after finitely many episodes almost surely, and its physical hitting mean is <=U(x). Each episode has finitely many jumps almost surely, so no explosion occurs before that head. No bound on the EXPECTED number of episodes or genuine jumps was inserted.

From each head state take one ordinary jump. There are finitely many successors, finite initial holding means, and uniformly finite physical excursion means by (P1). The trace of the ORIGINAL marked chain on the finite head is irreducible. A finite path/block lower bound gives a geometric expected trace return count. Summing actual excursion means by the strong Markov property gives finite positive physical return to a chosen marked head state. Its repeated fixed-rate holding times have divergent total almost surely, proving nonexplosion for the entire chain. The physical regenerative occupation formula gives positive recurrence. There is no implication of finite stationary q.

Episodes that stop before their first jump can instead use the standard Filonov lower condition sigma>=first_jump wedge eta, with a positive uniform eta on each finite sublevel. The same nonaccumulation argument applies. An episode with infinitely many jumps before termination needs a SEPARATE localization/nonexplosion proof; (P1) is not permission to ignore such an explosion branch.

## 3. Exact calibration: positive recurrence need not pay stationary activity

Consider the one-species mass-action network

    0->A (1), A->2A (2), 2A->3A (1),
    A->0 (3), 2A->A (1).

It is NOT weakly reversible and is not offered as a counterexample within the target class. Its birth and death rates are

    lambda_n=n^2+n+1, mu_n=n^2+2n.

For U(n)=n the exact physical generator is LU=1-n. The ordinary physical Foster/nonexplosion argument proves positive recurrence. Its stationary weights obey

    pi_(n+1)/pi_n=(n^2+n+1)/[(n+1)(n+3)], pi_n~C n^(-3).

The asymptotic follows by expanding log of the exact product; the remainder is summable. Therefore pi is normalizable while E_pi q=+infinity, since q_n=2n^2+3n+1. The embedded stationary measure is asymptotic to C/n and is not normalizable; expected genuine-jump return is infinite. Physical return mean is finite. This exact ordinary example is a discriminator against silently turning the physical target into an activity theorem, not a new favourable endpoint.

## 4. The primary lead changes the proof target, not the dimension

Agazzi-Laurence, arXiv 2610.31550v1 (22 October 2026), Theorem4.1/Definition4.2 and AppendixA.1, use expected energy loss paying elapsed physical time. Their theorem is PLANAR bulk stability with assumptions on compactified drift and compatible boundary estimates; it does not solve the coupled four-species boundary problem. Their diagonal repulsion hypothesis also limits admissible polynomial growth. Thus arbitrarily increasing a receiver's power is not a free operation. Their patching lemmas require actual ordering or smoothing estimates across collars; no transport inequality is imported here.

The present live candidate is a polynomial of the marked log-factorial value, with state-dependent physical episodes and explicit first/second increment controls. Neutral switches and rare repaid switches must be tested at that SAME receiver before assuming their former theorems compose.
