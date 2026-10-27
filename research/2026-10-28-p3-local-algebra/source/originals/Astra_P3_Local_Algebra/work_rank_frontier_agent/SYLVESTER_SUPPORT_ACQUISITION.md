# Acquiring a global quadratic defect by a manufactured scalar orbit

This proves an extension of the acquired-field counting interface that removes its per-field-block unique-decoding radius on a quantified family. The primary bandwidth-one construction uses a selfadjoint annihilator and a seven-dimensional scalar orbit, uniformly for every field degree at least seven. The earlier one-sided operator is preserved as a general-bandwidth construction. The algorithm is deterministic and exact; a deterministic support-transversality condition guarantees recovery, and a uniform random rank error satisfies it with an explicit probability bound. Generic multivariate point counting remains the established Lauder–Wan algorithm, not a new implementation here.

## 1. Input and notation

Let \(F=\mathbb F_{2^d}\), \(V=F^b\), and \(n=bd\). The field and the identification of the original bit space with \(V\) are acquired from the radical-free third difference tensor of a raw Boolean cubic, as in the preserved acquired-field compiler. More generally they may be acquired from the residue field of a nilpotent centroid. No field, coordinates, quadratic base, defect, support, or rank is supplied by the user.

Use the nondegenerate binary pairing

\[
\langle x,y\rangle=\operatorname{Tr}_{F/\mathbb F_2}\sum_{i=1}^{b}x_i y_i.
\]

Its matrix is the block trace Gram matrix \(G\). A binary alternating polar matrix \(B\) determines the selfadjoint binary map \(L=G^{-1}B\). Multiplication \(M_a:x\mapsto ax\) is selfadjoint for this pairing.

For bandwidth \(s\ge1\), with \(2s<d\), define

\[
\mathcal C_s=\left\{L_0(x)=\sum_{t=-s}^{s} C_t x^{2^t}: C_t\in F^{b\times b}\right\}.
\]

The powers act componentwise; negative powers are interpreted modulo \(d\). Require \(G L_0\) to be alternating. Assume for the recovery theorem that

\[
L=L_0+E,\qquad L_0\in\mathcal C_s,\quad E=E^*,\quad GE\text{ alternating},\quad\operatorname{rank}_{\mathbb F_2}E=r.
\]

Write \(U\) both for an \(n\times r\) binary column matrix spanning \(\operatorname{im}E\) and for its column space. There is a nonsingular alternating \(r\times r\) binary matrix \(K\) such that

\[
E=U K U^*,\qquad U^*=U^\top G.
\]

In particular \(r\) is even. This factorization is used only in the proof; the algorithm never receives it.

## 2. A manufactured annihilator

Take the acquired degree-\(d\) field generator \(z\). Put \(k=2s+1\), \(a=z^{2^s}\), and define the ordinary scalar polynomial

\[
Q(T)=\prod_{j=0}^{k-1}(T+z^{2^j})=\sum_{j=0}^{k}c_j T^j.
\]

The roots are distinct. The binary-linear operator on maps

\[
\mathcal H(L)=\sum_{j=0}^{k}M_{c_j}\,L\,M_a^j                                      \tag{1}
\]

is computable from the raw matrix and the acquired field.

**Lemma 1.** \(\ker\mathcal H=\mathcal C_s\).

**Proof.** Every binary-linear map \(F\to F\) has a unique expansion \(\sum_{t=0}^{d-1}v_t X^{2^t}\). Thus every map \(V\to V\) has a unique matrix-coefficient version. On its term \(C_t x^{2^t}\), (1) multiplies the coefficient by \(Q(a^{2^t})\). The Frobenius orbit of the degree-\(d\) element \(a\) has length \(d\), and exactly the residues \(t=-s,\ldots,s\) give roots of \(Q\). This proves both inclusions. \(\square\)

Define scalar subspaces

