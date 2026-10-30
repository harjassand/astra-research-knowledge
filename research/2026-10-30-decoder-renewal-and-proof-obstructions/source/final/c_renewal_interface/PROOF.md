# Spent-carrier disposal imposes a quadratic feedback cost

30 October 2026. C's constructive recurrence and architecture obstruction.
This concerns the SAME fresh-junk forward source as ROOT28. It is not a
lower bound for all approximate physical-query inversion.

## 1. Native source, controller class and query convention

The unknown source is

    N_U(X)=U(X tensor I_r/r)U*,
    U:C^2 tensor C^r -> C^D,   D>=2r.

The payload is one independently singly encoded logical qubit, with an
arbitrary inaccessible reference. Each auxiliary call has fresh independent
maximally mixed junk. No source environment, junk label, inverse, controlled
unknown operation, quantum switch or U-dependent advice is supplied.

There is ONE initial auxiliary forward call, independent of the payload,
on any known state of a logical input and known memory E. A Bell input is
allowed. Denote its physical output Bp and the encoded payload B0. The
controller then performs m feedback cells. In cell t it chooses two known
isometries

    V_(+,t),V_(-,t): E_(t-1) -> E_t tensor A_t,

where A_t is a logical qubit, and applies

    W_t=P_+^(B0,Bp) tensor V_(+,t)
                +P_-^(B0,Bp) tensor V_(-,t),
    P_+/-=(I+/-SWAP_(B0,Bp))/2.                         (1)

It forwards A_t through N_U to obtain the next Bp, and DISCARDS the spent
physical Bp from the preceding cell. B0 is retained. At most two physical
carriers are retained between cells (three transiently during the call).
The whole known memory E_t is retained. Its dimension is unrestricted; it
may contain EVERY known reference R created by the canonical memory port,
all measurement records and clean workspaces. Arbitrary known memory-only
processing can be absorbed into the two isometries by purification. The
isometries can coherently depend on earlier stored classical outcomes.

All physical-carrier operations BEFORE final extraction are exactly those
in (1), and the spent-carrier discard. In particular the theorem does not
allow retaining a spent physical carrier as part of E, transferring its
whole state to another register before discard, extra physical rotations
or measurements, or a different interaction with B0. Such operations are
potential escapes, not admitted shortcuts. The final known decoder may
be ANY CPTP map on B0, current Bp and all E_m. We do not restrict its cost.

The counted auxiliary native calls are Q=m+1, in addition to the original
payload encoding if that is counted separately. m counts CELLS, not total
queries. A finite-cap adaptive schedule within this class can be padded
only if it still executes the declared spent-carrier disposal at each
cell; we do not silently pad a branch that has already applied a different
physical final decoder. The theorem below concerns a fixed m-cell schedule,
with coherent/record-dependent known-memory adaptation inside those cells.

## 2. An exact all-r logical recurrence

Write

    A_t=(V_(+,t)+V_(-,t))/2,
    B_t=(V_(+,t)-V_(-,t))/2.

These maps act only on known memory. They obey

    A_t* A_t+B_t* B_t=I,
    A_t* B_t+B_t* A_t=0.                               (2)

In the hidden input frame, split the whole physical SWAP into a logical
SWAP F=(L0,Lp) and the junk SWAP G=(J0,Jp). The cell before the next call
is therefore I tensor A_t+F tensor G tensor B_t. Moving the same unknown U
through whole-register permutations is an analysis identity, not a gate.

Suppose the two live junk carriers have state I/r tensor I/r independent
of every logical carrier and E. For each pair of branches u,v in {0,1},

    Tr_Jp[G^u (I/r tensor I/r) G^v]
       = I_J0/r,             u=v,
       = (1/r) I_J0/r,       u!=v.                     (3)

In particular the remaining junk REFACTORIZES, including in the cross
terms; it is not merely known to have the right marginal. The fresh source
appends an independent I/r. Induction pays (3) at every cell even when all
known memory is entangled with both logical carriers. There is no assumed
reset, classical sector process or Markov closure.

Let rho act on (L0,Lp,E), with an arbitrary external reference. Regard A_t
and B_t as appending the next logical carrier Lnew. Trace the spent Lp.
The exact reduced recurrence, with every E_t output retained, is

    T_(r,t)(rho)=D_t(rho)+(1/r) X_t(rho),

    D_t(rho)=Tr_Lp[ A_t rho A_t* + F B_t rho B_t* F ],
    X_t(rho)=Tr_Lp[ A_t rho B_t* F + F B_t rho A_t* ].   (4)

