# P3: completed predictable-fault return

Chat: https://chatgpt.com/c/6af3030c-e834-83ec-b294-ad6a7f60aa46
Current user: 0f02b21e-c0d6-4f41-acb1-10513c571f19; final: 7c7cc6f0-a58a-5494-bcf9-9809ac9d902e. UI showed Pro and an idle composer.
Exact issued prompt: work/astra-renewed-pro-programmes-20261103/P3_FULL_ELEMENTARY_PREDICTABLE_FAULT_UNIFORM_TIME_COMPILER_PRO_20261111.txt; SHA-256 ce18a6abb49f212e4ec4d7df789dbb5517eac76709e912abf8e5a538b2fd983c.
Final is the complete available UI-copied Markdown, not a literal database-byte claim. Current expanded activity and available current helper panels follow; accessibility math may fragment or repeat. Stationary obstructions reported no final response available. Earlier chat-wide panels are in P3_PRO_D257E8_STATIONARY_ROBUSTNESS_RETURN_20261111.md. No ZIP or output file appeared in the current visible response; availability elsewhere is unknown. No held source was recovered.

## Full copied final

**Yes. Under the accepted elementary return-controller construction in your premise, the full predictable-fault statement can be achieved.** The extension requires a uniform moment argument and a comparison over a fixed-length window. The stationary occupation argument alone is insufficient.

The useful additional conclusion is stronger than the population bound in the question: the construction can be parameterized so that
\[
\sup_{\substack{\text{admissible predictable faults}\\t\ge0}}
\mathbb E_{j(x_0)}(1+|Z_t|_1)^2
\le B_2,
\qquad B_2\le C_{\mathcal R}W^{p_{\mathcal R}}.
\tag{1}
\]
This pays for every marked firing and for the absolute-mean errors caused by faults.

I give the construction, the new estimates, the predictable-fault comparison, and an effective parameter and resource ledger below. The only accepted compiler results used are the ones in your premises. In particular, no invariant law, return-time bound, minorization, or weighted mixing envelope is supplied as an additional oracle.

---

## 1. The fixed elementary network

Use the return-controller realization from your constant-error premise, with the following choices made explicit.

All descriptions in this section concern a fixed finite network. Input-dependent quantities appear only in its constant rate coefficients.

### The original graph and the return words

Use the **unsaturated** ideal
\[
I_{\mathcal R}
=
\left\langle X^{y_r}-X^{z_r}:r\in\mathcal R\right\rangle.
\]
Compute a binomial Gröbner basis in a graded monomial order. Write its oriented rules as
\[
\alpha_g\longrightarrow\beta_g.
\]

For each rule, find a finite directed original-reaction word
\[
\alpha_g=p_{g,0}\longrightarrow p_{g,1}
 \longrightarrow\cdots\longrightarrow p_{g,\ell_g}=\beta_g.
\tag{2}
\]
These are terminating fixed-\(\mathcal R\) searches: monomial congruence for the unsaturated ideal is actual undirected reachability, and weak reversibility turns each undirected step into a directed word.

Choose a positive integer weight \(\omega\) satisfying
\[
\omega\cdot(\alpha_g-\beta_g)\ge1
\tag{3}
\]
for every reduction rule. Consequently, the normal form in the class of \(x_0\) has weight at most \(\omega\cdot x_0\). The compiler never computes the normal form of the variable input.

The elementary controller collects a rule’s source by binary reactions and then executes (2) through protected unary phases. The physical decoder of a word phase is its **current** payload \(p_{g,i}\). Thus every word-phase transition realizes an enabled original edge.

For analysis, use the separate nonnegative linear payload \(\bar D\), which holds \(\alpha_g\) throughout the word and changes to \(\beta_g\) upon completion. Define
\[
V(z)=\omega\cdot\bar Dz,\qquad n(z)=1+V(z).
\tag{4}
\]
This analytical payload is not a feedback signal.

### Prefixes and outward commitments

Use unique-parent binary assembly and release for the fixed catalytic table supplied by the higher-molecularity premise. Let \(D_0\ge1\) bound its encoded complex orders.

First assembly steps have forward/reverse coefficients \(\theta,1\); later steps have coefficients \(1,1\). Representative conversions are slowed by the common factor \(\theta\).

A conversion with positive change in \(V\) passes through \(M\) primary commit phases. Set
\[
g=4M.
\]
Primary progress has raw coefficient \(g\), and every phase has baseline abort coefficient \(1\). Multiply initiation by \((1+1/g)^M\). This preserves the intended nominal completed flux.

Each pending token also has a \(J\)-stage abort counter. **Primary progress preserves the abort-counter index.** For every species \(S\) with positive analytical weight, include the corresponding binary counter-progress reaction with coefficient
\[
\eta\,\omega\cdot\bar DS.
\]
For a token whose source payload has weight \(d_Y\), the nominal total counter hazard per token is exactly
\[
\eta(V-d_Y).
\tag{5}
\]
The subtraction is the falling-factorial self-exclusion. Catalysis includes sequestered payloads, not just free original molecules.

### Probes, retained identities, and the mode veto

Retain the controller mechanisms in the accepted construction:

- constant-rate probe immigration;
- \(J\) probe stages, each with unit death;
- activation into a retained controller identity and a mode marker;
- binary collection, protected unary words, and release;
- identity-preserving aborts;
- active-identity coalescence and dead retirement;
- a binary veto of pending outward commitments whenever a mode carrier is present.

An inactive probe is not a controller identity and cannot coalesce. Its only harmful transition before activation is its unit death. This fact will prevent a population exponent proportional to \(J\).

Let \(Q(z)\) be the weighted queue from that construction: it counts probes, active and dead identities, and zero-payload pending tokens. Choose its fixed weights so that dead progress decreases \(Q\), coalescence decreases \(Q\), and the only increases of \(Q\) are bounded constant-rate immigrations.

On the canonical communicating class,
\[
1+|z|_1\le C_{\mathcal R}(n(z)+Q(z)).
\tag{6}
\]
The identity invariant bounds every mode marker by the counted controller identities, so no auxiliary population is omitted.

All these reactions have at most two molecules on each side.

### Actual graph preservation

The graph argument is unchanged by the parameter choices below:

- assembly, release, counters, vetoes, and identity bookkeeping have decoded change zero;
- representative conversions have an enabled original decoded edge;
- protected word phases have the corresponding enabled edge in (2);
- baseline aborts, releases, word completion, and retirement provide finite paths back to canonical states;
- the \(w=0\) channels of the supplied catalytic table lift every original edge.

These are local payload statements and hold from **every fine state**, independently of the invariants used in the estimates. Therefore
\[
D(\widehat\Gamma)=\Gamma
\tag{7}
\]
for the actual communicating classes, and \(\widehat\Gamma\) is closed and irreducible. All admitted rate multipliers are positive, so they do not change this graph.

---

## 2. A common Lyapunov function for every instantaneous fault vector

Until the common clock normalization in Section 6, time and rates are **raw**.

Prove the following estimates for the entire multiplier box
\[
r_e\in[1/2,3/2].
\tag{8}
\]
They therefore hold for the smaller tolerance ultimately emitted by the compiler.

The queue satisfies, for every fixed integer \(a\ge1\),
\[
\mathcal L_{\mathbf r}Q^a\le C_a-c_aQ^a.
\tag{9}
\]
The constants are uniform in the rate vector. The fast mode veto preserves \(V\) and preserves or decreases \(Q\); increasing its coefficient cannot spoil this estimate.

### Pending-commit credit

Consider a pending token with:

- source weight \(d_Y\);
- outward increment \(\Delta>0\);
- \(i\in\{1,\ldots,M\}\) primary steps remaining;
- \(j\in\{1,\ldots,J\}\) abort-counter steps remaining.

Put
\[
G=\frac32g,\qquad B=\frac12,\qquad
a_Y(V)=\frac12\eta(V-d_Y)_+,
\]
and define
\[
p_{i,j}^{Y}(V)
=
\sum_{\ell=0}^{j-1}
\binom{i+\ell-1}{\ell}
\frac{G^i a_Y(V)^\ell}
     {(G+B+a_Y(V))^{i+\ell}}.
\tag{10}
\]
Use the bookkeeping boundary values \(p_{0,j}=1\) and \(p_{i,0}=0\). There are no physical pending tokens with \(i=0\).

This is the success probability for the worst permitted forward rate and the smallest permitted abort rates, with \(V\) frozen. It satisfies
\[
G(p_{i-1,j}-p_{i,j})
+a_Y(p_{i,j-1}-p_{i,j})
-Bp_{i,j}=0.
\tag{11}
\]

For an integer \(h\ge2M+2\), define
\[
F_h(z)
=
n^h
+
2\sum_{\text{pending tokens}}
p_{i,j}^{Y}(V)
\big[(n+\Delta)^h-n^h\big]
+
c_hQ^{h+3},
\tag{12}
\]
where \(c_h\) is a sufficiently large fixed rational constant.

This is **one fixed state function**, independent of the fault policy, the current multiplier vector, and the mode. It obeys
\[
c(n^h+Q^{h+3})
\le F_h
\le C(n^h+Q^{h+3}).
\tag{13}
\]

Here is the cancellation that makes it useful.

The token’s own primary, gate, and baseline-abort transitions have nonpositive credit drift by (11) and rate monotonicity. At actual completion, the physical token disappears, whereas the bookkeeping boundary in (11) is \(p_{0,j}=1\). The factor \(2\) in (12) therefore leaves a negative surplus after paying the outward increase of \(n^h\). Mode vetoes only remove credit.

For sufficiently large \(n\),
\[
p_{i,j}^{Y}\le \frac{C_J}{\eta n},
\qquad
\left|\frac{d}{dV}p_{i,j}^{Y}\right|
\le \frac{C_Mp_{i,j}^{Y}}{n}.
\tag{14}
\]
On \(Q\le4n\), there are \(O(n)\) pending tokens. The cross-credit change caused by another bounded \(V\)-jump is consequently at most
\[
C_{h,J}\eta^{-1}n^{h-2}.
\]
It is absorbed by the completion surplus when \(n\ge C_{h,J}/\eta\).

New outward tokens always enter with \(M\) primary steps remaining. Their total initiation intensity is \(O(n)\), while
\[
p_{M,J}^{Y}\le C_{M,J}(\eta n)^{-M}.
\]
Thus their total positive credit drift is at most
\[
C_{h,J}\eta^{-M}n^{h-M}.
\]

Writing \(b_V=b_{V,+}+b_{V,-}\) for the total intensity of nonzero \(V\)-changes gives the common cone estimate
\[
\boxed{\;
\mathcal L_{\mathbf r}F_h
\le
C_{h,J}\eta^{-M}n^{h-M}
-c_hn^{h-1}b_V,
\qquad Q\le4n,
\;}
\tag{15}
\]
outside an explicit tail threshold.

Outside the inner cone, the positive drift of the first two terms of (12) is at most \(C_{h,J}Q^{h+1}\). The queue term dominates it:
\[
\mathcal L_{\mathbf r}F_h
\le C_{h,J}-c_{h,J}Q^{h+3},
\qquad Q>2n.
\tag{16}
\]

