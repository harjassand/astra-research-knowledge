# Continual-noise lifetime for a time-independent 4D sweep Lindbladian

Status: mathematical proof complete under the exact model and named standard
imports after principal-investigator reconstruction and a fresh adversarial
internal audit. See cold_audit/COLD_PROOF_AUDIT.md. Historical originality,
external correctness and formal certification are not established. This is an
ideal-model theorem, not a physical demonstration.

## Exact statement

There exist constants b in N and epsilon,A,c>0, independent of system size
and storage time, with the following property. For sufficiently large M and
L=bM, place a qubit on each plaquette of the periodic four-dimensional cubic
lattice. There are 6L^4 qubits, grouped into cells of dimension 64. Start in
ANY state in the 4D toric code space, including entanglement with a reference.

Use independent rate-kappa Poisson attempts at every primal and dual vertex.
At a vertex with no incoming syndrome edges and a nonempty even set O of
outgoing edges, sort O and pair consecutive directions. Flip the one or two
positively based faces of these pairs. Otherwise do nothing. The pairing is
fixed in advance. This is the known sweep operation; it is not invented here.

The quantum generator is time independent:

    L_total = sum_(v,O,sector) D[J_(v,O,sector)]
              + sum_(face f,P in {X,Y,Z}) lambda_P D[P_f],

    J_(v,O,Z) = sqrt(kappa) Z_(paired faces) Pi_(v,O),

with dual X jumps. Pi checks the eight incident commuting edge stabilizers,
requiring no incoming defect and the specified outgoing pattern. There are
seven active patterns per vertex per sector, at most 24 qubits per jump
support, and bounded range/rates independent of L. D[J](rho)=J rho J^dagger
-{J^dagger J,rho}/2. There is no schedule or auxiliary classical memory.

Assume independent constant-rate single-qubit Pauli noise with

    max(lambda_X+lambda_Y,lambda_Z+lambda_Y) <= epsilon kappa.

There is a fixed perfect final syndrome-recovery decoder Dec_L such that,
for all T>=0, the decoded logical channel obeys the unhalved diamond bound

    || Dec_L exp(T L_total) Enc_L - id_logical ||_diamond
       <= min(2, A L^4 (1+kappa T) exp(-c L)).             (T)

The same argument bounds the probability of any change of decoded logical
homology before T. All six encoded logical qubits are covered. In particular,
times kappa^(-1) exp(a L), a<c, have vanishing error as L increases.

This statement uses exact engineered syndrome-conditioned Pauli jumps,
perfect code-space initialization and ideal readout. It does not establish
robustness to arbitrary coherent/generator perturbations, or a noisy-readout
threshold. L=bM specifies a family of sizes, not every positive integer L.

## 1. Exact support envelope

For one CSS sector let eta_x mark possible syndrome vertices. Start eta=0.
Every physical face fault sets its four corners to 1. At a common vertex
clock v update simultaneously using the OLD state:

    eta'_v = eta_v AND OR_i eta_(v-e_i),
    eta'_(v+e_i+e_j) = eta_(v+e_i+e_j)
                       OR (eta_v eta_(v+e_i) eta_(v+e_j)), i<j.

All other entries remain unchanged. This map is monotone. An incoming
syndrome edge supplies an occupied predecessor and prevents erroneous
erasure at v. A legal trailing correction removes its syndrome at v; its
only possibly new vertices are the paired opposite corners, whose three
source vertices were occupied. Thus actual syndrome support is contained
in eta for every common event sequence, including continual faults.

Healthy coordinate halfspaces x_i>=0 are invariant without faults. From a
healthy halfspace h(x)<=-sb, h=sum x_i, a site clears permanently after its
four predecessors clear and its next own clock rings. Directed last-passage
certificates of depth H have tail at most 2*8^H exp(-kappa t/2). The argument
uses fresh independent exponential residuals on predecessor-directed clocks.

