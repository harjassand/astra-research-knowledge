# P3 completed return — 83f03f59

Chat: https://chatgpt.com/c/6af2bff2-ef48-83ec-be8e-26ac8b99ab06
Model: GPT-6 Pro, as observed. Exact question: `work/astra-renewed-pro-programmes-20261103/P3_FULL_ROBUST_KINETICS_FRESH_AFTER_716AA3_PRO_20261110.txt` (approved two-final-LF omission). No original ZIP appeared in the response or visible outputs.

The native reader limits the response to 20,000 characters. Its Markdown prefix is preserved below, followed by the full visible answer in the browser accessibility representation. Mathematical notation in that representation is split across elements, and the displayed activity-lower-bound table cell is visibly truncated; the same bound appears in the surrounding answer. The browser Copy control reported copied but its supported clipboard read returned empty. Visible activity was expanded as shown. No private reasoning was requested.

## Native response prefix (truncated at 20,000 characters)

## Result

**Under the accepted starting mathematics in your message, I obtain an affirmative construction for the full compiler.** The new step is a finite catalytic construction that supplies the three nominal hypotheses of completed **136C for every fixed weakly reversible \(R\)**:

\[
\boxed{
\begin{aligned}
\sum_{x\in\Gamma}\pi_\lambda(x)a(x)
   \bigl(f(x)-\pi_\lambda f\bigr)^2
   &\le C_G W^{p_G}\,\mathcal E(f),\\[2mm]
a(x)&\ge c_aW^{-p_a}(1+|x|_1)^2,\\[2mm]
\pi_\lambda a&\le C_AW^{p_A}.
\end{aligned}}
\tag{1}
\]

Here \(a\) counts **all actual labelled firing intensities, including null channels**. Every constant and exponent in (1) is computable from \(R\). The augmentation is fixed before \(x_0,\lambda,\epsilon\) are supplied.

The construction uses finite original reaction words, closes them under a finite joining operation, and assigns exact cycle-balanced rates. The crucial point is that the joining operation controls the activity introduced by its own added channels. It does not require an endless sequence of further catalytic additions.

Applying the **accepted full 136C transfer** to (1) supplies the required rational \(\delta,T\), uniform nonexplosion and positive recurrence, both stationary accuracy requirements, both transient accuracy requirements, and the expected number of actual firings.

I give the construction, the universal argument, and the resource accounting below. The final transfer is inherited capital; I am not claiming an independent reproof of 136C.

---

# 1. Accepted inputs and notation

I use these accepted operations at their stated scopes:

1. **Bounded inward words.** Outside a computable polynomial head, the actual class has an original enabled word
   \[
   x\longrightarrow x-g
   \]
   whose displacement and excursion are bounded by fixed-\(R\) constants, whose displacement has signs directed toward \(x_0\), and which strictly decreases
   \[
   \Phi(x)=\|x-x_0\|^2.
   \]

2. **The nominal physical-gap construction.** Its fixed catalytic channel table admits, for each input, rates at most one with invariant law \(\pi_\lambda\) and
   \[
   \operatorname{Var}_{\pi_\lambda}(f)
   \le G_0W^{g_0}\mathcal E_0(f).
   \tag{2}
   \]
   Only its fixed channel table and quantitative gap theorem will be needed. The new compiler will not need to evaluate its rates.

3. **Completed 136C.** Its full constructive transfer applies once the three inequalities in (1), the rational-rate bounds, and compilation costs are supplied.

Write
\[
x^{\underline c}
=\prod_i\frac{x_i!}{(x_i-c_i)!},
\]
with value zero unless \(x\ge c\) coordinatewise.

For the new nominal generator \(Q\), put
\[
a(x)=\sum_e q_e(x),
\qquad
\mathcal E(f)
=\frac12\sum_{x,e}\pi_\lambda(x)q_e(x)
       \bigl(f(x+\nu_e)-f(x)\bigr)^2.
\tag{3}
\]

The index \(e\) denotes physical labelled channels. An occurrence decomposition used in the proof will sum exactly to these physical rates.

The new construction has three parts:

- compute finitely many original words that add nonnegative population;
- use their reverses to obtain fixed inward words in every sufficiently remote state;
- join their closed cycles so that every large firing activity has a short path toward substantially greater \(\pi_\lambda a\)-weight.

---

# 2. An effective finite collection of nonnegative pumping words

For each nonempty coordinate set \(S\subseteq\{1,\ldots,d\}\), define
\[
P_S=
\left\{
p\in\mathbb N^d:
p\longrightarrow p+h
\text{ for some }0\ne h\in\mathbb N^d,\ 
\operatorname{supp}h\subseteq S
\right\}.
\tag{4}
\]

Every path here uses original enabled reactions.

The set \(P_S\) is upward closed: a word enabled at \(p\) remains enabled after adding any nonnegative background. Dickson’s lemma therefore gives a finite covering set of starting markings.

For the resource contract, existence of a finite set is insufficient. We need a terminating procedure that finds one and certifies that it covers all of \(P_S\).

## 2.1 Actual communication as a monomial congruence

Form the binomial ideal
\[
I_R=\left\langle X^{y_r}-X^{z_r}:r\in R\right\rangle
\subseteq\mathbb Q[X_1,\ldots,X_d].
\tag{5}
\]

As a vector space, this ideal is spanned by differences of monomials connected by translated reaction relations. Consequently its quotient has one basis element for each connected monomial class, and
\[
X^u-X^v\in I_R
\quad\Longleftrightarrow\quad
u,v\text{ are connected by translated reaction relations}.
\tag{6}
\]

Weak reversibility makes this exactly **actual communication**. Indeed, the reverse of an enabled reaction
\[
n+y_r\longrightarrow n+z_r
\]
can be executed by translating a fixed original complex-graph path from \(z_r\) back to \(y_r\) by the same \(n\ge0\).

Thus (6) uses the actual enabled graph, including its boundary restrictions.

## 2.2 A terminating test for a pump inside a downward box

Consider a box whose coordinates in \(B\) have upper bounds \(b_i\), with the remaining coordinates \(F\) unrestricted.

Because \(P_S\) is upward closed, the box intersects \(P_S\) precisely when it contains a pump starting with bounded coordinates exactly \(b\). Define
\[
J_b=
\left(I_R:X_B^b\right):
\left(\prod_{j\in F}X_j\right)^\infty,
\qquad
K_b=J_b\cap\mathbb Q[X_i:i\in S].
\tag{7}
\]

The box intersects \(P_S\) if and only if \(K_b\) contains
\[
X^h-1
\quad\text{for some }0\ne h\ge0
\text{ supported on }S.
\tag{8}
\]

The saturation in (7) supplies a sufficiently large free-coordinate background. Conversely, any finite free-coordinate background is dominated by some common power of the saturating monomial.

There is an exact finite test for (8):
\[
\exists\,0\ne h\ge0,\ X^h-1\in K_b
\quad\Longleftrightarrow\quad
\exists\,i\in S:\ 1\in K_b+\langle X_i\rangle.
\tag{9}
\]

The reverse implication deserves explanation. Monomial colons, monomial saturation, and elimination preserve the quotient’s description by monomial congruence classes. If \(1=X_iF\) in that quotient, expand \(F\) into monomials. The coefficient of the class of \(1\) must receive a contribution from at least one monomial \(X_iX^u\) in that same class. Hence
\[
X_iX^u-1\in K_b.
\]
This is a genuine nonconstant monomial relation.

All operations in (7)–(9) are terminating exact Gröbner-basis operations over \(\mathbb Q\).

## 2.3 Computing and certifying the finite cover

Maintain a finite list \(A\) of witnessed pumping starts.

The complement
\[
\mathbb N^d\setminus\uparrow A
\]
is an effectively computable finite union of downward boxes: for each \(a\in A\), an uncovered marking must satisfy \(p_i<a_i\) for at least one coordinate.

Test those boxes using (7)–(9).

If a box contains a pump, enumerate original reaction words until finding one with nonzero nonnegative displacement supported on \(S\), whose minimal enabling marking lies in that box. A word \(r_1\cdots r_\ell\) has explicitly computable minimal enabling marking
\[
p_i=
\max\left(
0,\
\max_{1\le j\le\ell}
\left[
y_{r_j,i}
-\sum_{k<j}(z_{r_k,i}-y_{r_k,i})
\right]
\right).
\tag{10}
\]

A positive box test guarantees that this search terminates. Add its start and witness word.

Each new start lies outside the upward closure of all previous starts. Dickson’s lemma excludes an infinite such sequence. When every remaining box tests negative, the list is certified complete.

Perform this for every nonempty \(S\), and store directed reverse words as well.

**This is finite, computable preprocessing depending only on \(R\).** It uses no supplied reachability, counting, class, or stationary-law oracle.

---

# 3. Every sufficiently remote state admits a fixed inward pump

The next step connects the accepted inward geometry with the finite lists just constructed.

Let \(B\ge1\) bound each coordinate of an accepted inward word’s endpoint displacement, and let \(r\) bound its internal excursion. Let \(Y\) bound original reactant coordinates.

We will establish:

> Outside a computable polynomial head, every \(x\in\Gamma\) has a stored fixed-length original word
> \[
> x\longrightarrow x-\widehat h,
> \]
> where \(0\ne\widehat h\ge0\), and every coordinate changed by \(\widehat h\) is larger than all fixed catalytic thresholds and a sufficiently large fixed multiple of \(W\).

This does not require interpreting “sign-conformal” as a no-overshoot condition.

## 3.1 Separate large and small coordinates

Choose a polynomial threshold \(A_0(W)\) dominating the inherited geometric head, \(|x_0|_1\), \(W\), and the fixed constants needed below. Define
\[
A_{k+1}=K_R(A_k+1)^{d+1},
\qquad 0\le k<d.
\tag{11}
\]

If \(\max_i x_i>A_d\), one of the \(d\) intervals
\[
(A_k,A_{k+1}],\qquad 0\le k<d,
\]
contains no coordinate of \(x\). One coordinate is already above \(A_d\), leaving at most \(d-1\) coordinates for these \(d\) intervals.

For an empty interval, put
\[
S=\{i:x_i>A_{k+1}\}.
\]
Then \(S\ne\varnothing\), while every coordinate outside \(S\) is at most \(A_k\).

## 3.2 Find a nonnegative displacement supported on \(S\)

Follow the accepted inward words for more than the number of possible outside-\(S\) endpoint configurations.

Their outside-\(S\) coordinates remain bounded by \(A_k+B\): bounded sign-directed steps can overshoot their target only by a bounded amount.

The coordinates in \(S\) stay above \(x_0\), and stay large, because (11) reserves much more population than this polynomial number of bounded word displacements can remove.

Two endpoints \(z_i,z_j\) therefore agree outside \(S\). Their difference
\[
h=z_i-z_j
\]
satisfies
\[
h\ge0,\qquad
\operatorname{supp}h\subseteq S,\qquad h\ne0.
\tag{12}
\]
The last assertion follows from strict decrease of \(\Phi\).

## 3.3 Transport the displacement back to the original state

A pump at the later phase \(z_i\) would not suffice. We need one at the original \(x\).

Let the prefix be \(x\to z_i\). Execute
\[
x\longrightarrow z_i
\longrightarrow z_i-h
\longrightarrow x-h,
\tag{13}
\]
where the last segment is the directed reverse prefix, translated downward by \(h\).

This translation is enabled. Subtraction affects only the large coordinates in \(S\). If the prefix has \(t\) inward words, it suffices to reserve
\[
\min_{i\in S}x_i>2Bt+r+Y.
\tag{14}
\]
For a forward microstep with source \(u\) and reactant \(y_r\), its translated reverse can use background \(u-y_r-h\ge0\). The fixed complex-return word is then enabled throughout. Coordinates outside \(S\) are unchanged by the translation.

Thus \(x-h\in P_S\).

Choose a stored start \(p\le x-h\), with stored pump
\[
p\longrightarrow p+\widehat h,
\qquad
0\ne\widehat h\ge0,\quad
\operatorname{supp}\widehat h\subseteq S.
\]
Outside \(S\), \(p+\widehat h=p\le x\). Inside \(S\), the thresholds exceed every fixed coordinate of every stored \(p+\widehat h\). Therefore
\[
p+\widehat h\le x.
\]
The stored reverse word gives the required **fixed-length** transition
\[
x\longrightarrow x-\widehat h.
\tag{15}
\]

The potentially long path in (13) proves availability. It is not the path used for the subsequent conductance bound.

---

# 4. A finite catalytic joining construction

