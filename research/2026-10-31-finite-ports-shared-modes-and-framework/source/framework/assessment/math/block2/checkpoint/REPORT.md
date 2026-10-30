# Exceptional face at s=1/3: canonical cubic modes, sharp ROC boundary, and a compatible heat attack

The central question—whether every globally rank-one-convex polynomial in the stated fixed-leading face is quasiconvex—remains unresolved in this tranche. The result retained here is a canonical representation of all four exceptional cubic modes, an explicit sharp rank-one minimization with a finite exact membership operation for all block-diagonal lower quadratics, and a compatible QC construction for a two-real-dimensional subfamily of the exceptional modes. The natural inherited heat construction has a provable gap from the ROC boundary; its failure is not a QC counterexample.

All calculations use only the frozen packet and local symbolic computation. `verify.py` independently reconstructs the identities below using the already installed SymPy; its complete passing output is `verification.txt`. No field search or passing finite collection of fields is used to assert QC.

## 1. Coordinates and normalization

Write

    x=(a+d,c-b),  y=(a-d,c+b),  eta(y)=(y1^2-y2^2,2y1y2),
    J(y1,y2)=(-y2,y1).

Then |x|^2-|y|^2=4 det A, and

    3 F_(1/3)(A) = F0(x,y) = 2|x|^2|y|^2+|y|^4.

Use P=3p throughout the derivations: multiplying the entire polynomial by three preserves ROC and QC. A matrix increment is rank one precisely when its coordinate increment (u,v) satisfies |u|=|v|. Hence it suffices to use independent unit vectors u,v.

At such an increment, the acoustic kernel is (2u,-v). The cubic condition is therefore

    (2 x·partial_x-y·partial_y) C = 0 on |x|^2=|y|^2.       (1)

## 2. All eight cubic modes and a unique normal form

Every cubic satisfying (1) has exactly the form

    C(x,y)=x·[tau |y|^2+M eta(y)]
               +(beta·y)(|x|^2+|y|^2),                    (2)

where tau,beta are arbitrary real two-vectors and M is an arbitrary real 2 by 2 matrix. These are eight independent parameters. The tau,beta terms are precisely translations, since

    DF0:(Vx,Vy)=4(Vx·x)|y|^2
                       +4(Vy·y)(|x|^2+|y|^2).

Thus, after a unique argument translation and adjustment of quadratic and affine terms, every candidate has the form

    P=F0+C_M+Q+affine,       C_M=x·M eta(y).                (3)

This is an explicit realization of the four additional modes, not a claim that their existence or dimension was newly discovered.

Proof of completeness. The cubic polynomial in (1) is divisible by N=|x|^2-|y|^2: a polynomial vanishing on this nonsingular real quadratic hypersurface is divisible by its irreducible defining polynomial. This can also be checked directly by division in x1 and varying the other three real coordinates on an open set. Write C as its components C_(k,3-k) in x/y degree. The operator in (1) acts by 3k-3. If its quotient by N is alpha·x+gamma·y, its x-degree-one component is -|y|^2 alpha·x, but the operator's x-degree-one component is zero. Hence alpha=0. The degree-three and degree-zero components give C_(3,0)=0 and C_(0,3)=|y|^2(gamma·y)/3; degree two gives C_(2,1)=|x|^2(gamma·y)/3. The remaining C_(1,2) is unrestricted. Splitting each quadratic in y into trace and traceless parts proves (2). The exact receiver also obtains rank 12 of the full 20-cubic acoustic map and rank 8 of this basis.

## 3. Explicit sharp lower-quadratic ROC condition

For independent unit u,v, put

    w=eta(v),   y=t v+z Jv,   xi=x+2t u.

Direct differentiation gives

    F0''(x,y)[(u,v),(u,v)] = 4|xi|^2+8z^2,
    C_M''(x,y)[(u,v),(u,v)] = 2 xi·Mw+4z u·MJw.

