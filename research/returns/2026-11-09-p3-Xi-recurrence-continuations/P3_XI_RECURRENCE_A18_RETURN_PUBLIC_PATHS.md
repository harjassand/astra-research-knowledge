# P3 Xi recurrence continuation return

Chat: https://chatgpt.com/c/6af0a937-daa0-83ec-99c5-8df8b56023e0
Prompt source: P3_FULL_RECURRENCE_AFTER_RADIAL_RETURN_XI_20261109.txt
Prompt turn: a18a519c-6dbb-4565-ad8e-b5360f0d05c7
Response: 1920ebd0-dc04-4a76-9019-c5d417dde3fa
Model selected at dispatch: GPT-6 standard, Extra High. Collected 9 November 2026 Brisbane.
No producer ZIP visible.

## Complete response

# Weak-reversibility recurrence: renewed investigation

**The unrestricted theorem remains unproved in this investigation.** I have not found a weakly reversible network with proved explosion, transience or null recurrence either. The current literature continues to identify arbitrary-dimensional positive recurrence as an open problem. citeturn981598search0turn981598search1turn981598view0

I examined the specified results of Kriebel, Wiuf–Xu and Agazzi–Laurence. Their conclusions do not combine automatically into the requested theorem: Kriebel's result is restricted to one linkage class and molecularity at most two; Wiuf–Xu's recurrence theorem assumes stoichiometric rank one; and Agazzi–Laurence require additional planar hypotheses together with compatible boundary estimates. citeturn959145view0turn959145view7turn959145view9turn959145view11

## 1\. A different global potential

I investigated a potential that avoids marking a particular reaction target.

Let \(\mathcal C\) be the set of complexes after removing population-preserving self-reactions. For any nonabsorbing state \(x\), define

\[
g(x)=\max_{\substack{c\in\mathcal C\\c\leq x}}(x)_c,
\qquad
V(x)=\sum_{i=1}^d\log(x_i!)-\log g(x).
\]

Equivalently,

\[
V(x)=\min_{\substack{c\in\mathcal C\\c\leq x}}
\sum_i\log((x_i-c_i)!).
\]

Because \(\mathcal C\) is finite, \(V\) is nonnegative and has finite sublevel sets. In particular,

\[
V(x)\geq
\sum_i\log(x_i!)-D_{\max}\log(1+\|x\|_1),
\]

where \(D_{\max}=\max_{c\in\mathcal C}|c|\)\.

