# The 11/13 exposed boundary seed is polyconvex

The substantive continuation resolves a question left open in the supplied
case. Put

\[
 F_0(A)=F_{11/13,28/13}(A)
       =T^2+\frac{60}{13}q^2+\frac{44}{13}qX .
\]

**Theorem 1.** This polynomial is polyconvex on all real 2 by 2 matrices.
An explicit scalar minor-support rule is

\[
 \lambda(A)=\frac{23}{5}X(A)+\frac{9488}{715}\det A.                 \tag{1}
\]

For every real base matrix \(A\) and every real increment \(H\),

\[
 F_0(A+H)-F_0(A)-DF_0(A):H-\lambda(A)\det H\ge0.                 \tag{2}
\]

This is a global supporting-plane certificate. It is not a conclusion from
failure to find a non-polyconvexity witness, and it does not restrict the
convex minor lift to a polynomial.

**Theorem 2.** Let

\[
 \beta(u)=\frac{1-3u^2}{1+3u^2},\qquad
 r(u)=4-\frac{12u}{1+3u^2}.
\]

For every real \(u\) with

\[
 |u-1/6|<2^{-54},                                               \tag{3}
\]

the quartic \(F_{\beta(u),r(u)}\) is polyconvex, with the actual continuing
support rule

\[
 \lambda_u(A)=\frac{23}{5}X(A)+
 \left(4r(u)+8-\frac{92u}{5(1-3u^2)}\right)\det A.               \tag{4}
\]

The radius is deliberately conservative. No wider interval follows from
the numerical searches.

Combined with the initial tranche's full-cone exposed-ray theorem, (3)
is an arc of exposed polyconvex (hence quasiconvex) rays on the curved
rank-one-convex boundary. The separately inherited arc about \(u=1/30\)
remains non-polyconvex and quasiconvex. Thus this same exposed boundary
contains certified open arcs of both kinds. The accepted heat certificate
at the 11/13 seed remains valid; ordinary polyconvexity now accounts for its
quasiconvexity.

## A complete matrix test behind the acquisition

For a positive homogeneous quartic \(F\), define, at a nonzero matrix \(R\),

\[
 S_F(R)=\frac12D^2F(R)-\frac{DF(R)\otimes DF(R)}{4F(R)}.           \tag{5}
\]

Quartic polarization gives

\[
 \begin{split}
 F(A+tR)-F(A)-tDF(A):R-\lambda t^2\det R
 =t^2\left[\frac12D^2F(R)[A,A]-\lambda\det R
              +tDF(R):A+t^2F(R)\right].
 \end{split}
\]

Minimizing the bracket over the real scalar \(t\) shows that a minor support
at \(A\) exists exactly when

\[
 A^\mathsf T S_F(R)A-\lambda\det R\ge0
 \quad\hbox{for every nonzero }R.                              \tag{6}
\]

For rank-one-convex \(F\), the determinant-zero constraints in (6) hold.
Indeed \(D^2F(R)\) is PSD at a rank-one \(R\), and Euler's identity and
Cauchy--Schwarz in that PSD form give
\[
 S_F(R)\succeq\frac16D^2F(R)\succeq0 .
\]

Thus a positive rank-one-convex quartic is polyconvex if and only if

\[
 \frac{S_F(R_+)}{\det R_+}
 -\frac{S_F(R_-)}{\det R_-}\succeq0
 \quad
 (\det R_+>0,\ \det R_-<0).                                    \tag{7}
\]

For sufficiency, every base \(A\) then has overlapping lower and upper scalar
support intervals. They are finite because one fixed direction of each
determinant sign bounds them. Choose any scalar in the overlap, apply (6),
and use the convex supremum construction below. Necessity follows from
the same support cuts. This derivation was used as the strongest ordinary
comparison, not as a free scalar-selection oracle.

The numerical test full_pc_search.py uses a five-parameter representation
of nonsingular direction pairs modulo their scales and simultaneous output
rotations. The executed search bounds logarithmic singular values by 4 and
uses finitely many starts. It minimizes the smallest eigenvalue in (7),
thereby optimizing the base matrix exactly for each proposed pair. It recovers the supplied non-polyconvex B1 mechanism but
did not produce a violation at B0. Its finite searches do not establish
polyconvexity; they led to the actual rule (1), which is checked globally.
No priority claim is made for the support-cut criterion.

## The serious failed support rule

The acoustic zeros force a prospective quadratic rule

\[
 \lambda(A)=L X(A)+\left(\frac{216}{13}-\frac{8L}{11}\right)\det A
\]

to take the correct value at an acoustic base. Merely imposing this local
condition is insufficient.

The simple choice \(L=4\) passes the local acoustic factorization and has a
strict positive lifted matrix at the acoustic zero. Nevertheless it fails
globally. For

\[
 A=\begin{pmatrix}0&10\\9&0\end{pmatrix},\qquad
 H=\begin{pmatrix}1&0\\0&-2/5\end{pmatrix},
\]

its support expression is exactly

\[
 F_0(A+H)-F_0(A)-DF_0(A):H
 -\left(4X(A)+\frac{1960}{143}\det A\right)\det H
       =-\frac{72027}{89375}<0.                               \tag{8}
\]

