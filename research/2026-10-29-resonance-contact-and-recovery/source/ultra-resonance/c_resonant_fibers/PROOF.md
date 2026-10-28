# Finite resonant fibers, collective pair dynamics and a paid compact prediction

This is an explicit closed-Hamiltonian construction, not a generic many-body
closure or a newly acquired physical experiment. The mean-field/pre-relaxation
principle has strong primary antecedents. The actual source, order of limits
and all approximation costs below are narrower than generic late-time
interacting prediction. `PROJECTOR_OBSTRUCTION.md` gives the load-bearing
failure of replacing a finite-band question by an exact resonance projector.
`PRIOR_AND_DECISION.md` states why no new useful capability over an equally
informed pre-relaxation method has been established.

## 1. Exact input and output

Take N divisible by four, N>=8, periodic spinless fermions with CAR, and

    H=H0+lambda V,
    H0=-J sum_j(c_j^dag c_(j+1)+c_(j+1)^dag c_j),
    V=sum_(r=1)^R a_r sum_j n_j n_(j+r),
    A=sum_r |a_r|,  R<N/2,  J>0.

All displayed indices are periodic. The actual consumer fixes R=2,
a1=1,a2=1/3,J=1,N=2^128,lambda=N^-8 and interaction time
tau=lambda*t=1/2. Thus t=2^1023 in J^-1 MODEL units. This clock is a
mathematical input, not a demonstrated isolation time or evidence of utility.

Fourier modes have k=2pi m/N. Let K_N be the representatives
`-pi/2<k<pi/2`, one member of each pair `(k,pi-k)`, excluding the two fixed
momenta. Its size is M=N/2-1. Set

    b_k^dag=c_k^dag c_(pi-k)^dag,  N_k=b_k^dag b_k

on the subspace where a pair is either empty or doubly occupied. The two fixed
momenta are empty. The initial state is the KNOWN compact pure Gaussian state

    Psi0=prod_(k in K_N) [sqrt(3)/2+(1/2)b_k^dag] |vac>.

This input has even parity, specified anomalous pair coherence and about N/4
particles on average. It is not a generic thermal state, arbitrary Gaussian
input, fixed-number ensemble or a state supplied merely through samples.
Every occupied pair has zero H0 energy, so H0 annihilates this entire paired
subspace. Define the bounded even observable

    C=sum_j (-1)^j c_j c_(j+1)=2 sum_(k in K_N) cos(k) b_k,
    O_N=(C-C^dag)/(4iN).

Consequently [H0,O_N]=0 and ||O_N||<=1/4. The output is its specified-time
expectation. It is neither a state reconstruction nor an entire adaptive time
record. N, coefficients and the initial covariance are supplied by these
compact formulas; a generic N-by-N coefficient/state table is not silently
read in sublinear time.

## 2. Exact resonance classification and a finite-volume cost

The one-body dispersion is e(k)=-2J cos k. A momentum-conserving quartic
transition `(k,K-k)->(p,K-p)` has energy difference

    Delta=-4J cos(K/2) [cos(k-K/2)-cos(p-K/2)].

It is resonant exactly for the forward/exchange transitions, or for K=pi
modulo 2pi. For any other transition the difference factors as a product of
three nonzero sines/cosines on the finite grid. Each nonzero factor has
absolute value at least sin(pi/N)>=2/N. Therefore

    |Delta|>=64J/N^3.                                      (2.1)

This deliberately conservative SMALL-GAP cost may not be discarded before
passing to a large-volume limit. The momentum-space quartic representation
has at most N^3 ordered terms, each coefficient bounded by A/N and each
fermion monomial of norm at most one. Write

    V(t)=exp(iH0t)V exp(-iH0t)=Vbar+W(t).

The nonresonant primitive B(t)=integral_0^t W(s)ds thus satisfies

    sup_t ||B(t)|| <= A N^5/(32J) =: b_N.                  (2.2)

Also ||V||,||Vbar||<=AN; Vbar is an exact time average, hence a contractive
conditional expectation on this finite algebra.

Let U_I(t)=exp(iH0t)exp[-i(H0+lambda V)t]. Duhamel followed by integration
by parts against B gives the STATE-INDEPENDENT bound

    ||U_I(t)-exp(-i lambda Vbar t)||
      <=lambda b_N [1+2lambda AN t]
       =lambda b_N [1+2AN tau].                            (2.3)

For completeness the integrand is
`U_I(t,s) W(s) exp(-i lambda Vbar s)`. Differentiating its two unitary factors
in the integration-by-parts remainder costs at most
`lambda(||V(s)||+||Vbar||)`; there is no exponential Gronwall in physical
time. No finite-volume spectral diagonalization is an input oracle.

