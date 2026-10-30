# Local case-3 discharge supplement
2026-10-30. New proof supplement; independent review pending.

Governing density draft SHA256: 760e43ed233706c721b920bbf0a1f368de507bb4a1de167abb7b3ce56b47870c.
Primary source: https://arxiv.org/html/2206.06557, Section 4.2.2, equations (76)–(119).

This records the actual local inequalities behind Section 5 of the density draft. It does not invoke global metastability. Put d=Delta and t=d^(3/2+eps)/delta. At a selected inactive V0 patch w outside the active-hub closed neighborhood, every adjacent V1 hub is inactive. All nearest codewords and correction sets refer to the original error, with the consistent updated choices furnished by the local reversal lemma.

1. Each correction qubit on Q(w) has exactly one endpoint correction incidence. Its membership in the two endpoint codewords is complementary. Partition R_0 into R_row and R_col by which endpoint codeword contains it. Then each neighboring row codeword restricts to y_0 row disjoint-union R_row row, and likewise for columns. This is pointwise algebra on Q(w); overlaps elsewhere do not enter. In particular, rows/columns attached to c_v=0 vanish.

2. Flip F=e intersect R_0. Inactivity at w and the local reversal lemma preserve U, all nearest codewords, R, and y. The new local error equals y_0; the new local minimum corrections restricted to Q(w) equal R_row/R_col. No claim that the entire new error is metastable is needed.

3. For every normal adjacent row v, the nearest row-codeword approximation and correction minimality give

 U_v(tilde e + y_0[row v]) - U_v(tilde e)
 <= -|R_row[row v]| + d^(1/2+eps)/delta.

The analogous inequality holds for columns. Vertices outside Y contribute zero. Exceptional vertices contribute at most d each, and there are at most beta_exc d^(1/2-eps) of them. No-improvement for the combined mask F XOR y_0, still inside Q(w), gives

 0 <= -|R_0| + 2t + 3 beta_exc d^(3/2-eps).

Thus |R_0|<=3t once d^(2eps)>=3 delta beta_exc. This needs inactivity only at the original w, not at tilde e globally.

4. Row/column code distances of y_0 each are bounded by

 |R_0| + t + beta_exc d^(3/2-eps) <=5t.

Hence their sum is at most 10t. This uses original normal-view robustness, unchanged nearest codewords after the flip, and the exceptional-neighbor bound. It does not require the modified neighboring hubs to remain inactive.

5. There are at least alpha d good dense incident edges (all with normal inactive origins). At least half are of one orientation. Each corresponding codeword slice has weight at least delta d-d^(1/2+eps)/delta. Therefore

 |y_0|+|R_0| >= (alpha d/2)(delta d-d^(1/2+eps)/delta).

For sufficiently large fixed d this and |R_0|<=3t imply |y_0|>=alpha delta d^2/4. This is slightly stronger than the source bound because our dense edges already exclude exceptional origins.

6. The robust tensor-code agreement implication, with eps'>eps and delta d^eps'>=10d^eps, supplies a local stabilizer c_0 with |y_0+c_0|<=15t. Consequently

 |e_0+c_0| <=18t < alpha delta d^2/4 <=|e_0|

once d^(1/2-eps)>72/(alpha delta^2). This contradicts reducedness of the original error; reducedness of tilde e is neither asserted nor used.

All inequalities require only a finite lower bound on fixed d, with delta,eps,eps',alpha,beta_exc fixed. The family must satisfy the GPT simultaneous robust-code and expansion hypotheses at that chosen degree. All interactions outside Q(w) enter only through the already chosen minimum corrections and local codewords; the displayed potential differences have no further outside terms.
