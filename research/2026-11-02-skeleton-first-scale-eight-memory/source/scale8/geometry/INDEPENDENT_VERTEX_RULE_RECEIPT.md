# Independent primary-source vertex rule receipt

2026-11-02. Independently read arXiv:2605.10943v1 §§2.4, 6.2.1, 6.2.4–6.2.5 from the saved source.txt. Scope: exact abstract vertex sheaf rule and a geometric separation fact, NOT a completed vertex-star incidence reconstruction or witness theorem.

Equation (43) fixes the vertex stalk from the actual abstract edge/face incidence:

F_v = {a in F2^{faces incident on v}: a|faces(e) belongs to F_e for every e incident on v}.

Equivalently stack the embedded local parity-check matrices H_e into A_v; then F_v=ker A_v, and vertex-to-edge restriction is coordinate projection. For degree3 blue edges use H_e rows 110,101; for degree3 red use row111; for degree2 use row11. Boundary degree1 codes must retain their color: blue repetition is F2 (no constraint), red parity is {0} (row1). These boundary rules matter and cannot be inferred from the uncolored degree2 convention.

This gives an exact algorithm once full abstract incidence is supplied. Coordinate overlap of embedded edges does not merge them. It is unsafe to impose these equations directly on arbitrary relative face-syndrome traces: they define vertex cochains, not a universal zero-boundary condition on a patch's syndrome.

Section6.2.5, Table1: W0=[-2.5,3.5]^3+ell Z³ has no ribs and no new cylinder-induced boxes. It contains only separate original/copy refinement gadgets. Actual cylinder attachments occur in W1 (T/free crosses) and W2 (glued crosses). Therefore geometric meeting at an old lattice vertex does not itself impose a cross-sheet equality U=V or remove cylinder charge W. Any paired cancellation theorem must derive the needed equalities through actual W1/W2 rib circuitry and inherited sheaf relations, with boundary carries retained.

Section6.2.4 confirms inherited O–P–Q seam color in a doubled T, separate abstract overlapping edges, and subcomplex handling: one retained arm or two retained arms are allowed; the latter uses degree2 code {00,11}. This prohibits silently treating every terminal collar as a three-arm blue star.

No exact complete vertex-star edge/face list was obtained from prose alone in this pass. The paper says sheaf data and illustrated gadgets uniquely specify it; that is not a machine-readable incidence certificate. The current conditional T-star quotient remains conditional until that gluing is supplied.

## Conditional mapping-cylinder representation audit

The proposed X-doubling reduced complex

C1 = C1(Xa) direct-sum C1(Xb) direct-sum C0(R),
C2 = C2(Xa) direct-sum C2(Xb) direct-sum C1(R),
d(x,y,z) = (delta x,delta y,i0* x+i1* y+delta_R z)

is consistent with the local sheaf assignments under explicit hypotheses: R is the abstract compatible-rib graph; i0 and i1 are its actual maps into the two refined sheets; vertical cylinder edges carry R vertex stalks (T inherited code; glued cross repetition4 for X doubling); free crosses remain abstractly separate. The interior attaching edge formerly repetition2 becomes blue repetition3, both dimension1, so its original x/y coordinate survives. Band faces correspond to R edges.

The source's T polygons are subdivided, including degenerate embedded cells. Degree2 subdivision pairs must be transported/eliminated before this is a reduced complex. Thus this is not an asserted equality of raw physical cochain spaces or a Hamming isometry. A chain-map and norm-controlled reduction must be recorded separately.

Most importantly, R is a SPAN into the sheets, not necessarily the same subgraph under the translation identification: actual compatible planes4,5 in both images correspond to pretranslation planes4,5 on one sheet and3,4 on the other. Hence i0*=i1* cannot be assumed. A proof using the reduced formula must retain those offset inclusion maps and all boundary ports. This audit finds no local algebraic contradiction but does not certify complete all-gadget incidence or no-loss global contraction.
