# Completed scoped mathematical review of the reciprocal receiver continuation

28 October 2026. Source-exposed intake-owner reconstruction of all five supplied
notes and the final scientific report. This is a completed internal review of
exactly the mathematical scopes below, not a recovered archive review or a
second reviewer independent at the start. Those conditional scopes are accepted
internally verified. Hardware calibration, code replay, practical advantage and
historical priority remain separate. No scientific producer script was executed.

## A. Reciprocal collection and actual acquired information

For a fixed reciprocal passive source, a reciprocal launcher with forward U
and reverse transpose U^T returns u^T T_z u through its driven feed. Its target
residue is (t^T u)^2, whose magnitude equals matched-target power. The Schur
complement of the hidden load yields T_z=S0+z tt^T/(1-sz); |s|<=1 and |z|<1
make the denominator nonzero. A fixed reciprocal lossy front end can be reduced
to a passive reciprocal two-port for each configuration. This per-configuration
identity does not prove that arbitrary changing front ends share one fixed Gram.
Control needs an actual fixed calibrated linear command map and source.

Expanding half-combined powers gives I0-Ipi=2R Re h and
Ipi/2-I3pi/2=2R Im h. Four absolute errors bounded by eta give independent
quadrature bounds eta/R and hence field error sqrt(2)eta/R. Twelve powers
acquire the three fields. These are additional interference observations;
intensity-only square-root lower bounds retain their original scope. Reference
power, combiner loss, detector dynamic range and all calibration are charged.

## B. Uniform three-load recovery, including zero residue

Subtract the three fields to obtain c=a/(1-r^2 s^2) and d=rs c. Both are zero
when a=0; otherwise |d/c|<=r. For feasible pairs k=d/c,k'=d'/c', direct
expansion proves Delta Psi=(1+kk')Delta c-(k+k')Delta d, Psi=c-d^2/c.
Thus the residue map is Lipschitz on the physical set even at (0,0).

For noisy chat,dhat, radial clipping at fixed chat has displacement at most
ed+r ec, so |dc-d|<=2ed+r ec. The preceding feasible-pair identity gives
residue error <=(1+3r^2)ec+4r ed. With ec<=epsilon_h/r and
ed<=2epsilon_h/r, magnitude error is at most K_r epsilon_h,
K_r=1/r+3r+8. At r=1/2 this is 23/2; detector-only error is
23 eta/(sqrt(2)R). No separate accurate pole estimate or nonzero signal is
needed. The complex feasible set is nonconvex, so nearest projection cannot
be assumed nonexpansive. The explicit radial clip is the reviewed estimator.
An inward rational clip adds its certified error, and outward magnitude bounds
add theirs; no unacquired implementation is asserted here.

## C. Common calibration, relative bounds and actual load power

Expansion of fixed imperfect phasors gives alpha h+beta conjugate(h)+b.
Real contrast coefficients cancel common b, preserve alpha and give beta
conjugate(c),beta conjugate(d). Exact load subtraction is
h_zeta-h_z=a(zeta-z)/((1-s zeta)(1-sz)), bounded by p lambda,
lambda=d_z/(1-rmax)^2. It is proportional to p and contains no h0.

Compare noisy contrasts with (alpha c,alpha d). Apply B, bounding beta errors
by |beta|p/(1-r^2) and r|beta|p/(1-r^2). This gives the stated
|p_tilde-q|<=B+Theta q, q=|alpha|p, with
Theta=K_r lambda(1+bmax/gL)+(1+7r^2)bmax/((1-r^2)gL).
For gL>0,Theta<1 rearrangement and gL<=|alpha|<=gU prove
[max(0,p_tilde-B)/((1+Theta)gU),(p_tilde+B)/((1-Theta)gL)] intersect[0,1].
Do not cap q at one before inversion. If these qualifications fail, a sound
unresolved interval replaces a fabricated relative certificate. Common phase
is harmless; load-dependent phase is not common. The final-load factor follows
from (1-|z|^2)p/|1-sz|^2 and triangle bounds, giving factors
(1-d0)/(1+d0) and its reciprocal for |z_op|<=d0<1.
No actual gain,load interval or stability law has been acquired in hardware.

## D. Whole-Gram reconstruction and qualified scalar-to-matrix interface

For one fixed G=bb*,||G||<=1, the unit quadrature probes give Re G_jk and
minus Im G_jk with the signs in ALL_INPUT_GRAM. Each cross-component error is
at most 2delta; the pivot error is at most delta, so
||qhat-q||<=sqrt(8n-7)delta=e. Rank one gives qq*=dG and ||q||^2=d tau.
On D>4delta, d>=D-delta>0. Adding/subtracting qq*/D bounds the matrix error by
[2sqrt((D+delta)T_upper)e+e^2]/D+T_upper delta/D.
Because T_upper<=n(D+delta) and delta/D<1/4, this is bounded by
[(5/2)sqrt(n(8n-7))+(8n-7)/4+5n/4]delta<11n delta.
On D<=4delta, every true diagonal<=5delta, so the zero estimate has error
<=5n delta. Delta zero also works: only the zero source takes its zero branch.
The output is PSD rank at most one. There are 3n-2 scalar queries, costing
36n-24 raw powers, plus twelve for optional verification.

