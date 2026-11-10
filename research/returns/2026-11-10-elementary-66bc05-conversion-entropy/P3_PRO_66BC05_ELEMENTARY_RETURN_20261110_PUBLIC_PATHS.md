# P3 completed return — elementary robust compiler

Chat: https://chatgpt.com/c/6af3030c-e834-83ec-b294-ad6a7f60aa46. User turn bce2476c-5f03-4c05-90dd-cb319d7c0a21; final 66bc05ad-6aef-5ea0-a64c-f379d793d8ef. UI displays Pro and response complete.

Exact held question: work/astra-renewed-pro-programmes-20261103/P3_FULL_ELEMENTARY_BIMOLECULAR_ROBUST_COMPILER_PRO_20261110.txt (SHA-256 763d020a3d951274080c1315b1e71681a8a64204db6470c6d9add624f203f111). No producer ZIP appeared in Outputs.

The complete available final below was copied via the response Copy control and TextEdit accessibility. Native read supplied the first 20,000 characters, also included below. UI and accessibility serialization may alter formatting and mathematical rendering; byte identity is not asserted. The expanded visible activity and three visible subagent final panels follow, as accessibility output.

## Full response (UI copy)

**I have not resolved the entire universal statement.** I can establish a substantial partial result: using your accepted higher-molecularity compiler, the elementary prefix construction can meet the **full nominal contract on infinite classes**, and it can also meet the **robust finite-time accuracy and physical-cost requirements** with a polynomial numerical rate tolerance.
What I cannot establish is that **every admitted independently perturbed process is positive recurrent and has the required stationary law, stationary first moments, and stationary population bound**. I also do not have an obstruction covering every allowed elementary design. Consequently, this is neither a complete affirmative answer nor a complete negative answer.
The distinction matters here:
**Requirement
What the analysis establishes**
Fixed finite elementary network and fixed linear decoder
Established
Exact decoded communicating classes and permitted decoded moves
Established
Nonexplosion under all admitted errors
Established
Nominal positive recurrence and unique stationary law
Established
Nominal stationary TV and absolute first-moment accuracy
Established with polynomial parameters, including infinite classes
Nominal transient accuracy and all physical costs
Established with polynomial parameters
Perturbed transient TV and absolute first-moment accuracy at one compiled time
Established uniformly over a polynomial numerical error box
Perturbed population and total firing costs through that time
Established uniformly
Perturbed positive recurrence and stationary requirements
**Not established**
Below are the quantitative arguments, followed by a concrete counterexample to automatic spectral-gap inheritance. That counterexample identifies a failed proof route; it does not disprove your universal statement.
**1. Fixed elementary construction and exact graph preservation**
Write the accepted catalytic table as
\[ Y_r=y_r+w_r\longrightarrow Z_r=z_r+w_r, \qquad r=1,\ldots,m. \]
Its nominal constants are denoted by \(\kappa_r\), with
\[ 0<\kappa_r\le1. \]
Run the accepted compiler at accuracy \(\epsilon/16\). Absorb that fixed change of accuracy into its fixed computable constants, so that its nominal mixing time \(T_0\) and rate reciprocals satisfy
\[ T_0,\ \max_r\kappa_r^{-1}\le C W^p, \]
where \(C,p\) depend only on \(R\). Its nominal law at \(T_0\) has TV and absolute coordinate-mean errors at most \(\epsilon/16\).
Set
\[ d_*=\max\!\left(1,\max_r|Y_r|_1,\max_r|Z_r|_1\right). \]
Use the prefix construction in your premises, ordering each complex canonically and sharing identical ordered prefixes. In particular, every auxiliary prefix has a **unique defining parent**.
Let the auxiliary encoding vectors be
\[ c_1,\ldots,c_{s_a},\qquad 2\le |c_j|_1\le d_*, \]
and let \(E\) have these columns. The decoder is
\[ D(n,a)=n+Ea. \]
Thus
\[ |(n,a)|_1\le |D(n,a)|_1. \tag{1} \]
Give prefix \(j\) activity \(\theta\lambda^{c_j}\). Before a common rate normalization, use:
	•	first binding/release constants \(K\theta,K\);
	•	later binding/release constants \(K,K\);
	•	representative-conversion constant \(\kappa_r/\theta\) when \(|Y_r|_1\ge2\), and \(\kappa_r\) otherwise.
Every reaction has at most two molecules on each side.
Every binding or release has decoded change zero. An enabled representative conversion contains the full encoded source \(Y_r\), so its decoded state contains \(y_r\), and its decoded change is \(z_r-y_r\). Hence it realizes an enabled original edge.
Moreover, every fine state releases to the canonical encoding of its decoder value. Reversing that release path reconstructs the fine state. Since the table includes \(w=0\), every original edge lifts between its canonical encodings. Consequently,
\[ \boxed{\widehat\Gamma=\{(n,a):n+Ea\in\Gamma\}.} \tag{2} \]
This is an equality involving the **actual communicating class**, with no replacement by a lattice or compatibility set.
**Nonexplosion is automatic for elementary networks of this kind**
There is a useful fact that applies more generally than this construction:
Every finite mass-action network with at most two molecules on each side of every reaction is nonexplosive for every finite positive rate vector.
Let \(V(u)=1+|u|_1\). A reaction increasing \(|u|_1\) must have zero or one reactant. Therefore
\[ \mathcal LV(u)\le C_0+C_1|u|_1. \]
Stopping and Grönwall’s inequality prevent the population from becoming unbounded in finite time. On a bounded-population set, there are finitely many states and a bounded total firing intensity, including null and parallel channels. Thus infinitely many actual firings cannot accumulate there either.
This proves nonexplosion under the whole admitted error box. It does **not** establish positive recurrence.
**2. Polynomial stationary approximation on infinite classes**
The nominal lift is complex balanced. Its product-form measure is therefore available on each closed irreducible class; this is the standard complex-balance product-form theorem. <u>[web.math.wisc.edu](web.math.wisc.edu/~dfanderson/papers/ACKProdFormFinal.pdf?utm_source=chatgpt.com)</u>
Write
\[ w(x)=\frac{\lambda^x}{x!}, \qquad q_\theta(x)= \sum_{a:Ea\le x} \frac{\theta^{|a|}(x)_{Ea}}{a!}. \]
The decoded stationary law is exactly
\[ \rho_\theta(x) = \frac{\pi_\lambda(x)q_\theta(x)} {\mathbb E_{\pi_\lambda}q_\theta(X)}. \tag{3} \]
The infinite-class estimate can be made quantitative without a class oracle. The key is to use the exact generating function
\[ \boxed{ \sum_{x\in\mathbb N^d} w(x)q_\theta(x)e^{t|x|_1} = \exp\!\left( e^t\sum_i\lambda_i+ \theta\sum_{j=1}^{s_a}\lambda^{c_j}e^{t|c_j|_1} \right). } \tag{4} \]
Using \(q_\theta(x)\le e^{s_a\theta |x|^{d_*}}\) globally would be inadequate: that upper bound can grow too quickly to integrate against Poisson tails. Equation (4) retains the actual compound-Poisson structure.
**A usable normalization bound comes from \(x_0\)**
Because \(x_0\in\Gamma\),
\[ Z_\Gamma\ge w(x_0). \]
Also,
\[ w(x_0)\ge W^{-2|x_0|_1}, \tag{5} \]
since \(\lambda_i^{-1}\le W\) and \(x_0!\le W^{|x_0|_1}\).
This does not require a supplied rare-class lower bound. Its logarithmic cost is controlled directly by the input.
Assume
\[ \theta s_aW^{d_*}\le1. \]
Equations (4)–(5), evaluated at \(t=1/d_*\), give
\[ \mathbb E_{\pi_\lambda} \left[q_\theta(X)e^{|X|_1/d_*}\right] \le e^{4W^2}. \tag{6} \]
Choose, for the static estimate alone,
\[ B_{\rm stat}=16d_*(d_*+1)W^2, \]
and
\[ \boxed{ \theta\le \frac{\epsilon} {128s_a(B_{\rm stat}+1)^{d_*+1}}. } \tag{7} \]
The cases needing no auxiliary prefixes can be handled directly.
For any \(B\ge B_{\rm stat}\), (6) implies
\[ \mathbb E_{\pi_\lambda}\!\left[ q_\theta(X)(|X|_1+1) \mathbf1_{\{|X|_1>B\}} \right] \le (2d_*+1)e^{4W^2-B/(2d_*)} \le\frac{\epsilon}{32}. \tag{8} \]
Inside \(|x|_1\le B\), provided (7) holds with this \(B\),
\[ q_\theta(x)-1 \le \frac{\epsilon}{64(B+1)}. \tag{9} \]
Let \(r_\theta=\pi_\lambda q_\theta\). Combining the interior estimate and the weighted tail gives
\[ 0\le r_\theta-1 \le \frac{3\epsilon}{64(B+1)}. \]
Therefore
\[ \|\rho_\theta-\pi_\lambda\|_{\rm TV} \le r_\theta-1<\frac{\epsilon}{8}. \tag{10} \]
For each coordinate,
\[ \begin{aligned} |\rho_\theta X_i-\pi_\lambda X_i| &\le \pi_\lambda\!\left[|X|_1(q_\theta-1)\right] +(r_\theta-1)\pi_\lambda|X|_1\\ &<\frac{\epsilon}{8}. \end{aligned} \tag{11} \]
Thus **the nominal infinite-class stationary approximation has a polynomial numerical choice of \(\theta\)**.
For example, the reciprocal in (7) is bounded by a fixed-\(R\) constant times \(W^{2d_*+3}\). The cutoff is used only in the proof. No reaction is reflected, killed, disabled, or externally reset at that population.
**3. Polynomial nominal moments uniformly over all time**
The nominal transient population bound can also be made polynomial without first proving a spectral gap.
Let \(\mu\) be the nominal fine stationary measure and
\[ N(u)=|Du|_1,\qquad H=4W^2,\qquad q=\lceil H\rceil, \qquad r=\frac{q}{q-1}. \]
The same generating-function estimates give
\[ \mu(e^{N/d_*})\le e^H, \qquad \mu(j(x_0))\ge e^{-H}. \tag{12} \]
Let \(f_t\) be the density, relative to \(\mu\), of the nominal process started at \(j(x_0)\). The adjoint Markov semigroup contracts \(L^r(\mu)\), so
\[ \|f_t\|_{L^r(\mu)} \le \mu(j(x_0))^{-1/q}\le e. \tag{13} \]
The choice \(r\) close to one is useful: an \(L^2\) estimate would retain an exponentially large initialization factor.
For every fixed integer \(h\ge1\),
\[ N^{hq}\le d_*^{hq}(hq)!\,e^{N/d_*}. \]
Hölder’s inequality and (12)–(13) therefore yield
\[ \boxed{ \sup_{t\ge0} \mathbb E_{j(x_0)}N(Z_t)^h \le 9(5d_*h)^hW^{2h}. } \tag{14} \]
The stationary moments satisfy corresponding bounds. Equation (1) makes these bounds apply to every auxiliary population as well.
A further consequence, used below, is
\[ \boxed{ \sup_{t\ge0} \mathbb E_{j(x_0)} e^{N(Z_t)/(d_*q)} \le e^2. } \tag{15} \]
After all physical rate constants are normalized to at most one, the total labelled firing intensity satisfies
\[ a_{\rm fine}(u)\le M_f(1+N(u))^2, \]
where \(M_f\) is the fixed number of fine channels. Thus
\[ \mathbb E[\text{all actual firings through }T] \le C_R T W^4 \tag{16} \]
in the nominal case.
This counts binding, release, null, and parallel firings. The estimate holds for every supplied finite \(T\); a polynomial mixing time still needs a separate argument.
**4. Nominal polynomial mixing without a global fine-chain spectral gap**
That argument can be supplied using averaging on a bounded region **only as an analytical device**.
**Fast mixing inside a bounded decoded fibre**
Fix \(x\) with \(|x|_1\le B\). Remove the common factor \(K\) from the binding generator and denote the resulting fibre generator by \(F_x\). Its invariant distribution is
\[ \nu_x(a) = \frac{\theta^{|a|}(x)_{Ea}} {a!\,q_\theta(x)}. \tag{17} \]
Suppose
\[ \theta(B+1)^{d_*}\le\frac12, \qquad s_a\theta B^{d_*}\le1. \]
Releasing one whole prefix of encoding \(c\) changes its stationary weight by the factor
\[ \frac{a_c}{\theta}\frac{n!}{(n+c)!} \ge \frac{1}{\theta(B+1)^{d_*}} \ge2. \tag{18} \]
During its at most \(d_*\) partial releases, the weight loses at most a factor \((B+1)^{2d_*}\). Releasing all prefixes takes at most \(d_*B\) steps. There are at most \((B+1)^{s_a}\) states in the fibre, and every used release transition has rate at least one.
An anchored path inequality consequently gives
\[ \operatorname{Var}_{\nu_x}h \le d_*B(B+1)^{s_a+2d_*} \mathcal E_{F_x}(h,h). \tag{19} \]
For the initialization cost,
\[ \nu_x(a)\ge e^{-1}(\theta/B)^B. \]
Only its logarithm is needed. Integrating the finite reversible mixing estimate gives the following safe sup-norm corrector bound:
\[ \left\|F_x^{-1}(I-\Pi_x)\right\|_{\infty\to\infty} \le C_F, \]
where one may take
\[ \boxed{ C_F= 8d_*(B+1)^{s_a+2d_*+4}\theta^{-1}. } \tag{20} \]
**The averaged rates are explicit**
For a representative source of order at least two,
\[ \mathbb E_{\nu_x}a_{Y_r} = \theta(x)_{Y_r} \frac{q_\theta(x-Y_r)}{q_\theta(x)}. \]
The corresponding identity for an original-species source is obtained by replacing the auxiliary count with its free-species count.
Hence the exact averaged decoded rate is
\[ \boxed{ \overline q_r(x)= \kappa_r(x)_{Y_r} \frac{q_\theta(x-Y_r)}{q_\theta(x)}. } \tag{21} \]
On \(|x|_1\le B\), its generator differs from the original catalytic generator by at most
\[ 4s_am\theta(B+1)^{2d_*} \tag{22} \]
in the bounded-function operator norm.
For the comparison, send either process to a cemetery state when its decoded population first leaves \(N\le B\). This defines finite stopped processes for the proof; it is not the implemented network.
Write their fine generator as
\[ KF+S, \]
where \(S\) contains representative conversions. Its total conversion intensity in this region is bounded by
\[ M_0=m\theta^{-1}(B+1). \tag{23} \]
Solving the fibre Poisson equation and applying Dynkin’s formula gives, for a decoded test function bounded by one,
\[ \left| \mathbb E g(DZ_T^{B}) -\mathbb E g(\overline X_T^{B}) \right| \le \frac{8C_F(M_0+2TM_0^2)}{K}. \tag{24} \]
The endpoint corrector terms include the initial canonical state, so fibre-equilibrated initialization is unnecessary. A coordinate-mean test costs only an additional factor \(B\).
**Polynomial parameter choices and removal of stopping**
Choose
\[ B=\lceil C_BW^4\rceil, \qquad \theta= \frac{\epsilon} {128s_am(T_0+1)(B+1)^{2d_*+1}}, \tag{25} \]
and
\[ \boxed{ K= 1+ \frac{1024C_F(B+1)(M_0+2T_0M_0^2)}{\epsilon}. } \tag{26} \]
Here \(C_B\) is a sufficiently large **computable fixed-\(R\) constant**. It can be chosen explicitly from the supplied \(C,p\), the finite table, and the moment constants in (14).
For clarity, there is no circular dependence hidden in the exit estimate. Take the fixed moment order
\[ h=p+4d_*+16. \]
Only conversions can change \(N\), and their raw intensity is at most \(m\theta^{-1}(N+1)\). Therefore
\[ \begin{aligned} \mathbb P(\tau_B^{\rm fine}\le T_0) &\le C_R T_0\theta^{-1}B^{-(h-1)}W^{2h}\\ &\le C_R C_B^{2d_*+2-h}W^{-23}. \end{aligned} \tag{27} \]
The original catalytic process has a corresponding, smaller exit bound.
Because \(h>2d_*+2\), increasing \(C_B\) decreases the bound despite the resulting decrease in \(\theta\). The endpoint first-moment contribution of an exited path is bounded by
\[ \mathbb E[N(Z_{T_0})\mathbf1_{\{\tau_B\le T_0\}}] \le \bigl(\mathbb EN(Z_{T_0})^2\bigr)^{1/2} \mathbb P(\tau_B\le T_0)^{1/2}. \tag{28} \]
Equations (14) and (27) make this contribution smaller than the allocated accuracy budget.
Combining (22), (24), the two stopping errors, and the accepted original accuracy proves nominal transient TV and absolute first-moment errors below \(\epsilon/8\), after fixed enlargement of the constants.
**Physical normalization and complexity**
Equation (26) ensures \(K\ge\theta^{-1}\). Divide every raw rate constant by \(K\), and use physical time
\[ \boxed{T=KT_0.} \tag{29} \]
Every resulting nominal constant is at most one.
All rate reciprocals, \(K\), \(T\), and the total actual firing count are polynomial in \(W\). For example, loose exponents from these formulas are
\[ \theta^{-1}=O_R(W^{p+8d_*+5}), \]\[ T,\ \max_e k_e^{-1} = O_R(W^{5p+4s_a+32d_*+44}), \]
and
\[ \mathbb E[\text{all nominal firings through }T] = O_R(W^{5p+4s_a+32d_*+48}). \tag{30} \]
The compiler evaluates fixed-degree rational expressions. It does **not** enumerate the ball, the fibres, the communicating class, or the stopped generator. Thus the numerical population cutoff used in the proof does not become a numerical-population loop in the binary compiler.
This closes the nominal infinite-class contract under your accepted premise.
**5. Polynomial robustness through the compiled finite time**
The transient requirements can be made robust without assuming that the perturbed chain has a stationary distribution.
Here is a direct argument that includes errors in **every** physical channel.
Use the normalized physical process and write
\[ c=d_*q. \]
Let \(J\) bound the positive change in decoded total population at one reaction; \(J\le2d_*\) is sufficient. Define a second analytical cutoff
\[ B^\sharp = J+ \left\lceil 128(M_f+d_*+J+2)c(T+W^2+1) \right\rceil, \]
and
\[ A=M_f(B^\sharp+1)^2. \]
Choose
\[ \boxed{ \delta= \min\left\{ \frac12,\, \frac{\epsilon} {64d_*(B^\sharp+J+1)(A+1)(T+1)} \right\}. } \tag{31} \]
Both \(B^\sharp\) and \(\delta^{-1}\) are polynomial in \(W\).
**Stopped path comparison**
From the nominal exponential-moment estimate (15), the probability of leaving the region before \(T\) satisfies
\[ p_0 \le M_fTe^2(2c+1) \exp\!\left[-\frac{B^\sharp-J}{2c}\right]. \tag{32} \]
Stop the full **labelled reaction history** at this exit. Before stopping, its total intensity is at most \(A\). If
\[ r_e=\widetilde k_e/k_e,\qquad |r_e-1|\le\delta, \]
the path likelihood \(L_T\) satisfies
\[ \mathbb E_0 L_T^2\le e^{\delta^2AT}. \tag{33} \]
Consequently,
\[ \operatorname{TV}(\text{stopped perturbed path}, \text{stopped nominal path}) \le \frac12\sqrt{e^{\delta^2AT}-1}, \tag{34} \]
and
\[ p_{\sim} \le e^{\delta^2AT/2}\sqrt{p_0}. \tag{35} \]
Null and parallel firings are included in this likelihood calculation as separate marked events.
**Rare exits do not spoil absolute moments**
Under admitted errors, every physical constant is at most \(3/2\). For the total **fine** count,
\[ \widetilde{\mathcal L}(|u|_1+1)^2 \le12M_f(|u|_1+1)^2. \]
At the exit, the fine count is at most \(B^\sharp+J\). Thus
\[ \begin{aligned} &\mathbb E_{\sim}\!\left[ (1+N(Z_t))^2\mathbf1_{\{\tau_{B^\sharp}\le t\}} \right]\\ &\qquad\le d_*^2(B^\sharp+J+1)^2e^{12M_fT}p_{\sim}. \end{aligned} \tag{36} \]
The cutoff above was chosen so that the exponential tail in (32)–(35) dominates this post-exit growth. In particular, the right-hand side can be bounded by \(\epsilon/128\), uniformly for \(t\le T\).
Combining the stopped comparison and these exit contributions gives perturbed-versus-nominal terminal TV and absolute first-moment differences within the remaining accuracy budget. Therefore the actual perturbed process satisfies the two requested **transient** accuracy inequalities.
It also satisfies
\[ \sup_{t\le T}\mathbb E_{\sim}|Z(t)|_1 \le B^\sharp+2 \]
and
\[ \boxed{ \mathbb E_{\sim}[\text{all actual firings through }T] \le \frac32M_fT\bigl[(B^\sharp+1)^2+1\bigr]. } \tag{37} \]
These bounds are uniform over every independent fixed rate choice in the compiled error box.
If \(P=5p+4s_a+32d_*+44\), a deliberately loose common numerical exponent for these finite-horizon costs is \(4P+7\). This is a polynomial numerical statement, with the common clock slowing and every fine firing charged.
**The limitation is exact:** the cutoff and comparison depend on the finite horizon \(T\). They do not give a uniform-in-time tightness bound for the perturbed process.
**6. Why the original weighted estimate cannot simply be transferred**
There is a legal prefix lift for which the original catalytic chain has strong activity-weighted coercivity, but the fine nominal chain has **zero ordinary spectral gap for every positive \(K,\theta\)**.
Take the original weakly reversible structure
\[ B\rightleftarrows A+B, \qquad 3A+B+C\rightleftarrows4A+B+C. \]
Add the allowed catalyst \(w=A\) to the first pair, giving
\[ A+B\rightleftarrows2A+B. \]
Set original activities and table rates equal to one.
On the actual class
\[ B=1,\qquad C=0, \]
the \(C\)-containing reactions are disabled. The original \(A\)-population is the birth–death chain
\[ b_n=1+n,\qquad d_n=n^2, \]
with
\[ \pi_n=e^{-1}/n!, \qquad a_n=1+n+n^2. \]
It has, for example, the explicit weighted inequality
\[ \sum_n\pi_na_n(h_n-\pi h)^2 \le3240\sum_{n\ge1}\pi_nn^2(h_n-h_{n-1})^2. \tag{38} \]
One elementary proof uses geometrically weighted Cauchy–Schwarz on \(h_n-h_0\), followed by
\[ \sum_{r\ge0}\frac{2^r(r+2)^2}{r!}=18e^2. \]
Now choose prefixes
\[ DP_j=jA+B,\quad j=1,\ldots,4, \]
and full representatives
\[ DQ_3=3A+B+C,\qquad DQ_4=4A+B+C. \]
Use the following binding/release pairs:
**Pair
Forward constant
Reverse constant**
\(B+A\rightleftarrows P_1\)
\(K\theta\)
\(K\)
\(P_j+A\rightleftarrows P_{j+1}\), \(j=1,2,3\)
\(K\)
\(K\)
\(P_3+C\rightleftarrows Q_3\)
\(K\)
\(K\)
\(P_4+C\rightleftarrows Q_4\)
\(K\)
\(K\)
The conversions are
\[ B\rightleftarrows P_1 \quad\text{with constants }1,1/\theta, \]\[ P_1\rightleftarrows P_2, \qquad Q_3\rightleftarrows Q_4 \quad\text{with constants }1/\theta,1/\theta. \]
This network is elementary and detailed balanced. A common normalization makes all constants at most one.
On the class \(C=0\), \(Q_3,Q_4\) are absent. However, their prefixes \(P_3,P_4\) can still sequester the conserved \(B\).
The fine stationary law consists of:
	•	an independent free count \(X=A\sim\operatorname{Pois}(1)\);
	•	one \(B\)-containing marker \(J\in\{0,1,2,3,4\}\), with weights\[ (1,\theta,\theta,\theta,\theta). \]
