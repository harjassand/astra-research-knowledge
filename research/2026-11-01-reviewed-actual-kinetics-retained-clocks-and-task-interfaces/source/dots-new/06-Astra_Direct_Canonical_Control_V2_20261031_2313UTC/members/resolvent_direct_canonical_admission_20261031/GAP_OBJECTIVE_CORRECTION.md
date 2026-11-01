# Withdrawn auxiliary optimization claim; main admission unaffected

The whole independent review supplied the following exact counterexample.
Original claim: maximizing the canonical LP gap delta also minimizes
C_X=maxdiag(X)/delta. This was false: its normalization bounds diagonals of ALL
X M_a^T, not only X. Homogeneous scaling does not justify the claimed equivalence.

Take baseline M0=I and

 M1=[[3/4,1/4,0],[-1/2,3/2,0],[0,0,1]].

The witnesses X=[[4/5,0,0],[-1/5,3/5,0],[0,0,1]] and the same matrix with
X33=4/5 both satisfy every canonical inequality at delta=3/5. Their C_X values
are 5/3 and 4/3. This delta is optimal: baseline column2 yields delta<=X22;
action1 column1's off-diagonal sign gives X21<=-X22/3; action1 column2's diagonal
bound gives 1>=-X21/2+3X22/2>=(5/3)X22. Therefore delta<=3/5.

It is an actual stochastic-source example, not an arbitrary unrealizable table.
For gamma=9/10 and singleton blocks, set

 A0=[[1/2,1/2,0],[1/4,3/4,0],[0,0,1]],
 A1=[[103/144,41/144,0],[49/72,23/72,0],[0,0,1]].

Then H=(1-gamma)(I-gamma A0)^-1 and I-t(A1-A0)H=M1 exactly.
`check_gap_objective_counterexample.run()` checks these identities and all witness
inequalities with exact rationals and zero observations.

The claim is removed from current PROOF.md, not weakened into a new optimizer
claim. All five v1 files and their manifest are byte-preserved under
history_v1_2256UTC. The main positive-witness bound, source residual transport,
small-LP consumer, noisy-family success proof and direct.py never needed any
optimality of C_X. They compute/check the actual witness and actual bound. Thus
this correction changes an auxiliary comparative statement, not a successful
scientific certificate into a failed one. The defect and reviewer credit remain
visible; no accepted earlier archive is altered.
