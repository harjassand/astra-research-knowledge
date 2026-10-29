# Independent reconstruction and the calibration-to-science repair

Reviewer B, 2026-10-30. Producer inputs are read-only. This note records the
mathematical reconstruction while the producer finishes its separate
`calibration_bridge/` extension. No source experiment or nonlinear trajectory
has been rerun. A final review will bind the completed snapshot separately.

## 1. The exact finite-pulse operation

The model is a **classical complex-amplitude** equation with a real symmetric
linear Hamiltonian, a known globally switchable common onsite Kerr coefficient,
and one calibrated complex drive/readout port. Known dimension, cyclicity,
phase, Euclidean amplitude metric, absence or calibrated treatment of loss,
and the common actuator are actual premises. They are not inferred merely
from a small finite ringdown residual.

In warranted linear reference coordinates, the real orthogonal realization
has quartic tensor

`T_abcd = sum_j Q_ja Q_jb Q_jc Q_jd`.

The energy identity between the ACTUAL endpoints of a fixed finite unforced
pulse is exactly

`F_T(y)-F_T(x) = 2(x* K0 x-y* K0 y)/g`.

This is a finite linear inverse in real `Sym^4`, of dimension
`m=binomial(n+3,4)`. It uses neither a supplied cubic Volterra kernel nor a
pure Kerr kick with the linear Hamiltonian turned off.

Here is an independent reconstruction of the all-size injectivity argument.
For a putative real `Sym^4` null tensor, analytic dependence of the bounded
norm-preserving Kerr flow on real time extends an identity on any open
finite time interval to time zero. At two distinct positive radii the
derivative equations have respective homogeneous factors `r^4` and `r^6`;
the two-by-two system gives separate invariance under the linear and onsite
Kerr generators. **Two prescribed finite times would not give this claim.**

For the pure Kerr generator, work in the polynomial ring with independent
formal `z_j,bar(z_j)` and grade monomials by charge `alpha-beta`. In each
nonzero charge space the derivative is multiplication by the nonzero
polynomial `-i sum_j (alpha_j-beta_j) z_j bar(z_j)`. No zero divisors implies
that the entire coefficient polynomial in that charge space vanishes. Any
mixed multiset of four tensor indices admits a division into two unbarred
and two barred indices with nonzero charge. The coefficient of that
monomial is a positive integer times that SAME real symmetric tensor entry;
no other index multiset contributes it. The types `aaab`, `aabb`, `aabc`,
and `abcd` are all covered. Thus only `sum_j a_j |z_j|^4` remains.

The linear generator applied to this remainder contains, for each edge,
`K_jk (a_j I_j-a_k I_k) Im(bar(z_j)z_k)`, up to a common nonzero factor/sign.
Turn on only the two coordinates of one edge and vary both positive
intensities and their phase. Both `a_j` and `a_k` vanish. Every vertex of a
connected graph with `n>=2` is incident to an edge, so the tensor is zero.
An isolated vertex and `n=1` are correctly excluded. The apparently tempting
null vector `||z||^4` is not in this real-symmetric-tensor image by itself:
the real isotropic tensor also produces `|z^T z|^2` on complex arguments.

Finite-dimensional span then gives at most `m` paired direction/time
settings, hence `2m` records. A nonzero selected minor is a real-analytic
function on the product of complex spheres and open time intervals. Full
rank follows almost surely for a JOINT absolutely continuous full-density
draw (in particular independent full-density draws). It gives no uniform
singular-value floor, conditioning, sample complexity, or constructive
well-conditioned design. The actual finite matrix needs its own qualifier.

## 2. Finite error and execution boundaries

The four-factor telescoping inequality gives a feature error at most
`4 R^3 d`, and a row error at most `8 R^3 d`, provided `R` bounds BOTH the
true and reconstructed endpoints. The known physical tensor has Frobenius
norm `sqrt(n)`, so the displayed finite receiver need not absorb an unknown
parameter norm. Its right-side error and left-inverse argument are sound
with separately warranted endpoint, linear-model, and energy-defect inputs.
Ordinary contraction and a tested contraction eigenvalue gap recover axes
only up to the admitted signed permutation; port calibration anchors its
one visible direction.

The directed-Arb producer consumer proves statements about the exact stored
dyadic design/data, using an auditor-known exact source tensor. This is
legitimate finite-data/source-qualified arithmetic. It is not an unknown
physical-source error warrant and it does not validate the numerical flow.
In particular, a tiny energy defect bounds the energy identity residual,
not the trajectory error of an adaptive DOP853 call.

The matched ordinary orthogonal-manifold Gauss--Newton method is a serious
comparator. It uses the same acquired linear reference and the first 12
endpoint experiments, with analytic sensitivities and both declared starts
retained. Its all-140 forecasts condition on the measured initial endpoint
of each experiment. Its observed advantage in this retained model remains:
fewer training experiments and a substantially smaller physical-matrix
error. Neither two converged starts nor this one source proves global
convergence. The energy theorem remains differentiated in its all-size
ambient injectivity and linear finite-endpoint receiver; no practical
advantage follows from that difference.

