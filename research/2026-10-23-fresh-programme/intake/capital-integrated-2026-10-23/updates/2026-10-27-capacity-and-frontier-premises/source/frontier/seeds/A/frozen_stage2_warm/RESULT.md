# Warm continuation: a quartic obstruction and a fixed-output global reformulation

27 October 2026. **The all-copy Werner target remains unresolved. No negative witness for a tensor power of the specified Werner state is supplied.** Stage 1 and its frozen copy were preserved. This continuation gives an exact obstruction to extending the block-zero geometry using only generic positivity, then constructs an equivalent full-target reachability formulation. Neither the activation principle nor the general separability reformulation is claimed as new: primary precedents are Vollbrecht--Wolf and Clarisse. The explicit calculations below are reconstructed and checked here; historical priority is unestablished.

Let \(\rho=(2I-F_3)/15\), \(K=I-\Omega_3\Omega_3^*/2\). Thus \(\rho^\Gamma=(2/15)K\). The fixed target is \(q_n(C)\ge0\) for all finite \(n\) and arbitrary complex matrices of rank at most two.

## 1. Strong opposition to the live block-zero route

The stage-1 full Hessian identity extends algebraically to any base Hermitian quadratic form
\[
 q_B(Z)=\langle\operatorname{vec}Z,B\operatorname{vec}Z\rangle,
 \quad R=B^\Gamma,
\]
with the same vectorization and crossed contraction. Define its one-qutrit extension
\[
 Q_B(C)=\langle\operatorname{vec}C,(K\otimes B)\operatorname{vec}C\rangle
       =\sum_{i,j=0}^2q_B(C_{ij})-\tfrac12q_B\Big(\sum_i C_{ii}\Big),
\tag{1}
\]
with physical factors regrouped. We prove a particularly strong local statement when \(B,R\succ0\), then give an exact negative rank-two matrix for that same extended form.

### Local theorem

For every \(N\) and every \(B,B^\Gamma\succ0\) on \(\mathbb C^N\otimes\mathbb C^N\), every point of
\[
 \mathcal M=\{P_E\otimes uv^*: E\in\operatorname{Gr}(2,3),\ u,v\ne0\}
\tag{2}
\]
is a critical zero and a local minimum of \(Q_B\) on the complex rank-two variety. Near this family the zero set is the smooth manifold (2), of real dimension \(4N+2\); the Hessian kernel is exactly its tangent. A single positive neighborhood radius works around the compact family \(\mathcal M_1\) with \(\|uv^*\|_F=1\). This theorem concerns the auxiliary form (1), not the unresolved tensor-power form.

**Proof.** Use a first-site unitary to take \(E=\operatorname{span}(e_0,e_1)\), and normalize \(u,v\). Factor \(C_0=\operatorname{diag}(uv^*,uv^*,0)=U_0V_0^*\). Every rank-two tangent is represented by
\(H=XV_0^*+U_0Y^*\). Stage 1's identity, with its identical algebra, gives the quadratic coefficient
\[
 \mathcal H=\tfrac12q_B(H_{00}-H_{11})+q_B(H_{01})+q_B(H_{10})
 +\sum_{a=0}^1\langle w_a,Rw_a\rangle,
 \quad w_a=x_{2,a}\otimes v-u\otimes y_{2,a}.
\tag{3}
\]
Because \(B,R\succ0\), this vanishes precisely when the three displayed upper-block matrices vanish and every \(w_a=0\). The latter means \(x_{2,a}=c_au\), \(y_{2,a}=c_av\). Thus the kernel consists exactly of upper blocks \(H_{00}=H_{11}=T\), \(H_{01}=H_{10}=0\), where \(T\) is tangent to the nonzero rank-one variety at \(uv^*\), together with the four real plane-rotation directions \(H_{2a}=c_a uv^*\), \(H_{a2}=\bar c_a uv^*\). These are precisely the tangents of (2). The rank-one variety has real dimension \(4N-2\), and \(\operatorname{Gr}(2,3)\) has dimension four.

All members of (2) are critical zeroes by the first-site contraction, exactly as in stage 1. The Hessian is positive on a normal complement. Adapted local coordinates and Taylor's integral formula therefore establish local nonnegativity and the local zero set, not merely second-order stability. Compactness of \(\mathcal M_1\) gives a common radius by a finite subcover. More quantitatively, if \(B,R\succeq\mu I\), (3) dominates \(\mu\operatorname{dist}(H,T\mathcal M)^2\): the upper terms are the ordinary squared normal distance, and writing \(x=cu+x_\perp\), \(y=dv+y_\perp\) gives \(\|x\otimes v-u\otimes y\|^2=|c-d|^2+\|x_\perp\|^2+\|y_\perp\|^2\), which dominates the corresponding normal distance. QED.

