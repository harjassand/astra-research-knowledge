# P3; chat https://chatgpt.com/c/6af3030c-e834-83ec-b294-ad6a7f60aa46; user 3226b984-3ce8-45ec-b941-8233a0f915bc; assistant 68fe8fe4-4d2c-5b13-a481-e5bf9ce50d54; question P3_FULL_DETAILED_BALANCED_KINETIC_COMPILER_PRO_20261111.txt.

Native final returned without truncation flag. Current expanded activity and full helper panels are unsaved. No ZIP visible in inspected response; other availability unknown. Native reader text is not a database-byte identity claim.

## Full final

**I have not resolved the full universal statement.** I can establish a nominally detailed-balanced elementary realization with the required graph, reverse-label map, zero-auxiliary initialization, and complete timed-path accuracy under predictable faults. I can also pay the **actual faulty process’s entire expected work through \(H\tau\), including rare excursions**, with universal polynomial bounds.

The remaining gap is specific: for general \(A>0\), I have not proved the two polynomial bounds for **every physical time \(t\)** under arbitrary predictable faults. I also have no obstruction applying to every allowed design. Therefore I am not asserting either a full affirmative or a full negative.

There are two useful advances beyond simply attaching a detailed-balance certificate to the earlier construction:

1. A uniform choice of prefix activities makes variable-order conditioning particularly simple.
2. A marked-path relative-entropy estimate pays the actual finite-horizon tail and work costs without a population truncation.

I give the construction and these bounds below, followed by the precise remaining issue.

## 1. What is established

For the construction below, the status is:

| Requirement | Result |
|---|---|
| Every physical reaction has at most two molecules on each side | Proved |
| Structure, decoder and reverse/observation maps depend only on \(R,\bar r\) | Proved |
| Every decoder column is nonzero; initialization is exactly \((x_0,0)\) | Proved |
| Exact all-state directed reachability and class preimages | Proved |
| Exact rational nominal detailed-balance certificate for every channel | Proved |
| Nonexplosion for all times under every admitted predictable fault rule | Proved |
| Complete timed marked-path TV accuracy on \([0,\tau]\) | Proved |
| Universal polynomial output, precision, rate, activity and clock costs | Proved |
| Polynomial expected population supremum and **all firings through \(H\tau\)**, including faulty excursions | Proved |
| Required whole-run costs at zero faults | Proved |
| Required whole-run costs under predictable faults when \(A=0\) | Proved |
| Required whole-run costs under predictable faults for general \(A>0\) | **Not proved** |

The \(A=0\) result follows from a structural consequence of detailed balance: in that case the supplied \(\omega\) must actually be conserved by every original reaction.

## 2. A uniform paired-prefix realization

Assume \(m>0\); the empty reaction list is handled exactly.

Write
\[
q_r=|y_r|_1,\qquad
J=\sum_{r=1}^m q_r,\qquad
k_*=\min_r k_r.
\]
Order each explicitly listed source complex deterministically.

For every label with \(q_r>0\), introduce a private pending species \(C_r\), with
\[
PC_r=y_r.
\]
For \(q_r\ge2\), introduce private prefix species
\[
S_{r,2},\ldots,S_{r,q_r}.
\]
Their decoder columns are the corresponding partial source complexes. There is no separate product chain: the supplied reverse label already provides the product-side pending species and release chain.

Every original species has its identity decoder column. All decoder columns are nonzero and have total order at most \(D\).

Let
\[
s_r=
\begin{cases}
A_i,&y_r=e_i,\\
S_{r,q_r},&q_r\ge2.
\end{cases}
\]

The hidden reactions are
\[
A_{i_1}+A_{i_2}\rightleftarrows S_{r,2},
\qquad
S_{r,j-1}+A_{i_j}\rightleftarrows S_{r,j},
\]
and
\[
s_r\rightleftarrows C_r.
\]

