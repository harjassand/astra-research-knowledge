# Exact heralded decoding of an unknown mixed qubit encoding by exterior projection
2026-10-29. Author theorem; independent receiving review requested. Primary overlap remains under investigation. Generic exterior algebra, Schur processing and isometry inversion are established tools, not claimed as newly invented.

## Model and physical protocol
Let L=C2, J=Cr, and V:L tensor J -> B=CD be an unknown isometry, D>=2r. The memoryless encoder is N(rho)=V(rho tensor sigma)V†, with unknown density matrix sigma on J. The ambient junk dimension r is supplied. Full rank sigma gives positive success; a rank-deficient sigma gives zero success in this protocol. This is not an exact rank-discovery procedure.

Put m=2r. Before the unknown payload arrives, make m-1 forward calls of N on one half of independently prepared qubit Bell pairs, retaining the untouched reference qubits A_1,...,A_(m-1) and all encoded B outputs. Later receive the encoded payload N(rho) in B_m. No reference retained from the payload's original preparation is available to the decoder.

Measure the known antisymmetric projector P_wedge on all m B registers. On failure report failure; the payload may be damaged and no retry-preserves-payload claim is made. On success discard all B registers. Apply Pauli Y to each of the m-1 retained reference qubits (a global phase is irrelevant), then apply the KNOWN SU2 Schur transform. The state is supported in total spin1/2. Output that spin qubit and discard its multiplicity register. This is a forward-CPTP-query protocol; it never invokes V†, a source/environment inverse, controlled-N, a Petz-adjoint oracle, or a classical reconstruction of V or sigma.

## Exact CP factorization, including references
Equivalently prepare singlet rather than Bell probes; the Y conversions merely switch these conventions. Choose any basis of J. For every fixed sequence of junk Kraus indices, antisymmetric contraction defines a linear map M_alpha:L -> L^(tensor(m-1)) on the reference qubits, with an additional unobserved junk/environment label. All B inputs lie in the same m-dimensional subspace V(L tensor J). Its mth exterior power is ONE-dimensional. Thus unknown V contributes the same exterior vector to every logical input and junk term; it cannot remain entangled with the recovered logical qubit after success.

For every U in SU2, singlets are invariant under U tensor U, while the full B wedge transforms under U tensor I_r by det(U tensor I_r)=det(U)^r=1. Consequently each M_alpha is an SU2 intertwiner:
 M_alpha U=U^(tensor(m-1)) M_alpha.
The known Schur decomposition of m-1 qubits is a direct sum of spin irreps tensor multiplicities. By Schur's lemma, an intertwiner from the fundamental spin1/2 has no other-spin component, and in the spin1/2 block has the form I_2 tensor |v_alpha>. Therefore the successful decoded CP map is exactly rho ->p rho, tensor an input-independent residual state. The same identity holds with an arbitrary external reference entangled with rho. No assumption of a pure junk state is used.

This argument also permits an arbitrary jointly correlated junk state on J^tensor m, initially independent of all logical inputs/references, with the same local V on all calls: conditional correctness survives, though the IID success formula below need not. It does not cover arbitrary causally interacting source memory merely from its one-call marginal N.

## Success probability and query count
For the IID model, the B marginal of each training call is tau=N(I_2/2). The success effect on the payload gives
 p(rho)=Tr[P_wedge tau^(tensor(m-1)) tensor N(rho)].
On the m-dimensional common support, the polarized determinant identity yields
 p(rho)=det(tau)/m *Tr[tau^(-1) N(rho)].
Since tau=V((I_2/2) tensor sigma)V†, the trace is Tr[2rho tensor I_r]=2r=m. Hence
 p=det(tau)=(det sigma)^2/2^(2r).
This is independent of rho, V and the ambient output dimension D. There are exactly2r-1 forward training calls, followed by the one encoded payload supplied to the decoder. At r=1 the probability is1/4. At r=2 with sigma=I_2/2 it is1/256. Tiny eigenvalues make the probability tiny; there is no rank- or spectrum-independent yield guarantee. Singular sigma is handled by continuity and has zero success.

## Control and resource obligations
Store2r-1 encoded D-dimensional training outputs plus2r-1 protected reference qubits until payload arrival. The exterior projection is a known permutation-control operation on m D-dimensional registers. A finite permutation-LCU construction with coherent outcome/uncompute realizes its Lüders instrument; success alone can also be realized by its projector Kraus operator. Known controlled register swaps cost O(log D) bit swaps each, but enumerating m! permutations is a large rank-dependent cost. No efficient generic compiler is silently assumed. The final Schur transform acts on only2r-1 qubits and is known, not V-dependent. Finite control error and conditional normalization must be charged; the theorem states the ideal known-control interface.

## Evidence and relation to prior work
`check_rank_two_decoder.py/json` independently executes the actual exterior Kraus contractions for r=2, D=4,5,7 and several junk spectra, followed by fixed Y and explicit spin1/2 decoder. It verifies scalar-identity decoded Kraus maps and the determinant success law. These are floating diagnostics; the intertwiner argument is the governing general proof.

Yoshida, Soeda and Murao, *Universal construction of decoders from encoding black boxes*, arXiv:2110.00258v4, gives output-dimension-independent inversion for pure isometry encoders. Its Lemma4 Eq23 is an equality of CPTP maps, not restricted to product inputs, and supplies a separately useful Schur compression mechanism. We have not yet established whether this precise mixed-encoding exterior decoder appears in that or later literature. arXiv:2602.05828 treats unknown-channel adjoints/Petz recovery virtually via expectation estimation; it does not provide a physical inverse oracle for use here.

`check_exact_intertwiners.py/json` additionally constructs every nonzero logical-to-reference exterior Kraus tensor for r=1,2,3 in the canonical embedding, applies the fixed real iY basis conversion, and verifies both SU2 generator intertwining equations with exact integers. It checks97 nonzero junk strings and the exact success-effect combinatorial factor m!/2. These checks independently fix the logical orientation and normalization; covariance extends them to the unknown embedding, while the proof covers general r.
