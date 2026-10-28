# Working bridge: fast finite service of q entangled temporal inputs

28 October2026,14:45UTC. **Unreceived derivation, conditional on the separate small-loss bandit candidate.** No source calls. This is the next capability question, not a change to either frozen source or a received repeated-use claim.

## Proposed actual controller

Hold q unknown qubits with arbitrary joint reference, initially product with the source memory. Store them trusted until used, and isolate every recovered output from all later controls/source interactions. Current decoder exploration is fixed privately before each call. While fewer thanq payloads have been delivered, draw a fresh private USE coin of probability r; USE sends the next held payload through the same complete source port and applies the frozen decoder, with no measurement/learning update. TEST instead runs the actual six-state decoder-return experiment, records y, and updates using ghat/p, p=1−r. All role-independent call timing/control boundaries from the terminal theorem remain. Stop whenq uses succeed or at a deterministic capN. On shortfall produce physical replacement outputs for missing slots; no free transmission/bypass of held unknown inputs is assumed.

The PROBE/USE occupation law is not the all-probe law. Write A_t for the predictable indicator that fewer thanq payloads have yet been used. In an analysis padded toN rounds, inactive rounds have zero gradient/loss and do not require source calls. The actual gradient is A_t I_TEST ghat/p. Its conditional mean is A_t times the current linear calibration gradient, and its local second moment is at most(8D²/p) A_t q_t(C_t). These statements are on the actual mixed-service process.

## Why full quantum inputs, not separate marginal promises

Analyze the GLOBAL q-input Choi experiment with a product of q Bell pairs, keeping all references. At each USE the NEXT untouched input/reference Bell pair is independent of the entire preceding process, despite correlations among source memory and earlier references/outputs. This is a property of this global Choi input, NOT an assertion that arbitrary jointly entangled service inputs are conditionally independent. It makes the current conditional channel and the Bernoulli calibration mean legitimate.

The final q-input service is nevertheless one CPTP channel acting on arbitrary joint inputs. Subsequent trace-preserving operations on source memory cannot change an already isolated output/reference marginal when averaged over later measurement records. Thus the expected sum of final delivered Bell failures equals the sum of the current USE conditional Bell failures. Commuting Bell-failure projectors imply I−tensor_i Phi_i <=sum_i(I−Phi_i). Treat shortfall as ONE event of probability beta rather than chargingq beta. Hence

    ell_global <= (3/2)r sum_t E[A_t q_t(C_t)]+beta.

The intended comparator is the cumulative per-use marginal Bell cost

    C_N(D)=r sum_t E[A_t ell(D E_(t,h))]

of one fixed decoder on the ACTUALLY visited mixed occupation. It is not the global entanglement loss of an oracle service, and does not compare to a policy that changes earlier TEST instruments. Under the common CP-dominant algebra contract, the same fixed D_* is per-history optimal. In the logical-noiseless common-algebra subfamily C_N(D_*)=0, so the construction would deliver a genuine reliable joint q-input channel without reset. For general correlated logical noise, replacing this cumulative comparator by relative global-channel risk is OPEN and must not be inferred.

## Candidate explicit cap

Let L_short=ceil log2(16/epsilon), mu=2q+8L_short, and chooseN a sufficiently large power of2. Set r=mu/N<=1/2, p=1−r. Fresh role sampling uses exactly log2N fair bits and a comparison with integer mu per active round. The independent role coins imply shortfall probability at most Pr[Binomial(N,r)<q]<=exp(−mu/8)<=epsilon/16, since mu>=2q. The source never learns the current coin through a separate classical port; quantum input discrimination is part of its same CPTP map.

Use eta=gamma/(128D²), comparator smoothing zeta=epsilon/(16mu), and prox residual delta=eta epsilon/(64mu). Then8eta D²/p<=gamma/8. The small-loss mirror argument would give

    (1−gamma/8)L <= L_D+zeta N+k log(1/zeta)/eta+N delta/eta,
    L=E sum_t A_t q_t(C_t).

Let L0=ceil log2(16mu/epsilon), and choose the least power of2 satisfying

    N>=max{2mu,1024mu D² k L0/(gamma epsilon)}.

After multiplying by(3/2)r, the additive bound is the same39epsilon/112 as the single-terminal calculation. Including shortfallepsilon/16 and one whole-process allowanceepsilon/2 would yield

    ell_global <=(1+gamma)inf_D C_N(D)+epsilon.

With D=3d²,k=2d, the finite source cap scales as

    O((q+log(1/epsilon)) d^5 log((q+log(1/epsilon))/epsilon)
                                        /(gamma epsilon)).

This is near-linear inq at fixed physical patch and target; NOT an asymptotic capacity statement. The logarithmic factor, huge conservative constants, every dense decoder application, all q-input/isolated-output storage, and long holding duration remain paid. It protectsq temporal logical inputs using the SAME local source register, notq simultaneous independent logical subsystems orq recovered qubits per source call.

## Optional global private Pauli framing

Choose independent private Pauli keys for allq input/output slots and do not feed them to the learning rule or public controls. Apply each input frame immediately before its eventual USE and its inverse after the actual decoder; isolate that output. Because future inputs and prior outputs are untouched by intervening controls, this is algebraically the global q-input/output Pauli twirl of the complete adaptive unframed channel. Missing-slot replacements receive the matching output frame too. At the global Choi input, the input keys can be moved to untouched references, so the probe/role record law is unchanged. The averaged q-channel becomes Pauli and its half-diamond distance to identity equals its global Bell loss. This is a conventional changed-service operation, paid by2q private bits and actual trusted Pauli controls, not a guarantee conditioned on keys or a free role-sealing theorem.

Load-bearing checks still needed: finite prox certificates with importance weighting; complete adaptive channel/twirl identity including shortfall replacement and arbitrary reference; exact source occupation when prior outputs are isolated; and a fresh independent receiver/control review. No result is promoted by this scratch note.
