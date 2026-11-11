# P1 completed return

Chat: https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2
Question: P1_FULL_ORIGINAL_QUARTIC_AFTER_ROW_DUALITY_PRO_20261111.txt; user 2d4d6d56-f2cd-45fb-bea7-dd48f74536bb; assistant 9cd28da4-e300-5867-a55e-ff7dad606232.

Native reader returned this full final without a truncation flag. Visible activity/helper panels not saved. Four linked individual files were visible but not collected under existing transfer restrictions; no ZIP visible in the response. No database-byte identity claimed.

## Full final

**I have not solved the full original problem.** This continuation establishes a stronger compatible row-defect estimate and a certified procedure for conditional row minimization. It also completes an exact investigation of four compatible families. None supplies the required universal inequality or an actual negative original gap.

The complete proofs, independent checks, exact arithmetic records, and scope statements are saved in:

- :chatgpt-content-reference{index="1"}[ROW_DUALITY_CONTINUATION_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/ROW_DUALITY_CONTINUATION_RESULTS.txt)
- [Updated complete research packet](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal)

The accepted unrestricted large-\(k\) proof is preserved unchanged. Here are the mathematical results of this continuation and the precise comparison that remains missing.

## 1. A stronger original-density row-defect theorem

Write the **rows** of a matrix as \(F=(x;y)\). For a second-row increment \(z\in\mathbb R^2\), define
\[
\begin{aligned}
B_F(z)
&=J_k(x,y+z)-J_k(x,y)-D_yJ_k(x,y)\cdot z,\\
h_F(z)&=D_y^2J_k(F)[z,z],\\
q_k(z)&=J_k(0,z)
=\frac{\ell}{8n}\left(k^2z_1^4+2z_1^2z_2^2+z_2^4\right).
\end{aligned}
\]
Here \(q_k\) denotes the row restriction, rather than the earlier lower-endpoint quantity \(Q_k(F)\).

For every \(k>1/3\), every \(F,z\), and every \(0\le\theta\le1/6\),
\[
\boxed{
B_F(z)\ge
\theta h_F(z)+
\left(1-\frac{2}{3(1-2\theta)}\right)q_k(z).
}
\tag{1}
\]

This retains a portion of the row Hessian while accounting for the reduction in the quartic reserve.

### Proof of the allocation

The row line
\[
r(t)=J_k(x,y+tz)
\]
is convex by rank-one convexity. For \(z\ne0\), its second derivative therefore has the form
\[
r''(t)=12q_k(z)(t-s)^2+\beta,
\qquad \beta\ge0.
\]
Consequently,
\[
B_F(z)=q_k(z)-4q_k(z)s+6q_k(z)s^2+\frac{\beta}{2},
\]
and
\[
h_F(z)=12q_k(z)s^2+\beta.
\]
Subtracting the right side of (1) leaves exactly
\[
6q_k(z)(1-2\theta)
\left(s-\frac{1}{3(1-2\theta)}\right)^2
+\left(\frac12-\theta\right)\beta,
\]
which is nonnegative.

Thus (1) allocates **one original Bregman remainder**. No quadratic and quartic reserves are counted twice.

### The optimized convex remainder

Taking the supremum in (1) gives a convex, even function
\[
\Psi_F(z)=
\sup_{0\le\theta\le1/6}
\left[
\theta h_F(z)+
\left(1-\frac{2}{3(1-2\theta)}\right)q_k(z)
\right].
\]
This supremum has an explicit value. With \(h=h_F(z)\) and \(q=q_k(z)\),
\[
\boxed{
\Psi_F(z)=
\begin{cases}
q/3,&h\le4q/3,\\[1mm]
h/2+q-2\sqrt{hq/3},&4q/3\le h\le3q,\\[1mm]
h/6,&h\ge3q.
\end{cases}}
\tag{2}
\]
In particular,
\[
B_F(z)\ge\Psi_F(z),\qquad
\Psi_F(z)\ge\gamma_k|z|^4,\qquad
\Psi_F(z)\ge\frac16h_F(z),
\]
where
\[
\gamma_k=\frac{\ell\min(k^2,1)}{24n}.
\]

Now fix an actual first row \(x=a+Df\), an actual candidate second row \(y_0=b+Dg_0\), and any solenoidal stress \(\tau\in L^{4/3}\). Put
\[
F_0=(x;y_0),\qquad e=D_yJ_k(F_0)-\tau.
\]
Integration against compatible row differences gives the new global estimate
\[
\boxed{
\min_g\int_{\mathbb T^2}J_k(a+Df,b+Dg)
\ge
\int_{\mathbb T^2}J_k(F_0)
-\int_{\mathbb T^2}\Psi_{F_0}^*(e).
}
\tag{3}
\]

