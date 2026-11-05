# Companion: finite acquisition for sector-bounded passive oscillator baths

## Status and purpose

This is an analytic companion construction. It extends the accepted passive-relaxation bridge to positive mixtures of damped oscillators, while preserving the actual finite trap, finite-bin metrology, retained initial state, finite release, and finite numerical operation. It is not a claim of a new exponential-compression scale, and no complete large-dictionary experiment was executed for this companion. The main programme can instead use the broader random-window construction for an LTI plant; that construction trades this deterministic damping geometry and nonlinear visible law for linear superposition and a randomized deployment time.

## 1. Physical class

Let nu be an unknown positive finite measure on pairs (lambda,omega), with mass at most B, lambda>=0, and |omega|<=Q lambda for a declared finite Q. Put C=1+Q. For each pair let a=-lambda+i omega. A complex state means two real mechanical internal coordinates. The system is

\[
\dot x=-V'(x)-\operatorname{Re}\int z_a\,d\nu+f,
\qquad \dot z_a=a z_a+\dot x.
\tag{1}
\]

The supplied visible law is strongly monotone by mu>0 and locally Lipschitz with computable bounds. The initial bath energy is at most E0=(1/2)int |z_a(0)|^2 dnu. The local drag is normalized to one. The actual apparatus has the moving-trap, finite force/position average, clock, release and independently movable local viscous-support operations declared in the accepted bridge. The metrology can be noisy and have bounded systematic errors; any force backaction is charged.

The energy identity is

\[
\frac{d}{dt}\left[V(x)+\frac12\int |z_a|^2d\nu\right]
=f\dot x-\dot x^2-\int\lambda|z_a|^2d\nu.
\tag{2}
\]

Thus the model is passive even though its response can oscillate and change sign. It has a real two-state block realization for every atom, with skew part omega and dissipation lambda. Unbounded rates are treated by the mild semigroup realization; finite spectral truncation and the energy bound justify the same integral identities by limits. No rate moment, hidden dimension or positive lower rate is supplied. Sectoriality makes the only zero-damping atom have omega=0.

The kernel is

\[
K(t)=\operatorname{Re}\int e^{at}d\nu,
\qquad |K(t)|\le B,
\qquad \int_0^\infty |K'(t)|dt\le CB.
\tag{3}
\]

The last bound follows from |a|<=C lambda and integrates before taking the absolute value of the mixture. This inequality is a sufficient bound, not a characterization of all passive kernels.

More precisely, writing beta=nu(total), the derivative bound is C beta and K(0)=beta. The comparisons below use C beta-beta=(C-1)beta<=(C-1)B; they do not subtract a supplied upper mass bound as though it were the actual mass.

Introduce y_a=x-z_a. Then dot y_a=a(y_a-x), and relative to a reference xr,

\[
\dot x+V'(x)+P_K(x-x_r)=f+g(t),
\quad P_Ku=K(0)u+K'*u,
\quad g(t)=\operatorname{Re}\int e^{at}(y_a(0)-x_r)d\nu.
\tag{4}
\]

If |x-xr|<=A_hist over the physical preparation history, solving the y equation gives

\[
\int |y_a(t)-x_r|d\nu\le \sqrt{2BE_0}+CB A_{\rm hist}=:G.
\tag{5}
\]

Indeed the coefficients of the observed-history contribution are bounded by exp(-lambda t)+C(1-exp(-lambda t))<=C. There is no factor equal to the number of probes. Every old-force function with this envelope satisfies

\[
|g'(t)|\le CG/(et),\qquad t>0.
\tag{6}
\]

## 2. Earned moving-trap tracking

Program u(t), with |u|<=A, and use the finite feedforward center

