# Local reactive control of an unknown thermal transport law

30 October 2026. Root construction and proof. This is a finite-band response
and noise theorem, not an assertion that passive network synthesis or integral
control is new. It uses the stronger ordinary reciprocal-wave construction
developed during the same investigation and makes its unknown-source receiver
explicit. The application in `SELECTIVE_TRANSPORT_COUPLING_AND_ACTION.md`
selects a physical task: couple the net currents of two native systems while
retaining their independent nonflat density evolution.

## 1. Consequence and actual interfaces

An actual local controller can approximate a nonlocal constraint on thermal
currents without identifying the native kinetic matrix. Its target is the
**actual impedance-metric constraint**, which generally differs from an
Euclidean subtraction of current. Both force response and thermal noise are
controlled in a declared frequency band. Prepared correlations alone do not
supply the response port.

Let v be m physical native currents, with density continuity `dx=Bv dt`.
All native displacement, including the controller's reaction, is counted in v.
Apparatus energy/charge transported in a different channel is a separately
declared output; it is not implicitly included in a suppressed native current.
Let the native quadratic density energy have matrix H, and write

    K=B^* H B >=0.

The complete native linear port, in Laplace variables, is

    [R(z)+K/z] v = f + xi.                                  (1)

R(z) is an unknown causal passive matrix impedance. It can include inertia,
arbitrarily many hidden linear relaxation coordinates, and a nonrational bath
memory. The actual port, its stationary initialization, and its load response
are supplied; they do not follow from static Gibbs weights. In the band
`0<|omega|<=Omega`, warrant

    Re R(i omega) >= r_- I,       ||R(i omega)|| <= r_+,       (2)

where `Re M=(M+M^*)/2` and `0<r_-<=r_+`. The entire causal system is assumed
well defined, with no visible undamped current mode. A frozen hidden parameter
may choose R within this class; all estimates below are pointwise uniform in it.
No finite predictive-state dimension, hidden-state reset, or mixing time is
inferred from (2).

For the thermal-noise statement the actual native bath is stationary Gaussian
at temperature T and obeys

    S_xi(omega)=2T Re R(i omega).                            (3)

Its innovations are independent of the controller bath at this same T. Known
cross-bath correlations would need their actual cross-spectrum; they are not
silently discarded. Bounds (2) are warranted population/interface bounds, not
a finite-data acquisition theorem. A finite calibration grid alone does not
certify all frequencies without a valid regularity or realization premise.

Choose a real, bounded-range controller matrix A with bounded local coefficients.
Its columns are colocated with the native current ports. Put

    L=A^* A,    P=projection onto ker A,    Q=I-P,
    lambda=min positive eigenvalue of L.

The desired controlled currents are P v. Require `B P=0`: the selected
directions are native cycles rather than density sources. This requirement
implies `KP=PK=0`. The choice of a local A is an actual architecture. Arbitrary
desired projectors are not claimed to have such a local realization.

## 2. Build the controller from local reciprocal ports

Use normalized storage q in R^m and a second field p with A's row dimension.
For a>0, gamma>=0 and g>0, run

    dq = (g v-a A^* p)dt,
    dp = (a A q-gamma A A^* p)dt + sqrt(2T gamma) A dV,       (4)

and apply the reciprocal native force `-g q`. The coupling is two way: current
charges the local storage and storage reacts on that same current. A sensor
writing a number is not this force port. The auxiliary damping and noise act
through A and A^*, conserving the protected storage sum. Every operation in
(4) is local when A is local. No projector P is computed or physically applied.

The controller energy is `(||q||^2+||p||^2)/2`. The conservative terms exchange
energy with the native port at power `g q^* v`; the native reaction supplies
the negative of that power. Damping loses `gamma ||A^*p||^2`, with its actual
matched thermal noise. An independent grounded damper on p is a different
architecture, and may destroy the useful transport receiver.

At thermal equilibrium the controller's normalized coordinates have covariance
T I (decoupled conserved p directions may instead be fixed). These are local
independent preparations, or a warranted joint equilibrium preparation. The
displacement-unit counter q/g has covariance `T/kappa`, `kappa=g^2`. This pays
weak tap precision/compliance and range, not automatically divergent stored
thermal energy. Actual preparation and any retained old record must support
the stated conditional future bath law.

Exactly, on every trajectory,

    P[J(t)-J(0)] = [Pq(t)-Pq(0)]/g.                         (5)

