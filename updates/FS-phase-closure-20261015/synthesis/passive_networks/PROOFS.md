# Fixed-task passive-network certificates

Worker derivations, 2026-10-15 Australia/Brisbane. These results apply to the stated finite linear models. Algebraic derivation and executed checks do not establish historical originality, a microscopic liquid response, a realizable nanofluidic specimen, or physical task advantage.

## 1. Arbitrary steady reciprocal network: eliminate every mediator once

Let generalized velocities/flows be v=(x,y,z), where x is the fixed source-service vector, y contains all useful receiver ports, and z all unforced internal coordinates. Use conjugate forces f=Rv, with R real symmetric positive semidefinite. Power entering the full device is v^T Rv; all internal losses are already included there. Assume R_zz is positive definite. Force-free internal coordinates satisfy

    z = -R_zz^-1 (R_zx x + R_zy y).

Completing the square, or substituting this equation, gives the terminal matrix

    R_T = R_TT - R_Tz R_zz^-1 R_zT >= 0.

Thus an arbitrary number of mediator nodes, paths and receiver ports reduces to

    R_T = [ A   -B ] ,     D(x,y)=x^T A x - 2 x^T B y + y^T C y.
          [-B^T  C ]

Assume C>0. Define b=B^T x, S=b^T C^-1 b and

    D0=x^T(A-B C^-1 B^T)x.

Then

    D(x,y)=D0+(y-C^-1 b)^T C (y-C^-1 b),
    P_out=b^T y-y^T C y.

Here P_out=-f_y^T y is total useful receiver power, not an unloaded velocity. There may be multiple receiver tasks; allowing their total power alone is a relaxation if individual flows, pressures, isolation or minimum powers are also specified.

## 2. Exact positive-output loss envelope

For fixed x, S>0 and a required total P in [0,S/4],

    min_{y: P_out=P} D(x,y)
      = D0 + (S/4) [1-sqrt(1-4P/S)]^2.             (1)

The same minimum holds for P_out>=P. For P>S/4 no receiver state can meet the output in this model.

Proof. Whiten the receiver coordinate: u=C^(1/2)y, a=C^(-1/2)b, so ||a||^2=S. The power constraint is

    P_out = S/4 - ||u-a/2||^2.

The dissipation is D0+||u-a||^2. A sphere of radius sqrt(S/4-P) around a/2 is closest to a along their common line. Its nearest point is u=t a, where

    t=[1+sqrt(1-4P/S)]/2 in [1/2,1].

Substitution proves (1). The P_out>=P region is the corresponding ball; a lies outside it except at P=0, so the same nearest point applies. This is Euclidean geometry after whitening, not an invocation of an efficiency formula.

An algebraically attaining load is f_y=-L_load y with

    L_load=(1/t-1) C >= 0.                         (2)

This is a passive coupled load. Its hardware must be physically available and counted. If receivers cannot be cross-connected, C has unsuitable signs, or the load would violate mass isolation, (1) remains a lower bound and (2) is not an acquired implementation. If C is a grounded graph Laplacian, a scaled copy is an ordinary passive friction/resistor graph; its fabrication, volume, contacts and parasitic loss are still real costs.

### Fixed-task loss replacement

Let the matched old source task dissipate x^T R_b x. A necessary and, within the unrestricted terminal model, sufficient condition for lower net source-minus-output power is

    x^T R_b x > D0 + (S/4)[1-sqrt(1-4P/S)]^2.       (3)

For a prescribed fraction theta=4P/S of each task's own maximum output, define

    alpha(theta)=[1-sqrt(1-theta)]^2/4.

Uniform saving over nonzero x in a service subspace x=T a, with T a full-column-rank basis matrix, is equivalent to

    T^T [R_b - (A-B C^-1 B^T) - alpha(theta) B C^-1 B^T] T > 0.  (4)

This matrix test prevents selecting a different favorable service direction after comparing devices. It includes the entire eliminated mediator network and the output penalty.

