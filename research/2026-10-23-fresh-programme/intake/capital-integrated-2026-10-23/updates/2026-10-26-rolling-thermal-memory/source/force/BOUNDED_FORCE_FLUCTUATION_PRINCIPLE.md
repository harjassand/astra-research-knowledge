# What a bounded internal force changes in a complete Gaussian support

25 October 2026. This chooses a different physical consequence from the
costly compact rotor: a fixed bounded internal quantum force can change
cold transport without borrowing large mechanical inertia or hidden
kinetic fluctuations. The exact organising identity below applies to the
ENTIRE canonical support and its leads at equilibrium, not a projected
oscillator or an elastic transmission approximation.

The spin--oscillator/reaction-coordinate mechanism and momentum squeezing
are conventional. The claim here is the explicitly proved matrix response,
all-mode kinetic domination and reorganisation-energy boundary, together
with its consequence for the already constructed finite-band cold family.
No priority, acquired material conjunction or finite equilibration clock
is inferred.

## 1. Definite full Hamiltonian

Use a finite pinned Gaussian regulator with actual canonical mechanical
coordinates q and momenta p, constant positive mass matrix M and positive
spring matrix K. The physical mass representation can be diagonal; a
constant canonical change to common/relative coordinates is allowed. Add
a finite-dimensional internal system with self-adjoint Hamiltonian H_A
and ONE bounded Hermitian force operator Q, ||Q||<=q_*:

    H=H_G+H_A-lambda Q v^T q,
    H_G=(1/2)p^T M^-1 p+(1/2)q^T Kq,                  (1)
    C=v^T K^-1 v.

There is no coupling to mechanical momentum and no extra thermal port.
Q need not commute with H_A. A bounded Q^2 counterterm, if physically
specified, belongs in H_A; it is not silently omitted. Completing the
mechanical square makes the lower stability bound explicit:

    H >= H_A-(lambda^2 C/2)Q^2.

This also defines a lower-bounded operator/Gibbs state through the usual
quadratic-form construction. No classical replacement of Q is required.
Take a local thermodynamic lead limit only after the finite-regulator
identities below. The static port compliance C must remain bounded for
the uniform energy conclusions.

## 2. Exact matrix response identity without a spin path assumption

Let beta be inverse energy temperature, nu_n=2pi n/(beta hbar), and use
CONNECTED, normalized imaginary-time covariances

    Chi(n)=(1/hbar)int_0^(beta hbar) exp(i nu_n tau)
           <T_tau (q(tau)-qbar)(q(0)-qbar)^T> d tau,
    S(n)=(1/hbar)int_0^(beta hbar) exp(i nu_n tau)
           <T_tau (Q(tau)-Qbar)(Q(0)-Qbar)> d tau.

Put G_n=(K+nu_n^2 M)^-1. The exact mechanical equation of motion and
its equal-time canonical contact term give

    Chi(n)=G_n+lambda^2 G_n v S(n) v^T G_n.            (2)
    qbar=lambda K^-1 v Qbar.                         (3)

For completeness, applying -M partial_tau^2+K to the time-ordered q,q
correlation produces hbar*delta times the identity plus the force-Q
correlation. Applying it to q,Q produces only the latter source:
[q,Q]=[p,Q]=0, so that cross equation has no contact term. Its solution
is lambda G_n v S(n). Substitution proves (2), including n=0 after
centering. Equivalently it is the exact source identity from Gaussian
elimination. This equation-of-motion derivation does not require positive
classical paths for the internal system or commutation of its different
time operators.

Hermitian KMS autocorrelation has a nonnegative Matsubara coefficient:
S(n)>=0. Its Lehmann representation pairs energies E_a<E_b with
2(p_a-p_b)(E_b-E_a)/[(E_b-E_a)^2+(hbar nu_n)^2], times the nonnegative
matrix element squared; the static diagonal term is nonnegative too.
Also

    (1/beta)sum_n S(n)=Var(Q)<=q_*^2.                 (4)