The observed channel for label \(r\) is
\[
\begin{cases}
C_r\longrightarrow C_{\bar r},&q_r>0,\ q_{\bar r}>0,\\
\varnothing\longrightarrow C_{\bar r},&q_r=0,\ q_{\bar r}>0,\\
C_r\longrightarrow\varnothing,&q_r>0,\ q_{\bar r}=0,\\
\varnothing\longrightarrow\varnothing,&q_r=q_{\bar r}=0.
\end{cases}
\tag{1}
\]
Its reverse is the channel labelled \(\bar r\).

If \(r=\bar r\) is a nonempty null label, its observed channel is the actual self-reverse null reaction
\[
C_r\longrightarrow C_r.
\]
Distinct null and parallel labels remain distinct physical labels.

There are exactly
\[
s=d+J,\qquad m_f=2J+m
\tag{2}
\]
fine species and directed labelled channels.

### Actual graph preservation

Every hidden reaction preserves \(P\). Every observed channel labelled \(r\) has increment \(z_r-y_r\), and the presence of \(C_r\) ensures \(Pu\ge y_r\).

Every fine state can be released to \(j(Pu)\), and all release steps have hidden reverses. An enabled original edge lifts by assembling its source, entering its pending species, firing (1), and releasing the reverse-side pending species.

Consequently, for all fine states,
\[
\boxed{u\leadsto v\iff Pu\leadsto Pv.}
\tag{3}
\]

No controller sector, externally executed release, or reset enters this argument.

## 3. Activities, rates and an exact detailed-balance certificate

Put \(\Gamma=\Gamma_B\), and use \(U=1+B\) from the question. Introduce positive rational parameters \(K,\theta\), with \(Q=\theta^{-1}\).

Assign **relative** auxiliary activities
\[
w(S_{r,j})=\theta U^{-j},
\qquad
w(C_r)=\theta U^{-q_r}.
\tag{4}
\]
The emitted **absolute** activities are
\[
\boxed{\widetilde a_S=w(S)a^{PS},}
\tag{5}
\]
with \(\widetilde a_i=a_i\) on original species.

Use the following raw coefficients \(\kappa_e\), before common normalization.

| Reaction | Raw coefficient |
|---|---:|
| First prefix assembly | \(K\theta/U^2\) |
| Later prefix assembly | \(K/U\) |
| Every prefix release | \(K\) |
| Full-prefix \(s_r\to C_r\), \(q_r\ge2\) | \(K\) |
| Unary-source \(A_i\to C_r\), \(q_r=1\) | \(K\theta/U\) |
| Every \(C_r\to s_r\) hidden return | \(K\) |
| Observed label \(r\), \(q_r>0\) | \(g_r=Qk_rU^{q_r}\) |
| Observed label \(r\), \(q_r=0\) | \(k_r\) |

All propensities use falling factorials without additional symmetry factors.

Every hidden pair is exactly balanced by (5). For a nonempty observed source,
\[
g_r\widetilde a_{C_r}
=
Qk_rU^{q_r}\theta U^{-q_r}a^{y_r}
=
k_ra^{y_r}.
\]
The supplied original balance identity therefore gives
\[
g_r\widetilde a_{C_r}
=
g_{\bar r}\widetilde a_{C_{\bar r}}.
\tag{6}
\]
For an empty/nonempty pair, the same calculation gives
\[
k_r=g_{\bar r}\widetilde a_{C_{\bar r}}.
\]
For empty null pairs, the input identity gives \(k_r=k_{\bar r}\). Self-reverse null channels satisfy the certificate identically.

Dividing every raw coefficient by one common \(H\) preserves all these equalities exactly.

### Why the activities are affordable

Let
\[
M_a=2+\sum_i(a_i+a_i^{-1}).
\]
For every auxiliary payload of order at most \(D\),
\[
a^{PS},\ (a^{PS})^{-1}\le M_a^D\le\Xi.
\]
Furthermore, every auxiliary belongs to a source chain, so
\[
U^{q_r}\le\Gamma/k_r\le\Gamma/k_*.
\]
Thus
\[
\max_S\bigl(\widetilde a_S+\widetilde a_S^{-1}\bigr)
\le 2Q\Gamma k_*^{-1}\Xi.
\tag{7}
\]

