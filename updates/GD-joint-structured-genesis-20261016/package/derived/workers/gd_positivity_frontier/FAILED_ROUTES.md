# Decisive rejected routes and their scope

1. **Angular minimization does not supply an isotropic lower comparison.**
   At r=1, with complex gradient variables z=(a+d+i(c-b))/2 and
   ζ=(a-d+i(c+b))/2, exact algebra gives
   J1=2(|z|4+|ζ|4-|z|2|ζ|2+Re(z conjugate ζ)(|z|2-|ζ|2)).
   Minimizing the last angular phase gives the objective isotropic envelope
   2(p4+q4-p2q2-pq|p2-q2|), p=|z|, q=|ζ|.
   Along the rank-one line I+v e11 its left derivative at v=0 is 5 and its
   right derivative is 3. The envelope is therefore not rank-one convex.
   It cannot enter an isotropic rank-one-convex-to-quasiconvex theorem.
   The discarded phase carries a linear null cancellation whose average
   vanishes for the actual periodic gradient; replacing it by an absolute
   value loses that cancellation. This rejects this specific lower-envelope
   architecture, not all complex-gradient methods.

2. **A coarse sampled moment linear program missed the small-scale law.**
   One diagnostic sampled 100001 integer/8 matrices and imposed mass, mean
   diagonal entries and mean determinant, using simultaneous off-diagonal
   sign pairs. It returned the trivial I law with objective 2. This is a
   finite-sample optimum only. It is contradicted as a continuum conclusion
   by the exact four-atom family in PROOF.md. The family was subsequently
   derived analytically by matching the rare diagonal determinant with
   paired shears. The script and diagnostic output are preserved to avoid
   silently dropping the failed search.
   This used an existing local SciPy 1.18.1 directory; nothing was installed.

3. **The four-atom law cannot be promoted to a gradient counterexample.**
   Its zero mean, zero determinant and local plane equations hold exactly,
   but its support reduces by invertible left/right maps to diagonal
   matrices. Classical diagonal gradient-Young-measure structure and the
   independently audited rank-one convexity exclude its realization as a
   homogeneous gradient Young measure. Its negative energy diagnoses the
   information lost by a minor-moment/Gram relaxation.

4. **Averaging the successful characteristic planes has no proved budget.**
   Exact torus Haar independence produces the moment factorization in the
   new restricted theorem. General Hessian fields do not have that product
   structure. No positive mixture of plane decompositions with matching
   cubic and quartic costs was constructed. Equation (17) in PROOF.md is
   the precise remaining U=0 obligation.

No Fourier optimization was run. No tiny-tube constant was improved.