### Exact strictly-PPT counterexample to the global extension

On the remaining local space \(\mathbb C^3\otimes\mathbb C^2\), use \(P_\pm=(I\pm F_3)/2\), \(P=\Omega_2\Omega_2^*/2\), \(Q=I_4-P\). Define
\[
 \sigma_6=\frac{8P_-\otimes P+P_+\otimes(P+3Q)}{84},
 \qquad \sigma_{\rm mix}=\tfrac9{10}\sigma_6+\tfrac1{10}I_{36}/36,
 \qquad B=\sigma_{\rm mix}^\Gamma.
\tag{4}
\]
The state \(\sigma_6\) is the normalized local qubit compression of Vollbrecht--Wolf's qutrit universal activator. Positivity and trace one follow directly from the displayed orthogonal projectors. Its partial transpose is
\[
 \sigma_6^\Gamma=\frac1{56}(I-P_3)\otimes(I+F_2)
                 +\frac1{14}P_3\otimes(I-F_2)\succeq0,
\tag{5}
\]
where \(P_3=\Omega_3\Omega_3^*/3\). Consequently \(B,B^\Gamma\succeq I/360\). The local theorem applies to **every** normalized repeated rank-one block zero with a uniform radius.

Nevertheless, \(Q_B\) is negative on rank two. Index its rows and columns by triples \((i,j,a)\in\{0,1,2\}^2\times\{0,1\}\). Define two-column integer matrices by
\[
 (U_0)_a=|a,2,0\rangle,\quad
 X_a=\sum_{i=0}^2|i,i,a\rangle,\quad
 Y_0=\sum_i|i,i,1\rangle,\quad Y_1=-\sum_i|i,i,0\rangle,
 \quad V_0=U_0.
\]
For \(C(t)=(U_0+tX)(V_0+tY)^*\), direct rational contraction gives the **exact** polynomial
\[
 \boxed{Q_B(C(t))=\frac{1409}{5040}t^2-\frac{73}{840}t^4.}
\tag{6}
\]
The cubic coefficient is zero. The factor Gram matrices both equal \((1+3t^2)I_2\), so the matrix has rank exactly two for every real \(t\), with equal nonzero singular values. At \(t=2\), \(Q_B=-49/180<0\). Its norm-square is 338; the normalized value is \(-49/60840\).

This explicitly opposes the idea that positive crossed operators, lower-copy positivity, all block-zero local minima, or even a uniform local radius around that entire family suffice for a global induction. Here the base form is positive **on every matrix**, a stronger premise than lower-copy rank-two positivity. Its qutrit extension still has a distant negative rank-two point. The negative example is for \(K\otimes\sigma_{\rm mix}^\Gamma\), **not** \(K^{\otimes n}\), so it does not refute the Werner candidate. A successful argument must use the special tensor-power structure beyond these generic positivity and local-geometry properties.

The same integer factors were also tested against the actual target, embedding the final qubit into a qutrit. In that case the exact identity is
\[
 q_3(C(t))=6t^2+\tfrac{33}{2}t^4\ge0\quad\text{for every real }t.
\]
The quadratic coefficient from the stage-1 normal form is \(3/2+2+1+3/4+3/4=6\). The leading matrix factors as \(D=|\Omega_3\rangle\langle\Omega_3|\otimes(E_{01}-E_{10})\), with the first Bell vector internal to each party; hence its coefficient is \(q_2(|\Omega_3\rangle\langle\Omega_3|)q_1(E_{01}-E_{10})=(33/4)2=33/2\). A common diagonal sign symmetry fixes \(C_0,D\) and negates the tangent, so the cubic vanishes. Thus the auxiliary negative path decisively fails as a proposed Werner witness; substituting a PPT activator for an unacquired Werner-power output changes the sign.

## 2. A full-target fixed-output object

The opposition suggested a different object: the four coefficients of states reachable from Werner powers by arbitrary local filters into \(\mathbb C^3\otimes\mathbb C^2\) on each side. This retains every rank-two witness.

