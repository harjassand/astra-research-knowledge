# The full clock Gibbs trace: an all-size one-phase cylinder expansion

29 October 2026. This is a new continuation. The endpoint/path and zero-T
stability packages are frozen and unchanged. No finite Hamiltonian fixture
or dynamics is run. All traces below include EVERY clock level.

## 1. Target, units and ordinary prior boundary

In the exact prefix gauge the two-body simulator is Delta H'(lambda;S),

    H'(lambda;S)=sum_i Q_i+lambda sum_e V_e(S),
    Q_i=I-|0><0|_i.                                        (1)

There is one L-dimensional clock per source check. Every gauged hopping
label e has clock support of size <=q and norm <=1 in
B(clocks) tensor l1(free source-check symbols). At most d hopping labels
touch a clock. Only its OWN wrapping hop contains S_c. Other factors are
diagonal clock signs. This native symbol placement is retained throughout.
The source's physical check relations are imposed only at final evaluation.

Let beta be the PHYSICAL inverse temperature, and t=beta Delta the scaled
clock inverse temperature. Put

    Z_t(S)=Tr_clock exp[-t H'(lambda;S)],
    F_beta(S)=-log Z_(beta Delta)(S).                        (2)

The trace is unnormalized. A unit of source check-defect energy is one,
as in the accepted Hcode=sum_c(I-S_c)/2 convention.

The controlled ordinary methods are finite-slab quantum contour expansions
and scalar Kotecky--Preiss cluster bounds. In particular
[Borgs--Kotecky--Ueltschi 1996, Sections3--5](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/Low-Temperature-Phase-Diagrams-for-Quantum-Perturbations-of-Classical-Spin-Systems-.pdf)
already use a fixed-size imaginary-time transfer slab and contours.
[Helmuth--Mann 2023](https://arxiv.org/html/2201.06533v2)
add constructive inclusion-exclusion weights and algorithms. Their displayed
full statements have translation-invariant/pure-phase assumptions. We do
not silently apply such a statement to arbitrary syndrome signs or the
inhomogeneous clock graph: Sections2--5 give the one-product-phase
construction directly, needing only bounded rank and incidence.

The newer [Mann--Waite2601.21140v2, Theorem1](https://arxiv.org/html/2601.21140)
has a sufficient coupling window proportional to exp(-2qt)/t. That
fixed-temperature weak-coupling window does not pay the present fixed-lambda,
large-t regime. No new general contour principle or historical novelty is
claimed here.

## 2. Exact transfer slabs and label activities

Choose a fixed large integer delta0. For t>=3delta0 write

    M=floor(t/delta0)>=3, delta=t/M in [delta0,2delta0].      (3)

Thus exp(-tH') is EXACTLY the M-th power of T=exp(-delta H').
The slab size never grows with M. With N0=sum_i Q_i define

    T=exp(-delta N0) sum_(J subset E) W_J,
    W_empty=I.                                             (4)

W_J is the exact-label part of the interaction-picture Dyson series:
every label in J occurs at least once and no other label occurs. The series
uses exp(sN0)V_e exp(-sN0), 0<=s<=delta. Its support is the union U_J of
the label supports. Its norm in the stated operator/coefficient Banach
algebra satisfies

    ||W_J|| <= w^|J|,
    w=exp[delta |lambda| exp(2qdelta)]-1.                   (5)

Indeed each interaction-picture factor has norm <=exp(2qdelta). If label e
occurs m_e>=1 times, time interleavings and the integration factorial give
the product of a_e^m_e/m_e!, a_e=delta|lambda|exp(2qdelta).
Summing the positive m_e yields (5). This is not a bound using the extensive
norm of exp(delta N0).

If J splits into spatially disjoint components of its support hypergraph,
their W_J factorize exactly. Dyson interleavings sum to the product of
the component series, and those operators commute. Common symbols cause
no problem: their coefficient algebra is commutative; independence of
the symbols is not used for this factorization.

## 3. A gas of connected bad spacetime sets

Make a spatial graph on clock cells by joining every pair in the support
of a native gauged hopping label. Its degree is at most d(q-1). Its product
with the M-cycle in time has degree at most

    Dst=d(q-1)+2, K=Dst+1.                                 (6)

Insert computational clock bases between the M transfer factors in the
trace. At slab k choose J_k in (4) and let a_(i,k+1) be its end clock state.
Mark the spacetime cell (i,k) BAD if i belongs to U_(J_k), or if that end
state is nonzero. Outside the active U_(J_k), the clock state is unchanged
through the slab and contributes exp[-delta 1_(a_(i,k+1)!=0)].

Connected components of the bad set, in this spacetime graph, factor
EXACTLY. An active quantum label has all its cells in one component. A
nonzero state propagated across two slabs connects their cells by a
temporal edge; an input nonzero state ending in an active vacuum cell is
connected in the same way. The vacuum outside the component has a unique
state and weight one. Thus no clock state, quantum label or consistency
condition couples two nonadjacent components. A component that winds
around time is retained, with the original trace condition.

For a nonempty connected bad set B, let z_B(S) be the sum of precisely
those microscopic choices with bad set B and vacuum outside. Compatibility
means no common or adjacent cells. Then

    Z_t(S)=sum_(compatible families Gamma) prod_(B in Gamma) z_B(S). (7)

All activities are scalar elements of the free-symbol l1 algebra. The
quantum noncommutativity was handled inside each exact W_J and its matrix
elements; (7) is an ordinary commutative polymer gas.

Here is an explicit positive majorant including every primitive cost. Put
A=union of active cells in a fixed history, n=total number of slab labels.
Then |A|<=qn; every cell in B\A has a nonzero end state. Equation (5) and
the onsite factors therefore give

    w^n exp[-delta0 |B\A|]
        <= max(w^(1/q),exp(-delta0))^|B|, provided w<=1.

There are at most L^|B| assignments of end clock states. At most d|B|
distinct slab labels have support contained in B, so at most 2^(d|B|)
label subsets are possible. The internal Dyson sums have already been
paid in (5). Consequently

    ||z_B||_l1 <= epsilon^|B|,
    epsilon=L 2^d max(w^(1/q),exp(-delta0)).                 (8)

These deliberately loose dimension/label costs are NOT supplied for free.
The estimate holds in every finite spatial graph and with every choice
of formal syndrome signs, including assignments not physically admissible.

## 4. Absolute logarithmic clusters and an explicit constant gate

There are at most K^(2m) connected m-cell sets containing a fixed cell,
by the depth-first-walk bound. An incompatible polymer has a cell in the
closed neighborhood of the reference polymer. Define

    b=K^2 exp(2)epsilon,
    b<=1/[2(K+1)], B0=b/(1-b).                              (9)

Apply the ordinary KP criterion to activities exp(|B|)z_B with size
function |B|. The incompatibility sum is at most

    |G| K sum_(m>=1)b^m = |G| K b/(1-b) < |G|.

The scalar complex-activity theorem applies coefficientwise in the
commutative l1 algebra by its absolute majorant. Write the absolutely
convergent logarithm as a sum over connected logarithmic MULTI-polymers C,
with total mass m_C=sum_(B in C)|B| counting repetitions. The rooted bound is

    sum_(C: union C contains x) ||Phi_C||_l1 exp(m_C) <= B0. (10)

One obtains (10) by summing the rooted-polymer KP bound over B containing
x; overcounting repeated choices is harmless. The same bound holds on the
infinite time graph with the finite spatial graph held fixed. The ordinary
theorem used here is [Ueltschi0304003v3, Theorem1/equations3--5](https://arxiv.org/abs/math-ph/0304003).
For real lambda, this logarithm equals the ordinary real log of the
positive clock trace. It starts on that branch at lambda=0 and cannot
change branch under the zero-free KP gate. The intermediate exact-label
operators need not be Hermitian; no positivity of individual activities
is required by the scalar complex-activity theorem.

A completely rational, very conservative sufficient parameter prescription
is available. Set

    eps0=1/[16(K+1)K^2], A0=L 2^d/eps0, eta=1/A0,
    delta0=bit_length(A0),
    lambda_T=eta^q * 2^(-8qdelta0)/(4delta0).                (11)

A0 is an integer. Then exp(-delta0)<2^(-delta0)<=eta.
Uniformly for delta in [delta0,2delta0] and |lambda|<=lambda_T,

    delta |lambda| exp(2qdelta)<=eta^q/2,
    w<=eta^q,
    epsilon<=eps0,
    b<=1/[2(K+1)], B0<=Bstar=1/(2K+1).                     (12)

We used exp(1)<4, the sharper elementary exp(2)<8, and
exp(x)-1<=2x for 0<=x<=1/2. The second bound pays b in (9), not merely
the first looser exponential bound. This gate is
constant in N. It can require a MUCH smaller lambda, hence MUCH larger
Delta, than the previously compiled clock recipe. The literal old recipe
is not asserted to meet (11).

## 5. Temporal lifting, zero-temperature identification, local residual

A logarithmic cluster includes a connected incompatibility graph of
polymers, not just one bad component. Its UNION of cells is connected in
the spacetime graph and has at most m_C cells. If m_C<M/2, every simple
cycle in this union has fewer than M temporal steps and has zero winding.
The whole connected cluster therefore lifts to the infinite time cover.
Given one vertex lift, the lift is unique. Its temporal span is at most
m_C-1<M/2. Conversely a cluster of this mass in the infinite cover projects
injectively; the projection creates no new overlap or adjacency, so preserves
the incompatibility graph, tuple multiplicities and Ursell coefficient.
The component weights also agree, because a nonwinding component has a
vacuum cut and the slab operators are identical.

This is a bijection between the small clusters modulo time translation
on the line and modulo cyclic time translation on the cylinder. Each
small cylinder orbit has EXACTLY M placements. If a nonzero cyclic shift
fixed the cluster, lift uniqueness would make its finite lifted union
invariant under a nonzero translation h modulo an integer multiple of M,
which is impossible. Ordered multi-polymer tuples retain their ordering;
there is no extra division by their orbit or stabilizer.

Let p_infinity(S) be the sum of one representative of each finite line
cluster modulo simultaneous integer time translation. It is well-defined
at each FIXED finite spatial size: every orbit can be shifted to contain
some cell in time layer zero, so (10) bounds its total l1 norm by Nclock B0.
The matched small clusters cancel exactly in

    log Z_(Mdelta)(S)-M p_infinity(S).

Using (10), all remaining cylinder clusters have mass >=M/2; their total
norm is <=M Nclock B0 exp(-M/2). The same bound holds for M times the
remaining line-orbit sum. Hence the difference divided by M tends to zero
at each finite N. Evaluating each formal sign assignment, the elementary
finite-dimensional spectral limit gives

    p_infinity(S)=-delta E(S).                              (13)

E(S) is the actual scaled clock ground energy already acquired by KT.
This identification is made at fixed finite N BEFORE invoking a bound
uniform in N. No exchange of the N and zero-temperature limits is needed.

The decisive improvement over the global trace bound is NATIVE SYMBOL
INCIDENCE. If a coefficient of Phi_C contains S_c, that cluster contains
c's wrapping label at some time, hence a cell (c,k). Projection onto
symbol parities containing c is contractive in l1. Sum (10) over these
M anchors on the cylinder, or choose one such anchor at time zero for
each line orbit. The SAME cancellation of small clusters proves

    log Z_t(S)=-t E(S)+Theta_t(S),
    sup_c sum_(X containing c)|Theta_t,X|
         <=2M B0 exp(-M/2).                                (14)

Symbol-free scalar terms can be extensive and are retained; they cancel
in all syndrome ratios. Equation (14) is before quotienting physical
check relations. Equivalently its left side is
(1/2)||Theta_t-T_c Theta_t||_l1 for the sign-flip automorphism T_c.
There is no invalid derivative of S_c subject to S_c^2=1. The root is
one native clock cell per marked check and per slice, not all Nclock cells.

## 6. The source Peierls deletion bound survives

Also impose the frozen ground-energy gate lambda<=lambda_*=rho^L/12 and
Delta=1/(4lambda^L). Its proven local incidence bound gives

    Delta E(S)=scalar+sum_c Q_c+Rground(S),
    sup_c sum_(X containing c)|Rground_X|<=1/8.             (15)

For a valid primary witness tau contained in a syndrome sigma, deleting
tau changes the defect term by |tau|. The ground remainder can change it
by at most |tau|/4, and (14) changes the dimensionless free energy by at
most 4M B0 exp(-M/2)|tau|. Thus

    F_beta(sigma)-F_beta(sigma+tau)
       >= beta_eff |tau|,
    beta_eff=(3/4)beta-4M B0 exp(-M/2).                     (16)

The primary witness is itself a valid coboundary, so this deletion stays
in the admissible syndrome set and is injective for a fixed tau. The
logical multiplicity of every admissible Pauli syndrome sector is the
same; taking the full clock trace introduces exactly the weights in (2),
not a further degeneracy or unobserved normalization.

Whenever beta_eff>beta_c, where beta_c is the supplied primary counting
threshold in defect-energy-one units, the full native-clock Gibbs state
therefore obeys the SAME source two-sector decoder-bad bound

    p_bad0<=4 * 2^(-2^(k-1)).                               (17)

No large-polymer logical remainder appears: (1) depends exactly only on
source stabilizers, at EVERY energy, so the full logical algebra is inert
in this Hamiltonian. This statement is not a claim about arbitrary added
physical Hamiltonian errors.

The physical temperature can be chosen fixed in N. For an explicit useful
coarse test let BDelta be any integer with Delta<2^BDelta and set
Mcrit=2(BDelta+4). If M>=Mcrit, (12) gives

    4M B0 exp(-M/2)/beta
        <=4 Bstar Delta/delta0 exp(-M/2)<=1/4,

so beta_eff>=beta/2. For instance require beta>2beta_c and
floor(beta Delta/delta0)>=max(3,Mcrit). All these are fixed-parameter
conditions. They do not require N exp(-beta Delta gap) to be small.

## 7. Scope and primitive cost

This is a full-partition-function, all-size theorem for the SAME native
Pauli-clock Hamiltonian form. It retains all excited-clock sectors and
their possibly large physical interactions. The price is an additional
explicit constant coupling gate, potentially an even more prohibitive
penalty; no practical temperature/strength tolerance is claimed.

The extra analytical symbol algebra is not a new physical register.
No hidden background generator, environment reset or arbitrary clock
preparation is used to obtain (14). For finite truncations, connected
spacetime sets of mass m have bounded-degree enumeration exp(O(m));
each slab activity can be evaluated by its finite-label inclusion-exclusion
or Dyson series on at most m active clock cells. The clock matrix size is
at most L^m, with up to 2^(dm) native label subsets and 2^m symbol
assignments if coefficients are explicitly recovered. These are charged
exponential-in-m primitives, not a free local pressure oracle. The theorem
needs only their proved norm bounds and no activity evaluation.

Native bath access, initialization of a logical-encoded thermal environment,
and a useful physical storage mechanism are separate operations. The
specified dynamical composition is stated separately after its full
logical/support/rate costs are paid; no native Davies limit is imported.
