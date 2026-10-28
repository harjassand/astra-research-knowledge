# Robust window regeneration with causal quantum detectors

29 October 2026, Australia/Brisbane. Authored extension by compact_memory.
Independent review is separate. Builds on OUTPUT_PORT_REGENERATION.md and
the accepted predecessor first-mean/contact machinery at their stated scope.

## 1. Goal, physical scope and statement

Exact full swaps are not needed for a polylogarithmic finite-memory
representation when a finite-mean invariant region is available. Work with
one retained canonical oscillator a and a finite sequence of fresh modes
b_j. Fresh b_j have fixed thermal means n_j<=nbar, are independent of the
whole incoming state and one another, and can equivalently be supplied as
a finite product before the window with access delayed until their contact.
Thermal means may differ with j but are not selected from a quantum record
inside the window. Such a selection would require its own construction.

Each prescribed passive contact couples only a to its own b_j. At the end
its retained amplitude is c_j, with |c_j|<=cbar<1. Scalar waveforms and any
passive phases are supplied and fixed independently of incoming records.
During the contact, source-controlled bounded Weyl vertices have total
variation action <=alpha and one-particle displacement norm <=b. Full sines
and cosines in either canonical quadrature are examples. No nonlinearity
is linearized. Source/data/controller operations act on neither a nor the
currently interacting b_j nor future fresh modes. After departure b_j may
undergo arbitrary common complete causal detection or joint processing
with past departed modes and source/controller, with actual records used
for source feedback. It cannot return to the passive network. Its quantum
state may remain as detector memory; that extra memory is not compacted.

Assume the exact complete dynamics has a uniform boundary contract
Tr[N_a rho]<=E. The accepted first-row construction supplies such a
contract, for example P=sqrt(E),

    sqrt(cbar^2 P^2+nbar)+alpha*b <= P.                 (1)

Common complete operations on departed modes preserve the unconditional
mean of a. Normalized rare conditional branches need not obey (1).

For an L-contact window ending at any cut, define

    delta_L=asin(cbar^L)*sqrt((2*nbar+1)*E+nbar),
    T_window(d,L)=delta_L+T_d(alpha*L,b,nbar),           (2)

where T_d is any of the explicit certificates in
OUTPUT_PORT_REGENERATION.md. The actual retained output has tail amplitude
at most min(1,T_window). Consequently its complete CPTP compression costs
at most T_window+T_window^2 in half trace distance.

Any strict passive contraction cbar<1 is sufficient for the asymptotic
construction. There is NO condition cbar*exp(alpha)<1: such a condition
would result from a needlessly termwise comparison and is removed below.

## 2. Why arbitrary causal departed-mode detectors are permitted

Fix the final output a at the end T of the window. At an intermediate time
t let r_t be this mode pulled backward through only the future prescribed
passive network. The support of r_t lies in the currently retained a, the
current active fresh mode, and future fresh modes. It has zero support on
every mode that departed before t. This follows directly from the absence
of return: the later passive network is identity on every departed mode.

Let U_B(t) be the passive prefix, and r=U_B(t)^dagger r_t U_B(t), which is
the fixed initial-coordinate mode U_B(T)^dagger a U_B(T). Any physical
control/detector operation at t acts only on source/controller and already
departed modes. It commutes with r_t and r_t^dagger. Its pullback by U_B(t)
therefore commutes with r and r^dagger.

These operations may be arbitrary and non-Gaussian. They need not commute
with the other original bosonic modes, and treating them as source-only
relative to every original window mode would be incorrect. What is true,
and sufficient, is that they act in the COMMUTANT OF THE FINAL OUTPUT
ALGEBRA. Complete instrument dilations, including actual records, obey the
same commutation statement. Additional dilation ancillas can be placed in
the rest factor at the outset; no output-mode operation is needed to
complete their isometries to unitaries.

