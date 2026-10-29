# Locality cost of a bounded current controller

30 October 2026. Root theorem. This concerns an actual counter architecture,
not every possible way to reduce current variance. It supplies a resource
comparison for the event-updated gate and established paired-current routes.

## 1. Actual premises

A reversible, nonexplosive jump process on an N-site periodic ring has visible
occupancies eta_i in {0,1}, M_N/N -> m in (0,1), arbitrary extra hidden state,
and local memory coordinates z_i. Its actual stationary law mu_N has uniform
canonical visible marginal. Start at mu_N. Its preparation and complete future
conditional generator are premises; conditioning on future apparatus records
is not licensed. No hidden-state mixing or independence assumption is made.

Each actual event a has signed physical bond currents j^a and memory update
Delta_a z. All particle motion, including apparatus motion, is counted, with

    Delta_a eta = B j^a,  (B j)_i=j_(i-1)-j_i.                 (1)

Assume |z_i|<=b, sum_i|j_i^a|<=J, sum_i|Delta_a z_i|<=Z. Both event supports
lie in one circular interval of length R_N. The total rate of events changing
eta or z is at most rN at each state. The budgets b,J,Z,r do not grow with N
in the principal statement. Extra events changing neither may be omitted.

An exact physical counter obeys, on every event,

    sum_i Delta_a z_i = sum_i j_i^a.                         (2)

It follows that the complete total current equals sum_i[z_i(t)-z_i(0)] and is
bounded by 2bN. A small measured variance does not itself imply (2). A single
global bit can be placed at one memory coordinate, but coupling its update to
a distant hop has range of order N in these premises.

## 2. Exact corrected Fourier mode

Let k=2pi/N, d=exp(ik)-1, and set

    X=sum_i exp(iki)eta_i,  Z_k=sum_i exp(iki)z_i,
    F=X-d Z_k.                                             (3)

Equation (1) gives Delta_a X=d sum_i exp(iki)j_i^a. Choose a reference i_a in
the event's circular support. By (2),

    Delta_a F=d sum_i[exp(iki)-exp(iki_a)](j_i^a-Delta_a z_i),
    |Delta_a F|<=|d| |k| R_N(J+Z).                          (4)

For the actual reversible Dirichlet form this proves

    D_N(F)=(1/2)E_mu sum_a rate_a|Delta_a F|^2
       <=(rN/2)|d|^2 k^2 R_N^2(J+Z)^2.                    (5)

This is an exact finite-size identity and bound, not local-equilibrium closure.

## 3. Visible density relaxation, not just a hidden spectral gap

Reversibility and 1-exp(-tx)<=tx give

    E_mu|F(t)-F(0)|^2<=2t D_N(F).                           (6)

For complex F apply the real spectral theorem to its real and imaginary parts.
No irreducibility is needed. Also |d[Z_k(t)-Z_k(0)]|<=2bN|d|. Therefore

    E_mu|X(t)-X(0)|^2
      <=2rNt |d|^2 k^2 R_N^2(J+Z)^2+8b^2N^2|d|^2.        (7)

The canonical marginal gives exactly

    Var_mu(X)=M_N(N-M_N)/(N-1)=:V_N,                       (8)

which is of order N. Thus

    E|X(t)-X(0)|^2/V_N <= C t R_N^2/N^4+C' b^2/N.          (9)

For R_N=o(N), the left side tends to zero on any fixed diffusive horizon t=N^2T.
Ordinary diffusion changes this Fourier mode by a nonzero fraction of its
stationary variance on that horizon. The local counter therefore cannot retain
that density relaxation law. A fixed fractional decorrelation needs time at
least order N^4/R_N^2. This is a statement about actual visible density, since
E|X(t)-X(0)|^2=2[V_N-Re E X(t)bar X(0)], not merely a gap created by frozen memory.

A spectral-gap upper bound follows too: ||dZ_k||_2<=bN|d|=O(b), whereas
||X||_2 is order sqrt(N); hence Var(F) is order N and gap<=C R_N^2/N^4.

## 4. Approximate counter and actual leakage

If (2) fails, define

    e_a=sum_i(j_i^a-Delta_a z_i),
    ell_N=(1/N)E_mu sum_a rate_a e_a^2.                     (10)

Split Delta F into d exp(iki_a)e_a plus the support remainder in (4). Then

    D_N(F)<=N|d|^2 ell_N+rN|d|^2 k^2 R_N^2(J+Z)^2,
    E|X(N^2T)-X(0)|^2/V_N
       <=C T[ell_N+R_N^2/N^2]+C'b^2/N.                    (11)

A local bounded-rate architecture with vanishing per-site quadratic mismatch
cannot both implement this current-counter mechanism and retain ordinary
diffusion. Keeping diffusion needs a nonvanishing mismatch, macroscopic range,
or a growing resource explicitly visible in the bounds. Small measured current
variance alone does not bound ell_N, and is not substituted for this premise.

## 5. Constructive comparison and scope

The all-to-all Gaussian paired-current construction in
`PAIRED_CURRENT_COMPARATOR_AND_DENSITY_LAW.md` has an exactly unchanged complete
density law and zero total current, paying range of order N. Its finite-range
version attains the analogous N^4/R_N^2 scale in a harmonic continuous-current
model; this does not prove sharpness within every bounded-occupation jump class.
The root shared-bit gate
also pays macroscopic interaction range; its density receiver is separate.

Local dipole-conserving paired moves are the z_i=0 case and have strong direct
predecessors, including Meerson2406.03462 and Morningstar--O'Dea--Richter2304.12354.
The use here includes bounded local controller memory, unknown reversible
kinetics, actual range/rate/leakage budgets, and a visible-density correlation
bound without ergodicity. Priority for this particular resource statement is
unresolved. The result does not exclude nonreversible, growing-memory,
long-range or incompletely recorded-current architectures outside its premises.
