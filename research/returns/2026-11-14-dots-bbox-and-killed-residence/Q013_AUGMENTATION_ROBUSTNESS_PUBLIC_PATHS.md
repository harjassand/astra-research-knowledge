# Orientation-independent envelope extension (derived, not implemented)

The six-direction implementation assumes uniform diagonal orientation. To remove that assumption while preserving a supplied arbitrary fixed one-diagonal-per-plaquette augmentation, use all eight lattice directions as the code alphabet, but reject any decoded step or canonical DFS edge absent from the supplied augmentation. Use augmentation neighbors for connectivity, lift, and exclusion. Reverse-direction labels must remain paired.

For a<=49 let P_a=2 ceil(2 sqrt(a)) and k_a=floor(8P_a-a/25). Set b_a=(10/27)^k_a per code. Since e^-1<10/27 and k_a<=8P_a-a/25, physical activity is <=b_a. At most n64^(a-1) codes exist, so
Γ8=n sum_{a=1}^{49}64^(a-1)b_a =0.002233492042929214... .

This number is computed by finite exact rational sums. Thus the same Poisson construction accepts compatible collections with probability >=exp(-Γ8)>.9977. It is an efficient unconditional full-core sampler for ANY supplied fixed augmentation, despite the much larger envelope than uniform six-neighbor coding. No need to know the normalizer or discard rare large components. The supplied graph predicate must specify the actual original diagonals; this construction does not invent that predicate. Rectangle site-count convention still remains an explicit parameter.

This is a derived extension, not executed eight-direction code. The existing executed source.py remains six-direction only.

## Implemented continuation

`source8.py` now implements this construction. `Core(L,box_sites,diag,max_area=None)` requires a supplied deterministic oracle: diag(x,y)=True means SW-to-NE for the plaquette with lower-left anchor(x,y), False means SE-to-NW. Every anchor is reduced moduloL. All eight direction indices have inverse indexj^1; diagonals are admitted only when the oracle authorizes the corresponding edge. Connectivity, lift checking, canonical ordered DFS, and interpolymer exclusion all use the supplied graph. Physical energy still uses only the original four nearest-neighbor directions. No diagonal coupling is added.

A tighter legitimate area cap is box_sites², not49. With explicit box_sites5 or6 this reduces Γ8 to1.0863424808e-7 or1.0863471832e-7, respectively. Thus the executed implementation preserves fast nonempty acquisition as well: its rational acceptance lower bound is>.31 for either convention, expected attempts<100/31. Unconditional acceptance is>0.99999989. Exact rational checks cover every polymer size through the applicable25/36 cap. The inequality e^-1<10/27 follows already from the first six nonnegative Taylor terms for e, so the envelope needs no floating constants.

`test_source8.py` exhaustively checks all15,275 subsets of sizes1..4 on a5×5 torus with2-site box, for uniformNE, uniformNW, and alternating plaquette diagonals. Each pattern yields225 admissible connected polymers. All adjacency reversals, canonical-code inversions and code uniqueness pass. It also runs1000 nonempty R200 draws for each orientation/box pair. All6000 observed outputs are singletons. As previously, this tests conditional sampling execution, not rare large-polymer frequencies. `source8_tests.json` records actual results.

Graph-oracle access is charged once per tested edge; if the oracle is an explicitL²-bit table its acquisition/storage costsO(n). A simple fixed orientation or arithmetic pattern costsO(logL) bits to evaluate. The algorithm does not acquire an unknown original graph or decide what the intended rectangle convention was. For the fixedR200 parameters it uses finite expected work and no distribution truncation. General-temperature or growing-r polynomial complexity is not claimed; the envelope may grow badly in those regimes.
