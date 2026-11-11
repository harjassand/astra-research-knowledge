# P3 uniform kinetic trajectory: available completed return

Chat: https://chatgpt.com/c/6af3030c-e834-83ec-b294-ad6a7f60aa46. User turn c51f74ec-66ad-44ad-8e47-68a481727073; final 134de84d-42fe-52e2-8a3b-a5bf5843383a. UI showed Pro, final Copy and idle composer. Issued question: work/astra-renewed-pro-programmes-20261103/P3_FULL_UNIFORM_CONSERVATIVE_KINETIC_TRAJECTORY_COMPILER_PRO_20261111.txt, SHA-256 3d74df682459665425a2228daabf7bbf976fbf8c8695e57fd7243bb282f0ae83.

The complete available final is copied verbatim from the UI, not a database-byte identity claim. Current activity and three helper panels were visible, but TextEdit timed out during their capture; they are not included. This is a concrete activity-capture gap. No archive or output download was attempted; ZIP availability is unknown and all source holds persist.

## Full copied final

**Yes. The full uniform compiler exists.** A private-prefix elementary lift, together with a quantitative averaging lemma for complete marked paths, gives the requested construction.

One explicit, deliberately generous choice of uniform resource constants is
\[
\boxed{
p_D=5D+25,\qquad
A_D=2^{100(D+1)^3}.
}
\tag{1}
\]

The essential additional result is a **path-space averaging bound that preserves exact event times**. It handles the initial assembly period, the hidden state after every observed event, original null and parallel labels, and the terminal part of the observation interval. I prove that bound below and then give explicit rational compiler outputs.

---

## 1. The fixed elementary structure

Write
\[
m=|\mathcal R|.
\]
For each distinct complex \(c\) occurring in the reaction list, choose a deterministic ordering of its molecules:
\[
c=A_{i_1}+\cdots+A_{i_q},\qquad q=|c|_1.
\]

When \(q\ge2\), introduce private species
\[
P_{c,2},\ldots,P_{c,q}
\]
and hidden reversible channels
\[
A_{i_1}+A_{i_2}\rightleftarrows P_{c,2},
\tag{2}
\]
\[
P_{c,j-1}+A_{i_j}\rightleftarrows P_{c,j},
\qquad 3\le j\le q.
\tag{3}
\]

“Private” is important: prefixes belonging to different complex chains remain different species even when their decoded populations coincide. In particular, an intermediate prefix is not identified with another complex’s representative. Each prefix then has at most one hidden upward extension.

Define
\[
\operatorname{rep}(c)=
\begin{cases}
\varnothing,&|c|_1=0,\\
A_i,&c=e_i,\\
P_{c,q},&|c|_1=q\ge2.
\end{cases}
\]
For every original label \(r\), emit a separate central channel
\[
\operatorname{rep}(y_r)\longrightarrow\operatorname{rep}(z_r),
\tag{4}
\]
and map its fine label to \(r\). Map all assembly and release labels to the hidden symbol.

Every channel in (2)–(4) has at most two molecules on each side. Null and parallel central labels remain separately counted.

The decoder \(P\) is the identity on original species, and
\[
P(P_{c,j})=e_{i_1}+\cdots+e_{i_j}.
\tag{5}
\]
Every decoder column is nonzero. The zero complex is represented by the actual empty complex, without a zero-payload species.

Let \(M\) be the number of distinct complexes occurring in the list, and let
\[
S=\sum_{\substack{c\text{ occurring}\\|c|_1\ge2}}(|c|_1-1)
\]
be the number of prefix species. Then
\[
M\le2m,\qquad
S\le2m(D-1),
\tag{6}
\]
and the numbers of species and fine channels satisfy
\[
s=d+S,\qquad
m_f=m+2S\le(4D-3)m.
\tag{7}
\]

The species, channels, decoder, and label map depend only on \(\mathcal R\).

### Exact graph, reachability, and communicating classes

