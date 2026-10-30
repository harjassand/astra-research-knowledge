# Two-parameter same-envelope norm: the growth-to-soft-retention correction
30 October 2026. Binding refinement of POSITIVE_BLOCK_MOMENT_RECEIVING.md. This corrects a real insufficiency in the first retention draft. Local proof awaiting review.

## The rejected shortcut
A signed component controlled only with F=e^(sU) can have norm exp(rho_g n). From that bound alone, G=1+e^(-alpha n)F costs exp(rho_g n), not 1+exp[-(alpha-rho_g)n]. A separate small root-only moment estimate with DIFFERENT positive envelopes is insufficient. The old V1 draft is preserved under failed_drafts and must not be used alone.

## 1. Both subset indices are retained
For current remaining records R, use all pairs B,A subset R:

 H_(B,A)(t)=(product_(j in B)phi_j(t))(product_(j in A)Z_j(t)),
 W_(B,A)(t)=(product_(j in B)w_j(t)) M^|A|.

Here phi_j>=I is the actual phase metric, first the growth exponential F_j and later the softened G_j. The positive scalar w_j is its normalization budget; it need not equal a physical moment. Define the norm by ONE pair of positive diagonal envelopes Y_L,Y_R in a positive 2-by-2 block with off-diagonal X, requiring

 Tr(H_(B,A)Y_L,R)<=C W_(B,A) for EVERY B,A.             (D1)

The B=A=empty condition makes this a definite norm dominating trace norm, even if some normalized tests are <I. All reference-stabilized statements use the same definition. This is a finite norm family, not an exponential-size physical procedure.

## 2. Intervals and growth endpoints
For EVERY phase subset B, the actual phase/root drift has its phase source sum_(j in B)a_j(t) and the same coefficientwise root hierarchy indexed by A. Set w'_j=a_j w_j. Divide the corresponding complete operator comparisons by product_B w_j. The root affine comparison has normalized row sum<=1 whenever z_*j<=M. Applying the SAME actual CP map to Y_L,Y_R proves contraction in (D1), simultaneously for every pair B,A.

A soft-target attachment multiplies a selected phase factor by at most exp(epsilon_init L_new), while its rooted pullback is nonincreasing; multiply that w_j by this declared factor. The actual PRE-to-POST endpoint has phi'_j<=phi_j after pullback and similarly for all rooted subsets. Good-cut maps contract. Graph/copy endpoints and moving charts are the reviewed ones; no new physical operation is introduced.

During growth, w_j<=w_seed exp(rho_g n_j), using actual geometric prefix size. Root-only tests B=empty retain their original normalization M^|A| throughout. Thus they do not accumulate an exp(rho_g n_j) cost.

## 3. Marking J has an index shift, not an unmarked-volume cost
For an output test H'_(B,A), with B,A subset R\J, the source-strip cross-map proof uses the incoming test H_(B union J,A). This is the SAME incoming index for its two positive diagonal envelopes. All phase/root metrics commute in the actual chart, untouched factors cancel, and the bounded-leg orbit constants are uniform in A,B. Each new marked j supplies a source-strip factor on at least one ket/bra, so the two leg inequalities have product coefficient

 C_local product_(j in J)barrier_j^(-1/2).

Applying the reciprocal-envelope rescaling proof gives the induced bound

 C_local product_(j in J)[w_j(t) barrier_j^(-1/2)].     (D2)

The normalization ratio is W_(B union J,A)/W'_(B,A)=product_J w_j. There is no factor from any j outside J. Source-strip/projector terms or endpoint cross terms are summed with their real finite per-mark multiplicity. The same incoming-envelope pair works for all B,A after a given elementary cross map, because all inequalities are operator inequalities with the same local legs. Triangle inequality handles their sum.

This index shift is the precise simultaneous version of the earlier pre-mark integrating-factor argument. It avoids pretending that one scalar weighted trace norm automatically controls the root-only identity term at a later metric switch.

## 4. Seed reception with a same-envelope bound
The actual positive seed map has, uniformly over all input states and references,

 T_seed^* H_(B,A)<=w_seed^|B| M^|A| I,

by its reviewed joint defect-cone expansion (overlap of A and B only weakens this product upper bound). Choose M and w_seed at least the corresponding finite weighted seed constants. The SAME positive state/map is the initial envelope pair, so its norm is<=1.

For initial marked sectors J, use the reviewed uniform mixed bad-cone/weight effect bounds and their common Stinespring block envelope. They give at most (3 sqrt(p_seed))^|J| in the remaining normalized family, with fixed constants already included in p_seed/w_seed. Initial phase cuts and projections are actual algebraic sector resolutions. No reset or cut is silently presumed perfect.

## 5. Exact soft switch with the SAME envelopes
At the end of growth replace each phase test F_j by G_j=I+e^(-alpha n_j)F_j. For every B,A,

 H_new_(B,A)=sum_(C subset B) exp[-alpha sum_(j in C)n_j] H_old_(C,A).

This is an exact commuting operator identity. Use the SAME Y_L,Y_R from (D1) on every term. Then

 Tr(H_new_(B,A)Y_L,R)
 <= C M^|A| product_(j in B)[1+e^(-alpha n_j)w_j].

Therefore set w_j,new=1+e^(-alpha n_j)w_j,old; the switch contracts the norm. Since w_j,old<=w_seed e^(rho_g n_j),

 w_j,new<=1+w_seed e^[-(alpha-rho_g)n_j].              (D3)

No new state, measurement, or positive flag was inserted. This exact operator sum is why the extra phase-subset index is essential.

## 6. Retention and all-selected flag counting
During retention set w_j(t)=w_j,entry exp(epsilon_nj t), using the soft-phase/root coefficientwise inequality. Equations (D1)-(D2) then contract intervals and charge each newly marked record only

 [1+w_seed e^(-(alpha-rho_g)n_j)] exp(epsilon_nj t_mark)
       times its exponentially small source-strip factor.

The actual insertion incidence is O(n_j H), and the existing D-dependent generating-SUM proof yields the stated polynomial-prefactor/exponential-barrier mark bound. Growth insertion pays w_seed exp(rho_g n_k) times its barrier, which is absorbed in the corrected c_g. Initial/growth/retention first marks are disjoint possibilities in the exact triangular norm majorant; their nonnegative parameter sums combine by expansion.

At final time choose B=empty in (D1). Every signed component has a simultaneous ROOT-ONLY family on its remaining records with no cost proportional to their sizes or to their number. The final physical-port Cauchy--Schwarz extraction and binomial sum are therefore valid. The same enlarged norm also avoids fixing future D in advance, although that earlier bookkeeping remains a legitimate way to organize the flag sum.

## Scope
This correction proves the required same-envelope metric transition and local insertion receiving. It preserves the actual bounded-body/measurement-assisted/scheduled contract. It does not establish the quantum consumer, native compiler, coherent-input measurement interface, practical threshold, or novelty. The accompanying retention theorem must be read with this refinement, not the preserved rejected V1 alone.