\[
C=\operatorname{span}_{\mathbb F_2}\{c_0,\ldots,c_k\},\quad c=c_{k-1},\quad
R=\operatorname{span}_{\mathbb F_2}\{1,a,\ldots,a^k\},\quad S=C+cC+R.              \tag{2}
\]

We use directly checkable scalar conditions

\[
\dim C=\dim R=k+1,\qquad C\cap cC=\mathbb F_2 c.                           \tag{3}
\]

**Lemma 2.** Conditions (3) hold for every acquired generator whenever \(d\ge3\cdot2^{2s}\). Moreover \(\dim S\le6s+4\), and for \(s=1\), \(\dim S=10\).

**Proof.** First regard the coefficients as polynomials in an indeterminate \(Z\). The coefficient \(c_j(Z)\) is the sum of \(Z^e\) over exponents whose \(k\)-bit binary expansion has weight \(k-j\). These supports are disjoint, so the \(k+1\) coefficients are independent. Their highest degrees are \(2^k-2^j\), including zero for \(j=k\).

The multiplier \(c(Z)=\sum_{i=0}^{k-1} Z^{2^i}\) has degree \(2^{k-1}\). For \(0\le j<k\), the products \(c c_j\) have distinct highest degrees \(3\cdot2^{k-1}-2^j\ge2^k\), whereas every element of \(C\) has degree at most \(2^k-1\). Thus these \(k\) products are independent modulo \(C\); the remaining product \(c c_k=c\) lies in \(C\). No nonzero polynomial of degree below \(d\) vanishes at \(z\), so the degree bound preserves these facts after evaluation. It proves \(\dim(C+cC)=2k+1\) and the intersection assertion.

The powers \(a^j=z^{j2^s}\), \(0\le j\le k\), are distinct powers of degree below \(d\), hence independent. Both \(C+cC\) and \(R\) contain 1, so \(\dim S\le(2k+1)+(k+1)-1=3k+1=6s+4\). For \(s=1\),

\[
C=\langle1,z+z^2+z^4,z^3+z^5+z^6,z^7\rangle,\qquad R=\langle1,z^2,z^4,z^6\rangle,
\]

and direct coefficient comparison gives \(\dim S=10\). The program checks (3), so it can also accept smaller degrees where this uniform sufficient bound is unnecessary. \(\square\)

For the **legacy one-sided operator** at bandwidth one and \(7\le d\le11\), the implementation can try full-degree generators if \(z=X\) fails. It tries at most \(2^{11}\) candidates, an absolute bounded-size fallback. Valid reference presentations are \(h=0x83,0x11b,0x203,0x409,0x805\) in degrees 7 through 11; field isomorphism transfers their certified generators. All 389 irreducible presentations in these degrees were checked, with at most 11 trials in the actual tests. The stronger primary operator in Section 3.1 removes this fallback entirely.

## 3. Exact support acquisition

For a binary scalar subspace \(S\subset F\), write \(SU\) for the span of all \(su\). The recovery condition is

\[
\dim(SU)=(\dim S)r.                                                       \tag{4}
\]

Equivalently, multiplication \(S\otimes_{\mathbb F_2}U\to V\) is injective. This is a geometric condition on the actual hidden support, not a supplied decomposition.

**Theorem 3.** Under (3) and (4), a deterministic polynomial-time algorithm recovers the exact planted \(L_0,E\) from \(L\). No inequality between \(r\) and \(d\) is required; \(r\) may exceed \(d\).

**Proof.** Compute \(H=\mathcal H(L)=\mathcal H(E)\). Selfadjointness of scalar multiplication gives

\[
H=[c_0U\ \cdots\ c_kU]\operatorname{diag}(K,\ldots,K)[U\ aU\ \cdots\ a^kU]^*.   \tag{5}
\]

Both outer matrices have column rank \((k+1)r\) by (4), and the middle matrix is invertible. Therefore

\[
W:=\operatorname{im}H=CU.                                                 \tag{6}
\]