This is a documented scalar-to-Gram interface only when the same calibrated
linear map defines G throughout and each query has a simultaneous total error
bound. For shared-calibration intervals [Lj,Hj], their centers with common
radius delta=max_j(Hj-Lj)/2 supply that bound if every interval contains its
actual p. Acquisition may be adaptive, but the simultaneous promise must cover
the actual chosen queries. Uniform numerical constants need a uniform bound;
query-specific relative intervals alone do not silently supply a small delta.
Per-configuration reciprocal returns under arbitrary command-dependent
reflections are insufficient. Reconstruction and sequential-control schedules
are alternatives, not additive query costs. A top eigenvector of Ghat has
ideal regret<=2||Ghat-G||; finite command errors cost extra.

## E. Exact information failures and bounded-reference exponent

The two scalar passive matrices in NEW_LIMITS have equal returns 0 and1/32
at loads0,1/2 but target powers1/16 and1/25; their -1/2 returns differ.
Symmetric row-sum bounds certify contraction. Scaling t'=ct,s'=c^2s and
z'=z/c^2 preserves every complex return while p'=c^2p whenever passivity
survives. The explicit rational scale witness remains passive. Neither full
coherent access nor adaptive commands removes an unacquired load scale.

For A=1/10,k=1/5, A(1+ikz)/(1-ikz) equals a false target with residue2ikA
and pole ik. Its phase factors at+-1/2 are (99+-20i)/101. A load-dependent
reference rotation of a target-free constant A therefore produces all twelve
false-source powers exactly. Choose t with t^2=2ikA; |t|=1/5 and symmetric
row sums<=2/5 show the false two-port is passive. A fit cannot acquire reference
commonality. The separate load-dependent gain failure is not automatically
indistinguishable in all reference sums.

For bounded R<=Rmax and |z|<=rmax<1, a source with t=sqrt(epsilon)v and
S0=s=0 is passive, ||G||=epsilon, and |h|<=rmax epsilon. Every intensity differs
from its zero-source value by at most C epsilon,
C=Rmax rmax+rmax^2/2. For 0<delta<=C, take epsilon=delta/C. One common
transcript gives worst-case Gram error at least delta/(2C). For deterministic
control,n>=2, a unit v bilinearly orthogonal to the transcript's command gives
regret epsilon. This matches a linear bounded-error exponent at fixed bounded
reference, not optimal dimension constants or a photon lower bound. The
coherent note's looser rmax=1 constant is consistent with NEW_LIMITS.

## F. Conditional short-window energy and settling

If an independently certified complete-block error obeys integral_T |e|^2
<=T d_j^2, every contained window W has RMS error<=sqrt(T/W)d_j. A narrow
pulse shows why the complete-block RMS bound is not pointwise. Cauchy-Schwarz
then bounds averaged detector error by (1+R)d_window+d_window^2/2 when
stationary |h|<=1. This proves only the conversion from an acquired energy
bound. Stationary scattering data and quiet accessible power do not acquire
T or hidden decay; added receiver/load path delays belong in T. Photon,
actuation,reference,reset and settling costs remain explicit. Finite coordinate
quantization plus common attenuation is not falsely relabelled as one b-bit
product; denser masks can require O(n^2) channel writes.

## G. Actual acceptance and remaining evidence gaps

Accepted: the declared passive reciprocal residue; four-phase field acquisition;
uniform clipped three-load power bound; shared-calibration interval; all-input
rank-one Gram theorem; one-load,scale and phase counterexamples; bounded-reference
linear exponent; conditional window-energy conversion. This completed owner
review is sufficient at these mathematical scopes, with actual source hashes.
It does not accept arbitrary command-dependent cavities as a fixed Gram,
unrestricted reference drift as common calibration, or photon superiority.

The linked continuation ZIP displayed an explicit access denial. No permission,
account or access change,producer export request or bypass was performed. The
archive code,raw transcripts,numerical results and its completed scoped reviews
remain unacquired. Counts/tables in the provided notes/report are source-reported
offline emulations,not intake replay or laboratory operation. The older111-member
source archive is separately privately preserved; this review does not audit its
whole proof,copy its unlicensed third-party source data,or replace its original
square-root/eleven-reading theorem or407-versus539 scoped comparator.
Hardware calibration/stability,settling,model-fit uncertainty,complete-resource
advantage and historical priority remain open. Mission NOT_ACHIEVED.
