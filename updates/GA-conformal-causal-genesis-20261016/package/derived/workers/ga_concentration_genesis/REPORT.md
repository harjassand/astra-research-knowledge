# Quantitative concentration and the exact spatial-profile obstruction

Research date: 16 October 2026, Australia/Brisbane.
Worker: ga_concentration_genesis.
Repository pin supplied by the parent: f80a8f15137575133ad2c9af975513b32e8fa93e.
Only this worker directory was modified. No Git operation or additional worker was used.

## Result and scope

The sharp conformal ratio has an exact invariance and a stronger concentration obstruction than the incoming report records.

1. Its supremum is identical for smooth periodic maps, compactly supported smooth planar maps, and zero-boundary W^{1,4} maps in any nonempty bounded open domain.
2. Under A_r=1, Q_r=epsilon, and a fixed positive ratio, a fixed fraction of the quartic energy lies at gradient size at least a constant times epsilon^{-1/2}, on a set of area O(epsilon^2). These powers are optimal.
3. This concentration need not create an atom, a distinguished location, or any nonzero profile under translations and isotropic dilations that preserve the L^4 gradient norm. A disjoint cloud of identical compatible bubbles preserves the ratio exactly while its limiting quartic-energy measure can be any prescribed probability measure, including Lebesgue measure. For a uniform grid cloud, every such spatial profile is zero.
4. Disjoint components cannot improve the ratio beyond their best component. The closed cone of attainable integrated (A,C,Q) moments on the plane is exactly a second-order cone, with its sole unknown parameter equal to Gamma_r.

Thus an argument that reduces near-kernel loss to finitely many spatial concentration profiles is false without an additional selection or localization theorem. A general procedure that selects a small component and then independently renormalizes its amplitude is not excluded; proving such a procedure for arbitrary compatible fields is a further obligation.

No upper bound Gamma_r <= 1, negative Jensen field, or all-background quasiconvexity theorem is proved here. The quantitative estimate uses the incoming mixed-derivative interpolation estimate, whose analytic proof is explicitly supplied in the source. The transplantation, cloud, cone, and profile-obstruction proofs below are elementary and independent of external Young-measure theorems.

## 1. Definitions and admitted analytic input

Write

\[
 F=D\phi=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
 \sigma=r+1,\quad \kappa=\frac{r(r+2)}3,\quad r>0,
\]

\[
 q=\sigma a+d,\qquad
 P_r(F)=2aq^2-(r+2)qa^2+rqc^2-2qbc-\kappa a^3-\kappa ac^2.
 \tag{1}
\]

The integrated moments, using unnormalized Lebesgue integrals, are

\[
 A(\phi)=\int J_r(D\phi),\quad
 C(\phi)=\int P_r(D\phi),\quad
 Q(\phi)=\int(q^2+\kappa c^2).
 \tag{2}
\]

On a torus of any fixed volume, using normalized averages instead changes all three moments by the same factor and leaves C^2/(4AQ) unchanged.

Here J_r has exactly the unchanged source coefficients:

\[
 \alpha=\frac{3r}{8(r+2)},\quad
 \beta=\frac{r(r-1)}6,\quad
 u=a^2+c^2,\ v=b^2+d^2,\ j=ad-bc,
\]

\[
 J_r(F)=\alpha(u+v-2j)^2+\beta u^2+j^2+ruj.
 \tag{3}
\]

The sharp ratio is

\[
 R(\phi)=\frac{C(\phi)^2}{4A(\phi)Q(\phi)}
 \quad\text{when }A(\phi)Q(\phi)>0.
 \tag{4}
\]

The incoming report proves the following interpolation estimate for compatible periodic maps, and by zero extension for compact maps:

\[
 \|a\|_{8/3}^2
 \le K_\sigma\|(q,c)\|_2\|F\|_4.
 \tag{5}
\]

This is a nonlinear estimate. No linear Korn estimate for the rank-changing operator is used. We admit (5) with the proof in source Section 2.1–2.2: periodic Hodge decomposition, mixed-derivative complex interpolation with endpoints 2 and 4, and bounded Riesz/Hilbert multipliers. All later applications retain its finite unspecified constant K_sigma.