Since O_N commutes with H0, (2.3) compares the original physical expectation
directly with the secular expectation. Its expectation error is at most
`2||O_N||` times the right side. The receiver conservatively uses that right
side itself. At lambda=N^-8 this is O(A^2 tau/N^2), rather than an unqualified
thermodynamic weak-coupling statement. In particular this construction does
NOT claim the thermodynamic-limit-first regime lambda*N>>tau used in the
usual local pre-relaxation discussion.

## 3. Exact collective pair Hamiltonian

For each interaction range set

    f_r(k)=cos(rk), g_r(k)=sin(rk)       for odd r,
    f_r(k)=sin(rk), g_r(k)=cos(rk)       for even r.

Then f_r^2+g_r^2=1. On the paired subspace put

    Q0=sum_k N_k, Qg_r=sum_k g_r(k)N_k, Bf_r=sum_k f_r(k)b_k.

Literal antisymmetrization of the density vertex gives

    <p,K-p|V_r|k,K-k>
       =(2a_r/N)[cos(r(p-k))-cos(r(p+k-K))].

At K=pi this is `(4a_r/N) f_r(p)f_r(k)`. The full restricted secular
Hamiltonian is exactly

    Vbar_pair=(4/N) sum_r a_r [Q0^2-Qg_r^2
                  +Bf_r^dag Bf_r-sum_k f_r(k)^2 N_k].       (3.1)

The subtracted diagonal prevents counting the forward diagonal twice. The
subspace is invariant: the only non-forward transitions move an entire
K=pi pair. This is not a closure hypothesis about an interacting state.

An equivalent M-qubit Hamiltonian has on-site terms
`(4/N)sum_r a_r f_r(k)^2 N_k` and pair terms `(1/N)V_kl`, where

    V_kl=sum_r a_r [8(1-g_r(k)g_r(l))N_kN_l
                  +4f_r(k)f_r(l)(b_k^dag b_l+b_l^dag b_k)].

For each r the density and exchange pieces act on separate number blocks;
their joint operator norm is at most16|a_r|. Thus ||V_kl||<=16A.

`check_resonance.py` independently Fourier-transforms the literal real-space
two-particle density interaction in Q[zeta_32], checks ALL784 vertices at
N8, then constructs the secular paired block with exact fermionic signs.
It matches all64 entries of (3.1) and checks no secular transition leaves
that block. Exact energy equality is determined in the cyclotomic field,
without a floating tolerance. This is a finite consumer, not a proof of
the all-N classification by testing.

## 4. A constructed mean-field approximation, with a finite-N error

Use the exact product-state mean-field equation for this M-qubit Hamiltonian:
each on-site Hamiltonian is supplemented by the partial expectation of every
V_kl/N in the other one-site state. The approximation remains a product in
pair-qubit variables; the true state need not remain Gaussian or unentangled.

Here is a direct quantitative propagation-of-product-marginals argument, also
valid for these inhomogeneous couplings. Let p_k(t) project onto the one-qubit
mean-field ray, q_k=1-p_k, and

    alpha(t)=(1/M)sum_k <Psi(t),q_k(t)Psi(t)>.

Initially alpha=0. After cancelling the one-body mean-field terms, insert
`p_l+q_l` on the other site in each commutator. The `p_l ... p_l` part cancels
its partial expectation. Write v=max||V_kl||<=16A. Terms of the form
`q_k p_l V_kl q_l p_k` are bounded by v sqrt(alpha_k alpha_l). Terms with
q_l on both sides cost at most2v alpha_l. The remaining pair-creation sum
uses, for fixed k,

    T_k=sum_(l!=k) q_l V_kl p_l p_k,
    ||T_k Psi||^2 <= v^2(M+M^2 alpha).

For distinct l,m, move q_l through the m-site interaction and q_m through the
l-site interaction. Their cross term is bounded by
`v^2 sqrt(alpha_l alpha_m)`; diagonal terms cost v^2. Cauchy--Schwarz over k
and `sqrt(alpha(alpha+1/M))<=alpha+1/(2M)` then give

    alpha'<=8v(M/N)alpha+v/N<=64A alpha+16A/N.

It follows that

    alpha(tau)<=(exp(64A tau)-1)/(4N).                      (4.1)

The trace distance of one marginal from its pure mean-field ray is at most
`2sqrt(alpha_k)`. Averaging the norm-1/2 pair quadratures in O_N gives

    |<O_N>_secular-<O_N>_MF|
       <=sqrt(exp(64A tau)-1)/(4sqrt(N)).                  (4.2)