Finally,
\[
\boxed{\;
\mathcal L_{\mathbf r}F_h
\le
C_{h,J}\eta^{-M}
\bigl(1+F_h^{\,1-M/h}\bigr)
\quad\text{globally on }\widehat\Gamma.
\;}
\tag{17}
\]
For the moderate region \(\eta n=O(1)\), use the bound \(p_{i,j}\le1\); then the positive drift is \(O(n^h)\), which is bounded by the right side of (17). This avoids introducing an extra inverse power of \(\eta\).

All coefficients and thresholds in these estimates have computable rational bounds obtained from finite sums, bounded-jump inequalities, and the fixed channel list.

Because (15)–(17) hold for every instantaneous multiplier vector, they remain valid inside conditional expectations for arbitrary predictable faults. No frozen-rate argument is being substituted for a common-function argument.

---

## 3. Controlled excursions give uniform second moments

Choose a fixed exposure/word length \(\ell\) for the controller, and put
\[
q=2\ell,\qquad M=q+3,\qquad \eta=\rho^{-8}.
\tag{18}
\]
The scale \(\rho=W^a\) will be chosen last.

### A bounded service block

Suppose
\[
n(z)=n,\qquad Q(z)\le2n,
\]
and \(n\) exceeds a sufficiently large threshold. Stop at
\[
\sigma=\min\{1,\ \text{first nonzero \(V\)-change},\
                    \text{first }Q\ge4n\}.
\]

Uniformly conditional on the complete past and over every future predictable fault rule,
\[
\mathbb P(\text{\(V\) changes before the other stops}\mid\mathcal F_0)
\ge c_Jn^{-q}.
\tag{19}
\]

The exponent \(q\) is independent of \(J\). To see this, admit one fresh probe and exclude other queue immigrations during the block. This has constant probability. While \(V\) has not changed, the probe’s gate intensity is bounded below by \(\eta V/2\), and its only harmful competitor is unit death. Once \(\eta V\) exceeds a computable multiple of \(J\), its \(J\) stages succeed within a fixed interval with probability bounded below by a fixed \(c_J>0\).

After activation, at most \(\ell\) relevant exposure, collection, and word steps are required. Each can be forced with probability at least \(c_Jn^{-2}\) against the remaining \(O(n^2)\) obstructive intensity. Earlier \(V\)-changes count as success. The fast veto is helpful and need not be excluded.

The successful event stays in the buffer: only the admitted immigration increases \(Q\), by a fixed amount. This proves success **before a \(V\)-change-or-buffer-exit race**, rather than merely a bound on that combined stopping event.

### Stopped rewards

Before \(\sigma\), \(V\) is constant and \(N=|Z|_1\le C_Jn\). Stopped Dynkin and the compensator of the first \(V\)-change give
\[
\begin{aligned}
\mathbb E[F_h(Z_\sigma)-F_h(Z_0)\mid\mathcal F_0]
&\le C_{h,J}\eta^{-M}n^{h-M}
-c_hn^{h-1}\mathbb E\int_0^\sigma b_V(Z_s)\,ds\\
&\le C_{h,J}\eta^{-M}n^{h-M}
-c_{h,J}n^{h-q-1}.
\end{aligned}
\tag{20}
\]
Since \(M=q+3\), the positive term is two population degrees smaller. Thus
\[
n\ge C_{h,J}\eta^{-M/2}
\tag{21}
\]
makes (20) at most \(-c_{h,J}n^{h-q-1}\).

For reward order \(r\), choose
\[
h(r)=\max(2M+2,q+r+1),\qquad
k(r)=h(r)+3=\max(2M+5,q+r+4).
\tag{22}
\]
Then (20) pays the integral of \((1+N)^r\) during the service block. When \(Q>2n\), (16) pays the same reward until return to the inner cone or entry into the core.

Pasting these conditional stopped inequalities gives
\[
\sup_{\mathsf a}
\mathbb E_u^{\mathsf a}
\int_0^{\tau_{\mathcal B}}(1+N_s)^r\,ds
\le C_{r,J}(1+N(u))^{k(r)},
\tag{23}
\]
where
\[
\mathcal B=\{n\le R,\ Q\le4R\},\qquad
R=C_J\rho^{r_0}.
\tag{24}
\]
Here and below \(u\in\widehat\Gamma\), the class of the compiled input.

One may take
\[
r_0=2+8(M+q+4).
\tag{25}
\]
This dominates the powers required by (21) and the probe threshold. Only finitely many reward orders are needed below. Take the maximum of their core coefficients; there is no assertion of one coefficient uniform over all possible orders.

The coefficients in (23) are independent of \(\rho\). Its dependence on \(\rho\) is confined to the stopping set.

### Sixth return moment and fourth-moment growth

Conditional on any history before \(\tau_{\mathcal B}\), the remaining fault rule is still admissible. Therefore (23) and
\[
\tau^p=p\int_0^\tau(\tau-s)^{p-1}\,ds
\]
give
\[
\sup_{\mathsf a}\mathbb E_u^{\mathsf a}\tau_{\mathcal B}^p
\le C_{p,J}(1+N(u))^{d_p},
\qquad
d_p=2M+5+(p-1)(q+4).
\tag{26}
\]
We use this only through \(p=6\).

Meanwhile, localized Dynkin applied to (17), followed by Jensen’s inequality, yields
\[
\sup_{\mathsf a}\mathbb E_u^{\mathsf a}(1+N_t)^4
\le
C_J\eta^{-4}(1+N(u))^7(1+t)^{4/M}.
\tag{27}
\]

Nonexplosion and the localization needed here hold directly. In an elementary network, a positive physical population jump has at most one reactant. Its total intensity is bounded by \(C(1+N)\). Up to any finite population level, the total marked intensity is bounded. This argument also applies to bounded predictable multipliers.

Combining (26) for \(p=6\) with (27) gives the integrable killed-excursion estimate
\[
\boxed{\;
\sup_{\mathsf a}
\mathbb E_u^{\mathsf a}
\big[(1+N_t)^2;\tau_{\mathcal B}>t\big]
\le
C_J\eta^{-2}(1+N(u))^c(1+t)^{-2},
\;}
\tag{28}
\]
where
\[
c=\left\lceil\frac{7+d_6}{2}\right\rceil.
\tag{29}
\]
Indeed, before weakening the time exponent to \(-2\), Cauchy–Schwarz gives \(2/M-3<-2\).

### Summing excursions at a deterministic time

Let \(\alpha_i\) be exits from \(\mathcal B\) and \(\beta_i\) their subsequent return times.

An exit lands at population at most \(C_JR\). Its predictable intensity is at most
\[
\Lambda\le C_J(1+R)^2.
\tag{30}
\]
The possibly large raw mode-veto coefficient does not enter this bound: those reactions preserve \(V\) and decrease or preserve \(Q\), so they cannot cause an exit.

Conditioning at \(\alpha_i\), applying (28), and summing gives
\[
\begin{aligned}
\mathbb E(1+N_t)^2
&\le C_JR^2+
 C_J\eta^{-2}(1+R)^c
 \mathbb E\sum_{\alpha_i\le t}(1+t-\alpha_i)^{-2}\\
&\le C_JR^2+
 C_J\eta^{-2}(1+R)^c\Lambda
 \int_0^\infty(1+s)^{-2}\,ds.
\end{aligned}
\tag{31}
\]
The last step is the exit counting-process compensator.

The canonical initial state is in \(\mathcal B\). Hence
\[
\boxed{\;
\sup_{\mathsf a,t\ge0}
\mathbb E_{j(x_0)}^{\mathsf a}(1+N_t)^2
\le B_2:=C_{2,J}\rho^\beta,
\qquad
\beta=16+r_0(c+2).
\;}
\tag{32}
\]

For arbitrary \(u\in\widehat\Gamma\), including the initial excursion before first entry into \(\mathcal B\), the same proof gives
\[
\sup_{\mathsf a,t\ge0}
\mathbb E_u^{\mathsf a}(1+N_t)^2
\le C_{2,J}\rho^\beta(1+N(u))^c.
\tag{33}
\]

This is the required deterministic-time moment bound. An averaged occupation estimate would not establish (31).

---

## 4. A polynomial nominal window from every moderate fine state

The next task is nominal only. This is where the accepted construction’s rare-intervention separation is used.

### The uncoloured base

Project away the abort-counter indices and probes. In the passive reference process, a terminal abort-counter event is null and a terminal probe event removes the probe. The projected base is autonomous.

