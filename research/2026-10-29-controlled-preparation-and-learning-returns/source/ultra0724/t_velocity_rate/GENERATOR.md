# Conserved-currency nonlinear Markov receiver

29 October 2026. Ideal real-valued/random-source mathematics, not a finite-bit
output or physical gas qualification. This file derives the model transformation;
termination and costs are in PROOF.md. Historical priority is UNKNOWN.

## 1. Actual hard-sphere convention

For probability measures f_t on R^3, use the homogeneous weak equation

    d <phi,f>/dt = int f(dv) f(dw) |v-w| E_sigma[phi(p)-phi(v)],
    p=(v+w+|v-w|sigma)/2, q=(v+w-|v-w|sigma)/2,

where sigma is uniform on the unit sphere. Thus the angular measure has total
mass one. There is no additional 4pi, half-rate, Maxwell approximation, Gaussian
blur commutation or finite-population approximation in this convention.
Exchange v,w and sigma -> -sigma gives the equivalent pair-symmetric expression
one half times [phi(p)+phi(q)-phi(v)-phi(w)].

Fix a>0, e0=int |v|^2 f0(dv), c=a+e0, h(v)=a+|v|^2. Elasticity gives

    h(p)+h(q)=h(v)+h(w).

Suppose provisionally g_t(dv)=h(v)f_t(dv)/c. It is a probability law.

## 2. A normalized positive update

For current v, propose events at rate

    Lambda(v)=(c/a)(|v|+sqrt(a)).

At an event at time s, obtain an independent w with law g_s and accept with

    Q(v,w)=c |v-w|/[h(w)Lambda(v)]
          =a |v-w|/[(a+|w|^2)(|v|+sqrt(a))].

This is in [0,1]: if x=|v|/sqrt(a),y=|w|/sqrt(a), triangle inequality reduces
the claim to x+y <= (1+y^2)(x+1), whose excess is
x y^2+(y-1/2)^2+3/4. A rejection keeps v.
On acceptance draw sigma, form p,q, and retain p with probability
h(p)/[h(p)+h(q)], otherwise retain q. No signed or multiplicative output mass
is introduced. This extra outgoing selection is essential; simply deleting
the mass variable in Fournier's ordinary recursion is incorrect.

For a test psi the normalized nonlinear generator is

    G_g(psi)=int g(dv)g(dw) c |v-w|/h(w)
       { [h(p)psi(p)+h(q)psi(q)]/[h(v)+h(w)] - psi(v) }.

Exchange the two iid inputs. The gain coefficient becomes

    (c |v-w|/2)(1/h(v)+1/h(w))/(h(v)+h(w))
      =c |v-w|/[2h(v)h(w)].

The loss symmetrizes with exactly the same coefficient. Therefore

    G_g(psi)=int g(dv)g(dw) c |v-w|/[2h(v)h(w)]
       [h(p)psi(p)+h(q)psi(q)-h(v)psi(v)-h(w)psi(w)].       (G)

Substituting g=hf/c shows G_g(psi)=(1/c) d<h psi,f>/dt.
This proves the generator identity without assuming a g sampler exists.
The recursive construction in PROOF.md supplies that missing existence.

## 3. Reverse identification without an unknown normalization

Conversely let a probability-valued g_t solve this nonlinear jump equation
with sufficient finite event intensity, starting from g0=hf0/c. In (G), the
bounded tests psi=1/h and psi=v_j/h give zero, by conservation of particle
number and momentum. Hence f_t=c g_t/h has total mass one and the same
momentum as f0. Since g_t is probability-valued,

    int |v|^2 f_t = c int g_t - a int f_t = c-a=e0.

For any bounded continuous phi, use psi=phi/h in (G); it gives the actual
conservative hard-sphere equation for f_t. Standard uniqueness of the
conservative homogeneous hard-sphere solution then identifies this law.
All terms are integrable: f has finite energy, and int ff |v-w| is finite.

## 4. Normalized output instead of a random mass

Independently repeat a complete g_t draw and accept its returned v with
probability a/h(v). Its mean success probability is

    int g_t(dv) a/h(v)=a/c,

and the accepted law is f_t. Expected complete g proposals are c/a. If e0>0,
choosing a=e0 makes this exactly two. This is a rejection operation on an
already normalized law; it is not self-normalized importance sampling.

For source f0 supported in a warranted radius R, g0 can be sampled by drawing
f0 and accepting h(v)/(a+R^2), with mean c/(a+R^2). For an explicitly supplied
finite source table, reweighting that table by h/c is another acquired input
operation. An arbitrary unknown source does not grant g0 for free.

## 5. Closest ordinary constructions

Fournier's 2019 hard-potential recursion (arXiv:1703.10874v1, Sections 2--3)
already acquires an exact weighted output (M,V), with E[M 1_(V in A)]=f_t(A),
and proves termination with a stopped recursive counter. That work is the
source of the generic recursion/stopping method used here. Its multiplicative
M update, and the source's expressly unresolved second moment of M, differ
from the normalized positive update above. Generic recursive hard-rate
simulation is therefore established prior.

Energy packets/energy-weighted BTE simulation are also established, e.g.
Peraud--Hadjiconstantinou 2011, arXiv:1109.3910v1 Section 2.2, for phonon
relaxation-time transport. That operation does not itself prove this nonlinear
elastic-gas lineage or its iid f_t rejection law. A priority claim would need
a broader historical assessment; none is made here.
