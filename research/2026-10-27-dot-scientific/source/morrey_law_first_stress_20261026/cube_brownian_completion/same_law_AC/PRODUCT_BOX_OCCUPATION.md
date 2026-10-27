# Exact same-terminal-law positive AC substitution

## Source and geometry
Each received box is a three-level subtree of an ACTIVE component of the adopted141 exact root. At its root x, each level adds one of the fixed pair +-v_i with probability1/2, independently of earlier signs; det V!=0, where V has columns v_i. All eight corners x+V epsilon are strict PSD-interior helpers. Convexity of the positive-definite cone implies the whole closed parallelepiped is inside the physical domain. Every v_i is J-null. The exact incoming policy probability, adopted root component weight, original internal actions and eight unchanged downstream (time,state) nodes are retained in the interface receipt.

Replace only this three-level conditional subtree by x+V Z(t), where the three coordinates Z_i are independent standard Brownian motions started0 and individually stopped/absorbed on first reaching +-1. Continue until all coordinates have been absorbed, then select the ORIGINAL downstream node with its exact helper corner and remaining horizon. Independence and symmetry give each corner probability1/8, exactly the original conditional law. Therefore the whole finite terminal random variable law, its source/cubic moments and all completion/Gram arrays remain unchanged. This is not an excursion returning to x and not an unreceived posterior completion.

The covariance at time t is sum_{i:coordinate i active} v_i v_i^T. It is PSD and J-orthogonal since each v_i is null; initially it is full rank. The expected stopping time is at most sum_i E tau_i=3. The expected Hessian-occupation trace is exactly (1/2)sum_i ||v_i||^2, matching the old sequential product subtree. Thus all occupation measures below are finite.

## All strata, not only the interior
Let p(t,u) be the standard Brownian Dirichlet heat kernel from0 on(-1,1), S(t)=integral p(t,u)du, and a(t)=1-S(t). A coordinate's law at t is p(t,u)du + (a(t)/2)(delta_-1+delta_+1).

For each subset A of active coordinates and each fixed choice of signs on its complement, define the positive parameter-space measure

    (1/2) [sum_{i in A} v_i v_i^T]
    * integral_0^infinity [a(t)/2]^(3-|A|) product_{i in A}p(t,u_i) dt
    * product_{i in A}du_i.

Push this matrix-valued measure forward by u -> x+Vu, with the complementary coordinates fixed to their signs. For |A|=3 this is the interior AC occupation. For |A|=2 it is each face occupation; for |A|=1 it is each edge occupation. For A empty the covariance vanishes, so there is no vertex occupation. These are the COMPLETE positive occupations, not a fake continuation on the physical PSD boundary: the entire auxiliary box, including its faces/edges, lies strictly inside the physical domain. All pieces are J-null and finite, and the stopped Ito identity gives the eight-corner law minus delta_x. Then apply the exact incoming mass, root weight and six S3 images.

## Uniform interior Loewner lower bound
For t in[1/4,1/2] and |u|<=1/2,

    p(t,u)=sum_{k>=0} exp(-(2k+1)^2*pi^2*t/8)
                           cos((2k+1)*pi*u/2) >=1/4.

A rational proof: first term > (1/2)(7/10)=7/20, since pi^2<10, exp(5/8)<2, and cos(pi/4)>7/10. Using pi^2>9, the absolute remaining tail is <=exp(-81/32)/(1-exp(-9/2)) < (1/12)/(1-1/64)=16/189. Their difference exceeds1/4. The three elementary exponential inequalities are certified by finite rational Taylor bounds in the companion script.

Thus integral p(t,u1)p(t,u2)p(t,u3)dt >=(1/4)*(1/4)^3=1/256 on the central half-box. The spatial interior matrix density obeys

    dM/dx >= VV^T/(512 |det V|).

If T=Tr(VV^T), then lambda_min(VV^T)>=4 det(V)^2/T^2, since the product of the other two eigenvalues is <=T^2/4. Multiplying the exact incoming mass, adopted root weight and the identity S3 weight1/6 gives the explicit alpha I in the interface. This is a genuine Loewner lower bound, not merely a trace estimate. Other permutations can be separately retained/combined without double-counting.

## Accounting with the unchanged completion
The previous full141 bound discarded the entire positive actual finite-line occupation and bounded the negative part of the source-linked completion/cubic stress. No cancellation by the old selected subtree's line occupation was credited in that bound. Removing those old positive line pieces therefore does not undo a previously credited reduction. The new box interior, faces and edges are positive; retain them all in the actual representation, and credit only a RECEIVED interior reduction against the unchanged scalar completion, using alpha I. Everything else remains safely discarded in the upper estimate. Existing source, arithmetic, continuous-tail, cubic, face/edge and own-Gram payments remain unchanged.

Compatibility of several replacements requires checking that no selected root lies strictly inside another selected three-level subtree. Their spatial supports may overlap; occupation densities then ADD, while the negative-part reduction must be integrated without double-counting the same baseline negative bulk. This compatibility and overlap accounting is separate from each single-box interface.
