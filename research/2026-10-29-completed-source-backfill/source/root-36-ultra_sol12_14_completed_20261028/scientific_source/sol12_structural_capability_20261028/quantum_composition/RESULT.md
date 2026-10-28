# A finite positive composition receiver for strong coherent sources

The acquired theorem is

`Delta(rho_p) >= (1-sum_i p_i^2)/128`

for every mixture of at most five of the nine qutrit Weyl-Bell states,
with arbitrary weights and arbitrary chosen labels. Delta is strictly
positive except at the pure Bell vertices. This is an unflagged mixing
operation on maximally entangled positive seeds; positivity under such
mixing is not supplied by generic convexity. It is a whole finite family,
not an easy-fixture extrapolation. The proof is in `SIC_SPARSE_PROOF.md`.

The subsequent peer majorization construction receives the ENTIRE
nine-weight Bell simplex qualitatively. I independently reconstructed
and accepted its finite eigenvalue argument in
`PEER_MAJORISATION_CHALLENGE.md`; attribution remains with the peer.
This closes finite Weyl-channel composition and every Bell seed's whole
white curve, hence its inherited arbitrary common-bath lift. The
quantitative five-weight receiver and the stronger source-specific
margin below remain separate acquired statements.

The exact reduction is `Delta(rho_p)=2S(sum p_i S_i)-H(p)`, where the
S_i are Hesse SIC projectors. Their pair overlaps fix output purity as
`(1+3sum p_i^2)/4`. Established sharp entropy/purity extrema reduce the
problem to one variable. A 39-cell exact rational cover proves the whole
interior, and an analytic tail covers every arbitrarily small nonzero
admixture near a pure vertex. The resulting per-source conservative
receiver needs only rational squaring/summing of the supplied weights.

## Shortest operational consequence and actual source

For the antisymmetric isometry `V|i>=sum_jk epsilon_ijk|jk>/sqrt2`,
`omega_p=(V tensor I)rho_p(V* tensor I)` extends the normalized qutrit
antisymmetric state, and
`I(Q1:Q2|R)_omega-log3=Delta(rho_p)`.
Thus every qutrit Weyl random-unitary squashing channel with at most five
nonzero branches is unable to reduce this CMI below log3, for all branch
probabilities. The branch label is actually discarded; retaining a
classical flag would give a different, already paid operation. This does
not bound arbitrary squashing channels or establish the full conjecture.

`compile_sparse_bell.py` acquired the literal rank-five Q(omega) source
with labels `(00,01,02,10,11)` and weights `(64,8,4,2,1)/79`.
Its reference dimension is three and antisymmetric extension dimension
27. All 243 extension partial-trace components check exactly. Its
conservative universal CMI excess is `515/199712` nats; the stronger
source-specific entropy-envelope receiver certifies `43/500` nats.
The complete exact source and both receivers are saved in
`outputs/SPARSE_BELL_SOURCE.json`. Matrix entry rational lengths are at
most eight bits. This is an acquired synthetic mathematical input.

## Equally informed ordinary comparator and paid boundary

Current Astra sources were read selectively at revision
`8d51d60762b3ee28c10aaaa56e1b92da119dc1cc`.
N1093 already proves the whole reduction-positive region `X<=3EX`,
including PPT/separable inputs. On this Bell simplex its premise is
exactly `max p_i<=1/3`; the acquired source violates it by `64/79>1/3`.
N1098 already proves a quantitative theorem whenever one orthonormal
eigenbasis has Schmidt rank at most two. That theorem pays all 3-by-2
inputs and, via purification duality, every rank-two source. Here every
nonzero eigenvalue is distinct and its eigenvector is a Schmidt-rank-three
Bell state. More strongly, fidelity `64/79>2/3` proves Schmidt number
three, excluding even any convex low-Schmidt decomposition.

The source has four zero eigenvalues, so it does not meet a faithful
condition-number<=24 premise (N1095). Five distinct positive eigenvalues
also exclude a direct projector/two-level representation. On the literal
reference-three slice, flat main plus white/rank-one reset (N1096) has
ranks 1,3,4 or9, not five; no nontrivial extra reference bath fits this
slice. Sol11 local-ray seeds are near a single Bell projector; these
arbitrary-weight mixtures include strong finite moves. These comparisons
are premise exclusions at the stated representation. They do not prove
exclusion from every known class under every alternate representation.

An equally informed ordinary method is allowed the Bell symmetry and
sharp Harremoes--Topsoe entropy/purity envelopes used here. Those tools
are established science. For a specified p it may diagonalize the same
three-by-three M_p, or certify its entropy using exact spectral intervals.
The useful construction is the finite universal positive-composition
receiver and its cheap rational input rule. There is no established
computational advantage over a tailored ordinary implementation, and no
historical novelty claim from this bounded source search.

## Acquisition and limits

Exact channel replay took about 0.130s; the complete scalar certificate
took 0.062s after imports, with 77 examined cells, 39 accepted cells,
depth eight, 78 square roots, 309 logs and maximal rational length 7,866
bits. The exact source/extension/strong receiver took 0.0112s; its
source-specific interval bound used 7,622-bit rationals. These observed
local runtimes exclude interpreter startup, paper/source retrieval,
human mathematical development, independent review and hardware.

For a rational k-branch model supplied as labels and weights (k<=5), the
universal receiver reads k weights, checks nonnegativity/normalization,
and computes `(1-sum p_i^2)/128` using O(k) rational operations. Bit cost
still includes the supplied probability numerators and denominators;
ordinary rational arithmetic has no free precision. If a full unknown
matrix is supplied instead, Bell diagonality, exact support and the
weight representation must first be acquired and verified. Twirling an
unknown source is not a proof for that original source.

No physical Weyl controls, calibrated source, tomography/support
certificate, random branch generator or qutrit isometry were acquired.
They remain part of any full experimental cycle. An assumption of exactly
five supported branches is not a finite-data certificate of exact zeros.
The proof is not a device or a quantitative advantage in a real system.

The sparse purity receiver alone does not pay support six through nine:
its relaxation becomes negative for support six without giving a negative
quantum deficit. The peer subsequently supplied an all-nine majorization
receiver, independently reconstructed in `PEER_MAJORISATION_CHALLENGE.md`.
This pays the entire Bell simplex, all its white curves and inherited
arbitrary common-bath lifts. Weyl convolution stays in that simplex, so
finite sequential Weyl-channel composition is also received. The sparse
theorem still supplies the explicit all-weight margin1/128; historical
priority remains unknown. A numerical curvature search is retained in
`outputs/SIC_CURVATURE_DIAGNOSTIC.json` only as a diagnostic, not as a
certified counterexample. The independent root all-white construction was
whole-read and accepted at its scope in `ROOT_WHITE_CURVE_REVIEW.md`.
Root's separate exact strong-source whole-white certificate was also
whole-reviewed and accepted in `ROOT_STRONG_WHITE_REVIEW.md`. Its literal
noncommuting bath has trace10, reference6, extension54 and certified CMI
excess1/100. Its finite Sturm/log receiver took0.377s including SymPy and
used at most14,115-bit entropy endpoints; no fresh duplicate acquisition
is claimed by this review.
The specific unpaid quantum-memory operation is recorded in
`FULL_SIC_TARGET.md`: independent noncommuting PSD matrix weights C_i on
the Bell labels, beyond commuting weights and the paid common affine
bath form. Scalar-to-quantum-memory entropy contraction is not automatic.
Unrestricted quantum entropy, arbitrary coherent positive composition,
historical priority, physical implementation and practical advantage
remain NOT_ESTABLISHED here.
