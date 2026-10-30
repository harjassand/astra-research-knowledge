# Joint composition–phase Green transport by positive forests

Status: personally derived, not yet independently reviewed. This is a transport theorem for a killed joint shell, NOT recurrence or a global forcing contraction.

## Setting and exact object
Fix a finite phase alphabet j and integer offsets h_j. Shell R has states (c,j), 0<=c<=R+h_j, representing two actual populations C=c and A=R+h_j-c. Retain exactly those physical reactions preserving R; kill at every other reaction. Rates are finite positive sums of mass-action monomials k(A)_a(C)_b. No phase is averaged, and the Green kernel is the actual occupation kernel until R first changes.

Assume the killed shell is transient. This can be certified by directed reachability of killing, not by recurrence of the full network. Let G_R=(-Q_R)^(-1).

## Finite endpoint test
Choose a fixed integer L above all A reactant orders and compare R and R+1 on the SAME core c<=M=R-L. The omitted endpoint blocks have fixed sizes, independent of R. For sufficiently large R, their positive-rate graph is fixed because C is large and A takes only finitely many fixed values.

Eliminate each endpoint block exactly. Assume:
1. each endpoint state can reach the core or killing;
2. the resulting effective off-diagonal/killing supports on the common core agree for the two shells.

These are finite graph conditions. They are not a supplied Lyapunov barrier. They must actually be checked; one may NOT infer them from weak reversibility alone. Only finitely many core boundary rows are altered by this elimination.

The endpoint Schur-complement rates are nonnegative rational functions of R, with positive forest representations. Equal nonzero support therefore implies that corresponding effective rates have ratios between C^-1 R^-d and C R^d for some finite C,d. They need not have constant ratios.

## The forest bound
Away from the finitely many altered rows, compare the same state (c,j). A increases by one, C stays fixed. For an enabled source order a,

    (A+1)_a/(A)_a = (A+1)/(A-a+1) <= 1 + D/(A-D+1),

where D bounds the A source orders; for a=0 the ratio is one. Positive sums and killing rates inherit this bound. In any rooted spanning forest, each state contributes at most ONE outgoing rate. Across the K fixed phases, the sum of the logarithms of all such ratios is O(KD log R), because A runs through a consecutive interval. Thus every corresponding forest monomial changes by at most a fixed power of R. The finitely many effective boundary rows contribute another fixed power.

The determinant of -Q and each nonzero inverse numerator have positive directed-forest expansions. Summing preserves the same monomial comparison; dividing numerator by denominator yields

    C^-1 R^-p G_R(x,y) <= G_(R+1)(x,y) <= C R^p G_R(x,y)

for x,y in the common core, whenever the entry is nonzero. Here each full Green restricted to the core equals the inverse of its exact endpoint Schur complement. The equality of effective support preserves the zero pattern as well.

Constants depend on the fixed phase alphabet, orders, rates, L and endpoint forest degrees, not on R. No mixing estimate, spectral gap, unimodality, stationary averaging or pointwise infinite-fiber comparison is used.

## Actual coupled test
For the rank-three network in FROZEN_BOUNDARY_COMPOSITION_INSTABILITY.md, use the exact tree offsets recorded in tree_residual_matrix.py, K=4,8,12. Retain only delta=0 reactions, killing all others. The program check_joint_endpoint_support.py checks the finite endpoint graphs using integer falling factorials. At L=3 (and also 4,5,8,12):
- both old and new endpoint blocks reach the core or killing;
- effective core-edge and killing supports coincide.

This is an exact finite graph certificate valid for every sufficiently large R, not a large-R numerical eigenvalue test: the endpoint graph depends on R only through positive C factors, and all those factors remain positive for R>=L+3. The saved JSON records the complete signatures. Transience of the whole neutral killed shell has a direct certificate: follow immigration repeatedly. Each such reaction is enabled; it either has nonzero residual increment (killing immediately), or advances B by one. Within at most K+1 immigrations the path therefore encounters killing. This proves transience independently of recurrence and without any mixing estimate.

## Limits and next obligation
This proves a genuinely joint, growing-fiber Green comparison beyond the earlier scalar birth–death shell. It is only polynomial. It does NOT provide 1+O(1/R) profile shifts, and a polynomial loss cannot silently be absorbed into fixed-inflation errors. It also does NOT assert entrywise comparison at low-A endpoints: enabled-edge supports can differ there. Those endpoints were eliminated exactly, not declared regular.

A possible stronger representation is majority-coordinate insertion: add the extra particle to A on C<=N/2 and to C on C>N/2. Then every matched rate changes by 1+O(1/N) across O(N) vertices, giving a constant forest cost; the unmatched finite row moves to the interior, where exact Schur-complement support AND leading-degree comparison must still be earned. This stronger construction is not yet proved here.
