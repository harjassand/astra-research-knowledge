# A sharp multilinear determinantal inequality and exact global SU(d)-singlet entanglement

**Research state, 2026-10-08 Brisbane:** Independently derived in this single-agent investigation using elementary Cauchy–Binet and AM–GM, then reconstructed from Schur–Weyl theory. These are rigorous conditional-free algebraic proofs given standard representation theory, not externally reviewed or historical-priority certified. **This does not establish a once-in-a-century or field-breaking discovery.** Distinguish novelty from correctness. No subagents.

## THEOREM 1: Sharp determinant-power squarefree coefficient bound (all dimensions and powers)

Fix integers d,r>=1 and n=dr. Let v_1,...,v_n be arbitrary vectors in C^d, and define

    Q(t_1,...,t_n)=det(Sum_(i=1)^n t_i v_i v_i^*).

Then

    0 <= [t_1 ... t_n] Q(t)^r
       <= (r!)^d Prod_(i=1)^n ||v_i||².                        (1)

Both bounds are exact. The upper equality is attained with r copies of each vector of any fixed orthonormal basis of C^d. The same proof holds over R.

**Direct complete proof.** Normalize all nonzero columns; if a column is zero both sides are zero. Fix all norms=1. Set F_r(v_1,...,v_{dr}) equal to the indicated squarefree coefficient. By Cauchy–Binet,

    Q(t)=Sum_(B subset [dr], |B|=d) w(B) t_B,
    w(B)=|det([v_i]_(i in B))|²>=0.

Expanding Q(t)^r and picking out the squarefree monomial means choosing r ORDERED pairwise disjoint d-subsets that partition [dr]. Consequently, FOR EVERY r>=2,

    F_r(V)=Sum_(B subset [dr], |B|=d) w(B) F_(r-1)(V_(B^c)). (2)

For r=1, F_1(V)=|det V|²<=Prod ||v_i||²=1 by Hadamard. Assuming the inequality for r-1, and recalling each remaining column is unit,

    F_r(V) <= ((r-1)!)^d Sum_(|B|=d) w(B)
             = ((r-1)!)^d det(V V^*)          [Cauchy–Binet]
             <= ((r-1)!)^d (Tr(V V^*)/d)^d   [eigenvalue AM–GM]
             = ((r-1)!)^d r^d = (r!)^d.

For sharpness set V=[I_d|...|I_d] with r copies of the standard basis. The polynomial is Q(t)=Prod_(a=1)^d(Sum_(j=1)^r t_(a,j)), so the desired squarefree coefficient in Q^r equals Prod_a r!=(r!)^d. Homogeneity restores arbitrary norms. QED.

**Remark:** This argument is a short induction; variants of such inequalities may already exist in mixed-discriminant or immanant literature. Historical priority is UNKNOWN. It does NOT solve Lieb's general permanental-dominance conjecture.

## THEOREM 2: Exact separable overlap of maximally-mixed SU(d) singlets

Fix d>=2, r>=1, n=dr and Hilbert space H=(C^d)^tensor n. Let P_inv be the orthogonal projector onto the SU(d)-invariant subspace, and define

    Omega_(d,r)=P_inv / f_(r^d),

where f_(r^d)=dim P_inv=(dr)! Prod_(j=0)^(d-1) j! / Prod_(j=0)^(d-1)(r+j)! is the hook-length/rectangular Specht dimension.

Define

    p_(d,r)= f_(r^d)*(r!)^d/(dr)!
           = Prod_(j=0)^(d-1) [j! r!/(r+j)!]
           = Prod_(j=0)^(d-1) binom(r+j,j)^(-1).          (3)

Then

    max_(sigma in SEP_n) Tr(P_inv sigma) = p_(d,r).

In particular, a product state with r copies of each one of d mutually orthogonal pure states is an optimizer.

**Proof reconstructing normalization from first principles.** Define the determinant singlet
    |Delta_d>=(d!)^(-1/2) Sum_(pi in S_d) sgn(pi) |pi(1),...,pi(d)>.