Hence Chi(n)-G_n is a positive semidefinite rank-one matrix at EVERY
Matsubara frequency. All coefficients refer to the full interacting Gibbs
state of (1), not a free internal-state correlation.

## 3. All canonical momentum fluctuations decrease

For any real linear combination f^T p, stationarity and p=M dot q give
the canonical contact identity

    Gamma_p=(1/beta)sum_n [M-nu_n^2 M Chi(n) M].        (5)

Gamma_p is the symmetrized momentum covariance; its mean is zero. The
apparent two divergent pieces in (5) are kept COMBINED. One derivation
uses the positive Lehmann measure of (Mf)^Tq, its canonical first moment,
and the coth partial-fraction identity. At each finite regulator the
combined series converges to <(f^T p)^2>. Thus there is no independent
infinite contact subtraction or uncounted ultraviolet completion.

Subtract the corresponding Gaussian formula and use (2):

    Gamma_p-Gamma_p,G
       =-(lambda^2/beta)sum_n nu_n^2 S(n)
          (M G_n v)(M G_n v)^T <=0.                   (6)

The n=0 term vanishes. Every actual mechanical momentum combination has
variance AT MOST that of the unchanged free Gaussian support at the same
temperature. This is exact at arbitrary coupling and temperature for (1).
The bounded internal force does not implement a large kinetic mass by
exciting hidden mechanical momentum. It changes the fluctuation spectrum
in a different way from the compact rotor.

For Y=v^T q, write c_n=v^T G_n v<=C and V_0=Var_G(Y).
Equations(2)--(4) give the complementary coordinate inequality

    0<=Var(Y)-V_0
       =(lambda^2/beta)sum_n c_n^2 S(n)
       <=lambda^2 C^2 Var(Q).                         (7)

There is no contradiction with the fixed canonical f-sum: the exact
contact in (5) is the same before and after adding the internal sector.

## 4. A finite energy cost for the ENTIRE Gaussian support

Let Delta T be the full mechanical kinetic-energy change from the free
Gaussian state, and Delta V_c the connected spring-energy change. The
identities give

    Delta V_c=(lambda^2/(2beta))sum_n S(n)
                         v^T G_n K G_n v >=0,
    Delta T=-(lambda^2/(2beta))sum_n nu_n^2 S(n)
                         v^T G_n M G_n v <=0.         (8)

Set D=M^-1/2 K M^-1/2. The scalar eigenvalue inequalities

    D/(D+nu^2)^2 <=D^-1,
    nu^2/(D+nu^2)^2 <=(1/4)D^-1

then prove

    0<=Delta V_c<=lambda^2 C Var(Q)/2,
    0<=-Delta T<=lambda^2 C Var(Q)/8.                 (9)

The mean in (3) adds lambda^2 C Qbar^2/2 to the spring energy and no
momentum energy. Consequently, with

    E_*=lambda^2 C q_*^2/2,

the TOTAL uncentered spring-energy increase is at most E_*, the total
mechanical kinetic-energy decrease is at most E_*/4, and

    |<H_G>_H-<H_G>_G|<=E_*.                          (10)

The interaction obeys
0<=lambda<Q v^Tq><=lambda^2 C<Q^2><=2E_*.
Here the mean contribution is included; its connected counterpart follows
by summing c_n S(n). An additive counterterm or H_A energy is separately
counted as specified in (1).

For a positive pair-spring physical support, (6) lowers each individual
kinetic variance and (2) raises each individual spring-bond variance.
Thus the two signed sums in (8) do not hide cancellations among omitted
lead modes. If C is bounded uniformly in the chain regulator, the sums
of local spring-energy increases and kinetic-energy decreases in a local
thermodynamic limit retain the bounds (9)--(10), by finite partial sums
and positivity. The infinite reservoir baseline energy is not called a
finite number. These are bounds on its explicitly defined excess.

