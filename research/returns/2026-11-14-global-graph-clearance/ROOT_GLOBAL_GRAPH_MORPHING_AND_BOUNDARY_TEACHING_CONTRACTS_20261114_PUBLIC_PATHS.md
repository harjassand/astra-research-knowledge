GLOBAL GEOMETRIC PATHS, POSITIVE CURRENT FIELDS AND PHYSICAL RESPONSE COORDINATES
14 November 2026 Brisbane. ROOT-owned conditional derivations.

These are constructions within declared models, using classical geometric,
network and contraction arguments. No novelty, manufactured material, installed
measurement accuracy, component lifetime or useful-system advantage is claimed.
No producer code or unavailable dossier is used. The two owned scripts and JSON
files named below contain introduced finite diagnostics, not physical services.

1. A positive global formation path for graph-shaped sheets

The earlier actual primary van Rees--Vouga--Mahadevan2017,
https://pmc.ncbi.nlm.nih.gov/articles/PMC5676909/ , DOI10.1073/pnas.1709025114,
main through191 including Eqs3--5/Theorem1 and its displayed proof, supplies the
algebraic bilayer metric inverse. Its thin Kirchhoff--Love/StVenant--Kirchhoff,
independently orthotropic equal-thickness layers and sufficiently-small-thickness
conditions remain. Later examples, SI, sources and code were not read here.
The inverse is credited prior construction, not an invention of this note.

Here is a restricted positive answer to the separate global-intersection issue.
Let Omega be a convex subset of R2, f:C2(Omega)->R, and ||Hess f||op<=M throughout
Omega. Put y_t(x)=(x,t f(x)), 0<=t<=1, with upward unit normal n_t. Thicken it by
F_t(x,z)=y_t(x)+z n_t(x), |z|<=a. If a M<1, F_t is injective for EVERY t and all
normal fibers remain separated. More precisely, for x!=x' and any z,z' in that
interval,
  |F_t(x,z)-F_t(x',z')| >= (1-a t M)|x-x'|.

