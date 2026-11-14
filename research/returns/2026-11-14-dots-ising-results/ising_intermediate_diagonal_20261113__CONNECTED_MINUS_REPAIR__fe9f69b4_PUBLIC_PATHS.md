# Diagonal-cylinder finite-pocket repair

This is a local constructive lemma, not a majority-completion theorem.

Work in the cylinder modulo translation(L,L), with physical NN adjacency for plus and matching8-adjacency for minus. Suppose an eligible gate would detach a contractible minus pocket C from the retained essential minus component. Its only external minus contacts are lifts of that gate. The transverse functional u=x−y has the SAME value at every periodic gate lift.

If C has a site with u above the gate value, choose a maximal-u site. Its east and south neighbors have larger u, hence lie outside C; neither can be a gate lift. Both are plus, giving a legal two-neighbor birth. If C extends below the gate value, choose minimal u; west and north give the analogous birth. If every site of C has the same u as the gate, all physical NN neighbors change u and cannot be gate lifts, so every site has four plus neighbors.

An eligible chosen site might be an articulation of the remaining minus pocket. In that case recurse into a component detached from the retained gate, with this chosen site as the new gate. Such a component is strictly smaller. The same transverse argument applies, because all periodic images of every new gate still have equal u. Eventually one obtains an eligible non-articulation site. Remove it, then repeat. This empties C while retaining minus connectivity and retaining the original gate until last.

The argument explicitly handles C touching several periodic copies of one gate; it does not require C plus the gate to have a finite lift. It does require C itself to be contractible and the claimed single-gate external-contact condition.

To use the lemma in a global diagonal front, separately establish that deleting an eligible gate cannot split the remaining minus set into TWO essential components while the retained plus collar is NN-connected and essential and a fixed essential minus collar survives. The existing cylinder separation argument is the proposed interface. This note does not establish that the resulting front reaches majority before periodic pin contact, nor an energy/mincut bound after such contact.
