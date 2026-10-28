# Independent proof: known-code label lift with retained coordinate ancillas

28 October 2026. This is a separate review of the general known-linear-code construction. It does not infer a known code, nonlinear transversal, reversible decoder circuit or pre-noise port from a logical black box. Those are explicitly supplied, paid interfaces. The unknown quantity acquired is their fixed physical output realization behind V.

## 1. Known-code translation and actual ordinary moments

For any full-rank C and complete transversal, the decomposition x=C l(x) XOR e_(g(x)) is unique. Translating x by C a leaves the coset g unchanged and sends l to l XOR a. This is true even when the section g->e_g and l(x) are nonlinear. It is the exact algebraic property required later; no nearest-neighbor, minimum-weight or linear classical decoding rule is assumed.

The setting-0 labels (l,g) enumerate every physical computational string exactly once. Multiplication by its known coordinate sign therefore extracts Z_j/d before noise. A fixed physical X_f multiplies that coordinate Fourier component by (-1)^f_j. Summing the CP memory maps and conjugating by V gives the complete signed operator `C_j/d tensor H_j(omega)`.

For setting i>0, pair each codeword with its translate by c_i, and average the other k−1 ordinary logical computational bits, the sign of the ordinary X_i eigenstate, and all g. Each physical x appears with its unique partner x XOR c_i. The signed average is exactly X_(c_i)/d. Every physical X_f commutes with that translation, so the complete output is `B_Xi/d tensor T(omega)`. Averaging instead without a sign gives I_d/d for EACH setting. These identities hold on every memory matrix unit and hence after arbitrary memory-reference extension.

The actual record's setting weight m is essential: it cancels its setting probability 1/m and its squared-moment cost is m, not one. All labels remain averaged given the COMPLETE PRIOR record, although known present labels multiply the statistic. A map F_f selected by inspecting the current private setting or injection label would invalidate this derivation and is excluded by the stated physical instrument. The channel may nevertheless respond quantum mechanically to its physical input and arbitrarily to allowed past history. Individual readout branches can disturb retained memory.

Under the trusted CP inequalities H_j>=0 and T−H_j>=0, each normalized current memory state has theta_j in [0,1]. Each finite bank's contrast is a fixed reflection times a nonnegative scalar. Thus any certified nonzero stage determines the SAME physical coordinate generator, even if other coordinates become informative later. Logical X gaps are always 1/d. This is an acquisition mechanism under a structural promise, not a finite transcript test of that promise.

## 2. Finite statistics and termination accounting

The single-qubit product-shadow second-moment map is `rho -> rho+2 Tr(rho)I`; its n-fold tensor map is bounded by 3^n I on any n-qubit state. Consequently each of the n+k records has conditional squared moment at most m3^n I and centered increment norm at most `m d+1/d<=2md`. Centered conditional variance is no greater than that squared moment. The received matrix martingale inequality therefore has bank tail at most

    2d exp[-N_s a_s² / (2(m3^n+2md a_s/3))].

Since a_s<=1/(16d), the denominator is at most `2m3^n+m/12<=3m3^n`. With the stated N_s the exponent magnitude is at least (8/3)L. Hence the union over n+k record matrices and S+1 possible banks is at most `2d(n+k)(S+1)2^(-L)<=beta`. The factor 2 is the two spectral tails already included in the matrix bound, not another unpaid set of experiments. Matrix correlations and arbitrary coherent-memory evolution cause no independence requirement.

The finite rational Jacobi residual contributes at most a_s/4 in operator norm. Thus the received sign guard with total perturbation 5a_s/4 certifies every retained target within delta on this ONE event. Every fitted reflection remains exactly physical on other records. Fixed V makes retained certificates permanent; positivity or a spectral gap need not persist after certification. A finite caller-funded cap and abstention before payload are indispensable.

At the first sufficient scale `a_s<=delta gamma/5`, dyadic halving gives `a_s>delta gamma/10` (with the stated loose bound also covering the initial scale). Substitution proves `N_s<800m3^n L/(delta² gamma²)` and the geometric accumulated bill is strictly below 4N_s/3. The largest admissible dyadic delta has `delta²>epsilon/[16k²(4n+1)²]`, giving exactly the stated second bound. Gamma=theta/d explains the exponential 12^n, not a polynomial-width claim. The exact worst-case integer sum is retained. No arbitrary wait for unspecified later information is free.

## 3. The full-ancilla identity closes the lifecycle issue

For any exact physical reflection S, Q_j(S) is a literal involution. Its difference from Q_j(C_j) is `(S−C_j) tensor (I−X_(A_j))/2`, whose norm is exactly ||S−C_j||. The product W_hat is therefore unitary even when its coordinate controls do not commute. Because the phase oracles P_i are known diagonal unitaries, common conjugation gives exact reflections Zhat_i=W_hat†P_iW_hat and makes all the Zhat_i commute. No joint diagonalization or Boolean polynomial of incompatible learned operators has been used.

