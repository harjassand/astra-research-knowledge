# Explicit q-ary CSS/GRS outer entanglement-distillation wrapper

28 October2026. Author construction using conventional coding ingredients; independent review pending. This supplies an actual efficient outer decoder/circuit for a conditional inner-to-outer composition. It does not establish a new universal-distillation capability or a hardware threshold.

## 1. Input contract and what is not assumed

B independently prepared inner blocks each output the SAME fixed m-qubit pair of Alice/Bob registers. After a fresh bilateral Pauli twirl with its keys retired from the assessed output, each block is Bell diagonal and has probability of a nonidentity Bell error at most epsilon0. The blocks are independent; identical distribution is sufficient but not necessary if the uniform upper bound holds. Fresh independent inner random seeds and source blocks can produce this contract. An average guarantee under ONE shared inner seed does not imply it. Neither twirling nor marginal fidelity creates independence.

The inner procedure must count its failures and any variable-yield outcomes in this fixed-payload contract. It cannot select apparently good blocks for free or discard bad outcomes without charging success probability and source consumption. The wrapper assumes this inner contract, not supplied microscopic noise or a known Pauli distribution.

For an ideal q-dimensional Bell pair, define X(a)|x>=|x+a> and Z(b)|x>=(-1)^Tr(bx)|x>, over GF(q), q=2^h. Uniform bilateral P tensor conjugate(P), P=X(a)Z(b), dephases in this Bell basis. Alice can generate the2h random bits and communicate them to Bob; actual Pauli gates and classical communication are paid. The random keys are not then used to select the code or decoder. Public/retained external transcripts require the corresponding operational scope; the calculation below is Bell fidelity of the final quantum output, not an unqualified joint-record diamond claim.

## 2. An explicit dual-containing GRS code

Choose integers B,t with0<=4t<B and a field GF(q) of characteristic2 with B<=q. Put s=2t, r=B−s, ell=B−2s=B−4t. Pick B distinct field elements a_i. Let

    w_i = 1 / product_(j != i)(a_i−a_j),
    v_i = w_i^(q/2).

The square map is a bijection in characteristic2, so v_i²=w_i and v_i!=0. Define C=GRS_r(a,v), all vectors(v_i f(a_i)) with deg f<r. Its first s weighted Vandermonde rows generate H=GRS_s(a,v).

For every polynomial g of degree at most B−2, Lagrange interpolation gives sum_i w_i g(a_i)=0: compare the coefficient of x^(B−1) in its Lagrange expansion. Hence H C^T=0, since the largest monomial degree in these dot products is(s−1)+(r−1)=B−2. Both evaluation matrices have their stated full ranks; therefore row(H)=C^perp. Since s<=r and the same a,v are used, C^perp is contained in C. This proves the needed Euclidean dual containment directly; no Hermitian-dual convention is silently substituted.

The q-ary CSS stabilizer has X(h),Z(h) for h in C^perp, with all h field multiples included. The field dot products vanish, so the trace commutation phases vanish. Each X/Z family has q^s elements, giving a q^ell-dimensional quantum code. The classical C distance is B−r+1=2t+1. A nontrivial logical Pauli has at least one of its X/Z vectors in C outside C^perp, so the quantum distance is at least2t+1. A minimum-weight C word has that weight, while C^perp has larger minimum distance B−s+1 because B>4t. Such a C word is not a stabilizer. Thus the code is exactly

    [[B, B−4t, 2t+1]]_q.

It corrects every q-ary Pauli whose UNION of X/Z support has at most t sites.

## 3. A total efficient classical syndrome decoder

Given syndrome sigma=H e, solve H y=sigma for one deterministic representative y (free coordinates set to zero). Then y=e+c for some c in C. Decode y by Berlekamp–Welch: divide its coordinates by v_i, writing z_i=y_i/v_i. Solve the B linear equations

    Q(a_i)=E(a_i) z_i,

with E monic of degree t and deg Q<r+t=B−t. There are(r+t)+t=B unknown coefficients. If the actual error has weight w<=t, a solution exists: multiply its degree-w error locator by any monic polynomial of degree t−w and set Q=E f for the underlying degree-<r message polynomial. For ANY solution, Q−Ef vanishes at the B−w non-error positions and has degree<B−t<=B−w. Therefore Q=Ef identically. This proves correctness even when w<t and the linear system has nonunique solutions; selecting any solution is sufficient.

