# Actual destructive CSS measurement into a protected internal register
2026-10-30. Construction candidate; not an independent receipt.

## 1. Scope and resources
This construction consumes a native Tanner bank at a fixed, externally scheduled safe cut and produces its entire logical computational-basis outcome in the ordinary concatenated FT processor. There is no noiseless detector and no physical final decode. Native generators are switched OFF during capture; the consumed bank is not returned to service. Bounded joint finite CP-divisible cavity noise, finite reset primitives, the exact polynomial-qudit computation code, scheduled gates/connectivity and arbitrary-input totalizing correction are precisely those in the reviewed ordinary FT/factory interface. No extension to an infinite bath is implicit.

At the safe cut assume the already-earned positive logical-independent native error module, up to complete error epsilon_in, with canonical CSS weight r<=eN/h and BUSY count <=bN. The actual forest adds arbitrary operators on at most f b N DATA sites. Thus the bare physical DATA lies in the common operator span of Pauli errors of ordinary support at most

    t_in <= (e/h+f b)N.                                 (1)

Using 2f b instead is conservative if tracking sum-of-sector weights. This is an operator-span statement including arbitrary apparatus/reference coefficients, not a Pauli mixture. The full-Hilbert forest and actual busy support, not a fictitious ready reset, justify it. Require strict margins below the code's classical GPT receiving radius and quantum KL radius. The safe cut is fixed/exogenous, never selected by an unproved stopping rule.

## 2. The actual capture and bottom-up encoder
For each DATA site separately: perform finite reset of a record qubit, CNOT DATA->record, then consume DATA (trace it as an output system). A Z-basis measurement needs no basis change. For X-basis use H on DATA first and exchange the CSS sectors. Every reset, H, CNOT and idle is included in one constant-size coordinate capture module. The physical apparatus and discarded DATA remain in the retained environment if needed; no fresh bath is asserted. Subsequent couplings to records are still included in the incident noise budget.

Do NOT expose each record for the polynomial duration of global classical computation. Immediately, in parallel across all N coordinates, grow it to a k-level block:

* Stage 1: exact coherent base-code encoder on the raw embedded qubit and finite-reset ancillas, including the fixed qubit-to-qudit embedding. Count ANY faulty elementary location as a bad stage.
* Stage j>=2: refresh/totalize the incoming (j-1)-level block, prepare the fixed number of encoded zero ancillary symbols using ordinary (j-1)-level preparation modules, and execute the exact fixed base encoder with (j-1)-level rectangles. Include refresh, ancilla preparation, routing and padded input identities. These preparations may be synchronized before capture or executed while input identities protect the existing block; their complete schedule must occupy at most B child rectangles per stage for a fixed B. A stage is good only if ALL its child rectangles are good.
* Perform a top-level totalizing refresh before using the completed records. Its bad rectangles are charged to the global protected computation.

This is the upward counterpart of the accepted actual top-down decoder, but is not inferred by time reversal of a noisy/reset channel. It is a separately specified forward circuit. Exact polynomial-qudit encoder matrices and finite arithmetic are inherited from POLYNOMIAL_QUDIT_TO_TANNER_QUBIT.md; no per-level synthesis residue k delta is ignored.

Induction using the common-decoder and totalization properties: an all-good tower implements the coherent encoding isometry of its unknown input, into the admitted hierarchical sparse module. If a tower is bad, its arbitrary malformed output becomes an arbitrary encoded logical symbol after the top refresh; it may be correlated with every other bad coordinate/environment. Good towers still have the correct logical input. This is a statement about the entire two-sided operator span. A bad tower is not assigned a stochastic classical flip.

The raw ingress is NOT arbitrarily reliable. Let x_j be the reviewed rectangle strengths, x_j<=x_* (x_0/x_*)^(s^j), s>=2. Prefix-free physical supports of distinct stages/towers and the exact OR sieve imply, jointly for every set S of coordinates,

 ||sum_(histories bad on every coordinate in S) E_F||_diamond <= p^|S|,
 p <= exp[(B_cap+B) x_0/(1-x_0/x_*)]-1 = O(x_0).         (2)

Here capture and the physical qubit/qudit embedding are included in B_cap; all levels occupy disjoint spacetime circuit modules. This bound is uniform in k. Shared-bath independence is unnecessary. This fixed small floor is fully consistent with the bounded raw-ingress lower bound. The OUTER Tanner code, not the single raw bit, removes its macroscopic effect.

## 3. Explicit efficient corrected-word function
Write the CSS code as |z_L>=|C_X|^(-1/2) sum_(c in C_X)|a_z+c>, with C_X subset K=ker H_Z and K/C_X indexing logical Z labels. Choose a fixed binary linear label map ell:K->F_2^Klogical whose kernel is C_X (offline Gaussian elimination). The codeword sectors have exact H_Z word=0.

On arbitrary N-bit record y, compute H_Z y. Run the actual bounded-footprint orbit-minimizing local GPT tables on this stored syndrome, accumulating each accepted X-mask f. A fixed padded scan circuit is sufficient: O(N) complete scans of O(N) hubs, because U<=C_U N, every accepted move decreases integer U by at least one, and a nonterminal full scan must accept a move. Store all workspace reversibly; compute local tables by finite Toffoli/arithmetic circuits. Conditional halted steps act as identity. Cost is polynomial in N (conservatively O(N^2) local table steps plus polynomial routing and reversible storage), not a global minimum-weight search. The queue version is faster on a RAM but is NOT assumed to give a local constant-depth circuit.

On the common safe-error span the accepted GPT confinement/active-density theorem gives termination at U=0 and correction modulo C_X. The radius here must be the separately reviewed GPT decoding radius, with strict margin, not merely half the quantum distance. For words outside the safe set define the output by the same fixed padded circuit, with any fixed extension of ell; no partial algorithm is left undefined.

