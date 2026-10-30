# An exact weak-initiation credit with aborted transactions
2026-10-30. Root construction. Isolated four-phase controller, not a native overlap theorem.

## Actual model
Controller phases are 0 (idle), A (acquisition), C (committed), Q (cleanup). Hamiltonian H=epsilon(|A><0|+|0><A|). DATA-free jumps are sqrt(gamma)|C><A| (commit), sqrt(mu)|Q><A| (abort), and sqrt(nu)|0><Q| (ready). The useful terminal jumps are sqrt(kappa)|Q><C| tensor K_s, where Phi with Kraus K_s is idempotent. Optionally add onsite phase dephasing; let delta be its total damping rate on the 0/A coherence. All rates gamma,mu,nu,kappa are fixed positive. Put d=(gamma+mu)/2+delta.

Kill only the useful terminal gain, retaining all DATA-identity abort/cleanup returns and complete losses. Solve K_epsilon^*R=-I. In the ordered basis (0,A,C,Q), the only nonzero offdiagonal entry is

    R_(0,A)=-i/(2epsilon),  R_(A,0)=+i/(2epsilon).

The diagonal entries are

    r=R_00=(gamma+mu)d/(2gamma epsilon^2)
               +2/gamma+1/kappa+mu/(gamma nu),
    R_AA=r-d/(2epsilon^2),
    R_CC=1/kappa,
    R_QQ=r+1/nu.

Substitution verifies every matrix equation. The killed survival integral makes R positive. Alternatively positivity follows directly from its 0/A determinant and positive diagonal entries.

## Uniform spectral margin above the idle lifetime
For the 0/A block, Delta=R_00-R_AA=d/(2epsilon^2) and |R_0A|^2=1/(4epsilon^2). Its largest eigenvalue minus r is at most |R_0A|^2/Delta=1/(2d). Also R_CC<r and R_QQ=r+1/nu. Consequently

    ||R|| <=r+max{1/(2d),1/nu}.

Choose a fixed C0 strictly larger than that maximum and set Rmax=r+C0. This earns a size-independent O(1) excess over the divergent idle lifetime; choosing a generic loose multiple of ||R|| would miss this structure.

Set beta=b epsilon^2 with fixed small b>0 such that beta Rmax<1. Define S=(1-beta Rmax)I+beta R. Exactly,

    S_00=1-b C0 epsilon^2,
    S_0A=-i b epsilon/2,
    S_AA=1-b d/2-b C0 epsilon^2,
    S_CC=1-b(gamma+mu)d/(2gamma)
               -b epsilon^2(2/gamma+mu/(gamma nu)+C0),
    S_QQ=1-b epsilon^2(C0-1/nu).

Thus idle weighting differs from identity at order epsilon^2, idle/active coherence is order epsilon, and the useful active block has a fixed limiting discount. Cleanup has limiting S=I despite lying in the busy manifold; it is not falsely assigned a success-before-return gap.

## Exact DATA service
The reviewed local CP credit built from S and Phi satisfies

    L_phys^*F = -(b epsilon^2 I+s0 A_success)(V-Phi^*V),
    s0=1-beta Rmax>0.

Abort probability does not require an idempotent excursion mixture pPhi+(1-p)Id. The successful terminal channel is idempotent; the killed generator retains identity aborts. This is an exact generator statement for every positive epsilon, not a finite-time adiabatic approximation.

## Consequence and unresolved step
This example explicitly earns the weak-drive orders needed by a local multiplicative construction and shows why the resolvent's idle spectral structure matters. It does not establish those orders for every finite acquisition chain, dirty sector, monitor architecture or overlapping native controller. Those require a structural extension rather than extrapolation from this four-phase fixture.