## 2. Uniform block forcing with literal local primitive flags

Partition into cells C_z=bz+{0,...,b-1}^4 and set zeta_z(n)=1 if C_z is entirely
eta-free at n Delta. Fix s=1, C>10 log(8), and
R>=max(6,ceil(280 e C)+10); let Delta=Cb/kappa. Define

    A_i={w:||w||_infinity<=R,w_i>=0}, i=1,...,4,
    A_5={w:||w||_infinity<=R,sum_i w_i<=-s},
    phi(zeta)=OR_(j=1..5) AND_(w in A_j) zeta_w.

Phi is an attractive eroder. For a finite zero island its four coordinate
maxima never increase, while its minimum height rises at least s per round;
these two properties force extinction in finite linear-diameter time.

Define B_(z,n) solely from fresh primitive increments in slab n and a fixed
guard of coarse radius R+3. It is the union of: a physical birth meeting the
radius-(R+2) guard; failure of the lower-halfspace clearance certificates for
the b^4 target vertices; and existence of ANY m-event ordered backward clock
dependency chain ending at a target during the entire slab, m=floor(Rb/2).
There are at most 35 clock/input choices per causal step. A mark cannot be
reused in a zero-time cascade because all outputs read the old state.

Its marginal is bounded by

    delta <= 2b^4 exp(((s+4)log(8)-C/2)b)
             + b^4 (35 kappa Delta)^m/m!
             + 6 sigma ((2R+5)b+3)^4 Delta,              (B)

where sigma is the sector's face-fault rate. All dependencies are contained
in the fixed guard. Absence of the m-chain excludes arbitrary exterior input
and exterior births. Halfspace invariance/clearance and monotonicity therefore
give zeta_(z,n+1)>=phi(zeta_n shifted z) whenever B_(z,n)=0, uniformly over
ALL inputs, without an actual synchronous microscopic round.

The dependence radius of B in coarse coordinates is fixed independently of
b. Choose the target small delta first, then a fixed b making the first two
terms small, and finally a strictly positive sigma/kappa making the last term
small. This order is noncircular. No useful numerical threshold is obtained.

## 3. Published infinite-volume cluster control

Let theta_0=1 and theta_(z,n+1)=(1-B_(z,n))phi(theta_n shifted z). Then
zeta_n>=theta_n. On infinite Z^4, fixed guards give finite spatial dependence
and independent time slabs. The Liggett--Schonmann--Stacey product-domination
theorem couples B below iid deaths of parameter p(delta) tending to zero.
Choose these couplings independently in the slabs.

Hartarsky--Toninelli, arXiv:2212.08437v2, Corollary 9.5, gives exponential
diameter tails for every fixed-k connected SPACETIME zero component of an
attractive eroder with sufficiently small iid death. Its upper-invariant
healthy trajectory is below the cold all-one trajectory by pathwise
attractiveness, so the same upper bound applies to cold finite histories.
These are imported theorems, not new campaign discoveries. The original LSS
publisher PDF was access-blocked in this session; HT's explicit application
to fixed-range fresh blocks was read, and the standard LSS statement is named.

## 4. New finite-torus adapter and the whole-slab cover

Use native B-driven theta on the torus; do not assert torus product domination
or an all-time stationary tail. Set k=4R+4, ell=M/128 and take M sufficiently
large compared with these fixed radii. Reveal each layer's zero outputs in a
fixed order and stop at the first insertion creating a k-connected spacetime
component of diameter at least ell. Every prior component was smaller, hence
the entire new component lies within ell+k of the inserted anchor.

For a nonfault zero the DNF requires a zero parent in EVERY forcing set.
These parents are in older already revealed layers and are k-near, hence
belong to that same component. Its necessary zero ancestry is closed and
local. Copy primitive increments in a FIXED anchor patch enlarged by R+3,
lift injectively to Z^4, and extend independently outside. Induction replays
the zero witness in infinite theta; extra outside zeros only help. Apply
the infinite cluster tail and union over at most N M^4 insertion anchors:

    P(first macroscopic coarse zero component by layer N)
       <= C_1 N M^4 exp(-c_1 M).                         (F)

