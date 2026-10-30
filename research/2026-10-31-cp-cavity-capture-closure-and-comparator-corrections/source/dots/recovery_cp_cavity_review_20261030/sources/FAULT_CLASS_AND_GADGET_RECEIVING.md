# Exact fault-class support and a finite gadget receiving rule
30 October 2026. Companion derivation for CP_CAVITY_LOCAL_FAULT_BRIDGE.md; no universal threshold or autonomous compiler claim.

## 1. Why bath-only cavity changes do not spoil location support
A fault class F means the linear span of circuit maps in which every location outside F is its ideal gate, while locations in F may undergo arbitrary system/bath maps. Arbitrary bath-only evolution is allowed between locations. This is the nonprobabilistic, shared-bath fault-class meaning, not a distribution of independent CPTP errors.

On a synchronized layer of disjoint gate blocks, a cavity generator has the form

 sum_(j in R)L_id,j + Id_R tensor K_complement,

where K_complement is an actual CPTP generator. The two pieces commute on system supports. The layer propagator is therefore exactly the tensor product of the intended maps on R and an arbitrary joint map on the other active blocks and bath. A finite system matrix-unit expansion of the latter expresses it as a linear combination of products of maps on those other blocks, with bath-map coefficients. Each coefficient can be attached to one allowed faulty location, with bath-only history allowed when none is present. No norm estimate is taken on this expansion; its purpose is ONLY to establish linear-span support.

Composition over layers proves that T^R lies in the fault class Lambda without R. Each summand of E_F has R containing Lambda without F. The fault classes are nested, so E_F lies in class F. In particular E_empty is the ideal system circuit tensored with a bath channel, even though that bath channel differs from the bath dynamics of other cavities. It preserves the intended system/reference operation, including for initially correlated system-bath inputs.

For fixed schedules resolved into smaller intervals, apply the same argument on each interval where the active block partition is fixed. The resulting class allows arbitrary interactions inside each declared faulty location's duration; no interaction on an ideal location remains. A threshold proof formulated for strictly layered gate boxes can instead use the explicitly layered version, with any refinement overhead counted. Do not claim an arbitrary overlapping autonomous generator is a scheduled disjoint-gate circuit.

The bath-only differences between cavities thus affect the unconstrained bath coefficients, not the ideal-location support. The inclusive norms are proved BEFORE expanding these coefficients, so there is no hidden dimension or path-count factor from this representation.

## 2. An exact bad-gadget sieve
Suppose a fixed gadget has a disjoint set G of L physical locations, and its declared correctness condition is that fewer than t locations in G are faulty. This is a sufficient gadget assumption; it must be earned from an actual code/operation. For a fault set F write k=|F intersect G|. The elementary binomial identity is

 1_(k>=t)=sum_(s=t)^k (-1)^(s-t) binom(s-1,t-1) binom(k,s).

Hence its signed bad map is exactly

 Bad_G=sum_(S subset G, |S|>=t)
        (-1)^(|S|-t) binom(|S|-1,t-1) E(S),

where E(S)=sum_(F contains S)E_F is the original inclusive map. If ||E(S)||_diamond<=x^|S|, then

 ||Bad_G||_diamond
 <=sum_(s=t)^L binom(L,s)binom(s-1,t-1)x^s
 <=binom(L,t)x^t(1+x)^(L-t)=:x'.                    (1)

The last inequality follows from binom(L,s)binom(s-1,t-1)=(t/s)binom(L,t)binom(L-t,s-t). This bounds the actual bad sum, not the sum of the norms of every exact physical fault path.

## 3. Joint bad gadgets retain the inclusive norm law
For r selected gadgets on DISJOINT physical-location sets, multiply their sieve identities. Every term uses an inclusive set S equal to the disjoint union of one selected subset per gadget. Apply the same original local-noise bound x^|S|. The sum factorizes and gives

 ||sum_(F makes every selected gadget bad) E_F||_diamond <=(x')^r.

Thus if the actual gadget's good fault classes implement the intended logical operation on the prescribed incoming correctable modules, grouping exact physical paths by their bad-gadget set yields the same kind of signed local-noise interface with strength x'. This is the elementary norm/combinatoric part of recursive fault tolerance.

Overlapping extended rectangles, propagation between gadgets, input preparation, and recovery semantics need their actual standard construction. Their correctness is not inferred just from inequality (1). This result makes a precise receiving target: provide fixed-size gadgets and their usual fault-class correctness, then the broad HP/cavity noise law enters their combinatorial bad-set bound without any device-volume factor.

## 4. Scope
These are linear-algebraic and combinatorial deductions from the cavity bridge. They do not provide the gates, a noiseless decoder, a capture interface, or a native autonomous scheduler. A particular established fault-tolerance theorem may use another norm or enlarged rectangles; that match must be checked rather than announced.
