# Cooperative two-A activation: local Green and carried-output theorem

1 November 2026. Solo derivation. This is mathematical mass-action theory,
not operational chemistry. No independent review or novelty clearance is claimed.
The accepted Astra pure-source and one-A catalytic theorems remain accepted at
their exact scope. The present hypothesis requires **two** A in every fast
complex and explicitly permits both unbounded inactive faces A=0 and A=1.

## Contract

Fix d>=2, m>=3, and a finite homogeneous conservative reaction graph on
composition species A,X_1,...,X_(d-1). Every complex has total degree m and
contains at least 2A. The graph contains mA and each 2A+(m-2)X_i. At every
latter complex there is a positive-rate edge increasing A. For the global
application the graph is strongly connected. All coefficients are fixed and
strictly positive. Constants below may depend on this whole finite object.

Write N=A+sum X_i and Q_N for its exact falling-factorial generator. For large
N restrict to A>=2. This set is fast-invariant. Kill at

    d(A)+u+vA,    d(A)=k_D (A)_m,

where k_D>0 is fixed and u,v range over a fixed compact nonnegative box. The
terminal event D is the actual d-channel; its physical post-clearing A is A-m.
Let R be the killed Green operator, T=R1, U=RA, and K_D its marked output
subkernel. No stationary distribution, mixing time or existing return time is
used. Q_N has a finite state space at each N.

## 1. Low-A drift of inverse powers

For every fixed j>=1 put g_j(a)=(1+a)^(-j). A bounded A jump changes g_j by
at most C_j g_j(a)/a on A>=2; the target also has A>=2. A decreasing A jump
must have at least 3 source A, because its product retains 2. Its total positive
contribution to Q_N g_j is at most

    C_j A^(2-j) N^(m-3).

When 2<=A<=eta N, some X_i>=cN. The required edge from 2A+(m-2)X_i then has
rate at least c A^2 N^(m-2), and decreases g_j by at least c_j A^(-j-1).
Other A-increasing edges help. Choose eta>0 sufficiently small (separately
for a finite list of j when necessary). Uniformly on this region,

    Q_N g_j <= -c_j N^(m-2) A g_j.                 (1)

Every source has at least 2A, so globally the absolute drift is bounded by
C_j N^(m-2) A g_j. On A>=eta N this is O(N^(m-j-1)), whereas d g_j is
bounded below by c N^(m-j). Increasing N_0 therefore yields, everywhere,

    (Q_N-d-u-vA)g_j <= -c_j N^(m-2) A g_j.        (2)

Finite-state stopped Dynkin, followed by monotone passage, proves

    R[A g_j] <= C_j N^(-(m-2)) g_j(A_initial).    (3)

This is a relative carried-input estimate; it is stronger than an unweighted
mean bound multiplied by N. It will pay for repeated activation kernels.

## 2. Physical time and an inverse-input envelope

Use h(a)=1/(a-1). The same low-A calculation gives
Q_N h<=-cN^(m-2) on A<=eta N. On the complementary region |Q_N h|<=CN^(m-2),
while d h>=cN^(m-1). Hence the killed generator of h is at most -cN^(m-2).
It follows directly, without assuming finite absorption in advance, that

    T <= C N^(-(m-2))/(A_initial-1).             (4)

Also, (Q_N-d-u-vA)g_m<=-c uniformly for large N. To see this, use (1) for
the finitely many A<m; for m<=A<=eta N use d g_m>=c and Q_N g_m<0; for
A>=eta N the possible positive drift is O(1/N) and d g_m>=c. Thus

    T <= C g_m(A_initial).                      (5)

The identical argument with g_(m-1) and forcing A gives

    U <= C g_(m-1)(A_initial).                  (6)

These estimates retain the actual input A, including inputs large relative
to the total pool. They do not replace all clearing outputs by a worst reset.

## 3. A logarithmic, not strict-power, time/occupation gap

Set delta=(m-2)/(2m), K=N^delta and L=N^(delta/2), with integer roundings.
For the unkilled fast chain starting with A<=K, stop at first A>=K. The
drift calculation for h gives mean hitting time <=C N^(-(m-2)). Before the
hit the total added killing intensity is <=C(K^m+K+1). The integrated-hazard
coupling therefore bounds killing before the hit by

    C(K^m+K+1) N^(-(m-2)) = o(1).               (7)

This is uniform over initial A<=K and the other coordinates. It also proves
that the unkilled hit occurs, rather than assuming accessibility in a limit.