The decoded \(A\)-count is \(N=X+J\). Put
\[ q_n=1+\theta\sum_{j=1}^4(n)_j. \]
Then
\[ \mu(N=n)= \frac{e^{-1}q_n}{(1+4\theta)n!}. \]
Decoded downward jumps occur only through \(P_1\to B\) and \(P_2\to P_1\). Their conditional total intensity is exactly
\[ \overline d_n=\frac{n^2}{q_n} \sim\frac1{\theta n^2}. \tag{39} \]
For \(f_\ell=\mathbf1_{\{N\ge\ell\}}\), detailed balance gives
\[ \widehat{\mathcal E}(f_\ell) = \mu(N=\ell)\frac{\ell^2}{q_\ell}. \]
For sufficiently large \(\ell\),
\[ \operatorname{Var}_\mu(f_\ell) \ge\frac12\mu(N=\ell). \]
Therefore
\[ \frac{\widehat{\mathcal E}(f_\ell)} {\operatorname{Var}_\mu(f_\ell)} \le\frac{2\ell^2}{q_\ell}\longrightarrow0. \tag{40} \]
So the fine spectral gap is zero. Its total firing intensity is bounded below by a positive constant on this class, so an all-firing weighted Poincaré inequality would also imply a positive ordinary gap and is impossible here.
This example establishes a failure of automatic transfer. It does **not** obstruct all designs:
	•	another prefix order may avoid this sequestration;
	•	additional active conversions may remove it;
	•	the contract asks for accuracy from \(j(x_0)\), not a global \(L^2\) gap;
	•	the bounded-region argument above can still supply the required nominal finite-time accuracy.
