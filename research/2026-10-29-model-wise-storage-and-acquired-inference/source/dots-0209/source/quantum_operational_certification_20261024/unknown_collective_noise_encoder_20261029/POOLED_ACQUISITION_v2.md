# Pooled physical star acquisition: a factor-n call improvement
2026-10-29. Supplements DERIVATION_v1.md; supersedes its serial acquisition complexity only, not its proof or interfaces. Not independently reviewed.

For each of the 81 settings (a,b,c,d) in {X,Y,Z}^4, prepare root site 1 in the +d eigenstate and EVERY other site in +c. Apply one full array source call. Measure root along b and EVERY leaf along a. Retain all leaf-root outcome products. For each edge i,1, each product has mean T_i1[(a,b),(c,d)]. This follows by tracing the other qubits in each product-unitary realization. Each edge's m records are iid across reset calls. Correlations between edges due to the same z and reused root outcome are arbitrary but do not affect the per-edge Hoeffding bound and union bound. No joint independence assertion is needed.

Thus ALL star blocks require N=81m full-array calls, not 81(n−1)m. With m≥2η^(−2)log[162(n−1)/δ] and η=εg0/[200(n−1)], the certified diamond guarantee in v1 follows using
N = O(n² g0^(−2) ε^(−2) log(n/δ)) full-array calls,
O(nN) physical preparations AND readouts, O(n) constant-size counters per setting, and O(n) constant-size SVDs. Parallel calibrated site preparation/readout is an actual hardware requirement. Without it, the serial v1 schedule remains valid. This is not a cost-free multiplication of independently prepared local experiments.

The simulation `check_pooled_v2.py` samples ONE shared random collective rotation z per full source call and then actual conditional independent one-qubit output measurement outcomes, reusing each actual root outcome across all star correlations. It therefore retains the physical cross-edge dependence omitted from v1's deliberately independent banks. Conditional on z, all output states are product because all inputs are product. This is exact sampling of the stated acquisition model, not independent synthetic edge noise.

With seed 20261029, n=4, the minimum tested retained-bath entanglement fidelity at times 0,1,10,100,1000 is 0.9620126 for 81000 full calls; 0.9986011 for 810000 calls; 0.9994636 for 8100000 calls. These are finite small simulations, not the conservative high-probability theorem's sample prescription or experimental data. Calls remain numerous; no practical speed or sample advantage over an equally informed conventional symmetry-learning method is established.
