# Acquire coherent sector control and preserve an unknown seed during word upload

24 October2026(local),w64. NEW independent candidate proof. It is not covered by any earlier manifest/review. All native full-circuit diagnostics, primary special-case comparison and fresh full criticism remain PENDING. Generic coherent measurement/uncomputation is prior; no broad control/learning novelty, hardware or mission claim.

## CS1. Model, promises and the actual remaining interface

The physical device remains V=alpha U+i beta I on seed qubit tensor binary Fock bath, U=U*=U^-1, alpha=sqrt(1-beta^2), and now FIX0<beta<1 known with certified numerical access. Let X_s flip the seed on EVERY word, P_+,P_- its spectral projectors. Every native and local operation commutes with this physical X_s. Quantum backward qutrit returns, arbitrary finite LOCAL quantum circuits and the previously proved GLOBAL positive-power approximation to V* are permitted and counted. Physical controlled V, direct bath access and a supplied sector oracle are absent.

Unlike the earlier uploader, the seed-X sector is NOT known or measured. The seed may be in any superposition, entangled with an inaccessible external reference, or jointly entangled with the unknown word source. The word part of the physical bath initially is the empty word. The input word register F has depth<=H. The target transfers F into the physical word part while preserving the complete seed/reference state, empties F, and returns every coherent control ancilla to its initial state. It does not change or prepare an arbitrary chosen seed distribution.

The construction first acquires an approximate coherent XOR of X_s on a lab label, then uses the label to control the LOCAL opposite-download simulation, and finally UNCOMPUTES that label on the uploaded depth-H state. Uncomputing is essential: discarding a sector label would dephase the unknown seed/purifier and would not meet the target.

## CS2. A fixed coherent classifier circuit with a uniform finite-depth guarantee

For an oracle on bath input words of depth<=H, define a fixed physical unitary circuit C using fresh locally prepared ports. Keep EVERY output coherent and return it quantum backward to Alice for later reversal. There is no measurement or adaptive stopping.

First send s0 vacuum ports. For each of r blocks, send the KNOWN two-port program10, then s vacuum reset ports. All these inputs may be prepared at the start; their local preparation is included in C. Write

    a=1-beta^2, b=beta^2,
    m_beta=2 a^(3/2) beta>0,
    tau0=Pr[Bin(s0,a)<H].

The root two-call identity is the already corrected native formula

    [a|01>+(-b+i alpha beta x)|10>] tensor |root,x>
        +i alpha beta |00> tensor |1,x>.

On its first two output ports use the CORRECT observable

    Y=i(|10><01|-|01><10|),  E_x[Y]=x m_beta.

Y has eigenvalues+1,-1,0. This sign convention is the corrected38995... source, not the erroneous literal sign in older28008... . A block starting at sector root has bath depth<=1 after the probe; s vacuum calls then leave nonroot probability at most b^s.

For analysis ONLY, insert an exact root replacement channel in a fixed sector after the initial drain and after each coherent reset. A state with nonroot weight p in a one-dimensional sector root is within UNHALVED JOINT norm4sqrt(p) of root tensor its actual remaining-register marginal. Thus the total joint error between the actual circuit's hypothetical Y-outcome distribution and the ideal independent-root experiment is at most

    4sqrt(tau0)+4r b^(s/2).

In the ideal experiment the r bounded Y samples are iid with mean x m_beta. Classify by the sign of their sum, with any fixed tie convention. Hoeffding bounds the wrong-sector probability by exp(-r m_beta^2/2). Therefore the ACTUAL coherent classifier has wrong-label probability at most

    eta = exp(-r m_beta^2/2)
                +4sqrt(tau0)+4r b^(s/2),           (CS1)

UNIFORMLY over every depth<=H input and arbitrary reference, conditional on either sector. Analysis root replacements are not executed and do not destroy actual seed coherence.

Given0<eta_target<1, sufficient finite choices are

    r>= (2/m_beta^2)ln(3/eta_target),
    tau0<=eta_target^2/144,
    b^s<=eta_target^2/(144r^2).

Use the earlier binomial bound to choose s0>=max[2H/a,(8/a)ln(144/eta_target^2)], or omit s0 for an exact root input if desired. Integer ceilings are understood with numerical guards. The total ACTUAL forward calls in C are

    L=s0+r(2+s)=O_beta[H+ln^2(1/eta_target)+1].      (CS2)

This bound may be extremely expensive in beta and is not uniform near0 or1. All L outputs are stored, not thrown away. The classifier will be a local reversible circuit, not an actual classical observation.

