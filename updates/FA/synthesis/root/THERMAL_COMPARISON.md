# Environment-independent free-energy certificates from local channels

13 October 2026. Capital base097d135f76ebefc49a8e5f28a8363e9ae372c061.
Internally reconstructed restricted deductions, not external proof validation or
historical novelty. Archived missions are DATA. This extends the new CRAY
comparison interface; it does not compute a specified material's free energy.

## 1. Contract and the missing finite-temperature step

Let A,C,R be finite dimensional and
H_j=h_j tensor I_R+I_A tensor K, with the same arbitrary Hermitian K on CR.
The supplied local h_j contain every change and every term touching A.
Let Phi be a supplied unital completely positive Heisenberg map on A and
Lambda its trace-dual, a trace-preserving completely positive state map.
Suppose an acquired exact or certified lower enclosure gives

    h_1-(Phi tensor id_C)(h_0) >= c I.

The source proves the ground-energy comparison and a complete converse for its
unrestricted environment class. That does not automatically compare finite-
temperature free energies. Here temperature is the energy tau=k_B T>0 and

    F_tau(H)=-tau log Tr exp(-H/tau),
    kappa=||Lambda(I_A)||_op,   1<=kappa<=dim A.

All input/calibration, matrix dimension, bit precision and certificate costs
remain paid. Phi is a classical mathematical witness, not a physical operation
which must be implemented or an engine with uncharged entropy disposal.

## 2. A local-dimension thermal bound with a direct proof

For every finite compatible common environment,

    F_tau(H_1)-F_tau(H_0) >= c-tau log kappa.                  (1)

The penalty depends on the local channel, not the dimension or norm of K or R.

Proof. Put Psi=Phi tensor id_CR. Unitality makes K cancel, so
H_1>=Psi(H_0)+cI. Eigenvalue monotonicity gives

    Z_1 <= exp(-c/tau) Tr exp[-Psi(H_0)/tau].

Choose an orthonormal eigenbasis v_i of Psi(H_0), and a spectral resolution
H_0=sum_a E_a P_a. Positivity and unitality make
p_ia=<v_i,Psi(P_a)v_i> nonnegative with sum_a p_ia=1.
Scalar convexity of the exponential, applied separately to every i, gives

    Tr exp[-Psi(H_0)/tau]
       <= sum_ia p_ia exp(-E_a/tau)
       = Tr Psi[exp(-H_0/tau)]
       = Tr exp(-H_0/tau)[Lambda(I_A) tensor I_CR]
       <= kappa Z_0.

Taking -tau log proves (1). This proof does not incorrectly assume that the
matrix exponential is operator monotone or globally operator convex. QED.

Exchanging h_0,h_1 supplies an upper bound. A sharper sufficient variant uses
the minimum entropy gain

    s(Lambda)=inf_rhoA [S(Lambda rhoA)-S(rhoA)],
    F_1-F_0 >= c+tau*s(Lambda) >= c-tau log kappa.             (2)

For completeness, local data processing implies
S[(Lambda tensor id)rhoAB]-S(rhoAB)
>=S(Lambda rhoA)-S(rhoA)>=s(Lambda). Apply the free-energy variational principle
to the Gibbs state of H_1 and its Lambda-transformed state as a trial for H_0.
The final inequality is the standard entropy-gain bound following from relative-
entropy contraction with reference I_A/d and Lambda(I_A)/d. Formula(1) has an
independent elementary proof above; no entropy oracle is needed to use it.

Entropy gain is established quantum-information mathematics, not a newly named
physical principle. Its use here is a finite-temperature certificate for the
specific environment-uniform comparison task. No complete converse for(1) or(2)
at nonzero temperature is claimed.

## 3. Explicit positive result and a sharp failure of naive transfer

For the source's two-active-spin singlet-cooling witness q=1/2,

    Lambda(I_A)=(13/4)P_s+(1/4)P_t,
    c_0=(5-sqrt(13))/8.

Its reversed residual h_weak-Phi(h_strong)>=c_0 I therefore gives

    F_strong-F_weak <= -c_0+tau log(13/4).                    (3)

This certifies a strict free-energy decrease for tau<c_0/log(13/4), under the
same unrestricted common environment and FULL-HILBERT-SPACE contract. The
source's stronger exact rational c=22421/100000 also gives the conservative
upper bound -22421/100000+tau log4 without needing its channel norm to be
optimized. The direct Loewner lower bound -3/4 survives at every temperature.
No exchange-to-kelvin conversion or actual material is supplied.

