# Exact accepting polymers and a fixed-temperature undecidable order parameter in two dimensions

Research manuscript, 5 November 2026. Provisional result reviewed independently within the project; not externally peer reviewed.

## Abstract

We give an effective finite-alphabet, finite-range, integer-energy interaction on the square lattice at inverse temperature one whose exchange-odd order distinguishes halting from nonhalting. Auxiliary finite-group characters turn valid finite computation tableaux into an exact positive gas of accepting rectangles after summation, while invalid tableaux vanish by orthogonality. Uniform conditional high-temperature mixing identifies this representation for every physical Gibbs state. A pressure comparison and entropy-preserving recoloring give conditional Edwards–Sokal domination without spin FKG. In the halting branch, infinitely many positive-activity equality bridges join the two ordered Ising backbones; finite disagreement-component swaps then give zero odd expectations and exponential odd correlations in every translation-invariant Gibbs state. In the nonhalting branch the spin specification is exactly two independent ordered Ising models. The argument uses no sparse-independent-defect assumption and no reliable noisy computation.

## Reading conventions

Theorem and proof map appear first; Appendices A–F contain the complete detailed constructions and proofs used by that map, in this same file. Numbered section references inside an appendix are local to that appendix unless another appendix is named. The physical mismatch energy is K=6; the equivalent Ising Boltzmann-exponent coefficient is J=K/2=3. All hard constraints mentioned in the dual or Edwards–Sokal representations are proof devices; the physical model has only finite integer energies.

## 1. Precise theorem

There is an effective procedure which, from a deterministic Turing machine M and a prescribed finite input, produces:

- a finite alphabet S_M;
- a translation-invariant finite-range classical interaction on Z² with finite, nonnegative integer-valued local energies;
- an on-site involution tau;
- an on-site observable O in {−1,0,+1}, odd under tau;

such that, at the fixed inverse temperature beta=1:

1. If M does not halt, there are translation-invariant Gibbs states mu_+,mu_- exchanged by tau with E_mu+ O>1/2 and E_mu- O<−1/2. Their equal mixture has mean zero and nondecaying O two-point correlations, in fact bounded below by a fixed positive constant at every separation.
2. If M halts, every translation-invariant Gibbs state has E O=0 and

       |E[O_0 O_x]| <= C exp(−c ||x||_infinity).

   For example one may take C=10 and c=log(100/3), independently of M, by the explicit contour tail below. Full Gibbs-state uniqueness is neither claimed nor needed. More generally, every bounded local exchange-odd observable has zero mean, and separated exchange-odd correlations decay exponentially.

The lattice dimension, interaction support shapes, beta, and Ising energy scale are fixed. Only the finite alphabet and its explicit local energy table depend on the machine. No halting-time estimate is used to choose a coupling or cutoff.

Consequently no algorithm can decide, for all interactions in this effective family, which of these two mutually exclusive observable-specific TI Gibbs behaviors occurs. This statement is not a one-sided all-equilibria expectation promise: the nonhalting branch has both positive and negative ordered means.

## 2. The effective finite local model

Compile the machine into the labeled Wang set T of Appendix A; write t=|T|. Its finite nonzero-edge components are exactly valid accepting computation rectangles. Each such component has one marked top-left anchor. A finite component exists if and only if M halts.

Let G=(Z/2Z)^m have enough characters to label every edge color injectively, with exterior color0 assigned the trivial character. Put group variables g_e on lattice edges. At each site put two Ising spins s_v,r_v and a multiplicity variable b_v in {1,...,D}, where

    C0=10000(t+1),      D=C0+t.

For a tile z, let Chi_z be the product of its four edge characters and let I_z=1 except that a marked tile has I_z=1[s_v=r_v]. Define

    F_v=sum_{z in T} Chi_z I_z,       |F_v|<=t.

The site-factor energy is

    E_v=0 if b_v<=C0+F_v, and E_v=1 otherwise.

For each nearest-neighbor pair and each Ising layer, assign mismatch energy6. Thus the physical edge energy is

    6·1[s_v!=s_w]+6·1[r_v!=r_w].

Every local energy is a finite nonnegative integer. The involution exchanges s and r and fixes g and b; set O=(s-r)/2.

To obtain an ordinary site alphabet, store the east and north edge variables at their lower/left endpoint. Then

    |S_M|=4D |G|².

The site factor centered at v reads only v,v−e_1,v−e_2; the Ising factors are nearest-neighbor. These support shapes are fixed independently of M. The auxiliary multiplicity threshold is an explicit finite table, not an infinite-energy constraint.

At beta1, summing b_v gives the strictly positive factor

    C[1+a F_v],
    C=C0+t exp(−1),
    a=(1−exp(−1))/C.

The number a is not a prescribed noninteger energy. It is the exact consequence of summing a finite number of states with energies0 and1.

The small parameters obey

    u=at<10^(-4),
    16 exp(2) t a <0.012.

Thus conditioned auxiliary-edge Dobrushin mixing and the positive polymer cluster expansion have a uniform, generous convergence margin.

## 3. Exact certificates, not noisy acceptance

With all dangling group edges freely integrated in a finite volume, character orthogonality forces exact matching of the selected tiles and color0 on their exterior. Hence the normalized auxiliary partition function is exactly

    Xi_V(s,r)=sum_{compatible accepting rectangles gamma contained in V}
                    product_gamma a^{|gamma|} 1[s_anchor=r_anchor].

The sum is over collections of vertex-disjoint tableau-labeled rectangles; touching along zero edges is allowed. There are no false accepting tableaux with a small but positive error weight. Their Fourier terms vanish exactly.

This finite identity is not used to exclude arbitrary-boundary or infinite Fourier supports by assertion. The next step does that at the level actually needed, namely the induced spin specification.

## 4. Every physical Gibbs state enters the same positive representation

Appendix D proves the arbitrary-state statement.

Conditioned on a complete spin configuration, the group-edge model is uniformly Dobrushin unique. For a finite spin change, its marginal odds are the bare Ising odds multiplied by the expectation of the local factor ratio under that unique group law. Uniform boundary mixing identifies this expectation with the limit of free-boundary partition ratios. The exact Fourier formula identifies those ratios with Xi ratios.

The resulting spin interaction is the two bare Ising layers plus the absolutely summable accepting-polymer induced interaction. Every physical Gibbs spin marginal, not just a free-boundary limit, is Gibbs for it.

For the positive lift, fix an aligned reference in a finite spin region. Other assignments are obtained by forbidding polymer anchors at the newly unequal sites. The associated conditional-vacancy probabilities cancel the induced spin normalizers exactly. Thus every physical spin marginal has a canonical positive polymer extension in which:

- given the spins, polymers form the small-activity hard-core gas;
- given the polymers, spins have the bare two-Ising specification with forced equality at occupied anchors.

This also proves converse lifting for the exactly decoupled nonhalting branch.

## 5. The nonhalting branch

When M does not halt, the finite polymer family is empty, so Xi_V is identically1. Every physical Gibbs spin marginal has exactly the uncoupled pair-Ising specification. Lift the product plus/minus and minus/plus Ising states to obtain the two required TI physical states.

An elementary Peierls estimate gives a fixed quantitative margin. For the plus phase of one mismatch-energy6 Ising layer, put

    r=3 exp(−6),
    epsilon=4 sum_{n>=4} n r^n
           =4 r^4 [4/(1−r)+r/(1−r)^2]
           <4.94·10^(-8).

Then P(s_0=−1)<=epsilon, so its magnetization is at least1−2epsilon>1/2. In the product plus/minus state, O=1 unless one of the two spins is a minority spin, an event of probability at most2epsilon. At any two sites, a union bound yields

    E[O_0 O_x]>=1−8epsilon>1/4.

The layer-swapped state has the same two-point function and opposite mean. Their equal mixture has zero mean and the same uniform positive correlation lower bound. No limiting clustering assumption is needed for this witness.

## 6. The all-TI step: pressure and recoloring, not spin FKG

Appendix E proves the step that is not supplied by a finite-volume FK formula alone.

The canonical polymer lift is an equilibrium measure of a local hard-tile representation. Its pressure agrees with unrestricted hard-tile pressure because freely integrated dangling group variables impose zero tile colors, whereas dangling variables fixed to the group identity permit every boundary color. Positivity of the physical factors bounds the ratio by exp(O(boundary)). The canonical gas entropy identity has only boundary-order errors from crossing polymers, by their exponential activity tails.

Add Edwards–Sokal horizontal bonds in the two layers. Recolor every infinite full FK component to plus, leaving all bonds and polymers unchanged. Energy is unchanged, and block entropy changes by at most one bit for each boundary-touching graph component, hence by O(boundary). The recolored law remains an equilibrium measure. The Lanford–Ruelle theorem for an arbitrary SFT then supplies its local DLR property. No converse assertion for arbitrary frozen hard-tile Gibbs sectors is used.

This yields, for the ORIGINAL bond/polymer marginal, the horizontal conditional bound

    P(edge open | every other bond and all polymers)
        >= tanh(3).

The two-layer horizontal bond field therefore dominates independent Bernoulli(tanh3) bonds jointly, conditionally on the entire polymer configuration. Their projected intersection is iid with parameter

    q=tanh²(3)>0.99,

and can be coupled independently of all polymers.

The induced finite-volume spin weights need not be log-supermodular: competition between two diagonally offset accepting rectangles gives a negative lattice-condition determinant under a fixed exterior. This excludes the usual FKG lattice-condition argument and conditional attractiveness; it does not by itself disprove every unconditional association inequality. The proof uses none of these order properties.

## 7. The halting branch and the exact odd-component cancellation

Appendix F supplies the final argument.

