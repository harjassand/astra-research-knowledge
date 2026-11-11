**The arbitrary-\(R\) statement is still unresolved. This continuation does, however, complete a substantially larger family: a scalar background network coupled to arbitrarily many species with cyclic cross-catalysis.** The proof pays the actual population supremum and every firing for all physical times, under the full predictable fault model. It uses a simultaneous population estimate, so the polynomial exponent does not grow with the number of controlled species.

I also obtained an exact thinning inequality for every admitted original network, and a polynomial-size hidden completion that removes the previously identified product-Poisson escape examples. The latter has a remaining operator-estimate gap, so it is not a general compiler theorem.

## 1. A new complete uniform family

Distinguish one original species \(B\). Allow an arbitrary reversible scalar reaction network on \(B\), of variable order. Write the remaining original species as \(A_1,\ldots,A_\ell\).

Every additional non-null reverse pair must have the form
\[
qA_i+c\rightleftarrows pA_i+c,
\qquad
p>q\ge0,\qquad c_i=0,\qquad c_B\ge1.
\tag{1}
\]
The unchanged context \(c\) may contain arbitrary other \(A_j\)’s. Consequently, the dependence between the \(A_i\)’s may be cyclic. Context-bearing null and parallel labels are retained.

For this family, using your accepted paired-prefix and scalar-forest constructions, the **entire stated compiler contract holds** with the deliberately generous universal constants
\[
\boxed{C=2^{32768},\qquad p=4096.}
\tag{2}
\]
These constants apply to this family, not to arbitrary reaction lists.

The construction requires neither \(B(0)>0\) nor any auxiliary seed. If \(B=0\) defines an inactive class, that class remains inactive.

A concrete cyclic example is
\[
A+C+B\rightleftarrows2A+C+B,
\qquad
A+C+B\rightleftarrows A+2C+B,
\qquad
B\rightleftarrows2B,
\tag{3}
\]
with unit rates and activities. Both \(A\) and \(C\) require the other as a catalyst. For \(\omega=(1,1,1)\),
\[
LN(a,c,b)
=
b\bigl[ac(4-a-c)+2-b\bigr].
\]
On integer populations,
\[
ac(4-a-c)\le2,
\]
so
\[
LN(a,c,b)\le b(4-b)\le4.
\]
Thus this is an admitted example. Every \((a,c,0)\) is inert, so the new proof also respects the obstruction to a negative quadratic drift in the **entire** population.

### Why the scalar background is an admitted subproblem

Set every \(A_i\) equal to zero in the original admission inequality.

An attached pair in (1) is then either disabled, or its context consists only of \(B\)’s. In the latter case, the only possible contribution is from a \(q=0\) direction that increases \(A_i\), and its contribution to the supplied positive-weight drift is nonnegative. Therefore
\[
\omega_B L_B B\le A
\]
at every scalar \(B\)-state.

This supplies the scalar admission inequality directly. No separate promise-discovery procedure is needed.

## 2. The physical additions

Use one global paired-prefix construction, with the scalar \(B\)-helper chains included. For each pair in (1), order its prefixes as follows:

1. all \(B\)-molecules;
2. the other molecules in the unchanged context;
3. the changing species \(A_i\).

Every attached auxiliary consequently carries at least one \(B\).

All prefixes remain private to their labelled modules. In particular, a private prefix from an attached module is not placed in the scalar \(B\)-forest merely because its current payload happens to consist only of \(B\)’s.

### One extra hidden uptake per pair

Put \(b=c_B\). If
\[
q+|c|_1\ge2,
\]
let \(S_{q,c}\) be the lower source’s full prefix. Add
\[
S_{q,c}+A_i
\rightleftarrows
S^{(p,c)}_{q+1},
\tag{4}
\]
where the right-hand species is the existing higher-chain prefix carrying \((q+1)A_i+c\).