The new output is (L0,Lnew,E_t). N_U on Lnew and the factored new junk
restore the physical description. Equations (2) imply D_t is CPTP and
Tr X_t(rho)=0 for every rho: F commutes with A_t*B_t on the input space.
The exact T_(r,t) is CPTP by its native construction, for every integer r.

This is a finite logical-memory representation of a genuine physical
operation. It retains the growing known history without retaining the
spent physical carriers. It has no U-, spectral- or state-learning oracle.
It need not be computationally small when E grows; the bound below even
allows arbitrarily large E and an unbounded final known decoder.

## 3. What happens before a first cross insertion

D_t has a legitimate two-outcome CP instrument: its A branch and its B
branch. Along an all-A history the original payload is untouched and
independent of the known-memory/current-programme resource. After tracing
the spent programme, the rest is a SINGLE current source call on a known
possibly mixed/entangled logical input and memory. Its known memory's
marginal and the all-A survival probability are U-independent, because
tracing N_U is tracing its logical input. This holds by induction.

Let p_t be the probability of surviving t all-A branches, p_0=1, and

    d_t=p_(t-1)-p_t>=0.                                (5)

The d_t are the probabilities of a FIRST B branch at time t, hence sum
d_t=1-p_m. The p_t and d_t are independent of the payload and of U.

On such a first B branch, B_t has acted only on known programme memory;
the physical SWAP then moves the SOLE original payload carrier into the
spent leg, which is immediately discarded. Consequently the complete
remaining state is independent of the original logical input. For a Bell
test the untouched reference is I/2 and is product with the whole receiver.
Later CPTP maps cannot repair this erasure. This is a state-level statement,
not just a marginal-fidelity claim.

The all-A branch, conditioned on survival, is exactly a one-auxiliary-query
decoding resource. We import the accepted exact complete one-query bound
from root_comb/ROOT_MECHANISM.md Section 4, namely

    average_U Fe(one-query receiver N_U)<= (1+1/r)/4.    (6)

It permits arbitrary known entangled programme inputs, memory and final
processors, not only a normalized Bell programme. It is also attained
uniformly in U by the known SWAP-sector/transpose receiver. Therefore for
the cross-free process D_m ... D_1 and any final known decoder,

    average_U Fe(D)<=1/4+p_m/(4r).                      (7)

Any input-independent branch gives Bell fidelity exactly 1/4. Thus (7)
does not assume that such a branch can be detected by the receiver.

## 4. First-cross bound with the full retained history

Use the exact telescoping identity

    T_m ... T_1-D_m ... D_1
      =sum_t T_m ... T_(t+1) (X_t/r) D_(t-1)...D_1.    (8)

For a prefix in D that already had a B branch, the Bell reference is
product I/2. X_t has trace zero and acts only on the receiver, so this
entire contribution has ZERO Bell pairing after any subsequent maps and
final decoder. It is not necessary to bound these terms by a global
number-of-branches norm.

Only the all-A prefix contributes. Purify its subnormalized logical
state, and let alpha,beta be the two branch vectors obtained by A_t and
F B_t. Their squared norms are p_t and d_t. Partial trace gives

    ||X_t(all-A prefix)||_1 <=2 sqrt(p_t d_t).           (9)

This is the elementary rank-one trace norm/triangle bound; it includes
arbitrary inaccessible reference and the complete known history. Equation
(3) contributes the explicit 1/r. The cross output is Hermitian and trace
zero. All future exact maps and final decoding are CPTP, so contraction
and the effect inequality |Tr(E H)|<=||H||_1/2 give a fidelity contribution
of absolute value at most sqrt(p_t d_t)/r. Hence

    average_U Fe(T)<=1/4+
                [p_m/4+sum_t sqrt(p_t d_t)]/r
             <=1/4+[p_m/4+sqrt(m(1-p_m))]/r.            (10)

For m>=1 the last bracket is decreasing in p_m in [0,1], so

    average_U Fe(T)<= min{1, 1/4+sqrt(m)/r}.             (11)

The proof is uniform in every allowed choice of V_+,V_-, not just one
opposite sector angle or fixed memory dimension. Coherent known-memory
adaptation is included in these isometries. Equation (11) is an average
upper bound and therefore a worst-unknown-U obstruction. It is not an
upper bound on every specific known or favourably oriented U.

In particular a uniform arbitrary-input decoder with half-diamond error
at most epsilon must have Bell fidelity at least 1-epsilon for every U,
and thus, for epsilon<3/4,

    m >= r^2 (3/4-epsilon)^2.                           (12)

