A common all-fault Lyapunov construction for an open paired-prefix example

Question interface. The complete nominally detailed-balanced compiler return pays exact timed paths and actual faulty tails through H tau, but its general all-time estimate grows as exp(C delta^2 t). The construction here gives an ACTUAL common all-time drift for the uniform paired lift of A<->2A. This is an open, positive-upper-drift case, not the already conservative A=0 case. It is not a theorem for arbitrary networks or variable-order prefixes.

1. The actual elementary paired lift.

Use species A,C,D,S with decoder columns1,1,2,2, initialized (x0,0,0,0). Its raw reactions are
 A -> C at rate a per molecule, C -> A at rate b,
 C -> D at rate p, D -> C at rate q,
 D <-> S at rate c in EACH direction,
 S ->2A at rate d, 2A -> S at rate e.
The central C->D,D->C channels have the two original labels; all other channels are hidden. Thus graph/decoder/zero-auxiliary/nominal balance properties are exactly those in the paired compiler. For the return's uniform source activities,
 a=K theta/U, b=c=d=K,
 p=Q k_+ U, q=Q k_- U^2, e=K theta/U^2,
 Q=theta^(-1).
The prescribed original equilibrium is a_* =k_+/k_-. Fine activities are
 b_A=a_*, b_C=theta a_*/U,
 b_D=b_S=theta a_*^2/U^2.
Every pair is exactly detailed balanced. Divide all raw coefficients by the same H to obtain emitted coefficients at most1. No new controller or irreversible reaction is added.

2. An explicitly solvable absorbing unary problem.

Temporarily treat an original A as an absorbing output of weight1 and an exit2A as an absorbing output of weight2. The transient unary states are C,D,S. Let v_j be the probability of absorption at2A, and h_j the expected time to absorption. The ordinary three-state subgenerator T gives
 T v+exit_to_2A=0, T h=-1.
All entries are positive rational rates. The unique solutions are rational. Put
 L=p c d+b c d+q b d+q b c.
Then
 v_C=p c d/L,
 v_D=c d(p+b)/L,
 v_S=[c d(p+b)+q b d]/L,
 zeta=1-v_S=q b c/L>0.
In particular0<v_C<=v_D<=v_S<1. These are an ordinary finite Markov hitting calculation, not a physical reset or a class sampler.

Let hmax=max_j h_j and eta=zeta/[4(1+hmax)]. Define the FIXED species weights
 w_A=1, w_j=1+v_j+eta h_j, j=C,D,S.
They satisfy1<=w_j<=2-3zeta/4. On each transient unary state, the nominal weighted-population drift is EXACTLY-eta: the harmonic part has zero drift and the hitting-time part has drift-1. This strict interior margin is the useful operation.

3. The same weights control the entire instantaneous fault box.

Let R>=1+a+b+p+q+2c+d+e, and choose
 0<delta<=min(1/2,eta/(2R)).
Every independent predictable multiplier lies in[1-delta,1+delta]. Each unary weight increment has absolute value at most1. Perturbing all outgoing rates therefore changes a transient state's raw drift coefficient by at most delta R<=eta/2. All three auxiliary coefficients remain at most-eta/2, for every instantaneous multiplier vector and hence every history-dependent policy.

The binary binding has increment w_S-2<=-3zeta/4. Its faulty raw contribution is at most
 -beta A(A-1), beta=3e zeta/8.
The unary initiation A->C contributes at most(3a/2)A. Therefore for V=w.Z and n=|Z|_1,
 L_raw V<=(3a/2)A-beta A(A-1)-(eta/2)(C+D+S).
Set c0=min(beta/2,eta/2), and
 B0=[3a/2+beta+c0]^2/(4beta).
Completing the scalar square gives the pointwise, actual bound
 L_raw V<=B0-c0 n.                                          (1)
It includes the ordinary falling-factorial A(A-1), without a mass-action symmetry-factor change. Since n<=V<=2n, the emitted physical generator satisfies
 L V<=B0/H-[c0/(2H)]V.
Localization, the existing elementary nonexplosion argument and Dynkin's formula yield
 sup_(t>=0) E n_t<=n0+2B0/c0.                               (2)
No Markov assumption about the faulty marginal or stationary law of the faulty process is needed: (1) holds conditionally for the entire rate box.

4. Actual supremum population and every firing.

Only S->2A increases fine population, so pathwise sup_(s<=t)n_s<=n0+R_release(t). Its intensity is at most3d n/(2H). Thus
 E sup_(s<=t)(1+n_s)<=1+n0+[3d/(2H)](n0+2B0/c0)t.
The paired lift's exact count identities pay binary assemblies by releases and pending entries. Here there is no zero-source mark. All remaining counts have linear intensities. For example a conservative bound is
 E F_all(t)<=n0+[3(d+a+c+max(p,q))/H](n0+2B0/c0)t.
This counts hidden returns, releases, central labels and every failed binding/rebinding. Both required all-time polynomial forms follow, and at t=H tau the clock cancels. No rare physical trajectory is cut off.

5. The constants are genuinely polynomial for THIS fixed-size open example.

Let rmin=min(1,a,b,p,q,c,d,e)>0. From any transient state, a path of at most three unary jumps reaches A, with probability at least(rmin/R)^3. The expected time per block of three jumps is at most3/rmin. Hence
 hmax<=3R^3/rmin^4,
 zeta^(-1)<=4R^3/rmin^3.
The reciprocals eta^(-1),delta^(-1),beta^(-1),c0^(-1) and the ratios in (2) are fixed polynomials in R and rmin^(-1). Computing h uses only a three-by-three rational linear system, with polynomial bit complexity. The return's emitted rates and inverse rates are already polynomial in charged W, so these constants and the additional accuracy-compatible reduction of delta are polynomial in W. No inverse rare stationary atom, unbounded state enumeration or hidden network-dependent exponent is inserted.

The original process has L n=k_+ n-k_-n(n-1), which has a finite positive rational upper bound, for example(k_++k_-)^2/(4k_-). Thus this is a genuine admitted general-A>0 instance. The already supplied paired finite-horizon path comparison and resource ledger combine with the common drift to give its entire requested contract.

6. What remains for the FULL variable-network problem.

The useful new design principle is to solve a finite unary Dirichlet problem, keep strict weight room below every dangerous binary product sum, and pay independent perturbations from that interior margin. It works here because the three transient unary states have absorbing releases of weights1 and2 and the binding margin stays strictly negative. For arbitrary networks, a unary subsystem can branch, many binary source constraints interact, and a positive common weight vector with an inverse-polynomial margin is NOT supplied. A large finite matrix inverse can itself have an exponentially bad numerical margin; a polynomial bit algorithm is not a uniform polynomial physical bound. Variable-order auxiliary chains also add binary constraints absent in this example. No such universal feasibility, condition bound or full compiler closure is asserted.

Primary/contrary scope. Anderson--Cappelletti--Fan--Kim2309.06970v2 Example2.4 was refreshed: the detailed-balanced0<->A+B,B<->2B network has product-Poisson equilibrium but no positive L2 gap. Corollary3.3's positive result assumes inflow AND outflow of every species, not the exact arbitrary decoder graph here. Therefore no free uniform gap or autonomous equilibrium argument pays the adaptive all-time cost. The new proof above instead uses its explicitly constructed common pointwise drift. No held ACK2019/Anderson--Kim/NSF original, archive or alternate source was opened.