Thus any unit vector u in ker A has equilibrium variance
`Var(u^*J(t))<=4T/kappa`. This endpoint statement needs no kinetic
identification. Whole-horizon claims additionally use the actual response and
Gaussian path bounds, as supplied for the ring in the complementary proof.

## 3. Exact impedance and the constrained target

Eliminating p,q in the stationary linear response gives the controller impedance

    C_kappa(z)=kappa (z I+gamma L)
                        [z^2 I+gamma z L+a^2 L]^{-1},      (6)

understood by continuous extension on ker L, where it is `kappa/z`.
This follows on every eigenspace of the real symmetric L, and is an operator
identity by its spectral calculus. For an eigenvalue ell>0,

    c_ell(i omega)=kappa(i omega+gamma ell)
                         /(a^2 ell-omega^2+i gamma ell omega),
    Re c_ell = kappa gamma a^2 ell^2
               /[(a^2 ell-omega^2)^2+gamma^2 ell^2 omega^2]>=0. (7)

The lossless singular frequencies are handled by limiting the passive response;
the band chosen below is strictly below every nonzero controller resonance.

The actual native admittance and its intended ideal receiver are

    Y=[R+K/(i omega)+C_kappa]^{-1},
    Y_* = Q [Q(R+K/(i omega))Q |_Q]^{-1} Q.                  (8)

Y_* is the same native impedance restricted to currents in Q. It is a
mathematical comparison object, not a free physical constraint operation.
It retains native hidden memory in every allowed direction. It does not
promise a prescribed numerical conductivity independent of R.

For a static positive resistance R and no density storage at the measured
mode, putting D=R^{-1} gives, for a matrix U with orthonormal columns spanning P,

    Y_* = D-DU(U^*DU)^{-1}U^*D.                            (9)

This is obtained by solving `R v=f+U ell`, `U^*v=0` for the actual Lagrange
force. It is not generally `Q D Q`. In particular, a density-preserving
Euclidean current subtraction is a different operation when `BDU!=0`.

## 4. Uniform finite-band realization theorem

Assume

    Omega^2 <= a^2 lambda/2,
    r_+ Omega/kappa <= 1/2.                               (10)

Define

    e=2 Omega/kappa,
    d= (2 kappa/a^2)(gamma+Omega/lambda),
    Delta = d/r_-^2 + e(1+r_+/r_-)^2 + r_+^2 e^2/r_-.      (11)

Then, uniformly for every actual native R obeying (2),

    sup_(0<|omega|<=Omega) ||Y(i omega)-Y_*(i omega)|| <= Delta. (12)

Limits at zero are included whenever the actual boundary values exist.

### Proof

Decompose all matrices into Q and P blocks. Write
`Z_0=R+K/(i omega)`. Since KP=0, its off-diagonal blocks are exactly those of R,
with norms at most r_+. On P the full impedance is

    H_P=P R P + kappa/(i omega) I_P.

The Neumann estimate using (10) gives `||H_P^{-1}||<=e`. On Q, (6)-(7) and
`ell>=lambda` give `||Q C_kappa Q||<=d`.

The Q Schur complement is

    S=Q Z_0 Q + Q C_kappa Q - R_QP H_P^{-1} R_PQ.           (13)

Both `(Q Z_0 Q)|_Q` and S have inverse norm at most `1/r_-`.
For the latter assertion take any q, set `p=-H_P^{-1}R_PQ q`, and observe

    Re(q^*S q)=Re[(q,p)^*Z(q,p)]
               >=r_-(||q||^2+||p||^2)>=r_-||q||^2.

Thus no small Schur-remainder assumption is used to infer stability. The
resolvent identity now gives

    ||S^{-1}-(QZ_0Q)^{-1}|| <= (d+r_+^2 e)/r_-^2.

The two off-diagonal inverse blocks each have norm at most `r_+ e/r_-`.
The P inverse block has norm at most `e+r_+^2 e^2/r_-`. Adding these four
block bounds proves (12). The proof uses no commutativity between hidden
kinetics and the controller geometry, and no finite-dimensional realization
of the hidden bath. QED.

For bounded gamma and a, on a diffusive band `Omega=O(lambda)` the useful
window is `lambda << kappa <<1`; Delta tends to zero. For a ring,
`lambda~N^{-2}`. A choice `kappa~sqrt(lambda)` balances the two principal
terms and gives `Delta=O(sqrt(lambda))` on that band. This is a bound for this
architecture, not a universal optimality claim. The observation band lies
below the controller's communication frequency `a sqrt(lambda)`.

## 5. Response and noise are received together