### 1.1 An explicit pointwise coercivity constant

This auxiliary calculation independently reconstructs the source's B=0 calibration, so a merely asserted positive minimum is not needed.

Let t=(2r+1)/3 and

\[
 M_r=\begin{pmatrix}
 t^2&1/3&2t\\
 1/3&1&-2\\
 2t&-2&16/3+1/\alpha
 \end{pmatrix}.
\]

With w=ab+cd and z=(u,v,j)^T, direct polynomial expansion gives

\[
 J_r(F)=\alpha z^TM_rz+\frac{4\alpha}{3}w^2.
 \tag{6}
\]

The leading principal minors are

\[
 t^2,\quad \frac{4r(r+1)}9,\quad \frac{16(r+1)}{27}.
\]

They are positive for every r>0. Furthermore

\[
 \operatorname{tr}M_r^{-1}
 =\frac{15r^3+31r^2+46r+40}{4r(r+1)}.
\]

Since lambda_min(M_r) >= 1/tr(M_r^{-1}) and
u^2+v^2+j^2 >= (u+v)^2/2 = |F|^4/2, (6) yields

\[
 \boxed{J_r(F)\ge c_r|F|^4,\qquad
 c_r=\frac{3r^2(r+1)}
 {4(r+2)(15r^3+31r^2+46r+40)}>0.}
 \tag{7}
\]

The source's sharper r=1 constant is not needed. There is also a finite upper bound J_r(F) <= L_r|F|^4 by homogeneity and continuity. Thus A=1 implies

\[
 \|F\|_4\le B_r:=c_r^{-1/4}.
 \tag{8}
\]

Equations (5) and (7) imply 0 <= Gamma_r < infinity. A compact example below proves Gamma_r>0 for every r>0.

## 2. The sharp constant is independent of the test domain

**Theorem 1 (exact transplantation).** The following suprema are equal:

- R over smooth periodic maps on the standard square torus;
- R over periodic W^{1,4} maps on that torus;
- R over C_c^\infty(R^2;R^2);
- R over C_c^\infty(Omega;R^2), for any nonempty bounded open Omega;
- R over W^{1,4}_0(Omega;R^2), with W_0 defined as the closure of compact smooth maps.

Denote their common value by Gamma_r. No regularity of the boundary of Omega is required for this formulation of W_0.

**Proof.** Strong W^{1,4} approximation preserves the three polynomial integrals, since their degrees are 4, 3, and 2. It therefore preserves R at every map with AQ>0.

A compact smooth map can be placed inside a period cell and extended periodically. If the period size must change, the transformation

\[
 \phi_{\lambda,s,x_0}(x)=s\lambda\,
                  \phi((x-x_0)/\lambda)
 \tag{9}
\]

has gradient sF((x-x_0)/lambda) and exact moments

\[
 \boxed{A_{\lambda,s}=s^4\lambda^2A,\quad
 C_{\lambda,s}=s^3\lambda^2C,\quad
 Q_{\lambda,s}=s^2\lambda^2Q.}
 \tag{10}
\]

Thus R is unchanged. With s=1 and lambda small, any given compact map fits inside any prescribed open ball in Omega. Extension by zero then gives an admissible map in the other classes.

For the reverse periodic-to-compact direction, extend a smooth periodic phi to the plane. Let eta_L equal one on a square consisting of O(L^2) complete period cells, vanish outside a collar of fixed width around that square, and have uniformly bounded first derivatives. The map Psi_L=eta_L phi is compact smooth. On the collar, both Dphi and phi tensor Deta_L are uniformly bounded. The collar area is O(L). Hence

\[
 A(\Psi_L)=m_LA(\phi)+O(L),\quad
 C(\Psi_L)=m_LC(\phi)+O(L),\quad
 Q(\Psi_L)=m_LQ(\phi)+O(L),
\]

where m_L is the number of complete cells, asymptotic to a positive constant times L^2. The ratio tends to R(phi). Compact smooth approximation also proves the zero-boundary statement. This proves all equalities. \(\square\)

The source stated zero-boundary-to-periodic transfer, but did not explicitly prove the reverse transfer of the sharp supremum. The reverse cutoff argument is necessary: a periodic field cannot simply be declared compactly supported.