It holds at the natural \(L^4\)–\(L^{4/3}\) regularity. The pointwise conjugate is finite and measurable, with
\[
0\le\Psi_F^*(e)
\le
\frac{3}{4^{4/3}\gamma_k^{1/3}}|e|^{4/3}.
\]

There is also a directly evaluable upper bound on its cost:
\[
\boxed{
\Psi_F^*(e)\le
\min\left\{
\frac{3}{4^{4/3}\gamma_k^{1/3}}|e|^{4/3},
\frac32e^T\bigl(D_y^2J_k(F)\bigr)^\dagger e
\right\}.
}
\tag{4}
\]
The second expression is assigned \(+\infty\) outside the range of the row Hessian. Thus the estimate remains valid at degeneracy.

Equation (3) improves the supplied stress-defect operation for the same candidate and stress. Its missing application is still a uniform comparison between the defect and the candidate’s **original** energy above the affine value. The complete derivation is in :chatgpt-content-reference{index="2"}[ACTUAL_ROW_CORRECTION_AND_MIXED_DEFECT.md](sandbox:/workspace/scratch/21b466b728a1/moment_stress_defect_continuation/ACTUAL_ROW_CORRECTION_AND_MIXED_DEFECT.md).

## 2. An actual compatible correction removes the linear stress defect at \(k=1\)

At mean \(I\), take an arbitrary first-row potential \(f\) and define
\[
\boxed{
g_0=-2\Delta^{-1}\partial_1\partial_2f.
}
\tag{5}
\]
This is an operator on the original torus, with multiplier
\[
-\frac{2\xi_1\xi_2}{|\xi|^2}
\qquad(\xi\in\mathbb Z^2\setminus\{0\}).
\]
It produces a genuine periodic \(W^{1,4}\) potential. The supplied Beurling bound pays its \(L^4\) boundedness; no source lattice is changed. The underlying arbitrary-mean Burkholder/Beurling theorem retains the scope specified in your premise. 

Write
\[
G_0=D(f,g_0)=
\begin{pmatrix}a&b\\c&d\end{pmatrix}.
\]
The original row stress has the exact expansion
\[
D_yJ_1(I+G_0)
=(0,3)+(2c-3b,\;7a+2d)+N_2(G_0)+N_3(G_0),
\]
where
\[
N_2(G)=
\left(
2(a+d)c-(4a+2d)b,\;
5a^2+c^2+4ad-2bc
\right),
\qquad
N_3(G)=D_yJ_1(G).
\]
By (5),
\[
\operatorname{div}(2c-3b,\;3+7a+2d)
=2\Delta g_0+4f_{12}=0.
\]
The entire constant and linear stress is therefore already solenoidal.

With \(P_{\rm grad}=\nabla\Delta^{-1}\operatorname{div}\), choose the solenoidal part of the remaining stress. The defect becomes exactly
\[
\boxed{
e=P_{\rm grad}\bigl(N_2(G_0)+N_3(G_0)\bigr).
}
\tag{6}
\]

The original energy of this candidate is also explicit:
\[
\int J_1(I+G_0)-J_1(I)
=
4\|P_1Df\|_2^2
+\int\mathcal C(G_0)
+\int J_1(G_0),
\tag{7}
\]
where
\[
P_1=\partial_1^2\Delta^{-1},
\qquad
\mathcal C(G)
=(a+d)(a^2+c^2)+(4a+2d)(ad-bc).
\]
Combining (3), (6), and (7) gives
\[
\begin{aligned}
\min_g\left[\int J_1(e_1+Df,e_2+Dg)-J_1(I)\right]
\ge{}&
4\|P_1Df\|_2^2+\int\mathcal C(G_0)+\int J_1(G_0)\\
&-\int\Psi_{I+G_0}^*
\!\left(P_{\rm grad}(N_2(G_0)+N_3(G_0))\right).
\end{aligned}
\tag{8}
\]

**I have not proved that the right side of (8) is nonnegative for arbitrary \(f\).** The signed cubic is retained, and the defect must be paid from those same original terms.

For a fixed smooth profile scaled by \(\varepsilon\), the corrected defect begins at order \(\varepsilon^2\). Near \(I\), (4) consequently gives an \(O(\varepsilon^4)\) penalty. This explains the improvement over applying the quartic-only estimate at a constant second-row candidate. It does not provide a uniform arbitrary-amplitude theorem.

### An exact example checks this distinction

For
\[
f(x,y)=\frac{\sin(2\pi(x+y))}{2\pi},
\]
take first row \(e_1+\varepsilon Df\) and the constant second-row candidate \(e_2\). Every solenoidal \(\tau\) has quartic-only defect cost at least
\[
3\varepsilon^{4/3}.
\]
The candidate’s exact original gap is
\[
2\varepsilon^2+\frac{3}{16}\varepsilon^4.
\]
Thus, for \(0<\varepsilon\le1\), that sufficient lower bound is negative for **every** stress choice.

