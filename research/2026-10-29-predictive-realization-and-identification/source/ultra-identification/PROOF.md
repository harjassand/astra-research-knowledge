# Baseline mark-time data do not generally identify intervention response

The root three-state construction is correct, including the stronger pair
u=1 versus u=2 with the SAME positive background transition support, known
microscopic reset and known hidden mark-rate function. Below I independently
derive it, extend the structural scope, and distinguish genuinely additional
records from more statistics of the same visible path. No dynamics were run.

This is an elementary nonminimal phase-type / unexcited-subspace ambiguity.
It is not a countermodel of the pinned RuO2 graph/catalog, a sharp interval
theorem, an impossibility for every minimal hidden realization, or a physical
information barrier. No historical novelty is asserted.

## 1. Root construction: exact same-reset, same-function ambiguity

There are three hidden states0,1,2. The background generator and known
controlled killing matrix are

\[
Q_u=\begin{pmatrix}-2&2&0\\u/2&-u&u/2\\0&0&0\end{pmatrix},
\qquad D=\operatorname{diag}(0,1,2),\qquad p=(0,1,0).
\]

The controlled mark sends every state to the SAME new visible absorbing
state. State2 being absorbing for the BACKGROUND is not an additional visible
output: until the controlled mark the visible signal is constant. The mark
occurs with intensity bD(X_t), while Q and p remain unchanged. Observe only
the mark time tau or its censoring at a prescribed horizon, then the constant
absorbing output. In particular, background jump times are NOT observed.

With row-vector initial convention, let

\[
S_u(t,b)=p e^{(Q_u-bD)t}\mathbf1,
\quad L_u(z,b)=\int_0^\infty e^{-zt}S_u(t,b)dt
             =p(zI-Q_u+bD)^{-1}\mathbf1.
\]

Direct elimination, independently reproduced in derive.py, gives

\[
L_u(z,b)-\frac1{z+b}
=\frac{bu(b-1)}{(z+b)(z+2b)
 [z^2+(2+u+b)z+u+2b]}.                                      \tag{1}
\]

At baseline b=1, the full visible law is Exp(1) for EVERY u>=0, at every
horizon. Thus arbitrarily many exact baseline paths, not merely means or
one histogram, fail to distinguish these backgrounds. For distinct positive
u,v and 0<b<1, (1) differs: writing
\(A=(z+2)(z+b)>0\), the u-dependent factor is
\(u/[A+u(z+1)]\), strictly increasing in u for z>0. Hence target laws differ
even when background support is fixed and positive on exactly the same edges.
u=0 is useful only as a simple comparison to exp(-bt); it is not the
same-positive-support pair.

An independent local calculation is

