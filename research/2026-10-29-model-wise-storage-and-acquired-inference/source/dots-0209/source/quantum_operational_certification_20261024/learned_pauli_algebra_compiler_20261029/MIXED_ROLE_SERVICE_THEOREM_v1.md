# Finite-innovation entanglement service under a common Pauli algebra
2026-10-29. Frozen for independent audit. This builds on RETAINED_MEMORY_DISCOVERY_v1.md, replacing its one private terminal time with actual repeated mixed roles. Root proposed the service mechanism. No novelty or practical fault-tolerance claim is made.

## Exact interface
Fix n and known k0>=1, g=n-k0. For g=0 exact identity-support service is immediate. Otherwise assume a fixed unknown Pauli label subspace S* with symplectic cost a*+b*<=g, m*=dimS*<=2g. Every joint source Kraus operator at every actual adaptive history has support in span{P_s:s∈S*} on its n fresh source-input/output qubits, tensored with arbitrary operators on all source-accessible memory. The source memory may retain correlations with all older resources. The source has **no access** to private reference registers, isolated stored resources or private role coins; there are no extra source controls on those systems. Current fresh Bell input is independent of the entire previous quantum state, conditioned on the classical protocol history. A fresh input marginal alone would not suffice if its reference were source-accessible.

All ideal controls, Bell preparations, local storage and final classical communication are trusted. One source call maps the same n physical input qubits to n output qubits. Within these restrictions the source can change arbitrarily with time/history, use arbitrarily large retained quantum memory and have coherent Pauli process off-diagonals. It cannot anticipate the private current role or act on a new payload before that payload is accepted.

## Actual protocol (not a counterfactual all-probe process)
Maintain S_t, the span of labels from **actual probe rounds only**. Compile its noiseless factor using the explicit Clifford routine; pad gauge to exactlyg and logical to exactlyk0. Let C_t be the encoding Clifford.

On each round while fewer thanJ service resources have been stored:
1. Prepare n fresh Bell pairs R:B, apply C_t on B, and make the source call. This occurs identically for both roles.
2. Privately choose a fresh role coin, service with probability q∈(0,1), probe otherwise. The coin may be chosen earlier only if it remains inaccessible to the source and has no pre-call effect; post-call choice is cleanest.
3. On a probe: apply C_t* on R, Bell-measure R:B, append the physical-frame label v to S_t, and discard the measured systems.
4. On a service: apply C_t† on returned B, discard gauge from R and B, and isolate the remaining k0-ebit resource. Do **not** Bell-measure it, virtually or otherwise. S_t is unchanged.

Stop immediately afterJ services. Only after allJ resources have been isolated, accept fresh potentially jointly entangled payloads, independent of source/resource preparation (but possibly entangled with an external reference), and use standard trusted teleportation on the stored resources. J is any specified finite positive integer. Final system ordering is by service-arrival index, not source-call index.

## Conditional one-round comparison
Condition on the actual classical prefix H_t, which includes past probe results and roles. The previous stored resources may remain entangled with source memory; trace those spectator resources only to calculate the current marginal channel. Because the fresh Bell input is independent and the role coin is private and post-call, both prospective current branches arise from the **same actual pre-role quantum state**.

The physical probe conjugate restores the unencoded channel's Choi experiment exactly, including its memory instrument. Let p_t(v) be its conditional Bell-label distribution and let p_out,t=Pr[v∉S_t|H_t]. Since the joint support is S*, labels outside S* have zero probability. On the service branch, mixed-gauge identity gives conditional marginal Bell shortfall

  ell_t=1-F_t <= p_out,t.

The branch operations on memory/old resources are NOT asserted equal after this comparison. All future conditioning always uses the branch that actually occurred.

Let A_t be the predictable indicator that round t is reached beforeJ services. Let Z_t indicate an actual probe with v∉S_t. Let L_t=A_t 1[service_t] ell_t, interpreting ell_t as the conditional expected Bell shortfall of the newly stored resource. Then

  E[L_t|H_t] <= A_t q p_out,t,
  E[Z_t|H_t] = A_t(1-q)p_out,t.

Thus E L_t <=q/(1-q) E Z_t. Every Z_t=1 increases dimS_t by1, and S_t⊆S*, so pathwise sum_t Z_t<=m*. Summing nonnegative quantities with Tonelli, without assuming a bounded stopping time or using an unjustified optional-stopping identity, gives

  E sum_services ell_birth <= [q/(1-q)]m*.                 (1)

The stop time is almost surely finite because roles are independent Bernoulli q; expected source-call count is J/q.