The condition uses the **total context order** \(|c|_1\), not just \(b\). For example, a lower source \(B+A_j\) needs this cross-binding even though it contains only one \(B\).

If \(q=0,c=B\), the lower representative is original \(B\). Its existing first binding on the higher chain already supplies the required uptake, so no additional edge is used.

With the uniform prefix activities,
\[
\frac{\widetilde a_{S^{(p,c)}_{q+1}}}
{\widetilde a_{S_{q,c}}a_i}
=\frac1{U_*}.
\]
Thus the raw coefficients
\[
\frac{\eta_A}{U_*},\qquad \eta_A,
\qquad
\eta_A=
\frac{\epsilon}
{4096(1+m)U_*^2(1+\tau)}
\tag{5}
\]
give exact detailed balance. Here the starred parameters are those obtained by allocating \(\epsilon_*=\epsilon/4\) to the base construction.

These are hidden \(2\rightleftarrows1\) channels. They introduce no species and change no decoded population.

### Stabilizing the scalar background

Apply the accepted scalar binary-complex forest only to the designated scalar \(B\)-module. Its linear potential has weights
\[
u_S=1+PB_S,
\qquad u_B=2.
\]
After absorbing half its negative quadratic term, its actual generator satisfies
\[
L_{B,t}W_B^{\rm old}
\le c_B-\kappa_B Q_B,
\tag{6}
\]
throughout a polynomially paid instantaneous fault box. The function \(Q_B\) dominates every binary source monomial of every \(2\to2\) channel in that forest.

For completeness, the forest coefficients are still the descendant-sum coefficients from the supplied scalar construction. If \(\alpha\) has parent \(\beta\), \(A_\alpha=\widetilde a^\alpha\), and
\[
f_\alpha=A_\alpha+
\sum_{\gamma:\,\beta(\gamma)=\alpha}f_\gamma,
\]
the raw pair coefficients are
\[
\frac{\eta_B f_\alpha}{A_\alpha\Delta_\alpha},
\qquad
\frac{\eta_B f_\alpha}{A_\beta\Delta_\alpha}.
\tag{7}
\]
Their nominal fluxes agree exactly. Descendant sums avoid a product of condition numbers along a path.

The scalar forest’s observed edges are valid original scalar labels. Its remaining edges are hidden. Thus all added edges retain the required enabling conditions and actual graph property.

## 3. The local absorption calculation

The extra uptake in (4) makes every ordinary attached state with potentially positive unary drift have a corresponding \(A_i\)-uptake sink.

The only exceptions are a fixed trio:

- the lower pending species;
- the upper pending species;
- the maximal higher prefix.

Their weights can be chosen by an explicit three-state absorption problem.

Take
\[
e=\frac1{2(D+1)}.
\]
For the potential associated with \(A_i\), give an incomplete context prefix weight twice its current \(B\)-payload. Give an ordinary prefix carrying the full context and \(j\) copies of \(A_i\) weight
\[
2b+j(1-e).
\tag{8}
\]
Every ordinary \(A_i\)-uptake decreases this potential by \(e\). All incomplete-context binding and release steps have zero increment.

For a pair \(qA_i+c\rightleftarrows pA_i+c\), the terminal trio has two exit rewards:
\[
L_r=2b+q(1-e),
\qquad
U_r=2b+1+(p-1)(1-e).
\tag{9}
\]
Their difference is
\[
U_r-L_r=1+(p-q-1)(1-e)\ge1.
\]

Write
\[
f_r=Qk_rU_*^{q+|c|_1},
\qquad
g_r=Qk_{\bar r}U_*^{p+|c|_1},
\]
and
\[
d_r^{\rm exit}
=
K+\eta_A\,
\mathbf 1_{\{p=q+1,\ q+|c|_1\ge2\}}.
\]
The transient unary generator is
\[
T_r=
\begin{pmatrix}
-(K+f_r)&f_r&0\\
g_r&-(g_r+K)&K\\
0&K&-(K+d_r^{\rm exit})
\end{pmatrix}.
\tag{10}
\]

