# Finite-pulse energy tomography through one coherent port

This independent mechanism was derived and its finite model experiment
executed BEFORE reading root_nonlinear_port. It is a classical coherent-modal
equation, not automatically a quantum few-excitation Hamiltonian theorem:

 dot psi=-iK psi-i g(t)(|psi_j|^2 psi_j)_j+e1 u(t),
 y=e1^T psi, K=K^T real.                              (E1)

The Euclidean amplitude metric, complex phase reference, calibrated coherent
input/output, known dimension, exact cubic law and a common switchable g
are substantive model resources. The network is connected, n>=2, and the
linear port is cyclic. Global g=0 is permitted for steering/readout; K never
switches off. No physical apparatus/source qualification is claimed here.

## 1. Qualified linear coordinates and finite access

Ordinary one-port linear spectral/realization identification supplies K0,e0
and a WARRANTED common-Euclidean error budget. For a cyclic symmetric K it
is equivalent to a real orthogonal physical realization psi=Qx,
K=QK0Q^T, Qe0=e1. The scalar transfer cannot distinguish such Q. Known n,
mode visibility, bandwidth/alias bounds and fit conditioning must be paid;
a small finite trace residual does not exclude arbitrary hidden dark modes.

For g=0, piecewise-constant complex drives over L known finite intervals
give x(T)=U(T)x(0)+B u, U(t)=exp(-iK0 t),
B_l=integral_(interval_l) U(T-s)e0 ds. If sigma_min(B)>=s_p>0,
u=B^+[x_target-U(T)x(0)] supplies an actual finite port steering command.
Its coefficient norm is at most target-displacement norm/s_p. Integrated
drive power is h||u||^2 for equal interval widths h; peak amplitude and
finite switching edges need separate bounds. This is ordinary controllability,
not an ability to directly prepare each hidden node.

After a nonlinear pulse turn g off and collect the finite linear records
y_l=e0^T U(t_l)x+noise. With C_l=e0^T U(t_l) and s_o=sigma_min(C)>0,
xhat=C^+y has error<=||noise||/s_o for exact C. A warranted C perturbation
dC adds dC||x||/s_o. In the same fixed real coordinates, calibrated K/e
errors dK,de give dC<=sqrt(sum_l(de+||e0||t_l dK)^2).

Unitary waiting is NOT reset. Coherent reset is another finite steering
command to target0, after the measured state has evolved through its known
readout interval. Its residual includes tomography error, propagation error
and the measured steering-matrix uncertainty times the command norm. The
experiment actually performs this port-only cancellation and carries its
remaining residual into the next preparation. It also reads the initial
state before each science pulse, propagating it through that readout interval;
no free arbitrary-state or hidden-reset oracle is inserted.
The prototype's FIRST linear calibration starts from an assumed zero field.
Its later calibrated coherent resets do not pay that bootstrap premise.
Ordinary driven linear subspace identification can treat an unknown initial
condition as a nuisance state, but that replacement is not executed here.

## 2. Exact finite-pulse linear equations

In linear reference coordinates define the fully REAL symmetric tensor

 T_abcd=sum_j Q_ja Q_jb Q_jc Q_jd,
 F_T(x)=sum_abcd T_abcd x_a conjugate(x_b)x_c conjugate(x_d)
       =sum_j |(Qx)_j|^4.                              (E2)

Its Frobenius norm is sqrt(n). During an unforced pulse with any fixed known
g!=0, Hamiltonian E=x^*K0x+(g/2)F_T(x) is constant. Thus the ACTUAL finite
endpoint pair x,y gives exactly

 F_T(y)-F_T(x)=(2/g)(x^*K0x-y^*K0y).                   (E3)

K remains on. No small-g derivative, short-time limit, instantaneous nonlinear
kick, high-frequency limit or complete Volterra oracle is used. The left side
is linear in the m=binomial(n+3,4) real symmetric tensor coefficients. Fully
complex initial directions matter: the real tensor is evaluated on complex
fields with the actual Kerr conjugations, not replaced by (q dot x)^4 there.

## 3. Whole-family injectivity, then a finite design

Consider the actual Kerr flow Phi_t in physical coordinates. Suppose a
fully symmetric REAL order4 tensor D has

 F_D(Phi_t(r xi))=F_D(r xi)

for every complex unit xi, BOTH fixed positive radii r1!=r2, and all t in
some nonempty open finite interval. Analytic dependence on t extends the
identity to t0. Its derivative at0 has two homogeneous parts:

 r^4 L_K F_D(xi)+g r^6 L_C F_D(xi)=0.

The two-radius2x2 determinant is nonzero; hence both Lie derivatives vanish
on the unit sphere, and by homogeneity everywhere. Arbitrary TWO fixed times
would not justify this step. We use the analytic experiment FAMILY only to
prove existence/generic rank of a finite actual design.

The pure onsite Kerr flow is z_j(t)=exp(-it|z_j|^2)z_j. Expand F_D as a
bihomogeneous polynomial in z,conjugate(z). Its terms group by charge
k=alpha-beta. The Kerr derivative multiplies each charge group by
-i k dot I, I_j=|z_j|^2. For k!=0 this is a nonzero polynomial; the polynomial
ring has no zero divisors. Thus invariance permits only charge0 monomials,
i.e. functions of the independent intensities I_j. But a fully symmetric
REAL tensor with any mixed multiset of indices has a nonzero-charge monomial
whose coefficient is a positive integer multiple of that SAME tensor entry.
No different multiset contributes that monomial. It follows that every mixed
entry is0 and

 F_D(z)=sum_j a_j I_j^2.                               (E4)

