# An exact positivity obstruction to the literal generic-complex POVM lift

24 October 2026. Root construction; exact symbolic verification in the matching .py/.json. This is a failure of a proposed representation, not a separation theorem for information coefficients.

Take physical and original reference qubits A,R. Let sigma=(9/10)Phi_2+(1/10)I_4/4, with eigenvalues37/40 and1/40 (three times). Consider the strictly positive informationally complete POVM
E_(j,+/-)=(I +/- sigma_j/2)/6, j=X,Y,Z.
All effects have floor1/12 and their complex linear span is M_2.

Suppose a proposed top state G on A tensor R tensor R' is required to produce, for every measurement outcome, the arithmetic-mean Liouville baseline
Tr_A(E_i G)=[sigma_i tensor I+I tensor sigma_i^T]/(2r),
sigma_i=Tr_A(E_i sigma), r=2.

Informational completeness makes G unique: every physical matrix entry is fixed by the output constraints. The unique solution is
G=[sigma_AR tensor I_R' + Swap_(R,R')(sigma_AR^(T_R) tensor I_R')Swap_(R,R')]/(2r).
The transpose here is PARTIAL on R, not full on A,R. Full transpose would instead implement transposed effects and would not satisfy the required outputs for the Y effects.

The exact spectrum of this forced G is
1/8 (multiplicity4),
1/8-9sqrt(3)/80 (multiplicity2),
1/8+9sqrt(3)/80 (multiplicity2).
The middle eigenvalue is strictly negative. Thus no positive top state on this specified space can meet all these exact output arithmetic-mean constraints, even though the original input and all POVM effects are uniformly faithful.

The matching code verifies all six output identities symbolically, the effect-span rank4, the exact faithful input spectrum, and the exact negative lift eigenvalues. Recorded execution .05264seconds, Linux peakRSS46664KiB. These are observed checking costs, not total discovery costs.

What fails: extending the common-real/shared-antiunitary construction by silently replacing full transpose with partial transpose, or assuming the IC output constraints always admit a positive completion.

What does NOT follow: complete-Umegaki and conditional/SLD orders differ for this POVM; no such coefficient gap has been proved. A larger auxiliary space, a different asymptotic construction, or a different state representation could still establish equality. Even taking the two comparison POVMs identical makes their orders trivially equal while this literal lift remains impossible. Therefore failure of this lift is not evidence for a universal separation.
