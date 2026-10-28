# A spin-one source with internal imaginary-time structure

This continuation changes the boundary function itself. It does not enlarge
the old fugacity grid, assume a higher even moment, or omit a transfer mode.
The source identities below are mathematical; their computed thermal values
are numerical previews, not certified eigenvalue enclosures.

## 1. Definition, domain and parity

Use the accepted unit-circle history representation, J=K_beta/5, A=-J and
G_a=iS_a. A k-event history carries its beta^(k/2) word weight. All inserted
operators are time ordered inside the same one-spin trace as that history.
For 0<delta<1 define the z component

    g_delta(x)=-integral_0^1 sum_bc epsilon_zbc
                 Tr[T G_b(t+delta) G_c(t) word_beta(x)] dt,

where t+delta is modulo one. This is the global time average P0 of a two-spin
insertion source; it has zero TOTAL time frequency but nontrivial internal
relative time. The epsilon tensor couples the two vector insertions to spin1.
It transforms as an SO(3) vector and is real in the real spin-two basis used
by the history construction. It is not a mixture of higher spin lists.

The circle action is unitary and commutes with J. Interchanging b,c and
shifting the common insertion time gives exactly

    g_delta=-g_(1-delta),       g_(1/2)=0.

Thus a symmetric relative-time weight, including a constant weight, gives
the zero spin1 source. An odd kernel or a separation unequal to a half-period
is required. This does not remove nonzero-frequency modes from the transfer
trace: it only specifies the trial source.

Since [G_b,G_c]=-sum_a epsilon_bca G_a,

    -sum_bc epsilon_abc G_b G_c=G_a.

The one-sided limit g_(0+) is therefore the accepted single-insertion P0 f.
The opposite limit has the opposite sign. Relative-time reversal must not be
mistaken for evenness of this source.

For a fixed component, |g_delta(x)|<=40(2 sqrt(beta))^k. The history simplex
and three event labels give ||g_delta||^2<=1600 exp(12 beta). Hence these are
actual Hilbert-space trial functions for every finite beta. No finite history
length, event-time or photon-like state cutoff has been introduced.

## 2. Exact physical contraction

In the physical spin basis the insertion equals i B_delta, where

    B_delta=[S+(delta) S-(0)-S-(delta) S+(0)]/2,
    B_(0+)=Sz.

The displayed products are time-ordered insertion instructions; they are not
assumed Hermitian at finite separation. The i factors must be retained.
Using P0^2=P0 and [P0,J]=0 leaves only ONE relative-center integral in a form
with two projected boundary sources. For p>=0 the physical system is the
open p+2-site chain with dimensionless Hamiltonian H_eff=beta sum h_edge:

    <g_deltaL,A^p g_deltaR>
      =(-1)^(p+1)/5^p integral_0^1
          Tr[T B_deltaL(left at 0) B_deltaR(right at tau) e^(-H_eff)] d tau.

An original single source means B=Sz with no internal pair. A mixed source
requires three operator insertions; two bilocals require four. The minus sign
is i^2; (-1)^p is A=-J. There is no Gibbs normalization, extra beta factor,
free frequency degeneracy, or additional boundary factor of five.

The accepted open-chain history contraction extends by inserting the fixed
finite operators before summing bond histories. Operator norm bounds and the
absolutely convergent history expansion justify exchanging the time integrals
and bond sums. For a legacy endpoint fugacity r, the end bond is beta*r
(the p0 two-site bond is beta*r*s). This is the same old source interface;
the internal-time insertion changes only the boundary observable instructions.

The numerical contraction follows every chronological word literally. For
given tau, sort all insertion times, propagate with exp(-gap*H_eff), and
multiply the corresponding Sz or S+/- matrix between full eigenspaces.
All signed magnetization blocks are included. Although a bilocal's net
magnetization change is zero, its intermediate state belongs to M+1 or M-1;
those cross-block contributions cannot be omitted.

For two finite separations, ordering can change at

    0, 1, deltaL, 1-deltaR, (deltaL-deltaR) mod 1.

Splitting at those points gives smooth finite integrands. Gauss degrees
8/16 and a degree32 replay were used as numerical convergence diagnostics.
They are not rigorous quadrature intervals.

