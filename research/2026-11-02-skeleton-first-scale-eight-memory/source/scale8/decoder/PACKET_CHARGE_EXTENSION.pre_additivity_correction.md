# Bounded-packet / finite-state integer-charge theorem

This extends THEOREM.md beyond linear type weights. All hardened geometry, causal attachment, correction decomposition, intermediate-cost, common-lift, cochain-identity, and distance hypotheses of that theorem remain required. The conclusion is conditional on actual maps satisfying the charge inequalities; no full ell8 family theorem is asserted.

## 1. Packet data and charge

At each layer fix a partition of syndrome coordinates into packet blocks B, each containing at most b coordinates, with fixed bounded-size connected ambient shapes. Every block has a predetermined finite-state integer charge g_B:{0,1}^B -> nonnegative integers, satisfying

  g_B(0)=0;  g_B(x)>=1 for x!=0;
  a |x| <= g_B(x) <= c |x|,

for uniform positive a,c. Set Q(s)=sum_B g_B(s restricted to B). The block partition and charge tables are fixed independently of the sampled syndrome and decoder choices. No monotonicity under deleting bits, linearity, or subadditivity is assumed for a general charge table.

In the proposed packet norm, atoms are singletons and allowed face pairs, all atoms lie inside one bounded block, and g_B is minimum atom count. Then a=1/2 and c=1. More generally singleton atoms plus bounded-support atoms give a>=1/b and c=1. Pair-graph components of size at most 12, if established for the actual recursive geometry, are suitable blocks; their internal optimal matching is a finite lookup, not an accumulating rescaling of charge.

## 2. Complete-block input components and unique output-block ownership

The fixed active dependency graph must satisfy two closure properties:

- **Input closure:** an active input component contains the *entire state* of every packet block it meets, including all its occupied coordinates and the bounded zero-coordinate connectors. Thus input components partition active input blocks, and Q(input_C) is additive across components.
- **Output ownership closure:** for every possible output packet block, include fixed connections between all input dependency locations that can contribute to any coordinate of that block under any allowed branch. Merge active components connected by these preimage-block connections. Consequently every nonzero output packet block has one input-component owner, and that owner produces its full actual block state, including any internal XOR cancellations.

Include the full fine packet blocks and preimages of coarse packet-block adjacencies in the ambient graph. Bounded block size and uniformly bounded forward/reverse map footprints keep these connections and degrees uniformly bounded. The charged connected-shape bound remains a required verification: adding connectors is harmless only with a uniform O(Q(input_C)) bound. Ownership is asserted for the full set of possible sheet choices, not retroactively for whichever branch happened to be selected. This can be implemented with fixed bounded-range adjacency between occupied input dependencies whose possible outputs share a packet block, together with each occupied block's bounded connector neighborhood. Do not activate an arbitrarily long chain of empty blocks merely because they belong to the ambient graph: the active-shape linear-charge bound must survive the closure. The fixed graph supplies possible edges, not an instruction to include every empty vertex.

One can replace unique ownership with a directly proved subadditive contributor inequality for the exact block charge, but ordinary Hamming support coverage alone is NOT sufficient for arbitrary nonlinear g_B. The unique-owner construction avoids this issue.

## 3. Componentwise charge contraction

For every input component C and its full owned output-block configuration O(C), require

  Q(O(C)) <= (1/2) Q(input_C)

on a halving layer and Q(O(C))<=Q(input_C) on a nonincrease layer. Corrections and connected enlarged shapes have size at most A Q(input_C). A componentwise minimum-sheet choice is valid if the actual maps prove

  Q(p_A input_C)+Q(p_B input_C) <= Q(input_C).

For atomic packet norms, the last inequality follows from the per-atom inequality plus subadditivity. For an arbitrary finite-state charge table it must instead be verified directly. The output-block ownership closure ensures that the componentwise output charge is the charge of the actual owned block state, not an unjustified sum over pieces of that block.

## 4. Exact ancestor closure and mass recurrence

For each comparison run a, select the full forward changed-component trace. Whenever an upper selected input component is included, select its complete active packet blocks. For each of these blocks select its unique lower owner, and include that owner's complete input components/blocks. Continue downward to a fixed point. Let Q_i^a be the sum of charges of selected complete input blocks at level i.