### 2.1 The entire sharp problem can be concentrated near the kernel

**Corollary 1.** For every fixed admissible compact template psi with moments A_0,Q_0>0 and every sufficiently small epsilon>0, there is a compact compatible field in any prescribed nonempty open domain with

\[
 A=1,\qquad Q=\epsilon,\qquad
 C=\sqrt{\epsilon}\frac{C_0}{\sqrt{A_0Q_0}},
 \qquad R=R(\psi).
 \tag{11}
\]

In (9), take

\[
 s_\epsilon^2=\frac{Q_0}{A_0\epsilon},\qquad
 \lambda_\epsilon^2=\frac{A_0\epsilon^2}{Q_0^2}.
 \tag{12}
\]

The equalities follow from (10). The support diameter is O(epsilon) and the gradient amplitude is O(epsilon^{-1/2}). In particular the sequence tends to zero strongly in W^{1,p} for every p<4, while its L^4 gradient norm stays positive.

Consequently

\[
 \boxed{\Gamma_r=
 \sup_{\substack{A(\phi_n)=1,\ Q(\phi_n)\to0\\
 D\phi_n\to0\ {\rm in\ measure}}}
       \limsup_n R(\phi_n).}
 \tag{13}
\]

The same equality holds with strong W^{1,p} convergence to zero for every p<4. For a sequence of templates approaching Gamma_r, choose epsilon_n small enough at each stage to fit the domain and ensure these convergences. This is a diagonal selection over p increasing to 4.

Equation (13) says that treating every near-kernel concentrating sequence already treats the full sharp problem. It does not supply a compactness theorem for those sequences.

### 2.2 Ordinary oscillations preserve every fixed ratio too

For a smooth periodic map phi, put

\[
 \phi_n(x)=n^{-1}\phi(nx),\qquad n\in\mathbb N.
 \tag{14}
\]

Then Dphi_n(x)=Dphi(nx), so A,C,Q, and R are exactly unchanged. The maps tend uniformly to zero, their gradients converge weakly to zero in L^4, and their fourth powers are uniformly integrable because the gradients have a common L^\infty bound. Their moment measures converge to the corresponding constant multiples of Lebesgue measure.

Thus a claim that every sequence with a positive ratio must spatially concentrate would be false. The source's valid nonconcentration theorem includes the essential extra assumption Q_n->0. Construction (14) has fixed nonzero Q.

## 3. Quantitative concentration at the optimal scale

**Theorem 2 (critical amplitude and area).** Fix r>0. There exists a finite constant K_r, explicitly expressible below in terms of K_sigma and c_r, with the following property.

Let phi be compatible, A(phi)=1, Q(phi)=epsilon>0. For M>0 set

\[
 \tau_M=\int_{\{|D\phi|>M\}}|D\phi|^4,\qquad h=\sqrt\epsilon.
\]

Whenever Mh<=1,

\[
 \boxed{\frac{\|P_r(D\phi)\|_1}{\sqrt{Q(\phi)}}
 \le K_r\bigl((M\sqrt Q)^{1/3}+\tau_M^{1/4}\bigr).}
 \tag{15}
\]

The absolute integral on the left is stronger than the signed bound needed for R.

If R(phi)>=rho>0, define

\[
 \delta_\rho=\min\{1,(\sqrt\rho/K_r)^3\},\qquad
 E_\phi=\{|D\phi|>\delta_\rho/\sqrt Q\}.
\]

Then

\[
 \boxed{\int_{E_\phi}|D\phi|^4\ge\frac{\rho^2}{K_r^4},
 \quad
 \int_{E_\phi}J_r(D\phi)\ge c_r\frac{\rho^2}{K_r^4},
 \quad
 |E_\phi|\le B_r^4\delta_\rho^{-4}Q^2.}
 \tag{16}
\]

In particular, a fixed positive ratio at A=1 forces a fixed fraction of the quartic energy onto a set of area O(Q^2), at gradient size at least a constant times Q^{-1/2}.

### 3.1 Proof, retaining the constants

Set

