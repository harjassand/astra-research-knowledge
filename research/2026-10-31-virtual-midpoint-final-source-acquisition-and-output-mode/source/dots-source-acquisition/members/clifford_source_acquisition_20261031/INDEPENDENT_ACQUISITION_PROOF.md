# Raw Clifford source acquisition and a strict-return dichotomy

31 October 2026. Independent derivation checking the root proposal. This is a mathematical finite acquisition specification, not an executed general certificate finder or a novelty claim.

## 1. Exact declared input class

There are n source qubits. An explicit Clifford circuit acts on those qubits and e fresh ancillas in a specified pure stabilizer state, after which specified output wires are discarded and n designated source wires remain. Every gate, ancillary preparation and wire convention is known. The same channel Phi is repeated with fresh ancillas. The input excludes arbitrary probabilistic mixtures, non-Clifford gates, postselection and unrestricted classically adaptive channel descriptions unless they are separately compiled into this exact Clifford Stinespring form.

Let P_v denote the Hermitian n-qubit Pauli with binary label v in GF(2)^(2n). Pullback through the raw Clifford circuit gives

    U†(P_v on retained output tensor I_discard)U
       = epsilon(v) P_(Fv) tensor P_(Ev),

where F,E are binary linear maps and epsilon(v) is an exactly tracked sign with the chosen Hermitian Pauli convention. Let L_E be the binary stabilizer subspace of the input ancillas. Their expectation of P_(Ev) is zero outside L_E and is a known sign inside L_E. Therefore

    Phi†(P_v) = 0                         if v notin S,
    Phi†(P_v) = sign(v) P_(Fv)            if v in S,
    S = {v : Ev belongs to L_E}.

S is a binary linear subspace. The sign can have quadratic convention terms; it must not be assumed linear. This does not affect the survival-domain/image computation. A surviving identity label is a scalar identity, not a deleted observable.

## 2. Finite image iteration is exact

Define M_0=GF(2)^(2n) and

    M_(k+1)=F(M_k intersect S).

M_k is exactly the set of binary labels of the nonzero Pauli images of (Phi†)^k. This follows by induction: every reachable surviving label is in M_k; the next application kills precisely those outside S and maps the others by F. Conversely each element of M_k has a surviving original preimage, so no spurious label is introduced by the recursion. Since the channels are monomial in this basis, there is no cancellation between different initial observables to account for.

The subspaces are nested. M_1 is a subspace of M_0, and monotonicity of intersection and image propagates every inclusion. If M_(k+1)=M_k, applying the same operation gives equality forever. Otherwise the dimension drops by at least one. Consequently one reaches either zero or a nonzero plateau within at most 2n strict drops. A constant channel is acquired exactly when M_k={0}: then every output Pauli pulls back to a scalar identity or zero, so all outputs are independent of the input. Conversely a nonzero image contains a nonidentity Pauli pullback and proves nonconstancy.

All steps use Gaussian elimination on binary matrices of polynomial size in the raw circuit/register description. Reaching a nonzero plateau is a sound negative decision for eventual exact forgetting in THIS class, not an instability conclusion for an arbitrary quantum channel.

## 3. Constant output is not automatically pure

If M_m=0, simulate the explicit m-step channel on |0>^n by standard stabilizer operations, retaining enough tableau information to take the final partial trace. The resulting state sigma is constant for every input. It is a mixed stabilizer state with an efficiently obtained signed stabilizer group. If that group's rank is r, its purity is 2^(r-n); it is pure exactly when r=n. Reject pure-return admission when r<n.

If pure, synthesize a Clifford preparation V_psi of psi from its signed stabilizers. The output is fixed by Phi: Phi(Phi^m(rho))=Phi^m(Phi(rho)) implies Phi(sigma)=sigma. Thus Phi^m=Reset_psi and the full operator survival is zero. The same m is an acquired return certificate for the reviewed compiler. Reflection about psi is acquired by V_psi, a known all-zero phase reflection, and V_psi†, with polynomial implementation cost; it need not itself be a Clifford circuit.

The purity check is essential. A one-qubit counterexample is Phi=Hadamard conjugation after Z dephasing. Its adjoint sends X to Z and sends Z,Y to zero. The image chain has dimensions 2,1,0, but Phi² resets to I/2, not a pure state. Identity or Z dephasing gives a persistent nonzero image; a shift/discard-oldest/append-|+> channel gives the accepted exact n-step pure reset.

## 4. Acquiring the coefficient state with the correct phase

For the actual raw Stinespring W and the acquired pure fixed state, W psi is a pure product c tensor psi. A stabilizer marginal determines the ray of c, but the overlap A=(<c| tensor I)W and dark subtraction require a consistent phase; dropping this detail can change A psi=psi into a phase multiple.