For an enabled reaction \(s\to t\), write \(x'=x-s+t\)\. Since

\[
x'-t=x-s,
\]

direct cancellation gives the exact identity

\[
\boxed{
V(x')-V(x)
=
\log\frac{g(x)}{(x)_s}
-
\log\frac{g(x')}{(x')_t}.
}
\tag{1}
\]

This is a max-envelope version of the marked-residual factorial calculation. It does not require choosing a terminal complex or a path within a linkage class.

**Consequences.** If the fired source \(s\) maximizes \((x)_c\) among enabled complexes, then

\[
V(x')\leq V(x).
\]

Thus every reaction from a currently maximal falling-factorial source is nonincreasing for \(V\), regardless of the rate constants, molecularity, number of species or linkage classes.

There is also a uniform bound on the expected positive increment at one jump.

Let \(J\) be the number of distinct source complexes, and define their aggregate outgoing rates

\[
\bar\kappa_s=\sum_{r:y_r=s}\kappa_r,\qquad
K_\kappa=\frac{\max_s\bar\kappa_s}{\min_s\bar\kappa_s}.
\]

If \(X_1\) denotes the next population state of the embedded jump chain, then

\[
\boxed{
\mathbb E_x[(V(X_1)-V(x))_+]
\leq \frac{K_\kappa J}{e}.
}
\tag{2}
\]

To prove it, put \(u_s=(x)_s/g(x)\in(0,1]\) for enabled sources. Identity (1) yields

\[
(V(x')-V(x))_+\leq\log(1/u_s).
\]

The probability of selecting source \(s\) is

\[
p_s(x)=\frac{\bar\kappa_s(x)_s}
{\sum_z\bar\kappa_z(x)_z}
\leq K_\kappa u_s.
\]

Therefore

\[
\begin{aligned}
\mathbb E_x[(\Delta V)_+]
&\leq K_\kappa\sum_su_s\log(1/u_s)\\
&\leq K_\kappa J/e,
\end{aligned}
\]

using \(u\log(1/u)\leq1/e\)\.

This establishes a uniform bound on positive increments **per embedded jump**, not per unit of physical time. It is not a Foster drift certificate.

## 2\. A higher-rank obstruction to fixed-step drift

The potential above is useful, but it does not furnish the unrestricted recurrence theorem through any fixed number of embedded jumps.

Consider the following **one-linkage reversible network**, with all six rates equal to one\:

\[
\boxed{
A\rightleftarrows 2A+B,\qquad
A\rightleftarrows 3A+3B,\qquad
A\rightleftarrows 4A+4B.
}
\tag{3}
\]

Its stoichiometric rank is two, since \((1,1)\) and \((2,3)\) are linearly independent.

All states \(x_n=(n,0)\), \(n\geq1\), belong to the same reachable class. Indeed, three successive firings of \(A\to2A+B\), followed by \(3A+3B\to A\), give

\[
(n,0)\to(n+3,3)\to(n+1,0).
\]

Each individual reaction is reversible, so the sequence can also be reversed.

The network is genuinely positive recurrent. Because all forward and reverse constants are one, the product-Poisson weights

\[
\pi_\Gamma(a,b)=\frac{1}{Z_\Gamma a!\,b!},
\qquad (a,b)\in\Gamma,
\]

satisfy detailed balance. They are summable and have finite expected reaction intensity, establishing a nonexplosive positive recurrent chain.

Now consider the max-envelope potential \(V\) from Section 1.

At \(x_n=(n,0)\), only the complex \(A\) is enabled. Consequently,

\[
V(x_n)=\log((n-1)!).
\]

Each of the three possible first jumps fires \(A\to y\), where

\[
y\in\{2A+B,\ 3A+3B,\ 4A+4B\}.
\]

For all sufficiently large \(n\), the target complex \(y\) is the unique maximal falling-factorial source at

\[
x_n-A+y.
\]

Thus the first jump leaves \(V\) unchanged. At this new state, the reaction \(y\to A\) has propensity of order \(n^{y_A}\), while the aggregate propensity of every other enabled reaction is at most order \(n^{y_A-1}\)\. Hence the conditional probability of immediately returning to \(x_n\) is

\[
1-O(n^{-1}).
\]

Inductively, for every fixed integer \(k\), the probability that the first \(k\) jumps stay within these two-step excursions tends to one at rate \(1-O_k(n^{-1})\)\. On those excursions, \(V\) is constant. On the exceptional trajectories, the change in \(V\) is at most \(O_k(\log n)\), since each jump changes the population by a bounded vector.

Therefore,

\[
\boxed{
\lim_{n\to\infty}
\mathbb E_{x_n}\!\left[V(X_k)-V(x_n)\right]=0
\quad\text{for every fixed }k.
}
\tag{4}
\]

Here \(X_k\) is the embedded chain after exactly \(k\) jumps.

Equation (4) proves that no fixed \(k\) can give a uniform strict negative drift for this particular global potential outside finite sets, even in a detailed-balanced, positive recurrent network.

It does not rule out a different Lyapunov function, an adaptive stopping time, or a continuous-time argument. It shows specifically why the bounded positive-increment estimate (2) cannot simply be combined with a finite fixed-step argument to obtain the full theorem.

## 3\. A second attempted route: complex-graph entropy

Weak reversibility provides a positive invariant vector \(a=(a_y)_{y\in\mathcal C}\) for the finite reaction graph, satisfying

\[
\sum_{r:y'_r=y}\kappa_r a_{y_r}
=
a_y\sum_{r:y_r=y}\kappa_r.
\]

This is available for arbitrary molecularity and multiple linkage classes. It suggests using finite-state entropy dissipation to control the population process.

Let

\[
\nu(x)=\frac{e^{-d}}{\prod_i x_i!},
\qquad f(x)=\frac{p(x)}{\nu(x)}.
\]

For a finitely supported probability distribution \(p\), the formal entropy derivative under the master equation can be written exactly as

\[
\frac{d}{dt}H(p\mid\nu)
=
e^{-d}\sum_{\rho\geq0}\frac1{\rho!}
\sum_{r}
\kappa_r f(\rho+y_r)
\log\frac{f(\rho+y'_r)}{f(\rho+y_r)}.
\tag{5}
\]

Set \(h_\rho(y)=f(\rho+y)/a_y\)\. The inner sum becomes

\[
\begin{aligned}
&\sum_r\kappa_r a_{y_r}h_\rho(y_r)
\log\frac{h_\rho(y'_r)}{h_\rho(y_r)}\\
&\qquad+
\sum_r\kappa_r f(\rho+y_r)
\log\frac{a_{y'_r}}{a_{y_r}}.
\end{aligned}
\tag{6}
\]

The first term is nonpositive. This follows from \(\log u\leq u-1\) and stationarity of \(a\) on the complex graph.

**The obstruction is the second term.** It has no prescribed sign. When the complex stationary weights are compatible with a common chemical potential, \(a_y\propto c^y\) within each linkage class, it can be absorbed into the usual complex-balanced entropy calculation. Weak reversibility by itself does not guarantee that compatibility.

Thus finite complex-graph entropy dissipation is not sufficient to establish global stochastic recurrence. An additional estimate would have to control the uncompensated term in (6), particularly along unbounded boundary excursions.

## 4\. Exact point at which the unrestricted proof remains missing

The attempted methods leave three properties unestablished\:

1. **Boundary control\:** a drift estimate valid when arbitrarily many high-order restoring reactions are disabled, including multiscale boundary configurations.
2. **Linkage-class composition\:** a quantitative argument that handles competing reactions from distinct linkage classes without assuming a common complex-balanced measure.
3. **Physical return times\:** an integrable stopping-time estimate strong enough to give finite mean return in the original continuous-time process, rather than only favorable drift along selected paths or in restricted regions.

A potential way to close the argument would be to construct a proper class-wise energy \(W\), a finite exceptional set \(K\), and suitable stopping times \(\tau_x\) such that

\[
\mathbb E_x[W(X_{\tau_x})-W(x)]
\leq-\beta\,\mathbb E_x[\tau_x],
\qquad x\notin K,
\]

with the integrability, localization and nonexplosion hypotheses needed for a valid stopped-process Foster–Lyapunov theorem. The planar work of Agazzi–Laurence supplies such machinery only under its stated hypotheses; the required unrestricted construction has not been obtained here. citeturn466534view7

The ConStRAINeD group's full two-species proof is still listed as *in preparation* on its publications page, rather than as an available unrestricted theorem. citeturn934017view1

## Final result

The renewed investigation produced two rigorous mathematical observations\:

- An arbitrary-molecularity, arbitrary-linkage **max-envelope factorial identity**, with a uniform bound on positive increments per embedded jump.
- An explicit, irreducible, rank-two, reversible network proving that this potential cannot yield a uniform negative drift over any fixed number of embedded jumps, despite genuine positive recurrence.

Neither observation is a recurrence counterexample, and neither proves the missing stochastic return-time estimates.

**The full question remains unresolved.** I cannot justify a universal proof of nonexplosion and finite mean return under weak reversibility alone, nor exhibit a valid same-model counterexample. The exact distinction between the proved identities and the missing structural theorem is essential; the latter has not been established.

## Visible activity — Worked for 23m 26s

Planned the investigation and explored possible counterexamples
I’ll re-read the three scoped predecessors, then examine whether their drift methods can be combined across boundary regimes and linkage classes. I’ll also test explicit high-molecularity networks for transience or explosion. I’ll distinguish a complete proof from any new partial result or counterexample candidate.
Analyzed proof strategies, Lyapunov ideas, and conditional dynamics
Assessed excursion drift and tested ratchet mechanisms
Studied stationary measures and extended recurrence criteria
Searched 20 websites
The literature still leaves the arbitrary-dimensional conjecture open. A possible route is to compare the polynomial rates of growth and restoring reactions along boundary excursions, but pointwise drift cannot capture every such excursion. I’m checking whether an embedded-chain argument can supply a uniform finite-return estimate without assuming complex balance.
Ranked escape paths, evaluated the frontier, and assessed recurrence ideas
Searched 9 websites
Analyzed recurrence mechanisms and explored Lyapunov structure
Evaluated structural recurrence and nonexplosion conditions
Searched 8 websites
Evaluated structural approaches and recurrence mechanisms for robustness
Computed multi-step Lyapunov drift asymptotics
The max-envelope potential yields an exact jump identity and uniformly bounded expected positive increment, but that is still too weak. I found a reversible, product-Poisson example where the expected drift of this potential tends to zero over every fixed number of jumps along an unbounded ray in one class. I’m checking the construction and its reachability proof before using it as a limitation of the method.
Assessed recurrence questions
Verified the fixed-K max-envelope counterexample
Assessed recurrence arguments
Assessed recurrence, proof gaps, and entropy methods
Searched 2 websites

### Analyzed — trace 1

~~~python
import math, collections
C = [(0,0),(0,1),(1,2),(2,3)]
rates=[(a,b,1) for a,b in [(C[0],C[1]),(C[1],C[0]),(C[0],C[2]),(C[2],C[0]),(C[0],C[3]),(C[3],C[0])]]
def ff(x,y):
    res=1
    for a,b in zip(x,y):
        if a<b: return 0
        for j in range(b):
            res*=a-j
    return res
def V(x):
    enabled=[y for y in C if ff(x,y)>0]
    return math.lgamma(x[0]+1)+math.lgamma(x[1]+1)-math.log(max(ff(x,y) for y in enabled))
def trans(x):
    z=[]
    for s,t,k in rates:
        a=ff(x,s)
        if a:
            z.append(((x[0]+t[0]-s[0],x[1]+t[1]-s[1]),k*a))
    zsum=sum(q for _,q in z)
    return [(y,q/zsum) for y,q in z]
for n in [4,10,30,100,1000]:
    distr={(n,0):1.}
    print("n",n,"V0",V((n,0)))
    for k in range(1,7):
        nd=collections.defaultdict(float)
        for x,prob in distr.items():
            for y,p in trans(x):
                nd[y]+=prob*p
        distr=nd
        drift=sum(prob*(V(x)-V((n,0))) for x,prob in distr.items())
        print(k, round(drift,6), len(distr), end=' | ')
    print()
~~~

STDOUT/STDERR
~~~
n 4 V0 3.178053830347945
1 0.0 3 | 2 -0.033656 8 | 3 -0.112724 15 | 4 -0.215142 24 | 5 -0.277578 34 | 6 -0.383562 47 | 
n 10 V0 15.104412573075514
1 0.0 3 | 2 -0.242176 8 | 3 -0.306068 15 | 4 -0.590534 24 | 5 -0.683145 34 | 6 -0.935197 47 | 
n 30 V0 74.65823634883017
1 -0.0 3 | 2 -0.492097 8 | 3 -0.528513 15 | 4 -1.040613 24 | 5 -1.154845 34 | 6 -1.589187 47 | 
n 100 V0 363.73937555556347
1 0.0 3 | 2 -0.736291 8 | 3 -0.751946 15 | 4 -1.496166 24 | 5 -1.633222 34 | 6 -2.256457 47 | 
n 1000 V0 5912.128178488163
1 0.0 3 | 2 -1.146582 8 | 3 -1.148962 15 | 4 -2.296705 24 | 5 -2.490028 34 | 6 -3.446928 47 | 
~~~

### Analyzed — trace 2

~~~python
for n in [30,100,1000]:
 print("n",n)
 for b in range(7):
    x=(n,b)
    v=V(x)
    d={x:1.}
    vals=[]
    for k in range(1,5):
        nd=collections.defaultdict(float)
        for s,ps in d.items():
            for t,pt in trans(s):
                nd[t]+=ps*pt
        d=nd
        vals.append(sum(q*(V(s)-v) for s,q in d.items()))
    print(f"b={b}", " ".join(f"{v:.3g}" for v in vals))
~~~

STDOUT/STDERR
~~~
n 30
b=0 -9.47e-15 -0.492 -0.529 -1.04
b=1 -1.7 -1.64 -2.23 -2.46
b=2 0.116 0.00233 -0.468 -0.528
b=3 0.116 0.058 -0.401 -0.457
b=4 0.000744 -1.64 -1.58 -2.15
b=5 -4.02 -3.9 -4.02 -4.48
b=6 -8.39 -8.27 -8.34 -8.78
n 100
b=0 0 -0.736 -0.752 -1.5
b=1 -2.3 -2.28 -3.05 -3.42
b=2 0.0484 0.000276 -0.727 -0.754
b=3 0.0464 0.0232 -0.702 -0.725
b=4 8.15e-05 -2.28 -2.26 -3.03
b=5 -5.28 -5.23 -5.28 -6
b=6 -10.9 -10.9 -10.9 -11.6
n 1000
b=0 3.03e-13 -1.15 -1.15 -2.3
b=1 -3.45 -3.45 -4.6 -5.18
b=2 0.00724 3.95e-06 -1.15 -1.15
b=3 0.00691 0.00346 -1.14 -1.15
b=4 1.1e-06 -3.45 -3.45 -4.6
b=5 -7.6 -7.59 -7.6 -8.74
b=6 -15.6 -15.6 -15.6 -16.7
~~~

### Analyzed — trace 3

~~~python
C2=[(1,0),(2,1),(3,3),(4,4)]
rates2=[(C2[0],z,1) for z in C2[1:]]+[(z,C2[0],1) for z in C2[1:]]
def V2(x):
    e=[z for z in C2 if ff(x,z)]
    return math.lgamma(x[0]+1)+math.lgamma(x[1]+1)-math.log(max(ff(x,z) for z in e))
def trans2(x):
    z=[]
    for s,t,k in rates2:
        v=ff(x,s)
        if v:
            z.append(((x[0]+t[0]-s[0],x[1]+t[1]-s[1]),k*v))
    tot=sum(w for _,w in z)
    return [(y,w/tot) for y,w in z]
for n in [10,30,100,1000]:
    distr={(n,0):1.}
    vals=[]
    for k in range(1,7):
        nd=collections.defaultdict(float)
        for x,p in distr.items():
            for y,q in trans2(x): nd[y]+=p*q
        distr=nd
        vals.append(sum(p*(V2(x)-V2((n,0))) for x,p in distr.items()))
    print(n, vals)
~~~

STDOUT/STDERR
~~~
10 [1.1842378929335002e-15, 0.12280832248925505, -0.004572273308811105, 0.10398889168574277, -0.023503633558956016, 0.07142959941608182]
30 [-9.473903143468002e-15, 0.06946965686032824, -0.012171090115084281, 0.05462253049140473, -0.027463152220653028, 0.03620054769466994]
100 [-1.8947806286936004e-14, 0.029896627705040316, -0.006793727124146652, 0.022762158936083098, -0.014013804218560704, 0.01510762018582466]
1000 [3.0316490059097606e-13, 0.0045926841061066735, -0.0011377666200738056, 0.0034497690218940813, -0.002282190212726482, 0.00229847831867146]
~~~