Proof. Taylor's bound along the segment in the convex domain gives, for
D=y_t(x)-y_t(x'),
  |n_t(x).D| <= (t M/2)|x-x'|^2,
and the same bound at x'. With W=F_t(x,z)-F_t(x',z'),
  D.W >= |D|^2-a t M|x-x'|^2 >= (1-a t M)|D|^2.
Cauchy--Schwarz and |D|>=|x-x'| prove the inequality. If x=x', equality of the
offset points forces z=z'. Principal curvatures have magnitude<=t M, so the
same condition also excludes local normal-chart singularity. Convexity of the
parameter domain, a global Hessian bound and this graph representation are
essential to this proof. It does not cover a folded helicoid or arbitrary topology.

The graph path has forms
  a_t=I+t^2 grad f (grad f)^T,
  b_t=t Hess f /sqrt(1+t^2|grad f|^2).
Using the credited inverse with thickness parameter h gives layer metrics
  a_t+(2h/3)b_t and a_t-(2h/3)b_t.
Both have minimum Euclidean eigenvalue at least 1-(2h/3)t M. Taking total
thickness h=2a in the owned geometric example satisfies BOTH positivity and
global separation with a large explicit margin. The conclusion is a supplied
collision-free geometric path and required metric fields, not physical tracking
of that path. Actual layer-field writing, finite-thickness model error, fixtures,
load, dynamic stability, energy, renewal and metrology remain separate operations.

INTRODUCED f=.004 cos(kx)cos(ky)m on a .05m square, k=pi/.05m, has
  ||grad f||<=.2513274, M=.004 k^2=15.791367/m.
The Hessian eigenvalues are -.004 k^2 cos(k(x+y)) and
-.004 k^2 cos(k(x-y)), which establishes that bound without a grid argument.
With h=.0002m, a=.0001m, global fiber separation factor>=.9984208633 and layer
metric eigenvalue>=.9978944844. The owned script evaluates five homotopy values,
81 midsurface locations and three offsets/location. Its sampled minimum final
separation factor .9984682071 and metric eigenvalues .9978944844--1.0631654682
are floating diagnostics of this declared example. The proof applies to all
t and points. Six local metric components per location, 486 per sampled step,
are required field values, not installed actuators or a common-stimulus writer.

Artifact: ROOT_GRAPH_SURFACE_MORPHING_WITH_GLOBAL_CLEARANCE_20261114.py and JSON.

2. An exact positive-current dual in a restricted cyclic grid

Let there be m rows and L horizontal edges/row, nodes at columns0..L. Every
horizontal resistance r_i,k lies in [rmin,rmax]. At EVERY column, including
the boundary, connect adjacent rows by the SAME conductance g>0. All row ends
are accessible ports; interior nodes are inaccessible. This fixed transverse
structure is an indispensable restriction, not a theorem for arbitrary varying
rungs, arbitrary networks or the producer's unavailable dossier.

Inject current I into the left end of row s and extract I at its right end.
Every other boundary port has zero external current. Let J_k be the vector of
left-to-right horizontal currents in column segment k, and introduce the boundary
vectors J_0=J_(L+1)=I e_s. With R_k=diag(r_i,k) and the row-path Laplacian H,
KCL and the voltage drop across segment k give the exact dual equations
  -D^2 J_k+g H R_k J_k=0,  k=1..L,
where D^2 J_k=J_(k-1)-2J_k+J_(k+1).

The block matrix A has diagonal blocks 2I+g H R_k and off-diagonal blocks -I.
It has nonpositive off-diagonals, column sums zero internally and positive
column sums at the end segments. The connected row/column structure makes it
irreducible. Apply the elementary minimum principle to A^T: at a negative
minimum a row with nonnegative sum cannot produce a positive right side; equality
propagates to a boundary row with strictly positive sum and gives a contradiction.
Thus (A^T)^-1>=0, hence A^-1>=0. Consequently EVERY J_i,k>=0. Summing the dual
equations over rows gives -D^2 sum_i J_i,k=0 with value I at both ends, so
  sum_i J_i,k=I for all k.

Put S_k=I-J_s,k>=0. Since neighboring horizontal currents are nonnegative,
  -D^2 S_k=(g H R_k J_k)_s <=g deg(s) rmax I.
The discrete parabola P_k=k(L+1-k)/2 solves -D^2P=1 with zero boundary values.
The scalar maximum principle gives
  0<=S_k<=g deg(s) rmax I P_k.
Therefore, with epsilon=g degmax rmax (L+1)^2/8,
  J_s,k>=(1-epsilon)I,
  sum_(i!=s) J_i,k<=epsilon I.
The bounds hold throughout arbitrary resistance changes that remain inside the
declared box. They do not require uniform initial rows or microscopic tomography.

A physical all-state memory law would still have to establish writing for
selected current >=Iwrite and nondisturbance for the complete exposure history
at <=Isafe. A feasible static current window requires
  Iwrite/(1-epsilon)<=I<=Isafe/epsilon.
No relay, memristor, safe cumulative exposure, transient, leakage, tolerance,
thermal, retention or finite-pulse bound is supplied by this inequality.

3. A globally conditioned functional inverse after row-uniform writing

NOW restrict actual states to r_i,k=r_i, a different, smaller domain. For unit
current injection into row s let F_s(r) be its measured boundary energy. The
classical envelope identity gives
  partial F_s/partial r_i=sum_k J_i,k;s^2.
Thus each diagonal derivative is >=L(1-epsilon)^2; each off-diagonal row sum is
<=L epsilon^2; every full row sum is <=L. Along a segment between r and r', choose
a coordinate of maximum parameter difference and apply these inequalities:
  L(1-2epsilon)||r-r'||inf <= ||F(r)-F(r')||inf <=L||r-r'||inf.
For epsilon<1/2 this is a global useful inverse bound independent of m,L after
normalizing F by L. There is no exponentially weak coordinate in THIS domain.

The explicit map
  T(r)=clip_box[r-(F(r)-Ftarget)/L]
is a contraction with factor<=2epsilon, since each row of I-DF/L has absolute
sum <=1-(1-epsilon)^2+epsilon^2=2epsilon. It fixes the target and converges
globally. If combined target/measurement error in F is <=eta L each iteration,
the resulting parameter-error floor is bounded by eta/(1-2epsilon), subject to
the actual row-uniform domain and measurement model. Model acquisition, probes,
read time, source range and evaluation are paid; exact F is not a sensor.

If ALL actual edge resistances lie within relative delta of a known target
(including unchanged transverse edges), Thomson's variational principle supplies
the all-boundary-input impedance bound
  (1-delta)Ztarget <= Zactual <= (1+delta)Ztarget.
Row-uniform inference alone does NOT certify unknown within-row disorder. A
qualified writing law or a separate physical certificate must earn that premise.
Nor does this inverse supply continuous component actuation to a binary relay.

The owned diagnostic solves full Kirchhoff systems AND the independent dual
systems for all64 introduced {1,2}^6 corners of a3-row/2-segment grid and16
further finite nonuniform cases. With conservative epsilon<=.06, largest sampled
off-row SUM=.0551206200, smallest selected=.9448793800, dual discrepancy<2.94e-14
and conservation error<3.27e-14. Three row-uniform inverse runs reach floating
precision in12 iterations; they are numerical diagnostics, not new convergence
proofs, physical learning, or measurements of component uncertainty.