If an unchanged irreducible old loss term x^T R_b x is still present in the full new network, and every added element contributes nonnegative dissipation, minimizing the additional coordinates cannot reduce that term. Therefore (3) fails. This is conditional on the old loss depending on the task variable actually held fixed. It is not a prohibition on passive impedance matching or geometric drag reduction that changes old dissipative states at the same useful downstream service.

### Recovery of the supplied two-fluid model

For A=c1+k, C=c2+k, b=k u1,

    D0=[c1+k c2/(k+c2)]u1^2,
    S=k^2 u1^2/(k+c2).

At P=0 equation (3) is exactly c_b-c1>k c2/(k+c2). Positive P adds the explicit penalty in (1). Unloaded operation P=0 and maximum-output operation P=S/4 are different endpoints.

An exact arithmetic witness has u1=1, c1=1/2, c2=k=1, old c_b=2, y=2/5, load=1/5. Then P=2/25, source input=11/10, D=51/50<2. A real advantage is permitted **if** the old source loss actually drops from 2 to 1/2 while the new coefficients coexist. Holding c_b=c1=1/2 instead makes the same added converter worse than its baseline. These rational values are a model witness, not material data.

## 3. Coupled pump efficiencies define a different, valid task

Suppose the actual matched task is both the original source flow and useful receiver power P. Let the donor pump have the same measured efficiency eta1 in both cases, an independent receiver pump have efficiency eta2, and candidate auxiliary power be P_aux. The candidate's minimum donor electrical input is (D_min(P)+P)/eta1+P_aux. The separate-pump comparator consumes D_b/eta1+P/eta2, plus any common overhead.

Hence candidate advantage requires

    D_min(P)-D_b < P(eta1/eta2-1)-eta1 P_aux.        (5)

An added passive converter can therefore beat a poor separate receiver pump even if it increases source-minus-output dissipation. That is a replacement of a system conversion loss, not recovery of an unchanged wall-friction loss. If eta1=eta2 and P_aux>=0, a positive excess dissipation cannot win. Real pump efficiencies generally change with pressure/flow and must be measured on the same operating points; equality of eta1 is a stated simplification, not a default physical fact. Equation (5) also assumes the output is the specified useful hydraulic service; leakage, mixing or pressure ripple can invalidate task equivalence.

## 4. Every mediator path inherits ground leakage

For a scalar grounded friction graph, write

    D(v)=sum_i gamma_i v_i^2 + sum_edges k_ij(v_i-v_j)^2,

with gamma_i,k_ij>=0. Its matrix R has nonpositive off-diagonal entries and row sums gamma. After eliminating an internal set I with H=R_II>0, the effective terminal graph has

    k_eff,ij=k_ij+(K_TI H^-1 K_IT)_ij,  i!=j,
    gamma_eff,T=gamma_T+K_TI H^-1 gamma_I,           (6)

where K_TI=-R_TI>=0. The inverse of a grounded graph block is entrywise nonnegative, so all inherited ground leakage in (6) is nonnegative.

Proof of the row-sum identity: R_II 1_I+R_IT 1_T=gamma_I. Therefore

    (R_TT-R_TI H^-1 R_IT)1_T
      =gamma_T-R_TI H^-1 gamma_I.

The off-diagonal identity follows directly from the same Schur complement. A single mediator gives k_eff=lambda1 lambda2/S and gamma_eff,i=gamma_i+lambda_i gamma/S, S=gamma+lambda1+lambda2. Equation (6) is the exact multipath generalization. Hidden mediators do not justify keeping their off-diagonal transmission while discarding their diagonal leakage.

### Parallel paths and a lossy-separator bound

At fixed boundary velocities, the minimum graph dissipation is monotone nondecreasing in each k_ij and gamma_i. This follows because each underlying quadratic term increases pointwise before minimization. Thus adding passive parallel paths cannot reduce fixed-boundary dissipation unless something about the old loss or task changes.

For a source node held at v=1, all other nodes unforced, define

    r_i=sum_j k_ij/(gamma_i+sum_j k_ij)<=1.

The harmonic velocity at node i is the probability of reaching the source before absorption in a substochastic random walk: transition i->j has probability k_ij/(gamma_i+sum k), and the remaining probability is absorption at ground. This follows from the node force balance and the uniqueness of its bounded solution in a grounded connected finite graph.

