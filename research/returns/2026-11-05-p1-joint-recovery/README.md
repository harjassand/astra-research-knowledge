# Arbitrary-accuracy causal compression with a physical reverse decoder

The supplied recovery return constructs a causal energy-window compressor for the **actual homogeneous tracial partial-SWAP stream**. It gives a finite-angle/count recovery bound and a strict, potentially tiny weak-angle memory-coefficient improvement over the explicit store-all inverse reader, after paying extra acquisition. **The unrestricted optimal joint angle/error/memory/processing law remains unresolved.** Retained memory still has quartic weak-angle order, and generic block circuitry is exponential in block size.

Read the [37-page consolidated report](package/output/pdf/joint_recovery_continuation.pdf), [complete energy-compressor proof](package/joint_algebra/train_energy_compression.md), [general loss/retention framework](loss-and-retention.md), [processing, restricted boundaries and evidence](processing-and-evidence.md), [original ZIP](original/joint_recovery_continuation.zip), [complete interruption-recovery capture](P1_JOINT_RECOVERY_INTERRUPTION_RETURN_20261105.txt) and [provenance](SOURCES.json).

The capture preserves the recovery prompt, complete current rendered answer/activity, native prefix and the earlier interrupted trace. The ZIP arrived after capture; its historical unavailable-download header is unchanged. The final recovered answer governs over tentative statements in the predecessor trace. No missing response or thinking text is reconstructed.

## Fixed source and finite recovery law

An arbitrary qubit, including its inaccessible reference, encounters fresh independent I/2 carriers once each through `U=cos(theta)I+i sin(theta)SWAP`, `0<theta<pi/2`. Receiver processing is chronological and permits initialized workspace, instruments and feedback. The final source is discarded; there is no source access, bath purifier, preparation key, return link or changed emitter. Error is half diamond norm.

Write `s=sin(theta)`, `r=1-s^4`. The accepted store-all inverse-dummy decoder has error `3r^N/4`. For an n-carrier block, n>=2, the new two-outcome positive instrument has `A_-²+A_+²=I` and each support rank at most `floor((47/48)2^n)`. All outcomes are retained; no success postselection is used. Set

```text
delta_n=min{1,4pi²s^4(1+r^(n-1))/(n-1)},
fbar_n=min{1,delta_n/(1-r^n)}.
epsilon_rec <= (3/4)[r^N+(1-r^N)fbar_n].
```

Full blocks are processed, with an incomplete last block kept intact. Total implementation channel error nu adds at most nu.

Since `(47/48)^33<1/2`, 33 blocks can be deterministically packed into at most `33n-1` qubits conditional on their classical outcomes. For N divisible by 33n, retained data is at most `N-N/(33n)` and core peak is this quantity plus O(n). Work registers, service queues, routing and physical protection are separate paid resources.

When `n s^4<=1`, `fbar_n<=16pi²/[n(n-1)]`. For ideal target eta, sufficient conditions are `n(n-1)>=24pi²/eta`, `n s^4<=1` and `r^N<=2eta/3`, rounding N to a multiple of 33n. Thus arbitrary accuracy is attained in an explicit joint regime. An all-angle version uses `n-1>=12pi²/eta` and can add O(eta^-1) collection cost; it need not beat raw storage at fixed angle.

## The actual weak-angle comparison includes extra collisions

Fix target epsilon, `e=4epsilon/3`, `L=log(1/e)` and `p_n=16pi²/[n(n-1)]`. Choose fixed n with `p_n<e/2` and `n>4224pi²/(eL)`, before taking theta to zero. Acquiring until `r^N<=(e-p_n)/(1-p_n)` gives

```text
limsup_(theta->0) sin(theta)^4 M_core
 <= (1-1/(33n))log[(1-p_n)/(e-p_n)]
 <= L-L/(66n) < L.
```

The benchmark leading coefficient is L. This is a strict improvement against that reader, not the unknown optimum; constants can require enormous fixed blocks and certify a minuscule saving. Finite synthesis error tending to zero preserves the strict limit under the stated service/circuit assumptions. It does not establish smaller-order memory or a noisy hardware physical-cell advantage.

## Boundary identity earns low disturbance; supports earn a physical decoder

For `H_n=sum_j SWAP_(j,j+1)` and the actual ordered source circuit U,

```text
[H_n,U]=s²(U SWAP_(S,1)-SWAP_(S,n)U).
```

The extensive charge's disturbance reduces to endpoints. A smooth positive spectral instrument bounds loss by its scalar Lipschitz constant squared times `s^4(1+r^(n-1))`. Exact second/fourth moments of the centred charge give both tail ranks, producing the elementary numerical 47/48 bound without an unknown density-of-states constant. This preserves coherence within each support, unlike measuring a complete spin path or energy eigenvector.

Support encoders K_x=V_x A_x have a Petz branch map equal to the isometric **support embedding**. No inverse filter or small-probability conditioning is needed. Unpacking followed by the original inverse collisions on a tracial dummy gives the deterministic CPTP decoder and exact block recurrence. A complementary Berry–Esseen window option saves roughly half log2(n) qubits per block, using a proved primary theorem with its unspecified constant retained rather than assigned a fictitious numerical value.

The rational-XXX/Yang–Baxter, monotone quantum-norm, recovery-comparison and compilation machinery are credited in [source records](package/source_manifest_joint.json). The source describes complete new proofs/finite cross-checks, not external peer review. The older [crossing and carrier-loss results](../2026-11-05-p1-causal-recovery/README.md) remain intact. Erasure before access is not coherent compression before discard. No scientific programme, dense solver, native compiler, PDF builder, fresh Capital audit or corpus build was run for publication.