Consequently

    P''[(u,v),(u,v)]
      =4|xi+Mw/4|^2+8[z+(u·MJw)/4]^2
         +2Q(u,v)-|Mw|^2/4-(u·MJw)^2/2.                 (4)

This is a complete square identity, including every acoustic direction: no pseudoinverse or near-root cutoff is involved. It proves the exact equivalence

    P is globally ROC
      iff Q(u,v) >= |M eta(v)|^2/8
                         +(u·MJ eta(v))^2/4             (5)

for every pair of unit vectors u,v. A failed inequality has the explicit minimizing background

    x=-M eta(v)/4,
    y=-(u·MJ eta(v)) Jv/4.                               (6)

This establishes necessity as well as sufficiency. The previous general Schur elimination is credited to `math/quadratic_boundary/PROOF.txt`; (4) evaluates it in elementary coordinates for this exceptional geometry.

### A finite exact membership operation for all block-diagonal quadratics

For

    Q(x,y)=x^T A x+y^T D y,     A,D symmetric,

define the homogeneous binary quartic matrix

    K(v)=[(v^TDv)|v|^2-|M eta(v)|^2/8] I
                +|v|^4 A-(MJ eta(v))(MJ eta(v))^T/4.    (7)

Equation (5) is equivalent to K(v) being PSD for all v. For a real symmetric 2 by 2 matrix this is equivalent to nonnegativity of its two diagonal entries and determinant. Thus membership is decided by exactly three univariate nonnegativity operations on degrees at most 4,4,8 after v=(1,t). Infinity follows by continuity of the homogeneous forms. This covers all four exceptional cubic modes and all six coefficients of a block-diagonal quadratic, including degenerate boundary points.

`block_membership` in `verify.py` implements this exact operation for rational inputs. It uses square-free decomposition and exact real-root counts, rather than a sampling grid or a positive-definite-only criterion. The receiver checks boundary and below-boundary examples.

For a full Q with cross term 2x^TB y, (5) is still exact, but this tranche does not eliminate both angular variables into a comparably simple finite operation. In particular, (5) is not advertised as a completed effective classification for all ten quadratic coefficients.

### The full sharp isotropic threshold

If Q=nu(|x|^2+|y|^2), and sigma1>=sigma2 are the singular values of M, then (5) is exactly

    nu >= (2 sigma1^2+sigma2^2)/16.                        (8)

Indeed maximize first over u, obtaining (|Mw|^2+2|MJw|^2)/16, then over unit w. Since eta maps the unit circle onto itself and |Mw|^2+|MJw|^2=tr(M^TM), the maximum is (2 sigma1^2+sigma2^2)/16. This is the actual global ROC boundary, not a sufficient large stabilization.

For M=I, the sharp coefficient is 3/16. At the minimizing direction u=e2,v=e1 and background x=-e1/4,y=-e2/4, the rank-one Hessian is 4nu-3/4. In original matrix coordinates these are

    increment R=(1,-1;1,-1)/2,
    background A=(-1,-1;-1,-1)/8.

A coefficient below 3/16 fails ROC, and therefore supplies no separation.

## 4. A compatible QC construction for two exceptional modes

Consider the conformal coefficient subspace

    C_kappa=Re[kappa conjugate(X) Y^2],
    X=x1+i x2, Y=y1+i y2.

It corresponds to M being a scalar times a proper rotation, so both singular values are |kappa|. Rotations of input and output preserve F0 and the isotropic quadratic and can make kappa real and nonnegative. It suffices to give the certificate for kappa=1.

Let f=u1+i u2 be the actual deformation, with complex derivatives

    P=f_zz,  Qc=f_(z conjugate(z)),  R=f_(conjugate(z) conjugate(z)).

The letter Qc here is a complex Hessian coordinate, not the lower quadratic. The compatible real Hessian is

    (h0,h1,h2,h3,h4,h5)
      =(Re(P+2Qc+R), -Im P+Im R, Re(-P+2Qc-R),
        Im(P+2Qc+R), Re(P-R), Im(-P+2Qc-R)).