Injectivity on \((C+cC)\otimes U\) preserves intersections:

\[
W\cap cW=(C\cap cC)U=cU,\qquad U=c^{-1}(W\cap cW).                        \tag{7}
\]

This acquires a basis \(\widehat U\) of the support by binary Gaussian elimination. Form the full-column-rank matrix \(W_C=[c_0\widehat U\ \cdots\ c_k\widehat U]\), and express each column of \(H\) uniquely in it. In (5), the first \(r\) coefficient rows are exactly \(\widehat K\widehat U^*\), since the first right power is \(a^0=1\). Multiplying those rows on the left by \(\widehat U\) recovers \(E\). Finally \(L_0=L+E\). There is no additional code-distance or uniqueness assumption. \(\square\)

The implementation verifies the directness of the recovered \(S\widehat U\), the rank and alternation of \(GE\), and \(\mathcal H(L+E)=0\). It extracts all band coefficients by exact linearized-polynomial solves. Every returned decomposition is therefore exact, including on inputs outside the promised family. If \(H=0\), it returns the verified rank-zero representation \(L_0=L\), which need not be a planted representation outside the hypotheses.

There is no support enumeration, search over \(2^d\) scalars, or list decoder. Dense binary and field linear algebra gives a deliberately loose bound \(O(s n^5)\) bit time and \(O(s n^2)\) working bits with classical arithmetic. Earlier centroid acquisition and output integration add their separately charged polynomial costs. No sharp matrix-exponent claim is needed.

### 3.1. Stronger selfadjoint bandwidth-one operator

For bandwidth one, use the symmetric bivariate polynomial

\[
P(X,Y)=(X+Y)(X^2+Y)(X+Y^2)
=X^4+Y^4+(X+X^2)(Y+Y^3)+(X+X^3)(Y+Y^2).
\tag{10}
\]

Put \(p=z+z^2\), \(q=z+z^3\), and let \(C=\langle1,z^4,p,q\rangle\). Define

\[
\mathcal H_{\rm sa}(L)=L M_{z^4}+M_{z^4}L+M_p L M_q+M_q L M_p.
\tag{11}
\]

On a Frobenius coefficient \(C_t x^{2^t}\), this multiplies by \(P(z,z^{2^t})\). For a degree-\(d\) generator, it vanishes exactly when \(t=0,1,-1\pmod d\). The third factor gives \(z=z^{2^{t+1}}\), so no unintended square-root branch occurs. Thus \(\ker\mathcal H_{\rm sa}=\mathcal C_1\).

For every \(d\ge7\), the four scalars \(1,z^4,p,q\) are independent. Let \(S=C+pC\). The product \(p\cdot1=p\) lies in \(C\). The other three products have independent nonzero classes modulo \(C\): \(p^2=z^2+z^4\notin C\); \(pq\) has degree five; and \(pz^4\) has degree six. No relation of degree at most six vanishes at \(z\). Consequently

\[
C\cap pC=\mathbb F_2p,\qquad \dim S=7.                                    \tag{12}
\]

Let \(V_C=[U\ z^4U\ pU\ qU]\), and let \(J_4\) swap coordinate blocks 0 with 1 and 2 with 3. For the hidden error,

\[
\mathcal H_{\rm sa}(E)=V_C(J_4\otimes K)V_C^*.                             \tag{13}
\]

If \(\dim(SU)=7r\), then \(V_C\) has full column rank, and the middle alternating matrix is invertible. Hence \(W=\operatorname{im}\mathcal H_{\rm sa}(L)=CU\), and

\[
U=p^{-1}(W\cap pW).
\]

After expressing \(H\)'s columns in the basis \([U\ z^4U\ pU\ qU]\), the **second** block of \(r\) coefficient rows is \(K U^*\). Multiplying it by \(U\) reconstructs \(E\). This index matters: the first block is \(K U^*M_{z^4}\), not \(K U^*\).