\[
 B=B_r,\quad \ell_r=\max\{1,\kappa^{-1/2}\},\quad
 D=K_\sigma\ell_rB.
\]

Since ||q||_2<=h, ||c||_2<=h/sqrt(kappa), estimate (5) gives

\[
 \|a\|_{8/3}^2\le Dh. \tag{17}
\]

Let L={|F|<=M}, E={|F|>M}, z=Mh, and tau=tau_M.

The low-gradient part of the exceptional term a^3 satisfies

\[
 \int_L|a|^3
 \le M^{1/3}\int|a|^{8/3}
 \le hD^{4/3}z^{1/3}.
 \tag{18}
\]

For the high part, Holder with exponents 4/3 and 4 gives

\[
 \int_E|a|^3
 \le\|a\|_{8/3}^2\|a1_E\|_4
 \le Dh\,\tau^{1/4}. \tag{19}
\]

The second low-gradient estimate that uses (17) is

\[
 \|a^21_L\|_2
 \le M^{2/3}\|a\|_{8/3}^{4/3}
 \le D^{2/3}z^{2/3}. \tag{20}
\]

All remaining low parts use the L^2 defect directly. Applying the triangle inequality to the six terms in (1) gives:

| Term | Integral over L, divided by h |
| --- | --- |
| 2aq^2 | at most 2z |
| -(r+2)qa^2 | at most (r+2)D^{2/3}z^{2/3} |
| rqc^2 | at most r z/sqrt(kappa) |
| -2qbc | at most 2z/sqrt(kappa) |
| -kappa a^3 | at most kappa D^{4/3}z^{1/3} |
| -kappa ac^2 | at most z |

For example,

\[
 \int_L|qbc|\le \|q\|_2 M\|c\|_2,\qquad
 \int_L|ac^2|\le\|c\|_2 M\|c\|_2.
\]

On E, use ||q||_2<=h or ||c||_2<=h/sqrt(kappa) for one factor. Every quadratic remaining factor has its L^2(E) norm bounded by a fixed coefficient times tau^{1/2}. The first term uses |aq|<=(sigma+1)|F|^2. Thus all high parts other than a^3 contribute at most

\[
 h(4r+8+\sqrt\kappa)\tau^{1/2}.
\]

Together with (18)–(20),

\[
\begin{split}
 \frac{\|P_r(F)\|_1}{h}\le{}&
 \kappa D^{4/3}z^{1/3}
 +(r+2)D^{2/3}z^{2/3}
 +\left(3+\frac{r+2}{\sqrt\kappa}\right)z\\
 &+(4r+8+\sqrt\kappa)\tau^{1/2}
 +\kappa D\tau^{1/4}.
\end{split} \tag{21}
\]

For z<=1, z^{2/3},z<=z^{1/3}. Also tau<=B^4, so tau^{1/2}<=B tau^{1/4}. One valid choice in (15) is

\[
\begin{split}
 K_r={}&\kappa D^{4/3}+(r+2)D^{2/3}
 +3+\frac{r+2}{\sqrt\kappa}\\
 &+(4r+8+\sqrt\kappa)B+\kappa D .
\end{split} \tag{22}
\]

If R>=rho, then |C|/h>=2sqrt(rho). Apply (15) with M=delta_rho/h. Its low contribution is at most sqrt(rho), so tau_M^{1/4}>=sqrt(rho)/K_r. This proves the first inequality in (16); coercivity gives the second. Markov's inequality gives the area bound. \(\square\)

### 3.2 Sharpness and limits of the conclusion

For the fixed smooth compact profile in (12), the largest gradient is O(epsilon^{-1/2}), and J_r(Dphi_epsilon)<=constant epsilon^{-2}. It follows that:

- a threshold M_epsilon with M_epsilon sqrt(epsilon)->infinity eventually sees no gradient at all;
- a set of area o(epsilon^2) carries o(1) quartic energy.

Thus neither the critical gradient exponent 1/2 nor the area exponent 2 in (16) can be improved uniformly. Numerical constants and the rho dependence in (16) are not asserted optimal.

The theorem controls the total area of an energy-carrying set. It does not say that this set lies in a ball of radius O(Q), nor that a positive fraction of the energy enters one ball. Those stronger geometric statements are false, as the next construction shows.