Nevertheless, the actual conditional minimum satisfies
\[
\boxed{
\min_g\left[
\int J_1(e_1+\varepsilon Df,e_2+Dg)-J_1(I)
\right]\ge\frac{\varepsilon^4}{16}>0.
}
\tag{9}
\]
To prove this, average the second potential along translations \((x,y)\mapsto(x+t,y-t)\). Row convexity makes the energy decrease under this averaging. The averaged perturbation is pointwise rank one, so the accepted rank-one quartic reserve applies.

This supplies an exact positive example where the crude stress allocation fails. It also shows why improving the candidate and retaining quadratic curvature are substantive steps.

## 3. Conditional row minimization can be performed with certified finite arithmetic

The new algorithmic result is:

> For rational \(k>1/3\), rational affine rows \(a,b\), and a supplied finite rational Fourier first potential \(f\), the conditional minimum
> \[
> m(f;a,b)=\min_g\int J_k(a+Df,b+Dg)
> \]
> can be enclosed in a rational interval of any prescribed positive rational width. The construction also returns an actual finite rational Fourier second potential with a certified prescribed \(L^4\) distance to the unique minimizing gradient.

This is a proved algorithm specification. **I did not invoke this search in the continuation**, and no computed conditional minimum is being reported.

### The a posteriori certificate

For a rational Fourier candidate \(g_0\) and an exactly solenoidal rational Fourier stress \(\tau\), let
\[
E_0=\int J_k(a+Df,b+Dg_0),
\qquad
r=\int|D_yJ_k(a+Df,b+Dg_0)-\tau|^{4/3}.
\]
Then
\[
E_0-C_{\gamma_k}r\le m(f;a,b)\le E_0,
\qquad
C_\gamma=\frac{3}{4^{4/3}\gamma^{1/3}}.
\tag{10}
\]
The minimizing second-row gradient \(y_*\) satisfies
\[
\boxed{
\|y_*-(b+Dg_0)\|_4
\le\frac{r^{1/4}}{(2\gamma_k)^{1/3}}.
}
\tag{11}
\]
This follows by adding the original Bregman inequalities in both directions and using the solenoidal stress pairings.

The upper energy \(E_0\) is an exact rational Laurent constant coefficient. The fractional moment \(r\) requires an additional certified operation.

### Paying the \(4/3\)-moment

Let \(e\) be the finite Fourier residual and choose a rational coefficient bound \(M\ge\|e\|_\infty\). Set
\[
z(x)=\frac{|e(x)|^2}{M^2}\in[0,1].
\]
For any requested rational error \(\rho>0\), take
\[
N\ge\max\left(1,\left\lceil\frac{2M^4}{\rho^3}\right\rceil\right).
\]
The Bernstein polynomial of
\[
H(z)=M^{4/3}z^{2/3}
\]
has the one-sided error
\[
0\le H-B_NH
\le\left(\frac{M^4}{4N}\right)^{1/3}\le\rho/2.
\]
Its coefficient targets satisfy
\[
h_j^3=\frac{M^4j^2}{N^2},
\]
so rational bisection with exact cube comparisons gives upper coefficients within \(\rho/2\). Adding the remaining \(\rho/2\) produces a polynomial \(P_N\) with rational coefficients such that
\[
H(z)\le P_N(z)\le H(z)+\rho.
\]
Exact Laurent integration therefore returns
\[
\boxed{
r\le r^+:=\int P_N(z(x))\le r+\rho.
}
\tag{12}
\]

This involves no spatial quadrature, sampling, or exact-real comparison. It also avoids replacing the natural \(L^{4/3}\) moment by an \(L^2\) quantity.

If the residual support lies in \([-K,K]^2\), the note gives a conservative bound of
\[
100(N+1)^2(4NK+1)^4
\]
rational additions and multiplications for the polynomial calculation, together with explicit bisection counts and computable integer-bit bounds.

### Why the search terminates

Enumerate finite rational Fourier candidate potentials and finite rational solenoidal stresses, with increasing support and coefficient bounds. At each finite stage compute the exact energy and the certified bound (12).

Termination follows from:

1. Strong \(L^4\) approximation of the attained minimizing row gradient by rational Fourier gradients.
2. Strong continuity of the cubic constitutive stress from \(L^4\) to \(L^{4/3}\).
3. Strong density of rational Fourier solenoidal stresses in solenoidal \(L^{4/3}\).

Hence admissible candidate/stress pairs exist with \(r\) arbitrarily small. Every fixed rational pair eventually appears, while the certified integration error tends to zero. The stopping criterion eventually succeeds.

