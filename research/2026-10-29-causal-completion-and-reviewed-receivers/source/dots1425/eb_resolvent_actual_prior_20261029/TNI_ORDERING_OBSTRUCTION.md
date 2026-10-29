# State-dependent EB-event renewal has an ordering obstruction
2026-10-29. Exact rejected extension.

It is tempting to replace a constant-weight EB CPTP branch by an EB trace-nonincreasing event E≤CPΨ with E†I≥αI. Let R=Ψ−E. Then ||R||diamond≤1−α and the left-resolvent sum Fleft=ΣR^n E has the desired identity id−Fleft=(id−R)^−1(id−Ψ). But Fleft need not be TP.

Counterexample: classical2-state channels in column convention,
E=[[1/2,3/4],[0,0]], R=[[0,0],[1/2,1/4]].
Their sum Ψ is stochastic. E is an EB event with input effect diag(1/2,3/4)≥I/2. Nevertheless
Fleft=(I−R)^−1E=[[1/2,3/4],[1/3,1/2]],
whose column sums are5/6 and5/4. It is not TP and is trace-increasing on the second input.

The physical first-hit channel Fright=ΣE R^n=E(I−R)^−1=[[1,1],[0,0]] IS TP by effect telescoping. But its identity has the other ordering,
id−Fright=(id−Ψ)(id−R)^−1,
which does not directly bound its disturbance by the original one-step residual. Additional commutation or structural control would be required. The constant-weight CPTP theorem avoids the issue because every term has a state-independent scalar trace weight.

Thus full-rank event effects alone do not establish the proposed left-resolvent EB-channel claim. This does not rule out a different instrument-based construction.