This is the paid state/closure premise. It is a standard mean-field-type
mechanism, proved here with the actual interaction norm and source state;
it is not ETH, Markovianity, local equilibrium or an assumed factorization
of the true global state.

## 5. The nonlinear Bloch field and an exact self-term cancellation

Let r(k)=(rx,ry,rz), with N_k expectation `(1-rz)/2` and b_k expectation
`(rx+i ry)/2`. Introduce the finite measure

    nu_N=(2/N)sum_(k in K_N) delta_k,

whose mass is 1-2/N. For any measure nu of mass at most one define

    Fx_r=integral f_r rx dnu, Fy_r=integral f_r ry dnu,
    G_r=integral g_r(1-rz)dnu, Z0=integral(1-rz)dnu,
    h_x=sum_r a_r f_r Fx_r,
    h_y=sum_r a_r f_r Fy_r,
    h_z=-sum_r a_r[Z0-g_r G_r].

The finite-N mean-field spin equation is EXACTLY

    partial_tau r(k)=2 h(k,r) cross r(k).                  (5.1)

The on-site term, same-spin subtractions and self-exclusion in (3.1) combine
to an extra field `-(2/N)sum_r a_r f_r(k)^2 r(k)`. It is parallel to r(k),
so it cancels from (5.1), rather than being forgotten as an O(1/N) term.

This is a finite-rank nonlinear collective field, not a linear or Gaussian
fixed-coefficient closure. Its continuum measure is
`dnu=dk/pi` on [-pi/2,pi/2]. Then

    M_y(tau)=(1/4)integral cos(k) ry(k,tau) dnu,
    r(k,0)=(sqrt(3)/2,0,1/2).                              (5.2)

For real profiles use the maximum of the Euclidean vector norms. The map
h is affine with

    |h(r)-h(s)|<=sqrt(5) A ||r-s||_infty.

Comparing to a unit-length target solution, the common rotation drops out
of the derivative of the error norm. Hence the real stability exponent
can be taken as L=5A. A fixed error delta in each scalar collective moment
adds at most6A delta to the spin derivative. Consequently

    profile error <=6A tau exp(5A tau) delta.              (5.3)

This rotational bound is used to pay numerical errors; an unqualified
dimension- or time-independent closure is not asserted.

## 6. Compact quadrature of the source, rather than an N-loop

Write R1=sum_r r|a_r|. For the continuum solution,
`|partial_k h|<=sqrt(5) R1`. The rotation term again drops from the norm of
`partial_k r`, giving `|partial_k r|<=6R1 tau` for the constant initial ray.
The moment integrands have real bound2 and Lipschitz constant at most
`2R+6R1 tau`. Midpoint cells around the finite paired grid and its two missing
endpoint strips therefore give a moment error

    delta_N <= [4+(pi/2)(2R+6R1 tau)]/N.                   (6.1)

At the actual R2,R1=5/3,tau=1/2 this is less than22/N. Combining (5.3) and
the observable quadrature gives the finite-grid error
`delta_N[1+6A tau exp(5A tau)]/4`.

High-order quadrature is also PAID. Continue k analytically to imaginary
height eta while retaining the same real time-dependent collective moments.
The label-dependent spin equation is linear in r once these moments are fixed.
For `S_eta=sum_r |a_r|sinh(r eta)`, its complex norm satisfies

    ||r(k+i eta,tau)||<=exp(6 S_eta tau).                   (6.2)

The real part of the complex cross-product generator is skew-Hermitian;
only Im h contributes to growth, with norm at most3 S_eta. Thus no analytic
strip of the true solution is assumed without a bound.

On the Bernstein ellipse rho=3/2 for k=(pi/2)x, eta=5pi/24. Rational
exponential bounds prove, for the actual two interaction ranges,

    S_eta<13/10,  cosh(2eta)<2,
    M_all=2[1+exp(39/10)]

as a common modulus bound for all moment integrands at tau<=1/2. For a
Q-node Gauss--Legendre rule normalized to probability, a Chebyshev polynomial
of degree2Q-1 and positivity/exactness of the rule give

    delta_Q<=12 M_all (2/3)^(2Q).                          (6.3)

Indeed the Chebyshev tail is at most `2M rho^[-(2Q-1)]/(rho-1)`; both the
integral and the rule are contractions in the sup norm. Its contribution to
the output is `delta_Q[1+6A tau exp(5A tau)]/4`.

`acquire_quadrature.py` actually isolates all48 roots of the exact Legendre
polynomial in disjoint rational sign-changing intervals. Its floating
leggauss call supplies proposals only. The polynomial degree proves these
are all roots; differentiating the polynomial in rational intervals gives
positive weights. A rational Machin bound and Taylor remainders give every
trigonometric parameter. The actual fixed-point intervals contain the exact
positive normalized rule, including its sum-one identity. No quadrature
oracle or uncertified floating root is a scientific premise.