No uniform formula for the successful stage is asserted. The proof supplies totality and finite work at each stage, with all approximation errors accounted for. An independent analytic audit checked the upper-error direction, stopping thresholds, natural-exponent density, and bit accounting. See :chatgpt-content-reference{index="3"}[CERTIFIED_CONDITIONAL_ROW_SOLVER.md](sandbox:/workspace/scratch/21b466b728a1/root_row_duality_continuation/CERTIFIED_CONDITIONAL_ROW_SOLVER.md).

The outstanding quantifier is crucial:
\[
\boxed{
m(f;a,b)\ge J_k(a,b)
\quad\text{for every }f,\ a,\ b,\ k>1/3.
}
\tag{13}
\]
Computing one conditional minimum to arbitrary accuracy does not establish (13).

## 4. The completed compatible investigation is positive for all means and amplitudes

At \(k=17/50\), I investigated four complete families based on the retained smooth heat-obstruction potential
\[
\phi(x,y)=\frac1{2\pi}
\left(
\cos(2\pi x)+\cos(2\pi y),\
\frac{\cos(4\pi x)+\cos(4\pi y)}5
+\cos(2\pi x)\cos(2\pi y)
\right).
\]
For
\[
v\in\{e_1,e_2,e_1+e_2,e_1-e_2\},
\]
define the actual compatible fields
\[
G_{v,t}
=D\left(\phi+\frac{t}{2\pi}\partial_v\phi\right),
\qquad t\in\mathbb R.
\]

For all four directions,
\[
\boxed{
\int J_{17/50}(A+G_{v,t})-J_{17/50}(A)>0
\quad\text{for every real }t\text{ and every real }A.
}
\tag{14}
\]

This is an exact all-amplitude calculation. Set \(E=D\phi\), \(O_v=\partial_vE/(2\pi)\), and \(z=t^2\). Parity and periodic integration give
\[
H_{G_{v,t}}=H_E+zH_{O_v},\qquad
b_{G_{v,t}}=t^3b_{O_v},\qquad
c_{G_{v,t}}=c_E+zc_{2,v}+z^2c_{O_v}.
\]
After eliminating every affine mean,
\[
\min_A\operatorname{gap}(A,G_{v,t})
=\frac{P_v(z)}{2\det(H_E+zH_{O_v})}.
\]
Exact principal minors prove the denominator positive. Each \(P_v\) has degree six, and **all seven rational coefficients are strictly positive**.

Every \(c_{2,v}\) is negative: these compatible variations initially lower the zero-mean energy. Equation (14) establishes that the four full families nevertheless stay above their affine values even after optimizing the mean.

The bounded calculation used:

| Item | Actual result |
|---|---:|
| Complete families | 4 |
| Counted rational operations | 89,492 |
| Largest conservative intermediate bit bound | 201 bits |
| Polynomial-remainder operations | 0 |
| Root-isolation steps | 0 |
| Parent calculation wall time | 0.354451239 seconds |

All integration was exact constant-coefficient extraction. The complete rational polynomials, matrices, principal minors, script, and receipt are retained in the packet; the proof and cost account are in :chatgpt-content-reference{index="4"}[DERIVATIVE_PHASE_FAMILY_RESULT.md](sandbox:/workspace/scratch/21b466b728a1/construction_derivative_continuation/DERIVATIVE_PHASE_FAMILY_RESULT.md).

## 5. The nonlinear representation checks have limited conclusions

Three further analytic checks were completed and independently reviewed:

| Construction | Established conclusion | Scope still outside the result |
|---|---|---|
| A concrete regular Burkholder graph core with the original translated quadratic form matched | Its normalized cubic on the matched quadratic kernel remains zero for every fixed finite graph matrix; it cannot touch the original cubic there | Singular limits and other nonlinear cores |
| A single positive affine-transformed and shifted Burkholder block plus a polyaffine correction | It cannot converge locally uniformly to a strictly coercive homogeneous quartic, even with divergent or ill-conditioned parameters | Positive sums, integrals, and nonlinear graph constructions |
| An actually dominated target-specific projection calibration approaching the target value | Its constraint has a positive inradius; its effective graph coefficient cannot diverge by collapsing that constraint | Constructing the required dominated calibration, or other limiting mechanisms |

These results refine the available representation boundaries. They supply no negative original gradient and no touching minorant for the full family.

## The unresolved statement

The original all-mean criterion remains
\[
\boxed{
b_G^T H_G^\dagger b_G\le2c_G
\qquad\text{for every actual compatible }G=D\phi.
}
\]
The automatic range condition remains available. The mixed-defect theorem improves one way of estimating conditional minimization, but I have not shown that its defect is uniformly bounded by the same original energy reserve.

Accordingly, **this continuation does not meet your requested full affirmative or full negative endpoint**. It adds proved operations and exact compatible certificates, with their finite work and approximation accounted for; the universal sharp comparison is still missing.