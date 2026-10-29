# A dimension-uniform information-thinning construction

The localizer is not limited to certifying exactly pair-supported output arrays or a tiny perturbation of one qubit example. A connected well-conditioned primitive yields a strict RELATIVE conditional-information gap. Constant-degree expanders turn that into a fixed global-erasure budget with only linearly many classical readout outcomes. The resulting erasure row has full input support and is outside the pair-output compiler.

## 1. General theorem: graph gap becomes a global-erasure budget

Use the notation and hypotheses of COHERENT_NEIGHBOURHOOD Sections1–3, but informational completeness and linear independence are not needed for the following inequality. Let

    V=sum_i <l_i,B_i l_i>=g_M(H)-g_ref(H_R).

The equality is the reference-gauge decomposition. The weighted-mean argument there gives V<=M sum_i||l_i-lbar||^2. Therefore, BEFORE converting to the Euclidean norm S0,

    g_E-g_F >= gamma (g_M-g_ref),
    gamma=delta*m*lambda_2(L_G)/(2M).                              (1)

Classical postprocessing cannot increase SLD, so

    0<=g_E-g_ref<=g_M-g_ref.

Let Er_gamma(E) be the measurement with effects ((1-gamma)E_y)_y and one additional effect gamma I. For 0<=gamma<=1 its complete SLD form is (1-gamma)g_E+gamma g_ref. Thus (1) implies

    Er_gamma(E) >=_complete SLD F,
    Er_gamma(E) >=_complete unrestricted Umegaki F.                 (2)

The latter step uses accepted N675. Equivalently, for finite divergence values and arbitrary states alpha,beta on A R,

    D(F_R alpha||F_R beta)-D(alpha_R||beta_R)
       <=(1-gamma)[D(E_R alpha||E_R beta)-D(alpha_R||beta_R)].        (3)

The unsubtracted flagged inequality (2) is the governing statement at support boundaries; infinity-minus-infinity is not defined. Setting beta=alpha_R tensor alpha_A gives the fully quantum mutual-information comparison

    I(R:F) <= (1-gamma) I(R:E),       for EVERY state on A R.        (4)

This has the form of a complete RELATIVE contraction coefficient in Belzig–Gao–Smith–Wu Definition7.1, not a contraction of D(E_R alpha||E_R beta) by a number below1 when reference marginals differ. Reference-only information is preserved and must be subtracted or flagged as in (2)–(3).

For a D-regular undirected multigraph, use every edge with w=1/(2D), BEC erasure e=3/10 and BSC crossover d=1/10, plus singleton filler1/2. Parallel edges retain distinct flags. A loop consumes two incidences and gives singleton rows, with zero edge loss. The graph Laplacian and Poincare inequality use the same multiplicities. Then

    delta=(4d(1-d)-e)/(2D)=3/(100D),
    gamma >= (3/200)(m/M)[lambda_2(L_G)/D].                         (5)

Consequently a fixed normalized expander gap and a fixed ratio m/M produce a positive gamma INDEPENDENT of both primitive outcome count and reference dimension. P has at most(3D/2+1)n outcomes, Q at most(D+1)n. No quadratic complete-graph edge table is necessary.

## 2. An explicit primitive using ordinary local Pauli measurements

Let d=2^q with q>=1. Enumerate the d^2-1 nonidentity Hermitian Pauli strings W_a, with W_a^2=I, Tr W_a=0 and Tr W_a W_b=d delta_ab. Put D0=d^2-1, m0=ceil(sqrt(2D0)), n=m0^2. Define

    M_(a,+)=(I+W_a/2)/n,
    M_(a,-)=(I-W_a/2)/n,       a=1,...,D0,
    M_c=I/n                    for n-2D0 additional labels.        (6)

They sum to I, span the input Hermitian space, and obey

    I/(2n)<=M_i<=3I/(2n),      hence m/M>=1/3.                     (7)

No SIC existence, latent-state preparation, untouched-reference access, or exponential state reconstruction is assumed. Equation(6) has a direct ordinary implementation: choose a Pauli label with probability2/n per a, measure its local single-qubit bases and take their parity, flip the parity with probability1/4, and output its sign. Each additional identity label has probability1/n. At most q local Pauli measurements and an exact rational choice suffice per use; a uniform n-ticket rejection uses fewer than2 ceil(log2 n) expected random bits, and the parity flip needs two fair bits. There are O(d^2) settings and labels: this is EXPONENTIAL in qubit count q, not an efficient many-qubit tomography or prediction claim. The primitive's absolute information about an arbitrary input may shrink with d. Our dimension-uniform statement is relative to this supplied primitive.

## 3. Standard explicit expander; no new graph claim

On vertices Z_(m0)^2 use the standard Margulis–Gabber–Galil multigraph. From each (x,y), create four undirected forward edges to

    (x+2y,y), (x+2y+1,y), (x,y+2x), (x,y+2x+1),

