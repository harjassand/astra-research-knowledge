# An actual reused-carrier cell loses its target before rare collisions

30 October 2026. C. This is an ALL-HORIZON obstruction for the literal
uniform circuit in FIRST_OPERATION.md, plus an open parameter region.
It is not a lower bound for all three-carrier algorithms or for generic
approximate native inversion. All previous freezes are unchanged.

## 1. Actual circuit and full target being bounded

The source is the SAME memoryless flat qubit encoding

    N_U(X)=U(X tensor I_r/r)U*,  U*:U=I_(2r), D>=2r.

The initial target is singly encoded, with any inaccessible reference.
Two auxiliary ordinary calls prepare programmes on known logical inputs
(0,+ are the literal choice), and known memory M starts in +. Every
fresh call uses independent I_r/r. There is no exposed flag, source
adjoint, controlled unknown operation, switch, or U-dependent advice.

The known staged circuit, including source input and all phases, is:

    pre C_M SWAP01;
    V_can(a,b):M -> A3,M',R;
    ordinary N_U on A3;
    post C_M' SWAP01, then C_R SWAP13, then C_M' SWAP12;
    H_M'; trace physical3 and known R;
    retain physical0,1,2 and known M'.                    (1)

This PHYSICALLY REUSES programme1 before and after the source call,
interacts with the NEW source output before tracing it, and transfers
through programme2. Its source input can be payload-correlated. It is
not the newest-only conveyor or the previous spent-carrier class.

We choose ONE nontrivial active port

    a=11/14, b=5/14, a^2+3b^2=1.                        (2)

Its input-channel coefficient is4b^2-1=-24/49, not a decoupled Bell
input. The known M port and all three physical carriers are retained
between steps; no product-junk reset is made. The final processor may
be ANY known CPTP map on all remaining physical carriers and M, even
with unbounded computational resources. Thus the obstruction includes
every finite6*dim(M) relational decoder, rather than choosing a weak
output-M readout as a convenient target.

Fidelity is UNCONDITIONAL at throughput one. A tiny accepted subbranch
is not promoted into a high-throughput or a restoring-failure service.

Let m be any finite number of repeated cells. Auxiliary source count
is m+2, plus the original payload encoding if counted. The theorem is

    E_P Fe(R N_(U_P)) <= min(1, 1/4+36/r),              (3)

where U_P is the explicit fixed-Pauli-frame ensemble in Section6. The
bound is UNIFORM IN m, and hence implies failure of any uniformly
accurate all-U decoder in this fixed controller family. It is not a
pointwise bound for every specially oriented/known U. In particular

    sup_U (1/2)||R_U N_U-id||diamond
                         >=max(0,3/4-36/r).             (4)

R_U here includes all actual source calls of the controller; only its
known final decoding rule is chosen freely. There is no perfect bath,
noisy-hardware, practical threshold or physical execution claim.

## 2. Why a distinct-live-tag reduction is exact

For the proof unravel each I_r/r in a FIXED common junk basis as a
uniform classical hidden label j. This is a mathematical decomposition
of the actual channel; no label is given to the user. Controlled physical
permutations move the WHOLE tagged logical carrier. If all CURRENT live
labels are distinct, there is a unitary change of coordinates sorting
the current labelled carriers into:

    tag-position arrangement; one logical data register per live tag;
    known controller memory and any reference.           (5)

In these coordinates a known controlled physical permutation acts on
the position arrangement and its known control, and as the IDENTITY on
the logical data attached to each tag. It does not become a controlled
logical gate on an unknown source block. All known memory/source-input
operations act outside the original target's data register.

Initially the original logical input is independent of all auxiliary
data and known memory. Before any live-tag collision its sorted logical
data therefore stays a tensor factor, with its arbitrary reference,
attached to its ORIGINAL tag. Moving that tag coherently among positions
does not change or copy its logical data into M. When the tag is traced
out, the original logical input is exactly erased from ALL remaining
systems. This is stronger than a marginal decoded-fidelity statement.

Other programme logical registers can be entangled with known memory.
They still never interact again with that memory as DATA before a live
collision: all subsequent permutations only change their positions.
Their logical states, including each fresh source logical output, may
therefore be traced out in the reduced position/memory process. A local
unitary source frame on such a logical register can be commuted through
future position-only controls and eliminated under that trace. This
pays the reduced channel rather than assuming a classical sector model.

Only CURRENT live distinctness is required. A label previously discarded
may reappear in a later fresh call, and then has the SAME unknown source
frame as before, not a newly drawn independent frame. It can be renamed
as a new live carrier role in (5), because no other LIVE carrier has that
label and no old logical data register interacts again. The reduced
position/memory map is invariant under these role names. We do NOT
replace a returning label's source frame by an independent one. If the
original target tag is still alive, its reappearance is necessarily a
LIVE collision and is counted. If it has already been lost, learning
its frame later cannot revive its erased reference correlations.

## 3. Exact coherent12-dimensional no-collision walk