The inequality allows every known reference history and every final CPTP
extraction; adding an acknowledgement or a larger final decoder cannot
remove it. It identifies SPENT PHYSICAL CARRIER DISPOSAL as the failing
interface. It does not show quadratic complexity for general native
queries, arbitrary two-carrier interactions, a retained-physical-history
comb, or a different approximation mechanism.

## 5. Literal canonical memory-port specialization

For the admitted fixed memory port put

    a(delta)=cos(delta)/2+sqrt(3) sin(delta)/2,
    b(delta)=cos(delta)/2-sin(delta)/(2sqrt(3)),
    K=(I-2 SWAP_(M,R))/sqrt(3),
    V0=id_M tensor |Phi>_(A,R).

The exact known isometry is

    V(delta)=[cos(delta)I+sin(delta)K] V0,
    V0* K V0=0,   V0* K^2 V0=I.                        (13)

Use V_+=V(delta), V_-=V(-delta), giving A=cos(delta)V0
and B=sin(delta)K V0. This is not a free filter or a unitary on arbitrary
M,R inputs; only the Bell-appended subspace is its input. A finite known
Stinespring implementation is already supplied by the Pauli port.

The recurrence (4) becomes

    T_r=c^2 T_A+s^2 T_B+(cs/r) X,
    ||X||_diamond<=2,

where T_A,T_B are CPTP and X is trace-annihilating. The c,s stand for
cos(delta),sin(delta). Cross interference is linear in s/r; a B branch
has weight s^2, independent of r. Its first occurrence before a cross
erases the original payload, exactly as in Section 3. This is the paid
variance/noise mechanism behind the obstruction, not a guessed Zeno rate.

If the NEW R and new physical output are also erased, the named M channel
has Bloch contraction

    c^2-s^2/3=1-(4/3)sin^2(delta).                      (14)

It is the mixture c^2 id+s^2 (AdX+AdY+AdZ)/3. In this
specialization tracing the whole fresh port annihilates the cross term
already at one cell. Keeping R is therefore necessary even for the
first-order signal, but (11) shows that keeping ONLY known-reference
history while erasing spent physical carriers is still insufficient for
a subquadratic high-fidelity decoder in this architecture.

For predetermined opposite angles there is the additional elementary
bound

    Fe <=1/4+sqrt(1+18m)/(4r).                          (15)

Indeed p_t=product_(j<=t)c_j^2, the normalized cross map has diamond at
most 2, and its action on the Bell-minus-product correlation has norm at
most 3 p_(t-1)|c_t s_t|/r. Its Bell contribution is at most half that.
Also sum p_(t-1)^2 c_t^2 s_t^2 <=(1-p_m^2)/2. Maximizing
p_m/(4r)+(3/(2r))sqrt[m(1-p_m^2)/2] gives (15).
The broader and slightly stronger large-m bound (11) is the main result;
(15) records the independently derived narrower route, not a claimed
optimal coefficient.

## 6. What the construction decides, and what remains open

The original exact-success-or-draw question has a stronger general answer
from the accepted root EXACT_HERALDING_SCHUR theorem: capped exact success
<=Pr[Bin(Q,1/r)>=r], and any a.s. exact Las Vegas inverse has expected
queries >=r^2. A failure that really restores the encoded payload and
retains history is already included. We do not repeat that proof as a new
construction or extrapolate it to approximate recovery.

The present approximate theorem is independent of exact polynomial zeros.
It gives a finite conditional-memory representation and a whole-family
obstruction for one tempting repair: dispose the spent physical carriers
but keep all named logical-reference memory. It rules out an O(1/r) noise
suppression for that operation. It does NOT rule out the fully unclosed
physical history in root COHERENT_MEMORY_PORT, where discarded-path
erasure is unavailable, nor root's differently warranted persistent-source
process. Source persistence changes the joint oracle and is not obtained
from a memoryless marginal.

Ordinary DME/HME already pays a signal 1/r against constant collision
variance, and the strong flat RDS/Petz route already supplies quadratic-r
recovery with paid programmes. This theorem provides a reason the present
physical feedback/disposal representation cannot beat that rank scaling;
it is not a new quadratic algorithm or an advantage claim. Pure-isometry
success-or-draw and four-query inversion remain ordinary r=1 operations;
they do not imply restoring failure for the fresh mixed source.

The surviving worthwhile question is a representation that preserves the
physical permutation/coherence history while allowing an efficient final
extraction, or a genuinely acquired joint-source persistence operation.
General approximate linear-r native inversion remains OPEN.