See lead/STOPPED_TORUS_REPLAY.md for the fixed local-witness event that avoids
conditioning an adaptive patch or copying a wrapped light cone.

Throughout slab n, every infected fine cell either has an initial infected
ancestor within coarse radius R, or has B_(z,n)=1. Thus slab-occupied cells
are contained in N_R({theta_n=0}) union {theta_(n+1)=0}. Adjacent occupied
fine vertices map to k-near coarse spacetime zeros. A fine syndrome component
of ambient torus infinity-diameter L/32 maps to coarse diameter at least
M/32-2R-1>ell. This covers ALL times in a slab, including transient defects.

## 5. Accumulated homology and the quantum channel

Fix a decoder filling each syndrome component of diameter below rho=L/8
inside its uniquely lifted coordinate box; otherwise use a fixed global
filling. Identical unaffected components have identical fillings. For one
local noise/correction 2-chain F, if all precomponents have diameter below
r=L/32, all changed components, their old/new fillings and F lie in a common
embedded box of side at most 2r+1<rho. Therefore the closed chain

    F+D(s)+D(s+boundary(F))

is a stabilizer boundary. The decoded homology of the ENTIRE accumulated
error chain cannot change at any such event. No ancestry is discarded merely
because its syndrome vanishes. Before coarse first escape, the whole-slab
cover keeps every physical component small, so logical homology remains zero.

Take N=ceil(T/Delta)+1 in (F) and union the primal/dual sector bounds. Y faults
correlate the sectors but do not affect this union bound. On each Pauli-error
trajectory every syndrome projector is 0 or 1, and jump/no-jump rates depend
only on syndrome, independently of the logical/reference input. This direct
trajectory argument covers the two-face jumps; no single-bit-only reduction
theorem is silently extended. A homologically trivial residual is a stabilizer
on every encoded state. Twice the bad-trajectory probability bounds the
unhalved diamond distance, proving (T) after absorbing fixed b,C into A,c.

## Resources, predecessor and frontier

Physical resources in the ideal model are 6L^4 data qubits, 14L^4 correction
jump terms, bounded support and fixed rates. The proof's b,Delta,eta,theta
are not implemented registers or a global physical clock. A deterministic
small-component filling is obtainable by axial prism contraction inside its
box in O(L^5) elementary binary toggles; a polynomial binary-linear-algebra
fallback defines recovery everywhere. See lead/READOUT_CONSTRUCTION.md.
Readout and initial encoding are idealized, separately charged operations.

The sweep/causal geometry predecessor is Kubica--Preskill, 1809.10145. The
closest reviewed static 4D engineered-dissipation memory is Pastawski et al.,
1010.2901, whose local 4D result is numerical. The rigorous 2610.05589v1
competitor supplies synchronous/Floquet memory. Thermal results use Gibbs
syndrome initialization; 2507.10976v1 states the ordinary cold-Glauber problem
is open. None of these comparisons certifies exhaustive historical novelty.

Unacquired: constant-range realization of a 4D interaction graph in physical
3D, fabricated conditioned dissipators, preparation/calibration fidelity,
reservoir/reset/energy costs, noisy readout, robustness to imperfect correction
terms, and a useful threshold. These remain research obligations. No energy,
manufacturing or Kardashev capability is demonstrated by this theorem.

Primary sources: https://arxiv.org/abs/1809.10145 ;
https://arxiv.org/abs/1010.2901 ; https://arxiv.org/abs/2610.05589v1 ;
https://arxiv.org/html/2212.08437v2 ; https://doi.org/10.1214/aop/1024404279 ;
https://arxiv.org/html/2507.10976v1 .
