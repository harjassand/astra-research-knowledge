# A passive resistor-network realization of the intervention-order obstruction

**Root-origin construction; complementary analytic challenge and exact nodal checks.**
1 November 2026. This note binds the abstract signed-path obstruction to ordinary positive-conductance resistor networks. The response representation and earlier dark-path idea are inherited from Astra at revision `51ce47ce39f976517d60e2f87bbe280b651f6056`; this literal circuit realization and its analysis were developed in the present investigation. It is a theorem about a declared circuit class, not a claim that a laboratory circuit was built or calibrated.

## 1. Physical source, controls and receiver

Fix an integer n>=2, kappa>0 and delta>0. There are two boundary rails held at normalized potentials 0 and 1, and n+1 internal nodes numbered 0,...,n. Put s=2/kappa. At internal node j, install conductance s*a_j to rail 1 and conductance s*(1-a_j) to rail 0. A zero conductance means that branch is absent. All present conductances are positive.

The two sources have baseline internal potential vectors

    a_A=(0,1/2,...,1/2,0),
    a_B=(0,1/2,...,1/2,1).

Thus only the last internal node's anchor changes rails. Both retain total anchor conductance s at every internal node. Actuator i adds conductance u_i>=0 between internal nodes i-1 and i, for i=1,...,n. The dose budget is sum u_i<=delta. The receiver measures the total terminal current drawn from rail 1 at fixed unit voltage, equivalently effective conductance. It has no internal node probes and is not given the hidden anchor wiring. Actuator labels and allowable conductances are the same in both sources.

The lower bound is about the support of the complete actual added-conductance vector. A fully active reference network with one altered edge is a dense intervention. Off-state leakage would also have to be included in that complete command; the exact zero-support statement is a condition of this ideal circuit class, not an assertion about a particular switch.

## 2. Baseline and literal nodal equations

Let E be the n by n+1 incidence matrix with row i equal to e_i-e_(i-1), and U=diag(u). Kirchhoff's equations for internal potentials x are

    (s I + E^T U E)x = s a.                         (1)

The coefficient matrix is positive definite for every legal command. The actual rail-1 current is

    J(u)=sum_(j=0)^n s a_j(1-x_j).                  (2)

Equivalently it is the minimum electrical dissipation at unit applied voltage:

    J(u)=min_x sum_j[s a_j(x_j-1)^2+s(1-a_j)x_j^2]
                       +sum_i u_i(x_i-x_(i-1))^2.

The anchor terms complete the square as

    s||x-a||^2 + c0,
    c0=sum_j s a_j(1-a_j)=(n-1)s/4=(n-1)/(2kappa).

The two baselines are therefore exactly equal, positive for n>=2. At zero command, x=a, independently confirming (2). No subtraction of a model-dependent hidden baseline is being smuggled into the observable; even the full raw terminal currents agree at baseline.

**Scope correction:** the construction is restricted to n>=2. For n=1 its sole potential difference is 0 versus 1, not a pair of endpoint values of magnitude 1/2. Adding a common parallel rail resistor would make that baseline positive but would not restore the claimed G=1/2 bound. Nothing in the asymptotic result needs n=1.

## 3. Exact response representation

Write y=sqrt(s)(x-a), g=Ea and H=E/sqrt(s). Minimizing the energy gives

    J(u)=c0+min_y [||y||^2+(g+Hy)^T U(g+Hy)]
        =c0+g^T P(I+PBP)^(-1)Pg,
    P=diag(sqrt(u)), B=H H^T=(1/s)E E^T.             (3)

Hence B has diagonal kappa and adjacent offdiagonal entries -kappa/2, with all other entries zero. It is strictly positive definite because the path incidence rows are linearly independent. In particular the original source contract B>=0 and B_ii<=kappa is satisfied.

For source A,

    g_A=(1/2,0,...,0,-1/2),

and for source B,

    g_B=(1/2,0,...,0,1/2).

Thus all interior actuators are exactly dark at baseline, |g_i|<=G=1/2, and the global response scale is L=delta/4. Every negative entry of B is an ordinary incidence inner product; no physical negative resistor or transformer is required.

## 4. All proper-support currents are identical

Let at least one u_i vanish. In the actuator-index path, the corresponding inactive index separates the first and last bright entries into different active components. Multiplying the component containing the last bright entry by -1 changes g_A to g_B while leaving the restricted path matrix B unchanged. This diagonal sign change commutes with P and proves equality in (3).