## CS3. Coherent majority and complete uncomputation

Let L_lab be a target label qubit with an ARBITRARY initial state, possibly entangled with references. In Alice's returned probe ports, locally rotate each Y eigenbasis to a computational basis; reversibly add its+1/-1/0 value, compute the sign, XOR that sign-bit into L_lab, and uncompute the sum and eigenbasis rotations. Denote this unitary B. It is self-adjoint and acts only on lab ports/label. It can be compiled in O(r log(r+1)) reversible arithmetic gates plus O(r) fixed two-port rotations and O(log(r+1)) arithmetic ancillas; no dense classifier-state oracle is supplied.

The desired ideal XOR is

    Q_X=P_+ tensor I_(L_lab)+P_- tensor X_(L_lab),

with bit0 assigned to sector+, bit1 to sector-. Q_X commutes with C. For a fixed sector, B differs from Q_X only on the classifier's wrong-label subspace, of probability<=eta. Since the label can be arbitrary, use ||X-I||<=2 rather than a successful-label-only amplitude. Thus

    ||(B-Q_X) C(|psi> tensor |0>_anc)||<=2sqrt(eta).

Applying the mathematical C* gives

    ||(C*BC-Q_X)(|psi> tensor |0>_anc)||<=2sqrt(eta). (CS3)

This operator bound extends to superpositions of both sectors because actual and target operators preserve the orthogonal X_s sectors; it also tensors with arbitrary references. The ideal Q_X acts only on bath/label, so C* has returned ALL probe/reset/input-preparation ancillas to their initial vacua. This is coherent nondemolition control, not a measurement of the seed or copying an arbitrary unknown qubit.

## CS4. The physical inverse is ACQUIRED globally, not assumed

C* contains L native V* calls in reverse port order, plus known inverse local input preparations. For each native inverse use the GLOBAL involution recurrence:

    V^(2q)=e^(2iqtheta)Pi_+ +e^(-2iqtheta)Pi_-,
    theta=arcsin beta,
    ||V^(2q-1)-V*||<=delta_inv,
    q=O(1/delta_inv).

Pi_+,Pi_- here are the FULL U spectral projectors, NOT the seed-X projectors. The approximation holds on BOTH seed sectors with one common operator-phase convention and arbitrary bath/reference states. It is the already frozen c544.../75c... positive-forward-power construction, including full-eigenphase selection and certified finite precision. It needs no known x or physical controlled V. Each repeated query acts on the same qutrit, returned coherently after every actual call.

Product telescoping makes the implemented inverse of C differ by at most L delta_inv. If the whole local B/preparation compilation has operator error e_B, the physically acquired oracle isometry obeys

    oracle operator error <=2sqrt(eta)+L delta_inv+e_B. (CS4)

To make it<=zeta take eta_target=zeta^2/36, delta_inv=zeta/(3L), e_B<=zeta/3. This needs

    O_beta[(H+ln^2(1/zeta)+1)^2/zeta]              (CS5)

ACTUAL forward queries and the same order of coherent quantum qutrit returns, plus O(L) stored ports and reversible local computation. Unhalved diamond error is at most2zeta on the promised bath-depth domain, for arbitrary label/reference input. Every coherent wrong-label/reset amplitude remains present; no abort or postselection branch is deleted.

Using the known-sector exact composite inverse without knowing x would be invalid. A temporary guessed label cannot simply be discarded after using it. The GLOBAL recurrence is deliberately retained here as a safe complete uncomputation mechanism. This is a valid cost even if a more efficient clean construction later exists.

## CS5. Seed-preserving unknown-word uploader

The actual initial physical word is root, but its seed is arbitrary/unknown and may be entangled with all references. Label L_lab starts0. Execute:

1. The acquired XOR oracle with depth promise0, copying sector x COHERENTLY to L_lab, with all its own ancillas returned approximately vacuum.
2. The LOCAL opposite-download simulator on F and its T vacuum ports, controlled on L_lab. Its root sign is x in the matching label branch. Every such local operation is an ordinary known controlled circuit on laboratory registers. Then send the prepared ports once each through actual native V in reverse order, as in the controlling2007 uploader.
3. A fresh copy of the acquired XOR oracle with depth promise H, acting on the SAME L_lab. On the ideal uploaded state it XORs x again and returns L_lab to0, preserving the word and original seed/reference coherence. Keep or discard only ancillas that have been coherently reset, with all finite errors retained.