This is a failed scalar support rule, not a non-polyconvexity witness for
\(F_0\). Changing the actual rule to \(L=23/5\) resolves the global failure.
The failed candidate and exact witness are preserved in
b0_pc_candidate_L4.json and b0_pc_verification.json.

## Proof of the global support

Represent matrices as four-vectors \((a,b,c,d)\). Write

\[
 D=\operatorname{diag}(1,-1,1,-1),\qquad
 E=\begin{pmatrix}
 0&0&0&1\\0&0&-1&0\\0&-1&0&0\\1&0&0&0
 \end{pmatrix}.
\]

Thus \(X(A)=A^\mathsf TDA\) and
\(\det A=A^\mathsf TEA/2\). Set

\[
 B_*=\frac{23}{5}D+\frac{4744}{715}E .
\]

The actual polynomial matrix checked by the certificate is

\[
 C(R)=2F_0(R)D^2F_0(R)
      -DF_0(R)\otimes DF_0(R)
      -4F_0(R)(\det R)B_* .                                   \tag{9}
\]

Its entries are homogeneous of degree six. The exact certificate proves

\[
 C(R)\succeq0\quad\hbox{for every real }R.                     \tag{10}
\]

The defining entries are literal rational coefficients in
b0_pc_certificate.json. The standard-library receiver
verify_b0_pc.py independently reconstructs (9) from \(F_0\) and (1),
rather than accepting saved matrix entries as an oracle.

Here is why its positivity check is global. Left output rotations preserve
\(F_0\) and \(\lambda\). The map \(R\mapsto CR C\), with
\(C=\operatorname{diag}(1,-1)\), preserves both. Column swap preserves
\(F_0\), reverses \(\det R\), and reverses \(\lambda\). These give ordinary
matrix congruences for (9); no spatial wedge-orientation convention is
needed. Scale, rotate, reflect, and swap columns as necessary to obtain

\[
 R=\begin{pmatrix}1&b\\0&d\end{pmatrix},
 \quad 0\le b,\quad b^2+d^2\le1 .
\]

The certificate covers the larger square \(0\le b\le1,-1\le d\le1\).

It uses the acoustic factors

\[
 w=d,\qquad g=b^4-\frac{93}{14}b^2+1
\]

and the explicit kernel

\[
 k=\begin{pmatrix}
 1\\
 63b^3/146-913b/292\\
 455b^3/1606-4777b/3212\\
 196b^2/803-893/803
 \end{pmatrix}.
\]

Let \(Q\) have first column \(k\) and its other columns the last three
standard coordinate vectors. Let \(\Delta\) be 5 by 4, with first column
\((d,g,0,0,0)^\mathsf T\) and its other columns the final three standard
coordinate vectors. The receiver checks the actual rational identity

\[
 Q^\mathsf T C Q=\Delta^\mathsf T M\Delta .                    \tag{11}
\]

The lift \(M\) is strictly positive on

\[
 [25/64,51/128]\ \times[-1/128,1/128].
\]

On the other 84 rectangles of the exact 85-rectangle cover, \(C\) itself is
strictly positive. All 4,193 matrix Bernstein coefficients are verified
strictly positive definite by integer Bareiss elimination after positive
denominator clearing. The cover is checked for containment, disjoint
interiors, and exact total area 2. Nonnegative Bernstein basis functions
prove positivity throughout each box. Identity (11) retains the genuine
null vector at \(d=g=0\). It does not assume a uniform positive margin for
the original singular matrix.

Finally \(F_0(R)>0\) for \(R\ne0\). For example, in Hopf variables,

\[
 F_0=(X+11Z/13)^2+Y^2+\frac{243}{169}Z^2 ,
\]

and \(T^2=X^2+Y^2+Z^2\). Quartic polarization and completion of a scalar
square give the exact identity

\[
 \begin{split}
 &F_0(A+H)-F_0(A)-DF_0(A):H-\lambda(A)\det H\\
 &\quad =
 \frac{A^\mathsf T C(H)A}{4F_0(H)}
 +\frac{(DF_0(H):A+2F_0(H))^2}{4F_0(H)}
 \quad (H\ne0).
 \end{split}                                                  \tag{12}
\]

Both terms are nonnegative by (10). The \(H=0\) case is immediate.
This proves (2).

## An unrestricted convex minor lift

For completeness an actual convex representation follows from the supports:

\[
 \begin{split}
 G(A,s)=\sup_B\{&
 F_0(B)+DF_0(B):(A-B)\\
 &+\lambda(B)[s-\det B-\operatorname{cof}B:(A-B)]\}.
 \end{split}                                                  \tag{13}
\]

Every term is affine in \((A,s)\), so \(G\) is convex. Equation (2) gives
\(G(A,\det A)=F_0(A)\), with equality supplied by \(B=A\).
It is finite everywhere: choose \(Y\) with
\(\det Y=s-\det A\). The point \((A,s)\) is the average of
\((A+Y,\det(A+Y))\) and \((A-Y,\det(A-Y))\), which bounds the supremum in
(13) by a finite average of two values of \(F_0\). The support at \(B=0\)
also gives \(G\ge0\). Thus this is polyconvexity with an arbitrary finite
convex minor lift, not convexity of a guessed polynomial lift.

