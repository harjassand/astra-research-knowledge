# Independent review: bounded-speed raw-latch ingress
30 October 2026. Scoped PASS of the frozen lower bound under the explicit generator contract below. No novelty assessment and no assertion about a general quantum source carrying correlated side information.

## Frozen source
`ROOT_BOUNDED_INGRESS_LOWER_BOUND.md`
SHA256 `11b6cd5b19522ac910525b7c9e7dbb93e5ecd213f4dbf74ee8ed175f4ad7dd4a`.

## Exact accepted contract
The initial accessible state is |m><m|_B tensor sigma_C, m uniform, with sigma_C identical for both m. B is a qubit. The processor is an input-independent CPTP evolution on its complete accessible systems, possibly with a classical transcript/controller encoded in C. Its prescribed terminal horizon T is fixed. Between local instantaneous operations the generator splits into B-local and C-local Lindblad/CPTP-generator terms plus a bounded information-transmitting term L_int. The induced trace-norm bound J on Hermitian operators holds on the entire accessible B tensor C system, including any ancillas used in the process. For a uniform complete statement, impose the corresponding bound after arbitrary auxiliary reference extension.

All information flow from B into another system, including a detector outcome, feedback transcript, or output report, must obey this finite ingress bound. Local operations confined to B or C may be arbitrarily fast; an instantaneous cross-interface instrument is not admitted. The reset reservoir is permanently unavailable. The decoder receives no separate m-dependent reference or side channel.

These points are the mathematical reading of the source's finite ingress condition. Its phrase “arbitrary ... intermediate operations” must not be detached from that condition.

## Derivation audit
Let Delta_BC(t)=rho_0^0(t)-rho_1^0(t) under the intended no-replacement evolution. It remains Hermitian and has norm at most2 by CPTP trace-distance contraction. Partial tracing gives

 d Delta_C/dt = L_C(t) Delta_C + Tr_B L_int(t) Delta_BC,

because a trace-preserving B-local generator disappears under Tr_B. With Delta_C(0)=0 and the CPTP C-only propagator U_C(t,s), variation of constants yields

 Delta_C(t)=integral_0^t U_C(t,s) Tr_B L_int(s) Delta_BC(s) ds.

Both maps outside L_int contract the Hermitian trace norm. Therefore ||Delta_C(t)||_1/2<=Jt. No assumption of classical evolution or factorization at positive time enters.

For the replacement generator lambda(R-I), R(rho)=I_B/2 tensor Tr_B rho, its exact Poisson expansion has a state-independent first-event density lambda exp(-lambda s). The no-event normalized state evolves by the intended CPTP process. The first event leaves accessible trace distance at most min(1,Js). Subsequent dynamics cannot increase this distance. A decoder supplied with the first-event time has the same uniform prior on m, because the clock is independent of m. Helstrom discrimination then gives conditional error at least (1-Js)/2 for Js<=1. Integrating over 0<=s<=tau and discarding the nonnegative remaining error proves equation(1).

For tau=min(T,1/(2J)), the integrand factor 1-Js is at least1/2. Equation(2), [1-exp(-lambda tau)]/4, follows. The J=0 case follows directly with factor1/2 instead of1/4. The weak-rate order lambda/J is correctly stated only for T>=1/(2J); no positive T-independent floor is asserted for T approaching zero.

The norm convention is conservative and valid: a Hamiltonian commutator has induced/completely bounded trace norm at most2||H||; R-I has diamond norm at most2, so rate lambda=eta/2 fits a budget eta. These are sufficient upper bounds, not claims of exact norms.

## Feedback, stopping, and purported counterexamples
Adaptive operations cause no problem if their full retained transcript/controller belongs to C and their instruments are represented by input-independent channels. A measurement of B that instantaneously deposits m in C is an unbounded ingress operation and violates the premise, even if described as “only measurement” or “classical feedback.” The same applies to an instantaneous noiseless external report of m. An adaptive output time must be modeled inside a common fixed horizon with the timing/output transcript included; the frozen proof does not establish a separate random-stopping-time inequality by substituting a random T.

Access to the reset environment invalidates the loss step, because the erased distinction may reside there. Initially m-dependent DATA also invalidates Delta_C(0)=0. Coherent or correlated quantum-source ensembles require their own conditional distinguishability analysis. These are correctly excluded by the source rather than silently solved.

## Executable supplemental check
`check_ingress.py` considers a genuine continuous-time classical subcase: B is copied into C by a Poisson CPTP copy channel of rate g while B undergoes the stated replacement channel. It computes the exact four-state Markov semigroup and optimal final accessible discrimination error for 36 choices of rates and time. With J=2g, every case obeys the root bound. It also verifies the stronger model-specific first-event bound lambda[1-exp(-(lambda+g)T)]/[2(lambda+g)].

A separate exact matrix check shows that an instantaneous copy into an isolated reliable C before reset preserves distinguishability1. This is a counterexample to dropping the bounded-ingress premise, not to the theorem. Numerical checks supplement the analytic proof and are not a general proof.

## Conclusion
Accepted: the specific raw-bit product-input architecture has a worst-case local-noise acquisition floor independent of subsequent memory size when incident transmission speed stays bounded and retention lasts at least order1/J. This does not preclude a downstream error-correcting source tolerating a fixed sparse acquisition floor, establish a multirecord local-stochastic lower bound, or prohibit reliable fault-tolerant computation supplied with redundant inputs.