The source's uniform-integrability result follows immediately from (15): if Q_n->0 and the fourth powers are uniformly integrable, first hold M fixed and pass to the limit, then let M->infinity. The new content is the optimal amplitude/area scale, together with the obstruction to turning it into atomic or finite-profile compactness.

## 4. Arbitrary concentration measures at an unchanged ratio

**Theorem 3 (compatible bubble cloud).** Let Omega be a nonempty bounded open domain. Fix a smooth compact template psi with moments A_0,Q_0>0, and write

\[
 c_0=\frac{C_0}{\sqrt{A_0Q_0}},\qquad
 \rho_0=\frac{c_0^2}{4}.
\]

For every probability measure mu on the closure of Omega, there are phi_n in C_c^\infty(Omega;R^2) and epsilon_n->0 such that

\[
 A(\phi_n)=1,\quad Q(\phi_n)=\epsilon_n,\quad
 C(\phi_n)=c_0\sqrt{\epsilon_n},\quad R(\phi_n)=\rho_0,
 \tag{23}
\]

and, as measures on the closure,

\[
 \boxed{
 \begin{aligned}
 J_r(D\phi_n)\,dx&\stackrel *\rightharpoonup\mu,\\
 \frac{q_n^2+\kappa c_n^2}{\epsilon_n}\,dx
                    &\stackrel *\rightharpoonup\mu,\\
 \frac{P_r(D\phi_n)}{\sqrt{\epsilon_n}}\,dx
                    &\stackrel *\rightharpoonup c_0\mu.
 \end{aligned}} \tag{24}
\]

Moreover Dphi_n->0 in measure, Dphi_n converges weakly to zero in L^4, and its ordinary gradient Young measure is delta_0. For a fixed template, its support area is O(epsilon_n^2).

**Construction and proof.** Choose finitely supported probability measures

\[
 \mu_n=\sum_{j=1}^{N_n}w_{n,j}\delta_{x_{n,j}}
                   \stackrel *\rightharpoonup\mu,
\]

with positive weights, distinct points inside Omega, and sum_j w_{n,j}=1. Choose epsilon_n small enough that the copies below have disjoint supports lying inside Omega. This is always possible because there are only finitely many points at each stage.

Use the common amplitude

\[
 s_n^2=\frac{Q_0}{A_0\epsilon_n},
\]

and the copy radii

\[
 \lambda_{n,j}^2=\frac{A_0\epsilon_n^2w_{n,j}}{Q_0^2}.
 \tag{25}
\]

Set

\[
 \phi_n(x)=\sum_j s_n\lambda_{n,j}
           \psi((x-x_{n,j})/\lambda_{n,j}).
 \tag{26}
\]

Every summand is a genuine compatible gradient. Disjoint support makes the three integrals add exactly. Equations (10) give, for copy j,

\[
 \boxed{A_{n,j}=w_{n,j},\quad
 Q_{n,j}=\epsilon_n w_{n,j},\quad
 C_{n,j}=c_0\sqrt{\epsilon_n}\,w_{n,j}.}
 \tag{27}
\]

This proves (23).

For a continuous test function zeta, the error between the quartic moment of copy j tested against zeta and w_{n,j}zeta(x_{n,j}) is bounded by w_{n,j} times a modulus of continuity at the copy's support diameter. The maximum diameter tends to zero. Sum the errors and use mu_n->mu. This proves the first limit in (24); the other two are identical. For the signed cubic measure, bound the error by the fixed finite constant

\[
 \frac{\int |P_r(D\psi)|}{\sqrt{A_0Q_0}}
\]

times that modulus of continuity.

The union of supports has area at most

\[
 |\operatorname{supp}\psi|\sum_j\lambda_{n,j}^2
 =|\operatorname{supp}\psi|\frac{A_0}{Q_0^2}\epsilon_n^2.
\]

Thus the gradients tend to zero in measure. Their L^4 norms remain bounded, indeed

\[
 \int|D\phi_n|^4=\frac{\int|D\psi|^4}{A_0}.
 \tag{28}
\]