Artifact: ROOT_POSITIVE_CURRENT_GRID_AND_FUNCTIONAL_INVERSE_SCREEN_20261114.py/JSON.

4. Fixed physical response versus state-dependent normalization

For two homogeneous continuous rows of resistance/length r coupled by g/length,
write k=sqrt(2rg), s=kL/2. A current I entering and leaving only the top row has
bottom-row current
  j_bottom(x)=I[1-cosh(k(x-L/2))/cosh(s)]/2.
Its maximum fraction is (1-sech(s))/2. An antisymmetric two-row read has energy
relative to its uncoupled read equal to tanh(s)/s. Allowing .06 off-row current
therefore changes that particular read by .0803523015; the single-row write
power ratio is [1+tanh(s)/s]/2=.9598238492. This is a separate excitation from
equal transverse voltage patterns imposed at both ends.

For an m-row common-end voltage eigenmode of the transverse path Laplacian
with eigenvalue lambda, a uniform discrete grid obeys
  (2+r g lambda)v_k-v_(k-1)-v_(k+1)=0, v_0=v_L=1.
With boundary rungs present its physical modal conductance is
  G=2[(1-v_1)/r+g lambda]; without them omit the last term.
This fixed-unit conductance differs from the dimensionless number G L r/2.
If r doubles, nearly doubled G L r/2 does NOT mean nearly doubled G.

The available producer final reports .205 and .396 relative to a longitudinal
reference proportional to1/r, at r120 and240ohm, and quotes their1.93 ratio.
IF these are the stated normalization, the actual conductance ratio is
  (.396/.205)*(120/240)=.9658536585,
approximately a3.4% decrease. The fragmented transcript does not support a new
exact geometry or a recovered model. It DOES require keeping these two meanings
separate. Nonzero useful loop participation and a growing-family access theorem
can remain valid; a1.93-fold physical conductance contrast is not supplied by
that normalization ratio.

ROOT's separately declared16-row examples with15 or16 segments, fixed270kOhm
rungs and120/240ohm horizontal states yield physical high/low ratios .96359--
.97171, versus normalized ratios1.92718--1.94342, depending on whether end rungs
are included. They are not reproductions of the unavailable producer model.
For fixed g and small r g L^2, leading common-end conductance is determined by
the fixed rungs; resistance-state sensitivity enters the screening correction.

5. Self-created access: a strong existing adaptive construction and its limits

Actual DISTINCT primary: Bonifaci--Mehlhorn--Varma, Physarum Can Compute Shortest
Paths, exact https://arxiv.org/pdf/1106.0423v3 . Abs metadata verified v3 dated
12Oct2011 before PDF navigation; displayed PDF also has a22Oct2018 header date.
Retain that literal artifact scope. Actual main0--430/pp0--7 read: fixed positive
edge lengths, positive initial diameters, imposed unit source-sink current,
resistance L_e/D_e, and local law Ddot_e=|Q_e|-D_e. Displayed theorem guarantees
attraction to unit flows on shortest paths; a unique shortest path gives a single
limit. Rate statements in the read introduction require stabilizing flow
directions; later proofs, algorithms, biology sources and experiments unread.
This is its own primary, not recovery of another paper's failed access.

The law is a real existing mathematical route for boundary flow to organize an
initially unselected network. It does not supply nonvolatile memory, a general
address compiler, preserved useful loops, a physical common freeze cue or cheap
restoration after preparing the path.

For two parallel paths with lengths L1<L2, let D1+D2=1, x=D1, a=1/L1,b=1/L2.
The declared ideal law gives
  xdot=x(1-x)(a-b)/(a x+b(1-x)),
  time(x0->x1)=[b log(x1/x0)-a log((1-x1)/(1-x0))]/(a-b).
With x0=.5,x1=.99,L1=1 and gaps1,.1,.01,.001, introduced normalized times are
8.5071,49.8632,463.4240,4599.0319. As the path gap shrinks, discrimination time
grows. With the boundary drive removed the SAME law gives Ddot=-D, so the entire
prepared access state decays by exp(-1) per normalized time unit. A nonvolatile
gate changes the physical model and must be supplied. Neither this known law
nor these two-path calculations complete a reusable self-organized writer.

The constructive operations supplied here are a globally clear geometric graph
path, a conditional positive-current compiler, and a bounded row-functional
inverse. They do not supply the physical means of writing arbitrary intrinsic
geometry or arbitrary hidden network functions. Those are concrete remaining
operations; broad labels for new foundations do not supply them.