## 4.1 Initial indexed templates

Construct a finite indexed list of connected directed closed-walk templates containing:

1. Original weak-reversibility cycles covering every original reaction.
2. Every stored pump followed by its directed reverse.
3. Each pump closed walk translated by \(2e_i\), for every coordinate \(i\).
4. An original directed return cycle through every channel in the accepted nominal-gap table.

For item 4, if the accepted channel is
\[
y_r+w\longrightarrow z_r+w,
\]
translate an original complex-return cycle through \(r\) by \(w\).

Each template edge is therefore an allowed catalytic copy of an original reaction. Every original \(w=0\) channel is included.

## 4.2 Join at a coordinatewise maximum

Take two previously constructed components \(C,D\) using disjoint sets of initial indices. Choose vertices \(c\in C\), \(b\in D\), and set
\[
H=c\vee b
\]
coordinatewise.

Translate \(C\) by \(H-c\), translate \(D\) by \(H-b\), and take their union. The shifts are nonnegative, and the two components meet at \(H\).

The result is again strongly connected and balanced as a directed multigraph.

Include **every** component obtainable by binary joins of disjoint index sets, with each initial index used at most once, and include all partial joins.

This family is finite: each join strictly increases the number of initial indices used, and each stage has finitely many component and vertex choices.

The distinction from an unrestricted recursive closure is decisive. If a component already contains the required pump index, we will use that pump inside the component. If it does not, the required join is already in the finite family.

## 4.3 Exact graph preservation

An added edge always has the form
\[
y_r+w\longrightarrow z_r+w,\qquad w\ge0.
\]
Whenever it is enabled, the corresponding original reaction is enabled and has the same destination population.

Since every original \(w=0\) channel remains,
\[
\boxed{\text{The entire directed population graph is exactly the original graph.}}
\tag{16}
\]

This holds at every population, including populations outside the input class.

---

# 5. Nominal rates and exact stationarity

Let:

- \(J\ge1\) be the total number of edge occurrences across the finite joined family;
- \(D\ge1\) bound the **total degree** of every complex in the family and every stored pump displacement.

Set
\[
\alpha=
\frac1{2J}\prod_{i=1}^d\min(1,\lambda_i)^D.
\tag{17}
\]

Give every edge occurrence with source complex \(c\) the coefficient
\[
\beta_c=\alpha\lambda^{-c}.
\tag{18}
\]

Aggregate occurrences with the same original label \(r\) and catalyst \(w\). If their fixed multiplicity is \(m_{r,w}\), the physical output coefficient is simply
\[
\boxed{
\kappa_{r,w}
=m_{r,w}\alpha\lambda^{-(y_r+w)}.
}
\tag{19}
\]

Distinct original reaction labels remain distinct.

Put
\[
A=(d+1)D.
\]
Since \(W\ge\lambda_i,\lambda_i^{-1}\),
\[
\frac1{2J}W^{-A}
\le\beta_c\le\frac1{2J}.
\]
Consequently,
\[
\boxed{
0<\kappa_{r,w}\le\frac12,\qquad
\max_{r,w}\kappa_{r,w}^{-1}\le2JW^A.
}
\tag{20}
\]

All these coefficients are ordinary positive rationals.

## 5.1 Constant stationary flux around each translated component

At population \(x=n+c\), the stationary flux of an occurrence with source \(c\) is
\[
\begin{aligned}
\pi_\lambda(n+c)\,
\beta_c(n+c)^{\underline c}
&=
\frac{\alpha}{Z_\Gamma}
\frac{\lambda^n}{n!}.
\end{aligned}
\tag{21}
\]

It is independent of the edge’s position within the component.

Every component is balanced. Its translates therefore give exact stationary flow balance. If one translated vertex lies in \(\Gamma\), all vertices of that connected translated component lie in \(\Gamma\).

Summing components proves exact conditional-Poisson balance on the actual class. Polynomial activity is integrable against each conditional-Poisson law, so this balance gives a nonexplosive nominal process with stationary law \(\pi_\lambda\). A quantitative bound on that activity will be proved below without a rare-class estimate.

## 5.2 Retain the accepted ordinary gap by domination

Each channel in the accepted nominal-gap table has a matching family occurrence, with the same reactant and jump. Its accepted coefficient is at most one, whereas the matching occurrence has coefficient at least
\[
k_{\min}=(2J)^{-1}W^{-A}.
\]

Thus, channel by channel,
\[
\mathcal E(f)\ge k_{\min}\mathcal E_0(f).
\]
Equation (2) gives
\[
\boxed{
\operatorname{Var}_{\pi_\lambda}(f)
\le 2JG_0W^{A+g_0}\mathcal E(f).
}
\tag{22}
\]

This requires no cycle decomposition of the accepted generator and no online evaluation of its rates.

---

# 6. Every tail activity has a short path with comparable conductance

Write
\[
w(x)=\pi_\lambda(x)a(x).
\]

At a tail state \(x\), choose a largest enabled family occurrence. Its stationary flux is at least \(w(x)/J\). Let its source be \(c\), in component \(C\).

Select the fixed inward pump from Section 3:
\[
p+\widehat h\longrightarrow p.
\]
Let \(B\) denote its initial template index and \(b=p+\widehat h\).

## Case 1: \(B\) is absent from \(C\)

The join of \(C\) and \(B\) at
\[
H=c\vee b
\]
is already in the family. Both \(c,b\le x\), so \(H\le x\).

Follow the pump in that joined component. It runs physically from \(x\) to \(x-\widehat h\). Relative to the selected occurrence, every path-edge flux has ratio
\[
\frac{\lambda^{x-H}/(x-H)!}
     {\lambda^{x-c}/(x-c)!}
=
\lambda^{-(H-c)}
(x-c)^{\underline{H-c}}
\ge W^{-D}.
\tag{23}
\]

The falling factorial is a positive integer because the join is enabled.

## Case 2: \(B\) is already present in \(C\)

Let its translated downward pump inside \(C\) run
\[
b'\longrightarrow b'-\widehat h.
\]
Put \(n=x-c\). Execute:

