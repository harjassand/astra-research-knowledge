# A common raw factorial envelope: earned transport and a decisive failure

Same principal, new ordinary argument. This is not a recurrence theorem. The raw source identities derive from the established log-factorial/source-probability mechanism; choosing one maximum across available sources is the representation tested here.

Let C be the raw source set of a finite weakly reversible network, with genuine channels r:y_r->y'_r, constants kappa_r>0 and standard falling-factorial propensities. Weak reversibility ensures every product is also a source. Put

    a_y(x)=(x)_y, a_*(x)=max_(y in C) a_y(x),
    B(x)=x!/a_*(x)=min_(y<=x,y in C) (x−y)!,
    V_alpha(x)=B(x)^alpha,  0<alpha<1.

Work on an active irreducible class. Then q>=kappa_min, since an enabled integer source has a_y>=1. V_alpha is normlike: a_* is at most a fixed polynomial in total count, while x! grows factorially in at least one coordinate.

For an actual reaction from y, write z=x−y and x'=z+y'. The source y' is enabled at x', so B(x')<=z!. Therefore

    V_alpha(x')/V_alpha(x) <=[a_*(x)/a_y(x)]^alpha.             (B1)

In particular an actual maximizing source cannot increase this value, including a move between different activation layers. Let K=sum_r kappa_r. Weighted Holder gives the uniform full-output bound

    P V_alpha/V_alpha
      <=a_*^alpha/q sum_r kappa_r a_y^(1−alpha)
      <=(K a_*/q)^alpha <=(K/kappa_min)^alpha=:C_alpha.       (B2)

This includes EVERY competing channel. It requires neither an ordered source chain nor a scalar reaction anchor. Iteration pays every fixed-horizon actual output. For 0<=beta<alpha and an episode of at most h actual jumps, conditional integration of the actual holding clock gives

    E integral (1+q)V_beta dt
      <=(1+1/kappa_min)V_beta(x) sum_(j=0)^(h−1) C_beta^j.    (B3)

Thus this is a genuine common finite-path transport/physical reward envelope. It does not earn a return, a negative drift or a global receiver.

## The fully informed conservative comparator defeats universality

Use the already documented conservative-linkage example underlying N1394's distinct adjoint failure:

    2A --100--> A+B --1-->2A,
    0 <-> A, 0 <-> B, all four port constants1.

At x=(n/2,n), a_*=(x)_AB for all large even n. For alpha=1/2, the full embedded one-step V_alpha ratio tends to

    R=[25 sqrt(2)+(1/2)/sqrt(2)]/(25+1/2)>1.

The low-order ports vanish from the embedded law on every fixed finite path, and all finitely many bounded offsets have the same limiting fast probabilities. For every fixed horizon h, V_alpha is therefore a strict submartingale throughout that finite reachable patch once n is large. No adaptive stopping rule bounded by h and requiring at least one jump has negative expected V_alpha drift. Equivalently its optimal finite-horizon stop chooses to stop immediately after the forced first step in the limiting problem, leaving defect R−1>0.

The ordinary exact solution is much stronger. For N=A+B the fast linkage preserves N and LN=2−N. For W=t^N,

    LW/W=2(t−1)+(t^−1−1)N,

which proves recurrence and pays every smaller exponential physical activity reward, since q is quadratic. The failure is in the unweighted factorial representation, not the network. N1394 already warned that a closed conservative fast linkage defeats an unweighted factorial adjoint; the backward adaptive-horizon calculation here preserves that warning rather than announcing a general new receiver.

On the banked ordered family, high-precision finite probes also distinguish fixed-horizon observation from delayed repayment: ordinary h-step output can remain positive on the A-axis, while an actual adaptive stopping calculation first finds negative paid output after the borrowed inventory has had time to return. These are finite diagnostics only, not a classwide certificate. They do not erase the conservative counterexample.