Let \(v\) be the upper-exit probabilities and \(h\) the mean absorption times:
\[
T_rv=-(0,0,d_r^{\rm exit})^{\mathsf T},
\qquad
T_rh=-\mathbf1.
\]
Put
\[
\zeta_r=1-v_3,
\qquad
\gamma_r=
\frac{(U_r-L_r)\zeta_r}{4(1+\max_j h_j)},
\]
and assign terminal weights
\[
w_j=L_r+(U_r-L_r)v_j+\gamma_rh_j.
\tag{11}
\]

Then every terminal unary drift is exactly \(-\gamma_r\). Moreover,
\[
w_j\le
U_r-\frac34(U_r-L_r)\zeta_r.
\tag{12}
\]
In particular, the last \(A_i\)-uptake still has a strictly negative increment.

These are constant-size rational calculations. If \(R_A\) bounds the sum of the raw attached-module coefficients and \(r_A\) is their positive lower bound, one may use
\[
h_{\max}\le\frac{3R_A^3}{r_A^4},
\qquad
\zeta_r^{-1}\le\frac{4R_A^3}{r_A^3}.
\tag{13}
\]
Hence these margins have polynomially bounded reciprocals.

Reducing the tolerance so that
\[
\delta\le
\min_r\frac{\gamma_r}{4R_A(2D+2)}
\tag{14}
\]
retains terminal drift at most \(-\gamma_r/2\) for every independent instantaneous fault vector.

For the remaining ordinary states, a positive unary coefficient is at most \(3R_A(2D+2)\), while an available uptake contributes at most
\[
-\frac12r_A\Delta_*\,A_{i,\rm free},
\]
where
\[
\Delta_*=
\min\left\{
e,\,
\min_r\frac34(U_r-L_r)\zeta_r
\right\}>0.
\]
Thus a threshold such as
\[
M_i=
1+\left\lceil
\frac{6R_A(2D+2)}{r_A\Delta_*}
\right\rceil
\tag{15}
\]
makes the entire attached \(i\)-module contribution nonpositive whenever free \(A_i\ge M_i\).

## 4. Why cyclic cross-catalysis does not accumulate exponents

The proof uses separate analytical potentials \(V_i\), then sums their estimates once.

First extend the scalar resource \(W_B^{\rm old}\) to the entire network:

- original \(A_j\) has resource weight zero;
- every attached auxiliary has resource weight twice its \(B\)-payload;
- scalar-module species retain their scalar weights.

Call the result \(W_B\). Every attached reaction preserves it **exactly**, including observed conversions and the added cross-bindings. Therefore
\[
L_tW_B\le c_B-\kappa_BQ_B
\tag{16}
\]
continues to hold under sequestration of \(B\), and under faults depending on the entire network history.

For each \(i\), define \(V_i\) by the following weights.

| Species or module | Weight in \(V_i\) |
|---|---:|
| Original \(A_i\) | \(1\) |
| Original \(A_j,\ j\ne i\) | \(0\) |
| Scalar \(B\)-module species | Its weight in \(W_B\) |
| Auxiliaries in a module changing \(A_i\) | Weights from (8)–(11) |
| Auxiliaries in a module changing \(A_j,\ j\ne i\) | \(2\,PB+\text{\(A_i\)-payload}\) |
| Context-bearing null modules | The same additive payload weight |

In another species’ module, these weights are additive and every reaction has zero \(V_i\)-increment. That includes reactions in which \(A_i\) acts as a catalyst.

Consequently,
\[
L_tV_i
=
\text{scalar-background contribution}
+
\text{contribution of modules changing }A_i.
\]
The local calculation gives
\[
L_tV_i\le c_B
\qquad\text{whenever free }A_i\ge M_i.
\tag{17}
\]