Every fine state \(u\) can be released to \(j(Pu)\) using only hidden channels. Reversing that release sequence provides a hidden path from \(j(Pu)\) back to \(u\).

A central channel labelled \(r\) can fire only when its source representative is present. That implies
\[
Pu\ge y_r,
\]
and its decoded increment is precisely \(z_r-y_r\).

Conversely, when \(x\ge y_r\), assemble a representative of \(y_r\) from \(j(x)\), fire the central channel labelled \(r\), and release the product representative. This gives a finite fine path from
\[
j(x)\quad\text{to}\quad j(x-y_r+z_r)
\]
with exactly that original label and otherwise hidden labels.

Consequently, for **arbitrary fine states** \(u,v\),
\[
\boxed{
u\leadsto v
\quad\Longleftrightarrow\quad
Pu\leadsto Pv.
}
\tag{8}
\]
It follows that each fine communicating class is exactly the full preimage of an original communicating class. No reversibility assumption on the original network is needed.

### Conservation and the hard population bound

Hidden channels preserve \(P\) exactly. Central channels have decoded increment \(z_r-y_r\), so every fine channel conserves \(\omega\cdot Pz\).

Every decoder column has positive integer \(\omega\)-weight. Thus, pathwise and under every fault rule,
\[
|Z_t|_1
\le \omega\cdot PZ_t
=\omega\cdot x_0
\le B.
\tag{9}
\]

Positive conservation weights also imply that any original reaction involving the zero complex must be \(0\to0\). Such a label is emitted as a genuine labelled \(\varnothing\to\varnothing\) channel.

---

## 2. Raw rates and the hidden fibre law

First specify raw coefficients. A single common normalization will subsequently make every emitted coefficient at most one.

Choose positive rationals \(K,\theta\), with \(\theta\le1\). Give the first assembly and its reverse the coefficients
\[
K\theta,\quad K,
\tag{10}
\]
and give each later assembly and release the coefficients
\[
K,\quad K.
\tag{11}
\]
Give central label \(r\) the raw coefficient
\[
b_r=
\begin{cases}
k_r/\theta,&|y_r|_1\ge2,\\
k_r,&|y_r|_1\le1.
\end{cases}
\tag{12}
\]

Disable the central channels temporarily. On the fibre \(Pu=x\), the hidden process is a finite irreducible reversible chain.

Write a fine state as \((v,a)\), where \(v\) counts free original molecules, \(a\) counts prefix species, and
\[
v+Ea=x.
\]
Its invariant probability is
\[
\nu_x(v,a)
=
\frac{x!}{q_\theta(x)}
\frac{\theta^{|a|_1}}{v!\,a!},
\tag{13}
\]
where
\[
q_\theta(x)
=
\sum_{Ea\le x}
\frac{\theta^{|a|_1}(x)_{Ea}}{a!}.
\tag{14}
\]

The detailed-balance identities follow directly from (10)–(11), including repeated-molecule first bindings under the falling-factorial convention.

Neither \(\nu_x\) nor \(q_\theta(x)\) is computed by the compiler. They are analytical objects.

### Exact averaged labelled intensities

For a prefix representative of \(y\),
\[
\mathbb E_{\nu_x}N_{\operatorname{rep}(y)}
=
\theta(x)_y\frac{q_\theta(x-y)}{q_\theta(x)}.
\]
For an original-species representative, the same identity holds without the factor \(\theta\). Therefore the exact averaged intensity of every original label is
\[
\boxed{
\bar\lambda_r(x)
=
k_r(x)_{y_r}
\frac{q_\theta(x-y_r)}{q_\theta(x)}.
}
\tag{15}
\]
Both sides are zero when \(x\not\ge y_r\). For \(y_r=0\), the ratio is one.

On \(|x|_1\le B\),
\[
1\le q_\theta(x)\le \exp(S\theta B^D).
\tag{16}
\]
Indeed, after dropping the constraint \(Ea\le x\), each summand is bounded by
\[
\frac{(\theta B^D)^{|a|_1}}{a!}.
\]

