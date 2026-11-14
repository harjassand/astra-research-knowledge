# Local seed extraction does not require global winding classification

For an actual fixed-augmentation plus component, grow a deterministic connected prefix from a canonical site, adding an adjacent site at a time and assigning its lifted integer coordinates. Stop as soon as either lifted bounding-box side reaches400 sites. Every addition moves by at most one in each coordinate relative to an existing neighbor, so either side increases by at most one. At the first stop, one side is exactly400 and the other is at most400.

Before this stop, an inconsistent lift cannot occur: a cycle with nonzero torus displacement would require coordinate span at least L−1 along its vertices. Since all current spans are below400<L−1, no such cycle is present. Likewise projection of the prefix is injective. The seed therefore lies in an actual contractible400×h box with h≤400, even when the FULL component winds once, diagonally, or in both directions.

If growth exhausts the component without stopping, that component has a consistent lift fitting a399-square; it belongs to the small-component class. Thus every component outside that class supplies the local seed. The chosen prefix is not assumed to be an entire original component; original sites outside its bounding rectangle remain part of the physical state.

This is an existence/extraction lemma only. It does not itself prove that bootstrap closure fills the seed rectangle under the exact allowed augmentation, nor that partial closure has a paid preimage bound. It also does not license completing the rectangle after first majority has already been hit. Those are separate path and entropy interfaces.