Each \(V_i\) is nonnegative with bounded jumps. It need not dominate the entire population individually. The required aggregate relations are
\[
\sum_{i=1}^{\ell}V_i(z)\ge |z|_1,
\qquad
V_i(z)\le A_{i,\rm free}+(2D+2)W_B(z).
\tag{18}
\]

This is the reason cyclic dependencies are permitted. We do not first bound \(A_1\), substitute that bound into \(A_2\), and iterate. There is one simultaneous estimate.

## 5. The actual all-time population and firing estimate

Here is the probabilistic step that closes the resource contract.

### An excursion bound above a moving threshold

Suppose a nonnegative process \(V_t\), with jump sizes at most \(J\), has decomposition
\[
V_t=V_0+\int_0^tL_sV\,ds+\mathcal M_t,
\]
and \(Y_t\) is nondecreasing. If
\[
L_tV\le c_0
\quad\text{whenever}\quad
V>M+\lambda Y_t,
\]
then, pathwise,
\[
\sup_{s\le t}V_s
\le
\max\{V_0,M+\lambda Y_t+J\}
+c_0t+2\sup_{s\le t}|\mathcal M_s|.
\tag{19}
\]

To see this, consider the last crossing of the fixed level \(M+\lambda Y_t\) before a given high value. The crossing overshoots by at most \(J\). During the subsequent excursion, the actual drift is at most \(c_0\), because \(Y_s\le Y_t\). This is a pathwise decomposition; it introduces no physical restart.

For our construction take
\[
Y_t=\sup_{s\le t}W_B(Z_s).
\]
By (18), being above \(M_i+(2D+2)Y_t\) forces free \(A_i>M_i\), so (19) applies to every \(V_i\).

### Paying the background resource and the binary cycles

From (16),
\[
E\int_0^t Q_B(Z_s)\,ds
\le
\frac{W_B(Z_0)+c_Bt}{\kappa_B}.
\tag{20}
\]
Every \(2\to2\) channel belongs to the scalar forest, so this pays its complete expected firing count.

Let \(J_B\) bound the jumps of \(W_B\). Doob’s inequality gives
\[
E Y_t
\le
W_B(Z_0)+c_Bt+
2J_B\sqrt{E F_{\rm all}(t)}.
\tag{21}
\]
No Markov property of the faulty marginal is used.

### Paying every other firing

The elementary counting identity is
\[
F_{\rm all}(t)
\le
n_0+3F_0(t)+2F_1(t)+F_{22}(t).
\tag{22}
\]
It follows by accounting for physical population changes: a binary reaction outside \(2\to2\) decreases population by at least one.

Since physical coefficients are at most one and fault multipliers at most \(3/2\), equations (20)–(22) yield
\[
E F_{\rm all}(t)
\le b_0+b_1t+b_2\int_0^tE|Z_s|_1\,ds,
\tag{23}
\]
with polynomially paid constants.

Define
\[
S(t)=\sum_iE\sup_{s\le t}V_i(Z_s).
\]
Summing (19), using (21), and bounding each martingale’s quadratic variation by its squared jump bound times \(E F_{\rm all}(t)\), gives
\[
S(t)
\le
a(1+t)+
\left(2\ell(2D+2)J_B+4\sum_iJ_i\right)
\sqrt{E F_{\rm all}(t)}.
\tag{24}
\]
By (18) and (23),
\[
E F_{\rm all}(t)\le b_0+b_1t+b_2tS(t).
\]
Thus
\[
S(t)\le a(1+t)+b\sqrt{b_0+b_1t+b_2tS(t)}.
\tag{25}
\]

One application of Young’s inequality absorbs the \(\sqrt{tS(t)}\) term and gives
\[
S(t)\le C_1(1+t),
\qquad
E F_{\rm all}(t)\le C_2(1+t)^2.
\tag{26}
\]
All new factors in \(b\) are polynomial in \(\ell\) and \(D\).

