# The sign-only quotient-invisibility threshold is sharp

Let A_e=F_2[t]/(t^e) and lambda_e extract coefficient t^(e-1). Consider

    H(X,Y,Z)=X^2 Z+Y^3+Z^3+XYZ.

Its residue gradient is (YZ,Y^2+XZ,X^2+Z^2+XY), and has no nonzero
geometric zero. To see this, YZ=0. If Y=0, then XZ=0, and the last
equation forces X=Z=0. If Z=0, the second equation forces Y=0, and then
the last forces X=0. Thus the residue projective cubic is smooth over every
characteristic-two field.

For X=sum_i X_i t^i, put h=floor((e+1)/3). A noise term using X_h needs
quotient height h+1, exactly one above the general invisibility theorem's
range. There are pure quadratic, rank-two perturbations with

| Chain depth | Perturbation Q | Z(H,Q)/Z(H,0) |
| --- | --- | --- |
| e=0 modulo3 | X_h Y_h | 1/2 |
| e=1 modulo3 | X_h Z_h | -1 |
| e=2 modulo3 | X_h Y_h | 2 |

In particular Q(0)=0 in every case, but the signed sum changes. No linear
or constant error term is needed.

## Exact proof for every depth

At depths1,2,3, complete binary evaluation gives

    e=1: Z(H,0)=2,  Z(H+X_0 Z_0)=-2;
    e=2: Z(H,0)=8,  Z(H+X_1 Y_1)=16;
    e=3: Z(H,0)=64, Z(H+X_1 Y_1)=32.

These are identities of Boolean polynomials on3,6,9 variables, respectively,
and the attached program constructs their ANFs directly from coefficient
convolution and exhaustively checks them.

For larger e, highest-digit orthogonality first forces the residue vector
to zero because the residue cubic is smooth. Every necessary intermediate
step preceding the displayed terminal has the noise independent of its
highest digit. Substituting X=tX',Y=tY',Z=tZ' reduces the cubic depth by
three and the noise coefficient index by one, while the two unused layers
give factor2^6. Iterating reaches exactly one of the displayed three
terminals. Thus the ratios hold for all e. The noise polar form has rank
two since it is the product of two distinct coordinate bits.

The unperturbed signed counts are 2^(2e) for e=0 modulo3, and 2^(2e-1)
otherwise. In the second case this uses the explicit depth-one value2.

This is a sharpness result for the universal identity
Z(H,Q)=(-1)^Q(0) Z(H,0). It is not a counting-time lower bound and does not
show that the weighted critical-ray algorithm's sufficient height condition
is an optimal tractability boundary. A richer terminal calculation can
still handle particular larger-height perturbations.

## Executed program

`quotient_height_boundary.py` independently constructs the raw ANFs for
e=1 through8 and evaluates both complete truth tables, totaling38,347,920
assignments. It verifies all ratios above, including24-variable examples.
`quotient_height_boundary_results.json` contains the exact ANFs and counts.
The program also records all eight residue-gradient values: zero has one
preimage, whereas (1,0,0) has none. Accordingly a linear error in the new
digit gives another direct failure, including complete cancellation at the
depth-two terminal. The rank-two version is the stronger counterexample.