with modular arithmetic. Incoming inverse edges supply the other four incidences. This is8-regular including loop multiplicities. The credited Gabber–Galil bound is adjacency nontrivial eigenvalues in absolute value at most5sqrt2, so lambda_2(L)>=8-5sqrt2>4/5. Construction8.1/Theorem8.2 of Hoory–Linial–Wigderson2006 states this exact convention and credits Gabber–Galil1981. The source is acquired; expander construction and gap are ordinary antecedents, not inventions here.

HLW is a survey locator. The exact all-moduli convention and bound are also stated in the acquired primary research paper Gross–Eisert, Section2.2; its negative vertical shift is permutation-conjugate to our convention by R(x,y)=(-x,y). The four integer identities and visually checked printed spectral numerator are paid in SPECTRAL_SOURCE_BRIDGE.md/SPECTRAL_BRIDGE.json. The original GG/Jimbo–Maruoka proof bytes were not acquired; this is a named standard theorem import, not an independently re-proved spectral claim.

Equations(5) and(7) therefore give the rational all-q receiver

    gamma=1/2000,
    Er_(1/2000)(E) >=_complete unrestricted Umegaki F,
    I(R:F)<=1999/2000 I(R:E).                                    (8)

There are13n P outcomes and9n Q outcomes in the literal flagged construction (loops keep their three/two singleton flags). Global erasure adds one output. Each readout can be computed from eight local graph incidences without storing all edges; modular operations take O(log n) bit words. Compilation emits O(n) sparse classical row descriptions and O(n) one-Pauli effect descriptions. Explicit dense matrices would cost O(nd^2) entries and are not treated as free.

## 4. Exact nonsimulation and an input-domain discriminator

Relabel the primitive outcomes so that the +/- pair of one selected Pauli W_1 occupies neighbouring vertices(0,0) and(1,0). This requires only one fixed label swap. Prepare the two faithful mathematical inputs

    rho_+=(I+W_1/2)/d,       rho_-=(I-W_1/2)/d,

with equal prior. Their primitive signed probabilities are +1/(4n), -1/(4n), and0 elsewhere. Any support edge meeting just one nonzero score contributes the SAME guessing score under P and Q; an edge joining the two labels contributes a strict Q advantage. There is at least one such edge. Therefore

    p_guess(F)-p_guess(E) >=1/(640n)>0.                           (9)

Global erasure only lowers E's guessing success, so F also outperforms Er_(1/2000)(E). Hence the complete entropy order (8) has NO CPTP postprocessing simulator. Informational completeness alone is not used as a simulation theorem. This is a computable family in arbitrarily large qubit dimensions, not a complementary-channel/capacity construction.

The actual quantum primitive is load-bearing. On the LATENT unrestricted classical n-letter input, the same arrays Er_gamma(P),Q need not be ordered. For the executed graph, two nonadjacent vertices have disjoint P and Q output supports, so Q distinguishes that pair perfectly while the global erasure destroys gamma of its classical Fisher information. A faithful rational approximation gives an exact negative gap. The compiler records that classical witness and checks that its tiny coordinate probabilities violate the actual primitive bound p_i>=1/(2n). Thus one must not replace the supplied quantum-input cone by the full classical simplex, or infer a hidden classical-state actuator from the coefficient representation.

## 5. Executed generic-family receiver and comparison

compile_expander_family.py implements (6), the eight-incidence graph, all flagged rows including loops and parallel edges, the global erasure, exact degree/column normalization, the faithful classical domain counter, and the quantum binary scores. It emits EXPANDER_FAMILY.json plus its sparse input arrays. The finite query uses q=2 as a literal instantiation of an all-q theorem; it is not an additional fitted example, parameter search, or evidence for extrapolating an unproved scaling law. The graph spectral theorem pays all q; an exact LDL check separately qualifies the literal finite graph's rational4/5 gap.

The strongest ordinary comparator gets the SAME primitive, Pauli controls, complete graph/expander options, and matrix order bounds. It can reproduce the classical BEC/BSC design and standard spectral sparsification. The additional mathematical bridge here is the noncommutative weighted-score/coercivity lift giving a global erasure budget despite arbitrary quantum reference and overlapping readout pairs. This is not a faster graph constructor or a new expander theorem. Binary complete coefficients are already covered by Erikssonv2; that paper's unfiltered zero-Doeblin activation does not supply (8), because our strictly positive primitive restricts the accessible reference blocks. Belzig–Gao–Smith–Wu's general relative-expansion programme is also prior; this provides a concrete structured family of its complete mutual-information comparisons, not a solution for their arbitrary channel classes.

The capability gained is exact synthesis of a finite structured, dimension-uniform information-thinning relation with a computable constant and a known nonsimulation boundary. Practical sensing, record-compression savings, capacity activation, efficient many-body prediction, experimental acquisition and civilization-scale leverage remain NOT_ESTABLISHED. Those do not follow from an information order or from a constant relative coefficient.
