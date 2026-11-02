# A two-rib terminal normal form (declared reduced module)

This improves the candidate coarse carrier: the source's two parallel ribs can carry the duplicated residue. It is not necessary to guess that the eventual coarse map duplicates a syndrome in the two sheets. The following is exact for the declared two-rib module; identification with a full physical coarse map still needs consistent parent-face reductions and global port gluing.

## Module and actual local pattern it represents

Along an inherited three-page seam, the two new attaching ribs partition each sheet into three intervals. Name the quotient face-syndrome blocks

    a−,a0,a+, b−,b0,b+, c0,c1.

The two sheets are a,b; the two cylinder rib blocks are c0,c1. Each block lies in Q=F_2^3/F, where F is the INHERITED old seam code. Each nonzero Q label has a weight-one representative for either blue repetition F or red parity F.

The four classes of blue attaching-edge correction are

    a−+a0+c0,   a0+a++c1,
    b−+b0+c0,   b0+b++c1,

with any physical arm label; inherited F corrections act separately within each block. This is the consecutive-star incidence, not a replacement of the sheaf data.

## Exact flow representation

Use five vertices 0,A,B,D0,D1, and edges

    a−=0A, a0=AD0, a+=AD1,
    b−=0B, b0=BD0, b+=BD1,
    c0=0D0, c1=D0D1.

A nonzero Q-valued edge has cost one. The four attaching moves are the four triangle cycles. The complete relative charges are the boundary at A,B,D0,D1:

    A=a−+a0+a+,
    B=b−+b0+b+,
    D0=a0+b0+c0+c1,
    D1=a++b++c1.

These are complete because the graph is connected and the four triangle cycles form its cycle basis. This keeps correlated charges as physical face-block packets.

## Paired-rib residue and factor two

If the full surrounding circuit produces A=B=D0=0, let s=D1. The syndrome is equivalent by the four attaching cycles to

    a−=a0=a+=b−=b0=b+=0,   c0=c1=s.

A nonzero s cannot be realized by one occupied edge: there is no 0--D1 edge. It is realized by the two-edge path c0,c1. Hence the exact minimum weight in that relative class is2, or0 if s=0. Equivalently the paired-rib normal form contracts to its coarse label with factor1/2.

The program exhausts every block-label input: 65536 for inherited blue and256 for inherited red. It verifies the complete relative costs, all1024/32 matching inputs, and explicitly solves each matching input to the paired-rib target by the four physical-pattern triangle moves. The minima of the nonzero coarse classes are exactly2.

## Where the actual gluing gate remains

The charges A,B,D0 do not vanish for arbitrary relative inputs. They must be transported/canceled by the real W1/W2 circuitry and sheet collars, with owned-site bookkeeping. W0 has no cylinder, so conversion to sheet carries must be budgeted. The full transfer table retains all256/16 relative classes and their minimizing realizations; it does not discard unmatched traces.

This makes a finite carry-potential/min-terminal-cost gluing test possible. It does not yet prove the matching conditions, identify s with a legitimate syndrome of the previous complete code, or show that the proposed normal-form choices have the needed componentwise decoder stability.
