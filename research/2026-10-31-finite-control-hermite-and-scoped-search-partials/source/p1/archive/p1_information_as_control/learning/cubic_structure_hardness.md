# Recognizing a globally affine direction of a cubic is NP-hard

P1 side note, 30 October 2026. This is an elementary reduction with an inverse-polynomial gap. It concerns one specific representation-discovery task, not the complexity of all adaptive sensing policies.

## The recognition problem

Input: an explicitly supplied homogeneous cubic polynomial F on R^D with integer coefficients. Decide whether there is a nonzero direction d such that, for every base point x, the restriction t -> F(x+t d) is affine in t.

For a homogeneous cubic,

`D_d^2 F(x)=2 gradient(F)(d)^T x`.

Thus the recognition problem is exactly whether the gradient has a nonzero real zero. The direction can be normalized to unit length by homogeneity.

**Claim.** The problem is NP-hard. More strongly, the constructed instances have the following promise gap, where N is the number of Boolean and auxiliary variables in the construction:

* YES: some unit d has gradient(F)(d)=0;
* NO: every unit d has `||gradient(F)(d)||_2>1/(384N)`.

Equivalently, for standard Gaussian base point X, the expected squared directional curvature is zero in a YES instance and exceeds `4/(384N)^2` in every unit direction in a NO instance.

All dimensions, coefficient bit lengths and the reciprocal gap are polynomial in the original Boolean input size. This is a computational obstruction after the cubic coefficients have already been supplied or acquired.

## Homogeneous quadratic encoding of 3-SAT

Start with n Boolean variables and m clauses of three literals. Introduce one auxiliary Boolean variable a_j per clause. Let N=n+m and use homogeneous coordinates

`v=(t,x_1,...,x_n,a_1,...,a_m)`.

For every original and auxiliary variable y include the quadratic constraint

`y^2-t y=0`.

For a positive literal x_i, let its false-indicator linear form be `ell=t-x_i`. For a negative literal not-x_i, use `ell=x_i`. For each clause with false indicators ell_1,ell_2,ell_3 include

`ell_1 ell_2-t a_j=0`,

`a_j ell_3=0`.

Call all these homogeneous quadratics q_1,...,q_J, where J=N+2m=n+3m.

If t=0, the Boolean constraints force every other coordinate to be zero. Hence any nonzero common zero has t!=0. Dividing by t gives original and auxiliary variables in {0,1}. The auxiliary equals the product of the first two false indicators, and the final constraint says the three literals cannot all be false. Therefore the q_j have a common nonzero real zero exactly when the Boolean formula is satisfiable.

Conversely a satisfying assignment, t=1, and auxiliaries equal to the corresponding two false-indicator products supply such a zero. This uses only real homogeneous quadratics with bounded integer coefficients.

## Cubic encoding

Introduce scalar w and z in R^J, and define

`F(w,z,v)=w^3+3w||z||^2+sum_j z_j q_j(v)`.

The ambient dimension is `1+J+(N+1)=2n+4m+2`. Write a direction as d=(a,b,h). If q_j(v)=v^T A_j v, then

`gradient_w F(d)=3(a^2+||b||^2)`,

`gradient_z F(d)=6ab+q(h)`,

`gradient_v F(d)=2 sum_j b_j A_j h`.

The first component forces a=b=0 at any gradient zero. The remaining equations then reduce exactly to q_j(h)=0. Thus a nonzero globally affine direction exists exactly when the SAT instance is satisfiable.

The positivity in the w component is what prevents extraneous directions in the newly introduced z variables. The polynomial is sparse with polynomially many degree-three monomials. Expanding it into a dense coefficient array also takes only polynomial time.

## Quantitative gap for the quadratic constraints

Suppose a vector v=(t,y_1,...,y_N) has norm squared at least 1/2 and every encoded quadratic has absolute value at most epsilon, with epsilon<=1/(192N).

From `|y_i^2-t y_i|<=epsilon`,

`|y_i|<=|t|+sqrt(epsilon)`.

Therefore

`1/2<=||v||^2<=(2N+1)t^2+2N epsilon`.

As epsilon<=1/(8N), this implies `t^2>=1/(12N)`. Normalize all coordinates by t and let delta=epsilon/t^2. Then delta<=1/16.

For each normalized variable u, `|u(u-1)|<=delta`. Its distance to one of 0 and 1 is at most 2delta. Round to that Boolean value. Every normalized false indicator is likewise within 2delta of its Boolean counterpart and has magnitude at most 1+2delta.

The product of two such approximate false indicators differs from the product of their Boolean counterparts by at most

`4delta+4delta^2<=5delta`.

After rounding, the auxiliary gate equality has an integer residual of absolute value at most `delta+5delta+2delta=8delta<=1/2`, so its residual is exactly zero. The clause product constraint has integer residual at most `delta+5delta=6delta<1`, hence also zero. The rounded assignment satisfies every clause.

Consequently, for an unsatisfiable instance, no vector of squared norm at least 1/2 can make every quadratic residual <=1/(192N).

## Quantitative gap for cubic affine-direction recognition

Suppose ||d||=1 and `||gradient(F)(d)||_2<=eta`, with eta<=1/(384N). The nonnegative first component gives

`a^2+||b||^2<=eta/3`.

Thus `||h||^2>=1-eta/3>=1/2`. The z components give

`|q_j(h)|<=eta+6|a b_j|`

`<=eta+3(a^2+b_j^2)<=2eta<=1/(192N)`.

By the preceding rounding argument the Boolean instance must be satisfiable. Contraposition proves the promised NO-case lower bound.

The coefficients need not be exponentially small, and the obstruction is not merely a question of exact equality at unattainable numerical precision. The gap is inverse polynomial. If a bounded polynomial normalization of F is desired, both the coefficient norm and the reciprocal normalized gap remain polynomial in the original instance size.

## Interpretation and limits

If a fixed unobserved subspace L makes a smooth target affine on every corresponding observation fiber, then every direction in L is a globally affine direction. The reduction therefore obstructs a generic efficient recognizer or optimizer for this particular conditional-affine representation, even at degree three and after complete coefficient acquisition.

It does not prove that all adaptive polynomial sensing is hard. It does not prove an optimal query lower bound for the constructed cubic. A single affine direction alone need not save a total observation: observing its complement and then the remaining affine scalar can still use every input dimension. Nor does the reduction establish hardness of a statistically averaged approximate representation under an arbitrary alternative error criterion. The quantitative result specifically concerns global directional curvature, measured by its Gaussian L2 norm over base points.

The Hermite family in the companion construction avoids this discovery problem by declaring its context/response split and feature layout, then learning only its unknown finite coefficients. It should not be presented as having discovered an arbitrary cubic factorization.

## Primary-source relation

Hillar and Lim, Most tensor problems are NP-hard (JACM, 2013), proves broad hardness of tensor eigenvalue, singular-value, rank and approximation tasks, including symmetric cases. Its primary abstract was read. The reduction above is provided in full rather than relying on a loosely matched tensor-hardness theorem:

https://arxiv.org/abs/0911.1393

This is a scope-specific application and elementary proof, not a claim of historical novelty for cubic singularity hardness.

## Executable algebra

`check_cubic_hardness.py` enumerated all 256 subsets of the eight distinct three-variable clauses. It checked 2048 assignment encodings, 1024 satisfying affine directions, and 256 exact central-second-difference identities against a separately expanded sparse cubic representation. All passed. An explicit unsatisfiable 40-dimensional cubic with 88 monomials and coefficients bounded by 3 is saved in `cubic_hardness_example.json`. Its inverse-polynomial lower bound comes from the proof above, not from a numerical search over directions.
