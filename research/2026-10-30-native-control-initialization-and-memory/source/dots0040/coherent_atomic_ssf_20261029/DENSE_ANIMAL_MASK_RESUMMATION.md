# Dense-animal sieve stress test and a useful exact masked resummation

2026-10-29. This records a failed general approach and a concrete repair for a special overlapping-certificate family. It does not complete the continuous coherent-Hamiltonian threshold.

## 1. An exact bounded-degree dense-animal example

Fix integer k>=5. Let C be a path of k−1 vertices with endpoint r. Attach at r a complete binary tree of depth a, and attach a private path of length b to every depth-a leaf, where

    L=3k+1,  a=floor(L/2),  b=ceil(L/2).

Let D be the set of far endpoints of the private paths, so |D|=M=2^a. The full graph has maximum degree three. Allow occupied fault variables only at vertices in C union D; every other vertex has zero fault budget.

Define b_dense(T)=1 if there is a connected containing animal W with

    |W|>=4k,      |W intersect T|>=|W|/4.

On this restricted set of variables, this event is EXACTLY

    b_dense(T)=1{C subset T} 1{T intersect D is nonempty}.   (1)

Proof of the forward direction: all k−1 core sites plus any far endpoint have a connected hull of (k−1)+L=4k sites and k faults.

Conversely suppose the full core is not occupied. If a connected W contains c core faults and r_far>=1 far endpoint faults, with c>=1, its tree hull has at least

    c+L+(r_far−1)b

vertices: the core segment contributes at least c−1 edges, the first root-to-endpoint path has L edges, and each extra far endpoint contributes its disjoint private b-edge path. Here c<=k−2. The density requirement would give

    3c+4 r_far >= L+(r_far−1)b,

which fails for c<=k−2, L=3k+1, and b>4. If W has no core fault and at least two far endpoint faults, its hull contains all their private paths and hence more than 4 r_far vertices. A single far endpoint or core-only subset supplies fewer than k faults and cannot make a size-at-least-4k animal dense. Finally, with no far endpoint even a full core has only k−1 faults. This proves (1).

This is an abstract bounded-degree graph example; it is not asserted to be a particular quantum code family.

## 2. Why absolute Möbius summation fails badly

For uniform inclusive fault budget η on these variables, the weighted absolute Möbius sum of (1) is

    K_b(η)=η^(k−1)[(1+η)^M−1].                         (2)

Since M is exponential in k, this can be enormous even when a classical product-measure bad probability is at most η^(k−1). In particular, a generic proof which bounds every Möbius coefficient absolutely will not establish the desired dense-animal threshold merely by connected-animal counting. The componentwise factorization in CONNECTED_OCCUPIED_SIEVE.md does not apply: the actual occupied sites are not connected, and their clean connecting paths matter.

## 3. Exact repair using arbitrary zero/full masks

Independent CPTP switching supplies more than the inclusive bound with all unselected noise fully present. It also bounds the selected inclusive sum while any specified unselected subset is switched completely off.

For (1), let F(C;D=full) be the inclusive sum requiring every core location faulty with all leaf noise left fully present, and F(C;D=0) the same sum with every leaf generator switched off. Then exactly

    B_b=F(C;D=full)−F(C;D=0),
    ||B_b||_diamond<=2η^(k−1).                         (3)

Thus all M alternatives are resummed without paying either M independent terms or exp(Mη). This is valid for noncommuting joint system-bath evolution whenever the required masked generator interpolations are CPTP. It is not a probability argument and does not create a physical fault-label record.

The example establishes two useful points simultaneously: the naive absolute-Möbius criterion is too strong for dense animals, while a mask-aware resummation can recover a threshold-compatible bound for highly overlapping certificates.

## 4. Remaining constructive challenge

For general asynchronous SSF witnesses, one would need to organize overlaps into such reusable cores/alternative regions, or another bounded-complexity hierarchy, while preserving a large mandatory fault budget. A canonical first-witness partition alone does not provide this: excluding every earlier witness is generally not equivalent to switching a fixed collection of local generators off.

The positive Poisson-CPTP spacetime-chain proof avoids this problem because its terminal event is an actual classical record event. For continuous coherent Hamiltonian insertions the same geometric chain, by itself, is not a positive event, and the masked-resummation step remains unproved beyond special families such as (1).
