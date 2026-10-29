# Complete positivity and equilibrium completion

29 October 2026, Brisbane. New complementary construction. This uses
**completely positive matrices** (nonnegative Gram factorizations), not
completely positive quantum maps. The factorization cone and Horn witness
are classical. Their use below is at a specified calibrated CTMC interface.

## 1. Exact equilibrium criterion at the hidden-clock boundary

Retain m ports and positive weights w_B, a symmetric irreducible trace
Laplacian S with off-diagonal flows F_ij=-S_ij, and equal excess loads
v_R=v_L=v>=0 of positive total V. Set c=V/Lambda for a supplied hidden
rate ceiling Lambda. Port ceilings ell_i allow spare flux

    a_i=w_i ell_i-sum_{j!=i}F_ij.

As in the independently checked clock-rigidity proof, every compatible
finite positive CTMC has only rate-Lambda hidden stars; there are no hidden-
hidden transitions. A star x of mass w_x has incoming distribution alpha_x
and outgoing distribution beta_x on ports, and contributes

    M_x=w_x alpha_x beta_x^T

to residence transport. Direct port flows are D_ij=F_ij-Lambda M_ij for
i!=j, and native return flow is Lambda M_ii.

**Theorem.** A zero-entropy compatible finite CTMC exists iff there is a
completely positive matrix M satisfying

    M1=v,
    Lambda M_ij<=F_ij for i!=j,
    Lambda M_ii<=a_i.

For a richer interface supplying M itself, simply test these constraints
and membership M in CP_m. These are exact mathematical conditions, not an
efficient acquisition or factorization algorithm claim.

**Proof.** Zero entropy forces detailed balance on every edge, so each
star has alpha_x=beta_x. Thus M=sum_x w_x alpha_x alpha_x^T is completely
positive. Conversely write M=sum_x z_x z_x^T with z_x>=0, dropping zero
columns. Set s_x=1^T z_x, w_x=s_x^2 and alpha_x=beta_x=z_x/s_x. Then
sum_x w_x=1^T M1=V; incoming and outgoing fluxes at each port-hidden edge
are Lambda w_x alpha_x. Every hidden rate is Lambda, and all are balanced.
Add symmetric direct flows F_ij-Lambda M_ij, which are nonnegative by the
constraints. They preserve S, while M preserves the equal load vector and
c=V/Lambda. The native port budgets hold. Irreducibility follows from S,
after deleting absent stars. All edges satisfy detailed balance. QED.

An ordinary PSD test is necessary but insufficient starting at five ports.
The CP/nonnegative-Gram factorization of reversible two-step kernels has
clear primary antecedents: Caputo, Chen, Gu and Polyanskiy (2024), Section
2.3 and Lemma 2.9, explicitly relate factorizable kernels to complete
positivity and exhibit the distinction from nonnegative PSD matrices.
The theorem above is a translation into the clock-rigid continuous-time
record, with its native flow and residence constraints. It must not be
presented as discovery of CP matrix geometry or reversible factorization.

## 2. A five-port obstruction forced by the original mean record

Let C be the adjacency matrix of the five-cycle and define

    M=I+(17/30)C.

Give every port weight 1 and prescribe

    F_ij=17/30 on cycle neighbors, and 0 otherwise,
    v_R=v_L=(32/15)1,
    V=c=32/3, Lambda=1,
    ell_i=32/15 for every port.

The trace departure is 17/15, so each spare native flux is a_i=1.
Clock rigidity and the constraints imply M_ii<=1, each neighboring M_ij
<=17/30 and all other off-diagonal entries zero. But their row upper sums
are 1+2(17/30)=32/15, exactly the required load. Therefore EVERY feasible
transport equals the displayed M. This conclusion needs no extra measured
M beyond the original mean record and the stated execution ceilings.

### Positive definite, entrywise nonnegative, but not completely positive

The eigenvalues of C are 2cos(2pi k/5). The smallest eigenvalue of M is

    1-(17/60)(1+sqrt(5)) > 0,

because 43>17sqrt(5). Thus M is positive definite and nonnegative.

Let H=11^T-2C, the classical Horn copositive matrix. For z>=0,

    z^T H z=(sum z_i)^2-4 sum_{cycle edges {i,j}} z_i z_j >=0.

A self-contained proof of the last inequality: normalize sum z_i=1 and
maximize the edge-product sum on the simplex. Whenever two nonadjacent
vertices carry positive mass, holding their combined mass fixed makes the
objective affine in its allocation, so move all that mass to whichever
vertex has at least the larger neighboring sum. This does not decrease
the objective and strictly reduces support. Repeat until the support is
a clique. The five-cycle has no triangle, so that support has size at most
two, and its edge product is at most 1/4. This is the standard elementary
Motzkin-Straus argument specialized to C5.

But

    <H,M>=5-10(17/30)=-2/3.

If M=sum z_x z_x^T with z_x>=0, then <H,M>=sum z_x^T H z_x>=0, a
contradiction. Thus no finite-dimensional equilibrium realization exists
under the stated ceilings, despite symmetric S, balanced loads and a
positive definite residence transport. This is an all-hidden-dimensions
certificate, not failure of a numerical factorization routine.

## 3. Exact finite-entropy realization and optimum for the five-port record

