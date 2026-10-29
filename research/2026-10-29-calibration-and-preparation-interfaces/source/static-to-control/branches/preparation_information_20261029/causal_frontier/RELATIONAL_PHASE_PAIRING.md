# Relational phase information: one simultaneous pair can replace unpaired laws

29 October 2026. Root proposed the paired-quadrature mechanism; this note
independently verifies it, makes the errors and timing costs explicit, and
places it alongside the Gibbs mean route. No physical pair was acquired.

## 1. The exact native relation

In the free kinetic driver of NATIVE_REFERENCE_FRAME_IDENTIFIABILITY.md,
define the external-actuator-frame feature and the local force features by

    z(x)=(cos(nx),sin(nx))^T,
    h_phi(x)=(cos(nx+phi),sin(nx+phi))^T=R_phi z(x).         (1)

The local pair is an explicit measurement interface. It is not automatically
available from a single sine readout; its quadrature gains, relative phase
and simultaneity must be justified. Allow receiver forces alpha dot h_phi
with calibrated coefficients alpha. Translation x->x+phi/n removes phi
from h_phi and every such local force, while preserving the free driver,
uniform preparation and thermal noise. Thus the full joint h_phi,y,w path
laws under any prescribed alpha schedule are phi independent. The same
holds for causal alpha choices using only the declared local record.

The external z path law by itself is also phi independent: the free driver
does not depend on phi. Even perfect knowledge of BOTH separate full path
laws does not specify their JOINT coupling. This statement concerns unpaired
laws; synchronized records of the same realization are additional data.

For the free stationary driver, with

    C_n(t)=exp[-n^2 tau/gamma_d
                     (t-(1-exp(-gamma_d t))/gamma_d)],

the within-frame records are

    E[h_phi h_phi^T]=E[zz^T]=I/2,
    E[h_phi(t)h_phi(0)^T]=E[z(t)z(0)^T]=C_n(t) I/2.       (2)

These are direct angle averages and Gaussian-increment averages. Any
record constructed solely from the local h/receiver paths inherits the
translation ambiguity; this does not require asserting that every earlier
Astra object called G or H has the same definition as (2).

The genuinely paired static record is instead

    E[h_phi z^T]=R_phi/2.                                 (3)

It identifies the relative phase and therefore changes the available
information. Formula (3) is an ensemble relation, but estimation of its
mean is not necessary if an actual simultaneous vector pair is available.

## 2. One-pair exact and robust calibration

At ANY one physical configuration, with no distributional assumption,

    c_phi=h_1 z_1+h_2 z_2=cos(phi),
    s_phi=h_2 z_1-h_1 z_2=sin(phi).                        (4)

Hence one noiseless simultaneous pair determines phi modulo 2pi. Equivalently
arg[(h_1+i h_2)(z_1-i z_2)]=phi. It requires no mixing time, independent
restart, or full hidden-state observation. One instantaneous outer product
h z^T is rank one and is NOT itself R_phi/2; it is (4), together with the
known SO(2) rotation structure, that makes one pair sufficient.

Suppose the actual reported vectors obey warranted simultaneous bounds

    ||hhat-h||_2<=epsilon_h<1,
    ||zhat-z||_2<=epsilon_z<1.                            (5)

Normalize the reports or simply take the argument of their complex product.
The Euclidean epsilon-ball around a unit vector subtends angle at most
arcsin(epsilon). Consequently the circular phase error satisfies

    d_circle(phihat,phi)
       <=arcsin(epsilon_h)+arcsin(epsilon_z).              (6)

This is deterministic. It needs no independence of errors or random state
sampling. The associated rotation error is
||R_phihat-R_phi||_op=2 sin(d_circle(phihat,phi)/2).

For additive isotropic two-dimensional Gaussian sensor noise of known
standard deviations eta_h,eta_z per coordinate, choose
epsilon_h=eta_h sqrt(2log(2/alpha)) and
epsilon_z=eta_z sqrt(2log(2/alpha)). The Rayleigh norm tail and a union bound
give (5)--(6) with failure probability at most alpha, provided both epsilons
are below one. Cross-channel independence is not needed for that union
bound; the actual marginal noise laws and calibration still must be valid.

The SO(2) feature structure is essential. A single paired vector does not
identify an arbitrary rotation in higher dimensions: its stabilizer remains.
For a general group action, enough paired configurations must be acquired
to reduce the common stabilizer to the subgroup irrelevant to the intended
consequence. Removing a symmetry obstruction does not automatically remove
unrelated hidden-model ambiguities.