Define three bilinear complex expressions

    S1=conjugate(X) P+2 conjugate(Y) Qc,
    S2=conjugate(Y) R+conjugate(X) Qc+Y conjugate(Qc),
    S3=conjugate(X) Qc+2Y conjugate(Qc).

The inherited primary closed-form heat correction has the particularly simple exact factorization

    corrected heat density of F0
       =16(|S1|^2+2|S2|^2+|S3|^2).                       (9)

For provenance, this is the s=1/3 specialization, multiplied by three, of the Bruno–Pasqualotto Appendix A primitive replayed in `math/rotational_faces/receive.py`. In original entry coordinates the primitive used here is

    alpha_F=(3T+14D) theta+(9T-6D) zeta,
    theta=-c da-d db+a dc+b dd,
    zeta=-b da+a db-d dc+c dd.

The factorization (9) is the new representation used in this attack; the homogeneous QC theorem and primitive retain their source credit.

For C_1=Re[conjugate(X)Y^2], introduce the closed linear two-form

    Omega_C=-8(a-d) da wedge dc+8(b+c) da wedge dd
                 +8(b+c) db wedge dc+8(a-d) db wedge dd.

It gives the exact compatible identity

    corrected heat density of C_1 = 32 Re(R S3).          (10)

Closure is checked symbolically. It has an explicit global polynomial primitive: alpha_C=(1/3) interior_E Omega_C, with E the radial vector field.

For Q_nu=nu(|x|^2+|y|^2)=2nu T, take the constant closed two-form whose upper-triangular coefficients in the ordered pairs (ab,ac,ad,bc,bd,cd) are

    nu * (-8,-16,0,0,-16,-8).

The corrected quadratic density is exactly 64nu |R|^2. Adding (9) and (10) therefore gives

    16[|S1|^2+2|S2|^2+|S3+conjugate(R)|^2
                                      +(4nu-1)|R|^2].    (11)

The expression is nonnegative precisely under the sufficient condition nu>=1/4. For general kappa the same transported certificate requires nu>=|kappa|^2/4.

This is an actual compatible QC construction. Along ordinary componentwise heat flow of an affine mean plus a periodic perturbation, integration by parts gives minus the uncorrected density as the energy derivative. The pullback of each exact two-form integrates to zero. Hence (11) makes the energy nonincreasing to its affine-mean limit. The periodic/compactly supported approximation argument is the same as in the supplied primary homogeneous certificate, and all correcting forms here are global polynomials. No pointwise minimizing matrix field is asserted to be a gradient. Arbitrary means and amplitudes are covered.

Translations, affine terms, and additional ROC quadratics can be added to this QC family. For the last statement use the ordinary Fourier proof that a quadratic nonnegative on rank-one amplitudes is QC.

## 5. A sharp obstruction even after optimizing the cubic correction

The gap between the actual ROC threshold 3/16 and the certificate threshold 1/4 is not just a loose Young inequality. Fix the primary quartic correction (9), but allow ANY closed linear two-form as the cubic correction and ANY constant closed two-form as the quadratic correction. Then a globally nonnegative pointwise heat density for C_1+Q_nu is possible only if nu>=1/4. Thus optimizing all polynomial quadratic primitives for the cubic cannot close this gap while retaining the primary leading density.

Proof. Average a proposed pair of corrections over the one-parameter simultaneous rotations preserving C_1: if the domain angle is theta, take output angle -3theta. Average also over simultaneous conjugation of X,Y,P,Qc,R. These transformations preserve the leading density, C_1, Q_nu and positivity, and preserve the relevant polynomial and closure classes. The Hessian coordinates P,Qc,R have respective circle weights -5,-3,-1. The averaged quadratic density is therefore

    16(a|P|^2+b|Qc|^2+c|R|^2).

Its integral on compatible periodic fields must equal that of the uncorrected Q_nu density. The Fourier multipliers of P,Qc,R have equal absolute value, giving a+b+c=4nu. At base A=0 the quartic and cubic heat densities vanish, so a,b,c>=0 are necessary.

