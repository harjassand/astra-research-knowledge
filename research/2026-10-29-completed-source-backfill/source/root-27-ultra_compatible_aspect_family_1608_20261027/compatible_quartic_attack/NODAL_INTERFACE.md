# Exact compatible P1 profile interface

Source profile: `data/EXACT_COMPATIBLE_PROFILE.json`, produced by
`exact_profile.py` from the retained `data/schur_refinement.json` mesh128
run. It contains the exact target coefficients, integer nodal values, common
node denominator10^8, rational moments and the exact optimal background.
No coefficient symmetry is imposed: L+M=1/10^10 is retained.

The physical cell is [0,1]^2 with periodic identification. Nodes are ordered
`integer_nodes[i][j][output]`, with x=i/n, y=j/n and output0/1. The displacement
at that node is its integer value divided by `node_denominator`. Indices wrap
modulo n. Each square uses the same lower-left to upper-right diagonal.
In the unwrapped square let v0=(i,j),v1=(i+1,j),v2=(i+1,j+1),v3=(i,j+1).
The two triangles are(v0,v1,v2) and(v0,v2,v3), each of normalized area1/(2n^2).
Their gradient rows, for each output component independently, are

    n*(phi(v1)−phi(v0), phi(v2)−phi(v1)),
    n*(phi(v2)−phi(v3), phi(v3)−phi(v0)).

Matrix vectors use row-major order(a,b,c,d), representing[[a,b],[c,d]].
The stored `background_minimizer` has that same order and is in the same
coordinates/amplitude units as the rational nodal potential. Adding it as an
affine map gives B+Dphi. The mean gradient and mean determinant are exactly
zero by direct integer replay. Shared nodes give a continuous piecewise
affine potential, not merely a determinant-balanced atomic distribution.

`normalized_nodes` in the numerical records are different floating candidate
values before rounding. The exact artifact is the authoritative retained
profile. Its fourth moment is recorded; it is not assumed to equal one.
An FFT interpolation of these node samples is another compatible smooth
profile, but is not identical to the triangular P1 interpolant. Exact heat
smoothing of the latter should use its actual Fourier coefficients or an
explicit approximation error. This distinction does not prevent testing a
separately declared smooth interpolation at its own scope.

For the analytic aspect-ratio family, take bar_phi(x) to be the y-average.
It is the piecewise linear interpolation of the nodal row averages. Summing
the triangular interpolation correction over j telescopes, so on column i,

    bar_phi'(x)=sum_j[phi(i+1,j)−phi(i,j)].

Then psi=phi−bar_phi is itself P1 and has zero y-mean. For every t>0,
phi_t(x,y)=bar_phi(x)+t*psi(x,y/t) is periodic on[0,1]x[0,t] and has gradient
law[bar_phi'+t*psi_x | psi_y], with the same original triangle weights.
This family retains differential compatibility exactly; it is not obtained
by altering an arbitrary atomic law without a potential.