Perform polynomial division, verify zero remainder, degree<r, valid code syndrome and at most t mismatched coordinates. On success return e_hat=y−c_hat. On failure return a fixed fallback error vector and a failure flag, without postselection or undefined control. The quantum protocol can still output its registers. Errors beyond t may be corrected, miscorrected or flagged, but are already inside the allowed bad event. Each X and Z syndrome is decoded separately. Exact Gaussian elimination costs O(B³) field operations per solve; no exponentially sized hash table or assumed nearest-codeword oracle is used.

## 4. Actual one-way bilateral circuit and orientation

Let H be its s independent rows. Extend those rows inside C by ell rows L, and extend C to the full field space by s rows R. Explicitly, take the remaining weighted Vandermonde rows for L, and standard unit rows in the nonpivot columns of a row reduction of C for R. Let T have rows[H;L;R]. T is invertible and H R^T is invertible.

Let Lin(T)|x>=|xT>, for row-coordinate vectors x. Let F be the field-trace Fourier transform

    F|x> = q^(−1/2) sum_y (-1)^Tr(xy)|y>.

It is real and self-inverse. Define U_enc=Lin(T)(F^tensor s tensor I): first apply F on the first s input registers, then apply Lin(T). With the first and last s input registers initially zero, this encodes the middle ell registers as uniform cosets of C^perp in C.

The distillation protocol does not inject new encoded pairs. It starts with the B noisy Bell pairs. Both parties apply U_dec=U_enc† (more generally Alice U_dec and Bob conjugate(U_dec); all gates here are real). Thus ideal B Bell pairs remain B Bell pairs. Each party measures the first and last s decoded registers in the computational basis; Alice sends her2s field-valued outcomes to Bob. Bob subtracts them from his corresponding outcomes, which is XOR in characteristic2.

For a Bell error X(e)Z(f) on Bob's incoming registers, define

    e_prime=e T^(−1),   f_prime=f T^T.

After decoding, the first-s X labels are f_prime_first=H f, and the last-s X labels are e_prime_last. Denote the observed differences by d_first,d_last. Hence the actual classical syndromes are

    sigma_f=d_first,   sigma_e=(H R^T) d_last.

Bob executes the finite decoder of Section3 to obtain e_hat,f_hat. He computes e_hat_prime and f_hat_prime and applies their inverse Pauli on the MIDDLE ell output registers. For every input error of weight at most t, these are the exact residual logical Pauli labels, so all ell output Bell pairs are perfect. Ancillary measurement outcomes cause no hidden logical correction: after a bilateral real Clifford, each input Pauli-labeled Bell state is a tensor product of Pauli-labeled Bell states, and the measured registers are separate factors. Their phases do not affect the remaining pairs. The code below verifies this orientation directly, not merely equality of syndrome dimensions.

For t=0 the protocol reduces to the identity outer code, with no checks and a trivial decoder. The positive-error-correction regime uses t>=1 and B>=5.

## 5. Field and gate construction are paid operations

A general GF(2^h) can be represented by binary polynomials modulo an irreducible degree-h polynomial. Field addition is XOR; multiplication and inversion have polynomial bit cost in h. One may find and verify the modulus using standard finite-field polynomial algorithms; it is not assumed to come from enumerating2^h objects in a regime where h is large.

A particularly explicit efficient specialization avoids that issue entirely. Choose h=max(1,ceil(log2 B)), so B<=q<=2B (with q=B when B>=2 is a power of two). Enumerate monic degree-h binary polynomials with constant term1 and test irreducibility by Frobenius powers and polynomial gcd. There are at most B candidates, each checked in polynomial(h) time. This is a deterministic polynomial-in-B field construction. It is implemented separately in check_field_and_gates_v1.py.

A Gaussian column elimination of T gives O(B²) field-coordinate additions/scalings/swaps implementing Lin(T), with the inverse obtained by reversing inverse operations. Multiplication by a known nonzero field scalar is an invertible h-bit linear map and compiles to O(h²) CNOT/SWAP gates. A controlled field addition y maps to y+a x uses at most h² CNOT gates. Field Fourier F uses h Hadamards and an invertible binary trace-Gram basis change, also O(h²) elementary gates. Therefore each party's whole outer unitary has O(B² h²) elementary Clifford gates; preparation/measurement of the2s h discarded qubits and4t h forward syndrome bits are additional explicit resources. Bob's output Pauli uses O(ell h) elementary gates. The trace-Gram matrix is nonsingular: the finite-field trace polynomial is nonzero of degree<q, and multiplication by any nonzero scalar permutes the field. Hence every nonzero field element pairs to trace1 with some element. The field basis, trace pairing and both binary orientation conventions must be fixed, as in the program.

