# Scalable conditional unary Gibbs loading through a coherent open-rod gas

2026-11-03. Main construction. Independent audit has passed the exact open-rod representation, source-root normalization, displayed KP constants, and elementary parent gap. This is an IDEAL active conditional loader, not noisy physical WRITE or joint-bath loading.

## 1. Parameters and conditional target

For any fixed check weight K>=3, overlap bound D including self, set d=2^K and

 delta0=4t/K^2,
 U=delta0,
 g=delta0/(2000 D d),
 delta=delta0-2g^2/t >= delta0/2,
 J=2g^2/(tK).

A smaller positive constant g also works. Fix an allowed syndrome s and include the full unary Hilbert space in H_s. Let tau=beta/2. Require

 beta >= 2/(7delta/8) log(4000 D d^2).

This is only a thermal-through-line condition. Memory independently requires beta J>=B*, and potentially a larger beta for the host's classical syndrome sampler. Both are compatible at a fixed temperature independent of system size.

At K7,D43,t=1 the point is g=7.415757000474608e-9, J=1.571241482573947e-17. The through-line condition is beta t>=609.261; the independent memory condition is beta t>=6.3643940864e16 B*. These are rigorous existence-scale parameters, not practical hardware temperatures.

## 2. Exact vector and nilpotent source algebra

Let r be the all-reference clock vector. Vectorize exp(-tau H_s) on left and right copies of the clocks. Normalize its vacuum coefficient, not its norm:

 F|r,r> = vec(exp(-tau H_s))/<r|exp(-tau H_s)|r>.

On each clock-half, creation maps |alpha><e0| commute with all others; any product of two on the same half vanishes. F has constant coefficient1, so S=log F exists uniquely in this finite nilpotent algebra. The normalized vector exp(S)|r,r> purifies the exact conditional Gibbs state exp(-beta H_s)/Z_s.

## 3. Open trajectory gas

Resolve every clock path on [0,tau] at reference visits. Species are ordinary excursions, an initial nonreference-to-reference source, a final reference-to-nonreference source, and a through-source never visiting reference. N!=1 histories are through-sources. Retain full trajectories until spectator phases have been evaluated.

Vacuum cuts factor because the reference is rank one. Interclock phases are products of pairwise unit-modulus factors, exactly as for the previously audited closed rod gas. Same-clock overlapping rods are excluded. Each initial/final label belongs to its own doubled endpoint. Thus the coefficient polynomial is the source gas divided by the no-source gas. Its logarithm is precisely the source-containing connected-cluster expansion; this is not a positive trajectory sampler.

Absolute one-clock majorants, summed over labels, are

 ordinary: 2g^2 exp(-delta ell) du dell,
 initial or final: 2d g exp(-delta ell) dell,
 through: d^2 exp(-delta tau).

The Q-propagator bound uses the full hard-core number sectors, not an ideal occupation-sector restriction. A first/last return requires one endpoint coupling; the reference departure vector has squared norm2g^2. Dimension factors above safely dominate entrywise sums.

## 4. KP certificate and the operator creation-log bound

Use a=.1,h=1,b=delta/8,lambda=delta-b and E=exp(a+h)<4. Inflate each rod activity by exp(h), and use KP size a+b ell. Sufficient bounds are

 4D E (2g^2/lambda) <= b,
 4D E [2g^2/lambda^2+4d g/lambda]
   +4D E d^2 exp(-lambda tau) <= a.

Our g/delta<=1/(1000Dd). The three constant contributions are bounded respectively by .000042, .073143 and .004, totaling below .1. The length contribution is below .000037 delta, less than b. These deliberately conservative estimates cover both boundaries and all through-lines.

Resolve S into connected spatial hull C and nonempty endpoint-source support X subset of the doubled C. Source-rooted KP gives

 sup_i sum_(C,X:i in X) exp(|C|) |s_(C,X)|
 <= E[2dg/lambda+d^2 exp(-lambda tau)]
 <= .010143/D =: epsilonS.

Here |s| is coefficient l1 norm; it dominates operator norm. Rooting at the unique source rod carrying endpoint i is correct in the nilpotent algebra. No beta-length integration occurs at that root. Hulls include unmarked internal clocks; operators act only on X because s is a classically fixed input. This distinction is essential.

Since |X|<=2|C| and max_x x exp(-x)=1/e,

 A:=sup_i sum_(C,X:i in X) |X| |s_(C,X)|
 <=2 epsilonS/e < .0075/D.

## 5. Elementary, geometry-independent parent gap

Let q_i=I-|e0><e0| on each clock-half and S_i=sum of creation terms using i. For u in [0,1],

 B_i(u)=exp(uS)q_i exp(-uS)=q_i-uS_i,
 P(u)=sum_i B_i(u)^dagger B_i(u).

The B_i commute and are idempotent. Their common kernel is exactly exp(uS)|r,r>, so P(u) has a unique zero vector. The independently audited commutator argument gives

 P(u)^2 >= [1-2A-2A^2] P(u).