If \(S\theta B^D\le1\), then
\[
|\bar\lambda_r(x)-k_r(x)_{y_r}|
\le
2S\theta B^D\,k_r(x)_{y_r}.
\tag{17}
\]
This concerns each separate label, including original null labels.

---

## 3. Uniform mixing inside the fibres

Put
\[
U=1+B,\qquad
C_D(B)=D[8U]^{D-1}.
\tag{18}
\]

Use the supplied tagged-prefix release estimate:
\[
\mathbb E[\text{release lifetime of a tagged prefix}]
\le \frac{C_D(B)}K.
\tag{19}
\]
It is independent of the number of species because each private prefix has only one possible upward extension.

Suppose
\[
\theta\le
\frac1{1024(1+M)U^3C_D(B)}.
\tag{20}
\]
Set
\[
h=\frac{16B\,C_D(B)}K.
\tag{21}
\]

There are at most \(B\) prefix lineages initially. By (19), Markov’s inequality and a union bound, the probability that any initial lineage survives until \(h\) is at most \(1/16\).

The total first-assembly immigration intensity is at most
\[
2K\theta M U^2.
\]
Hence the probability of any new prefix birth during the entire interval \([0,h]\) is at most
\[
2K\theta M U^2h
=
32\theta M B U^2C_D(B)
\le\frac1{32}.
\tag{22}
\]

If all initial lineages have released and no new prefix has been born, the state at time \(h\) is canonical. Thus, from every fine encoding of \(x\), the hidden kernel has a common atom at \(j(x)\) of mass at least \(1/2\).

Let \(F_x(t)\) denote the hidden semigroup. Its Dobrushin coefficient at \(h\) is at most \(1/2\). Therefore
\[
d(t):=
\sup_{\substack{\omega\cdot x\le B\\Pu=x}}
\|F_x(t;u,\cdot)-\nu_x\|_{\rm TV}
\le 2^{-\lfloor t/h\rfloor},
\]
and
\[
\boxed{
I:=\int_0^\infty d(t)\,dt\le2h.
}
\tag{23}
\]

No number of fine states, minimum stationary probability, or spectral gap enters this estimate.

---

## 4. Full timed marked-path averaging

Here is the additional theorem needed to close the question’s open interface.

### Lemma

Suppose a fine process has hidden dynamics within decoder fibres, with invariant fibre laws \(\nu_x\), and
\[
\sup_{x,u:\,Pu=x}
\|F_x(t;u,\cdot)-\nu_x\|_{\rm TV}\le d(t),
\qquad
I=\int_0^\infty d(t)\,dt<\infty.
\]
Suppose its total central marked intensity is bounded by \(\Lambda\). Let \(\bar X\) have the averaged labelled intensities
\[
\bar\lambda_r(x)=\mathbb E_{\nu_x}\lambda_r^{\rm fine}.
\]

Then, from **any initial fine encoding** \(u_0\),
\[
\boxed{
\operatorname{TV}\!\left(
\mathcal L(\text{complete decoded central marked path on }[0,\tau]),
\mathcal L(\text{complete marked }\bar X\text{ path on }[0,\tau])
\right)
\le \Lambda I(1+\Lambda\tau).
}
\tag{24}
\]

The comparison retains exact event times and every central label.

### Proof

Introduce an independent Poisson proposal clock of rate \(\Lambda\), solely for the proof. Let its times be \(T_j\), its gaps be \(S_j=T_j-T_{j-1}\), and \(T_0=0\).

There is an exact representation of the fine process as follows:

1. Between proposals, run its hidden fibre dynamics.
2. At a proposal, given fine state \(u\), select central label \(r\) with probability
   \[
   \lambda_r^{\rm fine}(u)/\Lambda.
   \]
3. Select rejection with the remaining probability.
4. An accepted channel fires with its actual label and update.