This is a universal polynomial in the charged quantities. In particular, the very small relative weight of a long prefix is paid by \(\Gamma\), while its activity factor is paid by \(\Xi\).

## 4. Explicit parameters

The following choices suffice for the proved parts of the contract:
\[
C_{\mathrm f}=4(D+1)^2,
\]
\[
\begin{aligned}
Q={}&1+4096(1+m)UC_{\mathrm f}
       +128\epsilon^{-1}(J+1)\Gamma(1+\tau),\\
\theta={}&Q^{-1},\\
\Lambda={}&m+Q\Gamma U,\\
K={}&1+Q\Gamma+
512\epsilon^{-1}BC_{\mathrm f}\Lambda(1+\Lambda\tau),\\
H={}&1+K+Q\Gamma,\\
\delta={}&
\frac{\epsilon}{128m_fU^2(1+H\tau)},\\
c_e={}&\kappa_e/H.
\end{aligned}
\tag{8}
\]

These formulas imply \(0<c_e\le1\) and \(0<\delta<1/2\). The compiler evaluates ordinary rational expressions; it computes no invariant law or normalizer.

## 5. Complete timed-path accuracy

Here the physical process is untruncated. Stopping is used only to compare path laws.

### Hidden-fibre equilibrium

On a fibre \(Pu=x\), let \(v\) be the free-original population and \(b\) the auxiliary population, so \(v+Eb=x\). The hidden invariant law is
\[
\nu_x(v,b)
=
\frac{x!}{q(x)}
\frac{w^b}{v!\,b!},
\qquad
q(x)=\sum_{Eb\le x}\frac{w^b(x)_{Eb}}{b!}.
\tag{9}
\]
The common factor \(a^x\) cancels when conditioning on \(Pu=x\).

The exact averaged observed intensity is
\[
\boxed{
\bar\lambda_r(x)
=
k_r(x)_{y_r}\frac{q(x-y_r)}{q(x)}.
}
\tag{10}
\]

Below \(N(x)<B\), every auxiliary contributes at most \(\theta\) to the exponential generating bound, because
\[
w(S)B^{|PS|_1}
=
\theta(B/U)^{|PS|_1}\le\theta.
\]
There are \(J\) auxiliaries, so
\[
1\le q(x)\le e^{\theta J}.
\tag{11}
\]
The averaged/original stopped marked-path discrepancy is consequently at most
\[
2\theta J\Gamma\tau\le\epsilon/64.
\tag{12}
\]

### Uniform hidden mixing

Below the cutoff, a tagged prefix has downward rate \(K\) and upward rate at most
\[
(K/U)B\le K.
\]
The full-prefix/pending exchange adds one level. Its mean complete-release time is at most
\[
C_{\mathrm f}/K.
\]

At most \(B\) auxiliary lineages are initially present. New lineages arise through first bindings and unary pending entries, at total intensity at most \(K\theta m\).

At
\[
h=\frac{16BC_{\mathrm f}}K,
\]
the probability of an initial survivor is at most \(1/16\), and the probability of any new lineage is at most
\[
16\theta mBC_{\mathrm f}<1/64.
\]
Thus every hidden fibre kernel has a common canonical atom of mass at least \(1/2\) at time \(h\). Its integrated mixing envelope satisfies
\[
I\le2h.
\tag{13}
\]

The raw central intensity below cutoff is at most
\[
m+Q\Gamma B<\Lambda.
\]
The supplied complete marked-path uniformization estimate therefore gives
\[
\Lambda I(1+\Lambda\tau)
\le
\frac{32BC_{\mathrm f}\Lambda(1+\Lambda\tau)}K
\le\epsilon/16.
\tag{14}
\]
This comparison retains exact times, all null labels, arbitrary post-event encodings, and the first exit event.

### Predictable faults

Couple the emitted nominal and faulty processes using their complete fine marked histories. Before exit, the mismatch intensity is at most
\[
\delta m_fU^2.
\]
Over physical time \(H\tau\), the resulting stopped-path error is at most
\[
\delta m_fU^2H\tau\le\epsilon/128.
\tag{15}
\]
Hidden and null mismatches are included, so future faults cannot exploit an uncounted history discrepancy.