Name the original tag0, two other CURRENT live roles1,2, and append a
fresh live-disjoint role3. A tag-position basis is one of the six
arrangements of0,1,2, times known M=c in{0,1}. Its dimension is12.
There are coherent superpositions of positions; no population-only
random walk or positive-mean-speed argument is used.

For old known bit c, V_can has the following paths in order(M',A3,R):

    m=c,   A=c,   R=c:      raw coefficient2b;
    m=c,   A=1-c, R=1-c:    raw coefficienta+b;
    m=1-c, A=1-c, R=c:      raw coefficientb-a.           (6)

Their amplitudes are raw/sqrt2. The final H maps m to j with an
additional factor(-1)^(m j)/sqrt2. The physical permutation is

    g=(12)^m (13)^R (01)^(m+c).                         (7)

Apply (7) to the four labels. The label ending at physical position3
is traced. Different discarded labels are orthogonal physical-junk
Kraus outcomes, so their coherences are not retained. For the SAME
discarded label, all compatible position coherences ARE retained.
After a nontarget discard, canonically rename the two surviving other
roles as1,2. Histories with different discarded-label records are
orthogonal environment branches; merging their canonically relabelled
states is a legitimate CP sum, not conditioning on a future event.

Thus Kraus labels are(source logical A traced for this reduced walk,
known R traced, physical discarded tag). Each entry is exactly

    [raw coefficient] (-1)^(m j)/2.                     (8)

The source logical register is traced only in the analysis justified
in Section2; the actual circuit still uses its physical output before
discard. The exact code builds every entry of (8) and preserves all
matrix coherences. Symbolically, for every a,b,

    sum_all K* K=(a^2+3b^2)I_12.                        (9)

All144 quadratic-polynomial entries of (9) were checked exactly. At
normalized ports this is a CPTP walk, including absorption. Let S be
its survival CP map, summing the Kraus outcomes that do NOT discard
tag0. It is trace-nonincreasing; target loss is the complementary
positive event. Source flag values or discarded labels are never
observed by the physical user.

## 4. Exact lifetime, not an assumed gap or a fitted spectrum

For the actual fixed port (2), LIFETIME_CERTIFICATE.json contains a
rational12x12 real symmetric G and strict rational LDL pivots. Exact
arithmetic verifies

    G>0,     G-S*(G)=I.                                (10)

Every one of144 residual entries is exact. No eigenvalue tolerance,
simulated path, claimed mixing hypothesis or finite-time extrapolation
enters (10). A78-variable fraction-free solve proposed G; the residual
and positivity are the acceptance conditions.

Since S* is positive, (10) also gives G>=I. Exact rational absolute row
sums bound G<16I. For initial tag arrangement(0,1,2) and M=+,

    Tr G rho0 <15.                                     (11)

Summing the positive telescoping identity for (10) gives

    sum_(t>=0) Tr S^t(rho0) <=Tr G rho0 <15.             (12)

This is the expected number of fresh source slots attempted while the
original tag is still present in the no-live-collision walk. More
generally its uniform bound is16, and G<=16I implies

    S*(G)<= (1-1/16)G,
    Tr S^m(rho)<=16(15/16)^m.                           (13)

There is no protected original-tag mode at zero collision rate for
this actual controller. Equation (10) is an all-order operator norm
certificate, rather than a conclusion from one target state or from
the apparent speed of a classical particle.

The compiler ran once in0.041535s after imports. It checked the symbolic
Gram, exact lifetime residual and12 strict pivots; no rank was
substituted. Its largest fraction-free integer was583 bits. No native
source, trajectory, RNG, optimizer, Q=3 fidelity fit or quantum circuit
was run. Root independently rebuilt the literal circuit and certificate
in root_controller_intake/ without importing the producer, accepting
only the circuit/CP/lifetime scope before the present bridge.

## 5. Finite-r first-collision stopping and the full bill

Initially the three source labels are independent uniform. The chance
that any two coincide is at most3/r. Suppose they are distinct and the
original tag is still alive. The set of three CURRENT live labels is
well-defined on each past source/discard record, even though their
positions may be coherently superposed. The next independent uniform
source label hits this set with probability EXACTLY3/r, for r>=3.
This is a causal incoming-source event independent of the input. It is
not an observed actuator or a label chosen after seeing the future.

Conditional on avoiding this event, the normalized tag/memory update
is exactly S plus its loss branch, by Section2. Thus until the first
live collision, fresh role relabelling gives the SAME12-dimensional
walk. There is no hidden replacement of source frames on returning
dead labels. For any finite horizon h,

    Pr(first live collision before target loss, by h
          | initially distinct)
       =sum_(t<h) (3/r)(1-3/r)^t Tr S^t(rho0)
       <= (3/r) Tr G rho0 <45/r.                       (14)

The source-call timing is crucial: the new label is sampled before
the post-cell target loss, so a collision and loss on the same cell
are conservatively counted as collision-first. Combining (14) and the
initial union bound yields an input-independent bad-event probability

    p_bad <= min(1,48/r), uniformly in h.                (15)

For r=1,2 this bound is trivial; no nonexistent distinct-label event
is asserted. Only the input-independent no-collision/source process
is used to bound the first bad event. Nothing is inferred about what
the controller does after that event; it is granted perfect recovery.

## 6. An adversarial fixed-Pauli-frame source makes the failure operational

For each j in{0,...,r-1}, choose P_j independently and uniformly from
the four logical Paulis, ONCE for the entire experiment. Let

    U_P(|a> tensor |j>)=|j> tensor P_j|a>,               (16)

with a known embedding into D if necessary. This is an admissible
isometry in the original source class. Every reappearance of j uses
the SAME P_j. For an upper bound we may even grant the final decoder
the block/flag-coordinate convention and this ensemble law; the P_j
values themselves are unknown. The physical controller still performs
the same fixed staged circuit, not a flag-selective intervention.

On a branch with no initial/live collision before the target's loss,
Section2 factors the original encrypted logical qubit from all other
data before that loss. If the tag is lost by the final time, all
remaining systems are independent of the original logical input,
even if its old label/frame is learned later.

If the tag is still present at the final time, its P_(j0) has never
appeared in another simultaneous live source carrier: initially the
programme flags differed, and every reappearance while it is alive
would have been a live collision. Nor could j0 have been queried and
discarded earlier while the original was alive without such a
collision. The original data factor is the ONLY occurrence of
P_(j0) before the first bad event. Its value is independent of all
other source frames and reduced tag/controller records. Averaging
that fixed unknown Pauli completely twirls this original data qubit
and breaks its Bell-reference correlations, even though the final
processor may read all remaining physical flags and use arbitrary
known CPTP operations. Sorting/unsorting positions is independent of
P_(j0) and cannot restore that correlation.

Consequently every good branch has Bell fidelity exactly1/4 after
this Pauli-frame average. The bad-event probability is independent of
the logical input before the first bad event and is bounded by (15);
its later behavior is granted fidelity1. Hence

    E_P Fe <= (1-p_bad)/4+p_bad
            <=min(1,1/4+36/r),                         (17)

for EVERY finite horizon and EVERY known final CPTP decoder. This is
an adversarial ensemble bound, so at least one fixed native U_P
defeats any proposed uniformly accurate decoder. It is NOT a claim
that a source whose frame happens to match a known decoder cannot be
decoded. Bell-input trace distance is at least1-Fe, giving (4).

If a specified finite relational readout/decoder makes the logical
channel U-independent, (17) bounds that common channel as a corollary.
No free exponential final map is needed for the result; allowing one
does not repair this controller's premature data loss.

## 7. A robust open parameter family, with its actual constants

The conclusion is not a singular rational-coefficient accident. For
another normalized real port(a',b') let

    d^2=(a'-11/14)^2+3(b'-5/14)^2 <=1/64^2.             (18)

The known Pauli Stinespring isometries differ in operator norm by
exactly d, because their label components are orthogonal. The fixed
pre/post controls, source, tracing isometries and survival projection
do not enlarge this bound. Thus, with L=16,

    ||S'*(G)-S*(G)|| <=2L d <=1/2,
    2G-S'*(2G)>=I.                                    (19)

The initial no-collision lifetime is therefore less than30 and its
uniform bound less than32. Repeating the ACTUAL causal argument gives

    p_bad<=min(1,93/r),
    E_P Fe<=min(1,1/4+279/(4r)).                        (20)

All other gates and the declared memory/source wiring are unchanged.
This is a mathematical open-family obstruction, not a physical noise
threshold or an acquired calibration region. It includes r-dependent
ports only if they stay in (18). It does NOT control tuning toward
a=+/-b or another change of architecture; no uniform lifetime near
those protected/independent-query limits is inferred from (10).

## 8. Scientific outcome and the surviving operation

This was a real reused-P1 attempt with a payload-correlated source
input, postinteraction with the fresh source output and bounded
known memory. It was not killed merely by holding-time equivalence
or by extrapolating the exact-success Schur theorem. Its exact
coherent target-tag lifetime shows why it fails before useful rare
collisions, uniformly over all horizons and even the strongest final
receiver. Ordinary identity protection of the physical target does
not have this loss, but also supplies no inverse by itself.

The surviving requirement is now precise: keep a protected original-tag
algebra at zero collision rate AND make its order1/r effective channel
a useful logical pump into a finite known output. The admitted
T0+qT1 peripheral-projection theorem can test such a future controller,
but the current fixed controller fails its useful protected-mode
premise. The independent-query pointsa=+/-b are already handled by
ordinary programme-copy barriers. Rank-dependent weak tuning away
from them and a different staged control remain OPEN, not excluded
by a finite lifetime at one port or by the robust local region above.

The complete ordinary flat RDS/Petz quadratic-r service remains the
strongest admitted generic positive comparator. For the specially
structured known-flag ensemble (16), an ordinary controller allowed
to read/keep the flag and wait for a matching query can instead
avoid throwing the data away; our obstruction is to this stipulated
staged controller, not a claim of hardness even for that simple
subfamily. All source latency/protected storage/controller costs
remain charged; no practical or hardware advantage was established.