For an outward channel with balanced flux \(J_e=\kappa_e\lambda^Y\), the nominal activity of primary phase \(i\) is
\[
c_{e,i}
=
\frac{\theta J_e}{g}
(1+1/g)^{M-i-1}
\le\theta\lambda^Y.
\tag{34}
\]
The last-phase flux is \(\theta J_e\); the total abort flux cancels the excess initiation. Thus the uncoloured base is complex balanced. Its invariant law is the corresponding product-Poisson law restricted to its actual class, by the stochastic complex-balance product-form theorem. [arxiv.org](https://arxiv.org/abs/0803.3042?utm_source=chatgpt.com)

Let \(s_0\) be its species count, including the \(M\) primary phases. It does **not** include the \(J\) counter colours. Set
\[
b_\theta=2D_0+5,\qquad
\theta=(W\rho)^{-b_\theta}.
\tag{35}
\]

The nominal fibre comparison and canonical-anchor estimates from the supplied construction give
\[
\operatorname{TV}(D_*\mu_0,\pi_\lambda)
+
\max_i|\mu_0(Dz)_i-\pi_\lambda X_i|
\le C_{\mathcal R}\theta W^{2D_0+2}.
\tag{36}
\]

For clarity, the effective weak-Poincaré comparison used here has coefficient
\[
A(B)\le
C_{\mathcal R}\theta^{-1}W^{p_0+2D_0}
(1+B)^{s_0+4D_0+2},
\tag{37}
\]
and factorial tail remainder
\[
b(B)\le
\exp\!\left(C_{\mathcal R}W^2
-c_{\mathcal R}B\log\frac{B}{C_{\mathcal R}W}\right).
\tag{38}
\]
The ball in these estimates is analytical; it does not modify the process.

Taking \(B=C\rho^2\), a sufficient mixing exponent is
\[
Q_0=
2b_\theta+p_0+2D_0+
2(s_0+4D_0+2)+20.
\tag{39}
\]
From every uncoloured base state with \(N\le C\rho\), at
\[
T_0=C_0\rho^{Q_0}
\tag{40}
\]
the fine-state TV error can be made at most \(\rho^{-10}\). Fine-state TV contraction gives the same bound at every later time. The all-time second-moment estimate then pays the absolute decoded means at every later time as well.

This uses no positive ordinary spectral gap for the infinite elementary chain.

### Strict clean states and nominal returns

Let \(\mathcal C\) consist of states with:

- no mode or controller identities;
- no probes;
- all pending abort-counter indices equal to zero;
- \(N\le C_{\mathrm{typ}}W^2\).

The nominal return argument of the accepted controller gives
\[
\mathbb E_u^{\,0}\tau_{\mathcal C}
\le
C_J\rho^{E+7J}(1+N(u))^{k_0},
\qquad k_0=3q+19,
\tag{41}
\]
where \(E\) is fixed before \(J\).

Here is the quantitative mechanism behind this all-state estimate. From the original large core, a nominal trial has polynomial duration and succeeds with probability at least \(c_J\rho^{-7J}\). Above the low threshold \(V=\rho\), a tagged probe has \(J\) lower gate rates of order
\[
\eta\rho=\rho^{-7},
\]
which gives the \(\rho^{-7J}\) factor. Existing active mode instead uses retained identities and the Gröbner words to reach normal form. The death and veto coefficients are chosen to pay mode extinction, unwanted commitments, retirement, and the final nominal restart.

Failed endpoints are paid before retrying. For the nominal return potential
\[
U_4(u)=\mathbb E_u^{\,0}
\int_0^{\tau_{\mathcal B_0}}(1+N_s)^4\,ds,
\]
the stopped-reward estimate gives a polynomial bound, and
\[
\mathcal L_0U_4\le K_4-(1+N)^4.
\]
Consequently a trial of bounded duration pays both its occupation cost and the expected \(U_4\) of its endpoint. Geometric retries therefore yield (41), without conditioning a polynomial moment bound on a rare failure.

This nominal argument is not applied to adaptive faults.

### Rare interventions over a long nominal interval

From \(c\in\mathcal C\), the passive reference has, for each fixed \(h\),
\[
\sup_{t\ge0}\mathbb E_c^{\rm ref}(1+N_t)^h
\le C_h\big[W^2(1+\log\rho)\big]^h.
\tag{42}
\]
A token cohort decomposition, baseline unit-death survival, and the \(J\) required gate events give
\[
\mathbb P_c^{\rm ref}
(\text{an intervention by time }S)
\le
C_J\eta^J(1+S)
\big[W^2(1+\log\rho)\big]^{J+1}.
\tag{43}
\]
The dependence on \(S\) is linear. Each token’s baseline lifetime supplies the integrable survival factor in the ordered gate-event integrals.

The distinction between (42) and the coarse controlled bound (33) matters: substituting a large power of \(\rho\) for each of the \(J\) reference moments would destroy the separation.

### Choosing one window

Before choosing \(J\), define
\[
\begin{aligned}
b&=\beta+10, &
R_{\rm cut}&=\rho^b,\\
\beta_{\rm cap}&=\beta+bc, &
\beta_{\mathcal C}&=\beta+2c+2,\\
P&=E+bk_0+\beta_{\rm cap}+Q_0+40.
\end{aligned}
\tag{44}
\]
Choose
\[
S=C_S\rho^{7J+P}.
\tag{45}
\]

From \(1+N(u)\le R_{\rm cut}\), (41) and Markov’s inequality give
\[
\mathbb P_u^0(\tau_{\mathcal C}>S-T_0)
\le
C_J\rho^{-\beta_{\rm cap}-Q_0-40}.
\tag{46}
\]
Equation (33) pays the first-moment contribution of this failure by Cauchy–Schwarz.

On successful arrival, the remaining nominal time lies in \([T_0,S]\). The strong Markov property applies, and the clean-start estimates are uniform over all such lags.

For the clean-start comparison, (43) contains
\[
\eta^JS=\rho^{P-J}.
\]
The full nominal process from a clean state has second moment at most \(C_J\rho^{\beta_{\mathcal C}}\), by (33). Thus the same intervention probability pays both TV and absolute means provided
\[
J>P+\beta_{\mathcal C}+40.
\tag{47}
\]
Also impose the earlier, fixed nominal trial inequalities on \(J\).

Finally choose \(\rho=W^a\) with \(a\) sufficiently large. All remaining \(W\)-powers and logarithms in (43) are fixed after \(J\); for each fixed integer \(b'\),
\[
(1+\log\rho)^{b'}\le C_{b'}\rho.
\]
Therefore the choices are noncircular.

The resulting nominal full-network estimate is
\[
\boxed{\;
\sup_{\substack{u\in\widehat\Gamma\\1+N(u)\le R_{\rm cut}}}
\left[
\operatorname{TV}(D_*P_S^0(u,\cdot),\pi_\lambda)
+
\max_i\left|P_S^0(Dz)_i(u)-\pi_\lambda X_i\right|
\right]
\le\frac{\epsilon}{8}.
\;}
\tag{48}
\]

---

## 5. The fixed-window lemma for arbitrary predictable faults

This is the step that gives accuracy at **every** sufficiently late deterministic time.

Consider a normalized elementary network with \(m\) labelled channels, nominal coefficients at most \(1\), and decoder coefficient bound
\[
d_*=\max_j |De_j|_1.
\]
Suppose its whole-run, all-policy second-moment bound is \(B_2\), and its nominal time-\(T\) law satisfies (48) from populations at most \(R_{\rm cut}\).

Fix any admissible fault policy and any deterministic \(t\ge T\). Put \(a=t-T\).

Define an analytical comparison process \(Y\) that follows the actual process until \(a\) and uses nominal rates thereafter. This switched rule is itself an admissible predictable policy from the canonical initial state. Hence
\[
\mathbb E(1+|Y_t|_1)^2\le B_2.
\tag{49}
\]

Conditional on the history at \(a\), the comparison endpoint has nominal law \(P_T^0(Z_a,\cdot)\). The large-start event
\[
F=\{1+|Z_a|_1>R_{\rm cut}\}
\]
satisfies
\[
\mathbb P(F)\le\frac{B_2}{R_{\rm cut}^2},
\qquad
\mathbb E[(1+|Y_t|_1)\mathbf1_F]
\le\frac{B_2}{R_{\rm cut}}.
\tag{50}
\]
The second inequality uses the unconditional bound (49); no conditional moment estimate on a rare starting tail is needed.

Now couple **all labelled firing marks** of the actual and comparison processes during this window. Before their first mismatch, their complete marked histories agree. Predictability therefore permits the usual common-intensity coupling even when the fault rule reads the entire past.

The mismatch intensity is at most
\[
\delta\sum_e k_e(Z_s)_{\alpha_e}
\le \delta m(1+N_s)^2.
\]
Consequently,
\[
p_{\rm mis}\le\delta mB_2T.
\tag{51}
\]
Null and parallel marks are included: a mismatched null mark is flagged because the adversary may use it in its subsequent decisions.

Both endpoint marginals have second moment at most \(B_2\), so
\[
\max_i
\left|\mathbb E(DZ_t)_i-\mathbb E(DY_t)_i\right|
\le
2d_*B_2\sqrt{\delta mT}.
\tag{52}
\]

Combining these estimates, with \(M_\pi=\max_i\pi_\lambda X_i\), gives
\[
\begin{aligned}
\operatorname{TV}(\mathcal L(DZ_t),\pi_\lambda)
&\le \frac{\epsilon}{8}
+\frac{B_2}{R_{\rm cut}^2}
+\delta mB_2T,\\
\max_i|\mathbb E(DZ_t)_i-\pi_\lambda X_i|
&\le \frac{\epsilon}{8}
+\frac{d_*B_2}{R_{\rm cut}}
+\frac{M_\pi B_2}{R_{\rm cut}^2}
+2d_*B_2\sqrt{\delta mT}.
\end{aligned}
\tag{53}
\]
The canonical Poisson anchor gives the computable bound \(M_\pi\le C_{\mathcal R}W^2\).

The cutoff in (44) makes the tail terms smaller than \(\epsilon/8\) after the final choice of \(a\). Emit
\[
\boxed{\;
\delta=
\min\!\left\{
\frac12,\,
\frac{\epsilon^2}
{256\,m(1+d_*)^2B_2^2(1+T)}
\right\}.
\;}
\tag{54}
\]
Then (53) is strictly below \(\epsilon\) in both requirements.

The proof works for each \(t\ge T\), with the **same** rates, tolerance, and window length. It does not accumulate an error estimate from time zero.

The comparison process is only a proof device. The emitted physical network performs no switch or reset.

---

## 6. Physical normalization, stationary laws, and all firing costs

Let \(\kappa_e\) be the raw coefficients of the construction. Normalize once:
\[
H=1+\sum_e\kappa_e,\qquad
k_e=\frac{\kappa_e}{H},\qquad
T=HS.
\tag{55}
\]
Then \(0<k_e\le1\).

Deterministic time rescaling preserves predictability and the multiplier box. Thus the uniform-in-time moment bound (32) transfers unchanged to physical time. Return-time estimates were used in raw time; their clock factors have been included in \(T\).

### Every firing is paid

For every admitted policy,
\[
\sum_e k_er_e(t)(Z_t)_{\alpha_e}
\le \frac32m(1+N_t)^2.
\]
Therefore
\[
\boxed{\;
\mathbb E[\text{all labelled firings on }[0,t]]
\le\frac32mB_2t
\quad\text{for every }t\ge0.
\;}
\tag{56}
\]
This counts binding, release, abort, unsuccessful controller actions, null firings, and parallel labels. Also,
\[
\sup_{\mathsf a,t\ge0}\mathbb E|Z_t|_1\le\sqrt{B_2}.
\tag{57}
\]

### Frozen faults

For constant admitted multipliers, the process is a nonexplosive, time-homogeneous irreducible chain on \(\widehat\Gamma\).

The uniform second-moment bound makes its Cesàro occupation laws tight. A subsequential limit is invariant: if
\[
\nu_L=\frac1L\int_0^L\mathcal L(Z_t)\,dt,
\]
then
\[
\|\nu_LP_s-\nu_L\|_{\rm TV}\le \frac{2s}{L}.
\]
On the countable state space, tight subsequences converge in TV, and Markov contraction passes this identity to the limit.

Thus the chain has an invariant probability, is positive recurrent, and has a unique stationary law \(\mu_r\). Moreover,
\[
\mathbb E_{\mu_r}(1+N)^2\le B_2.
\tag{58}
\]
The late-time decoded TV bounds pass to the Cesàro limit. Uniform integrability from (32) passes the absolute-mean bounds as well. This establishes all the requested frozen-rate stationary conclusions.

---

## 7. Explicit computable constants and compiler cost

Here is an effective ledger. Its size is deliberately conservative.

All preprocessing below depends only on \(\mathcal R\).

1. Compute the fixed catalytic table, unsaturated Gröbner basis, directed word certificates, weight \(\omega\), decoder, and elementary templates.
2. Let \(A_0\) bound Gröbner-head orders and \(L_0\) bound directed word lengths. A sufficient exposure length is
   \[
   \ell=10(A_0+1)(D_0+A_0+L_0+5).
   \]
3. Set \(q,M,k_0,r_0,b_\theta,Q_0\) by (18), (25), (35), (39), and \(k_0=3q+19\).
4. Choose integer constants \(C_+,b_+\) bounding the total positive-jump intensity and jump size of \(1+V+Q\):
   \[
   \text{positive intensity}\le C_+(1+V+Q),\qquad
   \text{positive jump}\le b_+.
   \]
   These are independent of \(J\): probe/counter progress preserves \(V+Q\), and each pending token has one primary-completion channel. Put
   \[
   \gamma_k=1+C_+\big[(1+b_+)^k-1\big].
   \]
   For the nominal return trials, sufficient degrees are
   \[
   \begin{aligned}
   r_1&=r_0\bigl(2+k_0+(4w+4)\gamma_{k_0}\bigr),\\
   u_d&=(q+2)r_1+4,\\
   v&=u_d+2r_1+6,\\
   E&=(k_0+3)r_0+Q_0+u_d+2r_1+30.
   \end{aligned}
   \tag{59}
   \]
   Use identity-death coefficient \(\rho^{-u_d}\) and veto scale \(A=\rho^v\).
5. Compute \(d_6,c,\beta,b,\beta_{\rm cap},\beta_{\mathcal C},P\) from (26), (29), (32), and (44).
6. Choose \(J\) satisfying (47) and the finite nominal-trial inequalities. All their degrees have already been chosen.
7. Compute rational upper and lower constants for the finite collection of Lyapunov, service, nominal, and intervention estimates. Choose \(a\) last.

The last step is effective. For example, collect the remaining error conditions as
\[
C_iW^{u_i}\rho^{-s_i}\le c_iW^{-r_i},
\qquad s_i>0,
\]
after bounding fixed logarithmic powers by \(C\rho\). Choose an integer \(a\) satisfying
\[
a s_i\ge u_i+r_i+
\left\lceil\log_2(C_i/c_i)\right\rceil+2
\]
for every row, and set \(\rho=W^a\).

Every constant here can be bounded by rational arithmetic on finite certificates. The service probabilities use elementary upper and lower hazard bounds. The Lyapunov constants come from the finite sums in (10) and polynomial bounded-jump estimates. These are fixed preprocessing calculations, not searches over an input-dependent population ball or stationary distribution.

Let \(p_0\) also dominate the accepted higher-molecularity compiler’s bit-work and reciprocal-rate exponents, enlarging it to an integer if necessary. A sufficient raw reciprocal-rate degree is
\[
u_{\rm rate}=\max\{p_0+2b_\theta,u_d,8\}.
\]
The normalization satisfies \(H\le C_J\rho^v\), and the resulting bounds include
\[
\begin{aligned}
T&\le C_J\rho^{v+7J+P},\\
\delta^{-1}
&\le C_J\rho^{2\beta+v+7J+P+2},\\
\max_e k_e^{-1}
&\le C_J\rho^{v+u_{\rm rate}}.
\end{aligned}
\tag{60}
\]

For a completely explicit computable pair, take
\[
\boxed{\;
p_{\mathcal R}
=
2p_0+4+
a\bigl(2\beta+2v+7J+P+u_{\rm rate}+20\bigr).
\;}
\tag{61}
\]
Let \(N_{\mathcal R}\) be an integer exceeding the bit-operation count and stored certificate length of a specified implementation of the fixed preprocessing above, including the computed rational coefficient bounds. Define
\[
\boxed{\;
C_{\mathcal R}=2^{(N_{\mathcal R}+2)^4}.
\;}
\tag{62}
\]
This is an explicit computable function of the fixed structure. It absorbs all fixed searches, coefficients, network size, and arithmetic overhead.

For the variable input, \(W\) has \(O_{\mathcal R}(L)\) bits. The additional compiler operations are fixed rational powers, additions, multiplications, divisions, and comparisons, together with the accepted higher compiler. Hence bit work, memory, and output satisfy
\[
C_{\mathcal R}(1+L)^{p_{\mathcal R}}.
\]
Equations (32), (55)–(60) give every numerical physical bound in the question with the same enlarged pair.

Empty structures can be handled directly. Singleton classes need no class-recognition oracle: the general construction already has constant decoded output on such a class.

---

The published results you named provide useful criteria, but the extension above uses the explicit common credit function and the excursion argument. Anderson–Kim’s Theorem 3.2 imposes double-fullness and reaction-graph paths from double complexes to unary or zero complexes. Douc–Moulines–Rosenthal’s inhomogeneous theorem assumes its pairwise minorization and drift conditions. Those hypotheses are not invoked here as consequences of graph faithfulness. [aimspress.com](https://www.aimspress.com/aimspress-data/mbe/2023/3/PDF/mbe-20-03-217.pdf?utm_source=chatgpt.com)

Thus the same fixed finite elementary realization, with the parameter order specified above, satisfies **all** of the requested conclusions: actual graph and class preservation, arbitrary predictable-fault accuracy at every deterministic \(t\ge T\), frozen-rate recurrence and stationary accuracy, and polynomial numerical bounds for the entire physical population and every actual marked firing.

---

## Current visible activity

you may use all subagents avaible"
    - generic: …
    - button "Show more":
      - generic: Show more
    - button "Copy message":
    - button "Share prompt":
    - button "Edit message":
    - button "Worked for 109m 6s" [expanded] [active]:
      - generic: Worked for 109m 6s
    - paragraph: I’ll check whether the return-controller construction can give uniform moment bounds under adaptive faults, then use those bounds to tackle accuracy at every late deterministic time. The stationary occupation argument alone does not give that conclusion, so the two steps need separate proofs.
    - region "Subagent activity":
      - button "Stationary obstructions"
      - text: ","
      - button "Conversion stationarity"
      - text: and
      - button "Alternative elementary"
      - text: updated
    - generic: Analyzing the User’s Request
    - region "Subagent activity":
      - button "Alternative elementary"
      - text: updated
    - paragraph: Defined robust hitting values and derived short-time spike bounds
    - paragraph: Refined uniform moment bounds and applied subgeometric drift theorem
    - paragraph: Developed excursion bounds
    - paragraph: Derived return-time bounds
    - paragraph: Fixed common core R
    - paragraph: Fixed base Foster order and checked enlarged-radius exponents
    - paragraph: Extended uniform Foster bounds
    - region "Subagent activity":
      - button "Stationary obstructions"
      - text: ","
      - button "Conversion stationarity"
      - text: and
      - button "Alternative elementary"
      - text: updated
    - paragraph: Developed block coupling
    - paragraph: Set up asynchronous coupling
    - paragraph: Developed pairwise Lyapunov bounds
    - paragraph: Checked coupling coadaptedness
    - paragraph: Bounded coupled-block costs and checked truncated-time independence
    - paragraph: Verified uniform C-probability
    - paragraph: Bounded pair recovery moments
    - paragraph: Fixed and configured weighted coupling parameters
    - paragraph: Fixed semigroup mixing bounds
    - paragraph: Chose explicit convergence time
    - paragraph: The uniform moment step has a concrete route. The tail-return estimates can be made conditional on the entire past, so they still apply under predictable faults. Higher return-time moments then bound the population during each excursion outside a finite analytical region. Summing those bounds over excursion starts gives uniform moments at deterministic times, rather than only an occupation average.
    - region "Subagent activity":
      - button "Conversion stationarity"
      - text: ","
      - button "Stationary obstructions"
      - text: and
      - button "Alternative elementary"
      - text: updated
    - generic: Searched 22 websites
    - paragraph: Established the first-jump DPP and checked U-sup computability
    - paragraph: Defined pair population cap
    - paragraph: Derived pair recovery bounds
    - paragraph: Calculated the trial horizon
    - paragraph: Checked endpoint coupling
    - paragraph: Checked uniform moment bounds
    - paragraph: Bounded coupling-time moments
    - paragraph: Fixed the coupling exponent
    - paragraph: Derived uniform moment bounds
    - paragraph: Established noncircular state moment bounds
    - paragraph: Checked parameter bounds
    - generic: Searched 22 websites
    - region "Subagent activity":
      - button "Stationary obstructions"
      - text: finished
    - paragraph: Developed finite-horizon coupling and verified fixed-time mixing
    - paragraph: Set up full-window coupling and bounded expectation error
    - paragraph: Chose a cutoff for mixtures
    - paragraph: Chose D and J
    - region "Subagent activity":
      - button "Conversion stationarity"
      - text: ","
      - button "Alternative elementary"
      - text: and
      - button "Stationary obstructions"
      - text: updated
    - paragraph: Constructed admissible hybrid coupling and verified marked intensity
    - paragraph: Verified adaptive coupling bound
    - paragraph: Set coupling error bounds
    - paragraph: Formalized conditional window comparison
    - paragraph: Chose the window exponent
    - paragraph: Bounded cutoff mixture error
    - paragraph: Checked tail-radius scaling
    - region "Subagent activity":
      - button "Conversion stationarity"
      - text: ","
      - button "Stationary obstructions"
      - text: and
      - button "Alternative elementary"
      - text: finished
    - paragraph: Verified drift exponents and checked enlarged B
    - paragraph: Established history-uniform bounds
    - paragraph: Bounded expected F growth
    - paragraph: Checked moment bounds
    - paragraph: Bounded exit intensity and total moments
    - paragraph: Checked clock error bounds and calculated C_R preprocessing cost
    - paragraph: Refined explicit constants
    - paragraph: Set p_R from bounds and cleared m_R counts
    - paragraph: Checked moment-based stationarity
    - paragraph: Simplified recurrence proof
    - paragraph: There is now a simpler path to the late-time guarantee. For any deterministic endpoint, compare the preceding fixed-length window with a nominal run from the same fine state. That nominal comparison is itself an admissible continuation of the earlier faulty run, so the uniform moment bound applies to both endpoints. This pays the effect of adaptive faults on the window and lets the nominal return-and-mixing estimate finish the argument.
    - generic: Searching probability.ca
    - region "Subagent activity":
      - button "Obstructions"
      - text: updated
    - paragraph: I’m checking the step that must control the whole infinite run. The proposed argument bounds second moments uniformly over all allowed fault histories by summing excursions outside a finite set used only in the proof. The remaining audit is whether those excursion bounds follow from the controller’s pointwise rate estimates without assuming independence of the faults.
    - region "Subagent activity":
      - button "Stationary obstructions"
      - text: and
      - button "Conversion stationarity"
      - text: updated
    - paragraph: Derived and bounded Fh credit derivatives
    - paragraph: Bounded tail derivatives and initiation terms
    - paragraph: Derived robust bounds for queue drift
    - paragraph: Bounded outside-cone drift and credit contributions
    - paragraph: Extended the global drift bound
    - paragraph: Verified block-drift bounds
    - paragraph: Formalized probe and controller hazard bounds
    - paragraph: Formalized weighted tail bounds and checked V drift bounds
    - paragraph: Established nonexplosion and exponential drift bounds
    - paragraph: Checked clean-return estimate applicability and bounds
    - paragraph: Refined fixed-block bounds
    - region "Subagent activity":
      - button "Obstructions"
      - text: and
      - button "Stationary obstructions"
      - text: updated
    - paragraph: Checked stopping-time drift bounds and exponent constraints
    - paragraph: Checked excursion-rate bounds
    - paragraph: Determined Ctyp normalization
    - paragraph: Estimated clean-return time
    - paragraph: Checked fine-graph closure
    - paragraph: Computed fixed resource constants and compiler cost bounds
    - paragraph: Bounded coefficient bitlengths and refined the p_R bound
    - paragraph: Handled controller and singleton edge cases
    - paragraph: Refined robust-mixing proof and checked post-activation aborts
    - paragraph: Formalized the conditional bound
    - paragraph: Prepared F_h tail bounds
    - paragraph:
      - text: The audit found a simpler way to prove the excursion bound. Within a fixed-length block, the controller has a polynomially bounded chance of changing the decreasing weight before leaving a buffered region. The probe’s
      - math:
        - generic: J
      - generic: J
      - text: "stages affect the constant in that bound, but not its population exponent. This preserves the parameter order: the moment and return-time exponents can be fixed before choosing"
      - math:
        - generic: J
      - generic: J
      - text: .
    - region "Subagent activity":
      - button "Stationary obstructions"
      - text: updated
    - generic: Searching 2 websites
    - region "Subagent activity":
      - button "Conversion stationarity"
      - text: updated
    - paragraph: Checked compiler constant formulas and phase-count bounds
    - paragraph: Refined γ_k growth bound
    - paragraph: Chose the birth bound
    - paragraph: Prepared nominal phase certificate
    - region "Subagent activity":
      - button "Obstructions"
      - text: finished
    - paragraph: Built a Poisson coupling
    - paragraph: Derived microinterval probability bounds
    - paragraph: Prepared indexed probability recurrence and formed the F_h expression
    - paragraph: Derived the cross-boundary relationships
    - paragraph: Bounded event and cross-generator drift terms
    - paragraph: Finalized finite h set
    - paragraph: Checked restart mixing bounds
    - paragraph: Tuned activation exponents
    - paragraph: Checked NF extinction bounds
    - paragraph: Defined the conservative exponent
    - paragraph: Checked nominal fine-TV mixing
    - region "Subagent activity":
      - button "Obstructions"
      - text: updated
    - paragraph: Checked queue Lyapunov bounds
    - paragraph: Computed explicit coefficient bounds
    - paragraph: Verified Gröbner head encoding and binomial congruence
    - paragraph: Checked preprocessing independence and verified gate hazard count
    - paragraph: Verified the proof bounds
    - paragraph: Checked clean-state base class
    - paragraph: Checked graph edge validity and original paths
    - paragraph: Checked normalization bounds and set nominal error bound
    - paragraph: Chose exponent from constants
    - paragraph: Prepared numerical ledger
    - paragraph: "The pending-commit calculation checks out. A single fixed Lyapunov function works for every allowed instantaneous rate vector: its credit uses worst-case forward and abort rates, and the fast mode veto can only reduce that credit. Together with the excursion estimate, this supplies the uniform second-moment bound needed for both late-time accuracy and the cost of all firings."
    - paragraph: Derived finite-h F_h bounds
    - paragraph: Proved hybrid moment bound
    - paragraph: Defined resource constants
    - paragraph: Checked fibre comparison conditions
    - region "Subagent activity":
      - button "Obstructions"
      - text: and
      - button "Conversion stationarity"
      - text: updated
    - paragraph: The late-time comparison now follows from a fixed-length window. For any chosen endpoint, an analytical comparison process follows the faulty run until the window starts, then uses nominal rates. The uniform moment bound pays for large states at the window’s start, and a marked coupling bounds every adaptive fault during the window. The same tolerance works at every endpoint because this bound does not grow with the elapsed run time.
    - paragraph: Prepared nominal base certificate
    - paragraph: Checked conditional tail bounds
    - generic: Searching arxiv.org
    - paragraph: Verified the Q0 formula
    - paragraph: Checked computable certificate using return-controller network
    - region "Subagent activity":
      - button "Obstructions"
      - text: and
      - button "Conversion stationarity"
      - text: updated
    - paragraph: Checked the moment bound
    - paragraph: Verified fixed constant bounds
    - paragraph: Derived explicit parameter bounds
    - paragraph: Checked weak-PI variance decay
    - paragraph: Adopted null final events
    - paragraph:
      - text: "The parameter choices are consistent: the population and return-time exponents come first, the probe length"
      - math:
        - generic: J
      - generic: J
      - text: comes next, and the scale
      - math:
        - generic: ρ
        - generic: =
        - generic: W
        - generic: a
      - generic: ρ =
      - text: W
      - generic: a
      - text: comes last. The nominal mixing estimate also applies to the full fine-state law, so contraction and the moment bounds pay for absolute-mean accuracy at every later time. I’m assembling the proof and the explicit resource bounds.
    - paragraph: Chose rho threshold
    - paragraph: Fixed constants sequentially
    - paragraph: Verified stationary moment bounds
    - 

## Current visible helper panels

  - complementary:
    - heading "Subagents" [level=2]
    - button "Enter full view":
    - button "Close panel":
    - tabpanel "Subagents" [active]:
      - button "Back to subagents":
      - generic: Conversion stationarity
      - heading "Status" [level=2]
      - generic: Done
      - heading "Final response" [level=2]
      - paragraph: Yes. The ledger value
      - math:
        - generic: Q
        - generic: "0"
        - generic: =
        - generic: "2"
        - generic: b
        - generic: θ
        - generic: +
        - generic: p
        - generic: "0"
        - generic: +
        - generic: "2"
        - generic: D
        - generic: "0"
        - generic: +
        - generic: "2"
        - generic: (
        - generic: s
        - generic: "0"
        - generic: +
        - generic: "4"
        - generic: D
        - generic: "0"
        - generic: +
        - generic: "2"
        - generic: )
        - generic: +
        - generic: "20"
      - text: Q
      - generic: "0"
      - text: = 2
      - text: b
      - generic: θ
      - text: +
      - text: p
      - generic: "0"
      - text: + 2
      - text: D
      - generic: "0"
      - text: + 2(
      - text: s
      - generic: "0"
      - text: + 4
      - text: D
      - generic: "0"
      - text: + 2) + 20
      - paragraph:
        - text: is a certified conservative exponent for nominal
        - strong: uncoloured-base fine-state TV mixing
        - text: from every state with
        - math:
          - generic: "N"
          - generic: (
          - generic: u
          - generic: )
          - generic: ≤
          - generic: C
          - generic: R
          - generic: ρ
        - generic: N(u) ≤
        - text: C
        - generic: R
        - text: ρ
        - text: ", provided"
        - math:
          - generic: s
          - generic: "0"
        - text: s
        - generic: "0"
        - text: counts only the uncoloured base, including its
        - math:
          - generic: M
        - generic: M
        - text: primary phases.
      - paragraph:
        - text: The
        - math:
          - generic: +
          - generic: "20"
        - generic: "+20"
        - text: is ample slack. Here is the certificate.
      - heading "Weak-Poincaré coefficient" [level=3]
      - paragraph: The finite-path comparison gives
      - math:
        - generic: Var
        - generic: ⁡
        - generic: μ
        - generic: "0"
        - generic: f
        - generic: ≤
        - generic: A
        - generic: (
        - generic: B
        - generic: )
        - generic: E
        - generic: "0"
        - generic: (
        - generic: f
        - generic: ","
        - generic: f
        - generic: )
        - generic: +
        - generic: b
        - generic: (
        - generic: B
        - generic: )
        - generic: osc
        - generic: ⁡
        - generic: (
        - generic: f
        - generic: )
        - generic: "2"
        - generic: ","
      - generic: Var
      - text: μ
      - generic: "0"
      - text: f ≤
      - text: A(B)
      - text: E
      - generic: "0"
      - text: (f, f) +
      - text: b(B)
      - generic: osc
      - text: (f
      - text: )
      - generic: "2"
      - text: ","
      - paragraph: with
      - math:
        - generic: A
        - generic: (
        - generic: B
        - generic: )
        - generic: ≤
        - generic: C
        - generic: R
        - generic: θ
        - generic: −
        - generic: "1"
        - generic: W
        - generic: p
        - generic: "0"
        - generic: +
        - generic: "2"
        - generic: D
        - generic: "0"
        - generic: (
        - generic: "1"
        - generic: +
        - generic: B
        - generic: )
        - generic: s
        - generic: "0"
        - generic: +
        - generic: "4"
        - generic: D
        - generic: "0"
        - generic: +
        - generic: "2"
        - generic: .
        - generic: (1)
      - generic: A(B) ≤
      - text: C
      - generic: R
      - text: θ
      - generic: −1
      - text: W
      - text: p
      - generic: "0"
      - text: "+2"
      - text: D
      - generic: "0"
      - text: (1 +
      - text: B
      - text: )
      - text: s
      - generic: "0"
      - text: "+4"
      - text: D
      - generic: "0"
      - text: "+2"
      - text: .
      - text: (
      - generic: "1"
      - text: )
      - paragraph: "This bound is certified by the following finite combinatorial estimates:"
      - list:
        - text: A whole auxiliary release raises its final weight by at least
        - math:
          - generic: "["
          - generic: θ
          - generic: (
          - generic: C
          - generic: R
          - generic: B
          - generic: )
          - generic: D
          - generic: "0"
          - generic: "]"
          - generic: −
          - generic: "1"
          - generic: ≥
          - generic: "1."
        - text: "[θ("
        - text: C
        - generic: R
        - text: B
        - text: )
        - text: D
        - generic: "0"
        - text: "]"
        - generic: −1
        - text: ≥
        - generic: "1."
        - text: Intermediate release weights lose at most a factor
        - math:
          - generic: (
          - generic: C
          - generic: R
          - generic: B
          - generic: )
          - generic: "2"
          - generic: D
          - generic: "0"
        - text: (
        - text: C
        - generic: R
        - text: B
        - text: )
        - text: "2"
        - text: D
        - generic: "0"
        - text: .
        - text: There are at most
        - math:
          - generic: (
          - generic: C
          - generic: R
          - generic: B
          - generic: )
          - generic: s
          - generic: "0"
        - text: (
        - text: C
        - generic: R
        - text: B
        - text: )
        - text: s
        - generic: "0"
        - text: possible starting states, and each complete release path has length at most
        - math:
          - generic: C
          - generic: R
          - generic: B
        - text: C
        - generic: R
        - text: B
        - text: . Thus the fibre-path congestion is at most
        - math:
          - generic: C
          - generic: R
          - generic: B
          - generic: s
          - generic: "0"
          - generic: +
          - generic: "2"
          - generic: D
          - generic: "0"
          - generic: +
          - generic: "1"
          - generic: .
        - text: C
        - generic: R
        - text: B
        - text: s
        - generic: "0"
        - text: "+2"
        - text: D
        - generic: "0"
        - text: "+1"
        - text: .
        - text: A lifted original canonical edge has elementary conductances at least
        - math:
          - generic: c
          - generic: R
          - generic: θ
          - generic: W
          - generic: −
          - generic: "2"
          - generic: D
          - generic: "0"
          - generic: (
          - generic: C
          - generic: R
          - generic: B
          - generic: )
          - generic: −
          - generic: "2"
          - generic: D
          - generic: "0"
        - text: c
        - generic: R
        - text: θ
        - text: W
        - text: −2
        - text: D
        - generic: "0"
        - text: (
        - text: C
        - generic: R
        - text: B
        - text: )
        - text: −2
        - text: D
        - generic: "0"
        - text: times its original conductance. The factor
        - math:
          - generic: g
        - generic: g
        - text: cancels against the primary-phase activity. Canonical-edge path overlap is bounded by the fixed channel list, because a fine state and the original channel label determine the corresponding canonical source.
        - listitem: Apply the original global Poincaré inequality and charge cutoff-crossing edges to the original Poisson tail.
      - paragraph: The exponent in (1) is a conservative bound dominating the resulting terms. This certificate neither enumerates a population ball nor assumes a local-ball spectral gap.
      - heading "Substitution into the density estimate" [level=3]
      - paragraph: Set
      - math:
        - generic: θ
        - generic: =
        - generic: (
        - generic: W
        - generic: ρ
        - generic: )
        - generic: −
        - generic: b
        - generic: θ
        - generic: ","
        - generic: B
        - generic: =
        - generic: C
        - generic: R
        - generic: ρ
        - generic: "2"
        - generic: ","
        - generic: W
        - generic: ≤
        - generic: ρ
        - generic: .
      - generic: θ =
      - text: (Wρ
      - text: )
      - text: −
      - text: b
      - generic: θ
      - text: ", B ="
      - text: C
      - generic: R
      - text: ρ
      - generic: "2"
      - text: ", W ≤"
      - generic: ρ.
      - paragraph: Then
      - math:
        - generic: A
        - generic: (
        - generic: B
        - generic: )
        - generic: ≤
        - generic: C
        - generic: R
        - generic: ρ
        - generic: a
        - generic: "0"
        - generic: ","
      - generic: A(B) ≤
      - text: C
      - generic: R
      - text: ρ
      - text: a
      - generic: "0"
      - text: ","
      - paragraph: where
      - math:
        - generic: a
        - generic: "0"
        - generic: =
        - generic: "2"
        - generic: b
        - generic: θ
        - generic: +
        - generic: p
        - generic: "0"
        - generic: +
        - generic: "2"
        - generic: D
        - generic: "0"
        - generic: +
        - generic: "2"
        - generic: (
        - generic: s
        - generic: "0"
        - generic: +
        - generic: "4"
        - generic: D
        - generic: "0"
        - generic: +
        - generic: "2"
        - generic: )
        - generic: .
      - text: a
      - generic: "0"
      - text: =
      - text: "2"
      - text: b
      - generic: θ
      - text: +
      - text: p
      - generic: "0"
      - text: +
      - text: "2"
      - text: D
      - generic: "0"
      - text: +
      - text: 2(
      - text: s
      - generic: "0"
      - text: +
      - text: "4"
      - text: D
      - generic: "0"
      - text: +
      - generic: 2).
      - paragraph:
        - text: For
        - math:
          - generic: "N"
          - generic: (
          - generic: u
          - generic: )
          - generic: ≤
          - generic: C
          - generic: R
          - generic: ρ
        - generic: N(u) ≤
        - text: C
        - generic: R
        - text: ρ
        - text: ", the canonical-anchor estimate gives"
      - math:
        - generic: −
        - generic: log
        - generic: ⁡
        - generic: μ
        - generic: "0"
        - generic: (
        - generic: u
        - generic: )
        - generic: ≤
        - generic: C
        - generic: R
        - generic: ρ
        - generic: "2"
        - generic: .
      - text: −
      - generic: log
      - text: μ
      - generic: "0"
      - text: (u) ≤
      - text: C
      - generic: R
      - text: ρ
      - generic: "2"
      - text: .
      - paragraph: The cutoff remainder satisfies
      - math:
        - generic: b
        - generic: (
        - generic: B
        - generic: )
        - generic: ≤
        - generic: C
        - generic: R
        - generic: exp
        - generic: ⁡
        - generic: ⁣
        - generic: (
        - generic: C
        - generic: R
        - generic: W
        - generic: "2"
        - generic: −
        - generic: c
        - generic: R
        - generic: B
        - generic: log
        - generic: ⁡
        - generic: B
        - generic: C
        - generic: R
        - generic: W
        - generic: )
        - generic: .
      - generic: b(B) ≤
      - text: C
      - generic: R
      - text: exp
      - generic: (
      - text: C
      - generic: R
      - text: W
      - generic: "2"
      - text: −
      - text: c
      - generic: R
      - text: B
      - generic: log
      - text: C
      - generic: R
      - text: W
      - generic: B
      - generic: )
      - text: .
      - paragraph: For the adjoint point density,
      - math:
        - generic: Var
        - generic: ⁡
        - generic: μ
        - generic: "0"
        - generic: f
        - generic: t
        - generic: ≤
        - generic: e
        - generic: −
        - generic: "2"
        - generic: t
        - generic: /
        - generic: A
        - generic: (
        - generic: B
        - generic: )
        - generic: μ
        - generic: "0"
        - generic: (
        - generic: u
        - generic: )
        - generic: −
        - generic: "1"
        - generic: +
        - generic: b
        - generic: (
        - generic: B
        - generic: )
        - generic: μ
        - generic: "0"
        - generic: (
        - generic: u
        - generic: )
        - generic: −
        - generic: "2"
        - generic: .
        - generic: (2)
      - generic: Var
      - text: μ
      - generic: "0"
      - text: f
      - generic: t
      - text: ≤
      - text: e
      - generic: −2t/A(B)
      - text: μ
      - generic: "0"
      - text: (u
      - text: )
      - generic: −1
      - text: +
      - text: b(B)
      - text: μ
      - generic: "0"
      - text: (u
      - text: )
      - generic: −2
      - text: .
      - text: (
      - generic: "2"
      - text: )
      - paragraph: At
      - math:
        - generic: T
        - generic: "0"
        - generic: =
        - generic: C
        - generic: R
        - generic: ρ
        - generic: a
        - generic: "0"
        - generic: +
        - generic: "20"
        - generic: ","
      - text: T
      - generic: "0"
      - text: =
      - text: C
      - generic: R
      - text: ρ
      - text: a
      - generic: "0"
      - text: "+20"
      - text: ","
      - paragraph:
        - text: the first term in (2) is smaller than any fixed inverse power of
        - math:
          - generic: ρ
        - generic: ρ
        - text: ", and the second term is also smaller than any fixed inverse power once"
        - math:
          - generic: ρ
        - generic: ρ
        - text: exceeds a computable structural threshold. In particular, increase the fixed coefficient if needed to obtain
      - math:
        - generic: sup
        - generic: ⁡
        - generic: "N"
        - generic: (
        - generic: u
        - generic: )
        - generic: ≤
        - generic: C
        - generic: R
        - generic: ρ
        - generic: TV
        - generic: ⁡
        - generic: (
        - generic: P
        - generic: T
        - generic: "0"
        - generic: "0"
        - generic: (
        - generic: u
        - generic: ","
        - generic: ⋅
        - generic: )
        - generic: ","
        - generic: μ
        - generic: "0"
        - generic: )
        - generic: ≤
        - generic: ρ
        - generic: −
        - generic: "10"
        - generic: .
        - generic: (3)
      - text: N(u)≤
      - text: C
      - generic: R
      - text: ρ
      - generic: sup
      - generic: TV
      - generic: (
      - text: P
      - text: T
      - generic: "0"
      - generic: "0"
      - text: (u, ⋅),
      - text: μ
      - generic: "0"
      - generic: )
      - text: ≤
      - text: ρ
      - generic: −10
      - text: .
      - text: (
      - generic: "3"
      - text: )
      - paragraph:
        - text: All quantities entering
        - math:
          - generic: a
          - generic: "0"
        - text: a
        - generic: "0"
        - text: are fixed before
        - math:
          - generic: J
        - generic: J
        - text: . The only
        - math:
          - generic: J
        - generic: J
        - text: "-dependence is in later constants and in the final choice of"
        - math:
          - generic: ρ
          - generic: =
          - generic: W
          - generic: a
        - generic: ρ =
        - text: W
        - generic: a
        - text: .
      - heading "All-late decoded means" [level=3]
      - paragraph:
        - text: Fine-state TV contraction gives (3) for every
        - math:
          - generic: t
          - generic: ≥
          - generic: T
          - generic: "0"
        - generic: t ≥
        - text: T
        - generic: "0"
        - text: . The near-
        - math:
          - generic: L
          - generic: "1"
        - text: L
        - generic: "1"
        - text: moment estimate from these initial states gives
      - math:
        - generic: sup
        - generic: ⁡
        - generic: t
        - generic: ≥
        - generic: "0"
        - generic: E
        - generic: u
        - generic: "N"
        - generic: t
        - generic: "2"
        - generic: ≤
        - generic: C
        - generic: R
        - generic: ρ
        - generic: "4"
        - generic: ","
        - generic: E
        - generic: μ
        - generic: "0"
        - generic: "N"
        - generic: "2"
        - generic: ≤
        - generic: C
        - generic: R
        - generic: ρ
        - generic: "4"
        - generic: .
      - generic: t≥0
      - generic: sup
      - text: E
      - generic: u
      - text: "N"
      - generic: t
      - generic: "2"
      - text: ≤
      - text: C
      - generic: R
      - text: ρ
      - generic: "4"
      - text: ","
      - text: E
      - text: μ
      - generic: "0"
      - text: "N"
      - generic: "2"
      - text: ≤
      - text: C
      - generic: R
      - text: ρ
      - generic: "4"
      - text: .
      - paragraph: Consequently, maximal coupling and Cauchy–Schwarz yield
      - math:
        - generic: max
        - generic: ⁡
        - generic: i
        - generic: ∣
        - generic: E
        - generic: u
        - generic: (
        - generic: D
        - generic: Z
        - generic: t
        - generic: )
        - generic: i
        - generic: −
        - generic: E
        - generic: μ
        - generic: "0"
        - generic: (
        - generic: D
        - generic: Z
        - generic: )
        - generic: i
        - generic: ∣
        - generic: ≤
        - generic: C
        - generic: R
        - generic: ρ
        - generic: "2"
        - generic: TV
        - generic: ⁡
        - generic: (
        - generic: P
        - generic: t
        - generic: "0"
        - generic: (
        - generic: u
        - generic: ","
        - generic: ⋅
        - generic: )
        - generic: ","
        - generic: μ
        - generic: "0"
        - generic: )
        - generic: ≤
        - generic: C
        - generic: R
        - generic: ρ
        - generic: −
        - generic: "3"
        - generic: ","
        - generic: t
        - generic: ≥
        - generic: T
        - generic: "0"
        - generic: .
      - generic: i
      - generic: max
      - text: ∣
      - text: E
      - generic: u
      - text: (D
      - text: Z
      - generic: t
      - text: )
      - generic: i
      - text: −
      - text: E
      - text: μ
      - generic: "0"
      - text: (DZ
      - text: )
      - generic: i
      - text: ∣
      - text: ≤
      - text: C
      - generic: R
      - text: ρ
      - generic: "2"
      - generic: TV
      - generic: (
      - text: P
      - generic: t
      - generic: "0"
      - text: (u, ⋅),
      - text: μ
      - generic: "0"
      - generic: )
      - text: ≤
      - text: C
      - generic: R
      - text: ρ
      - generic: −3
      - text: ", t ≥"
      - text: T
      - generic: "0"
      - text: .
      - paragraph:
        - text: Add the separate nominal static decoded-law and absolute-mean approximation to the conditional-Poisson target. This proves the required clean/reference estimate uniformly over every remaining deterministic lag in
        - math:
          - generic: "["
          - generic: T
          - generic: "0"
          - generic: ","
          - generic: S
          - generic: "]"
        - text: "["
        - text: T
        - generic: "0"
        - text: ", S]"
        - text: .
- status
- status

---

  - complementary:
    - heading "Subagents" [level=2]
    - button "Enter full view":
    - button "Close panel":
    - tabpanel "Subagents" [active]:
      - button "Back to subagents":
      - generic: Alternative elementary
      - heading "Status" [level=2]
      - generic: Done
      - heading "Final response" [level=2]
      - paragraph:
        - text: The hybrid fixed-window argument is valid. It avoids the adaptive clean-return problem entirely and gives uniform bounds at every deterministic
        - math:
          - generic: t
          - generic: ≥
          - generic: T
        - generic: t ≥
        - generic: T
        - text: .
      - heading "1. The hybrid is covered by the uniform controlled-moment theorem" [level=2]
      - paragraph:
        - text: Fix
        - math:
          - generic: t
          - generic: ≥
          - generic: T
        - generic: t ≥
        - generic: T
        - text: and put
        - math:
          - generic: a
          - generic: =
          - generic: t
          - generic: −
          - generic: T
        - generic: a =
        - generic: t −
        - generic: T
        - text: . Let
        - math:
          - generic: X
        - generic: X
        - text: be the actual controlled process. Construct
        - math:
          - generic: "Y"
        - generic: "Y"
        - text: to agree with
        - math:
          - generic: X
        - generic: X
        - text: through time
        - math:
          - generic: a
        - generic: a
        - text: ", and then use the nominal full-network rates."
      - paragraph:
        - text: "This is an admissible full-run policy: it uses the original predictable multipliers before"
        - math:
          - generic: a
        - generic: a
        - text: and the multipliers
        - math:
          - generic: "1"
        - generic: "1"
        - text: "afterward. Therefore the canonical uniform bound applies to both endpoints:"
      - math:
        - generic: E
        - generic: (
        - generic: "1"
        - generic: +
        - generic: "N"
        - generic: (
        - generic: X
        - generic: t
        - generic: )
        - generic: )
        - generic: "2"
        - generic: ≤
        - generic: B
        - generic: "2"
        - generic: ","
        - generic: E
        - generic: (
        - generic: "1"
        - generic: +
        - generic: "N"
        - generic: (
        - generic: "Y"
        - generic: t
        - generic: )
        - generic: )
        - generic: "2"
        - generic: ≤
        - generic: B
        - generic: "2"
        - generic: .
        - generic: (53)
      - generic: E(1 +
      - text: N(
      - text: X
      - generic: t
      - text: )
      - text: )
      - generic: "2"
      - text: ≤
      - text: B
      - generic: "2"
      - text: ", E(1 +"
      - text: N(
      - text: "Y"
      - generic: t
      - text: )
      - text: )
      - generic: "2"
      - text: ≤
      - text: B
      - generic: "2"
      - text: .
      - text: (
      - generic: "53"
      - text: )
      - paragraph:
        - text: Until their first marked mismatch,
        - math:
          - generic: X
        - generic: X
        - text: and
        - math:
          - generic: "Y"
        - generic: "Y"
        - text: have the same state. After physical normalization, the mismatch intensity is at most
      - math:
        - generic: δ
        - generic: ∑
        - generic: e
        - generic: k
        - generic: e
        - generic: (
        - generic: Z
        - generic: )
        - generic: α
        - generic: e
        - generic: ≤
        - generic: C
        - generic: R
        - generic: δ
        - generic: (
        - generic: "1"
        - generic: +
        - generic: "N"
        - generic: (
        - generic: Z
        - generic: )
        - generic: )
        - generic: "2"
        - generic: .
      - text: δ
      - generic: e
      - generic: ∑
      - text: k
      - generic: e
      - text: (Z
      - text: )
      - text: α
      - generic: e
      - text: ≤
      - text: C
      - generic: R
      - text: δ(1 +
      - text: N(Z)
      - text: )
      - generic: "2"
      - text: .
      - paragraph: Thus
      - math:
        - generic: p
        - generic: m
        - generic: i
        - generic: s
        - generic: ":"
        - generic: =
        - generic: P
        - generic: (
        - generic: X
        - generic: t
        - generic: ≠
        - generic: "Y"
        - generic: t
        - generic: )
        - generic: ≤
        - generic: C
        - generic: R
        - generic: δ
        - generic: B
        - generic: "2"
        - generic: T
        - generic: p
        - generic: h
        - generic: "y"
        - generic: s
        - generic: .
        - generic: (54)
      - text: p
      - generic: mis
      - text: :=
      - text: P(
      - text: X
      - generic: t
      - generic: 
      - text: =
      - text: "Y"
      - generic: t
      - text: ) ≤
      - text: C
      - generic: R
      - text: δ
      - text: B
      - generic: "2"
      - text: T
      - generic: phys
      - text: .
      - text: (
      - generic: "54"
      - text: )
      - paragraph: Null and parallel labels can be included in this coupling; flagging a mismatched null mark only makes the bound more conservative.
      - paragraph: For decoded means,
      - math:
        - generic: ∣
        - generic: E
        - generic: (
        - generic: D
        - generic: X
        - generic: t
        - generic: )
        - generic: i
        - generic: −
        - generic: E
        - generic: (
        - generic: D
        - generic: "Y"
        - generic: t
        - generic: )
        - generic: i
        - generic: ∣
        - generic: ≤
        - generic: C
        - generic: R
        - generic: B
        - generic: "2"
        - generic: p
        - generic: m
        - generic: i
        - generic: s
        - generic: .
        - generic: (55)
      - text: ∣E(D
      - text: X
      - generic: t
      - text: )
      - generic: i
      - text: − E(D
      - text: "Y"
      - generic: t
      - text: )
      - generic: i
      - text: ∣
      - text: ≤
      - text: C
      - generic: R
      - text: B
      - generic: "2"
      - text: p
      - generic: mis
      - text: .
      - text: (
      - generic: "55"
      - text: )
      - paragraph:
        - text: The estimates do not depend on the absolute time
        - math:
          - generic: t
        - generic: t
        - text: .
      - heading "2. The starting-state tail is paid by the unconditional hybrid moment" [level=2]
      - paragraph: Choose a cutoff
      - math:
        - generic: R
        - generic: "0"
        - generic: =
        - generic: ρ
        - generic: b
      - text: R
      - generic: "0"
      - text: =
      - text: ρ
      - generic: b
      - paragraph:
        - text: with
        - math:
          - generic: b
        - generic: b
        - text: fixed before
        - math:
          - generic: J
        - generic: J
        - text: . Uniform moments give
      - math:
        - generic: P
        - generic: (
        - generic: "N"
        - generic: (
        - generic: X
        - generic: a
        - generic: )
        - generic: ">"
        - generic: R
        - generic: "0"
        - generic: )
        - generic: ≤
        - generic: B
        - generic: "2"
        - generic: /
        - generic: R
        - generic: "0"
        - generic: "2"
        - generic: .
      - text: P(N(
      - text: X
      - generic: a
      - text: ) >
      - text: R
      - generic: "0"
      - text: ) ≤
      - text: B
      - generic: "2"
      - text: /
      - text: R
      - generic: "0"
      - generic: "2"
      - text: .
      - paragraph: Its endpoint contribution satisfies
      - math:
        - generic: E
        - generic: ⁣
        - generic: "["
        - generic: "N"
        - generic: (
        - generic: "Y"
        - generic: t
        - generic: )
        - generic: "1"
        - generic: "{"
        - generic: "N"
        - generic: (
        - generic: X
        - generic: a
        - generic: )
        - generic: ">"
        - generic: R
        - generic: "0"
        - generic: "}"
        - generic: "]"
        - generic: ≤
        - generic: B
        - generic: "2"
        - generic: /
        - generic: R
        - generic: "0"
        - generic: .
        - generic: (56)
      - text: E
      - generic: "["
      - text: N(
      - text: "Y"
      - generic: t
      - text: )
      - text: "1"
      - text: "{N("
      - text: X
      - generic: a
      - text: )>
      - text: R
      - generic: "0"
      - text: "}"
      - generic: "]"
      - text: ≤
      - text: B
      - generic: "2"
      - text: /
      - text: R
      - generic: "0"
      - text: .
      - text: (
      - generic: "56"
      - text: )
      - paragraph: This is the correct use of the hybrid moment. It does not assume that the nominal process started from a rare large state has a small conditional endpoint moment.
      - paragraph:
        - text: Taking
        - math:
          - generic: b
        - generic: b
        - text: above the exponent in
        - math:
          - generic: B
          - generic: "2"
        - text: B
        - generic: "2"
        - text: ", with a fixed margin, makes both the TV and absolute-mean tail contributions small."
      - heading "3. Only nominal clean return is needed inside the cutoff" [level=2]
      - paragraph:
        - text: Conditional on
        - math:
          - generic: X
          - generic: a
          - generic: =
          - generic: u
        - text: X
        - generic: a
        - text: =
        - generic: u
        - text: ", the future"
        - math:
          - generic: "Y"
        - generic: "Y"
        - text: is the nominal full process from
        - math:
          - generic: u
        - generic: u
        - text: . Suppose
      - math:
        - generic: E
        - generic: u
        - generic: τ
        - generic: C
        - generic: ≤
        - generic: C
        - generic: J
        - generic: ρ
        - generic: "7"
        - generic: J
        - generic: +
        - generic: E
        - generic: (
        - generic: "1"
        - generic: +
        - generic: "N"
        - generic: (
        - generic: u
        - generic: )
        - generic: )
        - generic: q
        - generic: ","
      - text: E
      - generic: u
      - text: τ
      - generic: C
      - text: ≤
      - text: C
      - generic: J
      - text: ρ
      - generic: 7J+E
      - text: (1 +
      - text: N(u)
      - text: )
      - generic: q
      - text: ","
      - paragraph:
        - text: with
        - math:
          - generic: E
          - generic: ","
          - generic: q
        - generic: E, q
        - text: fixed before
        - math:
          - generic: J
        - generic: J
        - text: .
      - paragraph:
        - text: For
        - math:
          - generic: "N"
          - generic: (
          - generic: u
          - generic: )
          - generic: ≤
          - generic: R
          - generic: "0"
        - generic: N(u) ≤
        - text: R
        - generic: "0"
        - text: ", choose"
      - math:
        - generic: T
        - generic: r
        - generic: a
        - generic: w
        - generic: =
        - generic: ρ
        - generic: "7"
        - generic: J
        - generic: +
        - generic: D
        - generic: .
      - text: T
      - generic: raw
      - text: =
      - text: ρ
      - generic: 7J+D
      - text: .
      - paragraph: Then
      - math:
        - generic: P
        - generic: u
        - generic: (
        - generic: τ
        - generic: C
        - generic: ">"
        - generic: T
        - generic: r
        - generic: a
        - generic: w
        - generic: −
        - generic: T
        - generic: "0"
        - generic: )
        - generic: ≤
        - generic: C
        - generic: J
        - generic: ρ
        - generic: E
        - generic: +
        - generic: b
        - generic: q
        - generic: −
        - generic: D
        - generic: ","
        - generic: (57)
      - text: P
      - generic: u
      - text: (
      - text: τ
      - generic: C
      - text: ">"
      - text: T
      - generic: raw
      - text: −
      - text: T
      - generic: "0"
      - text: ) ≤
      - text: C
      - generic: J
      - text: ρ
      - generic: E+bq−D
      - text: ","
      - text: (
      - generic: "57"
      - text: )
      - paragraph:
        - text: provided
        - math:
          - generic: T
          - generic: r
          - generic: a
          - generic: w
          - generic: ≥
          - generic: "2"
          - generic: T
          - generic: "0"
        - text: T
        - generic: raw
        - text: ≥
        - text: "2"
        - text: T
        - generic: "0"
        - text: .
      - paragraph:
        - text: Let
        - math:
          - generic: E
          - generic: c
          - generic: a
          - generic: p
        - text: E
        - generic: cap
        - text: be a pre-
        - math:
          - generic: J
        - generic: J
        - text: exponent bounding the nominal second moment uniformly over all times and all starts with
        - math:
          - generic: "N"
          - generic: (
          - generic: u
          - generic: )
          - generic: ≤
          - generic: R
          - generic: "0"
        - generic: N(u) ≤
        - text: R
        - generic: "0"
        - text: ":"
      - math:
        - generic: sup
        - generic: ⁡
        - generic: s
        - generic: ≥
        - generic: "0"
        - generic: ","
        - generic: "N"
        - generic: (
        - generic: u
        - generic: )
        - generic: ≤
        - generic: R
        - generic: "0"
        - generic: E
        - generic: u
        - generic: (
        - generic: "1"
        - generic: +
        - generic: "N"
        - generic: (
        - generic: Z
        - generic: s
        - generic: )
        - generic: )
        - generic: "2"
        - generic: ≤
        - generic: C
        - generic: J
        - generic: ρ
        - generic: E
        - generic: c
        - generic: a
        - generic: p
        - generic: .
      - text: s≥0,
      - text: N(u)≤
      - text: R
      - generic: "0"
      - generic: sup
      - text: E
      - generic: u
      - text: (1 +
      - text: N(
      - text: Z
      - generic: s
      - text: )
      - text: )
      - generic: "2"
      - text: ≤
      - text: C
      - generic: J
      - text: ρ
      - text: E
      - generic: cap
      - text: .
      - paragraph: Choose, for example,
      - math:
        - generic: D
        - generic: ">"
        - generic: E
        - generic: +
        - generic: b
        - generic: q
        - generic: +
        - generic: E
        - generic: c
        - generic: a
        - generic: p
        - generic: +
        - generic: "10"
        - generic: ","
      - generic: D >
      - generic: E +
      - generic: bq +
      - text: E
      - generic: cap
      - text: +
      - generic: 10,
      - paragraph:
        - text: and also large enough to dominate the fixed exponent in
        - math:
          - generic: T
          - generic: "0"
        - text: T
        - generic: "0"
        - text: . Then the late-clean-hit contribution to absolute means is small by Cauchy–Schwarz.
      - paragraph:
        - text: This uses the old
        - strong: nominal
        - text: clean-return result. No adaptive version of its hitting potential is needed.
      - heading "4. The remaining interval starts clean and has a deterministic conditional length" [level=2]
      - paragraph: "On"
      - math:
        - generic: "{"
        - generic: τ
        - generic: C
        - generic: ≤
        - generic: T
        - generic: r
        - generic: a
        - generic: w
        - generic: −
        - generic: T
        - generic: "0"
        - generic: "}"
        - generic: ","
      - text: "{"
      - text: τ
      - generic: C
      - text: ≤
      - text: T
      - generic: raw
      - text: −
      - text: T
      - generic: "0"
      - text: "},"
      - paragraph: the remaining duration
      - math:
        - generic: s
        - generic: =
        - generic: T
        - generic: r
        - generic: a
        - generic: w
        - generic: −
        - generic: τ
        - generic: C
      - generic: s =
      - text: T
      - generic: raw
      - text: −
      - text: τ
      - generic: C
      - paragraph:
        - text: is measurable at the clean stopping time and lies in
        - math:
          - generic: "["
          - generic: T
          - generic: "0"
          - generic: ","
          - generic: T
          - generic: r
          - generic: a
          - generic: w
          - generic: "]"
        - text: "["
        - text: T
        - generic: "0"
        - text: ","
        - text: T
        - generic: raw
        - text: "]"
        - text: .
      - paragraph:
        - text: From that clean state, couple the nominal full process to the passive nominal reference. The reference base is accurate in law and absolute means uniformly for every
        - math:
          - generic: s
          - generic: ≥
          - generic: T
          - generic: "0"
        - generic: s ≥
        - text: T
        - generic: "0"
        - text: . The probability of a physical intervention during the remaining interval is at most
      - math:
        - generic: C
        - generic: J
        - generic: η
        - generic: J
        - generic: T
        - generic: r
        - generic: a
        - generic: w
        - generic: W
        - generic: "2"
        - generic: J
        - generic: +
        - generic: "3"
        - generic: (
        - generic: "1"
        - generic: +
        - generic: log
        - generic: ⁡
        - generic: ρ
        - generic: )
        - generic: J
        - generic: +
        - generic: "2"
        - generic: =
        - generic: C
        - generic: J
        - generic: ρ
        - generic: D
        - generic: −
        - generic: J
        - generic: W
        - generic: "2"
        - generic: J
        - generic: +
        - generic: "3"
        - generic: (
        - generic: "1"
        - generic: +
        - generic: log
        - generic: ⁡
        - generic: ρ
        - generic: )
        - generic: J
        - generic: +
        - generic: "2"
        - generic: .
        - generic: (58)
      - text: C
      - generic: J
      - text: η
      - generic: J
      - text: T
      - generic: raw
      - text: W
      - generic: 2J+3
      - text: (1 +
      - generic: log
      - text: ρ
      - text: )
      - generic: J+2
      - text: =
      - text: C
      - generic: J
      - text: ρ
      - generic: D−J
      - text: W
      - generic: 2J+3
      - text: (1 +
      - generic: log
      - text: ρ
      - text: )
      - generic: J+2
      - text: .
      - text: (
      - generic: "58"
      - text: )
      - paragraph:
        - text: The nominal full-process second moment from
        - math:
          - generic: C
        - generic: C
        - text: ", uniform over all times, pays the intervention contribution to absolute means."
      - paragraph:
        - text: Therefore choose
        - math:
          - generic: J
        - generic: J
        - text: after
        - math:
          - generic: D
        - generic: D
        - text: ", larger than"
        - math:
          - generic: D
        - generic: D
        - text: plus the clean-start second-moment exponent and a fixed margin. Then choose the outer power in
        - math:
          - generic: ρ
          - generic: =
          - generic: W
          - generic: a
        - generic: ρ =
        - text: W
        - generic: a
        - text: sufficiently large to pay the
        - math:
          - generic: W
        - generic: W
        - text: and logarithmic factors in (58).
      - paragraph: "There is no conditioning-on-no-intervention error: compare unconditionally from the clean stopping time and charge the bad event through the coupling."
      - heading "5. Parameter order is noncircular" [level=2]
      - paragraph: "A valid order is:"
      - list:
        - listitem: Prove the uniform controlled-moment bounds, including arbitrary-initial-state bounds.
        - text: Fix the starting cutoff exponent
        - math:
          - generic: b
        - generic: b
        - text: .
        - text: Determine
        - math:
          - generic: E
          - generic: c
          - generic: a
          - generic: p
        - text: E
        - generic: cap
        - text: and choose
        - math:
          - generic: D
        - generic: D
        - text: .
        - text: Choose
        - math:
          - generic: J
          - generic: ">"
          - generic: D
          - generic: +
        - generic: J >
        - generic: D+
        - text: the remaining fixed moment exponents.
        - text: Choose the outer population/accuracy power
        - math:
          - generic: a
        - generic: a
        - text: in
        - math:
          - generic: ρ
          - generic: =
          - generic: W
          - generic: a
        - generic: ρ =
        - text: W
        - generic: a
        - text: .
        - text: Choose
        - math:
          - generic: δ
        - generic: δ
        - text: small enough for (54)–(55), including physical clock normalization.
      - paragraph: For example, if
      - math:
        - generic: B
        - generic: "2"
        - generic: ≤
        - generic: C
        - generic: J
        - generic: ρ
        - generic: Q
        - generic: "2"
        - generic: ","
        - generic: T
        - generic: p
        - generic: h
        - generic: "y"
        - generic: s
        - generic: ≤
        - generic: C
        - generic: J
        - generic: ρ
        - generic: "7"
        - generic: J
        - generic: +
        - generic: D
        - generic: +
        - generic: A
        - generic: max
        - generic: ⁡
        - generic: ","
      - text: B
      - generic: "2"
      - text: ≤
      - text: C
      - generic: J
      - text: ρ
      - text: Q
      - generic: "2"
      - text: ","
      - text: T
      - generic: phys
      - text: ≤
      - text: C
      - generic: J
      - text: ρ
      - text: 7J+D+
      - text: A
      - generic: max
      - text: ","
      - paragraph: a tolerance of order
      - math:
        - generic: δ
        - generic: =
        - generic: ρ
        - generic: −
        - generic: (
        - generic: "7"
        - generic: J
        - generic: +
        - generic: D
        - generic: +
        - generic: A
        - generic: max
        - generic: ⁡
        - generic: +
        - generic: "2"
        - generic: Q
        - generic: "2"
        - generic: +
        - generic: "10"
        - generic: )
      - generic: δ =
      - text: ρ
      - text: −(7J+D+
      - text: A
      - generic: max
      - text: "+2"
      - text: Q
      - generic: "2"
      - text: +10)
      - paragraph: is more than sufficient after enlarging the final fixed constants. It remains a polynomial numerical tolerance.
      - heading "6. Frozen stationary robustness follows without a separate localization theorem" [level=2]
      - paragraph: For frozen multipliers, uniform full-population moments make the Cesàro laws tight. On the countable fine class, a tight convergent subsequence converges in TV. The identity
      - math:
        - generic: ∥
        - generic: μ
        - generic: t
        - generic: P
        - generic: s
        - generic: −
        - generic: μ
        - generic: t
        - generic: ∥
        - generic: T
        - generic: V
        - generic: ≤
        - generic: "2"
        - generic: s
        - generic: /
        - generic: t
      - text: ∥
      - text: μ
      - generic: t
      - text: P
      - generic: s
      - text: −
      - text: μ
      - generic: t
      - text: ∥
      - generic: TV
      - text: ≤
      - generic: 2s/t
      - paragraph: then gives an invariant probability. Irreducibility gives positive recurrence and uniqueness.
      - paragraph: The all-late decoded TV bounds pass to this invariant law by averaging. The absolute-mean bounds pass using the uniform second moment. Thus the new fixed-window proof can replace the earlier stationary cycle-ratio argument in the final dependency chain.
      - paragraph:
        - strong: I found no remaining logical gap in this hybrid closure
        - text: ", provided the newly audited uniform controlled moments hold for the full fine population and the stated nominal clean-return estimate applies to all fine states in the communicating class. Those are precisely the hypotheses you identified."
