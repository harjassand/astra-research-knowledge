# A globally strongly convex representative with a direct local formula

Root construction extending the thermal-independent structural branch. The
starting input is the graph-tangent gap proved in
`../../structural_opening/PROOF.md`, not a new acquisition of the earlier
strict-PC certificate. No cheap global evaluator or physical entropy
technology is established.

Let h be the branch's smooth rational normal extension of W_epsilon and let

    h(z)>=h(mA)+Dh(mA):(z-mA)+c|z-mA|²,
    c=min(epsilon/2,delta/8,M/4)>0.

Choose kappa=c/2 and set h0(z)=h(z)-kappa|z|². At every graph point its
tangent has global gap c/2. In particular the graph point A=0 gives
h0(z)>=(c/2)|z|². Therefore conv(h0) is globally finite. The function

    G(z)=conv(h0)(z)+kappa|z|²

is globally c-strongly convex in the ordinary Euclidean five-minor
coordinates. The stable-tangent lemma applies to h0 at every graph point,
so G equals h on an open neighborhood of the entire graph. Thus it is
smooth there, and its graph restriction is exactly W_epsilon. This is
stronger than merely giving a globally convex extension smooth near the
graph. It does not make W_epsilon convex as a function of matrix entries.
The nonlinear minors interface is essential.

## Explicit uniform tube on a bounded part of the graph

Here are finite rational bounds permitting direct evaluation of h inside
a certified neighborhood, without evaluating any convex envelope. They
are deliberately conservative and must not be described as practically
well conditioned.

Let C be the ordinary coefficient-l1 norm of the quartic F and P the same
norm of p6. For k=p6/(T+sigma)², literal product differentiation gives

    |k|<=P|A|², |Dk|<=10P|A|,
    ||D²k||<=106P,
    ||D³k||<=1248P/sqrt(sigma).

For completeness, the D² coefficients are 30,52,24 multiplying
P r^4/(r²+sigma)², P r^6/(r²+sigma)³ and
P r^8/(r²+sigma)^4. Each ratio is <=1. The D³ coefficients are
120,432,504,192 multiplying P r^(2j-1)/(r²+sigma)^j for j=2,3,4,5.
Each ratio is <=1/sqrt(sigma): put t=r/sqrt(sigma) and bound
t^(2j-1)<=(1+t²)^j. These are operator multilinear bounds, following
||D^j p6||<=6!/(6-j)! P r^(6-j).

Fix |A0|<=R and a unit five-dimensional ball around m(A0). On this ball
put b=R+1, D=R+3/2 and U=R+2. Then |B|<=b,
|s-q(B)|<=D, ||D(s-q(B))||<=U and ||D²(s-q(B))||=1.
Choose rational K3>=1248P/sqrt(sigma), and put K2=106P,
K1=10Pb, K0=Pb². Product differentiation of h gives the bounds

    H2=12Cb²+2epsilon+D K2+2K1 U+K0+2M(U²+D),
    H3=24Cb+D K3+3K2 U+3K1+6M U.

They bound its Hessian norm and third derivative norm throughout that
unit ball. Subtracting kappa|z|² changes H2 by at most c and leaves H3.
The graph Hessian of h0 is at least cI. Define

    K=H2+c, r=min(1/2,c/(4H3)),
    rho=min(r/4,c r/(16K)).

On B(mA0,2r), its Hessian is at least cI/2. The stable-tangent estimate
with old global gap c/2 shows every point y with |y-mA0|<rho has a
globally supporting tangent. Hence conv(h0)=h0 and G=h there. The same
rho works for all |A0|<=R. Exact arithmetic verifies the constants in
`EXACT_CONSTRUCTION.json` for epsilon=1/100 and R=1,10,100.

The guaranteed radius at R=1 is only about 1.736e-41. This is a useful
negative practical finding about this conservative proof: existence and
direct evaluation on a mathematically explicit neighborhood do not yet
provide a robust numerical entropy interface. Sharper local certificates
or a differently conditioned construction would be needed for that use.
Increasing numerical precision alone is not a claimed technological gain.

## Independent replay and review boundary

Root reconstructed F and p6 from literal rational coefficients, without
importing producer functions. The exact l1 norms are
C=2535570311/2500000000 and P=1976430361/156250000. The independent
finite stencil yields the same relative quartic approximation floor

    23251991479965369/335009162080000000000 > 0.

The script verifies this algebra and all displayed example constants.
The analytic stable-tangent and weighted-blowup arguments require the
separate whole-proof review; finite algebra alone does not establish them.
The strong-convex extension and tube above are root-authored and have not
been independently audited by a second context at the time of writing.