In this passive interaction picture, each nonlinear Weyl vertex factors
into an output displacement D_r(beta) and an operator on the orthogonal
rest factor. The output amplitude obeys |beta|<=b because passive mixing
preserves the full one-particle norm. Its source coefficient also belongs
to the rest factor. Absorb the complete causal detector/control dynamics
in a second rest-only interaction picture. This changes the rest operator
in each vertex, possibly making it highly non-Gaussian, but preserves its
operator norm and leaves D_r(beta) unchanged. Therefore the output-algebra
lemma applies with total window action A<=alpha*L.

## 3. The initial output-coordinate marginal

At the beginning of a window the exact retained state rho_a may be arbitrary
and correlated with source/reference/old detector memory, subject only to
Tr[N_a rho_a]<=E. The fresh inputs are independent of that whole state. The
backward passive output mode has the form

    r=xi*a + sum_j eta_j*b_j,
    |xi|=product_j |c_j|<=cbar^L,
    |xi|^2+sum_j |eta_j|^2=1.                           (3)

The normalized fresh combination b_eff=(sum_j eta_j*b_j)/sqrt(1-|xi|^2)
has thermal marginal with mean

    n_eff=sum_j |eta_j|^2*n_j/(1-|xi|^2)<=nbar.          (4)

It can be correlated with other orthogonal combinations of the fresh
modes when their temperatures differ. No independence from those rest
modes is assumed. It IS independent of the original a/source state,
because the entire fresh product was independent. Its thermal marginal
follows either from the product Gaussian characteristic function or direct
passive covariance transformation. Thus the marginal of r is precisely
a thermal attenuator of rho_a with retained amplitude |xi|.

## 4. Global comparison vector: avoiding an exponential loss

Choose a purification of the complete input. Rotate the fresh modes to
include b_eff, and remove the harmless phase of xi by a phase rotation of
a, which preserves its mean. The final passive network has the same first
row as a beam splitter of angle theta=arccos|xi| on a,b_eff. Its remaining
rows differ only by a passive unitary acting on the retired/rest factor.
Consequently it suffices to compare this beam splitter with theta=pi/2.

For J=i(b_eff^dagger*a-a^dagger*b_eff), fresh-product independence and the
thermal marginal give the exact quadratic-form identity

    ||J psi_in||^2=(2*n_eff+1)*Tr[N_a rho_a]+n_eff.      (5)

The inaccessible thermal purifier and other fresh modes may remain in the
reference. Correlations between b_eff and these modes do not change (5).
The original a remains independent of the entire fresh state. No second
moment of N_a is required. The accepted predecessor generator-row proof
justifies this identity and passive Duhamel on its graph domain; here the
passive generator is constant and commutes with its own unitary group.

The global purified-vector difference between the actual passive state and
the full-swap comparator is therefore at most

    |theta-pi/2|*sqrt((2*n_eff+1)*E+n_eff)<=delta_L.      (6)

In the final-output-coordinate factorization, the comparator has thermal
output marginal tau_(n_eff), while its rest state may be correlated with
that output. Equation (6) is a statement about GLOBAL vectors, not merely
trace distance between marginal states. The comparator is a mathematical
state used in this proof; no physical preparation or fresh-product promise
for that comparator is claimed.

Here the order of the coordinate transformations matters. Write the exact
full evolution as U=U_B(T) U_I, including all complete control dilations in
U_I. Let U_hatB denote the mathematical passive full-swap comparator used
in (6). In final-output coordinates define

    V=U_B(T) U_I U_B(T)^dagger.

The actual output is V U_B(T)psi=U_B(T)U_I psi; the comparison output is
V U_hatB psi. Apply this SAME V, with all actual controls and record
dilations, to the two passive-output vectors. It is an isometry, so their
vector distance remains at most delta_L. The output-algebra lemma applies
to V with the physical final-mode projector Q_a, and requires only the
thermal a marginal of U_hatB psi, not a product with the rest. Therefore
the comparator's final tail is bounded by T_d(alpha*L,b,nbar). Projection
and triangle inequality prove (2). Equivalently one may compare psi with
U_B(T)^dagger U_hatB psi in the original frame and use Q_r U_I. Applying
bare U_I to both passive-output vectors would be an ordering mistake.