For \(m\ge0\), take arbitrary complex filters \(A,B:\mathbb C^{3^m}\to\mathbb C^3\otimes\mathbb C^2\). They may be rescaled to Kraus contractions without changing any sign. Set
\[
 s=(A\otimes B)\rho^{\otimes m}(A^*\otimes B^*).
\]
Apply the local twirl \((U_3\otimes V_2)_A\otimes(U_3\otimes\bar V_2)_B\). Its output is uniquely
\[
 \mathcal T(s)=aP_-\otimes P+bP_-\otimes Q+cP_+\otimes P+dP_+\otimes Q,
 \qquad a,b,c,d\ge0.
\tag{7}
\]
Define \(\ell(a,b,c,d)=-3a+9b-2c+6d\). The twirl preserves the functional \(\operatorname{Tr}[s(\rho\otimes W_2)]\), where \(W_2=I_4/2-P\), and
\[
 \operatorname{Tr}[s(\rho\otimes W_2)]=\ell/10.
\tag{8}
\]

**Complete acquisition map.** Let \(\xi_0=\sum_{i,j}|i,i\rangle_A|j,j\rangle_B\otimes(|0,1\rangle-|1,0\rangle)\), with norm-square 18, and \(\xi=\xi_0/\sqrt{18}\). For every rank-two \(C\) at \(n=m+1\) copies, write
\(C=u_0v_1^*-u_1v_0^*\). Splitting the first physical coordinate, define
\[
 A^*|i,a\rangle=(u_a)_i,\qquad B^*|j,b\rangle=(v_b)_j.
\]
Then \(\operatorname{vec}C=\sqrt{18}(I\otimes A^*\otimes I\otimes B^T)\xi\). Local Bell contraction gives
\[
 \langle\xi,(\rho^\Gamma\otimes s^\Gamma)\xi\rangle
  =\frac19\operatorname{Tr}[s(\rho\otimes W_2)]=\ell/90.
\]
Therefore
\[
 \boxed{q_{m+1}(C)=(15/2)^{m+1}\ell/5.}
\tag{9}
\]
Conversely, every such pair of filters defines a rank-at-most-two \(C\) by this same contraction. There is no support restriction or approximation. Every complex coefficient is included, and the transpose on Bob's filter is essential.

Let \(\mathcal C_m\) be the convex cone generated by the four-vectors (7), and \(\mathcal C_\infty=\overline{\bigcup_m\mathcal C_m}\). The cones increase: append local \(\langle0|\) filters on an unused copy, obtaining a positive scalar multiple of the old output. Convex mixing adds no negative sign unavailable to some branch. Thus the original full target is equivalent to
\[
 \boxed{\ell\ge0\quad\text{on }\mathcal C_\infty.}
\tag{10}
\]
This is a constant-dimensional output representation, **not** an acquired finite-dimensional recursion: the filters have \(6\times3^m\) entries. No closure rule determining \(\mathcal C_{m+1}\) from only the four numbers at level \(m\) is proved. Twirling early discards coherent information required by later filters.

## 3. The PPT outputs can be uniformly separated from the PPT boundary

A symmetric state (7) has trace \(3a+9b+6c+18d\). In addition to coefficient nonnegativity, PPT is equivalent to
\[
 a+c\le3(b+d),\quad a+b\le2(c+d),\quad 3b+2c\le a+6d.
\tag{11}
\]
The four sector eigenvalues of its partial transpose are
\[
 (a+b+c+d)/4,\quad(-a+3b-c+3d)/4,\quad
 (-a-b+2c+2d)/2,\quad(a-3b-2c+6d)/2.
\]
These constraints permit negative \(\ell\), as (4) already demonstrates.

There is an explicit **separable** normalized state \(z\), freely preparable, with
\[
 (a_z,b_z,c_z,d_z)=(1/16,1/144,1/32,1/32),\quad
 \ell(z)=0,\quad z\succeq I/144,\quad z^\Gamma\succeq I/192.
\tag{12}
\]
To construct it, average the twirls of these two product states across Alice:Bob:

1. \(\alpha=(|00\rangle+|11\rangle)/\sqrt2\), \(\beta=(|01\rangle-|10\rangle)/\sqrt2\). Their coefficients are \((1/12,0,0,1/24)\).
2. \(\alpha=|00\rangle\), \(\beta=(|00\rangle+|10\rangle)/\sqrt2\). Their coefficients are \((1/24,1/72,1/16,1/48)\).

These are product states between the parties; internal local entanglement is allowed. Each twirl is a mixture of local unitaries. The partial-transpose eigenvalues of their average are \(19/576,1/192,1/36,1/12\), proving (12).