The original escape probability is
\[
\mathbb P(\sigma_B\le\tau)
\le\frac{N_0+A\tau}{B}<\epsilon/32.
\]
Coupling the stopped records and then their continuations gives
\[
\begin{aligned}
d_{\mathrm{TV}}(\text{full faulty decoded path},\text{full original path})
&\le
\epsilon/16+\epsilon/64+\epsilon/128+\epsilon/32\\
&=\frac{15\epsilon}{128}<\epsilon.
\end{aligned}
\tag{16}
\]
The event times in this coupling agree exactly when the coupling succeeds. No residence time is deleted.

## 6. All-time nonexplosion and an exact firing budget

Write \(n(z)=|z|_1\). Under the enlarged error box \([1/2,3/2]\), positive physical-population jumps occur only at prefix releases and nonempty zero-source births. Their total intensity is at most
\[
\frac32(n+m).
\tag{17}
\]
A pure-birth process with immigration dominates population growth. At bounded population, all marked rates are bounded. This proves nonexplosion for all times and supplies the preliminary finite-time integrability needed below.

For actual firing counts, let:

- \(\mathsf A,\mathsf R\) count prefix assemblies and releases.
- \(\mathsf I,\mathsf U\) count hidden pending entries and returns.
- \(\mathsf J\) count nonempty-to-nonempty observed events, including null events.
- \(\mathsf F_b\) count all zero-source marks, including \(0\to0\).
- \(\mathsf F_d\) count nonempty-source-to-empty marks.

Pending-count accounting gives
\[
\mathsf U+\mathsf F_d\le\mathsf I+\mathsf F_b.
\]
Physical-population accounting gives
\[
\mathsf A\le n_0+\mathsf R+\mathsf F_b,
\qquad n_0=|x_0|_1.
\]
Therefore
\[
\boxed{
F_{\mathrm{all}}(t)
\le
n_0+2\mathsf R(t)+2\mathsf I(t)
+\mathsf J(t)+3\mathsf F_b(t).
}
\tag{18}
\]

Each count on the right has unary or zero-order intensity. Since \(\theta m/U\le1\), their rates under faults satisfy
\[
\lambda_{\mathsf R},\lambda_{\mathsf I},\lambda_{\mathsf J}
\le\tfrac32n,
\qquad
\lambda_{\mathsf F_b}\le\tfrac32m.
\]
Consequently,
\[
\boxed{
\mathbb EF_{\mathrm{all}}(t)
\le
n_0+\frac{15}{2}\int_0^t\mathbb En(Z_s)\,ds+\frac92mt.
}
\tag{19}
\]

This accounts for every quadratic assembly without requiring a second-moment estimate. It also shows that a suitable whole-run population estimate would pay the entire activity contract.

## 7. Actual rare excursions are paid through \(H\tau\)

This step applies to the **actual faulty process**, including trajectories that leave the analytical cutoff.

At zero faults, the fine detailed-balance certificate gives the full product-Poisson invariant law
\[
\mu=\bigotimes_S\operatorname{Pois}(\widetilde a_S).
\]
It can be used without computing a communicating-class normalizer. The product-form and stochastic reversibility implications are the standard detailed-balance conclusions described by Anderson–Craciun–Kurtz. :chatgpt-content-reference{index="0"}

Let
\[
H_0=\log\frac1{\mu(j(x_0))}.
\]
Compare the complete faulty fine marked path, started at \(j(x_0)\), with the nominal fine marked process started from \(\mu\). The latter is only a reference law in the proof; no equilibrium initialization is physically performed.

Project any external fault randomness predictably onto the complete fine marked history. The resulting conditional multipliers remain in \([1-\delta,1+\delta]\).

For \(r\) in this interval,
\[
r\log r-r+1\le\delta^2.
\]
The marked likelihood formula yields
\[
\boxed{
D\!\left(
P_{\mathrm{fault}}^{[0,t]}
\middle\|
P_{\mathrm{nom},\mu}^{[0,t]}
\right)
\le H_0+2\delta^2\mathbb EF_{\mathrm{all}}(t).
}
\tag{20}
\]
Every hidden and null mark is included in this entropy calculation.

