# Earned scientific checkpoint

The fixed task is `packet/MATH_TASK.md`: resolve QC for the entire exceptional s=1/3 ROC polynomial face. The central question is still open. Original proof and code for this attempt are frozen beside this capsule; read `REPORT.md`, `PROOF.md`, `classify.py`, `verify_fixture.py` and `heat_obstruction.py` for the exact constructions. These are assets, not a prescribed next method.

Use z=(x,y)=(a+d,c-b), w=(u,v)=(a-d,c+b), r=|z|^2, t=|w|^2, nu(w)=(u^2-v^2,2uv). Multiplying the task polynomial by three gives leading F=t^2+2rt. The complete admissible cubic space has eight dimensions. After a unique argument translation and deletion of affine terms, every globally ROC candidate has form P=F+z^T M nu(w)+Q(z,w), arbitrary real 2x2 M and full quadratic Q.

For unit vectors a,b set n=nu(b), e=Jn. The derived EXACT full ROC criterion is

8Q(a,b)>=|Mn|^2+2(a^T M e)^2.

The acoustic matrix has constant rank three, so there is no omitted singular-chart limit. The receiver implements a finite exact rational-input classifier using rational parametrizations of both circles and sign projection/root isolation for a bivariate polynomial of degree <=(4,8). All cross quadratic terms and weak boundaries are included. The proof explains why strict negativity on an omitted projection fiber would persist into an open tested cell. It is not an optimal-complexity claim.

For Q=alpha*r+beta*t the threshold is alpha+beta>=(2sigma1(M)^2+sigma2(M)^2)/8. In particular the explicit admitted boundary member is

P0=t^2+2rt+x(u^2-v^2)+2yuv+(3/16)(r+t).

It is globally ROC by the exact criterion. It is NOT polyconvex: at A0=(z,w)=((-1/4,0),(0,-1/4)), a null rank-one Hessian direction forces the only possible determinant-support multiplier to 1/16; B0=(z,w)=((-11/20,0),(0,-1/8)) then gives support gap -3/20480. The proof permits general finite convex minor lifts. This is not a QC counterexample or a gradient measure.

For that same P0 a stronger METHOD BARRIER was established. No polynomial closed differential two-form of any degree can make the ordinary componentwise-heat density globally pointwise PSD. After actual rotation symmetry averaging and exact gauges, acoustic and sharp-boundary null columns reduce all allowed coefficients; two necessary scores force j>=-3/4 and j<=-19/24. Higher-degree polynomial corrections cannot evade it because their leading PSD density vanishes on a spanning set of plane-wave Hessians. This excludes the stated polynomial heat-certificate class, not nonpolynomial/angular corrections, a different compatible evolution, a non-heat proof, or QC itself.

Root read the full proof and source report. Original exact replay outputs are retained; targeted root replays of the admitted fixture and polynomial heat obstruction are being run. No historical-priority claim or finite list of safe gradient fields establishes the unresolved QC statement. The inherited homogeneous QC primitive, general Schur/moment reduction and already known exceptional rank retain their credit.

Continue the same central question from these earned facts. QC of P0 is a concrete unsolved boundary case; the full target also includes all M and every Q admitted by the criterion. The exact proofs and failed certificate class are available equally to all continuations. No sibling construction or next representation is supplied.