\[
S_u'(0,b)=-b,\quad S_u''(0,b)=b^2,\quad
S_u'''(0,b)=-b^3+ub(b-1).                                   \tag{2}
\]

For u!=v and b!=1 these analytic survival functions differ on every
nonzero time interval. Therefore every positive censoring horizon admits a
target visible-path distinction, although this alone is not a claim that
their endpoint event probabilities differ at EVERY particular time.

## 2. Irreducible reversible extension, all known resets

For c>=0 replace the background by

\[
Q_{u,c}=\begin{pmatrix}-(c+2)&c+2&0\\u/2&-u&u/2\\0&c&-c\end{pmatrix}.
                                                                    \tag{3}
\]

For c>0 and u>0 this is an irreducible birth-death chain on the SAME fixed
three-state path. It is reversible with weights proportional to

\[
\pi_{u,c}=\left(\frac{u}{2(c+2)},1,\frac{u}{2c}\right):
\quad \pi_0 Q_{01}=\pi_1 Q_{10},\quad
\pi_1 Q_{12}=\pi_2 Q_{21}.                                  \tag{4}
\]

No equilibrium preparation is assumed: the prescribed reset remains the
same known pure state p. The stationary weights in (4) vary with u and are
NOT an additional supplied measurement.

Set w=(-1,0,1)^T and A=Q_{u,c}-D. Exactly,

\[
A\mathbf1=-\mathbf1-w,\qquad Aw=-(c+2)w.                    \tag{5}
\]

The two-dimensional span V=span{1,w} is invariant and both actions are
independent of u. Solving the two scalar equations in (5) yields the ENTIRE
survival vector

\[
e^{At}\mathbf1=e^{-t}\mathbf1
 -\frac{e^{-t}-e^{-(c+2)t}}{c+1}\,w.                        \tag{6}
\]

It is independent of u. Thus the baseline mark-time law is the same for
each corresponding known reset distribution p, including EVERY pure hidden
state, not just the central reset. Different reset choices need not have
the same law as each other; their respective laws are the same across u.
More baseline preparations therefore do not repair THIS ambiguity.

For target b define

\[
\begin{aligned}
D_0&=(z+b)(z+c+2)(z+c+2b),\\
D_1&=z^2+(c+1+2b)z+b(c+2).
\end{aligned}
\]

For the common central reset, independent symbolic inversion gives

\[
L_{u,c}(z,b)-\frac1{z+b}
 =\frac{ub(b-1)}{(z+b)(D_0+uD_1)},                          \tag{7}
\]

and consequently

\[
L_{u,c}-L_{v,c}
=\frac{b(b-1)(u-v)(z+c+2)(z+c+2b)}
 {(D_0+uD_1)(D_0+vD_1)}\ne0                               \tag{8}
\]

for z>0, b>0 with b!=1 and distinct positive u,v. All denominators are
positive. The same third-derivative difference in (2) holds for every c.

Zero mark intensity is also inessential. For ANY known rho>0, take
D_rho=D+rho I, whose three diagonal entries are strictly positive. Then

\[
S^{rho}_{u,c}(t,b)=e^{-b\rho t}S_{u,c}(t,b),\qquad
L^{rho}_{u,c}(z,b)=L_{u,c}(z+b\rho,b).                       \tag{9}
\]

Equation(6) still gives identical baseline laws for every corresponding
known reset, and (8) still separates target laws. Thus the ambiguity is
compatible with irreducibility, reversibility, fixed positive background
support and a uniformly positive, exactly known mark-rate function.

## 3. An exact bounded query and deterministic finite horizon

The following constants are for the ORIGINAL c=0,rho=0 pair, not a numerical
claim about the stronger extensions. At b=1/2,z=1, (1) gives exactly

\[
L_1=17/26,\qquad L_2=11/17,\qquad L_1-L_2=3/442.             \tag{10}
\]

These are expectations of the bounded visible reward
F=integral_0^tau e^{-t}dt=1-e^{-tau}. Censor at the deterministic horizon6:
F_6=1-e^{-min(tau,6)}. Each omitted expectation tail lies in[0,e^{-6}], so

\[
E_{u=1,b=1/2}F_6-E_{u=2,b=1/2}F_6
 \ge 3/442-e^{-6}>3/442-1/400=379/88400>0.                   \tag{11}
\]

The strict bound e^6>400 is certified by the positive rational Taylor
polynomial through degree17, whose value is1201332481/2977975. This supplies
an exact, bounded, finite-horizon prediction ambiguity, without numerical
matrix exponentials or new stochastic trajectories.

## 4. Which additional waiting/event records help?

Any statistic, independently randomized processing, censoring or repeated
reset experiment that uses only the stated baseline visible records has
the same law under the indistinguishable models. This includes residual
waiting times conditional on survival, mark counts per reset, endpoint
flags and all their joint summaries. The residual mark-time law for the
central reset is exponential, so that extra terminology creates no new
information. Even adaptive choices of known resets/censoring based on past
visible records preserve equivalence in (6), by conditioning episode by
episode. This does not cover observing new physical events within an episode.

Indeed, if an added clock detects ANY background transition, no state label
is required to identify u in this DECLARED one-parameter family. From the
central reset the first event of either kind has rate

    u+1+rho at baseline.

Equivalently, the probability the mark happens before any background jump
is (1+rho)/(u+1+rho). Either exact law identifies u. With a fixed horizon T,
the probability of no event of either kind is exp(-(u+1+rho)T), also injective.
This is a genuinely new event readout, not a statistic of the original mark
time. It is not a universal identification theorem for arbitrary unknown Q.

One additional NONBASELINE setting b_star!=1 also identifies u within the
known family, since (7) is injective in u at every z>0. That is an acquired
intervention experiment, not a free prediction from baseline. No finite-data
cost or physical ability to execute it is supplied by this identifiability
argument, and the statement does not identify arbitrary backgrounds.

## 5. The genuinely sufficient path record: paired integrated intensity

Knowing the state function d(x) is not knowing its realized path integral.
If the per-episode record ALSO acquires

    A_T=integral_0^{tau wedge T} d(X_t)dt,

paired with its mark count N_T and the observed bounded reward, ordinary
Girsanov gives the exact finite-horizon intervention expectation

    E_b F = E_1[F b^{N_T} exp((1-b)A_T)].                    (12)

It requires no background generator. If d<=dmax and0<b<=1, weights are at
most exp((1-b)dmax T), so finite-sample bounded confidence is available under
an actually warranted sampling/measurement contract. Brackets on A_T give
intervals, as in the separately accepted coarse native receiver. The current
mark-only record does not supply that extra observable or its bracket.

Pairing, rather than just another marginal, matters. With rho>0, tau is
almost surely finite and the ordinary integrated-hazard clock gives

    A_tau ~ Exp(1)

for EVERY background in this family. The marginal tau from the central
reset is also independent of u at baseline. Nevertheless their JOINT law
depends on u. Exactly, for s>-1,z>=0,

\[
E_1 e^{-z\tau-sA_\tau}
 =p[zI-Q+(1+s)D_\rho]^{-1}D_\rho\mathbf1
 =\frac{1-zL^{rho}(z,1+s)}{1+s}.                            \tag{13}
\]

At z=0 this is1/(1+s), proving the common Exp(1) activity marginal. At
z>0,s!=0, (8)--(9) show the joint transform differs. Thus even both separate
exact marginal laws do not replace the paired record. No actual integrated
intensity measurement was acquired in this assignment.

This does not make infinite-horizon reweighting economical: its weight
W=b exp((1-b)A_tau) has second moment b²/(2b-1) for b>1/2 and infinite second
moment for0<b<=1/2. Finite censoring controls the range but can still be
costly. Identification and efficient acquisition remain separate questions.

The visible baseline hazard itself equals1+rho at the central reset. It is
therefore known exactly from unlimited mark records. Simply multiplying it
by b is wrong: the target hazard is

    b E_b[d(X_t) | tau>t],

and intervention changes the hidden conditional law. Knowledge of the
baseline visible intensity does not provide the target filtering law.

## 6. A sufficient structural alternative, with its acquisition gate

Ordinary finite-dimensional realization theory explains the failure.
If baseline survival vectors are acquired for ALL known microscopic resets,
one knows f(t)=exp(A_1 t)1 and its derivatives, where A_1=Q-D. Let

    V=span{1,A_1 1,A_1²1,...}.

The baseline determines A_1 restricted to V. If the KNOWN matrix D preserves
V, then A_b=A_1-(b-1)D also preserves V and its restriction is determined.
The target survival vector can then be computed inside V without learning
the rest of Q. If V is the whole hidden state space, the usual full-rank
Krylov matrix recovers A_1 itself. These are sufficient conditions, not
assumptions granted by one fixed-reset scalar survival curve.

Here V=span{1,w}, and D w=w+w² is outside V. Baseline excites only V while
the intervention couples it to the missing direction. This is precisely why
all-reset baseline data are insufficient. It is not a claim that generic
minimal realizations are nonidentifiable, nor that every restricted native
rate library has this ambiguity.

## 7. Prior, cost and decision

Primary context checked: Ryden, *On identifiability and order of continuous-
time aggregated Markov chains, Markov-modulated Poisson processes, and
phase-type distributions*, Journal of Applied Probability1996
([publisher abstract](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/on-identifiability-and-order-of-continuoustime-aggregated-markov-chains-markovmodulated-poisson-processes-and-phasetype-distributions/FE3D6254299BA201DF0943B2817B4A74));
and Lindqvist, *Phase-type models for competing risks, with emphasis on
identifiability issues*, DOI10.1007/s10985-022-09547-7
([full primary article, §2](https://pmc.ncbi.nlm.nih.gov/articles/PMC10006281/)).
Their phase-type nonuniqueness / realization theory is controlling context.
No detailed external theorem is needed as a premise of the elementary proof,
and no priority for this fixed-D example or extension is inferred.

derive.py independently checks the general matrix identities, original
root resolvent, third derivative, distinct-u formula, reversibility,
positive-intensity shift and exact finite-horizon gap. No producer module
was imported. The successful symbolic/rational kernel took0.1861s after
imports. One preliminary check used structural equality of an unexpanded
Sympy matrix expression and failed; replacing it by the mathematically
equivalent simplified difference fixed that executable assertion. It was
additional setup cost, not a failed mathematical identity. No stochastic
model, new trajectory, physical action or parameter grid was run.

Decision: more of the SAME baseline mark-time data cannot universally pay
the intervention interface, even with known reset/function/support and
reversible irreducible backgrounds. A source-specific identifiability
condition, a genuinely richer paired path/event record, or a paid additional
intervention can do so in qualified settings. This does not invalidate the
accepted native interval receiver, which explicitly acquires more coarse
activity information and never claimed point identification or sharpness.
