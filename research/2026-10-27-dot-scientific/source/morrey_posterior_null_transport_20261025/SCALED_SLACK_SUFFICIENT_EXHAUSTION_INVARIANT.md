# A quantitative sufficient invariant for a recurring posterior cycle

**Conditional theorem only.** This note proves what a successful both-branch label policy would imply. It does not prove that such a policy exists for the cosine source. The finite constructions and moment-face obstruction do not establish its preservation.

Let sigma be an actual source posterior, m=E Z, X=Z-m, V=E|X|²>0, C=E XX^T, and require D=E q(Z)-q(m)=0. Let a=C^{-1}E[Xq(X)], e=q(X)-a.X, delta=E e². Define

 gamma=min{|a.v|: |v|=1, q(v)=0}.

The minimum is attained. It is zero when the hyperplane perpendicular to a meets the null cone. The formulas previously used for a timelike a apply only in the timelike/positive-gamma case; no positive-gamma assumption is needed here.

Assume fixed constants c,s>0 give, at every state where a mean step is to be performed,

    C >= c V I,                  delta-gamma² V >= s V².       (I)

The first inequality necessarily has c<=1/3. Choose any minimizing unit null direction v and set

 h=(C^{-1}v).X - (a.v/delta)e.

Regression orthogonality gives E h=0, E[Xh]=v, and E[q(X)h]=0 EXACTLY. Therefore posterior multipliers1±epsilon h give means m±epsilon v and retain D0.

## Uniform positive step and explicit variance payment

The source lies in[-1,1]^3, so |X|<4 and V<=3. Since the operator norm of J is1,

 E q(X)² <=16V,  |a|²<=16/c,  |e|<=16(1+1/sqrt(c)).

From (I), delta>=gamma²V+sV². The arithmetic-geometric mean inequality gives

 gamma/delta <=1/(2sqrt(s)V^(3/2)).

Also |(C^{-1}v).X|<=4/(cV)<=8/(cV^(3/2)). Consequently, with

 K=8/c+8(1+1/sqrt(c))/sqrt(s),

we have ||h||_infinity<=K/V^(3/2). Choose

 epsilon=V^(3/2)/(2K).

Both posterior density factors then lie in[1/2,3/2]. The actual mean split is null, its child means are in E because they are actual barycenters, and its acquired mean variance is exactly

    epsilon²=V³/(4K²).                                       (II)

This pays the whole two-branch source decomposition, not an infinitesimal formal direction.

## What recurrence would imply

Suppose an actual finite-label policy, applied to every descendant as needed, preserves the parent mean and D0, keeps every branch, and brings EVERY nonterminal posterior to (I), with the SAME c,s. Labels may change covariance and higher moments. Labels with unchanged means preserve average conditional variance. At each generation apply the above mean step to every nonterminal label posterior; V=0 states are left fixed.

Writing v_n for the average conditional variance after n generations, Jensen and (II) give

 v_(n+1)<=v_n-v_n³/(4K²).

If v_n becomes zero, exhaustion is already achieved. Otherwise

 1/v_(n+1)² >=1/v_n²+1/(2K²),

and hence

 v_n <=(v_0^{-2}+n/(2K²))^(-1/2).

Every finite actual source-posterior null mean tree can be completed by the accepted exact axis-chord receiver, giving an actual complete paid law nu_n with

 W1(mu,nu_n)<=sqrt(3 v_n)
             <=sqrt3 (v_0^{-2}+n/(2K²))^(-1/4) ->0.

Thus maintaining (I) with a genuine finite both-branch label policy would prove source membership in the closed laminate class, with an explicit rate. It would resolve this candidate's reachability, not the full positive Morrey conjecture.

## Actual remaining interface

No invariant-preserving label policy has been proved. The audited root label and one subsequent null mean step establish finite compatibility, and the exact 11-atom obstruction shows that freezing all quadratic and selected higher moments cannot supply a uniform label rate. The covariance-changing escape demonstrates an available relaxation but does not prove that its descendants remain in (I). A sequence of shrinking density floors, isolated positive slack values, or a favorable branch is not a substitute for fixed c,s on ALL descendants. This is the explicit preservation problem still open.