Set
\[
M_0=H_0+(\mathrm e-1)\sum_S\widetilde a_S.
\]
Data processing and the entropy variational inequality, applied to \(n\), give
\[
f(t):=\mathbb En(Z_t)
\le M_0+2\delta^2\mathbb EF_{\mathrm{all}}(t).
\]
Using (19),
\[
f(t)\le
M_0+2\delta^2n_0
+15\delta^2\int_0^t f(s)\,ds
+9\delta^2mt.
\tag{21}
\]
Since \(n_0\le M_0\), Gronwall gives
\[
\boxed{
f(t)\le
\left(\frac32M_0+9m\delta^2t\right)e^{15\delta^2t}.
}
\tag{22}
\]

A rational bound, requiring no logarithmic computation, is
\[
M=1+3\sum_S\widetilde a_S+N_0^2+N_0\Xi\ge M_0.
\]
Here
\[
\max_S\widetilde a_S\le\Xi,\qquad s\le2W^2,
\]
so
\[
M\le8W^3.
\tag{23}
\]

For \(T=H\tau\), the tolerance in (8) ensures \(\delta^2T\le1\). Thus
\[
\sup_{s\le T}\mathbb En(Z_s)\le2^{30}W^3.
\]
Only releases and zero-source births increase \(n\), so
\[
\mathbb E\sup_{s\le T}(1+n(Z_s))
\le
1+n_0+\frac32\int_0^T f(s)\,ds+\frac32mT.
\]
Together with (19),
\[
\boxed{
\mathbb E\sup_{s\le H\tau}(1+|Z_s|_1),
\quad
\mathbb EF_{\mathrm{all}}(H\tau)
\le2^{34}W^3(1+H\tau).
}
\tag{24}
\]

Equation (24) pays the whole actual tail through the accuracy horizon. It does not discard work on low-probability paths.

## 8. Uniform resource accounting for these proved conclusions

Direct substitution gives
\[
\begin{aligned}
B,U&\le2^7W^3,
&C_{\mathrm f}&\le2^4W^2,
&J&\le W^2,\\
Q&\le2^{25}W^6,
&\Lambda&\le2^{33}W^{10},\\
K&\le2^{88}W^{27},
&H&\le2^{89}W^{27},
&H\tau&\le2^{89}W^{28}.
\end{aligned}
\]
Also,
\[
\delta^{-1}\le2^{113}W^{37},
\qquad
\max_ec_e^{-1}\le2^{128}W^{39},
\]
and
\[
\max_S(\widetilde a_S+\widetilde a_S^{-1})
\le2^{26}W^9.
\tag{25}
\]
The decoder entries are at most \(D\le W\).

Combining (24) with the clock bound,
\[
\boxed{
\mathbb EF_{\mathrm{all}}(H\tau),
\quad
\mathbb E\sup_{s\le H\tau}(1+|Z_s|_1)
\le2^{124}W^{31}.
}
\tag{26}
\]

Expanded complexes give \(J\le L\). All required powers of \(U\) and all activity monomials have \(O(L^2)\) bits. The species/channel lists have polynomial size, and ordinary integer arithmetic and fraction reduction give, conservatively, a bound of
\[
2^{200}(1+L)^{12}
\]
for work, memory and output.

Thus universal constants such as \(2^{1024},128\) cover the proved resource statements. They are **not** claimed as constants for the unresolved whole-run faulty bounds.

## 9. Nominal whole-run costs and an exact drift identity

At zero faults, entropy contracts relative to \(\mu\):
\[
D(\mathcal L(Z_t)\|\mu)\le H_0.
\]
Therefore
\[
\sup_{t\ge0}\mathbb En(Z_t)\le M_0\le8W^3.
\]
The release-count bound and (18) then give
\[
\mathbb E\sup_{s\le t}(1+n(Z_s))
\le \operatorname{poly}(W)(1+t),
\]
and even
\[
\mathbb EF_{\mathrm{all}}(t)
\le \operatorname{poly}(W)(1+t)
\]
at zero faults.