## 3. A real missing reset in the original execution

`energy_experiment.py` executes the calibration pulse and ringdown from
zero. It subsequently assigns the science residual to zero instead of
carrying the remaining calibration field or canceling it. Unitary ringdown
does not remove that field. The in-science resets correctly carry their
own residuals, but they cannot pay this earlier boundary retrospectively.
The original execution therefore consists of TWO separately zero-initialized
segments. This observation does not refute the energy identity/injectivity
theorem, the finite-data matrix certificate, or the numerical within-science
comparison. It rules out presenting that saved run as an executed single
calibration-to-science protocol from only its stated first zero field.

Root and producer have acknowledged this issue. The producer is preserving
the original execution and constructing a separate mathematical bridge,
without new trajectories. The bridge must be distinguished from an executed
reset and from any new observation/rank claim.

## 4. Independent finite bootstrap reset budget

The following supplies a paid repair under the SAME warranted common
Euclidean linear-model error premise. Let true `||e||=1`,
`||K-Khat||<=dK`, and `||e-ehat||<=de`. During calibration, drive by one for
`p=1/5`, then wait `W=32`. Let `xcalhat` be the state predicted from that
known drive history in the estimated linear system. Duhamel gives

`||xcal-xcalhat|| <= p de+(p W+p^2/2) dK
                     = de/5+(321/50)dK`.

No further measurement is required to construct this particular estimate.
For a reset of length `P=16` with `L=32` bins of width `h=1/2`, form the
estimated finite control matrix `Bhat`. Each column perturbation is at most
`h(de+P dK)`, and hence

`||B-Bhat|| <= sqrt(L) h(de+P dK) =: dB`.

Compute any finite command `v` and certify its finite arithmetic residual

`eta_cmd = ||exp(-i Khat P) xcalhat+Bhat v||`.

The actual residual after this command obeys

`||r0|| <= de/5+(321/50)dK + P dK ||xcalhat||
           +dB||v||+eta_cmd`.

Since `||xcalhat||<=p(1+de)`, an exact pseudoinverse command satisfies
`||v||<=p(1+de)/s_p` if `sigma_min(Bhat)>=s_p>0`. A finite rounded command
can instead be consumed directly through its actual norm and `eta_cmd`.
The extra operation costs 16 normalized time units, integrated squared-input
proxy `h||v||^2`, and peak at most `||v||`; these quantities are not joules
or an acquired hardware specification. With the old source-qualified
calibration errors and an actual certified finite frame, it is inexpensive
in the model. It does not remove the externally warranted calibration gate.

The remaining science composition can use its actual closed-loop reset
gain, instead of an exponential in all 140 pulse times. Let `P_C` and
`P_B` be the implemented finite read and control inverses, and `R=15.5`.
For equal additive record words the residual response through one cycle is
controlled by

`Areset=U_true(P+R)-B_true P_B U_hat(P+R) P_C C_true`.

Factoring its difference from zero using `B_true P_B-I`,
`P_C C_true-I`, and `U_true-U_hat` pays this gain from the same model/frame
qualifiers. The nonlinear part costs at most
`exp(3 |g| Rball^2 tau_max)` between two EXACT Kerr flows. If their record
noise words differ, add the separately bounded affine input term; it cannot
be discarded by asserting equal distributions.

Crucially this comparison does NOT turn old unvalidated ODE endpoints into
exact-flow endpoints. Any numerical transfer from the old stored design to
a newly composed exact protocol needs a separately warranted old trajectory
error, in addition to this reset budget. That warrant is currently UNKNOWN.
The mathematical reset and composition theorem can still be accepted without
claiming the proper-protocol rank or its data were executed/certified.

## 5. Prior boundary actually checked

The pinned N596/N597 packets and full governing s41/h16 reports were read
selectively, preserving their distinct first-order and damped-second-order
models, direct-coupling/gap assumptions, exact-kernel versus physical
acquisition distinction, and unresolved oscillator robustness disagreement.
They already expose hidden axes by cubic response contractions. Nothing in
this review reopens those accepted or reported results or promotes their
disputed robust scope.

The primary [Usevich--Dreesen--Ishteva paper, Section 2.3 and Section 3]
(https://arxiv.org/html/2109.09584v1) was read at its actual FIR/polynomial
parallel Wiener--Hammerstein and estimated-Volterra-kernel interface. It is
a strong tensor/branch-identification antecedent, not a direct finite-pulse
Kerr network theorem. [Schoukens et al.]
(https://arxiv.org/html/1708.06543v1) already use input-output data, several
excitation levels, branch decomposition, and final joint nonlinear least
squares. [Wu--Qin--Xiu, Section 2.2]
(https://arxiv.org/html/1905.10396v2) explicitly begin with state/derivative
pairs, or approximate derivatives from state trajectories. Conservation-based
Hamiltonian fitting and strong nonlinear fitting are established operations.
These inspected sources do not by themselves furnish the exact two-radius
real-`Sym^4` proof above. This bounded primary screen is not a historical
priority clearance or exhaustive literature search.