Boundedness in L^4 and convergence in measure imply weak convergence to zero in L^4. The classical Young measure is delta_0 by convergence in measure. \(\square\)

For an extremizing sequence of templates, choose epsilon_n still smaller to control support size and the test-function errors. After changing signs to make C_0 nonnegative, every prescribed mu can therefore accompany a sequence whose ratios approach Gamma_r. The spatial concentration measure by itself places no restriction on the sharp constant.

### 4.1 A diffuse cloud with no nonzero critical spatial profile

Take Omega=(0,1)^2. Use an n by n grid of centers and weights w_{n,j}=1/n^2. Choose epsilon_n->0 so that each support lies well inside its grid cell. The limiting measure mu in (24) is Lebesgue measure.

Let H_n=Dphi_n. Each copy carries the same fourth-power mass

\[
 \frac1{n^2}\frac{\int|D\psi|^4}{A_0}.
\]

For every Euclidean ball,

\[
 \boxed{\sup_x\int_{B(x,t)}|H_n|^4
             \le K_\psi(t^2+n^{-2}).}
 \tag{29}
\]

Indeed a ball meets at most a constant times (nt+1)^2 grid cells, and one can bound each intersected copy by its full mass. The constant is independent of epsilon_n. Consequently, for every t_n->0,

\[
 \sup_x\int_{B(x,t_n)}|H_n|^4\to0. \tag{30}
\]

Now apply an arbitrary critical isotropic translation/dilation:

\[
 \widetilde H_n(z)=\lambda_n^{1/2}
                         H_n(x_n+\lambda_n z).
 \tag{31}
\]

This is the gradient of
lambda_n^{-1/2} phi_n(x_n+lambda_n z), and preserves the full L^4 gradient norm.

If lambda_n->0, (30) shows that tilde H_n->0 strongly in L^4_loc. If lambda_n stays bounded above and away from zero, its support measure tends to zero and it is bounded in L^4_loc, so it converges weakly to zero there. If lambda_n->infinity, its support measure is at most |Omega|/lambda_n^2 and the same argument applies. Subsequences cover every possible lambda_n. Thus

\[
 \boxed{\text{Every weak }L^4_{\rm loc}\text{ profile under (31) is zero.}}
 \tag{32}
\]

Nevertheless the total quartic energy is one, Q_n->0, and the signed normalized ratio is the nonzero fixed rho_0. There is no atom in the limiting quartic-energy measure, and no finite collection of nonzero critical spatial profiles can capture this loss.

The construction also permits templates psi_n with R(psi_n)->Gamma_r. The fourth-power mass of each copy is still at most B_r^4/n^2 by (7), so the constant in (29) can be chosen uniformly. Choose epsilon_n small enough to fit every copy in its grid cell and make their total support area tend to zero. This produces an actual extremizing sequence with all properties (30)–(32). Thus absence of nonzero critical spatial profiles is compatible with the full sharp supremum, not merely with a small positive witness.

This is an exact failure of spatial-profile compactness, not a heuristic example. It does not exclude selecting one copy, discarding the others, and multiplying the selected copy by an additional amplitude to restore unit energy. Such an independently renormalized selection preserves the ratio for this explicit cloud. Extending that operation to arbitrary near-kernel fields requires a new compatible localization argument.

### 4.2 An exact compact nonzero template for every r

For completeness, let G be the tent function supported on [0,2],
G(y)=y on [0,1] and G(y)=2-y on [1,2]. Let

\[
 F(x)=
 \begin{cases}
 x,&0\le x\le2,\\
 6-2x,&2\le x\le3,\\
 0,&\text{otherwise}.
 \end{cases}
\]

Take psi=(F(x)G(y),0), extended by zero. It is a compact W^{1,infinity} compatible map. Here c=d=0, a=F'G, b=FG', and P_r=r(2r+1)a^3/3.

Exact one-dimensional integration gives

\[
 \int a^4=\frac{36}{5},\quad
 \int a^2b^2=\frac{16}{3},\quad
 \int b^4=\frac{96}{5},\quad
 \int a^3=-3.
\]

Therefore

\[
 A_0=\frac{r(12r^2+12r+115)}{10(r+2)},\quad
 Q_0=4(r+1)^2,\quad C_0=-r(2r+1),
\]