**Theorem 3a (primary interface).** For every \(d\ge7\), a compatible bandwidth-one base plus a selfadjoint alternating rank-\(r\) defect is recovered in polynomial time whenever \(\dim((C+pC)U)=7r\). The syndrome and all supports are manufactured from the input; \(r\) is not supplied. There is no relation required between \(r\) and \(d\), no extra right-orbit condition, and no field-element search. Every successful output is verified exactly.

The public API defaults to this operator at bandwidth one. `method='one_sided'` preserves the earlier construction and its data; wider bandwidths currently use that general operator. Both remain combinable with the earlier bounded-distance Gabidulin route. Neither new method uniformly dominates bounded-distance decoding on adversarial supports.

The four-dimensional syndrome expansion is minimal within this particular symmetric scalar-sandwich family. Indeed write such an operator as \(\sum_{i,j}K_{ij}M_{c_i} L M_{c_j}\), with independent binary scalar coefficients \(c_i\) and symmetric binary \(K\). Annihilating field-linear maps forces \(\sum_iK_{ii}c_i^2=0\), hence every diagonal coefficient is zero. A nonzero rank-two alternating \(K\) would yield an operator \(M_u L M_v+M_v L M_u\) with independent nonzero scalars \(u,v\). On Frobenius squaring its multiplier is \(uv^2+vu^2=uv(u+v)\ne0\). Thus rank two cannot annihilate bandwidth one; rank at least four is necessary. This is a limitation of this operator family, not a lower bound for other support-recovery algorithms.

## 4. A rigorous random-support guarantee

Fix the top tensor, its acquired field, the compatible base, and the scalar space \(S\) before sampling the error. Choose \(r\) columns \(u_1,\ldots,u_r\) independently and uniformly from \(V\), and choose a fixed nonsingular alternating binary \(K\).

**Theorem 4.** With \(t=\dim S\),

\[
\Pr[\dim(SU)<tr]\le(2^{tr}-1)2^{-n}<2^{tr-n}.                            \tag{8}
\]

**Proof.** A dependence is a nonzero tuple \((s_1,\ldots,s_r)\in S^r\) with \(\sum_i s_i u_i=0\). Fix such a tuple. Some \(s_j\ne0\), and multiplication by \(s_j\) is a bijection of \(V\). Conditional on all other columns, the sum is uniform in \(V\), so it vanishes with probability exactly \(2^{-n}\). A union bound over the \(2^{tr}-1\) tuples proves (8). Independence of the bad events and a random-subspace intersection heuristic are not used. \(\square\)

If \(U\) is conditioned to have rank \(r\le n-1\), the bound is at most \(2^{tr-n+1}\), because full rank has probability at least \(1-2^{r-n}\ge1/2\). With fixed nondegenerate alternating \(K\), this generates the uniform distribution over rank-\(r\) alternating polar matrices after multiplication by the fixed Gram matrices: binary congruence acts transitively on those matrices, and all matrices have the same number of ordered factor preimages. Thus the guarantee applies to uniform dense rank-\(r\) quadratic defects.

For the primary bandwidth-one construction the failure bound is therefore less than \(2^{7r-n}\) for independent support columns, or \(2^{7r-n+1}\) for a uniformly random rank-\(r\) alternating defect. For fixed bandwidth and \(r=o(n)\), condition (4) holds with probability \(1-2^{-n+o(n)}\). Field coordinates acquired from the third tensor depend only on the top degree and are independent of the quadratic error. Their fixed invertible coordinate change preserves uniform support. Thus the guarantee applies to the raw-input compiler.

## 5. Counting consequence and the removed obstruction

Once the alternating defect is recovered, the preserved real Walsh identity expresses its quadratic phase as \(2^r\) linear-character leaves with denominator \(2^{r/2}\). Integration of the compatible base yields a trace polynomial of ordinary field degree at most \(2^s+1\), retaining the constant and binary-linear corrections. Every leaf adds only a field-linear trace form. The established Lauder–Wan single-point-count construction gives