There is also an exact useful identity for the nominal averaged chain. If \(v\) is the free-original population under \(\nu_x\), shifting \(v\) by \(y\) in (9) gives
\[
\mathbb E_{\nu_x}(v)_y
=(x)_y\frac{q(x-y)}{q(x)}.
\]
Hence
\[
\boxed{
\bar L N(x)
=
\mathbb E_{\nu_x}\!\left[LN(v)\right]
\le A.
}
\tag{27}
\]
Different partition ratios do not prevent transfer of this particular drift inequality to the **nominal averaged chain**.

Equation (27) is not a pointwise drift inequality for the actual finite-speed process. For example,
\[
A\rightleftarrows2A,\qquad k_+=k_-=a=1
\]
has original drift
\[
Ln=2n-n^2\le1.
\]
But at a fine state containing \(n\) pending molecules for the source \(A\) and no other species, the actual raw decoded drift is
\[
QU\,n>0.
\]
A corrected Lyapunov function or a different design is needed to bridge that distinction.

## 10. The full contract does close when \(A=0\)

Suppose the promise is
\[
LN(x)\le0\qquad\forall x.
\]
Under the full original product-Poisson law with activities \(a\),
\[
\mathbb E LN(X)
=\sum_r k_ra^{y_r}\,\omega\cdot(z_r-y_r)=0,
\]
by pairing reverse labels.

Every state has positive Poisson mass. Thus
\[
LN(x)\equiv0.
\]
Independence of the falling-factorial monomials gives, for every source complex \(c\),
\[
\sum_{r:y_r=c}k_r\,\omega\cdot(z_r-c)=0.
\tag{28}
\]
Therefore \(c\mapsto\omega\cdot c\) is harmonic on each finite reverse-connected complex graph. The maximum principle makes it constant on each component. Consequently,
\[
\boxed{\omega\cdot(z_r-y_r)=0\quad\forall r.}
\tag{29}
\]

Every fine channel then conserves \(\omega\cdot PZ\), independently of its rate errors:
\[
|Z_t|_1\le\omega\cdot PZ_t=N_0
\quad\text{pathwise for all }t.
\]
All-time firing costs follow immediately. Together with the construction above, this proves the entire requested contract in the \(A=0\) subcase, and more generally whenever the supplied \(\omega\) is directly conserved by every reaction.

## 11. The remaining general-\(A>0\) gap

The bound actually obtained under arbitrary predictable faults is (22):
\[
\mathbb En(Z_t)
\le
\left(\tfrac32M_0+9m\delta^2t\right)e^{15\delta^2t}.
\]
Choosing a small fixed positive \(\delta\) makes this useful through \(H\tau\). It does **not** turn it into the required polynomial estimate for every \(t\ge0\).

Simply reversing the old collision returns does not fix this. If
\[
C_r+S\to s_r+S
\]
has coefficient \(\eta d_S\), detailed balance requires a reverse coefficient proportional to
\[
\eta d_S\,\frac{\widetilde a_{C_r}}{\widetilde a_{s_r}}.
\]
That reverse creates pending molecules at quadratic intensity. The earlier bounded-credit argument relied on linear initiation intensity, so its constant drift budget is lost.

This is a failure of that particular repair, not a universal impossibility result. Likewise, existing recurrence results with additional structural assumptions do not provide the required arbitrary-history, universally polynomial population estimate; for example, the Anderson–Cappelletti–Kim result imposes a binary single-linkage setting and a pure-species-complex condition. :chatgpt-content-reference{index="1"}

The unresolved assertion is therefore
\[
\boxed{
\sup_{\text{admitted predictable faults}}
\mathbb E\sup_{s\le t}(1+|Z_s|_1)
\le C W^p(1+t)
\quad\text{for every }t\ge0,
}
\]
for some allowed detailed-balanced realization, or an obstruction ruling out every such realization. Once that population estimate is available for the paired lift, (18) pays all firings. I have not proved that estimate for general \(A>0\), so the complete universal question remains unresolved in this analysis.