The state |Psi>=|Delta_d>^tensor r belongs to the SU(d)-invariant subspace. Schur–Weyl duality identifies this entire subspace with one irreducible S_n module of shape (r^d), multiplicity f_(r^d) (the associated SU(d) representation is determinant^r, trivial on SU(d)). Therefore the full S_n twirl of |Psi><Psi| equals Omega_(d,r) by Schur's lemma.

For a normalized product vector |v>=tensor_i|v_i>, a determinant block on sites B contributes exactly |det(V_B)|²/d!. Averaging over all n! site permutations, and noting that an UNORDERED partition into r size-d blocks occurs r!(d!)^r times, gives

    <v|Omega_(d,r)|v> = [r!/(dr)!] Sum_(unordered partitions (B_1,...,B_r))
                         Prod_a |det(V_(B_a))|²
                      = F_r(V)/(dr)!.

Thus <v|P_inv|v>= f_(r^d) F_r(V)/(dr)! <=p_(d,r) by Theorem 1; a balanced orthonormal product saturates. Linear convexity extends to all fully separable mixed states. QED.

**Exact algebraic corollary (restricted rectangular immanants).** If A=(<v_i,v_j>) is a positive semidefinite n×n Gram matrix with rank<=d, then

    Imm_(r^d)(A)=[t_1...t_n]det(Sum_i t_i v_i v_i^*)^r
                  <=(r!)^d Prod_i A_ii.

Indeed the expectation of the symmetric-group central idempotent is f/(n!) times the rectangular immanant; compare this with the SU(d)-invariant projector expectation in the previous proof. This is ONLY a rank<=d claim, not arbitrary PSD matrix. E.g., at identity A of rank dr, such a bound may FAIL for some d,r.

## THEOREM 3: Four exactly optimized multipartite entanglement measures

Retain n=dr, P=P_inv, Omega=P/f and p=p_(d,r). Let |b> be the balanced orthogonal product tensor consisting of r copies of each e_j. Define its SU(d)×S_n twirl

    sigma_opt = Twirl_SU(d) Twirl_S_n |b><b|.

This state is manifestly fully separable. It commutes with SU(d) AND S_n. By Schur–Weyl and multiplicity-one of shape (r^d), on the invariant subspace it must equal a scalar multiple of the identity. Since Tr(P sigma_opt)=p, it follows that

    P sigma_opt P = p Omega, with sigma_opt block diagonal
      sigma_opt=p Omega+(1-p) tau, tau>=0, supp(tau) orthogonal to P.

This explicitly saturates the following exact values (natural logarithms):

    min_(sigma in SEP_n) 1/2||Omega-sigma||_1 =1-p,
    E_R(Omega):=min_(sigma in SEP_n) D(Omega||sigma)=-log p,
    E_max(Omega):=min_(sigma in SEP_n) D_max(Omega||sigma)=-log p,
    R_g(Omega):=min{s>=0:(Omega+s eta)/(1+s) in SEP_n; eta density}=1/p-1.

**Matching lower bounds:** For all sigma in SEP, q=Tr(P sigma)<=p. The projective binary measurement (P,I-P) has target outcome (1,0) and competitor (q,1-q): hence trace distance>=1-q>=1-p and relative entropy>=-log q>=-log p. For max-relative entropy, Omega<=e^c sigma implies 1=Tr(P Omega)<=e^c q<=e^c p, so c>=-log p. Robustness: if (Omega+s eta)/(1+s)=sigma_sep, then Tr(P sigma_sep)>=(1+s)^(-1), forcing s>=p^(-1)-1. The explicit sigma_opt above reaches all four bounds and supplies eta=tau for robustness.

**Low entanglement-depth contrast:** The same permutation twirl of |Delta_d>^tensor r is Omega; consequently Omega is exactly d-producible (mixture of tensor-products of d-qudit determinants). Thus for every fixed d>=2 as r->infinity, the state can have trace distance 1-o(1) from the full SEP set despite entanglement depth <=d.