This is uniformization of the central channels only. An accepted null channel is a genuine counted event. A rejected proposal is not a physical firing.

Suppose the decoded proposal histories have agreed so far, and their common decoded state is \(x\). Condition on the full coupled history at the previous proposal and on the next gap \(S_j=s\).

The next fine endpoint has law
\[
F_x(s;u,\cdot).
\]
Maximally couple this endpoint \(U_j\) to a fresh variable \(V_j\) with marginal \(\nu_x\). The coupling fails with probability at most \(d(s)\).

Now use an independent common uniform mark to apply the central label-or-rejection kernel to both endpoints. If \(U_j=V_j\), the chosen label or rejection agrees, and an accepted original event occurs at **exactly the same proposal time** on both sides.

For the comparison process, conditional on the previous joint history and the new gap,
\[
\mathbb P(\text{label }r)
=
\frac{\mathbb E_{\nu_x}\lambda_r^{\rm fine}}{\Lambda}
=
\frac{\bar\lambda_r(x)}{\Lambda}.
\]
This probability is independent of the gap. Its marginal is therefore exactly the averaged marked chain.

The actual fine state after a rejection or accepted event can be arbitrary. The next coupling remains valid because the fibre bound is uniform over every starting fine state. Thus conditioning on observed null marks or on the absence of observed events introduces no additional assumption.

The probability of any disagreement is at most
\[
\mathbb E\sum_{j:T_j\le\tau}d(S_j).
\]
The Poisson renewal identity gives
\[
\mathbb E\sum_{j:T_j\le\tau}d(S_j)
=
\int_0^\tau
\Lambda e^{-\Lambda s}d(s)
\bigl[1+\Lambda(\tau-s)\bigr]\,ds
\le \Lambda I(1+\Lambda\tau).
\tag{25}
\]

On the agreement event, every accepted mark has the same label and the same exact time. Between accepted marks, hidden dynamics preserves the decoder. Hence the complete decoded marked paths are identical.

There is no terminal correction: hidden firings after the last accepted central event leave the decoded path unchanged. This proves (24). ∎

**The proposal clock, maximal couplings, and variables \(V_j\) are analytical proof devices.** The compiler never samples a fibre equilibrium, and the physical network contains no reset or proposal mechanism. All actual residence time remains in the observed timeline.

### Application to the prefix lift

Every central channel has at most one physical reactant. From \(N\le B\) and (12),
\[
\sum_r\lambda_r^{\rm fine}(u)
\le \frac{mU}{\theta}.
\]
Take
\[
\Lambda=\frac{mU}{\theta}.
\tag{26}
\]
Equations (21), (23), and (24) yield
\[
\boxed{
\operatorname{TV}(\text{nominal decoded full path},\text{averaged full path})
\le
\frac{32B\,C_D(B)\Lambda(1+\Lambda\tau)}K.
}
\tag{27}
\]

This proves the proposed averaging interface with an explicit constant, uniformly in the network.

---

## 5. Averaged path versus the prescribed original path

The original total marked intensity satisfies
\[
\sum_r k_r(x)_{y_r}\le mU^D
\]
on the conserved state space.

Couple the averaged and original chains by common labelled intensities until their first marked disagreement. Equation (17) gives
\[
\boxed{
\operatorname{TV}(\text{averaged full path},\text{original full path})
\le 2Sm\theta U^{2D}\tau.
}
\tag{28}
\]

This is again a complete marked-path coupling. A discrepancy in a null label or in a parallel label counts as a disagreement even when the population change happens to coincide.

No equilibrium or recurrence property of the original chain is used.

---

## 6. Explicit compiler outputs

For \(m=0\), emit no channels, the identity decoder, \(H=1\), and \(\delta=1/2\). All requirements then hold exactly.

Suppose \(m\ge1\). Compute
\[
B=\max(1,\omega\cdot x_0),\qquad U=1+B,\qquad C=C_D(B).
\]

