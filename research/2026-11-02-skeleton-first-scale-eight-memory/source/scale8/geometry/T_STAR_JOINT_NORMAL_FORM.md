# Actual doubled-T collar: joint relative normal form and its unmatched charges

Status: exact finite algebra for the declared, source-consistent compressed doubled-T module of Fig.26, with both possible inherited seam colors. **The norm-controlled lift through every raw degenerate T polygon remains conditional on a complete coface/subdivision certificate; see the audit amendment below.** This supplies a *conditional* two-copy contraction and identifies the additional relative boundary charges. It does not assert these charges vanish in the recursively glued family.

## Incidence provenance and safe compression

Source: arXiv:2605.10943v1 §6.2.4, Fig.26, together with Example6.8/Fig.20's explicit polygon lists and the final sheaf-data paragraph. Saved figures T.svg/T.png and T_polygons.svg/T_polygons.png.

There are three original faces incident on the old T edge. At a transverse attaching rib, each face has two sides in the original sheet and two sides in its translated copy. The cylinder has three surfaces, one for each incident face; they meet along O–P–Q. The attaching edge has the two sheet-side faces and its cylinder surface as incident faces. This is the source's abstract incidence, not an identification of overlapping embedded edges. In particular O–P–Q retains the OLD seam code F, even in an X doubling; it must not automatically be made blue.

The source explicitly subdivides each of the three cylinder surfaces into two polygons in Example6.8 (left): the upper pair shares RQ, the right pair shares P D_0, the lower pair shares P D_1. Those are internal edges of their respective surfaces. Collapsing such degree-2 face adjacency is legitimate for the syndrome calculation: its edge column flips the two faces, so any pattern can be moved to one chosen anchor with final weight its parity, at most its initial weight. The abstract overlapping edges along the inherited seam remain distinct and are NOT collapsed or glued by their coordinates. Additional ordinary grid subdivisions on each sheet-side region admit the same transport.

Use five 3-bit blocks:

    a−, a+, b−, b+, c.

Here a,b identify the two sheets, ± the sides of the attaching rib along the old T edge, and c the three cylinder arms. For X doubling, the new attaching-edge correction columns are, for j=1,2,3,

    a−_j + a+_j + c_j,       b−_j + b+_j + c_j.

The inherited seam permits the old code F separately on each of these five blocks. F is span{111} for a blue old seam and the even-weight subspace for a red old seam. If the stated within-surface transports are certified to use actual degree-2 edges with no omitted cofaces, these local columns lift through those transports to physical sheaf-edge corrections in the patch. This statement concerns syndrome images of corrections; no stabilizer filling or all-scale homotopy is inferred.

## Exact quotient theorem

Write [x] for x modulo F in Q=F_2^3/F. The complete relative invariants of the local correction span are

    U = [a− + a+],
    V = [b− + b+],
    W = [a+ + b+ + c].

Every correction column preserves these three charges. Conversely they are complete: choose representatives and eliminate the a−/b− entries by the new attaching columns; the remaining old-seam freedom gives exactly Q^3. Equivalently the annihilator has the form

    (A, A+C, B, B+C, C),     A,B,C in F-perp.

Thus the quotient dimension is 3 dim(Q): six for an inherited blue seam, three for an inherited red seam. The script independently verifies generator ranks nine and twelve, respectively.

## Joint contraction when neighboring traces match

Assume the exact relative conditions

    U = V,       W = 0.

Let s be a deterministic minimum-Hamming-weight representative of U. Completeness of the invariants gives a local correction to the residual

    (s, 0, s, 0, 0).

This is an exact duplicated-sheet normal form in the declared reduced module. It is NOT the result of independently minimizing the two sheets.

The original weight obeys

    |a−|+|a+| >= min{|x|:[x]=U}=|s|,
    |b−|+|b+| >= min{|x|:[x]=V}=|s|.

Adding, and retaining the nonnegative |c|, proves

    2 |s| <= |a−|+|a+|+|b−|+|b+|+|c|.

Thus the coarse residue s contracts weight by one half. Degree-2 input compression can only reduce weight, so the inequality remains true compared with the pre-compression physical input. A deterministic GF(2) solve produces a correction in the declared reduced generator set; a norm-controlled raw physical lift still needs the stated incidence check.

`t_star_joint_certificate.py` exhausts 32768 inputs for each old color. It verifies all 2048 matching blue-seam inputs and all 8192 matching red-seam inputs, reconstructs each correction image, checks the normal form, and checks the factor-two weight inequality.