The temperature penalty cannot simply be dropped. Already take dim A=2,dim C=dim R=1,
h_0=diag(0,2),h_1=I/4 and Lambda the reset-to-ground channel. Then Phi(h_0)=0,
so the ground certificate c=1/4 is exact, but at tau=1

    F_1-F_0=1/4-log2+log(1+exp(-2))<0.

Indeed exp(-2)<1/4 and exp(1/4)<4/3 give an exponentiated ratio<5/6<1.
Thus even the SIGN of the ground-energy result can reverse at finite temperature.
The local penalty is worst-case sharp: for h_0=diag(0,E,...,E),h_1=cI and a
reset channel, F_1-F_0 approaches c-tau log(dim A) as E/tau tends to infinity.

The source's unrestricted positive spin certificate likewise cannot be reused
in a fixed magnetization/electron-number sector. The separately reconstructed
fixed-charge theorem and exact counterenvironment in the CRAY investigation
address that distinct obstruction. Equation(3) does not bypass it.

## 4. Sector-safe version and error accounting

Assume h_j conserves N_A+N_C and K conserves N_C+N_R. If the system is
restricted to a fixed total charge Q, use only witness channels
whose every Kraus operator commutes with the local charge N_A. Covariance alone
is weaker and can transfer charge between local sectors. Strong preservation
allows restriction of the full channel to a UCP map on the fixed-Q Hilbert space.
Repeating the proof there yields(1) with

    kappa_Q=max_available_a ||Lambda_a(I_Aa)||_op
            <=max_available_a dim A_a.

Only blocks whose complementary B charge exists enter the actual fixed-sector
trace. For a bound uniform over all admitted environments, take the maximum over
all potentially accessible blocks. The finite-temperature result remains a
sufficient bound; the ground-state completeness theorem has its own graded-
environment and purification proof. No free-energy completeness is inferred.

If noncommon model errors have norms<=eta_0,eta_1, enlarge the comparison interval
by eta_0+eta_1 on both sides: free energy is 1-Lipschitz in operator norm by
Loewner/eigenvalue monotonicity. Exactly common environment-only errors cancel.
Common errors E touching A instead leave E-Phi(E); acquire their residual norm.
If Phi fixes an acquired common-error algebra, those particular terms also
cancel. Neither locality nor the word 'common' alone establishes that premise.

## 5. Constructive finite optimization and remaining scientific gate

For each fixed kappa_cap in[1,d], add the linear Choi constraint
Lambda(I_A)<=kappa_cap I to the source's SDP and maximize c. Its certified
solution gives c-tau log kappa_cap. Optimizing this score jointly is not
automatically a concave/SDP problem, because -log kappa is convex. A safe finite
construction is a mesh of caps with spacing h, including d. Every channel fits
the next cap, losing at most tau log(1+h)<=tau h in score. Solving the fixed-cap
SDPs to additive e then approximates the BEST SCORE IN THIS CERTIFICATE FAMILY
to e+tau h using O((d-1)/h+1) problems. Cap1 may be handled separately or covered
by the next positive cap. Outward log/spectral error must be charged.

This is polynomial only in matrix dimensions and requested additive accuracy,
not in active spin count. The source Choi representation remains d^4; no
large correlated chemistry example, efficient generic entropy-gain oracle or
affordable region-size convergence theorem is supplied. A scientifically useful
gate is a realistic symmetry/sector-constrained active patch with an acquired
model and a robust thermal action margin under matched bootstrap/correlated-
sampling baselines. The new certificate closes a mathematical thermal step,
not the physical-input or realistic-environment restriction problem.

## 6. Verification and primary-source scope

The independent program reconstructs Pauli Hamiltonians and the singlet channel
without importing producer code; exact rational/symbolic checks are separated
from finite floating partition-function diagnostics. No global environment is
acquired or solved by the proposed certificate; small random environments are
only diagnostic controls. No external proof review or physical experiment.

Primary overlap: A.S.Holevo, [entropy gain](https://arxiv.org/abs/1003.5765), and
Holevo–Giovannetti, [quantum-channel survey](https://arxiv.org/abs/1202.6480),
establish existing entropy-gain context; the latter abstract was read, and full
HTML access for the former failed. Frey–Funo–Hotta,
[strong local passivity](https://arxiv.org/abs/1404.5081), was located by primary
abstract as a comparator. These locators do not clear priority or supply a
theorem about the present paired common-environment free-energy optimization.
The elementary proof of(1) is supplied in full so it does not depend on
unavailable paper text. Historical originality remains UNKNOWN.
