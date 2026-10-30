# CP cavities give a volume-free local-fault expansion for centered HP noise
30 October 2026. New working construction; independent review pending. This is a finite scheduled-circuit noise-interface theorem, not a new universal fault-tolerance theorem or a claim of historical novelty.

## 1. Exact input contract
Let S be finitely many bounded-dimensional system sites, with an arbitrary retained finite-dimensional bath B. Intended gates form a fixed finite schedule. At any time their active supports are disjoint blocks, each of at most g sites; include idle blocks as locations. Each location lasts at most tau. Its intended time-local generator is a CPTP generator acting only on that block. Instantaneous intended CPTP gates at the partition boundaries can also be inserted. Adaptive scheduling is not silently included.

The actual time-local generator is

 L(t)=L_id(t)+L_B,raw(t)+sum_e N_e(t).

The complete generator produces CPTP propagators on every time interval. Each N_e is centered (trace-annihilating), Hermiticity-preserving, and acts on at most q system sites and the bath. It need NOT generate CP dynamics on its own. Its completely bounded trace norm is at most eta_e(t), with incident bound sum_(e contains i) eta_e(t)<=eta for every system site. The raw bath generator need not be CP separately. Finite-dimensional bounded piecewise-continuous coefficients suffice below. Infinite bath extensions require the corresponding bounded-normal generator/dilation/limit hypotheses and are not asserted here.

All norms below are complete trace norms, and every estimate is uniform over the initial bath state, system-bath correlations, and retained references. No positive fault trajectory is assumed.

## 2. Actual CP cavities, without deleting HP terms
For a selected set R of active gate blocks, let E_R embed the maximally mixed state on their union and let Tr_R trace that union out. For a superoperator A define

 P_R(A)=Id_R tensor [Tr_R A E_R].

For disjoint blocks j, the superoperator projections P_j commute, are idempotent, have norm at most one on completely bounded trace maps, and P_R=product_(j in R)P_j. These are projections of GENERATORS, not physical resets applied to the input state.

Define the cavity generator

 L^R=L_id+P_R(L-L_id).

It is CPTP. Indeed Tr_R L E_R is a legitimate generator on the complement: the CPTP short-step maps Tr_R exp(hL) E_R equal I+h Tr_R L E_R+O(h²), whose product limit is its semigroup. The reduced intended gates on R vanish under the trace, while those on the complement are unchanged. Restoring the independent intended generators on R therefore gives precisely L^R. This remains true when L_B,raw or the individual N_e are not CP generators.

In a cavity, every block in R has exactly its intended isolated gate during its declared interval. All system/bath disturbance has zero system support there. Bath terms induced by the reduction are allowed; their norm need not be accumulated over the entire apparatus.

For a set R of space-time locations, apply this construction at time t to the subset R(t) active then. Its full propagator T^R is CPTP. Repeated uses of a physical qubit at distinct times cause no ambiguity.

## 3. Exact fault paths by Moebius inversion
Let Lambda be the finite set of all locations. For F subset Lambda define the signed map

 E_F=sum_(A subset F) (-1)^|A| T^((Lambda without F) union A).

Then sum_F E_F=T^empty, the actual channel. Every summand in E_F is a circuit with arbitrary disturbance only at locations in F; all other locations are ideal isolated operations. Thus E_F is supported on the usual fault-location class F, although E_F need not be positive or trace preserving.

For every specified set S0 of locations, cancellation gives the exact inclusive sum

 E(S0):=sum_(F contains S0) E_F
       =sum_(R subset S0) (-1)^|R| T^R.                (1)

This inclusive sum, not a sum of individual path norms, is the local nonprobabilistic noise interface.

## 4. CP interpolation and the mixed derivative bound
For real z_j in [0,1], j in S0, interpolate the cavity generators multilinearly:

 L(z,t)=L_id(t)+product_(j in S0(t))[(1-z_j)I+z_j P_j](L-L_id).

It is a convex combination of actual cavity generators at every time, hence its propagators are CPTP and completely contractive. At cube vertices its full propagator T(z) equals T^R. Integrating the mixed derivative over the cube represents (1), up to an irrelevant sign.