Suppose M halts and fix one finite accepting species gamma_* of positive activity. Finite physical energies give infinitely many aligned sites almost surely. Conditional on a spin configuration with infinitely many eligible anchors, finite-species polymer DLR excludes a finite total polymer collection: n mutually disjoint far-away candidates have empty probability at most (1+w_*)^(−n). Consequently there are infinitely many occupied anchors almost surely.

An infinite set independent of supercritical iid percolation intersects its unique infinite cluster almost surely. Applying this to the occupied anchors and the independent common lower field gives an occupied equality bridge on its infinite cluster C. Therefore both layer copies of C belong to one full FK component.

At q>0.99, every nearest-neighbor component of Z² minus C is finite and has an exponential radius tail. A direct closed-dual-contour bound gives, with R=||x||_infinity and alpha=3(1−q),

    P(0 connected to x in Z² minus C)
       <= sum_{n>=max(4,2R)} 4n alpha^n.

Any infinite full FK component must contain a layer copy of C, because its projection cannot remain in one finite complementary hole. The bridge thus makes the full FK infinite component unique.

Let D={v:s_v!=r_v}. Both copies of C have the same spin color, so D lies in Z² minus C and has only finite components. Swapping the two physical spins on any one such component preserves every local physical energy: internal edges are layer-swapped, boundary neighbors are aligned, and all Fourier factors depend on the spins only through their equality indicator. Finite-volume DLR makes this an exact measure-preserving involution.

It cancels E O and cancels E[O_0 O_x] unless0 and x lie in the same D component. For a direct bound put beta0=3/100. For R>=2, the tail divided by beta0^R is at most4 beta0(3−beta0)/(1−beta0)^3=356400/912673<1, using R beta0^R<=beta0/(1−beta0)^2. The cases R=0,1 follow directly from the same geometric series. In particular the tail is at most10·(0.03)^R for all integer R>=0. This proves the constants stated in the theorem and exponential decay for every TI physical Gibbs state. A finite union of components gives the same conclusion for all bounded local exchange-odd observables.

The accepting activity can be arbitrarily tiny. Only its strict positivity is used to obtain infinitely many anchors and one bridge. No absolute perturbation error is compared with a late-halting activity.


## 8. Status, standard inputs, and limitations

No construction-specific implication is left as an unproved hypothesis in the assembled argument. Independent internal assembly and end-to-end adversarial reviews have been completed. This is a research proof, not a claim of external peer review.

The standard analytic results used are: the Dobrushin uniqueness/comparison criterion for finite-alphabet inhomogeneous specifications; the Kotecký–Preiss low-activity hard-core polymer expansion; the relative entropy-rate chain rule; the Gibbs/equilibrium variational principle on the full shift for exponentially summable interactions; and the equilibrium-to-Gibbs direction of Lanford–Ruelle on an SFT. The numerical hypotheses for the first two are checked below. The hard-constraint variational direction is stated precisely in Appendix E, and its role is restricted to equilibrium measures obtained there.

The result classifies the specified exchange-odd observables in translation-invariant Gibbs states. It does not claim uniqueness of the full Gibbs measure, classification of non-translation-invariant Gibbs states, or an algorithmically bounded crossover size for a late-halting machine. Infinite dual tile components are not ruled out pointwise; their possible pressure and projection effects are controlled analytically. Reliable noisy self-organization is not assumed or used by this proof.

## 9. Sources for standard tools

- R. L. Dobrushin, uniqueness and comparison criteria for Gibbs random fields; the elementary single-edge influence computation used here is given in Appendix B.
- R. Kotecký and D. Preiss, *Cluster expansion for abstract polymer models*, Communications in Mathematical Physics 103 (1986), 491–498. The weighted incompatible-polymer sum is checked explicitly in Appendix B/C.
- T. Meyerovitch, *Gibbs and equilibrium measures for some families of subshifts*, arXiv:0903.1426, Section3. Its stated Lanford–Ruelle theorem applies to any SFT and a potential with d-summable variation. Condition(D) occurs only in the converse Gibbs-to-equilibrium statement. https://arxiv.org/pdf/0903.1426

The square-lattice high-density percolation bound is proved by closed dual contours in Appendix F; no sharp percolation threshold is used. The nonhalting magnetization margin is proved by the elementary Peierls bound in Section5 above.


## Appendix A. Effective finite accepting-tableau compiler

### 1. Result and scope

For every machine/input pair (M,w), the algorithm below produces a finite alphabet of edge colors, a distinguished color 0, and a finite set of labeled Wang tiles. Every finite nonzero-edge-connected component in a color-matching configuration on Z², with vacuum outside the selected tiles, is a solid rectangle of width and height at least two. It contains exactly one marked tile. Its rows encode a genuine bounded-width computation of M from w, and its final row contains a genuine halting state. A finite component exists if and only if M halts on w.

There is no additional possibility of a finite headless cycle, a ring with a hole, or a nonaccepting component. Different rectangles may touch across zero-colored edges without being in the same component.

This is a finite-component statement, not a claim that all bi-infinite matching configurations are accepting rectangles. Infinite planes, strips, and periodic winding components are not excluded by the grammar. They must be handled by the separate uniform auxiliary mixing/projection argument. In particular, a free-dangling-edge Fourier identity must not be replaced by a periodic-volume identity without accounting for winding terms.

### 2. Normalize the machine without a cleanup assumption

A cleanup sweep and an all-ACCEPT top row are unnecessary. A finite horizontal automaton can check that the top row contains exactly one halting head and no other head.

First make halting absorbing and complete the transition table on every nonhalting state/symbol pair. A missing transition of the original machine can be redirected to the distinguished halt state if that is its halting convention. Introduce a distinct absorbing reject state.

A two-sided tape is represented on a one-sided physical tape. Physical cell j >= 0 stores a pair (A_j,B_j), representing original cells j and -j-1. A head has a machine state and a track bit A or B. Its moves are:

- Track A, original right: physical right, keep A.
- Track A, original left away from j=0: physical left, keep A.
- Track A, original left at j=0: stay in the same physical cell, switch to B.
- Track B, original left: physical right, keep B.
- Track B, original right away from j=0: physical left, keep B.
- Track B, original right at j=0: stay in the same physical cell, switch to A.

The transition writes only the selected component of the symbol pair. Each physical cell carries a permanent bit b, equal to one exactly at j=0. This makes the move rule local. The other component of a pair is retained. Thus one original step is one physical step, including a track switch at the origin.

On an interval of width W, a move through the right wall instead leaves an absorbing reject head at its source cell, after the prescribed write. It cannot create a halt head. A physical move through the left wall is likewise rejecting, although valid folded histories never request one. Importantly, overflow takes precedence even if the same original transition changes the state to HALT. This only rejects some narrow certificates; a sufficiently wide interval reproduces every finite genuinely halting history.

The finite cell alphabet Sigma consists of:

- A pair of tape symbols, the bit b, and no head.
- A pair of tape symbols, the bit b, a machine state (including HALT and REJECT), and a track bit.
- A poison letter for each b, used only to totalize malformed local inputs.

Let # be an outside-wall symbol, not in Sigma.

### 3. A completely local radius-one update

