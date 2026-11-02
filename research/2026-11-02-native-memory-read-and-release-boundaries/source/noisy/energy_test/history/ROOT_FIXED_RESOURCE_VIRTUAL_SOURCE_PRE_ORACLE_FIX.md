# Root refinement: arbitrary small common noise with fixed gaps and fixed gate arity

1 November2026. Proposed strengthening of the driven-reference-charge attack. Not a static-autonomous or native-two-body claim.

## Common-rate noise creates a temperature gradient
Fix beta>0, a gap Delta>0, and independent X-flip probability p in (0,1/2). An onsite Gibbs qubit of gap E has post-noise excitation probability
 r_E=p+(1-2p)/(1+exp(beta E)).
Define beta_eff(E)=log[(1-r_E)/r_E]/E. Put a=1-2p, x=beta E/2. Then
 beta_eff(E)=beta artanh(a tanh x)/x.
The derivative of f(x)=artanh(a tanh x) is
 f'(x)=a/[1+(1-a²)sinh²x],
strictly decreasing for x>0. Hence f(x)/x strictly decreases. In particular, with fixed hot gap2Delta and cold gapDelta,
 0<beta_h:=beta_eff(2Delta)<beta_c:=beta_eff(Delta).
No gap parameter needs to grow as p decreases.

Choose an integer m>beta_c/[2(beta_c-beta_h)], fixed with respect to memory size n. Consider m hot spins and2m-1 cold spins, plus one battery spin of gapDelta. The two configurations
 A=(all hot1, all cold0, battery0),
 B=(all hot0, all cold1, battery1)
have the same total charge2mDelta. Their bath-supplied forward/backward probabilities obey
 log(u/d)=2mDelta(beta_c-beta_h)-beta_cDelta>0.
Thus this composite virtual transition pumps the battery upward. m and its rate can be extremely unfavorable as p→0, but remain n-independent constants for each fixed nonzero p.

## No unpriced many-body primitive
The 3m-spin transposition A↔B is NOT assumed as a native gate. Give O(m) zero-energy scratch/flag qubits a specified clean computational-basis pattern on an explicitly counted thermal branch of probability2^-O(m). Compute the predicate 'configuration is A or B' reversibly into a flag using bounded-body controlled gates whose targets have zero reference energy. Controls are diagonal projectors in resource/battery energy bases, so every such gate commutes with K. Negative controls are projectors, not energy-changing pre-flips.

With the flag held, perform m conditional resonant triplet exchanges:
 |1_hot,00_low> ↔ |0_hot,11_low>.
Each hot spin has gap2Delta, each low spin gapDelta, and the last low pair contains the battery spin. Every exchange has fixed body order (four including the control flag), independent of m and p. On A/B these swaps transform one pattern into the other. On every other configuration the flag is zero and they do nothing. The union predicate is unchanged at the endpoint, so reverse its computation to restore all scratch exactly. The resulting full circuit realizes the desired transposition with no measurement or entropy erasure. Its duration/gate count depends polynomially on m and is constant in n.

For a unary battery edge, include the constant-size domain-wall guard in the predicate. Scratch remains O(m); ordinary zero-energy Toffoli/controlled gates have fixed arity. The whole construction acts unitarily and K-conservingly on ALL states, not only the selected clean branch. The clean branch is used solely to lower-bound performance probability.

## Integration with the logarithmic buffer
Use the separate constructive attack's O(log n) unary buffer, middle-peaked target law, fresh initial bath bank and flagged energy-resolved code-Pauli steps. Lower edges use the virtual pump; upper edges use ordinary low-gap thermal contacts, whose post-noise excitation probability is below1/2. Alternating forward/backward sweeps yield a c^O(L) minorization when only O(L) active wall-edge choices are counted; a c^O(L²) proof would be insufficient and must not be substituted.

All bath resource gaps are in {0,Delta,2Delta}. The maximum gate/body size is fixed by local code energy resolution and the constant controlled exchanges, not by m. The O(m) scratch plus O(log n) unary initial branch has probability c(p)n^-c', while refill time and total fresh-resource count are polynomial in n with potentially enormous p-dependent degrees/constants.

Equal-gap nearest-neighbor SWAPs route resource/workspace states; no memory data need move and no large-range selector is granted. No fresh pure ancillas, external work battery or reset source enters after initialization. Control timing is externally prescribed and charged; every actual control term commutes with K. This is therefore an explicitly DRIVEN model, not a construction of an autonomous clock.

The cleanest logical counterexample puts no noise on the memory and common noise on all resource species. A uniform-all-carriers variant additionally needs the short-time forward-Pauli logical-protection bound for the actual code. Do not silently identify these scopes.

## Consequence to test
For every fixed p>0, the above uses the SAME bounded gap set and native bath-gate arity. Only the amount of bath resource and circuit length change. If the buffer/path/locality join passes, a uniform long-lifetime claim for all polynomial-volume baths and all K-conserving driven controls cannot follow from small per-spin preparation noise alone. This does not refute the stationary-reference theorem, static-H memory theorem, or a restricted benign controller/noise model.