For each undirected cycle edge {i,j}, introduce two hidden stars, each of
weight 16/15. The first has incoming fractions (5/8,3/8) on (i,j), outgoing
fractions (3/8,5/8); the second swaps these. All hidden rates are 1.

The pair contributes 1/2 to each endpoint diagonal of M and 17/30 to each
off-diagonal direction on that edge. Summing over the five edges gives
exactly M above. No direct port jumps are needed. There are ten hidden
states and fifteen total states. Each port departs at 32/15, each hidden
state at 1, and every microscopic transition has its reverse.

The entropy is

    E=(16/3)log(5/3),
    sigma=E/W=(16/47)log(5/3), W=47/3.

This is the exact minimum over all compatible finite CTMCs. To prove it,
finite entropy forces equal incoming/outgoing support for each star. A
star's support must be a clique of the graph of positive entries of M:
otherwise its positive outer product would put mass at a forbidden zero.
Every C5 clique has at most two vertices. Thus each hidden star is binary
(or a single-port star), and the binary Jeffreys bound from the independent
two-port review applies to each. Total star mass is V=32/3, total diagonal
transport is trace M=5, and convexity gives

    E>=V*g(5/V)
      =(32/3)*[4*(1/4)*atanh(1/4)]
      =(16/3)log(5/3).

All constructed stars have the same return fraction 15/32 and swapped
binary distributions, so both binary and Jensen equality conditions hold.
Infinite-entropy alternatives cannot improve this finite attained minimum.

## 4. Stronger temporal principle: every finite-time equilibrium kernel is CP

Root proposed the instantaneous hidden excursion density test. Its argument
extends to every positive time and every nonnegative time bin, removing any
need to estimate a derivative at time zero for the corresponding witness.

For a stationary reversible CTMC, let A=-L_BI>=0, D=diag(w_I)>0, and
G=L_II symmetric. The interior excursion flux density is

    K(t)=A exp(-D^-1 G t) D^-1 A^T
        =A D^-1/2 exp(-H t) D^-1/2 A^T,
    H=D^-1/2 G D^-1/2.

The symmetric matrix -H is Metzler. Hence exp(-Ht/2) is entrywise
nonnegative for all t>=0. Consequently

    K(t)=B_t B_t^T,
    B_t=A D^-1/2 exp(-Ht/2)>=0.

Thus **K(t) is completely positive for every t>=0**, with no hidden rate
ceiling or clock saturation required. A nonnegative weighted integral
K_f=integral f(t)K(t)dt is also completely positive whenever finite,
because the finite-dimensional CP cone is closed and convex. In particular
every interior-duration bin has a CP flux matrix. Direct jumps are a
separate zero-duration atom and must not be mixed into this density test.

For the constructed fifteen-state model, no hidden-hidden transitions occur,
so K(t)=exp(-t)M. This is symmetric and positive definite at EVERY t, and
each scalar spectral coefficient is completely monotone. Nonetheless

    <H,integral_0^h K(t)dt>=-(2/3)(1-exp(-h))<0

for every h>0. It therefore rules out ANY finite reversible CTMC completion
of the complete native boundary event-time interface, without assuming the
hidden clock ceiling or state count. A full time-reversal-symmetric observed
law can thus fail the stronger microscopic equilibrium-completion condition.

This conclusion is scoped to resolved ports and native excursions, the
correct reversal, and their calibrated intensity weights. Arbitrary coarse
labels or an unweighted row-normalized kernel need not satisfy the displayed
Gram identity. Unknown stationary entrance weights must be acquired or
otherwise supplied; they are not provided by choosing reset ports uniformly.

### Finite-window acquisition implication, not an executed assay

For this model, native port intensities are equal: rho=32/15. Choose the
reset port i uniformly, retain the next return endpoint j and whether the
interior duration is in (0,h], and score Y=H_ij on such a return, otherwise
Y=0. Then |Y|<=1 and

    E Y=<H,K_bin>/(5rho)=-(1-exp(-h))/16.

With supplied equal calibrated entrance intensities, every compatible
equilibrium model has E Y>=0. Ordinary Hoeffding bounds therefore provide
a finite-data witness using a bounded score, without an infinite-duration
tail premise. For h=log 2 the true mean is -1/32. Timing tolerance and reset
availability remain physical/instrument premises. Censoring at h needs an
authorized reset from the resulting hidden state if one wants to terminate
the trial there; otherwise the remaining native wait is charged. No assay
has been executed by this note, and no confidence claim is made from the
exact supplied-generator calculations alone.

## 5. Scope of novelty and next obligation

The CP cone, Horn witness, Motzkin-Straus argument, reversible kernel
factorizations, binary Jeffreys inequality and convex mixture methods all
have classical antecedents. The proposed addition is their calibrated
continuous-time consequence and temporal-entrance interface: exact clock-
constrained equilibrium completion, a forced five-port obstruction with
an attained nonzero dissipation minimum, and finite-window CP witnesses
for hidden equilibrium even when observed event-time reversal and PSD
tests pass. Historical priority is not established by the targeted search.

The hardest operational obligation is acquiring the correctly weighted
native entrance/exit/time-bin record with honest uncertainty under weaker
access. The bounded finite-bin witness removes a tail-moment requirement
for this new consequence; it does not remove endpoint resolution, intensity
calibration, reset cost or timing precision. The equally informed comparator
is the same conventional copositive witness evaluated on the same acquired
bin counts, not a full hidden generator fit.