For the averaged cubic density, charge counting leaves exactly the real parts of these five monomials:

    conjugate(X) Qc R, conjugate(Y) R^2, X R conjugate(P),
    Y Qc conjugate(P), Y R conjugate(Qc).

For example, the first term has output/domain weights (1,3), matching C_1. All three-factor monomials have total output weight at most three and domain weight at most five; invariance under output=-3 domain therefore leaves only weights (1,3) and its conjugate. Enumerating the variables with these weights gives the displayed five monomials. Simultaneous conjugation makes their coefficients real.

Reconstructing the Hessian of C_1 and imposing closure of a general linear two-form gives the COMPLETE family of possible coefficient vectors, in units of 16,

    (2,0,0,4-gamma,gamma),        gamma real.              (12)

`verify.py` solves all 24 linear two-form coefficients and the five density coefficients exactly, including the four closure equations. Equivalently, the allowed two-form is ((gamma-2)/2) Omega_C. The earlier certificate has gamma=4.

For a real epsilon tending to zero through positive values, choose the finite jet/base

    R=1, Qc=epsilon, P=2epsilon^2/(1+epsilon),
    X=-(1+epsilon)/(epsilon(1-epsilon)),
    Y=1/(1-epsilon).

Then exactly S1=S2=0 and S3=-1, so the quartic density is 16. For every fixed gamma, the cubic density from (12) tends to -32: its first monomial tends to -1, while its fourth and fifth monomials tend to zero. The other two coefficients are zero. Thus the quartic-plus-cubic density tends to -16. The quadratic density tends to 16c. Positivity implies c>=1 and therefore 4nu>=1. Equation (11) attains the bound. This proves the obstruction at precisely its stated scope.

This argument uses local compatible Hessian jets to test a proposed pointwise heat certificate. It is NOT a compatible integrated negative-energy field and is NOT a QC violation. It does not exclude a different leading primitive, a nonpolynomial cubic correction, or a non-heat QC proof. It does exclude every closed linear cubic correction and constant quadratic correction with the fixed primary leading primitive.

## 6. Exact remaining frontier and relation to predecessors

The supplied work already gave the exceptional dimension, general Schur elimination, homogeneous QC, and moment-Schur reduction. It explicitly did not classify the extra modes. The additions here are (2)–(4), the exact finite block-diagonal lower-quadratic membership operation (7), the singular-value boundary (8), and the compatible nontranslation QC construction (9)–(11) with its sharp completion obstruction.

A concrete frontier is the family

    P_nu=F0+Re[conjugate(X)Y^2]+nu(|x|^2+|y|^2),
                      3/16 <= nu < 1/4.

Every member is globally ROC. QC in this interval is not established here, including its left endpoint. In the task's original normalization the left endpoint is

    p=F_(1/3)+(1/3)Re[conjugate(X)Y^2]
                           +(1/16)(|x|^2+|y|^2).

A complete positive resolution must cover the other two exceptional cubic directions and all cross quadratic terms as well, or produce an independently admitted ROC candidate and an actual compatible energy violation. None has been acquired in this tranche.

## Reproduction and artifacts

Run `python3 verify.py` from this directory. It checks the entire cubic kernel, rank-one completion, exact boundary membership fixtures, source primitive, complex square factorization, closed cubic correction, constant quadratic correction, and the degenerating-jet identities. `verification.txt` is the captured successful output. `heat_probe.py`, `cubic_heat.py`, `heat_null_modes.py`, `quadratic_heat.py`, and `heat_family_probe.py` retain the exploratory calculations; they are not needed by the independent receiver. One attempted SciPy-assisted direction was abandoned because SciPy is absent; no installation or numerical result was used.

Only `INITIAL.txt`, `packet/MATH_TASK.md`, `packet/SOURCES.txt`, and the named frozen mathematical sources were read. The unrelated sibling eight-mode detector was not imported. No external correctness or historical-priority claim is made.