\[
 \boxed{R(\psi)=
 \frac{5r(r+2)(2r+1)^2}
 {8(r+1)^2(12r^2+12r+115)}>0.}
 \tag{33}
\]

At r=1 this is 135/4448. Compact mollification preserves the moments and nonzero C, so a smooth compact template as required in Theorem 3 exists for every r>0. This low ratio is only an explicit existence witness, not a proposed sharp lower bound.

## 5. The exact moment cone and what profile splitting can prove

### 5.1 No gain from disjoint components

Suppose phi_i have disjoint compact supports. Set
rho_* = max_i R(phi_i), ignoring zero components. If Q_i=0, compatibility of a compact map forces that component to be zero. Then

\[
 |\sum_iC_i|
 \le2\sqrt{\rho_*}\sum_i\sqrt{A_iQ_i}
 \le2\sqrt{\rho_*}\sqrt{\sum_iA_i\sum_iQ_i}.
\]

Thus

\[
 \boxed{R(\sum_i\phi_i)\le\max_iR(\phi_i).} \tag{34}
\]

Equality holds for the cloud in Theorem 3: all signs agree, every component has the same ratio, and A_i/Q_i is independent of i.

The same calculation applies to an asymptotically disjoint profile decomposition if its A,Q moments add, and its cubic remainder is negligible relative to the square root of the total Q. Those hypotheses cannot be omitted. In particular, they do not follow merely from weak W^{1,4} convergence or from the source's nonconcentration result.

### 5.2 Full closure of the planar moment set

Let

\[
 \mathcal M_r=\{(A(\phi),C(\phi),Q(\phi)):
                    \phi\in C_c^\infty(\mathbb R^2;\mathbb R^2)\}.
\]

**Theorem 4 (exact cone relaxation).**

\[
 \boxed{\overline{\mathcal M_r}
   =\{(A,C,Q):A,Q\ge0,\ C^2\le4\Gamma_rAQ\}.}
 \tag{35}
\]

Here the closure is in R^3. Equivalently, this is the closed conic hull of moments obtained in any fixed nonempty bounded open domain. It is not the unscaled moment set of a fixed bounded domain; that set also has volume constraints such as Q<=constant sqrt(A).

**Proof.** Spatial dilation in (10), with s=1, multiplies the entire triple by an arbitrary positive scalar. Translation of compact supports makes addition exact. Hence M_r is a convex cone, and changing phi to -phi changes only the sign of C.

By definition of Gamma_r, every point of M_r lies in the cone on the right of (35).

Conversely, prescribe A,Q>0 and a number C with C^2<4Gamma_rAQ. Choose a template with ratio rho>C^2/(4AQ). If its moments are A_0,C_0,Q_0, take

\[
 s^2=\frac{AQ_0}{QA_0},\qquad
 \lambda^2=\frac{Q^2A_0}{AQ_0^2}.
 \tag{36}
\]

Then (10) yields the prescribed A,Q and cubic value of magnitude 2sqrt(rho AQ). Combine disjoint positive and negative copies with cone weights theta and 1-theta to attain exactly the prescribed C, where

\[
 \theta=\frac12\left(1+\frac{C}{2\sqrt{\rho AQ}}\right).
\]

Thus the strict interior is already attained. Approximation by ratios tending to Gamma_r gives the boundary with A,Q>0. Letting one of A,Q tend to zero gives the two axes, with C->0. This proves (35). Theorem 1 proves the equivalent fixed-domain conic-hull statement. \(\square\)

For real coefficients x,y,z, the associated exact dual criterion is

\[
 xA+yQ+zC\ge0\quad\text{for every compatible compact map}
\]

if and only if

\[
 \boxed{x,y\ge0,\qquad xy\ge\Gamma_r z^2.} \tag{37}
\]

Indeed the smallest permissible C is -2 sign(z)sqrt(Gamma_rAQ), and positivity of the resulting binary quadratic form gives (37).

This cone theorem is a relaxation description, not an evaluation of Gamma_r. It shows precisely what a moment-only relaxation can and cannot add: after compatibility is compressed into these three integrated moments, the single remaining parameter is the original sharp constant. Disjoint mixtures and concentration geometry cannot determine it.