Define
\[
\boxed{
Q=
1+1024(1+M)U^3C
+32\epsilon^{-1}(1+S)(1+m)U^{2D}(1+\tau),
\qquad
\theta=Q^{-1}.
}
\tag{29}
\]
Then set
\[
\boxed{
\Lambda=mUQ,
\qquad
K=1+Q+
512\epsilon^{-1}BC\Lambda(1+\Lambda\tau).
}
\tag{30}
\]

These choices enforce (20). They also give \(S\theta B^D<1\) and make the two nominal path errors satisfy
\[
2Sm\theta U^{2D}\tau\le\frac{\epsilon}{16},
\tag{31}
\]
\[
\frac{32BC\Lambda(1+\Lambda\tau)}K
\le\frac{\epsilon}{16}.
\tag{32}
\]

Let \(\kappa_e\) denote the raw coefficients specified in (10)–(12). Define
\[
\boxed{
H=1+K+Q,\qquad c_e=\frac{\kappa_e}{H}.
}
\tag{33}
\]
Every raw coefficient is at most \(\max(K,Q)\), so \(0<c_e\le1\).

Finally emit
\[
\boxed{
\delta=
\frac{\epsilon}
{16m_fU^2(1+H\tau)}.
}
\tag{34}
\]
It is a positive rational below \(1/2\).

All these quantities are obtained by ordinary exact rational arithmetic.

---

## 7. Arbitrary predictable rate faults

Compare the actual normalized fine process with its nominal counterpart on the physical interval \([0,H\tau]\).

Couple **every fine firing label**, including hidden labels and all null and parallel marks, until the first mismatch. Before that mismatch, the complete fine histories agree. Thus the fault multipliers remain predictable in the joint construction, regardless of their dependence on prior states, firings, or admissible external randomness.

At a common fine state, the total mismatch intensity is at most
\[
\sum_e c_e|a_e(t)-1|(Z_t)_{\alpha_e}
\le \delta m_fU^2.
\]
Therefore
\[
\operatorname{TV}(
\text{actual full fine marked path},
\text{nominal full fine marked path})
\le
\delta m_fU^2H\tau
\le\frac{\epsilon}{16}.
\tag{35}
\]

Applying \(P\), erasing hidden labels, and rescaling times are measurable maps, so TV cannot increase.

The normalized nominal process observed at physical time \(Ht\) has exactly the law of the raw nominal process at time \(t\). Combining (27), (28), and (35),
\[
\boxed{
\begin{aligned}
&\operatorname{TV}\!\left(
\mathcal L\!\left(
\text{actual decoded marked path, times divided by }H
\right),
\mathcal L(X\text{ marked path on }[0,\tau])
\right)\\
&\hspace{4cm}\le
\frac{\epsilon}{16}
+\frac{\epsilon}{16}
+\frac{\epsilon}{16}
=
\frac{3\epsilon}{16}
<\epsilon.
\end{aligned}
}
\tag{36}
\]

The same emitted \(c_e,H,\delta\) works for every admitted predictable fault family. No switching-frequency or regularity bound is used.

---

## 8. Uniform physical costs

Let
\[
c_D=D8^{D-1},\qquad
a_D=4096c_D,
\]
and
\[
h_D=2+2a_D+512c_Da_D(1+a_D).
\tag{37}
\]
These depend only on \(D\).

Since \(M\le2m\), \(S\le2m(D-1)\), and every positive quantity appearing in the definition of \(W\) is bounded by \(W\), the explicit choices give
\[
Q\le a_DW^{2D+4},
\qquad
\Lambda\le a_DW^{2D+6},
\tag{38}
\]
and
\[
K,H\le h_DW^{5D+14}.
\tag{39}
\]
Consequently,
\[
H\tau\le h_DW^{5D+15}.
\tag{40}
\]

### Reciprocal rate coefficients