\[
q=x_r+u+\frac{\dot u+V'(x_r)}k.
\tag{7}
\]

Its derivative is a known command derivative, not a specimen-velocity measurement. The trap applies k(q-x). Let e=x-xr-u. At a first crossing of |e|=R, the absolute memory contribution is bounded by CB R. Because |P_Ku|<=(1+C)BA, a sufficient global tracking bound is

\[
\|e\|_\infty\le\max\left\{|e(0)|,
\frac{G+(1+C)BA+\Phi(A)+\epsilon_{\rm act}}
{k+\mu-(C-1)B}\right\},
\quad k+\mu>(C-1)B,
\tag{8}
\]

where Phi(A)=max_{|s|<=A}|V'(xr+s)-V'(xr)|. The proof uses a first-crossing comparison and (3); it does not assume that K is completely monotone. A center-position error eps_q contributes k eps_q to eps_act.

Initial centering is finite. For a fixed center q0, choose xr solving xr+V'(xr)/k=q0. If d0 bounds the initial visible displacement and G0 bounds the initial old force, let

\[
R_0=\max\{d_0,G_0/[k+\mu-(C-1)B]\},\quad a_0=k+\mu+K(0).
\]

Then

\[
|x(t)-x_r|\le d_0e^{-a_0t}+(G_0+CBR_0)/a_0.
\tag{9}
\]

If only a mass bound is known, use the slower exponent k+mu and denominator k+mu. Increasing k makes the second term small; a finite hold makes the first small. The force cap includes |V'(xr)|+kR0. A consistent A_hist is obtained from d0, A and the certified tracking tube, then k is chosen to satisfy (8)-(9).

For a quintic monotone ramp u=A S(t/h), S(s)=10s^3-15s^4+6s^5, the speed/acceleration bounds of the accepted bridge apply unchanged:

\[
U=15A/(8h),\quad U_2=10\sqrt3 A/(3h^2),\quad U_3=60A/h^3;
\quad |\dot q|\le U+U_2/k,\quad |\ddot q|\le U_2+U_3/k.
\tag{10}
\]

The force cap during the probe is |V'(xr)|+U+k delta_x. If acceleration continuity is required, use its accepted septic alternative. Calibration, front-end force range and finite timing are actual resource requirements.

## 3. Finite metrology and the phase-bearing filtered class

The same triangular finite-box observable measures Re int z_a dnu without measuring point velocity:

\[
R=\sum_{r=1}^{2n}a_rF_r-V'(x_r+u)-\frac{X_R-X_L}{w}.
\tag{11}
\]

With the same declared finite averages, one residual has deterministic error

\[
b_{\rm met}=\Omega_V(\delta_x)+\epsilon_V+\epsilon_f
+2\epsilon_x/w+F_{\rm hold}/n
\]

and white-instrument-noise variance at most

\[
v_{\rm met}\le2v_f/(3w)+2v_x/w^3.
\tag{12}
\]

Overlapping windows may share noise; use the joint concentration/union bound as in the accepted bridge. Arbitrary rational endpoints can be scheduled with merged finite bins and streaming sums.

For a ramp and subsequent triangle, define the known complex filter

\[
F(a)=\left[\int_0^h\frac{S'(s/h)}h e^{a(h-s)}ds\right]
\left[\frac{e^{aw}-1}{aw}\right]^2,
\tag{13}
\]

with the continuous value at a=0. The acquired object is

\[
K_*(t)=\operatorname{Re}\int e^{at}F(a)d\nu.
\tag{14}
\]

The factors have modulus at most one, but usually have nonzero phase. K_* is not automatically a positive passive kernel. This is the key difference from a completely monotone bath. The learner must fit the known filtered atoms Re[e^{at}F(a)] with positive weights, and output the corresponding UNFILTERED passive atoms Re[e^{at}].

If D is the nonnegative delay represented by the ramp and triangle, E[D]=h/2+w. Integrating |e^{at}-e^{a(t+D)}| and using |a|/lambda<=C yields

\[
\|K-K_*\|_{L^1(0,T)}\le CB(h/2+w).
\tag{15}
\]

The fitted unfiltered kernel pays the same bound for its own filtering. Thus the complete unfiltered comparison includes TWO such terms. No deconvolution is performed.

After an aged baseline of duration Ha>2w, subtract a baseline from every post-ramp residual and divide by A. A sufficient simultaneous report allowance is

\[
\eta_a=\frac{CG(h+T+4w)/(e(H_a-2w))
+2(1+C)B\delta_x+2b_{\rm met}}A
+\sqrt{\frac{4v_{\rm met}\log(2M/\alpha_a)}{R_a A^2}}
+\eta_{\rm clock}+\eta_{\rm report}.
\tag{16}
\]

Every repeated probe pays its reverse ramp and aged baseline. Equation (5) applies throughout, so there is no hidden reset. Fixed systematic errors impose accuracy floors.

## 4. Finite positive fitting from those reports

Normalize time by T and mass by B. Let eps=zf/(BT) in (0,1). Put

\[
a_*={\varepsilon\over16},\quad C=1+Q,\quad\rho=1+1/C,
\quad J=\lceil\log_2(1/a_*)\rceil,
\]

\[
n_c=\lceil2C\rceil\lceil\log_2(256C/\varepsilon)\rceil,
\quad L_c=\lceil\sqrt{2n_c-1}\rceil,
\quad d={\varepsilon\over16L_c},\quad M=J n_c.
\tag{17}
\]

Partition [a_*,1] into J intervals with endpoint ratio at most two. On each use nc Chebyshev-root nodes. Round a node in an interval beginning at a_j to a rational with error at most d a_j/(8C). Require the physical reports to obey |yi-k_*(tilde ti)|<=d.

Both true and fitted filtered kernels extend holomorphically into Re z>Q|Im z| and have modulus at most one there. For an interval [a,2a], its Bernstein ellipse with parameter rho has leftmost real coordinate a[3/2-(rho+rho^-1)/4] and maximal imaginary coordinate a(rho-rho^-1)/4. The containment condition follows from

\[
(1+Q)\rho+(1-Q)\rho^{-1}={4C+1\over C+1}<4<6.
\tag{18}
\]

For a bounded analytic function, Chebyshev interpolation has error at most 4(C+1)rho^-nc. Applying this to the difference gives at most 16C rho^-nc. Discrete cosine orthogonality bounds the Lebesgue constant by sqrt(2nc-1). The real-time derivative is bounded by C/(e t), so the rational-node rounding adds at most d/2 to the difference at each exact node. Consequently, if an emitted positive-weight filtered model obeys |hat k_*(tilde ti)-yi|<=r, then

\[
\|k_*-\widehat k_*\|_1
\le 2a_*+16C\rho^{-n_c}+L_c(r+2d).
\tag{19}
\]

Unlike the positive relaxation case, both kernels can be negative, so the unsampled initial interval costs 2a_*.

### A finite rational dictionary with a true witness

Let Smax=1+h/T+2w/T, lambda0=d/(16 C Smax),

\[
H_\lambda=\lceil32C/d\rceil,\qquad
H_r=\max\{1,\lceil32Q/d\rceil\}.
\]

Let lambda_max=2 ceil(log2(16/d))/a_*, and choose the first R such that lambda0 2^R>=lambda_max. Use rates

\[
\lambda=\lambda_0 2^j(1+\ell/H_\lambda),
\quad 0\le j<R,\quad0\le\ell<H_\lambda,
\]

plus the last endpoint. Pair them with r=Q l/Hr, l=0,...,Hr and omega=r lambda. Add the frozen atom (0,0). Negative omega gives the same real filtered atom and need not be duplicated.

Very slow atoms round to the frozen atom, with error <=d/16. For middle atoms, round lambda and r down. Since

\[
|a-a'|/\lambda'\le C/H_\lambda+Q/H_r\le d/16,
\]

their exponential difference at every nonnegative time, including filtered times, is at most d/16. Fast atoms above the cutoff can be discarded: every rounded sample time is at least a_*/2 and their contribution is <=d/16. Therefore every admitted measure has a positive finite-dictionary witness with mass at most one and report discrepancy <=d/16 before report noise. This witness proves feasibility; the algorithm never sees the hidden measure.

Evaluate each filtered atom to rational error d/4 and solve

\[
w\ge0,\quad\sum_jw_j\le1,\quad |\overline A w-y|\le2d.
\tag{20}
\]

Finite rational LP is available. A finite enumeration of rational support and weights is an alternative guaranteed algorithm. Conic Caratheodory elimination on the M reports plus mass keeps at most M+1 atoms. Round retained weights down with total loss at most d/8. Exact interval checking gives r<=19d/8. The right side of (19) is at most 59 eps/128<eps/2. All constants can be conservatively rounded upward.

The final passive, unfiltered model therefore satisfies

\[
\boxed{\|K-\widehat K\|_1
\le 2CB(h/2+w)+BT[2a_*+16C\rho^{-n_c}+L_c(r+2d)].}
\tag{21}
\]

Complex exponentials, the polynomial ramp integral and the finite triangle filter are computable with rational Taylor enclosures, scaling and squaring, and finite arithmetic. Their arguments are bounded by the explicit largest dictionary rate and horizon. There is no transcendental coefficient oracle. In (13), the quintic ramp factor has the entire expansion sum_{k>=0}(ah)^k/k! times 60/[(k+3)(k+4)(k+5)], which supplies a direct interval implementation if desired.

The resource counts are

- M,m=O(C log(C/eps) log(1/eps)); every nonzero oscillator has two real states.
- D<=1+(R Hlambda+1)(Hr+1) dictionary atoms, with all grid parameters above explicit.
- For fixed Q, D is polynomial in eps^-1, with no hidden dimension factor.
- Encoded model bits are O(m[log(C/eps)+scale bits]); the dyadic rational grid avoids encoding a long product of nearly equal ratios.
- Fitting time and workspace depend on D. The mode bound is not a claim that fitting or acquisition are equally small.

## 5. Retained initialization and finite release

After calibration hold |x-xr|<=delta_x for Hg. Read the actual bath force Re int(y-x)dnu over the last positive normalized window of support b<Hg, obtaining c with metrology error eta_g. Solving the y equation during the hold gives

\[
\sup_{0\le t\le T}|g_r(t)-c|
\le\eta_g+(1+2C)B\delta_x+
\frac{CG(b+T)}{e(H_g-b)}.
\tag{22}
\]

The hidden displacement caused by the imperfect hold costs CB delta_x; the measured force differs from the old homogeneous force by (1+C)B delta_x. Frozen force survives and is measured.

Release the stiffness from k to zero over tau, keeping its last center fixed, while the local viscous support rises to the selected initial force. Put

\[
D_r=G+F_r+|V'(x_r)|,\qquad
d_r=((C-1)B-\mu)_+.
\]

A first-running-maximum comparison gives

\[
\delta_{\rm in}\le
\begin{cases}
\delta_x e^{d_r\tau}+D_r(e^{d_r\tau}-1)/d_r,&d_r>0,\\
\delta_x+D_r\tau,&d_r=0.
\end{cases}
\tag{23}
\]

The release-aware old-force uncertainty is

\[
\gamma_{\rm rel}=\eta_g+(1+C)B\delta_x+CB\delta_{\rm in}
+\frac{CG(b+\tau+T)}{e(H_g-b)}.
\tag{24}
\]

The actuator requires finite stiffness slew 15k/(8tau), support startup acceleration 15F/(8tau), and subsequent acceleration bounded by the input time modulus. Support speed, travel, force, work and calibration are charged exactly as in the accepted bridge, using the enlarged state bounds. An instantaneous release or a free force oracle is not used.

## 6. Prediction certificate and finite execution

Initialize all learned oscillator states at zero, and the visible coordinate at xr. The simulator is

\[
\dot q=-V'(q)-\operatorname{Re}\sum_jw_j r_j+f+c,
\quad\dot r_j=a_j r_j+\dot q,\quad r_j(0)=0.
\tag{25}
\]

Let tilde q be the actual numerical path, rho its residual in this equation, and U its certified maximum slope. Put R= zeta U+gamma_rel+||rho||infinity+xi_f. The physical error obeys

\[
\dot e+a_V(t)e+P_Ke=r(t),\quad a_V(t)\ge\mu,
\quad |r(t)|\le R.
\tag{26}
\]

A direct first-running-maximum certificate, valid for any known strongly monotone visible law, is

\[
\|e\|_\infty\le
\begin{cases}
\max\{\delta_{\rm in},R/[\mu-(C-1)B]\},&\mu>(C-1)B,\\
\delta_{\rm in}+RT,&\mu=(C-1)B,\\
\delta_{\rm in}e^{dT}+R(e^{dT}-1)/d,&d=(C-1)B-\mu>0.
\end{cases}
\tag{27}
\]

No dominance premise is required for the finite-horizon theorem; loss of dominance is paid through the stated amplification.

A second certificate uses passivity and can be independent of Q. Realize P_K e by w_a satisfying dot w_a=a w_a+dot e and w_a(0)=e(0). If mu<=a_V(t)<=L on a known common reachable interval, then

\[
E_e=\tfrac\mu2 e^2+\tfrac12\int |w_a|^2d\nu,
\quad E'_e\le\tfrac12r^2+\frac{(L-\mu)^2}{\mu}E_e.
\]

Hence, with c_L=(L-mu)^2/mu,

\[
|e(t)|\le e^{c_Lt/2}
\left[(1+B/\mu)\delta_{\rm in}^2+
\frac1\mu\int_0^t e^{-c_Ls}r(s)^2ds\right]^{1/2}.
\tag{28}
\]

For the quadratic law V'(x)=mu x+v0, the sharper direct square completion gives

\[
|e(t)|\le\left[(1+B/\mu)\delta_{\rm in}^2+
\frac1{2\mu}\int_0^t r(s)^2ds\right]^{1/2}.
\tag{29}
\]

Reachable intervals for L are earned from (2), the supplied energy bound, the finite preparation history, and the bounded later input. In particular H(t)<=H(0)+int f^2/4; strong convexity converts that energy bound into a visible-coordinate interval. The surrogate uses V-cq and includes its residual in the delivered input allowance.

For finite computation, use piecewise-linear q and exact within-step modal formulas

\[
r_j(s)=e^{a_js}r_j(0)+v\frac{e^{a_js}-1}{a_j},\quad 0\le s\le\Delta.
\tag{30}
\]

The scalar endpoint equation has derivative at least 1/Delta+mu-B. Thus choosing Delta<=1/(2B), when B>0, guarantees a monotone bisection problem. B=0 needs no such restriction. Rational enclosures of the complex exponentials and finite state intervals implement it. A safe within-step residual bound, apart from accumulated enclosure errors, is endpoint_error+Delta[(L+B)|v|+Lf+sum_j w_j|a_j|R_j], where R_j bounds the complex modal magnitude throughout the step. One may take R_j<=|r_j(0)|+|v|Delta. This supplies finite step halving and finite precision termination because the fitted rate set is finite. Modal work is O(m) per step, plus one scalar solve. The phase-bearing mode registers must remain two-dimensional; deleting their imaginary parts would invalidate the operation.

The one successful acquisition/initialization event supports every later computable finite-modulus input on the chosen horizon. Physical replay still requires its own initialization. The cost of choosing or optimizing an input is additional.

## 7. Comparison and limitations

Fast sectorial convolution is established machinery. Schadle, Lopez-Fernandez and Lubich's fast oblivious convolution quadrature computes N steps with O(N log N) arithmetic and O(log N) active memory from a sectorial Laplace-transform access model. Sectorial analyticity and exponential compression are therefore not new claims here. Bockius and collaborators already obtain positive-real Markov models from sampled correlation data, while Lei, Baker and Li obtain rational GLE parameterizations, including oscillatory response. Recent spectral filtering also gives dimension-independent prediction in substantial linear-system settings.

The companion's additional work is the declared finite-control report operation, its phase-correct positive fit, the retained-force initialization, and composition to the actual numerical output. It is a sufficient acquisition theorem for normal damped oscillator mixtures, not every passive operator. Its finite-Q condition excludes a nonzero lossless frequency, and its resource bounds worsen with Q. The separate random-window programme is more consequential if its quadratic passive storage and superposition premises are available: it can avoid this damping condition entirely by changing the initialization and representation.

Primary references inspected:

1. Schadle, Lopez-Fernandez, Lubich, Fast and Oblivious Convolution Quadrature, 2006, https://arxiv.org/abs/math/0504461 .
2. Lei, Baker, Li, Data-driven parameterization of the generalized Langevin equation, 2016, https://pmc.ncbi.nlm.nih.gov/articles/PMC5167214/ .
3. Bockius et al., Model reduction techniques for the computation of extended Markov parameterizations for generalized Langevin equations, 2021, https://arxiv.org/abs/2101.02657 .
4. Hazan et al., Spectral Filtering for General Linear Dynamical Systems, 2018, https://papers.nips.cc/paper_files/paper/2018/file/d6288499d0083cc34e60a077b7c4b3e1-Paper.pdf .