## 6. Consequences for the sharp problem

The source's nonconcentration theorem is correct with its stated uniform-integrability assumption. Its scaling example can be strengthened to the following exact conclusions:

1. The whole sharp constant survives inside the class A=1, Q->0, Dphi->0 in measure.
2. A positive ratio forces quartic concentration at amplitude Q^{-1/2} and total area Q^2, with optimal exponents.
3. The limiting concentration measure may be diffuse, singular continuous, atomic, or any mixture; it need not select a place to blow up.
4. Even after allowing arbitrary L^4-critical translations and isotropic dilations, a positive-ratio near-kernel sequence can have no nonzero profile.
5. If one can genuinely split the moments into disjoint or asymptotically disjoint components, selecting the best component is sufficient. Establishing such a split or a compatible cutoff-and-renormalization theorem for arbitrary fields is the missing step; it is not supplied by ordinary weak compactness.

Accordingly, a valid next theorem would need to retain the normalized quadratic and cubic defects, or prove a compatible amplitude-renormalized selection result. Merely proving tightness of the quartic-energy measure, checking that it has no atoms, or extracting finitely many critical spatial profiles cannot settle Gamma_r.

Nothing here promotes conformal-background control to arbitrary full-rank backgrounds. Even a proof Gamma_r<=1 would retain that separate source limitation.

## 7. Prior literature and actual reading scope

The distinctions between oscillations, concentration, and generalized defect information are classical. The elementary constructions here must not be presented as inventing those subjects.

- Fonseca, Muller, and Pedregal, Analysis of Concentration and Oscillation Effects Generated by Gradients, SIAM J. Math. Anal. 29 (1998), 736–756, DOI 10.1137/S0036141096306534. The primary publisher abstract states a joint treatment for L^p-bounded gradients, recording oscillations by Young measures and concentration by a varifold. Only its abstract, metadata, and reference list were read in this worker. Its detailed theorem is not imported as a premise. [Primary publisher record](https://epubs.siam.org/doi/10.1137/S0036141096306534).
- Kinderlehrer and Pedregal, Characterizations of Young Measures Generated by Gradients, Archive for Rational Mechanics and Analysis 115 (1991), 329–365. The primary publisher record was read. Its characterization theorem is not needed in these elementary proofs, and no priority claim is made for the law-based interpretation. [Primary publisher record](https://link.springer.com/article/10.1007/BF00375279).
- Pedregal, Characterization of Homogeneous Gradient Young Measures in Case of Arbitrary Integrands, Annali della Scuola Normale Superiore di Pisa 29 (2000), 531–546. The primary Numdam publication record was read as a scope comparator; its proof is not a premise. [Primary journal archive](https://www.numdam.org/item/ASNSP_2000_4_29_3_531_0/).

The new specialized claims promoted in this worker are the quantitative estimate (21), its critical-scale consequence (16), and their exact combination with the moment-preserving cloud and no-profile construction for this conformal ratio. Historical originality is UNKNOWN. The elementary transplantation, cone, and disjoint-mixture arguments are generic homogeneous-variational tools.

No published or preprint claim resolving the planar rank-one-convexity/quasiconvexity problem is used.

## 8. Reproducibility and limitations

The accompanying exact verifier independently checks:

- the cubic expansion (1);
- the positive Gram identity (6), principal minors, inverse trace, and explicit coercivity constant;
- all exponents in (10), (12), (25), (27), and (36);
- the exact compact tent-template moments and positive ratio (33);
- exact rational cloud sums and the equality case of disjoint-component Cauchy–Schwarz;
- an exact Laurent-polynomial periodic frequency replication fixture.

The verifier does not certify the analytic interpolation theorem, Holder/Markov arguments, cutoff limits, weak convergence, or the continuum profile statement. Those proofs are supplied above. Its receipt is an algebra/integral receipt, not formal mathematical verification or an all-gradient sharp bound.

Run, from this directory:

    python3 verify_exact.py

External mathematical correctness and historical priority remain unreviewed. Gamma_r<=1 remains open in this worker.