Thus its gap is greater than .9848 uniformly in u, beta and number of clocks. This proof works on arbitrary bounded-degree graphs and does not assume a geometric stability theorem or a bounded condition number for exp(S).

Proof reference: /workspace/shared/UNARY_THERMOFIELD_PARENT_GAP_AUDIT.md.

## 6. Constructive finite-hull computation

For a finite induced clock set B, pin its exterior to reference, delete exterior hopping terms, and compute exp(-tau H_(s,B)) by dense matrix arithmetic. Form F_B and S_B=log F_B in the finite creation algebra. Define the hull contribution

 Phi_C=sum_(B subset C) (-1)^(|C|-|B|) S_B.

Then S_V=sum_(C subset V) Phi_C exactly, and disconnected C have Phi_C=0. Restriction preserves a path weight exactly when its whole spatial hull remains, so Mobius cancellation selects that hull. Truncate to connected |C|<=L. Enumeration, matrix exponentiation, finite nilpotent algebra and inclusion-exclusion cost exp(O(KL)) per root, at fixed physical parameters. Independent details: /workspace/shared/UNARY_THERMOFIELD_MOBIUS_CONSTRUCTION_AUDIT.md.

The source-anchored bound gives ||S_i-S_i^(L)||<=epsilonS exp(-L). For 2m clock-halves,

 ||P(1)-P_L(1)||
 <=2m(2+2epsilonS)epsilonS exp(-L)=:Delta_L.

Both parents are positive and have their own exact unique ground vector. The full parent gap gamma>.9848 implies squared ground-state overlap loss at most Delta_L/gamma. Thus purification trace-distance error is at most 2 sqrt(Delta_L/gamma), and discarding the right copy cannot increase it. Choose L=O(log(m/epsilon^2)) and allocate half the error budget here. This avoids the invalid exp(||S||) truncation estimate.

The truncated parent still has the same uniform gap by the same coefficient-norm argument. Ideal adiabatic evolution along P_L(u) prepares its ground state. Derivative norms are O(m) at fixed parameters, giving a conservative polynomial runtime O(m^2/epsilon) after choosing a smooth schedule and assigning the remaining error budget. Digital simulation, term synthesis and routing add polynomial overhead. Arithmetic precision is allocated over the polynomially many operations; beta, K and D are fixed parameters, not hidden variables scaling with m.

## 7. What this operation supplies

If the open-representation audit passes, this is an all-volume fixed-temperature ideal conditional quantum Gibbs preparation algorithm at constant g>0, even though beta g is huge. It neither samples signed trajectories as probabilities nor assumes a quantum rapid-mixing theorem.

With a separately verified positive sampler for the ACTUAL constrained syndrome law pi_beta(s) proportional to Z_s, prepare the corresponding target syndrome/logical state, perform this conditional clock preparation, and apply the common prefix Clifford. This composes into a reference-safe ideal thermal encoding. The classical sampler must belong to the same host and include the coupled free-energy corrections; it cannot be imported from the random K7 family without checking its assumptions.

Physical resources include 2Km clock qubits during preparation, universal gates, classical enumeration and matrix arithmetic, and geometric routing. The parent path is an ACTIVE circuit resource, not the passive three-body HOLD Hamiltonian. Its very large constants and colder sufficient parameters must be compared fairly with active correction.

No fixed-local-noise output theorem follows. Fault tolerance can protect internal computation under an appropriate model, but terminal transfer to bare memory still needs a basin or Gibbs-subpreserving noisy-handoff theorem. The exact microscopic bath's correlated equilibrium is also not prepared by this isolated conditional constructor.

## Final audit implementation clarifications

Expand each quadratic S_i^dagger S_i into PAIRS of finite hull terms. Each resulting term acts on at most 2L physical clocks, and the number of pairs is polynomial. Do not synthesize B_i densely on the union of all its hulls, which can contain polynomially many sites.

Finite precision must account for matrix exponential scale exp(O(beta L ||h||)) and cancellation in both Mobius subtraction and the nilpotent logarithm. Working precision polynomial in L, beta, and log(1/epsilon) suffices at fixed beta,K,D, and all errors are allocated across the polynomial operation count. Consequently the construction is polynomial in system size and target accuracy, not asserted uniformly polynomial in K or beta.

## Explicit asymptotic cost summary

With L=O(log(m/epsilon^2)), a conservative classical finite-hull and coefficient synthesis cost is m exp[O((K+log(D+1))L)], times polynomial factors in L,beta and precision. Expanding parent quadratic terms squares the dictionary size but preserves polynomial scaling. Dense term synthesis acts on at most 2KL physical qubits. A basic product-formula digital implementation of the gapped parent path and polynomial-overhead routing therefore remains polynomial in m and 1/epsilon at fixed K,D,beta. Peak gate strengths can be bounded by allowing longer gate time. This is not constant depth, not passive loading, and not a claim of practical constants. Hold needs Km clock qubits; preparation temporarily uses 2Km plus data and computing ancillas.