Choose geometric thresholds k_j between L and K/4, separated by a factor 4.
At a first hit the bounded jump overshoot is O(m). Exit from [k_j/2,2k_j]
then requires at least c k_j bounded jumps. The stopped jump intensity is at
most C k_j^2 N^(m-2). During

    t_j=c_0/[k_j N^(m-2)],

the probability of an exit is at most 1/4, by the stopped expected jump count
and a sufficiently small fixed c_0. The killing probability is at most
C k_j^m t_j=o(1), uniformly over these thresholds. Consequently each reached
band contributes at least c N^(-(m-2)) to actual A-occupation before killing.
The band intervals, stopped at their exits, do not overlap: the next threshold
is beyond the preceding band. For initial A<=L, (7) makes their reach
probabilities at least 1-o(1). There are c log N bands. Hence

    U >= c log N N^(-(m-2))   if A_initial<=L.

Combine with (4). For initial A>L, stop at killing or first A<=L; before
that stop U_pre>=L T_pre, and the entrance lies in [L-m,L]. Strong Markov
and the preceding ratio for that actual entrance give, from EVERY active input,

    T <= [C/log(2+N)] U.                        (8)

All the occupation and time integrals end at the SAME actual killing time.
The proof works for all allowed competitors u,v; it uses no sample averages.

## 4. The actual marked output carries inverse powers

For a fixed j, g_j(A-m)<=C_(m,j) g_j(A) on A>=m. Choose M_j larger than twice
this ratio bound. At low A, (1) implies

    (Q_N-d-u-vA)(M_j g_j)+d g_j(A-m) <=0.

At A>=eta N the negative remaining multiple of d g_j is order N^(m-j),
whereas the possible positive Q_N term is order N^(m-j-1); the same inequality
therefore holds for large N. The killed Green identity yields

    K_D[g_j(A_after)] <= M_j g_j(A_initial).     (9)

This includes the actual A_after=0,1 outputs. It is not a conditional bound
after an observed output, and is not an independent redraw of A.

For j=m the marked forcing d(A)g_m(A-m) is uniformly bounded. Thus also

    K_D g_m <= C T <= C p_N,  p_N=N^(-(m-2)).    (10)

The clearing compensator bounds R(A)_m. Holder on the finite occupation
measure, using A^m<=C[(A)_m+1], gives

    U <= C T^((m-1)/m)(1+T)^(1/m)=o(1).         (11)

As a result uT+vU=o(1), uniformly, and K_D1>=1/2 for large N. Equation (10)
can be strengthened to K_D g_m<=C p_N K_D1. If an output is selected by its
pre-clearing B phase, apply this inequality at its FINAL stage entrance before
integrating over that entrance. The same relative bound survives even a rare
phase selection. Conditioning on the observed A_after instead is forbidden.

Finally d(A)<=C N^(m-1) A and K_D1>=1/2 imply

    U >= c N^(-(m-1)).                          (12)

## 5. Restoring the common B catalyst

For B>=q put s=(B)_q. Physical fast and clearing generators are s Q_N and
s d, and physical competitors are k_I and k_T AB. Dividing the entire killed
generator by s gives u=k_I/s, v=k_T B/s in a bounded box. Physical T and U
are divided by s; their ratio is unchanged. The actual output kernels in
(9)--(10) are unchanged. In particular

    P_I=k_I T_phys,
    P_T=k_T B U_phys,
    K_T g_j(A+ m-1) <= C [B/(B)_q] p_N g_j(A),
    K_I g_j(A+1) <= C [(B)_q]^-1 p_N g_j(A).    (13)

The last two follow from (3), not from multiplying a terminal probability by
a separately conditioned output moment. These are the carried-kernel bounds
needed to sum arbitrarily many extra activations in a high-phase processor.

## Scope and negative control

The source multiplicity TWO is essential to (8). For minimum multiplicity
three, the logarithmic-band occupation contributions scale as k_j^-1 and
their sum stays bounded; this proof supplies no vanishing T/U. The finite
controls show this distinction: for m=4, minimum A=2, the largest T/U falls
from 0.27869 at N=32 to 0.15398 at N=4096; for m=5, minimum A=3, it instead
approaches about 0.25 on the tested range. These finite values are controls,
not asymptotic proof or a transience result for the second family.

The governing exact CME script and all-input residuals are in
`work/mechanism_selection_20261101/cooperative_pool_controls.py` and
`cooperative_pool_controls.json`. The accepted earlier one-A theorem cannot
be invoked by subtracting one A: that operation changes the connector,
terminal seed head and physical occupation weights. Equations (1)--(13)
above are a new derivation for the stated physical generator.