There is a direct circuit solution without a phase oracle. On fresh known work, prepare psi with the chosen V_psi, run the original ancillary preparation and raw unitary W, then apply V_psi† on the retained source output. The result is exactly c tensor |0> on the work source, with the phase inherited from the actual gates. Thus this circuit prepares the correct c with clean returned work and has an acquired inverse/control. It uses the original W rather than a new channel with the same density matrix. It also avoids enumerating an exponential Kraus list. Global phases in an independently synthesized state ray need not be guessed.

The overlap block A is now acquired using W and this c preparation. Since A fixes psi and is contractive, P reduces A. Projection of the m-step dilation gives A^m Q=0. All circuit and controlled-operation costs are explicit polynomial costs in the input circuit size, n and e.

## 5. Stronger necessity: any strict pure-return bound forces exact forgetting

This improves the proposed sufficient threshold delta<1/2: for this monomial-Pauli class, with a pure fixed psi, ANY strict uniform return coefficient delta<1 forces the corresponding channel power to be constant.

Here is a channel-level lemma independent of stabilizer implementation. Let Psi be a CPTP map with pure fixed psi and suppose Psi†(U)=V, where U,V are Hermitian unitaries and V is nonidentity with both eigenspaces nonempty. For a Stinespring isometry W of Psi,

    (U tensor I_env) W = W V.

Indeed the squared norm of their difference on any vector is zero, using Psi†(U)=V and U²=V²=I. Also W psi=psi tensor c for some unit c.

Put a=<psi,V psi>=<psi,U psi>. If |a|<1, the normalized vector v=(V-a)psi/sqrt(1-a²) is orthogonal to psi and Wv=(U-a)psi tensor c/sqrt(1-a²). Its output is a pure state orthogonal to psi. If |a|=1, psi lies in the a eigenspace of both U and V. Any input in the opposite V eigenspace has output in the opposite U eigenspace, again orthogonal to psi. Therefore

    ||Psi†(I-|psi><psi|)||=1,

and no operator inequality Psi†Q<=delta Q with delta<1 is possible.

Apply this lemma to Psi=Phi^k. If M_k is nonzero, some nonidentity output Pauli pulls back to a signed nonidentity input Pauli, so U,V as above exist. If M_k=0, the channel is constant, and its pure fixed state forces that constant to be psi. Thus every accepted pure fixed-source strict-return certificate in this exact raw class collapses to a finite exact-reset certificate, detected by the image iteration. When the constant output is mixed there cannot be a pure fixed state at all, because applying the constant power to a purported pure fixed state would preserve it.

This does not say that arbitrary noisy channels with a spectral gap forget in finite time. Their Pauli coefficients need not be only zero or signed unit values. It also does not make an asymptotic mixing estimate in another norm an acquired operator certificate.

## 6. Resulting finite mathematical procedure

1. Parse the exact Clifford circuit, pure stabilizer ancillary state and retained/discarded wire sets. Form F,E, signs and S by tableau propagation.
2. Iterate binary subspaces until zero or a nonzero plateau. The bound is 2n strict dimension drops.
3. If nonzero plateau, reject this exact pure-return interface. If zero, compute the constant stabilizer output and test purity.
4. If pure, emit m, the subspace chain, signed fixed-state tableau and preparation, the original W/control/inverse circuits, the phase-consistent c preparation, and psi reflection. These certify Phi^m=Reset_psi and acquire the input interface.

Every stage has polynomial cost in the supplied finite raw circuit size and register sizes. This note specifies and proves the algorithm; it does not claim an implemented general finder or executed regression suite. Its negative completeness is only for the declared raw Clifford-Stinespring pure-return question.

Coupling access and centering remain separate: an arbitrary non-Clifford K can be supplied with its actual encoding, and an explicit sign extension can be used if a different centered physical model is intended. Therefore the full driven consumer is not automatically classically simulable by Gottesman–Knill just because its source acquisition uses tableaux. Conversely no classical hardness or practical superiority follows.

## 7. Strong ordinary prior comparison

Efficient Clifford/tableau simulation, mixed stabilizer handling and state synthesis are established tools; see [Aaronson–Gottesman](https://arxiv.org/abs/quant-ph/0406196). [Yashin et al.](https://arxiv.org/abs/2511.05478) explicitly discuss efficient representations and composition of stabilizer operations/Clifford channels. The construction here uses that ordinary machinery.

[Xiong et al., 2026](https://arxiv.org/html/2609.30125v1) explicitly credit Looi–Griffiths for abstract stabilizer-channel normal forms and compute transmission factors from interaction data in their specified setting. Their paper's detailed scope uses equal-size odd-prime registers and regular interactions, so its particular rank formulas should not be silently applied to every qubit circuit here. [Looi–Griffiths](https://arxiv.org/abs/1107.1761) already develop stabilizer-channel characterization through tripartite stabilizer structure. Only its accessible abstract/metadata were used in this comparison; a publisher search result showed authorization requirements, and no restricted full text was pursued.

Accordingly the contribution of this note is the explicitly checked finite image/purity/interface conjunction and the stated strict-return implication, not invention of stabilizer-channel normal forms, a general learning algorithm, or a demonstrated novelty claim.