There is also a direct circuit proof. Removing at least one active-control edge separates the internal node-0 endpoint from the internal node-n endpoint. Reflect all internal potentials x_j to 1-x_j in the component containing node n. Its other nodes have symmetric half-and-half anchors to the two rails. Reflection interchanges the node-n anchor, leaves all dissipation terms in that component unchanged, and changes none of the remaining components. The two minimum dissipations, hence full terminal currents, agree.

Consequently every command with support at most n-1 has exactly the same raw scalar reading in both circuits, at every nonnegative amplitude. Unlimited repetitions, infinite precision, adaptive query choice, and a perfect baseline measurement do not reveal which circuit is present through this restricted interface.

## 5. Dense separation and explicit lower bound

Apply the full equal-dose command u=t*1, t=delta/n. The common shifted matrix I+tB is tridiagonal with diagonal 1+kappa*t and offdiagonal -kappa*t/2. Let D_n be its determinant. Then

    D_0=1, D_1=1+kappa*t,
    D_j=(1+kappa*t)D_(j-1)-(kappa*t/2)^2 D_(j-2).

Its endpoint inverse entry is positive and equals

    [(I+tB)^(-1)]_(1n)=(kappa*t/2)^(n-1)/D_n.

The two endpoint diagonal contributions agree, while the cross contribution reverses sign. Therefore

    Delta_n=J_B(t1)-J_A(t1)
           =4 G^2 (kappa/2)^(n-1) t^n / D_n >0,
    G=1/2.                                         (4)

The original signed-path cofactor mechanism is now realized by entirely passive circuits. Hadamard and positivity give the exact rational bound

    1<=D_n<=(1+kappa*t)^n,
    Delta_n >=(4L/n)[q/(2n)]^(n-1)/(1+q/n)^n,
    q=delta*kappa,

and therefore

    Delta_n >=(4L/n)exp(-q)[q/(2n)]^(n-1).           (5)

For n=2, kappa=delta=1, the circuits have baseline c0=1/2 and dense responses J_A=9/14 and J_B=7/10, giving gap2/35. The checker obtains these values from literal three-internal-node Kirchhoff solves as well as (3)--(4).

## 6. Consequence for actual experiments

Because all lower-order transcripts are identical, no predictor based solely on support-at-most-n-1 experiments can approximate both full terminal-current laws uniformly within error <Delta_n/2. This remains true with bounded adversarial noise, since the common exact transcript is permitted. A randomized predictor cannot attain success probability greater than 1/2 on both disjoint accuracy events.

Holding q,L positive and fixed, (5) has

    log(L/Delta_n)<=n log n+O_q(n).

Thus, over this passive electrical subclass alone, a dimension-uniform reusable law at accuracy epsilon requires simultaneous order

    k >=(1-o(1)) log(L/epsilon)/log log(L/epsilon).

The theorem therefore applies to conventional grounded resistor networks, without assuming arbitrary Gram matrices are physically realizable. It does not lower-bound total measurements, supply current, total computation, or learning precision by the same expression.

## 7. What remains charged

The construction uses n actuator edges and O(n) anchor branches. Its baseline effective conductance/current at unit voltage grows as (n-1)/(2kappa); source power, current capacity, receiver dynamic range and calibration cannot be omitted from a hardware comparison. The gap in (4) becomes extremely small with increasing n at fixed dose, so the result expresses an information boundary, not cheap experimental distinguishability.

The source class assumes stationary linear resistors, calibrated positive conductance commands, settled Kirchhoff response and a scalar terminal receiver. These conditions have not been acquired from laboratory data. A comparator supplied the wiring or internal-voltage sensing has more information and can distinguish the sources cheaply. A conventional scalar-source learner with the same allowed commands and readings obeys exactly the same lower bound and can adopt the root's finite-noise construction.

## 8. Challenge and execution scope

The complementary challenge reconstructed the complete anchor energy, current formula, incidence Gram representation, proper-support circuit reflection, tridiagonal cofactor and asymptotic inversion. It found and corrected the n=1 endpoint-amplitude issue. `check_resistor_network_lower_bound.py` solves the actual full internal-node system using exact rational arithmetic and independently checks the reduced formula and gap. Its finite checks do not prove the all-n statements; the ordinary derivations above do.
