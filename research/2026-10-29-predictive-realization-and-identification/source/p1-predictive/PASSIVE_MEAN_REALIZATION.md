# A small positive realization of the complete mean record

29 October 2026, Brisbane. Root's construction after the acquired boundary
record, with a sharper lower bound from the independent boundary challenge.
This is a finite reversible Markov realization, not just an evaluation
formula. Context, calibration and acquisition costs remain explicit.

## Theorem: at most one added state per retained port

Let a finite reversible module have retained ports B, |B|=m, hidden interior
I, positive mass vector w and conductance Laplacian L. Every interior
component touches B. Internal module connectivity is otherwise unnecessary;
the external assembly may connect several internal components. Let

    S=L_BB-L_BI L_II^{-1}L_IB,
    b=w_B-L_BI L_II^{-1}w_I,
    c=w_I^T L_II^{-1}w_I,
    v=b-w_B, V=sum v.

Then v>=0 and V=sum_I w_i. If I is nonempty, V,c>0. Define gamma=V/c.
Construct a new network as follows:

1. Keep the same labelled port states with the same masses w_B.
2. Put direct conductance -S_ij between each pair i!=j of ports.
3. For every i with v_i>0, add one private leaf of mass v_i attached only
   to port i by conductance gamma*v_i.

Every mass and conductance is positive when present. Rates are conductance
divided by the departure-state mass. Every added leaf has exit rate gamma.
The reduced module has at most 2m states and its record is exactly

    (S_tilde,b_tilde,c_tilde,w_tilde_B)=(S,b,c,w_B).             (1)

Proof. A pendant edge eliminates with zero Schur contribution. Its entire
mass v_i is transferred to the boundary load at i, and its contribution
to c is v_i^2/(gamma v_i)=v_i/gamma. Summing gives V/gamma=c. The port
network already has Laplacian S. If I is empty, V=c=0 and the original
port network itself is the realization. A proposed record with V=0,c>0
or V>0,c=0 is not a finite positive source record and is not covered.

## Consequences, not an unidentified original process

The new source preserves exactly:

- Every boundary-started mean time to a nonempty absorbing boundary set.
- Every equilibrium-conditioned mean to such a set.
- Every equilibrium-source mean after a conductance-calibrated passive
  exterior is attached at the ports, including additional weighted nodes.
- The same mean family for fixed native port killing hazards, because the
  port masses are retained and a hazard kappa adds diag(w_B*kappa).
- All means for absorbing unions of whole modules when this construction
  is performed separately within each module and all cross-module edges
  retain their endpoints. Each module uses its own gamma_j=V_j/c_j.

The first assertion follows from S_RR h_R=b_R. The others follow from
complete-record composition and (1). Initial equilibrium is the invariant
mass law of the complete assembly, conditioned outside the chosen target.
This is not a statement for arbitrary hidden-state initial distributions.

More generally, for disjoint nonempty source and target unions C,A of
whole modules, let h_ports=K_A^{-1}b_live. Then

    E_{w(.|C)} tau_A = [sum_{j in C} c_j +
                         sum_{j in C} b_j^T h_{B_j}] / sum_{j in C} mu_j.

This follows by weighting each module's eliminated Poisson equation.
Therefore the realization preserves means BETWEEN specified macroscopic
regions, including arbitrary mixtures of within-module equilibrium laws.
The statistical certificate for this bilinear expression requires an
additional positive-order argument; quadratic Loewner order alone is not
sufficient. The separate between-region consumer supplies that argument.

The original port holding rates generally change. The construction does
not preserve its path law, all return-time distributions, finite-time
survival, arbitrary time-dependent controls, or operations on removed
states. A fixed native port hazard is covered because it adds a known
term in the retained mass metric; it does not require preservation of
the original departure-hold law.

The replacement's dynamic response is

    K_tilde(z)=S+z diag(w_B)+[z gamma/(gamma+z)] diag(v).

It has K_tilde'(0)1=b and -1^T K_tilde''(0)1/2=c, while generally
disagreeing with the true K(z). One shared leaf time scale per module
suffices for this mean family. No single-scale premise on the original
eliminated dynamics is made.

## The 2m state bound is worst-case sharp

Here the interface includes labelled ports and their masses w_B. Write
G=L_II and J=-L_IB>=0 in any positive reversible realization, and set

    C=J^T G^{-1}J.

This Gram matrix has rank at most |I|. Since
v=J^T G^{-1}w_I and c=w_I^T G^{-1}w_I, Cauchy--Schwarz gives

    C_ii >= v_i^2/c.

For i!=j, G^{-1} is nonnegative and the direct conductances are nonnegative,
so 0<=C_ij<=-S_ij. Therefore, if

    v_i^2/c > sum_{j!=i}(-S_ij)   for every port i,

C is strictly diagonally dominant and nonsingular. Every such realization
must contain at least m hidden states.

For m>=2 choose w_B=1, v=1, c=m, and let S be the complete graph with
each edge conductance epsilon=1/[2m(m-1)]. Its off-diagonal row mass is
1/(2m), while v_i^2/c=1/m. The pendant construction above realizes this
connected record with exactly 2m states, and the rank argument proves
that no smaller positive reversible realization with this interface can
do so. For m=1, positive c requires at least one hidden state, giving
the same sharp total bound 2. The boundary challenge supplied this sharper
Gram-rank argument after root's initial star-support lower bound.

This is not a lower bound for a signed/non-Markov algebraic data structure,
an interface omitting w_B, or a task asking fewer questions. It is an exact
worst-case realization theorem for the stated positive reversible class.

## Acquired realization and full costs

The exact quantities are not assumed free. Native excursion data acquire
intervals for s, departure holding times, first interior duration moments
and squared interior durations. They determine w_B,S,v,c in one arbitrary
scale. A positive proposal can use midpoint conductances, midpoint masses
and midpoint residence terms, then apply the construction. Original-source
guarantees come from the whole confidence set, not from declaring that
proposal to be the identified source.

For modular composition retain each c_j, acquired by summing squared-time
contributions over that module's ports under the separator warranty.
Removing an absorbed module removes its population and residence term.

Preparation of the finite model takes O(m^2) arithmetic operations after
the record exists; coefficient bit complexity remains a separate bill.
Its direct port graph may be dense. A conventional O(m^3) positive solve
of the Schur record is usually cheaper than simulating the replacement.

A large c gives a small gamma. Few states do not imply bounded rate range,
short acquisition, cheap precision, or fast simulation of native waiting
events. This is a mathematical/executable surrogate, not a new physical
rate-control operation. An exponentially large resolved boundary remains
exponentially large; its discovery and further compression are separate.

The addition is a positive finite representative of an entire consequence
equivalence class, a sharp state-size bound and a native acquisition route.
State elimination, Kron reduction, exact milestoning and positive moment
realization are established families. Strong conventional consumers can
adopt this construction. Historical priority and a speed advantage are
not established by the theorem or its finite controls.
