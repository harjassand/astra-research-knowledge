# Direct erosion without bootstrap mergers

For E(S)=8P(S)-0.04|S|, deletion of a plus site with k physical nearest-neighbor plus neighbors has energy change 16k-32+0.04.

Let C be an original augmented-connected component, with a contractible rectangular lift and horizontal span w<=400. In descending row order, delete each occupied contiguous horizontal run from left to right. The rule applies to the ORIGINAL component support, not a filled hull. A site being deleted has no occupied neighbor above (higher rows are gone) and no occupied neighbor left (earlier sites in its run are gone). It therefore has k<=2 and energy increment <=0.04. The final site of a run also has no right neighbor, so k<=1 and increment <=-15.96. For a run of length ell<=w, completed run energy change is <=0.04*ell-16<=0. Thus all completed-run energies are nonincreasing; during a run, the height above its initial energy is at most 0.04*(ell-1)<=15.96.

Outside C no plus site can be physical-NN adjacent to C, because physical NN edges are among augmented connectivity edges. Since this construction only deletes, no new adjacency is introduced. Consequently this estimate is valid in the full configuration with every thermal companion retained. Holes, overhangs, and multiple row-runs cause no problem. Swapping coordinate axes covers components with either span<=400. No bootstrap addition occurs, hence no component merger provenance is created.

For several such components, process components in a deterministic original-root order. Completed components have no positive net energy change; only the currently active run can exceed the original full energy, by at most15.96. Total deletions are at mostn.

Limitations: this is an explicit communication-height/path construction only. It does not establish a killed-generator gap, congestion, or mean duration. A weighted reconstruction of erased original components and the active partially erased component is still required. Components whose two spans exceed400 and winding components are not covered by this contractible small-component statement.