## From birth fidelities to a joint stored resource
After a service is stored, later operations act only on its complement. Although later probe conditioning can steer its conditional state, the complete averaged subsequent process through the almost-sure stop is trace-preserving on that complement. Therefore its averaged Bell-projector expectation at the final stop equals its expectation when born. More formally, for each service-arrival index j, sum over its birth prefixes and all future transcripts; the future adaptive instrument is trace-preserving when outcomes are forgotten. Bounded observables and almost-sure termination permit the limit of truncated processes. Hence the sum of expected final marginal shortfalls equals the left side of (1).

On the fixed output resource Hilbert space define P_j=|Phi_(2^k0)><Phi_(2^k0)| on resource j. These projectors commute because resources occupy disjoint isolated registers, even though their state can be arbitrarily correlated. The operator union bound

  I-product_{j=1}^J P_j <= sum_{j=1}^J(I-P_j)

therefore yields for the averaged joint resource state Omega_J

  1-Tr[(product_j P_j)Omega_J] <= [q/(1-q)]m* <= [q/(1-q)]2g. (2)

This is a joint fidelity guarantee uniform over each finiteJ, not a per-history service-quality guarantee and not an assertion about an already formed infinite tensor product.

Set q=epsilon/(2g+epsilon). Then the joint Bell infidelity is at mostepsilon for **every finite requested numberJ of resources**, and expected calls are J(2g+epsilon)/epsilon. Standard teleportation using the joint resource outputs a correlated Pauli channel on all J*k0 logical qubits. Its all-identity probability is precisely the joint Bell overlap; therefore its reduced half-diamond distance from the joint identity channel is at mostepsilon. Entangled payloads are included. This is an averaged reduced-channel statement; it is not a bound of orderepsilon on the full source-purification distance.

## Scaling and physical restrictions
- The common unknown algebra may contain exponentially many labels and need never be fully reconstructed. At most2g actual innovative probes can occur; rare delayed components pay via the private role probability rather than a minimum-excitation premise.
- Gates and binary processing per call are polynomialn using the actual compiler. References are n qubits per current probe; terminal resource storage grows J*k0 per side. Trusted storage is a decisive required interface, not a solved capability.
- q depends inversely on g. For fixed n and error budgetepsilon this gives positive average throughput q*k0 ebits per n-qubit source BLOCK call. If g,k0=Theta(n), this is Theta(epsilon) ebits per block, **Theta(epsilon/n) per physical source-input qubit**, not a nonzero normalized asymptotic rate. The theorem does not establish capacity-achieving communication.
- Physical control/acquisition/storage errors accumulate with number of calls and stored systems. The bound independent ofJ concerns the ideal unknown-source-induced error only. Fixed per-gate/storage noise cannot be ignored asJ grows. Probe-label errors can create false algebra generators and break S_t⊆S*. An implementation must detect excessive learned cost and use an independently justified fallback or abort.
- Full environment reconstruction, Pauli probability tomography, and full-reference-row polar normalization are avoided. Unknown tensor-product frame or non-Clifford algebra discovery is not solved.
- An equally informed conventional subsystem/stabilizer learner may use this same protocol. The mechanism is an operational bridge beyond the iid/excitation requirement, not a proven historical novelty or advantage over all adaptive conventional recovery.

## Evidence and dependencies
Governing exact mixed-gauge identity: COHERENT_MIXED_GAUGE_BRIDGE_v2.md (new, awaiting independent review).
Compiler: algebra_compiler_v1.py (actual elementary Clifford gates; finite exact-binary tests).
Terminal role-hiding retained-memory circuit check: memory_algebra_discovery_v1.py/.json. This validates the one-round role identities and common-algebra memory instrument, but **does not itself simulate multiple unmeasured stored service resources**. The service theorem relies on the conditional argument and commuting-projector proof above; a multi-service joint-state fixture remains to be added. No internal acceptance receipt yet.

## Finite cap and classical-record scope addendum (00:26UTC)
For a deterministic operation cap L, choose Lq>=max(2J,8 ln(1/delta_cap)). Couple roles to L independent Bernoulli coins even after the conceptual stop. The chance of fewer thanJ services by L is at most exp(-Lq/8)<=delta_cap by the standard multiplicative binomial bound. Stop at min(the Jth service,L). If the cap is hit early, supply fixed correctly sized fallback resource states for missing outputs. Apply the innovation proof with the bounded predictable alive indicator; add at mostdelta_cap for the cap event. Joint Bell loss is thus bounded by [q/(1-q)]2g+delta_cap. This is the finite executable version; it does not condition on successful acquisition or hide failure runs.

Teleportation outcomes and correction-key records are averaged/discarded in the claimed reduced channel. Retaining them requires a separate channel-distance argument; no such extension is assumed here. The pre-payload acquisition transcript can be treated as a classical flag independent of the subsequently accepted payload: conditional on that flag, ordinary teleportation is still a Pauli channel, and the average error is the weighted Bell shortfall. Correlations with inaccessible source purifications remain outside the linear-error claim.