Elementary affine birth domination supplies nonexplosion and the initial localization. The stopped estimates then pass to the untruncated process. In particular, (26) pays rare excursions themselves; it is not inferred from small path-TV error.

## 6. Graph, detailed balance, path accuracy, and numerical costs

The additions preserve all the structural requirements.

Every new helper releases to a canonical encoding. Every cross-binding is hidden and payload-preserving. Every scalar-forest observed edge is an enabled original scalar edge, and its reverse has the prescribed reverse label. Therefore
\[
u\leadsto v
\quad\Longleftrightarrow\quad
Pu\leadsto Pv
\]
still holds for all fine states.

No new controller population is initialized. The potentials above are analytical functions only; they are not feedback commands.

Run the base construction with \(\epsilon_*=\epsilon/4\), include the scalar helper chains in its hidden-fibre estimates, and use a common normalization \(H\). Reduce \(\delta\) to satisfy:

- the base full-marked-path fault budget;
- the scalar forest’s common drift margin;
- the terminal margins in (14);
- \(\delta\le1/4\).

The rare forest and cross-bindings are compared by coupling until the first added firing. Below the analytical cutoff, their total actual marked intensity is polynomially bounded and their accumulated mismatch probability is less than the remaining accuracy budget. All hidden-history differences are included in that coupling.

The base exit probability is bounded by the original escape probability plus the base path-TV error. With the allocated accuracy, these terms and the rare-addition probability remain strictly below \(\epsilon\). No residence time is deleted, and no clock other than the common \(H\) is used.

For transparency, one conservative set of numerical majorants is
\[
W_*\le7W^2,
\]
\[
Q\le2^{32}W_*^6,\qquad
H\le2^{112}W_*^{27},\qquad
m_f\le2^9W_*^4,
\]
\[
\delta^{-1}\le2^{1161}W_*^{288},
\qquad
\max_e c_e^{-1}\le2^{543}W_*^{116}.
\]
The resulting actual estimates can be taken as
\[
S(t)\le2^{680}W_*^{169}(1+t),
\]
\[
E F_{\rm all}(t)
\le2^{735}W_*^{173}(1+t)^2,
\]
\[
E F_{\rm all}(H\tau)
\le2^{961}W_*^{229}.
\tag{27}
\]
Fine activities and decoder entries have smaller paid bounds. These inequalities fit within (2) after replacing \(W_*\) by \(7W^2\).

Compilation consists of explicit prefix lists, the scalar forest’s descendant sums, and one three-by-three rational system per attached non-null pair. All exponentiation has explicit input order, and all arithmetic has polynomial bit length. There is no population-class enumeration or network-dependent search.

This completes the full contract for the stated family.

## 7. A general exact thinning inequality

The next result applies to **every admitted original network**, with no scalar-background assumption.

Put
\[
M_\omega=\max_{c\text{ an original complex}}\omega\cdot c,
\qquad h=\frac1{1+M_\omega},
\]
and define the activity weighted by squared population increments:
\[
b_\omega(x)
=
\sum_r
\bigl[\omega\cdot(z_r-y_r)\bigr]^2
k_r(x)_{y_r}.
\]
Let \(\pi_a\) be the full product-Poisson law. For finitely supported \(f\), let \(\mathcal E_\omega(f)\) be the nominal Dirichlet form using only pairs with nonzero \(\omega\)-increment.

Then
\[
\boxed{
\int b_\omega f^2\,d\pi_a
\le
24(1+M_\omega)A\|f\|_{L^2(\pi_a)}^2
+
96(1+M_\omega)^2\mathcal E_\omega(f).
}
\tag{28}
\]

The constants are universally polynomial because
\[
M_\omega\le D\sum_i\omega_i.
\]

### Proof