Now suppose a normalized reachable output \(s\) has \(\ell(s)<0\). Let
\[
 t=1/386,\qquad \tau=(1-t)z+ts.
\]
Since \(\|s^\Gamma\|_{op}\le\|s^\Gamma\|_F=\|s\|_F\le1\),
\[
 \tau\succeq I/288,\qquad
 \tau^\Gamma\succeq\big((1-t)/192-t\big)I=I/384,
 \qquad \ell(\tau)=t\ell(s)<0.
\tag{13}
\]
Mixing the successful filter output with a freely prepared separable state is a stochastic LOCC operation; adjust the classical branch weight for the filter's nonzero success probability. No entangled auxiliary resource is assumed free. A Haar twirl can be implemented exactly as a finite convex combination on the particular state by finite-dimensional Caratheodory. Approximation can also preserve all conclusions after choosing a slightly smaller mixing parameter to leave slack above the stated eigenvalue bounds.

Consequently the full target fails **if and only if** some finite Werner power can produce, by stochastic LOCC, a symmetric state on \(6\times6\) satisfying
\[
 \tau\succeq I/288,\qquad \tau^\Gamma\succeq I/384,\qquad\ell(\tau)<0.
\tag{14}
\]
For the reverse implication, append one fresh Werner copy and use the fixed local Bell/antisymmetric test above. A negative mixture expectation has a negative branch, giving an ordinary rank-two witness. The positivity gaps and output dimension in (14) are independent of copy number. Success probability and required filter description remain uncontrolled. No reachability or impossibility theorem deciding (14) is established.

### A certificate obstruction at the freely preparable boundary

The fixed operator \(\mathcal W=\rho\otimes W_2\) is block-positive: for every product vector across the two parties, the \(m=0\) acquisition map reduces its expectation to the one-copy rank-two inequality. Its partial transpose is block-positive as well, by partial conjugation of the product vectors. The ensemble constructing \(z\) consists entirely of zero product vectors for \(\mathcal W\), and \(z,z^\Gamma\succ0\).

It follows directly that both \(\mathcal W\) and \(\mathcal W^\Gamma\) are optimal against subtraction of a positive operator. If \(H\succeq0\) and \(\mathcal W-H\) remained block-positive, evaluate on every zero product vector and average: \(\operatorname{Tr}(Hz)=0\). Since \(z\succ0\), this forces \(H=0\). Apply the same argument to \(z^\Gamma\) for the partial transpose. Also \(\mathcal W\) cannot be decomposable: an expression \(\mathcal W=H+J^\Gamma\), \(H,J\succeq0\), would imply \(0=\operatorname{Tr}(\mathcal Wz)=\operatorname{Tr}(Hz)+\operatorname{Tr}(Jz^\Gamma)\), forcing the nonzero witness to vanish. This is consistent with the established nondecomposable-witness formulation; it blocks a PPT-only certificate, not every possible coherent-filter invariant.

## 4. Verification, overlap, and remaining obligation

`activation_path_exact.py` uses standard-library rational arithmetic. It checks every entry of (5), trace one, the full polynomial (6), and the negative point at \(t=2\). An initial factor-of-two error in converting sector eigenvalues to unnormalized \(I\pm F\) terms was caught by this entry check and corrected; the retained receipt has zero entry residual. The factorization proves rank two independently of numerical rank. The script runs with `python -O`.

`reachability_check.py` uses exact complex SymPy arithmetic. One- and two-copy filters independently reconstruct both sides of (9), including Bob's transpose, with zero residual. It also constructs both product inputs for (12) and computes their four coefficients before taking the average. These are checks of explicit identities; the all-copy coverage is the proof of the acquisition map, not sample coverage. `activation_exact.py` retains the preceding direct qutrit-output reconstruction of the known activator, before its qubit compression.

Primary overlap checked: [Vollbrecht--Wolf, quant-ph/0201103v2](https://arxiv.org/pdf/quant-ph/0201103), whose symmetric activator supplies the starting point of (4); [Clarisse, quant-ph/0510035v3](https://arxiv.org/html/quant-ph/0510035v3), particularly its activation discussion and separability reformulation. Their general principles are prior theory. The precise local-geometry opposition, acquisition constants, and strict-PPT dilution are derived above without assuming the all-copy target. No exhaustive novelty determination or external audit is claimed.

The surviving obligation is **target-specific reachability**: either prove (10)/(14) impossible for every finite Werner power using an invariant that retains coherent local-filter information, or supply explicit reachable filters crossing \(\ell=0\). Replacing that acquisition problem with arbitrary PPT states is invalid, because the exact activator is already a counterexample to such a relaxation. Returning to only the Hessian is also insufficient, as (6) shows even under stronger base positivity. The all-copy theorem and an admissible negative witness remain absent.