The selected upper blocks are a subset of full output blocks owned by selected lower components F_i^a. Therefore positivity, additivity across whole blocks, and componentwise contraction give

  Q_{i+1}^a
    <= sum_{C in F_i^a} Q(O(C))
    <= (1/2) sum_{C in F_i^a} Q(input_C)
     = (1/2) Q_i^a.

No bitwise monotonicity of g_B is used: selected blocks retain their *whole actual state*. Extra forward-selected components only increase lower mass; all upper extras force their own downward ancestry. The same recurrence with factor one holds on intermediate nonincrease layers. Uniformly bounded intermediate layer count gives total selected space–scale charge O(Q_0^0+Q_0^1).

Each added owner attaches to its upper block by a fixed dependency connector, so the closed two-run trace is connected and rooted at the fault. Shapes, connectors, packet-state labels, and any selected atom-decomposition labels cost O(total charge) vertices or finite marks. Their number is therefore exponential in total base charge in the fixed bounded-degree space–scale graph, with no free depth labels or system-volume factor.

## 5. Local fault comparison and honest Gibbs payment

Let F be the at-most-k syndrome coordinates flipped by the single-qubit error. Only blocks meeting F can have different initial block states; their union and connectors form a bounded root neighborhood (at most bk coordinates). The possible charge change in these blocks is uniformly bounded by their finite tables. No bound is assumed on the sizes of components they subsequently merge or split: those components are charged whole.

Let M count the *distinct original Gibbs-occupied coordinates* in the union of all selected base blocks from the two runs. Write Q_0=Q_0^0+Q_0^1. Since the syndromes agree outside F and g_B(x)<=c|x|,

  Q_0 <= c (|selected occupied base inputs in run 0|
             + |selected occupied base inputs in run 1|)
      <= 2c M + 2c k.

For the singleton/pair metric c=1, this is Q_0<=2M+2k. Thus the leaf payment is at least M>=Q_0/(2c)-k genuinely distinct occupied Gibbs bits, not two independent syndrome samples.

A fixed witness leaf set of size M has probability <=q^M. **For q<1, more occupied leaves make this upper bound smaller:** if a single-run charge is no larger than its occupied count, then q^{occupied count}<=q^{charge}, not the reverse. In duplicated-charge indexing, the honest activity is sqrt(q) when c=1, up to the fixed fault allowance. In distinct-leaf indexing, shape entropy is A^{M+O(k)}, yielding the same (Aq)^M form as THEOREM.md after changing constants.

## 6. Consequential instability conclusion

If an input discrepancy survives to level h, one run has a nonzero block, hence selected charge at least one. Its ancestry has base charge at least 2^h. The upper comparison bound g<=c Hamming gives at least 2^h/c-k distinct original occupied leaves in that run.

If the two syndromes agree below h, common higher corrections cancel under the common lifts. The residual physical correction difference satisfies

  weight(R_e) <= 1+C Q_0 sum_{i<h}(K/2)^i
              <= 1+C'(M+k) S_h(K).

If it is nontrivial logical, distance forces M >= (d-1)/(C' S_h(K))-k. Rooted-animal counting and the Gibbs inclusion bound now give exactly the same form as the Hamming theorem:

  P[fixed-qubit logical decoder instability]
    <= B exp[-c(q) min{2^h, d/S_h(K)}],

with fixed additive cutoffs absorbed into B. All depth-dependent conclusions and exponents are unchanged. A charge contraction rho<1 instead of 1/2 replaces 2^h by rho^{-h} and S_h by sum_{i<h}(K rho)^i.

## 7. What this does and does not establish for the packet proposal

Conditional on the actual blue maps satisfying the stated per-atom two-sheet inequality, the actual red maps being charge-nonincreasing, uniformly bounded packet blocks, owner closure, and the remaining cochain/common-lift hypotheses, the packet metric supplies the contraction consumer needed for the consequential theorem. This shows that raw 1-to-2 Hamming inflation is not an abstract obstruction when it is one allowed cost-one packet.

It does not certify the blue/red map columns, the recursive packet-block bound, admissibility, global cochain identities, or exact lift/homotopy support for the concrete family. Those are separate geometric/algebraic obligations. There is no full-family lifetime claim here.
