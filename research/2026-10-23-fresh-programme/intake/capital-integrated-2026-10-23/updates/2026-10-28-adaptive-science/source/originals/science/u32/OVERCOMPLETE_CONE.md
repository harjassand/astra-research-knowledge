# An overcomplete observable cone certificate

This extends the square gauge certificate. It is a further sufficient
construction, not an acquired universal CP learner. The positivity/polyhedral
realization framework is standard; the formulas state how to verify a candidate
against the actual count intervals. No historical priority or incumbent
advantage is asserted.

## Count-residual verification

Retain the normalized core and rank-exhaustion assumptions from the governing
theorem. In preparation coefficients the true operators are C_z=H^{-1}H_z.
Choose q>=r virtual vertices as columns of V in R^(r by q), with

    rank V=r,       1_r^T V=1_q^T.

Find a right inverse L in R^(q by r), V L=I_r, and an initial distribution
eta>=0 with V eta=e_1. The mass identities imply 1_q^T L=1_r^T automatically.
V can contain negative entries. Candidate nonnegative lifted operators Khat_z
must have exact joint column sums sum_o 1_q^T Khat_(a,o)=1_q^T.

In any other observable basis replace 1_r^T by its known trace functional
ell^T, and require ell^T V=1_q^T. Then 1_q^T L=ell^T and the identical
proof applies. The exact fixture below uses homogeneous Bloch coordinates
with ell=(1,0,0), rather than preparation coefficients.

Suppose |H-Hhat|<=D_H, |H_z-Hhat_z|<=D_z and an entrywise bound
|H^{-1}|<=M_H has been certified. For each branch compute

    Rhat_z = Hhat_z V - Hhat V Khat_z,
    E_z = |L| M_H [ |Rhat_z| + D_z |V| + D_H |V Khat_z| ].       (1)

If Khat_z-E_z>=0 for every branch, the following exact true positive lift
exists:

    K_z = Khat_z + L(C_z V - V Khat_z).                       (2)

It obeys V K_z=C_z V because V L=I. The error in (2) is bounded entrywise
by (1), using the exact residual H_z V-H V Khat_z. Consequently K_z>=0.
For every action the correction's column-mass sum vanishes:

    sum_o 1_q^T(K_z-Khat_z)
       = 1_r^T[sum_o C_z V - V sum_o Khat_z] = 0.

Here true TP gives 1_r^T sum_o C_z=1_r^T, and the fitted causal identity
gives 1_r^T V sum_o Khat_z=1_q^T. Thus K_z is a true stochastic lift.
Starting at eta, its full word probabilities equal the true instrument's
probabilities by intertwining. The same local box-simplex TV certificate and
full-transcript/clock/reuse coupling apply in q latent labels.

This does not assume an exact observed equality at noisy counts: the measured
residual Rhat is explicitly paid. It also does not assume a physical meaning
for the virtual vertices. The price of the proposed cone and its lifting
conditioning appears in |V|, |L| and M_H.

For fixed rational V and L, searching for a certified Khat can be written as
a linear feasibility problem. Introduce nonnegative auxiliary matrices
dominating the absolute residual and |V Khat|, impose (1) as a lower bound
on Khat, and impose stochastic column sums. These are linear inequalities
and equalities. Initial feasibility V eta=e_1, eta>=0 is another linear
program. Searching V and L themselves remains nonconvex and is not solved
by this reduction. The code below verifies a rational exact fixture; it does
not implement or benchmark a general LP solver.

## Why q=r can fail even in a strictly positive regime

Let the minimal real-qubit coordinates be (t,x,z). The R action rotates the
Bloch plane by 90 degrees and then depolarizes with factor lambda=13/20.
Its operator is

    C_R=[[1,0,0],[0,0,lambda],[0,-lambda,0]].

It is CP: a convex mixture of a unitary conjugation and complete depolarizing
noise. The other action has outcomes +/- with full-rank effects
E_+=(I+Z/2)/2, E_-=(I-Z/2)/2 and outputs
tau_+=(I+Z/2)/2, tau_-=(I-Z/2)/2:

    T_(M,+)(rho)=Tr(E_+ rho) tau_+,
    T_(M,-)(rho)=Tr(E_- rho) tau_-.

These measure-and-prepare maps are CP and sum to a TP map. Starting at +Z,
rotations and the readout tests give exact minimal observable rank three.

No three-state positive exact realization exists. Such a realization would
have a 3 by 3 nonnegative stochastic matrix P similar to C_R, because its
dimension equals the minimal observable rank. Its eigenvalues would be
1,+i lambda,-i lambda, so tr(P)=1 and tr(P^2)=1-2lambda^2. Nonnegativity
gives tr(P^2)>=sum_i P_ii^2 >= [tr(P)]^2/3=1/3. Therefore lambda<=1/sqrt(3),
contradicting 13/20. This argument is exact and not a finite search failure.

A four-state positive lift does exist with strict branch margins. Let V's
columns be the four Bloch cardinal states +Z,+X,-Z,-X. R is represented by

    K_R=lambda P_cycle+(1-lambda) 11^T/4.

Its smallest entry is (1-lambda)/4=7/80. For each measurement outcome, use
the state distribution u_+=(1/8,1/8,1/8,1/8)+(1/2)e_(+Z),
u_-=(1/8,1/8,1/8,1/8)+(1/2)e_(-Z). Multiply these by the corresponding
effect probabilities at each vertex. Every branch entry is at least 1/32.
The initial state is the +Z vertex. All intertwining and mass identities
are checked with Fraction arithmetic in overcomplete_fixture.py.

For a literal legal-count coordinate translation, take preparation columns
B=[(+Z), R(+Z), R^2(+Z)] in homogeneous Bloch coordinates and test rows
F=[trace; M+; R-then-M+]. Then

    B=[[1,1,1],[0,lambda,0],[1,0,-lambda^2]],
    F=[[1,0,0],[1/2,0,1/4],[1/2,-lambda/4,0]],
    H=F B,       V_p=B^{-1} V_Bloch,       L_p=L_Bloch B.

Both B and F are invertible: det B=-lambda(1+lambda^2), det F=lambda/16.
The translated vertices have mass 1_r^T V_p=1_q^T, V_p L_p=I, and the
first lifted state maps to e_1. The helper independently verified this
translation and a nonzero-residual perturbation with positive uncertainty
widths in helper/overcomplete_replay/INDEPENDENT_OVERCOMPLETE_CHECKS.json.

This is an exact parameterized CP example validating the enlarged
representation and showing a genuine limitation of the square gauge.
It is not a count-acquired experiment: no shots are attributed to it, and
no latent matrices are passed off as learner inputs. Sufficiently narrow
count intervals around a nonsingular legal core can in principle certify
a nearby strictly positive lift via (1), but that acquisition and search
have not been executed here. The noiseless coherent family still excludes
every finite q. Thus this extension narrows the mechanism gap while leaving
the universal nonpolyhedral confidence geometry unresolved.