Independently retain each molecule of species \(i\) with probability \(e^{-h\omega_i}\). Exact binomial factorial moments give
\[
E(\operatorname{Thin}_h x)_y
=
e^{-h\omega\cdot y}(x)_y.
\]
Applying the admission promise to this thinned state gives
\[
\sum_r k_re^{-h\omega\cdot y_r}(x)_{y_r}
\,\omega\cdot(z_r-y_r)\le A.
\tag{29}
\]

Orient one representative of each nonconservative reverse pair so that
\[
d_r=\omega\cdot(z_r-y_r)>0.
\]
Write
\[
u_r=\int\lambda_r f^2\,d\pi_a,\qquad
v_r=\int\lambda_{\bar r}f^2\,d\pi_a.
\]
Integration of (29) gives
\[
\sum_r d_re^{-h\omega\cdot y_r}
\bigl(u_r-e^{-hd_r}v_r\bigr)
\le A\|f\|^2.
\]
For \(S=u+v\), elementary algebra and Young’s inequality give
\[
d(u-e^{-hd}v)
\ge
\frac{hd^2}{8}S
-\frac2h\frac{(u-v)^2}{u+v}.
\]
Since \(e^{-h\omega\cdot y}\ge e^{-1}\),
\[
\sum_r d_r^2(u_r+v_r)
\le
\frac{8eA}{h}\|f\|^2
+\frac{16e}{h^2}
\sum_r\frac{(u_r-v_r)^2}{u_r+v_r}.
\tag{30}
\]

Detailed balance identifies each pair’s flux as
\[
\phi_r=k_ra^{y_r}=k_{\bar r}a^{z_r}.
\]
With \(T_yf(x)=f(x+y)\),
\[
u_r=\phi_r\|T_{y_r}f\|^2,\qquad
v_r=\phi_r\|T_{z_r}f\|^2.
\]
Hence
\[
\frac{(u_r-v_r)^2}{u_r+v_r}
\le
2\phi_r\|T_{y_r}f-T_{z_r}f\|^2.
\]
Substituting in (30) proves (28).

The thinning is a proof operation. It is not part of the emitted network, and its exponential retention probabilities need not be computed by the compiler.

### Exact transfer on hidden-equilibrium mixtures