In particular ||z||^4 is NOT an extra null vector in this real Sym4 class:
a real isotropic tensor also contributes |z^Tz|^2 on complex arguments.

The linear K derivative of(E4) is, up to one common sign,
4 sum_(j<k) K_jk(a_j I_j-a_k I_k)Im(conjugate(z_j)z_k).
Activate only one edge's two coordinates, vary their intensities and relative
phase. Every nonzero K_jk forces a_j=a_k=0. Every vertex of a connected n>=2
network has an incident edge. Therefore D=0. An isolated vertex retains its
own |z_j|^4 invariant; n1 is an exception to ambient energy identification
(the physical unit coefficient can instead be known by normalization).

Consequently the family of(E3) rows spans ALL real Sym4. Some finite m rows
are independent. Pair every such setting with the other preparation radius;
there are at most m paired settings and2m records. A nonzero m-minor is an
analytic function of their complex unit directions and finite pulse times.
Drawing m paired settings from any smooth positive-density distributions on
the sphere and an open finite time interval gives full rank almost surely.
No quantitative lower singular value follows. The ACTUAL finite design
must be measured and conditioned; finite exact uniqueness is not uniformly
efficient noisy acquisition.

## 4. Finite-noise receiver

Use an orthonormal real Sym4 basis theta with feature b(x), so F=b(x) dot
theta, ||theta_true||=sqrt(n). For ||x||,||y||<=R,
||b(x)-b(y)||<=4R^3||x-y|| by four-factor telescoping and orthogonal projection.
If each reconstructed endpoint has error<=d, each energy-design row has
error<=8R^3 d. Suppose ||K0-Khat||<=dK, and a per-experiment energy identity
defect is <=dE. The right-side error is at most

 e_b=4dK R^2/|g|+8||Khat|| R d/|g|+2dE/|g|.            (E5)

For an ACTUAL estimated M-by-m design Ahat with certified sigma_min>=s>0,
an estimate thetahat and observed residual r=||Ahat thetahat-bhat|| satisfy

 ||thetahat-theta_true||
 <=[r+sqrt(M)e_b+sqrt(M)(8R^3d)sqrt(n)]/s.              (E6)

This uses Ahat directly and never absorbs an unknown error norm. Control-g
calibration error, endpoint switching error and residual g during linear
intervals must enter d/dE; they are not removed by the algebra. Standard
orthogonal-tensor contraction then recovers axes up to signed permutation:
A_w=T(.,.,w,w)=sum_j(q_j dot w)^2 q_j q_j^T. Its gap is chosen/tested
OFFLINE from the acquired tensor, so it is not the fixed beta=alpha K_j1^2
gap of s41. A tensor error epsilon_T gives contraction error<=epsilon_T||w||^2;
a qualified simple gap permits ordinary Davis--Kahan axis/K error bounds.
An internal axis's sign and label cannot be observed by these identical
onsite laws. The port axis is anchored by e0; an absolute hidden physical
labeling or sign convention is not silently recovered.

## 5. Finite actuator/readout and measurement cost boundary

The mathematical piecewise-constant g pulse is finite in amplitude/duration;
it is NOT an instantaneous pure-Kerr map. Finite rise/fall/off imperfections
are nonetheless additional controls. For norm<=R, real g preserves norm and
C(z)=|z|^2z has Lipschitz constant<=3R^2 and norm<=R^3. If g_actual differs
from the commanded waveform by L1 error deltaG, Duhamel/Gronwall gives

 endpoint error<=R^3 deltaG exp(3R^2 integral|g_actual|).

This pays finite edges and residual nonlinearity. R on the LINEAR steering
interval must be bounded from its actual drive, not only the science-pulse
norm. A safe unitary bound is R_start+sqrt(T) ||u||_L2. The common actuator
must actually meet the corresponding spatial/rate/off-state calibration;
none is measured in this packet. Ordinary optical outcoupling/readout also
has backaction/loss. The ideal coherent amplitude instrument here is a model
resource; a known linear readout loss may be calibrated, but unmodelled
loss during the nonlinear pulse invalidates the energy identity.

If one complex scalar record has independent sub-Gaussian quadrature scale
sigma0, obtaining simultaneous absolute precision eta for S records with
failure delta by repetition requires O(sigma0^2 eta^-2 log(S/delta)) repeats.
If repetition needs a new prepared trajectory, multiply ALL preparation,
pulse, readout and reset times, not just the final scalar observation count.
Adversarial calibration error is not averaged away. Source noise floors,
global actuator access and these repetitions are unacquired apparatus inputs.

The CPU experiment acquires a finite port model trace and actual140 finite
pulses, not H3 oracle values. Its numerical ODE integration is NOT validated;
small observed conservation defects are diagnostic. The finite-data algebra
can instead consume a warranted dE. Its linear-calibration error in the
reported fixture is checked against auditor-known truth, not established
from an unrestricted noisy trace. These qualifications prevent promoting
model reconstruction into an economical physical network instrument.
