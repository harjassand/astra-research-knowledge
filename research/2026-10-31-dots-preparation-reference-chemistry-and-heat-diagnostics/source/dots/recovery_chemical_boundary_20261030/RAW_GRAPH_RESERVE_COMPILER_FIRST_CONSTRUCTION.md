# First broader construction: acquire a reserve from a raw conversion graph

30 October 2026. Exploratory construction after the dormant closure candidate. This is not another claimed recurrence family and not a novelty claim for Poisson equations or phase-type hitting times.

## 1. Input and an actual polynomial-size compiler

Input a finite strongly connected conversion graph on types X_1,...,X_k with rational positive edge rates q_ij and nonnegative birth rates b_ij, at least one positive. Reactions are `X_i+D -> X_j+D` and `X_i+D -> X_i+X_j`. Let Q be the conversion generator and b_i=sum_j b_ij. In the common operational clock of D, this is a linear conversion/birth module. Births consume one D but add a type molecule; no event in this module decreases R=sum X_i.

Compute the stationary row vector pi of Q, beta=pi b>0, and solve the finite Poisson equation

`Q h = beta 1-b`, `pi h=0`.

Shift h so min h_i=0. Set H=max h_i, M=max_i sum_j q_ij(h_j-h_i)^2. For a desired integer s>=1 define

`c_b=s/(5/2)^(s+1)`,
`C_s=s(s+1)/2 * (4/3)^(s+2)`,
`epsilon=min(1/2, 1/(2H), c_b/(2s), s beta/(C_s M))`,

omitting fractions with zero denominator. Output v_i=1+epsilon h_i, S=v·X, and h_s=(1+S)^-s. This is an explicit rational computation: two finite linear solves and fixed rational arithmetic, not an assumed Lyapunov vector or an optimizer searching the infinite population space. Dense arithmetic uses O(k^3) operations; conditioning and certificate bit lengths remain part of its actual cost.

## 2. Finite-count proof

Write z=1+S>=1+R and 1<=v_i<=3/2. A birth increases S by v_j>=1, and its finite-difference h_s decrement is at least `c_b h_s/z`. A conversion changes S by epsilon(h_j-h_i). Taylor's theorem with the actual positive finite-jump denominator gives remainder at most `C_s epsilon^2(h_j-h_i)^2 h_s/z^2`.

Summing conversion first-order terms and births gives

`L h_s <= d h_s/z [-s epsilon beta R + (s epsilon-c_b) sum_i b_i X_i] + C_s epsilon^2 M d R h_s/z^2`.

By the explicit epsilon choice, the b_i term is nonpositive and the remainder is at most half of the first negative term. Since R/z>=1/(5/2) for R>=1,

`L h_s <= -(s epsilon beta/5) d h_s`.

This holds at EVERY finite nonzero population, not only in a fluid limit. A transition that exhausts D is retained with its actual larger S; no extinction of R occurs. Additional D+D -> X_j+D channels only improve this inverse-reserve drift.

The calculation recovers the kind of hidden reserve that was manually supplied by A+eta C in the completed local work. Its ingredients are ordinary finite-state Poisson equations and finite-difference estimates; a standard informed branching-process method may reproduce it. It is capital for acquiring a boundary interface, not itself the scientific endpoint.

## 3. Decisive failure of a naïve transfer to the distinguished-A clock

The compiled reserve controls total type population, NOT how quickly the distinguished clearing species A appears.

Take the directed conversion cycle C->E->A->C, births only from A, initial residual A=E=0,C=M,D=1. Before the first residual A is made, D remains one, no birth occurs, and neither the 2A clearing nor 2A seed clock is enabled. Each initial C molecule independently takes an Erlang(2,1) time to first reach A. Therefore

`P(tau_first_A>t)=[exp(-t)(1+t)]^M`,
`E tau_first_A = integral_0^infinity exp(-Mt)(1+t)^M dt`,
`E tau_first_A ~ sqrt(pi/(2M))`.

This exact first-arrival law already rules out a uniform O(1/M) clearing-time bound. The common physical seed factor is constant before first A, so physical restoration does not erase the obstruction. Adding the D+D reverse-seed channel does not help this initial face because D=1 makes its propensity zero.

Thus simply replacing the manually chosen reserve by the compiled vector in the existing x^3+nD resolvent is INVALID. A correct acquisition theory must discover path-dependent arrival scales, rather than silently retaining the old direct-source clock.

## 4. The next concrete object

For an arbitrary raw conversion graph, shortest paths to A give computable exponents ell_i and constants c_i with `P_i(X_t=A)>=c_i t^ell_i` for small t. The actual incoming composition then supplies a finite arrival polynomial `sum_i X_i c_i t^ell_i`. Independent-particle occupancy bounds can acquire a first-arrival/hitting profile from that polynomial without enumerating the whole count state space.

These phase-type and binomial tools are ordinary comparators. The open inventive step is to combine their acquired arrival profile with the EXISTING occupation-relative feedback and phase-weighted source law, so that nonlinear clearing and dormant return use the same earned clock. If that cannot be done without supplying the missing return kernel as an assumption, this opening should be rejected rather than advertised as a general barrier compiler.

A second boundary is already visible: births from types other than A can exhaust D before A appears with nonvanishing probability. The scalar small-return premise then fails again; a larger coupled face operator would be required. No general recurrence claim follows from the reserve compiler.