Set g(y)=ell(y+f(y)). For every w=a_z+c and every admitted input flip mask u,

    g(w+u)=z.                                           (3)

The syndrome evolution depends only on H_Zu, not w or z. This is the important code-zero-sector advantage: there is no unknown dense baseline. Execute this COMPLETE Boolean/reversible circuit on the encoded records using ordinary FT, including extraction of all Klogical output bits and their encoded dephasing (copy each logical output to a protected garbage register and discard it). Discard raw records and all work at the endpoint. Keeping only corrected labels but leaking raw records to an accessible consumer would be a DIFFERENT instrument.

## 4. Complete instrument, not just label correctness
Let V be the original CSS encoding isometry and C be the coordinate-local capture dilation |y>_D -> |y>_D |y>_R, with intended discarded DATA and ancillas included in garbage. Consider any two admitted coefficient histories E_a,E_b: native input Pauli errors, capture faults and arbitrary operators on bad record coordinates. Their combined support is at most t_in+t_rec coordinates on each side. Coordinate-local isometries preserve the original code KL condition: C† E_a† E_b C acts only on the union of their original coordinate supports. For 2(t_in+t_rec)<d,

    V† C† E_a† E_b C V = c_ab I_L.                     (4)

This does NOT claim all errors can be pushed through C as DATA-only operators. They need not; the local-isometry KL argument suffices.

Let P_z be the projector on record words with g(y)=z, and Pi_z the logical computational-basis projector. Equation (3), including arbitrary record operators (expand on computational matrix units), proves the common intertwining identity

    P_z E_a C V = E_a C V Pi_z.                         (5)

For native Z errors this includes their phases; errors on discarded DATA are retained in E_a. Logical g is computed reversibly and its output deliberately dephased, so off-diagonal output z,z' terms vanish. Combining (4),(5),

 V† C† E_b† P_z E_a C V = c_ba Pi_z.                  (6)

After tracing consumed bank/garbage, each coefficient map therefore implements the SAME ideal destructive logical instrument

    M_Z(rho_LR)=sum_z |z><z|_out tensor Tr_L[(Pi_z tensor I_R)rho_LR]

times its auxiliary coefficient. Equation (6) is exactly the reference-uniform statement; merely having the right classical label was insufficient. Arbitrary two-sided bath coefficients and coherent native syndrome superpositions are included by linearity. No virtual fault flag is measured. The output |z> here is the logical value of a physical protected block, not an exposed perfect register. Residual hierarchical correctable errors remain and are handled by the ordinary common decoder chart / subsequent good FT rectangles.

For a subset of logical bits, measure the whole CSS logical basis then discard unwanted bits ONLY if that finer measurement is desired: this destroys unmeasured logical coherences. The claimed primitive is explicitly whole-bank destructive logical Z (or X), not a nondestructive selected observable.

## 5. Exact signed counting and normalization
Let t_rec=theta N, K_bad=floor(theta N)+1, with t_in+theta N inside the GPT safe radius and 2(t_in+theta N)<d. The full-circuit exact cardinality sieve gives

 b_rec <= binom(N,K_bad) p^K_bad (1+p)^(N-K_bad).         (7)

Choose fixed x_0 small enough for b_rec=exp(-Omega(N)). Let b_comp=(1+x_k)^L-1 for the entire protected corrected-word circuit, including final totalizing refresh, encoded dephasing and all work/idles. The record predicates and protected computation rectangles are physically disjoint. Their full-circuit joint sieve yields

 b <= b_comp+(1+b_comp)b_rec.                            (8)

On the complement the common logical instrument is M_Z tensor signed auxiliary K. The actual decoded reduced output is CPTP, so exactly the existing trace-defect argument gives

 ||actual protected logical instrument - M_Z||_diamond
       <= epsilon_in+2b.                               (9)

The output chart is an analysis tool for specifying an operational protected-register interface, not an ideal detector being inserted. Every later ordinary FT consumer receives its hierarchical sparse module. Complete output-state claims without this chart require comparing to a noisy encoded-output module, not to a perfectly encoded physical density operator.

## 6. Bell measurement and resources
For two code-identical banks, actual transversal CNOT A->B followed by physical H on A, then the above Z capture on both, implements whole-bank logical Bell measurement: Z labels on A after H are XX outcomes; Z labels on B are ZZ outcomes, with a fixed convention. Use the accepted matching pulse prefix bound or directly absorb the constant-depth CNOT/H/capture module into enlarged paired-coordinate record groups. A fault on a paired group may spoil a coordinate in EACH bank. Count groups jointly and require each bank's enlarged initial radius plus new group budget inside its decoder margin. Do not multiply bank failure probabilities. Equations (4)-(6) apply to the product code and joint Bell projectors; or conjugate by ideal transversal CNOT/H and reuse the two commuting CSS measurement instruments. No physical logical H gate native preservation is required: H is part of a terminal destructive readout, with sector checks transformed accordingly.

For L=poly(N) ideal Boolean gates and target b_comp=exp(-cN), k=O(log N), tower size/time bounded by ordinary A^k,D_g^k, and total work/storage/time polynomial in N, potentially enormous. The native DATA is needed only during the constant-depth terminal capture, not during the polynomial classical latency. Existing unconsumed native banks, if any, require their own memory survival during that latency; that cost must be added by a receiver. No result here establishes geometry-restricted routing, autonomy, a final classical detector, practical latency, or advantage over ordinary scheduled FT. The strongest comparator is ordinary concatenated FT doing exactly the same encoded Bell measurement and classical processing; our contribution is only a candidate earned interface out of the live native memory.