\[
2^{r+O(b(\log n+s))}\operatorname{poly}(L+n)                              \tag{9}
\]

bit time, with the same field-evaluation space bound as the earlier acquired-field theorem. Leaves are streamed and do not add a \(2^r\) space factor. This consequence is unconditional with respect to the ETH manuscript.

The earlier block decoder required \(2r\le d-2s-1\). The new theorem replaces that sufficient radius by (4). It does not claim worst-case recovery for every rank-\(r\) defect. For fixed \(s\), \(r=o(n)\), and \(b\log n=o(n)\), it yields a subexponential exact count with overwhelming probability over a uniform rank-\(r\) defect even when \(r/d\to\infty\). For example, \(d=m^2\), \(b\asymp m^2\), and even \(r\asymp m^3\) give \(n\asymp m^4\), exponent \(O(m^3+m^2\log m)\), and \(r/d\asymp m\). The top tensor must still acquire the stated field; the theorem does not include generic circuits or arbitrary cubics.

An equally informed supplied-representation comparator has the same Walsh and field-count costs. The strengthened result is acquisition from the raw scalar cubic, not an improvement to the point-count algorithm or a demonstrated practical advantage against other exact solvers.

### Joint interface with a nilpotent algebra counter

The matrix theorem also applies when an independently acquired algebra is \(A=F[t]/(t^e)\), the original module is \(A^3\), and its residue-field coordinate space is \(F^{3e}\). A scalar linear functional applied to an ordinary cubic over \(A\) is an ordinary field cubic in those \(3e\) coordinates. Hence its quadratic polar blocks have bandwidth one. Any exact ring evaluator that accepts added binary linear forms can be used at each Walsh leaf after the support recovery above.

If that ring evaluator runs in polynomial time and space, the resulting count takes \(2^r\operatorname{poly}(L+n)\) time and polynomial space for \(n=3ed\). The primary seven-dimensional orbit permits \(r=o(n)\) even for fixed \(d\ge7\) and growing \(e\); in particular \(r=O(\log n)\) is polynomial time. This paragraph is an interface consequence, conditional on the independently proved ring evaluator, not a claim that this file implements it.

## 6. Executed cases and decisive failures

The first one-sided matrix implementation recovered the exact planted base and defect for:

| Original bits \(n\) | Field degree \(d\) | Field variables \(b\) | Bandwidth \(s\) | Defect rank \(r\) |
|---:|---:|---:|---:|---:|
|108|12|9|1|8|
|204|12|17|1|16|
|208|16|13|1|16|
|504|24|21|1|32|
|432|48|9|2|12|

Each includes 1,024 exact quadratic identities. The \(r=16,d=12\) and \(r=32,d=24\) cases demonstrate recovery above the entire field dimension. Source data records old block-decoder acceptance or rejection. The bandwidth-two case is an algebra test and can lie within the old radius; it does not establish another separation.

The stronger selfadjoint implementation replayed all five witnesses and the already-acquired raw 108-bit matrix, returning the same exact bases and defects. It also recovered a new \(n=105,d=7,b=15,r=8\) witness, for which the old radius is two and the defect rank exceeds \(d\). All 389 irreducible field presentations of degrees seven through eleven were exhaustively checked with the single generator \(z=X\); every one has the seven-dimensional scalar certificate, and every Frobenius coefficient was checked to vanish under (11) exactly at indices \(0,1,-1\). The source and results are `selfadjoint_support_checks.py` and `sylvester_selfadjoint_results.json`.

Two failures are preserved. A defect that is itself a compatible codeword has zero manufactured syndrome: the raw input has an exact rank-zero alternative, so planted recovery is impossible without extra conditions. Its scalar orbit fails (4). A sufficiently large generic support saturates the ambient space; the implementation rejects its incompatible intersection dimensions. These are failures of this acquisition route, not counting lower bounds.