For the TRUE coordinate reflections, W_* maps `(V|x>,|a>)` to `(V|x>,|a XOR x>)`. Thus the true augmented Z_i acts by the phase `(-1)^(l_i(x XOR a))`. The map

    |l,g,a> -> V|C l XOR e_g XOR a> tensor |a>

is a unitary bijection of the ENTIRE enlarged Hilbert space. Physical translation by c_i changes only l_i, by the uniqueness property in section 1, for every a. This proves all logical Pauli commutations and anticommutations on all coordinate-ancilla states, not merely on an initially clean subspace. With a=0 it is the desired original decoder. The source with clean A appended has this same fixed augmented Pauli/gauge form: each gauge CP block simply acquires the appended |0><0| coordinate-ancilla factor.

This full-space result is load-bearing. Approximate gates can entangle A with physical outputs and earlier receivers. Later blocks still act on those SAME A wires. There is no projection, postselection, reinitialization or replacement of them during the service. Their eventual discard and the originals' discard occur only after the entire multi-logical network. Proving a reflection identity only at a=0, then silently resetting A between blocks, would not justify this construction; the manuscript expressly avoids that error.

The oracle P_i needs no unknown source operation. It is the known reversible permutation x->(l(x),g(x)) on the receiver's A register, a phase on logical output i, and its inverse. It acts coherently on superpositions and uncomputes all work. A supplied truth table also gives a finite permutation circuit, possibly exponentially expensive; no efficient decoder oracle is inferred. Measurements of A or a classical-only evaluation interface would not be a substitute.

## 4. Uniform coherent extraction and resource counts

Unitary telescoping gives ||W_hat−W_*||<=n delta and therefore ||Zhat_i−Z_i*||<=2n delta. The logical-X target has error at most delta, extended by the identity on A. These are full operator bounds independent of the state or occupation of any gauge/ancilla.

The literal three-controlled-reflection block is unitary for any supplied reflections. Relative to its true block it has norm error at most twice the Z error plus the X error. Telescoping ALL k blocks, without commuting or resetting any approximate subsystem, yields eta<=k(4n+1)delta. The true full network swaps each logical factor with its mixed receiver qubit and leaves the augmented gauge intact. Purify that mixed receiver preparation and every gauge/memory state. Its ideal final vector lies entirely in the joint correct Bell subspace. The norm of the actual orthogonal component is at most eta, so its squared probability is at most eta². This proves the uniform complete-reference bound epsilon/4; it is not a generic conversion from Bell error to unframed diamond error.

To implement controlled Zhat_i, apply W_hat unconditionally, controlled P_i, and W_hat†. This sandwich is EXACTLY controlled Zhat_i even when its external receiver control is coherent. It does not require extra receiver controls on each coordinate copy gate. Each of the 2k Z invocations therefore uses 2n coordinate-copy operations, giving 4kn controlled learned coordinate reflections and 8kn Hadamards. The k logical-X invocations cost k additional controlled learned reflections. The two Z-oriented CNOTs per logical SWAP add 4k receiver Hadamards. Each controlled P_i uses decoder, controlled phase, inverse: 4k total decoder/inverse circuit executions and 2k controlled-Z gates. All n coordinate ancillas, k receivers, decoder work and original output wires remain live for their declared durations. These are structured calls; elementary synthesis and routing are separately paid, not hidden inside a claim of scalable width.

The intended original-source decoder is always a specified exact extraction. Its full-CPTP oracle label needs the separate CP dominance F_(e_g)>=F_(C a XOR e_g), which coordinate biases do not imply. The one-service accepted-risk ledger imports the received uniform certificate/record-law comparison. Further adaptive use imports the separate COMPLETE CP-domination theorem with its private frame retirement, discarded gauge and receiver records, common-controller and whole-process implementation requirements. This proof does not relax any of them.

## 5. Independent fixtures and preserved scope

The independent check uses two genuinely nonlinear transversals: repetition [3,1], and [4,2] with columns 1100,0011 and representatives 0000,1000,0010,0110. It tests the full augmented bijection and Pauli relations on every (x,a) basis value, not only a=0. It separately constructs actual ordinary preparation-label averages and verifies complete retained-memory coordinate/X moments with a nontrivial rational entangling mixer and correlated physical-X-pattern instruments. Retained-memory off-diagonal matrix units are included.

A distinct [3,2] multi-logical fixture deliberately perturbs one coordinate reflection so it does NOT commute with another. It constructs all copy gates, their common W_hat, the exact mutually commuting lifted Zhat_i, the full augmented identification, and the complete 3k-gate network with every coordinate ancilla retained. Exact complete-reference tests include both A=0 and a coherent gauge/retained-memory purification whose branches have different nonzero coordinate ancillas. The tests therefore exercise the new lifecycle claim rather than only a clean-subspace identity. Source counts and RNG counts remain zero; these exact fixtures are not an acquisition experiment or a general compiler execution.

The equally informed conventional learner has the same known code/transversal/decoder, actual pre-noise port, retained labels and structural CP promises, and can use this very construction. It learns an unknown physical realization of a SUPPLIED subsystem. Unknown-code discovery, efficient unbounded-width tomography, practical threshold, improved intrinsic code noise and historical priority are not claims of this receipt.
