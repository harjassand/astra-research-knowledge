**Yes. The full open-network, variable-order contract has an affirmative construction.** One may take, for example, the universal constants
\[
\boxed{C=2^{4096},\qquad p=256.}
\]
These constants are deliberately loose.

The additional physical mechanism is simple: each nonempty-source label gets a pending species carrying its actual source population. Binary collision reactions return pending molecules to their source representatives. A bounded credit function then controls the expected number of **all original-labelled completions**, uniformly under predictable faults. Two pathwise counting identities charge every assembly, release and collision return.

This provides the global cost bound independently of the original drift promise. The promise is used to control the target process’s escape probability during the finite-horizon path comparison.

Below is the construction and proof.

## 1. Species, decoder and physical reactions

Write
\[
m=|R|,\qquad q_r=|y_r|_1,\qquad q_r'=|z_r|_1.
\]
If \(m=0\), emit only the original species, no channels, \(P=I\), \(H=1\) and \(\delta=1/2\). All conclusions are immediate. Henceforth assume \(m\ge1\).

Order each complex’s explicitly listed molecules deterministically, for example by species index.

### Private prefix species

For each label \(r\), create:

- A private source-prefix species \(S_{r,j}\) for every \(2\le j\le q_r\).
- A separate private product-prefix species \(T_{r,j}\) for every \(2\le j\le q_r'\).
- A pending species \(C_r\) whenever \(q_r>0\).

All these species are distinct, including when their decoded populations coincide. In particular, source and product chains remain separate for a null original reaction.

The decoder sends a prefix to the multiset of its first \(j\) original molecules, and
\[
PC_r=y_r.
\]
It is the identity on original species.

Define the representatives
\[
s_r=
\begin{cases}
\text{the original source species},&q_r=1,\\
S_{r,q_r},&q_r\ge2,
\end{cases}
\]
and
\[
t_r=
\begin{cases}
\varnothing,&q_r'=0,\\
\text{the original product species},&q_r'=1,\\
T_{r,q_r'},&q_r'\ge2.
\end{cases}
\]

Every decoder column is nonzero. If \(S\) is any fine species, put
\[
d_S=|PS|_1.
\]
Then
\[
1\le d_S\le D.
\]

For a fine state \(u\), use the three distinct population quantities
\[
n(u)=|u|_1,\qquad V(u)=|Pu|_1,\qquad N(Pu)=\omega\cdot Pu.
\]
They satisfy
\[
n(u)\le V(u)\le N(Pu).
\tag{1}
\]

### Prefix assembly and release

Each private chain has the usual reversible binary steps:
\[
A_{i_1}+A_{i_2}\rightleftarrows S_{r,2},
\qquad
S_{r,j-1}+A_{i_j}\rightleftarrows S_{r,j},
\]
and likewise for its product chain.

These are hidden channels.

### Pending initiation, return and completion

For every \(q_r>0\), add the hidden pair
\[
s_r\rightleftarrows C_r
\]
and the observed channel
\[
C_r\longrightarrow t_r
\quad\text{with label }r.
\tag{2}
\]

For \(q_r=0\), use the observed channel
\[
\varnothing\longrightarrow t_r
\quad\text{with label }r.
\tag{3}
\]

Thus \(0\to0\) remains an actual marked null channel. Every other original null or parallel label is also retained as its own observed channel.

### Binary collision returns

For every \(r\) with \(q_r>0\), and every fine species \(S\), add
\[
\boxed{C_r+S\longrightarrow s_r+S.}
\tag{4}
\]
These channels are hidden.

Every reaction in the emitted network has at most two molecules on each side. All auxiliary species carry actual original population, and all auxiliary populations initially equal zero.

Let
\[
S_{\mathrm p}
=\sum_r(q_r-1)_++\sum_r(q_r'-1)_+,
\qquad
m_+=|\{r:q_r>0\}|.
\]
The numbers of fine species and labelled channels are
\[
s=d+S_{\mathrm p}+m_+,
\qquad
m_f=2S_{\mathrm p}+2m_++m+m_+s.
\tag{5}
\]
The entire structure, decoder and label map depend only on \(R\).

## 2. Exact directed-graph preservation

Every hidden channel preserves \(P\).

If an observed channel with label \(r\) is enabled, then either \(q_r=0\), or its state contains a \(C_r\) molecule carrying \(y_r\). Consequently
\[
Pu\ge y_r,
\]
and its decoded increment is exactly \(z_r-y_r\).

Every fine state can reach its canonical encoding by hidden reactions: return all pending molecules, then release all prefixes. All these baseline hidden steps are reversible. Therefore
\[
u\;\longleftrightarrow\;j(Pu)
\tag{6}
\]
within the hidden graph.

Given an enabled original edge \(x\xrightarrow{r}x-y_r+z_r\), its canonical lift assembles the private source, enters \(C_r\), fires (2), and releases the product. For a zero source, use (3) and release its product.

It follows that, for **all** fine states,
\[
\boxed{u\leadsto v\quad\Longleftrightarrow\quad Pu\leadsto Pv.}
\tag{7}
\]
This proves both directed reachability and exact communicating-class preimages. The hidden release paths establish a graph property; they are not externally executed resets.

## 3. Explicit compiler parameters and rates

Use the question’s \(B,\Gamma_B\), and set
\[
U=1+B,\qquad \Gamma=\Gamma_B,\qquad k_*=\min_r k_r.
\]
Define
\[
C_{\mathrm f}
=16(D+1)^2\left[1+\left(\frac{\Gamma}{k_*}\right)^2\right],
\qquad
F=(D+1)\Gamma+2Dm,
\]
followed by
\[
\begin{aligned}
Q={}&1+4096(1+m)U^3C_{\mathrm f}
       +128\epsilon^{-1}F\Gamma(1+\tau),\\
\theta={}&Q^{-1},\\
\Lambda={}&m+QU,\\
K={}&1+Q+
512\epsilon^{-1}BC_{\mathrm f}\Lambda(1+\Lambda\tau),\\
\eta={}&\frac{\epsilon}{128U^2(1+\tau)},\\
H={}&1+KU+Q+\eta D,\\
\delta={}&\frac{\epsilon}{128m_fU^2(1+H\tau)}.
\end{aligned}
\tag{8}
\]

First assign **raw** coefficients \(\kappa_e\) as follows.

| Channel type | Raw forward coefficient | Raw reverse coefficient |
|---|---:|---:|
| First source-prefix assembly, \(q_r\ge2\) | \(K\theta k_rU^{2-q_r}\) | \(K\) |
| Later source-prefix assembly | \(KU\) | \(K\) |
| First product-prefix assembly | \(K\theta U^{-2}\) | \(K\) |
| Later product-prefix assembly | \(K/U\) | \(K\) |
| \(s_r\rightleftarrows C_r,\ q_r\ge2\) | \(K\) | \(K\) |
| \(s_r\rightleftarrows C_r,\ q_r=1\) | \(K\theta k_r\) | \(K\) |
| Observed \(C_r\to t_r\) | \(Q\) | — |
| Observed \(\varnothing\to t_r\) | \(k_r\) | — |
| Hidden \(C_r+S\to s_r+S\) | \(\eta d_S\) | — |

All propensities use the stipulated falling-factorial convention, without inserting symmetry factors.

Output
\[
\boxed{c_e=\kappa_e/H.}
\tag{9}
\]
The formulas imply \(\theta m\le1\). Every raw coefficient is at most
\[
\max\{KU,Q,\eta D,1\}<H.
\]
Thus \(0<c_e\le1\), and \(0<\delta<1/2\).

All parameters are rational and computed by ordinary exact rational arithmetic.

## 4. Nonexplosion under every predictable fault rule

The following global arguments work for the larger multiplier box
\[
\frac12\le a_e(t)\le\frac32.
\tag{10}
\]

Physical population increases only through:

- Unary prefix releases, each increasing it by one.
- Zero-source observed channels, each increasing it by at most one.

There is one release channel per prefix species. After normalization, its coefficient is \(K/H\le1\). Hence the total positive-population-jump intensity is bounded by
\[
\frac32\bigl(n(Z_t)+m\bigr).
\tag{11}
\]

A pure-birth process with immigration therefore dominates positive population growth. At bounded population, the sum of all marked intensities is bounded by
\[
\frac32m_f(1+n)^2.
\]
These facts prove nonexplosion, including hidden and null firings, and provide finite moments on every bounded time interval for the localization arguments below.

The stronger polynomial-in-time estimates come from the next two steps.

## 5. A common bounded credit controls all observed completions

This is the global estimate that pays for rare excursions.

Put
\[
G=\frac32Q,
\qquad
\chi_r(v)=
\frac{G}{G+K/2+(\eta/2)(v-q_r)_+}
\quad(q_r>0),
\]
and define
\[
\Psi(u)=\sum_{r:q_r>0}u_{C_r}\chi_r(V(u)).
\tag{12}
\]
This is one fixed state function, independent of the fault history.

For \(v\ge2D\),
\[
\chi_r(v)\le\frac{4G}{\eta v}.
\]
For \(v<2D\), use \(\chi_r(v)\le1\). Since the number of pending molecules is at most \(V(u)\),
\[
\boxed{
0\le\Psi(u)\le S_0:=2D+\frac{4G}{\eta}.
}
\tag{13}
\]
Canonical initialization gives \(\Psi(j(x_0))=0\).

For this calculation, let \(\mathcal L_{\mathbf a}^{\rm raw}\) denote the instantaneous generator with coefficients \(\kappa_ea_e\), before division by \(H\). Write
\[
b(u,\mathbf a)
=\sum_{r:q_r>0}Qa_r\,u_{C_r}
\tag{14}
\]
for its total nonempty-source observed intensity. Every null and parallel label is included.

### The credit of the completing or returning molecule

The nominal collision-return intensity targeting \(C_r\) is exactly
\[
\eta u_{C_r}\bigl(V(u)-q_r\bigr).
\tag{15}
\]
For \(S=C_r\), falling factorials give
\[
\eta q_r u_{C_r}(u_{C_r}-1),
\]
which supplies precisely the self-exclusion in (15). Under faults, the per-pending-molecule return hazard is at least
\[
K/2+\frac{\eta}{2}(V-q_r).
\]

If \(g\le G\) is the actual completion rate per pending molecule and \(u\) is its total return rate, then
\[
g(1-\chi_r)-u\chi_r\le0.
\tag{16}
\]
Therefore its own removal contributes at most minus its actual completion intensity to the credit drift.

No observed completion creates a pending species: product representatives are original species or private product-prefix species.

### Initiation credit

Private source representatives of order at least two each initiate at raw coefficient \(K\). For each original unary species, the sum of its initiation coefficients is at most
\[
K\theta\sum_r k_r\le K\theta m\le K.
\]
Thus total initiation intensity under faults is at most \(3KV\), and its credit influx is at most
\[
3KS_0.
\tag{17}
\]

### Changes in the other pending molecules’ credits

A completion changes \(V\) by
\[
|z_r|_1-|y_r|_1,
\]
whose absolute value is at most \(D\).

An increase of \(V\) decreases every other credit. Zero-source births have the same favorable property.

For a decrease of \(V\), assume first that \(V\ge4D\). Throughout the intervening interval,
\[
|\chi_r'(v)|\le\frac{8G}{\eta V^2}.
\]
There are at most \(V\) remaining pending molecules, so their total credit increase per completion is at most
\[
\frac{8GD}{\eta V}.
\tag{18}
\]

Set
\[
R_*=1+4D+\frac{32GD}{\eta},
\qquad
C_0=3KS_0+GR_*^2.
\tag{19}
\]
Above \(R_*\), (18) is at most \(1/4\) per completion. Below \(R_*\), a completion increases other credits by at most \(R_*\), while
\[
b(u,\mathbf a)\le GV\le GR_*.
\]

Combining these estimates gives the pointwise inequality
\[
\boxed{
\mathcal L_{\mathbf a}^{\rm raw}\Psi
\le C_0-\frac12 b(u,\mathbf a)
}
\tag{20}
\]
for every state and every multiplier vector in (10).

Because (20) holds pointwise, it remains valid for arbitrary predictable, history-dependent multipliers.

### Consequences in physical time

Let \(J_+(t)\) count all nonempty-source observed firings, and \(J_0(t)\) all zero-source observed firings. Dividing (20) by \(H\), applying Dynkin’s formula and using \(\Psi\ge0\) yields
\[
\mathbb E J_+(t)\le \frac{2C_0}{H}t.
\tag{21}
\]
Also,
\[
\mathbb E J_0(t)\le\frac{3m}{2H}t.
\tag{22}
\]

Hidden channels preserve \(V\), and each observed firing increases it by at most \(D\). Pathwise,
\[
\sup_{s\le t}V(Z_s)
\le |x_0|_1+D\bigl(J_+(t)+J_0(t)\bigr).
\]
Consequently,
\[
\boxed{
\mathbb E\sup_{s\le t}(1+|Z_s|_1)
\le
1+|x_0|_1+
\frac{D(2C_0+3m/2)}H\,t.
}
\tag{23}
\]

This bound holds throughout the actual, untruncated run.

## 6. An exact budget pays for every fine firing

Let the following count actual physical firings up to time \(t\):

- \(\mathsf A,\mathsf R\): prefix assemblies and releases.
- \(\mathsf I,\mathsf U,\mathsf J,\mathsf C\): pending initiations, baseline returns, collision returns and nonempty-source observed completions.
- \(\mathsf F_0\): zero-source observed firings.

Zero-auxiliary initialization gives the exact pending-count identity
\[
\sum_r Z_{C_r}(t)
=\mathsf I-\mathsf U-\mathsf J-\mathsf C\ge0.
\]
Hence
\[
\mathsf I+\mathsf U+\mathsf J+\mathsf C\le2\mathsf I.
\tag{24}
\]

Each prefix assembly decreases physical population by one, and each release increases it by one. Pending transitions and collision returns preserve physical population. Nonempty-source completions never increase it; zero-source firings increase it by at most one. Thus
\[
\mathsf A\le |x_0|_1+\mathsf R+\mathsf F_0.
\tag{25}
\]

If \(\mathsf F_{\rm all}(t)\) counts **all** fine firings, (24)–(25) give
\[
\boxed{
\mathsf F_{\rm all}(t)
\le |x_0|_1+2\mathsf R(t)+2\mathsf I(t)+2\mathsf F_0(t).
}
\tag{26}
\]

Both release and initiation intensities are at most
\[
\frac{3K}{2H}n(Z_t).
\]
Therefore
\[
\boxed{
\mathbb E\mathsf F_{\rm all}(t)
\le |x_0|_1+
\frac{6K}{H}\int_0^t\mathbb E V(Z_s)\,ds+
\frac{3m}{H}t.
}
\tag{27}
\]
Together with (23), this is a quadratic-in-time bound.

In particular, the quadratic mass-action intensities of assemblies and collision returns require no second-moment assumption. Their counts are paid by the pathwise budget (26).

## 7. The nominal hidden-fibre law and averaged intensities

For the accuracy proof, define a reference process with the same raw rates but with collision returns (4) omitted. This is an analytical comparison process; every emitted collision-return channel remains present with its positive coefficient.

Temporarily consider only the reference hidden reactions within \(Pu=x\). Assign original species activity \(1\), and auxiliary activities
\[
\begin{aligned}
w(S_{r,j})&=\theta k_rU^{j-q_r},\\
w(T_{r,j})&=\theta U^{-j},\\
w(C_r)&=\theta k_r.
\end{aligned}
\tag{28}
\]
The raw hidden rates are detailed balanced with these activities.

Let \(a\) be the auxiliary population vector, \(E\) its decoder matrix, and \(v=x-Ea\) the free-original population. Define
\[
q(x)=\sum_{Ea\le x}\frac{w^a(x)_{Ea}}{a!}.
\tag{29}
\]
The unique hidden-fibre invariant law is
\[
\nu_x(v,a)
=\frac{x!}{q(x)}\frac{w^a}{v!\,a!}.
\tag{30}
\]
Finiteness and irreducibility of each fibre follow from (1) and the hidden release paths. Neither \(q(x)\) nor \(\nu_x\) is computed by the compiler.

The exact pending marginal identity is
\[
\mathbb E_{\nu_x}C_r
=\theta k_r(x)_{y_r}\frac{q(x-y_r)}{q(x)}.
\]
Since the observed completion coefficient is \(Q=\theta^{-1}\),
\[
\boxed{
\bar\lambda_r(x)
=k_r(x)_{y_r}\frac{q(x-y_r)}{q(x)}.
}
\tag{31}
\]
For a zero source, this formula also holds, with ratio \(1\).

### Uniform partition bound below the cutoff

Whenever \(N(x)<B\), one has \(|x|_1<B\). Expanding the exponential gives
\[
q(x)\le
\exp\!\left(\sum_S w(S)B^{d_S}\right).
\]

For a source prefix,
\[
w(S_{r,j})B^j
\le \theta k_rU^{2j-q_r}
\le \theta k_rU^{q_r}.
\]
All source prefixes therefore contribute at most \(\theta D\Gamma\). Product prefixes contribute at most \(\theta Dm\), and pending species at most \(\theta\Gamma\). Thus
\[
\boxed{1\le q(x)\le e^{\theta F},\qquad N(x)<B.}
\tag{32}
\]

Our choice of \(Q\) ensures \(\theta F\le1\), so
\[
|\bar\lambda_r(x)-\lambda_r(x)|
\le2\theta F\,\lambda_r(x).
\tag{33}
\]
The total original intensity below the cutoff is at most \(\Gamma\). Marked common-intensity coupling consequently bounds the stopped averaged-versus-original path discrepancy by
\[
2\theta F\Gamma\tau\le\epsilon/64.
\tag{34}
\]

## 8. Uniform fibre mixing with variable reaction order

The order-dependent release estimate is paid by \(\Gamma\) for source chains and by a polynomial in \(D\) for product chains.

### Tagged source lineage

For a source of order \(q\ge2\), assign depths
\[
1=S_{r,2},\ldots,q-1=S_{r,q},\qquad q=C_r,
\]
with depth zero meaning complete release.

The downward rate is \(K\). Prefix upward rates are at most \(KUB\le KU^2\), and the final prefix-to-pending rate is \(K\).

A reflecting birth–death chain on \(\{0,\ldots,q\}\), absorbed at zero, with downward rate \(K\) and upward rate \(Ku\), \(u=U^2\), dominates its release time. Its mean absorption time from the top is
\[
\frac1K\sum_{j=0}^{q-1}(q-j)u^j
\le\frac{q^2U^{2q-2}}K.
\]
But
\[
\Gamma\ge k_rU^q,\qquad U^q\le\Gamma/k_*.
\]
Hence the source-lineage mean release time is at most \(C_{\mathrm f}/K\).

### Product and unary lineages

For a product chain, upward rates are at most
\[
(K/U)B\le K.
\]
Its mean release time is at most \(D^2/K\), irrespective of whether any source has comparable order. A unary pending molecule releases in mean time \(1/K\).

Thus every initially present auxiliary lineage has mean release time at most
\[
C_{\mathrm f}/K.
\tag{35}
\]

### A canonical atom

New lineages arise only from first prefix bindings and unary-source pending initiations. Their total nominal intensity below the cutoff is at most
\[
4K\theta mU^2.
\]

Set
\[
h=\frac{16BC_{\mathrm f}}K.
\tag{36}
\]
There are at most \(B\) initially present auxiliary lineages. By (35), the probability that any survives until \(h\) is at most \(1/16\).

The probability of any new lineage during the interval is at most
\[
4K\theta mU^2h
=64\theta mBU^2C_{\mathrm f}
\le1/64.
\]
Therefore, from every fine encoding of every \(x\) below the cutoff, the hidden kernel at time \(h\) puts mass at least \(1/2\) on \(j(x)\).

Writing \(F_x(t)\) for this hidden kernel,
\[
\sup_{u:Pu=x}
\|F_x(t;u,\cdot)-\nu_x\|_{\rm TV}
\le2^{-\lfloor t/h\rfloor}.
\]
Consequently the integrated mixing bound is
\[
\boxed{
I:=
\int_0^\infty
\sup_{\substack{x:N(x)<B\\u:Pu=x}}
\|F_x(t;u,\cdot)-\nu_x\|_{\rm TV}\,dt
\le2h.
}
\tag{37}
\]

No fibre or population ball is enumerated.

## 9. Complete marked-path comparison, including exact times

Throughout this section, analytical stopping retains the exiting label, its exact time and the decoded landing state. After exit, the comparison is stopped; no mixing assertion is needed in an exit fibre.

### Finite-speed averaging

Before exit, the reference central intensity is at most
\[
Q\sum_r C_r+m\le QB+m<\Lambda.
\]

The marked uniformization comparison gives
\[
d_{\rm TV}\bigl(
\text{reference stopped decoded path},
\text{averaged stopped marked path}
\bigr)
\le\Lambda I(1+\Lambda\tau).
\tag{38}
\]

Here is why the estimate preserves exact times. Use a common rate-\(\Lambda\) Poisson proposal clock in the coupling proof. Between proposals, the actual fine encoding evolves under its hidden kernel. At a proposal, couple its pre-proposal encoding to a fresh \(\nu_x\) encoding, and then use the same acceptance and original-label mark.

For a gap of length \(s\), the coupling error is bounded by the hidden mixing envelope. Summing over the first proposal and subsequent proposals gives, respectively, bounds \(\Lambda I\) and \(\Lambda^2\tau I\). On successful coupling, the observed events occur at exactly the same proposal times. Null labels are processed as observed events, and each post-event encoding can be arbitrary.

The proposal clock and equilibrium couplings are proof variables, not physical devices.

By (8), (36) and (37),
\[
\Lambda I(1+\Lambda\tau)
\le
\frac{32BC_{\mathrm f}\Lambda(1+\Lambda\tau)}K
\le\epsilon/16.
\tag{39}
\]

### Adding the physical collision returns

Their nominal raw total intensity is
\[
\eta\sum_{r:q_r>0}C_r(V-q_r)\le\eta V^2.
\]
Before the weighted cutoff, \(V<B\). Coupling until the first extra collision return therefore gives stopped-path error at most
\[
\eta B^2\tau\le\epsilon/128.
\tag{40}
\]

### Arbitrary predictable faults

Compare the emitted nominal and faulty processes over physical time \([0,H\tau]\), stopping at the decoded cutoff.

While their entire fine firing histories agree, the sum of their marked intensity differences is at most
\[
\delta\sum_e c_e(Z)_{\alpha_e}
\le\delta m_fU^2.
\]
Thus all-mark common-intensity coupling gives
\[
d_{\rm TV}\bigl(
\text{faulty stopped fine path},
\text{nominal stopped fine path}
\bigr)
\le\delta m_fU^2H\tau
\le\epsilon/128.
\tag{41}
\]

This comparison counts a mismatched hidden or null firing as a mismatch. Consequently it remains valid even when future faults depend on every hidden, null and parallel mark. Predictability is sufficient; no switching-frequency or variation bound is used.

Rescaling time by \(H\) and applying the observation map cannot increase TV.

### Total stopped-path error

Combining (34), (39), (40) and (41),
\[
\boxed{
d_{\rm TV}\bigl(
\text{faulty stopped decoded marked path},
\text{original stopped marked path}
\bigr)
\le\frac{3\epsilon}{32}.
}
\tag{42}
\]

### Removing analytical stopping

Let \(\sigma_B\) be the first time the original process reaches \(N\ge B\). Its supplied drift inequality gives
\[
\mathbb P(\sigma_B\le\tau)
\le\frac{N_0+A\tau}{B}
<\frac{\epsilon}{32}.
\tag{43}
\]
The same localization argument establishes nonexplosion of the original marked process.

For completeness, if two stopped-path laws have TV distance \(a\), and the reference full path exits with probability \(b\), their full-path laws have TV distance at most \(a+b\): maximally couple the stopped records and extend their conditional continuations. Agreement of the stopped records together with no reference exit forces agreement of the entire paths.

Applying this to (42)–(43),
\[
\boxed{
d_{\rm TV}\!\left(
\mathcal L\bigl(\text{complete marked decoded path of }Z(H\cdot)\bigr),
\mathcal L\bigl(\text{complete marked path of }X\bigr)
\right)
\le\frac{\epsilon}{8}<\epsilon.
}
\tag{44}
\]

The emitted process continues normally on every excursion. Its costs there are already covered by (23) and (27).

## 10. Universal numerical resource bounds

Here are explicit bounds showing that no exponent depends on \(D\) or the network.

From the definition of \(W\),
\[
B,U\le2^7W^3,\qquad
\Gamma,k_*^{-1},D,m,\tau,\epsilon^{-1}\le W.
\]
Direct substitution gives
\[
\begin{aligned}
C_{\mathrm f}&\le2^7W^6,
&F&\le4W^2,\\
Q&\le2^{42}W^{16},
&\Lambda&\le2^{50}W^{19},\\
K&\le2^{125}W^{49},
&\eta^{-1}&\le2^{22}W^8,\\
H&\le2^{133}W^{52},
&m_f&\le16W^3.
\end{aligned}
\tag{45}
\]

The credit constants satisfy
\[
S_0\le2^{68}W^{24},
\qquad
R_*\le2^{71}W^{25},
\qquad
C_0\le2^{196}W^{73}.
\tag{46}
\]
Equations (23) and (27) consequently imply
\[
\mathbb E\sup_{s\le t}(1+|Z_s|_1)
\le2^{200}W^{74}(1+t),
\tag{47}
\]
and
\[
\mathbb E\mathsf F_{\rm all}(t)
\le2^{210}W^{74}(1+t)^2.
\tag{48}
\]
Since \(H\tau\le2^{133}W^{53}\),
\[
\boxed{
\mathbb E\mathsf F_{\rm all}(H\tau)
\le2^{480}W^{180}.
}
\tag{49}
\]

### Reciprocal rates

The potentially small source first-binding coefficient satisfies
\[
\begin{aligned}
\bigl(K\theta k_rU^{2-q_r}\bigr)^{-1}
&\le Q\,U^{q_r-2}/k_r\\
&\le Q\Gamma k_*^{-2}.
\end{aligned}
\tag{50}
\]
The other relevant reciprocals satisfy
\[
\begin{aligned}
(K\theta U^{-2})^{-1}&\le QU^2,\\
(K\theta k_r)^{-1}&\le Q/k_*,\\
(K/U)^{-1}&\le U,\\
(\eta d_S)^{-1}&\le\eta^{-1}.
\end{aligned}
\]
Thus
\[
\max_e\kappa_e^{-1}\le2^{56}W^{22},
\qquad
\boxed{\max_e c_e^{-1}\le2^{189}W^{74}.}
\tag{51}
\]
Also,
\[
\boxed{\delta^{-1}\le2^{159}W^{63}.}
\tag{52}
\]

The variable-order distinction is visible in these estimates. A large **source** order is paid through \(\Gamma\) and \(k_*^{-1}\). A large **product** order uses adjacent rate ratios \(1/U\); the full product activity \(\theta U^{-q_r'}\) is never required as a physical reaction coefficient.

Every requested numerical bound is therefore dominated by
\[
2^{4096}W^{256}
\]
with the prescribed time factors.

## 11. Uniform binary complexity

The compiler performs only deterministic list processing, construction of the displayed channels and decoder, and evaluation of the displayed rational expressions.

Because complexes are explicitly expanded,
\[
d,m,D\le L,\qquad S_{\mathrm p}\le L.
\]
Hence \(s\le3L\), and
\[
m_f\le8(1+L)^2.
\]
Even dense stoichiometric output has polynomial size.

The integers \(B,U\) have \(O(L)\) bits. Each required power \(U^{q_r}\) has
\[
O(q_r\log U)=O(L^2)
\]
bits. Summing the rational terms defining \(\Gamma\), and evaluating all parameters and rates, keeps numerator and denominator lengths \(O(L^2)\).

Using schoolbook integer arithmetic, Euclidean fraction reduction and straightforward loops, a conservative bound for bit operations, working memory and total output is
\[
2^{1000}(1+L)^{12}.
\tag{53}
\]
This is covered by the stated universal \(C,p\).

There is no preprocessing search depending on the reaction graph, no class enumeration, and no computation of a normalizer or invariant law. The formulas also terminate on nonadmitted inputs; the drift promise is needed only for the accuracy conclusion through (43).

## Scope of the proof

The global estimates here come from the physical pending-species reactions, the common credit (20), and the exact firing budget (26). They do not require a stationary distribution. The suggested Gupta–Briat–Khammash moment theorem uses a negative-drift inequality together with a separate diffusivity bound; its hypotheses are stronger than the upper-drift promise in this question. [arxiv.org](https://arxiv.org/pdf/1304.5404?utm_source=chatgpt.com)

The construction above supplies the entire requested contract:

- Elementary reactions on both sides, with structure depending only on \(R\).
- Nonzero decoder columns and exactly zero auxiliary initialization.
- Exact all-state directed reachability and communicating-class preimages.
- Complete timed labelled-path TV accuracy, retaining original null and parallel events.
- Uniformity over arbitrary predictable rate faults.
- Nonexplosion, linear expected supremum population and quadratic expected all-firing growth for the entire physical run.
- Universal polynomial binary and numerical costs, including variable reaction order and all excursions.