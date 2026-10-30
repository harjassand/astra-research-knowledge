# Actual finite program clocks: correlated unfinished-set bound
2026-10-30. Local analytic lemma for the proposed asynchronous gate. This is not by itself an accepted protected-gate theorem.

## 1. Actual three-state channel and exact Gramian
At each program site use labels 0,e,1, Hamiltonian H=Omega(|e><0|+|0><e|), and the single physical jump J=sqrt(kappa)|1><e|, with fixed Omega,kappa>0. Let B=P0+Pe. The absorbing label is 1. On the 0/e corner the killed adjoint is

    K*(R)=i[H,R]-(kappa/2){Pe,R}.

The positive solution of K*R=-I_active is EXACTLY

    R = [[2/kappa+kappa/(4 Omega^2), -i/(2 Omega)],
         [i/(2 Omega),               2/kappa]].

Its determinant is 4/kappa^2+1/(4 Omega^2)>0. Extend it by zero at 1. With Rmax=||R||, A=R/Rmax, a=lambda_min(R)/Rmax>0 and r=1/Rmax,

    a B <= A <= B <= I,
    L_program* A = -r B <= -r A.                    (1.1)

No dephasing approximation or instantaneous clock service is used. A has genuine 0/e coherences.

## 2. Joint noisy model and norm convention
Work in the PRODUCT PROGRAM GAUGE, before any native forest transformation. The nominal generator is L_memory+sum_i L_program,i. L_memory acts trivially on program registers, including its actual finite native monitors and resets. A retained bath is allowed.

Let the actual perturbation be a sum of bounded normal HP local generator terms N_Z*(t), each annihilating identity, acting on an arbitrary system patch and the SAME retained bath. A local Hamiltonian contributes cb norm at most 2||h_Z||, and a local Lindblad dissipator at most 2||L_Z||^2. Assume

    max_i sum_(Z whose program support contains i) ||N_Z*(t)||cb <= eta,
    each term touches at most q program sites,

uniformly in t, with fixed q>=1. The support is AFTER the onsite program gauge; this gauge only adds program registers in the same original physical columns. Terms with no program support give zero on program-only observables. Bath-only evolution also gives zero. Assume well-defined joint CPTP propagators, as in the storage theorem.

## 3. Moment comparison without independence
For a finite program set S, m=|S|, put M_S=product_(i in S) A_i and m_S(t)=Tr(M_S rho(t)). M_empty=I. All products are positive commuting products on distinct program sites, even though A_i is not diagonal in 0/e.

By the actual nominal dynamics,

    L_nominal* M_S <= -r m M_S.

For a perturbation term let K=S intersect program_support(Z). If K is empty, its contribution is zero. Otherwise locality/bimodularity and ||product_(i in K)A_i||<=1 give the FULL JOINT operator estimate

    N_Z* M_S <= ||N_Z*||cb M_(S\K).                 (3.1)

It holds with arbitrary DATA/controller/bath correlations; the untouched M_(S\K) factors act outside the term's program support and commute its bath coefficients. Positivity of rho then gives the hierarchy

    d m_S/dt <= -r m m_S
                +sum_(Z: K nonempty) ||N_Z*||cb m_(S\K).

Choose eta<r and let p(0)=1 solve

    p'=-r p+eta p^(1-q),
    p(t)^q=exp(-q r t)+(eta/r)(1-exp(-q r t)).       (3.2)

Thus 0<p<=1. Induct on m. Assuming every smaller moment is bounded by p to its size, every summand above is at most ||N_Z*||cb p^(m-|K|)<=||N_Z*||cb p^(m-q). The sum of incidences is <=eta m, whereas

    (p^m)'=-r m p^m+eta m p^(m-q).

Scalar comparison and m_S(0)<=1 yield

    m_S(t)<=p(t)^|S|.                               (3.3)

No product initialization was needed for this bound. In particular the actual all-zero program input satisfies it. The argument works for time-dependent perturbations and a retained common bath; it never conditions the noise to be Markovian on the program alone.

Since product B_i<=a^(-m)M_S,

    Pr(all i in S have unfinished label 0 or e at t)
        <=[p(t)/a]^|S|.                             (3.4)

The physically missing-gate label is only 0 for the gauge below, so (3.4) is a conservative bound for missing gates too. The bound is uniform over all initial logical/reference states, even when DATA becomes correlated with programs and bath.

For any prescribed q_tail>0 choose a fixed latency T and then eta sufficiently small so p(T)/a<=q_tail. For example it suffices that exp(-q r T)<= (a q_tail)^q/2 and eta/r <= (a q_tail)^q/2. Every constant is independent of block length N. The same tail bound remains valid for all t>=T under sustained perturbations.

## 4. Exact physical gauge compatibility
For onsite U_i on the paired DATA resource column, define

    G_i=P0 tensor I+(Pe+P1) tensor U_i.

Conjugation gives the physical program Hamiltonian

    Omega(U_i tensor |e><0|+U_i^dagger tensor |0><e|),

while the e->1 jump stays sqrt(kappa)|1><e| tensor I because G_e=G_1=U_i. Native memory terms are conjugated too. Declaring the paired DATA resources, resource ancillas and program register as a NEW physical fixed-dimensional column keeps every hub/resource nominal term two-site in that grouped-site model; onsite native resets/monitors remain onsite. This requires colocation or actual joint onsite DATA_A/DATA_B/program Hamiltonian capability. Mere notation does not create a coupler, preserve elementary-qubit two-body locality, or allow remote LOCC halves. This statement requires the full conjugated nominal memory generator, not an unchanged memory generator plus only a programmed gate term.

The program-frame perturbation retains its joint cb norm and bounded incidence under this onsite conjugation. Thus Sections 1–3 apply to the ACTUAL finite-rate physical program, not an ideal schedule.

## 5. Scope
This proves only the program-label local-stochastic moment interface and its physical gauge. It does not yet prove that the correlated missing-gate suffix is correctable with stored faults. That needs the operator envelope and strong-memory moment argument, with every dressed energy/history occupation counted. It does not provide live handoff, noisy retrieval, repeated gates or universal programmable computation.