This explicit conjugation was required by the actual independent
fault_locality review; it makes the intended coordinate identification
unambiguous without changing the bound or certificate code.

One could instead compare every Dyson word separately, obtaining the
unnecessary factor exp(alpha*L)*delta_L. Applying the complete common
propagator first removes that artifact. This is a useful representation
correction, not evidence for a physical alpha-dependent mixing threshold.

## 5. Beginning the computation and complete process composition

For cuts j>=L, (2) applies to the last L actual contacts, using the exact
boundary mean at their beginning. For the first j<L contacts, suppose the
initial memory marginal is thermal with mean <=nbar, including vacuum,
and independent of future fresh inputs. It may be correlated with the
source. The backward passive output marginal is then thermal, since it is
a normalized linear combination of independent thermal marginals. Applying
the output-algebra lemma directly gives T_d(alpha*j,b,nbar), bounded by
the same larger-action certificate T_d(alpha*L,b,nbar). Thus (2) is a
uniform bound at EVERY contact cut under this supplied initial contract.

For an arbitrary finite-mean initial state, the after-L-contacts statement
still holds. The first L-1 cuts require their own initial-state tail
allowance, or no compression until the first certified boundary. Neither
an arbitrary unknown initial state nor its finite representation is free.

Let E_j be exact contact/instrument maps and F_j=C_d o E_j, with C_d the
complete CPTP compression from the companion proof. Use the telescoping
identity with EXACT PREFIXES and compressed suffixes:

    E_J...E_1-F_J...F_1
      =sum_j F_J...F_(j+1) (E_j-F_j) E_(j-1)...E_1.      (7)

Every local difference is evaluated on the actual exact history, so the
window proof never needs to contain the artificial C_d maps. Later common
F maps are contractive. It follows that

    d_final <= min(1,J*(T_window+T_window^2)).            (8)

This includes arbitrary retained source/reference states, complete actual
records, common causal detector memory and downstream common readout. It
does not approximate normalized rare branches or assert that a detector's
own noise/uncertainty is small. Nor does it bound the total dimension of
the rest factor. No artificial compression is physically implemented.

## 6. Scaling and a declared numerical family

At fixed cbar<1,E,nbar, choose L=O(log(J/epsilon)) so delta_L is at most a
chosen part of epsilon/J. Then A=alpha*L=O(log(J/epsilon)). Taking
K=O(A+log(J/epsilon))=O(log(J/epsilon)) suffices for the exponential-series
remainder. At fixed valid Chernoff point z, a cutoff

    d=O(b^2 log^2(J/epsilon)+log(J/epsilon))              (9)

suffices. Thus the persistent bosonic interface has dimension polynomial
in the logarithm of the workload and inverse representation tolerance.
The estimate is not a physical minimum or an optimal exponent.

The executable uses alpha=1/100, b^2=21/10, nbar=1/10000, cbar=1/10,
P=sqrt(E)=1/40, and the rational row bound Lbar=29/2000. It independently
checks (P-Lbar)^2>=cbar^2*P^2+nbar and Lbar^2>=alpha^2*b^2. These are the
same sufficient invariant-region values as the reviewed predecessor,
reused at their actual scope. There are zero sampling shots and no new
physical interface acquisition. The code records its dimension, Dyson
order and lookback choices, exact directed upper bounds and complete
compression allowances separately from any solver or physical noise.

## 7. Boundaries

Direct coherent return of a departed mode, record-controlled passive
mixing, an operation on the current memory outside the admitted Weyl
vertices, and correlations among the claimed fresh inputs can invalidate
specific premises. They require a new construction. Finite-mean inputs
alone do not give an immediate rapidly decaying tail after a nonzero
remnant, as the coherent-state counterexample in the companion proof shows.
The lookback uses actual causal structure and fresh inputs to supply the
missing information; it is not a generic theorem for all stable means.

All conclusions are mathematical representation guarantees conditional on
the stated interface. Compactness alone does not solve a large quantum
source or detector process, prove a computing advantage, or pay for
calibration, supply, delivery, measurement, reset or fault-tolerant reuse.