If every path from a receiver to the source passes through at least m nodes in a set with r_i<=r<1 (counting visits can only add attenuation), then

    0<=v_receiver<=r^m.                            (7)

To prove it, condition on the successive mandatory lossy-node departures. Surviving each costs a factor at most r; all later hitting probabilities are at most one. Parallel path multiplicity does not remove this bound because outgoing transition probabilities already sum to at most r. The condition must be physically maintained as paths/couplings change: if extra paths raise sum k without raising gamma, the original r bound no longer applies. Equation (7) is a DC scalar grounded-graph result, not a general reactive, gyroscopic or quantum-network limit.

## 5. A concrete passive escape: reduce the old mediator's leakage

Consider a source coupled by lambda1 to a mediator, which leaks momentum to ground at gamma. Its original unloaded baseline has receiver absent and loss coefficient

    c_base=c1+lambda1 gamma_b/(lambda1+gamma_b).

Now change the same mediator to leakage gamma_n and attach a receiver through lambda2 with parasitic loss c2. The receiver branch presents g_R=lambda2 c2/(lambda2+c2). Eliminating both mediator and unloaded receiver gives

    c_new,unloaded=c1+lambda1(gamma_n+g_R)/(lambda1+gamma_n+g_R).

With lambda1 held fixed, genuine source-loss saving occurs exactly when

    gamma_n+g_R<gamma_b.                           (8)

This is a coupled, experimentally testable change: lowering the wall's old ground-leakage channel must pay for the receiver branch. Merely adding the receiver at unchanged gamma does not satisfy it. Positive useful output requires applying (1) to the resulting terminal matrix and further reduces the saving. A material change can also change lambda1,lambda2,c1,c2; then the full old/new expressions, not the simplified (8), must be measured. No same-regime material or control satisfying (8) is acquired here.

More generally reduce one internal ground shunt gamma_i by delta, with 0<=delta<=gamma_i and 1-delta(H^-1)_ii>0. The first condition preserves a passive ground shunt; invertibility alone would not license a negative physical leakage. Sherman-Morrison gives the exact terminal change

    R_T,new=R_T,old - [delta/(1-delta(H^-1)_ii)] w w^T,
    w=R_TI H^-1 e_i.                              (9)

The reduction is rank one. It helps a fixed source pattern only through (w^T x)^2. A single altered leakage channel cannot create strict improvement in every direction of a service space of dimension greater than one unless additional controls/changes cover its null directions. Formula (9) is standard rank-one inverse algebra applied to a specific loss-replacement question; historical mathematical novelty is not claimed.

## 6. Frequency dependence: eliminate dynamics before taking dissipation

Let a stable, well-posed linear passive terminal relation be f(omega)=Z(omega)v(omega). Use peak phasors with time dependence exp(i omega t). Then mean net input is

    D=Re(v^* Z v)/2=v^* R v/2,
    R=(Z+Z^*)/2>=0.

Internal force-free ports must first be eliminated with the **complex** Schur complement of Z. Its terminal relation remains passive because unforced internal ports supply no power. In general

    HermitianPart(Schur(Z)) != Schur(HermitianPart(Z)).

Taking real parts first can discard internal damping driven by reactive coupling.

Split source and receiver ports. Hold the possibly complex source waveform x fixed. Define

    C=R_22>0,  b=-Z_21 x,  c=R_21 x,
    D0=[x^* R_11 x-c^* C^-1 c]/2,
    K=(b^* C^-1 b)/4,
    Delta^2=(c+b/2)^* C^-1(c+b/2).

These are real nonnegative scalar quantities where indicated; D0>=0 follows from passivity. With u=C^(1/2)y,

    P_out=Re(y^* b)/2-y^* C y/2
         =K/2-||u-C^-1/2 b/2||^2/2,
    D=D0+||u+C^-1/2 c||^2/2.

Therefore P_max=K/2=b^* C^-1 b/8. For exactly specified P in [0,P_max], the exact algebraic envelope over receiver phasors is

    D_exact(P)=D0+[Delta-sqrt(K-2P)]^2/2.            (10)

