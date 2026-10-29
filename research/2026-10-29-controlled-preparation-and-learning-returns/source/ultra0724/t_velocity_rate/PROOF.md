# Normalized hard-sphere sampling by conserved-currency recursion

29 October 2026. This is an ideal-real/random-source operation for the explicitly
normalized homogeneous three-dimensional hard-sphere equation in GENERATOR.md.
It does not assert a finite-bit continuous output, uniform-in-time work, empirical
gas identification, historical novelty or practical superiority to DSMC.

## 1. Input and theorem

Input is a probability source f0 on R^3 with warranted support |v|<=R, exact known
energy e0=int |v|^2 f0(dv), and an independent source sampler. Fix a>0 and put
h(v)=a+|v|^2, c=a+e0, Lambda(v)=c(|v|+sqrt(a))/a. Source g0=hf0/c must be
sampleable: rejection with envelope a+R^2 supplies it, or an explicit finite
source table can be reweighted. The zero-energy point source may simply be
returned unchanged; no division by e0 is needed if a is otherwise chosen.

For every finite time t>=0, the recursive algorithm below terminates almost
surely, has finite expected total calls and returns a g_t-distributed velocity.
The subsequent a/h rejection returns iid velocities with law f_t, the unique
conservative solution of the actual hard-sphere equation. There is no population
limit, time mesh, weighted output, velocity cutoff or unknown partner-law oracle.
The theorem remains conditional on ideal arithmetic and the stated source.

## 2. Algorithm, including all dummy events

`currency(t)`:

1. Draw v from g0 and set s=0.
2. Draw E of unit exponential law; set s <- s+E/Lambda(v).
3. If s>t, return v. Otherwise call `currency(s)` independently to obtain w.
4. Accept with Q(v,w)=c|v-w|/[h(w)Lambda(v)]. If rejected, keep v. If accepted,
   draw a uniform unit vector sigma, compute elastic p,q, and replace v by p
   with probability h(p)/(h(p)+h(q)), otherwise by q.
5. Return to step 2.

`physical(t)`: independently repeat `currency(t)` and retain the result with
probability a/h(v). The generator identity and physical-law rejection are in
GENERATOR.md. Crucially even rejected collision proposals require the partner
call; its entire cost is counted.

## 3. Pointwise clock drift

The proposal Q is in [0,1]. Either outgoing speed is at most |v|+|w|, so for
the update Vnew (including its rejection and outgoing random choices),

    E_mark[Lambda(Vnew)-Lambda(v)]
       <= (c/a) Q(v,w)|w| <= c/sqrt(a) = K.                 (1)

For the last inequality put x=|v|/sqrt(a), y=|w|/sqrt(a). Triangle inequality
gives Q|w|/sqrt(a)<=y(x+y)/[(1+y^2)(1+x)]<=1 because
(1+y^2)(1+x)-y(x+y)=1+x(1+y^2-y)>0. This uniform pairwise bound needs no
moment of the recursively requested partner and is stronger than assuming
the as-yet unconstructed law g_s exists.

## 4. Nonexplosion and expected full tree size

We adapt the established stopped-counter construction of Fournier (2019),
arXiv:1703.10874v1 Section 3, with a different positive update. These details
are included to avoid treating the partner law as an oracle.

Let N_t be the total number of partner calls in the recursive tree, including
all descendants. A local event adds N_s^*+1, where the starred counter belongs
to the independent requested subtree. An infinite computation is assigned a
cemetery state and counter infinity. The minimal process obtained from the
recursive random tree has a time-inhomogeneous jump generator on (v,n):

    L_s Psi(v,n)=Lambda(v) E_{(w,n*)~G_s,mark}
                    [Psi(Vnew,n+n*+1)-Psi(v,n)],

where G_s is the law of the same minimal recursive output at time s, including
its possible cemetery mass. This equality follows by exposing only the draws
required up to time s. Equivalently finite tree truncations construct the
minimal process before the first unresolved descendant. No external G_s
sampler is part of the executable algorithm.

Stop at zeta_A=inf{s:N_s>=A}; the finite-counter process does not explode before
this time. In fact a finite tree with n events has n+1 source leaves and its
returned squared speed is at most (n+1)R^2, because either outgoing squared
speed is at most |v|^2+|w|^2. Thus all pre-stopping speeds/rates are explicitly
bounded by R sqrt(A) and c(R sqrt(A)+sqrt(a))/a. Define Z_A(t)=E[N_t wedge A] and
F_A(t)=E[Lambda(V_t) 1_(N_t<A)], taking the latter as zero at the cemetery.
Dynkin's identity on these stopped bounded-rate states and

    ((n+n*+1) wedge A)-(n wedge A) <= 1+(n* wedge A)

give

    Z_A(t) <= int_0^t F_A(s)[1+Z_A(s)] ds,
    Z_A(t) <= exp(int_0^t F_A(s)ds)-1.                     (2)