- status
- status

---

  - complementary:
    - heading "Subagents" [level=2]
    - button "Enter full view":
    - button "Close panel":
    - tabpanel "Subagents" [active]:
      - button "Back to subagents":
      - generic: Obstructions
      - heading "Status" [level=2]
      - generic: Done
      - heading "Final response" [level=2]
      - paragraph:
        - text: "One final scope qualification: the return and “arbitrary initial state” estimates should apply to"
        - strong:
          - text: states in the preserved fine communicating class of the compiled
          - math:
            - generic: x
            - generic: "0"
          - text: x
          - generic: "0"
        - text: . That is sufficient for every use in the hybrid and stationary arguments.
      - paragraph:
        - text: "They should not be stated for every fine state in every other communicating class without further proof: a different class could conserve a large"
        - math:
          - generic: V
        - generic: V
        - text: ", making any"
        - math:
          - generic: V
        - generic: V
        - text: "-change service event impossible. This does not affect the proposed closure when the class restriction is explicit."
      - paragraph:
        - text: With that qualification, the clarified structural hypotheses, and the explicit common
        - math:
          - generic: F
          - generic: h
        - text: F
        - generic: h
        - text: ", I have no remaining algebraic or probabilistic objection to the closure audited here."
- status
- status

Stationary obstructions panel reported “No final response is available.” Earlier chat-wide helper material is available in the previous P3 D257E8 handoff.