The deterministic map F: (Sigma union {#})^3 -> Sigma is needed only on triples whose center lies in Sigma. It is defined as follows, with a deterministic poison convention on malformed cases.

Every nonhalting/nonreject head computes its write, new state, new track, and physical displacement from its old state, selected tape symbol, track, and permanent bit. HALT and REJECT compute a stay-put identity update. A head's proposed motion can be computed from its own letter alone; whether the target is # is then visible in its centered triple.

For a center letter x:

1. Its output symbol pair is its own prescribed write if x carries a head, and its unchanged pair otherwise. Its permanent bit is copied.
2. A head whose displacement is zero remains at the center with its new state/track.
3. A head moving into an outside wall remains at the center as REJECT.
4. A head moving to an actual neighbor leaves no head at its old cell.
5. An incoming head proposal from the left or right neighbor installs that proposal's new state/track at the center, using the center's output symbol pair.
6. Conflicting head proposals, an incoming head entering an already occupied center, any poison in the triple, or other malformed symbol data produce the poison letter with the center's permanent bit. Any case not covered above is assigned this same poison output.

For the valid one-head configurations reached from the prescribed initial row, rules 1-5 alone apply. Their output has exactly one head: an ordinary simulated head, HALT, or absorbing REJECT. The global update is precisely the bounded-width folded simulation. The table is finite and effective. There is no nondeterministic choice of a purported successor.

The poison behavior is not relied upon to establish soundness: the exact bottom row and the deterministic one-head invariant already exclude all malformed histories.

### 4. Two explicit finite row automata

Let P be the finite folded input prefix of length ell >= 1. At cell zero it contains the initial head on track A and permanent bit one. All other prefix cells have no head and bit zero. Unused tape components are blank. Let z be the blank, headless, bit-zero cell letter. The bottom-row language is exactly

    P z*.

The geometric width restriction already requires W >= 2. In particular, the bottom automaton does not accept a prefix of P. The DFA states are 0,...,ell plus a rejecting sink. From state i<ell, the only nonrejecting letter is P_i and the next state is i+1. From state ell, the only nonrejecting letter is z and the state remains ell. Start state is 0; sole accepting state is ell. Undefined transitions enter the rejecting sink, which is never accepted.

The top-row DFA has states unseen, seen, and dead. A headless nonpoison letter leaves unseen or seen unchanged. A HALT-head letter changes unseen to seen. A second HALT head, any other head, or any poison enters dead. Start is unseen; sole accepting state is seen. Thus its language has exactly one HALT head and otherwise plain tape letters.

For interior rows use the one-state DFA that accepts every letter in Sigma. Tile conditions separately require the permanent bit of the center letter to be one exactly in the leftmost column, at every height.

### 5. Complete finite tile generation algorithm

A candidate tile is the finite tuple

    (h,v,p,x,q,k_minus,k_plus),

where h is L,I,R; v is B,I,T; p,q are in Sigma union {#}; x is in Sigma; and k_minus,k_plus are states of the row DFA selected by v. Enumerate all such tuples and retain exactly those satisfying:

1. p=# iff h=L, and q=# iff h=R. Thus all other p,q are in Sigma.
2. The permanent bit of x is one iff h=L.
3. k_plus is the DFA transition from k_minus on letter x, and neither state is dead/rejecting.
4. If h=L then k_minus is the DFA start state.
5. If h=R then k_plus is an accepting DFA state.

Put y=F(p,x,q). The four edge colors are the following finite tuples, with every displayed tuple a nonzero color:

    West  = 0                  if h=L,
            (H,v,p,x,k_minus)  otherwise.
    East  = 0                  if h=R,
            (H,v,x,q,k_plus)   otherwise.
    South = 0                  if v=B,
            (V,h,x)            otherwise.
    North = 0                  if v=T,
            (V,h,y)            otherwise.

H and V are distinct formal tags. The single symbol 0 is distinct from every tuple, including tuples carrying blank tape letters or numerical DFA state zero. Mark the tile iff (h,v)=(L,T).

This algorithm is the tile set; it only enumerates finite alphabets and evaluates finite transition tables. It is not an oracle for whether an accepting rectangle exists. Labeled duplicates with the same four colors may be retained as distinct tile species, or deduplicated together with their mark. Retaining them merely changes positive multiplicities, never the existence or validity of a component. For a quantitative Fourier implementation, use the count of retained labeled types consistently.

### 6. Proof that all finite components are accepting rectangles

Every selected tile has at least one nonzero horizontal edge and one nonzero vertical edge. At a nonzero edge, color matching forces a selected neighboring tile in the same component.

Take a finite component and a tile at its minimum y-coordinate. Its south edge must be zero, so it has v=B. Follow its horizontal nonzero edges. Finiteness forces a row beginning with h=L and ending with h=R, with h=I between them. Every nonzero horizontal edge carries v, so the whole row has v=B. Neither an internal gap nor a premature L/R is possible: zero cannot match a nonzero color.

Every cell of this bottom row has a nonzero north edge. The matching row above has exactly the same h sequence, because vertical colors carry h. Its leftmost and rightmost cells therefore cannot extend the row horizontally. Horizontal colors give it one common v, which is I or T because its south edges are nonzero. Repeat. Finiteness forces a T row, and a T row has no nonzero north edge. There can be no extra cells connected beyond the resulting rectangle: its complete exterior boundary is color zero. A hole, a ragged row, or a branch would contradict this induction. Because L and R are distinct choices, and B and T are distinct choices, both dimensions are at least two.

In each row, matching overlapping horizontal colors forces the stored triples to be the consecutive triples of one word x_0...x_(W-1), with # immediately outside the two ends. The DFA states match too. Consequently the bottom word is exactly P z*, the top word contains exactly one HALT head, and each interior word has no extra filter.

Vertical matching forces x_i of the next row to equal F of the preceding row's triple, for every i. The bottom row is the true initial one-head configuration, so induction gives the unique finite-interval simulation. A right-wall collision enters REJECT forever and cannot meet the top filter. Hence a valid rectangle certifies genuine halting before any boundary failure. The marked tile is exactly its unique top-left corner.

Conversely, if M halts after t original steps, choose W >= 2 large enough to contain every folded position used by those steps and the complete input. The bounded-width simulation then reaches HALT with no rejection. Stack the initial configuration and its successive images, continuing the absorbing halt state if needed so that height is at least two. Take its first row as B, last row as T, and all others as I. Their overlapping triples and accepting DFA runs give exactly the prescribed tiles and matching colors. This constructs a finite component.

### 7. Positivity and exact integer-energy realization

The existing ancillary realization is correct. Let t be the number of labeled tile types. Inject the edge-color set into the character labels of G=(Z/2Z)^m, with color zero sent to the trivial character. Taking 2^m at least the number of colors is enough. Assign distinct nonzero characters to distinct nonzero colors.

For a vertex define

    F_v = sum_t Chi_t(g) I_t(s_v,r_v),

where I_t is one except on marked tiles, where it is 1[s_v=r_v]. F_v is an integer in [-t,t]. Choose computable integers C0>t and D=C0+t. With a_v in {1,...,D}, assign local energy zero to a_v <= C0+F_v and energy one to the remaining values. Both numbers of ancillary states are nonnegative integers, and the zero-energy count is strictly positive. At inverse temperature one its exact sum is

    W_v = C0 + t exp(-1) + (1-exp(-1)) F_v
        = C (1+a F_v),
    a = (1-exp(-1))/(C0+t exp(-1)).

Thus W_v>0 and a<1/C0. For the auxiliary uniqueness estimate alone C0=101t+1 would give a t<1/100. The assembled construction uses the larger C0=10000(t+1), which also ensures the stated polymer-expansion margin, without consulting a halting time. The group and ancillary alphabets may be large but are finite and computable from M,w. Together with integer Ising bond energies, every physical energy is integer-valued. No physical coupling is set to a noncomputable real.

Store north/east edge group variables at each lattice site. Each local factor then reads its own pair and the corresponding west/south neighboring variables. This is an ordinary translation-invariant finite-range finite-alphabet lattice interaction.

Under a free auxiliary boundary, normalized Haar summation imposes equality of colors at internal edges and color zero at dangling edges. Expanding each local factor into its vacuum term or one labeled tile term gives only the accepting rectangles proved above. One marked tile contributes exactly one alignment indicator. The surviving expansion is a nonnegative hard-core gas of these complete rectangle species, allowing contact along zero edges.

### 8. What this audit does not acquire

The grammar and positive finite-energy realization are closed. The arbitrary-boundary infinite-volume spin projection is proved separately in Appendix D, and the sufficient all-TI exchange-odd decay statement is proved in Appendices E–F. These are not consequences of the grammar alone; no classification into exactly two full Gibbs phases is asserted. In particular, local positivity is not an FKG proof for the hard-core polymer marginal.

### 9. Reproducible checks

`checks/check_explicit_tableau_grammar.py` is an executable implementation of the tile generator, including the folded local update. Its rectangle counter does not call the update rule or row automata: it assembles the generated Wang colors directly. The resulting counts are compared with independently iterated machine histories.

The run recorded in `checks/explicit_tableau_grammar_results.json` passed 84 combinations of widths 2-4 and heights 2-5 across seven machines: immediate halting, stationary nonhalting, right-overflow nonhalting, left-fold nonhalting, halting after crossing the fold in both directions, a halting transition rejected at width two but accepted at width three, and an initially halting machine. The generated sets have 1,824 to 6,560 labeled tile types in these one-symbol examples.

A separate exhaustive status-only enumeration allows vacuum, side-touching rectangles, and all nine (h,v) tile statuses. It checked all closed assignments in 2x2, 3x3, 4x4, and 5x4 boxes: respectively 2, 10, 128, and 544 assignments, containing 1, 9, 240, and 1,264 finite components. Every component was a solid rectangle with exactly one marked corner. The proof above, rather than these finite tests, covers arbitrary sizes and machines.

The ancillary identity was checked exactly as a polynomial in x=exp(-1), including both extreme values F=+-t. No floating-point positivity or numerical nonhalting test is used. An independent signed-tape implementation also tested 160 random two-symbol/three-state machines, 923 finite-width trajectories and 21,532 exact state/tape comparisons, including both fold directions, writes, overflow and absorbing HALT; all passed. These finite tests are supplementary checks, not premises of the arbitrary-machine proof.


## Appendix B. Local Fourier and conditional-mixing audit

### 1. Integer energies give the stated local factor exactly

Let T be a finite set of Wang tiles, each with four colors in an injectively labeled subset of the character group of G=(Z/2Z)^m. Reserve character 0 for the exterior color. At each undirected lattice edge put a uniformly counted variable g_e in G. For spins s_v,r_v in {−1,+1}, write

F_v(g,s,r) = sum_{t in T} I_t(s_v,r_v) product_{e incident v} chi_{c_e(t)}(g_e),

where I_t is either 1 or 1[s_v=r_v]. Then F_v is an integer and |F_v|≤t0:=|T|. Let C0,D,K_aux be positive integers satisfying C0>t0 and D≥C0+t0. Add a local ancilla j_v in {1,...,D}, with energy 0 when j_v≤C0+F_v, and K_aux otherwise. Exactly summing j_v gives

W_v = Ceff +(1−exp(−K_aux))F_v,
Ceff = D exp(−K_aux)+(1−exp(−K_aux))C0.

Thus W_v/Ceff=1+aF_v, a=(1−exp(−K_aux))/Ceff>0. Every microscopic energy is an integer, and every microscopic Boltzmann weight is strictly positive. F_v may be negative without causing a problem. Also a≤1/C0, so C0≥64t0+1 gives epsilon:=a t0<1/64. No approximation of exp(−K_aux), and no noninteger microscopic coupling, is used. K_aux=1 is already sufficient for this small-activity choice.

Store the east and north edge variables at their southwest endpoint, for example. Each site factor then uses finitely many neighboring site coordinates. This is a finite-alphabet, translation-invariant finite-range model. Independent Ising interactions with mismatch energy K=6 preserve the integer-energy property.

### 2. Exact finite-volume character expansion

Expand product_v(1+aF_v), choosing at most one tile at every selected vertex. On each integrated edge, character orthogonality gives

|G|^(−1) sum_g chi_c(g)chi_d(g)=1[c=d].

On a dangling edge with only one selected endpoint, it gives 1[c=0]. Consequently, with all dangling edge variables freely integrated, surviving terms are precisely finite colored components whose nonzero colors match across internal edges and whose external colors are zero. All surviving term weights are nonnegative: a per selected tile, and an equality indicator at each marked corner. Signs occur before edge summation, not in the final finite polymer weights.

With fixed dangling edge variables, unmatched nonzero boundary characters may survive. Their signs need not be positive. A boundary-insensitive argument is therefore needed before passing to arbitrary Gibbs states.

### 3. Finite nonzero-edge components really are rectangles

The required grammar must be enforced as follows. Every tile has h in {L,I,R} and v in {B,I,T}.

- West is zero exactly when h=L; east is zero exactly when h=R.
- South is zero exactly when v=B; north is zero exactly when v=T.
- Nonzero horizontal matches preserve v, and go from h in {L,I} to h in {I,R}.
- Nonzero vertical matches preserve h, and go from v in {B,I} to v in {I,T}.
- All tableau/geometry internal colors are nonzero, and distinct labels are not accidentally identified in G.

In a finite nonzero-edge component, each maximal horizontal segment is L,I*,R with constant v. If its v is not T, every site forces a selected neighbor above, of the same h. The L and R labels of that next row prohibit extension beyond the existing interval. Thus the next row has exactly the same horizontal interval. Repeating upward and downward produces a solid axis-aligned rectangle with bottom B, top T, and a unique copy of each corner. There are no finite holes, branches, stepped sides, or missing interior sites. Rectangles may touch across zero-color edges, but they are separate nonzero-edge components.

This lemma assumes the displayed grammar; merely calling tile types “left/interior/right” does not establish it. One-cell widths/heights are excluded by the three-valued grammar unless extra types are deliberately added.

### 4. Infinite components are NOT absent

The grammar allows infinite strips, half-planes, and planes whenever the tableau symbols admit the corresponding local matching. A usual headless blank-to-blank interior computation gives an all-interior full-plane example. Periodic volumes can also have winding components without any marked accepting corner. Therefore the assertion “every component is an accepting finite rectangle” is false in infinite or periodic geometry.

This does not invalidate the construction. The small positive Fourier factors give a direct uniform boundary-mixing proof, below. It is unnecessary and incorrect to declare infinite supports pointwise impossible.

### 5. Uniform auxiliary-edge Dobrushin bound

Fix an arbitrary spin configuration (s,r). Consider the edge-variable Gibbs model with vertex factors 1+aF_v. Every factor is in [1−epsilon,1+epsilon]. Put R=(1+epsilon)/(1−epsilon).

Changing one edge variable f can affect the conditional distribution of a distinct edge e only if they share a vertex. For such a pair, the unnormalized likelihood ratio of the new and old conditional laws lies in [R^(−1),R]. The sharp elementary likelihood-ratio TV bound gives

c_ef ≤ (R−1)/(R+1)=epsilon.

There are at most six other edges sharing the endpoints of e. Hence the Dobrushin row sum is alpha≤6epsilon<1. This estimate is uniform in the complete spin configuration, boundary conditions, machine, volume, and group size. It supplies uniqueness of the conditional auxiliary-edge Gibbs law and uniform exponential boundary comparison.

For a local function A depending on the four edges incident to v, the standard comparison sum gives

|E_fixed A−E_free A| ≤ 4 osc(A) alpha^d/(1−alpha),

where d is their minimum edge-adjacency distance to the dangling boundary edges. The free model integrates the dangling edges; the fixed model conditions on arbitrary values of them. One may obtain this directly by summing influence paths: every path reaching a changed boundary kernel has length at least d, and the total length-l path weight is at most alpha^l. The bound is not an assertion that the dual tiles themselves form independent percolation.

### 6. Exact no-halt decoupling in every Gibbs state

Appendix A proves that a finite boundary-closed rectangle exists if and only if M halts, including soundness at the finite tape boundary.

If M does not halt, the free-dangling-edge character expansion on EVERY finite set has only its empty term. Thus its normalized auxiliary partition function equals exactly 1, for every assignment of s and r.

Change only the physical spins at v, from assignment A to B. Let

L_v(g)=(1+aF_v(g,B))/(1+aF_v(g,A)).

It lies in [R^(−1),R]. The free-edge expectation under spin assignment A is exactly the partition-function ratio, hence exactly 1. The fixed-edge ratio is E_fixed L_v. Section 5 proves uniformly

|Z_fixed(B)/Z_fixed(A)−1| ≤ 4(R−R^(−1)) alpha^d/(1−alpha).

As the conditioning box recedes, the auxiliary contribution to the conditional local-spin odds therefore tends uniformly to 1. Apply DLR in a large joint box, condition on all other spins, and then let the box grow. The limiting single-site conditional probabilities for (s_v,r_v) are exactly those of the two original, decoupled Ising layers. Averaging out any auxiliary tail conditioning does not change this identity. Positivity then gives the full decoupled Ising specification.

Thus EVERY Gibbs state of the physical finite-energy model projects in the nonhalting branch to a Gibbs state of the decoupled Ising system. Conversely, free-dangling auxiliary integrations leave finite-volume spin laws exactly unchanged, and subsequential joint limits lift the usual product Ising phases. Translation-covariance of the unique conditional auxiliary law preserves TI lifts.

This proof handles possible infinite or winding dual supports through actual positive-model boundary mixing. It does not silently assume a finite-polymer representation for arbitrary dual boundary states.

### 7. Why a separate all-TI step is necessary

In the halting branch, finite-volume integration gives a hard-core gas of accepting rectangles, with a factor 1[s_anchor=r_anchor] at each unique marked corner. This is not automatically a pairwise ferromagnetic spin interaction or a log-supermodular marginal.

The finite-volume uncolored Edwards–Sokal representation has horizontal FK opening probability at least tanh(K/2)=tanh3. Under arbitrary fixed spin boundaries, however, an edge joining components attached to opposite boundary colors has opening probability zero. Appendix E supplies the equilibrium/recoloring argument that extends this lower bound to EVERY TI physical Gibbs state. Appendix F then obtains the required decay. Neither of these steps follows from the local Fourier calculation alone.


## Appendix C. Positive finite-energy Fourier construction

### 1. Target observable and two physical spin layers

At each v in Z² put two spins s_v,r_v in {−1,+1}. Give every nearest-neighbor edge energy

    K 1[s_u≠s_v] + K 1[r_u≠r_v],

with the fixed integer mismatch energy K=6. The final observable is

    O_v=(s_v−r_v)/2.

The exact on-site involution tau exchanges s_v and r_v and leaves every auxiliary variable fixed. Appendix D proves exact independence of the two spin specifications on nonhalting, giving opposite-layer ordered witnesses. Appendices E–F prove zero exchange-odd expectations and exponential exchange-odd correlations in every TI state on halting. They do not assert classification into exactly two full Gibbs phases.

A common overall Ising sign may remain ordered on halting. Full Gibbs-state uniqueness is not required for the observable contract.

### 2. Finite Wang tiles for accepting rectangles

Effectively compile M into a finite set T_M of Wang tiles with a distinguished exterior edge color0. All internal matching colors are nonzero. The required geometry can be expressed by two status fields

    h in {L,I,R},  v in {B,I,T}.

The west edge is0 exactly for h=L, and the east edge is0 exactly for h=R. Every other horizontal edge has a nonzero color carrying the vertical status v plus the computational matching information. Horizontal matching therefore permits only a left boundary followed by interior columns and then a right boundary, with the same v along the row. Similarly, the south edge is0 exactly for v=B and the north edge is0 exactly for v=T; nonzero vertical colors carry h and the computation information. Vertical matching preserves h and permits B, interior rows, T.

For a finite nonzero-edge-connected component, choose its lowest row. Every tile there must have v=B, since otherwise it has a nonzero south edge requiring a lower tile in the same component. Following nonzero horizontal edges gives one complete finite row from L through zero or more I tiles to R. Nonzero north edges force a complete row immediately above with the same column-status sequence. Its common vertical status is I or T. Continue until the unique T row. This proves the component is a solid rectangle of width and height at least2, not a punctured or ragged shape. Tiles beyond its boundary connect only via color0, hence lie in other components. Side-touching rectangles are allowed but remain distinct components.

The explicit compiler is given and independently checked in Appendix A. It folds an arbitrary two-sided TM onto a one-sided tape, enforces the prescribed input and exactly one initial head with a bottom-row DFA, and encodes each deterministic update with overlapping lower-row triples. HALT and right-wall REJECT are absorbing. The top-row DFA requires exactly one HALT head and no other head; no cleanup sweep is needed. Overflow takes priority and cannot create a halting certificate. Therefore:

    a finite valid rectangle exists iff M halts on its prescribed input.

If M halts, choose a width larger than the used folded tape and enough rows for its halting history; the absorbing halt state permits padding. If a valid accepting rectangle exists, its exact deterministic local history yields a genuine halting computation before any rejecting wall collision.

Mark the unique top-left corner. A rectangle carries exactly one marked tile. This corner will supply the physical alignment indicator below. The explicit compiler retains exactly this geometry. Its companion script exhaustively checked the actual finite tile table on 84 width/height cases over seven small machines, and separately checked small component geometries; the proof, rather than those finite checks alone, establishes the arbitrary-machine statement.

### 3. Fourier factors

Let G=(Z/2Z)^m have at least as many characters as there are edge colors. Assign color0 to the trivial character and all other edge colors to distinct nontrivial real characters chi_c:G→{−1,+1}.

Put one auxiliary variable g_e in G on each unoriented lattice edge. For a vertex v and tile t define

    Chi_t(g)=chi_cN(t)(g_N) chi_cE(t)(g_E)
              chi_cS(t)(g_S) chi_cW(t)(g_W).

Let I_t(s_v,r_v) equal1 for every unmarked tile and equal 1[s_v=r_v] for the marked corner. Define

    F_v(g,s,r)=sum over t in T_M of Chi_t(g) I_t(s_v,r_v).

With t=|T_M|, F_v is an integer and |F_v|≤t on every physical configuration.

Choose integer C0>t and D=C0+t. Put a local auxiliary a_v in {1,...,D}. Its energy is

    E_v=0  if a_v≤C0+F_v;
    E_v=1  otherwise.

This is a finite local rule with only integer energies0 and1. Summing a_v exactly gives, at beta1,

    W_v = (C0+F_v) + (D−C0−F_v)e^(−1)
        = C + lambda F_v,
    C=C0+t e^(−1),  lambda=1−e^(−1).

Thus W_v=C[1+a F_v] with

    a=(1−e^(−1))/(C0+t e^(−1)) <1/C0.

Every factor is strictly positive, since C0>t. Taking C0 sufficiently large makes a arbitrarily small without adjusting any physical energy to an uncomputable or critical real number. The local alphabet grows, but remains finite and effectively known. Edge variables can be stored at the lower/left endpoint, giving an ordinary finite-range, translation-invariant site model. All energies, including K, are integers.

### 4. Exact finite-volume dual identity

Integrate every auxiliary edge variable against normalized Haar measure, including free dangling edges of a finite volume. Expand each normalized vertex factor as either its vacuum term1 or one tile term a Chi_t I_t.

Orthogonality gives

    average_g chi_c(g)chi_d(g) = 1[c=d].

A dangling edge instead gives average_g chi_c(g)=1[c=0]. Thus surviving terms are precisely assignments of Wang tiles and vacuum such that adjacent colors match and all exposed boundary colors are0. The finite nonzero-edge components are the accepting rectangles from Section2.

After dropping spin-independent factors, the exact auxiliary partition function is

    Z_aux(s,r)= sum over vertex-disjoint collections Gamma of accepting rectangles
                 product over gamma in Gamma of
                    a^(area(gamma)) 1[s_anchor(gamma)=r_anchor(gamma)].

A polymer includes its complete tableau, not only its geometric rectangle. Distinct tableaux with the same support are distinct polymer species. Rectangles may touch along exterior color0 edges. They may not share a vertex. Every coefficient in this dual gas is nonnegative.

If M does not halt, no finite accepting rectangle exists, and this finite-volume expression is identically1 for every spin assignment. If M halts, at least one positive-activity species exists. This identity, unlike a noisy verifier, has no contribution from an invalid accepting tableau.

The identity uses a free auxiliary boundary. Arbitrary fixed auxiliary boundary values can support open or infinite dual components. Their disappearance from the infinite-volume induced interaction needs the high-temperature step below; it must not be asserted from the finite identity alone.

### 5. Uniform high-temperature auxiliary control

The auxiliary model conditioned on an arbitrary complete pair-spin configuration has vertex factors 1+aF_v, with |aF_v|≤u=at. For u sufficiently small, it satisfies a uniform Dobrushin criterion. An edge variable meets two factors and has at most six other edge-variable neighbors. For two edges sharing one factor, the sharp likelihood-ratio comparison proved in Appendix B gives variation at most u. Hence the Dobrushin row sum is at most6u<0.0006. This bound is independent of the machine's halting time, spin assignment, and group size.

Separately, the finite closed-component gas has activities a^n. A crude count of connected supports and tile fillings containing a fixed site is at most (16t)^n. Taking 16 e² t a sufficiently small supplies a standard absolute polymer-cluster expansion, uniformly for alignment indicators in [0,1]. The actual rectangular count is much smaller; no improvement is needed for convergence. More explicitly, put rho=16 exp(2)t a<0.012. For every polymer gamma,

    sum_{gamma_prime incompatible with gamma}
        [w_gamma_prime exp(|gamma_prime|)] exp(|gamma_prime|)
      <= |gamma| rho/(1−rho) < |gamma|.

This is the Kotecký–Preiss criterion with control function |gamma|, even after multiplying each activity by exp(|gamma|). It gives absolute convergence with an exponential size margin, uniformly after any subset of anchors is forbidden. Connected clusters have connected union support and diameter bounded by the sum of their polymer sizes. Therefore the induced interaction and its boundary correction have exponentially summable spatial tails; in particular they have the d-summable variation required later.

The direct arbitrary-Gibbs-state argument is now supplied in Appendix D. Conditional auxiliary uniqueness identifies the edge law given every complete spin configuration. A finite spin-change Radon–Nikodym ratio converges uniformly from free auxiliary boundaries, so the exact Fourier identity identifies the spin specification for every physical Gibbs state. An aligned finite reference then yields a positive annealed polymer lift: conditional on the polymers, the spins have precisely the two-Ising specification with forced equality at occupied anchors. On nonhalting the induced spin interaction is exactly the two bare independent Ising interactions, not merely close to them. The full projection/lift proof is Appendix D.


## Appendix D. Every physical Gibbs state has the positive polymer lift

### Result

The free auxiliary-boundary Fourier identity is sufficient to identify the spin specification of **every** Gibbs state of the positive finite-alphabet physical model, not only limits with a specially chosen boundary. Every such spin marginal admits an annealed, positive, finite-accepting-polymer extension. Conditional on the polymers, its spin specification is precisely the two bare Ising layers with equality constraints at occupied polymer anchors. The subsequent all-TI merger is proved in Appendix F after the equilibrium step in Appendix E.

The argument uses two independently checkable hypotheses:

1. Conditioned on every complete spin configuration, the physical auxiliary-edge model has a unique Gibbs state, with uniform boundary mixing for local observables.
2. The positive abstract polymer gas has an absolutely convergent low-activity cluster expansion, uniformly after any subset of anchors is forbidden.

Both follow from the explicit small parameter checked in Appendices B and C. This note gives the projection and lift argument in detail; it does not replace the separate tile-grammar audit.

### 1. Notation and hypotheses

Write sigma_v=(s_v,r_v), with s_v,r_v in {−1,+1}, and A_v(sigma)=1[s_v=r_v]. Let H_0 be the sum of the two nearest-neighbor ferromagnetic Ising Hamiltonians. After summing each local 0/1-energy multiplicity variable, the auxiliary factors are

    f_v(g,sigma)=1+a F_v(g,sigma),       1−u ≤ f_v ≤ 1+u,
    u=a|T|<1.

The four-edge factor at v depends on the physical spins only through sigma_v. All g_e take values in a fixed finite group. Constants dropped in defining f_v are independent of sigma.

For a finite set V, use free dangling edge variables and normalized Haar measure on every edge incident to V:

    Z_V(sigma)=integral product_{v in V} f_v(g,sigma) dg.

The exact finite Fourier identity is

    Z_V(sigma)=sum_{Gamma compatible, all supports in V}
                    product_{gamma in Gamma} w_gamma A_anchor(gamma)(sigma),
    w_gamma=a^{|support(gamma)|}.

A species includes its entire accepting tableau. Supports are finite rectangles and distinct polymers may not share a vertex. There is exactly one anchor per species. The family can be empty. Denote the right side by Xi_V(sigma).

For conditioned g, a Dobrushin row-sum estimate uniform in sigma gives a unique infinite-volume law Q^g_sigma. In particular, for every fixed finite-support bounded observable R and growing boxes V containing its support,

    E_{Q^{g,free}_{V,sigma}} R -> E_{Q^g_sigma} R,

uniformly in the entire sigma configuration. The finite-volume measure here contains the factors centered in V; omission of exterior factors is just another boundary perturbation far from R.

For the polymer gas, take the rooted activity bound sufficiently strong to imply

    sup_x sum_{gamma containing x} w_gamma exp(2|support(gamma)|) << 1.

A crude bound by connected lattice sets and tile assignments is

    sum_{n>=1} (16 |T| a exp(2))^n.

For example, C0=10000(|T|+1) in the physical multiplicity construction makes this small. Removing activities by setting some A_v to zero cannot worsen the absolute convergence bound. Let Q^p_sigma be the canonical infinite-volume polymer law obtained from the free finite-volume laws. The convergent expansion gives local convergence and convergence of finite spin-change partition ratios. Translation covariance follows from the construction.

### 2. Identify the spin specification of an arbitrary physical Gibbs state

Let mu be any infinite-volume Gibbs state of the physical finite-range model. Sum its independent local multiplicity variables first; this gives the positive joint spin/edge specification with factors f_v. Disintegrate this measure over the complete spin configuration sigma. The conditional edge law is Gibbs for the edge factors at that sigma. Uniform uniqueness implies

    mu(dg | sigma)=Q^g_sigma(dg)

for almost every sigma. This conclusion is independent of the boundary construction or extremality of mu.

Fix a finite spin region Lambda and two assignments eta,eta' there, with a common complete exterior configuration xi. Put sigma=eta xi and sigma'=eta' xi. Their auxiliary local weight ratio is the bounded, strictly positive observable

    R_{sigma,sigma'}(g)=product_{v in Lambda} f_v(g,sigma') / f_v(g,sigma).

The positive joint DLR specification, or equivalently its finite spin-change Radon–Nikodym identity, implies that the spin marginal nu of mu has conditional odds

    nu(eta' | xi) / nu(eta | xi)
      = exp(−H_0(eta'|xi)+H_0(eta|xi))
        E_{Q^g_sigma} R_{sigma,sigma'}.

This equality may first be stated for almost every xi. The uniformly continuous right side then defines the corresponding quasilocal spin specification everywhere. Strict positivity of the physical model supplies nonzero finite-block conditional probabilities.

For finite V containing Lambda, the same expectation under the free edge law is exactly

    E_{Q^{g,free}_{V,sigma}} R_{sigma,sigma'}
       = Z_V(sigma') / Z_V(sigma)
       = Xi_V(sigma') / Xi_V(sigma).

Uniform edge mixing therefore proves

    E_{Q^g_sigma} R_{sigma,sigma'}
       = lim_{V -> Z^2} Xi_V(sigma') / Xi_V(sigma).             (1)

This is the desired all-Gibbs projection identity. Open auxiliary Fourier components selected by an arbitrary physical boundary cannot create an extra spin interaction: their possible effect on the local odds is removed by conditioned auxiliary uniqueness before the free-boundary Fourier identity is used.

For completeness, the absolutely convergent polymer expansion of log Xi_V gives a translation-invariant absolutely summable induced potential. Each connected cluster contributes its usual Ursell coefficient times the product of its activities and anchor indicators. Its support is the union of the polymer supports in the cluster. The above exponential rooted bound also controls the diameter-weighted potential norm. Equation (1) identifies the spin marginal as Gibbs for H_0 plus this induced potential. No sign property of that induced potential is asserted.

### 3. A finite reference change avoids division by zero activities

Fix Lambda and exterior xi, and choose a reference spin assignment eta^* on Lambda that is aligned at every site. For instance eta^*_v=(+1,+1). Let sigma^*=eta^* xi. For another eta set

    B(eta)={v in Lambda: eta_v is unequal},
    E_B={Gamma: no polymer anchor lies in B}.

In every finite free polymer volume V containing Lambda, the gas with sigma=eta xi is exactly the gas with sigma^*, conditioned on E_{B(eta)}. Indeed only anchor eligibility changes, and changing an eligibility from1 to0 removes precisely the configurations with an occupied anchor there. Consequently

    Xi_V(eta xi)/Xi_V(sigma^*) = Q^p_{V,sigma^*}(E_{B(eta)}),
    Q^p_{V,eta xi} = Q^p_{V,sigma^*}( . | E_{B(eta)}).

The event E_B concerns finitely many anchors, although their possible species have unbounded finite supports. The exponential rooted tail controls the probability of large species at those anchors uniformly in V. Thus convergence from cylinder events extends to E_B, and

    Xi_V(eta xi)/Xi_V(sigma^*) -> b_eta:=Q^p_{sigma^*}(E_{B(eta)})>0,
    Q^p_{eta xi} = Q^p_{sigma^*}( . | E_{B(eta)}).              (2)

Positivity can be seen without a cluster expansion. Write

    S_B=sum_{gamma: anchor(gamma) in B} w_gamma < infinity.

Condition on all species with anchors outside B. Summing species anchored in B while dropping their incompatibilities gives a partition factor at most product_gamma(1+w_gamma) ≤ exp(S_B). The empty choice therefore has conditional probability at least exp(−S_B). Passing to the infinite-volume limit proves b_eta≥exp(−S_B). The argument remains valid when other anchor activities vanish.

Combining (1) with the aligned reference gives the spin kernel

    nu(eta | xi) proportional to exp(−H_0(eta|xi)) b_eta.       (3)

### 4. Construct and verify the positive joint lift

Define

    mu_hat(d sigma,d Gamma)=nu(d sigma) Q^p_sigma(d Gamma).

If nu is TI, mu_hat is TI. Equation (2), multiplied by (3), gives, conditioned on the exterior spins xi,

    mu_hat(eta,d Gamma | xi)
      proportional to exp(−H_0(eta|xi))
                     1[E_{B(eta)}](Gamma)
                     Q^p_{sigma^*}(d Gamma).

The b_eta factors cancel exactly. Hence the conditional spin law in Lambda, given all polymers and the exterior spins, is

    exp(−H_0(eta|xi)) product_{v in Lambda:
                some polymer is anchored at v} 1[eta_v aligned],

with its normalizing constant. This is precisely the pair-Ising specification with a forced vertical equality edge at each occupied anchor. Equality constraints at exterior anchors only involve exterior spins and cancel from this conditional.

Conditioned on the complete spins, Gamma has the positive hard-core polymer Gibbs law Q^p_sigma, with activities w_gamma A_anchor(gamma). In particular, for any proposed finite polymer gamma and given all other polymers, its occupation odds are w_gamma A_anchor when its support is vacant, and0 when incompatible. The usual removal/insertion conditionals hold for finite collections of species.

Together these local spin and polymer conditionals give the positive annealed specification. One may either use these conditionals directly, or formulate a joint DLR specification by resampling finitely many spins and finitely many polymer species. The compatibility constraints cause no disconnected local sectors: removing the finitely many involved polymers first allows all spin changes. For spatially local statements, the exponential rooted activity tail permits taking increasing finite sets of species. No infinite polymer is added to this state space.

This lift is a mathematical positive representation of every physical Gibbs spin marginal. It is not a pointwise sampling of the possibly signed Fourier expansion of a fixed auxiliary configuration, and it does not claim that all infinite auxiliary dual supports are impossible.

### 5. Immediate consequence in the nonhalting branch

If M never halts, the polymer family is empty. Then Xi_V(sigma)=1 for every V and sigma. Equation (1) makes every auxiliary correction to the spin odds exactly1. Therefore every physical Gibbs spin marginal is Gibbs for the two uncoupled Ising layers, with no residual interaction.

Conversely, any Gibbs state of the uncoupled pair-Ising specification lifts using Q^g_sigma and the independent local multiplicity kernels to a physical Gibbs state: the finite spin-change identity and the edge DLR specification verify compatibility. In particular, the product plus/minus and minus/plus Ising phases occur. At the fixed mismatch cost K=6 they have

    E[(s_0−r_0)/2]=+m_K or −m_K,

where m_K>0 for the mismatch-energy convention used here. This supplies the required nonhalting ordered witnesses.

### 6. Transition to the all-TI phase argument

The preceding argument establishes the positive lift for every physical Gibbs spin marginal. Appendix E proves the extra equilibrium/recoloring transfer needed for conditional FK domination, and Appendix F proves halting merger and odd-mode decay. Neither positivity of a finite-volume FK formula nor FKG of the effective spin interaction is assumed to supply those steps.


## Appendix E. Variational recoloring and conditional FK domination

### 1. Precise statement

Let the physical model be the positive finite-alphabet Fourier construction. The two horizontal spin layers have mismatch energy K·1[s_x != s_y], with integer K>0. Let the tile activity a be so small that the uniform rooted polymer sum

    sup_x sum_{gamma containing x} a^{|gamma|} exp(2|gamma|)

is sufficiently small. A species gamma includes its finite accepting tableau, and has exactly one anchor. Use the all-Gibbs positive lift proved in Appendix D.

For every TI physical Gibbs state, lift its spin marginal to the canonical finite-polymer gas and then to horizontal Edwards–Sokal bonds. Its horizontal-bond/polymer marginal satisfies, almost surely,

    P(omega_e=1 | all other horizontal bonds, all polymers)
       >= q := (1-exp(-K))/(1+exp(-K)) = tanh(K/2).           (FK)

The statement concerns the ORIGINAL marginal, although the proof uses a recolored spin extension. No association/FKG hypothesis on the polymer marginal is used.

The convention matters: q=tanh(K/2) for mismatch energy K; it would be tanh K for the Hamiltonian coefficient -K s_x s_y.

### 2. A local hard-tile/ES model used only as a variational vehicle

Use site variables tau_v in {vacuum} union T, spins (s_v,r_v), and two layers of horizontal bonds omega. Matching tile colors are a hard nearest-neighbor constraint; vacuum has color zero on all sides. Each occupied tile has weight a. A marked corner imposes s_v=r_v. For each layer edge put

    bond weight = 1-p                  when closed,
                  p·1[endpoint colors equal] when open,
    p=1-exp(-K).

Summing the bond gives exp(-K·1[unequal]). These weights define a finite-alphabet, translation-invariant finite-range interaction with hard constraints. Every allowed local energy is finite. Infinite matching tile components are allowed in this variational vehicle, but the canonical lift occupies only finite accepting rectangles.

Let P_open be its pressure with no restrictions on the tile colors pointing out of a finite box. Let P_zero be its pressure when all those external colors are zero. These pressures coincide.

### Boundary-pressure proof

Fix a spin configuration in a box V. In the Fourier identity, freely integrating all dangling group variables imposes exterior color zero and gives Xi_V(sigma), the finite accepting-polymer partition function. Instead fixing EVERY dangling group variable to the identity element gives character value 1 for EVERY exterior color. It therefore gives exactly the unrestricted-boundary hard-tile partition function, with no signs.

Only factors at boundary vertices can depend on dangling group variables. Since every positive Fourier factor lies in [1-u,1+u], writing R=(1+u)/(1-u) gives, uniformly in the spins,

    R^{-|boundary V|} Xi_V(sigma)
       <= Z_open,V(sigma)
       <= R^{|boundary V|} Xi_V(sigma).

The same comparison remains true after summing spins and ES bonds. Its logarithmic error is O(|boundary V|), proving P_open=P_zero. Locally admissible unrestricted box patterns need not all extend globally, so identify the global SFT pressure explicitly: every zero-boundary tile pattern extends by vacuum (with arbitrary exterior spins and closed exterior bonds), giving P_zero <= P_SFT <= P_open. The surface comparison makes all three pressures equal. In particular, frozen infinite hard-tile sectors cannot have a larger variational pressure than the canonical finite-polymer sector. This is a pressure statement, not an assertion that those sectors do not exist or are Gibbs-irrelevant under arbitrary boundaries.

The full finite-alphabet hard interaction obeys the usual variational upper bound: every TI admissible measure has specific entropy minus mean energy at most P_open. This follows directly from the finite-box entropy inequality against the unrestricted admissible partition function.

### 3. The canonical lift is actually an equilibrium measure

Let nu be a TI physical spin marginal. The all-Gibbs projection theorem identifies it as Gibbs for the bare two-layer Ising interaction plus the absolutely summable induced interaction obtained from log Xi. Hence it is an equilibrium measure for that summable interaction on the full spin shift.

Let rho(d sigma,d Gamma)=nu(d sigma) Q_sigma(d Gamma) be its canonical positive polymer lift. Write N_occ for the number of occupied tile sites per fundamental site. Its specific conditional entropy identity is

    h(rho)-h(nu) + log(a) E_rho N_occ
       = lim_{V -> Z²} |V|^{-1} E_nu log Xi_V(sigma).        (CE)

Here h is entropy per physical lattice site. There are no infinite polymers in Q_sigma. The identity is uniform under forbidding arbitrary anchors.

### Boundary justification of (CE)

A canonical hard-core gas has occupation probability at most w_gamma=a^{|gamma|} for each particular species, because its conditional insertion odds are at most w_gamma. The exponential rooted activity bound therefore implies

    sum_{gamma crossing boundary V} w_gamma |gamma|^j
       <= C_j |boundary V|,    j=0,1,2,

for square boxes (adjusting C_j for a fixed-width collar). It also bounds the entropy of the crossing-species indicators by O(|boundary V|): use subadditivity and h_2(p_gamma)<=w_gamma(1+|gamma| log(1/a)), since w_gamma is uniformly below 1/2.

Condition on the complete spins and on all polymers crossing the box boundary. Polymers contained entirely in the box form the free finite gas with the sites covered by crossing polymers forbidden. If that covered set is C, deleting its restriction changes log Xi by at most

    sum_{gamma: gamma intersects C} w_gamma <= K_0 |C|.

The expected |C| and the entropy needed to specify the crossing species are O(|boundary V|). The finite-volume Gibbs entropy identity for the remaining interior gas is exact. Restoring the crossing data changes conditional entropy and occupied area only by these boundary-order terms. Dividing by |V| proves (CE). Conditioned on the crossing polymers, the remaining interior gas depends on the spins only through sigma_V. Thus any additional information about the exterior spins is carried by crossing data of boundary-order entropy; it cannot leave an extensive conditional-entropy correction. The relative entropy-rate chain rule identifies the resulting conditional entropy rate with h(rho)-h(nu).

The cluster expansion of log Xi gives an absolutely summable translation-invariant potential, so the right side of (CE) is exactly the mean induced log-weight appearing in nu's variational functional. It follows that rho has specific free entropy P_zero=P_open for the local spin/tile model.

Finally extend rho by independent ES bond kernels conditional on the spins. For each edge the identity

    entropy of its conditional bond law + expected log bond weight
       = log[(1-p)+p·1[equal]]

is exact. The ES extension therefore has the same specific free entropy and is an equilibrium measure for the local hard-tile/ES interaction of Section 2.

### 4. Recoloring infinite components preserves the specific free entropy

For a realization of the full FK graph, include every occupied polymer anchor as a vertical equality edge. Keep every finite full-FK component's spin color unchanged. Recolor EVERY infinite full-FK component to +. Keep the complete tile/polymer configuration and every horizontal bond unchanged. This map is measurable and translation-equivariant, so it takes a TI law to a TI law rho_plus.

Every open horizontal edge and every equality anchor still joins equal spins. Closed-edge weights are independent of spins. Thus all local ES/tile energies are unchanged EXACTLY, not merely in density. The canonical finite-polymer property is also unchanged.

The entropy density is unchanged as well. In a finite box, an infinite full-FK component can meet the interior only through a local graph component touching the box boundary. Since vertical anchor edges stay in a single physical column, the number of such local boundary-touching components is at most twice the number of physical boundary sites. Original and recolored spin blocks agree on all other local components. Given either block and the common internal graph/tile labels, at most one bit per boundary-touching component specifies the other block. Therefore the absolute difference of the two block entropies is bounded by

    2 |boundary V| log 2

(up to a fixed collar for the chosen encoding). Dividing by |V| proves equality of entropy rates.

Consequently rho_plus has the same maximal specific free entropy as the original lift: it is also an equilibrium measure of the local hard-tile/ES interaction.

### 5. Why equilibrium implies the needed local DLR property

Only this direction of the variational principle is used for the hard interaction. It does not require declaring every frozen hard-tile Gibbs measure an equilibrium measure.

A maximizing TI measure must have the Gibbs conditional distribution for each finite block, among the fillings compatible with its exterior. Otherwise replacing the conditional law in separated copies of that block by its finite-volume Gibbs kernel yields a strict positive entropy-minus-energy gain per block, equal to the corresponding conditional relative entropy. Average over the finitely many translates of the block grid to preserve TI. Interaction neighborhoods can be chosen disjoint, and the replacement never uses an incompatible filling. A positive local discrepancy would therefore increase the specific free entropy by a positive density, contradicting maximality.

For a positive conditional discrepancy, first approximate the relevant exterior conditional information by a finite cylinder before selecting the separated block grid. This elementary local-resampling argument proves the required DLR equations for rho_plus, including joint finite changes of spins, tiles, and ES bonds. Hard constraints cause no exception: the conditional Gibbs kernel is simply restricted to allowed fillings, and the current filling guarantees that this set is nonempty almost surely.

A precise source for the direction used here is the Lanford–Ruelle theorem as stated in Meyerovitch, *Gibbs and equilibrium measures for some families of subshifts*, Section 3: every equilibrium measure for a potential with summable variation on any shift of finite type is Gibbs. Irreducibility/condition (D) is needed for the converse direction, which is not invoked. The hard-tile/ES admissible configurations form an SFT and the finite-valued potential on that SFT is local. Source: https://arxiv.org/pdf/0903.1426 .

### 6. Compute the horizontal-bond conditional in the recolored law

Condition on every polymer and every horizontal bond except e. Inspect the two endpoint components in the graph without e.

- If they are already connected, e opens with probability p.
- If they are distinct and at least one is finite, the finite component can be recolored by a finite admissible modification. The usual two-color count gives opening probability p/(2-p).
- If both are infinite, both have color + in rho_plus, whether e is open or closed. There is no forbidden opposite-color merge, and e opens with probability p.

The finite-component color count follows from DLR: a finite component has no other open or anchor edge to the exterior, and closed edges carry no spin-color energy. Thus the conditional opening probability is always at least q=p/(2-p).

Crucially, recoloring did not change the joint marginal of (horizontal bonds, polymers). The lower bound is therefore a property of that SAME marginal in the ORIGINAL lift. The possible different colors of its infinite components no longer obstruct the argument.

This proves (FK) for every TI physical Gibbs state.

### 7. Consequences and scope

Conditional on the polymer configuration, the horizontal FK marginal stochastically dominates independent Bernoulli(q) bonds in both layers jointly. No positive association is needed: the uniform single-coordinate conditional lower bound supplies the product domination. The coupling may be chosen so that the lower iid field has the same product law for every polymer configuration, hence is independent of that configuration.

The intersection of the two projected lower fields is iid Bernoulli(q²). Taking the computable integer K large enough makes it a high-density planar percolation field. Appendix F supplies the geometric argument. A particularly direct version uses the conditional-on-polymers coupling above: physical finite energy gives infinitely many eligible aligned sites; positive insertion odds for one fixed accepting species force infinitely many occupied anchors. This infinite anchor set meets the independent common iid backbone almost surely, so the two copies of that backbone join. The finite-hole estimate then makes every spin-disagreement component finite, and an exact finite-component layer swap gives zero means and exponential exchange-odd correlations. These geometric steps remain logically distinct from the variational argument.

No lower bound uniform in the machine's unknown halting time is asserted for the activity of a particular accepting rectangle. Positivity of that finite activity is enough for a finite modification; quantitative crossover scales may be arbitrarily large.


## Appendix F. Infinite-anchor merger and exchange-odd decay

### 1. Model and exact hypotheses

At each x in Z² put spins s_x,r_x in {−1,+1}. Take integer mismatch cost K=6 in each Ising layer, exactly as in the physical construction. Equivalently put J=K/2=3. The spin interaction is

    J sum_<xy> (s_x s_y + r_x r_y),  J = 3,

in the Boltzmann exponent. A translation-invariant family of finite, vertex-disjoint polymers has positive activities w_gamma. Each polymer has exactly one anchor a(gamma) and contributes the constraint s_a = r_a. The canonical small-activity gas is used; its configurations contain only finite polymers. Existence, uniqueness conditional on spins, exponential size tails, and the physical-model lift are handled in Appendix D.

Introduce horizontal Edwards–Sokal bonds in each layer, with p=1−exp(−2J). An occupied polymer is a forced vertical equality edge at its anchor. In a finite color-free volume the weight is

    p^|open| (1−p)^|closed| product_gamma w_gamma  2^(number of full FK components).

The following input is established in Appendix E:

**Recoloring input.** For every TI canonical joint spin/polymer/FK state, recoloring every infinite full FK component + preserves equilibrium and gives another joint Gibbs state with exactly the same FK/polymer marginal. In this recolored state finite FK component colors are independent fair signs, while every infinite component has color +. Consequently its FK/polymer marginal has conditional horizontal-edge probabilities at least p/(2−p)=tanh J. The original marginal has the same lower bound.

Appendix E proves this input by the entropy/pressure bridge, not by FKG of the polymer gas. Hard-core polymer weights need not satisfy the spin FKG lattice condition.

### 2. Common lower percolation and explicit planar holes

The single-edge lower bound implies stochastic domination of independent Bernoulli(tanh J) bonds on the union of both horizontal layers. Couple such independent lower fields Y^1,Y^2 below the actual FK bonds. Their intersection at corresponding lattice edges is iid Bernoulli(q), where

    q = tanh² J.

At J=3, q>0.99. A finite open cluster surrounding a given vertex has an enclosing closed dual contour; the contour sum at alpha=3(1−q)<0.03 is less than one, so theta=P(0 lies in an infinite open cluster)>0. Translation ergodicity of the iid field gives existence of an infinite open cluster almost surely. Two distinct infinite open clusters would, by planar separation, produce an infinite closed dual path. For any specified dual starting vertex, the probability of a closed self-avoiding dual path of length n is at most4·3^(n−1)(1−q)^n, which tends to zero; a countable union excludes every such infinite path. Thus the infinite open cluster is unique; call it C. The same embedded copy of C lies in the horizontal FK graph of each layer.

Here is an elementary version of the planar-hole estimate. In a box Lambda_n, wire all boundary vertices and let C_n be the vertices connected by open bonds to that boundary. Every connected component K of Lambda_n\C_n has an entirely closed primal edge boundary, hence a closed outer dual trail enclosing K. The trail may revisit a dual vertex but uses distinct edges, so a specified trail of length m is closed with probability(1−q)^m. If K contains 0 and x, with R=||x||_infinity, that walk has length at least max(4,2R). A safe bound for the number of such outer walks of length m enclosing 0 is 4m*3^m. Thus

    P(0 <--> x in Lambda_n\C_n)
      <= sum_{m >= max(4,2R)} 4m [3(1−q)]^m.                    (2.1)

The bound is independent of n. The boundary-connection sets decrease locally as n increases, so their complements increase. Passing to the limit gives (2.1) for Z²\C. A union bound over x on a square of radius R shows that the complement of C has only finite nearest-neighbor components, almost surely. It also gives exponential radius tails. This proof uses only elementary high-density percolation; q>0.99 is more than enough.

For alpha=3(1−q)<0.03 and k=max(4,2R), the displayed tail is at most

    4 alpha^k [k/(1−alpha) + alpha/(1−alpha)^2].                (2.2)

Counting a slightly larger class of outer walks changes only the harmless polynomial prefactor. The proof and later theorem need no sharp percolation threshold.

### 3. At most two infinite full FK components

Project a connected component of the bilayer FK graph onto Z². Its projection is nearest-neighbor connected because vertical edges are onsite. An infinite full FK component cannot stay in the complement of C: every connected component of that complement is finite. Therefore it meets C in at least one layer and contains the entire copy of C in that layer. There are only two copies. Hence

    number of infinite full FK components <= 2.                (3.1)

This avoids an independent Burton–Keane uniqueness argument within each layer. It also remains true after deleting or inserting finitely many vertical edges, because the common horizontal lower field is untouched.

### 4. One positive accepting species merges the two components

Suppose at least one finite polymer gamma_* is permitted, with activity w_*>0. Its translates are permitted at every anchor. No lower bound uniform in the unknown halting time is needed.

### 4.1 Infinitely many alignment sites and occupied anchors

For fixed other physical variables, changing the pair (s_x,r_x) changes at most eight mismatch terms of size K=6 and the single ancilla term of size1. Its four possible assignments have an energy range at most8K+1=49. Two assignments are aligned, so their conditional total probability is at least delta=(1/2) exp(−49)>0, uniformly in M and in all other physical variables. Integrating out auxiliary variables preserves the lower bound delta when conditioning only on all other spins. A sequential conditioning argument along any infinite list of sites gives infinitely many aligned sites almost surely. This does not need ergodicity or translation invariance.

Fix such a complete spin configuration sigma, and consider its canonical polymer law Q_sigma. The permitted anchors of gamma_* form an infinite set A. For each fixed finite box B_R choose n mutually disjoint translates of gamma_* whose anchors belong to A and whose supports avoid B_R. This is possible for every n, by greedy selection from the infinite set A.

Let E_R be the event that every occupied polymer support is contained in B_R. Condition on all species other than the chosen n candidates. If E_R can hold, those other occupied supports are contained in B_R. Consequently the n candidates are mutually compatible and compatible with everything else, and their finite-species conditional weights are independent Bernoulli choices with odds w_*. Thus

    Q_sigma(E_R) <= (1+w_*)^(-n).

Letting n increase shows Q_sigma(E_R)=0. Every finite polymer configuration belongs to some E_R because all its members are finite. Thus infinitely many polymers, and hence infinitely many distinct occupied anchors, occur almost surely.

### 4.2 The common iid field may be independent of all polymers

The recoloring theorem's horizontal single-edge lower bound holds conditional on the ENTIRE polymer configuration P as well as all other horizontal bonds. The product domination can therefore be coupled with lower iid bonds independent of P.

One explicit construction enumerates the countable horizontal edges. Sample P first, then use independent uniform U_e to sample each actual edge from its conditional law given P and previously sampled edges. The conditional opening probability is at least tanh J by the tower property. Set Y_e=1[U_e<=tanh J]. Then Y is a product Bernoulli field independent of P, and Y<=omega. The projected intersection of the two layer fields is iid Bernoulli(q), q=tanh²J, still independent of P. Complete the original spin conditional law afterward if desired; its marginal is unchanged.

### 4.3 An independent infinite anchor set hits the common cluster

For iid high-density percolation, put theta=P(0 in C)>0. The events {x in C} are mixing under translations: approximate them by the cylinder events that x connects to a large finite box boundary, and use independence of disjoint finite edge sets. Hence their covariances tend uniformly to zero as the separation tends to infinity.

Every deterministic infinite subset S of Z² intersects C almost surely. Indeed, choose n points of S mutually farther apart than a chosen distance L, and let X_n count their memberships in C. Then E X_n=n theta and

    Var(X_n) <= n + n² epsilon_L,   epsilon_L -> 0.

Chebyshev gives

    P(S intersects C nowhere) <= 1/(n theta²)+epsilon_L/theta².

First let n increase and then L increase. The probability is zero.

Condition now on the polymer configuration. Its anchor set S is infinite almost surely by Section 4.1, and C is independent of it by Section 4.2. Therefore some occupied anchor belongs to C almost surely. Its forced vertical edge joins the two copies of C. Section 3 says every infinite full FK component contains one of those copies, so the full FK graph has exactly ONE infinite component.

This proof applies directly to every TI state and avoids any need to condition on the event that the number of infinite clusters is two.

### 4.4 Alternative finite-edit merger (not needed for the primary proof)

In a translation-ergodic equilibrium component one can instead argue by finite edits in the recolored + state. If there are two infinite components, the horizontal graph has, with positive probability, a common backbone through an eligible anchor site whose complement has only finite nearest-neighbor components. Project this property to the horizontal graph; do NOT condition a DLR update on an extra lower-field coupling.

Delete every occupied polymer intersecting the support of a translate of gamma_* at that site, then insert the translate, holding spins and horizontal bonds fixed. Delete crossing polymers in their entirety, even if their anchors lie outside the target support. Only finitely many finite polymers are involved, so the whole change fits in a finite deterministic update box on a positive-probability subevent. Both infinite components are + in the recolored law, so insertion is admissible with positive DLR probability. The preserved horizontal backbone survives, and the insertion joins its two copies. The at-most-two argument leaves exactly one infinite component, contradicting ergodicity. This is a second proof; the independent-anchor proof above is shorter and avoids its ergodic decomposition details.

### 5. Exact finite-component swap

Let D={x:s_x != r_x}. Since the two copies of C belong to one FK component,

    D subset Z²\C.                                            (5.1)

Every nearest-neighbor component of D is consequently finite, with the radius tail bounded by (2.1).

Swap s and r on any one finite component K of D, keeping all other variables fixed. This preserves the entire Boltzmann weight:

* Inside K, both layer spins change sign, so horizontal products are unchanged.
* If x is in K and y is a neighbor outside K, then y is not in D. Therefore s_x s_y+r_x r_y=0 before and after the swap.
* All anchor equality indicators are unchanged at every site.
* Thus the Fourier physical factors and their ancilla multiplicities are unchanged as well. One need not perform the swap in the FK representation.

For a Gibbs state, the finite-volume DLR equation makes this an exact measure-preserving involution on the event that K is the specified finite disagreement component. Sum over the countably many finite K. With O_x=(s_x−r_x)/2,

    E O_x=0,
    E[O_0 O_x] = E[O_0 O_x 1{0 and x lie in the same D component}].

It follows that

    |E[O_0 O_x]| <= P(0 <--> x in Z²\C)
                 <= C_J exp(−c_J ||x||_infinity).              (5.2)

More generally every bounded local observable odd under layer exchange has zero expectation. For exchange-odd f,g supported in finite sets A,B, swap all finite D components meeting A. Unless one such component also meets B, this flips f and fixes g. A union bound yields

    |E[f g]| <= ||f||_infinity ||g||_infinity |A||B|
                C_J exp(−c_J dist_infinity(A,B)).             (5.3)

The constants depend on J, not on the first accepting rectangle's size or activity. This is not a claim of uniqueness of the full Gibbs state: the common global spin sign can still break symmetry. The symmetry being removed is precisely exchange of the two layers.

### 6. Nonhalting branch and scope

If the finite accepting family is empty, the canonical induced spin model is exactly two independent nearest-neighbor Ising models. At J=3 it has TI phases (+,−) and (−,+), with E O=+m_K and −m_K, respectively. They are exchanged by layer swap.

Together with the physical-to-canonical lift and the recoloring-equilibrium lemma, this proves the requested sharp distinction without reliable computation in a noisy trajectory: nonhalting admits exchange-broken TI phases, whereas halting forces every TI Gibbs state to have vanishing exchange-odd local expectations and exponential exchange-odd correlations.

The full construction uses the physical-lift, recoloring-equilibrium, and grammar proofs in Appendices A, D and E. The exact finite-volume FK formula alone does not establish the universal TI claim; the conditional equilibrium transfer is essential.
