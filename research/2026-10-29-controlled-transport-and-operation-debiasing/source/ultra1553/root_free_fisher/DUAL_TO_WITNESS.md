# From a linear-containment dual to an exact information witness

30 October 2026. Root construction. This consumes C's centered Fisher-unit-
ball formulation and the definite-pencil theorem in LINEAR_CONTAINMENT.md.
The intended information semantics remain
J_A=D((A tensor id)rho||(A tensor id)sigma)-D(rho_R||sigma_R), with defined
finite differences, inherited equal-reference equivalence and centered
free vectors. It is NOT a factor comparison of uncentered Fisher forms;
their common reference-score directions would force c>=1.

Given a rational infeasibility dual Y0,...,Yg with Y0>=0,
sum Aj^T tensor Yj>=0 and sum Tr(Yj Bj)<0, choose a small rational
epsilon>0 retaining negativity after Y0e=Y0+epsilon I. Put G=Y0e^T.
For the source variables Qi=I/n+Xi (i<n), Qn=I/n-sum Xi and
Ui=Vi+iWi (i<n), Un=-sum Ui, define the RATIONAL matrices

 Ei=G/n+Y_Xi^T, En=G/n-sum Y_Xi^T,
 Fi=Y_Vi^T+iY_Wi^T, Fn=-sum Fi.

Full transpose of the regularized dual source inequality gives

 Ei>0, sum Ei=G,
 [[diag(E_L,y),col(F_L,y)],[col(F_L,y)^*,G]]>0,
 E_A,y=sum_i A_yi Ei, F_A,y=sum_i A_yi Fi.

Thus sum F_L,y^* E_L,y^-1 F_L,y<=G. The corresponding target block,
with bottom cG, has negative quadratic form at the rational vector Omega
whose blocks are e1,...,e_m,e_b, b=m+1. Completing its top-block squares
therefore gives

 e_b^* [cG-sum F_K,y^* E_K,y^-1 F_K,y] e_b<0.

Set h_i=Fi e_b. The implicit effects/vectors

 Qi=G^-1/2 Ei G^-1/2, u_i=G^-1/2 h_i

are a legal centered free witness. Their form values are EXACTLY RATIONAL:

 F_A=sum_y h_A,y^* E_A,y^-1 h_A,y.

No matrix square root is evaluated. The source form is<=G_bb whereas the
target form is>cG_bb, hence F_K>cF_L for c>=0. If F_L=0 this is a kernel
obstruction, not a finite ratio; otherwise their exact ratio is>c. The
direct rational (Ei,hi) evaluation already exists in N1038. The added
operation is extraction from the GENERAL joint-design containment dual,
with a finite dimension bound and no nonlinear reference-state search.

An actual receiver need not trust a solver dual or rounding status. It can
check Ei>0, G>0, sum Ei=G, sum Fi=0, the source Schur inequality, the negative
target form and the final rational free ratio directly. A rounded proposal
that fails any needed sign remains a failure. The accepted free/entropy
representation then implies a violation at the stated conditional-Umegaki
boundary. A physically prepared finite state pair, or a numerical finite
entropy-ratio example, requires the separate active/vacuum construction and
its finite-perturbation/logarithm bounds; none is manufactured by this note.

The same source data and all repairs belong to ordinary SDP/Farkas methods.
Historical novelty, physical reference preparation and practical advantage
are unestablished. Full-problem experimental resources are not reduced to
the arithmetic runtime of a successful certificate intake.