For at least P,

    D_atleast(P)=D0+[max(Delta-sqrt(K-2P),0)]^2/2.   (11)

Proof: the power constraint is a sphere, or ball, about C^-1/2 b/2; the dissipation center is -C^-1/2 c. Their separation is Delta. Distance to a sphere is |Delta-radius|; distance to a ball is max(Delta-radius,0). This proof works for arbitrary numbers of source/receiver ports and all hidden network paths already contained in Z.

Equations (10)–(11) are bounds on every physical passive termination. Algebraic optimum phasors do not automatically produce a realizable causal multiport load, acceptable local port signs, amplitudes or fluid isolation. Conjugate reactance cancellation can be feasible at one frequency and fail across a band. Positive-real load synthesis, finite stored energy, actual material bandwidth and all control ports remain obligations. For singular C, these formulas require appropriate range conditions and restriction to its supported space; if b has a component in ker C, the ideal unrestricted-phasor model has no finite output ceiling. Passivity alone then supplies no practical power-density bound.

### Explicit passive counterexample to a naive steady extension

Take Z(s)=I+s M with M=[[2,1],[1,2]]>0. At omega=1,

    Z=[[1+2i, i],[i,1+2i]],  R=I.

It is a reciprocal passive mass/damper network. Its dissipative off-diagonal coupling is zero, but adding a unit real receiver load and holding source peak x=1 gives

    y=(-1-i)/4,
    P_out=1/16,
    P_in=5/8,
    D=9/16.

Thus a q parameter made from R_12 alone would incorrectly predict zero conversion. The unloaded forward and reverse velocity gains are both (-2-i)/5; their product is (3+4i)/25, not a real DC q^2. Eliminating the unloaded receiver from Z gives Re Z_eff=6/5, whereas eliminating it from R gives 1. That extra 1/5 is actual internal damping induced through the reactive channel.

For the same P=1/16, equation (10) gives D_min=1/2+(1/2-1/sqrt(8))^2/2, approximately 0.5107233. At this one frequency it is attained by the ordinary passive scalar load Z_load=(3+2sqrt(2))-2i: a positive damper with compensating spring reactance. This is a mathematical lumped-network realization, not a fabricated stationary-wall liquid device or a new conversion principle. It still dissipates more than the unchanged source baseline 1/2, so reactive coupling does not evade the fixed-task accounting.

## 7. Broadband and finite-time accounting

For mutually orthogonal steady harmonics, apply (11) at every frequency and sum mean powers. Allowing an independently chosen optimal load at every frequency is an optimistic relaxation. A genuine passive LTI load must be one causal positive-real network across the whole band, with finite components, stable interconnection and a countable preparation/reset energy. Therefore an integrated envelope is a necessary bound; equality cannot be granted by selecting unrelated favorable frequency points. Microscopic THz fluctuation frequencies in a DC drag integral are not the frequency of an externally imposed service waveform.

For independent steady real reciprocal task channels described by (1), with capacities S_j, the canonical penalty F(P_j)=S_j[1-sqrt(1-4P_j/S_j)]^2/4 is convex. At fixed total P, the relaxed sum is minimized with the same normalized fraction 4P_j/S_j and equals

    F_total(P)=(sum_j S_j)/4 [1-sqrt(1-4P/sum_j S_j)]^2.  (12)

This follows from Jensen after writing F(P_j)=S_j f(P_j/S_j). It is a relaxation if independently tunable mode loads are unavailable. Multiple channels enlarge measured capacity; they do not eliminate the positive-output penalty.

In time domain, passivity requires the storage balance

    W_source+W_aux-W_receiver = integral D dt + E_final-E_initial.

For a repeatable closed-storage cycle E_final=E_initial. Any apparent output from initial stored energy must count its preparation, and controls/switching/bath changes must enter through W_aux or other declared resource ports. If an unchanged old task-only dissipation term D_old[x(t)] remains, this balance gives net work at least integral D_old dt. No passive network or frequency choice removes that term. If geometry, impedance matching or wall chemistry reduces the actual old loss, that is the physical change to measure rather than a loophole in passivity.
