# Independent review: correlated-block sampling and fixed-code distillation

28 October2026. **Accepted at the exact finite-combinatorial and ideal-local-operation mathematical scope below, with OPERATIONAL_CLARIFICATION_v2.md load-bearing.** This is a conventional entanglement-distillation construction, not a new principle, noisy25-qubit implementation, acquired experiment or guaranteed-yield service. Author sources remain unchanged.

## Quantum-to-classical reduction

Independent bilateral Pauli averaging on each isolated pair is Bell-basis pinching: the four commuting bilateral conjugations have four distinct Bell characters. Tensor products pinch all N pair labels while retaining arbitrary positive subnormalized environment operators. No iid property or finite environment dimension is used. A one-pair explicit environment-qubit numerical check gives entry discrepancy1.39e−16; the general statement follows from the character/projector identity, not the numerical fixture.

A nonidentity Bell state disagrees with the Phi+ parity on exactly two of three independently chosen Pauli axes. The expected ideal Y/Y parity is negative, which the program and formula correctly account for. Keys are genuinely retired. The claimed diagonalization is NOT a statement conditional on a retained twirl key. The pairs must be isolated before private random selection; later arbitrary unmodeled source interaction is excluded.

## Exact tail and success interpretation

The reviewer conditions first on retained error count k, rather than using the author's sampled count h. For total weight w, the probability of k retained errors is C(n,k)C(m,w−k)/C(n+m,w). Multiplying by the binomial zero-or-few-failure tail and summing k>t gives the same expression. All w are exhaustively maximized with rational arithmetic. Three small instances are additionally checked by enumerating every binary error pattern and every sample subset.

For n25,m100,t4,c0, the exact maximum is97106/217474455, attained uniquely at total weight7. Every saved tail row for m25,50,100,200,500 and the stated iid-only diagnostic are independently reproduced. No quantum source samples are generated in these checks.

The accepted bad-label mass, not conditional decoding error, is bounded. For example, at total weight7 the acceptance probability is241136689/52846292565≈.00456298; the conditional bad-label fraction is23596758/241136689≈.0978564. Thus replacing the success-weighted .0004465 number by a conditional guarantee would be a substantial error. Some high-weight labels are actually correctable, so the bad-label bound need not be tight for the output error.

For each good label, the logical Bell pair factors from the environment and all public records. For bad accepted mass b, comparing its joint state with Phi+ tensored with its own environment marginal costs at most b in half trace norm. This proves equation(2), interpreting omega_acc as the JOINT output/environment state as clarified in v2. Subsequent teleportation is a CPTP contraction. Conditional bounds divide by actual acceptance; no arbitrary-source positive yield or finite repeat-until-success cost is established. A whole-protocol operational error nu can be added against the specified ideal reference, but replacing its success/reference marginal by the actual one can require a further comparison term.

## Explicit global decoder rather than a recursive substitute

The concatenated stabilizer has20 inner generators and4 lifted outer generators. Independence follows from inner-block independence and the induced outer logical action. Base-code exhaustive Pauli enumeration gives distance3. Every nontrivial concatenated normalizer requires at least3 nontrivial outer logical blocks, each of weight at least3, so distance is at least9; lifting weight3 logical representatives attains9.

The reviewer's executable check actually constructs a first-match minimum-weight syndrome table across all1,089,526 weight0–4 Pauli candidates. It contains627,841 distinct24-bit syndromes. For all461,685 collisions, candidate differences have the same logical commutation class and hence lie in the stabilizer. Actual correction representatives are stored during construction, not merely asserted. Their sorted syndrome/correction table has SHA2569643ab63edfe2b3cc44129e3d93b3e5188cfa453d4af4fac15185d3cb12df328. The reproducible program reconstructs this table; it need not be serialized as a large artifact. The computation explicitly pays the enumeration, dictionary and matching costs. Missing syndromes receive identity, so it defines a total decoder.

A recursive inner/outer minimum-weight decoder is not substituted. Such a different decoder can fail on four errors, and does not inherit this result merely from code distance.

## Bilateral operation and physical limits

Let V encode the code, let T_a map the standard code into syndrome sector a, and define C_a=V†T_a†. For Bell input with Pauli error E, A's conjugate syndrome measurement and B's measurement reveal syndrome difference s(E). Correct B with E_s†. For each correctable label, E_s†E is a stabilizer up to phase and therefore acts as a scalar within every syndrome sector. Apply C_a* on A and C_a on B after correction: each branch outputs the same logical Bell state. This supplies the ideal operation for the25-qubit code. Complex Clifford synthesis on A must be conjugated, not blindly copied from B; the author's separate v2 clarification is necessary.

The author's independent base-five-code256-branch matrix program was rerun in an isolated temporary directory and reproduces its saved output exactly. It is a sanity check of the ideal bilateral operation, not an implementation of the25-qubit circuit. The stated160 check interactions per side follow from20 weight4 and4 weight20 checks. Encoding/decoding, routing, quantum storage, actual test randomness, two-sided classical communication, measurement/feedback errors and final teleportation remain additional resources. They are not furnished by the existing single-site controller simulation or by the combinatorial bound.

Known scientific provenance is properly acknowledged: Bennett et al., *Mixed State Entanglement and Quantum Error Correction*, quant-ph/9604024v2, primary metadata checked at https://arxiv.org/abs/quant-ph/9604024 . The present acceptance rests on the explicit projector/Pauli argument and executed checks above, not on an unexamined noisy-hardware or optimal-distillation theorem. The Pfister capacity theorem is only a comparator, not imported into the certificate.