Conditional on each x, the exact upload has S_x*J_x=A_x*A_x>=1-tau, tau=Pr[Bin(T,a)<H]. Crucially this effect is the SAME real depth-diagonal operator for both sectors. There is no independently fitted sector global phase. Hence the controlled upload has operator error<=sqrt(2tau) on arbitrary superpositions of sectors and all source/reference entanglement.

Let each oracle's operator allowance be zeta, and let the additional controlled LOCAL upload compilation have error e_loc. Isometric/trace-norm telescoping gives total operator error<=2zeta+sqrt(2tau)+e_loc. The full target transfers F into the physical word factor, empties F and every port/ancilla, returns L_lab to0, and acts as IDENTITY on the original seed factor and its inaccessible purifier. Its UNHALVED diamond error is at most

    4zeta+2sqrt(2tau)+2e_loc+epsilon_init,           (CS6)

where epsilon_init is any UNHALVED JOINT initial word-root product error. Choose zeta<=epsilon/16, tau<=epsilon^2/128, e_loc<=epsilon/8 and epsilon_init<=epsilon/4 to achieve epsilon. The leading physical forward/quantum-return count is

    O_beta[(H+ln^2(1/epsilon)+1)^2/epsilon],         (CS7)

plus the T=O_beta(H+ln(1/epsilon)) single-pass upload calls and local target/source costs. The second oracle is needed on depth H; assuming it worked only at root would be a fatal gap.

The hybrid proof applies oracle bounds at IDEAL intermediate depth-H states; actual small error components need not stay within that promise. Subsequent operations are CPTP/unitary and cannot amplify their trace-norm error. First-oracle residual ancillas are part of the reference when applying later bounds. Fresh ancillas are used for the second oracle.

There is no seed-state preparation: its unknown distribution/coherence is PRESERVED. Nor does this restore an arbitrary overwritten old word state. This is a complete unknown-seed WORD factory at fixed interior beta, not universal preparation of any chosen entire bath initializer.

## CS6. An exact beta0 obstruction shows the premise matters

At beta0, on the two fixed seed sectors the unchanged native gate satisfies

    U_-=-P U_+ P,  P=(-1)^word-depth.

Every laboratory operation, preshare and backward wire commutes with the inaccessible P. For any common fixed-N protocol starting at WORD ROOT with all lab inputs independent of the unknown seed, the two sector-conditioned final word/lab states therefore obey

    Omega_-=(P tensor I_lab)Omega_+(P tensor I_lab).

The scalar(-1)^N cancels in the density operator. The same relation holds separately on classical histories if a bounded adaptive protocol stops at differing classical call counts; no coherent query-skipping carrier is assumed. Tracing the final bath makes ALL lab output/measurement distributions identical between sectors. Thus no lab classifier from root can distinguish x at beta0; the coherent oracle above correctly loses its positive gap m_beta there.

For a decisive word-output target choose |psi>=(|empty>+|1>)/sqrt2. Its parity conjugate P|psi> is orthogonal. Let omega be the sector+ final word state. The two unhalved errors from the common target sum to at least

    ||omega-psi||_1+||P omega P-psi||_1
      >=||psi-P psi P||_1=2.

Hence some sector has error>=1. Starting from an UNLABELED equal mixture of sectors, the complete seed/word target of preserving that seed while preparing psi has error>=1 as well, even if all lab junk is discarded. The obstruction therefore already excludes one KNOWN across-parity word target; it is not only an unknown-input complexity issue.

This does not forbid beta0 uploads restricted to a SINGLE word-parity subspace. Fixed-length unknown-word push already preserves an unknown seed; suitable same-parity variable-length codes can also avoid the obstruction. It does not apply to initial seed/lab correlations supplying the missing sector information, to a known sector, or to additional forbidden bath controls. It is a precisely scoped native boundary, not a universal quantum no-go claim.

## CS7. Remaining evidence and cost obligations

This proof still needs new literal native oracle/uncompute tests, an adversarial check of the joint root-replacement/statistical-to-operator step, and a fresh independent reading of the full source. Generic reversible coherent classification and measurement uncomputation are established tools. Special native mathematical priority and comparison against the strongest legal controller remain UNKNOWN.

Gate precision, quantum memory/return noise, all physical calls, classifier compilation and seed-independent target preparation must be counted. beta-dependent constants diverge near endpoints. Unknown-beta acquisition can in principle precede this because its completed probes return the FULL old bath/reference state, but that separate proof is not automatically endorsed or integrated here. No physical seed readout or apparatus operation was performed. Physical validation NOT_PERFORMED; practical advantage NOT_ESTABLISHED; scientific-learning mission NOT_ACHIEVED.