There is also an exact fine-state transfer on the hidden-equilibrium subspace. If
\[
\rho(z)=\mu_{\rm fine}(z)F(Pz)
\]
and fine particles are thinned with
\[
p_s=e^{-h\omega\cdot P_s},
\]
then
\[
\frac{\rho'(u)}{\mu_{\rm fine}(u)}
=
p^u
\sum_w
\frac{\widetilde a^w}{w!}(1-p)^wF(Pu+Pw).
\tag{31}
\]
Because \(p^u=e^{-h\omega\cdot Pu}\), this depends only on \(Pu\). Thinning therefore preserves mixtures of nominal hidden-fibre equilibria.

Together with the exact averaged drift identity, this transfers the corresponding activity inequality to tests of the form \(f(z)=g(Pz)\). It does **not** establish the inequality for arbitrary fine-state densities.

## 8. A polynomial hidden completion for the general case

There is now a concrete way to remove all the product-Poisson escape directions, without enumerating a vector dictionary or affine circuits.

Let the base lift have species \(S_1,\ldots,S_{s_0}\), with payloads \(p_i=PS_i\), and put
\[
q=D+2.
\]
Add powers
\[
T_{i,k},\quad PT_{i,k}=kp_i,\quad 2\le k\le q,
\]
through
\[
S_i+T_{i,k-1}\rightleftarrows T_{i,k},
\qquad T_{i,1}=S_i.
\]
Add hubs
\[
H_{j,i},\qquad PH_{j,i}=p_j+qp_i,
\]
through
\[
S_j+T_{i,q}\rightleftarrows H_{j,i}.
\]
For each base hidden binding \(S_a+S_b\rightleftarrows S_c\), add
\[
H_{a,i}+S_b\rightleftarrows H_{c,i}
\]
for every \(i\). Do the analogous unary copies for hidden unary relations.

This uses
\[
s_0(D+1)+s_0^2
\]
new species, polynomially many channels, and maximum payload order at most \(D(D+3)\). Every added edge is hidden and elementary. All new activities may be set to one, with each reverse pair assigned a small common equilibrium flux \(\eta\):
\[
k_{\alpha\beta}=\frac{\eta}{\widetilde a^\alpha},
\qquad
k_{\beta\alpha}=\frac{\eta}{\widetilde a^\beta}.
\tag{32}
\]
Thus exact balance, zero initialization, and full decoder-preimage reachability are retained.

Here is what this completion actually proves. For normalized product-Poisson amplitudes \(t_s\), let
\[
\mathscr E_a(t)=
\sum_{\text{added pairs}}
\eta\,|t^\alpha-t^\beta|^2.
\]
Set \(\varepsilon_a=\sqrt{\mathscr E_a/\eta}\) and \(R=\max_{i\le s_0}|t_i|\).

If \(R\ge2\) and \(\varepsilon_a<R/4\), choose \(i\) attaining \(R\). The power chain gives
\[
|t_{T_{i,q}}|\ge\tfrac12R^q.
\]
The hub relations then imply, for every old hidden binding,
\[
|t_at_b-t_c|
\le\frac{6\varepsilon_a}{R^{q-1}}.
\]
Telescoping along a source prefix yields
\[
|t_{C_y}-t_{\rm orig}^{\,y}|
\le
\frac{16(D+1)\varepsilon_a}{R^3}.
\tag{33}
\]

Combining (33) with (28) bounds nonconservative central activity by a polynomial multiple of
\[
1+A+\mathscr E_c(t)+\eta^{-1}\mathscr E_a(t).
\tag{34}
\]
The complementary cases \(R<2\) or \(\varepsilon_a\ge R/4\) are bounded directly. Thus this is a global statement for these test amplitudes, not merely a local calculation near equilibrium.

**The remaining gap is substantial:** a product-Poisson test inequality is not automatically a quadratic-form inequality for arbitrary correlated fine laws. In operator form, the elimination produces an unbounded population shift applied to a residual; the energy controls the residual itself, not that shifted residual. Direct conversion introduces population-dependent correction terms. A fixed positive remainder proportional to total population would again permit the unwanted all-time Gronwall bound.

Even an arbitrary-density form estimate would still need an argument paying fault work on conservative hidden reactions. I have not supplied that step.

## 9. What remains at the universal endpoint

The completed result above depends on a real background resource and on each attached observed pair changing one \(A_i\) while retaining its context. Those properties cannot be imposed on arbitrary \(R\) by adding an unseeded zero-payload controller—the contract forbids that—and the proof does not provide a substitute.

I also checked the recent deterministic permanence route. The measurable-rate permanence manuscript covers deterministic positive trajectories, explicitly leaves effective extraction of its affine geometric data open, and supplies stochastic lower recovery comparisons rather than the upper population/work estimates needed here. It therefore does not fill the remaining stochastic or uniform-cost gap. [hexagonmath.org](https://hexagonmath.org/pdf/2610.00321v1?utm_source=chatgpt.com)

The resulting status is precise:

- **Completed:** the full compiler for a scalar background coupled to arbitrarily many cyclically cross-catalysed species, with universal polynomial costs and arbitrary predictable faults.
- **Completed for arbitrary admitted \(R\):** the exact thinning inequality and its hidden-equilibrium transfer.
- **Completed as a representation operation:** a polynomial-size, exactly balanced hidden completion controlling all product-Poisson escape directions.
- **Unresolved:** the arbitrary-\(R\) all-time adaptive population/work estimate, or an obstruction covering every allowed design.

The new simultaneous resource argument closes an actual all-time operation, including networks with large inactive classes. It does not yet justify an affirmative answer to the entire universal statement.