1. a directed path \(c\to b'\) in \(C\), with background \(n\);
2. the downward pump, with background \(n\);
3. a directed path \(b'\to c\) in \(C\), with background \(n-\widehat h\).

The final population is \(x-\widehat h\).

The last background is nonnegative because \(\widehat h\) touches only large coordinates, exceeding every fixed source and displacement bound. Its flux ratio relative to the initial background is
\[
\frac{\lambda^{n-\widehat h}/(n-\widehat h)!}
     {\lambda^n/n!}
=
\lambda^{-\widehat h}n^{\underline{\widehat h}}
\ge W^{-D}.
\tag{24}
\]

Therefore both cases give a path \(\gamma_x\) to
\[
\rho(x)=x-\widehat h(x)
\tag{25}
\]
whose every edge has stationary flux at least
\[
\frac{w(x)}{JW^D}.
\tag{26}
\]

All path lengths and offsets belong to fixed finite lists. Let \(\ell\) bound their lengths. Every path stays within coordinate distance \(2D\) of its starting state, so any fixed edge location can be charged by at most
\[
(4D+1)^d
\]
starting states, with at most \(\ell\) uses per path.

Cauchy–Schwarz along the paths gives
\[
\boxed{
\sum_{x\notin H}w(x)
  \bigl(f(x)-f(\rho(x))\bigr)^2
\le K_{\rm path}W^D\mathcal E(f),
}
\tag{27}
\]
where the explicit choice
\[
\boxed{
K_{\rm path}=2\ell^2(4D+1)^dJ
}
\tag{28}
\]
suffices.

This is the universal conductance statement that was missing from the earlier route: **activity at every added channel is covered, including activity introduced by the controlling construction itself.**

---

# 7. The parent state has substantially greater activity weight

Let \(M\ge1\) bound the number of stored pump displacements.

Enlarge the polynomial head so that every coordinate touched by a selected \(\widehat h\) exceeds \(4D\) and \(2^{D+3}MW\).

Every enabled channel remains enabled after subtracting \(\widehat h\), and its falling-factorial intensity loses at most a factor \(2^{-D}\). Hence
\[
a(x-\widehat h)\ge2^{-D}a(x).
\tag{29}
\]

Also,
\[
\frac{\pi_\lambda(x-\widehat h)}{\pi_\lambda(x)}
=
\lambda^{-\widehat h}x^{\underline{\widehat h}}.
\tag{30}
\]

Every factor corresponding to a changed coordinate is large compared with its activity \(\lambda_i\). The chosen threshold yields
\[
\boxed{
w(\rho(x))\ge4M\,w(x).
}
\tag{31}
\]

Each state has at most \(M\) preimages under \(\rho\), because the displacement list is fixed. Therefore, for any nonnegative \(F\),
\[
\boxed{
\sum_{x\notin H}w(x)F(\rho(x))
\le\frac14\sum_yw(y)F(y).
}
\tag{32}
\]

The normalizing constant cancels throughout. No lower bound on the probability of the class is used.

---

# 8. Derivation of all three nominal hypotheses

## 8.1 Weighted activity inequality

Put \(u=f-\pi_\lambda f\). From
\[
u(x)^2
\le2\bigl(u(x)-u(\rho(x))\bigr)^2
  +2u(\rho(x))^2,
\]
equations (27) and (32) give
\[
\sum_xw(x)u(x)^2
\le
2\sum_{x\in H}w(x)u(x)^2
+
4K_{\rm path}W^D\mathcal E(f).
\tag{33}
\]

The head term is bounded by
\[
\sum_Hwu^2
\le\bigl(\sup_Ha\bigr)\operatorname{Var}_{\pi_\lambda}(f).
\]
Use the ordinary gap (22).

Thus a polynomial head and polynomial head activity yield the required polynomial weighted inequality. Explicit constants appear in Section 9.

The argument may first be applied on finite population balls. Since \(\rho(x)\le x\) coordinatewise, parents remain 

## Complete visible response (accessibility representation)

heading ChatGPT said:, Value: 4
									111 text ChatGPT said:
								112 heading Result, Value: 2
									113 text Result
								114 text Under the accepted starting mathematics in your message, I obtain an affirmative construction for the full compiler.
								115 text  The new step is a finite catalytic construction that supplies the three nominal hypotheses of completed 
								116 container
									117 text 136C for every fixed weakly reversible 
									118 text 𝑅
								119 text :
								120 container
									121 container
										122 container
											123 text ∑
											124 container
												125 text 𝑥 ∈ Γ
											126 text 𝜋
											127 text 𝜆
											128 text ( 𝑥 ) 𝑎 ( 𝑥 ) ( 𝑓 ( 𝑥 ) −
											129 text 𝜋
											130 text 𝜆
											131 text 𝑓
											132 text )
											133 text 2
										134 container
											135 text ≤
											136 text 𝐶
											137 text 𝐺
											138 text 𝑊
											139 container
												140 text 𝑝 𝐺
											141 text 𝐸 ( 𝑓 ) ,
										142 container
											143 text 𝑎 ( 𝑥 )
										144 container
											145 text ≥
											146 text 𝑐
											147 text 𝑎
											148 text 𝑊
											149 container
												150 text −
												151 text 𝑝
												152 text 𝑎
											153 text ( 1 + ∣ 𝑥
											154 text ∣
											155 text 1
											156 text )
											157 text 2
											158 text ,
										159 container
											160 text 𝜋
											161 text 𝜆
											162 text 𝑎
										163 container
											164 text ≤
											165 text 𝐶
											166 text 𝐴
											167 text 𝑊
											168 container
												169 text 𝑝 𝐴
											170 text .
									171 text (1)
								172 text Here 
								173 text 𝑎
								174 text  counts 
								175 text all actual labelled firing intensities, including null channels
								176 text . Every constant and exponent in (1) is computable from 
								177 text 𝑅
								178 text . The augmentation is fixed before 
								179 container
									180 text 𝑥
									181 text 0
									182 text , 𝜆 , 𝜖
								183 text  are supplied. The construction uses finite original reaction words, closes them under a finite joining operation, and assigns exact cycle-balanced rates. The crucial point is that the joining operation controls the activity introduced by its own added channels. It does not require an endless sequence of further catalytic additions. Applying the 
								184 text accepted full 136C transfer
								185 text  to (1) supplies the required rational 
								186 container
									187 text 𝛿 , 𝑇
								188 text , uniform nonexplosion and positive recurrence, both stationary accuracy requirements, both transient accuracy requirements, and the expected number of actual firings. I give the construction, the universal argument, and the resource accounting below. The final transfer is inherited capital; I am not claiming an independent reproof of 136C.
								189 heading 1. Accepted inputs and notation, Value: 1
									190 text 1. Accepted inputs and notation
								191 text I use these accepted operations at their stated scopes:
								192 content list
									193 container
										194 AXListMarker 1. 
										195 text Bounded inward words.
										196 text  Outside a computable polynomial head, the actual class has an original enabled word
										197 container
											198 text 𝑥 ⟶ 𝑥 − 𝑔
										199 text whose displacement and excursion are bounded by fixed-
										200 text 𝑅
										201 text  constants, whose displacement has signs directed toward 
										202 container
											203 text 𝑥 0
										204 text , and which strictly decreases
										205 container
											206 text Φ ( 𝑥 ) = ∥ 𝑥 −
											207 text 𝑥
											208 text 0
											209 text ∥
											210 text 2
											211 text .
									212 container
										213 AXListMarker 2. 
										214 text The nominal physical-gap construction.
										215 text  Its fixed catalytic channel table admits, for each input, rates at most one with invariant law 
										216 container
											217 text 𝜋 𝜆
										218 text  and
										219 container
											220 container
												221 container
													222 text Var ⁡
												223 container
													224 text 𝜋 𝜆
												225 text ( 𝑓 ) ≤
												226 text 𝐺
												227 text 0
												228 text 𝑊
												229 container
													230 text 𝑔 0
												231 text 𝐸
												232 text 0
												233 text ( 𝑓 ) .
											234 text (2)
										235 text Only its fixed channel table and quantitative gap theorem will be needed. The new compiler will not need to evaluate its rates.
									236 container
										237 AXListMarker 3. 
										238 text Completed 136C.
										239 text  Its full constructive transfer applies once the three inequalities in (1), the rational-rate bounds, and compilation costs are supplied.
								240 text Write
								241 container
									242 text 𝑥
									243 container
										244 text 𝑐 ‾
									245 text =
									246 text ∏
									247 text 𝑖
									248 container
										249 text 𝑥
										250 text 𝑖
										251 text !
									252 container
										253 text (
										254 text 𝑥
										255 text 𝑖
										256 text −
										257 text 𝑐
										258 text 𝑖
										259 text ) !
									260 text ,
								261 text with value zero unless 
								262 container
									263 text 𝑥 ≥ 𝑐
								264 text  coordinatewise. For the new nominal generator 
								265 text 𝑄
								266 text , put
								267 container
									268 container
										269 text 𝑎 ( 𝑥 ) =
										270 text ∑
										271 text 𝑒
										272 text 𝑞
										273 text 𝑒
										274 text ( 𝑥 ) , 𝐸 ( 𝑓 ) =
										275 text 1
										276 text 2
										277 text ∑
										278 container
											279 text 𝑥 , 𝑒
										280 text 𝜋
										281 text 𝜆
										282 text ( 𝑥 )
										283 text 𝑞
										284 text 𝑒
										285 text ( 𝑥 ) ( 𝑓 ( 𝑥 +
										286 text 𝜈
										287 text 𝑒
										288 text ) − 𝑓 ( 𝑥 )
										289 text )
										290 text 2
										291 text .
									292 text (3)
								293 text The index 
								294 text 𝑒
								295 text  denotes physical labelled channels. An occurrence decomposition used in the proof will sum exactly to these physical rates. The new construction has three parts:
								296 content list
									297 container
										298 AXListMarker • 
										299 text compute finitely many original words that add nonnegative population;
									300 container
										301 AXListMarker • 
										302 text use their reverses to obtain fixed inward words in every sufficiently remote state;
									303 container
										304 AXListMarker • 
										305 text join their closed cycles so that every large firing activity has a short path toward substantially greater 
										306 container
											307 text 𝜋
											308 text 𝜆
											309 text 𝑎
										310 text -weight.
								311 heading 2. An effective finite collection of nonnegative pumping words, Value: 1
									312 text 2. An effective finite collection of nonnegative pumping words
								313 text For each nonempty coordinate set 
								314 container
									315 text 𝑆 ⊆ { 1 , … , 𝑑 }
								316 text , define
								317 container
									318 container
										319 text 𝑃
										320 text 𝑆
										321 text =
										322 text {
										323 text 𝑝
										324 text ∈
										325 container
											326 text 𝑁 𝑑
										327 text :
										328 text 𝑝
										329 text ⟶
										330 text 𝑝
										331 text +
										332 text ℎ
										333 text  for some 
										334 text 0
										335 text ≠
										336 text ℎ
										337 text ∈
										338 container
											339 text 𝑁 𝑑
										340 text ,
										341 text supp
										342 text ⁡
										343 text ℎ
										344 text ⊆
										345 text 𝑆
										346 text }
										347 text .
									348 text (4)
								349 text Every path here uses original enabled reactions. The set 
								350 container
									351 text 𝑃 𝑆
								352 text  is upward closed: a word enabled at 
								353 text 𝑝
								354 text  remains enabled after adding any nonnegative background. Dickson’s lemma therefore gives a finite covering set of starting markings. For the resource contract, existence of a finite set is insufficient. We need a terminating procedure that finds one and certifies that it covers all of 
								355 container
									356 text 𝑃 𝑆
								357 text .
								358 heading 2.1 Actual communication as a monomial congruence, Value: 2
									359 text 2.1 Actual communication as a monomial congruence
								360 text Form the binomial ideal
								361 container
									362 container
										363 text 𝐼
										364 text 𝑅
										365 text =
										366 text ⟨
										367 container
											368 text 𝑋
											369 text 𝑦
											370 text 𝑟
										371 text −
										372 container
											373 text 𝑋
											374 text 𝑧
											375 text 𝑟
										376 text :
										377 text 𝑟
										378 text ∈
										379 text 𝑅
										380 text ⟩
										381 text ⊆ 𝑄 [
										382 text 𝑋
										383 text 1
										384 text , … ,
										385 text 𝑋
										386 text 𝑑
										387 text ] .
									388 text (5)
								389 text As a vector space, this ideal is spanned by differences of monomials connected by translated reaction relations. Consequently its quotient has one basis element for each connected monomial class, and
								390 container
									391 container
										392 text 𝑋
										393 text 𝑢
										394 text −
										395 text 𝑋
										396 text 𝑣
										397 text ∈
										398 text 𝐼
										399 text 𝑅
										400 text ⟺ 𝑢 , 𝑣  are connected by translated reaction relations .
									401 text (6)
								402 text Weak reversibility makes this exactly 
								403 text actual communication
								404 text . Indeed, the reverse of an enabled reaction
								405 container
									406 text 𝑛 +
									407 text 𝑦
									408 text 𝑟
									409 text ⟶ 𝑛 +
									410 text 𝑧
									411 text 𝑟
								412 text can be executed by translating a fixed original complex-graph path from 
								413 container
									414 text 𝑧 𝑟
								415 text  back to 
								416 container
									417 text 𝑦 𝑟
								418 text  by the same 
								419 container
									420 text 𝑛 ≥ 0
								421 text . Thus (6) uses the actual enabled graph, including its boundary restrictions.
								422 heading 2.2 A terminating test for a pump inside a downward box, Value: 2
									423 text 2.2 A terminating test for a pump inside a downward box
								424 text Consider a box whose coordinates in 
								425 text 𝐵
								426 text  have upper bounds 
								427 container
									428 text 𝑏 𝑖
								429 text , with the remaining coordinates 
								430 text 𝐹
								431 text  unrestricted. Because 
								432 container
									433 text 𝑃 𝑆
								434 text  is upward closed, the box intersects 
								435 container
									436 text 𝑃 𝑆
								437 text  precisely when it contains a pump starting with bounded coordinates exactly 
								438 text 𝑏
								439 text . Define
								440 container
									441 container
										442 text 𝐽
										443 text 𝑏
										444 text =
										445 text (
										446 container
											447 text 𝐼 𝑅
										448 text :
										449 container
											450 text 𝑋 𝐵 𝑏
										451 text )
										452 text :
										453 container
											454 text (
											455 text ∏
											456 container
												457 text 𝑗 ∈ 𝐹
											458 text 𝑋
											459 text 𝑗
											460 text )
										461 text ∞
										462 text ,
										463 text 𝐾
										464 text 𝑏
										465 text =
										466 text 𝐽
										467 text 𝑏
										468 text ∩ 𝑄 [
										469 text 𝑋
										470 text 𝑖
										471 text : 𝑖 ∈ 𝑆 ] .
									472 text (7)
								473 text The box intersects 
								474 container
									475 text 𝑃 𝑆
								476 text  if and only if 
								477 container
									478 text 𝐾 𝑏
								479 text  contains
								480 container
									481 container
										482 text 𝑋
										483 text ℎ
										484 text − 1 for some  0 ≠ ℎ ≥ 0  supported on  𝑆 .
									485 text (8)
								486 text The saturation in (7) supplies a sufficiently large free-coordinate background. Conversely, any finite free-coordinate background is dominated by some common power of the saturating monomial. There is an exact finite test for (8):
								487 container
									488 container
										489 text ∃ 0 ≠ ℎ ≥ 0 ,
										490 text 𝑋
										491 text ℎ
										492 text − 1 ∈
										493 text 𝐾
										494 text 𝑏
										495 text ⟺ ∃ 𝑖 ∈ 𝑆 : 1 ∈
										496 text 𝐾
										497 text 𝑏
										498 text + ⟨
										499 text 𝑋
										500 text 𝑖
										501 text ⟩ .
									502 text (9)
								503 text The reverse implication deserves explanation. Monomial colons, monomial saturation, and elimination preserve the quotient’s description by monomial congruence classes. If 
								504 container
									505 text 1 =
									506 text 𝑋
									507 text 𝑖
									508 text 𝐹
								509 text  in that quotient, expand 
								510 text 𝐹
								511 text  into monomials. The coefficient of the class of 
								512 text 1
								513 text  must receive a contribution from at least one monomial 
								514 container
									515 text 𝑋
									516 text 𝑖
									517 text 𝑋
									518 text 𝑢
								519 text  in that same class. Hence
								520 container
									521 text 𝑋
									522 text 𝑖
									523 text 𝑋
									524 text 𝑢
									525 text − 1 ∈
									526 text 𝐾
									527 text 𝑏
									528 text .
								529 text This is a genuine nonconstant monomial relation. All operations in (7)–(9) are terminating exact Gröbner-basis operations over 
								530 text 𝑄
								531 text .
								532 heading 2.3 Computing and certifying the finite cover, Value: 2
									533 text 2.3 Computing and certifying the finite cover
								534 text Maintain a finite list 
								535 text 𝐴
								536 text  of witnessed pumping starts. The complement
								537 container
									538 text 𝑁
									539 text 𝑑
									540 text ∖ ↑ 𝐴
								541 text is an effectively computable finite union of downward boxes: for each 
								542 container
									543 text 𝑎 ∈ 𝐴
								544 text , an uncovered marking must satisfy 
								545 container
									546 text 𝑝
									547 text 𝑖
									548 text <
									549 text 𝑎
									550 text 𝑖
								551 text  for at least one coordinate. Test those boxes using (7)–(9). If a box contains a pump, enumerate original reaction words until finding one with nonzero nonnegative displacement supported on 
								552 text 𝑆
								553 text , whose minimal enabling marking lies in that box. A word 
								554 container
									555 text 𝑟
									556 text 1
									557 text ⋯
									558 text 𝑟
									559 text ℓ
								560 text  has explicitly computable minimal enabling marking
								561 container
									562 container
										563 text 𝑝
										564 text 𝑖
										565 text = max ⁡
										566 text (
										567 text 0
										568 text ,
										569 container
											570 text max
											571 text ⁡
											572 text 1
											573 text ≤
											574 text 𝑗
											575 text ≤
											576 text ℓ
										577 container
											578 text [
											579 text 𝑦
											580 container
												581 text 𝑟
												582 text 𝑗
												583 text , 𝑖
											584 text −
											585 text ∑
											586 container
												587 text 𝑘 < 𝑗
											588 text (
											589 text 𝑧
											590 container
												591 text 𝑟
												592 text 𝑘
												593 text , 𝑖
											594 text −
											595 text 𝑦
											596 container
												597 text 𝑟
												598 text 𝑘
												599 text , 𝑖
											600 text ) ]
										601 text )
										602 text .
									603 text (10)
								604 text A positive box test guarantees that this search terminates. Add its start and witness word. Each new start lies outside the upward closure of all previous starts. Dickson’s lemma excludes an infinite such sequence. When every remaining box tests negative, the list is certified complete. Perform this for every nonempty 
								605 text 𝑆
								606 text , and store directed reverse words as well.
								607 container
									608 text This is finite, computable preprocessing depending only on 
									609 text 𝑅
									610 text .
								611 text  It uses no supplied reachability, counting, class, or stationary-law oracle.
								612 heading 3. Every sufficiently remote state admits a fixed inward pump, Value: 1
									613 text 3. Every sufficiently remote state admits a fixed inward pump
								614 text The next step connects the accepted inward geometry with the finite lists just constructed. Let 
								615 container
									616 text 𝐵 ≥ 1
								617 text  bound each coordinate of an accepted inward word’s endpoint displacement, and let 
								618 text 𝑟
								619 text  bound its internal excursion. Let 
								620 text 𝑌
								621 text  bound original reactant coordinates. We will establish:
								622 container
									623 text Outside a computable polynomial head, every 
									624 container
										625 text 𝑥 ∈ Γ
									626 text  has a stored fixed-length original word
								627 container
									628 text 𝑥 ⟶ 𝑥 −
									629 text ℎ
									630 text ^
									631 text ,
								632 container
									633 text where 
									634 container
										635 text 0 ≠
										636 text ℎ
										637 text ^
										638 text ≥ 0
									639 text , and every coordinate changed by 
									640 container
										641 text ℎ ^
									642 text  is larger than all fixed catalytic thresholds and a sufficiently large fixed multiple of 
									643 text 𝑊
									644 text .
								645 text This does not require interpreting “sign-conformal” as a no-overshoot condition.
								646 heading 3.1 Separate large and small coordinates, Value: 2
									647 text 3.1 Separate large and small coordinates
								648 text Choose a polynomial threshold 
								649 container
									650 text 𝐴
									651 text 0
									652 text ( 𝑊 )
								653 text  dominating the inherited geometric head, 
								654 container
									655 text ∣
									656 text 𝑥
									657 text 0
									658 text ∣
									659 text 1
								660 text , 
								661 text 𝑊
								662 text , and the fixed constants needed below. Define
								663 container
									664 container
										665 text 𝐴
										666 container
											667 text 𝑘 + 1
										668 text =
										669 text 𝐾
										670 text 𝑅
										671 text (
										672 text 𝐴
										673 text 𝑘
										674 text + 1
										675 text )
										676 container
											677 text 𝑑 + 1
										678 text , 0 ≤ 𝑘 < 𝑑 .
									679 text (11)
								680 text If 
								681 container
									682 container
										683 text max ⁡
									684 text 𝑖
									685 text 𝑥
									686 text 𝑖
									687 text >
									688 text 𝐴
									689 text 𝑑
								690 text , one of the 
								691 text 𝑑
								692 text  intervals
								693 container
									694 text (
									695 text 𝐴
									696 text 𝑘
									697 text ,
									698 text 𝐴
									699 container
										700 text 𝑘 + 1
									701 text ] , 0 ≤ 𝑘 < 𝑑 ,
								702 text contains no coordinate of 
								703 text 𝑥
								704 text . One coordinate is already above 
								705 container
									706 text 𝐴 𝑑
								707 text , leaving at most 
								708 container
									709 text 𝑑 − 1
								710 text  coordinates for these 
								711 text 𝑑
								712 text  intervals. For an empty interval, put
								713 container
									714 text 𝑆 = { 𝑖 :
									715 text 𝑥
									716 text 𝑖
									717 text >
									718 text 𝐴
									719 container
										720 text 𝑘 + 1
									721 text } .
								722 text Then 
								723 container
									724 text 𝑆 ≠ ∅
								725 text , while every coordinate outside 
								726 text 𝑆
								727 text  is at most 
								728 container
									729 text 𝐴 𝑘
								730 text .
								731 heading 3.2 Find a nonnegative displacement supported on , Value: 2
									732 text 3.2 Find a nonnegative displacement supported on 
									733 text 𝑆
								734 text Follow the accepted inward words for more than the number of possible outside-
								735 text 𝑆
								736 text  endpoint configurations. Their outside-
								737 text 𝑆
								738 text  coordinates remain bounded by 
								739 container
									740 text 𝐴
									741 text 𝑘
									742 text + 𝐵
								743 text : bounded sign-directed steps can overshoot their target only by a bounded amount. The coordinates in 
								744 text 𝑆
								745 text  stay above 
								746 container
									747 text 𝑥 0
								748 text , and stay large, because (11) reserves much more population than this polynomial number of bounded word displacements can remove. Two endpoints 
								749 container
									750 text 𝑧
									751 text 𝑖
									752 text ,
									753 text 𝑧
									754 text 𝑗
								755 text  therefore agree outside 
								756 text 𝑆
								757 text . Their difference
								758 container
									759 text ℎ =
									760 text 𝑧
									761 text 𝑖
									762 text −
									763 text 𝑧
									764 text 𝑗
								765 text satisfies
								766 container
									767 container
										768 text ℎ ≥ 0 , supp ⁡ ℎ ⊆ 𝑆 , ℎ ≠ 0.
									769 text (12)
								770 text The last assertion follows from strict decrease of 
								771 text Φ
								772 text .
								773 heading 3.3 Transport the displacement back to the original state, Value: 2
									774 text 3.3 Transport the displacement back to the original state
								775 text A pump at the later phase 
								776 container
									777 text 𝑧 𝑖
								778 text  would not suffice. We need one at the original 
								779 text 𝑥
								780 text . Let the prefix be 
								781 container
									782 text 𝑥 →
									783 text 𝑧
									784 text 𝑖
								785 text . Execute
								786 container
									787 container
										788 text 𝑥 ⟶
										789 text 𝑧
										790 text 𝑖
										791 text ⟶
										792 text 𝑧
										793 text 𝑖
										794 text − ℎ ⟶ 𝑥 − ℎ ,
									795 text (13)
								796 text where the last segment is the directed reverse prefix, translated downward by 
								797 text ℎ
								798 text . This translation is enabled. Subtraction affects only the large coordinates in 
								799 text 𝑆
								800 text . If the prefix has 
								801 text 𝑡
								802 text  inward words, it suffices to reserve
								803 container
									804 container
										805 container
											806 text min ⁡
										807 container
											808 text 𝑖 ∈ 𝑆
										809 text 𝑥
										810 text 𝑖
										811 text > 2 𝐵 𝑡 + 𝑟 + 𝑌 .
									812 text (14)
								813 text For a forward microstep with source 
								814 text 𝑢
								815 text  and reactant 
								816 container
									817 text 𝑦 𝑟
								818 text , its translated reverse can use background 
								819 container
									820 text 𝑢 −
									821 text 𝑦
									822 text 𝑟
									823 text − ℎ ≥ 0
								824 text . The fixed complex-return word is then enabled throughout. Coordinates outside 
								825 text 𝑆
								826 text  are unchanged by the translation. Thus 
								827 container
									828 text 𝑥 − ℎ ∈
									829 text 𝑃
									830 text 𝑆
								831 text . Choose a stored start 
								832 container
									833 text 𝑝 ≤ 𝑥 − ℎ
								834 text , with stored pump
								835 container
									836 text 𝑝 ⟶ 𝑝 +
									837 text ℎ
									838 text ^
									839 text , 0 ≠
									840 text ℎ
									841 text ^
									842 text ≥ 0 , supp ⁡
									843 text ℎ
									844 text ^
									845 text ⊆ 𝑆 .
								846 text Outside 
								847 text 𝑆
								848 text , 
								849 container
									850 text 𝑝 +
									851 text ℎ
									852 text ^
									853 text = 𝑝 ≤ 𝑥
								854 text . Inside 
								855 text 𝑆
								856 text , the thresholds exceed every fixed coordinate of every stored 
								857 container
									858 text 𝑝 +
									859 text ℎ
									860 text ^
								861 text . Therefore
								862 container
									863 text 𝑝 +
									864 text ℎ
									865 text ^
									866 text ≤ 𝑥 .
								867 text The stored reverse word gives the required 
								868 text fixed-length
								869 text  transition
								870 container
									871 container
										872 text 𝑥 ⟶ 𝑥 −
										873 text ℎ
										874 text ^
										875 text .
									876 text (15)
								877 text The potentially long path in (13) proves availability. It is not the path used for the subsequent conductance bound.
								878 heading 4. A finite catalytic joining construction, Value: 1
									879 text 4. A finite catalytic joining construction
								880 heading 4.1 Initial indexed templates, Value: 2
									881 text 4.1 Initial indexed templates
								882 text Construct a finite indexed list of connected directed closed-walk templates containing:
								883 content list
									884 container
										885 AXListMarker 1. 
										886 text Original weak-reversibility cycles covering every original reaction.
									887 container
										888 AXListMarker 2. 
										889 text Every stored pump followed by its directed reverse.
									890 container
										891 AXListMarker 3. 
										892 text Each pump closed walk translated by 
										893 container
											894 text 2
											895 text 𝑒
											896 text 𝑖
										897 text , for every coordinate 
										898 text 𝑖
										899 text .
									900 container
										901 AXListMarker 4. 
										902 text An original directed return cycle through every channel in the accepted nominal-gap table.
								903 text For item 4, if the accepted channel is
								904 container
									905 text 𝑦
									906 text 𝑟
									907 text + 𝑤 ⟶
									908 text 𝑧
									909 text 𝑟
									910 text + 𝑤 ,
								911 text translate an original complex-return cycle through 
								912 text 𝑟
								913 text  by 
								914 text 𝑤
								915 text . Each template edge is therefore an allowed catalytic copy of an original reaction. Every original 
								916 container
									917 text 𝑤 = 0
								918 text  channel is included.
								919 heading 4.2 Join at a coordinatewise maximum, Value: 2
									920 text 4.2 Join at a coordinatewise maximum
								921 text Take two previously constructed components 
								922 container
									923 text 𝐶 , 𝐷
								924 text  using disjoint sets of initial indices. Choose vertices 
								925 container
									926 text 𝑐 ∈ 𝐶
								927 text , 
								928 container
									929 text 𝑏 ∈ 𝐷
								930 text , and set
								931 container
									932 text 𝐻 = 𝑐 ∨ 𝑏
								933 text coordinatewise. Translate 
								934 text 𝐶
								935 text  by 
								936 container
									937 text 𝐻 − 𝑐
								938 text , translate 
								939 text 𝐷
								940 text  by 
								941 container
									942 text 𝐻 − 𝑏
								943 text , and take their union. The shifts are nonnegative, and the two components meet at 
								944 text 𝐻
								945 text . The result is again strongly connected and balanced as a directed multigraph. Include 
								946 text every
								947 text  component obtainable by binary joins of disjoint index sets, with each initial index used at most once, and include all partial joins. This family is finite: each join strictly increases the number of initial indices used, and each stage has finitely many component and vertex choices. The distinction from an unrestricted recursive closure is decisive. If a component already contains the required pump index, we will use that pump inside the component. If it does not, the required join is already in the finite family.
								948 heading 4.3 Exact graph preservation, Value: 2
									949 text 4.3 Exact graph preservation
								950 text An added edge always has the form
								951 container
									952 text 𝑦
									953 text 𝑟
									954 text + 𝑤 ⟶
									955 text 𝑧
									956 text 𝑟
									957 text + 𝑤 , 𝑤 ≥ 0.
								958 text Whenever it is enabled, the corresponding original reaction is enabled and has the same destination population. Since every original 
								959 container
									960 text 𝑤 = 0
								961 text  channel remains,
								962 container
									963 text The entire directed population graph is exactly the original graph.
									964 text (16)
								965 text This holds at every population, including populations outside the input class.
								966 heading 5. Nominal rates and exact stationarity, Value: 1
									967 text 5. Nominal rates and exact stationarity
								968 text Let:
								969 content list
									970 container
										971 AXListMarker • 
										972 container
											973 text 𝐽 ≥ 1
										974 text  be the total number of edge occurrences across the finite joined family;
									975 container
										976 AXListMarker • 
										977 container
											978 text 𝐷 ≥ 1
										979 text  bound the  total degree  of every complex in the family and every stored pump displacement.
								980 text Set
								981 container
									982 container
										983 text 𝛼 =
										984 text 1
										985 container
											986 text 2 𝐽
										987 text ∏
										988 container
											989 text 𝑖 = 1
										990 text 𝑑
										991 text min ⁡ ( 1 ,
										992 text 𝜆
										993 text 𝑖
										994 text )
										995 text 𝐷
										996 text .
									997 text (17)
								998 text Give every edge occurrence with source complex 
								999 text 𝑐
								1000 text  the coefficient
								1001 container
									1002 container
										1003 text 𝛽
										1004 text 𝑐
										1005 text = 𝛼
										1006 text 𝜆
										1007 container
											1008 text − 𝑐
										1009 text .
									1010 text (18)
								1011 text Aggregate occurrences with the same original label 
								1012 text 𝑟
								1013 text  and catalyst 
								1014 text 𝑤
								1015 text . If their fixed multiplicity is 
								1016 container
									1017 text 𝑚
									1018 text 𝑟
									1019 text ,
									1020 text 𝑤
								1021 text , the physical output coefficient is simply
								1022 container
									1023 container
										1024 text 𝜅
										1025 container
											1026 text 𝑟 , 𝑤
										1027 text =
										1028 text 𝑚
										1029 container
											1030 text 𝑟 , 𝑤
										1031 text 𝛼
										1032 text 𝜆
										1033 container
											1034 text − (
											1035 text 𝑦
											1036 text 𝑟
											1037 text + 𝑤 )
										1038 text .
									1039 text (19)
								1040 text Distinct original reaction labels remain distinct. Put
								1041 container
									1042 text 𝐴 = ( 𝑑 + 1 ) 𝐷 .
								1043 text Since 
								1044 container
									1045 text 𝑊 ≥
									1046 text 𝜆
									1047 text 𝑖
									1048 text ,
									1049 text 𝜆
									1050 text 𝑖
									1051 container
										1052 text − 1
								1053 text ,
								1054 container
									1055 text 1
									1056 container
										1057 text 2 𝐽
									1058 text 𝑊
									1059 container
										1060 text − 𝐴
									1061 text ≤
									1062 text 𝛽
									1063 text 𝑐
									1064 text ≤
									1065 text 1
									1066 container
										1067 text 2 𝐽
									1068 text .
								1069 text Consequently,
								1070 container
									1071 container
										1072 text 0 <
										1073 text 𝜅
										1074 container
											1075 text 𝑟 , 𝑤
										1076 text ≤
										1077 text 1
										1078 text 2
										1079 text ,
										1080 container
											1081 text max ⁡
										1082 container
											1083 text 𝑟 , 𝑤
										1084 text 𝜅
										1085 container
											1086 text 𝑟 , 𝑤
										1087 container
											1088 text − 1
										1089 text ≤ 2 𝐽
										1090 text 𝑊
										1091 text 𝐴
										1092 text .
									1093 text (20)
								1094 text All these coefficients are ordinary positive rationals.
								1095 heading 5.1 Constant stationary flux around each translated component, Value: 2
									1096 text 5.1 Constant stationary flux around each translated component
								1097 text At population 
								1098 container
									1099 text 𝑥 = 𝑛 + 𝑐
								1100 text , the stationary flux of an occurrence with source 
								1101 text 𝑐
								1102 text  is
								1103 container
									1104 container
										1105 container
											1106 text 𝜋
											1107 text 𝜆
											1108 text ( 𝑛 + 𝑐 )
											1109 text 𝛽
											1110 text 𝑐
											1111 text ( 𝑛 + 𝑐
											1112 text )
											1113 container
												1114 text 𝑐 ‾
										1115 container
											1116 text =
											1117 text 𝛼
											1118 container
												1119 text 𝑍 Γ
											1120 container
												1121 text 𝜆 𝑛
											1122 container
												1123 text 𝑛 !
											1124 text .
									1125 text (21)
								1126 text It is independent of the edge’s position within the component. Every component is balanced. Its translates therefore give exact stationary flow balance. If one translated vertex lies in 
								1127 text Γ
								1128 text , all vertices of that connected translated component lie in 
								1129 text Γ
								1130 text . Summing components proves exact conditional-Poisson balance on the actual class. Polynomial activity is integrable against each conditional-Poisson law, so this balance gives a nonexplosive nominal process with stationary law 
								1131 container
									1132 text 𝜋 𝜆
								1133 text . A quantitative bound on that activity will be proved below without a rare-class estimate.
								1134 heading 5.2 Retain the accepted ordinary gap by domination, Value: 2
									1135 text 5.2 Retain the accepted ordinary gap by domination
								1136 text Each channel in the accepted nominal-gap table has a matching family occurrence, with the same reactant and jump. Its accepted coefficient is at most one, whereas the matching occurrence has coefficient at least
								1137 container
									1138 text 𝑘
									1139 text min
									1140 text ⁡
									1141 text = ( 2 𝐽
									1142 text )
									1143 container
										1144 text − 1
									1145 text 𝑊
									1146 container
										1147 text − 𝐴
									1148 text .
								1149 text Thus, channel by channel,
								1150 container
									1151 text 𝐸 ( 𝑓 ) ≥
									1152 text 𝑘
									1153 text min
									1154 text ⁡
									1155 text 𝐸
									1156 text 0
									1157 text ( 𝑓 ) .
								1158 text Equation (2) gives
								1159 container
									1160 container
										1161 container
											1162 text Var ⁡
										1163 container
											1164 text 𝜋 𝜆
										1165 text ( 𝑓 ) ≤ 2 𝐽
										1166 text 𝐺
										1167 text 0
										1168 text 𝑊
										1169 container
											1170 text 𝐴 +
											1171 text 𝑔
											1172 text 0
										1173 text 𝐸 ( 𝑓 ) .
									1174 text (22)
								1175 text This requires no cycle decomposition of the accepted generator and no online evaluation of its rates.
								1176 heading 6. Every tail activity has a short path with comparable conductance, Value: 1
									1177 text 6. Every tail activity has a short path with comparable conductance
								1178 text Write
								1179 container
									1180 text 𝑤 ( 𝑥 ) =
									1181 text 𝜋
									1182 text 𝜆
									1183 text ( 𝑥 ) 𝑎 ( 𝑥 ) .
								1184 text At a tail state 
								1185 text 𝑥
								1186 text , choose a largest enabled family occurrence. Its stationary flux is at least 
								1187 container
									1188 text 𝑤 ( 𝑥 ) / 𝐽
								1189 text . Let its source be 
								1190 text 𝑐
								1191 text , in component 
								1192 text 𝐶
								1193 text . Select the fixed inward pump from Section 3:
								1194 container
									1195 text 𝑝 +
									1196 text ℎ
									1197 text ^
									1198 text ⟶ 𝑝 .
								1199 text Let 
								1200 text 𝐵
								1201 text  denote its initial template index and 
								1202 container
									1203 text 𝑏 = 𝑝 +
									1204 text ℎ
									1205 text ^
								1206 text .
								1207 heading Case 1: is absent from , Value: 2
									1208 text Case 1: 
									1209 text 𝐵
									1210 text  is absent from 
									1211 text 𝐶
								1212 text The join of 
								1213 text 𝐶
								1214 text  and 
								1215 text 𝐵
								1216 text  at
								1217 container
									1218 text 𝐻 = 𝑐 ∨ 𝑏
								1219 text is already in the family. Both 
								1220 container
									1221 text 𝑐 , 𝑏 ≤ 𝑥
								1222 text , so 
								1223 container
									1224 text 𝐻 ≤ 𝑥
								1225 text . Follow the pump in that joined component. It runs physically from 
								1226 text 𝑥
								1227 text  to 
								1228 container
									1229 text 𝑥 −
									1230 text ℎ
									1231 text ^
								1232 text . Relative to the selected occurrence, every path-edge flux has ratio
								1233 container
									1234 container
										1235 container
											1236 text 𝜆
											1237 container
												1238 text 𝑥 − 𝐻
											1239 text / ( 𝑥 − 𝐻 ) !
										1240 container
											1241 text 𝜆
											1242 container
												1243 text 𝑥 − 𝑐
											1244 text / ( 𝑥 − 𝑐 ) !
										1245 text =
										1246 text 𝜆
										1247 container
											1248 text − ( 𝐻 − 𝑐 )
										1249 text ( 𝑥 − 𝑐
										1250 text )
										1251 container
											1252 text 𝐻
											1253 text −
											1254 text 𝑐
											1255 text ‾
										1256 text ≥
										1257 text 𝑊
										1258 container
											1259 text − 𝐷
										1260 text .
									1261 text (23)
								1262 text The falling factorial is a positive integer because the join is enabled.
								1263 heading Case 2: is already present in , Value: 2
									1264 text Case 2: 
									1265 text 𝐵
									1266 text  is already present in 
									1267 text 𝐶
								1268 text Let its translated downward pump inside 
								1269 text 𝐶
								1270 text  run
								1271 container
									1272 text 𝑏
									1273 text ′
									1274 text ⟶
									1275 text 𝑏
									1276 text ′
									1277 text −
									1278 text ℎ
									1279 text ^
									1280 text .
								1281 text Put 
								1282 container
									1283 text 𝑛 = 𝑥 − 𝑐
								1284 text . Execute:
								1285 content list
									1286 container
										1287 AXListMarker 1. 
										1288 text a directed path 
										1289 container
											1290 text 𝑐 →
											1291 text 𝑏
											1292 text ′
										1293 text  in 
										1294 text 𝐶
										1295 text , with background 
										1296 text 𝑛
										1297 text ;
									1298 container
										1299 AXListMarker 2. 
										1300 text the downward pump, with background 
										1301 text 𝑛
										1302 text ;
									1303 container
										1304 AXListMarker 3. 
										1305 text a directed path 
										1306 container
											1307 text 𝑏
											1308 text ′
											1309 text → 𝑐
										1310 text  in 
										1311 text 𝐶
										1312 text , with background 
										1313 container
											1314 text 𝑛 −
											1315 text ℎ
											1316 text ^
										1317 text .
								1318 text The final population is 
								1319 container
									1320 text 𝑥 −
									1321 text ℎ
									1322 text ^
								1323 text . The last background is nonnegative because 
								1324 container
									1325 text ℎ ^
								1326 text  touches only large coordinates, exceeding every fixed source and displacement bound. Its flux ratio relative to the initial background is
								1327 container
									1328 container
										1329 container
											1330 text 𝜆
											1331 container
												1332 text 𝑛 −
												1333 text ℎ
												1334 text ^
											1335 text / ( 𝑛 −
											1336 text ℎ
											1337 text ^
											1338 text ) !
										1339 container
											1340 text 𝜆
											1341 text 𝑛
											1342 text / 𝑛 !
										1343 text =
										1344 text 𝜆
										1345 container
											1346 text −
											1347 text ℎ
											1348 text ^
										1349 text 𝑛
										1350 container
											1351 text ℎ
											1352 text ^
											1353 text ‾
										1354 text ≥
										1355 text 𝑊
										1356 container
											1357 text − 𝐷
										1358 text .
									1359 text (24)
								1360 text Therefore both cases give a path 
								1361 container
									1362 text 𝛾 𝑥
								1363 text  to
								1364 container
									1365 container
										1366 text 𝜌 ( 𝑥 ) = 𝑥 −
										1367 text ℎ
										1368 text ^
										1369 text ( 𝑥 )
									1370 text (25)
								1371 text whose every edge has stationary flux at least
								1372 container
									1373 container
										1374 container
											1375 text 𝑤 ( 𝑥 )
										1376 container
											1377 text 𝐽
											1378 text 𝑊
											1379 text 𝐷
										1380 text .
									1381 text (26)
								1382 text All path lengths and offsets belong to fixed finite lists. Let 
								1383 text ℓ
								1384 text  bound their lengths. Every path stays within coordinate distance 
								1385 container
									1386 text 2 𝐷
								1387 text  of its starting state, so any fixed edge location can be charged by at most
								1388 container
									1389 text ( 4 𝐷 + 1
									1390 text )
									1391 text 𝑑
								1392 text starting states, with at most 
								1393 text ℓ
								1394 text  uses per path. Cauchy–Schwarz along the paths gives
								1395 container
									1396 container
										1397 text ∑
										1398 container
											1399 text 𝑥 ∉ 𝐻
										1400 text 𝑤 ( 𝑥 ) ( 𝑓 ( 𝑥 ) − 𝑓 ( 𝜌 ( 𝑥 ) )
										1401 text )
										1402 text 2
										1403 text ≤
										1404 text 𝐾
										1405 container
											1406 text p a t h
										1407 text 𝑊
										1408 text 𝐷
										1409 text 𝐸 ( 𝑓 ) ,
									1410 text (27)
								1411 text where the explicit choice
								1412 container
									1413 container
										1414 text 𝐾
										1415 container
											1416 text p a t h
										1417 text = 2
										1418 text ℓ
										1419 text 2
										1420 text ( 4 𝐷 + 1
										1421 text )
										1422 text 𝑑
										1423 text 𝐽
									1424 text (28)
								1425 text suffices. This is the universal conductance statement that was missing from the earlier route: 
								1426 text activity at every added channel is covered, including activity introduced by the controlling construction itself.
								1427 heading 7. The parent state has substantially greater activity weight, Value: 1
									1428 text 7. The parent state has substantially greater activity weight
								1429 text Let 
								1430 container
									1431 text 𝑀 ≥ 1
								1432 text  bound the number of stored pump displacements. Enlarge the polynomial head so that every coordinate touched by a selected 
								1433 container
									1434 text ℎ ^
								1435 text  exceeds 
								1436 container
									1437 text 4 𝐷
								1438 text  and 
								1439 container
									1440 text 2
									1441 container
										1442 text 𝐷 + 3
									1443 text 𝑀 𝑊
								1444 text . Every enabled channel remains enabled after subtracting 
								1445 container
									1446 text ℎ ^
								1447 text , and its falling-factorial intensity loses at most a factor 
								1448 container
									1449 text 2
									1450 text −
									1451 text 𝐷
								1452 text . Hence
								1453 container
									1454 container
										1455 text 𝑎 ( 𝑥 −
										1456 text ℎ
										1457 text ^
										1458 text ) ≥
										1459 text 2
										1460 container
											1461 text − 𝐷
										1462 text 𝑎 ( 𝑥 ) .
									1463 text (29)
								1464 text Also,
								1465 container
									1466 container
										1467 container
											1468 text 𝜋
											1469 text 𝜆
											1470 text ( 𝑥 −
											1471 text ℎ
											1472 text ^
											1473 text )
										1474 container
											1475 text 𝜋
											1476 text 𝜆
											1477 text ( 𝑥 )
										1478 text =
										1479 text 𝜆
										1480 container
											1481 text −
											1482 text ℎ
											1483 text ^
										1484 text 𝑥
										1485 container
											1486 text ℎ
											1487 text ^
											1488 text ‾
										1489 text .
									1490 text (30)
								1491 text Every factor corresponding to a changed coordinate is large compared with its activity 
								1492 container
									1493 text 𝜆 𝑖
								1494 text . The chosen threshold yields
								1495 container
									1496 container
										1497 text 𝑤 ( 𝜌 ( 𝑥 ) ) ≥ 4 𝑀 𝑤 ( 𝑥 ) .
									1498 text (31)
								1499 text Each state has at most 
								1500 text 𝑀
								1501 text  preimages under 
								1502 text 𝜌
								1503 text , because the displacement list is fixed. Therefore, for any nonnegative 
								1504 text 𝐹
								1505 text ,
								1506 container
									1507 container
										1508 text ∑
										1509 container
											1510 text 𝑥 ∉ 𝐻
										1511 text 𝑤 ( 𝑥 ) 𝐹 ( 𝜌 ( 𝑥 ) ) ≤
										1512 text 1
										1513 text 4
										1514 text ∑
										1515 text 𝑦
										1516 text 𝑤 ( 𝑦 ) 𝐹 ( 𝑦 ) .
									1517 text (32)
								1518 text The normalizing constant cancels throughout. No lower bound on the probability of the class is used.
								1519 heading 8. Derivation of all three nominal hypotheses, Value: 1
									1520 text 8. Derivation of all three nominal hypotheses
								1521 heading 8.1 Weighted activity inequality, Value: 2
									1522 text 8.1 Weighted activity inequality
								1523 text Put 
								1524 container
									1525 text 𝑢 = 𝑓 −
									1526 text 𝜋
									1527 text 𝜆
									1528 text 𝑓
								1529 text . From
								1530 container
									1531 text 𝑢 ( 𝑥
									1532 text )
									1533 text 2
									1534 text ≤ 2 ( 𝑢 ( 𝑥 ) − 𝑢 ( 𝜌 ( 𝑥 ) )
									1535 text )
									1536 text 2
									1537 text + 2 𝑢 ( 𝜌 ( 𝑥 )
									1538 text )
									1539 text 2
									1540 text ,
								1541 text equations (27) and (32) give
								1542 container
									1543 container
										1544 text ∑
										1545 text 𝑥
										1546 text 𝑤 ( 𝑥 ) 𝑢 ( 𝑥
										1547 text )
										1548 text 2
										1549 text ≤ 2
										1550 text ∑
										1551 container
											1552 text 𝑥 ∈ 𝐻
										1553 text 𝑤 ( 𝑥 ) 𝑢 ( 𝑥
										1554 text )
										1555 text 2
										1556 text + 4
										1557 text 𝐾
										1558 container
											1559 text p a t h
										1560 text 𝑊
										1561 text 𝐷
										1562 text 𝐸 ( 𝑓 ) .
									1563 text (33)
								1564 text The head term is bounded by
								1565 container
									1566 text ∑
									1567 text 𝐻
									1568 text 𝑤
									1569 text 𝑢
									1570 text 2
									1571 text ≤ (
									1572 container
										1573 text sup ⁡
									1574 text 𝐻
									1575 text 𝑎 )
									1576 container
										1577 text Var ⁡
									1578 container
										1579 text 𝜋 𝜆
									1580 text ( 𝑓 ) .
								1581 text Use the ordinary gap (22). Thus a polynomial head and polynomial head activity yield the required polynomial weighted inequality. Explicit constants appear in Section 9. The argument may first be applied on finite population balls. Since 
								1582 container
									1583 text 𝜌 ( 𝑥 ) ≤ 𝑥
								1584 text  coordinatewise, parents remain in the ball, and the absorption is valid before taking limits. There is no assumption that the desired weighted norm is already finite.
								1585 heading 8.2 Polynomial stationary activity, Value: 2
									1586 text 8.2 Polynomial stationary activity
								1587 text Take 
								1588 container
									1589 text 𝐹 = 1
								1590 text  in (32). Then
								1591 container
									1592 container
										1593 text 𝜋
										1594 text 𝜆
										1595 text 𝑎 ≤
										1596 text 4
										1597 text 3
										1598 container
											1599 text sup ⁡
										1600 text 𝐻
										1601 text 𝑎 .
									1602 text (34)
								1603 text Again this can be proved first on finite balls and then passed to the limit. It supplies a quantitative bound without a rare-class normalization estimate.
								1604 heading 8.3 Quadratic lower bound on activity, Value: 2
									1605 text 8.3 Quadratic lower bound on activity
								1606 text On a non-singleton class, every state has an enabled original nonnull reaction. Hence
								1607 container
									1608 container
										1609 text 𝑎 ( 𝑥 ) ≥ ( 2 𝐽
										1610 text )
										1611 container
											1612 text − 1
										1613 text 𝑊
										1614 container
											1615 text − 𝐴
										1616 text .
									1617 text (35)
								1618 text This gives the required quadratic bound inside a polynomial head after paying the head’s squared radius. In the tail, choose 
								1619 text 𝑖
								1620 text  attaining 
								1621 container
									1622 container
										1623 text max ⁡
									1624 text 𝑗
									1625 text 𝑥
									1626 text 𝑗
								1627 text . It belongs to the large-coordinate set 
								1628 text 𝑆
								1629 text . The selected pump template translated by 
								1630 container
									1631 text 2
									1632 text 𝑒
									1633 text 𝑖
								1634 text  is enabled, because the additional two molecules are available there. One of its source intensities is at least a fixed polynomial fraction of 
								1635 container
									1636 text 𝑥 𝑖 2
								1637 text . Since 
								1638 container
									1639 text 𝑥
									1640 text 𝑖
									1641 text ≥ ∣ 𝑥
									1642 text ∣
									1643 text 1
									1644 text / 𝑑
								1645 text ,
								1646 container
									1647 container
										1648 text 𝑎 ( 𝑥 ) ≥
										1649 text 𝑐
										1650 text 𝑅
										1651 text 𝑊
										1652 container
											1653 text − 𝑝
										1654 text ( 1 + ∣ 𝑥
										1655 text ∣
										1656 text 1
										1657 text )
										1658 text 2
										1659 text .
									1660 text (36)
								1661 text The translation by 
								1662 container
									1663 text 2
									1664 text 𝑒
									1665 text 𝑖
								1666 text  is an installed catalytic copy. It adds no species or population-change vector.
								1667 heading 9. Explicit constants for the new construction, Value: 1
									1668 text 9. Explicit constants for the new construction
								1669 text Here is one conservative set of choices. Normalize the inherited geometric head as
								1670 container
									1671 text { 𝑥 :
									1672 container
										1673 text max ⁡
									1674 text 𝑖
									1675 text 𝑥
									1676 text 𝑖
									1677 text ≤
									1678 text 𝑐
									1679 text 𝑔
									1680 text 𝑊
									1681 container
										1682 text 𝑝 𝑔
									1683 text } ,
								1684 text with computable 
								1685 container
									1686 text 𝑐
									1687 text 𝑔
									1688 text ,
									1689 text 𝑝
									1690 text 𝑔
									1691 text ≥ 1
								1692 text . Retain the inherited gap constants 
								1693 container
									1694 text 𝐺
									1695 text 0
									1696 text ,
									1697 text 𝑔
									1698 text 0
								1699 text  from (2). Let
								1700 container
									1701 text 𝑝 = max ⁡ ( 1 , ⌈
									1702 text 𝑝
									1703 text 𝑔
									1704 text ⌉ ) , 𝐾 = 8 𝐵
									1705 text 3
									1706 text 𝑑
									1707 text + 4 ( 𝑟 + 𝑌 + 1 ) + 4 ,
								1708 text and set
								1709 container
									1710 container
										1711 text 𝐶
										1712 text 0
										1713 text = 1 + ⌈
										1714 text 𝑐
										1715 text 𝑔
										1716 text ⌉ + 4 𝐷 + 4 𝐵 + 4 𝑟 + 4 𝑌 +
										1717 text 2
										1718 container
											1719 text 𝐷 + 3
										1720 text 𝑀 .
									1721 text (37)
								1722 text Define
								1723 container
									1724 container
										1725 text 𝐴
										1726 text 0
										1727 text ( 𝑊 ) =
										1728 text 𝐶
										1729 text 0
										1730 text 𝑊
										1731 text 𝑝
										1732 text ,
										1733 text 𝐴
										1734 container
											1735 text 𝑘 + 1
										1736 text ( 𝑊 ) = 𝐾 (
										1737 text 𝐴
										1738 text 𝑘
										1739 text ( 𝑊 ) + 1
										1740 text )
										1741 container
											1742 text 𝑑 + 1
										1743 text .
									1744 text (38)
								1745 text For a monomial upper bound, recursively define
								1746 container
									1747 container
										1748 text 𝐶
										1749 container
											1750 text 𝑘 + 1
										1751 text = 𝐾 ( 2
										1752 text 𝐶
										1753 text 𝑘
										1754 text )
										1755 container
											1756 text 𝑑 + 1
										1757 text ,
										1758 text 𝐶
										1759 text 𝐻
										1760 text =
										1761 text 𝐶
										1762 text 𝑑
										1763 text , 𝑞 = 𝑝 ( 𝑑 + 1
										1764 text )
										1765 text 𝑑
										1766 text .
									1767 text (39)
								1768 text Then
								1769 container
									1770 text 𝐴
									1771 text 𝑑
									1772 text ( 𝑊 ) ≤
									1773 text 𝐶
									1774 text 𝐻
									1775 text 𝑊
									1776 text 𝑞
									1777 text .
								1778 text These choices pay for the tail argument. For example, at a separating band one may take
								1779 container
									1780 text 𝑡 =
									1781 text ⌈
									1782 text (
									1783 text 3
									1784 container
										1785 text 𝐴 𝑘
									1786 container
										1787 text ) 𝑑
									1788 text ⌉
									1789 text + 1 ≤ 2 ⋅
									1790 text 3
									1791 text 𝑑
									1792 text 𝐴
									1793 text 𝑘
									1794 text 𝑑
									1795 text .
								1796 text The outside-coordinate endpoint box has fewer than 
								1797 container
									1798 text 𝑡 + 1
								1799 text  states, while
								1800 container
									1801 container
										1802 text min ⁡
									1803 container
										1804 text 𝑖 ∈ 𝑆
									1805 text 𝑥
									1806 text 𝑖
									1807 text − 2 𝐵 𝑡 − 𝑟 − 𝑌 > 0
								1808 text and all endpoints remain beyond the inherited head. Use
								1809 container
									1810 container
										1811 text 𝐻 = { 𝑥 :
										1812 container
											1813 text max ⁡
										1814 text 𝑖
										1815 text 𝑥
										1816 text 𝑖
										1817 text ≤
										1818 text 𝐴
										1819 text 𝑑
										1820 text ( 𝑊 ) } ,
										1821 text 𝑀
										1822 text 𝑎
										1823 text = 𝐽 ( 𝑑 + 1
										1824 text )
										1825 text 𝐷
										1826 text 𝐶
										1827 text 𝐻
										1828 text 𝐷
										1829 text .
									1830 text (40)
								1831 text Then
								1832 container
									1833 container
										1834 text sup ⁡
									1835 text 𝐻
									1836 text 𝑎 ≤
									1837 text 𝑀
									1838 text 𝑎
									1839 text 𝑊
									1840 container
										1841 text 𝑞 𝐷
									1842 text .
								1843 text With 
								1844 container
									1845 text 𝐴 = ( 𝑑 + 1 ) 𝐷
								1846 text , the required explicit certificates are:
								1847 table
									1848 row
										1849 cell
											1850 text Quantity
										1851 cell
											1852 text Bound
									1853 row
										1854 cell
											1855 text Rate reciprocals
										1856 cell
											1857 container
												1858 container
													1859 text max ⁡
												1860 text 𝑒
												1861 text 𝜅
												1862 text 𝑒
												1863 container
													1864 text − 1
												1865 text ≤ 2 𝐽
												1866 text 𝑊
												1867 text 𝐴
									1868 row
										1869 cell
											1870 text Ordinary Poincaré constant
										1871 cell
											1872 container
												1873 text 2 𝐽
												1874 text 𝐺
												1875 text 0
												1876 text 𝑊
												1877 container
													1878 text 𝐴 +
													1879 text 𝑔
													1880 text 0
									1881 row
										1882 cell
											1883 text Stationary activity
										1884 cell
											1885 container
												1886 text 𝜋
												1887 text 𝜆
												1888 text 𝑎 ≤ 2
												1889 text 𝑀
												1890 text 𝑎
												1891 text 𝑊
												1892 container
													1893 text 𝑞 𝐷
									1894 row
										1895 cell
											1896 text Activity lower bound
										1897 cell
											1898 text ( \displaystyle a(x)\ge\frac{W^{-(A+2q)}}{8J(d+1)^2C_H^2}(1+
									1899 row
										1900 cell
											1901 text Weighted Poincaré constant
										1902 cell
											1903 container
												1904 text 𝐶
												1905 text 𝐺
												1906 text 𝑊
												1907 container
													1908 text 𝑝 𝐺
								1909 container
									1910 button Copy table
									1911 pop up button (collapsed) Description: Expand table, Secondary Actions: Expand
								1912 text Here
								1913 container
									1914 container
										1915 text 𝐶
										1916 text 𝐺
										1917 text = 4 (
										1918 text 𝑀
										1919 text 𝑎
										1920 text 𝐽
										1921 text 𝐺
										1922 text 0
										1923 text +
										1924 text 𝐾
										1925 container
											1926 text p a t h
										1927 text ) ,
										1928 text 𝑝
										1929 text 𝐺
										1930 text = max ⁡ ( 𝑞 𝐷 + 𝐴 +
										1931 text 𝑔
										1932 text 0
										1933 text , 𝐷 ) ,
									1934 text (41)
								1935 text and 
								1936 container
									1937 text 𝐾
									1938 text p
									1939 text a
									1940 text t
									1941 text h
								1942 text  is given in (28). Thus the three new inputs to 136C can be taken as
								1943 container
									1944 container
										1945 container
											1946 text 𝐶 𝐴
										1947 container
											1948 text = 2
											1949 text 𝑀
											1950 text 𝑎
											1951 text ,
										1952 container
											1953 text 𝑝 𝐴
										1954 container
											1955 text = 𝑞 𝐷 ,
										1956 container
											1957 text 𝑐 𝑎
										1958 container
											1959 text =
											1960 text 1
											1961 container
												1962 text 8 𝐽 ( 𝑑 + 1
												1963 text )
												1964 text 2
												1965 text 𝐶
												1966 text 𝐻
												1967 text 2
											1968 text ,
										1969 container
											1970 text 𝑝 𝑎
										1971 container
											1972 text = 𝐴 + 2 𝑞 ,
										1973 container
											1974 text 𝐶 𝐺
										1975 container
											1976 text = 4 (
											1977 text 𝑀
											1978 text 𝑎
											1979 text 𝐽
											1980 text 𝐺
											1981 text 0
											1982 text +
											1983 text 𝐾
											1984 container
												1985 text p a t h
											1986 text ) ,
										1987 container
											1988 text 𝑝 𝐺
										1989 container
											1990 text = max ⁡ ( 𝑞 𝐷 + 𝐴 +
											1991 text 𝑔
											1992 text 0
											1993 text , 𝐷 ) .
									1994 text (42)
								1995 text Every object on the right is obtained from terminating fixed-
								1996 text 𝑅
								1997 text  preprocessing and the accepted fixed-
								1998 text 𝑅
								1999 text  constants.
								2000 heading 10. The compiler, Value: 1
									2001 text 10. The compiler
								2002 heading Fixed- preprocessing, Value: 2
									2003 text Fixed-
									2004 text 𝑅
									2005 text  preprocessing
								2006 text The deterministic preprocessing performs:
								2007 content list
									2008 container
										2009 AXListMarker 1. 
										2010 text Compute original directed complex-return paths.
									2011 container
										2012 AXListMarker 2. 
										2013 text Obtain the accepted nominal-gap channel table and quantitative constants.
									2014 container
										2015 AXListMarker 3. 
										2016 text Compute and certify the finite pump lists for every nonempty 
										2017 text 𝑆
										2018 text .
									2019 container
										2020 AXListMarker 4. 
										2021 text Build the initial indexed closed-walk templates.
									2022 container
										2023 AXListMarker 5. 
										2024 text Enumerate every disjoint-index binary join.
									2025 container
										2026 AXListMarker 6. 
										2027 text Aggregate the resulting physical 
										2028 container
											2029 text ( 𝑟 , 𝑤 )
										2030 text  channel table and record its multiplicities.
									2031 container
										2032 AXListMarker 7. 
										2033 text Compute 
										2034 container
											2035 text 𝐷 , 𝐽 , 𝑀 , ℓ
										2036 text , the head constants, and the bounds in (42).
									2037 container
										2038 AXListMarker 8. 
										2039 text Compose those certificates with the accepted quantitative 136C routine.
								2040 text Every algebraic calculation, word search, stored path, join, and multiplicity is included in this preprocessing.
								2041 heading Variable-input compilation, Value: 2
									2042 text Variable-input compilation
								2043 text For 
								2044 container
									2045 text 𝑥
									2046 text 0
									2047 text , 𝜆 , 𝜖
								2048 text :
								2049 content list
									2050 container
										2051 AXListMarker 1. 
										2052 text Test whether any original nonnull reaction is enabled at 
										2053 container
											2054 text 𝑥 0
										2055 text .
									2056 container
										2057 AXListMarker 2. 
										2058 text For a non-singleton class, evaluate the rational rates (17)–(19).
									2059 container
										2060 AXListMarker 3. 
										2061 text Evaluate the required rational certificate bounds from 
										2062 text 𝑊
										2063 text .
									2064 container
										2065 AXListMarker 4. 
										2066 text Invoke the accepted completed-136C compiler with those rates and certificates.
									2067 container
										2068 AXListMarker 5. 
										2069 text Output its rational tolerance 
										2070 container
											2071 text 𝛿 ≤ 1 / 2
										2072 text  and rational time 
										2073 container
											2074 text 𝑇 > 0
										2075 text .
								2076 text The state-dependent choices of pumps, parents, and paths are proof devices. 
								2077 text The installed process evaluates none of them.
								2078 text  Its coefficients are fixed before it runs. In particular, for non-singleton inputs, the nominal rate formula depends only on 
								2079 text 𝜆
								2080 text . The initial marking and accuracy requirement enter the quantitative tolerance and time bounds.
								2081 heading Singleton and empty cases, Value: 2
									2082 text Singleton and empty cases
								2083 text A class is a singleton exactly when no original nonnull reaction is enabled at 
								2084 container
									2085 text 𝑥 0
								2086 text . This is a finite direct check. For that branch, use the same fixed augmentation and, for example, output
								2087 container
									2088 text 𝜅
									2089 container
										2090 text 𝑟 , 𝑤
									2091 text = 1 , 𝛿 =
									2092 text 1
									2093 text 2
									2094 text , 𝑇 = 1.
								2095 text Graph preservation ensures no added spatial transition is enabled. The whole law is exactly 
								2096 container
									2097 text 𝛿
									2098 text 𝑥
									2099 text 0
								2100 text  at every time, so all four accuracy errors are zero. Enabled null channels have constant total perturbed intensity at most
								2101 container
									2102 text 3
									2103 text 2
									2104 text 𝐽 ( 1 + ∣
									2105 text 𝑥
									2106 text 0
									2107 text ∣
									2108 text 1
									2109 text )
									2110 text 𝐷
									2111 text .
								2112 text Their expected firing count is therefore polynomially bounded. The empty-network case has zero firings.
								2113 heading 11. Independent coefficient errors and actual firing counts, Value: 1
									2114 text 11. Independent coefficient errors and actual firing counts
								2115 text The physical coefficient in (19) may contain several virtual cycle contributions. Under an admitted physical error, write
								2116 container
									2117 container
										2118 text 𝜅 ~
									2119 container
										2120 text 𝑟 , 𝑤
									2121 text =
									2122 text 𝛾
									2123 container
										2124 text 𝑟 , 𝑤
									2125 text 𝜅
									2126 container
										2127 text 𝑟 , 𝑤
									2128 text ,
									2129 text 𝛾
									2130 container
										2131 text 𝑟 , 𝑤
									2132 text ∈ [ 1 − 𝛿 , 1 + 𝛿 ] .
								2133 text The proof decomposition can assign that same multiplier to each corresponding contribution. Those virtual errors are correlated, but they lie within the independent-error envelope. A theorem valid for every independent choice also covers this correlated subclass. More directly, the certificates in (1) concern the 
								2134 text actual aggregated nominal generator
								2135 text , to which 136C applies. The occurrence decomposition introduces no additional physical firing. Its summed intensity is exactly the actual channel intensity. Null channels and distinct original parallel labels are included in 
								2136 text 𝑎
								2137 text , so the accepted transfer’s firing estimate pays for the requested total. Since 
								2138 container
									2139 text 𝛿 ≤ 1 / 2
								2140 text , every physical coefficient remains positive, and the entire spatial graph remains unchanged under every admitted perturbation.
								2141 heading 12. Full resource constants and the four guarantees, Value: 1
									2142 text 12. Full resource constants and the four guarantees
								2143 text The only quantitative routine inherited at this final stage is the 
								2144 text already accepted full 136C transfer
								2145 text . Feed it:
								2146 content list
									2147 container
										2148 AXListMarker • 
										2149 text the fixed physical channel table;
									2150 container
										2151 AXListMarker • 
										2152 text the rational-rate formula;
									2153 container
										2154 AXListMarker • 
										2155 text the rate-reciprocal bound;
									2156 container
										2157 AXListMarker • 
										2158 text the three explicit certificates in (42);
									2159 container
										2160 AXListMarker • 
										2161 text the fixed degree, jump, and encoding bounds.
								2162 text Let its resulting fixed-
								2163 text 𝑅
								2164 text  resource constants, after this substitution, be
								2165 container
									2166 text 𝐶
									2167 container
										2168 text 136 , 𝑅
									2169 text ,
									2170 text 𝑝
									2171 container
										2172 text 136 , 𝑅
									2173 text .
								2174 text These are computable through that accepted routine. I am using its quantitative construction as supplied capital, rather than inventing exponents from a version of its proof not reproduced here. To charge all new preprocessing, let 
								2175 container
									2176 text 𝑃 𝑅
								2177 text  be a recorded bound on the bit work, peak memory, and stored output of the terminating preprocessing above. All variable arithmetic outside 136C consists of a fixed number of exact rational operations with fixed exponents. Since
								2178 container
									2179 text log ⁡ 𝑊 =
									2180 text 𝑂
									2181 text 𝑅
									2182 text ( 𝐿 ) ,
								2183 text their bit lengths are polynomial in complete input length. A conservative schoolbook-arithmetic bound has the form
								2184 container
									2185 text 𝐶
									2186 container
										2187 text a
										2188 text r
										2189 text i
										2190 text t
										2191 text h
										2192 text , 𝑅
									2193 text ( 1 + 𝐿
									2194 text )
									2195 text 4
								2196 text for a directly computed fixed constant. For example, choose
								2197 container
									2198 container
										2199 text 𝑝
										2200 text 𝑅
										2201 text = max ⁡ { 4 ,
										2202 text 𝑝
										2203 container
											2204 text 136 , 𝑅
										2205 text , 𝐴 , 𝐷 } ,
									2206 text (43)
								2207 text and
								2208 container
									2209 container
										2210 text 𝐶
										2211 text 𝑅
										2212 text = 2 +
										2213 text 𝑃
										2214 text 𝑅
										2215 text +
										2216 text 𝐶
										2217 container
											2218 text a
											2219 text r
											2220 text i
											2221 text t
											2222 text h
											2223 text , 𝑅
										2224 text +
										2225 text 𝐶
										2226 container
											2227 text 136 , 𝑅
										2228 text + 4 𝐽 ,
									2229 text (44)
								2230 text increasing the integer by any explicitly recorded fixed encoding overhead. These are 
								2231 container
									2232 text computable constants of 
									2233 text 𝑅
								2234 text . The pump searches and join tables are charged through 
								2235 container
									2236 text 𝑃 𝑅
								2237 text ; they are not free advice or uncharged preprocessing. The accepted full transfer now gives, uniformly over all admitted fixed independent coefficient errors:
								2238 container
									2239 container
										2240 text nonexplosion and positive recurrence on  Γ ,
									2241 container
										2242 text a unique stationary law 
										2243 text 𝜇
										2244 container
											2245 text 𝜅 ~
										2246 text ,
									2247 container
										2248 text TV ⁡ (
										2249 text 𝜇
										2250 container
											2251 text 𝜅 ~
										2252 text ,
										2253 text 𝜋
										2254 text 𝜆
										2255 text ) ≤ 𝜖 ,
									2256 container
										2257 container
											2258 text max ⁡
										2259 text 𝑖
										2260 text ∣
										2261 container
											2262 text 𝐸
											2263 text 𝜇
											2264 container
												2265 text 𝜅 ~
										2266 container
											2267 text 𝑋 𝑖
										2268 text −
										2269 container
											2270 text 𝐸
											2271 text 𝜋
											2272 text 𝜆
										2273 container
											2274 text 𝑋 𝑖
										2275 text ∣
										2276 text ≤ 𝜖 ,
									2277 container
										2278 text TV ⁡  ⁣
										2279 text (
										2280 container
											2281 text Law
											2282 text ⁡
											2283 container
												2284 text 𝑥 0
											2285 text ,
											2286 container
												2287 text 𝜅 ~
										2288 text (
										2289 text 𝑋
										2290 text (
										2291 text 𝑇
										2292 text )
										2293 text )
										2294 text ,
										2295 container
											2296 text 𝜋 𝜆
										2297 text )
										2298 text ≤ 𝜖 ,
									2299 container
										2300 container
											2301 text max ⁡
										2302 text 𝑖
										2303 text ∣
										2304 container
											2305 text 𝐸
											2306 container
												2307 text 𝑥 0
											2308 text ,
											2309 container
												2310 text 𝜅 ~
										2311 container
											2312 text 𝑋 𝑖
										2313 text (
										2314 text 𝑇
										2315 text )
										2316 text −
										2317 container
											2318 text 𝐸
											2319 text 𝜋
											2320 text 𝜆
										2321 container
											2322 text 𝑋 𝑖
										2323 text ∣
										2324 text ≤ 𝜖 ,
								2325 text together with
								2326 container
									2327 text 𝑇 ,
									2328 text 𝛿
									2329 container
										2330 text − 1
									2331 text ,
									2332 container
										2333 text max ⁡
									2334 text 𝑒
									2335 text 𝜅
									2336 text 𝑒
									2337 container
										2338 text − 1
									2339 text ,
									2340 container
										2341 text sup ⁡
									2342 container
										2343 text 𝜅 ~
									2344 text 𝐸 𝐹 ( 𝑇 ) ≤
									2345 text 𝐶
									2346 text 𝑅
									2347 text 𝑊
									2348 container
										2349 text 𝑝 𝑅
									2350 text .
								2351 text Compilation work, memory, and output satisfy the corresponding
								2352 container
									2353 text 𝐶
									2354 text 𝑅
									2355 text ( 1 + 𝐿
									2356 text )
									2357 container
										2358 text 𝑝 𝑅
								2359 text bound. The absolute first moments are supplied by the accepted full transfer after proving its activity and coercivity hypotheses. They are not inferred from total variation alone.
								2360 heading What closes the previously open step, Value: 2
									2361 text What closes the previously open step
								2362 text The new universal operation is the combination of:
								2363 content list
									2364 container
										2365 AXListMarker 1. 
										2366 text Effective finite pump extraction  on the actual reaction congruence.
									2367 container
										2368 AXListMarker 2. 
										2369 text The polynomial-head tail lemma , which makes a fixed inward pump available at the original population, including boundary phases.
									2370 container
										2371 AXListMarker 3. 
										2372 text Finite disjoint-index joins , which cover the activity of every added component without infinite recursive augmentation.
									2373 container
										2374 AXListMarker 4. 
										2375 text Conductance comparison and parent-weight absorption , which prove the activity-weighted inequality, stationary activity bound, and quadratic activity lower bound for all 
										2376 text 𝑅
										2377 text .
								2378 text Those four steps supply the previously missing universal nominal design. The full robust conclusion then follows from the accepted 136C operation at exactly the whole-law, absolute-moment, and actual-firing scope stated in your question. The three helper allocations independently checked the delicate algebraic, boundary-enabling, joining, and absorption steps; their audits found no remaining gap in this construction under the accepted premises. No held paper or held artifact theorem was imported into the new argument.
								2379 

## Available visible activity (accessibility representation)

button (expanded) Worked for 81m 46s, Secondary Actions: Collapse
									108 text Worked for 81m 46s
									109 image
								2410 text I’ll continue from the accepted finite-exit operation and focus on the missing universal step: an allowed catalytic design that controls outward excursions, or a different mechanism that proves robustness. I’ll use the permitted helper slots for independent mathematical approaches, carry the source restrictions into each task, and distinguish completed results from remaining conjectures. Planned three proof approaches
								2411 container Subagent activity
									2412 container
										2413 button P3 catalytic design
										2414 text , 
										2415 button P3 alternative robustness
										2416 text  and 
										2417 button P3 obstruction audit
										2418 text  started working
								2419 text The work is split across catalytic design, alternative robustness arguments, and possible universal obstructions. I’m reading only the explicitly supplied, unheld sources at this stage. I’ve also loaded the cloud-runtime skill for local algebra checks; I won’t install anything or change access settings.
								2483 container
									2484 button (expanded) Used GitHub integration, searched the web, Secondary Actions: Collapse
									2485 container
										2486 text Used GitHub integration , searched the web
									2487 container
										2488 button (collapsed) Reviewed root polynomial activity gap findings, Secondary Actions: Expand
										2489 text Reviewed root polynomial activity gap findings
									2490 text Analyzing the Provided Information
								2423 text Tested catalyst polytope alignment pending source pointers
								2424 container Subagent activity
									2425 container
										2426 button P3 catalytic design
										2427 text , 
										2428 button P3 alternative robustness
										2429 text  and 
										2430 button P3 obstruction audit
										2431 text  updated
								2432 text Tested perturbation robustness and explored catalytic inward moves Constructed cycle-pool flows and designed inward cycle channels Derived drift bounds and aligned cycle supports Analyzed product networks, designed subset cores, and checked multiplier construction Analyzed overlap coefficients, catalyst thresholds, and feasible boundary cycles Mapped boundary classes and balanced drain-cycle catalyst inequalities Formulated channel constraints, aligned source polytopes, and reconciled boundaries Built a finite labeled graph and developed a finite-cycle lemma Tested cycle-based coercivity, divergence bounds, and finite-cycle densities Compared finite-exit outcomes, analyzed local kernels, and reassessed bounds Assessed perturbation effects and developed a cycle Harnack bound The supplied GitHub proof is accessible. It confirms that the all-activity trapping construction remains specific to that network; it does not supply the missing all-network grading. I’m now testing whether finite catalytic copies of reaction cycles can coordinate competing reactions near a boundary. The key difficulty is keeping the useful cycles enabled when some species have only a few molecules. Both optional paper fetches failed, so I’ve set them aside without retrying through another route. Searched catalytic network literature Built max-anchor fusion and checked bouquet and recurrence conditions Assessed bouquet construction, tested examples, and checked coefficient effects Constructed max-anchor gluing and checked closure Refined max-gluing proof and analyzed stability and dominant-source excursions Established finite motif cells, entropy drift, and cycle activity alignment Set cycle scaling and tested overlap gluing
								2433 container Subagent activity
									2434 container
										2435 button P3 obstruction audit
										2436 text  finished
								2437 text Derived a cycle bound without runtime checks Tested a cycle inequality and checked the AM-GM bound Tested an inequality proof and established the cycle bound
								2438 container Subagent activity
									2439 container
										2440 button P3 catalytic design
										2441 text  and 
										2442 button P3 alternative robustness
										2443 text  finished
								2444 text Derived boundary lemma, formalized access-anchor motifs, and assessed motif gluing Audited saturation proof and enumerated minimal markings Verified finite termination, checked pump geometry, and constructed shifted path Checked reverse-path feasibility and finite joined families Checked channel aggregation, coefficient bounds, and joined-network balance Verified nonexplosion using flow and checked path flux bounds Estimated flow lower bound and checked tail weight ratio Checked weighted gap and refined activity bounds Checked lower-bound derivation and specified geometric head bound Audited finite pump bounds and tested reversible-net bounds under 136C acceptance Evaluated fuel-bounded doubling, reversible cycles, and polynomial growth bounds Assessed Markov-basis claims, audited pump-detector proof, and defined counts One approach has now produced a candidate for the missing universal step. It uses finitely many original reaction words that remove population only from sufficiently large coordinates, then joins their closed cycles so that even very fast activity has a short path toward a state with greater Poisson weight. That is promising enough to audit as a possible full construction. The decisive checks are whether the finite word collection is computable and whether the cycle joins remain valid on every boundary class. I have not yet treated the candidate as proved.
								2445 container Subagent activity
									2446 container
										2447 button P3 catalytic design
										2448 text , 
										2449 button P3 obstruction audit
										2450 text  and 
										2451 button P3 alternative robustness
										2452 text  updated
								2453 text Prepared a proof artifact and formalized geometric constants
								2454 container Subagent activity
									2455 container
										2456 button P3 alternative robustness
										2457 text  updated
								2458 text Verified singleton bounds and closed C_R via 136C
								2459 container Subagent activity
									2460 container
										2461 button P3 obstruction audit
										2462 text  updated
								2463 text Prepared explicit technical proof and checked null-channel activity
								2464 container Subagent activity
									2465 container
										2466 button P3 catalytic design
										2467 text  and 
										2468 button P3 alternative robustness
										2469 text  finished
								2470 text Set singleton κ and prepared rate formulas with complexity bounds
								2471 container Subagent activity
									2472 container
										2473 button P3 obstruction audit
										2474 text  finished
								2475 text Checked finite-rate bounds, shifted reverse paths, and S-support basis Checked gate edge cases and micro accuracy Checked closure consistency The independent audits have found no remaining gap in the construction under the accepted premises. The key finite-closure argument is now clear: a component with large firing activity either already contains the required inward word, or it can be joined to that word using an unused template. This covers newly added channels without an endless sequence of further additions. I’m completing the rate, preprocessing, and firing-count accounting, then applying the accepted 136C transfer to obtain all four accuracy guarantees. Read file guidance and selected bound constants Verified endpoint and pumping bounds Designed colon saturation elimination and checked unit ideal membership Checked box wording, family domination, and rate scaling Refined the baseline bound
								2476 container Subagent activity
									2477 container
										2478 button P3 alternative robustness
										2479 text  and 
										2480 button P3 obstruction audit
										2481 text  finished
								2482 text Checked rate-family coverage and defined the Q0 table Clarified proof constants and checked time–delta bounds Applied Lax–Milgram and bounded transient firing Derived and verified Kpath explicit bounds Prepared construction proof and refined fixed-rate formulas Prepared augmentation table and bounded rational bit costs Checked constants and built conditional 136C inequality Compiled proof constants and built recursive join tables Prepared cycle-flow proof and established nonexplosion via flux Verified nominal nonexplosion
								110 