For Psi(v,n)=Lambda(v)1_(n<A), discard the nonpositive contribution from
transitions leaving the allowed counter range. Apply (1) on finite partner
states; a cemetery partner kills Psi and contributes nonpositively. Thus

    F_A(t) <= A0+K int_0^t F_A(s)ds <= A0 exp(Kt),
    A0=E_g0 Lambda(V0) <= (c/a)(R+sqrt(a)).                (3)

The finite-source tree speed bound makes further state localization unnecessary.
Combining (2)--(3), uniformly in A,

    E[N_t wedge A] <= exp[(A0/K)(exp(Kt)-1)]-1.

Monotone convergence shows N_t<infinity almost surely and proves

    E N_t <= exp[(A0/K)(exp(Kt)-1)]-1.                    (4)

Consequently no cemetery mass remains, the minimal recursive output is a
probability law g_t, and bounded-test Dynkin identities give its nonlinear
jump equation. This is the same generic termination device as the ordinary
Fournier algorithm, paid with the new update's explicit clock drift (1).

## 5. Identification and output cost

The finite intensity from (3) makes GENERATOR.md Section 3 applicable. In
particular tests 1/h and v_j/h conserve f_t=cg_t/h mass and momentum, and g_t
mass fixes f_t energy e0. Testing phi/h gives the conservative hard-sphere
weak equation. Standard uniqueness (as recalled in Fournier's Sections 1--2,
with the initial bounded source more than sufficient) identifies f_t.

Each g attempt uses N_t+1 initial draws, N_t event/partner proposals, and
exactly 2N_t+1 exponential draws: every node has its final overshoot draw,
in addition to its event draws. There are N_t accept/reject uniforms, at
most N_t spherical draws and at most N_t outgoing-choice uniforms. An
iterative stack implementation uses at most N_t+1 simultaneous frames.
Each g0 draw by source rejection uses mean (a+R^2)/c raw f0 draws.

The final physical rejection has success probability a/c. Independence of
successive complete attempts gives expected total cost c/a times the mean
cost of one g attempt, even though an attempt's cost can correlate with its
own output/success. No unjustified independence within an attempt is used.

Bounded tests of iid physical outputs admit ordinary Hoeffding sampling
guarantees, since their output weight is one. This does not make the random
computational cost bounded or prove an efficient high-confidence runtime.

## 6. A uniform fourth-moment bound for a sharper time-cost qualifier

This section is a model-side cost improvement after existence/identification;
it is not needed to close the stopping argument. Let mp=int |v|^p f_t(dv),
with e=m2=e0>0. For x=|v|^2,y=|w|^2, elastic sphere averaging gives

    E_sigma(|p|^4+|q|^4)
      =(x+y)^2/2+|v-w|^2|v+w|^2/6 <= (2/3)(x+y)^2.

Writing r=|v-w|, the weak equation implies

    m4' <= int ff r[-(x^2+y^2)/6+(2/3)xy]
         <= -m5/3 + m4*m1/3 +(4/3)m3*e.

The negative term uses r>=|v|-|w| (with its sign retained); the positive
term uses r<=|v|+|w|. Now m1<=sqrt(e), m3<=sqrt(e*m4), and
m5>=m4^(3/2)/sqrt(e), by Cauchy/Hölder. Therefore, for X=m4/e^2,

    m4' <= e^(5/2)[-X^(3/2)+X+4sqrt(X)]/3.

It follows that, with B=max{m4(0)/e^2, ((1+sqrt(17))/2)^2},

    sup_t m4(t) <= B e^2.                                (5)

Truncated polynomial tests/standard hard-sphere moment propagation justify
these differential inequalities from bounded f0; no closed finite moment
hierarchy is assumed. For a=e,c=2e, (5) gives

    E_g |V|^2=(e^2+m4)/(2e) <= (1+B)e/2,
    E_g Lambda(V) <= 2sqrt(e)[1+sqrt((1+B)/2)] = L.

Use the actual finite g intensity in (2), then remove A, to obtain the
sharper bound E N_t<=exp(Lt)-1. The physical rejection still costs a factor
two. This remains exponential in time, and no advantage over an equally
informed finite-population or deterministic hard-sphere solver follows.

## 7. Scope and strongest ordinary comparison

The constructed interface is an iid normalized hard-sphere law at any finite
time under ideal arithmetic and a qualified initial source, in place of an
unbounded random output mass. The collision rate and nonlinear loss are
handled explicitly; no Maxwell/angular-moment closure is imported.
Fournier's exact weighted recursion is the nearest exact ordinary comparator.
Continuous-time finite-population Kac/DSMC with correct actual pair rates is
the serious practical comparator; its population error must remain visible.
The present exponential-time tree bound is not a computational breakthrough
for late kinetic times. Finite-bit output and physical model acquisition are
separate questions, not silently paid by termination.