The separate `sylvester_raw_checks.py` completed whole acquisition on a raw 108-bit scalar cubic with an unknown rank-eight defect. The input has 104,741 Boolean ANF terms; its top field cubic contains all 84 triples of nine coordinates, and 216 binary shears disguise the inputs. The compiler was given only the original bit count and explicit ANF. It acquired a degree-12 field and nine field coordinates, recovered the exact planted defect, passed 1,024 further original-input/trace-reconstruction identities, and the old block decoder rejected the same acquired matrix. Full data are in `sylvester_raw_results.json`, with exact input in `raw_108_input.json`. The recorded roughly 206-second acquisition is diagnostic, not a benchmark. Generic multivariate point counting is not executed by these acquisition tests.

## 7. Prior machinery and scope

Recovery by multiplying and intersecting support subspaces is established LRPC machinery. Gaborit, Murat, Ruatta and Zémor introduced that decoder; later work refined it and analyzed failures. Burle and Otmani specifically explain why treating scaled syndrome subspaces as independent random subspaces is unjustified. Here the selfadjoint factorization (5) manufactures the full syndrome support and (8) is a direct union bound over coefficient tuples.

Low-rank images under left/right matrix operators also have classical displacement-structure ancestry, including Kailath, Kung and Morf's 1979 work. The present construction must not be advertised as inventing displacement rank or Krylov methods. Its specific operator is chosen to annihilate ordinary cubic trace polar terms, and support reconstruction supplies a count-preserving interface after the hidden algebra has been acquired.

Couvreur's deterministic symmetric-error results are an important comparator. Their code embeddings are arranged relative to the symmetric subspace. They do not directly recover the present model, where both compatible base and error are alternating and the earlier midpoint ambiguity remains.

The narrower candidate contribution is manufacturing a global Sylvester syndrome from a raw acquired-field scalar quadratic, exactly deconvolving its support, and obtaining the stated scalar-counting guarantee beyond the per-block radius. No historical first-priority claim is made. This is not a new generic decoder, new support-product principle, or executed general multivariate point counter.

### Primary references

1. Philippe Gaborit, Gaetan Murat, Olivier Ruatta, Gilles Zémor, *Low Rank Parity Check codes and their application to cryptography*, WCC 2013. <https://www.unilim.fr/pages_perso/olivier.ruatta/wccRank_sub.pdf>.
2. Nicolas Aragon, Philippe Gaborit, Adrien Hauteville, Olivier Ruatta, Gilles Zémor, *Low Rank Parity Check Codes: New Decoding Algorithms and Applications to Cryptography*, 2019. <https://arxiv.org/pdf/1904.00357>.
3. Étienne Burle, Ayoub Otmani, *An Upper-Bound on the Decoding Failure Probability of the LRPC Decoder*, 2023. <https://arxiv.org/pdf/2309.14028>.
4. Alain Couvreur, *Improved decoding of symmetric rank metric errors*, 2023. <https://arxiv.org/pdf/2212.08713>.
5. Alan G. B. Lauder, Daqing Wan, *Counting Points on Varieties over Finite Fields of Small Characteristic*, especially Proposition 36 and Section 6.4. <https://arxiv.org/pdf/math/0612147>.
6. Thomas Kailath, Sun-Yuan Kung, Martin Morf, *Displacement ranks of matrices and linear equations*, Journal of Mathematical Analysis and Applications 68(2), 395–407, 1979. Primary publisher record: <https://www.sciencedirect.com/science/article/pii/0022247X79901240>; author publication list: <https://web.stanford.edu/~tkailath/cgi-bin/PubsList.php>.

The preserved `deliverables/Astra_P3_Acquired_Field_Counters.tex` supplies the separately proved centroid acquisition, trace integration, real Walsh reconstruction, and charged Lauder–Wan bound used in (9).