**Asymptotics:** for fixed d,
    p_(d,r) ~ (Prod_(j=0)^(d-1) j!) r^(-d(d-1)/2).
So relative entropy grows as [d(d-1)/2]log r - Sum_j log(j!)+o(1), while global trace distance approaches 1 at polynomial rate r^(-d(d-1)/2).

**Examples:**
  d=2: p_(2,r)=1/(r+1) (2r qubits; trace distance r/(r+1)).
  d=3,r=2: p=1/18; trace distance 17/18; E_R=log18; R_g=17.
  d=3,r=3: p=1/40; trace distance 39/40; E_R=log40; R_g=39.
  d=4,r=2: p=1/180; trace distance 179/180; E_R=log180; R_g=179.

## Quantitative ideal white-noise certification (additional corollary)

For t in [0,1], let rho_t=(1-t)Omega_(d,r)+t I/d^(dr), i.e. a GLOBAL depolarizing mixture, not local independent noise. The witness W=pI-P_inv has negative expectation (and thus certifies entanglement) whenever

    (1-t)+t f_(r^d)/d^(dr)>p_(d,r),

equivalently

    t < t_cert=(1-p_(d,r))/(1-f_(r^d)/d^(dr)).

This is a **sufficient entanglement detection region**, NOT the exact full-separability threshold of rho_t. Examples: (d,r)=(3,2) gives t_cert≈0.95096685; (3,3) gives 0.97708492; (4,2) gives 0.99465693. For fixed d as r->infinity, t_cert→1 with 1-t_cert~p_(d,r)~c_d r^(-d(d-1)/2). This quantifies a peculiar globally robust but fixed-depth resource under the precisely defined noise model; not a device-level claim. The P_inv measurement may incur nontrivial Schur-transform/collective-control and readout costs, and local per-site decoherence is a different channel.


## Computational/adversarial tests and scope

1. Exact combinatorial coefficient enumeration (no optimizer) verifies equality in balanced frames for d=2,r=2,3 and d=3,r=2,3; numerical random complex Gram matrices for d=2..4 fall below the proposed bound. Earlier optimization for d=2,3,4,r=2 reached the equality point independently from random seeds. Such finite tests are checks, not proof; proof above is complete.
2. Independent SU(d) Lie-algebra kernel projector calculation, with no determinant-partition representation, verifies <balanced|P_inv|balanced>=1/2,1/3,1/4 for (d,r)=(2,1),(2,2),(2,3); 1/6,1/18 for (3,1),(3,2). The numerical projector rank also matches the hook-length formula (1,2,5,1,5).
3. The spin-zero qubit case has a separate direct SU2 Haar-integral/Hölder proof: f_i(g)=<psi_i|g|psi_i>, |f_i|²~Uniform[0,1] for Haar SU2. Hölder bounds |Integral Prod_i f_i|<=1/(r+1) for 2r unit Bloch states; r up and r down saturates, independently checking the all-d normalizations.
4. Necessity of quantum-state symmetrization: the balanced product alone is SEP, but its P-block is rank-one projected, NOT p Omega. The joint SU(d)×S_n twirl is essential for *attaining* trace-distance/relative-entropy/robustness bounds.
5. This proof concerns the full invariant projector maximally mixed state, not arbitrary pure singlet or arbitrary SU(d)-invariant mixed state. It does not resolve the extensive-marginal threshold theorem's separate Fourier/heat-kernel dependencies.
6. Equality rigidity/uniqueness for generic d,r has NOT been classified. Do not extrapolate the rank<=d rectangular immanant inequality to arbitrary rank.
7. No inference to a practical quantum preparation advantage, cryptographic secrecy, high entanglement depth or error-resilience. Preparing/detecting these highly symmetric global subspaces can require substantial resources.

## Further EXACT operational corollary: optimal zero-false-negative singlet test and fidelity

