# Gap-free online learning inside a finite guarded operation
2026-10-29. Author composition, independent review pending. Governing dependencies: v1 star-loss transfer, v2 exact rational learner, received physical-permutation CP/memory theorem, and the already constructed arbitrary-error CSS outer code. This adds finite roles/readiness; it does not assert competitive gate complexity or laboratory performance.

## Protocol and exact scope
Fix even n, a fixed K-dimensional singlet subcode, horizon/cap T, desired J service slots, correction radius t and allowed validation failures b. Choose p+a+s=1. Each unfinished round:
1. Draw candidate star rotations from the current independent expert distributions using fresh private coins; set the root frame toI and all other site frames to those rotations.
2. Privately choose LEARN with probabilityp, VALIDATE with probabilitya or SERVICE with probabilitys, independently of the fresh candidate draw.
3. LEARN uses the actual product-probe bank and updates the expert weights. VALIDATE uses a fresh matching-survival test in this candidate frame. SERVICE uses the same candidate frame and the actual private physical-permutation orbit on the next outer-code symbol.
Stop with acceptance after J services if at mostb validation failures; abort at b+1 validation failures, sampler exhaustion or the cap. If the Jth service completes on the last allowed round, acceptance is evaluated before cap exhaustion; exactly T calls are allowed, not T−1. The unknown payload may instead be deferred by the separately received resource-first wrapper.

All three choices use the same physical-source port and pre-call process boundary. No current role, probe setting, matching or group key may leak externally. For the online-learning READINESS proof the source must also not learn the fresh candidate-frame draw before its current channel is fixed. It may know previous frames/records and react to the current quantum input through that fixed map. Merely hiding a role while broadcasting the fresh randomized action is insufficient for the expert-loss argument.

## Soundness outside the collective-family promise
Conditioned on any chosen frame, the physical orbit gives a virtual CP good/bad instrument and p_bad<=C_n q_match, C_n=(n+2)/(n-1). Thus the competing-risk ratio is R=C_n s/a. LEARN calls may alter memory arbitrarily; they do not invalidate this conditional per-round inequality. With r=b+1 and p_f=1/(1+R), the already received negative-binomial guard bounds
 epsilon_guard = Pr[NB(r,p_f)>t]
              = Pr[Bin(t+b+1,p_f)<=b].
The actual outer corrector corrects arbitrary coherent/system-memory errors on <=t service positions. Therefore the accepted subnormalized channel differs by at most epsilon_guard in half diamond distance from identity payload tensor its accepted memory instrument, with the reviewed retirement/output conventions. The hidden collective-frame promise is NOT used in this soundness statement. Finite gate/calibration errors are separate; current role/key privacy and the required complete source boundary remain necessary.

## Gap-free readiness under the structural family
Under the fixed hidden collective-algebra promise, let L_T be the per-edge loss bound from v2, including its quadratic-net approximation. Write alpha_n=D/d=2^n/Catalan(n/2). The same sampled candidate law is used in validation and service. The matching pass expression is f0+nonnegative variance, so q_match<=p_raw. Consequently
 E total validation failures <=a alpha_n(n−1)L_T,
 E total virtual bad services <=s alpha_n(n−1)L_T.
No independent source calls, positive occupation gap or unique frame estimate is assumed.

After a stopping event, pad the analysis with zero-loss dummy rounds; no extra physical calls are performed. The expert weights may be regarded as unchanged because all dummy estimates can be identical across candidates. Markov bounds failure-abort probability by a alpha_n(n−1)L_T/(b+1). If J<=sT/2, private role coins give service-shortage probability <=exp(−sT/8). A capped exact sampler contributes delta_sampler. Thus

 Pr[ready by cap] >= 1−a alpha_n(n−1)L_T/(b+1)−exp(−sT/8)−delta_sampler.

The bound may be negative at practical sizes; clip it at0. It is a theorem under the exact common hidden algebra, not a numeric guarantee for the executed finite fixture. The prescribed candidates can remain nonidentifiable; only cumulative operational losses matter.

## An explicit positive source-exposure-rate family
Let B=2^h with h>=5, n=4h, and encode h logical qubits as h trusted four-spin singlet blocks. The physical orbit acts on the entire n-spin singlet sector, so its constant C_n does not incur the exponentially large d/K localization ratio of this small product subcode. Use the received full-field CSS outer code of length B over GF(2^h), t=B/8, output B−4t=B/2 field symbols, hence hB/2 logical qubits. Let b=B/32, T=9B, p=1/3, s=2/[3(C_n+1)], a=2C_n/[3(C_n+1)]. Then R=1, s>=2/9, J=B<=sT/2.

The binomial lower-tail bound gives epsilon_guard<=exp(−3B/128) for B>=32. Set epsilon_net=T^(-1/4), choose the rational SO3 net fromv2, and use its dyadic learning rate. Since n=O(logB), alpha_n=O(n^(3/2)) and logM=O(logT), the readiness error above is O(polylog(B)/sqrtB)+delta_sampler, tending to0 without an excitation gap. The quantum payload/source-exposure ratio at the deterministic cap is
 (hB/2)/(nT)=1/72.
This is a constant rate measured ONLY in native source-qubit exposures, conditional on the structural family and ideal/budgeted endpoints. It is not a channel-capacity claim for arbitrary noise, a constant-time computation rate, or a hardware threshold. Quantum buffers, encoder/decoder gates, classical learner time and private randomness remain paid.

The exact rational learner is polynomial but expensive: M=O(T^(3/4)) candidates per edge and integer bit length O(T m²logm) for the simple common-denominator implementation. The existing high-rate Schur subcode plus full-path logical testing achieves the same polynomial learning-transfer order within factor2 and is a strong conventional alternative. Local block matching/six-state tests are also constant-gap verification baselines; no algorithmic separation from them is claimed without an acquisition-transfer proof.

The finite no-reset simulations in this folder do NOT execute this entire large CSS family. They test the actual shared feedback and current-channel transfer on n4, with a finite net containing the true frames. The all-size result is the above analytic composition and remains subject to receiving review.