## 3. A finite contact-jet operation

The one-sided derivative g1=d g_delta/d delta at 0+ also exists in the
history Hilbert space. For a fixed history the only first-order changes are
arcs crossing one event. The exact spin identity is

    -sum_bc epsilon_abc G_b G_d G_c
        ={G_a,G_d}+6 delta_ad I.

Subtracting the original coincident insertion gives the event replacement
G_a G_d+6 delta_ad I inside the circularly ordered remaining word. Summing
this replacement over every history event gives g1. In particular the new
function depends on event cuts, not merely on adding another fugacity value.
Its bound is

    |g1(x)|<=25 k (2 sqrt(beta))^k,
    ||g1||^2<=625[12 beta+(12 beta)^2]exp(12 beta).

The difference quotients have the same k-weighted dominating bound. Their
pointwise limit and dominated convergence prove Hilbert differentiability.
Eight literal histories test the circular ordering, global translation,
relative-time sign and contact derivative independently of a physical trace.

For endpoint L and its neighbor define the Hermitian observable

    D_L=6 beta Sz_neighbor-{Sz_L,beta h_L,neighbor}/2.

Direct spin algebra gives

    sum_bc epsilon_zbc [H_eff,Sb_L] Sc_L
        =i D_L+[H_eff,i Sz_L]/2.

In a projected form the total-time commutator integrates to zero when it
commutes through the other endpoint insertions. Hence mixed jet/original
forms use -C_H(Sz_L,D_R), and jet/jet forms on at least three sites use
-C_H(D_L,D_R), with the same (-1)^p/5^p transfer factor as above. C_H is the
UNNORMALIZED unit-time Kubo correlation of the accepted source interface.
The first bounded trial used A g1, making every jet/jet form have at least
four sites and avoiding the shared-edge contact altogether.

## 4. The shared dimer contact cannot be discarded

On two sites D_L contains operators on R. Integrating by parts across the
other collapsed pair now has a nonzero ordering jump. The exact squared norm is

    ||g1||^2=-C_H(D_L,D_R)+Tr[K exp(-beta h)],
    K=beta[36 I-6((Sz_L)^2+(Sz_R)^2)
                    +{Sz_L,{Sz_R,h}}/4].

One way to derive the jump is to differentiate a right bilocal in a form
with a general insertion X. Besides C_H(X,iD_R), the integrated contact is

    Tr exp(-H)[sum_bc epsilon_zbc Sb_R X Sc_R-{X,iSz_R}/2].

For X=iD_L this is Tr(K exp(-H)). Operators at a separated endpoint commute
with every Sb_R and the term vanishes; on the shared dimer it reduces to the
symmetric K displayed above. Sympy verifies the exact Q(sqrt6) matrix
identities, including Tr K=400 beta. No eigensolver enters that algebra.

At beta3, the numerical dimer values are

    -C(D_L,D_R)=-1.4693060167644472e9,
    Tr(K exp(-3h))=5.106013092101896e9,
    ||g1||^2=3.636707075337449e9.

Ignoring the contact would give a negative purported norm. Direct finite
bilocal difference quotients converge to the corrected formula (relative
errors .01061,.00532,.00266 at delta=.002,.001,.0005). The formula, not those
finite checks, supplies the contact identity.

## 5. Validation and precision cost

The jet reduces to the available two-point validated Kubo operation plus a
small contact observable. At beta3, ||D||<=24 beta=72 and ||K||<=108 beta=324.
Its generic two-jet error prefactor can therefore be 1296 times the ordinary
Sz/Sz prefactor before source normalization. These costs are not free.

Finite bilocals instead need validated three/four-point traces and certified
piecewise integration. Their primitive insertion norm products are at most
12 and 36, respectively, using ||S+/-||=sqrt6 and the absolute coefficient
sums. The existing two-point blockwise certificate does not automatically
certify cross-M ladder chains or quadrature. No such larger certification
was launched, because the complete numerical preview remains far from the
required ratio precision.

All source/Ritz quantities here remain proposals. The full spin-list sixth
moments and every other rotation/time-frequency sector remain in the same
tail accounting as before. Neither this construction nor its bounded
failure proves a general restriction on all internal-time sources.