## 7. Numerical propagation without a free nonlinear-flow oracle

The delivered fixed query uses 48 modes, 512 steps of h=1/1024, Taylor
degree24 and 48 fractional bits. Exact interval arithmetic is performed in
signed __int128 with outward integer divisions. Products are safe because
every interval endpoint is checked strictly inside2^62, so each product is
strictly inside2^124. Intermediate sums are checked before conversion.
Restart points are additionally checked coordinatewise within2 and with
Euclidean norm at most1.01. No state vector or density matrix is allocated.

For a complex coordinate polydisc of radius1 around such a restart, the
right side of the exact quadrature ODE has coordinate bound40A and
Lipschitz bound32A. Picard iteration on the complex time disk
`r_time=1/(256A)` maps that polydisc strictly into itself and is a contraction.
The analytic solution has coordinate modulus less than3 there. Since
h/r_time=1/3 for the actual A=4/3, the degree24 coordinate Taylor tail is
bounded by `3*3^-24`, the conservative value used by the code.

The rescaled Taylor coefficients obey

    (k+1)y_(k+1)=2h sum_(j=0)^k H_j cross y_(k-j),

with H_j the affine collective field applied to the known coefficients.
This recurrence is propagated in intervals. At each endpoint the code
returns an exact dyadic midpoint and retains a Euclidean local-error bound;
it does NOT discard the old uncertainty without payment. The sum of those
local bounds is exactly

    3085352 / 2^48.

The initial dyadic approximation contributes at most2^-48. Real rotational
stability (5.3) propagates their sum by exp(5A tau); dividing by4 pays the
observable. Every restart is a known real point, and the exact target
quadrature flow has unit Bloch length, so no global interval-wrapping
assumption is needed. Parameter intervals are shared uncertain constants;
the local interval steps enclose every fixed exact parameter tuple admitted
by the acquired Gauss rule.

## 8. Actual original-model prediction and costs

`receive_prediction.py` composes exact rational errors, Taylor exponential
enclosures and an integer-square-root upper bound. It returns

    -0.10927576484299249 <= <O_N(t)> <= -0.10927561115965030,

with total width below1.536834e-7 for the declared compact source. The separate
absolute error terms (before the final extraction interval width) are

    validated numerical flow     <=7.681630e-8,
    continuum quadrature         <=4.259969e-13,
    finite-N paired grid         <=1.828469e-36,
    quantum product-marginal      <=2.494419e-11,
    original-H averaging         <=4.797872e-79.

The source has an exponentially large quantum state space, but that fact and
the huge time label do not by themselves imply a new useful capability. The
coupling, symmetry, state and queried object are unusually restrictive.

Actual host work after imports: exact source replay0.794147s; parameter
acquisition1.160137s; C++ compilation0.785285s; binary wall time1.021156s,
including0.522976s computation before serialization; rational receiver
0.011509s. The exact solver used55,443,456 interval multiplications,
54,927,360 interval additions and3,538,944 explicit scalar interval-division
operations. Products' directed scaling divisions are part of each multiply,
not extra falsely omitted work. Peak RSS was not measured. Primary downloads,
PDF extraction/reading, derivation and failed module probes are separate
retained costs. No original-time trajectory, Hilbert-state construction,
physical data, source fit, sampling or N-loop was performed.

As a mathematical algorithm, for `tau<=log(N)/(128A)` the quantum error is
at most N^-1/4/4. At lambda=N^-8 the averaging error is O(tau/N^2), and the
finite-grid error also vanishes. Analytic label quadrature requires
`Q=O(tau+log(1/epsilon))`; analytic Taylor propagation uses O(tau) steps and
degree/precision O(tau+log(tau/epsilon)). Exact polynomial root isolation can
be used if numerical proposals fail. Thus the compact family admits a
polynomial calculation in log N and log(1/epsilon), provided the finite-N
physical approximation errors already meet the requested tolerance. The
delivered executable is the actual fixed query above, not a claimed complete
generic implementation for arbitrary models, N, states or tolerances.

No practical quantum-device promise follows. A generic Hamiltonian error
has the usual time-amplified Duhamel cost; preparation, structural dispersion/
boundary accuracy and isolation for this time are not acquired. This is not
the thermodynamic-limit-first or fixed experimental-coupling regime. The
strongest source-aware ordinary resonant-HFB/pre-relaxation method receives
these same collective equations and may use the same quadrature and solver.
There is no demonstrated algorithmic separation from that informed method.