## Exact continuation and the radius

continue_b0_pc.py acquires actual rational functions for every coefficient
of the rule (4), the 4 by 4 support matrix, the polynomial kernel, and the
5 by 5 lift. Generic division gives (11) as a rational-function identity.
Every coefficient denominator is checked nonzero at \(u=1/6\); the matrices
there match the literal verified certificate exactly. The defining family
is saved in b0_pc_continuation.json.

The same finite strict Bernstein inequalities therefore persist on an
open interval. quantify_b0_pc_arc.py makes the interval explicit. At the
center it uses the exact eigenvalue bound
\(\det A/\operatorname{tr}(A)^{n-1}\) for each of the 4,193 PD coefficient
matrices. The minimum of those positive rational numbers is saved in
b0_pc_verification.json.

For each rational coefficient \(f=p/q\), the quantifier shifts its actual
polynomials to powers of \(z=u-1/6\), with reference radius \(R=1/1000\).
Writing \(p_0=p(1/6)\), \(q_0=q(1/6)\), it computes

\[
 S_q=\sum_{j\ge1}|q_j|R^{j-1},\qquad
 S_f=\sum_{j\ge1}|p_jq_0-p_0q_j|R^{j-1}.
\]

For \(h\le R\) and \(hS_q\le|q_0|/2\),

\[
 |f(u)-f(1/6)|\le h\,2S_f/q_0^2 .
\]

All 160 distinct rational functions needed by the matrices, kernel,
factors, and support rule are bounded. Bernstein conversion amplifies each
entry's summed coefficient error by at most \(3^6=729\) on the fixed cover:
the \(b\) intervals lie in \([0,1]\), and the \(d\) intervals satisfy
\(|d_{\rm left}|+\text{width}\le3\). Matrix sizes are at most 5.

The final dyadic choice \(h=2^{-54}\) keeps every denominator nonzero and
the operator change of every Bernstein coefficient matrix at most half
its verified positive eigenvalue lower bound. All comparisons are exact
fractions, saved in b0_pc_arc_radius.json. No sampling enters this radius.
This proves Theorem 2.

## A separate explicit non-polyconvex interval

The opposite-cut calculation also yields a parameter-uniform obstruction,
independent of the new polyconvex certificate. For every

\[
 0<u\le1/26
\]

take the actual base and directions

\[
 A=I,\qquad
 R_+=\begin{pmatrix}0&1\\-2u&0\end{pmatrix},\qquad
 R_-=\begin{pmatrix}1&0\\0&-2\end{pmatrix}.
\]

Their determinant signs are strictly opposite. The positive cut requires
\(\lambda\le U(u)=24-68u/(1+3u^2)\). The negative cut requires a lower bound
whose excess over \(U\) is exactly

\[
 -\frac{4(2817u^4-2733u^3+1371u^2+u-2)}
 {(1+3u^2)(147u^2-192u+97)}>0.                                \tag{14}
\]

The numerator polynomial has only negative Bernstein coefficients on
\([0,1/26]\):

\[
 -2,\quad -207/104,\quad-2221/1352,\quad
 -70021/70304,\quad-37821/456976.
\]

The quadratic denominator factor has positive Bernstein coefficients
\(97,1213/13,60727/676\). Therefore the gap is strictly positive throughout
the whole interval; no parameter sampling is a premise.

At \(u=0\), use \(R_+=[0,1;-1/100,0]\) instead. The exact support bounds
are \(602/25\) above and \(2336/97\) below, with positive gap \(6/2425\).
Hence the whole closed interval \(0\le u\le1/26\) is non-polyconvex.
nonpc_interval.py reconstructs the actual cuts and checks all interval
signs, with the literal data in nonpc_interval_result.json.

This proves non-polyconvexity, not quasiconvexity of that whole interval.
Only the already admitted quasiconvex subsets, including the endpoint
\(F_{1,4}\) and the B1 neighborhood, receive both conclusions.

## Reproduction and remaining scope

The complete center verification requires only the Python standard library:

    python3 verify_b0_pc.py

The actual rational continuation and radius use the locally installed SymPy:

    python3 continue_b0_pc.py
    python3 quantify_b0_pc_arc.py

The separate interval obstruction is reproduced with:

    python3 nonpc_interval.py

The center replay took about 1.5 seconds in the local runtime. The generic
continuing family took about 20 seconds to reconstruct and the exact radius
about 1 second. These are costs of these specific artifacts, not acquisition
complexity guarantees.

The initial exposed-ray theorem and the supplied non-polyconvex B1 result
are preserved. This tranche changes the B0 polyconvexity status from
unclassified to proved polyconvex, establishes (3), and proves (14) on an
explicit interval. It does not classify
the polyconvexity transition along the whole curved boundary. The full
quasiconvexity question outside the admitted arcs, completeness of either
the quadratic support rule or the heat correction, gradient microstructure
rigidity, and a general Morrey result remain unresolved. Historical priority
of this explicit certificate has not been established.
