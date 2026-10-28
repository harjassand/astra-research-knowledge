# Independent proof: physically exposed pre-noise syndrome excitation

28 October 2026. This separately reviews the concrete exploration architecture; it does not change the logical black-box access contract of earlier sources.

## 1. The physical port is indispensable

A known repetition encoder first maps |l> to |l*111>. The apparatus must then expose the three encoded wires BEFORE the unknown independent physical X-flip channel and its unknown fixed output mixer V. A fresh uniform choice e from {000,100,010,001} is implemented by I or one physical X. It costs exactly two fair bits and at most one extra X gate, not another unknown-channel invocation. This is not an operation assumed available at an enclosed logical source port and not an action on the unknown gauge subsystem.

The current injection label is independent of the logical input-axis/sign and source-current map; it is averaged in the ordinary feedback expectation. Retaining it in a past record is harmless, but conditioning the current asserted moment on it would instead give a different, nonuniform syndrome channel. An unknown output V generally makes post-output local Paulis inequivalent to this pre-noise operation.

## 2. Full coherent channel calculation

For each physical error pattern f and injection e, the effective X pattern is h=e XOR f. The quantum identity is valid on EACH logical basis vector:

    X_h Enc|l> = U_maj |l XOR alpha(h),g(h)>,

where h=e_g for alpha=0 and h=111 XOR e_g for alpha=1. The equality has no phase, so it also holds for every off-diagonal matrix unit |l><m|. Applying the SAME fixed V gives common U=V U_maj for injected calibration and uninjected payload channels.

For a pattern h of weight k, the effective calibration probability q_k is

    q0=(1-p)^2(1+2p)/4,
    q1=(1-p)(1-p+2p^2)/4,
    q2=p(2-3p+2p^2)/4,
    q3=p^2(3-2p)/4.

There are three distinct patterns at weights one and two. Thus

    A_I=diag(q0,q1,q1,q1),
    A_X=diag(q3,q2,q2,q2).

In particular q0+q3=q1+q2=1/4. The calibrated unsigned marginal is I8/8 after any V, not just after a known majority basis change.

Writing t=1-2p, the exact difference is

    A_I-A_X=diag((3t-t^3)/8,(t+t^3)/8,(t+t^3)/8,(t+t^3)/8).

For 0<=p<=1/2 all entries are nonnegative. The X signed block is I4/4. Hence the qualitative CP positivity and identity dominance needed by the margin-free learner hold for this particular mixed physical operation. They would NOT follow merely from adding arbitrary calibration noise to an unrelated source.

## 3. Same-U transfer and the precise information benefit

The calibration signed gaps are 1/8 for X and gamma_cal=t(1+t²)/16 for Z. For p<1/2 these identify the fixed full-envelope X/Z operators through the finite direct-gap certificate. The uninjected payload still uses the SAME U with its original GI/GX weights and optimum loss `3p²-2p³`. Once the operators are certified, the all-gauge receiver theorem applies to those payload states; no equality of calibration/payload gauge distributions is needed.

The native gap is gamma_native=t(1-t²)/8. Their exact difference and ratio are

    gamma_cal-gamma_native=t(3t²-1)/16,
    gamma_cal/gamma_native=(1+t²)/(2(1-t²))

for interior p. Therefore gain occurs only for t>1/sqrt(3); close to p=1/2 the injected gap is smaller. Improving the unsigned marginal floor alone is not a sufficient proxy for improving signed information: the relative Z contrast falls from t to t(1+t²)/2.

As p->0, gamma_native~p/2 while gamma_cal->1/8. The direct-gap fine source-call bound therefore removes this route's native p^-2 cost in the small-noise regime. It still scales with inverse epsilon and the actual gamma near p=1/2, and its funded-cap/acceptance qualifications remain. This is not optimality over every possible calibration learner.

The calibration oracle loss is `(3p-3p²+2p³)/2`; its excess over native payload loss is exactly `(3/2)p(1-p)(1-2p)`, strictly positive in the interior. The probes become noisier in logical loss even as useful all-syndrome information improves at small p. Injection must therefore be switched OFF for the advertised payload service.

At p=0 the extra port excites previously dormant syndromes and permits the certificate. This does not contradict no-access hidden-completion lower bounds. At p=1/2 the Z gap is zero, so the complementary generator cannot be acquired by this route. No observed pass certifies the physical bit-flip/mixer model itself.

## 4. Finite/resource scope

Ordinary logical X/Z eigenstates, the known encoder's two CNOTs and spectator resets, fresh two-bit injection, all product readouts, finite sign fits, synthesized coherent decoder, routing and whole-process implementation budgets remain paid. No protected calibration reference, unknown V inverse, gauge flag or microscopic environment is supplied. The strongest conventional learner receives precisely the same physical injection port and may use the same acquired moments/signs. The architecture's benefit is real within this changed access model, not a generic capability silently inherited by the original logical-port model.

The independent check verifies the physical Kraus construction with nontrivial rational entangling output mixers on every logical matrix unit; checks the actual coherent decoder's common-U SWAP identity; and enumerates actual injection/preparation/product-Pauli labels without source or RNG draws. These are exact mathematical fixtures, not a sampled implementation.
