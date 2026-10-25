# Joint experimental preparation can avoid hard posterior resampling

OWNED revealing correction to AVERAGE_PREPARATION_OBSTRUCTION658c7bf8:
its reductions and1/4,1/2 bounds concern a procedure that RECEIVES an
externally chosen native witness X and must then generate X'. They do NOT
obstruct an active experiment that can generate BOTH native addresses
together. Our source-query diagnostic has the latter freedom. The SAME
supposedly obstructive family admits an exact polynomial-time ideal joint
generator. No new fixture, source or target is needed; this is an exact
construction on the very family used in the obstruction.

## 1. An exact strongest baseline on the same hard family

Keep public one-way-permutation code P:{0,1}^n->{0,1}^n and

    h(0,z)=z,     h(1,z)=P(z),

with native nu uniform on the(n+1)-bit cube. Draw U uniform n bits,
compute Y=P(U), and draw independent fair B,B'. Return

    X =(0,Y) if B=0,  otherwise(1,U),
    X'=(0,Y) if B'=0, otherwise(1,U).                     (1)

Because P is a permutation, Y is uniform. Conditional on Y, U is its
unique inverse as a MATHEMATICAL witness; the algorithm already sampled U
and never computes that inverse. Given Y, the two independent branch bits
choose independently from the two native h-preimages. Therefore(1) has
EXACTLY the ideal native full-fibre product pair law Pi. Both endpoint
marginals are exactly nu and h(X)=h(X') always.

Cost is ONE known forward P evaluation, n+2 fresh fair bits and O(n)
address assembly/storage, with no old/current source value in preparation.
A current diagnostic then pays its actual two target values. It is
polynomial time and is available to an equally informed retaining/code-
aware comparator. The conditional distribution X'|X is mathematically the
hard posterior, but the joint generator does NOT accept an arbitrary
preexisting X as its input. Disintegration is not a free implementation,
and it is not necessary when both experimental inputs are controllable.

Thus the old cryptographic bounds remain valid at their declared
WITNESS-CONDITIONED transition interface; they do not show average-pair
preparation or experimental-coverage failure for the active query task.
For f(B,z)=B, this exact generator has disagreement1/2 and recovers the
full conditional diagnostic signal. The previous conclusion that efficient
native-pair experiments cannot reveal that distinction is defeated by(1).

## 2. A source-free forward-word compiler, not a supplied inverse

There is a constructive generalization. Suppose a retained closed code
has tagged native form

    h(j,z)=P_j(z),    j in{1,...,m}, z in Z,              (2)

where Z is an explicitly uniform-samplable finite domain and each known
P_j is a PERMUTATION of Z. This is a real semantic premise/certificate;
it cannot be recognized from a few outputs or inferred from source code
size. The native law is uniform tag times uniform Z. The compiler gets
the actual branch programs from the retained tagged code, not latent
coordinates or an inverse oracle. All extraction, verification and code
evaluation work is paid.

Seek FORWARD programs R_j and Q with

    P_j o R_j = Q        for every j,                     (3)

where R_j,Q are compositions of the known permutation programs (identity
included). No inverse instruction is present. A generic finite compiler
enumerates word tuples to a literal search/length budget and checks their
known-code identities; failure returns UNKNOWN with all search work paid.
Exact finite-domain checking may be expensive. A semantic identity oracle
or an efficient generic common-word solver is not supplied.

When the P_j COMMUTE, an actual bounded construction is immediate:

    Q=product_(k=1)^m P_k,
    R_j=the same product with P_j omitted.                (4)

Commutation moves P_j into its omitted position, proving(3). Each R_j is
a permutation because it is a composition of permutations. This gives an
explicit common forward cover rather than granting the desired sampler.
The m=2 identity/P case reduces literally to(1).

Draw U uniform Z, independent uniform J,J' in{1,...,m}, and return

    X=(J,R_J(U)),       X'=(J',R_J'(U)).                  (5)

Every endpoint marginal is exactly native, since each R_j is a permutation.
Q is a permutation, so conditional on Y=Q(U), U is uniquely specified and
the independent tags choose independently from ALL m native h-preimages.
Thus(5) is the exact full-fibre conditional product law, without inversion.
Only the two selected forward words need evaluation, at most2(m-1)
primitive forward calls in(4), plus seed/tag bits and address assembly.
No cost claim omits the earlier commutation/permutation checks or the
retained branch-code acquisition. General noncommuting families may fail
this word search; they are not silently declared to have a common cover.

## 3. Approximate known-code alignment has an honest finite guard

Exact global commutation need not be treated as free. For any proposed
forward words R_j and a proposed permutation word Q, define

    epsilon_j=Pr_U[P_j(R_j(U))!=Q(U)],
    epsilon_bar=(1/m)sum_j epsilon_j.                    (6)

All these are observable from KNOWN closed programs on paid uniform seeds.
Fresh uniform(U,J) tests give an ordinary finite joint-event certificate
for epsilon_bar. For example accepting at empirical mean<=epsilon/2 with
L>=12 ln(1/delta_align)/epsilon has false acceptance of epsilon_bar>epsilon
at most delta_align and rejection with epsilon_bar<=epsilon/4 at most
delta_align. This is a paid Bernoulli guard, not a source identity oracle.
Candidate search/repeated attempts require separate fresh/summable budgets;
no default replay seed supplies independence. If the domain sampler itself
has finite caps, couple to the ideal trials and charge abort separately.

Define an IDEAL virtual lift

    X*=(J,P_J^-1(Q(U))),

and similarly X'*, but do not execute either inverse. The ideal pair has
the desired full conditional law because Q is a permutation. Injectivity
of P_j implies X=X* whenever the corresponding known-code alignment test
in(6) passes. Hence the actual generator(5) satisfies

    TV(actual_joint,ideal_conditional_joint)
        <=2 epsilon_bar.                                (7)

Its two native marginals remain EXACT regardless of alignment error, since
the R_j are still known permutations. The permutation premise is therefore
essential and cannot be replaced merely by empirical equality(6).
This explicitly constructs an approximate generative experiment while
carrying its geometric error separately from source/target error.

## 4. Relation retention needs the joint law, not a transition oracle

Every proof in GUARDED_RELATION_RETENTION uses the distribution of the
prepared pairs. At acquisition it needs the full h-conditional product
joint law for the mode/collision argument; at later diagnostics it needs
native endpoint marginals and h preservation. It never needs to feed a
particular already-observed X into the preparation mechanism. Thus the
executable interface can be widened from a transition implementation
K0(X,.) to an explicit closed JOINT pair generator such as(1) or(5).
Guard timing, old equality access and actual code/preparation costs remain.

If(7) has certified epsilon_bar<=epsilon and the ACTUAL generator's old
aggregate relation guard certifies sum_i rho_i<=eta, the IDEAL full-h
collision defect for the full actual old tuple is at most

    eta+2epsilon.                                        (8)

The full tuple collision event is a single event, so the alignment error
is charged ONCE here, not r times; its actual defect is bounded by the
sum of per-source guarded defects. Mode selection then yields ONE hidden
map Phi with old tuple=Phi(h) outside native mass eta+2epsilon. The entire
post-expiry composition/diagnostic/prediction argument applies with that
larger semantic allowance. No numerical old source model or inverse is
called at any stage. As before, this is prospective; no guard is invented
for the already expired six-source history.

## 5. The remaining capability question

The meaningful obstacle is acquiring a usable FORWARD experimental cover,
not automatically a posterior transition for a given witness. These are
different computational interfaces even though they define the same
mathematical joint law. The two-branch example is a decisive counterexample
to equating them. Any broad preparation-hardness claim for the active task
must now resist competent JOINT generators, not just conditional inverters.

The known-witness RP=NP reductions remain genuine at their requested-label
interfaces. One cannot blindly replace them by average-pair lower bounds:
rare hard fibres and active choice of both inputs change the problem.
Likewise, the one-way-permutation example proves only the narrower given-
witness bound once(1) is admitted. This negative implication for that
claimed route is retained, not concealed by renaming its cost measure.

The generic word compiler may be exponential or fail; commutation,
permutation validity and native-law implementation remain material gates.
A competent same-evidence semantic/code compiler can adopt all of it;
coupling/shared-seed/group-cover ancestry must be checked before priority
or an advantage claim. No new source, current target, fixture, or observed
performance advantage is asserted. The new owned operation is the explicit
forward coupling and its guarded extension, which changes what native
experiment construction actually requires.

## 6. Direct primary ancestry checked after construction

[Goldwasser--Micali--Rivest (1988), Section 6.2.1](https://people.csail.mit.edu/rivest/pubs/GMR88.pdf)
already constructs a claw for commuting forward permutations by applying
each permutation to the same seed and reversing their order. Thus the
basic product trick is established cryptographic ancestry. The scoped
contribution investigated here is its explicit uniform joint law and
prospective semantic-guard composition, with compilation and alignment
costs retained; priority for that composition has not been established.
