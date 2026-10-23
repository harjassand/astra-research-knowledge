# Audit: recursive majority map and physical-site error

This checks the reversible map and the co-moving mismatch claim in
`REVERSIBLE_BIAS_AMPLIFICATION_OPENING.txt`; it does not assess its circuit
costs or the asymptotic comparison.

## Three-bit gate algebra

Use the convention that `CNOT(a,b)` has control `a` and target `b`. Starting
from `(x,y,z)`:

1. `CNOT(y,x)` changes the first wire to `s1=x XOR y`.
2. `CNOT(z,y)` changes the second to `s2=y XOR z`.
3. `CNOT(y,z)`, now controlled by updated `s2`, changes the third to
   `z XOR s2`.
4. `Toffoli(x,y;z)`, now controlled by updated `s1,s2`, changes it to
   `q=z XOR s2 XOR (s1 AND s2)`.

Since `z XOR s2=y`, this is `y XOR ((x XOR y) AND (y XOR z))`. If `y=0`,
that equals `x AND z`; if `y=1`, it equals 1 except when both `x=z=0`.
These are exactly the two cases of `Maj(x,y,z)`. The first two wires remain
`(s1,s2)`, so the chronological circuit implements the claimed map with
updated, rather than original, Toffoli controls.

For fixed `(s1,s2)`, the inputs are exactly
`(s1 XOR b, b, s2 XOR b)` for `b in {0,1}`. They are bitwise complements,
and their three-bit majorities are opposite. Thus `q` selects one of the two
inputs; equivalently, the map is bijective. Independently, bijectivity follows
because the stated CNOT/Toffoli sequence is a composition of reversible gates.

## Recursive fixed-syndrome complement

At a recursive node, its full syndrome consists of the three child syndromes
and the two new bits `(s1,s2)`. Holding this full syndrome fixed holds every
child syndrome fixed. Changing the node's `q` selects the other member of the
two-element parent fiber, so the three child `q` bits all flip. Inductively,
within each child, fixed child syndrome plus flipped child `q` selects the
complementary physical word. Therefore every one of the `L=3^k` physical bits
flips. The base case `L=1` is immediate. No independence between a block's
root `q` and that block's syndrome is needed; in general they can be
correlated.

## Co-moving mismatch probability

For two distinct adjacent length-`L` blocks, the decoded block after the
countershift has its own syndrome and the incoming neighboring root label.
The complement property makes it equal to its original word when the two root
labels agree, and its bitwise complement when they differ. Hence, at every
physical site, the mismatch indicator is exactly the same event
`{Q_left != Q_right}` (up to which neighbor the chosen shift uses).

With iid Bernoulli-`p` source bits, each root label is a depth-`k` ternary
majority of its own disjoint block. Its one-probability obeys
`epsilon_0=p` and `epsilon_(j+1)=3 epsilon_j^2 - 2 epsilon_j^3`. Root labels
of distinct blocks are independent because they are functions of disjoint
independent source bits. Thus the mismatch probability is exactly
`P(Q_left != Q_right) = epsilon_k(1-epsilon_k) +
epsilon_k(1-epsilon_k) = 2 epsilon_k(1-epsilon_k)` at every physical
site. This is a sitewise marginal statement, not a claim that all site errors
are independent. It also does not condition on the block's syndrome; such a
conditioning would generally alter the root-label law.

**Audit result:** the updated-control identity, recursive fixed-syndrome
complement, and exact per-site co-moving error formula are valid under the
opening's iid Bernoulli source assumption and for neighboring distinct blocks.