These are ideal logical gate counts, not a claim that physical noise vanishes for free. If implementation channels differ from the ideal primitives by half-diamond allowances eta_i, telescoping bounds the extra final error by sum_i eta_i. A vanishing-error physical claim needs this total to vanish (or a separate fault-tolerant local implementation), including measurements, classical controls and reset. No threshold or hardware energy/timing model is supplied here.

## 6. Small-field stripes across a larger inner payload

When the inner block has m>=h ebits, split it into J=floor(m/h) h-ebit symbols and discard fewer than h leftover ebits. Apply the SAME B-symbol outer construction independently to each stripe across the B inner blocks. Output length is

    J h (B−4t) ebits.

There is no extra union factor J in the logical error bound: if at most t WHOLE inner blocks have nonidentity Bell errors, every stripe has at most t erroneous sites and every stripe is corrected simultaneously. Errors may be correlated arbitrarily between stripes within one inner block. This argument requires the common bad-block indicator supplied by the original m-ebit Bell-diagonal inner state; it is not obtained by asserting independent stripe errors.

The total gate count is O(J B² h²)=O(B² m log B), and classical finite-field decoding remains polynomial, for example O(J B³ h²) bit operations with naive field arithmetic. Deterministic small-field construction costs polynomial(B). The discarded payload fraction is less than h/m. If m<h, this stripe version does not apply; reduce B or obtain a larger inner payload rather than violating B<=q.

## 7. Error exponent, rate and actual scope

Let epsilon0<gamma<1/4, t=floor(gamma B), and suppose B is large enough that t/B>epsilon0. Under the independent-block contract, the number of bad inner blocks is stochastically dominated by Binomial(B,epsilon0). All errors through t are corrected. Therefore the full output entanglement infidelity is at most

    Pr[Binomial(B,epsilon0)>t],

which decreases exponentially in B. For example a standard Chernoff/KL bound uses threshold(t+1)/B. No noise distribution over nonidentity Paulis is learned or supplied. Independence, bounded total bad probability and actual ideal local control suffice at this outer stage.

If an independently justified inner family consumes k source copies to output m~kR ebits with fixed epsilon0, choosing B=k gives total source copies k², output asymptotic rate R(1−4gamma), and exponentially small outer error in k. Stripes lose only O(log k/k) payload fraction. This is a conditional composition. In the near-pure source application delta<=c/k, the allowed source impurity shrinks as c/sqrt(total copies); it is NOT a theorem for a fixed positive-noise iid source. The inner source-promise acquisition, discarded branches, fixed-payload padding, packing, costs and fidelity guarantees must all be separately proved. A pure product source cannot supply R>0 merely because its purity is high.

## 8. Conventional comparison and remaining work

These are standard CSS/GRS and one-way purification ingredients made explicit for the interface. Li–Xing–Wang, arXiv:0812.4514, SectionsII–III, treats quantum GRS/MDS codes, including a Hermitian-code framework. Our particular characteristic2 Euclidean CSS construction is proved above rather than inferred by changing their conventions. Bennett–DiVincenzo–Smolin–Wootters, arXiv:quant-ph/9604024v2, Sections5.3 and6, develops the relationship between one-way distillation and quantum error correction. Sources: https://arxiv.org/abs/0812.4514 and https://arxiv.org/html/quant-ph/9604024v2 . No historical novelty for these coding ingredients or new hashing advantage is claimed.

The same outer wrapper is available to an equally informed conventional inner method. In particular, the separately preserved CONVENTIONAL_REBLOCKING_CORRECTION_v1.md observes that ordinary pure-state concentration on smaller blocks can already establish the same qualitative dilute-source asymptotic capability. This wrapper does not remove that comparison or establish superiority of the Schur low-defect inner construction. Its contribution is to close the explicit outer syndrome/circuit obligation, not to manufacture a new capacity result.

Finite-field tests, code matrices, compiled coordinate gates, complete BW fallback and Pauli-pattern recovery are preserved in this folder. They are exact finite arithmetic and Clifford-label checks, not noisy quantum hardware or full density-matrix simulation. A separate independent receipt governs acceptance.