## Exact obstruction to an unconditional local claim

A singleton cylinder-arm input c=e_j, all sheet blocks zero, has

    U=V=0, W=[e_j] != 0

for either inherited color. No correction confined to this star can turn it into a duplicated residual. This is a legitimate *relative boundary trace*: an ordinary degree-2 edge farther along that arm can produce one syndrome face in the star and its partner outside. It must not be excluded by assuming every star has a self-contained globally valid syndrome.

Therefore one cannot glue the conditional contraction theorem by just applying it independently at each star. The unmatched charges U+V and W must be retained, transported, and canceled by the actual surrounding doubled-square/rib circuit. The intended coarse sector has dim(Q) degrees of freedom; the additional 2 dim(Q) relative charges are precisely the collar gate.

## Useful complete transfer data

`t_star_transfer_table.py` retains ALL triples (U,V,W), not just matching ones. It enumerates the minimum input syndrome weight and a realizing pattern for all 64 blue-seam classes and all eight red-seam classes. These tables are suitable finite min-cost transfer data for a future gluing proof, without hiding unmatched boundary charges. Overlap between stars still requires a verified shared-cell accounting rule; summing these costs independently would double-count shared syndrome bits.

## What has and has not advanced

Earned here: inherited-color-sensitive T-star incidence, exact complete relative invariants, a concrete paired-sheet normal form, exhaustive local contraction under stated trace conditions, and an explicit unmatched trace obstructing an unconditional local claim.

Not earned: proof that actual full-gadget admissibility and a finite-depth cleaning schedule enforce U=V and W=0 at every required stage; a global coarse-chain map; componentwise contraction on removable witnesses; or the downstream memory claims.

## Carry correlations and a graphic representation

It is NOT safe to budget each of U,V,W separately. A single a+ face defect has charges (q,0,q), while the independent output-port choice a−=q,c=q would use two defects. Any no-loss edge-to-vertex transport must retain this correlation.

There is an exact compact representation. Consider the graph on vertices {0,U,V,W} with five edges

    a−: 0--U,   a+: U--W,
    b−: 0--V,   b+: V--W,
    c: 0--W.

Each edge carries a label q in Q=F_2^3/F. A nonzero label costs one, since every nonzero Q class has a weight-one representative for either old seam color. The Q-valued boundary at U,V,W is exactly (U,V,W) above. The two triangle-cycle moves are precisely the new blue attaching generators after quotienting the inherited seam code. Thus the complete local transfer metric equals the minimum number of occupied edges of a Q-valued flow on this five-edge graph with specified boundary charges. Blue Q has three nonzero labels; red Q has one.

This does not alter the physical model: quotienting by the actual inherited-seam corrections gives the flow representation, and a minimizing flow can be lifted back to physical face representatives plus correction columns. It is a candidate representation for gluing local carry packets while preserving shared costs, rather than falsely charging each coordinate independently.

The table contains 15 weight-one nonzero charge triples in the blue case and five in the red case. Blue maximum minimum cost is three; red maximum is two. All 64/eight triples are retained. Whether neighboring actual collars glue these flow ports to a vertex-star circuit with the desired two-copy normal form remains to be proved from their actual incidence matrices.

## Actual one-/two-arm boundary subcomplexes

The same quotient proof applies to the source's Fig.29/30 sub-T stars with d=1 or2 arms, replacing F_2^3 by F_2^d. The inherited codes MUST be retained: degree1 blue repetition is F_2, degree1 red parity is zero, and degree2 is span{11}. `t_subcomplex_certificate.py` checks all 32 patterns for each degree1 color and all1024 degree2 patterns. Matched counts are respectively32,8,256, all passing the same correction-existence and factor-two inequality. These are still relative matched-trace certificates; they do not force unmatched boundary charges to vanish.


## Independent incidence audit amendment (00:49 UTC)

The independent reader verified the source-consistency of the reduced module but did **not** certify full coface lists for the transverse subdivision edges in the raw T polygons. Example6.8 lists faces in a displayed OPQ-incident portion, not explicitly every coface of each internal edge. Accordingly the finite algebra, exact transfer metric, and matched-trace contraction are proved for the declared reduced module; the all-gadget physical norm-controlled reduction is still a separate unresolved premise. Do not promote this to an actual full-family contraction certificate. The central-cube certificate does not use this uncertain reduction and is unaffected.