Finite excess energy does NOT imply finite preparation time, finite
coherent phonon number or a unitary static force shift in one vacuum
Fock representation. The infrared preparation/record problem is still
the one treated by the earlier finite-control operations.

The coordinate, momentum-upper and potential-energy bounds have an exact
attaining case, not just a relaxed spectral extremum. If [H_A,Q]=0, Q is
conserved by the FULL contact, so S(n)=beta Var(Q) only at n=0. Each
internal sector is an ordinary Gaussian support displaced by
lambda K^-1 v Q. The momentum covariance is EXACTLY its free value,
Var(Y)-V_0=lambda^2 C^2 Var(Q), and the total spring-energy increase is
lambda^2 C<Q^2>/2. Thus Q^2=q_*^2 attains E_*.

This conserved example also shows why static softness is insufficient
for a heat operation. The static sector atom gives a Curie contribution
to the imaginary-time susceptibility, but no nonzero-frequency retarded
Q commutator. Its mechanical retarded response remains G and it adds no
heat scattering. A cold deficit needs the actual slowly changing internal
sector, not simply its large static susceptibility or reorganisation.

## 5. Actual finite-band spin contact, including a uniform kinetic cap

Apply this to FINITE_BAND_CONTACT.md: M includes both terminal atoms and
the genuine spin host, the two identical Rubin leads are retained, and

    Y=u_R-u_L, B_0=M/4, Q=sigma_z, lambda=k_0 d,
    H_A=-(hbar Delta_0/2)sigma_x-(epsilon/2)sigma_z,
    C=1/k_0 in the local infinite-chain limit.

The constant k_0 d^2/2 in the stated physical square is unchanged. Finite
far-pinned regulators have C<=1/k_0, so E_*<=k_0 d^2/2 uniformly. Neither
Delta_0 nor epsilon alters that bound. All mechanical masses, k_0,
lambda, lead atoms/springs and their finite band remain fixed.

The fixed Gaussian reference obeys all-mode elementary bounds

    V_0(T)<=k_B T/k_0+hbar/(2sqrt(B_0 k_0)),
    <P_Y^2>_G<=B_0 k_B T
                        +(hbar/2)sqrt[B_0(k_0+kappa_lead/2)].

The second follows from coth x<=1+1/x and Cauchy--Schwarz over the complete
normal-mode measure. The local moment sum is K_YY=k_0+kappa_lead/2;
the canonical mass is B_0. Bound modes, if a different fixed parameter
choice has them, are included by this normal-mode proof.
Equations(6)--(7) therefore bound the full port position, bare canonical
momentum and every other local mechanical momentum UNIFORMLY for
T<=T_0 and any retuned spin coefficients.

There is a stronger local limit as Delta_0 tends to zero. For n!=0 the
spin double commutator is

    <[sigma_z,[H,sigma_z]]>=2hbar Delta_0<sigma_x>,
    nu_n^2 S(n)<=2|Delta_0|/hbar.

Use c_n<=1/(k_0+B_0 nu_n^2) and the decreasing positive Riemann-sum bound

    (1/beta)sum_(n!=0)c_n^2
       <=(hbar/pi)int_0^infinity dnu/(k_0+B_0nu^2)^2
       =hbar/[4sqrt(B_0)k_0^(3/2)].

Equation(6), restricted to this actual relative momentum, proves

    0<=<P_Y^2>_G-<P_Y^2>_H
       <=[lambda^2 B_0^(3/2)/(2k_0^(3/2))]|Delta_0|. (11)

The mechanical momentum variance returns to its finite FREE Gaussian
value uniformly in temperature as the actual transverse coefficient
vanishes. This is not a growing-inertia/large-velocity mechanism.

For the already fixed natural-unit choice M=Z=hbar=1,
B_0=k_0=1/4, kappa_lead=2, alpha=1/4, d^2=pi/4:

    Var(Y)<=2+pi/4+4theta_0,
    <P_Y^2>_H<=theta_0/4+sqrt(5)/8,
    E_*=pi/32,
    0<=<P_Y^2>_G-<P_Y^2>_H<=(pi/128)|Delta_0|.        (12)

