# Parameterized complementary-Z trial completion

30 October 2026. Working completion for PARAMETRIC_INTERFACE_TRANSFER_CANDIDATE, not covered by the original four-species receipts. It checks the exact graph interfaces in ROOT_Z_TRIAL_LEDGER rather than assuming that ledger transfers automatically.

## 1. Exact activity and preservation

The common fast factor is (A)_a0(B)_q. At B>=q and A<a0 no fast event is enabled. At A>=a0 let a=A-a0 and n=sum_i X_i+D. For n>=2:

* D>=2 enables the positive 2D->a+D channel.
* D=1 and some type present enables a conversion or a+D birth; irreducibility supplies a positive outgoing conversion from each non-a type.
* D=0 is active exactly when a>=2, equivalently A>=m.

All enabled fast moves preserve this activity. Conversions keep D>=1 and a>=0. A birth entering D=0 has a_out>=2. A seed entering D>0 retains n>=2 and a>=0. The 2D reverse channel leaves D>=1 and adds a. Thus the activity indicator I in Z=B-N-hI is preserved, not merely N. The n<2 exceptions are a finite head and are handled by direct actual values/connector trials.

Connector activation from any inactive A>=1 enables activity: if D>0 then A_out=A+m-1>=m>a0, and if D=0 then A_out>=m. Its effect on Z is therefore neutral. Immigration enabling activity lowers Z by h. An active activation raises Z by h. Clearing is neutral if it destroys activity, and lowers Z by h if activity remains. These are the exact trial signs.

## 2. Finite-head clearing paths

For each fixed bound N_*, the active fast process reaches 2a and then clearing by a uniformly bounded prescribed path. With at least two types, convert two chosen molecules while D remains a catalyst. With one type, convert it to a and use a+D->2a; with zero types first use 2D->a+D. If D becomes zero, the resulting a>=2 keeps clearing enabled. At D=0 active input clearing is already enabled.

At most 2L+4 prescribed steps suffice. On a finite N head every required normalized fast rate is bounded below and every normalized total rate bounded above. Requiring each holding time to be at most a fixed multiple of 1/(b)_q gives a fixed positive success probability per fixed time block. This proves finite-head clearing-time moments <=C_j/(b)_q^j, without assuming independence between jump counts and holding times. All states reached by seeds satisfy the same accessibility because the reverse 2D channel is positive.

Adding connector birth stopping only shortens these fast trajectories. The active activation probability in a finite-head subepisode is at most t b U<=C b/(b)_q=O(b^(1-q)); immigration probability is O(b^-q). No stationary law is used.

## 3. Large hidden N

The completed positive-D first-connector law in the transfer supplies T,U<=C N^(-eta)/(b)_q. Hence its activation and immigration probabilities tend to zero uniformly in b>=q, since b/(b)_q is bounded. Its clearing-output inverse profile reset also tends to zero. Choose one fixed N_* so that clearing with A_out>=2m has probability at least a fixed c>0; this output is active regardless of D. This is a down-Z exit.

For active D=0, A>=m. Stop at the first seed, clearing, immigration or activation. Seed and clearing share (A)_m(b)_q with fixed positive marks. The seed probability is bounded below uniformly for sufficiently large b, because

    Ab/[(A)_m(b)_q] <= C b^(1-q),
    1/[(A)_m(b)_q] <= C b^-q.

Its actual seed output has unchanged N and positive D and is covered by the preceding uniform kernel. Active activation before that seed has probability O(b^(1-q)). Thus the bounded-stage large-N trial has down probability >=c, up probability <=C b^(1-q), and mean physical duration <=C. Inactive preparation is identical to the exact activity cases in Section 1: A=0 waits for compulsory immigration; A>=1 prescribes activation or terminates on the actual competing immigration. These waits have a fixed immigration-rate floor.

## 4. Finite hidden N and conditional renewal

In the finite head, prescribe inactive activation followed by actual clearing. If it does not exit down, its neutral net change is N->N-1 and B->B-1. Unexpected immigration terminates the trial; active activation terminates it up. After finitely many such pairs, either down has occurred or A=0. At A=0 prescribe at most m immigrations until activity is first enabled. The first is compulsory; subsequent required races have success probability at least c/z because B=z+O(1) and inactive A is bounded. Therefore

    p_down >= c z^(-(m-1)),
    p_up <= C z^(-(q-1)),
    E[trial duration | actual input] <= C.

The same inequalities hold in the large-N regime after weakening its constant down probability. Conditional renewal over actual neutral trial outputs gives expected trial count O(z^(m-1)), eventual upward strict-exit probability O(z^(-(q-m))), and mean strict-exit time O(z^(m-1)). No independence is claimed.

This earns the same Z stopped-value bound and exterior leakage C AB as the original ledger, conditional only on the transferred positive-D first-connector local law, not on the full graph recurrence conclusion. The r-side phase repair/correction and final two-potential localization still belong to the separate transfer candidate.