For nonempty A subset S0, the generator derivative vanishes unless all its locations are simultaneously active. At such a time,

 ||partial_A L(z,t)||_diamond
 <=2^|A| sum_(e touches every location in A) eta_e(t).       (2)

It vanishes for |A|>q. Terms not touching a differentiated location are annihilated by I-P_j. All remaining interpolation factors are contractions on the superoperator norm. No total-volume bound enters (2).

The repeated Duhamel derivative of T(z) is indexed by ordered SET PARTITIONS of S0. For a set partition pi, every block A in pi supplies one partial_A L insertion. Between insertions are the actual CP interpolated propagators, with norm at most one. Summing the chronological orders of the blocks partitions their independent integration cube (ties have measure zero). Consequently

 ||partial_(S0) T(z)||_diamond
 <= sum_(set partitions pi of S0) product_(A in pi) w_A,
 w_A=2^|A| integral sum_(e touches every location in A)eta_e(t) dt.   (3)

Only blocks with at most q members contribute. The same bound holds after the cube integration. Formula (3) has no global exp(eta times device volume times runtime).

## 5. Rooted partition recursion gives a local strength
Let Z(S0) denote the nonnegative partition sum in (3), with Z(empty)=1. For any j in S0,

 Z(S0)=sum_(A subset S0, j in A) w_A Z(S0 without A).

Suppose 0<x<=1. A particular noise term touching j meets at most q active locations. Therefore

 sum_(A contains j) w_A x^(-|A|)
 <= integral_(j active) sum_(e touches j) eta_e(t)
       (2/x)(1+2/x)^(q-1) dt
 <= g eta tau (2/x)(1+2/x)^(q-1)
 <= 2*3^(q-1) g eta tau x^(-q).

Set

 x=[2*3^(q-1) g eta tau]^(1/q),                         (4)

and assume the bracket is at most one. Induction on |S0| then gives Z(S0)<=x^|S0|. Together with (1)-(3),

 ||sum_(F contains S0)E_F||_diamond <= x^|S0|            (5)

for EVERY finite set of space-time locations. Unequal local durations/rates can instead use their actual integrated incidence. For q=1 the displayed bound is 2g eta tau; for q=2 it is sqrt(6g eta tau). These constants are conservative.

## 6. What the bridge supplies
Equations (1), (5), and the exact location-support property give a standard-looking signed local-noise expansion for the complete scheduled evolution under the broad HP decomposition, using only total CP-divisible dynamics. The bath may be shared and may retain arbitrary memory. Fresh noiseless bath replacement and an exponentially large device-volume penalty are not required.

A specific threshold theorem still needs to be matched to this COMPLETE SUPEROPERATOR norm convention and its gate/encoding/measurement/decoder assumptions. This note does not simply declare a universal computer. It supplies the noise interface and arbitrary-support linear-map fault classes used in nonprobabilistic fault-path proofs. Initial input preparation is a separate resource; the theorem does not remove the raw-latch ingress floor. The fixed schedule and finite-strength gate geometry are actual assumptions, not an autonomous controller construction.

## 7. Primary comparison and novelty boundary
Aharonov–Kitaev–Preskill, *Fault-tolerant quantum computation with long-range correlated noise*, quant-ph/0510231, already establishes a local-noise fault-tolerance interface for arbitrary shared baths and weak always-on pair Hamiltonian terms, with square-root strength and higher-body analogues: https://arxiv.org/abs/quant-ph/0510231 . Common-bath tolerance, root-power dependence, and fault-path combinatorics are therefore established machinery.

Aharonov–Ben-Or, *Fault-Tolerant Quantum Computation With Constant Error Rate*, quant-ph/9906129, supplies nonprobabilistic fault-tolerance constructions without intermediate ideal classical computation: https://arxiv.org/abs/quant-ph/9906129 . The exact match from (5) to a chosen theorem's norm and input conventions is still an explicit receiving step.

The construction tested here is the CP cavity/interpolation route for LOCAL CENTERED HP perturbations whose sum with the intended dynamics is a valid generator, without requiring deletion of each perturbation to preserve positivity. Historical novelty is not established. It is a mathematical finite-circuit interface, not practical hardware qualification.