Eliminating the independent controller bath gives its force-noise spectrum
`2T Re C_kappa`. Therefore the actual current spectrum is exactly

    S_v=2T Y Re(Z) Y^*=2T Re Y.                            (14)

The identity follows from `Y(Z+Z^*)Y^*=Y+Y^*`. The same identity on Q gives
`S_*=2T Re Y_*`. Consequently

    sup_band ||S_v-S_*|| <= 2T Delta.                      (15)

This is a complete stationary Gaussian-law statement at the declared linear
observation interface: its mean response and all covariance functions are
specified. It is not a claim about an arbitrary non-Gaussian bath having the
same two-point spectrum. Unknown response has not been inferred from
equilibrium weights alone; (1)-(3) are the actual receiving interface.

For a deterministic force f in L2, Plancherel gives

    ||v_mean-v_*mean||_L2 <= Delta ||f||_L2                 (16)

if its spectrum lies in the band. A causal finite-duration input cannot be
strictly band limited. When the native coercivity bound also holds outside
the band, its actual spectral leakage instead gives

    ||difference||_L2 <= Delta ||f_in||_L2
                                  +(2/r_-)||f_out||_L2.    (17)

Alternatively supply a separate warranted out-of-band response bound. No
unpaid infinite-past preparation is hidden in a finite-time forcing claim:
(16) is the stationary convolution receiver, and a different initial state
has its own actual transient. The explicit nonflat time-domain theorem for
the two-ring Gaussian program is separate.

## 6. What finite observation precision can certify

An exactly constrained ideal P-current is singular relative to a finite-kappa
continuous Gaussian current. A noiseless observation of that coordinate can
give total variation one even when (12) is small. Therefore small admittance
error is not silently converted to fine-record TV.

For a specified d-dimensional linear observation with frequency response
F(omega), define

    A_in=int_band ||F(omega)||_op^2 d omega/(2pi),
    A_out=int_outside ||F(omega)||_op^2 d omega/(2pi).

Under the bounds above its covariance difference has norm at most

    delta_Sigma=2T Delta A_in+(4T/r_-)A_out.                 (18)

Suppose the actual measurement adds an independently prepared Gaussian sensor
noise `N(0,sigma^2 I_d)` to both experiments. This is a paid sensor operation,
not a mathematical regularization retroactively attached to a noiseless task.
Let delta_mu be the actual mean-vector difference, computed or bounded from
the same force/filter interface. If `a_0=delta_Sigma/sigma^2<1`, the elementary
Gaussian relative-entropy formula implies

    KL(actual||ideal) <= ||delta_mu||^2/(2 sigma^2)
                         +d a_0^2/[4(1-a_0)],
    TV <= sqrt(KL/2).                                     (19)

Indeed, conjugate the covariance difference by the square root of the ideal
covariance (which is at least sigma^2 I); every relative eigenvalue has modulus
at most a_0, and `u-log(1+u)<=u^2/[2(1-a_0)]`. This controls the whole stated
finite measurement vector, including correlations across times and specimens.
Increasing its dimension or removing sensor noise changes the precision cost.

If a retained old record chooses the frozen native port or the deterministic
program, apply this bound conditional on that record only when its actual
initializer and future bath laws satisfy the same premises. Then average the
conditional TV bound while retaining that same record. Neither future bath
logs nor arbitrary adaptive feedback are covered by this open-loop stationary
Gaussian receiver. A fixed-probability calibration failure does not support
a speed-N rare-history statement.

## 7. Boundaries and primary construction credit

Passive interconnection, thermal fluctuation-dissipation, metric constraints,
integral control and Schur complements are established. Relevant primary
constructions are Freitas--Delvenne--Esposito, *Stochastic and Quantum
Thermodynamics of Driven RLC Networks*, PRX10,031005 (2020),
https://arxiv.org/abs/1906.11233; Ferguson et al., *Robust integral action of
port-Hamiltonian systems*, https://arxiv.org/abs/1801.06279; and
Lelievre--Rousset--Stoltz, *Langevin dynamics with constraints and computation
of free energy differences*, https://arxiv.org/abs/1006.4914.
Their primary constructions inform the comparison; they do not supply an
unmeasured native transducer in this theorem.

The proposed increment is the explicit local receiver, its uniform finite-band
response/noise error under hidden impedance, and the selected transport-history
application. Historical priority for this composition is unresolved. It is
not a newly discovered thermodynamic law or a certified manufactured device.
The independent nonlinear particle-field attack is saved with its missing
rare-history lemma and close Maggs--Levrel predecessor; it is not completed by
the Gaussian theorem.