**7. The remaining stationary perturbation problem**
There is an exact simplification of the rate-error problem, but I do not have the final theorem it would need.
Because every prefix has a unique defining binding step, binding/release errors can be absorbed into adjusted prefix activities. Keep original activities at \(\lambda\), and define recursively
\[ c'_P= \frac{\widetilde k_{\rm bind}} {\widetilde k_{\rm release}} c'_{\rm parent}\lambda_i. \]
For a first binding, use the corresponding two original activities.
Every actual binding/release pair is then exactly detailed balanced. With
\[ \rho=\frac{1+\delta}{1-\delta}, \]
the adjusted activities obey
\[ \rho^{-(d_*-1)} \le \frac{c'_P}{\theta\lambda^{DP}} \le \rho^{d_*-1}. \tag{41} \]
Adjust only the reference conversion constants to preserve the original complex fluxes. This produces an exactly complex-balanced **reference** process sharing all actual binding constants. The actual process differs from that reference only in the unary or zero-source conversion constants, by relative \(O_R(\delta)\).
Thus the unresolved operation can be stated more narrowly:
Prove a quantitative infinite-class stationary perturbation theorem for these prefix reference processes under small independent errors in their conversion constants, with polynomial stationary moment bounds and polynomial sensitivity.
A suitable conversion-activity weighted coercivity theorem, a uniform Lyapunov argument, or another elementary architecture could potentially supply it. The bounded-fibre proof above cannot simply be extended to infinity: for fixed \(\theta>0\), the condition \(\theta(B+1)^{d_*}\ll1\) eventually fails, and the canonical point can have extremely small conditional fibre probability.
The cited fast-reaction literature does not fill this step. Hoessly–Wiuf’s Theorem 4.1 assumes a finite closed state set and supplies compact-time approximation; their recurrence-transfer theorem imposes sub-conservativity, and their Section 5.3 explicitly distinguishes transient approximation from recurrence transfer. <u>[aimspress.com](aimspress.com/aimspress-data/mbe/2022/3/PDF/mbe-19-03-124.pdf?utm_source=chatgpt.com)</u> The later Hoessly–Wiuf–Xia stationary-reduction result addresses infinite-state issues under a complex-balanced distribution, but that assumption does not supply the independent-rate-error recurrence theorem required here. <u>[Cambridge Core](cambridge.org/core/journals/advances-in-applied-probability/article/asymptotic-analysis-for-stationary-distributions-of-multiscaled-reaction-networks/7551C68BD723A93B1D707B7A0F4226D2?utm_source=chatgpt.com)</u>
**Accordingly, the full universal robust statement remains unresolved in this answer.** The nominal infinite-class compiler and the robust finite-horizon requirements have quantitative constructions. The missing part is the stationary behavior of every process in one fixed nonzero rate-error box. Neither finite-time closeness nor the failure of one lift’s global gap decides that part.

## Native prefix (reader truncated at 20,000 characters)

**I have not resolved the entire universal statement.** I can establish a substantial partial result: using your accepted higher-molecularity compiler, the elementary prefix construction can meet the **full nominal contract on infinite classes**, and it can also meet the **robust finite-time accuracy and physical-cost requirements** with a polynomial numerical rate tolerance.

What I cannot establish is that **every admitted independently perturbed process is positive recurrent and has the required stationary law, stationary first moments, and stationary population bound**. I also do not have an obstruction covering every allowed elementary design. Consequently, this is neither a complete affirmative answer nor a complete negative answer.

The distinction matters here:

| Requirement | What the analysis establishes |
|---|---|
| Fixed finite elementary network and fixed linear decoder | Established |
| Exact decoded communicating classes and permitted decoded moves | Established |
| Nonexplosion under all admitted errors | Established |
| Nominal positive recurrence and unique stationary law | Established |
| Nominal stationary TV and absolute first-moment accuracy | Established with polynomial parameters, including infinite classes |
| Nominal transient accuracy and all physical costs | Established with polynomial parameters |
| Perturbed transient TV and absolute first-moment accuracy at one compiled time | Established uniformly over a polynomial numerical error box |
| Perturbed population and total firing costs through that time | Established uniformly |
| Perturbed positive recurrence and stationary requirements | **Not established** |

Below are the quantitative arguments, followed by a concrete counterexample to automatic spectral-gap inheritance. That counterexample identifies a failed proof route; it does not disprove your universal statement.

## 1. Fixed elementary construction and exact graph preservation

Write the accepted catalytic table as
\[
Y_r=y_r+w_r\longrightarrow Z_r=z_r+w_r,
\qquad r=1,\ldots,m.
\]
Its nominal constants are denoted by \(\kappa_r\), with
\[
0<\kappa_r\le1.
\]

Run the accepted compiler at accuracy \(\epsilon/16\). Absorb that fixed change of accuracy into its fixed computable constants, so that its nominal mixing time \(T_0\) and rate reciprocals satisfy
\[
T_0,\ \max_r\kappa_r^{-1}\le C W^p,
\]
where \(C,p\) depend only on \(R\). Its nominal law at \(T_0\) has TV and absolute coordinate-mean errors at most \(\epsilon/16\).

Set
\[
d_*=\max\!\left(1,\max_r|Y_r|_1,\max_r|Z_r|_1\right).
\]

Use the prefix construction in your premises, ordering each complex canonically and sharing identical ordered prefixes. In particular, every auxiliary prefix has a **unique defining parent**.

Let the auxiliary encoding vectors be
\[
c_1,\ldots,c_{s_a},\qquad 2\le |c_j|_1\le d_*,
\]
and let \(E\) have these columns. The decoder is
\[
D(n,a)=n+Ea.
\]
Thus
\[
|(n,a)|_1\le |D(n,a)|_1. \tag{1}
\]

Give prefix \(j\) activity \(\theta\lambda^{c_j}\). Before a common rate normalization, use:

- first binding/release constants \(K\theta,K\);
- later binding/release constants \(K,K\);
- representative-conversion constant \(\kappa_r/\theta\) when \(|Y_r|_1\ge2\), and \(\kappa_r\) otherwise.

Every reaction has at most two molecules on each side.

Every binding or release has decoded change zero. An enabled representative conversion contains the full encoded source \(Y_r\), so its decoded state contains \(y_r\), and its decoded change is \(z_r-y_r\). Hence it realizes an enabled original edge.

Moreover, every fine state releases to the canonical encoding of its decoder value. Reversing that release path reconstructs the fine state. Since the table includes \(w=0\), every original edge lifts between its canonical encodings. Consequently,
\[
\boxed{\widehat\Gamma=\{(n,a):n+Ea\in\Gamma\}.} \tag{2}
\]

This is an equality involving the **actual communicating class**, with no replacement by a lattice or compatibility set.

### Nonexplosion is automatic for elementary networks of this kind

There is a useful fact that applies more generally than this construction:

> Every finite mass-action network with at most two molecules on each side of every reaction is nonexplosive for every finite positive rate vector.

Let \(V(u)=1+|u|_1\). A reaction increasing \(|u|_1\) must have zero or one reactant. Therefore
\[
\mathcal LV(u)\le C_0+C_1|u|_1.
\]
Stopping and Grönwall’s inequality prevent the population from becoming unbounded in finite time. On a bounded-population set, there are finitely many states and a bounded total firing intensity, including null and parallel channels. Thus infinitely many actual firings cannot accumulate there either.

This proves nonexplosion under the whole admitted error box. It does **not** establish positive recurrence.

## 2. Polynomial stationary approximation on infinite classes

The nominal lift is complex balanced. Its product-form measure is therefore available on each closed irreducible class; this is the standard complex-balance product-form theorem. :chatgpt-content-reference{index="0"}

Write
\[
w(x)=\frac{\lambda^x}{x!},
\qquad
q_\theta(x)=
\sum_{a:Ea\le x}
\frac{\theta^{|a|}(x)_{Ea}}{a!}.
\]
The decoded stationary law is exactly
\[
\rho_\theta(x)
=
\frac{\pi_\lambda(x)q_\theta(x)}
     {\mathbb E_{\pi_\lambda}q_\theta(X)}. \tag{3}
\]

The infinite-class estimate can be made quantitative without a class oracle. The key is to use the exact generating function
\[
\boxed{
\sum_{x\in\mathbb N^d}
w(x)q_\theta(x)e^{t|x|_1}
=
\exp\!\left(
e^t\sum_i\lambda_i+
\theta\sum_{j=1}^{s_a}\lambda^{c_j}e^{t|c_j|_1}
\right).
} \tag{4}
\]

Using \(q_\theta(x)\le e^{s_a\theta |x|^{d_*}}\) globally would be inadequate: that upper bound can grow too quickly to integrate against Poisson tails. Equation (4) retains the actual compound-Poisson structure.

### A usable normalization bound comes from \(x_0\)

Because \(x_0\in\Gamma\),
\[
Z_\Gamma\ge w(x_0).
\]
Also,
\[
w(x_0)\ge W^{-2|x_0|_1}, \tag{5}
\]
since \(\lambda_i^{-1}\le W\) and \(x_0!\le W^{|x_0|_1}\).

This does not require a supplied rare-class lower bound. Its logarithmic cost is controlled directly by the input.

Assume
\[
\theta s_aW^{d_*}\le1.
\]
Equations (4)–(5), evaluated at \(t=1/d_*\), give
\[
\mathbb E_{\pi_\lambda}
\left[q_\theta(X)e^{|X|_1/d_*}\right]
\le e^{4W^2}. \tag{6}
\]

Choose, for the static estimate alone,
\[
B_{\rm stat}=16d_*(d_*+1)W^2,
\]
and
\[
\boxed{
\theta\le
\frac{\epsilon}
 {128s_a(B_{\rm stat}+1)^{d_*+1}}.
} \tag{7}
\]
The cases needing no auxiliary prefixes can be handled directly.

For any \(B\ge B_{\rm stat}\), (6) implies
\[
\mathbb E_{\pi_\lambda}\!\left[
q_\theta(X)(|X|_1+1)
\mathbf1_{\{|X|_1>B\}}
\right]
\le
(2d_*+1)e^{4W^2-B/(2d_*)}
\le\frac{\epsilon}{32}. \tag{8}
\]

Inside \(|x|_1\le B\), provided (7) holds with this \(B\),
\[
q_\theta(x)-1
\le \frac{\epsilon}{64(B+1)}. \tag{9}
\]

Let \(r_\theta=\pi_\lambda q_\theta\). Combining the interior estimate and the weighted tail gives
\[
0\le r_\theta-1
\le \frac{3\epsilon}{64(B+1)}.
\]
Therefore
\[
\|\rho_\theta-\pi_\lambda\|_{\rm TV}
\le r_\theta-1<\frac{\epsilon}{8}. \tag{10}
\]

For each coordinate,
\[
\begin{aligned}
|\rho_\theta X_i-\pi_\lambda X_i|
&\le
\pi_\lambda\!\left[|X|_1(q_\theta-1)\right]
+(r_\theta-1)\pi_\lambda|X|_1\\
&<\frac{\epsilon}{8}. 
\end{aligned} \tag{11}
\]

Thus **the nominal infinite-class stationary approximation has a polynomial numerical choice of \(\theta\)**.

For example, the reciprocal in (7) is bounded by a fixed-\(R\) constant times \(W^{2d_*+3}\). The cutoff is used only in the proof. No reaction is reflected, killed, disabled, or externally reset at that population.

## 3. Polynomial nominal moments uniformly over all time

The nominal transient population bound can also be made polynomial without first proving a spectral gap.

Let \(\mu\) be the nominal fine stationary measure and
\[
N(u)=|Du|_1,\qquad H=4W^2,\qquad q=\lceil H\rceil,
\qquad r=\frac{q}{q-1}.
\]
The same generating-function estimates give
\[
\mu(e^{N/d_*})\le e^H,
\qquad
\mu(j(x_0))\ge e^{-H}. \tag{12}
\]

Let \(f_t\) be the density, relative to \(\mu\), of the nominal process started at \(j(x_0)\). The adjoint Markov semigroup contracts \(L^r(\mu)\), so
\[
\|f_t\|_{L^r(\mu)}
\le
\mu(j(x_0))^{-1/q}\le e. \tag{13}
\]

The choice \(r\) close to one is useful: an \(L^2\) estimate would retain an exponentially large initialization factor.

For every fixed integer \(h\ge1\),
\[
N^{hq}\le d_*^{hq}(hq)!\,e^{N/d_*}.
\]
Hölder’s inequality and (12)–(13) therefore yield
\[
\boxed{
\sup_{t\ge0}
\mathbb E_{j(x_0)}N(Z_t)^h
\le
9(5d_*h)^hW^{2h}.
} \tag{14}
\]

The stationary moments satisfy corresponding bounds. Equation (1) makes these bounds apply to every auxiliary population as well.

A further consequence, used below, is
\[
\boxed{
\sup_{t\ge0}
\mathbb E_{j(x_0)}
e^{N(Z_t)/(d_*q)}
\le e^2.
} \tag{15}
\]

After all physical rate constants are normalized to at most one, the total labelled firing intensity satisfies
\[
a_{\rm fine}(u)\le M_f(1+N(u))^2,
\]
where \(M_f\) is the fixed number of fine channels. Thus
\[
\mathbb E[\text{all actual firings through }T]
\le C_R T W^4 \tag{16}
\]
in the nominal case.

This counts binding, release, null, and parallel firings. The estimate holds for every supplied finite \(T\); a polynomial mixing time still needs a separate argument.

## 4. Nominal polynomial mixing without a global fine-chain spectral gap

That argument can be supplied using averaging on a bounded region **only as an analytical device**.

### Fast mixing inside a bounded decoded fibre

Fix \(x\) with \(|x|_1\le B\). Remove the common factor \(K\) from the binding generator and denote the resulting fibre generator by \(F_x\). Its invariant distribution is
\[
\nu_x(a)
=
\frac{\theta^{|a|}(x)_{Ea}}
     {a!\,q_\theta(x)}. \tag{17}
\]

Suppose
\[
\theta(B+1)^{d_*}\le\frac12,
\qquad
s_a\theta B^{d_*}\le1.
\]

Releasing one whole prefix of encoding \(c\) changes its stationary weight by the factor
\[
\frac{a_c}{\theta}\frac{n!}{(n+c)!}
\ge
\frac{1}{\theta(B+1)^{d_*}}
\ge2. \tag{18}
\]

During its at most \(d_*\) partial releases, the weight loses at most a factor \((B+1)^{2d_*}\). Releasing all prefixes takes at most \(d_*B\) steps. There are at most \((B+1)^{s_a}\) states in the fibre, and every used release transition has rate at least one.

An anchored path inequality consequently gives
\[
\operatorname{Var}_{\nu_x}h
\le
d_*B(B+1)^{s_a+2d_*}
\mathcal E_{F_x}(h,h). \tag{19}
\]

For the initialization cost,
\[
\nu_x(a)\ge e^{-1}(\theta/B)^B.
\]
Only its logarithm is needed. Integrating the finite reversible mixing estimate gives the following safe sup-norm corrector bound:
\[
\left\|F_x^{-1}(I-\Pi_x)\right\|_{\infty\to\infty}
\le C_F,
\]
where one may take
\[
\boxed{
C_F=
8d_*(B+1)^{s_a+2d_*+4}\theta^{-1}.
} \tag{20}
\]

### The averaged rates are explicit

For a representative source of order at least two,
\[
\mathbb E_{\nu_x}a_{Y_r}
=
\theta(x)_{Y_r}
\frac{q_\theta(x-Y_r)}{q_\theta(x)}.
\]
The corresponding identity for an original-species source is obtained by replacing the auxiliary count with its free-species count.

Hence the exact averaged decoded rate is
\[
\boxed{
\overline q_r(x)=
\kappa_r(x)_{Y_r}
\frac{q_\theta(x-Y_r)}{q_\theta(x)}.
} \tag{21}
\]

On \(|x|_1\le B\), its generator differs from the original catalytic generator by at most
\[
4s_am\theta(B+1)^{2d_*} \tag{22}
\]
in the bounded-function operator norm.

For the comparison, send either process to a cemetery state when its decoded population first leaves \(N\le B\). This defines finite stopped processes for the proof; it is not the implemented network.

Write their fine generator as
\[
KF+S,
\]
where \(S\) contains representative conversions. Its total conversion intensity in this region is bounded by
\[
M_0=m\theta^{-1}(B+1). \tag{23}
\]

Solving the fibre Poisson equation and applying Dynkin’s formula gives, for a decoded test function bounded by one,
\[
\left|
\mathbb E g(DZ_T^{B})
-\mathbb E g(\overline X_T^{B})
\right|
\le
\frac{8C_F(M_0+2TM_0^2)}{K}. \tag{24}
\]
The endpoint corrector terms include the initial canonical state, so fibre-equilibrated initialization is unnecessary. A coordinate-mean test costs only an additional factor \(B\).

### Polynomial parameter choices and removal of stopping

Choose
\[
B=\lceil C_BW^4\rceil,
\qquad
\theta=
\frac{\epsilon}
 {128s_am(T_0+1)(B+1)^{2d_*+1}}, \tag{25}
\]
and
\[
\boxed{
K=
1+
\frac{1024C_F(B+1)(M_0+2T_0M_0^2)}{\epsilon}.
} \tag{26}
\]

Here \(C_B\) is a sufficiently large **computable fixed-\(R\) constant**. It can be chosen explicitly from the supplied \(C,p\), the finite table, and the moment constants in (14).

For clarity, there is no circular dependence hidden in the exit estimate. Take the fixed moment order
\[
h=p+4d_*+16.
\]
Only conversions can change \(N\), and their raw intensity is at most \(m\theta^{-1}(N+1)\). Therefore
\[
\begin{aligned}
\mathbb P(\tau_B^{\rm fine}\le T_0)
&\le
C_R T_0\theta^{-1}B^{-(h-1)}W^{2h}\\
&\le C_R C_B^{2d_*+2-h}W^{-23}. 
\end{aligned} \tag{27}
\]
The original catalytic process has a corresponding, smaller exit bound.

Because \(h>2d_*+2\), increasing \(C_B\) decreases the bound despite the resulting decrease in \(\theta\). The endpoint first-moment contribution of an exited path is bounded by
\[
\mathbb E[N(Z_{T_0})\mathbf1_{\{\tau_B\le T_0\}}]
\le
\bigl(\mathbb EN(Z_{T_0})^2\bigr)^{1/2}
\mathbb P(\tau_B\le T_0)^{1/2}. \tag{28}
\]
Equations (14) and (27) make this contribution smaller than the allocated accuracy budget.

Combining (22), (24), the two stopping errors, and the accepted original accuracy proves nominal transient TV and absolute first-moment errors below \(\epsilon/8\), after fixed enlargement of the constants.

### Physical normalization and complexity

Equation (26) ensures \(K\ge\theta^{-1}\). Divide every raw rate constant by \(K\), and use physical time
\[
\boxed{T=KT_0.} \tag{29}
\]
Every resulting nominal constant is at most one.

All rate reciprocals, \(K\), \(T\), and the total actual firing count are polynomial in \(W\). For example, loose exponents from these formulas are
\[
\theta^{-1}=O_R(W^{p+8d_*+5}),
\]
\[
T,\ \max_e k_e^{-1}
=
O_R(W^{5p+4s_a+32d_*+44}),
\]
and
\[
\mathbb E[\text{all nominal firings through }T]
=
O_R(W^{5p+4s_a+32d_*+48}). \tag{30}
\]

The compiler evaluates fixed-degree rational expressions. It does **not** enumerate the ball, the fibres, the communicating class, or the stopped generator. Thus the numerical population cutoff used in the proof does not become a numerical-population loop in the binary compiler.

This closes the nominal infinite-class contract under your accepted premise.

## 5. Polynomial robustness through the compiled finite time

The transient requirements can be made robust without assuming that the perturbed chain has a stationary distribution.

Here is a direct argument that includes errors in **every** physical channel.

Use the normalized physical process and write
\[
c=d_*q.
\]
Let \(J\) bound the positive change in decoded total population at one reaction; \(J\le2d_*\) is sufficient. Define a second analytical cutoff
\[
B^\sharp
=
J+
\left\lceil
128(M_f+d_*+J+2)c(T+W^2+1)
\right\rceil,
\]
and
\[
A=M_f(B^\sharp+1)^2.
\]
Choose
\[
\boxed{
\delta=
\min\left\{
\frac12,\,
\frac{\epsilon}
 {64d_*(B^\sharp+J+1)(A+1)(T+1)}
\right\}.
} \tag{31}
\]

Both \(B^\sharp\) and \(\delta^{-1}\) are polynomial in \(W\).

### Stopped path comparison

From the nominal exponential-moment estimate (15), the probability of leaving the region before \(T\) satisfies
\[
p_0
\le
M_fTe^2(2c+1)
\exp\!\left[-\frac{B^\sharp-J}{2c}\right]. \tag{32}
\]

Stop the full **labelled reaction history** at this exit. Before stopping, its total intensity is at most \(A\). If
\[
r_e=\widetilde k_e/k_e,\qquad |r_e-1|\le\delta,
\]
the path likelihood \(L_T\) satisfies
\[
\mathbb E_0 L_T^2\le e^{\delta^2AT}. \tag{33}
\]

Consequently,
\[
\operatorname{TV}(\text{stopped perturbed path},
                  \text{stopped nominal path})
\le
\frac12\sqrt{e^{\delta^2AT}-1}, \tag{34}
\]
and
\[
p_{\sim}
\le
e^{\delta^2AT/2}\sqrt{p_0}. \tag{35}
\]

Null and parallel firings are included in this likelihood calculation as separate marked events.

### Rare exits do not spoil absolute moments

Under admitted errors, every physical constant is at most \(3/2\). For the total **fine** count,
\[
\widetilde{\mathcal L}(|u|_1+1)^2
\le12M_f(|u|_1+1)^2.
\]
At the exit, the fine count is at most \(B^\sharp+J\). Thus
\[
\begin{aligned}
&\mathbb E_{\sim}\!\left[
(1+N(Z_t))^2\mathbf1_{\{\tau_{B^\sharp}\le t\}}
\right]\\
&\qquad\le
d_*^2(B^\sharp+J+1)^2e^{12M_fT}p_{\sim}.
\end{aligned} \tag{36}
\]

The cutoff above was chosen so that the exponential tail in (32)–(35) dominates this post-exit growth. In particular, the right-hand side can be bounded by \(\epsilon/128\), uniformly for \(t\le T\).

Combining the stopped comparison and these exit contributions gives perturbed-versus-nominal terminal TV and absolute first-moment differences within the remaining accuracy budget. Therefore the actual perturbed process satisfies the two requested **transient** accuracy inequalities.

It also satisfies
\[
\sup_{t\le T}\mathbb E_{\sim}|Z(t)|_1
\le B^\sharp+2
\]
and
\[
\boxed{
\mathbb E_{\sim}[\text{all actual firings through }T]
\le
\frac32M_fT\bigl[(B^\sharp+1)^2+1\bigr].
} \tag{37}
\]

These bounds are uniform over every independent fixed rate choice in the compiled error box.

If \(P=5p+4s_a+32d_*+44\), a deliberately loose common numerical exponent for these finite-horizon costs is \(4P+7\). This is a polynomial numerical statement, with the common clock slowing and every fine firing charged.

**The limitation is exact:** the cutoff and comparison depend on the finite horizon \(T\). They do not give a uniform-in-time tightness bound for the perturbed process.

## 6. Why the original weighted estimate cannot simply be transferred

There is a legal prefix lift for which the original catalytic chain has strong activity-weighted coercivity, but the fine nominal chain has **zero ordinary spectral gap for every positive \(K,\theta\)**.

Take the original weakly reversible structure
\[
B\rightleftarrows A+B,
\qquad
3A+B+C\rightleftarrows4A+B+C.
\]
Add the allowed catalyst \(w=A\) to the first pair, giving
\[
A+B\rightleftarrows2A+B.
\]
Set original activities and table rates equal to one.

On the actual class
\[
B=1,\qquad C=0,
\]
the \(C\)-containing reactions are disabled. The original \(A\)-population is the birth–death chain
\[
b_n=1+n,\qquad d_n=n^2,
\]
with
\[
\pi_n=e^{-1}/n!,
\qquad
a_n=1+n+n^2.
\]
It has, for example, the explicit weighted inequality
\[
\sum_n\pi_na_n(h_n-\pi h)^2
\le3240\sum_{n\ge1}\pi_nn^2(h_n-h_{n-1})^2. \tag{38}
\]
One elementary proof uses geometrically weighted Cauchy–Schwarz on \(h_n-h_0\), followed by
\[
\sum_{r\ge0}\frac{2^r(r+2)^2}{r!}=18e^2.
\]

Now choose prefixes
\[
DP_j=jA+B,\quad j=1,\ldots,4,
\]
and full representatives
\[
DQ_3=3A+B+C,\qquad DQ_4=4A+B+C.
\]

Use the following binding/release pairs:

| Pair | Forward constant | Reverse constant |
|---|---:|---:|
| \(B+A\rightleftarrows P_1\) | \(K\theta\) | \(K\) |
| \(P_j+A\rightleftarrows P_{j+1}\), \(j=1,2,3\) | \(K\) | \(K\) |
| \(P_3+C\rightleftarrows Q_3\) | \(K\) | \(K\) |
| \(P_4+C\rightleftarrows Q_4\) | \(K\) | \(K\) |

The conversions are
\[
B\rightleftarrows P_1
\quad\text{with constants }1,1/\theta,
\]
\[
P_1\rightleftarrows P_2,
\qquad Q_3\rightleftarrows Q_4
\quad\text{with constants }1/\theta,1/\theta.
\]

This network is elementary and detailed balanced. A common normalization makes all constants at most one.

On the class \(C=0\), \(Q_3,Q_4\) are absent. However, their prefixes \(P_3,P_4\) can still sequester the conserved \(B\).

The fine stationary law consists of:

- an independent free count \(X=A\sim\operatorname{Pois}(1)\);
- one \(B\)-containing marker \(J\in\{0,1,2,3,4\}\), with weights
  \[

## Expanded visible activity (accessibility)

41 button (expanded) Worked for 41m 20s, Secondary Actions: Collapse
									42 text Worked for 41m 20s
									43 image
								2357 text I’ll pursue the full infinite-class statement, using the higher-molecularity compiler as an accepted premise. I’ll split the work across elementary constructions, possible obstructions, and recurrence and perturbation estimates, then check whether the pieces meet every part of the resource contract.
								2358 container Subagent activity
									2359 container
										2360 button Elementary construction
										2361 text , 
										2362 button Obstructions
										2363 text  and 
										2364 button Lift analysis
										2365 text  started working
								2366 text I’m using the cloud runtime skill for the computational checks. Mathematically, the first pressure point is whether a fixed binary construction can retain control of the tails under independent rate errors; nominal complex balance alone does not establish that.
								2367 text Searched 26 websites
								2368 text Checked partition-ratio bounds and conditional tails
								2369 container Subagent activity
									2370 container
										2371 button Lift analysis
										2372 text  updated
								2373 text Tested weighted inequality transfer, Poincare obstruction, and reservoir-catalyzed splitting
								2374 text Estimated Q0 scaling, bounded count growth, and checked recurrence conditions
								2375 text Checked species closure, encoder drift, and weighted gap transfer
								2376 text Designed CRN scheduler and analyzed token control
								2377 text Compared conditional mixtures with cyclic balance and catalyst accelerations
								2378 text Tested prefix boundaries and weighted path tail bounds
								2379 text Analyzed weighted Poincaré bounds, fiber gaps, and gap loss
								2380 text Developed cycle-based bounds and tested deficiency-zero embeddings
								2381 text Tested source-specific species and checked tagged embeddings and lifted deficiency
								2382 text There is a useful opening on infinite classes: the nominal binary lift’s stationary law and absolute first moments appear to admit a polynomial accuracy bound. The estimate uses a cutoff only in the proof; the physical process remains unbounded. The harder step is still to control recurrence and convergence uniformly after the elementary reaction rates are perturbed.
								2383 container Subagent activity
									2384 container
										2385 button Elementary construction
										2386 text , 
										2387 button Obstructions
										2388 text  and 
										2389 button Lift analysis
										2390 text  updated
								2391 text Searched 17 websites
								2392 text Explored linkage augmentation, translated cycle joins, and silent join tests
								2393 text Compared linkage classes and tested path-based double-full construction
								2394 text Checked class bounds and designed chunk-state encoding
								2395 text Refined two-slot encoding and checked pump theorem stationary-law factors
								2396 text Designed control-token setup, leader bounds, and release scheme
								2397 text Checked controller balance and designed effective reaction rates
								2398 text Designed rate scaling, draw slots, and token overlap bounds
								2399 text Checked overlap, rate, and timechange centering bounds
								2400 text Checked weighted inequality
								2401 container Subagent activity
									2402 container
										2403 button Elementary construction
										2404 text  updated
								2405 text Formalized rare-token birth and equalized stage denominators
								2406 text Designed dummy padding and stage rates
								2407 text Checked adjusted rates and bounded token lifetimes
								2408 text Bounded transient costs, trace conductances, and overlap contributions
								2409 text Bounded first-commit intensity, stationary flows, and cluster tails
								2410 text Defined reference measure, bounded path flux, and tested product-form stationarity
								2411 text Tested product form, balanced token routes, and refined sequestration reset
								2412 text Designed leader collision rules and checked exact leader election
								2413 text Two parts can now be separated cleanly. Any finite network with at most two molecules on each side is nonexplosive, because a reaction that increases the total molecule count has at most one reactant. I also have an explicit polynomial choice of the prefix parameter for nominal stationary TV and absolute moment accuracy. Neither result yet proves uniform recurrence or mixing under rate errors; I’m testing an autonomous processing-token construction for that remaining step. Audited balance calculation, weighted Poincare control, and binding-tree consistency Analyzed conversion network errors, weighted PI, and tail bottlenecks Assessed catalyst bottlenecks and derived an entropy drift model Checked V at infinity
								2414 container Subagent activity
									2415 container
										2416 button Obstructions
										2417 text  and 
										2418 button Lift analysis
										2419 text  updated
								2420 text Searching 2 websites
								2421 text Audited Lp contraction and derived perturbed moment bounds Established transient accuracy by bounding cutoff and perturbed exit tails Assessed perturbed moments, built cutoff model, and bounded fiber lifetimes Derived symbolic compiler bounds
								2422 container Subagent activity
									2423 container
										2424 button Lift analysis
										2425 text  updated
								2426 text Checked derived lemmas and balance conditions Selected theta scaling, constructed cycle-based rates, and checked macro subnetwork Tested prefix variants and a Lyapunov inequality Checked drift domination
								2427 text Searched 9 websites
								2428 text Audited theorem constants and bounded lifted mgf
								2429 text Bounded the expectation shift
								2430 text Checked error bounds and rational bit complexity
								2431 text Bounded stationary moments and firing propensities
								2432 text A further estimate now gives polynomial bounds on every fixed population moment of the nominal lift, uniformly over all time from the canonical initial state. That also bounds every physical firing over any polynomial time horizon. I also found a concrete reason the supplied robustness estimate cannot simply be copied to the lift: an elementary network can have many binding and release events while those events leave the decoded state unchanged. The total-activity weighted inequality can then fail. This limits that proof route; it does not disprove the universal statement. Checked R’s graph and derived the reduced product law Checked original table weights and verified the Poisson shift Verified the weighted bound
								2433 container Subagent activity
									2434 container
										2435 button Lift analysis
										2436 text , 
										2437 button Obstructions
										2438 text  and 
										2439 button Elementary construction
										2440 text  updated
								2441 text Searched 13 websites
								2442 container Subagent activity
									2443 container
										2444 button Obstructions
										2445 text  and 
										2446 button Elementary construction
										2447 text  finished
								2448 text Checked averaging bounds and corrector estimates
								2449 text Verified fiber path bounds and derived an anchored path inequality
								2450 text Checked the mixing bound
								2451 text Bounded fine-grid exit errors and fixed moment order
								2452 text Checked exit-probability bounds and normalized physical rates
								2453 text Polished nominal theorem proof and derived uniform exit bounds
								2454 text Bounded exit via B2 and subsequent moments
								2455 text Bounded perturbed exit probability and finite-time TV error
								2456 container Subagent activity
									2457 container
										2458 button Elementary construction
										2459 text  and 
										2460 button Lift analysis
										2461 text  updated
								2462 text Defined bounded reference dynamics and checked likelihood moments
								2463 text Checked the second-moment and refined the mgf bounds
								2464 text Formalized finite-horizon lemma and defined shared prefix labels
								2465 text Checked canonical prefix ordering and bounded binding-weight ratios
								2466 text Derived explicit construction constants
								2467 text The remaining gap is narrower now. The estimates support polynomial convergence at the compiled time, including a polynomial tolerance for rate errors over that finite horizon. What I still cannot justify is positive recurrence and stationary accuracy for every rate vector in the same error box. Finite-time closeness does not establish either property. I also checked an example where a nominal prefix lift has zero global spectral gap. That rules out a blanket gap-transfer argument, although it does not rule out polynomial-time accuracy from the specified canonical start. Verified Girsanov error bounds
								2468 container Subagent activity
									2469 container
										2470 button Elementary construction
										2471 text  finished
								2472 text Refined the proof structure Handled trivial cases and prepared nominal averaging formulas Checked stationary requirements Clarified bound constants Verified the gap counterexample and checked the ordering choice Derived finite-horizon cost bounds The checks support a substantial partial result: an untruncated elementary construction can meet the full nominal contract and the robust finite-time requirements, with all auxiliary populations and firings charged. The unresolved requirements are positive recurrence, stationary law and moment accuracy, and the stationary population bound under arbitrary admitted rate errors. I’ll state that limit explicitly alongside the estimates and the counterexample to automatic gap transfer. Assembled fine-graph proof Set nominal mixing constants Defined explicit fibre constants Established transient error bounds and clarified prefix-counter scope Set up the product form
								44 

## Visible subagent panel: SUBAGENT

container Description: Subagents, ID: app-shell-tab-panel-app-shell-tab:1
									4805 container
										4806 button Back to subagents
											4807 image
										4820 text Elementary construction
									4821 container
										4822 heading Status, Value: 2
											4823 text Status
										4824 text Done
										4825 heading Final response, Value: 2
											4826 text Final response
										4827 container
											4828 text The finite-horizon perturbation argument is valid. It closes robust transient TV and absolute first-moment accuracy, together with polynomial transient fine-population and total-firing bounds,  provided the nominal polynomial mixing time and nominal uniform exponential-moment estimate are already proved . It does not establish perturbed recurrence or stationary accuracy.
										4829 text Here is an explicit version with constants.
										4830 heading Assumptions and notation, Value: 2
											4831 text Assumptions and notation
										4832 text Let the normalized elementary prefix lift have:
										4833 content list
											4834 container
												4835 AXListMarker • 
												4836 container
													4837 text 𝐾 ≥ 1
												4838 text  labelled physical channels, counting null and parallel channels separately;
											4839 container
												4840 AXListMarker • 
												4841 text nominal constants 
												4842 container
													4843 text 𝑘
													4844 text 𝑒
													4845 text ≤ 1
												4846 text ;
											4847 container
												4848 AXListMarker • 
												4849 text decoder maximum column sum 
												4850 container
													4851 text 𝐷 ≥ 1
												4852 text ;
											4853 container
												4854 AXListMarker • 
												4855 text maximal positive decoded-total jump 
												4856 container
													4857 text 𝐽 ≥ 0
												4858 text ;
											4859 container
												4860 AXListMarker • 
												4861 text no zero-decoded species, so
												4862 container
													4863 text ∣ 𝑍
													4864 text ∣
													4865 text 1
													4866 text ≤ ∣ 𝐷 𝑍
													4867 text ∣
													4868 text 1
													4869 text ≤ 𝐷 ∣ 𝑍
													4870 text ∣
													4871 text 1
													4872 text ;
											4873 container
												4874 AXListMarker • 
												4875 text decoded-changing channels of arity zero or one on the source side.
										4876 text The last property holds for the prefix lift: binding/release has zero decoded change, and macro conversions are zero/unary.
										4877 container
											4878 text Write 
											4879 container
												4880 text 𝑁 ( 𝑡 ) = ∣ 𝐷 𝑍 ( 𝑡 )
												4881 text ∣
												4882 text 1
											4883 text . Assume the nominal chain started from 
											4884 container
												4885 text 𝑗 (
												4886 text 𝑥
												4887 text 0
												4888 text )
											4889 text  satisfies
										4890 container
											4891 container
												4892 text sup ⁡
											4893 container
												4894 text 𝑡 ≥ 0
											4895 text 𝐸
											4896 text 0
											4897 text 𝑒
											4898 container
												4899 text 𝑁 ( 𝑡 ) / 𝑐
											4900 text ≤
											4901 text 𝑒
											4902 text 2
											4903 text , 𝑐 = 𝐷 𝑞 , 𝑞 = ⌈ 4
											4904 text 𝑊
											4905 text 2
											4906 text ⌉ .
										4907 container
											4908 text Let 
											4909 container
												4910 text 𝑇 > 0
											4911 text  be the nominal polynomial mixing time.
										4912 text Define
										4913 container
											4914 text 𝑎 = 𝐾 + 𝐷 + 𝐽 + 2 , 𝑆 = 𝑇 +
											4915 text 𝑊
											4916 text 2
											4917 text + 1 ,
										4918 text and choose the integer cutoff
										4919 container
											4920 text 𝐵 = 𝐽 +
											4921 text ⌈
											4922 text 128
											4923 text 𝑎
											4924 text 𝑐
											4925 text 𝑆
											4926 text ⌉
											4927 text .
										4928 text Let
										4929 container
											4930 text 𝐴 = 𝐾 ( 𝐵 + 1
											4931 text )
											4932 text 2
										4933 text and choose
										4934 container
											4935 text 𝛿 = min ⁡
											4936 text {
											4937 container
												4938 text 1 2
											4939 text ,
											4940 container
												4941 text 𝜖
												4942 text 64
												4943 text 𝐷
												4944 text (
												4945 text 𝐵
												4946 text +
												4947 text 𝐽
												4948 text +
												4949 text 1
												4950 text )
												4951 text (
												4952 text 𝐴
												4953 text +
												4954 text 1
												4955 text )
												4956 text (
												4957 text 𝑇
												4958 text +
												4959 text 1
												4960 text )
											4961 text }
											4962 text .
										4963 container
											4964 text These are rational/integer calculations of polynomial binary complexity. If 
											4965 text 𝑇
											4966 text  is polynomial in 
											4967 text 𝑊
											4968 text , then 
											4969 container
												4970 text 𝐵 ,
												4971 text 𝛿
												4972 container
													4973 text − 1
											4974 text  are polynomial in 
											4975 text 𝑊
											4976 text .
										4977 heading 1. Nominal exit probability, Value: 2
											4978 text 1. Nominal exit probability
										4979 text Let
										4980 container
											4981 text 𝜏
											4982 text 𝐵
											4983 text = inf ⁡ { 𝑡 : 𝑁 ( 𝑡 ) > 𝐵 } .
										4984 container
											4985 text The cutoff exceeds 
											4986 container
												4987 text 𝑁 ( 0 )
											4988 text . Before an exit, a positive decoded jump must occur from 
											4989 container
												4990 text 𝑁 > 𝐵 − 𝐽
											4991 text . Its total intensity is at most 
											4992 container
												4993 text 𝐾 ( 1 + 𝑁 )
											4994 text . Using the jump compensator,
										4995 container
											4996 text 𝑃
											4997 text 0
											4998 text (
											4999 text 𝜏
											5000 text 𝐵
											5001 text ≤ 𝑇 ) ≤ 𝐾
											5002 text ∫
											5003 text 0
											5004 text 𝑇
											5005 text 𝐸
											5006 text 0
											5007 text  ⁣
											5008 text [
											5009 text (
											5010 text 1
											5011 text +
											5012 text 𝑁
											5013 text (
											5014 text 𝑡
											5015 text )
											5016 text )
											5017 container
												5018 text 1
												5019 text {
												5020 text 𝑁
												5021 text (
												5022 text 𝑡
												5023 text )
												5024 text >
												5025 text 𝐵
												5026 text −
												5027 text 𝐽
												5028 text }
											5029 text ]
											5030 text 𝑑 𝑡 .
										5031 container
											5032 text For 
											5033 container
												5034 text 𝑐 ≥ 1
											5035 text ,
										5036 container
											5037 text ( 1 + 𝑛 )
											5038 text 1
											5039 container
												5040 text { 𝑛 > 𝑏 }
											5041 text ≤ ( 2 𝑐 + 1 )
											5042 text 𝑒
											5043 container
												5044 text − 𝑏 / ( 2 𝑐 )
											5045 text 𝑒
											5046 container
												5047 text 𝑛 / 𝑐
											5048 text .
										5049 text Hence
										5050 container
											5051 text 𝑝
											5052 text 0
											5053 text : =
											5054 text 𝑃
											5055 text 0
											5056 text (
											5057 text 𝜏
											5058 text 𝐵
											5059 text ≤ 𝑇 ) ≤ 𝐾 𝑇
											5060 text 𝑒
											5061 text 2
											5062 text ( 2 𝑐 + 1 ) exp ⁡  ⁣
											5063 text [
											5064 text −
											5065 container
												5066 text 𝐵
												5067 text −
												5068 text 𝐽
												5069 text 2
												5070 text 𝑐
											5071 text ]
											5072 text .
										5073 text This charges decoded-changing events only, as appropriate for exits. Binding and release events are still included in the likelihood and activity calculations below.
										5074 heading 2. Stopped marked-path likelihood, Value: 2
											5075 text 2. Stopped marked-path likelihood
										5076 container
											5077 text Stop the full marked reaction process at 
											5078 container
												5079 text 𝜏 𝐵
											5080 text . Under the nominal law, its all-label total intensity is bounded by 
											5081 text 𝐴
											5082 text , including null and parallel firings.
										5083 text For fixed errors
										5084 container
											5085 text 𝑟
											5086 text 𝑒
											5087 text =
											5088 container
												5089 text 𝑘
												5090 text ~
												5091 text 𝑒
											5092 container
												5093 text 𝑘 𝑒
											5094 text , ∣
											5095 text 𝑟
											5096 text 𝑒
											5097 text − 1 ∣ ≤ 𝛿 ,
										5098 text the marked-path likelihood is
										5099 container
											5100 text 𝐿
											5101 text 𝑇
											5102 text =
											5103 text ∏
											5104 container
												5105 text firings before  𝑇 ∧
												5106 text 𝜏
												5107 text 𝐵
											5108 text 𝑟
											5109 text 𝑒
											5110 text exp ⁡  ⁣
											5111 text [
											5112 text −
											5113 container
												5114 text ∑ 𝑒
											5115 text (
											5116 container
												5117 text 𝑟 𝑒
											5118 text −
											5119 text 1
											5120 text )
											5121 container
												5122 text ∫ 0
												5123 text 𝑇
												5124 text ∧
												5125 container
													5126 text 𝜏 𝐵
											5127 container
												5128 text 𝑎 𝑒
											5129 text (
											5130 container
												5131 text 𝑍 𝑠
											5132 text )
											5133 text 𝑑
											5134 text 𝑠
											5135 text ]
											5136 text .
										5137 text The standard bounded-intensity exponential-martingale calculation gives
										5138 container
											5139 text 𝐸
											5140 text 0
											5141 text 𝐿
											5142 text 𝑇
											5143 text 2
											5144 text ≤
											5145 text 𝑒
											5146 container
												5147 text 𝛿
												5148 text 2
												5149 text 𝐴 𝑇
											5150 text .
										5151 text Thus the TV distance between the two stopped marked-path laws is at most
										5152 container
											5153 text 𝑣 ≤
											5154 text 1
											5155 text 2
											5156 container
												5157 text 𝑒
												5158 container
													5159 text 𝛿
													5160 text 2
													5161 text 𝐴 𝑇
												5162 text − 1
											5163 text .
										5164 text Cauchy–Schwarz applied to the stopped exit event gives
										5165 container
											5166 text 𝑝
											5167 text ∼
											5168 text : =
											5169 text 𝑃
											5170 text ∼
											5171 text (
											5172 text 𝜏
											5173 text 𝐵
											5174 text ≤ 𝑇 ) ≤
											5175 text 𝑒
											5176 container
												5177 text 𝛿
												5178 text 2
												5179 text 𝐴 𝑇 / 2
											5180 container
												5181 text 𝑝 0
											5182 text .
										5183 container
											5184 text The proposed 
											5185 text 𝛿
											5186 text  ensures 
											5187 container
												5188 text 𝛿
												5189 text 2
												5190 text 𝐴 𝑇 < 1
											5191 text  and
										5192 container
											5193 text 𝑣 ≤ 𝛿
											5194 container
												5195 text 𝐴 𝑇
											5196 text ≤
											5197 text 𝜖
											5198 container
												5199 text 64 𝐷 ( 𝐵 + 𝐽 + 1 )
											5200 text .
										5201 text This likelihood calculation is valid with null channels, because their marked firing processes are included even though they do not change the state.
										5202 heading 3. Post-exit moments are controlled uniformly, Value: 2
											5203 text 3. Post-exit moments are controlled uniformly
										5204 container
											5205 text For every elementary network with 
											5206 container
												5207 container
													5208 text 𝑘 ~
												5209 text 𝑒
												5210 text ≤ 3 / 2
											5211 text , only zero- or unary-source reactions can increase the  fine particle count
											5212 container
												5213 text 𝑛 = ∣ 𝑍
												5214 text ∣
												5215 text 1
											5216 text . Binary-source reactions have at most two products and cannot increase it.
										5217 container
											5218 text For 
											5219 container
												5220 text 𝑉 ( 𝑛 ) = ( 𝑛 + 1
												5221 text )
												5222 text 2
											5223 text , direct calculation gives
										5224 container
											5225 text 𝐿
											5226 text ~
											5227 text 𝑉 ( 𝑛 ) ≤ 12 𝐾 𝑉 ( 𝑛 ) .
										5228 text For example:
										5229 content list
											5230 container
												5231 AXListMarker • 
												5232 text zero-source reactions increase 
												5233 text 𝑛
												5234 text  by at most two;
											5235 container
												5236 AXListMarker • 
												5237 text unary-source reactions increase 
												5238 text 𝑛
												5239 text  by at most one;
											5240 container
												5241 AXListMarker • 
												5242 text all other reactions contribute nonpositively to this upper bound.
										5243 text At the exit,
										5244 container
											5245 text ∣ 𝑍 (
											5246 text 𝜏
											5247 text 𝐵
											5248 text )
											5249 text ∣
											5250 text 1
											5251 text ≤ 𝑁 (
											5252 text 𝜏
											5253 text 𝐵
											5254 text ) ≤ 𝐵 + 𝐽 .
										5255 container
											5256 text The strong Markov property therefore yields, for 
											5257 container
												5258 text 𝑡 ≥
												5259 text 𝜏
												5260 text 𝐵
											5261 text ,
										5262 container
											5263 text 𝐸
											5264 text ∼
											5265 text  ⁣
											5266 text [
											5267 text (
											5268 text ∣
											5269 text 𝑍
											5270 text (
											5271 text 𝑡
											5272 text )
											5273 container
												5274 text ∣ 1
											5275 text +
											5276 text 1
											5277 container
												5278 text ) 2
											5279 text ∣
											5280 container
												5281 text 𝐹
												5282 text 𝜏
												5283 text 𝐵
											5284 text ]
											5285 text ≤ ( 𝐵 + 𝐽 + 1
											5286 text )
											5287 text 2
											5288 text 𝑒
											5289 container
												5290 text 12 𝐾 ( 𝑡 −
												5291 text 𝜏
												5292 text 𝐵
												5293 text )
											5294 text .
										5295 container
											5296 text Since 
											5297 container
												5298 text 1 + 𝑁 ( 𝑡 ) ≤ 𝐷 ( 1 + ∣ 𝑍 ( 𝑡 )
												5299 text ∣
												5300 text 1
												5301 text )
											5302 text ,
										5303 container
											5304 text 𝐸
											5305 text ∼
											5306 text  ⁣
											5307 text [
											5308 text (
											5309 text 1
											5310 text +
											5311 text 𝑁
											5312 text (
											5313 text 𝑡
											5314 text )
											5315 container
												5316 text ) 2
											5317 container
												5318 text 1
												5319 text {
												5320 container
													5321 text 𝜏 𝐵
												5322 text ≤
												5323 text 𝑡
												5324 text }
											5325 text ]
											5326 text ≤
											5327 text 𝐷
											5328 text 2
											5329 text ( 𝐵 + 𝐽 + 1
											5330 text )
											5331 text 2
											5332 text 𝑒
											5333 container
												5334 text 12 𝐾 𝑇
											5335 text 𝑝
											5336 text ∼
											5337 text .
										5338 container
											5339 text This remains true uniformly for 
											5340 container
												5341 text 0 ≤ 𝑡 ≤ 𝑇
											5342 text . The same estimate applies nominally.
										5343 text The elementary birth bound also independently proves nonexplosion, so use of the strong Markov process here is legitimate.
										5344 heading 4. The explicit cutoff beats the post-exit growth, Value: 2
											5345 text 4. The explicit cutoff beats the post-exit growth
										5346 text With the choices above,
										5347 container
											5348 text 𝑐 ≤ 5 𝐷
											5349 text 𝑊
											5350 text 2
											5351 text ≤ 5 𝑎
											5352 text 𝑊
											5353 text 2
											5354 text , 𝐵 + 𝐽 + 1 ≤ 130 𝑎 𝑐 𝑆 ≤ 650
											5355 text 𝑎
											5356 text 2
											5357 text 𝑊
											5358 text 2
											5359 text 𝑆 .
										5360 container
											5361 text Because 
											5362 container
												5363 text 𝛿
												5364 text 2
												5365 text 𝐴 𝑇 ≤ 1
											5366 text ,
										5367 container
											5368 text 𝑝
											5369 text ∼
											5370 text ≤ 18 𝑎 𝑊
											5371 text 𝑆
											5372 container
												5373 text 1 / 2
											5374 text 𝑒
											5375 container
												5376 text − 32 𝑎 𝑆
											5377 text .
										5378 text Consequently,
										5379 container
											5380 text 𝐷
											5381 text 2
											5382 text ( 𝐵 + 𝐽 + 1
											5383 text )
											5384 text 2
											5385 text 𝑒
											5386 container
												5387 text 12 𝐾 𝑇
											5388 text 𝑝
											5389 text ∼
											5390 text ≤ 7,605,000
											5391 text 𝑎
											5392 text 7
											5393 text 𝑊
											5394 text 5
											5395 text 𝑆
											5396 container
												5397 text 5 / 2
											5398 text 𝑒
											5399 container
												5400 text − 20 𝑎 𝑇 − 32 𝑎 (
												5401 text 𝑊
												5402 text 2
												5403 text + 1 )
											5404 text .
										5405 container
											5406 text This is at most 
											5407 container
												5408 text 𝜖 / 128
											5409 text . One elementary verification is to use 
											5410 container
												5411 text 𝜖 ≥ 1 / 𝑊
											5412 text , multiply by 
											5413 container
												5414 text 128 𝑊
											5415 text , take logarithms, and bound
										5416 container
											5417 text log ⁡ 𝑎 ≤ 𝑎 , log ⁡ 𝑊 ≤
											5418 text 𝑊
											5419 text 2
											5420 text / 2 , log ⁡ 𝑆 ≤ 𝑆 .
										5421 text The remaining logarithm is bounded above by
										5422 container
											5423 text 23.5 − 25 𝑎 + ( 5.5 − 32 𝑎 )
											5424 text 𝑊
											5425 text 2
											5426 text + ( 2.5 − 20 𝑎 ) 𝑇 < 0.
										5427 text Thus
										5428 container
											5429 container
												5430 text sup ⁡
											5431 container
												5432 text 0 ≤ 𝑡 ≤ 𝑇
											5433 text 𝐸
											5434 text ∼
											5435 text  ⁣
											5436 text [
											5437 text (
											5438 text 1
											5439 text +
											5440 text 𝑁
											5441 text (
											5442 text 𝑡
											5443 text )
											5444 container
												5445 text ) 2
											5446 container
												5447 text 1
												5448 text {
												5449 container
													5450 text 𝜏 𝐵
												5451 text ≤
												5452 text 𝑡
												5453 text }
											5454 text ]
											5455 text ≤ 𝜖 / 128.
										5456 text The nominal version holds as well.
										5457 text This algebraic choice avoids computing tiny exponentials or encoding an exponentially small probability.
										5458 heading 5. Recovering the unstopped transient conclusions, Value: 2
											5459 text 5. Recovering the unstopped transient conclusions
										5460 text For TV, compare each actual terminal law to its stopped law. The discrepancy is at most its exit probability. Therefore
										5461 container
											5462 text TV ⁡ (
											5463 text 𝐿
											5464 text ∼
											5465 text ( 𝐷 𝑍 ( 𝑇 ) ) ,
											5466 text 𝐿
											5467 text 0
											5468 text ( 𝐷 𝑍 ( 𝑇 ) ) ) ≤ 𝑣 +
											5469 text 𝑝
											5470 text ∼
											5471 text +
											5472 text 𝑝
											5473 text 0
											5474 text .
										5475 container
											5476 text The bounds above make this less than 
											5477 container
												5478 text 𝜖 / 32
											5479 text .
										5480 container
											5481 text For coordinate 
											5482 text 𝑖
											5483 text , the stopped observable is bounded by 
											5484 container
												5485 text 𝐵 + 𝐽
											5486 text , so
										5487 container
											5488 text ∣
											5489 container
												5490 text 𝐸 ∼
											5491 text (
											5492 text 𝐷
											5493 text 𝑍
											5494 text (
											5495 text 𝑇
											5496 text ∧
											5497 container
												5498 text 𝜏 𝐵
											5499 text )
											5500 container
												5501 text ) 𝑖
											5502 text −
											5503 container
												5504 text 𝐸 0
											5505 text (
											5506 text 𝐷
											5507 text 𝑍
											5508 text (
											5509 text 𝑇
											5510 text ∧
											5511 container
												5512 text 𝜏 𝐵
											5513 text )
											5514 container
												5515 text ) 𝑖
											5516 text ∣
											5517 text ≤ ( 𝐵 + 𝐽 ) 𝑣 .
										5518 text For each of the two laws,
										5519 container
											5520 container
												5521 text ∣
												5522 text 𝐸
												5523 text (
												5524 text 𝐷
												5525 text 𝑍
												5526 text (
												5527 text 𝑇
												5528 text )
												5529 container
													5530 text ) 𝑖
												5531 text −
												5532 text 𝐸
												5533 text (
												5534 text 𝐷
												5535 text 𝑍
												5536 text (
												5537 text 𝑇
												5538 text ∧
												5539 container
													5540 text 𝜏 𝐵
												5541 text )
												5542 container
													5543 text ) 𝑖
												5544 text ∣
											5545 container
												5546 text ≤ 𝐸  ⁣
												5547 text [
												5548 text 𝑁
												5549 text (
												5550 text 𝑇
												5551 text )
												5552 container
													5553 text 1
													5554 text {
													5555 container
														5556 text 𝜏 𝐵
													5557 text ≤
													5558 text 𝑇
													5559 text }
												5560 text ]
												5561 text + 𝐸  ⁣
												5562 text [
												5563 text 𝑁
												5564 text (
												5565 container
													5566 text 𝜏 𝐵
												5567 text )
												5568 container
													5569 text 1
													5570 text {
													5571 container
														5572 text 𝜏 𝐵
													5573 text ≤
													5574 text 𝑇
													5575 text }
												5576 text ]
												5577 text ≤ 𝜖 / 64.
										5578 container
											5579 text Thus the perturbed and nominal terminal first moments differ by at most 
											5580 container
												5581 text 3 𝜖 / 64
											5582 text  with the sharper TV convention above, or at most 
											5583 container
												5584 text 𝜖 / 16
											5585 text  using a conservative factor-two bound.
										5586 container
											5587 text If the nominal compiler targets accuracy 
											5588 container
												5589 text 𝜖 / 2
											5590 text , these perturbative errors comfortably fit within the requested 
											5591 text 𝜖
											5592 text .
										5593 heading 6. Population and all-firing costs, Value: 2
											5594 text 6. Population and all-firing costs
										5595 container
											5596 text On 
											5597 container
												5598 text {
												5599 text 𝜏
												5600 text 𝐵
												5601 text > 𝑡 }
											5602 text , 
											5603 container
												5604 text 𝑁 ( 𝑡 ) ≤ 𝐵
											5605 text . Combining with the tail estimate,
										5606 container
											5607 container
												5608 text sup ⁡
											5609 container
												5610 text 0 ≤ 𝑡 ≤ 𝑇
											5611 text 𝐸
											5612 text ∼
											5613 text ( 1 + 𝑁 ( 𝑡 )
											5614 text )
											5615 text 2
											5616 text ≤ ( 𝐵 + 1
											5617 text )
											5618 text 2
											5619 text + 1.
										5620 text Therefore
										5621 container
											5622 container
												5623 text sup ⁡
											5624 container
												5625 text 0 ≤ 𝑡 ≤ 𝑇
											5626 text 𝐸
											5627 text ∼
											5628 text ∣ 𝑍 ( 𝑡 )
											5629 text ∣
											5630 text 1
											5631 text ≤ 𝐵 + 2.
										5632 container
											5633 text The total  actual marked firing intensity , including all binding, release, unsuccessful, null, and parallel reactions, is at most
										5634 container
											5635 text 3
											5636 text 2
											5637 text 𝐾 ( 1 + ∣ 𝑍
											5638 text ∣
											5639 text 1
											5640 text )
											5641 text 2
											5642 text .
										5643 text Hence
										5644 container
											5645 text 𝐸
											5646 text ∼
											5647 text [ all firings up to  𝑇 ] ≤
											5648 text 3
											5649 text 2
											5650 text 𝐾 𝑇 [ ( 𝐵 + 1
											5651 text )
											5652 text 2
											5653 text + 1 ] .
										5654 container
											5655 text This is polynomial in 
											5656 text 𝑊
											5657 text  whenever the nominal 
											5658 text 𝑇
											5659 text  is.
										5660 heading What this does and does not close, Value: 2
											5661 text What this does and does not close
										5662 text The argument supplies robust finite-horizon properties without proving any global Lyapunov condition for the perturbed chain:
										5663 content list
											5664 container
												5665 AXListMarker • 
												5666 text uniform nonexplosion;
											5667 container
												5668 AXListMarker • 
												5669 text robust transient TV accuracy;
											5670 container
												5671 AXListMarker • 
												5672 text robust transient absolute first moments;
											5673 container
												5674 AXListMarker • 
												5675 text polynomial transient fine populations;
											5676 container
												5677 AXListMarker • 
												5678 text polynomial all-label physical firing count.
										5679 container
											5680 text It does  not  prove that a perturbed chain has a stationary probability distribution, that it is positive recurrent, or that stationary moments are polynomial. The cutoff is chosen as a function of the finite horizon 
											5681 text 𝑇
											5682 text ; taking 
											5683 container
												5684 text 𝑇 → ∞
											5685 text  makes it diverge and yields no stationary tightness.
										5686 text I found no flaw in this finite-horizon closure, subject to the stated nominal premises.
		2356 

## Visible subagent panel: OBSTRUCTIONS

container Description: Subagents, ID: app-shell-tab-panel-app-shell-tab:1
									4827 container
										4828 button Back to subagents
											4829 image
										4830 text Obstructions
									4832 container
										4833 heading Status, Value: 2
											4834 text Status
										4835 text Done
										4836 heading Final response, Value: 2
											4837 text Final response
										4838 heading Status, Value: 2
											4839 text Status
										4840 container
											4841 text I found  no obstruction to every allowed elementary design . I did find two rigorous counterexamples to natural transfer claims:
										4842 content list
											4843 container
												4844 AXListMarker 1. 
												4845 text A legal, detailed-balanced elementary prefix lift can fail  every activity-weighted Poincaré inequality , even when the original catalytic chain has an explicit strong activity-weighted inequality.
											4846 container
												4847 AXListMarker 2. 
												4848 text Another legal, detailed-balanced prefix lift can have  zero ordinary spectral gap for every positive choice of the separation parameters . The mechanism is sequestration of a conserved catalyst in prefixes of reactions that are disabled on the communicating class.
										4849 container
											4850 text These counterexamples do  not  disprove the requested universal compiler. Different prefix ordering, additional catalytic macro channels, or a different elementary architecture can remove them.
										4851 text Your proposed repair—absorb binding/release errors into modified prefix activities and control only macro-conversion errors—survives these examples. I found no counterexample to the necessary conversion-weighted inequality consistent with the original strong activity-weighted premise.
										4852 heading 1. A particularly well-behaved original catalytic chain, Value: 2
											4853 text 1. A particularly well-behaved original catalytic chain
										4854 text Take the original weakly reversible structure
										4855 container
											4856 text 𝐵 ⇄ 𝐴 + 𝐵
										4857 container
											4858 text and add the allowed catalyst 
											4859 container
												4860 text 𝑤 = 𝐴
											4861 text , obtaining the four labelled channels
										4862 container
											4863 text 𝐵 ⇄ 𝐴 + 𝐵 , 𝐴 + 𝐵 ⇄ 2 𝐴 + 𝐵 .
										4864 container
											4865 text Set every nominal rate equal to 
											4866 text 1
											4867 text . On the communicating class 
											4868 container
												4869 text 𝐵 = 1
											4870 text , write 
											4871 container
												4872 text 𝑛 = 𝐴
											4873 text . The resulting birth–death chain has
										4874 container
											4875 text 𝑏
											4876 text 𝑛
											4877 text = 1 + 𝑛 ,
											4878 text 𝑑
											4879 text 𝑛
											4880 text = 𝑛 + 𝑛 ( 𝑛 − 1 ) =
											4881 text 𝑛
											4882 text 2
											4883 text .
										4884 text Its stationary law is
										4885 container
											4886 text 𝜋
											4887 text 𝑛
											4888 text =
											4889 container
												4890 text 𝑒
												4891 text −
												4892 text 1
											4893 container
												4894 text 𝑛 !
											4895 text ,
										4896 text because
										4897 container
											4898 text 𝜋
											4899 text 𝑛
											4900 text 𝑏
											4901 text 𝑛
											4902 text =
											4903 text 𝜋
											4904 container
												4905 text 𝑛 + 1
											4906 text 𝑑
											4907 container
												4908 text 𝑛 + 1
											4909 text .
										4910 text The total labelled firing intensity is
										4911 container
											4912 text 𝑎
											4913 text 𝑛
											4914 text = 1 + 𝑛 +
											4915 text 𝑛
											4916 text 2
											4917 text ,
										4918 text so
										4919 container
											4920 text 𝑎
											4921 text 𝑛
											4922 text ≥
											4923 container
												4924 text 1 2
											4925 text ( 1 + 𝑛
											4926 text )
											4927 text 2
											4928 text , 𝜋 𝑎 = 4.
										4929 text Its Dirichlet form is
										4930 container
											4931 text 𝐸 ( ℎ ) =
											4932 text ∑
											4933 container
												4934 text 𝑗 ≥ 1
											4935 text 𝜋
											4936 text 𝑗
											4937 text 𝑗
											4938 text 2
											4939 text (
											4940 text ℎ
											4941 text 𝑗
											4942 text −
											4943 text ℎ
											4944 container
												4945 text 𝑗 − 1
											4946 text )
											4947 text 2
											4948 text .
										4949 heading Explicit activity-weighted coercivity, Value: 3
											4950 text Explicit activity-weighted coercivity
										4951 text For completeness, there is a direct elementary proof of
										4952 container
											4953 text ∑
											4954 container
												4955 text 𝑛 ≥ 0
											4956 text 𝜋
											4957 text 𝑛
											4958 text 𝑎
											4959 text 𝑛
											4960 text (
											4961 text ℎ
											4962 text 𝑛
											4963 text − 𝜋 ℎ
											4964 text )
											4965 text 2
											4966 text ≤ 3240 𝐸 ( ℎ ) .
										4967 container
											4968 text Put 
											4969 container
												4970 text 𝑔
												4971 text 𝑛
												4972 text =
												4973 text ℎ
												4974 text 𝑛
												4975 text −
												4976 text ℎ
												4977 text 0
											4978 text , and 
											4979 container
												4980 text Δ
												4981 text 𝑗
												4982 text =
												4983 text ℎ
												4984 text 𝑗
												4985 text −
												4986 text ℎ
												4987 container
													4988 text 𝑗 − 1
											4989 text . Geometrically weighted Cauchy–Schwarz gives
										4990 container
											4991 text 𝑔
											4992 text 𝑛
											4993 text 2
											4994 text ≤ 2
											4995 text ∑
											4996 container
												4997 text 𝑗 = 1
											4998 text 𝑛
											4999 text 2
											5000 container
												5001 text 𝑛 − 𝑗
											5002 text Δ
											5003 text 𝑗
											5004 text 2
											5005 text .
										5006 container
											5007 text For 
											5008 container
												5009 text 𝑗 ≥ 1
											5010 text , writing 
											5011 container
												5012 text 𝑛 = 𝑗 + 𝑟
											5013 text ,
										5014 container
											5015 container
												5016 text ∑
												5017 container
													5018 text 𝑛 ≥ 𝑗
												5019 text 2
												5020 container
													5021 text 𝑛 − 𝑗
												5022 text 𝜋
												5023 text 𝑛
												5024 text 𝑎
												5025 text 𝑛
											5026 container
												5027 text ≤
												5028 text 𝜋
												5029 text 𝑗
												5030 text 𝑗
												5031 text 2
												5032 text ∑
												5033 container
													5034 text 𝑟 ≥ 0
												5035 container
													5036 text 2
													5037 text 𝑟
													5038 text ( 𝑟 + 2
													5039 text )
													5040 text 2
												5041 container
													5042 text 𝑟 !
											5043 container
												5044 text = 18
												5045 text 𝑒
												5046 text 2
												5047 text 𝜋
												5048 text 𝑗
												5049 text 𝑗
												5050 text 2
												5051 text .
										5052 text Here we used
										5053 container
											5054 container
												5055 text 𝑗 !
											5056 container
												5057 text ( 𝑗 + 𝑟 ) !
											5058 text ≤
											5059 text 1
											5060 container
												5061 text 𝑟 !
											5062 text ,
											5063 text 𝑎
											5064 container
												5065 text 𝑗 + 𝑟
											5066 text ≤ ( 𝑗 + 𝑟 + 1
											5067 text )
											5068 text 2
											5069 text ≤
											5070 text 𝑗
											5071 text 2
											5072 text ( 𝑟 + 2
											5073 text )
											5074 text 2
											5075 text .
										5076 text Consequently,
										5077 container
											5078 text 𝜋 ( 𝑎
											5079 text 𝑔
											5080 text 2
											5081 text ) ≤ 36
											5082 text 𝑒
											5083 text 2
											5084 text 𝐸 ( ℎ ) ≤ 324 𝐸 ( ℎ ) .
										5085 container
											5086 text Since 
											5087 container
												5088 text 𝑎 ≥ 1
											5089 text  and 
											5090 container
												5091 text 𝜋 𝑎 = 4
											5092 text ,
										5093 container
											5094 container
												5095 text 𝜋  ⁣
												5096 text [
												5097 text 𝑎
												5098 text (
												5099 text 𝑔
												5100 text −
												5101 text 𝜋
												5102 text 𝑔
												5103 container
													5104 text ) 2
												5105 text ]
											5106 container
												5107 text ≤ 2 𝜋 ( 𝑎
												5108 text 𝑔
												5109 text 2
												5110 text ) + 2 ( 𝜋 𝑔
												5111 text )
												5112 text 2
												5113 text 𝜋 𝑎
											5114 container
												5115 text ≤ 10 𝜋 ( 𝑎
												5116 text 𝑔
												5117 text 2
												5118 text ) ≤ 3240 𝐸 ( ℎ ) .
										5119 text Thus the elementary-lift failures below do not arise from a weak original chain.
										5120 heading 2. All-activity weighted coercivity can fail after an elementary lift, Value: 2
											5121 text 2. All-activity weighted coercivity can fail after an elementary lift
										5122 text Introduce auxiliary species with decoding
										5123 container
											5124 text 𝐷 𝑈 = 𝐴 + 𝐵 , 𝐷 𝐻 = 2 𝐴 , 𝐷 𝑉 = 2 𝐴 + 𝐵 .
										5125 container
											5126 text Keep 
											5127 container
												5128 text 𝐷 𝐴 = 𝐴
											5129 text , 
											5130 container
												5131 text 𝐷 𝐵 = 𝐵
											5132 text .
										5133 container
											5134 text For any 
											5135 container
												5136 text 𝐾 , 𝜃 > 0
											5137 text , use these binding/release channels:
										5138 container
											5139 table
												5140 row
													5141 cell
														5142 text Channel
													5143 cell
														5144 text Forward rate
													5145 cell
														5146 text Reverse rate
												5147 row
													5148 cell
														5149 container
															5150 text 𝐴 + 𝐵 ⇄ 𝑈
													5151 cell
														5152 container
															5153 text 𝐾 𝜃
													5154 cell
														5155 text 𝐾
												5156 row
													5157 cell
														5158 container
															5159 text 2 𝐴 ⇄ 𝐻
													5160 cell
														5161 container
															5162 text 𝐾 𝜃
													5163 cell
														5164 text 𝐾
												5165 row
													5166 cell
														5167 container
															5168 text 𝐻 + 𝐵 ⇄ 𝑉
													5169 cell
														5170 text 𝐾
													5171 cell
														5172 text 𝐾
											5173 button Copy table
										5174 text Use these macro-conversion channels:
										5175 container
											5176 table
												5177 row
													5178 cell
														5179 text Channel
													5180 cell
														5181 text Forward rate
													5182 cell
														5183 text Reverse rate
												5184 row
													5185 cell
														5186 container
															5187 text 𝐵 ⇄ 𝑈
													5188 cell
														5189 text 1
													5190 cell
														5191 container
															5192 text 1 / 𝜃
												5193 row
													5194 cell
														5195 container
															5196 text 𝑈 ⇄ 𝑉
													5197 cell
														5198 container
															5199 text 1 / 𝜃
													5200 cell
														5201 container
															5202 text 1 / 𝜃
											5203 button Copy table
										5204 container
											5205 text Every reaction has at most two molecules on each side. Every binding/release move has decoded change zero. Every macro conversion realizes the appropriate enabled original 
											5206 text 𝐴
											5207 text -birth or 
											5208 text 𝐴
											5209 text -death edge.
										5210 text All five reversible pairs are detailed balanced at activities
										5211 container
											5212 text 𝑐
											5213 text 𝐴
											5214 text =
											5215 text 𝑐
											5216 text 𝐵
											5217 text = 1 ,
											5218 text 𝑐
											5219 text 𝑈
											5220 text =
											5221 text 𝑐
											5222 text 𝐻
											5223 text =
											5224 text 𝑐
											5225 text 𝑉
											5226 text = 𝜃 .
										5227 container
											5228 text On the class of the canonical state with decoded 
											5229 container
												5230 text 𝐵 = 1
											5231 text , the fine conservation law is
										5232 container
											5233 text 𝐵 + 𝑈 + 𝑉 = 1.
										5234 text The product-form stationary law therefore has the following simple description:
										5235 content list
											5236 container
												5237 AXListMarker • 
												5238 container
													5239 text 𝑋 = 𝐴 ∼ Pois ⁡ ( 1 )
												5240 text ;
											5241 container
												5242 AXListMarker • 
												5243 container
													5244 text 𝐻 ∼ Pois ⁡ ( 𝜃 )
												5245 text ;
											5246 container
												5247 AXListMarker • 
												5248 text independently, the unique 
												5249 text 𝐵
												5250 text -containing marker is 
												5251 container
													5252 text 𝐵 , 𝑈 , 𝑉
												5253 text , with weights 
												5254 container
													5255 text 1 , 𝜃 , 𝜃
												5256 text .
										5257 container
											5258 text If 
											5259 container
												5260 text 𝐽 = 0 , 1 , 2
											5261 text  denotes these respective marker states, then the decoded 
											5262 text 𝐴
											5263 text -population is
										5264 container
											5265 text 𝑁 = 𝑋 + 2 𝐻 + 𝐽 .
										5266 heading Large firing activity with bounded decoded activity, Value: 3
											5267 text Large firing activity with bounded decoded activity
										5268 container
											5269 text Let 
											5270 container
												5271 text 𝑎 ^
											5272 text  count  all  fine labelled firings. The release channel 
											5273 container
												5274 text 𝐻 → 2 𝐴
											5275 text  gives
										5276 container
											5277 text 𝑎
											5278 text ^
											5279 text ≥ 𝐾 𝐻 .
										5280 text In contrast, decoded downward jumps occur only through
										5281 container
											5282 text 𝑈 → 𝐵 , 𝑉 → 𝑈 .
										5283 container
											5284 text There is only one marker, so the total decoded downward intensity is at most 
											5285 container
												5286 text 1 / 𝜃
											5287 text , independently of 
											5288 text 𝑁
											5289 text .
										5290 text Set
										5291 container
											5292 text 𝑓
											5293 text 𝑚
											5294 text =
											5295 text 1
											5296 container
												5297 text { 𝑁 ≥ 𝑚 }
											5298 text ,
											5299 text 𝑝
											5300 text 𝑚
											5301 text = 𝜇 ( 𝑁 = 𝑚 ) ,
											5302 text 𝑡
											5303 text 𝑚
											5304 text = 𝜇 ( 𝑁 ≥ 𝑚 ) .
										5305 text Detailed balance gives
										5306 container
											5307 text 𝐸
											5308 text ^
											5309 text (
											5310 text 𝑓
											5311 text 𝑚
											5312 text ) = stationary downward flux across  𝑚 ≤
											5313 container
												5314 text 𝑝 𝑚
											5315 text 𝜃
											5316 text .
										5317 text Meanwhile,
										5318 container
											5319 text 𝜇  ⁣
											5320 text [
											5321 container
												5322 text 𝑎 ^
											5323 text (
											5324 container
												5325 text 𝑓 𝑚
											5326 text −
											5327 text 𝜇
											5328 container
												5329 text 𝑓 𝑚
											5330 container
												5331 text ) 2
											5332 text ]
											5333 text ≥ ( 1 −
											5334 text 𝑡
											5335 text 𝑚
											5336 text )
											5337 text 2
											5338 text 𝐾
											5339 text 𝑝
											5340 text 𝑚
											5341 text 𝐸 [ 𝐻 ∣ 𝑁 = 𝑚 ] .
										5342 text To estimate the conditional mean, the independent Poisson identities give
										5343 container
											5344 text 𝐸 [ 𝑋 ( 𝑋 − 1 ) ∣ 𝑁 = 𝑚 ] =
											5345 container
												5346 text 𝑃 ( 𝑁 = 𝑚 − 2 )
											5347 container
												5348 text 𝑃 ( 𝑁 = 𝑚 )
											5349 text =
											5350 text 1
											5351 text 𝜃
											5352 text 𝐸 [ 𝐻 ∣ 𝑁 = 𝑚 ] .
										5353 container
											5354 text Let 
											5355 container
												5356 text 𝑢
												5357 text 𝑚
												5358 text = 𝐸 [ 𝑋 ∣ 𝑁 = 𝑚 ]
											5359 text  and 
											5360 container
												5361 text 𝑣
												5362 text 𝑚
												5363 text = 𝐸 [ 𝐻 ∣ 𝑁 = 𝑚 ]
											5364 text . Then
										5365 container
											5366 text 𝑢
											5367 text 𝑚
											5368 text 2
											5369 text −
											5370 text 𝑢
											5371 text 𝑚
											5372 text ≤
											5373 text 𝑣
											5374 text 𝑚
											5375 text / 𝜃 ≤ 𝑚 / ( 2 𝜃 ) ,
										5376 container
											5377 text so 
											5378 container
												5379 text 𝑢
												5380 text 𝑚
												5381 text =
												5382 text 𝑂
												5383 text 𝜃
												5384 text (
												5385 text 𝑚
												5386 text )
											5387 text . Since 
											5388 container
												5389 text 𝐽 ≤ 2
											5390 text ,
										5391 container
											5392 text 𝑣
											5393 text 𝑚
											5394 text =
											5395 container
												5396 text 𝑚 −
												5397 text 𝑢
												5398 text 𝑚
												5399 text − 𝐸 [ 𝐽 ∣ 𝑁 = 𝑚 ]
											5400 text 2
											5401 text ≥
											5402 text 𝑚
											5403 text 4
										5404 container
											5405 text for all sufficiently large 
											5406 text 𝑚
											5407 text .
										5408 container
											5409 text As 
											5410 container
												5411 text 𝑡
												5412 text 𝑚
												5413 text → 0
											5414 text , this yields
										5415 container
											5416 text 𝜇  ⁣
											5417 text [
											5418 container
												5419 text 𝑎 ^
											5420 text (
											5421 container
												5422 text 𝑓 𝑚
											5423 text −
											5424 text 𝜇
											5425 container
												5426 text 𝑓 𝑚
											5427 container
												5428 text ) 2
											5429 text ]
											5430 text ≥
											5431 container
												5432 text 𝐾 𝑚
											5433 text 16
											5434 text 𝑝
											5435 text 𝑚
										5436 container
											5437 text for all sufficiently large 
											5438 text 𝑚
											5439 text . Therefore,
										5440 container
											5441 container
												5442 text 𝜇 [
												5443 text 𝑎
												5444 text ^
												5445 text (
												5446 text 𝑓
												5447 text 𝑚
												5448 text − 𝜇
												5449 text 𝑓
												5450 text 𝑚
												5451 text )
												5452 text 2
												5453 text ]
											5454 container
												5455 text 𝐸
												5456 text ^
												5457 text (
												5458 text 𝑓
												5459 text 𝑚
												5460 text )
											5461 text ≥
											5462 container
												5463 text 𝐾 𝜃 𝑚
											5464 text 16
											5465 text ⟶ ∞ .
										5466 container
											5467 text Conclusion:  no finite constant 
											5468 text 𝐶
											5469 text  can satisfy
										5470 container
											5471 text 𝜇  ⁣
											5472 text [
											5473 container
												5474 text 𝑎 ^
											5475 text (
											5476 text ℎ
											5477 text −
											5478 text 𝜇
											5479 text ℎ
											5480 container
												5481 text ) 2
											5482 text ]
											5483 text ≤ 𝐶
											5484 text 𝐸
											5485 text ^
											5486 text ( ℎ )
										5487 container
											5488 text for this elementary lift, for any 
											5489 container
												5490 text 𝐾 , 𝜃 > 0
											5491 text .
										5492 container
											5493 text The reason is exact: 
											5494 container
												5495 text 𝐻 ⇄ 2 𝐴
											5496 text  generates increasingly many actual firings while contributing zero energy to every function constant on decoded fibres.
										5497 text A common normalization making every rate at most one scales both sides equally and does not change the conclusion.
										5498 heading 3. Dormant prefixes can destroy the ordinary spectral gap, Value: 2
											5499 text 3. Dormant prefixes can destroy the ordinary spectral gap
										5500 text Now take the original weakly reversible structure
										5501 container
											5502 text 𝑅 =
											5503 text {
											5504 text 𝐵
											5505 text ⇄
											5506 text 𝐴
											5507 text +
											5508 text 𝐵
											5509 text ,
											5510 text 3
											5511 text 𝐴
											5512 text +
											5513 text 𝐵
											5514 text +
											5515 text 𝐶
											5516 text ⇄
											5517 text 4
											5518 text 𝐴
											5519 text +
											5520 text 𝐵
											5521 text +
											5522 text 𝐶
											5523 text }
											5524 text .
										5525 container
											5526 text Add 
											5527 container
												5528 text 𝑤 = 𝐴
											5529 text  to the first pair, so the catalytic table includes
										5530 container
											5531 text 𝐴 + 𝐵 ⇄ 2 𝐴 + 𝐵 .
										5532 text Set nominal activities and original table rates equal to one.
										5533 text On the actual communicating class
										5534 container
											5535 text 𝐵 = 1 , 𝐶 = 0 ,
										5536 container
											5537 text the 
											5538 text 𝐶
											5539 text -containing reactions are disabled, and the original 
											5540 text 𝐴
											5541 text -chain is exactly the preceding well-behaved chain:
										5542 container
											5543 text 𝑏
											5544 text 𝑛
											5545 text = 1 + 𝑛 ,
											5546 text 𝑑
											5547 text 𝑛
											5548 text =
											5549 text 𝑛
											5550 text 2
											5551 text .
										5552 heading Prefix construction, Value: 3
											5553 text Prefix construction
										5554 text Introduce
										5555 container
											5556 text 𝐷
											5557 text 𝑃
											5558 text 𝑗
											5559 text = 𝑗 𝐴 + 𝐵 , 𝑗 = 1 , 2 , 3 , 4 ,
										5560 text and
										5561 container
											5562 text 𝐷
											5563 text 𝑄
											5564 text 3
											5565 text = 3 𝐴 + 𝐵 + 𝐶 , 𝐷
											5566 text 𝑄
											5567 text 4
											5568 text = 4 𝐴 + 𝐵 + 𝐶 .
										5569 text Use the binding/release channels
										5570 container
											5571 text 𝐵 + 𝐴 ⇄
											5572 text 𝑃
											5573 text 1
											5574 text with rates  𝐾 𝜃 , 𝐾 ,
										5575 container
											5576 text 𝑃
											5577 text 𝑗
											5578 text + 𝐴 ⇄
											5579 text 𝑃
											5580 container
												5581 text 𝑗 + 1
											5582 text , 𝑗 = 1 , 2 , 3 , with rates  𝐾 , 𝐾 ,
										5583 text and
										5584 container
											5585 text 𝑃
											5586 text 3
											5587 text + 𝐶 ⇄
											5588 text 𝑄
											5589 text 3
											5590 text ,
											5591 text 𝑃
											5592 text 4
											5593 text + 𝐶 ⇄
											5594 text 𝑄
											5595 text 4
											5596 text , with rates  𝐾 , 𝐾 .
										5597 text Use macro conversions
										5598 container
											5599 text 𝐵 ⇄
											5600 text 𝑃
											5601 text 1
											5602 text with rates  1 , 1 / 𝜃 ,
										5603 container
											5604 text 𝑃
											5605 text 1
											5606 text ⇄
											5607 text 𝑃
											5608 text 2
											5609 text with rates  1 / 𝜃 , 1 / 𝜃 ,
										5610 container
											5611 text 𝑄
											5612 text 3
											5613 text ⇄
											5614 text 𝑄
											5615 text 4
											5616 text with rates  1 / 𝜃 , 1 / 𝜃 .
										5617 container
											5618 text Again every channel is elementary and the fine network is detailed balanced at original-species activities one and all auxiliary activities 
											5619 text 𝜃
											5620 text .
										5621 container
											5622 text On the class 
											5623 container
												5624 text 𝐶 = 0
											5625 text , both 
											5626 container
												5627 text 𝑄
												5628 text 3
												5629 text ,
												5630 text 𝑄
												5631 text 4
											5632 text  are absent. But 
											5633 container
												5634 text 𝑃
												5635 text 3
												5636 text ,
												5637 text 𝑃
												5638 text 4
											5639 text  remain available even though they are merely prefixes of the disabled 
											5640 text 𝐶
											5641 text -containing complexes.
										5642 text The stationary law is:
										5643 content list
											5644 container
												5645 AXListMarker • 
												5646 container
													5647 text 𝑋 = 𝐴 ∼ Pois ⁡ ( 1 )
												5648 text ;
											5649 container
												5650 AXListMarker • 
												5651 text independently, one marker 
												5652 container
													5653 text 𝐽 ∈ { 0 , 1 , 2 , 3 , 4 }
												5654 text , where 
												5655 container
													5656 text 𝐽 = 0
												5657 text  denotes free 
												5658 text 𝐵
												5659 text  and 
												5660 container
													5661 text 𝐽 = 𝑗
												5662 text  denotes 
												5663 container
													5664 text 𝑃 𝑗
												5665 text ;
											5666 container
												5667 AXListMarker • 
												5668 text marker weights are
												5669 container
													5670 text ( 1 , 𝜃 , 𝜃 , 𝜃 , 𝜃 ) .
										5671 container
											5672 text The decoded population is 
											5673 container
												5674 text 𝑁 = 𝑋 + 𝐽
											5675 text . Define
										5676 container
											5677 text 𝑞
											5678 text 𝑛
											5679 text = 1 + 𝜃
											5680 text ∑
											5681 container
												5682 text 𝑗 = 1
											5683 text 4
											5684 text ( 𝑛
											5685 text )
											5686 text 𝑗
											5687 text .
										5688 text Its stationary probability is
										5689 container
											5690 text 𝑝
											5691 text 𝑛
											5692 text = 𝜇 ( 𝑁 = 𝑛 ) =
											5693 container
												5694 text 𝑒
												5695 text −
												5696 text 1
											5697 container
												5698 text ( 1 + 4 𝜃 ) 𝑛 !
											5699 text 𝑞
											5700 text 𝑛
											5701 text .
										5702 text The conditional marker probabilities are
										5703 container
											5704 text 𝜇 ( 𝐽 = 𝑗 ∣ 𝑁 = 𝑛 ) =
											5705 container
												5706 text 𝜃 ( 𝑛
												5707 text )
												5708 text 𝑗
											5709 container
												5710 text 𝑞 𝑛
											5711 text , 𝑗 = 1 , … , 4 ,
										5712 container
											5713 text and 
											5714 container
												5715 text 𝜇 ( 𝐽 = 0 ∣ 𝑁 = 𝑛 ) = 1 /
												5716 text 𝑞
												5717 text 𝑛
											5718 text .
										5719 heading Exact decay of the aggregate downward rate, Value: 3
											5720 text Exact decay of the aggregate downward rate
										5721 container
											5722 text Decoded 
											5723 text 𝐴
											5724 text -death occurs only through
										5725 container
											5726 text 𝑃
											5727 text 1
											5728 text → 𝐵 ,
											5729 text 𝑃
											5730 text 2
											5731 text →
											5732 text 𝑃
											5733 text 1
											5734 text ,
										5735 container
											5736 text both with rate 
											5737 container
												5738 text 1 / 𝜃
											5739 text . Thus the conditional downward intensity is exactly
										5740 container
											5741 container
												5742 text 𝑑 ‾
											5743 text 𝑛
											5744 text =
											5745 container
												5746 text 𝑛 + 𝑛 ( 𝑛 − 1 )
											5747 container
												5748 text 𝑞 𝑛
											5749 text =
											5750 container
												5751 text 𝑛 2
											5752 container
												5753 text 𝑞 𝑛
											5754 text .
										5755 container
											5756 text Since 
											5757 container
												5758 text 𝑞
												5759 text 𝑛
												5760 text ∼ 𝜃
												5761 text 𝑛
												5762 text 4
											5763 text ,
										5764 container
											5765 container
												5766 text 𝑑 ‾
											5767 text 𝑛
											5768 text ∼
											5769 text 1
											5770 container
												5771 text 𝜃
												5772 text 𝑛
												5773 text 2
											5774 text ⟶ 0.
										5775 container
											5776 text For 
											5777 container
												5778 text 𝑓
												5779 text 𝑚
												5780 text =
												5781 text 1
												5782 container
													5783 text { 𝑁 ≥ 𝑚 }
											5784 text , detailed balance gives
										5785 container
											5786 text 𝐸
											5787 text ^
											5788 text (
											5789 text 𝑓
											5790 text 𝑚
											5791 text ) =
											5792 text 𝑝
											5793 text 𝑚
											5794 container
												5795 text 𝑚 2
											5796 container
												5797 text 𝑞 𝑚
											5798 text .
										5799 container
											5800 text Writing 
											5801 container
												5802 text 𝑡
												5803 text 𝑚
												5804 text = 𝜇 ( 𝑁 ≥ 𝑚 )
											5805 text , for sufficiently large 
											5806 text 𝑚
											5807 text ,
										5808 container
											5809 container
												5810 text Var ⁡
											5811 text 𝜇
											5812 text (
											5813 text 𝑓
											5814 text 𝑚
											5815 text ) =
											5816 text 𝑡
											5817 text 𝑚
											5818 text ( 1 −
											5819 text 𝑡
											5820 text 𝑚
											5821 text ) ≥
											5822 text 1
											5823 text 2
											5824 text 𝑝
											5825 text 𝑚
											5826 text .
										5827 text Hence
										5828 container
											5829 container
												5830 text 𝐸
												5831 text ^
												5832 text (
												5833 text 𝑓
												5834 text 𝑚
												5835 text )
											5836 container
												5837 container
													5838 text Var ⁡
												5839 text 𝜇
												5840 text (
												5841 text 𝑓
												5842 text 𝑚
												5843 text )
											5844 text ≤
											5845 container
												5846 text 2
												5847 text 𝑚
												5848 text 2
											5849 container
												5850 text 𝑞 𝑚
											5851 text ⟶ 0.
										5852 container
											5853 text Conclusion:  the fine nominal chain has  zero spectral gap for every 
											5854 container
												5855 text 𝐾 , 𝜃 > 0
											5856 text .
										5857 container
											5858 text This is stronger than failure to obtain a polynomial comparison constant: no positive global 
											5859 container
												5860 text 𝐿 2
											5861 text  spectral gap exists for this particular lift.
										5862 heading What this does and does not establish, Value: 3
											5863 text What this does and does not establish
										5864 text It establishes that the following implication is false without additional structural work:
										5865 text “The original catalytic chain has strong activity-weighted coercivity; therefore its usual elementary prefix lift has a positive spectral gap.”
										5866 container
											5867 text It does  not  establish failure of the user’s compiler contract. In particular:
										5868 content list
											5869 container
												5870 AXListMarker • 
												5871 text the contract asks for mixing from the compiled canonical starting state, not a uniform global 
												5872 container
													5873 text 𝐿 2
												5874 text  gap;
											5875 container
												5876 AXListMarker • 
												5877 text zero gap permits subgeometric mixing that could still give polynomial numerical costs for this task;
											5878 container
												5879 AXListMarker • 
												5880 text adding active macro channels involving 
												5881 container
													5882 text 𝑃
													5883 text 3
													5884 text ,
													5885 text 𝑃
													5886 text 4
												5887 text  can remove this example;
											5888 container
												5889 AXListMarker • 
												5890 text changing the lift may prevent the sequestration.
										5891 heading 4. Assessment of your conversion-only perturbation route, Value: 2
											5892 text 4. Assessment of your conversion-only perturbation route
										5893 container
											5894 text If each auxiliary has one defining reversible binding step, independent errors in those binding/release rates can be incorporated into altered auxiliary activities. Those activities are finite products of equilibrium-rate ratios, so their relative distortion is bounded by a fixed-
											5895 text 𝑅
											5896 text  power of 
											5897 container
												5898 text 1 ± 𝛿
											5899 text .
										5900 container
											5901 text That leaves only macro-conversion errors relative to a suitably adjusted reference process. The relevant perturbation activity 
											5902 text 𝑏
											5903 text  then counts macro conversions rather than all fine firings.
										5904 container
											5905 text Neither counterexample above refutes coercivity weighted by 
											5906 text 𝑏
											5907 text :
										5908 content list
											5909 container
												5910 AXListMarker • 
												5911 text In the first example, 
												5912 text 𝑏
												5913 text  is bounded while the troublesome assembly activity grows.
											5914 container
												5915 AXListMarker • 
												5916 text In the second example, 
												5917 text 𝑏
												5918 text  itself decreases in the sequestered tail, at the same order as the escape activity.
										5919 container
											5920 text An argument using 
											5921 text 𝑏
											5922 text -weighted coercivity would still need to address:
										5923 content list
											5924 container
												5925 AXListMarker 1. 
												5926 text States with 
												5927 container
													5928 text 𝑏 = 0
												5929 text , and the appropriate positive extension or harmonic control through binding states.
											5930 container
												5931 AXListMarker 2. 
												5932 text First-moment estimates through dual weights; ordinary unweighted 
												5933 container
													5934 text 𝐿 2
												5935 text  control may be unavailable.
											5936 container
												5937 AXListMarker 3. 
												5938 text Mixing from canonical initialization without assuming a positive ordinary spectral gap.
											5939 container
												5940 AXListMarker 4. 
												5941 text Total physical firings separately, using adequate fine-population moments.
										5942 text I have no proof that these operations hold universally, and no universal negative showing that they cannot.
		2356 

## Visible subagent panel: LIFT

container Description: Subagents, ID: app-shell-tab-panel-app-shell-tab:1
									4829 container
										4830 button Back to subagents
											4831 image
										4832 text Lift analysis
									4834 container
										4835 heading Status, Value: 2
											4836 text Status
										4837 text Done
										4838 heading Final response, Value: 2
											4839 text Final response
										4840 heading Result of this subtask, Value: 2
											4841 text Result of this subtask
										4842 container
											4843 text I can close the  entire nominal version  of the elementary-lift contract on infinite communicating classes, with polynomial numerical rates, mixing time, auxiliary populations, and actual firing count. The proof uses analytical stopping only; the physical network remains autonomous and untruncated.
										4844 container
											4845 text I can also absorb all binding-rate errors into an exactly complex-balanced reference process, and a finite-horizon likelihood argument then gives polynomially robust transient accuracy and activity bounds. What this does  not  yet establish is positive recurrence and stationary accuracy of the actual perturbed process for arbitrarily long time. That is the remaining essential gap.
										4846 text The nominal construction and its estimates are detailed below.
										4847 heading 1. Fixed network and notation, Value: 1
											4848 text 1. Fixed network and notation
										4849 container
											4850 text Apply the accepted higher-molecularity compiler at a smaller accuracy, for example 
											4851 container
												4852 text 𝜖 / 16
											4853 text . Write its fixed catalytic table as
										4854 container
											4855 text 𝑌
											4856 text 𝑟
											4857 text ⟶
											4858 text 𝑍
											4859 text 𝑟
											4860 text , 𝑟 = 1 , … , 𝑚 ,
										4861 container
											4862 text with nominal constants 
											4863 container
												4864 text 0 <
												4865 text 𝜅
												4866 text 𝑟
												4867 text ≤ 1
											4868 text , complex balance at 
											4869 text 𝜆
											4870 text , and nominal mixing time 
											4871 container
												4872 text 𝑇 0
											4873 text . Its classes are the actual original classes.
										4874 container
											4875 text Absorb the constant incurred by replacing 
											4876 text 𝜖
											4877 text  with 
											4878 container
												4879 text 𝜖 / 16
											4880 text  into fixed computable constants 
											4881 container
												4882 text 𝐶 ≥ 1
											4883 text , 
											4884 container
												4885 text 𝑝 ∈ 𝑁
											4886 text , so that
										4887 container
											4888 text 𝑇
											4889 text 0
											4890 text ,
											4891 container
												4892 text max ⁡
											4893 text 𝑟
											4894 text 𝜅
											4895 text 𝑟
											4896 container
												4897 text − 1
											4898 text ≤ 𝐶
											4899 text 𝑊
											4900 text 𝑝
											4901 text .
										4902 container
											4903 text Its nominal decoded law at 
											4904 container
												4905 text 𝑇 0
											4906 text  has TV and absolute coordinate-mean error at most 
											4907 container
												4908 text 𝜖 / 16
											4909 text .
										4910 text Let
										4911 container
											4912 text 𝐷 = max ⁡  ⁣
											4913 text (
											4914 text 1
											4915 text ,
											4916 container
												4917 text max
												4918 text ⁡
												4919 text 𝑟
											4920 text ∣
											4921 container
												4922 text 𝑌 𝑟
											4923 container
												4924 text ∣ 1
											4925 text ,
											4926 container
												4927 text max
												4928 text ⁡
												4929 text 𝑟
											4930 text ∣
											4931 container
												4932 text 𝑍 𝑟
											4933 container
												4934 text ∣ 1
											4935 text )
											4936 text .
										4937 container
											4938 text Use the supplied prefix construction, with one important implementation detail: order each complex’s molecules canonically, share identical ordered prefixes, and give every auxiliary prefix a  unique parent prefix . This makes the assembly graph a forest and is useful for the perturbation argument.
										4939 text Let the auxiliary encoding vectors be
										4940 container
											4941 text 𝑐
											4942 text 1
											4943 text , … ,
											4944 text 𝑐
											4945 text 𝑠
											4946 text , 2 ≤ ∣
											4947 text 𝑐
											4948 text 𝑗
											4949 text ∣
											4950 text 1
											4951 text ≤ 𝐷 ,
										4952 container
											4953 text and let 
											4954 text 𝐸
											4955 text  have these columns. Then
										4956 container
											4957 text 𝐷
											4958 container
												4959 text d e c
											4960 text ( 𝑛 , 𝑎 ) = 𝑛 + 𝐸 𝑎 .
										4961 text Every auxiliary column is nonzero, so
										4962 container
											4963 container
												4964 text ∣ ( 𝑛 , 𝑎 )
												4965 text ∣
												4966 text 1
												4967 text ≤ ∣
												4968 text 𝐷
												4969 container
													4970 text d e c
												4971 text ( 𝑛 , 𝑎 )
												4972 text ∣
												4973 text 1
												4974 text .
											4975 text (1)
										4976 container
											4977 text Take auxiliary activities 
											4978 container
												4979 text 𝜃
												4980 text 𝜆
												4981 container
													4982 text 𝑐 𝑗
											4983 text . Raw first-binding/release rates are 
											4984 container
												4985 text 𝐾 𝜃 , 𝐾
											4986 text ; later assembly/release rates are 
											4987 container
												4988 text 𝐾 , 𝐾
											4989 text . Replace 
											4990 container
												4991 text 𝑌
												4992 text 𝑟
												4993 text →
												4994 text 𝑍
												4995 text 𝑟
											4996 text  by its representative conversion with raw rate 
											4997 container
												4998 text 𝜅
												4999 text 𝑟
												5000 text / 𝜃
											5001 text  if its source has order at least two, and 
											5002 container
												5003 text 𝜅 𝑟
											5004 text  otherwise.
										5005 text All physical reactions have at most two molecules on either side.
										5006 text The exact graph claim is as supplied, and in fact
										5007 container
											5008 container
												5009 text Γ
												5010 text ^
												5011 text = { ( 𝑛 , 𝑎 ) : 𝑛 + 𝐸 𝑎 ∈ Γ } .
											5012 text (2)
										5013 container
											5014 text Indeed every fine state releases to its canonical encoding, and the reversed assembly path recovers it; canonical original edges lift using the 
											5015 container
												5016 text 𝑤 = 0
											5017 text  channels.
										5018 heading 2. Infinite-class static error is polynomially controllable, Value: 1
											5019 text 2. Infinite-class static error is polynomially controllable
										5020 text Write
										5021 container
											5022 text 𝑤 ( 𝑥 ) =
											5023 container
												5024 text 𝜆 𝑥
											5025 container
												5026 text 𝑥 !
											5027 text ,
											5028 text 𝑞
											5029 text 𝜃
											5030 text ( 𝑥 ) =
											5031 text ∑
											5032 container
												5033 text 𝑎 : 𝐸 𝑎 ≤ 𝑥
											5034 container
												5035 text 𝜃
												5036 container
													5037 text ∣ 𝑎 ∣
												5038 text ( 𝑥
												5039 text )
												5040 container
													5041 text 𝐸 𝑎
											5042 container
												5043 text 𝑎 !
											5044 text .
										5045 text The fine product-form stationary measure has decoded law
										5046 container
											5047 container
												5048 text 𝜌
												5049 text 𝜃
												5050 text ( 𝑥 ) =
												5051 container
													5052 text 𝜋
													5053 text 𝜆
													5054 text ( 𝑥 )
													5055 text 𝑞
													5056 text 𝜃
													5057 text ( 𝑥 )
												5058 container
													5059 text 𝐸
													5060 container
														5061 text 𝜋 𝜆
													5062 text 𝑞
													5063 text 𝜃
													5064 text ( 𝑋 )
												5065 text .
											5066 text (3)
										5067 container
											5068 text The decisive point is to use the  exact compound-Poisson generating function , not 
											5069 container
												5070 text exp ⁡ ( 𝑠 𝜃 ∣ 𝑥
												5071 text ∣
												5072 text 𝐷
												5073 text )
											5074 text  globally:
										5075 container
											5076 container
												5077 text ∑
												5078 container
													5079 text 𝑥 ∈
													5080 text 𝑁
													5081 text 𝑑
												5082 text 𝑤 ( 𝑥 )
												5083 text 𝑞
												5084 text 𝜃
												5085 text ( 𝑥 )
												5086 text 𝑒
												5087 container
													5088 text 𝑡 ∣ 𝑥
													5089 text ∣
													5090 text 1
												5091 text = exp ⁡  ⁣
												5092 text (
												5093 container
													5094 text 𝑒 𝑡
												5095 container
													5096 text ∑ 𝑖
												5097 container
													5098 text 𝜆 𝑖
												5099 text +
												5100 text 𝜃
												5101 container
													5102 text ∑
													5103 text 𝑗
													5104 text =
													5105 text 1
													5106 text 𝑠
												5107 container
													5108 text 𝜆
													5109 text 𝑐
													5110 text 𝑗
												5111 container
													5112 text 𝑒
													5113 text 𝑡
													5114 text ∣
													5115 container
														5116 text 𝑐 𝑗
													5117 container
														5118 text ∣ 1
												5119 text )
												5120 text .
											5121 text (4)
										5122 text The known canonical state supplies the normalization bound
										5123 container
											5124 container
												5125 text 𝑤 (
												5126 text 𝑥
												5127 text 0
												5128 text ) ≥
												5129 text 𝑊
												5130 container
													5131 text − 2 ∣
													5132 text 𝑥
													5133 text 0
													5134 text ∣
													5135 text 1
												5136 text ,
											5137 text (5)
										5138 container
											5139 text because 
											5140 container
												5141 text 𝜆
												5142 text 𝑖
												5143 container
													5144 text − 1
												5145 text ≤ 𝑊
											5146 text  and 
											5147 container
												5148 text 𝑥
												5149 text 0
												5150 text ! ≤
												5151 text 𝑊
												5152 container
													5153 text ∣
													5154 text 𝑥
													5155 text 0
													5156 text ∣
													5157 text 1
											5158 text .
										5159 text Assume
										5160 container
											5161 container
												5162 text 𝜃 𝑠
												5163 text 𝑊
												5164 text 𝐷
												5165 text ≤ 1.
											5166 text (6)
										5167 container
											5168 text At 
											5169 container
												5170 text 𝑡 = 1 / 𝐷
											5171 text , (4) and (5) give
										5172 container
											5173 container
												5174 text 𝐸
												5175 container
													5176 text 𝜋 𝜆
												5177 text [
												5178 text 𝑞
												5179 text 𝜃
												5180 text ( 𝑋 )
												5181 text 𝑒
												5182 container
													5183 text ∣ 𝑋
													5184 text ∣
													5185 text 1
													5186 text / 𝐷
												5187 text ] ≤ exp ⁡ ( 4
												5188 text 𝑊
												5189 text 2
												5190 text ) .
											5191 text (7)
										5192 container
											5193 text Here 
											5194 container
												5195 text 𝑊 > 10
											5196 text , so the elementary estimate
											5197 container
												5198 text 2 𝑊 log ⁡ 𝑊 + 3 𝑊 + 3 ≤ 4
												5199 text 𝑊
												5200 text 2
											5201 text  is ample.
										5202 text For any
										5203 container
											5204 text 𝐵 ≥ 16 𝐷 ( 𝐷 + 1 )
											5205 text 𝑊
											5206 text 2
											5207 text ,
										5208 text we obtain
										5209 container
											5210 container
												5211 text 𝐸
												5212 container
													5213 text 𝜋 𝜆
												5214 text [
												5215 container
													5216 text 𝑞 𝜃
												5217 text (
												5218 text 𝑋
												5219 text )
												5220 text (
												5221 text ∣
												5222 text 𝑋
												5223 container
													5224 text ∣ 1
												5225 text +
												5226 text 1
												5227 text )
												5228 container
													5229 text 1
													5230 text {
													5231 text ∣
													5232 text 𝑋
													5233 container
														5234 text ∣ 1
													5235 text >
													5236 text 𝐵
													5237 text }
												5238 text ]
												5239 text ≤ ( 2 𝐷 + 1 )
												5240 text 𝑒
												5241 container
													5242 text 4
													5243 text 𝑊
													5244 text 2
													5245 text − 𝐵 / ( 2 𝐷 )
												5246 text ≤
												5247 text 𝜖
												5248 text 32
												5249 text .
											5250 text (8)
										5251 container
											5252 text The last inequality follows from 
											5253 container
												5254 text 𝑊 ≥
												5255 text 𝜖
												5256 container
													5257 text − 1
											5258 text ; no class probability or normalizer is supplied or computed.
										5259 container
											5260 text On 
											5261 container
												5262 text ∣ 𝑥
												5263 text ∣
												5264 text 1
												5265 text ≤ 𝐵
											5266 text ,
										5267 container
											5268 text 1 ≤
											5269 text 𝑞
											5270 text 𝜃
											5271 text ( 𝑥 ) ≤
											5272 text 𝑒
											5273 container
												5274 text 𝑠 𝜃
												5275 text 𝐵
												5276 text 𝐷
											5277 text .
										5278 text Thus if
										5279 container
											5280 container
												5281 text 𝜃 ≤
												5282 text 𝜖
												5283 container
													5284 text 128 𝑠 ( 𝐵 + 1
													5285 text )
													5286 container
														5287 text 𝐷 + 1
												5288 text ,
											5289 text (9)
										5290 text then
										5291 container
											5292 container
												5293 text 𝑞
												5294 text 𝜃
												5295 text ( 𝑥 ) − 1 ≤ 𝛼 , 𝛼 =
												5296 text 𝜖
												5297 container
													5298 text 64 ( 𝐵 + 1 )
												5299 text .
											5300 text (10)
										5301 container
											5302 text Let 
											5303 container
												5304 text 𝑟 =
												5305 text 𝐸
												5306 text 𝜋
												5307 text 𝑞
												5308 text 𝜃
											5309 text . Equations (8)–(10) yield
										5310 container
											5311 container
												5312 text 𝑟 − 1 ≤ 𝛼 +
												5313 text 𝜖
												5314 container
													5315 text 32 𝐵
												5316 text ,
											5317 text (11)
										5318 container
											5319 container
												5320 text 𝐸
												5321 text 𝜋
												5322 text ∣ 𝑋
												5323 text ∣
												5324 text 1
												5325 text ≤ 𝐵 + 1 ,
											5326 text (12)
										5327 text and
										5328 container
											5329 container
												5330 text 𝐸
												5331 text 𝜋
												5332 text [ ∣ 𝑋
												5333 text ∣
												5334 text 1
												5335 text (
												5336 text 𝑞
												5337 text 𝜃
												5338 text − 1 ) ] ≤ 𝐵 𝛼 +
												5339 text 𝜖
												5340 text 32
												5341 text .
											5342 text (13)
										5343 container
											5344 text Since 
											5345 container
												5346 text 𝑞
												5347 text 𝜃
												5348 text ≥ 1
											5349 text ,
										5350 container
											5351 container
												5352 text ∥
												5353 text 𝜌
												5354 text 𝜃
												5355 text − 𝜋
												5356 text ∥
												5357 container
													5358 text T V
												5359 text ≤ 𝑟 − 1 <
												5360 text 𝜖
												5361 text 8
												5362 text .
											5363 text (14)
										5364 text For each coordinate,
										5365 container
											5366 container
												5367 container
													5368 text ∣
													5369 text 𝜌
													5370 text 𝜃
													5371 text 𝑋
													5372 text 𝑖
													5373 text − 𝜋
													5374 text 𝑋
													5375 text 𝑖
													5376 text ∣
												5377 container
													5378 text ≤
													5379 text 𝐸
													5380 text 𝜋
													5381 text [ ∣ 𝑋
													5382 text ∣
													5383 text 1
													5384 text (
													5385 text 𝑞
													5386 text 𝜃
													5387 text − 1 ) ] + ( 𝑟 − 1 )
													5388 text 𝐸
													5389 text 𝜋
													5390 text ∣ 𝑋
													5391 text ∣
													5392 text 1
												5393 container
													5394 text ≤ 𝛼 ( 2 𝐵 + 1 ) +
													5395 text 𝜖
													5396 text 32
													5397 text +
													5398 container
														5399 text 𝜖 ( 𝐵 + 1 )
													5400 container
														5401 text 32 𝐵
													5402 text ≤
													5403 text 𝜖
													5404 text 8
													5405 text .
											5406 text (15)
										5407 container
											5408 text This proves polynomial static approximation on  every  class, including infinite classes.
										5409 heading 3. A near- contraction gives polynomial nominal moments for all time, Value: 1
											5410 text 3. A near-
											5411 container
												5412 text 𝐿 1
											5413 text  contraction gives polynomial nominal moments for all time
										5414 text This is useful independently of any mixing or spectral-gap estimate.
										5415 container
											5416 text Let 
											5417 text 𝜇
											5418 text  be the nominal fine stationary measure, and put
										5419 container
											5420 text 𝑁 ( 𝑢 ) = ∣
											5421 text 𝐷
											5422 container
												5423 text d e c
											5424 text 𝑢
											5425 text ∣
											5426 text 1
											5427 text , 𝐻 = 4
											5428 text 𝑊
											5429 text 2
											5430 text , 𝑞 = ⌈ 𝐻 ⌉ , 𝑟 =
											5431 text 𝑞
											5432 container
												5433 text 𝑞 − 1
											5434 text .
										5435 text The same generating-function estimate gives
										5436 container
											5437 container
												5438 text 𝜇 (
												5439 text 𝑒
												5440 container
													5441 text 𝑁 / 𝐷
												5442 text ) ≤
												5443 text 𝑒
												5444 text 𝐻
												5445 text , 𝜇 ( 𝑗 (
												5446 text 𝑥
												5447 text 0
												5448 text ) ) ≥
												5449 text 𝑒
												5450 container
													5451 text − 𝐻
												5452 text .
											5453 text (16)
										5454 container
											5455 text For the density 
											5456 container
												5457 text 𝑓 𝑡
											5458 text  of the process started at 
											5459 container
												5460 text 𝑗 (
												5461 text 𝑥
												5462 text 0
												5463 text )
											5464 text , stationarity and Jensen imply contraction of the adjoint Markov semigroup in 
											5465 container
												5466 text 𝐿
												5467 text 𝑟
												5468 text ( 𝜇 )
											5469 text :
										5470 container
											5471 container
												5472 text ∥
												5473 text 𝑓
												5474 text 𝑡
												5475 text ∥
												5476 container
													5477 text 𝐿
													5478 text 𝑟
													5479 text ( 𝜇 )
												5480 text ≤ ∥
												5481 text 𝑓
												5482 text 0
												5483 text ∥
												5484 container
													5485 text 𝐿
													5486 text 𝑟
													5487 text ( 𝜇 )
												5488 text = 𝜇 ( 𝑗 (
												5489 text 𝑥
												5490 text 0
												5491 text )
												5492 text )
												5493 container
													5494 text − 1 / 𝑞
												5495 text ≤ 𝑒 .
											5496 text (17)
										5497 container
											5498 text For every fixed integer 
											5499 container
												5500 text ℎ ≥ 1
											5501 text ,
										5502 container
											5503 text 𝑁
											5504 container
												5505 text ℎ 𝑞
											5506 text ≤
											5507 text 𝐷
											5508 container
												5509 text ℎ 𝑞
											5510 text ( ℎ 𝑞 ) !
											5511 text 𝑒
											5512 container
												5513 text 𝑁 / 𝐷
											5514 text .
										5515 container
											5516 text Hölder and (16)–(17) therefore give, for all 
											5517 container
												5518 text 𝑡 ≥ 0
											5519 text ,
										5520 container
											5521 container
												5522 container
													5523 text 𝐸
													5524 container
														5525 text 𝑗 (
														5526 text 𝑥
														5527 text 0
														5528 text )
													5529 text 𝑁 (
													5530 text 𝑍
													5531 text 𝑡
													5532 text )
													5533 text ℎ
												5534 container
													5535 text ≤ 𝑒
													5536 container
														5537 text ( 𝜇
														5538 text 𝑁
														5539 container
															5540 text ℎ 𝑞
														5541 text )
													5542 container
														5543 text 1 / 𝑞
												5544 container
													5545 text ≤
													5546 text 𝑒
													5547 text 2
													5548 text ( 𝐷 ℎ 𝑞
													5549 text )
													5550 text ℎ
												5551 container
													5552 text ≤ 9 ( 5 𝐷 ℎ
													5553 text )
													5554 text ℎ
													5555 text 𝑊
													5556 container
														5557 text 2 ℎ
													5558 text .
											5559 text (18)
										5560 container
											5561 text The same estimate holds for the original nominal process; using 
											5562 container
												5563 text 𝐷 ≥ 1
											5564 text  merely enlarges its constant.
										5565 text It also bounds the stationary moments. In particular, with
										5566 container
											5567 text 𝐴
											5568 text ℎ
											5569 text = 9 ( 5 𝐷 ℎ
											5570 text )
											5571 text ℎ
											5572 text ,
											5573 text 𝐹
											5574 text ℎ
											5575 text =
											5576 text 2
											5577 container
												5578 text ℎ − 1
											5579 text (
											5580 text 𝐴
											5581 text ℎ
											5582 text + 1 ) ,
										5583 text we have
										5584 container
											5585 container
												5586 container
													5587 text sup ⁡
												5588 container
													5589 text 𝑡 ≥ 0
												5590 text 𝐸 ( 𝑁 (
												5591 text 𝑍
												5592 text 𝑡
												5593 text ) + 1
												5594 text )
												5595 text ℎ
												5596 text ≤
												5597 text 𝐹
												5598 text ℎ
												5599 text 𝑊
												5600 container
													5601 text 2 ℎ
												5602 text .
											5603 text (19)
										5604 container
											5605 text This avoids the exponentially large 
											5606 container
												5607 text 𝐿 2
											5608 text  norm of the initial point mass. It uses 
											5609 container
												5610 text 𝑟 − 1 ≍
												5611 text 𝑊
												5612 container
													5613 text − 2
											5614 text , only as a proof parameter.
										5615 text Because of (1), (18) also bounds every auxiliary population.
										5616 heading 4. Explicit polynomial mixing of each bounded fast fibre, Value: 1
											5617 text 4. Explicit polynomial mixing of each bounded fast fibre
										5618 container
											5619 text Fix a decoded state 
											5620 text 𝑥
											5621 text  with 
											5622 container
												5623 text ∣ 𝑥
												5624 text ∣
												5625 text 1
												5626 text ≤ 𝐵
											5627 text . Remove the common factor 
											5628 text 𝐾
											5629 text  from the binding generator and call the resulting generator 
											5630 container
												5631 text 𝐹 𝑥
											5632 text .
										5633 text Its invariant probability on the fibre is
										5634 container
											5635 container
												5636 text 𝜈
												5637 text 𝑥
												5638 text ( 𝑎 ) =
												5639 text 1
												5640 container
													5641 text 𝑞
													5642 text 𝜃
													5643 text ( 𝑥 )
												5644 container
													5645 text 𝜃
													5646 container
														5647 text ∣ 𝑎 ∣
													5648 text ( 𝑥
													5649 text )
													5650 container
														5651 text 𝐸 𝑎
												5652 container
													5653 text 𝑎 !
												5654 text .
											5655 text (20)
										5656 text Assume
										5657 container
											5658 container
												5659 text 𝜃 ( 𝐵 + 1
												5660 text )
												5661 text 𝐷
												5662 text ≤
												5663 text 1
												5664 text 2
												5665 text , 𝑠 𝜃
												5666 text 𝐵
												5667 text 𝐷
												5668 text ≤ 1.
											5669 text (21)
										5670 container
											5671 text These are much weaker than the eventual choice of 
											5672 text 𝜃
											5673 text .
										5674 heading Release paths, Value: 3
											5675 text Release paths
										5676 text From any fibre state, release one complete auxiliary at a time.
										5677 container
											5678 text If one prefix with encoding 
											5679 text 𝑐
											5680 text  is completely released, the endpoint weight ratio is
										5681 container
											5682 container
												5683 container
													5684 text 𝜈
													5685 text 𝑥
													5686 text ( 𝑎 −
													5687 text 𝑒
													5688 text 𝑐
													5689 text )
												5690 container
													5691 text 𝜈
													5692 text 𝑥
													5693 text ( 𝑎 )
												5694 text =
												5695 container
													5696 text 𝑎 𝑐
												5697 text 𝜃
												5698 container
													5699 text 𝑛 !
												5700 container
													5701 text ( 𝑛 + 𝑐 ) !
												5702 text ≥
												5703 text 1
												5704 container
													5705 text 𝜃 ( 𝐵 + 1
													5706 text )
													5707 text 𝐷
												5708 text ≥ 2.
											5709 text (22)
										5710 container
											5711 text During an individual partial release, the weight ratio is at least
											5712 container
												5713 text ( 𝐵 + 1
												5714 text )
												5715 container
													5716 text − 2
											5717 text . Consequently, throughout the at most 
											5718 text 𝐷
											5719 text  partial releases of a single auxiliary, the weight stays at least
										5720 container
											5721 text ( 𝐵 + 1
											5722 text )
											5723 container
												5724 text − 2 𝐷
										5725 text times its weight at the start of that auxiliary’s release. Complete releases increase the weight, so this loss bound holds relative to the initial state of the entire path.
										5726 container
											5727 text The path length is at most 
											5728 container
												5729 text 𝐷 𝐵
											5730 text , and the number of fibre states is at most 
											5731 container
												5732 text ( 𝐵 + 1
												5733 text )
												5734 text 𝑠
											5735 text . Every release transition in 
											5736 container
												5737 text 𝐹 𝑥
											5738 text  has rate at least one when used.
										5739 text The anchored path inequality therefore gives
										5740 container
											5741 container
												5742 container
													5743 text Var ⁡
												5744 container
													5745 text 𝜈 𝑥
												5746 text ℎ ≤ 𝐷 𝐵 ( 𝐵 + 1
												5747 text )
												5748 container
													5749 text 𝑠 + 2 𝐷
												5750 text 𝐸
												5751 container
													5752 text 𝐹 𝑥
												5753 text ( ℎ , ℎ ) .
											5754 text (23)
										5755 text No reciprocal minimum stationary probability enters this gap bound.
										5756 text For the logarithmic initialization cost, (20)–(21) give
										5757 container
											5758 container
												5759 text 𝜈
												5760 text 𝑥
												5761 text ( 𝑎 ) ≥
												5762 text 𝑒
												5763 container
													5764 text − 1
												5765 text ( 𝜃 / 𝐵
												5766 text )
												5767 text 𝐵
												5768 text .
											5769 text (24)
										5770 container
											5771 text Integrating the standard finite reversible 
											5772 container
												5773 text 𝐿 2
											5774 text -to-TV bound yields an explicit sup-norm Poisson-corrector bound. A safely enlarged expression is
										5775 container
											5776 container
												5777 container
													5778 text ∥
													5779 text 𝐹
													5780 text 𝑥
													5781 container
														5782 text − 1
													5783 text ( 𝐼 −
													5784 text Π
													5785 text 𝑥
													5786 text ) ∥
												5787 container
													5788 text ∞ → ∞
												5789 text ≤
												5790 text 𝐶
												5791 text 𝐹
												5792 text ,
												5793 text 𝐶
												5794 text 𝐹
												5795 text = 8 𝐷 ( 𝐵 + 1
												5796 text )
												5797 container
													5798 text 𝑠 + 2 𝐷 + 4
												5799 text 𝜃
												5800 container
													5801 text − 1
												5802 text ,
											5803 text (25)
										5804 container
											5805 text where 
											5806 container
												5807 text Π 𝑥
											5808 text  averages against 
											5809 container
												5810 text 𝜈 𝑥
											5811 text .
										5812 text The actual intermediate estimates only require a logarithm of (24). Replacing that logarithm by a polynomial gives (25).
										5813 heading 5. Exact averaged rates and a finite killed-process averaging bound, Value: 1
											5814 text 5. Exact averaged rates and a finite killed-process averaging bound
										5815 text The following finite stopping is solely analytical. It does not modify the physical network.
										5816 container
											5817 text Stop either process when its decoded total population leaves 
											5818 container
												5819 text { 𝑁 ≤ 𝐵 }
											5820 text , and send it to one absorbing cemetery state. The fast binding process preserves 
											5821 text 𝑁
											5822 text , so it never causes killing. The finite state space can be defined mathematically without being enumerated by the compiler.
										5823 container
											5824 text Let 
											5825 text 𝑆
											5826 text  denote the raw conversion generator. On this stopped state space,
										5827 container
											5828 text 𝑄 = 𝐾 𝐹 + 𝑆 .
										5829 text Every conversion source is empty or one fine molecule, so
										5830 container
											5831 container
												5832 container
													5833 text sup ⁡
												5834 text 𝑢
												5835 text 𝑏
												5836 text 𝑆
												5837 text ( 𝑢 ) ≤ 𝑀 , 𝑀 = 𝑚
												5838 text 𝜃
												5839 container
													5840 text − 1
												5841 text ( 𝐵 + 1 ) .
											5842 text (26)
										5843 container
											5844 text In particular 
											5845 container
												5846 text ∥ 𝑆
												5847 text ∥
												5848 container
													5849 text ∞ → ∞
												5850 text ≤ 2 𝑀
											5851 text .
										5852 heading Exact averaged generator, Value: 3
											5853 text Exact averaged generator
										5854 container
											5855 text For a source complex 
											5856 container
												5857 text 𝑌 𝑟
											5858 text  of order at least two,
										5859 container
											5860 text 𝐸
											5861 container
												5862 text 𝜈 𝑥
											5863 text 𝑎
											5864 container
												5865 text 𝑌 𝑟
											5866 text = 𝜃 ( 𝑥
											5867 text )
											5868 container
												5869 text 𝑌 𝑟
											5870 container
												5871 text 𝑞
												5872 text 𝜃
												5873 text ( 𝑥 −
												5874 text 𝑌
												5875 text 𝑟
												5876 text )
											5877 container
												5878 text 𝑞
												5879 text 𝜃
												5880 text ( 𝑥 )
											5881 text .
										5882 text For a source original species, the corresponding identity is
										5883 container
											5884 text 𝐸
											5885 container
												5886 text 𝜈 𝑥
											5887 text 𝑛
											5888 text 𝑖
											5889 text =
											5890 text 𝑥
											5891 text 𝑖
											5892 container
												5893 text 𝑞
												5894 text 𝜃
												5895 text ( 𝑥 −
												5896 text 𝑒
												5897 text 𝑖
												5898 text )
											5899 container
												5900 text 𝑞
												5901 text 𝜃
												5902 text ( 𝑥 )
											5903 text .
										5904 text Thus the exact averaged rate is
										5905 container
											5906 container
												5907 container
													5908 text 𝑞 ‾
												5909 text 𝑟
												5910 text ( 𝑥 ) =
												5911 text 𝜅
												5912 text 𝑟
												5913 text ( 𝑥
												5914 text )
												5915 container
													5916 text 𝑌 𝑟
												5917 container
													5918 text 𝑞
													5919 text 𝜃
													5920 text ( 𝑥 −
													5921 text 𝑌
													5922 text 𝑟
													5923 text )
												5924 container
													5925 text 𝑞
													5926 text 𝜃
													5927 text ( 𝑥 )
												5928 text .
											5929 text (27)
										5930 text The formula includes source orders zero and one with the natural conventions.
										5931 container
											5932 text Since 
											5933 container
												5934 text 𝑞 𝜃
											5935 text  is coordinatewise nondecreasing,
										5936 container
											5937 text 0 ≤ 1 −
											5938 container
												5939 text 𝑞
												5940 text 𝜃
												5941 text ( 𝑥 −
												5942 text 𝑌
												5943 text 𝑟
												5944 text )
											5945 container
												5946 text 𝑞
												5947 text 𝜃
												5948 text ( 𝑥 )
											5949 text ≤
											5950 text 𝑞
											5951 text 𝜃
											5952 text ( 𝑥 ) − 1 ≤ 2 𝑠 𝜃 ( 𝐵 + 1
											5953 text )
											5954 text 𝐷
											5955 text .
										5956 container
											5957 text Therefore, if 
											5958 container
												5959 text 𝑄
												5960 text h
												5961 text i
												5962 text g
												5963 text h
												5964 text 𝐵
											5965 text  is the original higher-molecularity process killed at the same boundary,
										5966 container
											5967 container
												5968 text ∥
												5969 container
													5970 text 𝑄 ‾
												5971 text 𝐵
												5972 text −
												5973 text 𝑄
												5974 container
													5975 text h i g h
												5976 text 𝐵
												5977 text ∥
												5978 container
													5979 text ∞ → ∞
												5980 text ≤ 4 𝑠 𝑚 𝜃 ( 𝐵 + 1
												5981 text )
												5982 container
													5983 text 2 𝐷
												5984 text .
											5985 text (28)
										5986 text This also accounts for boundary-killing rates.
										5987 heading Averaging error, Value: 3
											5988 text Averaging error
										5989 container
											5990 text Let 
											5991 text 𝑈
											5992 text  embed decoded functions as functions constant on each fibre, and let 
											5993 text Π
											5994 text  be fibre averaging. For a bounded decoded test function 
											5995 text 𝑔
											5996 text , set
										5997 container
											5998 text 𝑓
											5999 text 𝑠
											6000 text = 𝑈
											6001 text 𝑒
											6002 container
												6003 text ( 𝑇 − 𝑠 )
												6004 container
													6005 text 𝑄 ‾
												6006 text 𝐵
											6007 text 𝑔 ,
											6008 text ℎ
											6009 text 𝑠
											6010 text = ( 𝐼 − Π ) 𝑆
											6011 text 𝑓
											6012 text 𝑠
											6013 text .
										6014 container
											6015 text For 
											6016 container
												6017 text ∥ 𝑔
												6018 text ∥
												6019 text ∞
												6020 text ≤ 1
											6021 text ,
										6022 container
											6023 text ∥
											6024 text ℎ
											6025 text 𝑠
											6026 text ∥
											6027 text ∞
											6028 text ≤ 4 𝑀 , ∥
											6029 text ∂
											6030 text 𝑠
											6031 text ℎ
											6032 text 𝑠
											6033 text ∥
											6034 text ∞
											6035 text ≤ 8
											6036 text 𝑀
											6037 text 2
											6038 text .
										6039 container
											6040 text Choose 
											6041 container
												6042 text 𝜒 𝑠
											6043 text  solving 
											6044 container
												6045 text 𝐹
												6046 text 𝜒
												6047 text 𝑠
												6048 text =
												6049 text ℎ
												6050 text 𝑠
											6051 text , with zero fibre means. From (25),
										6052 container
											6053 text ∥
											6054 text 𝜒
											6055 text 𝑠
											6056 text ∥
											6057 text ∞
											6058 text ≤ 4
											6059 text 𝐶
											6060 text 𝐹
											6061 text 𝑀 , ∥
											6062 text ∂
											6063 text 𝑠
											6064 text 𝜒
											6065 text 𝑠
											6066 text ∥
											6067 text ∞
											6068 text ≤ 8
											6069 text 𝐶
											6070 text 𝐹
											6071 text 𝑀
											6072 text 2
											6073 text , ∥ 𝑆
											6074 text 𝜒
											6075 text 𝑠
											6076 text ∥
											6077 text ∞
											6078 text ≤ 8
											6079 text 𝐶
											6080 text 𝐹
											6081 text 𝑀
											6082 text 2
											6083 text .
										6084 text Dynkin’s formula, including the absorbing cemetery state, gives
										6085 container
											6086 container
												6087 text ∣
												6088 text 𝐸
												6089 text 𝑔
												6090 text (
												6091 container
													6092 text 𝐷
													6093 text d
													6094 text e
													6095 text c
												6096 container
													6097 text 𝑍 𝑇 𝐵
												6098 text )
												6099 text −
												6100 text 𝐸
												6101 text 𝑔
												6102 text (
												6103 container
													6104 text 𝑋
													6105 text ‾
													6106 text 𝑇 𝐵
												6107 text )
												6108 text ∣
												6109 text ≤
												6110 container
													6111 text 8
													6112 text 𝐶
													6113 text 𝐹
													6114 text ( 𝑀 + 2 𝑇
													6115 text 𝑀
													6116 text 2
													6117 text )
												6118 text 𝐾
												6119 text .
											6120 text (29)
										6121 text The initial fine state may be canonical; it need not be equilibrated in its fibre. The endpoint corrector terms already account for initialization.
										6122 container
											6123 text For an absolute first-moment test, take 
											6124 container
												6125 text 𝑔 ( 𝑥 ) =
												6126 text 𝑥
												6127 text 𝑖
											6128 text  inside the finite region and zero at the cemetery state. Its sup norm is at most 
											6129 text 𝐵
											6130 text , so (28)–(29) incur only an additional factor 
											6131 text 𝐵
											6132 text .
										6133 heading 6. Resolving the apparent circularity in , and the exit estimate, Value: 1
											6134 text 6. Resolving the apparent circularity in 
											6135 container
												6136 text 𝐵 , 𝜃
											6137 text , and the exit estimate
										6138 text Here is one explicit choice showing that all powers can be fixed in advance.
										6139 text Let
										6140 container
											6141 text ℎ = 𝑝 + 4 𝐷 + 16 , 𝐴 = 128 𝑠 𝑚 .
										6142 text Set
										6143 container
											6144 container
												6145 text 𝐵 =
												6146 text ⌈
												6147 container
													6148 text 𝐶 𝐵
												6149 container
													6150 text 𝑊 4
												6151 text ⌉
												6152 text ,
											6153 text (30)
										6154 text and
										6155 container
											6156 container
												6157 text 𝜃 =
												6158 text 𝜖
												6159 container
													6160 text 𝐴 (
													6161 text 𝑇
													6162 text 0
													6163 text + 1 ) ( 𝐵 + 1
													6164 text )
													6165 container
														6166 text 2 𝐷 + 1
												6167 text .
											6168 text (31)
										6169 text Then set
										6170 container
											6171 container
												6172 text 𝐾 = 1 +
												6173 container
													6174 text 1024
													6175 text 𝐶
													6176 text 𝐹
													6177 text ( 𝐵 + 1 ) ( 𝑀 + 2
													6178 text 𝑇
													6179 text 0
													6180 text 𝑀
													6181 text 2
													6182 text )
												6183 text 𝜖
												6184 text .
											6185 text (32)
										6186 container
											6187 text Here 
											6188 container
												6189 text 𝐶
												6190 text 𝐹
												6191 text , 𝑀
											6192 text  are the explicit expressions in (25)–(26).
										6193 container
											6194 text The constant 
											6195 container
												6196 text 𝐶 𝐵
											6197 text  can be selected entirely from fixed data. For completeness, one sufficient recipe is the following.
										6198 text Define
										6199 container
											6200 text 𝐶
											6201 text 2
											6202 text = 900
											6203 text 𝐷
											6204 text 2
											6205 text ,
										6206 container
											6207 text 𝐾
											6208 container
												6209 text f i n e
											6210 text = 𝐴 𝑚 𝐶 ( 𝐶 + 1 )
											6211 text 2
											6212 container
												6213 text ℎ + 2 𝐷
											6214 text 𝐹
											6215 text ℎ
											6216 text ,
										6217 container
											6218 text 𝐾
											6219 container
												6220 text h i g h
											6221 text = 𝐶 𝑚
											6222 text 2
											6223 container
												6224 text ℎ − 𝐷
											6225 text 𝐹
											6226 text ℎ
											6227 text .
										6228 container
											6229 text Choose an integer 
											6230 container
												6231 text 𝐶 𝐵
											6232 text  at least
										6233 container
											6234 container
												6235 text max ⁡  ⁣
												6236 text {
												6237 text 16
												6238 text 𝐷
												6239 text (
												6240 text 𝐷
												6241 text +
												6242 text 1
												6243 text )
												6244 text ,
												6245 text 4
												6246 text 𝐷
												6247 text ,
												6248 text 1
												6249 text ,
												6250 container
													6251 text 2 20
												6252 text (
												6253 text 1
												6254 text +
												6255 container
													6256 text 𝐶 2
												6257 text )
												6258 text (
												6259 container
													6260 text 𝐾
													6261 text f
													6262 text i
													6263 text n
													6264 text e
												6265 text +
												6266 container
													6267 text 𝐾
													6268 text h
													6269 text i
													6270 text g
													6271 text h
												6272 text +
												6273 text 1
												6274 text )
												6275 text }
												6276 text .
											6277 text (33)
										6278 text These constants are deliberately loose.
										6279 heading Fine exit probability, Value: 3
											6280 text Fine exit probability
										6281 container
											6282 text The decoded total population changes only at conversion firings. Its jump size is at most 
											6283 container
												6284 text 2 𝐷
											6285 text , and its conversion intensity is at most
										6286 container
											6287 text 𝑚
											6288 text 𝜃
											6289 container
												6290 text − 1
											6291 text ( 𝑁 + 1 ) .
										6292 text Consequently, the all-time moment bound (19) gives
										6293 container
											6294 container
												6295 container
													6296 text 𝑃 (
													6297 text 𝜏
													6298 text 𝐵
													6299 container
														6300 text f i n e
													6301 text ≤
													6302 text 𝑇
													6303 text 0
													6304 text )
												6305 container
													6306 text ≤
													6307 text 𝑇
													6308 text 0
													6309 text 𝑚
													6310 text 𝜃
													6311 container
														6312 text − 1
													6313 container
														6314 text (
														6315 text 2
														6316 text 𝐵
														6317 text )
													6318 container
														6319 text ℎ − 1
													6320 text 𝐹
													6321 text ℎ
													6322 text 𝑊
													6323 container
														6324 text 2 ℎ
												6325 container
													6326 text ≤
													6327 text 𝐾
													6328 container
														6329 text f i n e
													6330 text 𝑊
													6331 container
														6332 text 2 𝑝 + 1 + 2 ℎ
													6333 text 𝐵
													6334 container
														6335 text 2 𝐷 + 2 − ℎ
												6336 container
													6337 text ≤
													6338 text 𝐾
													6339 container
														6340 text f i n e
													6341 text 𝐶
													6342 text 𝐵
													6343 container
														6344 text 2 𝐷 + 2 − ℎ
													6345 text 𝑊
													6346 container
														6347 text − 23
													6348 text .
											6349 text (34)
										6350 container
											6351 text The exponent 
											6352 container
												6353 text − 23
											6354 text  comes from
										6355 container
											6356 text 2 𝑝 + 1 + 2 ℎ + 4 ( 2 𝐷 + 2 − ℎ ) = 2 𝑝 + 8 𝐷 + 9 − 2 ℎ = − 23.
										6357 container
											6358 text Thus decreasing 
											6359 text 𝜃
											6360 text  when 
											6361 text 𝐵
											6362 text  grows does not invalidate the tail estimate. The fixed high moment 
											6363 text ℎ
											6364 text  pays for it.
										6365 heading Original exit probability, Value: 3
											6366 text Original exit probability
										6367 container
											6368 text The higher-molecularity total intensity is at most 
											6369 container
												6370 text 𝑚 ( 𝑁 + 1
												6371 text )
												6372 text 𝐷
											6373 text , so
										6374 container
											6375 container
												6376 text 𝑃 (
												6377 text 𝜏
												6378 text 𝐵
												6379 container
													6380 text h i g h
												6381 text ≤
												6382 text 𝑇
												6383 text 0
												6384 text ) ≤
												6385 text 𝐾
												6386 container
													6387 text h i g h
												6388 text 𝐶
												6389 text 𝐵
												6390 container
													6391 text 𝐷 − ℎ
												6392 text 𝑊
												6393 container
													6394 text 𝑝 + 4 𝐷 − 2 ℎ
												6395 text ,
											6396 text (35)
										6397 container
											6398 text which decays even faster than 
											6399 container
												6400 text 𝑊
												6401 text −
												6402 text 23
											6403 text .
										6404 text With (33), both exit probabilities are bounded by
										6405 container
											6406 container
												6407 container
													6408 text 𝑊
													6409 text −
													6410 text 23
												6411 container
													6412 text 2
													6413 text 20
													6414 text ( 1 +
													6415 text 𝐶
													6416 text 2
													6417 text )
												6418 text .
											6419 text (36)
										6420 text For absolute endpoint means, Cauchy–Schwarz and (18) give
										6421 container
											6422 container
												6423 text 𝐸
												6424 text [
												6425 text 𝑁
												6426 text (
												6427 container
													6428 text 𝑍
													6429 text 𝑇
													6430 text 0
												6431 text )
												6432 container
													6433 text 1
													6434 text {
													6435 container
														6436 text 𝜏 𝐵
													6437 text ≤
													6438 container
														6439 text 𝑇 0
													6440 text }
												6441 text ]
												6442 text ≤
												6443 container
													6444 text 𝐶 2
												6445 text 𝑊
												6446 text 2
												6447 container
													6448 text 𝑃 (
													6449 text 𝜏
													6450 text 𝐵
													6451 text ≤
													6452 text 𝑇
													6453 text 0
													6454 text )
												6455 text ≤
												6456 text 𝜖
												6457 text 1024
												6458 text .
											6459 text (37)
										6460 text This pays for trajectories which leave and later re-enter the finite region as well.
										6461 heading Combining the comparisons, Value: 3
											6462 text Combining the comparisons
										6463 container
											6464 text From (28) and (31), the killed averaged process and killed original process differ on a coordinate-mean test by at most 
											6465 container
												6466 text 𝜖 / 32
											6467 text .
										6468 container
											6469 text From (29) and (32), the killed fine process and killed averaged process differ on such a test by at most 
											6470 container
												6471 text 𝜖 / 128
											6472 text .
										6473 container
											6474 text The original process has target error at most 
											6475 container
												6476 text 𝜖 / 16
											6477 text , and the two stopping errors are bounded by (37). Their sum is less than 
											6478 container
												6479 text 𝜖 / 8
											6480 text . The TV bound is at least as easy.
										6481 container
											6482 text Thus the actual untruncated  nominal  fine process satisfies
										6483 container
											6484 container
												6485 text ∥ 𝐿 (
												6486 text 𝐷
												6487 container
													6488 text d e c
												6489 text 𝑍
												6490 container
													6491 text 𝑇 0
												6492 text ) −
												6493 text 𝜋
												6494 text 𝜆
												6495 text ∥
											6496 container
												6497 text T V
											6498 text <
											6499 text 𝜖
											6500 text 8
											6501 text ,
										6502 text and
										6503 container
											6504 container
												6505 container
													6506 text max ⁡
												6507 text 𝑖
												6508 text ∣
												6509 text 𝐸
												6510 text (
												6511 container
													6512 text 𝐷
													6513 text d
													6514 text e
													6515 text c
												6516 container
													6517 text 𝑍
													6518 text 𝑇
													6519 text 0
												6520 container
													6521 text ) 𝑖
												6522 text −
												6523 container
													6524 text 𝐸 𝜋
												6525 container
													6526 text 𝑋 𝑖
												6527 text ∣
												6528 text <
												6529 text 𝜖
												6530 text 8
												6531 text ,
											6532 text (38)
										6533 text in raw time.
										6534 heading 7. Rate normalization and all nominal resource costs, Value: 1
											6535 text 7. Rate normalization and all nominal resource costs
										6536 container
											6537 text Equation (32) ensures 
											6538 container
												6539 text 𝐾 ≥
												6540 text 𝜃
												6541 container
													6542 text − 1
											6543 text . Since 
											6544 container
												6545 text 𝜅
												6546 text 𝑟
												6547 text ≤ 1
											6548 text , every raw channel rate constant is at most 
											6549 text 𝐾
											6550 text .
										6551 container
											6552 text Divide all rates by 
											6553 text 𝐾
											6554 text , and output physical time
										6555 container
											6556 container
												6557 text 𝑇 = 𝐾
												6558 text 𝑇
												6559 text 0
												6560 text .
											6561 text (39)
										6562 text The resulting constants are all at most one. Their reciprocals are bounded by
										6563 container
											6564 text max ⁡ {
											6565 text 𝜃
											6566 container
												6567 text − 1
											6568 text , 𝐾
											6569 container
												6570 text max ⁡
											6571 text 𝑟
											6572 text 𝜅
											6573 text 𝑟
											6574 container
												6575 text − 1
											6576 text } ,
										6577 container
											6578 text which is polynomial in 
											6579 text 𝑊
											6580 text .
										6581 container
											6582 text The total number of fine channels is 
											6583 container
												6584 text 2 𝑠 + 𝑚
											6585 text . Every raw intensity is at most 
											6586 container
												6587 text 𝐾 ( 𝑁 + 1
												6588 text )
												6589 text 2
											6590 text , including null, binding, release, and parallel firings. Therefore the expected actual firing count by raw time 
											6591 container
												6592 text 𝑇 0
											6593 text , equivalently physical time 
											6594 container
												6595 text 𝐾
												6596 text 𝑇
												6597 text 0
											6598 text , is at most
										6599 container
											6600 container
												6601 text ( 2 𝑠 + 𝑚 ) 𝐾
												6602 text 𝑇
												6603 text 0
												6604 text 𝐹
												6605 text 2
												6606 text 𝑊
												6607 text 4
												6608 text .
											6609 text (40)
										6610 text Every such firing is counted.
										6611 text The population bounds are even stronger than needed:
										6612 container
											6613 container
												6614 container
													6615 text sup ⁡
												6616 container
													6617 text 𝑡 ≥ 0
												6618 text 𝐸 ∣
												6619 text 𝑍
												6620 text 𝑡
												6621 text ∣
												6622 text 1
												6623 text ≤ 45 𝐷
												6624 text 𝑊
												6625 text 2
												6626 text ,
												6627 text 𝐸
												6628 text 𝜇
												6629 text ∣ 𝑍
												6630 text ∣
												6631 text 1
												6632 text ≤ 45 𝐷
												6633 text 𝑊
												6634 text 2
												6635 text .
											6636 text (41)
										6637 text A crude numerical exponent read off from these formulas is:
										6638 container
											6639 text 𝜃
											6640 container
												6641 text − 1
											6642 text =
											6643 text 𝑂
											6644 text 𝑅
											6645 text (
											6646 text 𝑊
											6647 container
												6648 text 𝑝 + 8 𝐷 + 5
											6649 text ) ,
										6650 container
											6651 text 𝐾 =
											6652 text 𝑂
											6653 text 𝑅
											6654 text (
											6655 text 𝑊
											6656 container
												6657 text 4 𝑝 + 4 𝑠 + 32 𝐷 + 44
											6658 text ) ,
										6659 container
											6660 text 𝑇 ,
											6661 container
												6662 text max ⁡
											6663 text 𝑒
											6664 text 𝑘
											6665 text 𝑒
											6666 container
												6667 text − 1
											6668 text =
											6669 text 𝑂
											6670 text 𝑅
											6671 text (
											6672 text 𝑊
											6673 container
												6674 text 5 𝑝 + 4 𝑠 + 32 𝐷 + 44
											6675 text ) ,
										6676 container
											6677 container
												6678 text 𝐸 [ all firings through  𝑇 ] =
												6679 text 𝑂
												6680 text 𝑅
												6681 text (
												6682 text 𝑊
												6683 container
													6684 text 5 𝑝 + 4 𝑠 + 32 𝐷 + 48
												6685 text ) .
											6686 text (42)
										6687 text The compiler never enumerates the ball, fibres, communicating class, or a finite generator. It evaluates fixed-degree rational formulas. Their binary lengths are polynomial in the input length and the accepted compiler’s output lengths. Fixed preprocessing constants in (33) are explicit and computable from the accepted constants and fixed network.
										6688 heading Nonexplosion, Value: 3
											6689 text Nonexplosion
										6690 text There is also a simple general fact:
										6691 text Any finite mass-action network with at most two reactants and at most two products per channel is nonexplosive for every finite positive rate vector.
										6692 container
											6693 text The total fine molecule count can increase only through zero-order or first-order channels. Its upward rate is bounded by 
											6694 container
												6695 text 𝐶 ( 1 + ∣ 𝑍
												6696 text ∣
												6697 text 1
												6698 text )
											6699 text , so it is dominated by a linear immigration–birth process. At bounded total population there are finitely many states and bounded total firing rate, including null channels.
										6700 text For the nominal process, the complex-balanced product form is finite, has finite exit-rate mean, and is supported on the irreducible class (2). Hence nominal positive recurrence and uniqueness follow.
										6701 heading 8. Exact absorption of binding-rate errors, Value: 1
											6702 text 8. Exact absorption of binding-rate errors
										6703 text The parent’s proposed absorption lemma is valid.
										6704 container
											6705 text Let every binding/release constant be independently perturbed by a factor in 
											6706 container
												6707 text [ 1 − 𝛿 , 1 + 𝛿 ]
											6708 text , and put
										6709 container
											6710 text 𝜌 =
											6711 container
												6712 text 1 + 𝛿
											6713 container
												6714 text 1 − 𝛿
											6715 text .
										6716 container
											6717 text Keep the original species activities at 
											6718 container
												6719 text 𝜆 𝑖
											6720 text . Define each prefix activity recursively from its unique assembly parent:
										6721 container
											6722 container
												6723 text 𝑐
												6724 text 𝑃
												6725 text ′
												6726 text =
												6727 container
													6728 text 𝑘
													6729 text ~
													6730 text b
													6731 text i
													6732 text n
													6733 text d
												6734 container
													6735 text 𝑘
													6736 text ~
													6737 text r
													6738 text e
													6739 text l
													6740 text e
													6741 text a
													6742 text s
													6743 text e
												6744 text 𝑐
												6745 container
													6746 text p a r e n t
												6747 text ′
												6748 text 𝜆
												6749 text 𝑖
												6750 text .
											6751 text (43)
										6752 container
											6753 text For the first prefix, use the product of the corresponding two original activities. Then every perturbed binding/release pair is  exactly detailed balanced  at 
											6754 container
												6755 text 𝑐 ′
											6756 text .
										6757 container
											6758 text For a prefix of order at most 
											6759 text 𝐷
											6760 text ,
										6761 container
											6762 container
												6763 text 𝜌
												6764 container
													6765 text − ( 𝐷 − 1 )
												6766 text ≤
												6767 container
													6768 text 𝑐 𝑃 ′
												6769 container
													6770 text 𝜃
													6771 text 𝜆
													6772 container
														6773 text 𝑐 𝑃
												6774 text ≤
												6775 text 𝜌
												6776 container
													6777 text 𝐷 − 1
												6778 text .
											6779 text (44)
										6780 text Now define reference conversion constants by preserving the nominal complex flux:
										6781 container
											6782 container
												6783 text 𝑘
												6784 text 𝑟
												6785 container
													6786 text r e f
												6787 text =
												6788 text 𝑘
												6789 text 𝑟
												6790 container
													6791 text n o m
												6792 container
													6793 text 𝑐
													6794 text rep
													6795 text ⁡
													6796 text (
													6797 container
														6798 text 𝑌 𝑟
													6799 text )
													6800 text n
													6801 text o
													6802 text m
												6803 container
													6804 text 𝑐
													6805 text rep
													6806 text ⁡
													6807 text (
													6808 container
														6809 text 𝑌 𝑟
													6810 text )
													6811 text ′
												6812 text .
											6813 text (45)
										6814 text For empty or original-species sources, the ratio is one.
										6815 container
											6816 text The reference process uses the  actual perturbed binding constants  and the conversion constants (45). It is exactly complex balanced at 
											6817 container
												6818 text 𝑐 ′
											6819 text .
										6820 text The actual conversion constants satisfy
										6821 container
											6822 container
												6823 text 𝜌
												6824 container
													6825 text − 𝐷
												6826 text ≤
												6827 container
													6828 text 𝑘
													6829 text ~
													6830 text 𝑟
												6831 container
													6832 text 𝑘 𝑟
													6833 text r
													6834 text e
													6835 text f
												6836 text ≤
												6837 text 𝜌
												6838 text 𝐷
												6839 text .
											6840 text (46)
										6841 container
											6842 text For 
											6843 container
												6844 text 𝛿 ≤ 1 / ( 8 𝐷 )
											6845 text , their relative difference is at most 
											6846 container
												6847 text 8 𝐷 𝛿
											6848 text .
										6849 container
											6850 text The reference decoded weight is the same 
											6851 text 𝑞
											6852 text -formula with coefficients 
											6853 container
												6854 text 𝜃
												6855 text 𝑟
												6856 text 𝑗
											6857 text , where 
											6858 container
												6859 text 𝑟
												6860 text 𝑗
												6861 text ∈ [
												6862 text 𝜌
												6863 container
													6864 text − 𝐷
												6865 text ,
												6866 text 𝜌
												6867 text 𝐷
												6868 text ]
											6869 text . These coefficients are within a factor two of 
											6870 text 𝜃
											6871 text . All static and moment estimates above extend after fixed enlargements of constants.
										6872 container
											6873 text The bounded-fibre release proof also extends: endpoint weights gain at least 
											6874 container
												6875 text 1 / [ 2 𝜃 ( 𝐵 + 1
												6876 text )
												6877 text 𝐷
												6878 text ]
											6879 text , intermediate ratios lose only another fixed factor per prefix step, and perturbed release rates are at least half nominal. A fixed factor 
											6880 container
												6881 text 2
												6882 text 𝑂
												6883 text (
												6884 text 𝐷
												6885 text )
											6886 text  in 
											6887 container
												6888 text 𝐶 𝐹
											6889 text  and 
											6890 text 𝐾
											6891 text  suffices. The exact averaged reference rates retain (27), with the adjusted 
											6892 text 𝑞
											6893 text , because the factor 
											6894 container
												6895 text 𝑐 𝑃 ′
											6896 text  cancels against (45).
										6897 heading 9. A further finite-horizon robust estimate, Value: 1
											6898 text 9. A further finite-horizon robust estimate
										6899 text This is a useful strengthening, but it does not solve the stationary problem.
										6900 text After the absorption above, actual and reference processes have identical binding reactions and differ only in conversion multipliers
										6901 container
											6902 text 𝑟
											6903 text 𝑒
											6904 text =
											6905 container
												6906 text 𝑘 ~
											6907 text 𝑒
											6908 text /
											6909 text 𝑘
											6910 text 𝑒
											6911 container
												6912 text r e f
											6913 text , ∣
											6914 text 𝑟
											6915 text 𝑒
											6916 text − 1 ∣ ≤ 𝜂 , 𝜂 ≤ 8 𝐷 𝛿 .
										6917 text Their reference conversion activity satisfies
										6918 container
											6919 container
												6920 text 𝑏
												6921 container
													6922 text r e f
												6923 text ( 𝑢 ) ≤
												6924 text 𝐶
												6925 text 𝑅
												6926 text 𝜃
												6927 container
													6928 text − 1
												6929 text ( 𝑁 ( 𝑢 ) + 1 ) .
											6930 text (47)
										6931 container
											6932 text Let 
											6933 container
												6934 text 𝑅 𝑡
											6935 text  be the marked-path likelihood of the actual process relative to the reference. Both are nonexplosive by the elementary-network argument.
										6936 text A counting-process exponential-martingale calculation gives
										6937 container
											6938 container
												6939 text 𝐸
												6940 container
													6941 text r e f
												6942 text 𝑅
												6943 text 𝑡
												6944 text 2
												6945 text ≤
												6946 container
													6947 text [
													6948 text 𝐸
													6949 container
														6950 text r e f
													6951 text exp ⁡  ⁣
													6952 text (
													6953 text 11
													6954 container
														6955 text 𝜂 2
													6956 container
														6957 text ∫ 0 𝑡
													6958 container
														6959 text 𝑏
														6960 text r
														6961 text e
														6962 text f
													6963 text (
													6964 container
														6965 text 𝑍 𝑠
													6966 text )
													6967 text 𝑑
													6968 text 𝑠
													6969 text )
													6970 text ]
												6971 container
													6972 text 1 / 2
												6973 text .
											6974 text (48)
										6975 container
											6976 text To verify the coefficient: write 
											6977 container
												6978 text 𝑅 𝑡 2
											6979 text  as the square root of the exponential local martingale with rate multiplier 
											6980 container
												6981 text 𝑟 𝑒 4
											6982 text , times the compensator exponential. Cauchy–Schwarz and
										6983 container
											6984 text 𝑟
											6985 text 4
											6986 text − 1 − 4 ( 𝑟 − 1 ) = 6 ( 𝑟 − 1
											6987 text )
											6988 text 2
											6989 text + 4 ( 𝑟 − 1
											6990 text )
											6991 text 3
											6992 text + ( 𝑟 − 1
											6993 text )
											6994 text 4
											6995 text ≤ 11
											6996 text 𝜂
											6997 text 2
										6998 text give (48).
										6999 container
											7000 text The near-
											7001 container
												7002 text 𝐿 1
											7003 text  argument above gives uniformly in reference time
										7004 container
											7005 container
												7006 text 𝐸
												7007 container
													7008 text r e f
												7009 text 𝑒
												7010 container
													7011 text 𝑎 ( 𝑁 + 1 )
												7012 text ≤ 1 +
												7013 text 𝐶
												7014 text 𝑅
												7015 text 𝑎
												7016 text 𝑊
												7017 text 2
												7018 text , 0 ≤ 𝑎 ≤
												7019 text 1
												7020 container
													7021 text 2 𝐷 𝑞
												7022 text .
											7023 text (49)
										7024 container
											7025 text For example, differentiate the exponential and use Hölder plus the remaining half of the exponential-moment budget to bound
											7026 container
												7027 text 𝐸 [ ( 𝑁 + 1 )
												7028 text 𝑒
												7029 container
													7030 text 𝑎 ( 𝑁 + 1 )
												7031 text ] ≤
												7032 text 𝐶
												7033 text 𝑅
												7034 text 𝐷 𝑞
											7035 text .
										7036 container
											7037 text Jensen in time, (47)–(49), and 
											7038 container
												7039 text 𝑞 = 𝑂 (
												7040 text 𝑊
												7041 text 2
												7042 text )
											7043 text  imply, provided
										7044 container
											7045 text 𝜂
											7046 text 2
											7047 text 𝑇
											7048 text 0
											7049 text 𝜃
											7050 container
												7051 text − 1
											7052 text ≤
											7053 text 𝑐
											7054 text 𝑅
											7055 text 𝑊
											7056 container
												7057 text − 2
											7058 text ,
										7059 text that
										7060 container
											7061 container
												7062 text 𝐸
												7063 container
													7064 text r e f
												7065 text (
												7066 text 𝑅
												7067 text 𝑡
												7068 text − 1
												7069 text )
												7070 text 2
												7071 text ≤
												7072 text 𝐶
												7073 text 𝑅
												7074 text 𝜂
												7075 text 2
												7076 text 𝑇
												7077 text 0
												7078 text 𝜃
												7079 container
													7080 text − 1
												7081 text 𝑊
												7082 text 2
												7083 text , 0 ≤ 𝑡 ≤
												7084 text 𝑇
												7085 text 0
												7086 text .
											7087 text (50)
										7088 text Consequently,
										7089 container
											7090 container
												7091 text ∥
												7092 text 𝐿
												7093 container
													7094 text a c t
												7095 text (
												7096 text 𝐷
												7097 container
													7098 text d e c
												7099 text 𝑍
												7100 text 𝑡
												7101 text ) −
												7102 text 𝐿
												7103 container
													7104 text r e f
												7105 text (
												7106 text 𝐷
												7107 container
													7108 text d e c
												7109 text 𝑍
												7110 text 𝑡
												7111 text )
												7112 text ∥
												7113 container
													7114 text T V
												7115 text ≤
												7116 text 𝐶
												7117 text 𝑅
												7118 text 𝜂
												7119 container
													7120 text 𝑇
													7121 text 0
													7122 text 𝜃
													7123 container
														7124 text − 1
												7125 text 𝑊 ,
											7126 text (51)
										7127 text and
										7128 container
											7129 container
												7130 container
													7131 text max ⁡
												7132 text 𝑖
												7133 text ∣
												7134 text 𝐸
												7135 container
													7136 text a c t
												7137 text (
												7138 text 𝐷
												7139 container
													7140 text d e c
												7141 text 𝑍
												7142 text 𝑡
												7143 text )
												7144 text 𝑖
												7145 text −
												7146 text 𝐸
												7147 container
													7148 text r e f
												7149 text (
												7150 text 𝐷
												7151 container
													7152 text d e c
												7153 text 𝑍
												7154 text 𝑡
												7155 text )
												7156 text 𝑖
												7157 text ∣ ≤
												7158 text 𝐶
												7159 text 𝑅
												7160 text 𝜂
												7161 container
													7162 text 𝑇
													7163 text 0
													7164 text 𝜃
													7165 container
														7166 text − 1
												7167 text 𝑊
												7168 text 3
												7169 text .
											7170 text (52)
										7171 text Choosing, for example,
										7172 container
											7173 container
												7174 text 𝜂 ≤
												7175 container
													7176 text 𝜖 𝜃
												7177 container
													7178 text 𝐶
													7179 text 𝑅
													7180 text (
													7181 text 𝑇
													7182 text 0
													7183 text + 1 )
													7184 text 𝑊
													7185 text 3
											7186 text (53)
										7187 text is a rational polynomial numerical tolerance and safely pays these estimates.
										7188 container
											7189 text Moreover, Hölder with (48) and the reference 
											7190 container
												7191 text 2 ℎ
											7192 text -moment bound gives actual moments
										7193 container
											7194 container
												7195 container
													7196 text sup ⁡
												7197 container
													7198 text 0 ≤ 𝑡 ≤
													7199 text 𝑇
													7200 text 0
												7201 text 𝐸
												7202 container
													7203 text a c t
												7204 text 𝑁 (
												7205 text 𝑍
												7206 text 𝑡
												7207 text )
												7208 text ℎ
												7209 text ≤
												7210 text 𝐶
												7211 container
													7212 text 𝑅 , ℎ
												7213 text 𝑊
												7214 container
													7215 text 2 ℎ
												7216 text .
											7217 text (54)
										7218 text Thus actual transient population bounds and all actual firing counts through the compiled time remain polynomial uniformly over admitted errors.
										7219 container
											7220 text This is a finite-horizon statement. Its permitted 
											7221 text 𝜂
											7222 text  depends on 
											7223 container
												7224 text 𝑇 0
											7225 text ; it cannot be sent to arbitrary time with a fixed nonzero tolerance.
										7226 heading Remaining obstacle, Value: 2
											7227 text Remaining obstacle
										7228 container
											7229 text The preceding estimates do  not  prove that every admitted perturbed process is positive recurrent, or that its stationary decoded law and moments are close to the target.
										7230 text After exact binding-error absorption, the unresolved analytic step can be stated sharply:
										7231 text Establish a quantitative infinite-class recurrence/stationary perturbation theorem for the complex-balanced prefix reference process under small independent errors in its unary/zero-source conversion rates.
										7232 text The perturbation acts through conversion activity
										7233 container
											7234 text 𝑏
											7235 container
												7236 text c o n v
											7237 text ( 𝑢 ) ≤
											7238 text 𝐶
											7239 text 𝑅
											7240 text 𝜃
											7241 container
												7242 text − 1
											7243 text ( 1 + 𝑁 ( 𝑢 ) ) ,
										7244 container
											7245 text so an  all-firing  weighted Poincaré inequality is unnecessary. A suitable conversion-activity weighted inequality would suffice for the usual form-perturbation route.
										7246 container
											7247 text However, the bounded-fibre argument above cannot simply be continued to infinity. At large decoded populations, 
											7248 container
												7249 text 𝜃 ( 𝐵 + 1
												7250 text )
												7251 text 𝐷
											7252 text  is no longer small, and the canonical point may have exponentially small conditional fibre weight 
											7253 container
												7254 text 𝑞
												7255 text 𝜃
												7256 text ( 𝑥
												7257 text )
												7258 container
													7259 text − 1
											7260 text . Anchoring all fibres to the canonical state would therefore be invalid. A global proof needs fibre averages, a different recurrence argument, or a redesigned elementary lift.
										7261 text Accordingly, the full universal robust statement remains unresolved by this work, but the nominal infinite-class compiler and polynomial finite-horizon robustness have concrete quantitative proofs rather than only qualitative small-parameter limits.
		2356 