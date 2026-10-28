# Local simultaneous logical recovery with retained memory: acquired contractions and coherent extraction

28 October 2026. **New construction; independent receiving pending.** No source samples, simulated acquisition, hardware calls or performance advantage are claimed. Earlier received files remain immutable. This is one simultaneous q-logical payload, not q separate temporal uses. It does not import the growing-selector, approximate-locality or finite-time-tail extensions.

## 1. Physical contract and theorem target

Let 1<=q<=n and 1<=w<=n be integers. The receiver has a KNOWN n-qubit physical line P; each source call accepts q logical qubits through a fixed supplied encoder. It may prepare ordinary product states, measure every output qubit in a privately chosen Pauli basis, and implement known local controlled unitaries with paid routing. No calibration reference passes around the source. There is no output flag, source inverse, source gauge floor, environment reconstruction, or promise of reset.

The source retains arbitrary inaccessible quantum memory M. At each complete call its CP map has the form

    Efrak_t = Ad_(U tensor I_M') composed with
                sum_alpha (Ad_(P_alpha) tensor G_(alpha,t)),       (1)

where alpha ranges over q-qubit Paulis, U maps L tensor G to P, dim L=2^q, dim G=2^(n−q), and G_alpha:M→G M' are CP with sum_alpha Tr_G G_alpha trace preserving. U is fixed and unknown. The CP maps may change with time and exposed past history. This is an existence promise; the learner neither enumerates the4^q components nor stores a global2^n matrix.

For each i, the two true reflections

    B_(i,j)=U(sigma_j on L_i tensor I)U†,   j=X,Z,

are jointly supported in ONE unknown interval I_i of length at mostw. Their exact abstract logical algebras commute across i. For chi_(i,j)(alpha) defined by P_alpha sigma_(i,j) P_alpha=chi sigma_(i,j), require the uniform CP-order contrast promise

    H_(i,j):=sum_alpha chi_(i,j)(alpha)G_alpha,
    H_(i,j)−kappa G_total is CP,    0<kappa<=1,           (2)

where G_total=sum_alpha G_alpha. The supplied kappa is a positive RATIONAL lower bound on the margin; a larger real physical margin is used through this finite rational bound. All chosen positive numerical accuracy/implementation budgets, including nu and nu_rng, also have finite rational descriptions. Also G_total−H_(i,j) is CP, directly from the signed sum. The bound is supplied, not inferred from a fit, and applies to the actual conditional memory states after ANY allowed past records. To compare with the strongest full-CPTP joint recovery oracle, separately require

    G_I−G_alpha is CP for every alpha.                  (3)

Positive generator contrasts alone do NOT imply(3) whenq>1. The acquisition/extraction proof below remains valid without(3), but then its comparator is the stipulated ideal logical extraction rather than a claimed optimum.

All current private input labels, receiver choices, terminal time and computation timing are hidden through the COMPLETE current source port except for the quantum input itself. The current map is fixed/nonanticipating with respect to those fresh coins. Past measurement backaction on M is unrestricted. The initial full unknown payload Q and its arbitrary reference R are product with source/acquisition, and Q is held in trusted storage throughout acquisition. At the terminal call the decoder is frozen before seeing the unknown datum; its output is isolated and no update uses that datum. Storage, scheduling and control errors enter one complete-process budget, not a free initial-independence assumption.

Define W=min(n,3w−2), C=min(q,2W−1),

    K=min(q, W+2(C−1)(W−1)),    A=min(q,K²),
    R0=2^ceil(W/2),             G0=ceil(sqrt(5^W)).      (4)

R0 andG0 are known integers, with R0²<=2·2^W and G0²<=4·5^W. For rational0<epsilon<=1, set beta0=epsilon/8 and choose

    M0=n−w+1, d0=2^w,
    L0=ceil log2(2 d0 q M0/beta0),
    N0=ceil[256·12^w L0/kappa²],                        (5)
    N=least power of4 at least
                 [1152 A q R0 G0/(kappa epsilon)]².    (6)

The algorithm below uses at mostN0+N actual source calls, including the one simultaneous q-logical payload. On its declared ideal trusted-interface occupation, let R_* be the average Bell loss of D_*=Tr_G Ad_(U†) at the privately sampled fine-call time. With a whole-process complete discrepancy nu<=epsilon/4 for finite random/control/storage implementation, it achieves

    ell_joint(actual averaged payload channel)<=R_*+epsilon.       (7)

Under(3), R_* is the best FIXED full-CPTP recovery on those actually visited conditional memory states, and is also pointwise optimal at each such history. It is NOT the memory path produced by deploying that decoder throughout acquisition, not a future frozen-decoder guarantee, and not a per-record confidence certificate. There is no implicit dimension-free untwirled diamond conversion.

At fixedw, A is bounded independently ofq. The fine-call scale is

    O(A² q² 10^W/(kappa² epsilon²)),                    (8)

plus the logarithmic-in-n coarse call term(5). Total physical-qubit/readout traffic is O(n(N0+N)), not logarithmic in n. This deliberately retains the slow epsilon^(-2) rate. Its ordinary contraction learner is equally available to a conventional learner.

## 2. Actual product records, including overlap and quantum correlations

In every probe call measure ALL n output qubits, each in an independently uniform fresh Pauli axis a_l in{X,Y,Z}, obtaining b_l in{±1}. Save these actual labels/outcomes. For any interval J compute, purely classically,

    Z_J= tensor_(l in J) (3 Pi_(a_l,b_l)−I).            (9)

This is the standard local-Pauli shadow representation; see Huang–Kueng–Preskill, Proposition2, Eq.(S44), [primary manuscript](https://arxiv.org/pdf/2002.08953). We use its one-copy identity, not an iid state-estimation theorem. The following identities are proved here for the current arbitrary correlated marginal rho_J:

    E[Z_J]=rho_J,
    ||Z_J||op=2^|J|,       ||Z_J||F²=5^|J|,
    E[Z_J²]=(Phi^tensor|J|)(rho_J),  Phi(T)=T+2Tr(T)I
            =sum_(S subset J) 2^(|J|−|S|) rho_S tensor I_(J\S)
            <=3^|J| I.                                 (10)

For one qubit Z=(I+3b sigma_a)/2, Z²=(5I+3b sigma_a)/2. Averaging Born outcomes and the three axes gives E Z=rho and E Z²=rho+2I. Tensoring the linear measurement maps proves(10) for entangled states, without product-output assumptions. The norm equalities use eigenvalues2,−1 of each factor. The upper bound follows because every reduced density matrix is at mostI.

One physical record supplies the classical matrices for overlapping intervals; no output is cloned or measured incompatibly. All logical learners use conditional means given the ENTIRE PRIOR history, averaging over every other fresh input sign/axis and all current outcomes. We never condition a learner's asserted mean on other learners' current signs/outcomes. Joint record correlations and source-memory backaction are retained by the filtration. In particular deterministic cycling of measurement axes is NOT substituted: a time-varying source could otherwise make different coefficients refer to different conditional states.

For a current history h, after averaging the other logical inputs, write the physical output for input Pi_(j,s) on logicali as

    rho_h+s Delta_(i,j,h),
    rho_h=U(I_L/2^q tensor G_h)U†,
    Delta_(i,j,h)=B_(i,j) R_(i,j,h),
    kappa rho_h<=R_(i,j,h)<=rho_h.                       (11)

Here G_h is the emitted gauge density and R is obtained by replacing G_total by H_(i,j) in(2). The CP promise ensures these operator inequalities for the actual conditional memory state, including coherent retained memory. rho andR commute with every true logical generator. Extensions retaining M' satisfy the corresponding identities as well.

## 3. Count-acquired overlap localization with a fixed cap

ForN0 coarse calls prepare ALL q inputs in independent uniformly signed X eigenstates. For eachi and EVERY length-w intervalJ, accumulate the actual matrix s_i Z_J. Conditional on the prior record its mean is Delta_(i,X,h), reduced toJ. On any J containing I_i,

    ||(1/N0)sum_t E[s_i Z_J|past]||1>=kappa,             (12)

because the same fixed B_(i,X) pairs with each summand to give Tr R>=kappa. If J is DISJOINT from I_i, the conditional mean is exactlyzero at every step: conjugation by the local B_(i,Z) changes the sign of Delta_(i,X), leavesR invariant, and acts only on the subsystem traced out. This uses exact operator contrast, complementary-generator support and gauge commutation; generic locality alone would not justify it. Gauge aliases on overlapping patches are allowed.

Let X_t=s_i Z_J−E[s_i Z_J|past]. Its conditional mean iszero,

    ||X_t||op<=2d0,
    E[X_t²|past]=E[Z_J²|past]−Delta_J²<=3^w I.          (13)

The same formulas hold although differenti,J increments are correlated. Tropp's matrix Freedman Theorem1.2, applied to both signs of this one martingale, gives at a fixedN0

    Pr(||sum X_t/N0||op>=a)
      <=2d0 exp{−N0 a²/[2(3^w+2d0 a/3)]}.             (14)

The primary theorem's hypotheses are a self-adjoint martingale, an almost-sure increment upper bound and predictable quadratic-variation control; no within-copy or between-copy independence is imported. [Tropp, primary theorem](https://tropp.caltech.edu/papers/Tro11-Freedmans-Inequality.pdf).

Takea=kappa/(8d0). Equations(5),(14) and a union bound overqM0 processes give simultaneous trace-norm error at mostkappa/8 except probabilitybeta0. Indeed2(3^w+2d0a/3)<=4·3^w, and the exponent is at leastL0>=ln(2d0qM0/beta0).

Compute each known empirical trace-norm score to additive accuracykappa/16 using the finite backward diagonalization in §5. Choose the first interval with score>=kappa/2. On the simultaneous good event a true interval has score at least13kappa/16, whereas every disjoint interval has score at most3kappa/16. Hence every selected J_i overlaps I_i. Expand J_i by w−1 sites each side, clip to the physical boundary, and if necessary pad inside the line to a length-W interval W_i. It contains I_i. The algorithm learns these envelopes; none are supplied.

Color the known interval graph by a left-endpoint sweep. If no qualifying interval exists or more thanC colors are required, set a safe-replacement flag. Passing this guard is NOT evidence of source-family membership. On the good event the guard passes: every collection of envelopes covering one site fits inside at most2W−1 physical sites and contains that many independent commuting logical matrix algebras; their faithful joint representation requires at least one physical qubit per logical factor. Thus maximum overlap and interval chromatic number are at mostC.

For a total algorithm/comparator definition, even a flagged coarse history follows the fixed fine schedule with arbitrary predetermined patches and probe inputs; at its terminal source call it discards the physical output and returns the prescribed q-qubit replacement. It is not postselected away. Such histories cost at mostbeta0 to averaged Bell loss. All their calls/control caps count.

## 4. Learn observable contractions, not independently deployed decoders

On an unflagged coarse history initialize TWO independent Hermitian contraction iterates per logicali,

    A_(i,j,1)=0,      −I<=A_(i,j,t)<=I,   j=X,Z,

supported on its length-W envelope. They need not anticommute, and different logical learners need not commute. At fine stept all iterates and their possible extraction controls are frozen before any current outcomes. Prepare independent uniform axes j_i in{X,Z} and signs s_i for allq inputs. From the one actual product readout form

    g_(i,j,t)=−1{j_i=j} s_i Z_(W_i).                    (15)

For the linear loss and its common minimizer,

    L_(i,j,h)(A)=[1−Tr(A Delta_(i,j,h))]/2,
    e_(i,j,h)(A)=L(A)−L(B_(i,j))>=0,                    (16)

conditional expectation of(15) is the exact gradient −Delta/2 and ||g||F<=5^(W/2)<=G0. The factor1/2 from the input-axis draw is already the factor in(16); no extra importance factor is missing. These are computations from raw counts, not an oracle revealing the contrast matrix.

Use projected gradients with rational eta=R0/(G0 sqrtN):

    Y=A−eta g,    A_next≈Pi_[-I,I](Y),
    ||A_next−Pi(Y)||F<=u,   u=1/(16R0 N),              (17)

with EXACT Hermitian contraction feasibility and the fixed rational rounding scheme in §5. Starting atzero, ||B||F²=d=2^W<=R0² and the domain diameter is2sqrt d. Projection nonexpansiveness and(17) give pathwise

    sum_t <g_t,A_t−B>
      <=d/(2eta)+eta N G0²/2
         +N(4sqrt d u+u²)/(2eta)
      <=2 R0 G0 sqrtN.                                (18)

To check the last term,4sqrt d u<=1/(4N) and Nu²<=1/(256R0²N); it contributes less thanG0 sqrtN/(7R0), well within the displayed bound. Taking conditional expectations yields the same bound for sum_t E e_(i,j,h_t). Conditioning first on ANY good coarse history is legal: the local B is then feasible and the uniform CP contrast remains valid for every future memory state. No future iid bank or conditional-independence assertion is required.

Why does linear excess control the useful error? Set P=I−(AB+BA)/2>=0 for any Hermitian contractionA and reflectionB. SinceR,rho commute withB,

    e=(1/2)Tr(RP)>=(kappa/2)Tr(rho P),
    a:=Tr rho(A−B)²<=2Tr(rho P)<=4e/kappa.              (19)

The first inequality is operator order against a positiveP; it is not commutation ofA withR. The second usesA²<=I. Common B is therefore a pointwise optimizer despite arbitrarily large raw noise L(B). This is an excess-risk statement, not a small-raw-loss assumption.

## 5. Finite rational clipping, raw signs and physicality

Only KNOWN learned matrices are processed. Import the gap-free exactly-rational-unitary Jacobi primitive from §2 of `ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md`, SHA256 `8b5859b44e398d5d97d5b14580041bd9232b9fe59188a9c090634d6a4dbab0b6`, whose separate statistics receipt binds that final clarification. It uses at mostd² ceil log2(32d/zeta²) rational approximate two-coordinate rotations for a matrix in[0,I/2], with Frobenius off-diagonal residual<=zeta/4. Each rotation is EXACTLY unitary via rational stereographic quaternion coordinates; it is not a floating eigenbasis or an unknown eigenspace oracle. Finite precision is polynomial in matrix dimension, input bit length and log(1/zeta), with no eigengap premise.

For a general HermitianY with ||Y||op<=L, apply it toY/(4L)+I/4. Takezeta=tau/L. It produces an exactly rational unitaryQ and rational diagonalD with

    ||Y−Q D Q†||F<=tau.                                (20)

HereL=2+R0 is an integer upper bound for(17). Clip each diagonal entryD_ll to[−1,1] exactly. ThenP=Q clip(D) Q† is an EXACT rational contraction. The Frobenius projection onto the contraction ball is precisely spectral clipping and is nonexpansive, so ||P−Pi(Y)||F<=tau.

Settau=u/4 andt0=u/(16R0). Fix once the LARGEST dyadic grid meshv=2^(-k), k>=0, withv<=u/(64R0d). Round each real/imaginary upper-triangle entry ofP to that grid and impose Hermiticity exactly, obtainingPtilde with ||Ptilde−P||F<=2dv<=t0/2. Return

    A_next=Ptilde/(1+t0).                               (21)

Then ||A_next||op<=1 exactly and its additional Frobenius error is at mostt0(sqrt d+1/2)<u/8. This proves(17) with slack. All iterates have one predetermined rational denominator determined byv andt0, preventing recursive bit growth. Each step requires polynomial(d,logN,log(1/epsilon),log(1/kappa)) bit arithmetic apart from the explicit polynomial matrix dimensions; all local updates are paid. No channel SDP or arbitrary CPTP receiver is used during these probes.

For physical extraction, choose the LARGEST dyadicb=2^(-k), k>=0, with

    b²<=epsilon/(288Aq).                               (22)

Apply(20) to each currentA at toleranceb, writingC=Q D Q†. Define the exact-reference reflection

    S=Q diag(sign D_ll) Q†,  sign(0)=+1.                (23)

It is an EXACT rational Hermitian unitary even whenD has zero or nearly zero labels. No learner or source eigenvalue floor is assumed. The physical controlled unitary is synthesized to its declared operational tolerance; floating eigenvectors are never treated as exact controls.

For trueB commuting withrho, diagonalize rho,B jointly andC separately. Opposite signs ofB and an eigenvaluec ofC satisfy|B−c|>=1, including the chosen kernel sign. Summing weighted squared overlaps proves

    delta:=Tr rho(B−S)²<=4Tr rho(B−C)²
          <=8a+8b²<=32e/kappa+8b².                    (24)

This also proves the exact-sign inequality with constant4 atb=0. No learned Pauli relations are inferred or imposed. The same finite primitive computes a trace-norm score: use Frobenius residualtau<=kappa/(16d0), and sum absolute diagonal labels. Its trace-norm error is at mostsqrt(d0)tau<=kappa/16. All score/control computations can be padded to public worst-case durations.

## 6. One actual joint receiver, full Bell reference and causal cones

Use the known envelope color order fixed after coarse localization. Prepareq fresh receiver ancillasA_i each inI/2 by a private random bit and a reset; discard those preparation records. For eachi perform the actual three controlled reflections

    C_Z(S_Z)=((I+S_Z)/2) tensor I_A+((I−S_Z)/2) tensor X_A,
    C_X(S_X)=I_P tensor |0><0|_A+S_X tensor |1><1|_A,
    C_Z(S_Z), C_X(S_X), C_Z(S_Z).                        (25)

Keep ALL physical qubits and ancillas until these blocks finish, then discardP and keep allq ancillas jointly. Each gate is unitary for every learned reflection, even when learned generators fail every compatibility test. A collection of separately applied fitted CPTP decoders would not justify this joint channel and is deliberately NOT used.

The pointwise colored-cone proof from §§2–3 of the received `ordinary_colored_pooled_joint_recovery_20261028.md`, SHA256 `d63c30417caee39cc16f8b80f44bb01ac25933c7cab647f33897a651bdd22c47`, is imported ONLY as an algebraic receiver inequality, not its iid acquisition. Its bound is

    ell0_joint,h <=3A sum_i(delta_(i,Z,h)+delta_(i,X,h)/2).          (26)

Hereell0 is extraction loss for the virtual logical identity with the ACTUAL current total gauge stateG_h. The full referenceR, gauge purifier and ancilla purifiers are retained in its proof. It applies at each current conditional memory state: beforeU the physical+retained-memory marginal at global Bell input isI_L/2^q tensor G_(G M',h); after adjoining fresh mixed ancillas, EVERY ideal elementary controlled gate acts only on its distinct abstract logical factors and ancillas, so every ideal subset/prefix leaves this same physical+M'+ancilla marginal invariant. The ideal generators may overlap physically but are exact compatible abstract factors. Complete ideal i-SWAP recovers R_i.

For clarity, envelope locality is used to remove outside-cone gates in Heisenberg order separately for actual and ideal circuits, for arbitrary correlated states. Each backward cone has at mostK blocks, and each block appears in at mostK output cones by logical-algebra packing in its span. Comparing only those restricted actual/ideal circuits uses the invariant ideal prefix just stated. Their marginal Bell failures obeyp_i<=3|Anc(i)|sum_(j in Anc(i))(delta_Zj+delta_Xj/2). Summing the commuting Bell-failure operators proves3K² times the sum, and the global hybrid independently gives3q times the sum. This proves(26) withA=min(q,K²), without assuming independent marginal fidelities.

Combining(24),(26),

    ell0_joint,h <=(96A/kappa) sum_i(e_(i,Z,h)+e_(i,X,h)/2)
                       +36Aq b².                       (27)

Equations(18),(22) then give on each good coarse history

    (1/N)sum_t E ell0_joint,h_t
       <=288 A q R0 G0/(kappa sqrtN)+epsilon/8
       <=3epsilon/8.                                  (28)

## 7. From the ongoing probe history to a physical unknown payload

SampleT uniformly from{1,...,N} privately, independently of all source/probe/payload systems; it costslog2N fair bits. First perform the actualN0 coarse probes. Then perform only the firstT−1 fine probes, following the specified updates and controls. At fine callT send the held unknown q-qubit payload, apply the already frozen joint receiver(25), and perform no learner update from it. All hypothetical later probes in analysis are a mathematical all-probe extension, not additional actual calls. The complete ideal terminal channel is exactly

    Lambda=(1/N)sum_(t,h) p_t(h) D_(t,h) E_(t,h),        (29)

where h includes the complete coarse and fine-prefix records in THAT extension. Its initial payload/reference is product with them, so(29) holds for arbitrary entangled payload/reference input, not merely a maximally mixed marginal argument. This is the same private-terminal channel principle as the received one-qubit source `ordinary_prequential_terminal_memory_recovery_20261028.md` (SHA256 `20e59391aeab608e0fb76dbaee3fee6825d434991892a2c63fe5e57634316079`), now applied to oneq-qubit input and the constructed joint receiver. No independent decoder composition is inferred.

For each currenth, any decoder defines positive gauge Bell blocksT_alpha summing toI_G. WithD_* the common ideal extraction,

    ell(D E_h)−ell(D_* E_h)
      =sum_(alpha!=I) Tr[(G_(I,h)−G_(alpha,h))T_alpha]
      <=Tr[G_h(I−T_I)]=ell0_joint,h.                    (30)

The upper bound usesG_I−G_alpha<=G_total; pointwise nonnegativity and full-CPTP optimality additionally use(3). Thus(28), plus at mostbeta0 for bad coarse histories, bounds the ideal averaged excess byepsilon/2. A whole-process complete discrepancy nu<=epsilon/4 transfers actual service loss, leaving slack in(7). The comparator remains tied to the declared ideal-interface controller's occupation; this implementation allowance does NOT silently transfer it to different imperfect-controller memory histories.

Optional, separately paid: privately Pauli-frame the q inputs just before the terminal call and undo thoseq frames on the recovered outputs. With2q fresh bits andO(q) one-qubit controls, averaging makes the IDEAL entire terminal channel a Pauli channel. Its half-diamond distance to identity equals its global Bell loss. The same whole-q-input complete discrepancy transfers the operational bound by triangle inequality, even though the physically imperfect averaged channel need not be exactly Pauli. No untwirled dimension-free diamond guarantee is asserted and no key-conditioned authentication claim follows.

## 8. Complete source, bit, memory and control ledger

* The fixed call cap isN0+N, including one terminal simultaneousq-input call; a private early terminal time is paid, not a deterministic post-training service. Every calibration call preparesq single-qubit states and obtainsn local Pauli outcomes. There is no protected calibration reference and no cross-copy quantum workspace.
* The learner stores at mostqM0 coarse d0-by-d0 signed accumulators and2q fine d-by-d contraction matrices (d=2^W), plus current actual records. Full raw audit retention costsO((N0+N)(n+q)) symbols. Computation is polynomial in n,q,2^W,N and declared precision, not inlog of an arbitrary output dimension. The source's retained memory may be arbitrarily large and is not stored or characterized by the learner.
* Coarse scoring costsqM0 known-matrix diagonalizations. Each possible fine call pays2q finite contraction projections and2q backward sign computations/compilations, padded before the current role/input. Only the terminal receiver is coherently applied; probes use product Pauli readout. Each controlled reflection onW physical sites plus its ancilla has a generic dense synthesis costO(poly(W)4^W) before accuracy/routing overhead. Width remains a real exponential cost; the theorem is not efficient for arbitraryW growing linearly withn.
* The terminal receiver uses3q controlled local reflections, PLUS4q ancilla Hadamards when each of the two C_Z blocks is implemented by ancilla-basis conjugation of a controlled reflection. Alternatively those basis changes are included in synthesis of the full displayed C_Z matrix, not counted twice. It also usesq resets/mixing bits, alln+q data qubits until completion, and paid routing. Ancillas can start in an end block; move each distinct ancilla adjacent to its patch, execute its block, and reverse routing. At most2q(n+q) routing SWAPs restore physical and earlier-output positions. Net supports used by the cone proof are then exactlyW_i plus its own leaf ancilla. Color count is not claimed as the routed hardware depth. A fixed output endpoint adds only the explicitly required routing, not an automatic extra charge.
* Trusted input memory holds the fullq-qubit payload for up toN0+N call/computation periods. Computational padding, noisy memory, mixer preparation, gates, routing, measurement and random-sampler discrepancies must jointly satisfy ONE whole-process complete boundnu. Such a uniform physical accuracy interface is an assumption/budget, not certified by the mathematical fixtures.
* All measurement axes are sampled by two-bit rejection of the fourth value. LetB=N0+N andJ_rng=nB. Cap each atR_rng=ceil log2(4J_rng/nu_rng) trials, with0<nu_rng<=nu; total exhaustion probability<=J_rng 4^(−R_rng)<=nu_rng. Use a prescribed physical replacement on exhaustion. A conservative bit cap is log2N+qN0+2qN+2nB R_rng+q, plus2q if terminal Pauli frames are used. This countsq input signs, fine input-axis bits, alln output-axis choices and terminal mixed ancillas. Preparation/runtime maxima are fixed before outcomes.
* Only the coarse stage has a high-probability event, allocatedbeta0=epsilon/8. Fine acquisition uses conditional unbiasedness and pathwise regret in expectation, not an iid/tomography confidence assertion. Within-shot correlations, cross-learner correlations and adaptive memory persist. The fixed quantum model and supplied uniform operator contrast are not empirically inferred.

## 9. Conventional comparison, scope and remaining evidence

The equally informed conventional learner can use exactly the same product-Pauli records, martingale concentration, spectral clipping, rational controls and coherent extraction. Local shadows and online projected gradients are established machinery; the new question addressed is their paid composition into simultaneously compatible physical recovery under retained quantum memory. The received colored-cone result supplies the full-reference crosstalk mechanism. Reconstructing independent marginal channels and deploying them sequentially would not be an adequate comparator or proof, because those maps can erase other logical subsystems.

This construction removes reset and supplied patch location for a fixed common local algebra with supplied UNIFORM conditional contrasts. It does not learn an arbitrary changing algebra, infer model membership, supply drift prediction after a deterministic cutoff, optimize a growing encoder here, or promise small practical budgets. The separately received conservative bandit pilot remains negative evidence for practical generic-bandit constants, not evidence for this different local algorithm. Exact-source algebra/statistics fixtures and independent receipts will be separate. This file is not yet received.