## 3. Scalar local readout alternative

If only f=sin(nx+phi) is actually observed, then

    f=(sin phi,cos phi) dot z.

One f,z pair generically leaves a reflection ambiguity; the exact tangent
case f=+1 or -1 is an exception. Two simultaneous pairs whose
reference vectors are LINEARLY INDEPENDENT determine the coefficient vector.
Let Z have the two reference vectors as rows. An error guarantee must include
the actual inverse conditioning ||Z^-1|| and the errors of both Z and f.
Independence here is geometric noncollinearity, not an iid claim. Two nearly
parallel configurations are not an adequate acquisition certificate.

The stronger quadrature-pair interface in (1) avoids this configuration
conditioning obligation, but its extra physical feature readout is charged.

## 4. Spatial and temporal calibration are actual resources

If z is computed from a lab-frame position with error delta_x, then

    ||z(x+delta_x)-z(x)||_2
       =2|sin(n delta_x/2)| <=n|delta_x|.                 (7)

Fixed phase accuracy therefore requires spatial accuracy of order 1/n.
A direct calibrated feature meter may supply z without a position estimate,
but its field bandwidth, gain, error and reference phase must then be
supplied at the feature interface. A single scalar query does not buy (7).

If z is inferred by measuring the reference potential energy -u cos(nx)
and its quadrature, absolute energy-readout error eta_U becomes normalized
feature error eta_U/u. Under n u<=A this requires eta_U=O(1/n) for fixed
normalized accuracy. A bounded force ceiling alone supplies neither that
energy precision nor the spatial bandwidth.

Simultaneity matters. If the local and external features are acquired at
times separated by Delta, their phase relation includes n(x_(t+Delta)-x_t).
An actually warranted velocity bound V over that interval gives the
deterministic additional phase error n V|Delta|. Without such a bound, it
cannot be deleted.

For the stationary FREE OU driver at fixed times (or times and lag chosen
independently of the driver/record), the
integrated velocity increment is exactly centered Gaussian of variance

    V_x(Delta)=2tau/gamma_d
        [|Delta|-(1-exp(-gamma_d|Delta|))/gamma_d].         (8)

Hence with probability at least 1-beta, the extra phase mismatch is at most

    n sqrt[2 V_x(Delta) log(2/beta)].                     (9)

At small Delta this is approximately
n|Delta| sqrt[2tau log(2/beta)]. Thus fixed-confidence phase calibration
requires timing precision of order 1/n unless the channels are truly
simultaneous or the actual motion is otherwise resolved. Formula (8) is
specific to the free stationary driver; it must not be transferred to a
different controlled preparation without a valid increment law/bound.
Nor may it be transferred to a record-selected stopping time merely from
stationarity: selecting a large-velocity time changes the conditional
increment law, including its mean. Adaptive timing needs the deterministic motion bound
above or a separately warranted conditional increment certificate.

## 5. Consequences and matched alternatives

Within the supplied sinusoidal native model, the relative phase then predicts
the receiver mean under every calibrated potential setting psi and amplitude u:

    E w(h)=(a/gamma)(1-exp(-gamma h))
                    [I1(u/tau)/I0(u/tau)] sin(phi+psi).

A phase error epsilon gives a mean-prediction error at most R_h epsilon,
before adding the bath, amplitude, timing and preparation uncertainties.
More generally any already proved controlled consequence that is Lipschitz
in the relative rotation inherits its appropriate parameter sensitivity;
no unproved full-law robustness is assumed from this mean formula.

The matched conventional route is ordinary phase-reference alignment or
paired-feature regression. It uses exactly the same joint record and can
perform the same one-pair reconstruction. The addition is not a faster
trigonometric calculation. It is the native separation between complete
unpaired predictive records and the physical relational information required
to attach those records to an external actuator.

Two controlled Gibbs mean probes are another legal route when driver Gibbs
preparation and repeated independent trials are actually available. Their
signal shrinks as O(1/n) at bounded force n u<=A. The joint-pair route can
avoid a mixing/reset acquisition for phase alignment, while retaining its
explicit simultaneous-feature precision and bandwidth costs. Neither route
is declared universally cheaper without the actual sensor/preparation model.

The general importance of reference frames and relational rather than
absolute coordinates is established in Bartlett--Rudolph--Spekkens (2007)
and Marvian--Spekkens (2014), cited in the companion source receipt. No
historical priority is claimed for that principle or phase calibration.