For an arbitrary fully separable sigma, tr(P_inv sigma)<=p. Thus the binary global projector measurement {P_inv,I-P_inv} accepts Omega with probability 1 and accepts any fully separable adversary with probability at most p. The bound is SHARP (sigma_opt attains it), so p is exactly the optimal type-II error for the zero-type-I test P_inv. A POVM effect E with tr(E Omega)=1 must act as identity on supp(Omega); positivity implies E>=P_inv, hence cannot improve the worst-case separable false-positive probability.

Likewise, if F is SQUARED Uhlmann fidelity, monotonicity of fidelity under binary measurement gives F(Omega,sigma)<=tr(P_inv sigma)<=p for all SEP sigma. The explicit commuting sigma_opt satisfies F(Omega,sigma_opt)=p. Thus

    max_(sigma in SEP) F(Omega,sigma)=p;

the fidelity-defined logarithmic/geometric entanglement measures equal -log p and 1-p, respectively. This statement concerns the fidelity-based measure, NOT the convex-roof geometric measure. It is a single-copy theorem and does NOT assert multiplicativity across copies held jointly by laboratories.

## Strengthened historical-priority caution

Zhu, Chen and Hayashi, "Additivity and non-additivity of multipartite entanglement measures" (2010), https://arxiv.org/abs/1002.2511 , previously derived one- and two-copy entanglement measures for antisymmetric projector states and explicit geometric-measure nonadditivity. Therefore nonadditivity of antisymmetric-state geometric/relative entanglement measures is established prior art and MUST NOT be presented as a discovery here. Their result concerns different tensor and antisymmetric-projector contracts in its original one- and two-copy theorems. Rigorous comparison of their "generalized antisymmetric states" to the full maximally mixed SU(d)-singlet projector family (r^d) remains REQUIRED before claiming historical novelty for the exact formula here.

Rico, Grinko, Krebs and Zaw, Phys. Rev. Lett. 137 100203 (September 4 2026), https://doi.org/10.1103/nvk2-h8d5 , already connect Schur–Weyl isotypic measurements, multipartite entanglement structure and immanant inequalities; their abstract establishes fixed orders three/four and general entanglement witnesses. The present arbitrary-(d,r) coefficient bound may overlap with results in its supplement; an abstract-only comparison is NOT adequate for novelty certification.

Neither the current coefficient proof nor the previous SU(d)-marginal threshold solves Lieb's full permanental-dominance conjecture, which remains the higher-impact open gate. General rectangular immanants at arbitrary PSD rank are OUTSIDE the proof's domain.


## Historical novelty audit (limited, not decisive)

Relevant known math: Hadamard determinant bound, Cauchy–Binet, eigenvalue AM–GM, Schur–Weyl duality, hook-length formula and geometric measure/robustness of multipartite entanglement are all established ingredients. The precise full family of optimum entanglement quantities and normalized rectangular immanant inequality was not located in a targeted October 2026 literature scan; this is **NOT an exhaustive priority search**. Particularly relevant:
- Bapat–Sunder, "An extremal property of the permanent and the determinant" (1986), related immanant operator inequalities, https://doi.org/10.1016/0024-3795(86)90220-X
- Pate, "Immanant Inequalities, Induced Characters, and Rank Two Partitions" (1994), https://doi.org/10.1112/jlms/49.1.40
- Bürgisser, "The Computational Complexity of Immanants" (2000), https://doi.org/10.1137/S0097539798367880
- Huber–Maassen, "Matrix forms of immanant inequalities" (2021), https://arxiv.org/abs/2103.04317
- Vitagliano–Gühne–Tóth, SU(d) squeezing/singlet entanglement (2024/25), https://arxiv.org/abs/2406.13338

This theorem is reproducible and exact but has **not** been established as a human-revolutionizing, century-level breakthrough or historically novel. Next high-value directions: identify sharp analogues for NONRECTANGULAR Schur–Weyl sectors, nonidentical local dimensions/tensor representations, certified finite-size loss/noise bounds, implications to long-standing permanental-dominance conjectures (these remain open), or an actual scalable device capability. Attempting any such extension must preserve exact assumptions.