Because \(K\ge Q=\theta^{-1}\),
\[
K\theta\ge1.
\]
Every hidden raw coefficient is at least one, and every central raw coefficient is at least the corresponding \(k_r\). Thus
\[
\max_e c_e^{-1}
\le H\max_r k_r^{-1}
\le h_DW^{5D+15}.
\tag{41}
\]

Equation (34) gives
\[
\delta^{-1}
\le64D(1+h_D)W^{5D+19}.
\tag{42}
\]

### Every actual firing, for the entire run

The population bound (9) is pathwise. Since every normalized coefficient is at most one and every source has order at most two, every admitted actual channel intensity is at most
\[
\frac32U^2.
\]
Hence the total marked intensity is bounded deterministically by
\[
\frac32m_fU^2.
\tag{43}
\]

This proves nonexplosion under every predictable fault rule and gives, for every physical \(t\ge0\),
\[
\boxed{
\mathbb E[\text{all actual fine firings on }[0,t]]
\le \frac32m_fU^2t
\le6DW^3t.
}
\tag{44}
\]

In particular,
\[
\boxed{
\mathbb E[\text{all actual fine firings on }[0,H\tau]]
\le6Dh_DW^{5D+18}.
}
\tag{45}
\]

These counts include every assembly, release, unsuccessful assembly cycle, original null firing, and parallel label. The common slowdown has been paid through \(H\tau\).

Together with
\[
\sup_{t\ge0}|Z_t|_1\le B\quad\text{almost surely},
\]
these establish all physical requirements.

---

## 9. Uniform binary cost

The compiler performs only the following operations:

1. Read the explicit reaction list and conservation data.
2. Compute \(B=\max(1,\omega\cdot x_0)\).
3. Order the at most \(D\) molecules in each complex and identify equal whole complexes.
4. Emit the private prefix chains, decoder, and label map.
5. Evaluate (29)–(34) and divide each raw coefficient by \(H\).

There are no network-dependent terminating searches. In particular, there is no Gröbner computation, reachable-state enumeration, stationary-law calculation, or sampling subroutine.

For ordinary explicit binary vectors and lists, \(d,m\le L\). There are \(O(Dm)\) auxiliary species and channels. Even a dense decoder and dense stoichiometric output have polynomial size.

All numerical intermediate bit lengths are bounded by
\[
C(D+1)^2(1+L)
\]
for an absolute constant \(C\): the formulas use a fixed number of rational operations and integer powers of degree \(O(D)\). Schoolbook integer arithmetic, Euclidean reduction of fractions, and a simple pairwise comparison algorithm for whole-complex deduplication suffice.

A generous explicit bound covering bit operations, working memory, and total output is
\[
2^{20(D+1)^2}(1+L)^4.
\tag{46}
\]
The numerical prefactors in (38)–(45) are also below \(2^{20(D+1)^2}\) for \(D\ge3\).

Thus the pair in (1),
\[
p_D=5D+25,\qquad A_D=2^{100(D+1)^3},
\]
dominates every binary and numerical bound. There is no suppressed dependence on \(\mathcal R\), \(d\), the conservation weights, a state count, a gap, or a minimum probability.

---

## 10. What closes the full question

The decisive step is the marked-path averaging lemma (24). Its coupling provides equality of the **entire timed labelled output** on a high-probability event. It does not infer path convergence from endpoint convergence.

The cited Hoessly–Wiuf theorem gives compact-time state-probability convergence under its finite-closed-set and fast-return assumptions. Petrack–Doty’s result concerns exact algorithmic sampling of stochastic reaction-network configurations. The explicit uniformization coupling above supplies the additional physical marked-path comparison required here. [arxiv.org](https://arxiv.org/pdf/2110.13235?utm_source=chatgpt.com)

The resulting compiler therefore satisfies the whole contract: fixed elementary structure and nonzero decoder columns, exact directed reachability and communicating classes, canonical initialization, exact conservation, complete timed marked-path TV accuracy under arbitrary predictable faults, and uniform polynomial costs for the entire population and all actual firings.