Every host kinetic/strain-energy EXCESS is bounded as above, including
the complete fixed leads. The spin splitting energy is bounded too.

## 6. Consequence and strongest ordinary explanation

The accepted finite-band cold family chooses the ACTUAL bare splitting
Delta_0(theta)=2y theta exp(alpha c_L), alpha=1/4,y=.01,
with the exact fixed-cutoff c_L and |epsilon|<=hbar theta. It has a strict
positive limiting heat deficit under its explicit inclusive equilibrium
scattering/current contract. Equations(9)--(12) now show that this result
does not require unbounded mechanical kinetic energy or unbounded total
excess strain energy. The source contains the actual continuum/all-order
cold proof; it is not being replaced by a guessed spin-only scaling law.

The earlier positive scalar HARMONIC mass/port-motion frontier therefore
cannot be restored simply by adding a fixed mechanical kinetic-energy
cap. A bounded internal quantum force is a distinct escape. By contrast,
COMPACT_LOCK_KINETIC_COST.md shows that the literal winding amplifier
does pay divergent actual bare kinetic fluctuations. This is a comparison
of two specified mechanisms, not a universal classification of every
nonlinear or lever implementation.

The equally informed conventional explanation is the Rabi/spin-boson
reaction-coordinate model and its familiar momentum squeezing. Thorwart,
Paladino and Grifoni's primary Section2, Eqs(1)--(5), gives the exact
spin-plus-damped-oscillator mapping:
https://arxiv.org/html/cond-mat/0310140v1 . Those equations were reopened
directly. Joshi, Irish and Spiller, Scientific Reports7,45587 (2017),
Eqs(18)--(22), discuss enhanced position noise and reduced momentum noise
in a dispersive Rabi ground state and compare numerical full-Rabi results:
https://www.nature.com/articles/srep45587.pdf . Those governing passages
were directly read. They are close physical ancestry; their dispersive
or weak-residual-bath approximations are not used to prove the arbitrary-
temperature, arbitrary-H_A, complete-support identities above.

For inclusive nonlinear heat, the ordinary series-admittance antecedent
is Yamamoto--Glazman--Houzet, Eqs(2)--(8):
https://arxiv.org/html/2403.13552v1 . The actual Rubin normalization and
mechanical KMS/current contract remain those of FINITE_BAND_CONTACT.md.
No novelty clearance is supplied by these bounded comparisons.

The physical cost has moved into the REAL internal degree of freedom,
its force coupling, the cold retuning/bias confidence and physical-time
access. Fixed nonzero Delta_0 has zero cold deficit under the separately
proved fixed-control scope. The control acquisition/response clocks and
finite-instrument UNKNOWN gates remain; neither (6) nor finite energy
prepares an instantaneous KMS/NESS state. A material implementing the
spin/force/lead conjunction and actual finite-window heat validation are
still unacquired. This theorem is an organising response/resource result,
not a manufactured practical device advantage.

## 7. A bounded finite-matrix discriminator

check_bounded_force_fluctuations.py tests the normalizations against two
coupled physical oscillator coordinates with unequal masses and an
internal Hamiltonian containing all three Pauli directions. It directly
diagonalizes the combined Hamiltonian; the reference has the SAME masses
and springs. At oscillator cutoffs8,12,16 the largest selected Matsubara
identity residual decreases from7.96e-6 to8.88e-10 to1.63e-13. The last
case has positive covariance-difference eigenvalues with the predicted
signs, spring-energy increase .2527532966 below E_*=.3657142857, and
kinetic-energy decrease .0119593799 below E_*/4=.0914285714.

The separate commuting-Q case gives momentum covariance equal to its
free value within3.6e-14 and attains the spring-energy bound within2.3e-13.
These are floating oscillator-cutoff diagnostics; their drift does not
certify a continuum bath or a cold heat number. The operator/KMS proof
above supplies that exact equilibrium scope without relying on them.
